"""The Thaqalayn API as a source of record.

    thaqalayn-api.net  ──fetch──>  00-sources/api/<book>.jsonl  ──>  pages ──> passages
                                          + api/manifest.json          (one per hadith)

Three things make this different from every other source in the project, and
all three are handled here rather than left to the caller:

1. **There is no page number, and there never will be.** A record carries the
   work, the volume, the category, the chapter and the hadith's own number.
   That is the citation of record. Every edition ingested this way is stamped
   ``pagination: api-record`` so nothing downstream can print a page.

2. **The upstream is mutable.** thaqalayn.net is re-scraped weekly, so "the
   API said so" is not a citation — a snapshot is. Every book is pinned by
   SHA-256 in ``00-sources/api/manifest.json`` at fetch time, and
   ``--check`` reports drift without writing.

3. **The Arabic is real text**, not the positioned glyphs the PDF corpus
   extracts. It is still measured rather than assumed: the same
   ``glyph_damage_ratio`` gate runs over it in build_source_corpus.py.

One record in, one passage out. No block splitting, no sentence joining, no
speaker inference — the API already carries the divisions the work itself
prints, so guessing at more would only add something a reviewer has to check.
"""

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from . import config
from .arabic import arabic_char_count, has_broken_glyphs, normalize_arabic
from .pages import Page
from .passages import Passage

BASE = "https://www.thaqalayn-api.net/api/v2"
USER_AGENT = "noorpost-source-pipeline/1.0 (+https://github.com/zakijariwala/noorpost)"

# Fields kept from an API record. `_id` is a MongoDB object id that changes on
# every re-scrape, so keeping it would make every snapshot differ from the last
# for no reason. Everything else is kept verbatim, including the gradings and
# the matn/sanad split, because dropping a field is a decision a later reader
# cannot undo.
DROP_FIELDS = ("_id",)

# Upstream leaves editorial placeholders in `arabicText` where the Arabic has
# not been keyed in yet — twelve of them across the corpus on 2026-08-24.
# Stored as-is in the snapshot (the snapshot is the upstream, verbatim), but
# never promoted to arabic_raw: a field reading "To be added" is an absence, and
# an absence that looks like content is exactly what gets typeset by mistake.
ARABIC_PLACEHOLDERS = {"-", "s", "* * * * *", "notfound", "arabicnotfound",
                       "to be added", "arabictoadd", "n/a", "none"}
ARABIC_RANGE = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")


def real_arabic(value):
    """The Arabic of a record, or None. Anything carrying no Arabic script at
    all is an absence however it is spelled."""
    text = (value or "").strip()
    if not text or text.lower() in ARABIC_PLACEHOLDERS:
        return None
    if not ARABIC_RANGE.search(text):
        return None
    return text


class ApiError(Exception):
    pass


# --------------------------------------------------------------------------
# fetching
# --------------------------------------------------------------------------

def _get(path, timeout=180, retries=3):
    url = "%s/%s" % (BASE, path.lstrip("/"))
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise ApiError("GET %s failed after %d attempts: %s" % (url, retries, last))


def list_books():
    """Every book the API advertises, with its translator and id range."""
    books = _get("allbooks")
    if not isinstance(books, list):
        raise ApiError("allbooks did not return a list: %r" % (books,))
    return books


def fetch_book(book_id):
    """Every record in one book, in id order.

    A book advertised in allbooks can still come back empty — Kamal al-Din did
    on 2026-08-24, 659 records advertised and none served. That is a fact about
    the upstream scrape and is reported, never smoothed over.
    """
    records = _get(urllib.parse.quote(book_id))
    if isinstance(records, dict) and records.get("error"):
        raise ApiError("%s: %s" % (book_id, records["error"]))
    if not isinstance(records, list):
        raise ApiError("%s: expected a list, got %r" % (book_id, type(records).__name__))
    records = [{k: v for k, v in r.items() if k not in DROP_FIELDS} for r in records]
    records.sort(key=lambda r: r.get("id", 0))
    return records


# --------------------------------------------------------------------------
# the snapshot on disk
# --------------------------------------------------------------------------

def snapshot_path(book_id):
    return os.path.join(config.API, "%s.jsonl" % book_id)


def render_jsonl(records):
    """Deterministic: sorted keys, LF, one record per line. Two fetches of an
    unchanged book produce byte-identical files, which is what makes the hash
    mean something."""
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_snapshot(book_id, records):
    os.makedirs(config.API, exist_ok=True)
    body = render_jsonl(records)
    path = snapshot_path(book_id)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    return path, sha256_text(body)


def read_snapshot(book_id):
    path = snapshot_path(book_id)
    if not os.path.exists(path):
        raise ApiError("no snapshot for %s — run tools/fetch_thaqalayn.py" % book_id)
    with open(path, encoding="utf-8") as f:
        body = f.read()
    # split("\n"), never splitlines(): some records carry U+2028/U+2029, which
    # json.dumps does not escape and splitlines() treats as a line break — that
    # cuts a record in half and the read fails on a half-decoded line.
    records = [json.loads(line) for line in body.split("\n") if line.strip()]
    return records, sha256_text(body)


def load_manifest():
    if not os.path.exists(config.API_MANIFEST):
        return {"source": BASE, "books": {}}
    with open(config.API_MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest):
    os.makedirs(config.API, exist_ok=True)
    with open(config.API_MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


# --------------------------------------------------------------------------
# records -> pages -> passages
# --------------------------------------------------------------------------

def record_text(rec):
    """The English of one record, with the divisions the source itself prints.

    Nothing is reworded. The heading lines are the API's own `category` and
    `chapter` strings, which are the book's own division names.
    """
    parts = []
    cat = (rec.get("category") or "").strip()
    chap = (rec.get("chapter") or "").strip()
    if cat:
        parts.append("## " + cat)
    if chap and chap != cat:
        parts.append("### " + chap)
    en = (rec.get("englishText") or "").strip()
    if en:
        parts.append(en)
    return "\n\n".join(parts)


_PRINTED_NO = re.compile(r"^\s*\[?(\d+)\s*[\]\-ـ.–—)]")
_ENGLISH_NO = re.compile(r"^\s*(?:Hadith\s*\.?\s*)?(\d+)\s*[\-.–—)]", re.I)


def printed_number(rec):
    """The number the book itself prints on this report, or None.

    Not the API's ``id``. That is a running row count across the snapshot and
    no edition prints it: Man La Yahduruh al-Faqih vol. 2 record 624 is the
    book's hadith 2320. The Arabic carries the book's own number first; the
    English is the fallback where the Arabic has none.
    """
    for text, pat in ((rec.get("arabicText"), _PRINTED_NO),
                      (rec.get("englishText"), _ENGLISH_NO)):
        m = pat.match(text or "")
        if m:
            return int(m.group(1))
    return None


def _chapter_position(rec):
    """Position inside its chapter, from the record's own thaqalayn.net URL
    (``/hadith/<book>/<category>/<chapter>/<n>``)."""
    tail = (rec.get("URL") or "").rstrip("/").rsplit("/", 1)[-1]
    return int(tail) if tail.isdigit() else None


def internal_ref(rec, unique_numbers=True):
    """The citation of record for this corpus. Never a page, and never the
    API's row id.

    Volume matters: al-Kafi restarts in every volume. And where a book restarts
    its numbering in every chapter, as al-Kafi does, the number alone points at
    hundreds of reports, so the chapter is named. ``unique_numbers`` says
    whether the printed number is unique across this record's volume —
    `internal_refs` works that out over the whole snapshot.
    """
    vol = rec.get("volume")
    prefix = ("vol. %s, " % vol
              if vol not in (None, "", 1) or _is_multivolume(rec) else "")
    n = printed_number(rec)
    if n is not None and unique_numbers:
        return "%shadith %s" % (prefix, n)
    where = ", ".join(x for x in ((rec.get("category") or "").strip(),
                                  (rec.get("chapter") or "").strip()) if x)
    if n is None:
        n = _chapter_position(rec)
    return "%s%s, hadith %s" % (prefix, where, n)


def internal_refs(records):
    """`internal_ref` for every record, keyed by API id, with uniqueness
    decided per volume — Faqih numbers straight through, al-Kafi does not."""
    seen = {}
    for rec in records:
        n = printed_number(rec)
        if n is not None:
            key = (rec.get("bookId"), rec.get("volume"))
            seen.setdefault(key, []).append(n)
    unique = {k for k, ns in seen.items() if len(ns) == len(set(ns))}
    refs = {rec.get("id"): internal_ref(
                rec, (rec.get("bookId"), rec.get("volume")) in unique)
            for rec in records}
    # Some books repeat a chapter title, or restart numbering inside a part,
    # so book + chapter + number can still name two reports. A citation that
    # points at two reports points at neither: those carry the record's own
    # thaqalayn.net path, which is unique.
    counts = {}
    for ref in refs.values():
        counts[ref] = counts.get(ref, 0) + 1
    for rec in records:
        rid = rec.get("id")
        if counts[refs[rid]] > 1:
            path = urllib.parse.urlparse(rec.get("URL") or "").path.strip("/")
            refs[rid] = "%s (thaqalayn.net/%s)" % (refs[rid], path or "record %s" % rid)
    # Upstream occasionally splits one long report over several records that
    # share a URL (Faqih vol. 4, hadith 5762). Name the part.
    counts = {}
    for ref in refs.values():
        counts[ref] = counts.get(ref, 0) + 1
    for rec in records:
        rid = rec.get("id")
        if counts[refs[rid]] > 1:
            refs[rid] = "%s, record %s" % (refs[rid], rid)
    return refs


def _is_multivolume(rec):
    return "-Volume-" in (rec.get("bookId") or "")


def pages_from_records(records):
    """One record, one page. ``pdf_page`` is the record's API id — a storage
    key, not a sheet in a PDF and not the book's own hadith number (that is
    `printed_number`, and it is what `internal_ref` cites). The edition is
    stamped ``pagination: api-record`` so that distinction is enforced
    downstream and not left to whoever reads the number."""
    out = []
    for rec in records:
        text = record_text(rec)
        if not text.strip():
            continue
        out.append(Page(rec.get("id"), text, extraction_method="native_text"))
    return out


def passages_from_records(source_id, records, extraction_status="api-snapshot"):
    """One record, one passage. Deliberately not run through
    passages.segment(): the API already carries the work's own divisions, so
    re-splitting on blank lines would cut a report in half and re-detecting a
    speaker would invent a field the record already states or leaves blank."""
    out = []
    refs = internal_refs(records)
    for ordinal, rec in enumerate(records, 1):
        english = (rec.get("englishText") or "").strip()
        if not english:
            continue
        arabic = real_arabic(rec.get("arabicText"))
        page_no = rec.get("id")
        damaged = has_broken_glyphs(english)
        out.append(Passage(
            passage_id="%s-%04d-%03d" % (source_id, page_no or 0, 1),
            source_id=source_id,
            pdf_page_start=page_no, pdf_page_end=page_no,
            printed_page_start=None, printed_page_end=None,
            ordinal=1,
            section=(rec.get("category") or None),
            chapter=(rec.get("chapter") or None),
            title=None,
            speaker=None,
            subject=None,
            passage_type="hadith",
            internal_ref=refs[rec.get("id")],
            metadata_source="thaqalayn-api",
            register="english",
            arabic_raw=arabic,
            arabic_normalized=normalize_arabic(arabic) if arabic else None,
            english=english,
            text=english,
            arabic_char_count=arabic_char_count(arabic or ""),
            # The Arabic here is real Unicode, not the positioned glyphs the
            # PDF corpus extracts — but "not obviously broken" is not "checked
            # against the page", so it starts unverified like every other
            # Arabic in this project.
            arabic_verified=(0 if arabic else None),
            extraction_method="native_text",
            extraction_status=extraction_status,
            quotation_ready=0 if damaged else 1,
            char_count=len(english),
        ))
    return out

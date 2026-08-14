#!/usr/bin/env python3
"""
Read 00-foundations/citation-sheet.md into claims.yaml and citations.yaml.

    python tools/import_citation_sheet.py            # parse, resolve, write
    python tools/import_citation_sheet.py --dry-run  # show what it would write
    python tools/import_citation_sheet.py --no-resolve

The citation sheet is the project's existing record and stays the thing a human
edits. This turns its tables into records a machine can check, without changing
a word of it. The file is opened read-only; it is never written to by this tool.

What "resolve" means: where a row quotes a saying, the quote is looked up in
source.db. If it is found in exactly one passage of the cited edition, the
citation gains a passage_id and a page. That is a *location*, not a
verification — it says the words are on that page, not that the claim is true,
and it never changes a claim's status. TV becomes V only by a human act.

claim_id is derived from (env, item, claim text), so a row keeps its id when
rows are added above it.
"""

import argparse
import hashlib
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, db, metadata

SHEET = os.path.join(config.ROOT, "00-foundations", "citation-sheet.md")

EMPTY = {"", "—", "-", "–", "*to fill*", "*to fix*", "to fill", "n/a"}
REFERENCE_TABLES = {"Status codes", "How to fill a row"}

NO_SOURCE = {"needs a shia source", "non-islamic secondary source", "see `death-lines.md`"}

# Header signatures this tool understands. Anything else is left alone and
# reported, so a table cannot be dropped silently.
SHAPES = {
    ("env", "item", "claim", "work", "ref", "translator", "status", "note"): "claim_row",
    ("env", "seg", "masoom", "saying", "work", "ref", "status"): "hadith_row",
    ("env", "woman", "the act to source", "status"): "woman_row",
    ("entry", "points to", "status"): "blocked_row",
    ("envelope", "ah (death)", "ce (approx)", "checked twice"): "ahce_row",
}

STATUS_MAP = {
    "V": "V", "TV": "TV", "TRAD": "TRAD", "CONT": "CONT", "CUT": "CUT",
    "BLOCKED — NO SOURCE": "needs-review", "BLOCKED — NO RULE": "needs-review",
}


def clean(cell):
    """Strip markdown emphasis for comparison purposes. The original text is
    kept verbatim in the record — this is only used for matching."""
    s = (cell or "").strip().replace("**", "")
    s = re.sub(r"^\*+|\*+$", "", s).strip()
    return s


def is_empty(cell):
    return clean(cell).lower() in EMPTY


def norm_status(cell):
    s = clean(cell).replace("**", "").strip()
    up = s.upper()
    for k, v in STATUS_MAP.items():
        if up.startswith(k):
            return v
    return "needs-review"


def claim_id(env, item, text):
    h = hashlib.sha256(("%s|%s|%s" % (env, item, text)).encode("utf-8")).hexdigest()[:8]
    return "CLM-%s-%s" % (env or "GEN", h)


def citation_id(cid, source_id, ref):
    h = hashlib.sha256(("%s|%s|%s" % (cid, source_id, ref)).encode("utf-8")).hexdigest()[:8]
    return "CIT-%s" % h


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator(cells):
    return all(re.fullmatch(r":?-{2,}:?", c.strip() or "") for c in cells if c.strip() != "")


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

def parse_sheet(path):
    """-> (claims, rows_for_citations, skipped_tables)"""
    claims, cites, skipped = [], [], []
    heading = None
    shape = None
    ncols = None

    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            shape, ncols = None, None
            continue
        if not line.startswith("|"):
            continue

        cells = split_row(line)
        if is_separator(cells):
            continue

        sig = tuple(c.strip().lower() for c in cells)
        if sig in SHAPES:
            shape, ncols = SHAPES[sig], len(cells)
            continue
        if shape is None:
            # "Status codes" and "How to fill a row" are the sheet's own
            # documentation, not rows of claims.
            if len(cells) >= 2 and heading and heading not in REFERENCE_TABLES:
                skipped.append((heading, sig))
            continue
        if len(cells) != ncols:
            continue

        rec = ROW_PARSERS[shape](cells, heading)
        if rec:
            claim, cite = rec
            claims.append(claim)
            if cite:
                cites.append(cite)

    seen = set()
    deduped = []
    for c in claims:
        if c["claim_id"] in seen:
            continue
        seen.add(c["claim_id"])
        deduped.append(c)
    return deduped, cites, sorted(set(skipped))


def _base(env, item, text, status, heading, notes=None, work=None, ref=None, translator=None):
    env = clean(env).replace("—", "").strip() or None
    cid = claim_id(env, item, text)
    return {
        "claim_id": cid,
        "project_location": "00-foundations/citation-sheet.md § %s" % (heading or "?"),
        "env": env,
        "item": item,
        "claim_text": text,
        "status": status,
        "work_hint": work,
        "ref_hint": ref,
        "translator_hint": translator,
        "notes": notes or None,
        "created_from": "citation-sheet.md",
    }


def claim_row(cells, heading):
    env, item, cl, work, ref, translator, status, note = cells[:8]
    if is_empty(cl):
        return None
    c = _base(env, clean(item), clean(cl), norm_status(status), heading, note.strip() or None,
              clean(work) or None, clean(ref) or None, clean(translator) or None)
    return c, _citation_stub(c, work, ref, translator, quote=None)


def hadith_row(cells, heading):
    env, seg, masoom, saying, work, ref, status = cells[:7]
    if is_empty(saying):
        saying_text = "hadith card for %s — no saying selected" % clean(masoom)
        c = _base(env, "hadith card", saying_text, norm_status(status), heading,
                  "segment %s. %s" % (clean(seg), clean(status)))
        return c, None
    quote = clean(saying)
    c = _base(env, "hadith card", quote, norm_status(status), heading,
              "segment %s, %s" % (clean(seg), clean(masoom)),
              clean(work) or None, clean(ref) or None)
    return c, _citation_stub(c, work, ref, None, quote=quote)


def woman_row(cells, heading):
    env, woman, act, status = cells[:4]
    if is_empty(act):
        act_text = "the documented act for %s — not yet chosen" % clean(woman)
    else:
        act_text = clean(act)
    c = _base(env, "woman slot", act_text, norm_status(status), heading, clean(woman))
    return c, None


def blocked_row(cells, heading):
    entry, points, status = cells[:3]
    c = _base(None, "companion hadith card", "hadith card for %s" % clean(entry),
              norm_status(status), heading,
              "points to %s. %s" % (clean(points), clean(status)))
    return c, None


def ahce_row(cells, heading):
    env, ah, ce, _checked = cells[:4]
    if is_empty(ah) or is_empty(ce):
        return None
    c = _base(env, "panel", "AH %s converts to about %s CE" % (clean(ah), clean(ce)),
              "TV", heading, "AH→CE conversion. Check against a converter, not the formula.")
    return c, None


ROW_PARSERS = {
    "claim_row": claim_row, "hadith_row": hadith_row, "woman_row": woman_row,
    "blocked_row": blocked_row, "ahce_row": ahce_row,
}


def _citation_stub(claim, work, ref, translator, quote):
    work_c, ref_c = clean(work), clean(ref)
    if is_empty(work_c) or work_c.lower() in NO_SOURCE:
        return None
    if is_empty(ref_c) and not quote:
        return None
    return {
        "claim_id": claim["claim_id"],
        "work_text": work_c,
        "ref": ref_c or None,
        "translator": clean(translator) or None,
        "quote": quote,
        "verified": 1 if claim["status"] == "V" else 0,
    }


# --------------------------------------------------------------------------
# turning a work name into a source_id, and a quote into a page
# --------------------------------------------------------------------------

PAGE_RE = re.compile(r"\bpp?\.\s*(\d+)(?:\s*[–\-]\s*(\d+))?")


def resolve_source(work_text, aliases):
    key = work_text.lower().strip()
    if key in aliases:
        return aliases[key]
    # "Uyun Akhbar al-Rida, vol. 2" -> the vol. 2 edition
    m = re.match(r"(.*?),?\s*vol(?:ume)?\.?\s*(\d+)", key)
    if m:
        base, vol = m.group(1).strip(), m.group(2)
        for alias, sid in aliases.items():
            if alias.startswith(base) and alias.rstrip(".").endswith(vol):
                return sid
        base_sid = aliases.get(base)
        if base_sid:
            return base_sid[:-3] + "%03d" % int(vol)
    for alias, sid in sorted(aliases.items(), key=lambda kv: -len(kv[0])):
        if len(alias) > 6 and alias in key:
            return sid
    return None


def citation_type_for(edition, ref):
    if ref and PAGE_RE.search(ref):
        return "page"
    unit = (edition or {}).get("citation_unit")
    return unit if unit in config.CITATION_TYPES and unit != "none" else "internal-number"


def fold(text):
    """Comparison form. NFKC turns the ﬁ and ﬂ ligatures these PDFs are full of
    back into plain letters; curly quotes and whitespace are levelled. Used
    only for matching — nothing folded is ever stored."""
    s = unicodedata.normalize("NFKC", text or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


_PASSAGE_CACHE = {}


REF_NUM = re.compile(r"\bno\.\s*(\d+)|\bentry\s*(\d+)", re.I)


def resolve_quote(con, source_id, quote, ref=None):
    """Find the one passage holding this quote. Returns (passage_id, page) or
    (None, None) when it is absent or ambiguous. Never guesses.

    Where a quote appears more than once — Tuhaf al-Uqul carries some sayings
    twice — the row's own number breaks the tie. Only the source's number does;
    nothing is picked by position or by which came first.
    """
    if not quote or con is None:
        return None, None
    text = re.sub(r"^[“\"']+|[”\"'…\s]+$", "", quote).strip()
    text = re.split(r"[…]", text)[0].strip()
    if len(text) < 20:
        return None, None
    probe = fold(text)[:80]

    if source_id not in _PASSAGE_CACHE:
        _PASSAGE_CACHE[source_id] = [
            (r["passage_id"], r["pdf_page_start"], fold(r["text"]), r["internal_ref"])
            for r in con.execute("SELECT passage_id, pdf_page_start, text, internal_ref "
                                 "FROM passages WHERE source_id = ?", (source_id,))]

    hits = [(pid, pg, iref) for pid, pg, t, iref in _PASSAGE_CACHE[source_id] if probe in t]
    if len(hits) > 1 and ref:
        m = REF_NUM.search(ref)
        if m:
            want = m.group(1) or m.group(2)
            narrowed = [h for h in hits if h[2] and REF_NUM.search(h[2])
                        and (REF_NUM.search(h[2]).group(1) or
                             REF_NUM.search(h[2]).group(2)) == want]
            if len(narrowed) == 1:
                hits = narrowed
    return (hits[0][0], hits[0][1]) if len(hits) == 1 else (None, None)


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", default=SHEET)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-resolve", action="store_true")
    args = ap.parse_args()

    claims, stubs, skipped = parse_sheet(args.sheet)
    _, editions, by_id = metadata.load_sources()
    aliases = metadata.alias_map(editions)

    con = None
    if not args.no_resolve and os.path.exists(config.DB):
        con = db.connect(readonly=True)

    citations, unresolved = [], []
    for s in stubs:
        sid = resolve_source(s["work_text"], aliases)
        if sid is None:
            unresolved.append((s["claim_id"], s["work_text"]))
            continue
        ed = by_id.get(sid)
        ref = s["ref"]
        page_start = page_end = None
        m = PAGE_RE.search(ref or "")
        if m:
            page_start = int(m.group(1))
            page_end = int(m.group(2)) if m.group(2) else page_start

        passage_id, found_page = resolve_quote(con, sid, s["quote"], ref)
        note = None
        if passage_id:
            note = ("passage located by exact quote match in source.db — this is a location, "
                    "not a verification")
            if page_start is None:
                page_start = page_end = found_page

        citations.append({
            "citation_id": citation_id(s["claim_id"], sid, ref or (s["quote"] or "")[:40]),
            "claim_id": s["claim_id"],
            "source_id": sid,
            "passage_id": passage_id,
            "ref": ref,
            "citation_type": citation_type_for(ed, ref),
            "page_start": page_start,
            "page_end": page_end,
            "quote": s["quote"],
            "translator": s["translator"] or (ed or {}).get("translator"),
            "verified": s["verified"],
            "notes": note,
        })

    by_status = {}
    for c in claims:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1

    print("parsed %s" % os.path.relpath(args.sheet, config.ROOT))
    print("  claims     %d   (%s)" % (len(claims), ", ".join(
        "%s %d" % (k, v) for k, v in sorted(by_status.items()))))
    print("  citations  %d   (%d located to a passage by quote match)"
          % (len(citations), sum(1 for c in citations if c["passage_id"])))
    if unresolved:
        print("  work names with no edition in sources.yaml:")
        for cid, work in unresolved:
            print("    %s  %r" % (cid, work))
    if skipped:
        print("  tables not imported (no parser for their shape):")
        for heading, sig in skipped:
            print("    § %s  %s" % (heading, " | ".join(sig[:4])))

    if args.dry_run:
        for c in claims[:8]:
            print("   %s  [%s]  %s" % (c["claim_id"], c["status"], c["claim_text"][:70]))
        return 0

    metadata.dump_yaml(config.CLAIMS_YAML, {"claims": claims}, header=(
        "# Claims — one record per claim that reaches print.\n"
        "#\n"
        "# Generated from 00-foundations/citation-sheet.md by\n"
        "# tools/import_citation_sheet.py. The sheet stays the thing a human edits;\n"
        "# re-run the importer after editing it. claim_id is a hash of\n"
        "# (env, item, claim text) so ids survive rows being added above them.\n"
        "#\n"
        "# status: TV | V | TRAD | CONT | CUT | rejected | needs-review\n"
        "# Nothing prints on TV. TV becomes V only when a human has opened the fixed\n"
        "# edition at the named page — no tool in this repository may do it."))
    metadata.dump_yaml(config.CITATIONS_YAML, {"citations": citations}, header=(
        "# Citations — one record per claim-to-source link.\n"
        "#\n"
        "# Generated by tools/import_citation_sheet.py. A citation names an EDITION\n"
        "# (source_id) and a number: a page where the edition's pagination is the\n"
        "# printed one, otherwise the work's own internal numbering, which is stable\n"
        "# across editions. A citation with neither is not a citation.\n"
        "#\n"
        "# passage_id, where present, was located by matching the quoted text against\n"
        "# source.db. It records where the words are, not that the claim is verified."))
    print("\nwrote %s" % os.path.relpath(config.CLAIMS_YAML, config.ROOT))
    print("wrote %s" % os.path.relpath(config.CITATIONS_YAML, config.ROOT))
    print("\nNow: python tools/build_source_corpus.py --validate-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())

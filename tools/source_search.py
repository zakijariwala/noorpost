#!/usr/bin/env python3
"""
Find evidence for a claim. The primary interface for a coding agent.

    python tools/source_search.py "Yahya ibn Aktham"
    python tools/source_search.py --source SRC-IRS-001 --query "Yahya ibn Aktham"
    python tools/source_search.py --claim "Muhammad was known as al-Amin"
    python tools/source_search.py --claim CLM-03-7f3a1c92
    python tools/source_search.py "Shurayh" --json
    python tools/source_search.py --speaker "Imam Ali" --type saying --limit 5
    python tools/source_search.py --passage SRC-TAU-001-0142-002
    python tools/source_search.py --page SRC-TAU-001:142

What comes back always carries its provenance: which edition, which page,
which passage, how the text was extracted, and whether that edition's page
numbers may be cited at all.

Three things this will not do:

  * search anything outside 00-sources/. Draft letters, envelopes, zines and
    READMEs are not evidence, and indexing them would let a draft prove itself.
  * return a passage from a rejected source.
  * write a citation. It hands over the pieces; a human confirms and records
    it. An LLM cannot create a citation.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, db
from sourcelib.arabic import normalize_arabic

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "by", "for", "from", "had", "has",
    "have", "he", "her", "him", "his", "in", "is", "it", "its", "of", "on", "or", "she", "that",
    "the", "their", "them", "they", "this", "to", "was", "were", "when", "which", "who",
    "with", "about", "into", "out", "up", "down", "over", "under", "than", "then", "there",
}

SEARCH_COLUMNS = ("text", "english", "arabic_raw", "arabic_normalized",
                  "speaker", "subject", "chapter", "section", "title", "internal_ref")


# --------------------------------------------------------------------------
# query building
# --------------------------------------------------------------------------

def quote_token(tok):
    return '"%s"' % tok.replace('"', '""')


def build_match(query, exact=False, columns=None):
    """A plain string -> an FTS5 MATCH expression.

    Quoted so that a name with an apostrophe or a hyphen in it cannot be read
    as FTS syntax. --exact makes it a phrase, which is what an exact-name
    search wants.
    """
    query = query.strip()
    if not query:
        raise SystemExit("empty query")

    phrases = re.findall(r'"([^"]+)"', query)
    rest = re.sub(r'"[^"]*"', " ", query)
    tokens = [t for t in re.findall(r"[^\s]+", rest) if t]

    if exact and not phrases:
        expr = quote_token(query)
    else:
        parts = [quote_token(p) for p in phrases]
        parts += [quote_token(t) for t in tokens]
        expr = " AND ".join(parts) if parts else quote_token(query)

    if columns:
        expr = " OR ".join("%s : (%s)" % (c, expr) for c in columns)
    return expr


def claim_to_query(text):
    """A claim sentence -> the terms worth searching for, ORed.

    Every content word is kept, not just the capitalised ones: "al-Amin" and
    "al-Kadhim" are the most distinctive terms a claim about them can carry and
    they do not start with a capital. FTS5's bm25 ranks rare terms above common
    ones, so a passage matching "Amin" outranks one matching only "Makkah".

    A hyphenated or apostrophised term is quoted whole, which makes it a phrase
    — "al-Amin" matches al followed by Amin, not either alone.
    """
    words = re.findall(r"[\w'’\-]+", text)
    keep = []
    for w in words:
        lw = w.lower().strip("'’-")
        if not lw or lw in STOPWORDS or len(lw) < 3:
            continue
        keep.append(w.strip("'’-"))
    if not keep:
        keep = [text]
    return " OR ".join(quote_token(w) for w in dict.fromkeys(keep))


# --------------------------------------------------------------------------
# result shaping
# --------------------------------------------------------------------------

def edition_map(con):
    return {r["source_id"]: dict(r) for r in con.execute("SELECT * FROM v_editions")}


def locator(ed, row):
    """How this passage may be pointed at, and whether a page number is one of
    the ways. Never invents a printed page."""
    pagination = ed.get("pagination")
    out = {
        "pdf_page_start": row["pdf_page_start"],
        "pdf_page_end": row["pdf_page_end"],
        "printed_page_start": row["printed_page_start"],
        "printed_page_end": row["printed_page_end"],
        "internal_ref": row["internal_ref"],
        "section": row["section"],
        "pagination": pagination,
        "page_citable": pagination == "printed",
    }
    warning = config.PAGINATION_WARNING.get(pagination)
    if warning:
        out["pagination_warning"] = warning
    return out


def citation_string(ed, row):
    """The citation as it would be written, or a statement of what is missing.

    This assembles what the database holds. It does not decide that a claim is
    verified — that is a human act, recorded in claims.yaml.
    """
    bits = [ed.get("work") or ed["source_id"]]
    if ed.get("volume_title"):
        bits.append(ed["volume_title"])
    if row["internal_ref"]:
        bits.append(row["internal_ref"])
    elif row["section"]:
        bits.append(row["section"])
    if ed.get("pagination") == "printed":
        page = row["printed_page_start"] or row["pdf_page_start"]
        bits.append("p. %s" % page)
    core = ", ".join(bits)

    tail = []
    if ed.get("translator"):
        tail.append("trans. %s" % ed["translator"])
    if ed.get("publisher"):
        tail.append(ed["publisher"])
    if ed.get("year"):
        tail.append(str(ed["year"]))
    if tail:
        core += ". " + ", ".join(tail) + "."

    return "%s  [%s · pdf p %s · %s]" % (core, ed["source_id"], row["pdf_page_start"],
                                         row["passage_id"])


def citation_ready(ed, row):
    """Whether this passage could carry a citation at all today, and if not
    why not. Being findable is not the same as being citable."""
    blockers = []
    if ed.get("status") != "fixed":
        blockers.append("edition status is %r, not fixed" % ed.get("status"))
    if not ed.get("translator"):
        blockers.append("no translator credit — the project's own rule forbids citing it")
    if not row["internal_ref"] and ed.get("pagination") != "printed":
        blockers.append("no internal number on this passage and this edition's page numbers "
                        "are not citable")
    if not row["quotation_ready"]:
        if row["extraction_method"] == "ocr":
            why = "OCR text, unverified against the page"
        elif ed.get("arabic_extraction") == "unusable":
            why = ("this edition's Arabic extracts as broken glyphs — the text here is "
                   "damaged, not merely unverified")
        else:
            why = "carries Arabic, unverified against the page"
        blockers.append("not quotation-ready: %s" % why)
    return (not blockers), blockers


def shape(row, ed, snippet=None):
    ok, blockers = citation_ready(ed, row)
    out = {
        "passage_id": row["passage_id"],
        "source_id": ed["source_id"],
        "work": ed.get("work"),
        "edition": {
            "translator": ed.get("translator"),
            "publisher": ed.get("publisher"),
            "year": ed.get("year"),
            "volume": ed.get("volume_title") or ed.get("volume"),
            "status": ed.get("status"),
            "sha256": ed.get("sha256"),
            "arabic_extraction": ed.get("arabic_extraction"),
        },
        "locator": locator(ed, row),
        "passage_type": row["passage_type"],
        "speaker": row["speaker"],
        "subject": row["subject"],
        "chapter": row["chapter"],
        "section": row["section"],
        "register": row["register"],
        "text": row["text"],
        "english": row["english"],
        "arabic_raw": row["arabic_raw"],
        "arabic_verified": (None if row["arabic_verified"] is None
                            else bool(row["arabic_verified"])),
        "extraction_method": row["extraction_method"],
        "extraction_status": row["extraction_status"],
        "quotation_ready": bool(row["quotation_ready"]),
        "metadata_source": row["metadata_source"],
        "citation": citation_string(ed, row),
        "citation_ready": ok,
    }
    if blockers:
        out["citation_blockers"] = blockers
    if snippet:
        out["matched"] = snippet
    return out


# --------------------------------------------------------------------------
# queries
# --------------------------------------------------------------------------

def run_search(con, match, args, active_ids):
    where = ["p.source_id IN (%s)" % ",".join("?" * len(active_ids))]
    params = list(active_ids)
    if args.source:
        where.append("p.source_id = ?")
        params.append(args.source)
    if args.type:
        where.append("p.passage_type = ?")
        params.append(args.type)
    if args.speaker:
        where.append("p.speaker LIKE ?")
        params.append("%" + args.speaker + "%")
    if args.min_chars:
        where.append("p.char_count >= ?")
        params.append(args.min_chars)
    if args.quotation_ready:
        where.append("p.quotation_ready = 1")

    sql = ("SELECT p.*, snippet(passages_fts, 0, '»', '«', ' … ', 18) AS snip, "
           "       bm25(passages_fts) AS rank "
           "FROM passages_fts f JOIN passages p ON p.rowid = f.rowid "
           "WHERE passages_fts MATCH ? AND " + " AND ".join(where) +
           " ORDER BY rank LIMIT ?")
    return con.execute(sql, [match] + params + [args.limit]).fetchall()


def run_lookup(con, args):
    if args.passage:
        return con.execute("SELECT * FROM passages WHERE passage_id = ?",
                           (args.passage,)).fetchall()
    sid, _, page = args.page.partition(":")
    if not page:
        raise SystemExit("--page wants SOURCE_ID:PAGE, e.g. SRC-TAU-001:142")
    return con.execute("SELECT * FROM passages WHERE source_id = ? AND ? BETWEEN "
                       "pdf_page_start AND pdf_page_end ORDER BY ordinal",
                       (sid, int(page))).fetchall()


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def print_human(results, header=None):
    if header:
        print(header)
    if not results:
        print("no passages matched.\n"
              "Nothing outside 00-sources/ is searched — a claim with no hit here has no "
              "evidence in the source library, not merely no evidence in the drafts.")
        return
    for i, r in enumerate(results, 1):
        loc = r["locator"]
        page = "pdf p %s" % loc["pdf_page_start"]
        if loc["pdf_page_end"] != loc["pdf_page_start"]:
            page += "–%s" % loc["pdf_page_end"]
        if loc["printed_page_start"]:
            page += " (printed p %s)" % loc["printed_page_start"]

        print("\n%d. %s" % (i, r["passage_id"]))
        print("   %s — %s" % (r["source_id"], r["work"]))
        ed = r["edition"]
        print("   edition: %s%s [%s]" % (
            ed["translator"] or "no translator credit",
            ", " + str(ed["publisher"]) if ed["publisher"] else "",
            ed["status"]))
        print("   %s · %s%s" % (page, r["passage_type"],
                                " · " + r["speaker"] if r["speaker"] else ""))
        if loc.get("internal_ref"):
            print("   internal ref: %s" % loc["internal_ref"])
        if loc.get("pagination_warning"):
            print("   ⚠ %s" % loc["pagination_warning"])
        if r.get("matched"):
            print("   match: %s" % r["matched"].replace("\n", " "))
        body = (r["text"] or "").strip().replace("\n", "\n     ")
        if len(body) > 700:
            body = body[:700] + " …"
        print("     %s" % body)
        if r["arabic_raw"]:
            print("   arabic_verified: %s — compare against the page image before quoting:"
                  % r["arabic_verified"])
            print("     python tools/page_image.py --source %s --page %s"
                  % (r["source_id"], loc["pdf_page_start"]))
        print("   cite: %s" % r["citation"])
        if not r["citation_ready"]:
            for b in r.get("citation_blockers", []):
                print("   ✗ %s" % b)
    print("\n%d result(s). The page in the original PDF is the evidence; this is a pointer "
          "to it." % len(results))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?", help="what to search for")
    ap.add_argument("--query", dest="query_opt", help="same, as an option")
    ap.add_argument("--claim", help="a claim_id, or the claim sentence itself")
    ap.add_argument("--source", help="restrict to one edition, e.g. SRC-TAU-001")
    ap.add_argument("--type", help="passage_type, e.g. saying, sermon, letter")
    ap.add_argument("--speaker", help="substring of the speaker as printed")
    ap.add_argument("--passage", help="fetch one passage by id")
    ap.add_argument("--page", help="fetch a whole page: SOURCE_ID:PAGE")
    ap.add_argument("--exact", action="store_true", help="phrase search, not term AND")
    ap.add_argument("--arabic", action="store_true",
                    help="treat the query as Arabic and also search the normalised form")
    ap.add_argument("--quotation-ready", action="store_true",
                    help="only passages fit to quote verbatim today")
    ap.add_argument("--min-chars", type=int, default=0)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--db", default=config.DB)
    args = ap.parse_args()

    con = db.connect(args.db, readonly=True)
    eds = edition_map(con)

    # Phase 13 boundary, enforced in the query itself: rejected and missing
    # editions are not searchable, whatever else is asked for.
    active_ids = [sid for sid, e in eds.items()
                  if e.get("status") in ("fixed", "candidate", "verification-required")]

    header = None
    claim_row = None

    if args.passage or args.page:
        rows = run_lookup(con, args)
        results = [shape(r, eds[r["source_id"]]) for r in rows if r["source_id"] in eds]
        if args.json:
            print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
        else:
            print_human(results)
        return 0

    query = args.query or args.query_opt
    if args.claim:
        claim_row = con.execute("SELECT * FROM claims WHERE claim_id = ?",
                                (args.claim,)).fetchone()
        text = claim_row["claim_text"] if claim_row else args.claim
        match = claim_to_query(text)
        header = ("searching for evidence for: %s\n(this returns candidates. A candidate is "
                  "not a verification — TV becomes V only when a human has opened the named "
                  "edition at the named page.)" % text)
    elif query:
        if args.arabic:
            norm = normalize_arabic(query)
            match = "%s OR %s" % (build_match(query, args.exact),
                                  build_match(norm, args.exact))
        else:
            match = build_match(query, args.exact)
    else:
        ap.error("give a query, --claim, --passage or --page")

    rows = run_search(con, match, args, active_ids)
    results = []
    for r in rows:
        ed = eds[r["source_id"]]
        results.append(shape(r, ed, snippet=r["snip"]))

    if args.json:
        payload = {
            "query": query or args.claim,
            "match_expression": match,
            "searched": {"corpus_root": "00-sources/", "editions": len(active_ids)},
            "boundary": "00-sources/ only. Project drafts are not evidence.",
            "results": results,
        }
        if claim_row:
            payload["claim"] = {k: claim_row[k] for k in claim_row.keys()}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(results, header)
    return 0


if __name__ == "__main__":
    sys.exit(main())

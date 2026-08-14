#!/usr/bin/env python3
"""
The state of the evidence, in one report.

    python tools/source_audit.py                  # to the terminal
    python tools/source_audit.py --write          # to 00-sources/reports/source-audit.md
    python tools/source_audit.py --json

Answers the questions that decide what work is possible:

    which editions are fixed, candidate, missing, rejected
    which claims are TV, which are V
    claims with no citation
    citations with no page and no internal number
    citations pointing at a source that is not fixed
    sources with no metadata, no original PDF, or no hash
    Arabic passages awaiting visual verification
    passages that OCR produced and nobody has checked
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, db, metadata


def gather(con):
    q = lambda sql, *a: [dict(r) for r in con.execute(sql, a)]
    one = lambda sql, *a: con.execute(sql, a).fetchone()[0]

    editions = q("SELECT source_id, work, volume_title, translator, publisher, year, status, "
                 "pagination, citation_unit, permission, sha256, file, page_count, "
                 "ingested_pages, complete, extraction_method, arabic_extraction, "
                 "arabic_passages, notes "
                 "FROM v_editions ORDER BY status, source_id")

    by_status = {}
    for e in editions:
        by_status.setdefault(e["status"], []).append(e)

    claims = q("SELECT claim_id, env, item, status, claim_text, project_location FROM claims "
               "ORDER BY status, env, claim_id")
    claims_by_status = {}
    for c in claims:
        claims_by_status.setdefault(c["status"], []).append(c)

    no_citation = q(
        "SELECT c.claim_id, c.env, c.status, c.claim_text FROM claims c "
        "LEFT JOIN citations ct ON ct.claim_id = c.claim_id "
        "WHERE ct.citation_id IS NULL ORDER BY c.status, c.env")

    no_locator = q(
        "SELECT citation_id, claim_id, source_id, ref FROM citations "
        "WHERE (ref IS NULL OR ref = '') AND page_start IS NULL")

    unlocated = q(
        "SELECT ct.citation_id, ct.claim_id, ct.source_id, ct.ref FROM citations ct "
        "WHERE ct.passage_id IS NULL ORDER BY ct.source_id")

    not_fixed = q(
        "SELECT ct.citation_id, ct.claim_id, ct.source_id, e.status FROM citations ct "
        "JOIN editions e ON e.source_id = ct.source_id WHERE e.status != 'fixed'")

    v_without = q(
        "SELECT c.claim_id, c.env, c.claim_text FROM claims c WHERE c.status = 'V' "
        "AND NOT EXISTS (SELECT 1 FROM citations ct JOIN editions e "
        "ON e.source_id = ct.source_id WHERE ct.claim_id = c.claim_id "
        "AND e.status != 'rejected' AND (ct.ref IS NOT NULL OR ct.page_start IS NOT NULL))")

    arabic = q(
        "SELECT p.source_id, COUNT(*) n, "
        "       SUM(CASE WHEN p.arabic_raw IS NOT NULL THEN 1 ELSE 0 END) arabic_only, "
        "       e.arabic_extraction quality "
        "FROM passages p JOIN editions e ON e.source_id = p.source_id "
        "WHERE p.arabic_verified = 0 "
        "GROUP BY p.source_id ORDER BY n DESC")

    ocr = q("SELECT source_id, COUNT(*) n FROM passages WHERE extraction_method = 'ocr' "
            "AND COALESCE(quotation_ready,0) = 0 GROUP BY source_id ORDER BY n DESC")

    no_pdf = [e for e in editions
              if e["status"] not in ("missing", "rejected") and not e["file"]]
    no_hash = [e for e in editions
               if e["status"] not in ("missing", "rejected") and not e["sha256"]]
    fixed_incomplete = [e for e in editions if e["status"] == "fixed" and e["complete"] == 0]

    page_uncitable = [e for e in editions
                      if e["status"] in ("fixed", "candidate", "verification-required")
                      and e["pagination"] != "printed"]

    rejected = q("SELECT key, work, reason, decided_on FROM rejected_sources ORDER BY key")

    return {
        "generated": datetime.datetime.now(datetime.timezone.utc)
                              .replace(microsecond=0).isoformat(),
        "corpus": {
            "pages": one("SELECT COUNT(*) FROM pages"),
            "passages": one("SELECT COUNT(*) FROM passages"),
            "arabic_passages": one("SELECT COUNT(*) FROM passages WHERE arabic_raw IS NOT NULL"),
            "quotation_ready": one("SELECT COUNT(*) FROM passages WHERE quotation_ready = 1"),
            "built_at": db.get_meta(con, "built_at"),
            "build_mode": db.get_meta(con, "build_mode"),
            "pipeline_version": db.get_meta(con, "pipeline_version"),
        },
        "editions": editions,
        "editions_by_status": {k: [e["source_id"] for e in v] for k, v in by_status.items()},
        "claims_by_status": {k: len(v) for k, v in claims_by_status.items()},
        "claims": claims,
        "claims_without_citation": no_citation,
        "citations_without_locator": no_locator,
        "citations_not_located_to_a_passage": unlocated,
        "citations_on_unfixed_editions": not_fixed,
        "v_claims_without_usable_citation": v_without,
        "arabic_awaiting_verification": arabic,
        "ocr_awaiting_verification": ocr,
        "editions_without_original_pdf": [e["source_id"] for e in no_pdf],
        "editions_without_sha256": [e["source_id"] for e in no_hash],
        "fixed_but_incomplete": [e["source_id"] for e in fixed_incomplete],
        "editions_whose_pages_cannot_be_cited": [
            {"source_id": e["source_id"], "pagination": e["pagination"],
             "citation_unit": e["citation_unit"]} for e in page_uncitable],
        "rejected_sources": rejected,
    }


def render_md(a):
    L = []
    w = L.append
    w("# Source audit")
    w("")
    w("Generated by `tools/source_audit.py` from `00-sources/source.db`. "
      "**Do not edit — regenerate.**")
    w("")
    c = a["corpus"]
    w("Corpus built %s (`%s`, pipeline %s): **%d pages, %d passages**, %d carrying Arabic, "
      "%d quotation-ready."
      % (c["built_at"], c["build_mode"], c["pipeline_version"], c["pages"], c["passages"],
         c["arabic_passages"], c["quotation_ready"]))
    w("")

    w("## Editions")
    w("")
    w("| source_id | work | translator | status | pagination | page citable | Arabic |")
    w("|---|---|---|---|---|---|---|")
    for e in a["editions"]:
        w("| `%s` | %s%s | %s | **%s** | %s | %s | %s |" % (
            e["source_id"], e["work"],
            " — " + e["volume_title"] if e["volume_title"] else "",
            e["translator"] or "*none credited*", e["status"], e["pagination"],
            "yes" if e["pagination"] == "printed" else "no",
            e["arabic_extraction"] or "—"))
    w("")

    counts = {k: len(v) for k, v in a["editions_by_status"].items()}
    w("%s." % ", ".join("**%d %s**" % (v, k) for k, v in sorted(counts.items())))
    w("")

    w("## Claims")
    w("")
    w("| status | count |")
    w("|---|---|")
    for k, v in sorted(a["claims_by_status"].items()):
        w("| `%s` | %d |" % (k, v))
    w("")
    w("`TV` is not `V`. Nothing prints on `TV`, and no tool in this repository may "
      "change one into the other.")
    w("")

    def section(title, rows, cols, empty="None."):
        w("## %s" % title)
        w("")
        if not rows:
            w(empty)
            w("")
            return
        w("| %s |" % " | ".join(cols))
        w("|%s|" % "|".join("---" for _ in cols))
        for r in rows:
            w("| %s |" % " | ".join(str(r.get(c.replace(" ", "_"), "") or "") for c in cols))
        w("")

    section("Claims with no citation at all",
            a["claims_without_citation"][:200],
            ["claim_id", "env", "status", "claim_text"])
    section("V claims with no usable citation",
            a["v_claims_without_usable_citation"],
            ["claim_id", "env", "claim_text"],
            empty="None. Every `V` claim names a permitted edition and a number.")
    section("Citations with neither a page nor an internal number",
            a["citations_without_locator"], ["citation_id", "claim_id", "source_id"],
            empty="None. A citation without a number is decoration; there are none.")
    section("Citations not located to a passage",
            a["citations_not_located_to_a_passage"],
            ["citation_id", "claim_id", "source_id", "ref"],
            empty="None — every citation resolves to a passage in the database.")
    section("Citations resting on an edition that is not fixed",
            a["citations_on_unfixed_editions"],
            ["citation_id", "claim_id", "source_id", "status"])

    w("## Arabic awaiting visual verification")
    w("")
    if not a["arabic_awaiting_verification"]:
        w("None.")
    else:
        w("Arabic in this corpus is reordered by the PDFs' font encodings. None of it is "
          "quotation-ready until somebody has put it beside the page image "
          "(`tools/page_image.py`).")
        w("")
        w("| source_id | passages carrying Arabic | Arabic-only | extraction |")
        w("|---|---|---|---|")
        for r in a["arabic_awaiting_verification"]:
            w("| `%s` | %d | %d | **%s** |" % (r["source_id"], r["n"], r["arabic_only"],
                                               r["quality"] or "—"))
        w("")
        w("`unusable` is not a guess: it means over half the Arabic runs in that edition "
          "carry private-use codepoints or bidi controls, which is what a PDF leaves behind "
          "when it hands over positioned glyphs instead of text. **The Arabic in every "
          "Arabic-carrying edition here is in that state.** It is preserved verbatim and is "
          "never overwritten, but it cannot be quoted, and searching it will mostly fail. "
          "The fix needs the original PDFs:")
        w("")
        w("```bash")
        w("python tools/build_source_corpus.py --from-pdf --ocr --force-ocr "
          "--ocr-lang ara+eng --only SRC-NHB-002")
        w("```")
    w("")

    w("## OCR text awaiting visual verification")
    w("")
    if not a["ocr_awaiting_verification"]:
        w("None — no source in this corpus was extracted by OCR.")
    else:
        w("| source_id | passages |")
        w("|---|---|")
        for r in a["ocr_awaiting_verification"]:
            w("| `%s` | %d |" % (r["source_id"], r["n"]))
    w("")

    w("## Metadata gaps")
    w("")
    w("| gap | editions |")
    w("|---|---|")
    w("| no original PDF recorded | %s |" % (", ".join(
        "`%s`" % s for s in a["editions_without_original_pdf"]) or "—"))
    w("| no SHA-256 (edition not pinned) | %s |" % (", ".join(
        "`%s`" % s for s in a["editions_without_sha256"]) or "—"))
    w("| marked fixed but incomplete | %s |" % (", ".join(
        "`%s`" % s for s in a["fixed_but_incomplete"]) or "— *(none, as required)*"))
    w("")
    w("A fixed edition is identified by `source_id` **and** SHA-256. An edition with no "
      "hash is not pinned: another copy of the same work would cite different pages.")
    w("")

    w("## Editions whose page numbers may not be cited")
    w("")
    w("| source_id | pagination | cite by |")
    w("|---|---|---|")
    for e in a["editions_whose_pages_cannot_be_cited"]:
        w("| `%s` | %s | %s |" % (e["source_id"], e["pagination"], e["citation_unit"]))
    w("")

    w("## Rejected sources")
    w("")
    w("Excluded under the Shia-sources-only hard rule. Held here as a denylist only — "
      "checked by SHA-256 at ingest, so a re-downloaded copy is refused under any filename.")
    w("")
    w("| key | work | decided |")
    w("|---|---|---|")
    for r in a["rejected_sources"]:
        w("| `%s` | %s | %s |" % (r["key"], r["work"], r["decided_on"]))
    w("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true",
                    help="write 00-sources/reports/source-audit.md")
    ap.add_argument("--db", default=config.DB)
    args = ap.parse_args()

    con = db.connect(args.db, readonly=True)
    a = gather(con)
    con.close()

    if args.json:
        print(json.dumps(a, ensure_ascii=False, indent=2))
        return 0

    md = render_md(a)
    if args.write:
        os.makedirs(config.REPORTS, exist_ok=True)
        dest = os.path.join(config.REPORTS, "source-audit.md")
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print("wrote %s" % os.path.relpath(dest, config.ROOT))
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())

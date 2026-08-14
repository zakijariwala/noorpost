#!/usr/bin/env python3
"""
Build the whole source corpus: extraction, markdown, metadata validation,
SQLite ingestion, FTS index.

    python tools/build_source_corpus.py                 # build everything
    python tools/build_source_corpus.py --only SRC-TAU-001
    python tools/build_source_corpus.py --from-pdf      # re-extract from the PDFs
    python tools/build_source_corpus.py --from-pdf --ocr   # ...OCRing image-only PDFs
    python tools/build_source_corpus.py --hash-originals   # fill sha256/page_count
    python tools/build_source_corpus.py --validate-only

Two ways in, one pipeline:

    --from-text  (default)  00-sources/text/*.txt  ->  pages
    --from-pdf              00-sources/*.pdf       ->  pages   (needs poppler)

Both land on the same intermediate representation, and TXT, Markdown, the page
table and the passage table are all derived from that one list of pages. They
cannot drift apart because nothing generates them separately.

--from-text is the normal path and the one that works with a clone: the PDFs
are not in the repository, the extracted text is. --from-pdf is for a machine
that has the PDFs and wants to re-extract from scratch; it rewrites
00-sources/text/*.txt in exactly the format extract_text.py has always written.
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, db, extract, metadata, passages as seg
from sourcelib.arabic import arabic_char_count, glyph_damage_ratio
from sourcelib.pages import (Page, normalize_newlines, parse_txt, read_text_file, render_md,
                             render_txt, write_pages_jsonl, markers_monotonic)


def log(msg):
    print(msg, flush=True)


# --------------------------------------------------------------------------
# getting pages, either way
# --------------------------------------------------------------------------

def pages_from_text(edition):
    path = os.path.join(config.ROOT, edition["text_file"])
    if not os.path.exists(path):
        return None, {"error": "text file not found: %s" % edition["text_file"]}
    body, newline = read_text_file(path)
    pgs = parse_txt(body, extraction_method="inherited")
    prov = {
        "extraction_method": "inherited",
        "extraction_status": "inherited-from-text-corpus",
        "source_path": edition["text_file"],
        "newline": "crlf" if newline == "\r\n" else "lf",
        "pipeline_version": config.PIPELINE_VERSION,
        "note": ("pages read back from the existing [[p N]] corpus, which was produced by "
                 "tools/extract_text.py. Re-run with --from-pdf on a machine holding the "
                 "PDFs to re-derive them from the original."),
    }
    return pgs, prov


def pages_from_pdf(edition, allow_ocr, ocr_lang, ocr_dpi, write_text, force_ocr=False):
    pdf = extract.find_original(edition.get("file"))
    if not pdf:
        return None, {"error": "no original PDF for %s (file: %r)"
                              % (edition["source_id"], edition.get("file"))}
    sha = extract.sha256_file(pdf)
    if metadata.is_rejected(sha256=sha, filename=os.path.basename(pdf)):
        return None, {"error": "REFUSED: %s is on the rejected list" % os.path.basename(pdf)}
    pgs, prov = extract.extract_pdf(pdf, allow_ocr=allow_ocr, ocr_lang=ocr_lang,
                                    ocr_dpi=ocr_dpi, force_ocr=force_ocr)
    prov["source_path"] = os.path.relpath(pdf, config.ROOT)

    if write_text and edition.get("text_file"):
        dest = os.path.join(config.ROOT, edition["text_file"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="") as f:
            f.write(render_txt(pgs, "\n"))
        log("    wrote %s" % edition["text_file"])
    return pgs, prov


# --------------------------------------------------------------------------
# one edition
# --------------------------------------------------------------------------

def build_edition(con, edition, args):
    sid = edition["source_id"]
    if edition.get("status") in ("missing", "rejected"):
        return {"source_id": sid, "skipped": edition.get("status")}

    if args.from_pdf:
        pgs, prov = pages_from_pdf(edition, args.ocr, args.ocr_lang, args.ocr_dpi,
                                   not args.no_write_text, force_ocr=args.force_ocr)
        if pgs is None and args.fallback_to_text and edition.get("text_file"):
            log("    %s — falling back to the text corpus" % prov.get("error"))
            pgs, prov = pages_from_text(edition)
    else:
        pgs, prov = pages_from_text(edition)

    if pgs is None:
        return {"source_id": sid, "error": prov.get("error")}

    ok, problems = markers_monotonic(pgs)
    if not ok:
        return {"source_id": sid, "error": "page markers out of order: " + "; ".join(problems)}

    # printed page numbers. Only ever applied from an offset recorded by a
    # human in sources.yaml — never inferred, and never for an edition whose
    # pagination is known not to track the printed page.
    offset = edition.get("printed_page_offset")
    if offset is not None and edition.get("pagination") == "printed":
        for p in pgs:
            p.printed_page = p.pdf_page + offset

    # --- intermediate representation on disk -----------------------------
    os.makedirs(config.PAGES, exist_ok=True)
    header = {
        "source_id": sid,
        "work": edition.get("work"),
        "translator": edition.get("translator"),
        "sha256": edition.get("sha256"),
        "page_count_extracted": len(pgs),
        "first_page": pgs[0].pdf_page,
        "last_page": pgs[-1].pdf_page,
        **prov,
    }
    jsonl = os.path.join(config.PAGES, "%s.pages.jsonl" % sid)
    write_pages_jsonl(jsonl, header, pgs)

    # --- markdown, from the same pages -----------------------------------
    os.makedirs(config.MD, exist_ok=True)
    front = [
        ("source_id", sid),
        ("work", edition.get("work")),
        ("volume", edition.get("volume_title") or edition.get("volume")),
        ("author", edition.get("author")),
        ("translator", edition.get("translator")),
        ("publisher", edition.get("publisher")),
        ("year", edition.get("year")),
        ("status", edition.get("status")),
        ("pagination", edition.get("pagination")),
        ("citation_unit", edition.get("citation_unit")),
        ("sha256", edition.get("sha256")),
        ("extraction_method", prov.get("extraction_method")),
        ("extraction_status", prov.get("extraction_status")),
        ("pages", len(pgs)),
        ("generated_by", "tools/build_source_corpus.py %s" % config.PIPELINE_VERSION),
        ("note", "Representation of the source, not an edited version. "
                 "[[p N]] markers are the page boundaries of the original."),
    ]
    md_text = render_md(pgs, front)
    md_path = os.path.join(config.MD, "%s.md" % sid)
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md_text)

    # per-page markdown, sliced from the same render so the page table and the
    # .md file cannot disagree
    per_page_md = {}
    for p in pgs:
        per_page_md[p.pdf_page] = render_md([p])

    # --- database ---------------------------------------------------------
    ed = dict(edition)
    ed["extraction_method"] = prov.get("extraction_method")
    ed["extraction_status"] = prov.get("extraction_status")
    ed["ocr_engine"] = prov.get("ocr_engine")
    ed["ocr_engine_version"] = prov.get("ocr_engine_version")
    ed["ocr_confidence"] = prov.get("ocr_confidence")
    ed["ocr_timestamp"] = prov.get("ocr_timestamp")
    ed["pipeline_version"] = config.PIPELINE_VERSION
    ed["ingested_pages"] = len(pgs)
    if prov.get("sha256"):
        ed["sha256"] = prov["sha256"]
    if prov.get("pdf_page_count"):
        ed["page_count"] = prov["pdf_page_count"]
    db.upsert_edition(con, ed)

    db.replace_pages(con, sid, [{
        "source_id": sid,
        "pdf_page": p.pdf_page,
        "printed_page": p.printed_page,
        "page_label": p.page_label,
        # Stored LF-normalised. That is the only difference from the .txt
        # corpus, and render_txt() puts the original terminators back.
        "text": normalize_newlines(p.text),
        "markdown": per_page_md[p.pdf_page],
        "char_count": len(p.text),
        "arabic_char_count": arabic_char_count(p.text),
        "extraction_method": p.extraction_method,
        "ocr_confidence": p.ocr_confidence,
        "page_image_path": None,
    } for p in pgs])

    ps = seg.segment(sid, pgs, join_pages=not args.no_join_pages,
                     extraction_status=prov.get("extraction_status"))
    db.insert_passages(con, [p.as_row() for p in ps])

    # Is the Arabic in this edition usable at all? Measured, not assumed: a PDF
    # that hands over positioned glyphs rather than text leaves private-use
    # codepoints and bidi controls through the middle of every Arabic run.
    arabic_texts = [p.arabic_raw or p.text for p in ps if p.arabic_verified is not None]
    damage = glyph_damage_ratio(arabic_texts)
    ed["arabic_passages"] = len(arabic_texts)
    ed["arabic_extraction"] = ("none" if not arabic_texts
                               else "unusable" if damage >= 0.5
                               else "suspect" if damage > 0 else "ok")
    db.upsert_edition(con, ed)

    return {
        "source_id": sid,
        "pages": len(pgs),
        "passages": len(ps),
        "arabic_passages": sum(1 for p in ps if p.arabic_raw),
        "arabic_extraction": ed["arabic_extraction"],
        "extraction_method": prov.get("extraction_method"),
        "md": os.path.relpath(md_path, config.ROOT),
    }


# --------------------------------------------------------------------------
# hashing originals
# --------------------------------------------------------------------------

def hash_originals(editions):
    """Fill sha256 and page_count in sources.yaml from the PDFs actually held.
    Run this on the machine that has them."""
    doc = metadata.load_yaml(config.SOURCES_YAML)
    by_id = {e["source_id"]: e for e in doc.get("editions", [])}
    changed = 0
    for e in editions:
        raw = by_id.get(e["source_id"])
        if raw is None:
            continue
        pdf = extract.find_original(e.get("file"))
        if not pdf:
            continue
        sha = extract.sha256_file(pdf)
        if metadata.is_rejected(sha256=sha, filename=os.path.basename(pdf)):
            log("  REFUSED %s — rejected source" % os.path.basename(pdf))
            continue
        if raw.get("sha256") and raw["sha256"] != sha:
            log("  ⚠ %s: sha256 CHANGED. The fixed edition is identified by its hash — "
                "a different hash is a different edition." % e["source_id"])
        raw["sha256"] = sha
        n = extract.pdf_page_count(pdf)
        if n:
            raw["page_count"] = n
        log("  %s  %s  %s" % (e["source_id"], sha[:16], os.path.basename(pdf)))
        changed += 1
    if changed:
        header = open(config.SOURCES_YAML, encoding="utf-8").read().split("\nworks:")[0]
        metadata.dump_yaml(config.SOURCES_YAML, doc, header)
        log("updated %d records in %s" % (changed, os.path.relpath(config.SOURCES_YAML,
                                                                   config.ROOT)))
    else:
        log("no original PDFs found in %s" % " or ".join(
            os.path.relpath(d, config.ROOT) for d in config.ORIGINAL_DIRS))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", help="one source_id (repeatable)")
    ap.add_argument("--from-pdf", action="store_true", help="re-extract from the original PDFs")
    ap.add_argument("--fallback-to-text", action="store_true",
                    help="with --from-pdf, use the text corpus where a PDF is missing")
    ap.add_argument("--no-write-text", action="store_true",
                    help="with --from-pdf, do not rewrite 00-sources/text/*.txt")
    ap.add_argument("--ocr", action="store_true", help="OCR PDFs that carry no native text")
    ap.add_argument("--force-ocr", action="store_true",
                    help="OCR even where native text exists — the fix for an edition whose "
                         "Arabic extracts as broken glyphs. Use with --ocr-lang ara or eng+ara.")
    ap.add_argument("--ocr-lang", default="eng", help="tesseract language(s), e.g. eng+ara")
    ap.add_argument("--ocr-dpi", type=int, default=300)
    ap.add_argument("--no-join-pages", action="store_true",
                    help="do not join a passage that runs across a page break")
    ap.add_argument("--hash-originals", action="store_true")
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--db", default=config.DB)
    args = ap.parse_args()

    works, editions, by_id = metadata.load_sources()
    rejected = metadata.load_rejected()
    claims = metadata.load_claims()
    citations = metadata.load_citations()

    problems = metadata.validate(works, editions, claims, citations, rejected)
    if problems:
        log("METADATA PROBLEMS (%d):" % len(problems))
        for p in problems:
            log("  ✗ %s" % p)
    else:
        log("metadata: %d works, %d editions, %d claims, %d citations — no problems"
            % (len(works), len(editions), len(claims), len(citations)))

    if args.validate_only:
        return 1 if problems else 0
    if problems:
        log("\nrefusing to build on broken metadata")
        return 1

    if args.hash_originals:
        hash_originals(editions)
        return 0

    targets = [e for e in editions if not args.only or e["source_id"] in args.only]
    if not targets:
        log("no editions matched")
        return 1

    con = db.connect(args.db)
    db.create_schema(con)
    db.upsert_works(con, works.values())
    db.replace_rejected(con, rejected)

    results = []
    log("")
    for e in sorted(targets, key=lambda x: x["source_id"]):
        log("  %s  %s" % (e["source_id"], e.get("work")))
        r = build_edition(con, e, args)
        results.append(r)
        if r.get("error"):
            log("    ✗ %s" % r["error"])
        elif r.get("skipped"):
            log("    – %s, nothing to extract" % r["skipped"])
        else:
            log("    %d pages, %d passages%s  [%s]"
                % (r["pages"], r["passages"],
                   ", %d arabic" % r["arabic_passages"] if r["arabic_passages"] else "",
                   r["extraction_method"]))
    con.commit()

    # claims and citations
    db.replace_claims(con, claims, citations)

    log("\nbuilding FTS5 index …")
    db.rebuild_fts(con)

    db.set_meta(con, "pipeline_version", config.PIPELINE_VERSION)
    db.set_meta(con, "built_at",
                datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat())
    db.set_meta(con, "corpus_root", "00-sources/")
    db.set_meta(con, "build_mode", "from-pdf" if args.from_pdf else "from-text")
    con.commit()

    n_pages = con.execute("SELECT COUNT(*) c FROM pages").fetchone()["c"]
    n_pass = con.execute("SELECT COUNT(*) c FROM passages").fetchone()["c"]
    n_ar = con.execute("SELECT COUNT(*) c FROM passages WHERE arabic_raw IS NOT NULL").fetchone()["c"]
    con.close()

    built = [r for r in results if r.get("pages")]
    log("\n%d editions, %d pages, %d passages (%d carrying Arabic)"
        % (len(built), n_pages, n_pass, n_ar))
    log("db      %s" % os.path.relpath(args.db, config.ROOT))
    log("md      %s" % os.path.relpath(config.MD, config.ROOT))
    log("pages   %s" % os.path.relpath(config.PAGES, config.ROOT))
    log("\nSearch it:  python tools/source_search.py \"Yahya ibn Aktham\"")
    log("Audit it:   python tools/source_audit.py")

    errs = [r for r in results if r.get("error")]
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

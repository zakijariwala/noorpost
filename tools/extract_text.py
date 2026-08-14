#!/usr/bin/env python3
"""
Turn every PDF in 00-sources/ into page-numbered plain text in 00-sources/text/.

    python tools/extract_text.py            # skip files already done
    python tools/extract_text.py --force    # redo everything

Needs pdftotext (poppler). Already on PATH here.

Why this exists: a 400-page book is roughly 200,000 tokens. Reading one into
a model's context to check a single hadith costs more than the whole of the
rest of this project. Extracted text can be grepped instead — a hit comes back
as ten lines, about 200 tokens, and it carries the page number with it.

Each page break becomes a line reading

    [[p 137]]

so a grep hit can be traced to a printed page without opening the PDF.

The extraction itself now lives in tools/sourcelib/, so this script and
tools/build_source_corpus.py cut pages the same way — the .txt corpus, the
canonical Markdown and the passage database cannot drift apart. The output of
this command is unchanged, byte for byte.

00-sources/originals/ is searched as well as 00-sources/, and a PDF on the
rejected list (00-sources/metadata/rejected.yaml) is refused.
"""

import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, extract as ex, metadata
from sourcelib.pages import pages_from_pdftotext, render_txt, total_pdf_pages

ROOT = config.ROOT
SRC = config.SOURCES
OUT = config.TEXT


def extract(pdf, dest):
    """(sheet count, error). Unchanged in behaviour: pdftotext -layout, split on
    form feeds, drop pages holding no text, one [[p N]] line per page kept."""
    try:
        raw = ex.pdftotext_raw(pdf)
    except ex.ExtractionError as e:
        return None, str(e)[:200]

    pages = pages_from_pdftotext(raw)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(render_txt(pages, "\n"))
    return total_pdf_pages(raw), None


def pdf_paths():
    """Every PDF under 00-sources/ and 00-sources/originals/, by filename."""
    found = {}
    for d in config.ORIGINAL_DIRS:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.lower().endswith(".pdf"):
                found.setdefault(name, os.path.join(d, name))
    return sorted(found.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    pdfs = pdf_paths()
    if not pdfs:
        print("no PDFs in 00-sources/")
        return

    try:
        rejected = metadata.rejected_index()
    except metadata.MetadataError:
        rejected = (set(), set())

    total_chars = 0
    for name, path in pdfs:
        # Shia sources only. A rejected work is refused here as well as in the
        # corpus build, so it cannot be reached by a later grep.
        if metadata.is_rejected(filename=name, index=rejected) or \
           metadata.is_rejected(sha256=ex.sha256_file(path), index=rejected):
            print(f"  SKIP  {name}  ← rejected source, see 00-foundations/sourcing-rules.md")
            continue

        dest = os.path.join(OUT, os.path.splitext(name)[0] + ".txt")
        if os.path.exists(dest) and not a.force:
            total_chars += os.path.getsize(dest)
            print(f"  skip  {name}")
            continue
        print(f"  ...   {name}", flush=True)
        pages, err = extract(path, dest)
        if err:
            print(f"  FAIL  {name}: {err}")
            continue
        size = os.path.getsize(dest)
        total_chars += size
        note = "  ← almost no text, probably a scan without OCR" if size < 20000 else ""
        print(f"  ok    {name}  {pages} pages, {size//1024} KB{note}")

    print(f"\ntext in {OUT}")
    print(f"total {total_chars//1024} KB  (~{total_chars//4//1000}k tokens if ever read whole — don't)")
    print("""
Search it instead of reading it:

    grep -n -i -B2 -A6 "shurayh" 00-sources/text/*.txt
    grep -rn "three hundred" 00-sources/text/irshad--*.txt

Then read back to the nearest [[p N]] line above the hit for the page number.

Or search the structured corpus, which carries the edition and the page with
every hit and knows which editions' page numbers may be cited:

    python tools/build_source_corpus.py
    python tools/source_search.py "shurayh" --json""")


if __name__ == "__main__":
    main()

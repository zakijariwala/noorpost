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
"""

import argparse, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "00-sources")
OUT = os.path.join(SRC, "text")


def extract(pdf, dest):
    raw = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", pdf, "-"],
        capture_output=True, timeout=1800,
    )
    if raw.returncode != 0:
        return None, raw.stderr.decode("utf-8", "replace")[:200]

    text = raw.stdout.decode("utf-8", "replace")
    pages = text.split("\f")
    out = []
    for i, page in enumerate(pages, 1):
        page = re.sub(r"[ \t]+\n", "\n", page)
        page = re.sub(r"\n{3,}", "\n\n", page).strip()
        if not page:
            continue
        out.append(f"[[p {i}]]\n{page}")
    body = "\n\n".join(out)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(body)
    return len(pages), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    pdfs = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".pdf"))
    if not pdfs:
        print("no PDFs in 00-sources/")
        return

    total_chars = 0
    for name in pdfs:
        dest = os.path.join(OUT, os.path.splitext(name)[0] + ".txt")
        if os.path.exists(dest) and not a.force:
            total_chars += os.path.getsize(dest)
            print(f"  skip  {name}")
            continue
        print(f"  ...   {name}", flush=True)
        pages, err = extract(os.path.join(SRC, name), dest)
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

Then read back to the nearest [[p N]] line above the hit for the page number.""")


if __name__ == "__main__":
    main()

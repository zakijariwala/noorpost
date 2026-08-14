#!/usr/bin/env python3
"""
Render the exact original PDF page behind a source_id + page number, so a
reviewer can look at it.

    python tools/page_image.py --source SRC-NHB-002 --page 35
    python tools/page_image.py --source SRC-UYR-001 --page 341 --dpi 400 --open
    python tools/page_image.py --source SRC-TAU-001 --pages 140-143

This is how Arabic gets verified. Extracted Arabic in this corpus is reordered
by the PDFs' font encodings and cannot be trusted as a quotation — the page
image is the only way to check it, and arabic_verified stays false until
somebody has.

Images are cached under 00-sources/page-images/<source_id>/ and are not
tracked by git. Pages are rendered on request, not in bulk, because rendering
6,328 pages would put a gigabyte of PNGs in a text repository.

Needs pdftoppm (poppler) and the original PDF. The PDFs are not in the
repository — see HANDOVER.md for the release zip.
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, db, extract, metadata


def cache_path(source_id, page, dpi):
    return os.path.join(config.PAGE_IMAGES, source_id, "p%04d@%d.png" % (page, dpi))


def render(edition, page, dpi, force=False):
    sid = edition["source_id"]
    dest = cache_path(sid, page, dpi)
    if os.path.exists(dest) and not force:
        return dest, "cached"

    pdf = extract.find_original(edition.get("file"))
    if not pdf:
        raise SystemExit(
            "no original PDF for %s.\n"
            "  sources.yaml records file: %r\n"
            "  looked in: %s\n"
            "The PDFs are not tracked in this repository. Fetch the release zip "
            "(HANDOVER.md) or put the PDF in 00-sources/originals/."
            % (sid, edition.get("file"),
               ", ".join(os.path.relpath(d, config.ROOT) for d in config.ORIGINAL_DIRS)))

    if metadata.is_rejected(sha256=extract.sha256_file(pdf), filename=os.path.basename(pdf)):
        raise SystemExit("REFUSED: %s is on the rejected list" % os.path.basename(pdf))

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    produced = extract.render_page_png(pdf, page, os.path.splitext(dest)[0], dpi=dpi)
    if produced != dest:
        os.replace(produced, dest)
    return dest, "rendered"


def parse_pages(args):
    if args.pages:
        lo, _, hi = args.pages.partition("-")
        return list(range(int(lo), int(hi or lo) + 1))
    if args.page is None:
        raise SystemExit("give --page N or --pages N-M")
    return [args.page]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="source_id, e.g. SRC-NHB-002")
    ap.add_argument("--page", type=int)
    ap.add_argument("--pages", help="a range, e.g. 140-143")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--force", action="store_true", help="re-render even if cached")
    ap.add_argument("--record", action="store_true",
                    help="write the path into pages.page_image_path in source.db")
    ap.add_argument("--open", dest="open_it", action="store_true")
    args = ap.parse_args()

    _, editions, by_id = metadata.load_sources()
    ed = by_id.get(args.source)
    if ed is None:
        raise SystemExit("unknown source_id %s" % args.source)
    if ed.get("status") == "rejected":
        raise SystemExit("REFUSED: %s is a rejected source" % args.source)

    made = []
    for page in parse_pages(args):
        dest, how = render(ed, page, args.dpi, args.force)
        rel = os.path.relpath(dest, config.ROOT)
        print("%-9s %s" % (how, rel))
        made.append((page, rel))
        if args.open_it:
            for opener in ("xdg-open", "open"):
                try:
                    subprocess.run([opener, dest], check=False)
                    break
                except FileNotFoundError:
                    continue

    if args.record and os.path.exists(config.DB):
        con = db.connect()
        for page, rel in made:
            con.execute("UPDATE pages SET page_image_path=? WHERE source_id=? AND pdf_page=?",
                        (rel, args.source, page))
        con.commit()
        con.close()
        print("recorded %d page image path(s) in source.db" % len(made))

    print("\nCompare the image against the extracted text:")
    print("  python tools/source_search.py --page %s:%s" % (args.source, made[0][0]))
    print("If the Arabic matches, record arabic_verified for those passages — the pipeline "
          "will not set it for you.")


if __name__ == "__main__":
    sys.exit(main())

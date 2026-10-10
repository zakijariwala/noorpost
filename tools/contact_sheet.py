#!/usr/bin/env python3
"""Lay item previews side by side in one image, to review a set at a glance.

    python tools/contact_sheet.py OUT.png WIDTH COLUMNS IMG [IMG ...]

    # every front in the box, five across
    python tools/contact_sheet.py fronts.png 330 5 04-art/envelopes/preview/*-front.jpg
    # every companion portrait
    python tools/contact_sheet.py people.png 300 6 04-art/companions/preview/*-person.jpg

This is how every design round was reviewed: render (tools/render_envelopes.js,
tools/render_companions.js), sheet the previews, look, fix, repeat. Needs
Pillow (pip install Pillow) — a review aid only, not part of any build.
"""

import sys

from PIL import Image


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    out, width, cols, files = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        thumbs.append(im.resize((width, int(im.height * width / im.width))))
    rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
    sheet = Image.new("RGB", (cols * (width + 10), sum(max(t.height for t in r) + 10 for r in rows)), "#dddddd")
    y = 0
    for r in rows:
        for k, t in enumerate(r):
            sheet.paste(t, (k * (width + 10), y))
        y += max(t.height for t in r) + 10
    sheet.save(out)
    print(f"{out}: {len(thumbs)} images")


if __name__ == "__main__":
    main()

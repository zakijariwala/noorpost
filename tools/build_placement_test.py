#!/usr/bin/env python3
"""Placement test: real illustration dropped into the Paper Dunes frames.

    python tools/build_placement_test.py

The drawn art in 04-art/paper-dunes/ fixes composition and palette. It cannot
say how a finished, painterly illustration will sit on sand stock, under a
postmark, beside a dune band. This sheet answers that with stand-ins: ten
watercolour shrine images saved from Pinterest, each placed where the art
specs in 04-art/prompts.md say that subject belongs.

THE IMAGES ARE NOT OURS. They are third-party work, unlicensed, used to judge
layout and nothing else. This repository is public, so the images, the cropped
copies and the rendered sheet are all git-ignored; only this script, the crop
manifest and the README are tracked. Every page carries a PLACEHOLDER watermark
in print as well as on screen, so no screenshot or PDF of it can pass as a
proof. Nothing here may go into docs/.

Put the source screenshots in 04-art/placeholders/src/<id>.png (ids in
manifest.json), then run this. It crops them and writes placement-test.html.
"""

import html, io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperdunes_art as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "04-art", "placeholders")
E = html.escape

# Where each stand-in goes. Subjects follow the person/event print tables in
# 04-art/prompts.md; nothing is placed where the spec asks for something else.
PLAN = [
    ("Envelope 13 · Dhul Qa'dah · Imam al-Rida", [
        ("front", "17d6291a", "Envelope front — the shrine at Mashhad under the postmark", {"month": "DHUL QA'DAH", "n": "13"}),
        ("person", "c9147ea5", "Person print — the shrine at Mashhad (spec: 13)", {}),
        ("postcard", "7e2038d2", "Postcard front — Mashhad at dusk (13's front is unspecified)", {}),
    ]),
    ("Envelope 14 · Dhul Hijjah · Imam al-Jawad", [
        ("person", "c9793d2b", "Person print — the shrine at Kadhimiya (spec: 14)", {}),
    ]),
    ("Envelope 08 · Rajab · Imam al-Kadhim", [
        ("person-arch", "6e4b3941", "Person print — a barred window in Baghdad, not the shrine (spec: 08)", {}),
    ]),
    ("Envelope 10 · Sha'ban · Imam al-Mahdi", [
        ("event", "06f91c22", "Event print — Jamkaran, ring position 10 (spec: 10)", {}),
    ]),
    ("Envelope 04 · Rabi al-Thani · Imam al-Askari", [
        ("person", "c9d10feb", "Person print — a shrine grille, standing in for Samarra (spec: 04)", {}),
    ]),
    ("Envelope 01 · Muharram · Imam Husayn — mourning", [
        ("person", "b07bbb9c", "Person print — the shrine at Karbala, greyscale (spec: 01, mourning palette)", {"mourning": True}),
        ("postcard", "f6c2feb6", "Postcard front test — greyscale. Spec says the standard; this only tests a dome at postcard size", {"mourning": True}),
    ]),
    ("Everyone Else · al-Abbas", [
        ("person", "83de8618", "Companion person print — the shrine of al-Abbas", {}),
    ]),
]

CSS = """
.ph-art { position: absolute; display: block; mix-blend-mode: multiply; object-fit: contain; z-index: 0; }
.mourning .ph-art { filter: grayscale(1) contrast(1.08); }
/* Feather the edges: each painting's own paper fades into the stock instead of
   showing as a darker rectangle. */
.ph-person, .ph-event, .ph-postcard {
  -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%);
          mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%); }
.ph-person  { left: 4mm; top: 4mm; width: calc(100% - 8mm); height: calc(100% - 14mm); }
.ph-event   { left: 8mm; top: 18mm; width: calc(100% - 16mm); height: calc(100% - 30mm); }
.ph-postcard{ left: 6mm; top: 6mm; width: calc(100% - 12mm); height: calc(100% - 17mm); }
.ph-front   { left: 92mm; top: 30mm; width: 128mm; height: 124mm; }
.ph-arch { position: absolute; left: 16mm; right: 16mm; top: 14mm; bottom: 22mm; border-radius: 58mm 58mm 3mm 3mm;
           overflow: hidden; border: 1.6mm solid var(--dusk); z-index: 0; }
.ph-arch img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ph-mark span { font-size: 10pt; }
"""


def crops():
    with io.open(os.path.join(DIR, "manifest.json"), encoding="utf-8") as f:
        man = {m["id"]: m for m in json.load(f)["images"]}
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("needs Pillow: pip install pillow")
    missing = [i for i in man if not os.path.exists(os.path.join(DIR, "src", f"{i}.png"))]
    if missing:
        raise SystemExit("placeholder art not present (it is not in git — see 04-art/placeholders/README.md): "
                         + ", ".join(missing))
    for i, m in man.items():
        src = Image.open(os.path.join(DIR, "src", f"{i}.png")).convert("RGB")
        k = src.width / 923
        src.crop([round(v * k) for v in m["crop"]]).save(os.path.join(DIR, f"{i}.jpg"), quality=88)
    return man


def mark():
    return '<div class="watermark-placeholder ph-mark"><span>PLACEHOLDER — NOT LICENSED</span></div>'


def piece(kind, img, opts):
    m = bool(opts.get("mourning"))
    mcls = " mourning" if m else ""
    src = f"{img}.jpg"
    if kind == "front":
        ink = A.MOURN_INK if m else A.STD["dusk"]
        inner = (f'<img class="ph-art ph-front" src="{src}" alt="">'
                 '<div class="brand"><p class="kicker">Noor Post</p>'
                 '<div class="tag">One of fourteen. Open it on the day.</div></div>'
                 + A.stamp_ring(opts["month"], opts["n"], ink)
                 + '<div class="name-area"><p class="kicker">For</p><div class="who">[Child\'s name]</div></div>'
                 + mark())
        return f'<div class="page p-env env-front{mcls}" style="background:var(--dune)">{inner}</div>'
    if kind == "person":
        return f'<div class="page p-a5p{mcls}"><img class="ph-art ph-person" src="{src}" alt="">{mark()}</div>'
    if kind == "person-arch":
        return (f'<div class="page p-a5p{mcls}"><div class="ph-arch"><img src="{src}" alt=""></div>{mark()}</div>')
    if kind == "event":
        return (f'<div class="page p-a5l{mcls}"><img class="ph-art ph-event" src="{src}" alt="">'
                f'<div class="punch"></div>{mark()}</div>')
    if kind == "postcard":
        return f'<div class="page p-a6l{mcls}"><img class="ph-art ph-postcard" src="{src}" alt="">{mark()}</div>'
    raise ValueError(kind)


def build(man):
    groups = []
    for title, pieces in PLAN:
        items = "".join(
            f'<div>{piece(k, i, o)}<p class="cap screen-only">{E(cap)}<br>'
            f'<em>Stand-in: {E(man[i]["credit"])} — not licensed.</em></p></div>'
            for k, i, cap, o in pieces)
        groups.append(f'<section class="group"><h2 class="screen-only">{E(title)}</h2>'
                      f'<div class="row">{items}</div></section>')
    credits = "".join(f"<li>{E(m['subject'])} — {E(m['credit'])}</li>" for m in man.values())
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Placement test — Paper Dunes</title>
<link rel="stylesheet" href="../print/assets/print.css">
<link rel="stylesheet" href="../paper-dunes/paper-dunes.css">
<style>{CSS}</style>
</head><body class="set">
<header class="set-head screen-only"><h1>Placement test</h1>
<p>Finished, painterly art placed in the Paper Dunes frames, to see how it sits on sand stock, under the postmark and above
the dune band. <strong>Every image here is a third-party stand-in from Pinterest — not licensed, not ours, never to be
printed or published.</strong> Each sits where <code>04-art/prompts.md</code> places that subject. Watercolour on paper
is set with a multiply blend, so its own paper drops out and the stock shows through.</p>
<p>Credits: </p><ul style="font-family:var(--body);font-size:9pt;color:#5a4a55">{credits}</ul></header>
{"".join(groups)}
</body></html>
"""


def main():
    man = crops()
    out = os.path.join(DIR, "placement-test.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(build(man))
    print(f"placement test: {sum(len(p) for _, p in PLAN)} pieces → {os.path.relpath(out, ROOT)} (git-ignored)")


if __name__ == "__main__":
    main()

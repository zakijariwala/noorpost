#!/usr/bin/env python3
"""Build all fourteen envelopes, each in its own style, every item.

    python tools/build_envelopes.py           # write 04-art/envelopes/
    python tools/build_envelopes.py --check   # exit 1 if anything on disk is stale

One file per envelope, 04-art/envelopes/envelope-NN.html, printing straight to
one PDF with every item at its own size: envelope front and back, inside flap,
the letter as one A4 sheet folded to four A5 faces, hadith card, the session
card in its kind (conversation, mourning, open, or a case file with five
evidence cards and a sealed answer), person print, event print with the ring
punch, sticker sheet or pennant, and the return postcard.

Fourteen styles, one structure. Styles are data in tools/envelope_themes.py;
the drawings come from tools/envelope_art.py; every word comes from source via
tools/envelope_sources.py. The rules that hold across all fourteen are checked
here and again in tests/test_envelopes.py:

  - no envelope number on a hadith card (design-system.md §7)
  - an undecided silsila segment prints as a blank, never a guess
  - the mourning issues carry charcoal and ivory only
  - the last letter line is the ●○ line, set alone on face 3
"""

import html, io, os, re, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envelope_art as A
import envelope_sources as S
import mourning_art as M
from envelope_themes import THEMES, SCENES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "04-art", "envelopes")
E = html.escape

RADIUS = {"C": "2.5mm", "C2": "2.5mm", "C4": "4mm", "B": "4mm", "B3": "0", "A": "2mm", "A2": "2mm", "A3": "1mm",
          "D": "0", "E": "0", "F": "3mm", "G": "2mm", "M1": "0", "M2": "0"}

EXTRA = {
    "D": ".face, .band { box-shadow: inset 0 0 0 3mm var(--ground), inset 0 0 0 3.5mm #C9A04A, inset 0 0 0 4.4mm var(--ground), inset 0 0 0 4.7mm #1F3A7A; }",
    "F": ".face::after, .band::after { content: ''; position: absolute; inset: 4mm; border: 0.5mm dashed #B23A2E; border-radius: 2mm; pointer-events: none; z-index: 3; }",
    "E": ":root { --title-shadow: 0.7mm 0.45mm 0 rgba(255,72,176,0.7); }",
    "A3": ".face-letter, .face-panel { border-left: 3mm solid #0F3B3A; }",
    "B3": ".face-letter .letter-title { letter-spacing: -0.01em; }",
}

with io.open(os.path.join(ROOT, "00-foundations", "hadith-glosses.json"), encoding="utf-8") as _f:
    GLOSSES = __import__("json").load(_f)["glosses"]

CHAIN_03 = ("It begins with him. Everyone else in this box is his family, and every chain of teaching in it "
            "runs back through this one man to the words he was given.")
CHAIN = ("Every card in this box is one link. Lay all fourteen in order and the chain runs from the Prophet "
         "to the last of the twelve, each one passing on what was given.")


def lum(hexcol):
    if not hexcol.startswith("#"):
        return 1.0
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def theme_css(t):
    v, art = t["vars"], t["art"]
    dark_sky = lum(art["sky"]) < 0.42
    band = ("data:image/svg+xml," + quote(
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 60' preserveAspectRatio='none'>{t['band']}</svg>"))
    rules = [f"--{k.replace('_', '-')}: {val};" for k, val in v.items()]
    rules += [f"--display: '{t['fonts'][0]}', Georgia, serif;", f"--body: '{t['fonts'][1]}', Arial, sans-serif;",
              f"--dweight: {t['dweight']};", f"--band: url(\"{band}\");", f"--radius: {RADIUS[t['key']]};",
              f"--head-ink: {v['ground'] if dark_sky else v['ink']};",
              f"--env-ink: {v['ground'] if dark_sky else v['ink']};",
              f"--name-ink: {v['ground'] if lum(v['name_bg']) < 0.42 else v['ink']};",
              f"--chain: {v['card_accent'] if t['card'] in ('blobs', 'quarter', 'stars', 'bands', 'tile') else v['accent']};"]
    return ":root { " + " ".join(rules) + " }\n" + EXTRA.get(t["key"], "")


# ---------------------------------------------------------------- shells

def page(cls, inner, t, band=True, item=""):
    """`item` names the piece for the site's previews (tools/render_envelopes.js)."""
    m = " mourning" if t.get("mourning") else ""
    di = f' data-item="{item}"' if item else ""
    return f'<div class="page {cls}{" band" if band else ""}{m}"{di}>{inner}</div>'


def item(cap, pg):
    return f'<div>{pg}<p class="cap screen-only">{cap}</p></div>'


def group(title, items):
    return f'<section class="group"><h2 class="screen-only">{title}</h2><div class="row">{"".join(items)}</div></section>'


# ---------------------------------------------------------------- art helpers

def pen(t):
    return A.Pen(t["mode"], t["art"], mourning=t.get("mourning", False), heavy=t.get("heavy", False))


# Where the sun or moon goes, as fractions of the box, so it never sits behind a
# minaret, under the postmark, over a title or on top of an object.
SKY_AT = {"print": (0.2, 0.15), "front": (0.17, 0.42), "head": (0.93, 0.3), "object": (0.86, 0.24)}

# Things that stand on the near ground, drawn over it: 03's camel on the dune.
# Height above its foot of each tall object, in its own units, so a print can
# keep its top on the page.
OBJ_HEIGHT = {"tasbih": 76, "scroll": 78, "lantern": 56}

# Fronts that leave the sun top-left: (x, y, size) — a low, large sun sits half
# behind the far dune — or None for no sun. Keeps the fronts from one layout.
FRONT_SUN = {"03": (0.54, 0.64, 1.7), "04": None, "05": (0.3, 0.64, 1.7), "06": (0.8, 0.64, 1.5), "08": (0.84, 0.6), "11": (0.5, 0.34),
             "10": (0.76, 0.68, 1.5), "13": None}

# Where a front object stands, as fractions of the face, when the default
# would put it on the name label (the pen reaches far to its left).
FRONT_AT = {"qalam": (0.66, 0.74), "cloak": (0.66, 0.7)}

FOREGROUND = {
    "quba": lambda p, w, h, base, s: A.camel_standing(p, w * 0.22, base + h * 0.07, s * 1.15),
}


def subject_or_object(p, w, h, key, time, where="print", road_x=0.55, road_half=None, sun="default"):
    at = SKY_AT[where] if sun == "default" else sun
    if key == "road_dawn":
        return A.scene(p, w, h, A.SUBJECTS["road_dawn"], time, road_to=road_x, road_half=road_half, at=at)
    if key in A.SUBJECTS and not (where == "front" and key in FRONT_AT):
        return A.scene(p, w, h, A.SUBJECTS[key], time, at=at, fg=FOREGROUND.get(key))
    obj = A.OBJECTS[key]
    if where == "front":
        # On an envelope front the object sits right of centre, small enough to
        # leave the brand line, the postmark and the name label clear.
        return (A.sky(p, w, h, time, at) + A.dune(p, w, h, h * 0.66, h * 0.06, "far", 0.1)
                + obj(p, w * FRONT_AT.get(key, (0.54, 0.78))[0], h * FRONT_AT.get(key, (0.54, 0.78))[1],
                      min(w, h) / 175)
                + A.dune(p, w, h, h * 0.86, h * 0.05, "mid", -0.1))
    return (A.sky(p, w, h, time, SKY_AT["object"]) + A.dune(p, w, h, h * 0.66, h * 0.06, "far", 0.1)
            + obj(p, w / 2, h * 0.74, min(min(w, h) / 95, h * 0.6 / OBJ_HEIGHT.get(key, 60)))
            + A.dune(p, w, h, h * 0.86, h * 0.05, "mid", -0.1))


def vignette(p, key, x, y, s):
    """A subject or object drawn small, without its sky — for face 3 and cards."""
    if key in A.OBJECTS:
        return A.OBJECTS[key](p, x, y, s)
    if key == "road_dawn":
        # An empty road to a flat horizon, cropped to a window on the face.
        return (f'<clipPath id="rv"><rect x="{x - 40}" y="{y - 50}" width="80" height="56" rx="3"/></clipPath>'
                f'<g clip-path="url(#rv)">' + A.rect(p, x - 40, y - 50, 80, 56, "sky")
                + A.rect(p, x - 40, y - 22, 80, 28, "far", True) + A.road(p, None, y + 6, y - 22, x, half=24) + '</g>'
                + f'<rect x="{x - 40}" y="{y - 50}" width="80" height="56" rx="3" {p.s("shade", 0.5)}/>')
    return A.SUBJECTS[key](p, x, y, s * 0.35)


# ---------------------------------------------------------------- envelope

def stamp_ring(month, number, colour, ground):
    bars = "".join(f'<path d="M50 {y} q6 -3 12 0 t12 0 t12 0 t12 0 t12 0" fill="none" stroke="{colour}" '
                   f'stroke-width="1.3" opacity="0.85"/>' for y in (36, 44, 52, 60))
    return (f'<svg viewBox="0 0 120 96" class="stamp" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><path id="arcTop" d="M14 48 A34 34 0 0 1 82 48"/><path id="arcBot" d="M18 52 A30 30 0 0 0 78 52"/></defs>{bars}'
            f'<circle cx="48" cy="48" r="40" fill="{ground}" stroke="{colour}" stroke-width="2"/>'
            f'<circle cx="48" cy="48" r="27" fill="none" stroke="{colour}" stroke-width="1"/>'
            f'<text style="font-family:var(--body)" font-weight="800" font-size="7" letter-spacing="1.4" fill="{colour}" '
            f'text-anchor="middle"><textPath href="#arcTop" startOffset="50%">{E(month)}</textPath></text>'
            f'<text style="font-family:var(--body)" font-weight="800" font-size="6" letter-spacing="2" fill="{colour}" '
            f'text-anchor="middle"><textPath href="#arcBot" startOffset="50%">NOOR POST</textPath></text>'
            f'<text x="48" y="58" style="font-family:var(--display)" font-size="28" fill="{colour}" text-anchor="middle">{number}</text></svg>')


def seal(colour, inner):
    import math
    pts = []
    for i in range(36):
        a, r = math.pi * i / 18, 48 if i % 2 == 0 else 44
        pts.append(f"{50 + r * math.cos(a):.2f} {50 + r * math.sin(a):.2f}")
    return (f'<svg viewBox="0 0 100 100" class="seal" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<path d="M{" L".join(pts)}Z" fill="{colour}"/>'
            f'<circle cx="50" cy="50" r="34" fill="none" stroke="{inner}" stroke-opacity="0.5" stroke-width="1.4"/>'
            f'<path d="M50 24 L56 41 L74 38 L61 50 L74 62 L56 59 L50 76 L44 59 L26 62 L39 50 L26 38 L44 41Z" '
            f'fill="{inner}" fill-opacity="0.85"/><circle cx="50" cy="50" r="6" fill="{colour}"/></svg>')


def env_front(d, t, sc):
    p = pen(t)
    # 10's road comes in at the bottom right, clear of the name label
    art = A.svg(p, 229, 162, M.render(d["nn"], "front", 229, 162)
                or subject_or_object(p, 229, 162, sc["front"], sc["time"], "front", road_x=0.76, road_half=36,
                                     sun=FRONT_SUN.get(d["nn"], "default")))
    v = t["vars"]
    inner = (art + '<div class="brand"><p class="kicker">Noor Post</p>'
             '<div class="tag">One of fourteen. Open it on the day.</div></div>'
             + stamp_ring(d["stamp"], d["nn"], v["stamp"], v["ground"])
             + '<div class="name-area"><p class="kicker">For</p><div class="who">[Child&#39;s name]</div></div>')
    return page("p-env env-front", inner, t, band=False, item="front")


def env_back(d, t):
    p = pen(t)
    w, h = 229, 162
    v = t["vars"]
    if t["mode"] == "line":
        fl = lambda key: p.f(key)
    else:
        # the flap is the same stock as the body; only its edge band marks it
        fl = lambda key: f'fill="{ {"stock": v["ground2"], "edge": t["art"]["tile"], "flap": v["ground2"]}[key] }"'
    art = (f'<rect width="{w}" height="{h}" {fl("stock")}/>'
           f'<path {fl("edge")} d="M0 0 H229 V16 Q172 50 114.5 86 Q57 50 0 16Z"/>'
           f'<path {fl("flap")} d="M0 0 H229 V10 Q172 42 114.5 78 Q57 42 0 10Z"/>')
    inner = (A.svg(p, w, h, art) + seal(t["vars"]["seal"], t["vars"]["ground"])
             + '<div class="return"><strong>Noor Post</strong><br>[ Return address — not set ]</div>')
    return page("p-env env-back", inner, t, band=False, item="back")


FLAP_RUN = {"conversation": "Talk about it", "mourning": "Sit with it", "case": "Open the case file", "open": "Write one"}


def flap(d, t):
    runs = ['The letter — read it out loud, <span class="mark">●</span> and <span class="mark">○</span> taking turns',
            "The hadith card", "The prints", FLAP_RUN[d["session"]["kind"]],
            "The pennant" if d["mourning"] else "The stickers", "The postcard"]
    clock = ('<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="5" fill="none" '
             'stroke="currentColor" stroke-width="1.2"/><path d="M6 3.2V6l2 1.4" fill="none" stroke="currentColor" '
             'stroke-width="1.2" stroke-linecap="round"/></svg>')
    extra = '<p class="extra">This one has no game in it.</p>' if d["mourning"] else ""
    inner = (f'<div class="flap-block"><div class="lead"><p class="kicker">Envelope {d["nn"]} · {E(d["month"])} · Inside the flap</p>'
             f'<div class="big">Open together.</div><div class="time">{clock} About twenty-five minutes</div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up. <span class="mark">○</span> is you.</p>{extra}</div>'
             f'<ol>{"".join(f"<li><span>{r}</span></li>" for r in runs)}</ol></div>')
    return page("p-flap", inner, t, item="flap")


# ---------------------------------------------------------------- letter

def letter_sheets(d, t, sc):
    p = pen(t)
    body, close = d["voices"][:-1], d["voices"][-1]
    close_text = re.sub(r'<span class="mark">.*?</span>', "", close)
    close_text = re.sub(r"</?p[^>]*>", "", close_text).strip()
    head = A.svg(p, 148.5, 50, M.render(d["nn"], "head", 148.5, 50) or A.scene(p, 148.5, 50, A.SUBJECTS[sc["head"]], sc["time"], ground=0.86,
                                       scale=0.22, cx=0.78, road_to=0.72 if sc["head"] == "road_dawn" else None,
                                       road_half=14, at=SKY_AT["head"]), cls="head-art")
    title = E(d["title"]).replace("-", "\u2011")   # never break "Grown-Ups" at its hyphen
    face1 = (f'<div class="face face-letter first">{head}'
             f'<div class="head-text"><p class="kicker">Envelope {d["nn"]} · {E(d["month"])}</p>'
             f'<h1 class="letter-title">{title}</h1></div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up · <span class="mark">○</span> is you · '
             f'<span class="mark">●○</span> is together</p>'
             f'<div class="letter" data-flow="flow-{d["nn"]}">{"".join(body)}</div><div class="facenum">1</div></div>')
    face2 = (f'<div class="face face-letter"><p class="cont">{E(d["title"])} · continued</p>'
             f'<div class="letter" id="flow-{d["nn"]}"></div><div class="facenum">2</div></div>')
    close_art = A.svg(p, 148.5, 210, M.close_object(d["nn"], 74.25, 176) or vignette(p, sc["hero"], 74.25, 172, 0.8))
    face3 = (f'<div class="face face-close">{close_art}<p class="say">Say this one together</p>'
             f'<p class="together-big"><span class="mark">●○</span>{close_text}</p>'
             f'<p class="next">Then the hadith card.</p><div class="facenum">3</div></div>')
    pn = d["panel"]
    bl = "".join(f'<p class="bullet"><span class="dot">●</span>{b}</p>' for b in pn["bullets"])
    death, rest = (pn["after"][0], pn["after"][1:]) if pn["after"] else ("", [])
    face4 = (f'<div class="face face-panel"><div class="watermark-placeholder"><span>UNVERIFIED — TO VERIFY</span></div>'
             f'<div class="panel" data-fit><p class="kicker">Fact panel</p>'
             f'<h3>{E(pn["name"])}</h3>' + (f'<p class="honorific">{E(pn["honorific"])}</p>' if pn["honorific"] else "")
             + f'<p class="dates">{E(pn["dates"])}</p><hr>{bl}<hr>'
             f'<p class="death-line">{death}</p>' + "".join(f'<p class="standard">{r}</p>' for r in rest)
             + (f'<p class="credit">{pn["credit"]}</p>' if pn["credit"] else "") + '</div><div class="facenum">4</div></div>')
    a = page("p-spread", face4 + '<div class="fold"></div>' + face1, t, band=False, item="side-a")
    b = page("p-spread", face2 + '<div class="fold"></div>' + face3, t, band=False, item="side-b")
    return a, b


# ---------------------------------------------------------------- hadith card

ARCH = "M11 132 V58 A41.5 41.5 0 0 1 94 58 V132Z"
LANTERN = "M38 18 H67 L82 40 L90 62 L90 122 L74 136 H31 L15 122 L15 62 L23 40Z"


def card_art(t):
    p, v, kind = pen(t), t["vars"], t["card"]
    w, h = 105, 148
    bg, acc = v["card_bg"], v["card_accent"]
    if kind == "outline":
        return f'<path d="{ARCH}" fill="none" stroke="{v["ink"]}" stroke-width="0.5"/>'
    if kind == "wash":
        # one wash, one shape: the name sits inside it, not on a second blot
        return f'<g filter="url(#wash)"><path d="{ARCH}" fill="rgba(27,27,27,0.10)"/></g>'
    if kind in ("arch", "garden"):
        inner = (A.star(p, 30, 34, 1.6, "sun") + A.star(p, 74, 28, 1.2, "sun") +
                 A.dune(p, w, h, 120, 7, "far", 0.1) + A.dune(p, w, h, 128, 5, "mid", -0.1))
        if kind == "garden":
            inner = A.dune(p, w, h, 118, 7, "far", 0.1) + A.dune(p, w, h, 127, 5, "near", -0.1)
        return (f'<clipPath id="cc"><path d="{ARCH}"/></clipPath><path d="{ARCH}" fill="{bg}"/>'
                f'<g clip-path="url(#cc)">{inner}</g>'
                + (f'<path d="{ARCH}" fill="none" stroke="{acc}" stroke-width="1.6"/>' if kind == "garden" else ""))
    if kind == "lantern":
        return (f'<path d="M52.5 12 V18" stroke="{acc}" stroke-width="1"/><path d="{LANTERN}" fill="{acc}"/>'
                f'<path d="M40 22 H65 L78 42 L86 63 L86 120 L72 132 H33 L19 120 L19 63 L27 42Z" fill="{bg}"/>'
                f'<path d="M40 138 H65 L58 144 H47Z" fill="{acc}"/>')
    if kind == "frame":
        return (f'<rect x="6" y="14" width="93" height="126" fill="{bg}"/>'
                f'<rect x="8.5" y="16.5" width="88" height="121" fill="none" stroke="{acc}" stroke-width="0.6"/>'
                f'<rect x="10" y="18" width="85" height="118" fill="none" stroke="{acc}" stroke-width="0.25"/>'
                + "".join(A.star(p, x, y, 2.2, "gold") for x, y in ((52.5, 26), (52.5, 126))))
    if kind == "medallion":
        petals = "".join(f'<ellipse cx="52.5" cy="{126 - 9}" rx="2.6" ry="5" fill="{acc}" transform="rotate({a} 52.5 126)"/>'
                         for a in range(0, 360, 45))
        return (f'<rect x="7" y="14" width="91" height="126" rx="4" fill="{bg}"/>'
                f'<rect x="10" y="17" width="85" height="120" rx="3" fill="none" stroke="{acc}" stroke-width="0.5" stroke-dasharray="1.4 1"/>'
                f'<circle cx="52.5" cy="126" r="9" fill="{v["accent"]}"/>{petals}<circle cx="52.5" cy="126" r="3" fill="{bg}"/>')
    if kind == "blobs":
        return (f'<rect width="{w}" height="{h}" fill="{bg}"/><circle cx="6" cy="152" r="40" fill="{v["accent"]}" '
                f'style="mix-blend-mode:multiply"/><circle cx="104" cy="2" r="16" fill="{acc}" opacity="0.8"/>')
    if kind == "quarter":
        return (f'<rect width="{w}" height="{h}" fill="{bg}"/><path d="M105 18 V44 A26 26 0 0 1 79 18Z" fill="{acc}"/>'
                f'<path d="M0 148 V112 A36 36 0 0 1 36 148Z" fill="{acc}"/>')
    if kind == "stars":
        inner_stars = "".join(A.star(p, x, y, 1.4, "sun") for x, y in ((22, 30), (84, 40), (30, 96), (80, 104), (18, 64)))
        return (f'<rect width="{w}" height="{h}" fill="{bg}"/>{inner_stars}' + A.crescent(p, 88, 21, 5, "sun")
                + f'<rect x="4" y="4" width="97" height="140" fill="none" stroke="{acc}" stroke-width="0.6"/>')
    if kind == "bands":
        return (f'<rect width="{w}" height="{h}" fill="{bg}"/><rect y="108" width="{w}" height="10" fill="#F7D9C4"/>'
                f'<rect y="118" width="{w}" height="10" fill="#F2B8A2"/><circle cx="52.5" cy="128" r="11" fill="#E1A73A"/>'
                f'<rect y="128" width="{w}" height="20" fill="#1F2552"/>')
    if kind == "tile":
        cells = "".join(f'<rect x="{x}" y="{y}" width="7" height="7" fill="{c}"/>'
                        for i, (x, y) in enumerate([(x, 0) for x in range(0, 105, 7)] + [(x, 141) for x in range(0, 105, 7)]
                                                   + [(0, y) for y in range(7, 141, 7)] + [(98, y) for y in range(7, 141, 7)])
                        for c in [("#2343A8", "#F2A93B", "#D2483F")[i % 3]])
        return f'<rect width="{w}" height="{h}" fill="{bg}"/>{cells}'
    if kind == "vignette":
        return (f'<g filter="url(#wash)"><ellipse cx="52.5" cy="76" rx="44" ry="58" fill="#86C3D1" fill-opacity="0.35"/>'
                f'<ellipse cx="52.5" cy="140" rx="40" ry="9" fill="#E0A33A" fill-opacity="0.35"/></g>')
    raise ValueError(kind)


def hadith_cards(d, t):
    p = pen(t)
    s = d["saying"]
    seg = None if s.get("segment_conflict") else s.get("segment")
    mark = (f"Silsila segment {seg} of 14" if seg else 'Silsila segment <span class="undecided">––</span> of 14')
    who = "The Prophet Muhammad" if s["masoom"] == "The Prophet" else s["masoom"]
    said = f"{'The Prophet' if s['masoom'] == 'The Prophet' else s['masoom']} said"
    wash_defs = A.Pen("wash", t["art"]).defs() if t["card"] in ("wash", "vignette") else ""
    art = (f'<svg class="art" viewBox="0 0 105 148" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
           f'{wash_defs}{p.defs()}{card_art(t)}</svg>')
    if s.get("text"):
        words = (f'<p class="who-said">{E(said)}</p>'
                 f'<blockquote class="saying">&ldquo;{E(s["text"])}&rdquo;</blockquote><p class="by">{E(who)}</p>')
        mark_wm = ""
    else:
        # No saying is selected. The slot stays empty and says why — no quote
        # marks, no attribution, nothing a screenshot could pass off as a saying.
        words = ('<div class="saying blocked">No saying selected<br><span>Blocked on a source — '
                 'nothing prints here until its row on citation-sheet.md reads V</span></div>')
        mark_wm = '<div class="watermark-placeholder"><span>NO SAYING SELECTED</span></div>'
    front = page(f"p-a6p card-front card-{t['card']}", art + f'<p class="chain-mark">{mark}</p>' + words + mark_wm, t,
                 band=False, item="card-front")
    dots = "".join(f'<span class="{"on" if seg == i else ""}"></span>' for i in range(1, 15))
    gl = GLOSSES.get(d["nn"])
    note = (f'<div class="gloss"><p class="gloss-label">In our words</p><p class="gloss-text">{E(gl)}</p>'
            f'<p class="gloss-note">Noor Post&rsquo;s own words, not the translation.</p></div>' if gl and s.get("text") else "")
    cite = (f'<em>{E(s["work"])}</em>, {E(s["ref"])}. Translated by {E(s["translator"])}, Ansariyan Publications, Qum.'
            if s.get("text") else f'<strong>Blocked:</strong> {E(s.get("blocker", ""))}')
    back = page("p-a6p", f'<div class="card-back"><p class="kicker">Noor Post · The Fourteen</p><h3>The chain</h3>'
                f'<p>{CHAIN_03 if d["nn"] == "03" else CHAIN}</p><div class="chain-dots">{dots}</div>'
                f'<p class="note">Fourteen segments · historical order</p>{note}<p class="cite">{cite}</p></div>', t, item="card-back")
    text = re.sub(r"<[^>]+>", " ", front + back)
    if re.search(r"\benvelope\b|\b0\d\b", text, re.I):
        raise SystemExit(f"envelope {d['nn']}: a hadith card carries an envelope number — design-system.md §7")
    return front, back


# ---------------------------------------------------------------- session

def session_pages(d, t):
    s = d["session"]
    kind = s["kind"]
    if kind == "conversation":
        def q(label, flag, text):
            n = '<span class="n last">Last</span>' if label == "Last" else f'<span class="n">{label}</span>'
            fl = f'<span class="flagline">{E(flag)}</span>' if flag else ""
            return f'<div class="q">{n}<div class="t">{fl}{text}</div></div>'
        front = [x for x in s["questions"] if x[0] in ("1", "2", "3")]
        back = [x for x in s["questions"] if x[0] not in ("1", "2", "3")]
        f = (f'<div class="session" data-fit><h2 class="s-title">{E(s["title"])}</h2><p class="s-sub">{E(s["sub"])}</p>'
             + "".join(q(*x) for x in front) + '<p class="over">Turn over →</p></div>')
        b = (f'<div class="session" data-fit><p class="kicker">{E(s["title"])} · continued</p>'
             + "".join(q(*x) for x in back) + "</div>")
        return [("Session card — front", page("p-a6p", f, t, item="session")), ("Session card — back", page("p-a6p", b, t))]
    if kind == "mourning":
        blk = "".join('<div class="blk">' + "".join(f"<p>{x}</p>" for x in b) + "</div>" for b in s["blocks"])
        f = (f'<div class="session" data-fit><h2 class="s-title">{E(s["title"])}</h2><p class="s-sub">{E(s["sub"])}</p>'
             f'{blk}</div>')
        return [("Session card — one side", page("p-a6p", f, t, item="session"))]
    if kind == "open":
        blocks = s["blocks"]
        sizes = [sum(len(x) for x in b) for b in blocks]
        cut, run = len(blocks), 0
        for i, n in enumerate(sizes):
            if run + n / 2 > sum(sizes) / 2:
                cut = max(1, i); break
            run += n
        blk = lambda bs: "".join('<div class="blk">' + "".join(f"<p>{x}</p>" for x in b) + "</div>" for b in bs)
        f = (f'<div class="session" data-fit><h2 class="s-title">{E(s["title"])}</h2><p class="s-sub">{E(s["sub"])}</p>'
             f'{blk(blocks[:cut])}<p class="over">Turn over →</p></div>')
        b = f'<div class="session" data-fit><p class="kicker">{E(s["title"])} · continued</p>{blk(blocks[cut:])}</div>'
        return [("Session card — front", page("p-a6p", f, t, item="session")), ("Session card — back", page("p-a6p", b, t))]
    # case file: a question card, five evidence cards, a sealed answer
    out = [("Case file — the question", page("p-a6p", f'<div class="session" data-fit><p class="kicker">The case file</p>'
            f'<h2 class="s-title">The question</h2><p class="case-q">{s["question"]}</p>'
            f'<p class="s-sub">Five evidence cards. Read them in any order. Then say your answer out loud, before '
            f'anyone opens the sealed card.</p></div>', t, item="session"))]
    for ev in s["evidence"]:
        out.append((f"Evidence {ev['n']}", page("p-a7p", f'<div class="evidence" data-fit><p class="kicker">Evidence</p>'
                    f'<div class="ev-n">{ev["n"]}</div>' + "".join(f"<p>{x}</p>" for x in ev["text"]) + "</div>", t)))
    out.append(("Sealed answer — outside", page("p-a6p", f'<div class="sealed-front"><div class="seal-word">Sealed</div>'
                f'<p>{s["instruction"]}</p></div>', t)))
    out.append(("Sealed answer — inside", page("p-a6p", '<div class="answer" data-fit><p class="kicker">The answer</p>'
                + "".join(f"<p>{x}</p>" for x in s["answer"]) + "</div>", t)))
    return out


# ---------------------------------------------------------------- prints, stickers, pennant, postcard

def person_print(d, t, sc):
    p = pen(t)
    return page("p-a5p", A.svg(p, 148, 210, M.render(d["nn"], "person", 148, 210)
                               or subject_or_object(p, 148, 210, sc["person"], sc["time"], "print")), t, band=False,
                item="person")


def event_print(d, t, sc):
    p = pen(t)
    return page("p-a5l", A.svg(p, 210, 148, M.render(d["nn"], "event", 210, 148)
                               or subject_or_object(p, 210, 148, sc["event"], sc["time"], "print"))
                + '<div class="punch" title="Ring punch: 6 mm, centred, 12 mm from the top"></div>', t, band=False, item="event")


def stickers(d, t, sc):
    p = pen(t)
    kiss = ('<filter id="kiss" x="-25%" y="-25%" width="150%" height="150%">'
            '<feMorphology in="SourceAlpha" operator="dilate" radius="1.8" result="d"/>'
            '<feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>'
            '<feDropShadow in="w" dx="0" dy="0.4" stdDeviation="0.5" flood-color="#000000" flood-opacity="0.25" result="ws"/>'
            '<feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    slots = [(30, 44), (76, 44), (30, 92), (76, 92), (30, 138), (76, 138)]
    body = f'<defs>{kiss}</defs><rect width="105" height="148" fill="#FFFFFF"/>'
    for (x, y), key in zip(slots, sc["stickers"]):
        body += f'<g filter="url(#kiss)">{A.OBJECTS[key](p, x, y, 0.5)}</g>'
    return page("p-a6p", A.svg(p, 105, 148, body), t, band=False, item="stickers")


def pennant(d, t, sc):
    p = pen(t)
    ink, ivory = t["vars"]["ink"], t["vars"]["ground"]
    clip = '<clipPath id="pen"><path d="M22 26 H126 L74 192Z"/></clipPath>'
    motif = (A.standard(p, 74, 152, 0.62) if sc["event"] == "standard"
             else A.treaty(p, 74, 104, 0.76))  # the treaty, not a road: a road's taper echoes the pennant's own outline
    body = (f'{clip}<rect width="148" height="210" fill="{ivory}"/>'
            f'<path d="M0 22 Q74 30 148 22" fill="none" stroke="{ink}" stroke-width="0.6"/>'
            f'<path d="M22 26 H126 L74 192Z" fill="{ivory}" stroke="{ink}" stroke-width="0.5" stroke-dasharray="2 1.2"/>'
            f'<g clip-path="url(#pen)">{motif}</g><path d="M22 26 H126 V34 H22Z" fill="none" stroke="{ink}" stroke-width="0.4"/>')
    return page("p-a5p", A.svg(p, 148, 210, body), t, band=False, item="pennant")


def postcard_front(d, t, sc):
    p = pen(t)
    return page("p-a6l", A.svg(p, 148, 105, M.render(d["nn"], "postcard", 148, 105)
                               or subject_or_object(p, 148, 105, sc["postcard"], sc["time"], "print")), t, band=False,
                item="postcard")


def postcard_back(d, t):
    inner = ('<div class="pc-back"><div class="msg"><div class="big">We opened this one together.</div>'
             '<div class="sig"><span>●</span><span class="line"></span></div>'
             '<div class="sig"><span>○</span><span class="line"></span></div>'
             '<p class="small">Post it back to us, or keep it. Either is right.</p></div>'
             '<div class="addr"><div class="stampbox">Stamp</div><div class="to"><strong>Noor Post</strong>'
             '<div>[ Return address — not set ]</div><div class="ln"></div><div class="ln"></div></div></div></div>')
    return page("p-a6l", inner, t)


# ---------------------------------------------------------------- driver

def build(nn):
    d = S.load(nn)
    t, sc = THEMES[nn], SCENES[nn]
    sa, sb = letter_sheets(d, t, sc)
    cf, cb = hadith_cards(d, t)
    groups = [
        group("Envelope — C5, 229 × 162 mm", [item("Front", env_front(d, t, sc)), item("Back, with the seal", env_back(d, t))]),
        group("Inside the flap", [item("Running order and runtime", flap(d, t))]),
        group("The letter — one A4 sheet folded to A5", [
            item("Side A: face 4, the fact panel | face 1, the letter opens", sa),
            item("Side B: face 2, the letter continues | face 3, the line said together", sb)]),
        group("Hadith card — A6", [item("Front", cf), item("Back — no envelope number anywhere", cb)]),
        group({"case": "The case file", "conversation": "Session card", "mourning": "Session card — mourning",
               "open": "Session card — open"}[d["session"]["kind"]],
              [item(c, pg) for c, pg in session_pages(d, t)]),
        group("Prints — A5", [item("Person print", person_print(d, t, sc)),
                              item(f"Event print — ring position {int(nn)}. Red dashed circle = punch, screen only",
                                   event_print(d, t, sc))]),
        group("Pennant" if d["mourning"] else "Sticker sheet — A6, kiss-cut",
              [item("Pennant — replaces the stickers in a mourning issue", pennant(d, t, sc)) if d["mourning"]
               else item("Stickers", stickers(d, t, sc))]),
        group("Return postcard — A6 landscape", [item("Front", postcard_front(d, t, sc)), item("Back", postcard_back(d, t))]),
    ]
    head = (f'<h1>Envelope {nn} · {E(d["month"])} · {E(d["title"])}</h1>'
            f'<p><strong>Style {t["key"]} — {E(t["name"])}.</strong> {E(t["fonts"][0])} and {E(t["fonts"][1])}. '
            f'Every word read from source; every drawing from tools/envelope_art.py, which has no figure in it.</p>'
            f'<p>Still open where it shows: the fact panel is TO VERIFY and the return address is not set.</p>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Envelope {nn} — {E(t["name"])}</title>
<link rel="stylesheet" href="envelope.css">
<style>{theme_css(t)}</style>
<script defer src="envelope.js"></script>
</head><body class="{"mourning" if d["mourning"] else ""}">
<header class="set-head screen-only">{head}</header>
{"".join(groups)}
</body></html>
"""


def index():
    rows = ""
    for nn in S.ALL:
        d, t = S.load(nn), THEMES[nn]
        v = t["vars"]
        rows += (f'<a class="tile" href="envelope-{nn}.html" style="background:{t["art"]["sky"]};border-color:{v["accent"]}">'
                 f'<span class="n" style="color:{v["head_ink"] if "head_ink" in v else v["ink"]}">{nn}</span>'
                 f'<span class="m">{E(d["month"])}</span><span class="t">{E(d["title"])}</span>'
                 f'<span class="s">{t["key"]} · {E(t["name"])}</span></a>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Noor Post — the fourteen envelopes</title>
<style>
body {{ margin: 0; padding: 32px 16px; background: #F4EFE6; color: #2A2230; font-family: Georgia, serif; }}
main {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: 32px; margin: 0 0 6px; }} p {{ color: #5E5262; margin: 0 0 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }}
.tile {{ display: flex; flex-direction: column; gap: 4px; padding: 16px; border-radius: 8px; border-bottom: 6px solid; text-decoration: none; min-height: 150px; }}
.tile span {{ background: rgba(255,255,255,0.86); color: #2A2230; padding: 1px 6px; align-self: flex-start; border-radius: 3px; }}
.n {{ font-size: 28px; background: none !important; }} .t {{ font-weight: bold; }} .m, .s {{ font-size: 13px; }}
</style></head><body><main>
<h1>The fourteen envelopes</h1><p>Fourteen styles, one structure. Open one to see every item at true size; print it to PDF with no margins.</p>
<div class="grid">{rows}</div></main></body></html>
"""


def main():
    check = "--check" in sys.argv
    files = {f"envelope-{nn}.html": build(nn) for nn in S.ALL}
    files["index.html"] = index()
    stale = 0
    for name, content in files.items():
        path = os.path.join(OUT, name)
        old = io.open(path, encoding="utf-8").read() if os.path.exists(path) else None
        stale += old != content
        if not check:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
    print(f"envelopes: {len(files) - 1} built, {stale} {'stale' if check else 'written'}")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()

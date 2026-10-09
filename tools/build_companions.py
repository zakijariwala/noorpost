#!/usr/bin/env python3
"""Build the companions line — Everyone Else — every item, one file each.

    python tools/build_companions.py           # write 04-art/companions/
    python tools/build_companions.py --check   # exit 1 if anything on disk is stale

One file per companion, 04-art/companions/companion-<slug>.html, printing
straight to one PDF with every item at its own size: envelope front and back,
inside flap, the letter as one A4 sheet folded to four A5 faces (the fact
panel on its reverse), hadith card, person print, sticker sheet and the return
postcard. Five items, per 08-companions/README.md, and never an event print.

One style for the whole line (tools/companion_themes.LINE): thirty-nine
envelopes that belong together, like a set of stamps — each front carries its
person as a large perforated stamp. Each person brings their own colours,
place and portrait (tools/companion_art.py; faces are allowed in this line).
Only companions in a finished batch (companion_themes.BUILT) are written.

The line's rules, checked here and in tests/test_companions.py:
  - the card's chain is FIRST EDITION nn/39 and never a silsila segment number
  - no event print, ever
  - an unselected saying prints an empty, marked slot — never filler
  - every word of the letter and the panel comes from the entry file
"""

import html, io, json, math, os, re, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envelope_art as A
import companion_art as C
import companion_sources as S
from companion_themes import LINE, PEOPLE, BUILT
from build_envelopes import page, item, group, lum

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "04-art", "companions")
E = html.escape

with io.open(os.path.join(ROOT, "00-foundations", "hadith-glosses.json"), encoding="utf-8") as _f:
    GLOSSES = json.load(_f).get("companions", {})

PUBLISHER = {"Tuhaf al-Uqul": "Ansariyan Publications, Qum"}


# ---------------------------------------------------------------- style

def pen(t):
    return A.Pen(LINE["mode"], t["art"])


def theme(slug):
    t = dict(PEOPLE[slug])
    c, c2 = t["colour"], t["colour2"]
    t["vars"] = dict(ground="#FFFBF3", ground2=t["tint"], ink="#2A2230", soft="#5E5262", accent=c, child=c, bar=c2,
                     pill=t["tint"], pill_ink="#2A2230", card_bg=c, card_ink="#2A2230", card_accent=c, seal=c,
                     name_bg="#FFFFFF", stamp=c)
    return t


def css(t):
    v = t["vars"]
    scallops = "".join(f"<circle cx='{x}' cy='0' r='4' fill='%23FFFBF3'/>" for x in range(4, 400, 12))
    band = ("data:image/svg+xml," + quote(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 60' "
                                          f"preserveAspectRatio='none'><rect width='400' height='60' fill='{t['colour']}'/>")
            + scallops + "</svg>")
    dark = lum(t["art"]["sky"]) < 0.42
    rules = [f"--{k.replace('_', '-')}: {val};" for k, val in v.items()]
    rules += [f"--display: '{LINE['fonts'][0]}', Georgia, serif;", f"--body: '{LINE['fonts'][1]}', Arial, sans-serif;",
              f"--dweight: {LINE['dweight']};", f"--band: url(\"{band}\");", "--radius: 2.5mm;",
              f"--head-ink: {v['ground'] if dark else v['ink']};", f"--env-ink: {v['ink']};", f"--name-ink: {v['ink']};",
              f"--chain: {t['colour']};", "--facenum: #FFFBF3;", "--letter-pt: 11.5pt;", "--panel-pt: 11pt;"]
    return ":root { " + " ".join(rules) + " }"


# ---------------------------------------------------------------- the stamp

def perforated(x, y, w, h, paper, hole, r=1.9, step=5.2):
    """A sheet of stamp paper with its perforation bites, drawn in `hole`."""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{paper}"/>'
    nx, ny = max(2, round(w / step)), max(2, round(h / step))
    for i in range(nx + 1):
        cx = x + w * i / nx
        out += f'<circle cx="{cx:.2f}" cy="{y}" r="{r}" fill="{hole}"/><circle cx="{cx:.2f}" cy="{y + h}" r="{r}" fill="{hole}"/>'
    for j in range(1, ny):
        cy = y + h * j / ny
        out += f'<circle cx="{x}" cy="{cy:.2f}" r="{r}" fill="{hole}"/><circle cx="{x + w}" cy="{cy:.2f}" r="{r}" fill="{hole}"/>'
    return out


def place(p, t, w, h, at=None):
    """(back, front) of the person's place, from a backdrop key or a place spec."""
    bd = t["backdrop"]
    if isinstance(bd, dict):
        return C.compose(p, w, h, t["time"], bd, at)
    kw = {"at": at} if at else {}
    return C.BACKDROPS[bd](p, w, h, t["time"], **kw)


def portrait(p, t, w, h, figure_scale=1.0, at=None):
    """The person in their place, filling a w × h box: backdrop, figure, foreground."""
    back, front = place(p, t, w, h, at)
    if t["figure"] is None:          # Fitrus: the feather stands in for the figure
        return back + front
    sp = dict(t["figure"])
    sp.setdefault("trim", t["colour2"])
    # no two people hold their heads the same way: a small tilt, a glance, for some a smile
    k = sum(map(ord, t["colour"]))
    sp.setdefault("tilt", (-5, -2.5, 3, 5, 0, -3.5, 2)[k % 7])
    sp.setdefault("gaze", (-0.6, 0.5, 0, 0.6, -0.4)[k % 5])
    if sp.get("mouth", "closed") == "closed" and k % 3 == 0:
        sp["mouth"] = "smile"
    if isinstance(sp.get("prop"), str):
        sp["prop"] = C.PROPS[sp["prop"]]
    s = h * 0.74 / 125 * figure_scale * t.get("scale", 1.0)
    return back + C.figure(p, w / 2 + w * t.get("dx", 0), h + 1, s, sp) + front


def stamp(p, d, t, x, y, w, h, hole, clip_id, rot=-2.5):
    """The line's stamp: perforated paper, a coloured frame, the portrait, the name."""
    c = t["colour"]
    m = w * 0.056
    pic_x, pic_y, pic_w, pic_h = x + m, y + m, w - 2 * m, h - m - h * 0.167
    inner = (f'<clipPath id="{clip_id}"><rect x="0" y="0" width="{pic_w}" height="{pic_h}"/></clipPath>'
             f'<g transform="translate({pic_x} {pic_y})"><g clip-path="url(#{clip_id})">{portrait(p, t, pic_w, pic_h)}</g></g>')
    name = d["name"].upper()
    fs = min(w * 0.053, (w - 2 * m - 6) / (len(name) * 0.8))
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})" filter="url(#lift)">'
            + perforated(x, y, w, h, "#FFFDF8", hole)
            + f'<rect x="{x + m * 0.65:.2f}" y="{y + m * 0.65:.2f}" width="{w - m * 1.3:.2f}" height="{h - m * 1.3:.2f}" fill="{c}"/>'
            + inner
            + f'<text x="{x + w / 2}" y="{y + h - w * 0.106:.2f}" text-anchor="middle" style="font-family:var(--display)" '
              f'font-weight="700" font-size="{fs:.2f}" letter-spacing="{w * 0.005:.2f}" fill="#FFFDF8">{E(name)}</text>'
            + f'<text x="{x + w / 2}" y="{y + h - w * 0.061:.2f}" text-anchor="middle" style="font-family:var(--body)" '
              f'font-weight="800" font-size="{w * 0.0255:.2f}" letter-spacing="{w * 0.009:.2f}" fill="{t["colour2"]}">'
              f'FIRST EDITION · {d["n"]:02d}/39</text></g>')


def airmail(t, w, h, b=5.5):
    """The line's border: airmail stripes in the person's two inks, all the way round."""
    pat = (f'<pattern id="am" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           f'<rect width="14" height="14" fill="#FFFBF3"/><rect width="4.5" height="14" fill="{t["colour"]}"/>'
           f'<rect x="7" width="4.5" height="14" fill="{t["colour2"]}"/></pattern>')
    return (f'<defs>{pat}</defs><path fill="url(#am)" fill-rule="evenodd" '
            f'd="M0 0 H{w} V{h} H0Z M{b} {b} V{h - b} H{w - b} V{b}Z"/>')


LIFT = ('<filter id="lift" x="-10%" y="-10%" width="120%" height="125%">'
        '<feDropShadow dx="0.6" dy="1.4" stdDeviation="1.2" flood-color="#2A2230" flood-opacity="0.28"/></filter>')


def line_seal(colour, ground):
    """The line's plain seal: no month, no cancellation bars — these are dateless."""
    return (f'<svg viewBox="0 0 96 96" class="ee-seal" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><path id="eeTop" d="M14 48 A34 34 0 0 1 82 48"/><path id="eeBot" d="M16 50 A32 32 0 0 0 80 50"/></defs>'
            f'<circle cx="48" cy="48" r="40" fill="none" stroke="{colour}" stroke-width="2"/>'
            f'<circle cx="48" cy="48" r="27" fill="none" stroke="{colour}" stroke-width="1"/>'
            f'<text style="font-family:var(--body)" font-weight="800" font-size="7" letter-spacing="1.6" fill="{colour}" '
            f'text-anchor="middle"><textPath href="#eeTop" startOffset="50%">NOOR POST</textPath></text>'
            f'<text style="font-family:var(--body)" font-weight="800" font-size="6" letter-spacing="1.5" fill="{colour}" '
            f'text-anchor="middle"><textPath href="#eeBot" startOffset="50%">EVERYONE ELSE</textPath></text>'
            f'<path d="M48 36 L51 45 L60 45 L53 50.5 L55.5 59 L48 54 L40.5 59 L43 50.5 L36 45 L45 45Z" fill="{colour}"/></svg>')


# ---------------------------------------------------------------- envelope

def env_front(d, t):
    p = pen(t)
    w, h = 229, 162
    body = (f'<defs>{LIFT}</defs><rect width="{w}" height="{h}" fill="{t["tint"]}"/>' + airmail(t, w, h)
            + stamp(p, d, t, 116, 14, 98, 132, t["tint"], "sf"))
    inner = (A.svg(p, w, h, body + C.grain(w, h, 0.35))
             + f'<div class="brand"><p class="kicker">Noor Post · Everyone Else</p>'
               f'<div class="tag{" long" if len(d["points"]) > 95 else ""}">{E(d["points"])}</div></div>'
             + line_seal(t["colour"], t["tint"])
             + '<div class="name-area"><p class="kicker">For</p><div class="who">[Child&#39;s name]</div></div>')
    return page("p-env env-front ee-front", inner, t, band=False, item="front")


def env_back(d, t):
    p = pen(t)
    w, h = 229, 162
    art = (f'<rect width="{w}" height="{h}" fill="{t["tint"]}"/>'
           f'<path fill="{t["colour"]}" d="M0 0 H229 V16 Q172 50 114.5 86 Q57 50 0 16Z"/>'
           f'<path fill="{t["tint"]}" d="M0 0 H229 V10 Q172 42 114.5 78 Q57 42 0 10Z"/>')
    inner = (A.svg(p, w, h, art + C.grain(w, h, 0.3)) + line_seal(t["colour"], t["tint"]).replace('class="ee-seal"', 'class="seal"')
             + '<div class="return"><strong>Noor Post</strong><br>[ Return address — not set ]</div>')
    return page("p-env env-back", inner, t, band=False, item="back")


def flap(d, t):
    runs = ['The letter — read it out loud, <span class="mark">●</span> and <span class="mark">○</span> taking turns',
            "The hadith card", "The print", "The stickers", "The postcard"]
    inner = (f'<div class="flap-block"><div class="lead"><p class="kicker">Everyone Else · {E(d["name"])} · Inside the flap</p>'
             f'<div class="big">Open together.</div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up. <span class="mark">○</span> is you.</p></div>'
             f'<ol>{"".join(f"<li><span>{r}</span></li>" for r in runs)}</ol></div>')
    return page("p-flap", inner, t, item="flap")


# ---------------------------------------------------------------- letter

def hero(p, t, x, y, s):
    key = t["hero"]
    fn = C.OBJECTS.get(key) or A.OBJECTS[key]
    return fn(p, x, y, s)


def letter_sheets(d, t):
    p = pen(t)
    body, close = d["voices"][:-1], d["voices"][-1]
    close_text = re.sub(r'<span class="mark">.*?</span>', "", close)
    close_text = re.sub(r"</?p[^>]*>", "", close_text).strip()
    # the head strip: their sky and ground, and their object small at the right, clear of the title
    head = A.svg(p, 148.5, 50, C.sky(p, 148.5, 50, t["time"], (0.93, 0.3)) + A.dune(p, 148.5, 50, 36, 3, "far", 0.1)
                 + hero(p, t, 130, 44, 0.42) + A.dune(p, 148.5, 50, 44, 2, "mid", -0.1) + C.grain(148.5, 50, 0.4), cls="head-art")
    title = E(d["title"]).replace("-", "‑")
    face1 = (f'<div class="face face-letter first">{head}'
             f'<div class="head-text"><p class="kicker">Everyone Else · {E(d["name"])}</p>'
             f'<h1 class="letter-title">{title}</h1></div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up · <span class="mark">○</span> is you · '
             f'<span class="mark">●○</span> is together</p>'
             f'<div class="letter" data-flow="flow-{d["slug"]}">{"".join(body)}</div><div class="facenum">1</div></div>')
    face2 = (f'<div class="face face-letter"><p class="cont">{E(d["title"])} · continued</p>'
             f'<div class="letter" id="flow-{d["slug"]}"></div><div class="facenum">2</div></div>')
    close_art = A.svg(p, 148.5, 210, hero(p, t, 74.25, 178, 1.0))
    face3 = (f'<div class="face face-close">{close_art}<p class="say">Say this one together</p>'
             f'<p class="together-big"><span class="mark">●○</span>{close_text}</p>'
             f'<p class="next">Then the hadith card.</p><div class="facenum">3</div></div>')
    pn = d["panel"]
    face4 = (f'<div class="face face-panel"><div class="watermark-placeholder"><span>UNVERIFIED — TO VERIFY</span></div>'
             f'<div class="panel" data-fit><p class="kicker">Fact panel</p><h3>{E(d["name"])}</h3><hr>'
             + "".join(x.replace("<p>", '<p class="death-line">', 1) for x in pn["parts"])
             + '</div><div class="facenum">4</div></div>')
    a = page("p-spread", face4 + '<div class="fold"></div>' + face1, t, band=False, item="side-a")
    b = page("p-spread", face2 + '<div class="fold"></div>' + face3, t, band=False, item="side-b")
    return a, b


# ---------------------------------------------------------------- hadith card

def stamp_grid(n, colour):
    """Thirty-nine small stamps, this card's one filled: the line's own chain."""
    cells = ""
    for i in range(39):
        cx, cy = 4 + (i % 13) * 6.4, 4 + (i // 13) * 7.6
        on = i + 1 == n
        cells += (f'<rect x="{cx - 2.3}" y="{cy - 2.8}" width="4.6" height="5.6" rx="0.4" '
                  + (f'fill="{colour}"/>' if on else f'fill="none" stroke="{colour}" stroke-width="0.35"/>'))
    return f'<svg class="ee-grid" viewBox="0 0 84 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{cells}</svg>'


def hadith_cards(d, t):
    p = pen(t)
    s = d["saying"]
    mark = f"First edition · {d['n']:02d}/39"
    masoom = s.get("masoom") or ""
    who = "The Prophet Muhammad" if masoom.lower() == "the prophet" else masoom[:1].upper() + masoom[1:]
    said = ("The Prophet" if masoom.lower() == "the prophet" else who) + " said"
    art = (f'<svg class="art" viewBox="0 0 105 148" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{p.defs()}'
           f'<rect width="105" height="148" fill="{t["colour"]}"/>' + perforated(8, 8, 89, 132, "#FFFBF3", t["colour"], r=1.6, step=4.6)
           + f'<rect x="12" y="12" width="81" height="124" fill="none" stroke="{t["colour2"]}" stroke-width="0.5"/>'
           + A.star(p, 52.5, 121, 2.6, t["colour2"]) + '</svg>')
    if s.get("text"):
        words = (f'<p class="who-said">{E(said)}</p>'
                 f'<blockquote class="saying">&ldquo;{E(s["text"])}&rdquo;</blockquote><p class="by">{E(who)}</p>')
        wm = ('<div class="watermark-placeholder"><span>UNVERIFIED SELECTION</span></div>'
              if s.get("confidence") in ("low", "medium") else "")
    else:
        why = ("Blocked on a decision — this entry points to no Masoom and awaits a scholar call"
               if not masoom else "Blocked on a source — nothing prints here until its row on citation-sheet.md reads V")
        words = f'<div class="saying blocked">No saying selected<br><span>{why}</span></div>'
        wm = '<div class="watermark-placeholder"><span>NO SAYING SELECTED</span></div>'
    front = page("p-a6p card-front card-ee", art + f'<p class="chain-mark">{mark}</p>' + words
                 + '<p class="own-chain">Not a silsila segment · this set has its own chain</p>' + wm, t,
                 band=False, item="card-front")
    gl = GLOSSES.get(d["slug"])
    note = (f'<div class="gloss"><p class="gloss-label">In our words</p><p class="gloss-text">{E(gl)}</p>'
            f'<p class="gloss-note">Noor Post&rsquo;s own words, not the translation.</p></div>' if gl and s.get("text") else "")
    if s.get("text"):
        pub = PUBLISHER.get(s["work"])
        cite = (f'<em>{E(s["work"])}</em>, {E(s["ref"])}. Translated by {E(s["translator"])}'
                + (f", {E(pub)}." if pub else "."))
    else:
        cite = f'<strong>Blocked:</strong> {E(s.get("blocker", "no saying selected"))}'
    back = page("p-a6p", f'<div class="card-back"><p class="kicker">Noor Post · Everyone Else</p><h3>The other chain</h3>'
                f'<p>The box holds fourteen cards, one for each of the Fourteen. This set is the people around them: '
                f'thirty-nine cards, collected in any order.</p>{stamp_grid(d["n"], t["colour"])}'
                f'<p class="note">First edition · thirty-nine cards</p>{note}<p class="cite">{cite}</p></div>', t, item="card-back")
    text = re.sub(r"<[^>]+>", " ", front + back)
    if re.search(r"segment\s+\d|segment\s+<", front + back) or re.search(r"\bsegment \d+ of 14\b", text):
        raise SystemExit(f"{d['slug']}: a companion card carries a silsila segment number — 08-companions/README.md")
    return front, back


# ---------------------------------------------------------------- print, stickers, postcard

def person_print(d, t):
    p = pen(t)
    body = portrait(p, t, 148, 210, figure_scale=1.05)
    n = len(d["name"])
    pw = max(80, min(128, n * 2.9 + 16))                      # the plate grows with the name
    fs = min(5.4, (pw - 10) / (n * 0.5))
    plate = (f'<rect x="{74 - pw / 2:.1f}" y="188" width="{pw:.1f}" height="13" rx="2" fill="#FFFBF3" filter="url(#lift)"/>'
             f'<text x="74" y="196.6" text-anchor="middle" style="font-family:var(--display)" font-weight="700" '
             f'font-size="{fs:.2f}" fill="{t["colour"]}">{E(d["name"])}</text>')
    return page("p-a5p", A.svg(p, 148, 210, f"<defs>{LIFT}</defs>" + body + C.grain(148, 210) + plate), t, band=False, item="person")


def stickers(d, t):
    p = pen(t)
    kiss = ('<filter id="kiss" x="-25%" y="-25%" width="150%" height="150%">'
            '<feMorphology in="SourceAlpha" operator="dilate" radius="1.8" result="d"/>'
            '<feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>'
            '<feDropShadow in="w" dx="0" dy="0.4" stdDeviation="0.5" flood-color="#000000" flood-opacity="0.25" result="ws"/>'
            '<feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    body = f'<defs>{kiss}{LIFT}</defs><rect width="105" height="148" fill="#FFFFFF"/>'
    # the person's own stamp, small — the one sticker every envelope in the line has
    body += stamp(p, d, t, 9, 10, 40, 54, "#FFFFFF", "ss", rot=-4)
    slots = [(76, 44), (30, 98), (76, 98), (30, 140), (76, 140)]
    for (x, y), key in zip(slots, t["stickers"]):
        fn = C.OBJECTS.get(key) or A.OBJECTS[key]
        body += f'<g filter="url(#kiss)">{fn(p, x, y, 0.5)}</g>'
    return page("p-a6p", A.svg(p, 105, 148, body), t, band=False, item="stickers")


def postcard_front(d, t):
    p = pen(t)
    pc = t["postcard"]
    if isinstance(pc, dict):
        back, front = C.compose(p, 148, 105, t["time"], pc)
        art = back + front
    else:
        art = C.POSTCARDS[pc](p, 148, 105, t["time"])
    return page("p-a6l", A.svg(p, 148, 105, art + C.grain(148, 105)), t, band=False, item="postcard")


def postcard_back(d, t):
    inner = ('<div class="pc-back"><div class="msg"><div class="big">We opened this one together.</div>'
             '<div class="sig"><span>●</span><span class="line"></span></div>'
             '<div class="sig"><span>○</span><span class="line"></span></div>'
             '<p class="small">Post it back to us, or keep it. Either is right.</p></div>'
             '<div class="addr"><div class="stampbox">Stamp</div><div class="to"><strong>Noor Post</strong>'
             '<div>[ Return address — not set ]</div><div class="ln"></div><div class="ln"></div></div></div></div>')
    return page("p-a6l", inner, t)


# ---------------------------------------------------------------- driver

def build(slug):
    d, t = S.load(slug), theme(slug)
    sa, sb = letter_sheets(d, t)
    cf, cb = hadith_cards(d, t)
    groups = [
        group("Envelope — C5, 229 × 162 mm", [item("Front — the stamp", env_front(d, t)), item("Back, with the seal", env_back(d, t))]),
        group("Inside the flap", [item("Running order", flap(d, t))]),
        group("1 · The letter — one A4 sheet folded to A5", [
            item("Side A: face 4, the fact panel | face 1, the letter opens", sa),
            item("Side B: face 2, the letter continues | face 3, the line said together", sb)]),
        group("2 · Hadith card — A6", [item("Front", cf), item("Back — its own chain, no silsila number", cb)]),
        group("3 · Person print — A5", [item("Portrait", person_print(d, t))]),
        group("4 · Sticker sheet — A6, kiss-cut", [item("Stickers", stickers(d, t))]),
        group("5 · Return postcard — A6 landscape", [item("Front", postcard_front(d, t)), item("Back", postcard_back(d, t))]),
    ]
    head = (f'<h1>Everyone Else · {d["n"]:02d}/39 · {E(d["name"])}</h1>'
            f'<p><strong>{E(d["title"])}.</strong> {E(d["points"])} Five items, no event print, dateless.</p>'
            f'<p>One style for the whole line — {E(LINE["fonts"][0])} and {E(LINE["fonts"][1])}, cut paper, the person '
            f'on a stamp. Still open where it shows: the fact panel is TO VERIFY and the return address is not set.</p>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(d["name"])} — Everyone Else</title>
<link rel="stylesheet" href="companion.css">
<style>{css(t)}</style>
<script defer src="../envelopes/envelope.js"></script>
</head><body>
<header class="set-head screen-only">{head}</header>
{"".join(groups)}
</body></html>
"""


def index():
    rows = ""
    for slug in BUILT:
        d, t = S.load(slug), PEOPLE[slug]
        rows += (f'<a class="tile" href="companion-{slug}.html" style="background:{t["tint"]};border-color:{t["colour"]}">'
                 f'<span class="n" style="color:{t["colour"]}">{d["n"]:02d}</span>'
                 f'<span class="t">{E(d["name"])}</span><span class="m">{E(d["title"])}</span></a>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Noor Post — Everyone Else</title>
<style>
body {{ margin: 0; padding: 32px 16px; background: #F4EFE6; color: #2A2230; font-family: Georgia, serif; }}
main {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: 32px; margin: 0 0 6px; }} p {{ color: #5E5262; margin: 0 0 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }}
.tile {{ display: flex; flex-direction: column; gap: 4px; padding: 16px; border-radius: 8px; border-bottom: 6px solid; text-decoration: none; min-height: 120px; color: #2A2230; }}
.n {{ font-size: 28px; }} .t {{ font-weight: bold; }} .m {{ font-size: 13px; }}
</style></head><body><main>
<h1>Everyone Else</h1><p>{len(BUILT)} of 39 built. One style for the whole line; each person on their own stamp.</p>
<div class="grid">{rows}</div></main></body></html>
"""


def main():
    check = "--check" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    files = {f"companion-{slug}.html": build(slug) for slug in BUILT}
    files["index.html"] = index()
    stale = 0
    for name, content in files.items():
        path = os.path.join(OUT, name)
        old = io.open(path, encoding="utf-8").read() if os.path.exists(path) else None
        stale += old != content
        if not check:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
    print(f"companions: {len(files) - 1} built, {stale} {'stale' if check else 'written'}")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()

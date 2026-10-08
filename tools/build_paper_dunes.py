#!/usr/bin/env python3
"""Build the Paper Dunes envelope set — every item, end to end.

    python tools/build_paper_dunes.py           # write 04-art/paper-dunes/*.html
    python tools/build_paper_dunes.py --check   # verify, write nothing

Two sheets come out:

  envelope-03.html   the pilot, every item in the envelope: exterior front and
                     back with the seal, the inside flap, the letter as the
                     folded A4 sheet (four faces, fact panel on the back), the
                     hadith card, the session card, the person print, the event
                     print with its ring punch, the sticker sheet, and the
                     return postcard.
  envelope-01.html   the mourning issue, to prove the style holds when the
                     colour goes: black on ivory, the pennant in place of the
                     sticker sheet, and the standard with no rider.

Every word is read from the source files — the letter, fact panel and session
card from 01-pilot/envelope-03/, the sayings from hadith-assignments.json — so
the sheet can never disagree with the text it was built from. The art is drawn
by tools/paperdunes_art.py, which has no figure in it at all.

Each sheet prints straight to one PDF with mixed page sizes (CSS named pages):
headless Chromium, --print-to-pdf, no margins.
"""

import html, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperdunes_art as A
from build_print_templates import letter_voices, inline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "04-art", "paper-dunes")
PILOT = os.path.join(ROOT, "01-pilot", "envelope-03")
E = html.escape


def lines_of(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def box_saying(envelope):
    with io.open(os.path.join(ROOT, "00-foundations", "hadith-assignments.json"), encoding="utf-8") as f:
        for b in json.load(f)["box"]:
            if b["envelope"] == envelope:
                return b
    raise SystemExit(f"no box saying for envelope {envelope}")


# ---------- source parsing ----------

def fact_panel_03():
    """The panel as fact-panel-spec.md lays it out: name, honorific, dates,
    six bullets, the death line, the standard line, the credit."""
    out = {"bullets": [], "after": []}
    for ln in lines_of(os.path.join(PILOT, "fact-panel.md")):
        s = ln.strip()
        if s.startswith("## The one new thing"):
            break
        if not s or s == "---" or s.startswith("# ") or s.startswith("## ") or s.startswith("Follows") \
                or s.startswith("**Every claim"):
            continue
        if s.startswith("### "):
            out["name"] = s[4:].strip().title()
        elif s.startswith("*(") and "honorific" not in out:
            out["honorific"] = s.strip("*")
        elif s.startswith("**b.") or s.startswith("**d."):
            out["dates"] = s.strip("*")
        elif s.startswith("● "):
            out["bullets"].append(inline(s[2:]))
        elif s.startswith("<sub>"):
            out["credit"] = E(re.sub(r"</?sub>", "", s))
        else:
            out["after"].append(inline(s))
    return out


def session_03():
    """The card front of session-card.md, as (title, sub, questions). A question
    is (label, flag, text) — label '1'..'5' or 'Last'."""
    body, on = [], False
    for ln in lines_of(os.path.join(PILOT, "session-card.md")):
        if ln.startswith("## Card front"):
            on = True; continue
        if on and ln.startswith("## "):
            break
        if on and ln.startswith(">"):
            body.append(ln[1:].strip())
    blocks, cur = [], []
    for s in body:
        if s == "---":
            blocks.append(cur); cur = []
        elif s:
            cur.append(s)
    blocks.append(cur)
    title = blocks[0][0].lstrip("#").strip()
    sub = blocks[0][1].strip("*")
    qs = []
    for b in blocks[1:]:
        text = " ".join(b)
        m = re.match(r"\*\*(\d+|Last)[.:]\*\*\s*(.*)", text)
        if not m:
            continue
        label, rest = m.group(1), m.group(2)
        flag = None
        f = re.match(r"([●⚑])\s*\*\*(.+?)\*\*\s*(.*)", rest)
        if f:
            flag, rest = f"{f.group(1)} {f.group(2)}", f.group(3)
        qs.append((label, flag, inline(rest)))
    return title, sub, qs


# ---------- page shells ----------

def page(cls, inner, mourning=False):
    m = " mourning" if mourning else ""
    return f'<div class="page {cls}{m}">{inner}</div>'


def item(caption, pg):
    return f'<div>{pg}<p class="cap screen-only">{caption}</p></div>'


def group(title, items):
    return f'<section class="group"><h2 class="screen-only">{title}</h2><div class="row">{"".join(items)}</div></section>'


def doc(title, head, groups):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<link rel="stylesheet" href="../print/assets/print.css">
<link rel="stylesheet" href="paper-dunes.css">
<script defer src="../print/assets/overflow-guard.js"></script>
</head><body class="set">
<header class="set-head screen-only">{head}</header>
{"".join(groups)}
</body></html>
"""


# ---------- the envelope ----------

def envelope_front(month, number, name=None, mourning=False):
    w, h = 229, 162
    p = A.Pen(mourning)
    ground = A.MOURN_GROUND if mourning else A.STD["sky"]
    art = (A.rect(p, 0, 0, w, h, ground)
           + A.sun(p, 126, 98, 20)
           + A.dune(p, w, h, 112, 14, A.STD["apricot"], 0.1)
           + (A.standard(p, 180, 128, 0.42) if mourning else A.mosque(p, 176, 124, 0.3, dome="dusk", body="dusk"))
           + A.dune(p, w, h, 128, 12, A.STD["clay"], -0.05)
           + ("" if mourning else A.palm(p, 26, 140, 0.44) + A.palm(p, 40, 146, 0.34, lean=-3))
           + A.dune(p, w, h, 148, 8, A.STD["oasis"], 0.2))
    ink = A.MOURN_INK if mourning else "#5B3A63"
    who = (f'<div class="who">{E(name)}</div>' if name
           else '<div class="who blank">&nbsp;</div>')
    inner = (A.svg(w, h, art)
             + '<div class="brand"><p class="kicker">Noor Post</p>'
               '<div class="tag">One of fourteen. Open it on the day.</div></div>'
             + A.stamp_ring(month, number, ink, ground=A.MOURN_GROUND if mourning else A.STD["sand"])
             + f'<div class="name-area"><p class="kicker">For</p>{who}</div>')
    return page("p-env env-front no-band", inner, mourning)


def envelope_back(mourning=False):
    w, h = 229, 162
    p = A.Pen(mourning)
    stock = A.MOURN_GROUND if mourning else A.STD["dune"]
    flap = A.STD["sand"] if not mourning else A.MOURN_GROUND
    art = (A.rect(p, 0, 0, w, h, stock)
           + f'<path {p.fill(A.STD["apricot"])} d="M0 0 H229 V16 Q172 50 114.5 86 Q57 50 0 16Z"/>'
           + f'<path {p.fill(flap)} d="M0 0 H229 V10 Q172 42 114.5 78 Q57 42 0 10Z"/>')
    colour = A.MOURN_INK if mourning else A.STD["dusk"]
    inner = (A.svg(w, h, art) + A.seal(colour, mourning)
             + '<div class="return"><strong>Noor Post</strong><br>[ Return address — not set ]</div>')
    return page("p-env env-back no-band", inner, mourning)


def inside_flap(kicker, runs, extra=None, mourning=False):
    clock = ('<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="5" '
             'fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M6 3.2V6l2 1.4" fill="none" '
             'stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>')
    lis = "".join(f"<li><span>{r}</span></li>" for r in runs)
    extra = f'<p class="voicekey" style="opacity:1;font-style:italic">{extra}</p>' if extra else ""
    inner = (f'<div class="flap-block"><div class="lead"><p class="kicker">{kicker}</p>'
             f'<div class="big">Open together.</div><div class="time">{clock} About twenty-five minutes</div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up. '
             f'<span class="mark">○</span> is you.</p>{extra}</div><ol>{lis}</ol></div>')
    return page("p-flap", inner, mourning)


# ---------- the letter: one A4 sheet, folded ----------

def head_art_03():
    w, h = 148.5, 50
    p = A.Pen()
    hills = (f'<path {p.fill(A.STD["dusk"])} d="M0 40 L16 33 L28 37 L44 30 L60 36 L72 32 L86 38 '
             f'L102 31 L118 36 L134 32 L148.5 36 V50 H0Z" opacity="0.9"/>')
    body = (A.rect(p, 0, 0, w, h, A.STD["sky"]) + A.sun(p, 116, 30, 9) + hills
            + A.dune(p, w, h, 38, 6, A.STD["apricot"], 0.1)
            + A.palm(p, 134, 49, 0.22, lean=-3)
            + A.dune(p, w, h, 45, 4, A.STD["clay"], -0.1))
    return A.svg(w, h, body, cls="head-art")


def split_letter(voices, ratio=0.47):
    """Faces 1 and 2 share the letter; the closing ●○ line is lifted out to
    face 3. Split on whole lines nearest `ratio` of the text."""
    body, close = voices[:-1], voices[-1]
    if 'class="voice together"' not in close:
        raise SystemExit("the letter's last line is not the ●○ line — face 3 has nothing to carry")
    sizes = [len(re.sub("<[^>]+>", "", v)) for v in body]
    total, run, cut = sum(sizes), 0, len(body)
    for i, n in enumerate(sizes):
        if run + n / 2 > total * ratio:
            cut = i; break
        run += n
    return body[:cut], body[cut:], close


def face3_art():
    w, h = 148.5, 210
    p = A.Pen()
    body = (A.star(p, 30, 40, 2.2, A.STD["apricot"]) + A.star(p, 118, 52, 1.8, A.STD["clay"])
            + A.star(p, 104, 30, 1.4, A.STD["apricot"])
            + A.cloak(p, 74.25, 160, 1.0,
                      cords=[(14, 180), (134.5, 180), (132, 124), (16, 124)]))
    return A.svg(w, h, body)


def letter_sheet_03(title, voices, panel, kicker):
    f1, f2, close = split_letter(voices)
    close_text = re.sub(r'<span class="mark">.*?</span>', "", close)
    close_text = re.sub(r"</?p[^>]*>", "", close_text).strip()

    face1 = (f'<div class="face face-letter first">{head_art_03()}'
             f'<div class="head-text"><p class="kicker">{kicker}</p>'
             f'<h1 class="letter-title">{E(title)}</h1></div>'
             f'<p class="voicekey"><span class="mark">●</span> is the grown-up · '
             f'<span class="mark">○</span> is you · <span class="mark">●○</span> is together</p>'
             f'<div class="letter">{"".join(f1)}</div><div class="facenum">1</div></div>')
    face2 = (f'<div class="face face-letter"><p class="cont">{E(title)} · continued</p>'
             f'<div class="letter">{"".join(f2)}</div><div class="facenum">2</div></div>')
    face3 = (f'<div class="face face-close">{face3_art()}<p class="say">Say this one together</p>'
             f'<p class="together-big"><span class="mark">●○</span>{close_text}</p>'
             f'<p class="next">Then the hadith card.</p><div class="facenum">3</div></div>')
    bl = "".join(f'<p class="bullet"><span class="dot">●</span>{b}</p>' for b in panel["bullets"])
    death, standard = panel["after"][0], " ".join(panel["after"][1:])
    face4 = (f'<div class="face face-panel"><div class="watermark-placeholder"><span>UNVERIFIED — TO VERIFY</span></div>'
             f'<p class="kicker">Fact panel</p><div class="panel">'
             f'<h3>{E(panel["name"])}</h3><p class="honorific">{E(panel["honorific"])}</p>'
             f'<p class="dates">{E(panel["dates"])}</p><hr>{bl}<hr>'
             f'<p class="death-line">{death}</p><p class="standard">{standard}</p>'
             f'<p class="credit">{panel.get("credit", "")}</p></div><div class="facenum">4</div></div>')

    side_a = page("p-spread", face4 + '<div class="fold"></div>' + face1)
    side_b = page("p-spread", face2 + '<div class="fold"></div>' + face3)
    return side_a, side_b


# ---------- hadith card ----------

def card_front(saying, mourning=False):
    w, h = 105, 148
    p = A.Pen(mourning)
    arch = "M11 132 V58 A41.5 41.5 0 0 1 94 58 V132Z"
    if mourning:
        body = f'<path d="{arch}" fill="none" stroke="{A.MOURN_INK}" stroke-width="0.5"/>'
    else:
        body = (f'<clipPath id="archclip"><path d="{arch}"/></clipPath>'
                f'<path d="{arch}" fill="{A.STD["dusk"]}"/>'
                f'<g clip-path="url(#archclip)">'
                + A.star(p, 30, 34, 1.6, A.STD["apricot"]) + A.star(p, 74, 28, 1.2, A.STD["apricot"])
                + A.star(p, 82, 46, 1.8, A.STD["clay"])
                + A.dune(p, w, h, 120, 7, A.STD["apricot"], 0.1)
                + A.dune(p, w, h, 128, 5, A.STD["clay"], -0.1) + "</g>")
    seg = saying.get("segment")
    if saying.get("segment_conflict") or not seg:
        mark = 'Silsila segment <span class="undecided">––</span> of 14'
    else:
        mark = f"Silsila segment {seg} of 14"
    masoom = saying["masoom"]
    who = "The Prophet Muhammad" if masoom == "The Prophet" else masoom
    said = "The Prophet said" if masoom == "The Prophet" else f"{masoom} said"
    inner = (A.svg(w, h, body) + f'<p class="chain-mark">{mark}</p>'
             f'<p class="who-said">{E(said)}</p>'
             f'<blockquote class="saying">&ldquo;{E(saying["text"])}&rdquo;</blockquote>'
             f'<p class="by">{E(who)}</p>')
    return page("p-a6p card-front no-band", inner, mourning)


def card_back(saying, chain_text, mourning=False):
    seg = None if saying.get("segment_conflict") else saying.get("segment")
    dots = "".join(f'<span class="{"on" if seg == i else ""}"></span>' for i in range(1, 15))
    note = ('<p class="note">Segment number undecided — two schemes both number a card 1. '
            'The dot fills when it is fixed.</p>' if seg is None else "")
    cite = (f'<em>{E(saying["work"])}</em>, {E(saying["ref"])}. Translated by '
            f'{E(saying["translator"])}, Ansariyan Publications, Qum.')
    inner = (f'<div class="card-back"><p class="kicker">Noor Post · The Fourteen</p>'
             f'<h3>The chain</h3><p>{chain_text}</p>'
             f'<div class="chain-dots" aria-label="Fourteen segments in historical order">{dots}</div>'
             f'<p class="note">Fourteen segments · historical order</p>{note}'
             f'<p class="cite">{cite}</p></div>')
    return page("p-a6p", inner, mourning)


def card_guard(html_text):
    """design-system.md §7: the envelope number never appears on a hadith card."""
    text = re.sub(r"<[^>]+>", " ", html_text)
    if re.search(r"\benvelope\b|\b0\d\b", text, re.I):
        raise SystemExit("a hadith card carries an envelope number — design-system.md §7")


# ---------- session card ----------

def session_cards(title, sub, qs):
    def q(label, flag, text):
        n = '<span class="n last">Last</span>' if label == "Last" else f'<span class="n">{label}</span>'
        fl = f'<span class="flagline">{E(flag)}</span>' if flag else ""
        return f'<div class="q">{n}<div class="t">{fl}{text}</div></div>'
    front = [x for x in qs if x[0] in ("1", "2", "3")]
    back = [x for x in qs if x[0] not in ("1", "2", "3")]
    f = (f'<div class="session"><h2 class="s-title">{E(title)}</h2><p class="s-sub">{E(sub)}</p>'
         + "".join(q(*x) for x in front) + '<p class="over">Turn over →</p></div>')
    pen = A.Pen()
    carry = A.svg(105, 148, A.cloak(pen, 52.5, 116, 0.56, cords=[(20, 124), (85, 124), (86, 98), (19, 98)]))
    b = ('<div class="session">' + carry + '<p class="kicker">Talk about it · continued</p>'
         + "".join(q(*x) for x in back) + "</div>")
    return page("p-a6p", f), page("p-a6p", b)


# ---------- prints ----------

def person_print_03():
    w, h = 148, 210
    p = A.Pen()
    body = (A.rect(p, 0, 0, w, h, A.STD["sky"])
            + A.star(p, 28, 34, 1.8, A.STD["apricot"]) + A.star(p, 116, 24, 1.4, A.STD["clay"])
            + A.sun(p, 98, 122, 22)
            + A.dune(p, w, h, 150, 8, A.STD["apricot"], 0.1)
            + A.mosque(p, 74, 168, 0.6)
            + A.dune(p, w, h, 176, 6, A.STD["clay"], -0.1)
            + A.palm(p, 30, 196, 0.62, lean=3) + A.palm(p, 18, 214, 0.98, lean=5)
            + A.palm(p, 132, 214, 0.86, lean=-5)
            + A.dune(p, w, h, 200, 7, A.STD["oasis"], 0.15))
    return page("p-a5p no-band", A.svg(w, h, body))


def event_print_03():
    w, h = 210, 148
    p = A.Pen()
    grove = "".join(A.palm(p, x, 76, s, lean=l) for x, s, l in
                    [(148, 0.32, 3), (156, 0.4, -2), (165, 0.3, 4), (172, 0.36, -3), (182, 0.28, 2), (190, 0.34, -1)])
    body = (A.rect(p, 0, 0, w, h, A.STD["sky"])
            + A.sun(p, 120, 66, 15)
            + A.dune(p, w, h, 76, 4, A.STD["apricot"], 0.05)
            + grove
            + A.dune(p, w, h, 96, 8, A.STD["clay"], -0.1)
            + A.road(p, w, h, 76, 142)
            + A.camel_kneeling(p, 34, 124, 1.0)
            + A.dune(p, w, h, 136, 5, A.STD["oasis"], 0.2))
    return page("p-a5l no-band", A.svg(w, h, body) + '<div class="punch" title="Ring punch: 6 mm, centred, 12 mm from the top"></div>')


def sticker_sheet_03():
    w, h = 105, 148
    p = A.Pen()
    kiss = ('<filter id="kiss" x="-20%" y="-20%" width="140%" height="140%">'
            '<feMorphology in="SourceAlpha" operator="dilate" radius="1.8" result="d"/>'
            '<feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>'
            '<feDropShadow in="w" dx="0" dy="0.4" stdDeviation="0.5" flood-color="#3B2440" flood-opacity="0.3" result="ws"/>'
            '<feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    road_badge = (f'<g filter="url(#kiss)"><circle cx="76" cy="84" r="18" fill="{A.STD["sky"]}"/></g>'
                  f'<g clip-path="url(#badge)">'
                  f'<rect x="58" y="84" width="36" height="20" fill="{A.STD["apricot"]}"/>'
                  f'<path d="M66 102 C70 96 74 88 75.5 84 L76.5 84 C78 88 82 96 88 102Z" fill="{A.STD["dune"]}"/>'
                  + A.sun(p, 84, 76, 4) + '</g>')
    caravan = (f'<g filter="url(#kiss)"><path d="M10 136 Q30 126 52 132 L52 138 L10 138Z" fill="{A.STD["apricot"]}"/>'
               + A.camel_standing(p, 14, 134, 0.42) + A.camel_standing(p, 27, 131.5, 0.42)
               + A.camel_standing(p, 40, 132.5, 0.42) + '</g>')
    body = (f'<defs>{kiss}<clipPath id="badge"><circle cx="76" cy="84" r="18"/></clipPath></defs>'
            + A.rect(p, 0, 0, w, h, "#FFFFFF")
            + f'<g filter="url(#kiss)">{A.cloak(p, 52, 42, 0.72)}</g>'
            + f'<g filter="url(#kiss)">{A.palm(p, 26, 104, 0.42, lean=4)}</g>'
            + road_badge + caravan
            + f'<g filter="url(#kiss)">{A.sun(p, 86, 122, 7)}</g>'
            + f'<g filter="url(#kiss)">{A.star(p, 90, 52, 4, A.STD["clay"])}</g>'
            + f'<g filter="url(#kiss)">{A.star(p, 92, 18, 3.4, A.STD["apricot"])}</g>'
            + f'<g filter="url(#kiss)">{A.star(p, 54, 106, 3, A.STD["oasis"])}</g>'
            + f'<g filter="url(#kiss)">{A.lantern(p, 64, 128, 0.42)}</g>')
    return page("p-a6p stickers no-band", A.svg(w, h, body))


# ---------- postcard ----------

def postcard_front_03():
    w, h = 148, 105
    p = A.Pen()
    body = (A.rect(p, 0, 0, w, h, A.STD["sky"]) + A.sun(p, 112, 40, 14)
            + A.dune(p, w, h, 60, 6, A.STD["apricot"], 0.1)
            + A.dune(p, w, h, 80, 6, A.STD["clay"], -0.1)
            + A.cloak(p, 74, 86, 0.9, cords=[(8, 104), (140, 104), (146, 64), (2, 64)])
            + A.dune(p, w, h, 100, 3, A.STD["oasis"], 0.2))
    return page("p-a6l no-band", A.svg(w, h, body))


def postcard_back(mourning=False):
    inner = ('<div class="pc-back"><div class="msg"><div class="big">We opened this one together.</div>'
             '<div class="sig"><span>●</span><span class="line"></span></div>'
             '<div class="sig"><span>○</span><span class="line"></span></div>'
             '<p class="small">Post it back to us, or keep it. Either is right.</p></div>'
             '<div class="addr"><div class="stampbox">Stamp</div>'
             '<div class="to"><strong>Noor Post</strong><div>[ Return address — not set ]</div>'
             '<div class="ln"></div><div class="ln"></div></div></div></div>')
    return page("p-a6l", inner, mourning)


# ---------- the mourning issue ----------

def pennant_01():
    w, h = 148, 210
    p = A.Pen(True)
    cord = (f'<path d="M0 22 Q74 30 148 22" fill="none" stroke="{A.MOURN_INK}" stroke-width="0.6"/>')
    tri = f'<path d="M22 26 H126 L74 192Z" fill="{A.MOURN_GROUND}" stroke="{A.MOURN_INK}" stroke-width="0.5" stroke-dasharray="2 1.2"/>'
    hem = f'<path d="M22 26 H126 V34 H22Z" fill="none" stroke="{A.MOURN_INK}" stroke-width="0.4"/>'
    body = A.rect(p, 0, 0, w, h, A.MOURN_GROUND) + cord + tri + hem + A.standard(p, 74, 136, 0.62)
    return page("p-a5p pennant no-band", A.svg(w, h, body), True)


def event_print_01():
    w, h = 210, 148
    p = A.Pen(True)
    body = (A.rect(p, 0, 0, w, h, A.MOURN_GROUND)
            + A.dune(p, w, h, 112, 6, "", 0.05) + A.standard(p, 105, 118, 0.62)
            + A.dune(p, w, h, 130, 5, "", -0.1))
    return page("p-a5l no-band", A.svg(w, h, body) + '<div class="punch"></div>', True)


def postcard_front_01():
    w, h = 148, 105
    p = A.Pen(True)
    body = (A.rect(p, 0, 0, w, h, A.MOURN_GROUND) + A.dune(p, w, h, 84, 5, "", 0.1)
            + A.standard(p, 74, 92, 0.55))
    return page("p-a6l no-band", A.svg(w, h, body), True)


# ---------- driver ----------

CHAIN_03 = ("It begins with him. Everyone else in this box is his family, and every chain of "
            "teaching in it runs back through this one man to the words he was given.")
CHAIN_01 = ("Every card in this box is one link. Lay all fourteen in order and the chain runs "
            "from the Prophet to the last of the twelve, each one passing on what was given.")


def build_03():
    letter = lines_of(os.path.join(PILOT, "letter.md"))
    title = re.search(r"\*(.+?)\*", next(l for l in letter if l.startswith("## Letter"))).group(1)
    voices = letter_voices(letter)
    panel = fact_panel_03()
    s_title, s_sub, qs = session_03()
    saying = box_saying("03")

    side_a, side_b = letter_sheet_03(title, voices, panel, "Envelope 03 · Rabi al-Awwal")
    cf, cb = card_front(saying), card_back(saying, CHAIN_03)
    card_guard(cf + cb)
    sf, sb = session_cards(s_title, s_sub, qs)
    runs = ['The letter — read it out loud, <span class="mark">●</span> and '
            '<span class="mark">○</span> taking turns', "The hadith card", "The prints",
            "Talk about it", "The stickers", "The postcard"]

    head = ('<h1>Envelope 03 · The Cloak</h1>'
            '<p>Paper Dunes — every item in the envelope, at true size. Text is read from '
            '<code>01-pilot/envelope-03/</code> and <code>hadith-assignments.json</code>; the art is '
            'drawn by <code>tools/paperdunes_art.py</code>. Print this page to PDF with no margins: '
            'each item comes out on its own page at its own size.</p>'
            '<p>Still open, and marked where it shows: the fact panel is TO VERIFY, the silsila '
            'segment number is undecided, and the return address is not set.</p>')
    groups = [
        group("1 · Envelope exterior — C5, 229 × 162 mm", [
            item("Front — cancellation mark, name area (Named Edition)", envelope_front("RABI AL-AWWAL", "03", "[Child's name]")),
            item("Back — flap and wax seal, 32 mm", envelope_back())]),
        group("2 · Inside the flap — 148 × 100 mm", [
            item("Running order and runtime, nothing else", inside_flap("Envelope 03 · Inside the flap", runs))]),
        group("3 · The letter — one A4 sheet, folded to A5", [
            item("Print side A (outside): face 4, the fact panel | face 1, the letter opens", side_a),
            item("Print side B (inside): face 2, the letter continues | face 3, the line said together", side_b)]),
        group("4 · Hadith card — A6", [
            item("Front", cf), item("Back — no envelope number anywhere", cb)]),
        group("5 · Session card — A6", [item("Front", sf), item("Back", sb)]),
        group("6 · Prints — A5", [
            item("Person print — Masjid an-Nabawi, green dome, palms, early light", person_print_03()),
            item("Event print — the road to Quba, ring position 3. Red dashed circle = punch, screen only", event_print_03())]),
        group("7 · Sticker sheet — A6, kiss-cut", [
            item("The cloak with four corners, a palm, the Quba road, a caravan, small marks", sticker_sheet_03())]),
        group("8 · Return postcard — A6 landscape", [
            item("Front — the cloak", postcard_front_03()), item("Back", postcard_back())]),
    ]
    return doc("Envelope 03 — Paper Dunes", head, groups)


def build_01():
    saying = box_saying("01")
    cf, cb = card_front(saying, True), card_back(saying, CHAIN_01, True)
    card_guard(cf + cb)
    runs = ['The letter — read it out loud, <span class="mark">●</span> and '
            '<span class="mark">○</span> taking turns', "The hadith card", "The prints",
            "Sit with it", "The pennant", "The postcard"]
    head = ('<h1>Envelope 01 · Muharram — the mourning issue</h1>'
            '<p>The same set, with the colour taken out: black on ivory, per '
            '<code>design-system.md</code> §2. The paper-cut survives as line. A pennant replaces the '
            'sticker sheet, and the event print is one object, no scene: a standard with no rider.</p>')
    groups = [
        group("Envelope exterior — C5", [
            item("Front — cancellation reads MUHARRAM", envelope_front("MUHARRAM", "01", None, True)),
            item("Back — charcoal seal", envelope_back(True))]),
        group("Inside the flap", [item("The pennant replaces the stickers",
                                       inside_flap("Envelope 01 · Muharram · Inside the flap", runs,
                                                   "This one has no game in it.", True))]),
        group("Hadith card — A6", [item("Front", cf), item("Back", cb)]),
        group("Pennant and prints", [
            item("Pennant — cord-mounted, size to be set against a physical proof", pennant_01()),
            item("Event print — a standard with no rider, ring position 1", event_print_01())]),
        group("Return postcard", [item("Front — the standard", postcard_front_01()),
                                  item("Back", postcard_back(True))]),
    ]
    return doc("Envelope 01 — Paper Dunes, mourning", head, groups)


def main():
    check = "--check" in sys.argv
    out = {"envelope-03.html": build_03(), "envelope-01.html": build_01()}
    os.makedirs(OUT, exist_ok=True)
    stale = 0
    for name, content in out.items():
        path = os.path.join(OUT, name)
        old = io.open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != content:
            stale += 1
        if not check:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
    print(f"paper dunes: {len(out)} sheets, {stale} {'differ' if check else 'written'}")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()

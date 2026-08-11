#!/usr/bin/env python3
"""Build the review site from the content markdown into docs/."""

import os, re, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")

# ---------- markdown fragments -> html ----------

def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t

BRACKET_PLACEHOLDER = re.compile(r"^\[.*\]$")

def clean(lines):
    """Drop production placeholders and internal italic notes."""
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append("")
            continue
        if s.startswith("<sub>"):
            continue
        if BRACKET_PLACEHOLDER.match(s.replace("*", "").strip()):
            continue
        if s.startswith("*Every bullet on this panel"):
            continue
        if s.startswith("**Every claim on this panel"):
            continue
        if s.startswith("Follows `00-foundations"):
            continue
        if s.startswith("Rules: `editorial-rulebook"):
            continue
        if s.startswith("Image:"):
            continue
        if s.startswith("**Note for the scholar:**"):
            continue
        if s.startswith("**Pennant replaces the sticker sheet"):
            continue
        if s.startswith("**Two roles, and neither one gets an answer.**"):
            continue
        out.append(ln)
    return out

def blocks(lines):
    """Render a cleaned markdown fragment (paragraphs, bullets, quotes, rules, h3)."""
    out, para, quote = [], [], []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_quote():
        if quote:
            out.append('<div class="card">' + "".join(blocks(clean(quote))) + "</div>")
            quote.clear()

    for ln in lines:
        s = ln.rstrip()
        if s.startswith(">"):
            quote.append(s[1:].lstrip() if len(s) > 1 else "")
            continue
        flush_quote()
        if not s.strip():
            flush_para()
            continue
        if s.strip() in ("---", "***"):
            flush_para()
            out.append("<hr>")
            continue
        if s.startswith("### "):
            flush_para()
            out.append("<h3>" + inline(s[4:].strip()) + "</h3>")
            continue
        if s.startswith("## "):
            flush_para()
            out.append("<h2>" + inline(s[3:].strip()) + "</h2>")
            continue
        if s.startswith("#### "):
            flush_para()
            out.append("<h4>" + inline(s[5:].strip()) + "</h4>")
            continue
        if s.startswith("● ") or s.startswith("- "):
            flush_para()
            mark = "●" if s.startswith("●") else None
            body = s[2:].strip()
            if mark:
                out.append('<p class="bullet"><span class="dot">●</span>' + inline(body) + "</p>")
            else:
                out.append('<p class="bullet">' + inline(body) + "</p>")
            continue
        para.append(s.strip())
    flush_para()
    flush_quote()
    return out

def frag(lines):
    return "\n".join(blocks(clean(lines)))

# ---------- source parsing ----------

def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read().split("\n")

def section(lines, start_pred, level="## "):
    """Lines of the section whose heading matches start_pred, up to the next same-level heading."""
    body, on = [], False
    for ln in lines:
        if ln.startswith(level):
            if on:
                break
            if start_pred(ln):
                on = True
                continue
        elif on:
            body.append(ln)
    return body

def letter_body(lines):
    body, on = [], False
    for ln in lines:
        if "LETTER START" in ln:
            on = True
            continue
        if "LETTER END" in ln:
            break
        if on and ln.strip() != "---":
            body.append(ln)
    return body

def letter_title(lines):
    for ln in lines:
        m = re.match(r"^## Letter.*?\*(.+?)\*", ln)
        if m:
            return m.group(1)
    return "Letter"

def render_letter(body):
    out = []
    for ln in body:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("●○"):
            out.append('<p class="voice together"><span class="mark">●○</span>' + inline(s[2:].strip()) + "</p>")
        elif s.startswith("●"):
            out.append('<p class="voice adult"><span class="mark">●</span>' + inline(s[1:].strip()) + "</p>")
        elif s.startswith("○"):
            out.append('<p class="voice child"><span class="mark">○</span>' + inline(s[1:].strip()) + "</p>")
        else:
            out.append("<p>" + inline(s) + "</p>")
    return "\n".join(out)

# ---------- page shell ----------

def page(title, subtitle, body, depth=0, nav_current=None):
    base = "" if depth == 0 else "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(title)} — Noor Post</title>
<link rel="stylesheet" href="{base}style.css">
</head>
<body>
<header class="top">
  <a class="wordmark" href="{base}index.html">Noor&nbsp;Post</a>
  <nav>
    <a href="{base}index.html#the-fourteen">The Fourteen</a>
    <a href="{base}index.html#everyone-else">Everyone Else</a>
    <a href="{base}index.html#notebook">Noori's Notebook</a>
  </nav>
</header>
<main>
{body}
</main>
<footer>
  <p>Noor Post — draft for review. Not for circulation.</p>
</footer>
</body>
</html>
"""

def envelope_page(num, month, masoom, session, letter_ttl, letter_html, panel_html, casefile_html, session_html, flap_html):
    parts = [f"""<article class="envelope">
<div class="stamp">{html.escape(month)}</div>
<p class="kicker">Envelope {num} · {html.escape(month)}</p>
<h1>{html.escape(masoom)}</h1>
{flap_html}
<section class="letter">
  <h2 class="letter-title">{html.escape(letter_ttl)}</h2>
  <p class="voicekey"><span class="mark">●</span> the grown-up &nbsp;·&nbsp; <span class="mark">○</span> the child &nbsp;·&nbsp; <span class="mark">●○</span> together</p>
  {letter_html}
</section>
<section class="panel">
  <p class="itemlabel">Letter, reverse</p>
  {panel_html}
</section>"""]
    if casefile_html:
        parts.append(f'<section class="session">\n<p class="itemlabel">Case file</p>\n{casefile_html}\n</section>')
    if session_html:
        parts.append(f'<section class="session">\n<p class="itemlabel">Session card — {html.escape(session)}</p>\n{session_html}\n</section>')
    parts.append("</article>")
    return "\n".join(parts)

FLAP_ORDER = {
    "Mourning": "Sit with it",
    "Conversation": "Talk about it",
    "Case File": "Open the case file",
    "Open": "Write one",
}

def flap(session):
    fifth = "The pennant" if session == "Mourning" else "The stickers"
    extra = '<p class="flap-note">This one has no game in it.</p>' if session == "Mourning" else ""
    return f"""<section class="flap">
<p class="itemlabel">Inside the flap</p>
<p class="flap-lead"><strong>Open together. About twenty-five minutes.</strong></p>
<ol>
<li>The letter — read it out loud, ● and ○ taking turns</li>
<li>The hadith card</li>
<li>The prints</li>
<li>{FLAP_ORDER.get(session, session)}</li>
<li>{fifth}</li>
<li>The postcard</li>
</ol>
<p class="flap-key">● is the grown-up. ○ is you.</p>
{extra}
</section>"""

def companion_flap():
    return """<section class="flap">
<p class="itemlabel">Inside the flap</p>
<p class="flap-lead"><strong>Open together.</strong></p>
<ol>
<li>The letter — read it out loud, ● and ○ taking turns</li>
<li>The print</li>
<li>The stickers</li>
<li>The postcard</li>
</ol>
<p class="flap-key">● is the grown-up. ○ is you.</p>
</section>"""

# ---------- envelopes ----------

ENVELOPES = [
    ("01", "Muharram", "Imam Husayn", "Mourning"),
    ("02", "Safar", "Imam Hasan", "Mourning"),
    ("03", "Rabi al-Awwal", "The Prophet Muhammad", "Conversation"),
    ("04", "Rabi al-Thani", "Imam al-Askari", "Case File"),
    ("05", "Jumada al-Awwal", "Imam al-Baqir", "Conversation"),
    ("06", "Jumada al-Thani", "Sayyida Fatima", "Conversation"),
    ("07", "Rajab", "Imam Ali", "Conversation"),
    ("08", "Rajab", "Imam al-Kadhim", "Case File"),
    ("09", "Sha'ban", "Imam al-Sajjad", "Conversation"),
    ("10", "Sha'ban", "Imam al-Mahdi", "Open"),
    ("11", "Ramadan", "Imam al-Hadi", "Case File"),
    ("12", "Shawwal", "Imam al-Sadiq", "Conversation"),
    ("13", "Dhul Qa'dah", "Imam al-Rida", "Conversation"),
    ("14", "Dhul Hijjah", "Imam al-Jawad", "Case File"),
]

COMPANIONS = [
    ("salman", "Salman al-Farsi"),
    ("bilal", "Bilal"),
    ("maytham", "Maytham al-Tammar"),
    ("qambar", "Qambar"),
    ("abu-dharr", "Abu Dharr"),
    ("malik", "Malik al-Ashtar"),
]

ZINES = [
    ("ghadir-khumm", "Ghadir Khumm"),
    ("hira", "Hira"),
    ("mubahala", "Mubahala"),
    ("hudaybiyya", "Hudaybiyya"),
    ("the-trench", "The Trench"),
    ("jannat-al-baqi", "Jannat al-Baqi"),
    ("jamkaran", "Jamkaran"),
    ("the-road-to-karbala", "The road to Karbala"),
    ("kufa", "Kufa"),
    ("samarra", "Samarra"),
    ("laylat-al-mabit", "Laylat al-Mabit"),
    ("dahw-al-ard", "Dahw al-Ard"),
    ("constitution-of-medina", "The Constitution of Medina"),
    ("bayt-al-hikma", "Bayt al-Hikma"),
    # Fadak intentionally excluded — outline only, scholar decision pending before it is drafted.
]


def build_envelope(num, month, masoom, session):
    if num == "03":
        L = read("01-pilot/envelope-03/letter.md")
        P = read("01-pilot/envelope-03/fact-panel.md")
        S = read("01-pilot/envelope-03/session-card.md")
        ttl = "The Cloak"
        lh = render_letter(letter_body(L))
        panel = section(P, lambda x: x.startswith("## Letter, reverse"))
        ph = frag(panel)
        sh = frag(section(S, lambda x: x.startswith("## Card front")))
        ch = ""
    else:
        F = read(f"03-content/envelope-{num}.md")
        ttl = letter_title(F)
        lh = render_letter(letter_body(F))
        ph = frag(section(F, lambda x: x.startswith("## Fact panel")))
        ch = frag(section(F, lambda x: x.startswith("## Case File")))
        sh = frag(section(F, lambda x: x.startswith("## Session card")))
    return envelope_page(num, month, masoom, session, ttl, lh, ph, ch, sh, flap(session))


def build():
    os.makedirs(OUT, exist_ok=True)

    for num, month, masoom, session in ENVELOPES:
        body = build_envelope(num, month, masoom, session)
        with open(os.path.join(OUT, f"envelope-{num}.html"), "w", encoding="utf-8") as f:
            f.write(page(f"{masoom} — Envelope {num}", month, body))

    for slug, name in COMPANIONS:
        F = read(f"08-companions/{slug}.md")
        ttl = letter_title(F)
        lh = render_letter(letter_body(F))
        ph = frag(section(F, lambda x: x.startswith("## Fact panel")))
        points = ""
        for ln in F:
            m = re.match(r"^\*\*Points home:\*\* \*(.+?)\*", ln)
            if m:
                points = m.group(1)
                break
        body = f"""<article class="envelope companion">
<p class="kicker">Everyone Else</p>
<h1>{html.escape(name)}</h1>
<p class="points">{html.escape(points)}</p>
{companion_flap()}
<section class="letter">
  <h2 class="letter-title">{html.escape(ttl)}</h2>
  <p class="voicekey"><span class="mark">●</span> the grown-up &nbsp;·&nbsp; <span class="mark">○</span> the child &nbsp;·&nbsp; <span class="mark">●○</span> together</p>
  {lh}
</section>
<section class="panel">
  <p class="itemlabel">Letter, reverse</p>
  {ph}
</section>
</article>"""
        with open(os.path.join(OUT, f"companion-{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page(name, "Everyone Else", body))

    for slug, name in ZINES:
        F = read(f"09-zines/{slug}.md")
        pages = []
        for i in range(1, 9):
            sec = section(F, lambda x, i=i: x.startswith(f"## PAGE {i}"))
            label = ""
            for ln in F:
                if ln.startswith(f"## PAGE {i}"):
                    label = ln.split("—", 1)[1].strip() if "—" in ln else ""
            pages.append(f'<section class="zinepage"><p class="itemlabel">Page {i} · {html.escape(label)}</p>{frag(sec)}</section>')
        body = f"""<article class="zine">
<p class="kicker">Noori's Notebook</p>
<h1>{html.escape(name)}</h1>
<p class="points">One sheet, folded to eight pages.</p>
{''.join(pages)}
</article>"""
        with open(os.path.join(OUT, f"zine-{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page(name, "Noori's Notebook", body))

    # index
    rows = []
    for num, month, masoom, session in ENVELOPES:
        rows.append(f"""<a class="tile" href="envelope-{num}.html">
<span class="tilenum">{num}</span>
<span class="tilemonth">{html.escape(month)}</span>
<span class="tilename">{html.escape(masoom)}</span>
<span class="tilesession">{html.escape(session)}</span>
</a>""")
    comp = "".join(
        f'<a class="tile small" href="companion-{s}.html"><span class="tilename">{html.escape(n)}</span></a>'
        for s, n in COMPANIONS)
    zin = "".join(
        f'<a class="tile small" href="zine-{s}.html"><span class="tilename">{html.escape(n)}</span></a>'
        for s, n in ZINES)

    body = f"""<section class="hero">
<h1>Noor Post</h1>
<p class="lede">Fourteen sealed envelopes, one for each month of the Islamic year. A parent and a child open one together on the date it belongs to and work through it in about twenty-five minutes.</p>
<p class="lede small">Each envelope holds a two-voice letter, a fact panel, a hadith card, two prints, a session card, stickers and a postcard to send back.</p>
</section>

<section id="the-fourteen">
<h2>The Fourteen</h2>
<p class="sectionnote">In calendar order, as they arrive.</p>
<div class="grid">{''.join(rows)}</div>
</section>

<section id="everyone-else">
<h2>Everyone Else</h2>
<p class="sectionnote">Single envelopes about the companions. Four items, no date, bought one at a time.</p>
<div class="grid">{comp}</div>
</section>

<section id="notebook">
<h2>Noori's Notebook</h2>
<p class="sectionnote">One sheet, folded to eight pages, about a place or an event.</p>
<div class="grid">{zin}</div>
</section>"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Noor Post", "", body))

    print("built", len(ENVELOPES) + len(COMPANIONS) + len(ZINES) + 1, "pages")


if __name__ == "__main__":
    build()

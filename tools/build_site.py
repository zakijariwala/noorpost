#!/usr/bin/env python3
"""Build the review site from the content markdown into docs/."""

import os, re, html, shutil, glob

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
<p class="cardsback"><a href="envelope-{num}-cards.html">View every item as a card &rarr;</a></p>
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
<li>The hadith card</li>
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
    ("uthman", "Uthman ibn Sa'id al-Amri"),
    ("muhammad-ibn-uthman", "Muhammad ibn Uthman al-Amri"),
    ("husayn-ibn-ruh", "Husayn ibn Ruh al-Nawbakhti"),
    ("al-samarri", "Ali ibn Muhammad al-Samarri"),
    ("abbas", "Abbas ibn Ali"),
    ("fizza", "Fizza"),
    ("jabir", "Jabir ibn Abdullah al-Ansari"),
    ("qais", "Qais ibn Sa'd"),
    ("tawus", "Tawus al-Yamani"),
    ("safwan", "Safwan al-Jammal"),
    ("dibil", "Dibil al-Khuza'i"),
    ("ahmad-ibn-ishaq", "Ahmad ibn Ishaq al-Qummi"),
    ("abu-hashim", "Abu Hashim al-Ja'fari"),
    ("hisham", "Hisham ibn al-Hakam"),
    ("ali-ibn-mahziyar", "Ali ibn Mahziyar"),
    ("sumayyah", "Sumayyah bint Khabbat"),
    ("nusaybah", "Nusaybah bint Ka'b"),
    ("umm-ayman", "Umm Ayman"),
    ("halima", "Halima al-Sa'diyya"),
    ("asma", "Asma bint Umays"),
    ("khawla", "Khawla bint al-Azwar"),
    ("umm-kulthum", "Umm Kulthum bint Ali"),
    ("rabab", "Rabab bint Imra' al-Qays"),
    ("zaynab", "Zaynab bint Ali"),
    ("sakina", "Sakina bint al-Husayn"),
    ("fitrus", "Fitrus"),
    ("fatima-bint-asad", "Fatima bint Asad"),
    ("umm-al-banin", "Umm al-Banin"),
    ("hamida", "Hamida Khatun"),
    ("umm-farwa", "Umm Farwa"),
    ("narjis", "Narjis Khatun"),
    ("ruqayya", "Sayyida Ruqayya bint al-Husayn"),
    ("masuma", "Sayyida Ma'suma"),
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
    ("fadak", "Fadak"),
]


INTERNAL_REF = re.compile(
    r"\s*[—-]?\s*\(?\bsee\b[^.)]*`[^`]+\.md`[^.)]*\)?\.?"   # "— see `citation-sheet.md`."
    r"|\s*\(?`[^`]*\.md`\)?"                                  # any bare `file.md`
    r"|\s*\bper\s+`[^`]+`(\s*§\s*\d+)?",                      # "per `standard-lines.md` §4"
    re.I)

def strip_internal(text):
    """Remove internal file references from anything that reaches docs/.

    HANDOVER.md: the site shows only what a family receives. Item specs are
    published on the card pages by design, but the cross-references inside
    them are working notes and must not leak.
    """
    return re.sub(r"\s{2,}", " ", INTERNAL_REF.sub("", text)).strip(" .,—-") + "."


def items_table(F):
    """Parse the '## Items' markdown table into {num: (item, spec, state)}."""
    items = {}
    for ln in section(F, lambda x: x.startswith("## Items")):
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cols = [c.strip() for c in s.strip("|").split("|")]
        if len(cols) >= 4 and cols[0].isdigit():
            items[int(cols[0])] = (cols[1], cols[2], cols[3])
    return items


ENVELOPE_03_SEGMENT = ("Silsila segment 1: “It begins with him. Everyone else in this box is his family, "
                       "and every chain of teaching in it runs back through this one man to the words he was given.”")


def envelope_source(num):
    """Everything build_envelope and build_envelope_cards both need, read once."""
    if num == "03":
        L = read("01-pilot/envelope-03/letter.md")
        P = read("01-pilot/envelope-03/fact-panel.md")
        S = read("01-pilot/envelope-03/session-card.md")
        ttl = "The Cloak"
        lh = render_letter(letter_body(L))
        ph = frag(section(P, lambda x: x.startswith("## Letter, reverse")))
        sh = frag(section(S, lambda x: x.startswith("## Card front")))
        ch = ""
        items = items_table(read("01-pilot/envelope-03/items.md"))
    else:
        F = read(f"03-content/envelope-{num}.md")
        ttl = letter_title(F)
        lh = render_letter(letter_body(F))
        ph = frag(section(F, lambda x: x.startswith("## Fact panel")))
        ch = frag(section(F, lambda x: x.startswith("## Case File")))
        sh = frag(section(F, lambda x: x.startswith("## Session card")))
        items = items_table(F)
    return {"ttl": ttl, "lh": lh, "ph": ph, "ch": ch, "sh": sh, "items": items}


def build_envelope(num, month, masoom, session, src):
    return envelope_page(num, month, masoom, session, src["ttl"], src["lh"], src["ph"], src["ch"], src["sh"], flap(session))


# ---------- card view: one card per physical item ----------

ART_ICON = ('<svg viewBox="0 0 64 64" aria-hidden="true">'
            '<rect x="4" y="4" width="56" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<circle cx="21" cy="20" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<path d="M8 46 L24 30 L34 40 L44 26 L60 46" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
            '</svg>')

ITEM_META = {
    "Letter": ("A5", "portrait"),
    "Fact panel": ("A5", "portrait"),
    "Hadith card": ("A6", "portrait"),
    "Person print": ("A5", "portrait"),
    "Event print": ("A5", "landscape"),
    "Session card": ("A6", "portrait"),
    "Sticker sheet": ("A6", "portrait, die-cut"),
    "Pennant": ("—", "triangular, cord-mounted"),
    "Return postcard": ("A6", "landscape"),
}


def is_pending(state):
    s = state.lower()
    return any(k in s for k in ("pending", "blocked", "not yet", "to fill", "to select"))


def status_pill(pending):
    cls, label = ("placeholder", "Placeholder") if pending else ("written", "Written")
    return f'<span class="statuspill {cls}">{label}</span>'


def size_tag(name):
    size, orient = ITEM_META.get(name, ("—", "—"))
    return f'<span class="sizetag">{size} · {orient}</span>'


def card_shell(n, name, pending, body):
    # "Item", not "Card" — the product already means specific objects by "card"
    # (hadith card, session card), and reusing the word collides with them.
    return f"""<div class="itemcard">
  <div class="itemcard-head">
    <span class="itemtag">Item {n} · {html.escape(name)}</span>
    {size_tag(name)}
    {status_pill(pending)}
  </div>
  {body}
</div>"""


def art_block(spec, orientation):
    land = ' land' if orientation == "landscape" else ""
    return f"""<div class="artbox{land}">
  <div class="artbox-frame">{ART_ICON}</div>
</div>
<p class="artbox-caption">{inline(strip_internal(spec))}</p>
<p class="placeholdertag">Placeholder — no artwork made yet</p>"""


def hadith_block(spec, masoom, decided_note=None):
    """No quotation marks and no name in quote position.

    sourcing-rules.md: quote exactly, or don't quote. Rendering invented
    filler inside quote marks, attributed to a named figure, is the wrong
    shape even when labelled — a screenshot of one card loses the label.
    """
    extra = ""
    if decided_note:
        extra = f'<div class="decidednote"><p class="itemlabel">Already decided</p><p>{inline(decided_note)}</p></div>'
    return f"""<p class="itemspec">{inline(strip_internal(spec))}</p>
{extra}
<div class="placeholderquote">
  <p class="placeholderrule">Saying not yet selected.</p>
  <p>The chosen line will be set here, quoted exactly from the fixed edition, with the citation on the reverse. Nothing is printed on this card until its row on the citation sheet reads verified.</p>
</div>
<p class="placeholdertag">Placeholder — no saying chosen for this card</p>"""


def postcard_block(spec):
    return f"""<p class="itemlabel">Front</p>
<div class="artbox land">
  <div class="artbox-frame">{ART_ICON}</div>
</div>
<p class="artbox-caption">{inline(strip_internal(spec))}</p>
<p class="placeholdertag">Placeholder — front art not yet made</p>
<p class="itemlabel" style="margin-top:1.3rem">Back — fixed wording</p>
<blockquote class="postcardtext">
  <p>We opened this one together.</p>
  <p>● ______________________ &nbsp;&nbsp; ○ ______________________</p>
  <p><em>Post it back to us, or keep it. Either is right.</em></p>
</blockquote>"""


def build_envelope_cards(num, month, masoom, session, src):
    items = src["items"]
    cards, n = [], 1

    cards.append(card_shell(n, "Letter", False, f"""
<h2 class="letter-title">{html.escape(src['ttl'])}</h2>
<p class="voicekey"><span class="mark">●</span> the grown-up &nbsp;·&nbsp; <span class="mark">○</span> the child &nbsp;·&nbsp; <span class="mark">●○</span> together</p>
{src['lh']}
""")); n += 1

    cards.append(card_shell(n, "Fact panel", False, src["ph"])); n += 1

    if 2 in items:
        _, spec, _ = items[2]
        decided = ENVELOPE_03_SEGMENT if num == "03" else None
        cards.append(card_shell(n, "Hadith card", True, hadith_block(spec, masoom, decided))); n += 1

    if 3 in items:
        _, spec, state = items[3]
        cards.append(card_shell(n, "Person print", is_pending(state), art_block(spec, "portrait"))); n += 1

    if 4 in items:
        _, spec, state = items[4]
        cards.append(card_shell(n, "Event print", is_pending(state), art_block(spec, "landscape"))); n += 1

    body = src["ch"] or src["sh"]
    if body:
        note = ""
        if 5 in items:
            _, spec5, _ = items[5]
            note = f'<p class="itemspec">{inline(strip_internal(spec5))}</p>'
        cards.append(card_shell(n, "Session card", False, note + body)); n += 1

    if 6 in items:
        name6, spec, state = items[6]
        cards.append(card_shell(n, name6, is_pending(state), art_block(spec, "portrait"))); n += 1

    if 7 in items:
        _, spec, _ = items[7]
        cards.append(card_shell(n, "Return postcard", True, postcard_block(spec))); n += 1

    return f"""<article class="envelope cardsview">
<p class="kicker">Envelope {num} · {html.escape(month)} · card view</p>
<h1>{html.escape(masoom)}</h1>
<p class="points">Every physical item this envelope will hold, one card each — real content where it exists, clearly marked placeholders where nothing has been allocated yet.</p>
<p class="cardsback"><a href="envelope-{num}.html">&larr; Back to the full envelope</a></p>
<div class="itemgrid">
{''.join(cards)}
</div>
</article>"""


def build():
    os.makedirs(OUT, exist_ok=True)

    for num, month, masoom, session in ENVELOPES:
        src = envelope_source(num)
        body = build_envelope(num, month, masoom, session, src)
        with open(os.path.join(OUT, f"envelope-{num}.html"), "w", encoding="utf-8") as f:
            f.write(page(f"{masoom} — Envelope {num}", month, body))

        cards_body = build_envelope_cards(num, month, masoom, session, src)
        with open(os.path.join(OUT, f"envelope-{num}-cards.html"), "w", encoding="utf-8") as f:
            f.write(page(f"{masoom} — cards", month, cards_body))

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
        rows.append(f"""<div class="tilewrap">
<a class="tile" href="envelope-{num}.html">
<span class="tilenum">{num}</span>
<span class="tilemonth">{html.escape(month)}</span>
<span class="tilename">{html.escape(masoom)}</span>
<span class="tilesession">{html.escape(session)}</span>
</a>
<a class="tilecards" href="envelope-{num}-cards.html">All items as cards &rarr;</a>
</div>""")
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
<p class="sectionnote">Single envelopes about the companions. Five items, no date, bought one at a time.</p>
<div class="grid">{comp}</div>
</section>

<section id="notebook">
<h2>Noori's Notebook</h2>
<p class="sectionnote">One sheet, folded to eight pages, about a place or an event.</p>
<div class="grid">{zin}</div>
</section>"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Noor Post", "", body))

    # count what was actually written, rather than a formula that silently
    # drifts whenever a new page type is added (the card pages were missing)
    written = len(glob.glob(os.path.join(OUT, "*.html")))
    print(f"built {written} pages "
          f"({len(ENVELOPES)} envelopes + {len(ENVELOPES)} card views + "
          f"{len(COMPANIONS)} companions + {len(ZINES)} zines + index)")


if __name__ == "__main__":
    build()

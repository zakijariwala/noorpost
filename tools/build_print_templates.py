#!/usr/bin/env python3
"""Generate the companions-line print templates from the markdown source.

The first eighteen companion templates in 04-art/print/ were built by hand,
which is why the last twenty-one never got any — hand-building does not scale
with a line that keeps growing. This generates all four templates for every
entry in 08-companions/, so a new companion gets its templates the moment it
is written.

    python tools/build_print_templates.py            # write all
    python tools/build_print_templates.py --check    # verify, write nothing

--check regenerates in memory and diffs against what is on disk. It is how the
generator was proved faithful against the eighteen hand-built sets before it
was allowed to touch them.

Geometry, type and palette all come from assets/print.css, which is derived
from 00-foundations/design-system.md. Nothing about page size or colour is
decided here.

The line's protective rule changed on 2026-08-14. It used to be "no hadith
card, no event print", and the generator enforced the first half by simply
never emitting a card. The card half is overturned: these envelopes carry one,
numbered FIRST EDITION nn/39. What now has to hold is that the two chains stay
visibly separate, so guard() checks the narrower thing — no silsila segment
number anywhere in this line, and still no event print — and it runs on every
build, not only on --check. A card with no saying selected renders as an empty
slot; it never renders invented filler inside quote marks.
"""

import os, re, sys, html, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "08-companions")
OUT  = os.path.join(ROOT, "04-art", "print")


# ---------- markdown ----------

def inline(t):
    """Markdown inline -> HTML, matching the hand-built templates exactly."""
    t = html.escape(t, quote=True)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def read(slug):
    with open(os.path.join(SRC, f"{slug}.md"), encoding="utf-8") as f:
        return f.read().split("\n")


def name_of(lines):
    for ln in lines:
        m = re.match(r"^#\s+Everyone Else\s+—\s+(.+?)\s*$", ln)
        if m:
            return m.group(1)
    raise ValueError("no name heading")


def letter_title(lines):
    for ln in lines:
        m = re.match(r"^## Letter\s+—\s+\*(.+?)\*", ln)
        if m:
            return m.group(1)
    raise ValueError("no letter title")


def letter_voices(lines):
    out, on = [], False
    for ln in lines:
        if "LETTER START" in ln:
            on = True; continue
        if "LETTER END" in ln:
            break
        if not on:
            continue
        s = ln.strip()
        if not s or s == "---":
            continue
        if s.startswith("●○"):
            out.append(('<p class="voice together"><span class="mark">●○</span>'
                        + inline(s[2:].strip()) + "</p>"))
        elif s.startswith("●"):
            out.append(('<p class="voice adult"><span class="mark">●</span>'
                        + inline(s[1:].strip()) + "</p>"))
        elif s.startswith("○"):
            out.append(('<p class="voice child"><span class="mark">○</span>'
                        + inline(s[1:].strip()) + "</p>"))
    return out


def items(lines):
    """The '## Items' table as a list of (n, item, spec, state)."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            if on:
                break
            if ln.startswith("## Items"):
                on = True
            continue
        if on and re.match(r"^\|\s*\d+\s*\|", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            out.append((int(cells[0]), cells[1], cells[2], cells[3]))
    if not out:
        raise ValueError("no items table")
    return out


def hadith_card(lines):
    """(masoom, theme, state) for the card row. masoom/theme are None when the
    selection rule cannot produce a candidate — Khawla points to no Masoom."""
    for _, item, spec, state in items(lines):
        if item != "Hadith card":
            continue
        m = re.match(r"Saying of \*\*(.+?)\*\*, matched to (.+?)\. Conduct", spec)
        return (m.group(1), m.group(2), state) if m else (None, None, state)
    raise ValueError("no hadith card row")


def fact_panel(lines):
    """The '## Fact panel' section: its ### heading, its ● bullets, its closing line."""
    body, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            if on:
                break
            if ln.startswith("## Fact panel"):
                on = True
            continue
        if on:
            body.append(ln)

    heading, parts = None, []
    for ln in body:
        s = ln.strip()
        if not s or s == "---":
            continue
        if s.startswith("### "):
            heading = s[4:].strip()
            continue
        if s.startswith("● "):
            parts.append('<p class="bullet"><span class="dot">●</span>'
                         + inline(s[2:].strip()) + "</p>")
        else:
            parts.append("<p>" + inline(s) + "</p>")
    if heading is None:
        raise ValueError("no ### heading in fact panel")
    return heading, parts


# ---------- templates ----------

def letter_html(name, title, voices):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Companion — {html.escape(name)} — Letter</title>
<link rel="stylesheet" href="assets/print.css">\n<script defer src="assets/overflow-guard.js"></script>
<style>@page {{ size: 148mm 210mm; margin: 0; }} body {{ display:flex; justify-content:center; background:#ddd; }} .page {{ padding: 14mm 12mm; }}</style>
</head><body>
<p class="screen-only">Companion: {html.escape(name)} — letter (front), A5 portrait. Real, final text.</p>
<div class="page page-custom" style="width:148mm;height:210mm;">
<p class="kicker">Everyone Else · {html.escape(name)}</p>
<h1 class="letter-title">{html.escape(title)}</h1>
<p class="voicekey"><span class="mark">●</span> the grown-up \xa0·\xa0 <span class="mark">○</span> is you \xa0·\xa0 <span class="mark">●○</span> together</p>
<div class="letter">
{chr(10).join(voices)}
</div>
</div>
</body></html>
"""


def panel_html(name, heading, parts):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Companion — {html.escape(name)} — Fact panel</title>
<link rel="stylesheet" href="assets/print.css">\n<script defer src="assets/overflow-guard.js"></script>
<style>@page {{ size: 148mm 210mm; margin: 0; }} body {{ display:flex; justify-content:center; background:#ddd; }} .page {{ padding: 12mm 12mm; }}</style>
</head><body>
<p class="screen-only">Companion: {html.escape(name)} — fact panel (letter reverse), A5 portrait. Every claim is TO VERIFY.</p>
<div class="page page-custom" style="width:148mm;height:210mm;">
<div class="watermark-placeholder"><span>UNVERIFIED — TO VERIFY</span></div><p class="kicker">Everyone Else · {html.escape(name)} · Fact panel</p>
<div class="panel">
<h3>{html.escape(heading)}</h3>
{chr(10).join(parts)}
<hr>
</div>
</div>
</body></html>
"""


def card_html(name, masoom, theme, state):
    """The hadith card, front + back. No saying is selected for any of the
    thirty-nine, so the saying area prints as an empty slot with the selection
    rule beside it. Nothing here is ever set inside quote marks."""
    if masoom:
        rule = (f"The saying is of <strong>{html.escape(masoom)}</strong> — the Masoom this "
                f"envelope points home to — matched to {inline(theme)}, and never a repeat "
                f"of that Masoom&rsquo;s box card.")
        slot = ("SAYING NOT YET SELECTED<br>Arabic, translation and internal-number "
                "citation set here<br>— nothing is printed in this slot until a row on "
                "citation-sheet.md reaches V")
    else:
        rule = ("This envelope points home to no Masoom, so the selection rule produces no "
                "candidate. What the card carries is an open decision, not a sourcing job.")
        slot = ("SAYING BLOCKED ON A DECISION<br>The entry itself is awaiting a scholar call "
                "on whether it survives<br>— see 08-companions/khawla.md")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Companion — {html.escape(name)} — Hadith card</title>
<link rel="stylesheet" href="assets/print.css">\n<script defer src="assets/overflow-guard.js"></script>
<style>@page {{ size: 105mm 148mm; margin: 0; }} body {{ background:#ddd; }}
.sheet {{ display:flex; flex-wrap:wrap; justify-content:center; gap:6mm; }}
.page {{ padding: 0; }}
.chain {{ font-size:8pt; font-variant:small-caps; letter-spacing:0.05em; color:var(--accent-primary); }}
.chain em {{ font-style:normal; opacity:0.55; }}
@media print{{.page{{page-break-after:always;}}.page:last-child{{page-break-after:auto;}}}}
</style></head><body>
<p class="screen-only">Companion: {html.escape(name)} — hadith card, front + back, A6 portrait.
<strong>No saying is selected.</strong> 0 of 39 selected across the line; the front carries an empty
slot rather than placeholder text, because a screenshot of a card loses whatever label surrounded it.
The chain mark reads <code>nn</code> because the ordering scheme is undecided — see TASKS.md Phase 8.</p>
<div class="sheet">

<div class="page page-a6-portrait">
  <div class="watermark-placeholder"><span>NO SAYING SELECTED</span></div>
  <div class="hadith-front">
    <p class="chain">First Edition <em>nn</em>&thinsp;/&thinsp;39</p>
    <div class="placeholder-box" style="min-height:60mm;">{slot}</div>
    <p style="font-size:7pt; text-align:center; color:var(--accent-tertiary);">NOT A SILSILA SEGMENT — THIS LINE HAS ITS OWN CHAIN</p>
  </div>
</div>

<div class="page page-a6-portrait">
  <div class="watermark-placeholder"><span>NO SAYING SELECTED</span></div>
  <div class="hadith-front hadith-back">
    <p class="chain">Everyone Else &middot; {html.escape(name)}</p>
    <div class="citation">
      <p>{rule}</p>
      <p style="margin-top:6mm;"><strong>Status:</strong> {inline(state)}</p>
      <p style="margin-top:6mm; font-size:8pt; opacity:0.8;">Work, internal number, translator and edition print here. Conduct and ethics only, quoted exactly, from a fixed edition, cited by the work&rsquo;s own internal number — the same bar as a box card, per <code>sourcing-rules.md</code>.</p>
    </div>
  </div>
</div>

</div>
</body></html>
"""


def postcard_html(name):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Companion — {html.escape(name)} — Postcard</title>
<link rel="stylesheet" href="assets/print.css">\n<script defer src="assets/overflow-guard.js"></script>
<style>@page {{ size: 148mm 105mm; margin: 0; }} body {{ background:#ddd; }}
.postcard-back-inner{{padding:10mm;height:100%;display:flex;flex-direction:column;justify-content:center;}}
.postcard-back-inner p{{font-size:11pt;line-height:1.6;margin:0 0 6mm 0;}}
.sig-line{{display:flex;gap:8mm;font-size:10pt;}}
.sig-line span.blank{{border-bottom:0.3mm solid var(--text);flex:1;display:inline-block;height:5mm;}}
@media print{{.page{{page-break-after:always;}}.page:last-child{{page-break-after:auto;}}}}
</style></head><body>
<p class="screen-only">Companion: {html.escape(name)} — return postcard, front + back, A6 landscape.</p>
<div class="page page-custom" style="width:148mm;height:105mm;"><div class="placeholder-box" style="position:absolute; inset:8mm;">ART PLACEHOLDER<br>Postcard front — not yet specified<br>(no source spec exists for companion postcards)<br>— see 08-companions/README.md</div></div>
<div class="page page-custom" style="width:148mm;height:105mm;"><div class="postcard-back-inner">
<p>We opened this one together.</p>
<div class="sig-line"><span>●</span><span class="blank"></span><span>○</span><span class="blank"></span></div>
<p style="font-style:italic; margin-top:6mm; font-size:9.5pt;">Post it back to us, or keep it. Either is right.</p>
</div></div>
</body></html>
"""


# ---------- the rule this line is held to ----------

ITEMS = ["Letter + fact panel", "Hadith card", "Person print",
         "Sticker sheet", "Return postcard"]


def guard(slug, lines, out):
    """Fail the build if an entry or its templates break the 2026-08-14 rule.

    Two chains, kept visibly apart: fourteen silsila segments in the box,
    thirty-nine FIRST EDITION cards outside it. This checks the separation and
    the surviving half of the old rule — never an event print in this line.
    """
    got = [item for _, item, _, _ in items(lines)]
    if got != ITEMS:
        raise SystemExit(f"{slug}: items are {got}, expected {ITEMS}")

    # A number is what makes it a segment mark. Saying "not a silsila segment"
    # on the card face is the rule being stated, not broken.
    segment = re.compile(r"silsila\s+segment\s*\d|segment\s+\d+\s+of\s+14", re.I)
    for fname, content in out.items():
        if segment.search(content):
            raise SystemExit(f"{fname}: carries a silsila segment number — "
                             "that chain belongs to the box alone")
        if re.search(r"\bevent print\b", content, re.I):
            raise SystemExit(f"{fname}: carries an event print — the calendar "
                             "ring stays box-only")


# ---------- driver ----------

def render(slug):
    lines = read(slug)
    name  = name_of(lines)
    heading, parts = fact_panel(lines)
    masoom, theme, state = hadith_card(lines)
    out = {
        f"companion-{slug}-letter.html":      letter_html(name, letter_title(lines), letter_voices(lines)),
        f"companion-{slug}-fact-panel.html":  panel_html(name, heading, parts),
        f"companion-{slug}-hadith-card.html": card_html(name, masoom, theme, state),
        f"companion-{slug}-postcard.html":    postcard_html(name),
    }
    guard(slug, lines, out)
    return out


def main():
    check = "--check" in sys.argv
    slugs = sorted(f[:-3] for f in os.listdir(SRC)
                   if f.endswith(".md") and f != "README.md")

    written = new = differs = 0
    diffs = []
    for slug in slugs:
        for fname, content in render(slug).items():
            path = os.path.join(OUT, fname)
            existing = None
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    existing = f.read()
            if existing is None:
                new += 1
            elif existing != content:
                differs += 1
                diffs.append((fname, existing, content))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                written += 1

    print(f"{len(slugs)} companions · {len(slugs)*4} templates")
    print(f"  new (were missing): {new}")
    print(f"  differ from disk:   {differs}")
    if check:
        print("  --check: nothing written")
        for fname, old, cur in diffs[:3]:
            print(f"\n--- {fname} ---")
            for line in list(difflib.unified_diff(
                    old.split("\n"), cur.split("\n"), "on disk", "generated", n=1))[:25]:
                print("   " + line.rstrip())
    else:
        print(f"  written:            {written}")


if __name__ == "__main__":
    main()

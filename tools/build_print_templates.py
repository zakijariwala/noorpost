#!/usr/bin/env python3
"""Generate the companions-line print templates from the markdown source.

The first eighteen companion templates in 04-art/print/ were built by hand,
which is why the last twenty-one never got any — hand-building does not scale
with a line that keeps growing. This generates all three templates for every
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


# ---------- driver ----------

def render(slug):
    lines = read(slug)
    name  = name_of(lines)
    heading, parts = fact_panel(lines)
    return {
        f"companion-{slug}-letter.html":     letter_html(name, letter_title(lines), letter_voices(lines)),
        f"companion-{slug}-fact-panel.html": panel_html(name, heading, parts),
        f"companion-{slug}-postcard.html":   postcard_html(name),
    }


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

    print(f"{len(slugs)} companions · {len(slugs)*3} templates")
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

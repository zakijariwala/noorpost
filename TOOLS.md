# Tools

Everything used to get Noor Post to where it is, and what you need to keep
going on your own machine. Written 2026-10-10, at the hand-off from the cloud
sessions to local work.

---

## The short version

| Need | Tool | Required for |
|---|---|---|
| Python **3.11+** | language for every build script | everything |
| PyYAML | the only pip dependency of the source pipeline | the corpus, tests |
| Node.js **22** + Playwright **1.56** + Chromium | printing designs to PDF and preview images | design work only |
| Git + a GitHub account | the repo, the site | everything |
| Pillow (optional) | `tools/contact_sheet.py`, for reviewing previews side by side | design review only |
| poppler (optional) | `pdftotext`, `pdftoppm` — extracting and viewing source PDFs | source work only |
| tesseract (optional) | OCR for image-only PDFs | rarely |

**Nothing else.** No framework, no bundler, no image generator, no paid service.
Every drawing in the designs is SVG written by Python.

---

## Setting up your machine

```bash
git clone https://github.com/zakijariwala/noorpost.git
cd noorpost
python -m pip install -r requirements.txt      # PyYAML
python -m unittest discover -s tests            # 118 tests — should all pass
```

That is enough for writing, sourcing and the site. For the designs:

```bash
# Node 22 from nodejs.org (or: winget install OpenJS.NodeJS.LTS / brew install node@22)
npm install -g playwright@1.56.1
npx playwright install chromium                 # downloads the browser once
python -m pip install Pillow                    # optional, for contact sheets
```

Then, from the repo root:

```bash
# macOS / Linux
NODE_PATH=$(npm root -g) node tools/render_envelopes.js
# Windows PowerShell
$env:NODE_PATH = (npm root -g); node tools/render_envelopes.js
```

Optional source tools — only if you re-extract or look at original PDFs:
`brew install poppler` / `apt install poppler-utils` /
[poppler for Windows](https://github.com/oschwartz10612/poppler-windows).

---

## What each tool did

### Python (3.11 in CI, 3.13 on the Windows machine)

Every script in `tools/` is Python using only the standard library, except
PyYAML for source metadata and Pillow for the optional contact sheet. CI pins
**3.11**, so keep code 3.11-compatible — in particular **no backslash inside an
f-string's `{…}`** and no reuse of the outer quote character inside it (both are
3.12+ only and have broken builds here before).

| Script | Job |
|---|---|
| `build_envelopes.py` | The fourteen box envelopes, every item, each in its own style → `04-art/envelopes/` |
| `envelope_themes.py` | The fourteen styles and each envelope's scenes, as data |
| `envelope_art.py` | The box's drawing kit: dunes, skies, shrines, objects. **No figure anywhere in it.** |
| `mourning_art.py` | 01 and 02's own art: ink wash and engraving, two inks each |
| `envelope_sources.py` | Reads every word of an envelope from the markdown |
| `build_companions.py` | The thirty-nine companion envelopes → `04-art/companions/` |
| `companion_themes.py` | The companions line: one style, each person's colours, portrait, place, stickers |
| `companion_art.py` | Portraits (faces allowed in this line), props, the scene composer, objects |
| `companion_sources.py` | Reads a companion entry from `08-companions/` |
| `build_print_templates.py` | Plain text-layout templates for the companions → `04-art/print/` |
| `build_site.py` | The published site → `docs/` |
| `contact_sheet.py` | Previews side by side, for review |
| `build_source_corpus.py`, `source_search.py`, `source_audit.py`, `fetch_thaqalayn.py`, `extract_text.py`, `page_image.py` | The source pipeline — see `00-sources/README.md` |
| `select_hadith_cards.py`, `apply_hadith_assignments.py`, `verify_hadith_assignments.py` | Choosing and recording the hadith cards |

### Node.js + Playwright + Chromium

The designs are HTML pages with mixed `@page` sizes. `render_envelopes.js` and
`render_companions.js` open each page in headless Chromium, wait for the layout
script (`04-art/envelopes/envelope.js`) to flow the letter and fit the panels,
**refuse to print anything that still overflows**, then write one PDF per
envelope (`pdf/`) and a JPEG of every item (`preview/`). The site uses those
previews. Playwright was the only Node dependency.

### The review loop

Every design round in the 2026-10 sessions went the same way, and it is the
thing to keep doing:

1. Change data or drawing code → `python tools/build_envelopes.py` (or `build_companions.py`).
2. Render → `node tools/render_envelopes.js` (or `render_companions.js`).
3. Sheet the previews → `python tools/contact_sheet.py out.png 330 5 04-art/envelopes/preview/*-front.jpg`.
4. Look at the sheet, not the code. Fix what reads wrong. Repeat.
5. Before committing: `python -m unittest discover -s tests`, and `--check` on both builders.

### Git, GitHub, GitHub Pages, GitHub Actions

- The site is GitHub Pages from `main`, folder `/docs`: https://zakijariwala.github.io/noorpost/
- `.github/workflows/site.yml` runs on every push to `main`: validates source
  metadata, runs the tests, rebuilds the corpus and `docs/`, and commits the
  result back (`Rebuild the site and reports [skip ci]`). **So: merge to `main`
  and the site updates itself in a few minutes.**
- Work went on branches and pull requests (#7 – #10). **One lesson:** PR #9 was
  merged before its last two commits were pushed, so they never reached the
  site and needed PR #10. Before merging, check the PR's commit list is complete.
- **Caching:** Pages serves files with a 10-minute cache, and browsers keep
  images longer. `build_site.py` therefore links every design preview and PDF
  with a content fingerprint (`01-front.jpg?v=2d193153b1`), so a changed image
  gets a new address and shows at once. If something still looks old, hard-refresh.
- Release `sources-v1` holds the original source PDFs as a zip (not tracked in git).

### Claude Code — where the work was done

The design and build work in October 2026 was done with **Claude Code in a
cloud session** (claude.ai/code), connected to this repo. Inside it:

| Tool | Used for |
|---|---|
| **GitHub MCP connector** | Opening, reading and updating pull requests; checking merge state. (The cloud sandbox had no `gh` CLI.) |
| **Artifact canvas** (Claude Design) | The interactive design canvas in `04-art/design-canvas/` (`*.dc.html`) — the earlier style exploration, A/B/C and D/E/F directions, Muharram variations. |
| Headless Chromium + Playwright | Rendering, and screenshots to look at every change. |
| Pillow | Contact sheets for review. |

**Connectors that were available but not used for the designs:** Canva,
Figma, Google Drive/Docs/Sheets/Slides, Excalidraw. They are not needed: the
designs are code, so they rebuild exactly from the repo.

### Canva

`04-art/canva-build-brief.md` (2026-08-24) is a brief for building the
templates **by hand in Canva** — 24 master templates, sizes with bleed, the
ring-punch coordinates, the placeholder rules. It predates the coded designs
and is now an alternative path, not the current one. If final artwork is
commissioned in Canva or anywhere else, the coded designs (`04-art/envelopes/`,
`04-art/companions/`) are the reference for composition, palette and medium.
Note from that brief: Canva Free cannot upload fonts, so Fraunces may need a
substitute there.

### Sources (data, not software)

- **thaqalayn.net** — 32 Shia collections pinned in `00-sources/api/` by
  SHA-256; an approved source of record since 2026-08-24.
- **al-Islam.org** — several fixed editions (Tuhaf al-Uqul, Risalat al-Huquq,
  Sahifa Sajjadiyya, Uyun). It blocks scripts: open those links in a browser.

### Fonts

All design faces are SIL Open Font License, served locally from
`04-art/envelopes/fonts/` so printing works offline: Fraunces, Young Serif,
Bricolage Grotesque, Cormorant Garamond, Gloock, Marcellus, Space Grotesk,
Nunito Sans, Newsreader, Alegreya, Literata, Karla, Lora, Atkinson Hyperlegible.

---

## Cloud-only conveniences you will not have locally

- `NODE_PATH=/opt/node22/lib/node_modules` — a cloud path. Locally use `$(npm root -g)`.
- Chromium was preinstalled in the cloud; locally run `npx playwright install chromium` once.
- `python3.11` was used to mirror CI. Locally any 3.11+ is fine; if you have 3.12+,
  the f-string rule above is what keeps CI green.

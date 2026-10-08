# The fourteen envelopes — fourteen styles

Every envelope in the box, every item, each in its own style (decided 2026-10-08, `00-foundations/design-system.md` §1). Open `index.html` for the set, or any `envelope-NN.html` to see every item at true size. `pdf/` holds the printed sheets: one PDF per envelope, each page at its item's real size.

| Env | Month | Style |
|---|---|---|
| 01 | Muharram | M2 Ink Wash — mourning |
| 02 | Safar | M1 Charcoal Line — mourning |
| 03 | Rabi al-Awwal | C Paper Dunes |
| 04 | Rabi al-Thani | B3 Big Shapes |
| 05 | Jumada al-Awwal | D Illuminated |
| 06 | Jumada al-Thani | F Suzani |
| 07 | Rajab | A3 Mosaic Stars |
| 08 | Rajab | A Lantern Night |
| 09 | Sha'ban | C2 Dune Night |
| 10 | Sha'ban | A2 Lantern Dawn |
| 11 | Ramadan | B Tile Explorer |
| 12 | Shawwal | E Riso Press |
| 13 | Dhul Qa'dah | G Watercolour |
| 14 | Dhul Hijjah | C4 Garden Pop-up |

## What each envelope contains

Envelope front and back with the wax seal · inside flap · the letter, one A4 sheet folded to four A5 faces (letter, letter, the line said together, fact panel) · hadith card front and back · the session card in its kind — conversation, mourning, open, or a **case file** (question card, five evidence cards at A7, sealed answer) · person print · event print with the ring punch · sticker sheet, or the **pennant** in 01 and 02 · return postcard front and back.

## Build and print

```bash
python tools/build_envelopes.py                               # writes envelope-NN.html and index.html
python tools/build_envelopes.py --check                       # exit 1 if stale
NODE_PATH=$(npm root -g) node tools/render_envelopes.js       # writes pdf/ and preview/, refuses any envelope that overflows
python tools/build_site.py                                    # copies the set into docs/envelopes/ and onto each envelope's page
python -m unittest discover -s tests                          # includes tests/test_envelopes.py
```

| File | Role |
|---|---|
| `tools/envelope_sources.py` | Reads every word from source: `01-pilot/envelope-03/` and `03-content/envelope-NN.md`, sayings from `hadith-assignments.json`. |
| `tools/envelope_themes.py` | The fourteen styles as data, and each envelope's subjects from `04-art/prompts.md`. |
| `tools/envelope_art.py` | One kit of drawings, drawn by a pen whose mode is the style: cut, flat, line, wash, stitch, riso, gilt. **No figure anywhere in it.** |
| `tools/build_envelopes.py` | Assembles every item; enforces the no-envelope-number rule on cards. |
| `envelope.css` | What every style shares: sizes, the folded letter, voices, card positions, ring punch. |
| `envelope.js` | Lays each envelope out in the browser: flows the letter across faces 1–2 for that style's fonts, shrinks dense cards slightly, flags anything that still overflows. |
| `fonts/` | All fourteen families (SIL OFL), local, for offline print. |

## On the site

`tools/build_site.py` copies this folder into `docs/envelopes/` and puts each envelope's design on its own page: a **The design** section under the heading (every item, plus links to the true-size set and the print PDF), the design on each item in the card view, and the front on the home-page tile. Re-run `render_envelopes.js` before the site build whenever an envelope changes, so the previews and PDFs match.

## Rules held on every build

- No envelope number on any hadith card, front or back.
- A silsila segment prints only when decided — envelope 03's is shown as `––`.
- **06 and 10 have no saying selected** (both blocked on a source). Their cards print a marked empty slot, never filler in quote marks.
- 01 and 02 carry charcoal and ivory only — every colour on the page is checked.
- Every letter line in source appears in the sheet; the last (●○) line is set alone on face 3.
- The fact panel carries the TO VERIFY watermark.

## Still open

- **The art is production-quality placeholder.** It fixes composition, palette and medium for every item; final illustration can be commissioned or generated against `04-art/prompts.md`, per-envelope style lines included.
- Sayings for 06 and 10; envelope 03's segment number; the return address; bleed and CMYK (prepress).
- The companions line still prints in Paper Dunes from `04-art/print/`.

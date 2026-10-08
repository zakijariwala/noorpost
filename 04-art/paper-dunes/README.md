# Paper Dunes — the complete envelope

The house style since 2026-10-08 (`00-foundations/design-system.md` §1–2, amended). Layered cut paper: dunes, palms, a dome, a road, a cloak, in sand, apricot, rose clay, oasis teal and dusk plum. Young Serif for titles and the child's voice, Nunito Sans for reading aloud.

| File | What it is |
|---|---|
| `envelope-03.html` | **Every item in envelope 03, at true size.** Envelope front and back with the wax seal; the inside flap; the letter as one A4 sheet folded to A5 (face 1–2 the letter, face 3 the line said together, face 4 the fact panel); hadith card front and back; session card front and back; person print; event print with the ring punch; sticker sheet; return postcard front and back. |
| `envelope-01.html` | The mourning issue. Same set with the colour taken out: black on ivory, the pennant in place of the stickers, the standard with no rider. |
| `pdf/` | Both sheets printed to PDF. One page per item, each at its own size (C5, A4, A5, A6, flap). |
| `paper-dunes.css` | Page sizes and layouts for the set. Palette, faces and text classes come from `../print/assets/print.css`. |

## Rebuild

```bash
python tools/build_paper_dunes.py          # writes envelope-03.html, envelope-01.html
python tools/build_paper_dunes.py --check  # exits 1 if they are stale
```

Every word is read from source: the letter, fact panel and session card from `01-pilot/envelope-03/`, the sayings from `00-foundations/hadith-assignments.json`. Edit those, not the HTML.

To print, open the HTML in Chromium and print to PDF with **margins: none** and **background graphics on**; the named CSS pages give each item its own paper size. Or headless: `page.pdf({preferCSSPageSize: true, printBackground: true})`.

## The art

All of it is drawn by `tools/paperdunes_art.py` as SVG from a small kit of shapes. There is **no figure anywhere in the kit**, so nothing drawn from it can depict one of the Fourteen (`design-system.md` §3). The same functions draw the mourning art in line mode: charcoal outline on ivory, no fill colour.

These are production-quality placeholders, not the final commission. They fix composition, palette and layering for every item, so an illustrator (or the prompt block in `../prompts.md`) has an exact target.

## Rules the build enforces

- **No envelope number on a hadith card**, front or back (`design-system.md` §7). `card_guard()` fails the build if one appears.
- **The segment number prints as `––` while it is undecided.** Envelope 03's card is claimed as segment 13 by `citation-sheet.md` and segment 1 by `items.md`; the dot on the back stays empty until that is settled.
- **The fact panel carries the TO VERIFY watermark** until its rows on `citation-sheet.md` read `V`.
- **The last letter line must be the ●○ line**, since face 3 is built around it. The build stops if it is not.

## Still open

- Return address — bracketed, not set.
- The other twelve envelopes' full sets: the generator reads envelope 03's sources; extending it means pointing it at each envelope's files and adding their scenes to the art kit.
- Bleed (3 mm) and CMYK conversion — prepress, as before.

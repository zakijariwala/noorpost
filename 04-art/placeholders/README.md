# Placeholder art — placement tests only

Ten watercolour shrine images saved from Pinterest (2026-10-08), used to test how **finished, painterly art** sits in the Paper Dunes frames: on sand stock, under the postmark, above the dune band.

**They are not ours and not licensed.** Credits are in `manifest.json`. They are never printed, never sold, never published, and never go into `docs/`. Because this repository is **public**, the images, their crops and the rendered sheet are git-ignored (`.gitignore`). Only this README, `manifest.json` and `tools/build_placement_test.py` are tracked. Every page also carries a **PLACEHOLDER — NOT LICENSED** watermark in print as well as on screen.

## Run it

1. Put the source screenshots in `04-art/placeholders/src/<id>.png`, using the ids in `manifest.json`.
2. `python tools/build_placement_test.py`. This crops each image (cutting away the Pinterest buttons) and writes `placement-test.html`.

## Where each one goes

Every image sits where `04-art/prompts.md` places that subject:

| Envelope | Item | Stand-in |
|---|---|---|
| 13 · Imam al-Rida | Envelope front, person print, postcard | Mashhad ×3 |
| 14 · Imam al-Jawad | Person print | Kadhimiya |
| 08 · Imam al-Kadhim | Person print, in an arch frame | Minaret through a window ("a barred window in Baghdad") |
| 10 · Imam al-Mahdi | Event print | Jamkaran |
| 04 · Imam al-Askari | Person print | Shrine grille (stand-in for Samarra) |
| 01 · Imam Husayn | Person print, postcard test | Karbala dome, **in greyscale**: mourning stays black on ivory |
| Everyone Else · al-Abbas | Person print | Shrine of al-Abbas |

## What it showed

- **Watercolour on paper works on sand stock.** Set with a multiply blend and a feathered edge, the painting's own paper drops away and the stock shows through. Images on white or near-sand paper vanish into the page completely. Darker, textured paper (the first Mashhad image) still reads as a soft oval.
- **The mourning rule holds with painterly art.** Greyscale watercolour on ivory reads as mourning without looking like a missing colour proof.
- **The arch frame from the hadith card carries a photographic or dark image well.** Use it whenever the art does not have a light ground.
- **The envelope front takes a vignette** to the right of centre, under the postmark, with room left for the name area.

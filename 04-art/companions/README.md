# Everyone Else — the companions, designed

Built by `tools/build_companions.py`; printed by `tools/render_companions.js`.
One file per companion, every item at true size, printing to one PDF.

**One style for the whole line**, not one per envelope — unlike the box's
fourteen. Thirty-nine envelopes that belong together, like a set of stamps:

- **Front:** airmail-striped envelope; the person on a large perforated stamp,
  `FIRST EDITION · nn/39` under their name; the line's plain seal (no month, no
  cancellation — these are dateless); the points-home line, large.
- **Letter:** the box's folded A4 → four A5 faces, the fact panel on face 4.
- **Hadith card:** the card as a stamp, on its own chain (`nn/39`), never a
  silsila segment. Back: the thirty-nine-stamp grid, this one filled, and a
  draft *In our words* line (`00-foundations/hadith-glosses.json`, `companions`).
- **Person print:** a portrait — faces are allowed in this line
  (`08-companions/README.md`). Drawn by `tools/companion_art.figure`.
- **Stickers:** the person's own stamp, plus five from their entry's spec.
- **Return postcard:** their place, no person; fixed wording on the back.
- **Never an event print.**

Each person brings their own colours, place, portrait and stickers:
`tools/companion_themes.py`. Built in batches of three, in card order
(`hadith-assignments.json` `n`); `BATCHES` there lists what is done.

The shared stylesheet, layout script and fonts are the box's
(`../envelopes/`); `companion.css` holds only what is the line's own.

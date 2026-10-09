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
(`hadith-assignments.json` `n`); all thirty-nine are done.

## Decisions taken in the art, for review

- **The family of the Fourteen are veiled in light.** Faces are allowed in
  this line, but for the mothers, wives, sons and daughters of a Masoom
  (`VEILED` in `companion_themes.py`: Fatima bint Asad, Abbas, Umm Kulthum,
  Rabab, Zaynab, Sakina, Umm al-Banin, Ruqayya, Umm Farwa, Hamida, Ma'suma,
  Narjis) the face is drawn as light, with no features — the convention of
  devotional art. A test holds it. Reverse it per person if the scholar says so.
- **No Masoom is ever drawn, even where an entry's print spec implies one.**
  Fatima bint Asad's "two boys" (the Prophet and Imam Ali), the boy beside
  Umm Farwa and Hamida (Imam al-Sadiq, Imam al-Kadhim) and Umm al-Banin's
  children are replaced by objects: two pairs of sandals, a book, four marks.
- **Fitrus has no figure** — a feather stands in for him, per his item spec.
- **Zaynab's sticker sheet leaves out the chain link** the spec allowed; a
  raised hand and a road carry it instead.
- **Khawla's card** prints its own block: a decision (the entry points to no
  Masoom), not a missing source.

The shared stylesheet, layout script and fonts are the box's
(`../envelopes/`); `companion.css` holds only what is the line's own.

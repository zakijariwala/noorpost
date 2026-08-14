# Art prompt packs

Phase 4. Prompts for illustration generation only — the person prints, event prints, sticker sheets, envelope graphics, pennant and box. **Not for the letter, fact panel, hadith card text, or session card** — those are typeset layouts, not illustrations, and belong in a document template (Job 2, see `README.md` note below), not an image generator.

Tool recommendation: **Adobe Firefly** first choice (commercial-safe training data, matters for a paid print product), **Midjourney** as an alternative if style consistency across 60+ pieces proves easier there. **Not Google Stitch** — that tool generates app/web UI screens, not print illustration; no bleed/trim control, no fixed physical dimensions.

Every prompt below is the **master style block** plus **item specifics**. Paste both together. Regenerate the style block from `00-foundations/design-system.md` if that file changes — this is a derived artifact, not a second source of truth.

---

## Master style block — standard palette

Prepend to every prompt for **The Fourteen (except 01, 02)**, **event prints**, and the **envelope exterior**:

```
MEDIUM: hand-inked line illustration, fine consistent line weight, subtly imperfect linework —
the look of a small devotional press woodcut or etching, not a corporate icon, not a cartoon,
not a digital-clean vector.

PALETTE — strict, no exceptions: warm ivory background #F3EDE1. Line and shadow in near-black
ink #211B14. Spot accent fills ONLY from: deep gold #A9762F, muted teal #2C5F5A, terracotta
#B4472A — used sparingly as flat fills, never gradients, never full-color rendering, never
photorealistic color grading.

COMPOSITION: quiet and restrained. One clear subject. Generous negative space. No busy or
detailed background. No decorative border unless specified below.

NEGATIVE PROMPT: no photorealism, no 3D render, no glossy gradients, no cartoon or anime
style, no text or lettering baked into the image unless specified, no color outside the
fixed palette, no violence, wounds, or weapons shown in use, no crowds.
```

## Master style block — mourning palette (envelopes 01, 02 only)

Same as above, with the palette clause replaced:

```
PALETTE — strict, no exceptions: warm ivory background #F3EDE1. Line and shadow in charcoal-
black ink #1B1B1B only. No accent color anywhere — no gold, no teal, no terracotta.
```

## The two faces rules — append the one that applies

**The Fourteen (every envelope, no exceptions):**
```
RULE — NEVER DEPICT ANY OF THE FOURTEEN: no face, no figure, no likeness of the Prophet or
any Imam or Sayyida Fatima. Show them only by setting, object or absence — a shield, a cloak,
a doorway, an empty road. This is absolute.

Ordinary people present at a place ARE permitted (amended 2026-08-12, scholar-approved):
pilgrims and visitors in a courtyard may be drawn, faces included. They are people who
happen to be there, not a depiction of anyone this box is about.
```

**The companions line only (`08-companions/`):**
```
RULE — FACES ALLOWED: a plain, dignified human figure or portrait is permitted here, and
should be used — this is the one place in the whole product where it's allowed, and it needs
to read as a deliberate difference at a glance. No attempt at photorealistic likeness. Keep
the figure in the same linework style as everything else in the series, not rendered any more
realistically than the objects around it.
```

---

## Style block key

Used below so every row doesn't repeat the full block. Paste the referenced block from above (or the zine block introduced below) ahead of every subject line.

| Key | Meaning |
|---|---|
| **STD** | Master style block — standard palette |
| **MOURN** | Master style block — mourning palette (01, 02 only) |
| **NOFACE** | No-faces rule |
| **FACES** | Faces-allowed rule (companions line only) |
| **ZINE** | Zine style block — see below |

## Style block — zines

Zines print single-ink on equipment already owned (`09-zines/README.md`), not the three-accent palette used everywhere else. Prepend to every zine cover:

```
MEDIUM: hand-inked line illustration, single ink only, fine consistent line weight, the same
small-press woodcut/etching character as the rest of the product.

PALETTE — strict: one ink color only (charcoal-black #1B1B1B), on a plain light ground.
No second color, no accent, no gradient, no fill beyond linework and solid black shapes.

COMPOSITION: quiet, a single clear subject, generous negative space, no text baked in.

RULE — NO FACES: these are places and events, not people. No human figure shown in detail.

NEGATIVE PROMPT: no color of any kind beyond the single ink, no photorealism, no gradients,
no cartoon style, no crowds, no violence.
```

---

## Worked pack 1 — Envelope 03 (the pilot)

Source: `01-pilot/envelope-03/items.md`. These five are what Phase 1 is actually waiting on.

### Person print — Masjid an-Nabawi
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: Masjid an-Nabawi, the Prophet's mosque at Medina. The green dome, catching early
light. Palm trunks in the foreground, trunks only, no fronds cluttering the silhouette.
Early morning — long shadows, low warm light, the gold accent used for the light itself,
not for the dome.

FORMAT: A5 portrait (148 × 210 mm), full bleed, vertical composition with the dome upper-
third, palms grounding the bottom third.

NOTE: this print pairs with two other Medina person prints (envelopes 05, 09) that also
show Jannat al-Baqi from different angles — if generating those in the same session, hold
the light and line-weight identical across all three so they read as one set on a wall.
```

### Event print — the arrival at Quba
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: An empty desert road, arriving at a palm grove — the road runs out of frame at the
bottom edge of the composition. One kneeling camel, riderless or rider implied only by an
empty saddle, near the grove's edge. No other figures, no caravan crowd.

FORMAT: A5 landscape (210 × 148 mm), full bleed. Leave a clear, undecorated 15mm margin at
top-center for a physical ring punch — do not place linework or the subject in that zone.

NOTE: this is one of fourteen event prints that must hang together on one ring as a single
calendar. Hold line weight and palette identical to the other event prints in this pack.
```

### Sticker sheet
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: five small independent motifs, each usable alone, none requiring the others:
1. A cloak laid flat, four corners individually marked/emphasised
2. A single palm (trunk and simple frond, not a grove)
3. A road disappearing to a point (the Quba road motif, simplified)
4. A caravan silhouette — camels only, no riders
5. A small repeatable mark set: one stone, one corner-angle, four small marks suggesting
   four hands meeting at a point

FORMAT: A6 (105 × 148 mm) sheet, die-cut, each motif isolated with clear cut-margin around
it, no shared background, no text anywhere on the sheet.
```

### Return postcard — front
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: the cloak shape alone — the same cloak motif as the sticker sheet's first item,
but rendered larger and as the sole subject, centered.

FORMAT: A6 landscape (148 × 105 mm), full bleed. No text of any kind — the postcard's fixed
wording is typeset separately on the reverse, not part of this image.
```

### Envelope exterior
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: a circular postal-cancellation stamp design, reading "RABI AL-AWWAL" around the
ring in the display face style (a warm, slightly irregular soft-serif letterform — see
`design-system.md` §1, Fraunces). Gold ink line only, no fill inside the circle. Leave the
center of the circle empty — the month name sits on the ring, not in the middle.

FORMAT: circular motif approx. 45mm diameter, transparent/isolated background so it can be
placed onto the envelope stock separately from the name area and wax-seal graphic.

NOTE: this is a lettering-heavy piece. If Firefly/Midjourney struggle with clean circular
type, generate the line-art ring alone and typeset "RABI AL-AWWAL" separately in Fraunces —
don't fight the tool for something a font file does perfectly.
```

---

## Worked pack 2 — the four new companions

Source: `08-companions/uthman.md`, `abbas.md`, `fizza.md`, `jabir.md`. Companions use the **faces-allowed** rule, not the no-faces rule — flagged in each prompt below.

### Uthman ibn Sa'id al-Amri — person print
```
[Master style block — standard palette]
[Faces-allowed rule]

SUBJECT: an older man at a market oil stall — jars lined up, a hand scale, a plain market
backdrop kept simple (a wall, an awning edge, nothing busy). His expression unremarkable,
ordinary — this is a portrait of someone deliberately unremarkable to look at, not a heroic
portrait. Nothing in his dress or bearing hints he is anything but a tradesman.

FORMAT: A5 portrait (148 × 210 mm), full bleed.
```

### Uthman — sticker sheet
```
[Master style block — standard palette]
[No-faces rule — stickers stay object-only even in the companions line]

SUBJECT: an oil jar, a hand scale, a sealed folded letter, a simple market stall outline,
and the small repeatable mark set shared across the companions line.

FORMAT: A6 (105 × 148 mm) sheet, die-cut, motifs isolated, no text.
```

### Abbas ibn Ali — person print
```
[Master style block — standard palette]
[Faces-allowed rule]

SUBJECT: a young man at a riverbank, a waterskin held in one hand, body turned back toward
an implied camp rather than toward the water — the composition should read as "leaving the
river," not "arriving at it." No armour detail rendered in a way that reads as battle-ready;
keep it plain. No other figures, no violence, no weapons shown in use.

FORMAT: A5 portrait (148 × 210 mm), full bleed.

CAUTION: this is Karbala-adjacent subject matter. Keep the image entirely on the water/
restraint moment — nothing suggesting combat, injury, or the events after this moment.
```

### Abbas — sticker sheet
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: a waterskin, a simple flag/standard shape, a river's edge line motif, and the
shared repeatable mark set.

FORMAT: A6 (105 × 148 mm) sheet, die-cut, motifs isolated, no text.
```

### Fizza — person print
```
[Master style block — standard palette]
[Faces-allowed rule]

SUBJECT: a woman at ordinary household work — hands occupied with a task (folding cloth,
tending a small fire, or similar plain domestic action), an open book or page resting
nearby but not the focus. Calm, unposed, not a devotional or reverent pose — she is working,
not performing.

FORMAT: A5 portrait (148 × 210 mm), full bleed.
```

### Fizza — sticker sheet
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: an open book/page motif, a water jug, a simple broom, and the shared repeatable
mark set.

FORMAT: A6 (105 × 148 mm) sheet, die-cut, motifs isolated, no text.
```

### Jabir ibn Abdullah al-Ansari — person print
```
[Master style block — standard palette]
[Faces-allowed rule]

SUBJECT: a very elderly man, clearly aged in posture and dress, being led gently by the
hand — only the leading hand visible, not a second full figure, keeping the focus on Jabir.
A doorway ahead of him, slightly open. Expression peaceful, unhurried, not strained.

FORMAT: A5 portrait (148 × 210 mm), full bleed.
```

### Jabir — sticker sheet
```
[Master style block — standard palette]
[No-faces rule]

SUBJECT: a doorway motif, a pair of clasped/leading hands (hands only, no arms or figures),
an open hand extended in greeting, and the shared repeatable mark set.

FORMAT: A6 (105 × 148 mm) sheet, die-cut, motifs isolated, no text.
```

---

## How to use every table below

Each row is a **SUBJECT** line, pulled verbatim or near-verbatim from the item's own spec file (`03-content/envelope-XX.md`, `08-companions/*.md`, or `09-zines/*.md`) — nothing invented. Paste: the style block(s) named in the row, then `SUBJECT: [text from the row]`, then the FORMAT line for that item type (given once per table, not repeated per row).

**Do not invent scene content the source files don't already specify.** The prompt's job is to render what's already been decided, not add new claims into the art the way an unreviewed detail could sneak an unverified fact into a printed product.

---

## Pack 3 — all fourteen envelopes

### Person prints
**Format:** A5 portrait (148 × 210 mm), full bleed.

| Env | Style | Subject | Note |
|---|---|---|---|
| 01 | MOURN + NOFACE | The shrine at Karbala. | |
| 02 | MOURN + NOFACE | Jannat al-Baqi as it stands — low wall, unmarked ground, date palms, no dome. | Angle 1 of 3 — hold light/line identical across 02, 05, 09 |
| 03 | STD + NOFACE | Masjid an-Nabawi — green dome, palm trunks, early light. | See Worked pack 1 for full prose version |
| 04 | STD + NOFACE | The shrine at Samarra. | Pairs with 11 — identical linework |
| 05 | STD + NOFACE | Jannat al-Baqi, second angle — palm shade, the same low wall. | Angle 2 of 3 |
| 06 | STD + NOFACE | The door and courtyard of Sayyida Fatima's house — no building survives, the print is the threshold itself. | |
| 07 | STD + NOFACE | The shrine at Najaf. | |
| 08 | STD + NOFACE | A barred window in Baghdad. Not the shrine. | Pairs with 14 — identical linework |
| 09 | STD + NOFACE | Jannat al-Baqi, third angle. | Angle 3 of 3 |
| 10 | STD + NOFACE | An empty road at dawn. No grave, so no shrine — the only person print in the box that isn't a burial place. | |
| 11 | STD + NOFACE | The shrine at Samarra. | Pairs with 04 — identical linework |
| 12 | STD + NOFACE | The teaching circle — lamplight, manuscripts, a courtyard in Medina. No figures; the circle is shown by what's left on the floor. | |
| 13 | STD + NOFACE | The shrine at Mashhad. | |
| 14 | STD + NOFACE | The shrine at Kadhimiya. | Pairs with 08 — identical linework |

### Event prints
**Format:** A5 landscape (210 × 148 mm), full bleed, 15mm undecorated top-center margin for the ring punch (`design-system.md` §6).

| Env | Style | Subject | Ring pos. |
|---|---|---|---|
| 01 | MOURN + NOFACE | Karbala. One object, no scene: a standard with no rider. | 1 |
| 02 | MOURN + NOFACE | Arbaeen — an empty road to a flat horizon at dusk. | 2 |
| 03 | STD + NOFACE | The arrival at Quba — see Worked pack 1. | 3 |
| 04 | STD + NOFACE | Samarra itself — a garrison city, walls and a river, no people. | 4 |
| 05 | STD + NOFACE | Sayyida Zaynab's shrine at Damascus. | 5 |
| 06 | STD + NOFACE | Bayt al-Ahzan, the house she went to grieve in. | 6 |
| 07 | STD + NOFACE | The Kaaba. | 7 |
| 08 | STD + NOFACE | The cave at Hira. | 8 |
| 09 | STD + NOFACE | Munajat Sha'baniyya — a courtyard at night, one lamp, no figures. | 9 |
| 10 | STD + NOFACE | Jamkaran. | 10 |
| 11 | STD + NOFACE | Laylat al-Qadr. | 11 |
| 12 | STD + NOFACE | Eid al-Fitr. | 12 |
| 13 | STD + NOFACE | Sayyida Masuma's shrine at Qom. | 13 |
| 14 | STD + NOFACE | Ghadir Khumm. | 14 — last on the ring |

> Envelope 06's event print is `TRAD`-marked in `citation-sheet.md` — the image itself carries no claim needing the marker (a house, not an assertion), but keep the linework as restrained/undramatized as the other twelve.

### Sticker sheets (12 — not 01, 02, which take a pennant instead)
**Format:** A6 (105 × 148 mm) die-cut sheet, motifs isolated, no shared background, no text.

| Env | Style | Subject |
|---|---|---|
| 04 | STD + NOFACE | Letters, seals, a river, a road, small repeatable marks |
| 05 | STD + NOFACE | A pen, a split fruit, palm shade, small repeatable marks |
| 06 | STD + NOFACE | A hand-mill, a bowl, a threshold, counting marks in groups of ten |
| 07 | STD + NOFACE | A shield, a set of scales, a doorway, small repeatable marks |
| 08 | STD + NOFACE | A window, a lamp, a folded letter, small repeatable marks |
| 09 | STD + NOFACE | A list, an ear, a hand, a foot, a doorway, numbered marks |
| 10 | STD + NOFACE | Includes the seal used to close the letters written in the session — this sheet has a job beyond decoration |
| 11 | STD + NOFACE | A mat, a doorway at night, a lamp, small repeatable marks |
| 12 | STD + NOFACE | Manuscripts, a lamp, a flask, a courtyard, small repeatable marks |
| 13 | STD + NOFACE | A road, a coin, a sealed letter, a doorway, small repeatable marks |
| 14 | STD + NOFACE | A row of empty seats, a branching diagram, a doorway, small repeatable marks |

Envelope 03's sticker sheet is in Worked pack 1.

### Pennants (01, 02 only, replacing the sticker sheet)
**Format:** dimension not fixed — see `design-system.md` §4, decide against a physical proof, not a ruler. Generate the motif at a flexible aspect ratio for now.

```
[MOURN]
[NOFACE]

SUBJECT — envelope 01: the standard motif from the event print, simplified to a single
clean line-icon suitable for a small cord-mounted pennant.

SUBJECT — envelope 02: the empty-road motif from the event print, simplified the same way.

FORMAT: triangular pennant face, single motif centered, charcoal ink on ivory stock.
```

### Return postcards — front
**Format:** A6 landscape (148 × 105 mm), full bleed, no text (fixed wording is typeset separately on the reverse).

| Env | Style | Subject |
|---|---|---|
| 01 | MOURN + NOFACE | The standard (same motif as the event print) |
| 02 | MOURN + NOFACE | The empty road |
| 03 | STD + NOFACE | The cloak — see Worked pack 1 |
| 04 | STD + NOFACE | A sealed letter |
| 08 | STD + NOFACE | The barred window |
| 05, 06, 07, 09, 10, 11, 12, 13 | STD + NOFACE | **Not yet specified in any source file.** Default suggestion: reuse that envelope's primary sticker-sheet motif (e.g. 05 → the pen; 12 → the lamp) rather than inventing a new one — flag for a real decision before art is finalised. |
| 14 | STD + NOFACE | **Deliberately undecided** — `envelope-14.md` flags this as the last postcard in the box and asks whether it should say something the other thirteen don't. Decide before generating. |

### Envelope exteriors — the month-cancellation ring
**Format:** circular motif, ~45mm diameter, gold ink line on transparent ground (charcoal for 01/02); generate the ring alone and typeset the month name in Fraunces separately rather than fighting the tool for clean circular lettering (see Worked pack 1's note).

| Env | Month text | Style |
|---|---|---|
| 01 | MUHARRAM | MOURN |
| 02 | SAFAR | MOURN |
| 03 | RABI AL-AWWAL | STD — see Worked pack 1 |
| 04 | RABI AL-THANI | STD |
| 05 | JUMADA AL-AWWAL | STD |
| 06 | JUMADA AL-THANI | STD |
| 07 | RAJAB | STD — same stamp as 08, seal color differs |
| 08 | RAJAB | STD — same stamp as 07, seal color differs |
| 09 | SHA'BAN | STD — same stamp as 10 |
| 10 | SHA'BAN | STD — same stamp as 09 |
| 11 | RAMADAN | STD |
| 12 | SHAWWAL | STD |
| 13 | DHUL QA'DAH | STD |
| 14 | DHUL HIJJAH | STD |

---

## Pack 4 — the remaining six original companions

Person prints and sticker sheets, subjects pulled from each file's own item spec. Format: person print A5 portrait, sticker sheet A6 die-cut, same as Pack 2. All use **FACES** for the person print, **NOFACE** for the sticker sheet, **STD** palette throughout (companions line is dateless, no mourning variant).

| Companion | Person print subject | Sticker sheet subject |
|---|---|---|
| Salman al-Farsi | An older man, working, date palms behind him. | Palms, a spade, a road, a fire, small repeatable marks |
| Bilal | A man standing high up, early light, mouth open, city below. | A rooftop, sun, sound marks, small repeatable shapes. **No chains anywhere on the sheet.** |
| Maytham al-Tammar | A man at a market stall, dates in baskets, scales, ordinary morning. | Dates, baskets, scales, market awnings, small repeatable marks |
| Qambar | A young man in a good shirt, standing in a market street. | Two shirts, coins, a market street, a door, small repeatable marks |
| Abu Dharr | An old man sitting on the ground in front of a large new building. | A door, coins, a road out of a city, a water skin, small repeatable marks |
| Malik al-Ashtar | A very large man in plain clothes walking through a market, unrecognised. | A market street, a folded letter, a doorway, a road, small repeatable marks |

The four newer companions (Uthman, Abbas, Fizza, Jabir) are fully worked in Pack 2 above.

**Return postcard fronts for all ten companions are undecided** — no source file specifies one, unlike the Fourteen. Same recommendation as envelopes 05–13: default to that companion's primary sticker motif rather than leaving it to be improvised at prepress.

---

## Pack 5 — all fourteen zine covers

**Format:** A7 (roughly 74 × 105 mm, one panel of the folded A4 sheet — see `09-zines/README.md`'s imposition), single ink, full bleed within the panel. Use the **ZINE** style block for every row.

| Zine | Cover subject (from the zine's own PAGE 1) |
|---|---|
| Ghadir Khumm | A fork in a desert road |
| Hira | The cave mouth from inside, looking out |
| Mubahala | Two groups facing each other across open ground — tents or footprints standing in for the people, no figures |
| Hudaybiyya | A well and a low tent |
| The Trench | A straight ditch cutting across open ground |
| Jannat al-Baqi | A low wall and open ground beyond it |
| Jamkaran | A mosque courtyard at night |
| The road to Karbala | A single road running to the horizon |
| Kufa | A grid of straight streets seen from above |
| Samarra | A spiral minaret against open sky |
| Laylat al-Mabit | A doorway at night, a single lamp |
| Dahw al-Ard | Flat open ground to the horizon |
| The Constitution of Medina | A rolled document |
| Bayt al-Hikma | Shelves of scrolls |

Fadak has no cover prompt — it isn't drafted, per the standing scholar-decision block in `09-zines/outlines.md`.

---

## Pack 6 — elements with no fixed spec anywhere yet

These aren't sourced from any existing file — they're proposals, not decisions already made elsewhere in the project. Treat them as a starting point to accept, change, or hand to a scholar/designer, not as settled the way everything above is.

### Wax-seal sticker motif
No motif is specified anywhere in the repo — only that it exists and comes in gold (standard) or charcoal (mourning), per `design-system.md` §5.

```
[STD, or MOURN for 01/02]
[NOFACE]

SUBJECT: a small circular seal motif, simple and geometric — proposal: a plain rosette or
a single-word monogram in the display face, nothing devotionally specific enough to need
scholar sign-off. Avoid anything that reads as a national or sectarian symbol.

FORMAT: circular, ~20mm diameter, isolated on transparent ground.

FLAG: this is a proposed starting point, not a decision — confirm the motif before it's
cut into a die for 14+ envelopes' worth of seals.
```

### Box
No illustrated motif specified — `design-system.md` only fixes stock family (A5/A6) and palette. If the box carries any illustration at all (vs. being plain stock with a printed label), that's an open design decision, not just an art-generation task — flag before prompting anything here.

### Named Edition ribbon colourways
Not an illustration job — these are physical ribbon colors, named but never given hex targets anywhere in the project (`TASKS.md` Phase 5 names them: rose, sage, plum, ochre; flat ribbon only, never bows). Proposed targets, chosen to sit comfortably beside the fixed palette (`design-system.md` §2) without clashing with the gold seal:

| Colourway | Proposed hex | Note |
|---|---|---|
| Rose | `#C97B84` | Warm enough to sit near the terracotta accent without competing with it |
| Sage | `#8A9A7E` | Cooler counterpart to the muted teal |
| Plum | `#6B4C6B` | The one genuinely new hue family in the product — confirm it doesn't read as mourning-adjacent before committing |
| Ochre | `#C79A3E` | Close kin to the standard gold accent — the safest of the four |

**Flag: these are proposed, not fixed.** Confirm against an actual ribbon sample under real light before ordering — screen color and dyed-ribbon color diverge more than any other material in this product.

---

## What's still not covered

- **Job 2, the text layouts** (letter, fact panel, hadith card, session card, return postcard reverse, inside flap) — not an image-gen task. Say the word and I'll build these directly as print-ready HTML/CSS, exportable straight to PDF via headless Edge (confirmed working on this machine).
- **Hadith card front art**, if any is wanted beyond typeset text — no spec exists because hadith card content itself is still blocked on citation work.
- **Physical proofs** — the ring punch, the pennant dimension, the wax-seal die, the ribbon color — every one of these needs a real object in hand before it's final, per `design-system.md`'s own "What this doesn't settle."

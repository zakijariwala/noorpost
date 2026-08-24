# Canva build brief

What to build, at what size, in what order. Derived from `00-foundations/design-system.md`, `fact-panel-spec.md`, `09-zines/README.md` and `08-companions/README.md` — this file adds nothing new to the design system except the two decisions taken on 2026-08-24 and recorded in §0.

**Built for Canva Free.** Two things that plan cannot do are worked around in §2 and §3, and one of them changes a fixed Phase 0 decision.

---

## 0. Two decisions taken 2026-08-24

### The letter moves to A4 folded to A5

This closes the Gate 3 blocker in `04-art/print/README.md` — every letter template overflowed its A5 page by 28–76%.

| | |
|---|---|
| **Sheet** | A4 landscape, 297 × 210 mm, folded once down the vertical centre |
| **Result** | A bifolium: four A5-portrait faces, 148 × 210 mm each |
| **What it protects** | The body type size (unchanged), the 330–370 word spec (unchanged, all 53 letters stand as measured), and the fact panel staying on the same sheet as the letter |
| **What it costs** | One fold in assembly, and a paper spec change from A5 to A4 |

**Face assignment:**

```
  PRINT SIDE A (outside)          PRINT SIDE B (inside)
  ┌──────────┬──────────┐         ┌──────────┬──────────┐
  │  face 4  │  face 1  │         │  face 2  │  face 3  │
  │   FACT   │  LETTER  │         │  LETTER  │  THE     │
  │  PANEL   │  part 1  │         │  part 2  │  CLOSE   │
  └──────────┴──────────┘         └──────────┴──────────┘
        ↑ fold ↑                        ↑ fold ↑
```

A 330–370 word letter needed about 1.8 A5 faces at the fixed type size, so **two faces carry the whole letter with room to spare.** Face 3 is not filler — it takes the ●○ read-together close, set large, with white space around it. The last line of every letter is the one the parent and child say together; giving it its own face is the design doing what the spec already says.

Face 4 is the fact panel exactly as `fact-panel-spec.md` draws it. Nothing about the panel changes.

### The display face is substituted, and that is a spec change

`design-system.md` §1 fixes **Fraunces** for child lines, titles and envelope lettering. **Canva Free cannot upload fonts**, so Fraunces cannot be used unless Canva serves it.

**Check Canva's font list for Fraunces first.** If it is there, nothing changes. If it is not, substitute — and **record the substitution in `design-system.md` §1**, because it is a Phase 0 decision being altered, not a workaround.

What the substitute has to do, in priority order:

1. **Be a serif.** Fraunces was chosen because it is warm *and still dignified*. A rounded sans or a script fails the brief regardless of how friendly it looks.
2. **Separate from EB Garamond at a glance**, so a parent's eye tells the child's voice from the narration before reading the ● / ○ marks.
3. **Carry a real Bold or Black**, because titles and the fact-panel name depend on weight, not size.
4. **Read at 8 years old.** Set a child line in it, print at actual size, hand it to a child in the band.

Shortlist to audition in Canva, warmest first — none is a drop-in, all are serifs with more character than Garamond: **Bitter**, **Zilla Slab**, **Bree Serif**, **Lora**, **Merriweather**, **Playfair Display** (sharpest, least warm — the fallback, not the first choice).

**The test that decides it:** set the same child line twice, once in the candidate and once in EB Garamond, print both at actual size on ivory stock, and look at them from across a table. If you cannot tell which is the child's voice without reading the ○ mark, the candidate has failed the only job it has.

---

## 1. What to build — 24 master templates

A **master** is a locked layout with placeholder content. Everything else is a duplicate of a master with the copy swapped. Build masters first; never lay out a second envelope from scratch.

### Group A — The Fourteen (the box), 15 masters

| # | Master | Canvas (trim) | Faces | Mourning page? |
|---|---|---|---|---|
| A1 | **Letter + fact panel bifolium** | A5 portrait 148 × 210 | 4 | ✅ |
| A2 | **Hadith card** | A6 portrait 105 × 148 | 2 | ✅ |
| A3 | **Person print** | A5 portrait 148 × 210 | 1 | ✅ |
| A4 | **Event print** | A5 **landscape** 210 × 148 | 1 | ✅ |
| A5 | Session card — **Conversation** (×7 envelopes) | A6 portrait 105 × 148 | 2 | — |
| A6 | Session card — **Case File** (×4 envelopes) | A6 portrait 105 × 148 | 2 + 5 evidence + 1 sealed answer | — |
| A7 | Session card — **Mourning** (×2 envelopes) | A6 portrait 105 × 148 | 2 | *is* the mourning one |
| A8 | Session card — **Open** (×1 envelope) | A6 portrait 105 × 148 | 2 | — |
| A9 | **Sticker sheet** (die-cut, 12 envelopes) | A6 portrait 105 × 148 | 1 | not issued |
| A10 | **Pennant** (2 mourning envelopes only) | see §4 — proof it, don't rule it | 1 | mourning only |
| A11 | **Return postcard** | A6 **landscape** 148 × 105 | 2 | ✅ |
| A12 | **Envelope exterior** | see §4 | 1 | ✅ |
| A13 | **Inside flap block** | see §4 | 1 | ✅ |
| A14 | **Wax seal sticker** | 32 mm circle | 1 | ✅ (charcoal) |
| A15 | **Box** | set at Phase 5 from the finished stack | — | — |

### Group B — Everyone Else (companions), 7 masters

Five items per envelope, **never an event print**, and the hadith card runs on its own chain.

| # | Master | Canvas (trim) | Faces | Differs from the box how |
|---|---|---|---|---|
| B1 | **Letter + fact panel bifolium** | A5 portrait 148 × 210 | 4 | Faces allowed in the illustration |
| B2 | **Hadith card** | A6 portrait 105 × 148 | 2 | Chain mark reads `FIRST EDITION nn / 39`, **never** a silsila segment |
| B3 | **Person print** | A5 portrait 148 × 210 | 1 | Faces allowed |
| B4 | **Sticker sheet** | A6 portrait 105 × 148 | 1 | — |
| B5 | **Return postcard** | A6 landscape 148 × 105 | 2 | — |
| B6 | **Envelope exterior** | see §4 | 1 | **No month stamp.** This line is dateless — the circular postal cancellation is the box's mark and must not appear here |
| B7 | **Inside flap block** | see §4 | 1 | Running order lists five items, not seven |

### Group C — Noori's Notebook (zines), 2 masters

| # | Master | Canvas | Notes |
|---|---|---|---|
| C1 | **Zine page grid** — 8 × A7 pages | A7 74 × 105 | Design each page here, at reading size |
| C2 | **A4 imposition sheet** | A4 297 × 210 landscape, **one side only** | Paste the eight A7 pages into the fold layout — §5 |

### The scale this adds up to

| Line | Envelopes | Faces each | Faces total |
|---|---|---|---|
| The Fourteen | 14 | ~16 | ~224 |
| Everyone Else | 39 | 12 | 468 |
| Zines | 15 | 8 + 1 imposition | ~135 |
| | | **total** | **~830 artboards** |

That number is the argument for masters. Laying out 830 faces by hand is not a project; duplicating 24 masters 830 times is.

---

## 2. Canvas sizes — build every canvas oversized

**Canva Free cannot export bleed or crop marks.** The fix is to make the bleed part of the canvas: set every custom size to **trim + 6 mm** (3 mm on each edge), then mark the trim line with Canva guides.

| Item | Trim (mm) | **Canvas to set in Canva (mm)** |
|---|---|---|
| Letter face / person print — A5 portrait | 148 × 210 | **154 × 216** |
| Event print — A5 landscape | 210 × 148 | **216 × 154** |
| Hadith card / session card / sticker sheet — A6 portrait | 105 × 148 | **111 × 154** |
| Return postcard — A6 landscape | 148 × 105 | **154 × 111** |
| Zine page — A7 portrait | 74 × 105 | **80 × 111** |
| Zine imposition sheet — A4 landscape | 297 × 210 | **303 × 216** |
| Letter bifolium, imposed — A4 landscape | 297 × 210 | **303 × 216** |
| Wax seal sticker | 32 mm ⌀ | **38 × 38** |

**Setting guides** (File → Settings → *Show rulers and guides*, then drag from the ruler). Canva guides do **not** export, which is exactly what is wanted:

- **Trim guides** at 3 mm from every canvas edge. This is where the knife lands.
- **Safe guides** at **15 mm** from the canvas edge on A5/A4 items (3 bleed + 12 margin), **11 mm** on A6/A7 items (3 bleed + 8 margin). No text crosses this line.
- Background colour and any full-bleed art **must run to the canvas edge**, past the trim guide. Art that stops at the trim line produces a white sliver when the cut drifts, and the cut always drifts.

Save one blank canvas per size with the guides already dragged, then duplicate it for every new master. Dragging guides 24 times is where the errors get in.

---

## 3. Colour, with no Brand Kit

Canva Free will not lock a palette, so **build a swatch strip as page 1 of every master** — six 20 mm squares with the hex printed under each, and pick colour from it with the eyedropper rather than typing hex. Delete the swatch page before export.

**Standard palette** — the typeset system only. Artwork is not bound by it (`design-system.md` §2).

| Role | Hex |
|---|---|
| Stock / ground — warm ivory | `#F3EDE1` |
| Ink / primary text — near-black | `#211B14` |
| Primary accent — seals, headline rules, month stamp ring — deep gold | `#A9762F` |
| Secondary accent — session cards, sparingly — muted teal | `#2C5F5A` |
| Tertiary accent — woman slot marker, stickers — terracotta | `#B4472A` |

**Mourning palette** — envelopes **01 and 02 only.** Black on ivory, full stop. No gold, no teal, no terracotta.

| Role | Hex |
|---|---|
| Stock / ground — warm ivory (unchanged) | `#F3EDE1` |
| Ink (unchanged) | `#211B14` |
| Accent — replaces all three — charcoal-black | `#1B1B1B` |

**Do not set the ivory as a "paper" effect or a texture.** It is the stock. If you are printing on ivory paper, leave the canvas background as the ivory hex for on-screen accuracy and tell the printer the ground is the stock, not an ink. If you are printing on white, the ivory prints as a flood — which costs ink on every sheet and is a Phase 5 cost decision, not a design one.

**Canva Free exports RGB.** Nothing here is a CMYK build. That conversion is a real prepress step and happens outside Canva — the `#A9762F` gold especially, which is doing double duty as the seal and the stamp ring and may want to be a spot colour rather than a four-colour mix.

---

## 4. The pieces with geometry that is not a paper size

### Event print — the ring punch

Every one of the fourteen must clip onto the same 25 mm book ring in any order.

- **Hole: 6 mm diameter, single, horizontally centred, hole centre 12 mm from the top trim edge.**
- On the 216 × 154 mm canvas that is **x = 108 mm, y = 15 mm** from the top-left canvas corner.
- Draw it in the master as a **magenta circle outline on a layer named `PUNCH — DELETE BEFORE EXPORT`**, and keep **no critical linework within 25 mm of the top trim edge**. The ring hardware sits on the paper, not just through it.
- ⚠ **Punch a blank sheet at this spec and hang it on the actual ring before drawing fourteen illustrations against it.** `design-system.md` §6 says the same thing and it is still not done.

### Envelope exterior

No size is fixed in the design system, because it follows from the contents. Now that the letter is A4 folded to A5, the envelope must take an **A5 stack** — so a **C5, 229 × 162 mm** envelope, or a wallet of the same trim if you want a bespoke die.

Three elements, all on the front:

| Element | Where | Ink |
|---|---|---|
| Circular postal-cancellation month stamp | Centre-right, sized to read across a room | Gold `#A9762F` / charcoal on mourning |
| Name area | Lower third, display face | Ink. Named Edition prints the child's name here; everyone-else stock leaves it blank |
| Wax-seal sticker | Over the flap closure | Gold / charcoal. Named Edition ribbon is **flat, never a bow**, and the seal sits **over** the ribbon |

**The companions envelope carries no month stamp.** That line is dateless and the stamp is the box's mark.

### Inside flap block

One printed block, on the inside of the flap, read the moment the envelope opens. Two blocks only — nothing else earns the space:

1. **The running order** — what is inside, in opening order.
2. **The runtime** — the ~25 minute target, stated plainly.

Size it to the flap of whatever envelope you settle on. Treat it as a **148 × 100 mm** working area until the envelope is chosen.

### Pennant — the one thing not to set with a ruler

Triangular, cord-mounted, charcoal on ivory, **envelopes 01 and 02 only**, replacing the sticker sheet. `design-system.md` §4 deliberately leaves the dimension open: **print the letter and fact panel first, lay them out, and cut pennants until one reads right beside them.** Then record the number.

### Hadith card — the chain mark

Same A6 trim on both lines, and the design has to make the two chains unmistakable at a glance.

| | The box | Everyone Else |
|---|---|---|
| Chain mark | `Silsila segment n of 14` | `First Edition nn / 39` |
| Position | Small caps, top corner, front — findable in a stack, never competing with the saying | Same corner, same size |

**Write both out in words.** "Segment 7" and "07/39" set in the same corner at the same size are two marks a child sorts into one pile. *Silsila* and *First Edition* are the only things keeping them apart.

**The envelope number never appears on a hadith card** — not front, not back, not in the citation block, not as a footer. This is the rule most likely to leak from a template built by copying the fact panel, which does carry envelope numbering. Check it at every sign-off.

---

## 5. The zine imposition

One A4 sheet, printed **one side only**, folded to eight A7 pages, one cut. Pages do not sit in reading order:

```
  A4 LANDSCAPE, ONE SIDE

  ┌───────┬───────┬───────┬───────┐
  │   5   │   4   │   3   │   2   │   ← upside down
  ├───────┼───────┼───────┼───────┤
  │   6   │   7   │   8   │   1   │   ← right way up
  └───────┴───────┴───────┴───────┘
              ↑ centre slit ↑
```

**Print one test sheet, fold it, and read it before laying out a single zine.** Every zine programme in history has burned a run on this.

| Page | Job | Words |
|---|---|---|
| 1 | Cover — the name of the event or place, one image | ≤ 6 |
| 2 | Where and when | 40–60 |
| 3 | What happened, part one | 50–70 |
| 4 | What happened, part two | 50–70 |
| 5 | The thing most people do not know | 50–70 |
| 6 | What is there now | 40–60 |
| 7 | One thing to do, or one thing to look at | 30–50 |
| 8 | Back cover — sources, and where the rest is | ≤ 30 |

**No faces in the zines.** These are places and events. Page 8 always carries the source line — a zine is where a citation gets dropped for space, and it must not be.

---

## 6. Placeholder discipline — the rule that outranks looking finished

Three things are genuinely undecided, and a template that fills them in with plausible-looking text is worse than one that shows a hole.

| Slot | What the template prints | Why |
|---|---|---|
| **Hadith card, both lines** | An **empty slot**, with a line saying no saying has been selected | 0 of 14 box sayings and 0 of 39 companion sayings are chosen. `sourcing-rules.md`: quote exactly or don't quote. **Never set invented text inside quote marks**, and never attribute it to a named figure — a screenshot of one card loses whatever label surrounded it. |
| **Chain numbers** | Literal `nn` | The silsila numbering (the Prophet at 13 or at 1) and the companion chain order are both open. Build the chain mark as an **editable text layer**, never baked into art. |
| **Every fact panel claim** | The `UNVERIFIED — TO VERIFY` watermark stays on | Every claim in every panel is `TV` on the citation sheet. **Nothing prints on `TV`.** The Thaqalayn approval of 2026-08-24 makes clearing these rows much faster, but none of them is cleared yet. |

Put each of these on its own layer with `— PLACEHOLDER` in the layer name. A watermark you have to actively delete is a watermark that does not leak.

---

## 7. Order of build

Do not build 24 masters and then discover the fold is wrong.

1. **Build A1 alone, for envelope 03**, with the real letter text (*The Cloak*, 367 words) and the real fact panel.
2. **Print it, fold it, hold it.** Check the letter lands on faces 1–2 with room, the close sits alone on face 3, the panel fills face 4, and the fold does not run through anything.
3. **Read it aloud to a child in the 8–12 band and time it.** Four to four and a half minutes for the letter.
4. Only then build A2, A5, A11, A12, A13 — the rest of envelope 03's set — and print a complete pilot envelope.
5. **Punch a blank A5 landscape and hang it on the ring** before A4 (the event print) is designed.
6. Then the remaining box masters, then Group B, then Group C.

Envelope 03 is the pilot for a reason. Everything learned in steps 2–3 is cheap now and ruinous at Phase 5.

---

## 8. Inspiration — and what to steer away from

The product is a thing that gets kept, re-read and handled. Not a thing that gets scrolled.

**Look at:**

| Source | What to take from it |
|---|---|
| **Real postal ephemera** — first-day covers, aerogrammes, philatelic cancellation rings | The month stamp. Study actual cancellation marks: the ring, the wobble, the date sitting inside it. This is the single most identity-carrying mark in the product. |
| **Ladybird Books, 1960s–70s** | The discipline of one full-page picture facing one page of text, and never crowding either. Also the flat, confident colour that survives cheap printing. |
| **Penguin and Pelican covers, Tschichold era** | Grid, restraint, and the idea that a series identity comes from a repeated frame, not from repeated decoration. |
| **Museum object labels** | The exact register of the fact panel: name, dates, facts, no adjectives. A label that says *an enormous influence* is a bad label. |
| **Observer's Books, I-Spy books** | Pocket collectibles a child completes. This is what the three collections are for. |
| **Field guides and almanacs** | The fact panel is an almanac page, not an infographic. Rules and space do the work; there are no icons. |

**Steer away from:**

- **Infographic styling** — icon sets, stat callouts, coloured pills. The fact panel is a museum label, not a dashboard.
- **Gradients, drop shadows, glows.** Nothing here is screen-native. All of it is ink on ivory.
- **"Children's educational" clip art.** The child's voice is carried by the *typeface* and the ○ mark, not by cartoon friendliness. The product is trying to be kept, not skimmed.
- **Canva's stock templates.** Every one is built for screen or for a poster. Start from a blank custom canvas with your guides, every time.
- **More than one accent colour on a page.** Gold *or* teal *or* terracotta. Never two.

---

## 9. Naming, so version control survives Canva

Canva has no branches. The naming convention is the version control.

```
NP · <line> · <item> · <variant> · v<n>
```

- `NP · BOX · A1 letter-bifolium · STANDARD · v3`
- `NP · BOX · A4 event-print · MOURNING · v1`
- `NP · COMP · B2 hadith-card · v2`
- `NP · ZINE · C2 imposition · v1`

**Never edit a master in place once a duplicate exists.** Duplicate the master, bump the version, and leave the old one. When a master changes after ten envelopes are built from it, you need to know which ten.

---

## 10. What Canva does not finish

Canva Free takes this to approved layout, not to plate.

| Left over | Where it happens |
|---|---|
| **CMYK / spot conversion** | Prepress, Phase 5. Hand the printer the hex values and let them build it — the gold especially may want to be spot. |
| **Crop marks and registration** | The printer adds these from the oversized canvas. Tell them the bleed is 3 mm and built into the file. |
| **Die lines** — sticker sheet, pennant, box, any bespoke envelope | Supplied by the printer as a template you design into. Ask for them before designing those four. |
| **Real bold weights** | If the substituted display face has no true Bold in Canva, titles are being faked with size and spacing. That reads as thin at small sizes on ivory. Check the fact-panel name at actual size. |
| **The physical proofs still owed** | The ring punch, and the pennant dimension. Both are decided against paper, not a screen. |

# Design system

Phase 0.4. Rules for the seven items, the envelope, and the two collectible sets, fixed before a single piece of art is drawn. Art itself is Phase 4 — this file fixes the frame it goes in, not the drawings.

---

## 1. Typefaces

Two faces, both SIL Open Font License (free, no royalty, no attribution required, safe for a commercial print run), both on Google Fonts so every contributor can pull the identical file.

| Role | Face | Why |
|---|---|---|
| Body — letters, fact panels, hadith cards, all adult-facing copy | **EB Garamond** | A proven book-print revival with real italics and small caps. Reads as literary and settled, not corporate — matches a product that is trying to be kept, not skimmed. |
| Display — child lines (○), titles, the name on the fact panel, envelope exterior lettering | **Fraunces** | A variable "soft-serif" with deliberately warm, slightly irregular letterforms (its own designers call it Old Style with a WONK axis). Distinct enough from Garamond that a parent's eye separates the child's voice from the narration without needing the ● / ○ marks alone to do it — but it is still a serif, still dignified, not a cartoon face. |

**Settings:**
- Child lines (○): Fraunces, WONK axis on (the "soft" cut), regular weight. Warmth belongs to the child's voice.
- Titles and the name on the fact panel: Fraunces, WONK axis off, Black or Bold weight. Authority belongs to the title.
- Everything else: EB Garamond, regular for body, italic for the standard difference-of-opinion line (per `standard-lines.md`), small caps for dates on the fact panel (per `fact-panel-spec.md` §Typography).

**Not yet settled:** whether the Arabic on any item (silsila card reverse, if Arabic is ever quoted) needs a matching Arabic face. If it does, Noto Naskh Arabic is the safe default — same foundry family as Noto Serif, free, broad Unicode coverage. Flag if a design pass needs it; nothing in the fourteen letters currently quotes Arabic script.

---

## 2. Palette

**Amended 2026-08-12. The palette binds the printed system, not the artwork.**

| | Governed by |
|---|---|
| **The typeset system** — stock, body and display ink, seal, month-stamp ring, rules, the fact-panel skeleton, the flap block | **The fixed palette below. Unchanged.** This is what makes fourteen envelopes read as one product by envelope three, and the ivory-stock reasoning is about handling, not taste. |
| **Artwork** — person prints, event prints, sticker sheets, postcard fronts, and independently designed cards | **No fixed palette.** Illustrators choose their own colour. The one rule is that **colours must be complementary** — they must sit together, and sit against ivory stock and gold seal, without fighting. |

This resolves the Green Dome question outright: the dome is green because the dome is green, and no exception needs recording. It also settles the same question for every shrine, tilework and banner still to be drawn, which would otherwise have arrived one at a time.

**What "complementary" is doing here.** It is a real constraint, not a licence. A drawing still has to hang on a wall beside thirteen others and read as one set. What was a hex list is now a judgement call, so it moves from being checked mechanically to being checked at sign-off — see §3.

### Fixed palette — the typeset system

| Role | Name | Hex |
|---|---|---|
| Stock / ground | Warm ivory | `#F3EDE1` |
| Ink / primary text | Near-black ink | `#211B14` |
| Primary accent — seals, headline rules, envelope stamp ring | Deep gold | `#A9762F` |
| Secondary accent — used sparingly, session cards | Muted teal | `#2C5F5A` |
| Tertiary accent — the woman slot marker, sticker sheets | Terracotta | `#B4472A` |

Warm ivory over stark white because the product is handled and re-read, not displayed under gallery light — white stock shows handling faster and reads coldly next to gold foil or a wax seal. Gold as the primary accent because it is doing double duty: it is also the seal and the postal-cancellation-stamp ring color, so it needs to be one fixed ink the whole product recognises on sight by envelope three, same logic as the fact-panel skeleton.

~~**Open: the Green Dome.**~~ **Resolved 2026-08-12** by the amendment above — artwork is not bound by the fixed palette, so the green dome needs no exception and no sixth colour is added to the table.

### Mourning palette — envelopes 01 and 02 only

| Role | Name | Hex |
|---|---|---|
| Stock / ground | Warm ivory (unchanged) | `#F3EDE1` |
| Ink / primary text | Near-black ink (unchanged) | `#211B14` |
| Accent — replaces gold, teal and terracotta entirely | Charcoal-black | `#1B1B1B` |
| One permitted departure — the pennant cord only, never printed on paper | Unbleached cotton / natural | — |

No color accent in the mourning issues. Black on ivory, full stop — this is a restatement of common mourning convention (black is customary for Muharram and the early days of Safar), not a design flourish, and it is why the pennant replaces the sticker sheet rather than getting its own color: a sticker sheet is a reward object, and rewards are not the register of these two issues.

> **This one survives the 2026-08-12 amendment, and deliberately.** It is not a palette rule that happens to restrict colour — it is a *content* rule about the register of Muharram and Safar, which is why it is stated in terms of mourning convention rather than of hexes. Freeing artwork from the fixed palette does not free envelopes 01 and 02 from being mourning issues. **If the intent was to free these two as well, say so explicitly — it is a decision about observance, not about design, and it should not be made by implication.**

**CMYK / spot conversion is a prepress task**, not fixed here — hand these hex values to the printer once Phase 2 sets the print run and they will build the right build (spot gold foil vs. four-color gold, for instance, is a cost decision that belongs in Phase 5, not Phase 0).

---

## 3. Illustration style rules

| Rule | Applies to |
|---|---|
| **Never a depiction of any of the Fourteen.** No face, no figure, no likeness of a Masoom — shown instead by setting, object or absence (a shield, a cloak, a doorway, an empty road). **This half of the rule is absolute and is not what was relaxed.** | The Fourteen — all fourteen envelopes, every item |
| **Incidental people in a place are allowed** (2026-08-12, scholar-approved). Pilgrims and visitors present at a shrine may be drawn, including faces — they are people who happen to be there, not a depiction of anyone the box is about. A photograph of a shrine contains them and raises no question; a drawing is the same. | The Fourteen — person prints and event prints |
| **Faces allowed**, drawn plainly, no attempt at portraiture or likeness of a historical record that doesn't exist | The companions line — `08-companions/` only |
| One illustration style throughout — same hand, same line weight, same restraint — so a family can tell a Fourteen item from a companion item at a glance even before reading the faces rule | Both lines |
| No violence depicted. Where a letter's content is violent (Karbala, the shield case, the night search), illustrate the object, the aftermath, or the setting — never the act | The Fourteen |
| Landscape and person prints share one linework style; the calendar ring and the wall of prints must read as one set, not fourteen separate commissions | Person prints, event prints |
| Mourning issues (01, 02) drop color per §2 but keep the same line style — no separate "somber" illustration mode | 01, 02 |

**Amended 2026-08-12, on scholar approval.** The rule was previously a blanket ban on any human figure, which conflated two very different things. The concern it exists to protect is the depiction of the Masoomeen — that is untouched and absolute. Drawing the ordinary people who happen to be standing in a courtyard is a separate matter, and it is permitted.

The remaining rule is still the one a new illustrator will break first, because it is invisible in a single commission and only shows once two envelopes sit side by side. **Check it at every sign-off, not just the first** — and check the right half: not "is there a face", but "is this a depiction of one of the Fourteen".

---

## 4. Item templates

Paper sizes run on the A-series so the seven items share stock and a printer can nest them on one press sheet without custom trim. Dimensions below are the working spec for Phase 4 art and Phase 5 prepress — confirm against the actual printer's press-sheet layout before locking bleed.

| Item | Size | Orientation | Notes |
|---|---|---|---|
| Letter | A5 (148 × 210 mm) | Portrait | Front: letter. Back: fact panel. One sheet, per `fact-panel-spec.md`. |
| Hadith card | A6 (105 × 148 mm) | Portrait | Front: saying, silsila segment number (never the envelope number — rulebook, `spec-check.md`). Back: citation, per `sourcing-rules.md` citation format. |
| Person print | A5 (148 × 210 mm) | Portrait | Fixed by TASKS.md Phase 0.4. No faces on the Fourteen; faces allowed on companions. |
| Event print | A5 (148 × 210 mm) | Landscape | Fixed by TASKS.md Phase 0.4. Punched — see §6, ring position. Same stock and linework as the person print so all 28 (14+14) read as one wall. |
| Session card | A6 (105 × 148 mm) | Portrait | Same trim as the hadith card so both fit one card box. Conversation / Case File / Mourning / Open layouts per `spec-check.md` §Session types. |
| Sticker sheet | A6 (105 × 148 mm) die-cut | Portrait | Not issued for 01, 02 — pennant instead. |
| Return postcard | A6 (105 × 148 mm) | Landscape | Matches the international minimum postcard dimension, so it can post at postcard rate without a surcharge in most postal systems — confirm against the domestic carrier once Phase 6 sets the return-postcard process. Two signature lines, pre-addressed, per `HANDOVER.md`. |

**Pennant** (replaces sticker sheet, 01 and 02 only): triangular, cord-mounted, charcoal ink on ivory stock per the mourning palette. No fixed dimension yet — take it from whatever length reads well against the letter and fact panel once both are proofed; this is the one template better decided against a physical proof than a ruler.

---

## 5. Envelope exterior and inside flap

**Exterior:**
- Circular postal-cancellation month stamp, gold ink (standard palette) or charcoal (mourning), center-right, sized to read at a glance which month this is before the seal is broken.
- Name area, lower third, set in Fraunces (WONK off) — this is where the Named Edition prints the child's name; everyone-else stock leaves it blank or pre-set to a placeholder per the SKU.
- Wax-seal sticker, closing the flap. Gold for standard, charcoal for mourning, per §2. Ribbon (Named Edition only) is flat, never a bow, per `TASKS.md` Phase 5 — the seal sits over the ribbon, not beside it.

**Inside flap:** one printed block, visible the moment the envelope opens, before any item is drawn out.
- The running order — what's inside, in the order it's meant to be opened (letter, fact panel, hadith card, session card, collectibles).
- The runtime — the ~25 minute target, stated plainly, so a parent starting late on a school night knows what they're committing to before they open the letter.

Both are functional, not decorative — the inside flap is the one surface in the product a parent reads under time pressure. Keep it to those two blocks; nothing else earns space there.

---

## 6. Calendar ring position

**Fixed:** single centered hole, 6 mm diameter, punched 12 mm from the top edge, symmetric left-right — the same edge distance and hole diameter as the ISO 838 two-hole standard used across A4 ring binders, sized down to one hole because these fourteen prints hang on one ring, not a binder mechanism. All fourteen event prints punched identically so they hang in any order on the ring and rotate freely month to month.

**Ring hardware:** a standard 25 mm (1") nickel-plated book/binder ring — the same product sold for flashcards and index-card sets, cheap, widely stocked, and replaceable by a family without sourcing anything unusual. Ship one per box; it is cheap enough to be a hardware line item, not a custom part.

This closes the Phase 0.4 blocker in `spec-check.md` ("Ring punch position — All fourteen event prints"). **Proof it physically before Phase 4 art is finalised** — punch a blank A5 landscape sheet at this spec and confirm the ring doesn't crowd the linework near the top edge before committing fourteen illustrations to it.

---

## 7. Hadith card numbering placement

- The **silsila segment number** (1–14, historical order, per `spec-check.md`) prints small, top corner, front of the card, next to or beneath the saying — enough to be findable when the fourteen are laid out in a stack, not large enough to compete with the saying itself.
- The **envelope number never appears on a hadith card**, front or back, in any form — not in the citation block, not as a running footer. This is the rule most likely to leak from a template built by copying the fact-panel skeleton, which does carry the envelope's own numbering elsewhere. Check it explicitly at sign-off, per `checklist.md`.
- The citation block (back of the card) carries the work, number, and translator per `sourcing-rules.md` §Citation format — no envelope reference there either.

### Two chains, and the card has to say which one it is on (added 2026-08-14)

The companions line carries a hadith card as of 2026-08-14 (rulebook C6). Same A6 trim, same faces, same citation block — **a different chain, and the design has to make that unmistakable at a glance**, because keeping the two collections visibly separate is the whole mitigation for letting the second one exist.

| | The box | Everyone Else |
|---|---|---|
| Chain mark | `Silsila segment n of 14` | `First Edition nn / 39` |
| Length | Fourteen, subscription only | Thirty-nine, bought a piece at a time |
| Set in | Small caps, top corner, front | Same position, same size — **the words are what differ, so they must not abbreviate to each other** |

- **A companions card never carries a silsila segment number**, in any form or abbreviation. `tools/build_print_templates.py` fails the build if one appears.
- **Write the chain mark out in words on both lines.** "Segment 7" and "07/39" set in the same corner at the same size are two marks a child sorts into one pile. *Silsila* and *First Edition* are what keep them apart.
- The ordering that decides `01/39` through `39/39` is **still undecided** — templates print a literal `nn` until it is. See `TASKS.md` Phase 8.

---

## What this doesn't settle

- Final CMYK/spot builds — prepress, Phase 5.
- Pennant dimensions — decide against a physical proof, not a ruler.
- Whether an Arabic-script face is needed anywhere — currently no envelope quotes Arabic script; revisit if that changes.
- Actual press-sheet nesting — depends on the printer chosen in Phase 2/5; the A5/A6 sizing above is chosen to make that nesting easy, not to pre-empt it.

**Gate 0 note:** with this file, licensing, palette, illustration rules, and the seven templates all exist as fixed specs. The remaining Gate 0 items are the scholar relationship (`sources-needed.md` Tier 5) and sources still in hand per `sourcing-rules.md` — neither is a design question.

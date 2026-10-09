# Design system

Phase 0.4. Rules for the seven items, the envelope, and the two collectible sets, fixed before a single piece of art is drawn. Art itself is Phase 4 — this file fixes the frame it goes in, not the drawings.

---

## 1. Typefaces

> **Amended again 2026-10-08 — fourteen envelopes, fourteen styles.** Decided by the owner after the Paper Dunes pass: every envelope in the box gets its own style, because the run prints once and is not redesigned for at least a year. **Paper Dunes becomes envelope 03's style, not the house style.** Each envelope's faces, palette and illustration mode are now set per envelope in `tools/envelope_themes.py`; the full sets are built by `tools/build_envelopes.py` into `04-art/envelopes/`.
>
> | Env | Style | Faces | Art |
> |---|---|---|---|
> | 01 Muharram | M2 Ink Wash | Cormorant Garamond / Nunito Sans | black wash and red on ivory (2026-10-09) |
> | 02 Safar | M1 Charcoal Line | Young Serif / Nunito Sans | black line and green on ivory (2026-10-09) |
> | 03 Rabi al-Awwal | C Paper Dunes | Young Serif / Nunito Sans | cut paper |
> | 04 Rabi al-Thani | B3 Big Shapes | Bricolage Grotesque / Newsreader | flat, two inks |
> | 05 Jumada al-Awwal | D Illuminated | Cormorant Garamond / Alegreya | gilded, manuscript |
> | 06 Jumada al-Thani | F Suzani | Gloock / Karla | stitched |
> | 07 Rajab | A3 Mosaic Stars | Fraunces / Literata | flat, night tile |
> | 08 Rajab | A Lantern Night | Fraunces / Literata | flat, night |
> | 09 Sha'ban | C2 Dune Night | Young Serif / Nunito Sans | cut paper, night |
> | 10 Sha'ban | A2 Lantern Dawn | Fraunces / Literata | flat, dawn |
> | 11 Ramadan | B Tile Explorer | Bricolage Grotesque / Newsreader | flat, tile |
> | 12 Shawwal | E Riso Press | Space Grotesk / Atkinson Hyperlegible | riso overprint |
> | 13 Dhul Qa'dah | G Watercolour | Marcellus / Lora | wash, colour |
> | 14 Dhul Hijjah | C4 Garden Pop-up | Young Serif / Nunito Sans | cut paper, garden |
>
> **What still holds across all fourteen, because it is function and not look:** trim sizes and the A4-folded letter; the ● ○ ●○ voice marks; the fact-panel order; the chain mark, written out as *Silsila segment n of 14*; no envelope number on any hadith card; the ring punch; the name area on the front; the mourning register of 01 and 02 (black on ivory, no reward objects). `tests/test_envelopes.py` checks these on every build.
>
> **What this overrides, knowingly:** §3's "one illustration style throughout" no longer binds the box — each envelope has its own; the prompt-pack pairings 04/11 and 08/14 ("identical linework") no longer hold, since each pair now spans two styles. §3's absolute rule — never a depiction of any of the Fourteen — is untouched; the art kit has no figure in it. The companions line is not covered by this amendment and still prints from `04-art/print/assets/print.css` (Paper Dunes).


> **Amended 2026-10-09 — mourning in two inks.** Envelopes 01 and 02 are no longer charcoal and ivory only: each is a two-ink print on ivory — **black and red for 01 (Muharram), black and green for 02 (Safar)**. Black carries the line and the shade; the second ink marks what matters (01: the banner, the dusk over the camp, the glow behind the shrine; 02: the dome over Medina, the palms, the graves' shade, the treaty's seals). Nothing else enters either issue; `tests/test_envelopes.py` checks every colour. The paragraph below records the earlier rule.
>
> **Amended 2026-10-08 — Paper Dunes.** The two faces below are **retired** for the typeset system. Feedback on the envelope 03 proofs was that the product read as too plain for children; of four directions tried (`04-art/paper-dunes/`), the owner chose **Paper Dunes**. The faces are now:
>
> | Role | Face | Why |
> |---|---|---|
> | Body — letters, fact panels, cards, all adult-facing copy | **Nunito Sans** | A round, open humanist sans with a large x-height. Easy for an 8-year-old to follow over a parent's shoulder, and calm enough for the adult reading it aloud. Variable weight 400–800, real italics. |
> | Display — titles, the child's lines (○), the line said together (●○), the fact-panel name, envelope lettering | **Young Serif** | A warm, slightly soft serif. Still a serif and still dignified, so the §1 brief below (warm, not a cartoon face) is kept; it separates from the sans body at a glance, which is the job the display face has always had. Single weight. |
>
> Both SIL OFL, both on Google Fonts, both embedded for offline print in `04-art/print/assets/fonts-paper-dunes.css`. Letter body moves from 11.5 pt Garamond to **10.5 pt Nunito Sans** — the same reading size, because Nunito's x-height is larger. Noto Naskh Arabic stays the Arabic face. What follows is kept as the record of the original decision.

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

> **Amended 2026-10-08 — Paper Dunes.** The fixed palette for the typeset system is now the Paper Dunes palette below. It replaces the ivory / gold / teal / terracotta table that follows, which is kept as the record. **The mourning palette is unchanged** — envelopes 01 and 02 stay black on ivory, and every Paper Dunes colour collapses to charcoal or ivory on a `.mourning` page (`04-art/print/assets/print.css`), so nothing built on the new palette can leak colour into a mourning issue.
>
> | Role | Name | Hex |
> |---|---|---|
> | Stock / ground | Sand | `#FFF6EA` |
> | Second ground — envelope stock, pills, panels | Dune | `#FCEBD5` |
> | Primary text | Plum ink | `#3B2440` |
> | First paper layer; the child's-line strip | Apricot | `#F6B48A` |
> | Second paper layer | Rose clay | `#E58F7B` |
> | Small type in clay — kickers, marks, rules | Clay ink | `#B0503E` |
> | The child's voice; deep layer | Oasis | `#1F5C63` |
> | Silhouettes, the wax seal, the hadith-card arch | Dusk | `#5B3A63` |
>
> **The look:** layered cut paper. Dunes in two or three layers with a soft shadow between them, flat colour, no gradients, no outlines. Every page carries a two-layer dune band at its foot. The seal is dusk (was gold) and the cancellation ring is dusk (was gold). The illustration rules in §3 are untouched; the art kit in `tools/paperdunes_art.py` has no figure in it at all, so it cannot depict one of the Fourteen.

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
| Letter + fact panel | **A4 landscape (297 × 210 mm), folded once to A5 portrait** | Portrait faces | **Amended 2026-08-24 — see below.** A bifolium: four A5 faces. Faces 1–2 letter, face 3 the ●○ close, face 4 the fact panel per `fact-panel-spec.md`. Still one sheet. |
| Hadith card | A6 (105 × 148 mm) | Portrait | Front: saying, silsila segment number (never the envelope number — rulebook, `spec-check.md`). Back: citation, per `sourcing-rules.md` citation format. |
| Person print | A5 (148 × 210 mm) | Portrait | Fixed by TASKS.md Phase 0.4. No faces on the Fourteen; faces allowed on companions. |
| Event print | A5 (148 × 210 mm) | Landscape | Fixed by TASKS.md Phase 0.4. Punched — see §6, ring position. Same stock and linework as the person print so all 28 (14+14) read as one wall. |
| Session card | A6 (105 × 148 mm) | Portrait | Same trim as the hadith card so both fit one card box. Conversation / Case File / Mourning / Open layouts per `spec-check.md` §Session types. |
| Sticker sheet | A6 (105 × 148 mm) die-cut | Portrait | Not issued for 01, 02 — pennant instead. |
| Return postcard | A6 (105 × 148 mm) | Landscape | Matches the international minimum postcard dimension, so it can post at postcard rate without a surcharge in most postal systems — confirm against the domestic carrier once Phase 6 sets the return-postcard process. Two signature lines, pre-addressed, per `HANDOVER.md`. |

### The letter moved from A5 to A4 folded (2026-08-24)

**This closes the Gate 3 blocker** recorded in `04-art/print/README.md` and `TASKS.md`: every letter template — all fourteen here and all thirty-nine companions — rendered 28–76% taller than the A5 sheet it was specified on, and the rendered PDFs clipped the excess silently. The word-count spec, the A5 single-sheet spec and the type spec were mutually incompatible.

**The A5 spec is the one that gave.** Of the four options costed in `04-art/print/README.md`, this is the only one that changes nothing already written, measured or fixed:

| Kept | |
|---|---|
| Body type size and face | Unchanged. The letter is the one item read aloud, and shrinking it works against that. |
| 330–370 words, 6–9 child lines | Unchanged. All fifty-three letters stand exactly as written and audited in `03-content/spec-check.md`. |
| Fact panel on the same sheet as the letter | Unchanged. `fact-panel-spec.md`'s "story on the front, facts on the back, one sheet" survives — it is now one folded sheet. |
| Item count per envelope | Unchanged at seven. No new item, no new cost line. |

**What it costs:** the envelope's paper spec moves from A5 to A4, and assembly gains one fold. The envelope itself must now take an A5 stack — **C5, 229 × 162 mm**, or a bespoke wallet at that trim.

**Face 3 is not filler.** A 330–370 word letter needs about 1.8 A5 faces at the fixed type size, so faces 1–2 carry the whole letter with room. Face 3 takes the ●○ read-together close, set large, with space around it. The last line of every letter is the one the parent and child say together; giving it its own face is the design doing what §1 of the rulebook already asks for.

Build geometry, imposition and the Canva mechanics are in `04-art/canva-build-brief.md`.

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

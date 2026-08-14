# Envelope 03 — the remaining five items

The letter, its fact panel and the session card are written. These five are specified here and produced in Phase 1 print.

Running order, per `standard-lines.md` §5, prints inside the flap.

---

## Items

**This table is the machine-readable source** — `tools/build_site.py` reads it to build the card view, exactly as it reads the equivalent table in every `03-content/envelope-*.md`. The detailed sections below are the human-readable spec. **Keep the two in step.**

| # | Item | Spec | State |
|---|---|---|---|
| 2 | Hadith card | **Selected 2026-08-12.** “He who is deprived of kindness is deprived of goodness entirely.” — Tuhaf al-Uqul, short maxims of the Prophet, **no. 112** (trans. Badr Shahin, Ansariyan). Silsila **segment 13** per `spec-check.md` — **but see the numbering conflict below.** | Saying selected; segment number blocked |
| 3 | Person print | Masjid an-Nabawi. Green dome, palm trunks, early light. Full palette, no faces. | **First artwork received 2026-08-12** — ink-and-wash, green dome, minaret. Three deltas open, see below. File not yet in the repo. |
| 4 | Event print | The arrival at Quba. An empty road out of the desert, a kneeling camel, a palm grove. No figures. Ring position 3. | Pending |
| 6 | Sticker sheet | The cloak shape with four corners marked, a palm, the Quba road, a caravan, small repeatable marks. | Pending |
| 7 | Return postcard | Front: the cloak shape, single ink, no text. | Pending |

---

## 2. Hadith card

| | |
|---|---|
| **Front** | A saying of the Prophet. Conduct or ethics only. **Not yet selected** — see the blocker below. |
| **Back** | Silsila segment. |
| **Number printed** | Segment number, in historical order. **Not the envelope number.** Rule C3. |

**Silsila segment, draft:**

> **1.** It begins with him. Everyone else in this box is his family, and every chain of teaching in it runs back through this one man to the words he was given.

Segment 1 of 14, because the silsila runs in historical order while the envelopes run in calendar order — this is envelope 3 of 14 and card 1 of 14, and that mismatch is deliberate and must survive proofreading.

**Edition fixed and saying now selected (2026-08-12):**

> He who is deprived of kindness is deprived of goodness entirely.

Tuhaf al-Uqul, short maxims of the Prophet, **no. 112**, trans. Badr Shahin, Ansariyan. Cited by maxim number, not page — that file is a web-generated PDF, see Trap 2 in `HANDOVER.md`.

Deliberately *not* about trustworthiness. The letter and the fact panel already carry al-Amin, and the rulebook says the card must not repeat the letter.

### ⚠ The segment number is blocked, and it is now blocking print

This file's draft numbers the Prophet **segment 1**. `spec-check.md`'s silsila table numbers him **segment 13** and gives segment 1 to Imam Ali. Both are internally consistent documents and they disagree.

`spec-check.md` already flags this as undecided — *"Two defensible schemes exist… Pick one and apply it to all fourteen cards."* It was harmless while no card had a number on it. **Now that a saying is selected for all fourteen, the number is the last thing standing between these cards and layout, and two cards currently claim segment 1.** Decide the scheme before any hadith card is set.

---

## 3. Person print — A5 portrait, for the wall

**Masjid an-Nabawi.** Green dome, palm trunks, early light.

| | |
|---|---|
| Format | A5 portrait |
| Ink | Full palette |
| Faces | None. No figures at all in the Fourteen. |
| Destination | A wall. It is looked at daily for a year, so it must survive being looked at. |

### First artwork received — 2026-08-12

Ink-and-wash treatment: green dome, the near minaret and one further back, grey wash sky, no figures. The **no-faces rule is respected** and the register (hand-inked, restrained, generous negative space) matches the master style block. Three deltas to settle before this is accepted:

| # | Delta | Why it matters |
|---|---|---|
| 1 | ~~The dome is green and there is no green in the fixed palette.~~ | ✅ **Resolved 2026-08-12.** The fixed palette now binds the typeset system only; artwork chooses its own colour, subject to being complementary. `design-system.md` §2. The dome is green because the dome is green. |
| 2 | **The ground is white; the stock is warm ivory `#F3EDE1`.** *(Still open — this is a stock question, not a palette one, so the open-palette amendment does not touch it.)* | The paper is ivory. A white-ground image printed on it lands as a paler rectangle with a visible edge. **Supply the art on a transparent ground and let the stock show through** — then whatever colours the illustrator chooses sit on the same warm base as every other item. |
| 3 | **No palm trunks, and the composition is inverted from the brief.** The prompt asked for the dome in the upper third with palm trunks grounding the bottom third; here the minaret dominates the upper half and the dome sits centre-left with no foreground. | Not wrong in itself — it is a good composition. But **envelopes 02, 05 and 09 are meant to hang beside it as one Medina set** with consistent light and line weight, so whichever composition wins has to be the one all four are drawn to. Decide now, before the other three are commissioned, not after. |

**Note the tension.** The letter is set in Makkah, twenty-five years before the Hijra, and the person print is the mosque at Medina. That is correct — the person print is the place he is, not the place the letter is, and it pairs against the event print which carries the road that got him there.

Two of the fourteen person prints are Jannat al-Baqi from different angles (02, 05, 09 makes three). Draw all of the Medina prints as one set so the light is consistent across them.

---

## 4. Event print — landscape, punched for the calendar ring

**The arrival at Quba.** An empty road out of the desert, a kneeling camel, a palm grove. No figures.

| | |
|---|---|
| Format | Landscape |
| Punch | Fixed — `00-foundations/design-system.md` §6: 6mm hole, 12mm from top edge, single centered punch |
| Ring position | Third of fourteen in calendar order |
| Label | The Hijra |

The Hijra is the one event in the calendar ring that is a journey rather than a place, and drawing the arrival rather than the departure is what keeps it a place. The road runs out of frame at the bottom edge, so the ring reads as a road when the fourteen hang together.

---

## 5. Session card

Written. See `session-card.md`. Conversation type.

---

## 6. Sticker sheet

Not a mourning issue, so stickers rather than a pennant.

Contents:
- The cloak, as a shape, four corners marked
- A palm
- The Quba road
- A caravan
- Small repeatable marks for the child to use anywhere: a stone, a corner, four hands

**No faces, no figures, no text on the stickers.** A sticker with a sentence on it is a sticker that can only be used once.

---

## 7. Return postcard

Pre-addressed. Fixed wording per `standard-lines.md` §4:

> We opened this one together.
>
> ● ______________________  ○ ______________________
>
> *Post it back to us, or keep it. Either is right.*

Front: the cloak shape, single ink, no text.

---

## Exterior

| Element | Spec |
|---|---|
| Month stamp | Circular postal cancellation, **RABI AL-AWWAL** around the ring |
| Name | Handwritten, or printed for the Named Edition |
| Seal | Wax-seal sticker |
| Flap, inside | Running order and runtime block, per `standard-lines.md` §5 |

Flap block for this envelope:

> **Open together. About twenty-five minutes.**
>
> 1. The letter — read it out loud, ● and ○ taking turns
> 2. The hadith card
> 3. The prints
> 4. Talk about it
> 5. The stickers
> 6. The postcard
>
> ● is the grown-up. ○ is you.

---

## Blocking this envelope

- [x] Fixed edition of Tuhaf al-Uqul — `sourcing-rules.md`. Saying itself still needs picking, which is citation work, not art.
- [x] Ring punch position fixed project-wide — `design-system.md` §6. Physically proof the punch before the event print is drawn.
- [ ] Citation rows filled, all reading `V` — see `citation-sheet.md` open question 1, the sira gap
- [ ] Scholar review
- [ ] Timed with a real family

Artwork for the person print, event print, sticker sheet, and envelope exterior can now be briefed from this file and `design-system.md` — no remaining design blocker stands between spec and drawing.

# Citation sheet

One row per claim that reaches print. **Rows are written before copy, not after.**

Every row must reach `Verified` before Gate 3. A row still marked `TO VERIFY` at Gate 3 means the line it supports is cut, not printed hopefully.

## Status codes

| Code | Meaning |
|---|---|
| `V` | Verified. Opened the named edition, saw the number, read the line. |
| `TV` | To verify. Claim believed sound, not yet checked in the fixed edition. |
| `TRAD` | Traditional. Loved, retold, not documented from the time. Marked as such in the child's copy. |
| `CONT` | Contested between communities. Takes the standard differ line. |
| `CUT` | Checked, did not hold. Kept in the sheet so it is not researched twice. |

**Nothing prints on `TV`.** That is the whole point of the code.

---

## How to fill a row

| Column | Rule |
|---|---|
| Env | Envelope number, or `—` for project-wide |
| Item | letter / panel / hadith card / session card |
| Claim | The claim as it will be printed, not a summary of it |
| Work | Highest-ranked work that carries it, per `sourcing-rules.md` |
| Ref | Book, section, hadith or page number. **A row with no number is not a row.** |
| Translator | Named, matching the fixed edition |
| Status | Code above |
| Note | Contest, variance, or why it was cut |

---

## Envelope 03 — Rabi al-Awwal — Prophet Muhammad

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 03 | letter | The Quraysh rebuilt the Kaaba when the Prophet was about thirty-five | Sira / Tabari | *to fill* | *to fill* | TV | Sira material, not hadith. Needs a citable historical edition — this is outside the five priority works and needs a rule of its own. See open question 1 below. |
| 03 | letter | The clans disputed who would lift the Black Stone into place | Sira / Tabari | *to fill* | *to fill* | TV | Same. |
| 03 | letter | He spread a cloak, set the stone on it, and had each clan carry a corner | Sira / Tabari | *to fill* | *to fill* | TV | Same. Well attested; the point is which printed edition we cite. |
| 03 | panel | Makkah called him al-Amin before revelation | Sira / Tabari | *to fill* | *to fill* | TV | This is the one new thing for the adult. It must be the best-sourced claim in the envelope, not the worst. |
| 03 | panel | Khadija funded the early community out of her own trade | *to fill* | *to fill* | *to fill* | TV | Woman slot. Needs a documented statement of her funding, not a general statement of her wealth. |
| 03 | panel | Twenty-three years of revelation | *to fill* | *to fill* | *to fill* | TV | Standard, still needs a row. |
| 03 | panel | Birth 12th or 17th Rabi al-Awwal | — | — | — | CONT | Takes the standard differ line. |
| 03 | panel | Death 11 AH, Medina | *to fill* | *to fill* | *to fill* | TV | Date differs by community — 28 Safar or 12 Rabi al-Awwal. Both take the differ line. |
| 03 | panel | Elsewhere: work on the Grand Canal under the Sui in China, from around 605 CE | Non-Islamic secondary source | *to fill* | — | TV | AH→CE: the rebuilding sits around 605 CE, pre-Hijra, so no AH conversion needed here. Check the canal dates against a standard reference. |
| 03 | hadith card | *to select from Tuhaf al-Uqul* | Tuhaf al-Uqul | *to fill* | *to fill* | TV | Conduct or ethics only. |

---

## Project-wide rows

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| — | panel | All fourteen death lines | see `death-lines.md` | — | — | TV | Reviewed as one document, not envelope by envelope. |
| — | card | Silsila, historical order, fourteen segments | — | — | — | TV | Segment number prints on the card. Envelope number never does. |

---

## The women — one row each, owed before Gate 3

Each needs a documented act, not a relationship. See `fact-panel-spec.md` §6.

| Env | Woman | The act to source | Status |
|---|---|---|---|
| 01 | Umm al-Banin | *to fill* | TV |
| 02 | Zaynab | That Arbaeen exists because she survived and spoke | TV |
| 03 | Khadija | Funding the early community from her own trade | TV |
| 04 | Nargis | *to fill* | TV / likely TRAD |
| 05 | Zaynab | Her birth on 5 Jumada al-Awwal; the Damascus shrine | TV. **Repeat of envelope 02 — see `death-lines.md` problem 2.** |
| 06 | Fizza | Answering in Qur'anic verse for about twenty years | TRAD |
| 07 | Fatima bint Asad | Birth inside the Kaaba | TV. Marker wording to scholar — see `standard-lines.md` §2. |
| 08 | Hamida | That she taught | TV |
| 09 | Shahrbanu | Her origin | TRAD — accounts vary |
| 10 | Hakima Khatun | Present at the birth | TRAD by most accounts |
| 11 | Samana | *to fill* | TV |
| 12 | Umm Farwa | *to fill* | TV |
| 13 | Sayyida Masuma | Died at Qom travelling to reach him | TV |
| 14 | Umm al-Fadl | *to fill* | TV. **Conflicts with the death line — see `death-lines.md` problem 1.** |

---

## AH → CE conversion

The most likely factual error in the product, because it is the only place doing arithmetic.

```
CE ≈ 622 + (AH − 1) × 0.970224
```

The Hijri year is about 354 days, so the drift against CE is roughly eleven days a year and compounds. Over 260 AH that is about eight years of slip — enough to put the "elsewhere in the world" bullet in the wrong decade if the sum is done as `AH + 622`.

**Do not use `AH + 622`.** It is right for 1 AH and wrong by seven or eight years by the time the box reaches envelope 04.

| Envelope | AH (death) | CE (approx) | Checked twice |
|---|---|---|---|
| 01 | 61 | 680 | ☐ |
| 02 | 50 | 670 | ☐ |
| 03 | 11 | 632 | ☐ |
| 04 | 260 | 874 | ☐ |
| 05 | 114 | 732 | ☐ |
| 06 | 11 | 632 | ☐ |
| 07 | 40 | 661 | ☐ |
| 08 | 183 | 799 | ☐ |
| 09 | 95 | 713 | ☐ |
| 10 | — | — | — |
| 11 | 254 | 868 | ☐ |
| 12 | 148 | 765 | ☐ |
| 13 | 203 | 818 | ☐ |
| 14 | 220 | 835 | ☐ |

Every one of these is `TO VERIFY`. Each also crosses a Hijri new year at a different point, so a birth in Dhul Hijjah and one in Muharram of the same AH sit either side of a CE boundary. Check against a proper converter, not the formula, before print.

---

## Open questions this sheet raises

### 1. The five priority works do not cover biography

`sourcing-rules.md` fixes five works, all of them collections of sayings and reports of conduct. But **the letters are stories**, and the story material — the Kaaba rebuilding, the shield case, the prison years, the public examination — is sira and history, not hadith.

Envelope 03's entire letter has no row that can be filled from the five works.

Options:

1. **Add a sixth and seventh, fixed the same way.** al-Tabari's *History* in the SUNY translation, and one Shia biographical work — al-Mufid's *Kitab al-Irshad* is the obvious candidate and is the natural companion to the five.
2. Cite sira loosely and mark it all traditional. Weakens the product badly; most of it is documented.
3. Restrict letters to what the five works carry. Would cut roughly half the fourteen letters.

**Recommendation: option 1, and add al-Irshad and al-Tabari to the fixed-editions table.** This is a real gap in the PRD's sourcing rule rather than an oversight in this sheet, and it should be closed before any more letters are written.

### 2. The "elsewhere in the world" bullet has no source rule at all

Fourteen claims about world history, none of which any of the named works covers. Fix one general reference work for the whole project and cite it the same way — a standard encyclopedia or a single world-history reference, named in the fixed-editions table.

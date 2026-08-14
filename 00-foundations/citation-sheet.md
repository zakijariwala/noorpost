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
| 03 | letter | Quraysh rebuilt the Ka'ba when the Prophet was about thirty-five | **needs a Shia source** | — | — | TV | ⛔ Was `V` against Guillaume. **Removed 2026-08-12 under the Shia-sources-only rule.** The claim is not in doubt; the source is no longer permitted. Re-source from `al-Irshad` or another Shia work. |
| 03 | letter | The clans disputed who would lift the Black Stone into place | **needs a Shia source** | — | — | TV | ⛔ Same. |
| 03 | letter | He spread a cloak, set the stone on it, and had each clan carry a corner | **needs a Shia source** | — | — | TV | ⛔ Same. |
| 03 | panel | Makkah called him al-Amin before revelation | **needs a Shia source** | — | — | TV | ⛔ Same — **and this is the one new thing for the adult**, so it is the highest-priority row in the envelope. |

> ⛔ **2026-08-12 — the Shia-sources-only rule reverted these four rows.** They were the project's only fully verified letter, checked against Guillaume's Ibn Ishaq. That work is Sunni and has been removed from the project entirely, so the rows revert to `TV` and the extract has been deleted from `00-sources/text/`.
>
> **Nothing about the claims changed.** They are as well attested as they were an hour ago — the Kaaba rebuilding, the dispute, the cloak and the name *al-Amin* are all carried in Shia sira and history too. What is missing is a permitted edition to cite them from. **This is an acquisition problem, not a content problem**, and it is the reason `al-Irshad` is now the project's most valuable single purchase.
>
> The earlier page-number correction on these rows (pp. 66–67 → 84–86) is now moot and is kept only in the commit history.

| 03 | panel | Khadija funded the early community out of her own trade | *to fill* | *to fill* | *to fill* | TV | Woman slot. Needs a documented statement of her funding, not a general statement of her wealth. |
| 03 | panel | Twenty-three years of revelation | *to fill* | *to fill* | *to fill* | TV | Standard, still needs a row. |
| 03 | panel | Birth 12th or 17th Rabi al-Awwal | — | — | — | CONT | Takes the standard differ line. |
| 03 | panel | Death 11 AH, Medina | *to fill* | *to fill* | *to fill* | TV | Date differs by community — 28 Safar or 12 Rabi al-Awwal. Both take the differ line. |
| 03 | panel | Elsewhere: work on the Grand Canal under the Sui in China, from around 605 CE | Non-Islamic secondary source | *to fill* | — | TV | AH→CE: the rebuilding sits around 605 CE, pre-Hijra, so no AH conversion needed here. Check the canal dates against a standard reference. |
| 03 | hadith card | “He who is deprived of kindness is deprived of goodness entirely.” | Tuhaf al-Uqul | short maxims of the Prophet, **no. 112** | Badr Shahin | V | Selected 2026-08-12. See the all-fourteen table below. |

---

## Envelope 09 — Imam al-Sajjad

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 09 | letter/panel | *Risalat al-Huquq* has fifty-one entries | Risalat al-Huquq | Entries 1–51, numbered "1. The Greatest Right of Allah" through "51) The Right of People under the protection of Islam" | William C. Chittick | V | Counted directly off the English section headers in the fixed edition — 51, not "around fifty." One numbering quirk: the Arabic transliteration numerals drop out of sync after entry 39 (the unnumbered Arabic line for "the adversary against whom you have a claim"), but the English headers run 1–51 with no gap or repeat, and are the count of record. |
| 09 | letter | The right of the tongue, quoted exactly: "The right of the tongue is that you consider it too noble for obscenity, accustom it to good, refrain from any meddling in which there is nothing to be gained, express kindness to the people, and speak well concerning them." | Risalat al-Huquq | **Entry 3** (the treatise's own numbering — stable across editions, and the citation of record) | William C. Chittick | V | Full sentence, no ellipsis needed to fit a card — check `standard-lines.md` / card layout for whether it needs trimming with `…`, which is permitted, rather than paraphrase, which is not. **Page number deliberately omitted:** the copy in `00-sources/text/` is a web-generated al-Islam.org PDF whose pagination does not match the printed Muhammadi Trust edition fixed in `sourcing-rules.md`. Add a printed page only if someone checks a physical copy. |

---

## Envelope 13 — Imam al-Rida

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 13 | letter | Imam al-Rida's four conditions for accepting the succession — he would appoint nobody, dismiss nobody, change nothing already in place, and give no opinion unless asked | Uyun Akhbar al-Rida, vol. 2 | Three passages, all in vol. 2 of the fixed edition: the conditions as written to al-Ma'mun; the "distant advisor" statement; and his later reminder to al-Ma'mun when pressed to name a governor. Cite the second as primary. **Page numbers pending** — see the two-column/edition caveat in `sourcing-rules.md`; this edition's own internal chapter-and-report numbering is the stable reference, not the PDF page. | Dr. Ali Peiravi | V | Primary support: *"I will accept it under the condition that I do not interfere in dismissals or appointments, nor change any practices or traditions. I will just be a distant advisor."* Corroborated by: *"I will neither issue any orders, nor will I admonish anyone. I will not remove anyone from office, neither will I appoint anyone."* A third passage phrases the same conditions differently (*"I neither issue any orders, nor do I admonish against anything; I neither judge, nor change anything"*). **All three are the same event; the draft letter line is supported and stands.** ⚠ **2026-08-12 correction:** an earlier pass read only the third passage, wrongly recorded the draft as unsupported, and rewrote the printed line. Reverted. Lesson: a differently-worded passage is not disproof — search the whole work before cutting a line. |

---

## Hadith cards — all fourteen

Selected 2026-08-12. **Cited by the work's own internal number, never by page** — Tuhaf al-Uqul and Risalat al-Huquq are both web-generated PDFs whose pagination does not match the printed editions (Trap 2, `HANDOVER.md`). Every saying below is conduct or ethics, per `sourcing-rules.md` subject limits, and none repeats its envelope's letter.

| Env | Seg | Masoom | Saying | Work | Ref | Status |
|---|---|---|---|---|---|---|
| 01 | 3 | Imam Husayn | "The true stingy is that who refrains from greeting." | Tuhaf al-Uqul | short maxims, no. 18 | V |
| 02 | 2 | Imam Hasan | "The people who consult for their affairs will surely be guided to the right." | Tuhaf al-Uqul | short maxims, no. 1 | V |
| 03 | 13 | The Prophet | "He who is deprived of kindness is deprived of goodness entirely." | Tuhaf al-Uqul | short maxims, no. 112 | V |
| 04 | 11 | Imam al-Askari | "The heart of the foolish is in his mouth and the mouth of the wise is in his heart." | Tuhaf al-Uqul | short maxims, no. 21 | V |
| 05 | 6 | Imam al-Baqir | "No mixture is better than the mixture of clemency and knowledge." | Tuhaf al-Uqul | short maxims, no. 2 | V |
| 06 | 4 | Sayyida Fatima | — | — | — | **BLOCKED — no source** |
| 07 | 1 | Imam Ali | "The value of a man is what he does expertly." | Tuhaf al-Uqul | short maxims, no. 8 | V |
| 08 | 8 | Imam al-Kadhim | "Good neighborhood is not abstinence from harm. It is to tolerate the harm (of the neighbors)." | Tuhaf al-Uqul | short maxims, no. 13 | V |
| 09 | 5 | Imam al-Sajjad | "The right of the tongue is that you consider it too noble for obscenity…" (full text above) | Risalat al-Huquq | entry 3 | V |
| 10 | 14 | Imam al-Mahdi | — | — | — | **BLOCKED — no source** |
| 11 | 10 | Imam al-Hadi | "This world is like a market in which some profited and others lost." | Tuhaf al-Uqul | short maxims, no. 15 | V |
| 12 | 7 | Imam al-Sadiq | "He who treats people kindly will be accepted as arbiter." | Tuhaf al-Uqul | short maxims, no. 1 | V |
| 13 | 9 | Imam al-Rida | "Silence is one of the doors of wisdom. It yields amicability and leads to every goodness." | Tuhaf al-Uqul | short maxims, no. 8 | V |
| 14 | 12 | Imam al-Jawad | "To show a matter before preparing for it properly is spoiling it." | Tuhaf al-Uqul | short maxims, no. 12 | V |

### The two that cannot be selected yet

Neither is an oversight — **the source does not exist in this repo**, and no amount of searching the fixed editions will produce one.

**Envelope 06 · Sayyida Fatima · segment 4.** Tuhaf al-Uqul has no Fatima section at all — it runs the Prophet, then Imam Ali through Imam al-Askari, and she is not among them. Her sayings live mainly in works this project has not fixed an edition of, and the obvious candidate — her khutba — is exactly the contested ground envelope 06 is written to stay off. **Needs a new fixed edition acquired and recorded in `sourcing-rules.md` before a card can be set.**

**Envelope 10 · Imam al-Mahdi · segment 14.** This card is specified as a *tawqi'* from the minor occultation. Those are carried in Kamal al-Din and the two Kitab al-Ghayba works — all three already flagged in `sourcing-rules.md` as available only in an aggregator copy credited to `en.unknown`, which fails this project's own translator rule. **Same blocker as the envelope 10 occultation gap in `sources-needed.md` Tier 2.** It also carries the extra constraint that the tawqi' must be conduct, not theology (rule Q3), which narrows the field further once a source exists.

### One thing this unblocks, and one it blocks

**Unblocked:** twelve of fourteen hadith cards can go to layout as soon as the segment-numbering scheme is settled.

**Newly blocking:** the **silsila segment number prints on every card**, and the scheme is still undecided — `spec-check.md` numbers the Prophet 13 and Imam Ali 1, while `01-pilot/envelope-03/items.md` numbers the Prophet 1. Two cards currently claim segment 1. This was harmless while no card had a saying on it. It is not harmless now.

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

1. **Add a sixth work, fixed the same way — and it must be Shia.** al-Mufid's *Kitab al-Irshad* is the candidate and the natural companion to the five. *(An earlier version of this option also named al-Tabari's History; that is a Sunni work and is excluded by the hard rule in `sourcing-rules.md`.)*
2. Cite sira loosely and mark it all traditional. Weakens the product badly; most of it is documented.
3. Restrict letters to what the five works carry. Would cut roughly half the fourteen letters.

**Status: fully open again as of 2026-08-12.** This was briefly closed for envelope 03 using Guillaume's Ibn Ishaq, and al-Tabari Vol. VIII was fixed alongside it. **Both were Sunni works and have been removed under the hard rule at the top of `sourcing-rules.md`.**

Option 1 still stands, but it has to be executed with Shia works only. That narrows it to essentially one candidate:

- **al-Mufid, *Kitab al-Irshad*** — the Shia biography of the Twelve, in order. It is now **the single most important acquisition in the project**: it has to carry the narrative spine of most of the fourteen letters and much of the companions line. Two extracts sit in `00-sources/text/` already but neither credits a translator, so nothing can be cited from them. Acquiring a copy with a named translator (I.K.A. Howard is the standard one) closes more open rows than any other single purchase.
- Secondary Shia narrative works already held — Subhani's *The Message*, the Qarashi lives — may cover specific episodes and are permitted, but none is a substitute for al-Irshad and none has been fixed as an edition yet.

### 2. The "elsewhere in the world" bullet has no source rule at all

Fourteen claims about world history, none of which any of the named works covers. Fix one general reference work for the whole project and cite it the same way — a standard encyclopedia or a single world-history reference, named in the fixed-editions table.

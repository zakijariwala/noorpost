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
| 03 | panel | Makkah called him al-Amin before revelation | *The Fourteen Infallibles*, Yasin T. Al-Jibouri | "Holy Prophet", §*Year of the Elephant*, pp. 7–8 | English original — Al-Jibouri writes in English, no translator in the chain | **TV** → **passage found, edition not fixed** | **Reopened row, now half-closed 2026-08-14.** A permitted Shia source carrying the claim **has been found in the repo**: *"When Mohammed twenty years old, he was well-known for his truthfulness and uprightness, hence he was called AL-SADIQ, AL-AMIN"*, and the reasons follow on the same page — *"They used to seek his help to solve their problems. They entrusted him with their trusts. They never heard him lie or cheat."* That is the claim and the *"had reasons"* half of it, in one Shia work with a named author. **What stops it going to `V` is the edition, not the text** — this is an alhassanain.org web PDF with no publisher or year, and it is not one of the six fixed editions in `sourcing-rules.md`. Trap 1 checked: 0%, single-column, page markers are reliable. Trap 2 applies: cite the section heading, not the page. **This row closes the moment a sixth work is fixed** — see the decision below. |

> ⛔ **2026-08-12 — the Shia-sources-only rule reverted these four rows.** They were the project's only fully verified letter, checked against Guillaume's Ibn Ishaq. That work is Sunni and has been removed from the project entirely, so the rows revert to `TV` and the extract has been deleted from `00-sources/text/`.
>
> **Nothing about the claims changed.** They are as well attested as they were an hour ago — the Kaaba rebuilding, the dispute, the cloak and the name *al-Amin* are all carried in Shia sira and history too. What is missing is a permitted edition to cite them from. **This is an acquisition problem, not a content problem**, and it is the reason `al-Irshad` is now the project's most valuable single purchase.
>
> The earlier page-number correction on these rows (pp. 66–67 → 84–86) is now moot and is kept only in the commit history.
>
> **Update 2026-08-14 — one of the four is now a decision, not a search.** The al-Amin row above has a permitted Shia passage behind it, found in `00-sources/text/fourteen--the-fourteen-infallibles.txt`, which is by a named author and is not a translation at all. **The blocker on that row is no longer "no Shia source exists in the repo" — it is that the work is not a fixed edition.** The other three rows (the Ka'ba rebuilding, the dispute, the cloak) were searched in the same pass across the whole of `00-sources/text/` and **are not carried by anything held** — those remain an acquisition problem and still point at `al-Irshad`.
>
> **The decision this forces:** the fixed-editions table has six works and all six are hadith or letter collections, which is exactly why the sira gap exists. Fixing a seventh — a Shia biographical work — closes the al-Amin row and gives the other narrative rows somewhere to go. *The Fourteen Infallibles* is a candidate but a weak one (aggregator PDF, no publisher, no year). **`al-Mufid's Kitab al-Irshad` with a named translator is still the better purchase and still the right answer**; this finding does not change that, it just means one row no longer has to wait for it.

| 03 | panel | Khadija funded the early community out of her own trade | *to fill* | *to fill* | *to fill* | TV | Woman slot. Needs a documented statement of her funding, not a general statement of her wealth. |
| 03 | panel | Twenty-three years of revelation | *to fill* | *to fill* | *to fill* | TV | Standard, still needs a row. |
| 03 | panel | Birth 12th or 17th Rabi al-Awwal | — | — | — | CONT | Takes the standard differ line. |
| 03 | panel | Death 11 AH, Medina | *to fill* | *to fill* | *to fill* | TV | Date differs by community — 28 Safar or 12 Rabi al-Awwal. Both take the differ line. |
| 03 | panel | Elsewhere: work on the Grand Canal under the Sui in China, from around 605 CE | Non-Islamic secondary source | *to fill* | — | TV | AH→CE: the rebuilding sits around 605 CE, pre-Hijra, so no AH conversion needed here. Check the canal dates against a standard reference. |
| 03 | hadith card | “He who is deprived of kindness is deprived of goodness entirely.” | Tuhaf al-Uqul | short maxims of the Prophet, **no. 112** | Badr Shahin | V | Selected 2026-08-12. See the all-fourteen table below. |

---

### ✅ Envelope 03's four rows close on *The Message* (2026-08-24)

**Chapter 10, "From Marriage upto Prophethood"**, carries the whole letter narrative in one continuous passage — the flood and the demolition, the Copt mason, the walls to the height of a man, the Black Stone dispute, Bani Abduddar and Bani Adi, **the container filled with blood and the hands put into it**, the five days of suspended work, Abu Umayyah's proposal to accept whoever next entered the gate, and **the piece of cloth**.

| Row | Claim | Status now |
|---|---|---|
| Ka'ba rebuilding after the flood | ✅ | `V` — *The Message*, ch. 10 |
| The dispute over who sets the Stone | ✅ | `V` — same passage |
| The cloak | ✅ | *"the Holy Prophet asked them to bring a piece of cloth"* — same passage |
| Makkah called him al-Amin **before revelation, and had reasons** | ⚠ **half** | The passage has the crowd say *"It is Muhammad, the honest one. We agree to his acting as the arbitrator!"* — which carries the naming and the trust, at the gate, before revelation. **It does not carry "and had reasons."** Mark `CONT` and either narrow the panel's claim or close the second half from another work. |

**A grep for `al-Amin` returns nothing in this work** — the translation renders it *"the honest one"*. That is why four searches missed a passage that was in the library the whole time, and it is worth remembering before declaring any row unsourced: **search the claim, not the epithet.**

**Cite the chapter, never the page.** 549 web-generated pages against a 783-page printing; `[[p N]]` here is an artifact of the PDF.

---

## Envelope 09 — Imam al-Sajjad

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 09 | letter/panel | *Risalat al-Huquq* has fifty-one entries | Risalat al-Huquq | Entries 1–51, numbered "1. The Greatest Right of Allah" through "51) The Right of People under the protection of Islam" | William C. Chittick | V | **⚠ Two renderings of the same translator disagree, 2026-08-24. The count of record is unchanged at 51** — it was counted off the fixed edition's own English headers, which is the edition envelope 09 cites. The approved Thaqalayn corpus serves the same Chittick translation as **49 records**, ending on the same right. Someone has to establish which entries it drops before this row is quoted on anything other than the fixed edition. Counted directly off the English section headers in the fixed edition — 51, not "around fifty." One numbering quirk: the Arabic transliteration numerals drop out of sync after entry 39 (the unnumbered Arabic line for "the adversary against whom you have a claim"), but the English headers run 1–51 with no gap or repeat, and are the count of record. |
| 09 | letter | The right of the tongue, quoted exactly: "The right of the tongue is that you consider it too noble for obscenity, accustom it to good, refrain from any meddling in which there is nothing to be gained, express kindness to the people, and speak well concerning them." | Risalat al-Huquq | **Entry 3** (the treatise's own numbering — stable across editions, and the citation of record) | William C. Chittick | V | Full sentence, no ellipsis needed to fit a card — check `standard-lines.md` / card layout for whether it needs trimming with `…`, which is permitted, rather than paraphrase, which is not. **Page number deliberately omitted:** the copy in `00-sources/text/` is a web-generated al-Islam.org PDF whose pagination does not match the printed Muhammadi Trust edition fixed in `sourcing-rules.md`. Add a printed page only if someone checks a physical copy. |

---

## Envelope 13 — Imam al-Rida

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 13 | letter | Imam al-Rida's four conditions for accepting the succession — he would appoint nobody, dismiss nobody, change nothing already in place, and give no opinion unless asked | Uyun Akhbar al-Rida, vol. 2 | Three passages, all in vol. 2 of the fixed edition: the conditions as written to al-Ma'mun; the "distant advisor" statement; and his later reminder to al-Ma'mun when pressed to name a governor. Cite the second as primary. **Page numbers pending** — see the two-column/edition caveat in `sourcing-rules.md`; this edition's own internal chapter-and-report numbering is the stable reference, not the PDF page. | Dr. Ali Peiravi | V | Primary support: *"I will accept it under the condition that I do not interfere in dismissals or appointments, nor change any practices or traditions. I will just be a distant advisor."* Corroborated by: *"I will neither issue any orders, nor will I admonish anyone. I will not remove anyone from office, neither will I appoint anyone."* A third passage phrases the same conditions differently (*"I neither issue any orders, nor do I admonish against anything; I neither judge, nor change anything"*). **All three are the same event; the draft letter line is supported and stands.** ⚠ **2026-08-12 correction:** an earlier pass read only the third passage, wrongly recorded the draft as unsupported, and rewrote the printed line. Reverted. Lesson: a differently-worded passage is not disproof — search the whole work before cutting a line. |

---

## Envelope 08 — Imam al-Kadhim

**Worked 2026-08-14.** Row #4 on the `sources-needed.md` priority list — *"al-Kadhim's four years, consistent across letter, sealed answer and death line."* The whole of `qarashi--the-life-of-imam-musa-bin-jafar-al-kazim.txt` was searched, not the first hit. Trap 1 checked: 0%, single-column, page markers reliable.

**The work qualifies, and that is itself a finding.** Its title page credits **author Baqir Sharif al-Qarashi, translator Jasim al-Rasheed, publisher Ansariyan Publications, Qum** — author, translator *and* publisher. It is a better-credited source than the aggregator copies that fail this project's own rule, and `sources-needed.md` had it listed only as one of "four of the six Qarashi lives" missing without noting that the two held ones carry full credits.

| Env | Item | Claim | Work | Ref | Translator | Status | Note |
|---|---|---|---|---|---|---|---|
| 08 | letter/panel | Arrested in Medina, Shawwal 20, 179 AH | Qarashi, *The Life of Imam Musa bin Ja'far al-Kazim* | Ch. "Imam Musa is arrested" | Jasim al-Rasheed (Ansariyan) | **V** | Stated flatly, with the Imam taken in chains from the Prophet's grave. This is the start date the "four years" is counted from. |
| 08 | letter/panel | About a year of it was in Basra, before Baghdad | Qarashi, same work | Ch. "The Imam is carried to Baghdad", opening — *"stayed in the detention of 'Isa for a year"* | Jasim al-Rasheed (Ansariyan) | **V** | ⚠ **This corrected a printed line.** The letter opened *"held in a prison in Baghdad for about four years"*, which puts the whole span in the wrong city — roughly the first year was Basra, in 'Isa b. Ja'far's custody, and Baghdad came after. Fixed to *"held in prison, moved from city to city, for about four years"*; count re-measured, 357 → 359 words, still in range. **The fact panel was already right** (*"Medina for most of it, then Basra and Baghdad"*), so the two disagreed with each other and nobody had noticed. |
| 08 | letter/panel/death line | Held about four years without charge | Qarashi, same work | Computed: arrest Shawwal 179 → death 183 ≈ 3 years 9 months | Jasim al-Rasheed (Ansariyan) | **TRAD** | **"About four years" holds and all three places agree.** It is not `V` because the number is arithmetic across two dates rather than a statement in the source — no passage in the work says "four years" of the imprisonment. Keep the word *about*; it is doing real work. |
| 08 | panel | Died 183 AH | **contested inside the source itself** | §22 "The Time of his Death" | Jasim al-Rasheed (Ansariyan) | **CONT** | ⚠ **The held work does not support 183 in its own headline.** §22 gives *"Rajab 25, in the year 173 A. H."* as the famous narration, then names 181 and 186 as variants. **173 is impossible against this same book's arrest date of 179** and is almost certainly a digit error for 183; 183 appears in the book only inside a quotation from Dr. Muhammed Yousif Musa. **Do not print 183 on this source alone.** Check a physical copy of §22, or source the death date from Uyun or al-Irshad. The `AH → CE` table row for 183 is unaffected either way — but if the date moves, the death line, the panel dateline and that row all move together. |

### ⛔ Envelope 07's spine was cut and replaced (2026-08-24)

**The Shurayh shield case is `CUT`.** Five searches, each against a larger corpus than the last, ended with the complete `Kitab al-Irshad` — I. K. A. Howard's translation, all twelve Imams, acquired the same day. Ten passages there mention Shurayh and every one has him sitting as judge; **none is Imam Ali as the defendant over a coat of mail.** The last plausible source has now been checked and the claim is not in it.

**The letter was rewritten rather than left unsourced.** Its spine is now **Nahj al-Balagha, Letter 45**, to Uthman ibn Hunayf — the governor of Basra who attended a banquet the poor had been turned away from. It is in the fixed edition (`SRC-NHB-002`, trans. Sayed Ali Reza), cited by its own letter number, and it keeps the envelope's through-question intact: he appointed the man, he could have removed him, every storehouse between Egypt and India was his, and the whole episode is about what he did not take.

**Deliberately not used:** the Fadak passage further down the same letter. Envelope 07 does not go on that ground, and the letter draws only on the banquet, the two worn cloths and the bread.

| Row | Status |
|---|---|
| The shield case: Shurayh's name, ruling, grounds, congratulation | **`CUT`** — not in any held source, including the complete al-Irshad |
| The banquet at Basra, and what he wrote about his own house | **`V`** — Nahj al-Balagha, Letter 45, trans. Sayed Ali Reza |

---

**Row #5 checked in the same pass and it did not move.** The Shurayh shield case (envelope 07) needs a named narrator for the judge, the ruling and the grounds. Searched across the whole of `00-sources/text/`: the two `al-Irshad` extracts still credit **no translator at all** and so remain uncitable; Nahj al-Balagha carries Shurayh only in Letter 3, the house-purchase rebuke, which is a different episode entirely; nothing in either Fourteen volume carries the case. **Still blocked on `al-Irshad` with a named translator, exactly as recorded** — this is a confirmed negative, not an unchecked row.

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

## Hadith cards — the companions line, all thirty-nine

**Added 2026-08-14 by decision. 0 of 39 selected — this table is a placeholder, not a record of work.**

The companions line now carries a hadith card (`08-companions/README.md`; rulebook C5a/C6). **The evidentiary standard is identical to the box** — conduct and ethics only, quoted exactly, fixed edition, cited by internal number. A companion card is not a lighter row.

**Selection rule:** the saying is of the Masoom the envelope points home to, theme-matched to that person, and **never a repeat of that Masoom's box card above.**

**The binding constraint:** eight companions point to the Prophet and eight to Imam Husayn, so those two need **eight distinct sayings each**. Tuhaf al-Uqul carries a numbered short-maxims section for every Masoom except the two below.

### Six that cannot be selected

| Entry | Points to | Status |
|---|---|---|
| Fizza | Sayyida Fatima | **BLOCKED — no source.** Identical to envelope 06 above. |
| Muhammad ibn Uthman | Imam al-Mahdi | **BLOCKED — no source.** Identical to envelope 10 above. |
| Husayn ibn Ruh | Imam al-Mahdi | **BLOCKED — no source.** |
| Ali ibn Muhammad al-Samarri | Imam al-Mahdi | **BLOCKED — no source.** |
| Narjis Khatun | Imam al-Mahdi | **BLOCKED — no source.** |
| Khawla bint al-Azwar | **nobody** | **BLOCKED — no rule.** The only entry pointing to no Masoom. Needs a decision, not a source. |

**What this changes about priority.** The Sayyida Fatima gap and the Imam al-Mahdi gap each blocked exactly one box card. **They now block four items and five items respectively.** Either acquisition buys four times what it did before — reflected in `sources-needed.md`.

Asma bint Umays and Uthman ibn Sa'id point to more than one Masoom and are **not** blocked.

### The thirty-nine rows

**Selected 2026-08-24. Twenty-nine of thirty-nine carry a saying; ten are blocked.** Every saying below is quoted verbatim from Tuhaf al-Uqul (rank 1 in `sourcing-rules.md`), cited by the work's own maxim number, never a page. The selector is `tools/select_hadith_cards.py`; the record is `hadith-assignments.json`, and `tools/apply_hadith_assignments.py` is the only thing that writes the card row into an entry file, so the two cannot drift.

**Confidence is the selector's, not a scholar's.** `high` means the saying and the theme meet on more than one word and nothing else came close. Everything below `high` — twenty-two rows — is on `hadith-verification-worklist.md` and is to be checked by someone else before it reaches a card.

**The chain is numbered by the standing proposal**: grouped by the Masoom the envelope points home to, in historical order, and numbered **independently of the silsila** so the box's unresolved segment fight cannot leak into it. If the ordering decision goes another way, the numbers change and nothing else does.

| # | Entry | Points to | Theme | Saying | Ref | Confidence |
|---|---|---|---|---|---|---|
| 01/39 | Salman al-Farsi | the Prophet | who counts as family | “Regard your relatives even by means of mere greeting.” | short maxims of the Prophet, no. 165 | `medium` |
| 02/39 | Bilal | the Prophet | steadfastness | “Faith is two halves; one half is lying in patience and the other in thankfulness.” | short maxims of the Prophet, no. 99 | `high` |
| 03/39 | Abu Dharr | the Prophet | speaking for the poor | “Ask the scholars, speak with the wise, and sit with the poor.” | short maxims of the Prophet, no. 40 | `high` |
| 04/39 | Sumayyah bint Khabbat | the Prophet | holding on when it is not safe to | “Blessed are those who leave a current passion for obtaining a promised one that they have not seen yet.” | short maxims of the Prophet, no. 119 | `medium` |
| 05/39 | Nusaybah bint Ka'b | the Prophet | courage that shields somebody else | “It is illicit to violate anything of the believer: his honor, wealth, and blood—all are sanctified.” | short maxims of the Prophet, no. 164 | `low` |
| 06/39 | Umm Ayman | the Prophet | care that lasts a whole life | “Hearts are molded on cherishing those who treat them charitably and abhorring those who treat them nastily.” | short maxims of the Prophet, no. 17 | `medium` |
| 07/39 | Halima al-Sa'diyya | the Prophet | kindness to a child in your care | “Kindness gives embellishment to everything it joins, and clumsiness ruins everything it joins.” | short maxims of the Prophet, no. 95 | `medium` |
| 08/39 | Asma bint Umays | the Prophet | staying through every upheaval | “The proper fulfillment of the pledges is a part of faith.” | short maxims of the Prophet, no. 100 | `low` |
| 09/39 | Fizza | Sayyida Fatima | speech, and how little of it is needed | — | — | **BLOCKED** |
| 10/39 | Maytham al-Tammar | Imam Ali | truthfulness when it costs | “No one will find the true taste of faith before he neglects telling lies whether seriously or jokingly.” | short maxims of Imam Ali, no. 104 | `high` |
| 11/39 | Qambar | Imam Ali | service, and what a servant is owed | “Every powerful that is under God's control is humble.” | short maxims of Imam Ali, no. 95 | `low` |
| 12/39 | Malik al-Ashtar | Imam Ali | gentleness in authority | “People's similarity to their rulers is more than their similarity to their fathers.” | short maxims of Imam Ali, no. 57 | `medium` |
| 13/39 | Fatima bint Asad | Imam Ali | raising a child who is not your own | “A true friend is that who regards in misfortunes, absence, and after death.” | short maxims of Imam Ali, no. 129 | `low` |
| 14/39 | Qais ibn Sa'd | Imam Hasan | obeying when you think it is wrong | “He who depends upon God's good option for him will not wish to be in a situation other than that which God opts for him.” | short maxims of Imam al-Hasan, no. 6 | `high` |
| 15/39 | Abbas ibn Ali | Imam Husayn | a trust kept when nobody would have known | “Favors should be like the heavy rain that covers the pious and the sinful.” | short maxims of Imam al-Husayn, no. 3 | `medium` |
| 16/39 | Umm Kulthum bint Ali | Imam Husayn | children, in the worst of it | “Beware of things for which you apologize.” | short maxims of Imam al-Husayn, no. 16 | `low` |
| 17/39 | Rabab bint Imra' al-Qays | Imam Husayn | faithfulness that outlasts the person | — | — | **BLOCKED** |
| 18/39 | Zaynab bint Ali | Imam Husayn | the truth said in front of a ruler | “He who tries to achieve something through acting disobediently to God will miss what he expects and fall in what he fears.” | short maxims of Imam al-Husayn, no. 19 | `medium` |
| 19/39 | Sakina bint al-Husayn | Imam Husayn | remembering | — | — | **BLOCKED** |
| 20/39 | Fitrus | Imam Husayn | grief, and what it is owed | — | — | **BLOCKED** |
| 21/39 | Umm al-Banin | Imam Husayn | raising another woman's children as your own | — | — | **BLOCKED** |
| 22/39 | Sayyida Ruqayya bint al-Husayn | Imam Husayn | the smallest person in the room | “O son, beware of wronging him who does not have a supporter except God the Majestic.” | short maxims of Imam al-Husayn, no. 10 | `high` |
| 23/39 | Tawus al-Yamani | Imam al-Sajjad | worship nobody is watching | “Many are those whom are deceived by commendation.” | short maxims of Imam al-Sajjad, no. 23 | `low` |
| 24/39 | Jabir ibn Abdullah al-Ansari | Imam al-Baqir | keeping a trust across a lifetime | “Abide by piety, diligence, honesty, and fulfillment of the trusts of the charitable as well as the sinful.” | short maxims of Imam al-Baqir, no. 56 | `high` |
| 25/39 | Hisham ibn al-Hakam | Imam al-Sadiq | knowledge, whatever the age of the one holding it | “Everything has its tax and the tax of knowledge is to teach its people.” | short maxims of Imam al-Sadiq, no. 77 | `high` |
| 26/39 | Umm Farwa | Imam al-Sadiq | honouring a mother by name | “A twenty-year friendship is kinship.” | short maxims of Imam al-Sadiq, no. 16 | `low` |
| 27/39 | Safwan al-Jammal | Imam al-Kadhim | the earnings you refuse | “The expiation of working with the (unjust) rulers is to treat the friends with kindness.” | short maxims of Imam al-Kadhim, no. 20 | `medium` |
| 28/39 | Hamida Khatun | Imam al-Kadhim | teaching, and who is fit to teach | “The astonishment of the ignorant at the intelligent is greater than the astonishment of the intelligent at the ignorant.” | short maxims of Imam al-Kadhim, no. 34 | `low` |
| 29/39 | Dibil al-Khuza'i | Imam al-Rida | saying the thing out loud | “When you want to mention a present person, you should use his surname, but when you refer to an absent person, you should use his name.” | short maxims of Imam al-Rida, no. 13 | `low` |
| 30/39 | Sayyida Ma'suma | Imam al-Rida | family, and the road toward it | “The elder brother is as same as the father.” | short maxims of Imam al-Rida, no. 10 | `medium` |
| 31/39 | Ali ibn Mahziyar | Imam al-Jawad | discharging a trust, every time | “A believer is in need of successfulness from God, a self-preaching, and accession to the advisers.” | short maxims of Imam al-Jawad, no. 13 | `low` |
| 32/39 | Abu Hashim al-Ja'fari | Imam al-Hadi | giving before being asked | “The thankful of a grace should be happy for thankfulness more than it is for the grace.” | short maxims of Imam al-Hadi, no. 10 | `low` |
| 33/39 | Ahmad ibn Ishaq al-Qummi | Imam al-Askari | carrying other people's questions | “Those who advice their friends secretly are respecting them, and those who advice them openly are humiliating them.” | short maxims of Imam al-Askari, no. 33 | `medium` |
| 34/39 | Uthman ibn Sa'id al-Amri | Imam al-Askari | trustworthiness | “The faithful believer is a blessing for the believers and a claim against the disbelievers.” | short maxims of Imam al-Askari, no. 20 | `low` |
| 35/39 | Muhammad ibn Uthman al-Amri | Imam al-Mahdi | keeping a post without being seen to | — | — | **BLOCKED** |
| 36/39 | Husayn ibn Ruh al-Nawbakhti | Imam al-Mahdi | restraint in what is said | — | — | **BLOCKED** |
| 37/39 | Ali ibn Muhammad al-Samarri | Imam al-Mahdi | the close of a trust | — | — | **BLOCKED** |
| 38/39 | Narjis Khatun | Imam al-Mahdi | keeping what must be kept | — | — | **BLOCKED** |
| 39/39 | Khawla bint al-Azwar | nobody | — | — | — | **BLOCKED** |

### What the selection pass found

**Imam al-Husayn's section cannot fill his eight rows.** Tuhaf's short maxims of Imam al-Husayn yield nine numbered items; two are theological in register, one is an exegesis of a verse, one is a sermon fragment, and **no. 17 is a second saying about greeting, which would near-repeat box card 01's no. 18** — the exact failure the "do the eight as a set" note was written to prevent. Four usable maxims remain, and they are on rows 15, 16, 18 and 22. **Rows 17, 19, 20 and 21 are blocked on a source, not on effort.**

**The Thaqalayn corpus did not help here, and the reason is worth recording.** It is organised by topic rather than by speaker, so attribution has to be read off each report — and every apparent Imam al-Husayn hit in it turned out to be Imam al-Sajjad (*Ali ibn al-Husayn*) or a report *about* Imam al-Husayn rather than by him. Likewise every apparent Sayyida Fatima and Imam al-Mahdi hit. **The corpus is 32,531 records and it moved none of the six source-blocked rows.**

**Sayyida Fatima and Imam al-Mahdi remain blocked**, which keeps box cards 06 and 10 blocked with them. Both Kitab al-Ghayba works are now held with named translators, so the four al-Mahdi rows are a reading job rather than a purchase — but rule Q3 bans a tawqi' about religious authority, and that is most of what survives.

**Two constraints to hold while working down this table.**

**Eight distinct sayings for the Prophet and eight for Imam Husayn.** Those are the first sixteen rows and they are the hard part — the temptation is a near-repeat, and a near-repeat across two envelopes a child may own both of is worse than a weaker match. Do those sixteen as a set, not one at a time.

**No companion card repeats its Masoom's box card.** Two are already spent and must be struck off the candidate list before the Prophet's and Imam Husayn's sets are chosen:

| Spent on | Saying | Where |
|---|---|---|
| the Prophet | "He who is deprived of kindness is deprived of goodness entirely." | Tuhaf, short maxims of the Prophet, **no. 112** — envelope 03 |
| Imam Husayn | "The true stingy is that who refrains from greeting." | Tuhaf, short maxims of Imam Husayn, **no. 18** — envelope 01 |

The other ten selected box cards are listed in the table above and are struck off in the same way for their own Masoom.

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

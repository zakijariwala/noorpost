# Sources needed — the shopping list

Everything written so far sits at status `TV` on the citation sheet. **Nothing prints on `TV`.** This file is what turns those rows into `V`.

Ordered by how much it unblocks.

---

## Tier 1 — Fixed editions of the five priority works

**Blocks: all fourteen hadith cards, and every fact panel source credit.**

**Status: 6 of 6 confirmed.** All six translators are fixed in `sourcing-rules.md` — Nahj al-Balagha (Sayed Ali Reza) and al-Kafi (Muhammad Sarwar) confirmed against the physical/PDF title page on 2026-08-12. Publisher and year still need filling for those two, and permission is unchecked for all six — neither blocks hadith-card selection once citation work resumes. Kamal al-Din and both Kitab al-Ghayba works — which would close the Tier 2 occultation gap below — turned up in a third-party aggregator with no translator credited at all, so they don't qualify under this project's own citation rule; treat that gap as still open.

One edition per work, fixed for the project and never mixed. Page and hadith numbers move between editions; a card set against one edition and printed against another cites the wrong place.

| Work | What it unblocks | Common English editions to choose between |
|---|---|---|
| **Tuhaf al-Uqul** — Ibn Shu'ba al-Harrani | First choice for most of the fourteen hadith cards. It is organised by Masoom and it is counsel and conduct, which is exactly the register allowed. | Badr Shahin translation (Ansariyan) is the usual one |
| **Nahj al-Balagha** | Envelope 07's card; Malik al-Ashtar's letter in the companions line | Sayyid Ali Reza (WOFIS), or the recent Tahera Qutbuddin translation |
| **Sahifa Sajjadiyya** | Envelope 09 | William Chittick (Muhammadi Trust) |
| **Risalat al-Huquq** | Envelope 09 — **the letter says "around fifty" entries and that number must become exact** | Usually printed with Sahifa Sajjadiyya; confirm which edition of yours carries it |
| **al-Kafi** — al-Kulayni | Fallback for anything not in the above | Muhammad Sarwar, or the Islamic Seminary edition |
| **Uyun Akhbar al-Rida** — al-Saduq | Envelope 13 | Ali Peiravi (Ansariyan) |

**For each one, record:** translator, publisher, year, and **whether quotation is permitted**. Permission is a Phase 0 question, not a prepress question.

---

## Tier 2 — The sira gap

**Blocks: every letter's citations. All twenty of them — fourteen envelopes plus six companions.**

The five priority works are collections of sayings. **Every letter written is biography and narrative**, and none of it can be cited from Tier 1. This is the largest single hole in the project.

**Status (2026-08-12): two of four now fixed and citable.** Guillaume and Tabari Vol. VIII closed — see `sourcing-rules.md`. al-Irshad and Kamal al-Din remain open.

| Work | What it carries | Needed for | Status |
|---|---|---|---|
| **al-Mufid, Kitab al-Irshad** (trans. I.K.A. Howard) | Biography of the Twelve, in order. The natural companion to the five. | Envelopes 01, 02, 04, 05, 07–14 — the spine of most letters | Open. Both extracts in the repo carry no translator credit on the title page. |
| **Ibn Hisham / Ibn Ishaq, Sirat Rasul Allah** (trans. A. Guillaume) | Pre-revelation Makkah, the Kaaba rebuilding, al-Amin, the Hijra, the Trench, Hudaybiyya | **Envelope 03 in full**, plus Salman and Bilal, plus zines 04, 05, 14 | **Fixed.** Used to verify envelope 03's letter and panel, 2026-08-12. |
| **al-Tabari, History** (SUNY translation, 39 vols) | Rulers, dates, political events, the Abbasid period | The ruler bullet in all fourteen panels; envelopes 04, 08, 11, 13, 14 | **Volume VIII fixed** (Fishbein, trans. — Trench through the conquest of Makkah). Only that volume is in the repo; `tabari--the-history-of-al-tabari.txt` is the SUNY set's index (Vol. XL), not narrative content. |
| **al-Saduq, Kamal al-Din** *(if available)* | The occultation and the four deputies | Envelope 10 | Open — see Tier 1 note above: the aggregator copy has no translator credit and doesn't qualify. |

**You do not need all of Tabari.** Identify the two or three volumes covering 40–260 AH and get those.

---

## Tier 3 — One general world-history reference

**Blocks: fourteen "elsewhere in the world" bullets.**

There is currently no source rule for these at all. They are the bullet children read out unprompted and the easiest thing in the product for a hostile reader to check.

Fix **one** reference for the whole project and cite it the same way every time. A dated world-history timeline or a standard encyclopedia is sufficient — the requirement is consistency, not scholarship.

**Specific claims waiting on it:**

| Envelope | Claim | Risk |
|---|---|---|
| 01 | Council at Constantinople, into 681 CE | Date and characterisation |
| 02 | Horyu-ji burned and rebuilt, c. 670 CE | Date |
| 03 | Grand Canal work under the Sui, from c. 605 CE | Date. **Also the flat negative about stone building in Britain — either source it or cut it.** |
| 04 | Norse settlement of Iceland, traditionally 874 CE | "Traditionally dated" is doing work; check it |
| 05 | Bede finishing his history, c. 731 CE | Date |
| 06 | Sutton Hoo ship burial, c. 625 CE | Dating is approximate — the panel must not imply precision |
| 07 | Maya dated inscriptions at Tikal | **Vaguest of the fourteen. Most likely to need replacing.** |
| 08 | Charlemagne about a year from coronation, 799 CE | Straightforward |
| 09 | Leshan Buddha begun 713 CE | Date and the ninety-year figure |
| 10 | Alfred's translation programme | Date range |
| 11 | Diamond Sutra printed, 868 CE | **Claimed as "oldest dated printed book" — that is a superlative, which rule F2 bans. Source precisely or cut the claim.** |
| 12 | China recovering from the An Lushan rebellion | Dates |
| 13 | Norse raids on Britain and Ireland | Date range |
| 14 | British kingdoms consolidating under raid pressure | **Vague. Likely to need replacing.** |

---

## Tier 4 — Calendar and dates

**Blocks: every fact panel headline, every month stamp, the running order.**

1. **A Hijri–Gregorian converter you trust**, used for all twenty-eight birth and death years. Do not use `AH + 622` — it is right for 1 AH and about eight years wrong by envelope 04. See the table in `citation-sheet.md`.
2. **Your jamaat's calendar**, to settle:
   - ~~Imam Hasan — 7th or 28th Safar~~ **Decided: 28 Safar**, per `TASKS.md`'s open-decisions table — most publicly observed in India. The printed fact panel still carries the differ line; this fixes the production anchor only.
   - ~~The Prophet — 12th or 17th Rabi al-Awwal (birth), 28 Safar or 12 Rabi al-Awwal (death)~~ **Decided: 17 Rabi al-Awwal (birth), 28 Safar (death)** — same basis, same caveat.
   - Laylat al-Qadr — still open
   - The 05 / 11 swap between al-Baqir and al-Hadi — **still open.** Not a community-observance question, so it isn't resolved by the "most prominent in India" instruction that settled the other two. Provisionally kept as-is.
3. **Disputed years to settle from a source, not from memory:** Imam Hasan (49/50/51 AH), Imam al-Baqir (114/117 AH), Imam al-Sajjad (94/95 AH), Sayyida Fatima's birth year, Imam Ali's birth year.

---

## Tier 5 — The named scholar

Not a source, but it gates the same work. **Status: verbal agreement in place (2026-08-12), formal engagement — scope, turnaround, how sign-off is recorded — still pending.** Every row below stays blocking until that's formal; a verbal yes is enough to authorize drafting content that was previously withheld pending scholar involvement (see the Fadak zine), not enough to close a signature requirement.

| Needs a signature | Where |
|---|---|
| **Envelope 06, line by line, including the death line, which they write** | Blocks the entire print run of fourteen |
| All fourteen death lines, reviewed **as one document** | `death-lines.md` |
| Envelope 10's death-line substitute — the one slot carrying belief rather than record | `envelope-10.md` |
| Envelope 11's death line — accounts differ on the caliph; the draft dodges by naming none | `envelope-11.md` |
| Envelope 14 — the Umm al-Fadl conflict | `envelope-14.md` |
| Envelope 07 — how the other man in the market is described, and the birth-in-the-Kaaba marker | `envelope-07.md` |
| Envelope 12 — how far to go on the founders of other schools of law | `envelope-12.md` |
| Silsila numbering, and Sayyida Fatima's position in it | `spec-check.md` |
| Maytham — how the foretelling is characterised | `08-companions/maytham.md` |
| Abu Dharr — the decision to leave the other side unnamed | `08-companions/abu-dharr.md` |
| Ghadir zine, page 4 | `09-zines/ghadir-khumm.md` |
| Fadak zine — whether it is drafted at all | `09-zines/outlines.md` |
| Bilal — the subject matter, not just the facts | `08-companions/bilal.md` |

---

## The claims most likely to fail checking

Ranked. If a source has to be found for only ten things, find these.

| # | Claim | Where | Why it is on this list |
|---|---|---|---|
| 1 | ~~Makkah called him al-Amin before revelation, and had reasons~~ | 03 | **Verified 2026-08-12** — Guillaume, *The Life of Muhammad*, **p. 86**. See `citation-sheet.md`. |
| 2 | ~~Risalat al-Huquq entry count, and the tongue entry quoted exactly~~ | 09 | **Verified 2026-08-12** — 51 entries, tongue entry (3) quoted, p. 9. See `citation-sheet.md`. |
| 3 | ~~Imam al-Rida's four conditions~~ | 13 | **Verified 2026-08-12** — Uyun Akhbar al-Rida vol. 2 (Peiravi), three separate passages. **The letter's original wording is supported and stands.** An earlier pass wrongly rewrote it after reading only one of the three; that was reverted. See `citation-sheet.md`. |
| 4 | Al-Kadhim's four years, consistent across letter, sealed answer and death line | 08 | **Three places give the same number. If the source says otherwise, three edits.** |
| 5 | The shield case: Shurayh's name, ruling, grounds, congratulation | 07 | Everything rests on it being reported with the judge named |
| 6 | The wikala network and the named regions sending funds | 04 | The Case File's sealed answer is built on it |
| 7 | The examination of al-Jawad: questioner, question, answer | 14 | Ditto |
| 8 | The night house search | 11 | Ditto |
| 9 | Named students of al-Sadiq, one by one | 12 | Every name printed must be checkable |
| 10 | The four deputies, names, order, and the seventy-year span | 10 | And the tawqi' must be conduct, not theology |

---

## What is not blocked by any of this

Everything already written can be revised against sources rather than rewritten. **The structure holds regardless of what the sources say** — what changes is numbers, names, and whether a claim is marked traditional.

The exceptions, where a source could kill a whole item:

- **Hira zine, page 5** — that the Kaaba is in the sightline from the cave opening. The zine turns on it entirely.
- **Envelope 05** — his age at Karbala. Three or four; the letter says "about four" and leans on it.
- **Envelope 11** — the Diamond Sutra superlative.
- **Envelope 07** — the Tikal bullet.

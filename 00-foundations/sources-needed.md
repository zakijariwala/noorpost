# Sources needed — the shopping list

Everything written so far sits at status `TV` on the citation sheet. **Nothing prints on `TV`.** This file is what turns those rows into `V`.

Ordered by how much it unblocks.

---

## ✅ Closed 2026-08-24 — the Thaqalayn corpus

**thaqalayn.net is approved as a source of record.** Thirty-two Shia collections, 32,531 records, every one with a named translator, pinned in `00-sources/api/`. See `sourcing-rules.md` for what the approval settles and what it does not.

**What it closes outright:**

| Was blocked | Now |
|---|---|
| **Envelope 10 · Imam al-Mahdi · segment 14** — needed *Kamal al-Din* or a *Kitab al-Ghayba* **with a named translator** | **Closed.** Both Ghayba works are held and credited — al-Nu'mani (trans. Abdullah al-Shahin, 468 records) and al-Tusi (trans. Sayyid Athar Husain S. H. Rizvi, 774). Selection under rule Q3 is the remaining work, not acquisition. |
| **The four companion cards pointing to Imam al-Mahdi** — Muhammad ibn Uthman, Husayn ibn Ruh, al-Samarri, Narjis | **Closed by the same acquisition.** Five items, not one. |
| **Every fixed edition's page-number trap** | Sidestepped for anything cited from this corpus: it has no pages, so `hadith N` is the only thing there is to cite. |

**What it does not close, checked rather than assumed:**

| Still open | What the check found |
|---|---|
| **Envelope 06 · Sayyida Fatima · segment 4** | Searched across all 32,531 records. **Two passages look like her speaking**, both inside al-Kafi narrator chains, neither a conduct maxim of the kind the card needs. This is a smaller gap than before and still a gap. `Musnad Fatima al-Zahra`, `Ilal al-Shara'i` or `Da'a'im al-Islam` remain the acquisitions that would settle it. |
| **Fizza's companion card** | Same blocker, same reason. |
| **Khawla's card** | Unaffected — she points to no Masoom. Still a decision, not a purchase. |
| **Tier 2, the sira gap, in full** | The corpus is hadith. It carries no biography, no sira, no history. `Kitab al-Irshad` with a named translator is untouched as the top acquisition. |
| ~~**The Shurayh shield case** (envelope 07)~~ | **`CUT` 2026-08-24.** Fifth and final negative, against the complete `Kitab al-Irshad`. The letter was rewritten onto Nahj Letter 45 instead of waiting for a source that does not exist. |
| **A Shia history of 40–260 AH**, and a world-history reference | Neither is a hadith collection. No candidate here. |
| **Tuhaf al-Uqul** | **Not served by the API at all.** The rank-1 work stays on the PDF corpus. |

> ⚠ **One regression-shaped finding, and it needs a decision.** The API serves *Risalat al-Huquq* credited to **Chittick — the same translator as the fixed edition** — and it carries **49 records where the fixed edition's English headers run 1–51**, ending on the same right (the people under the protection of Islam). Envelope 09's letter and panel print **fifty-one**, verified 2026-08-12 by counting the fixed edition's own headers, and that count stands. **The finding is that the approved corpus is not always the fuller rendering of a work**, which is the argument against treating it as a replacement for anything.

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

## Tier 1b — the two hadith cards with no possible source

> ⚠ **Repriced 2026-08-14. This tier got four times more valuable and did not move.**
>
> The companions line now carries a hadith card too, and its saying must come from **the Masoom that envelope points home to** (`08-companions/README.md`). So these same two gaps now block **eight items, not two**:
>
> | Gap | Was | Now |
> |---|---|---|
> | **Sayyida Fatima** | box card 06 | box card 06 **+ Fizza** = 2 |
> | **Imam al-Mahdi** | box card 10 | box card 10 **+ Muhammad ibn Uthman, Husayn ibn Ruh, al-Samarri, Narjis** = 5 |
>
> *(The eighth blocked companion, Khawla, fails for a different reason — she points to no Masoom at all. No acquisition fixes her; she needs a decision.)*
>
> **Either acquisition now unblocks four times what it did.** Weigh this tier against the `Kitab al-Irshad` purchase accordingly — Irshad still carries more narrative rows, but the gap below is no longer a two-item problem.

**Blocks: 2 of 14 box hadith cards, and 5 of 39 companion cards. Everything else about those two envelopes is done.**

Twelve of the fourteen cards were selected on 2026-08-12. These two could not be, and the reason is not that the search was shallow — **every fixed edition and every credited text in `00-sources/text/` was checked.** Neither Masoom has a single conduct-register saying available in anything this repo holds:

| Source checked | Result for Sayyida Fatima | Result for Imam al-Mahdi |
|---|---|---|
| Tuhaf al-Uqul (priority work) | **No section at all** — it runs the Prophet, then Ali through al-Askari | **No section at all** |
| Nahj al-Balagha | Imam Ali only | — |
| Sahifa Sajjadiyya / Risalat al-Huquq | Imam al-Sajjad only | — |
| Uyun Akhbar al-Rida | One passing mention of her, not a saying by her | — |
| al-Kafi | The held copy is Vol. 1 (*Usul*) — Intelligence, Knowledge, Tawhid. No Fatima chapter, and the register is theological, not conduct | Same |

| Nuqoosh-e-Ismat (named translator) | Narrative only, no quoted sayings by her | Carries one tawqi' — *"It is your duty to issue verdicts and our job to verify them"* — which is **religious authority, banned by rule Q3** |
| The Fourteen Infallibles | Her material is the Fadak dispute and her death — contested ground envelope 06 exists to avoid, and the wrong register | — |
| Qarashi, *Life of Imam Mahdi* | — | Qur'anic verses and other people's questions; translator credited only as a bureau |

**What would unblock each — one acquisition apiece:**

| Envelope | Needs | Note |
|---|---|---|
| **06 · Sayyida Fatima · segment 4** | Any credited English edition carrying her short sayings — the *Musnad Fatima al-Zahra* material, or al-Saduq's *Ilal al-Shara'i* / *Ma'ani al-Akhbar*, or Da'a'im al-Islam | Her best-known conduct saying — praying for the neighbour before the household — sits in these. It is thematically ideal for envelope 06, which is about a private devotional practice, and would turn it outward. **Do not print it from memory; it has to come off a page.** |
| **10 · Imam al-Mahdi · segment 14** | *Kamal al-Din* or either *Kitab al-Ghayba*, **with a named translator** | Already flagged in Tier 2 as the occultation gap. The aggregator copies are credited `en.unknown` and fail this project's own rule. Note the extra constraint: most surviving tawqi'at are about authority or the occultation itself, so a conduct-only one is genuinely scarce — budget time to find it, not just to buy the book. |

**Why this is not being worked around.** A saying recalled from memory and typeset would look exactly like the other twelve and be indistinguishable on the card — and the whole citation apparatus exists to stop precisely that. This session already contains one instance of acting on an incomplete reading of a source (envelope 13, reverted). Two cards waiting on one purchase each is the cheaper outcome.

---

## ✅ Partly closed 2026-08-24 — *The Message* was in the library all along

**`SRC-MSG-001` — Subhani, *The Message: The Life of the Holy Prophet of Islam*.** Complete, 63 chapters, translated in-house by **Islamic Seminary Publications, Karachi, 1984** (ISBN 0941724387). It was sitting unused because the title page credits no individual translator, and the credit rule was being read as *name a person*. That reading is now fixed — see `sourcing-rules.md` "Who counts as a translator".

**What it closes:** the Prophet's own narrative material. **Three of envelope 03's four rows close outright**, and the fourth half-closes — see `citation-sheet.md`. It is also the natural source for the eight Prophet-facing companions.

**What it does not close:** it is a sira *of the Prophet*. **It carries nothing for the other thirteen Masoomeen**, so `Kitab al-Irshad` with an attributable translator remains the top acquisition and Tier 2 below stands for envelopes 01, 02, 04–14 and their companions.

## Tier 2 — The sira gap

**Blocks: every letter's citations. All twenty of them — fourteen envelopes plus six companions.**

The five priority works are collections of sayings. **Every letter written is biography and narrative**, and none of it can be cited from Tier 1. This is the largest single hole in the project.

**Status (2026-08-12): fully open. Nothing here is fixed.** Guillaume and Tabari Vol. VIII briefly closed part of it and were **removed as Sunni works** under the hard rule in `sourcing-rules.md`. **This gap must be closed with Shia sources only, and `al-Irshad` is now the project's most valuable single acquisition.**

| Work | What it carries | Needed for | Status |
|---|---|---|---|
| **al-Mufid, Kitab al-Irshad** (trans. I.K.A. Howard) | Biography of the Twelve, in order. The natural companion to the five. | Envelopes 01, 02, 04, 05, 07–14 — the spine of most letters, **and now envelope 03 as well** | **Open, and now the top acquisition in the project.** Both extracts in the repo carry no translator credit on the title page. |
| **al-Saduq, Kamal al-Din** *(if available)* | The occultation and the four deputies | Envelope 10 | Open — see Tier 1 note above: the aggregator copy has no translator credit and doesn't qualify. |

**The ruler bullet in all fourteen panels now has no source at all.** It was going to come from al-Tabari. A Shia history or biographical work has to carry it instead — al-Irshad covers some of it, and the Qarashi lives already held may cover more, but neither has been fixed as an edition.

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
| 1 | **Makkah called him al-Amin before revelation, and had reasons** | 03 | ⛔ **Was verified, reopened 2026-08-12, half-closed 2026-08-14.** Checked originally against Guillaume's Ibn Ishaq, removed as a Sunni work. **A permitted Shia passage carrying both halves of the claim has now been found in the repo** — *The Fourteen Infallibles* (Yasin T. Al-Jibouri), "Holy Prophet", §Year of the Elephant. **What blocks it is no longer the search, it is the edition:** that work is an aggregator PDF with no publisher or year and is not one of the six fixed editions. **This row now closes with a decision rather than a purchase** — see `citation-sheet.md`. |
| 2 | ~~Risalat al-Huquq entry count, and the tongue entry quoted exactly~~ | 09 | **Verified 2026-08-12** — 51 entries, tongue entry (3) quoted, p. 9. See `citation-sheet.md`. |
| 3 | ~~Imam al-Rida's four conditions~~ | 13 | **Verified 2026-08-12** — Uyun Akhbar al-Rida vol. 2 (Peiravi), three separate passages. **The letter's original wording is supported and stands.** An earlier pass wrongly rewrote it after reading only one of the three; that was reverted. See `citation-sheet.md`. |
| 4 | ~~Al-Kadhim's four years, consistent across letter, sealed answer and death line~~ | 08 | **Worked 2026-08-14 against Qarashi (trans. Jasim al-Rasheed, Ansariyan).** The three places agree and the number holds as *about* four years — arrest Shawwal 20, 179 AH, death 183 — but it is `TRAD`, not `V`: it is arithmetic across two dates, not a statement in the source. **Two things came out of it.** The letter said *"in a prison in Baghdad"* for the whole span when roughly the first year was Basra — corrected, and it had been contradicting its own fact panel. And **the death date is now `CONT`**: §22 of the held work prints 173 AH, which is impossible against its own arrest date. See `citation-sheet.md`. |
| 5 | The shield case: Shurayh's name, ruling, grounds, congratulation | 07 | Everything rests on it being reported with the judge named. **Confirmed negative 2026-08-14** — searched across the whole of `00-sources/text/`, not one work: both `al-Irshad` extracts still credit no translator, Nahj al-Balagha carries Shurayh only in Letter 3 (the house purchase, a different episode), and neither Fourteen volume has the case. **Still blocked on `al-Irshad` with a named translator.** |
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

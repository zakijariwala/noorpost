# Sourcing rules

---

## Priority order

Work down. A saying available in a higher work is cited from there.

| Rank | Work | What it is good for here |
|---|---|---|
| 1 | **Tuhaf al-Uqul** (Ibn Shu'ba al-Harrani) | First choice by design. It is a collection of counsel and conduct, organised by Masoom, which is exactly the register this product needs. Most hadith cards should come from here. |
| 2 | **Nahj al-Balagha** | Envelope 07, and letters and sayings elsewhere. Letter 31 to Imam Hasan is the richest single source in the project for child-facing conduct material. |
| 3 | **Sahifa Sajjadiyya** | Envelope 09. Also the natural home for Risalat al-Huquq, which travels with it in most editions. |
| 4 | **al-Kafi** (al-Kulayni) | The fallback for biography and for sayings not in 1–3. Large, well indexed, well translated. |
| 5 | **Uyun Akhbar al-Rida** (al-Saduq) | Envelope 13 primarily. |

**Bihar al-Anwar is never the citation of record.** It may be used to find where something sits, and then the earlier work is cited. If a claim exists only in Bihar, it is treated as traditional and marked as such, or it is cut.

---

## Subject limits

**Ethics and conduct only.**

| Allowed | Not allowed |
|---|---|
| How to treat a neighbour, a parent, an enemy, a servant, an animal | Anything jurisprudential — prayer rulings, fasting rulings, khums, taharah |
| Honesty, patience under provocation, keeping a promise, returning a trust | Anything theological — the nature of the imamate, raj'a, bada', the fine structure of occultation |
| What is owed to whom | Anything contested between schools of law |
| Documented events and their circumstances | Anything requiring a marja' to adjudicate |

The line to hold: **the product never puts the parent in a position of teaching a ruling.** If a child asks a ruling question, the envelope has done its job by prompting it and the parent takes it to their own family and their own scholar.

Where a session card risks drifting into a ruling — envelope 06 and the tasbih is the obvious one — the card asks about the practice, not about its status.

---

## Translations

Published translations only. No in-house rendering of Arabic, ever, even where a published one reads poorly.

| Rule | Why |
|---|---|
| Name the translator, the publisher and the year | It is a credit and it is a citation. Both are owed. |
| One edition per work, fixed for the project | Page numbers move between editions. Pick one, record it below, never mix. |
| Quote exactly, or don't quote | Trimming a saying to fit a card is rewriting it. Choose a shorter saying instead. |
| Ellipsis is allowed, paraphrase is not | `…` inside a quotation is honest. Smoothing is not. |
| Check permissions before print | Some translations are freely licensed, some are not. Establish this per work **before Gate 3**, not at prepress. |

### Editions fixed for this project

| Work | Translator | Publisher | Year | Permission checked |
|---|---|---|---|---|
| Tuhaf al-Uqul | Badr Shahin | Ansariyan Publications, Qum | *to fix* | ☐ |
| Nahj al-Balagha | *candidate: Sayed Ali Reza* † | *to fix* | *to fix* | ☐ |
| Sahifa Sajjadiyya | William C. Chittick | Muhammadi Trust of Great Britain and Northern Ireland | 1988 (foreword dated 17 Jan 1988) | ☐ |
| al-Kafi | *candidate: Muhammad Sarwar* † | Islamic Seminary Inc. (unconfirmed) | *to fix* | ☐ |
| Uyun Akhbar al-Rida | Dr. Ali Peiravi | Ansariyan Publications, Qum | *to fix* | ☐ |
| Risalat al-Huquq | William C. Chittick | Muhammadi Trust of Great Britain and Northern Ireland (bound with Sahifa Sajjadiyya) | 1988 | ☐ |

Four rows read straight off the title page already sitting in `00-sources/text/` — nobody had transcribed them. **Two rows are still open**, marked *candidate* † — the extracted text for these two carries no translator credit at all (page likely lost in scan/OCR), and al-islam.org itself returns a Cloudflare block to any non-browser fetch, so it can't be confirmed by script. The candidate names come from cross-referencing [ThaqalaynData](https://github.com/narmafraz/ThaqalaynData), an aggregator that packages the same named, human translations in hadith-numbered JSON:
- Nahj al-Balagha → credited there to `en.sayed-ali-raza`
- al-Kafi → credited there to `en.sarwar` (Muhammad Sarwar) or `en.hubeali` (HubeAli.com); Sarwar is favoured because the archive.org item description says "all eight volumes," matching the Islamic Seminary/Sarwar edition

**Do not promote either candidate to `V` without opening the physical or PDF title page and reading the name.** ThaqalaynData is a third party's aggregation, not the edition itself.

**A caution on ThaqalaynData specifically:** every hadith record in that dataset also carries an unlabelled `ai` block — LLM-generated narrator-identity guesses (with `"identity_confidence": "ambiguous"|"likely"|"definite"` tags), summaries, and machine translations into languages beyond the credited human one. It sits inside the same JSON object as the real citation. **Only ever use the field under `translations["<lang>.<named-translator>"]`. Never cite the `ai` block — it is unverified by definition, exactly what `TV` exists to stop.** Its `kamal-al-din`, `kitab-al-ghayba-numani`, and `kitab-al-ghayba-tusi` entries — which would otherwise close the envelope 10 occultation gap in `sources-needed.md` Tier 2 — are credited only to `en.unknown`. No translator name means no citation under this project's own rule above. Do not use them.

**Fill this table before writing a single hadith card.** A card written against one edition and printed against another is a citation that points at the wrong page, which is worse than no citation.

---

## Citation format

Fact panel foot:

> [Work], [book/section] [number]. Translated by [translator], [publisher] [year].

Hadith card reverse:

> [Work] [number] · trans. [translator]

Never cite without a number. A citation without a number is decoration.

---

## Facts that survive checking

The PRD's list, restated as what to go looking for:

| Use | Do not use |
|---|---|
| The ruler of the day, named, with dynasty | Follower counts |
| The length of the imamate, and from what age | "People influenced" |
| Named students, and where they went | Population figures |
| Attributed compilations | "The most X in history" |
| What was happening elsewhere in the world that year | Anything with an implied census |
| Documented places, and what stands there now | Anything that needs "roughly" to survive |

**The test: could a hostile reader check this in an afternoon and find it holds?** If the answer needs a caveat, the claim is either marked traditional or it is cut.

---

## Handling accounts that are loved but undocumented

Three moves, in order of preference:

1. **Use it and mark it.** Wording in `standard-lines.md`. The marker goes in the child's copy, not only the parent's.
2. **Move it to the parent's copy.** Where the account is beautiful but carries a claim the envelope should not assert to a child.
3. **Cut it.** Where the account only works if asserted flatly.

**Never quietly launder a traditional account into a documented register by dropping the qualifier.** The credibility of the whole product rests on the parent finding, when they check, that the envelope told them which was which.

---

## Where communities differ

Do not adjudicate. Ever. The standard line hands it to the parent, verbatim, per `standard-lines.md`.

This applies to dates, to observances, and to the events at the centre of Sunni–Shia dispute. **Envelope 06 does not go on that ground at all** — the letter is about the tasbih, and the fact panel is signed line by line by a named scholar.

---

## Working method

For every claim that reaches print:

1. Find it in the highest-ranked work that carries it.
2. Record work, number, translator, edition on `citation-sheet.md`, one row.
3. Note whether it is documented or traditional.
4. Note whether it is contested, and by whom.
5. Only then write the line that uses it.

**Rows are written before copy, not after.** Writing first and sourcing afterwards is how a nice sentence survives that nothing supports.

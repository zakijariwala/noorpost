# Handover

Everything needed to pick this up cold, on another machine or in a new session.

---

## Get set up

```bash
git clone https://github.com/zakijariwala/noorpost.git
cd noorpost
```

That is enough to start work. The searchable source text is in the repo.

Optional, only if you need the original PDFs — to read properly, or to check a translator's name on a title page:

```bash
curl -L -o sources.zip https://github.com/zakijariwala/noorpost/releases/download/sources-v1/noorpost-sources.zip
unzip sources.zip -d 00-sources
```

## What is where

| Path | What it is |
|---|---|
| `README.md` | Layout and status |
| `TASKS.md` | Ten phases, gated. Checkboxes are current. |
| `00-foundations/` | The rules. Everything else is checked against these. |
| `00-sources/text/` | 19 source texts as plain text, page-numbered. **Tracked.** |
| `00-sources/*.pdf` | The PDFs. **Not tracked** — from the release. |
| `01-pilot/envelope-03/` | Envelope 03, split across four files |
| `03-content/` | Envelopes 01, 02, 04–14, one file each, plus `spec-check.md` |
| `08-companions/` | The six companion envelopes |
| `09-zines/` | Zine template, two written in full, thirteen outlined |
| `docs/` | The published site. **Generated — never edit by hand.** |
| `tools/` | Three scripts |

## The three scripts

```bash
python tools/build_site.py       # rebuild docs/ from the markdown
python tools/fetch_sources.py    # find more sources (--download to fetch)
python tools/extract_text.py     # PDFs -> 00-sources/text/ (only if you re-download)
```

`build_site.py` strips every editorial note — the new-thing lines, blocking warnings, item specs, scholar flags, open questions. **The site shows only what a family receives.** If you add a new kind of internal note, check it does not leak: rebuild, then grep `docs/*.html` for it.

Site is at **https://zakijariwala.github.io/noorpost/** and serves from `main` `/docs`. Push and it updates.

---

## State

| Phase | Where it stands |
|---|---|
| 0 Foundations | Written. Blocked on fixed editions and a scholar. |
| 1 Pilot | Envelope 03 written. Not printed, not timed, not reviewed. |
| 2 Channel test | Not started. Needs a printed envelope. |
| 3 Content | **All fourteen letters, fact panels and session cards written.** Counts measured. Hadith cards blocked. |
| 4 Art | Nothing drawn. Every item is specified. |
| 5–7 | Not started. Gated behind the print run. |
| 8 Companions | Six written. |
| 9 Zines | Template plus two full, thirteen outlined. |

**Every factual claim in every fact panel is unverified.** They are marked `TV` on the citation sheet. Nothing prints on `TV`.

---

## The next job: citation work

This is the whole critical path. It turns `TV` rows into `V` rows.

### How to do it without burning tokens

**Never open a PDF.** Reading one costs about 200,000 tokens. The extracted text costs about 200 per hit.

```bash
grep -rn -i -C4 "shurayh" 00-sources/text/
grep -rn "three hundred" 00-sources/text/irshad--*.txt
```

Every page break in those files is a line reading `[[p 137]]`. **Read up from a hit to the nearest one — that is the page number for the citation.**

### The loop

1. Take one row from `00-foundations/citation-sheet.md`.
2. Grep for it.
3. Record work, page or hadith number, translator, edition on the row.
4. Set the status: `V` verified, `TRAD` traditional, `CONT` contested, `CUT` did not hold.
5. If it did not hold, fix the line in the envelope file — do not leave a claim standing on a `CUT` row.

**One row at a time. Ten rows is a good session.** The unit is the row, not the envelope and not the book.

### Where to start

`00-foundations/sources-needed.md` ranks the ten claims most likely to fail. Work down that list. The top three:

1. Makkah called him al-Amin before revelation — envelope 03, and it is the adult's new thing
2. Risalat al-Huquq entry count, and the tongue entry quoted exactly — envelope 09
3. Imam al-Rida's four conditions — envelope 13

### Fill this in first

The fixed-editions table in `00-foundations/sourcing-rules.md` is **empty**, and it blocks all fourteen hadith cards. For each work: translator, publisher, year, permission checked. A card set against one edition and printed against another cites the wrong page.

---

## What is still missing

**Sources.** `00-sources/text/` has Tuhaf al-Uqul, both parts of Nahj al-Balagha, Sahifa Sajjadiyya, Risalat al-Huquq, both volumes of Uyun Akhbar al-Rida, al-Kafi, two copies of Kitab al-Irshad, two of Guillaume's Sira, Subhani's *The Message*, two Qarashi lives, two Tabari volumes, and two on the Fourteen.

Not there:

| Missing | Blocks |
|---|---|
| Kamal al-Din / Jassim Hussain on the occultation | Envelope 10 — the four deputies |
| Tabari vol 19 (Karbala) and the Abbasid volumes | The ruler bullet in several panels |
| Four of the six Qarashi lives | Envelopes 05, 07, 11, 13 |
| **A world-history reference** | All fourteen "elsewhere in the world" bullets |

Both *Timetables of History* downloads are DRM-locked and will not extract. **A different world-history reference is needed** — that gap is unfixed.

`python tools/fetch_sources.py --tier 2` prints where to look. al-Islam.org blocks scripts, so those links open in a browser.

**A named scholar.** Fourteen items need a signature. `sources-needed.md` lists them. **Envelope 06 blocks the print run of all fourteen** — its death line is written by the scholar, not by us.

---

## Decisions still open

None of these need a source. They need you.

| Decision | What it touches |
|---|---|
| **Swap envelopes 05 and 11?** | Every item on both pages is keyed to the month |
| Silsila numbering — the Prophet at 13 or 1, and where Sayyida Fatima sits | All fourteen hadith cards |
| Zaynab holds two of fourteen women's slots (02, 05) | The one repeat in a feature sold on fourteen |
| Umm al-Fadl in envelope 14 — she holds the woman slot and the accounts implicate her in his death | Envelope 14's panel |
| Imam Hasan — 7th or 28th Safar | Envelope 02, and its stamp |
| The Prophet — 12th or 17th Rabi al-Awwal | Envelope 03, and its stamp |
| Whether Fadak gets a zine at all | Zine 11 |
| The calendar ring punch position | All fourteen event prints. **Fix it before anything is drawn.** |

---

## Rules that are easy to break

- **The segment number prints on the hadith card. The envelope number never does.** The silsila runs in historical order, the envelopes in calendar order.
- **No hadith card and no event print in the companions line, ever.** Those two carry the silsila and the ring. Break this and the box stops being the only way to complete anything.
- **The death goes in one fixed place** — last line of the fact panel, nowhere else. Fact and actor, no method.
- **One new thing for the adult, every envelope.** A fact, not a reflection.
- **Every activity needs two roles.** Anything one person can do alone fails the brief.
- **No subscription sells before all fourteen are printed.** This is what makes monthly a posting job.

Full set in `00-foundations/editorial-rulebook.md`. Per-envelope sign-off in `00-foundations/checklist.md`.

---

## Things worth knowing before you touch anything

**Text freezes at Gate 3.** All fourteen print as one run. An error found after that costs the run — which is why the citation work happens now and not after the art.

**The repo is public**, and so are the source texts in it and the zip on the release page. Those are translations whose licences have not been checked.

**`docs/` is generated.** Edit the markdown, run the build, commit both.

**The letters are measured, not estimated.** `03-content/spec-check.md` carries the counts and the command that produced them. Re-run it after editing any letter — 330 to 370 words, 6 to 9 child lines, none of them 15 words.

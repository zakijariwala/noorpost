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
| 0 Foundations | Written, including the design system (`00-foundations/design-system.md`). Blocked on two unconfirmed translator credits and a scholar. |
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

Every page break in those files is a line reading `[[p 137]]`. Read up from a hit to the nearest one — but **that number is the PDF sheet, not necessarily the book's printed page.** Two traps, both of which have already produced a wrong citation in this repo:

**Trap 1 — two-column scans.** Some files are two-page-per-sheet scans whose columns got merged onto single lines. There, one `[[p N]]` covers *two* book pages and the number is off by twenty or more. Check before citing:

```bash
# >25% means two-column: the [[p N]] markers are sheet numbers, not book pages
awk 'BEGIN{g=0} /\S {10,}\S/{g++} END{print int(g*100/NR)"%"}' 00-sources/text/FILE.txt
```

**Known two-column files — never cite their `[[p N]]` directly:**

| File | Two-column | What to do |
|---|---|---|
| `sira-guillaume--guillaumeathelifeofmuhammad.txt` | 38% | Read the running header on the line *after* the marker — it carries the real book pages (e.g. `[[p 67]]` → pages 86 and 87). Left column = even page, right = odd. |
| `kafi--alkafi-201601.txt` | 27% | **Tier 1 priority work — this trap is loaded and unused.** Same method. |
| `tabari--the-history-of-al-tabari.txt` | 41% | Index volume only, no narrative. Not citable at all. |

**Trap 2 — web-PDF pagination.** The al-Islam.org sources (Risalat al-Huquq, Sahifa Sajjadiyya, Uyun, Tuhaf) are generated PDFs. Their page numbers are artifacts of that generation and do **not** match the printed Ansariyan / Muhammadi Trust editions fixed in `sourcing-rules.md`. For these, **cite the work's own internal numbering** — entry number, hadith number, chapter-and-report — which is stable across editions. A page number there is decoration; the entry number is the citation.

### The loop

1. Take one row from `00-foundations/citation-sheet.md`.
2. Grep for it — **and grep the whole work, not just the first hit.** A passage phrased differently is not disproof. This is exactly how envelope 13's correct line got wrongly cut and then restored.
3. Check the file against Trap 1 and Trap 2 above before writing any page number.
4. Record work, internal number (preferred) or verified book page, translator, edition on the row.
5. Set the status: `V` verified, `TRAD` traditional, `CONT` contested, `CUT` did not hold.
6. If it did not hold, fix the line in the envelope file — do not leave a claim standing on a `CUT` row. **Before cutting, confirm the claim is absent from the whole work, not just from the passage you happened to find.**

**One row at a time. Ten rows is a good session.** The unit is the row, not the envelope and not the book.

### Where to start

`00-foundations/sources-needed.md` ranks the ten claims most likely to fail. Work down that list. **The top three are now verified (2026-08-12):**

1. ~~Makkah called him al-Amin before revelation~~ — envelope 03. Guillaume, *The Life of Muhammad*, **p. 86** — now a fixed edition, closing the sira gap for this envelope. See `sourcing-rules.md` and `citation-sheet.md`.
2. ~~Risalat al-Huquq entry count, and the tongue entry quoted exactly~~ — envelope 09. **51 entries**, not "around fifty" — letter and panel corrected. Tongue entry is **entry 3**, quoted in full on `citation-sheet.md`. *(Cite the entry number, not a page — this is a web-generated PDF; see Trap 2 above.)*
3. ~~Imam al-Rida's four conditions~~ — envelope 13. Uyun Akhbar al-Rida vol. 2 (Peiravi) carries them in **three** places. **The draft wording was already correct and stands** — appoint nobody, dismiss nobody, change nothing in place, no opinion unless asked. An earlier pass read only one of the three passages, wrongly declared the draft unsupported, and rewrote the printed line; that has been reverted.

Next down the list: #4, al-Kadhim's four years (envelope 08) — al-Kafi or Uyun Akhbar al-Rida are the likely works; #5, the Shurayh shield case (envelope 07) — needs al-Irshad, which is still an open edition (no translator credit on the title page yet, see `sourcing-rules.md`).

### Fill this in first

The fixed-editions table in `00-foundations/sourcing-rules.md` is **now filled — all six translators confirmed** (2026-08-12). Publisher and year still missing for two (Nahj al-Balagha, al-Kafi), and permission is unchecked for all six. A card set against one edition and printed against another cites the wrong page.

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

**A named scholar.** Fourteen items need a signature. `sources-needed.md` lists them. **Envelope 06 blocks the print run of all fourteen** — its death line is written by the scholar, not by us. **Verbal agreement is in place (2026-08-12)** — enough to authorize drafting previously-withheld content (the Fadak zine), not enough to close any signature requirement. Formal scope/turnaround/sign-off recording still needed.

---

## Decisions still open

None of these need a source. They need you.

| Decision | What it touches |
|---|---|
| **Swap envelopes 05 and 11?** | Every item on both pages is keyed to the month |
| Silsila numbering — the Prophet at 13 or 1, and where Sayyida Fatima sits | All fourteen hadith cards |
| Zaynab holds two of fourteen women's slots (02, 05) | The one repeat in a feature sold on fourteen |
| Umm al-Fadl in envelope 14 — she holds the woman slot and the accounts implicate her in his death | Envelope 14's panel |
| ~~Imam Hasan — 7th or 28th Safar~~ | **Decided: 28 Safar** (2026-08-12) — most publicly observed in India. Production anchor only; the differ line still prints in the fact panel. |
| ~~The Prophet — 12th or 17th Rabi al-Awwal~~ | **Decided: 17 Rabi al-Awwal** (birth), **28 Safar** (death) — same basis, same caveat. |
| ~~Whether Fadak gets a zine at all~~ | **Decided: yes**, on verbal scholar agreement (2026-08-12). Drafted with the outline's own cautions (factual land-dispute account, not polemic) still in force. |
| ~~The calendar ring punch position~~ | Fixed in `00-foundations/design-system.md` §6 (6mm hole, 12mm from edge, 25mm book ring). Still needs a physical proof before Phase 4 art commits to it. |

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

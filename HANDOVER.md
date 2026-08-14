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
| `00-sources/text/` | 15 source texts as plain text, page-numbered. **Tracked. Shia sources only** — see the hard rule in `sourcing-rules.md`. |
| `00-sources/*.pdf`, `00-sources/originals/` | The PDFs. **Not tracked** — from the release. Immutable. |
| `00-sources/metadata/` | `sources.yaml` (editions, hashes, pagination), `rejected.yaml` (the denylist), `claims.yaml`, `citations.yaml`. **Tracked.** |
| `00-sources/source.db` | SQLite + FTS5 over every page and passage. **Not tracked — rebuild it.** |
| `01-pilot/envelope-03/` | Envelope 03, split across four files |
| `03-content/` | Envelopes 01, 02, 04–14, one file each, plus `spec-check.md` |
| `08-companions/` | The six companion envelopes |
| `09-zines/` | Zine template, two written in full, thirteen outlined |
| `docs/` | The published site. **Generated — never edit by hand.** |
| `tools/` | The build scripts, plus `sourcelib/` — the source pipeline |

## The scripts

```bash
python tools/build_site.py             # rebuild docs/ from the markdown
python tools/build_print_templates.py  # 08-companions/*.md -> four print templates each
python tools/fetch_sources.py          # find more sources (--download to fetch)
python tools/extract_text.py           # PDFs -> 00-sources/text/ (only if you re-download)
```

`build_print_templates.py` also **enforces the companions line's protective rule**, on every build and not only on `--check`: no silsila segment number in a companion template, no event print, and an Items table of exactly the five fixed items. It exits non-zero rather than writing a template that breaks the separation between the two chains.

And the source pipeline, added 2026-08-14. `pip install -r requirements.txt` first
(PyYAML, and nothing else). Full account in `00-sources/README.md`.

```bash
python tools/build_source_corpus.py     # text/ -> pages -> md/ -> source.db + FTS5
python tools/source_search.py "Shurayh" # find evidence, with edition and page
python tools/page_image.py --source SRC-NHB-002 --page 35   # look at the original page
python tools/source_audit.py --write    # what is fixed, missing, TV, V, unverified
python -m unittest discover -s tests    # 40 tests
```

`source_search.py` searches `00-sources/` and nothing else, so a draft can never
become evidence for itself. It reports which editions' page numbers may be cited
— today, none of them can, which is why every citation goes by the work's own
internal numbering.

`build_site.py` strips every editorial note — the new-thing lines, blocking warnings, scholar flags, open questions. **The envelope, companion and zine pages show only what a family receives.** If you add a new kind of internal note, check it does not leak: rebuild, then grep `docs/*.html` for it.

**One deliberate exception: the card views** (`envelope-NN-cards.html`). These exist to show, internally, every physical item an envelope will hold and which of them nothing has been allocated to yet — so they *do* publish item specs and a written/placeholder status for each item. They are linked from the index and from each envelope page, carry `noindex`, and sit behind the same "draft for review, not for circulation" footer as the rest of the site, alongside the print proofs and art-prompt packs already published for internal access.

Even there, two things are still stripped or refused:

- **Internal cross-references** — `strip_internal()` removes any `` `something.md` `` reference from published spec text, so working notes in an Items table never reach the page.
- **Nothing is rendered as a quotation.** Placeholder hadith cards state that no saying has been chosen; they never render invented filler inside quote marks or attribute it to a named figure. `sourcing-rules.md` says quote exactly or don't quote, and a screenshot of one card loses whatever label surrounded it.

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
| 8 Companions | Thirty-nine written. **Restructured 2026-08-14 — see "The 2026-08-14 decisions" below. The structural sweep is done; 0 of 39 sayings selected.** |
| 9 Zines | Template plus two full, thirteen outlined. |

**Every factual claim in every fact panel is unverified.** They are marked `TV` on the citation sheet. Nothing prints on `TV`.

---

## The 2026-08-14 decisions

**Four decisions.** Recorded here because they change rules that other files state as settled, and because a reader who missed the session would otherwise trust the old wording. **When they were taken, nothing had been built, selected or written against any of them.**

**The structural sweep they needed is now done — same day, second session.** All thirty-nine entry files read *Five items* and carry a hadith card row naming the Masoom and the quality the saying has to match; the replacement rule — no event print, no silsila segment number — has replaced the old one in every file; `build_print_templates.py` emits a fourth template per entry and asserts the narrower rule on every build; and thirty-nine rows are written on `citation-sheet.md` for selections to land in one at a time.

**The selection work is still not started, and two things gate it.** 0 of 39 sayings chosen, and every chain number still reads `nn` because **the ordering scheme is undecided** — see "Decisions still open" below. Templates show the slot empty rather than filled with plausible-looking text, which is both the honest state and the rule: quote exactly or don't quote.

**1. The product is a first edition of two parts.** The Fourteen are the monthly subscription box. **Everyone Else is one envelope per individual** — all thirty-nine — bought singly, as a checkout add-on, or in a pack. Together they are the **first edition**, a closed set. **Second edition TBD**, and it is the only place new personalities go from now on.

**2. The companions line carries a hadith card.** The rule forbidding it — stated in `08-companions/README.md` as *"not a guideline"*, and as rulebook C5 — **is overturned.** The event-print half stands: the calendar ring stays box-only.

**3. The card is numbered on its own chain, `FIRST EDITION nn/39`** — never a silsila segment. **The cost was accepted, not overlooked: the box is no longer the only way to complete a collection.** A child can complete a thirty-nine-card chain without ever holding a subscription. The mitigation, and the thing that is now load-bearing, is that **the two chains stay visibly separate** — fourteen silsila segments in the box, thirty-nine first-edition cards outside it, and no card readable as belonging to the other set.

**4. The saying is of the Masoom the envelope points home to**, theme-matched to that person, never a repeat of that Masoom's box card.

### What decision 4 immediately blocked, and why it matters

**Six of the thirty-nine cannot be assigned a card**, and five fail on gaps the project already knew about:

| Blocked | Points to | Same blocker as |
|---|---|---|
| Fizza | Sayyida Fatima | **Box card 06** |
| Muhammad ibn Uthman, Husayn ibn Ruh, al-Samarri, Narjis | Imam al-Mahdi | **Box card 10** |
| Khawla bint al-Azwar | nobody — the one entry pointing to no Masoom | *(nothing; needs its own decision)* |

**This is the finding worth carrying forward.** Acquiring a fixed edition carrying Sayyida Fatima, or one carrying the tawqi'at with a named translator, **now unblocks eight items instead of two.** That is a real change to the priority order in `sources-needed.md`, and it was not true yesterday.

### Also learned, and it blocks the tooling

**There is no Python on the Windows machine this repo sits on.** `build_site.py`, `build_print_templates.py` and the other two **cannot be run there.** Install Python, or do tooling work elsewhere.

> **Amended 2026-08-14, second session — "read the markdown, not the published site" no longer applies to `docs/`.**
>
> It was sound advice when written, and it was checked before being retired. `docs/` had gone four commits without a rebuild, so it was rebuilt: **zero diff, on all 85 pages**, and `build_print_templates.py` reported zero files differing from disk. Everything those commits changed was either in a file the site does not publish or in material `build_site.py` strips — the Guillaume citation footer in `envelope-03/fact-panel.md` was a `<sub>` line, and `docs/envelope-03.html` carries no `<sub>` tags at all. The published site was also checked for the removed Sunni sources and is clean.
>
> **`docs/` is now rebuilt automatically.** `.github/workflows/site.yml` runs the source-metadata validation and the test suite, rebuilds `docs/` and commits it on every push to `main`. A push from a machine with no Python still updates the site, so the generated pages no longer fall behind an edit.
>
> Both scripts remain idempotent and safe to re-run by hand, and `build_print_templates.py --check` still reports drift without writing. `04-art/print/` is **not** in the workflow — it is content, not a published view, so it stays a deliberate act.
>
> What no automation can do is publish what has not been written. **`docs/status.html` measures that gap on every build** — sayings selected, illustrations that exist, claims still `TV` — from the repository itself, so the difference between "built" and "done" is visible without asking anyone.

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

**Known two-column file:** `kafi--alkafi-201601.txt` (27%) — a Tier 1 priority work, not yet cited from, so this trap is loaded and waiting. Read the running header on the line *after* the marker for the real book page (left column = even, right = odd). Run the check on every source acquired from here on.

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

`00-foundations/sources-needed.md` ranks the ten claims most likely to fail. Work down that list. **Two of the top three are verified; the first was reverted by the Shia-sources-only rule:**

1. **Makkah called him al-Amin before revelation** — envelope 03. ⛔ **Was verified, reopened 2026-08-12, half-closed 2026-08-14.** It was checked against Guillaume's Ibn Ishaq, a Sunni work removed under the Shia-sources-only rule in `sourcing-rules.md`. **A permitted Shia passage carrying the claim and its reasons has now been found in the repo** — *The Fourteen Infallibles* (Yasin T. Al-Jibouri), §*Year of the Elephant*, quoted on `citation-sheet.md`. **The blocker changed kind: it is no longer a search, it is that the work is not a fixed edition** (aggregator PDF, no publisher, no year). **This row now closes with a decision, not a purchase.** The other three envelope 03 rows — the Ka'ba rebuilding, the dispute, the cloak — were searched in the same pass and are carried by nothing held; they still need `al-Irshad`.
2. ~~Risalat al-Huquq entry count, and the tongue entry quoted exactly~~ — envelope 09. **51 entries**, not "around fifty" — letter and panel corrected. Tongue entry is **entry 3**, quoted in full on `citation-sheet.md`. *(Cite the entry number, not a page — this is a web-generated PDF; see Trap 2 above.)*
3. ~~Imam al-Rida's four conditions~~ — envelope 13. Uyun Akhbar al-Rida vol. 2 (Peiravi) carries them in **three** places. **The draft wording was already correct and stands** — appoint nobody, dismiss nobody, change nothing in place, no opinion unless asked. An earlier pass read only one of the three passages, wrongly declared the draft unsupported, and rewrote the printed line; that has been reverted.

4. ~~Al-Kadhim's four years~~ — envelope 08. **Worked 2026-08-14** against Qarashi's *Life of Imam Musa bin Ja'far al-Kazim*, which turns out to be **fully credited — author, translator (Jasim al-Rasheed) and publisher (Ansariyan)** — better than several sources this project has been treating as usable. Arrest is Shawwal 20, 179 AH; *about* four years holds and all three places agree. Recorded `TRAD`, not `V`: it is arithmetic across two dates, not a statement in the source.
5. **The Shurayh shield case** — envelope 07. **Confirmed negative 2026-08-14**, searched across the whole of `00-sources/text/` rather than one work. Both `al-Irshad` extracts still credit no translator; Nahj al-Balagha has Shurayh only in Letter 3, a different episode. **Still needs `al-Irshad` with a named translator.**

**Two things came out of #4 that are worth carrying forward.** The letter's opening line put all four years in Baghdad when roughly the first was Basra — **and it had been contradicting its own fact panel, which was already right.** Corrected, re-measured, 359 words. And **envelope 08's death date is now `CONT`, not `TV`**: §22 of the held work prints 173 AH, impossible against its own arrest date of 179, with 181 and 186 named as variants and 183 appearing only inside someone else's quotation. **The panel prints 183 with nothing behind it.** That is the next row to work, and it is a regression found rather than a row closed — which is the loop working.

Next after that: #6 onward on the list.

### Fill this in first

The fixed-editions table in `00-foundations/sourcing-rules.md` is **now filled — all six translators confirmed** (2026-08-12). Publisher and year still missing for two (Nahj al-Balagha, al-Kafi), and permission is unchecked for all six. A card set against one edition and printed against another cites the wrong page.

---

## What is still missing

**Sources.** `00-sources/text/` has Tuhaf al-Uqul, both parts of Nahj al-Balagha, Sahifa Sajjadiyya, Risalat al-Huquq, both volumes of Uyun Akhbar al-Rida, al-Kafi, two copies of Kitab al-Irshad, Subhani's *The Message*, two Qarashi lives, and two on the Fourteen. **All Shia.** Guillaume's Sira and the two Tabari volumes were removed on 2026-08-12 under the hard rule in `sourcing-rules.md`.

**Check the title page before assuming a held file is uncitable — one already was and nobody had looked.** `qarashi--the-life-of-imam-musa-bin-jafar-al-kazim.txt` credits **author, translator (Jasim al-Rasheed) and publisher (Ansariyan, Qum)**, which is a full citation chain and better than several files being treated as usable. `head -12` on the extracted text shows it. The two `al-Irshad` files, by contrast, credit **no translator at all**, which is exactly why they still block envelope 07.

Not there:

| Missing | Blocks |
|---|---|
| Kamal al-Din / Jassim Hussain on the occultation | Envelope 10 — the four deputies |
| A **Shia** history covering 40–260 AH | The ruler bullet in all fourteen panels — this had no source even before the rule, and now has no candidate either |
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
| **What orders the companions chain `01/39`–`39/39`?** | Every companion hadith card. Proposal: group by the Masoom pointed to, in historical order. **Number it independently of the silsila** — do not inherit the unresolved segment fight below. |
| **What does Khawla's card carry?** | She points to no Masoom, so the selection rule has nothing to draw on. Answer the scholar's category call on her entry first. |
| **What are the packs?** | How thirty-nine envelopes are sold. Groupings already in the material: the four nayibs, Karbala, the mothers, the Prophet's household. |
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
- **No event print in the companions line, ever.** It carries the calendar ring — now the only collection the box exclusively owns. ⚠ **The hadith-card half of this rule was overturned on 2026-08-14.** That line now carries a card, numbered `FIRST EDITION nn/39`, never a silsila segment. **What replaced the rule: the two chains stay visibly separate**, and `build_print_templates.py` fails the build if a companion template carries a segment number or an event print. See `08-companions/README.md`.
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

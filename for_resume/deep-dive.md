---
schema: 2
slug: noor-post
title: "Noor Post: designing a printed product that cannot ship a wrong fact"
summary: How a monthly printed series for families was scoped as a gated build, with a source pipeline, print tooling and recorded decisions that keep unverified content out of print.
generated: { at: 2026-09-27, commit: a1cbf81 }
---

## Context

Noor Post is a printed series for Shia families with children aged 8 to 12. Once a month a sealed envelope arrives for a specific date in the religious calendar. A parent and child open it together and spend about 25 minutes on a letter, a fact panel, a hadith card, a session card and a small set of other items. The first edition has two parts: the Fourteen, one envelope for each of the Fourteen Masoomeen, sold as a subscription box; and Everyone Else, 39 envelopes about companions and family members, sold singly, as an add-on or in packs.

Three constraints shaped every decision.

- **Accuracy cannot be patched.** A website can be fixed after release. A printed envelope in a child's hands cannot. All 14 box envelopes print as a single run, so one wrong fact found after production costs the whole run.
- **Sources must be traceable.** Every fact and every quotation has to trace to a named edition with a named translator. Where no permitted edition carries a claim, the claim does not print, however well known it is.
- **Nothing is sold that does not exist.** Monthly delivery has to be a posting job, never a production job. That means all 14 envelopes must be printed and in stock before one subscription is sold.

Success for this stage did not mean launch. It meant a complete first edition written against fixed rules, a source library strong enough to verify it, tooling that makes rule breaches visible rather than silent, and a clear list of what still blocks a print run.

## Timeline

- **2026-08-11: foundations and first content.** The repository started with content for all 14 envelopes, the companions line, zines and a review site. The same day, source PDFs were kept out of the repository and the published site, a fetcher was added for archive.org with manual links for sites that block scripts, a PDF text extractor made sources searchable, and a source inventory recorded what was present, degraded or missing.
- **2026-08-12: scale and first audit.** A design system and 12 zines were drafted. The companions line grew, and a gender imbalance was noticed and corrected: 17 of the first 18 companions were men, so 8 women were added and more followed, reaching 18 of 39. An audit of earlier sessions found 2 citation errors that had been recorded as verified; both were fixed, along with the method that caused them. Print templates were generated for all 39 companions, and verifying them surfaced the page-overflow defect described below. Site fixes closed an internal-reference leak and removed a placeholder that looked like a quotation.
- **2026-08-14: governance and pipeline.** A hard rule restricted the project to Shia sources only, and 2 works were deleted. Four product decisions restructured the first edition and overturned the rule against a companion hadith card. A source-of-truth pipeline took raw text to a searchable passage database. A storefront was built with no prices and nothing for sale, and a status dashboard was added to the site.
- **2026-08-24: verification at scale.** A large scholar-recommended collection was approved as a source of record and pinned. The letter format moved from A5 to A4 folded, closing the overflow blocker. Companion hadith cards were selected by a ranker and then checked by a verifier. A prototype build mode was introduced. The complete Kitab al-Irshad was acquired and one envelope's narrative was cut and rewritten to match it.

## Architecture in depth

### Rules as the first layer

Everything is checked against a foundations folder: an editorial rulebook, sourcing rules, source-truth rules, a citation format, standard lines, a fact-panel specification, a design system and a checklist. These were written before most content, following the stated working order: finish the rules, build one envelope, test it physically, test the channel, and only then write the rest.

### Source library and pipeline

The source library is the only part of the repository that counts as evidence. It has 4 layers.

- **Originals.** PDFs are immutable and kept out of git; they ship as a release archive.
- **Tracked text.** Page-marked plain text for 15 works, plus canonical Markdown and an intermediate page representation. The derived files are byte-identical across rebuilds, so any diff means the pipeline or its input changed. They cost 58 MB of redundancy, accepted so that extraction changes can be reviewed.
- **Pinned API collections.** 32 collections with 32,531 records, each with a named translator, stored once and pinned by SHA-256. A check command reports upstream drift without writing, and the corpus build refuses any edition whose snapshot no longer matches its recorded hash.
- **Metadata.** Editions with translator, hash and pagination type; a denylist of rejected works by hash; a claims ledger; and a citations ledger linking claims to sources.

From these, a build produces a SQLite database with FTS5 full-text search. At the last build it held 38,896 pages and 88,178 passages. The database itself is 182 MB, too large for GitHub, so it is rebuilt locally and in CI rather than tracked.

The search tool searches the source library and nothing else. A draft letter can therefore never be returned as evidence for itself. For each hit it reports the edition, translator and whether that edition's page numbers may be cited. Pagination is recorded per edition as print, web-generated, API record or unknown, so the tool prints "record N" for API sources instead of an invented page.

### Content and generators

Content lives as one Markdown file per envelope, companion and zine. Generators build everything downstream:

- print templates for each envelope and 4 per companion, from the Markdown;
- the review site, with envelope pages, per-item card views, print proofs and a design brief;
- a storefront catalogue imported from the same content list, so the shop cannot list something that does not exist;
- a citation sheet, a source audit and a status dashboard.

The site generator strips editorial notes, blocking warnings and internal file references, so envelope pages show only what a family receives. Card views are the one deliberate exception: they show internally which items still lack content, carry noindex and sit behind a "draft for review" footer.

### Continuous integration

On every push to the main branch, GitHub Actions validates the source metadata, runs 84 tests, rebuilds the corpus and the site, and commits the generated site back. The site path is excluded as a trigger so the workflow's own commit does not start another run. If metadata or tests fail, the site is not rebuilt on top of broken data.

## Decision log

**2026-08-12: generate templates rather than hand-build them.** The first 18 companion template sets were built by hand, so the last 21 never got any. A generator replaced them. Before it was allowed to write, a check mode regenerated every file in memory and compared it with disk: 50 of 54 were byte-identical, and the other 4 differed only by an apostrophe escape. Cost: a script to maintain. Benefit: a new companion gets templates the moment it is written, and the gap cannot reopen.

**2026-08-14: Shia sources only.** The rule bans non-Shia works as citations, as corroboration and even as a way to locate a passage. Two translated histories were deleted from disk rather than unlisted, so a later search cannot reach them; 19 source texts became 15. The cost was written down in full: the project's only fully verified envelope lost its 4 verified rows and returned to unverified. The claims were not wrong; they lacked a permitted edition. That turned one work, Kitab al-Irshad, into the most valuable acquisition in the project.

**2026-08-14: a first edition in two parts, and a hadith card for companions.** The product became a closed first edition: the Fourteen as the subscription box and 39 companion envelopes sold individually. A rule stating that companion envelopes must never carry a hadith card, written as "not a guideline", was overturned. The card is numbered on its own chain, "first edition nn/39", never as part of the box's 14-segment chain. Accepted cost: the box is no longer the only way to complete a collection. Mitigation: the two chains must stay visibly separate, and the template generator now fails the build if a companion template carries a box segment number or event print.

**2026-08-24: A4 folded instead of A5.** The word count (330 to 370), the A5 single-side sheet and the type specification could not all hold. Four options were costed. Folding one A4 sheet into 4 A5 faces was the only one that changed nothing already written: type size, word count, all 53 measured letters and the fact panel's place stayed. Cost: a larger paper specification, one extra fold in assembly and a larger C5 envelope.

**2026-08-24: prototype mode.** Sourcing rules written for a print run were blocking layout work, since a card could not be proofed if it could not be rendered. A single build-mode value now switches between prototype (everything renders, provisional content is marked on the artwork) and print (every rule returns, and a preflight command refuses the build until all pass). The rules were rescheduled, not deleted. The record rests on one stated principle: no order ships without human verification.

**2026-08-24: approve a pinned corpus as a source of record.** A scholar-recommended collection with named translators was approved and pinned. A claim carried by one of its passages now goes straight to verified, although scholar sign-off on wording is unchanged. Because the upstream is re-scraped weekly, nothing is cited live; every book is fixed by hash.

**2026-08-24: rank, then verify.** Companion hadith cards are chosen by a ranker from a pool of 596 candidate maxims, with register, length and already-used cards filtered first. The ranker only ranks. A separate verifier proves each chosen saying is in a held source at the given reference, and a single tool writes selections into entry files so templates cannot show a saying the entry does not carry.

## What went wrong

**Citations recorded as verified that were wrong.** An audit on 2026-08-12 found 2 errors. In one, an earlier pass searched a single passage, found different wording and rewrote a letter line, although the same volume carried the text in 3 places and 2 matched the original. The line was restored and now cites all 3. In the other, page numbers had been taken from a two-page-per-sheet scan, so they were sheet numbers and off by 18. Both were fixed along with the method: a claim is not unsupported because one passage differs, and scan sheet numbers are not printed pages.

**Letters that silently lost their last third.** Every letter template rendered 28–76% taller than its page. Because the page element hid overflow, as a trimmed page would, the print-to-PDF step produced a clean, single-page PDF with text missing. Nothing failed. The first response was not a design change: a screen-only guard now draws a red bar and logs a warning on any overflowing page, making the failure visible. The underlying fix, the A4 fold, followed 12 days later once the options were costed.

**A leak and a fake quotation on the site.** An internal filename reached a published page through an item specification. It was fixed at the build layer, so the whole class of leak is covered rather than one instance. Placeholder hadith cards had rendered filler text inside quotation marks with a name attached; since a screenshot loses any surrounding label, placeholders now state plainly that no saying has been chosen.

**Well-meant corrections.** The verifier found a card that had silently corrected a typo in its source edition. With only one copy of that work, the correction was an unattested change, so it was reverted. In another case, a word garbled in one PDF was restored because a second copy of the same translation printed it correctly.

## Operating it

The review site is generated into a docs folder and served by GitHub Pages from the main branch. CI rebuilds it on every push after validation and tests pass. The source database is rebuilt from tracked text and pinned snapshots, and the original PDFs come from a release archive. The storefront has no prices and an inert buy button, and a test fails if a currency symbol or money-shaped number reaches a page. The repository records no running costs.

## Results and lessons

The first edition's text is complete: 14 envelopes, 39 companions and 15 zines. The corpus holds 88,178 searchable passages, and 29 of 39 companion cards are selected and machine-verified. Nothing has been printed, the pilot and channel test have not started, and every fact panel claim remains unverified until checked. Formal scholar engagement is the main blocker.

The lessons are about making failure visible:

- A check that cannot fail is not protection. Silent clipping and silent drift were more dangerous than loud errors.
- Record what a decision costs, not only what it gains. Several reversals were only safe because their costs were written down where the next reader would see them.
- Separate ranking from verifying. Automated selection is useful only when an independent check proves the result.
- Reschedule rules rather than delete them. Prototype mode unblocked design without weakening the print standard.

## Roadmap

- Formal scholar engagement and sign-off, including the envelope that blocks the whole run.
- Print and time the pilot envelope with a real family.
- Run the channel test: ask at least one institution for a workable price for forty sets, and check the unit economics survive it.
- Close the open calendar decisions and select the remaining 10 companion cards.
- Produce the artwork and prove the calendar ring with physical prints.
- Only after all 14 envelopes are printed: open subscriptions.

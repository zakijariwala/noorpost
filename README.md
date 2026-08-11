# Noor Post

Printed series for Shia families with children aged 8 to 12, built around the Fourteen Masoomeen. One sealed envelope per month, opened by a parent and child together on the date it belongs to. About twenty-five minutes.

## Repository layout

| Path | What lives here |
|---|---|
| `PRD.md` | Product requirements. The source of truth for scope, tiers, channel and editorial rules. **Not yet in the repo — paste the current version in.** Everything in `00-foundations/` derives from its §7 and §8. |
| `TASKS.md` | Phased build plan. Ten phases, gated. Read this before starting work. |
| `00-foundations/` | Phase 0. The rules everything else is checked against, including `design-system.md` (typefaces, palette, templates, ring spec). |
| `01-pilot/` | Phase 1. Envelope 03 built end to end, plus the first zine. |
| `03-content/` | Phase 3. Envelopes 01–14 (03 lives in `01-pilot/`), plus `spec-check.md` — the measured counts for all fourteen letters. |
| `08-companions/` | Phase 8. Everyone Else — the companion envelopes. |
| `09-zines/` | Phase 9. Noori's Notebook. |
| `04-art/` | Phase 4. Illustration prompt packs (`prompts.md`) and a print-ready text-layout template, proved against envelope 03 (`print/`). |

Phase numbers in folder names match `TASKS.md`. Gaps in the numbering (02, 04–08) are phases with no text deliverable — channel test, art, production, commerce, launch.

## Working order

1. Finish `00-foundations/`. Nothing is written or drawn until the rules are fixed.
2. Build envelope 03 in `01-pilot/`. Print it. Use it with a real family.
3. Take it to a madrasa administrator and ask what forty sets would cost.
4. Only then write the other thirteen.

## Two constraints that shape everything

**All fourteen print before a single subscription sells.** Monthly must be a posting job, never a production job.

**The channel test comes before the full build.** One finished envelope and one zine are enough to run it.

## Status

| Phase | State |
|---|---|
| 0 — Foundations | Written in full, including the design system. All six translator credits confirmed. **Blocked on: formal scholar engagement (verbal agreement in place since 2026-08-12).** |
| 1 — Pilot | Envelope 03 written. Not printed, not timed, not reviewed. |
| 2 — Channel test | Not started. Needs a printed envelope. |
| 3 — Content build | **All fourteen letters, fact panels and session cards written**, and the silsila segments assigned. Counts measured in `03-content/spec-check.md`. Hadith card selection blocked; artwork pending. |
| 4 — Art | Illustration prompt packs written (`04-art/prompts.md`), covering every envelope, companion and zine. Text-layout print template proved against envelope 03 and extended to all fourteen envelopes and eighteen companions (`04-art/print/`). **No actual illustrations exist yet** — the prompts haven't been run through an image generator. |
| 5–7 — Production, commerce, launch | Not started. Gated behind the print run. |
| 8 — Companions | **Twenty-six written — all fourteen Masoomeen have a companion, eight of the twenty-six are women.** Artwork pending. |
| 9 — Zines | **All fifteen written in full**, including Fadak (verbal scholar agreement; full written sign-off still required before print). |

**Every fact in every fact panel is marked `TO VERIFY`.** Nothing here has been checked against a printed source, because no editions are fixed yet. The citation sheet's status codes exist so that nothing prints on an unverified row.

## What is blocking, right now

| Blocker | Blocks | Owner |
|---|---|---|
| A named scholar, **formally** engaged (verbal agreement in place) | Gate 3, and envelope 06 blocks the whole print run | You |
| The sira gap — the five priority works carry no biography, and the letters are all biography | Every letter's citations. See `00-foundations/citation-sheet.md`, open question 1 | Decision needed |
| Calendar ring punch position | All fourteen event prints | Fixed in `00-foundations/design-system.md` §6 — needs a physical proof, not a decision |
| Envelope 05 / 11 swap | Every item keyed to a month | Still open — not a community-observance question, so it wasn't resolved alongside the other calendar decisions. See `TASKS.md` |
| No actual illustrations exist | Phase 4 gate | Prompts ready (`04-art/prompts.md`) — needs someone to run them through an image generator |

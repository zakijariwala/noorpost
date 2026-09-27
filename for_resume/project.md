---
schema: 2
slug: noor-post
title: Noor Post
tagline: Monthly printed series for families, built on sources
publish: true
reason: ""
status: active
kind: product
size: large
started: 2026-08
ended: null
role: "Owner — scoped the product, set the rules, built the content and tooling"
summary: Planned a printed monthly series for families as a gated product build, backed by a searchable source corpus of 88,178 passages so nothing reaches print without a verified citation.
problem: Religious learning material for children aged 8 to 12 often states history and sayings with no traceable source, and a printed subscription cannot be corrected once a run ships.
stack: [Python, SQLite FTS5, PyYAML, HTML, CSS, GitHub Actions, GitHub Pages]
categories: [product, data, automation]
links: { live: "", docs: "", demo: "" }
metrics:
  - value: "88,178"
    label: "searchable passages across 38,896 source pages, each tied to an edition and translator"
    evidence: "00-sources/reports/source-audit.md"
  - value: "53"
    label: "envelopes written (14 subscription, 39 companions), plus 15 zines"
    evidence: "03-content/ ; 01-pilot/ ; 08-companions/ ; 09-zines/ ; README.md (Status)"
  - value: "84"
    label: "automated tests gating every site rebuild in CI"
    evidence: "tests/ ; .github/workflows/site.yml ; HANDOVER.md"
  - value: "29 of 39"
    label: "companion hadith cards selected and machine-verified against a held source"
    evidence: "HANDOVER.md (State) ; commit 016289f"
highlights:
  recruiter:
    - Structured a new physical product as 10 gated phases, with a hard rule that no subscription sells until all 14 envelopes are printed and in stock.
    - Put a channel test with real institutions before the full build, so the unit economics are proven before money is spent on print.
    - Made and documented reversible and irreversible product decisions, including overturning a core rule, with the cost of each written down.
  engineer:
    - Source pipeline turns immutable PDFs and pinned API snapshots into page-marked text, Markdown and a SQLite FTS5 passage database, with SHA-256 pinning and drift checks.
    - Retrieval searches only the source library, so a draft can never be cited as evidence for itself, and reports whether each edition's page numbers may be cited.
    - Generators build 4 print templates per companion from Markdown, proved byte-identical against hand-built sets and failing the build if a template breaks the product's separation rules.
    - A build-mode switch lets design drafts render everything, while a preflight command re-imposes every sourcing rule before a print run.
    - CI validates source metadata and runs tests before rebuilding the review site and status dashboard, and publishing strips internal notes and never renders a placeholder as a quotation.
  story: ""
skills: [Product scoping, Phase-gated delivery, Risk management, Decision records, Data provenance, Quality gates, Build automation, Unit economics planning]
ai_assisted: true
media: []
todo_owner:
  - "Why did you start Noor Post? A 1–3 sentence first-person story would fill highlights.story."
  - "Has the pilot envelope been printed and used with a family, and has the channel test with a madrasa run? Both are listed as not started."
  - "Is the scholar engagement now formal? It blocks Gate 3."
  - "The review site on GitHub Pages is marked 'draft for review, not for circulation'. Should it be linked publicly?"
  - "Any pricing, pre-orders or waitlist numbers you want to cite once available?"
generated: { at: 2026-09-27, commit: a1cbf81 }
---

## Overview

Noor Post is a printed series for Shia families with children aged 8 to 12, built around the Fourteen Masoomeen. Each month a sealed envelope is opened by a parent and child together on the date it belongs to, for about 25 minutes. The first edition has two parts: the Fourteen, sold as a monthly subscription box, and Everyone Else, 39 companion envelopes sold singly or in packs. The repository holds the product rules, all written content, print templates, a source library and the tooling that ties them together.

## The problem

Children's religious material often repeats stories and sayings with no source a parent could check. For a printed subscription the stakes are higher: all 14 envelopes print as one run, so an error found after production costs the whole run. The product needed a way to guarantee that every fact and quotation traces to a named edition before anything goes to print, and a delivery plan that does not sell what does not yet exist.

## What I built

- A foundations layer: editorial rulebook, sourcing and source-truth rules, citation format, design system and a standard checklist that everything else is checked against.
- Content for the whole first edition: 14 letters with fact panels and session cards, 39 companion envelopes (18 about women, after an early imbalance was spotted and fixed), and 15 zines.
- A source library of Shia works only: 15 page-marked texts and 32 pinned API collections (32,531 records), with edition metadata, a denylist, a claims ledger and a citations ledger.
- A source pipeline and search tool that return passages with edition, translator and citable locator.
- Print templates for every envelope and companion, a card-selection ranker and a verifier that proves each chosen saying is in a held source.
- A generated review site with envelope and card views, a status dashboard, print proofs and a storefront with no prices and nothing for sale until the gate allows it.

## Architecture

- **Rules:** Markdown and JSON in the foundations folder, including a build mode (prototype or print).
- **Sources:** immutable PDFs kept out of git; extracted text, pages and Markdown tracked for review; SQLite with FTS5 rebuilt on demand.
- **Content:** one Markdown file per envelope, companion and zine.
- **Generators:** Python scripts build print templates, the site, the shop, the dashboard, the citation sheet and the source audit.
- **CI:** on every push, GitHub Actions validates metadata, runs tests, builds the corpus and site, and commits the generated site to GitHub Pages.

## Key decisions

- **Gate the build, not only the code.** Ten phases, each with a gate. Physical pilot and a channel test come before writing the other 13 envelopes, and nothing sells before all 14 are printed. Monthly fulfilment must be a posting job, never a production job.
- **Shia sources only, enforced by deletion.** Two non-Shia works were removed from disk, not just unlisted, so a search cannot reach them. The cost was recorded: the only fully verified envelope lost its citations.
- **A companion hadith card, on its own numbered chain.** A rule forbidding it was overturned. The accepted cost is that the box is no longer the only complete collection; the mitigation is that the two chains stay visibly separate, and the template generator enforces it.
- **A4 folded instead of A5.** Every letter rendered 28–76% taller than its A5 sheet and the PDFs clipped silently. Of 4 costed options, folding an A4 sheet was the only one that changed nothing already written.
- **Prototype mode.** Sourcing rules were blocking layout work. A single switch now lets drafts render, and a preflight re-imposes every rule before print.
- **Approve a pinned corpus as a source of record.** A large scholar-recommended collection with named translators was pinned by hash, which let a claim carried by a passage go straight to verified.

## Results

- The whole first edition is written: 14 envelopes, 39 companions and 15 zines.
- 88,178 passages across 38,896 pages are searchable, and 29 of 39 companion cards are selected and verified against source.
- 84 tests pass in CI; the review site and dashboard rebuild on every push.
- Nothing is printed yet. The pilot, channel test and artwork are not started, and every fact panel claim stays marked unverified until checked.

## What's next

- Formal scholar engagement, which gates text freeze.
- Print and time the pilot envelope with a real family, then run the channel test for forty sets.
- Resolve the open calendar decisions and select the remaining companion cards.
- Produce artwork and prove the calendar ring on physical prints.

# Build mode — prototype vs print

**Decided 2026-08-24.** The sourcing rules were written for a print run and were being applied to a design draft. That made every layout task wait on a citation, which is the wrong order: **you cannot proof a card you are not allowed to render.**

Nothing here is deleted. It is **rescheduled.**

---

## The switch

`00-foundations/build-mode.json` carries one value:

```json
{ "mode": "prototype" }
```

| Mode | What it is for | What it does |
|---|---|---|
| **`prototype`** ← current | Layout, proofs, family testing, showing people the thing | Everything renders. Nothing blocks. Provisional content is marked on the artwork itself. |
| **`print`** | A production run | Every rule below comes back, and `tools/preflight_print.py` refuses the build until they all pass. |

Switch with the file, or per-command with `--mode print`.

---

## What prototype mode relaxes

| Rule | In print | In prototype |
|---|---|---|
| Nothing prints on a `TV` claim | Blocks | **Renders.** Fact panels keep their watermark and carry on. |
| A card needs a `V` citation | Blocks | **Renders.** `low` confidence is fine. |
| Never cite without a number | Blocks | **Renders.** An unnumbered locator is allowed and flagged. |
| No card repeats its Masoom's box card | Blocks | **Allowed**, marked `SPECIMEN`. |
| No two companion cards share a saying | Blocks | **Allowed**, marked `SPECIMEN`. |
| Blocked rows render an empty slot | Empty slot | **A specimen renders**, so the card can be proofed at real length. |
| Scholar sign-off on envelope 06 | Blocks the run | Does not block a draft. |
| Companion chain numbering undecided | — | Numbers render; they are data and change in one file. |

### Platform-sourced texts with no credit (added 2026-08-24)

A text obtained from a reputable platform may be **read from and drafted against** in prototype mode even where the title page credits no translator. `SRC-IRS-001` / `SRC-IRS-002` (`Kitab al-Irshad`) are marked `prototype_use: true` on that basis.

`preflight_print.py` still refuses a run while any edition in use lacks a credit, so the rectification is scheduled rather than skipped — which is exactly the shape of every other relaxation on this page.

## The one rule that does not relax, in any mode

> **Never render invented text inside quote marks, and never attribute it to a named figure.**

A screenshot loses whatever label surrounded it. A watermark can be cropped. A caption can be trimmed away by the person who reposts it. So a specimen is **either a real attributed saying from a held source** — reused or theme-unverified, and marked — **or it is visibly not a quotation at all**: no quote marks, no name, set as a typographic specimen block.

This is not strictness for its own sake. It is the single failure that cannot be undone after the fact, and it costs nothing to avoid, because 596 real attributed maxims are already indexed in `00-sources/reports/maxim-pool.json`.

---

## Before a print run

```bash
python tools/preflight_print.py
```

It re-imposes every relaxed rule at once and lists what is still open. It is the gate that makes the relaxation safe, and it is the reason none of this is a loss of rigour — the checks all still exist, they just stopped standing in front of a design task they were never about.

**No order ships without human verification.** That is the standing assumption this mode rests on; if it ever stops being true, this file is wrong and prototype mode should be turned off.

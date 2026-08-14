# Print templates — envelope 03 proof set

Job 2: the text-layout templates, built from `00-foundations/design-system.md`'s exact type, palette and page specs. This is a **design-system verification pass**, not finished production art — it proves the fonts, palette, page geometry, and content structure all render correctly together, using envelope 03 (the pilot) as the live example.

## What's here

| File | Content | Size |
|---|---|---|
| `envelope-03-letter.html` | The Cloak — real, final letter text | A5 portrait |
| `envelope-03-fact-panel.html` | The Prophet Muhammad — real fact panel, 6-bullet skeleton | A5 portrait |
| `envelope-03-hadith-card.html` | **Placeholder content** — see below | A6 portrait ×2 |
| `envelope-03-session-card.html` | Talk about it — real, final session card | A6 portrait |
| `envelope-03-postcard.html` | Fixed wording + art placeholder | A6 landscape ×2 |
| `envelope-03-flap.html` | Inside-flap block, fixed wording | A6 landscape |

`pdf/` and `screenshots/` hold rendered output for each — PDF via headless Edge (`--print-to-pdf`), PNG via headless Edge (`--screenshot`), both from the same HTML/CSS, so what you see in the PNG is what the PDF actually contains.

## The hadith card is a placeholder, not selected content

Hadith-card content is still blocked — no saying can be chosen until sourcing work resumes (see `sourcing-rules.md`). To verify the template without waiting on that, the card uses **Ayat al-Tathir (Qur'an 33:33)** as placeholder text: short, universally known, trivially verifiable by anyone, and useful specifically because it's Arabic script, which exercises the RTL/Naskh rendering path nothing else here does.

**This is marked, loudly, in three places**: the on-screen note, a diagonal watermark on both faces, and a footnote on the back explaining it doesn't even qualify as real hadith-card content (a Qur'anic verse isn't "ethics and conduct," the register hadith cards are restricted to). Don't let this leak into anything that looks like a cleared page — same discipline as the `UNVERIFIED — TO VERIFY` watermark on the fact panel, whose six bullets are real copy but still `TV` on `citation-sheet.md`.

## ⚠ Blocking defect — every letter template overflows its page

**Found 2026-08-12. It affects all fifty-three letter templates and it predates the companions generator.**

Every letter — all fourteen of the Fourteen and all thirty-nine companions — renders taller than the A5 page it is set on:

| | Overflow |
|---|---|
| The Fourteen, letter templates | 39–76% over (envelope 03, the pilot, is the worst at +76%) |
| Companion letter templates | 28–69% over |
| Fact panels, cards, postcards, flaps | **all fit** |

**Why nobody caught it.** `.page` carries `overflow: hidden`, which is what a trimmed page does — so the excess is clipped rather than shown, and `--print-to-pdf` then emits a clean, correct-looking, single-page PDF with roughly the last third of the letter missing. `pdf/envelope-03-letter.pdf` is one page and is missing text right now. The proof looks right, which is why it passed. Same failure shape the note at the bottom of this file already warns about for file paths: a valid-looking PDF of the wrong thing.

**What has been done about it.** Nothing that changes a design decision. `assets/overflow-guard.js` plus the `.overflows` rule in `print.css` now flag any overflowing page on screen with a red bar reading *CONTENT OVERFLOWS THIS PAGE*, and log the overage to the console. Screen only, no geometry changed, no cost in print. It makes the defect visible; it does not resolve it.

**What has to be decided, because all four options have real costs:**

1. **Reduce letter type size or leading.** Cheapest. But `design-system.md` §1 fixes the body face and the letter is the thing a parent reads aloud — shrinking it works against the one item in the box that most needs to be readable.
2. **Give the letter both sides of the A5 sheet.** But §4 assigns the back to the fact panel, so the fact panel would need its own sheet — a new item and a cost line.
3. **Move the letter to A4 folded to A5.** Four sides, keeps the type size, changes the envelope's whole paper spec.
4. **Cut the letters to fit.** They are specified at 330–370 words and measured against it; this would mean re-deciding the word spec, which every letter has been written and audited against.

**This is a Gate 3 blocker, not a prepress detail.** The word-count spec, the A5 spec and the type spec are currently mutually incompatible, and one of the three has to give before any letter can print.

## Known limitations — fix before this becomes production-final

- **Only regular and italic weights are embedded**, not true bold/black. Google's CSS2 API returned the same file for every weight requested (400/500/600/700 for EB Garamond; 400/600/900 for Fraunces) — likely a static-instance quirk of how those two families are served, not a font problem. Titles currently use size and spacing to read as "heavier," not a true bold cut. Re-fetch via the static (non-range) family API if a real bold is needed before print.
- **CMYK/spot conversion not done.** This is RGB, browser-rendered. A commercial printer needs a CMYK or Pantone build — a real prepress step, not something this HTML produces.
- **Bleed is not set.** Pages are exact trim size with zero bleed margin. Add 3mm (or whatever the chosen printer specifies) before this goes to prepress.
- **The ring-punch guide is not drawn on the event print template** — no event print template exists yet; only the six items envelope 03 already had text for are built here.
- **Fraunces' WONK axis isn't used.** Child-line "warmth" is approximated with italic + the accent color, not the true variable-font soft cut — the embedded file may not carry that axis at all (untested).

## How to regenerate

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --no-sandbox ^
  --print-to-pdf="pdf\envelope-03-letter.pdf" --print-to-pdf-no-header --no-pdf-header-footer ^
  "file:///C:/Users/SBI/pp/noorpost/04-art/print/envelope-03-letter.html"
```

Swap the filename for any of the six. **Use `file:///C:/...` (drive letter + colon), not a bare `/c/...` path** — the latter silently resolves to a Windows "File not found" page and still produces a valid-looking PDF of the error, which is exactly what happened on the first pass here before it was caught by screenshotting instead of trusting the file size alone.

## Not yet built

Every other envelope, all ten companions, all fourteen zine covers — this proves the system on one envelope. Extending it to the rest is mechanical once the pattern is approved: same CSS, same font embed, content pulled from each item's own source file the same way `build_site.py` already does for the web site.

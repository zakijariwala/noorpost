#!/usr/bin/env node
/* Print the fourteen envelopes to PDF, one file each, every item at its own
   page size — and refuse to write any envelope with text that does not fit.

     NODE_PATH=$(npm root -g) node tools/render_envelopes.js          # all
     NODE_PATH=$(npm root -g) node tools/render_envelopes.js 03 07    # some

   Needs Playwright with Chromium. Run tools/build_envelopes.py first. The page
   lays itself out (04-art/envelopes/envelope.js) and reports anything still
   overflowing in window.__overflows; a non-empty list fails the run. */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const dir = path.join(__dirname, '..', '04-art', 'envelopes');
const out = path.join(dir, 'pdf');
const nns = process.argv.slice(2).length ? process.argv.slice(2)
  : Array.from({ length: 14 }, (_, i) => String(i + 1).padStart(2, '0'));

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  let failed = 0;
  for (const nn of nns) {
    await page.goto('file://' + path.join(dir, `envelope-${nn}.html`));
    await page.waitForFunction(() => window.__laidOut === true, null, { timeout: 30000 });
    const bad = await page.evaluate(() => window.__overflows);
    if (bad.length) {
      console.log(`envelope ${nn}: OVERFLOWS — not printed: ${bad.join(', ')}`);
      failed++;
      continue;
    }
    await page.pdf({ path: path.join(out, `envelope-${nn}.pdf`), preferCSSPageSize: true, printBackground: true });
    console.log(`envelope ${nn}: printed`);
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();

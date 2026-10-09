#!/usr/bin/env node
/* Print the built companion envelopes to PDF, one file each, every item at its
   own page size — and refuse to write any with text that does not fit. Also
   saves a JPEG preview of each named item (data-item) to preview/, which
   tools/build_site.py places on each companion's page on the site.

     NODE_PATH=$(npm root -g) node tools/render_companions.js          # all built
     NODE_PATH=$(npm root -g) node tools/render_companions.js salman   # some

   Same layout pass as the box (04-art/envelopes/envelope.js). Run
   tools/build_companions.py first. */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const dir = path.join(__dirname, '..', '04-art', 'companions');
const out = path.join(dir, 'pdf');
const prev = path.join(dir, 'preview');
const slugs = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(dir).filter(f => /^companion-.*\.html$/.test(f)).map(f => f.slice(10, -5));

(async () => {
  fs.mkdirSync(out, { recursive: true });
  fs.mkdirSync(prev, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1250, height: 900 } });
  let failed = 0;
  for (const slug of slugs) {
    await page.goto('file://' + path.join(dir, `companion-${slug}.html`));
    await page.waitForFunction(() => window.__laidOut === true, null, { timeout: 30000 });
    const bad = await page.evaluate(() => window.__overflows);
    if (bad.length) {
      console.log(`${slug}: OVERFLOWS — not printed: ${bad.join(', ')}`);
      failed++;
      continue;
    }
    await page.pdf({ path: path.join(out, `companion-${slug}.pdf`), preferCSSPageSize: true, printBackground: true });
    await page.emulateMedia({ media: 'screen' });
    await page.addStyleTag({ content: '.page { box-shadow: none !important; }' });
    const items = await page.$$('[data-item]');
    for (const el of items) {
      const name = await el.getAttribute('data-item');
      await el.screenshot({ path: path.join(prev, `${slug}-${name}.jpg`), type: 'jpeg', quality: 80 });
    }
    console.log(`${slug}: printed, ${items.length} previews`);
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();

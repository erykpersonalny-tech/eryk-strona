// Użycie: node render.js <szablon.html> <dane.json> <wynik.pdf>
// Wstrzykuje JSON do szablonu (window.DATA) i drukuje A4 przez Chromium.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [tpl, dataFile, out] = process.argv.slice(2);
  if (!tpl || !dataFile || !out) { console.error('node render.js szablon.html dane.json wynik.pdf'); process.exit(1); }
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  const html = fs.readFileSync(tpl, 'utf8').replace('/*DATA*/null', JSON.stringify(data).replace(/</g, '\\u003c'));
  const tmp = path.join(path.dirname(path.resolve(tpl)), '.render-' + process.pid + '.html');
  fs.writeFileSync(tmp, html);
  const b = await chromium.launch();
  const p = await b.newPage();
  p.on('pageerror', e => console.error('Błąd w szablonie:', e.message));
  await p.goto('file://' + tmp, { waitUntil: 'networkidle' });
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 10000 });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close(); fs.unlinkSync(tmp);
  console.log('PDF:', out);
})();

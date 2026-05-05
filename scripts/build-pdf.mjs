// Build a single PDF of the full seattledogparkdata.com report by printing
// each report page from docs/ via headless Chrome and merging the results.
//
// The PDF is now generated directly from the live report pages (single
// source of truth) — no separate print template to keep in sync. CSS is
// injected at print time to hide nav chrome, the prev/next paginator,
// and the page footer.
//
// Run locally: npm install && npm run build:pdf
// CI: invoked by .github/workflows/build-pdf.yml on pushes to main that
// touch docs/**. The generated PDF is committed back to docs/ so the link
// on the landing page always points to the latest site content.

import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import url from 'node:url';
import puppeteer from 'puppeteer';
import { PDFDocument } from 'pdf-lib';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const OUT  = path.join(DOCS, 'seattle-dog-parks-report.pdf');

// Pages to merge into the PDF, in reading order. Each page is rendered
// in its full live form; PDF_OVERRIDES below hides the elements that
// don't belong in print (top nav, prev/next paginator, page footer).
const PAGES = [
  'index.html',
  'part1-the-gap.html',
  'part2-access.html',
  'part3.html',
  'enforcement.html',
  'budget.html',
  'peer-cities.html',
  'opinion.html',
];

// CSS injected into every page during PDF build. Hides on-screen
// navigation chrome that is meaningless in a printed document, and
// tightens layout density so we don't waste pages on whitespace.
const PDF_OVERRIDES = `
  /* Hide on-screen-only navigation chrome */
  .skip-link,
  .topbar,
  nav.paginate,
  footer { display: none !important; }

  /* Tighten the masthead so each chapter's date stamp is unobtrusive */
  .masthead { padding: 6px 0 4px !important; font-size: 9pt !important; margin-bottom: 8px !important; }

  /* Each page rendered by puppeteer becomes its own PDF subdocument
     and is concatenated by pdf-lib, so chapters already start on fresh
     pages naturally — no page-break-before rule needed. */

  /* Compress vertical rhythm. On-screen padding is tuned for desktop
     reading; in print these become wasted space. */
  body { font-size: 11pt; }
  .wrap { padding-top: 0 !important; padding-bottom: 0 !important; }
  .hero, .hero-number { padding: 12px 0 !important; margin: 0 0 12px !important; }
  .hero .deck, .hero-number .deck { margin-top: 8px !important; }
  .hero .big-number { font-size: 96pt !important; line-height: 0.95 !important; margin: 0 0 6px !important; }
  h1.hed { margin: 6px 0 8px !important; }
  h2 { margin-top: 14px !important; margin-bottom: 6px !important; }
  h2.finding { margin-top: 18px !important; }
  h3 { margin-top: 10px !important; margin-bottom: 4px !important; }
  p, ul, ol { margin-top: 0 !important; margin-bottom: 8px !important; }
  .lead { margin-bottom: 10px !important; }
  .stats { gap: 8px !important; margin: 8px 0 12px !important; }
  .stat { padding: 12px !important; }
  .takeaway, .note-box, .data-currency, .corrections, .ai-disclosure {
    padding: 10px 14px !important; margin: 8px 0 !important;
  }
  .chart-block { padding: 10px 12px !important; margin: 8px 0 12px !important; }
  .chart-wrap { margin: 6px 0 !important; }

  /* Page-break protection. Charts, maps, and tables are atomic visual
     units — never split them across pages. Small atomic UI elements
     (stat tiles, profile cards, timeline items) likewise stay intact.
     Larger flowing containers (case studies, multi-paragraph takeaways)
     are allowed to break so we don't leave half-page gaps. */
  .chart-block, .map-block, table.data,
  .stat, .hstat, .timeline-item, .principle, .profile-card,
  .chart-source, .chart-title, .chart-subtitle {
    page-break-inside: avoid; break-inside: avoid;
  }

  /* Keep headings glued to the paragraph that follows, and keep the
     intro paragraph glued to the chart/table it introduces. */
  h1, h2, h3, h4, .lead, .chart-title, .chart-subtitle {
    page-break-after: avoid; break-after: avoid;
  }
  .chart-block, .map-block, table.data {
    page-break-before: avoid; break-before: avoid;
  }

  /* Hide the index page's redundant "All the reports" section in
     PDF — the link-list above it already serves as a TOC. The :has()
     selector lets us hide the H2 that introduces the grid without
     adding a class to it. */
  body .report-grid,
  body h2:has(+ .report-grid) { display: none !important; }
`;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.mjs':  'application/javascript; charset=utf-8',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif':  'image/gif',
  '.webp': 'image/webp',
  '.ico':  'image/x-icon',
  '.json': 'application/json',
  '.csv':  'text/csv',
  '.xml':  'application/xml',
  '.txt':  'text/plain',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
};

function startStaticServer(dir) {
  const server = http.createServer(async (req, res) => {
    try {
      let rel = decodeURIComponent(req.url.split('?')[0]);
      if (rel.endsWith('/')) rel += 'index.html';
      const abs = path.join(dir, rel);
      if (!abs.startsWith(dir)) { res.writeHead(403); res.end(); return; }
      const data = await fs.readFile(abs);
      res.writeHead(200, { 'Content-Type': MIME[path.extname(abs).toLowerCase()] || 'application/octet-stream' });
      res.end(data);
    } catch {
      res.writeHead(404); res.end('not found');
    }
  });
  return new Promise(resolve => {
    server.listen(0, '127.0.0.1', () => resolve({ server, port: server.address().port }));
  });
}

async function renderPageToPdf(browser, baseUrl, page) {
  const p = await browser.newPage();
  // Emulate SCREEN media so Chart.js (and other JS-driven rendering) executes
  // — emulating print media freezes JS in a way that leaves <canvas> blank.
  // The injected style tag below provides the print-only overrides.
  await p.emulateMediaType('screen');
  await p.setViewport({ width: 850, height: 1100, deviceScaleFactor: 2 });
  const u = `${baseUrl}/${page}`;
  console.log(`Rendering ${u}`);
  await p.goto(u, { waitUntil: 'networkidle0', timeout: 90_000 });
  // Inject the PDF-build-only CSS overrides (hide nav/footer, page breaks).
  await p.addStyleTag({ content: PDF_OVERRIDES });
  // Chart.js, Leaflet tile loads, font-load, and image decode all settle a
  // beat after networkidle. Wait for the walkshed geojson + map tiles to
  // finish (Part II only), then an extra buffer for charts + font paint.
  try {
    await p.waitForFunction('window.__walkshedReady === true', { timeout: 30_000 });
  } catch {}
  await new Promise(r => setTimeout(r, 6000));
  // scale: 0.78 shrinks everything (text, charts, padding) to roughly
  // print-publication density. The on-screen layout is tuned for ~14pt
  // body type at 850px viewport; 0.78 brings that to ~11pt at Letter
  // width, with charts proportionally smaller.
  const bytes = await p.pdf({
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true,
    scale: 0.78,
    margin: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' },
  });
  await p.close();
  return bytes;
}

async function main() {
  const { server, port } = await startStaticServer(DOCS);
  const baseUrl = `http://127.0.0.1:${port}`;

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const merged = await PDFDocument.create();
  merged.setTitle('Seattle Dog Park Data — full report');
  merged.setAuthor('seattledogparkdata.com');
  merged.setCreationDate(new Date());

  try {
    for (const page of PAGES) {
      const bytes = await renderPageToPdf(browser, baseUrl, page);
      const doc = await PDFDocument.load(bytes);
      const pageCount = doc.getPageCount();
      console.log(`  ${page}: ${pageCount} pages`);
      const copied = await merged.copyPages(doc, doc.getPageIndices());
      copied.forEach(pg => merged.addPage(pg));
    }
  } finally {
    await browser.close();
    server.close();
  }

  const out = await merged.save();
  await fs.writeFile(OUT, out);
  console.log(`Wrote ${OUT} (${(out.length / 1024).toFixed(0)} KB, ${merged.getPageCount()} pages)`);

  // Cache-bust the PDF link on docs/index.html by stamping a version
  // based on PDF size + mtime. Browsers and Cloudflare treat a different
  // query string as a new URL, so readers don't get stuck on an old copy.
  const stat = await fs.stat(OUT);
  const v = `${out.length}-${Math.floor(stat.mtimeMs / 1000)}`;
  const indexPath = path.join(DOCS, 'index.html');
  let html = await fs.readFile(indexPath, 'utf8');
  // Match either the bare path or an existing versioned path
  const newRef = `seattle-dog-parks-report.pdf?v=${v}`;
  const before = html;
  html = html.replace(/seattle-dog-parks-report\.pdf(\?v=[^"'\s]*)?/g, newRef);
  if (html !== before) {
    await fs.writeFile(indexPath, html);
    console.log(`Stamped PDF link with ?v=${v} on docs/index.html`);
  }
}

main().catch(err => { console.error(err); process.exit(1); });

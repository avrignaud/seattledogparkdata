// Build a single PDF of the full seattledogparkdata.com report by printing
// each page from docs/ via headless Chrome and merging the results.
//
// Run locally: npm install && npm run build:pdf
// CI: invoked by .github/workflows/build-pdf.yml on pushes to main that touch
// docs/**. The generated PDF is committed back to docs/ so the link on the
// landing page always points to the latest site content.

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

// Order matches the reading order for the printed report.
const PAGES = [
  'index.html',
  'part1-the-gap.html',
  'part2-access.html',
  'budget.html',
  'enforcement.html',
  'opinion.html',
];

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
  await p.emulateMediaType('screen');
  const u = `${baseUrl}/${page}`;
  console.log(`Rendering ${u}`);
  await p.goto(u, { waitUntil: 'networkidle0', timeout: 60_000 });
  // Chart.js + Leaflet settle a beat after network idle. Give them room.
  await new Promise(r => setTimeout(r, 2500));
  const bytes = await p.pdf({
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' },
    preferCSSPageSize: false,
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
}

main().catch(err => { console.error(err); process.exit(1); });

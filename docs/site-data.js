/**
 * site-data.js — shared CSV loaders for seattledogparkdata.com charts.
 *
 * Goal: every chart on every page reads from a CSV in /data, mirrored to
 * /docs/data so GitHub Pages can serve it. No data is hardcoded in HTML.
 *
 * If you change a CSV in /data, run `scripts/sync-data.sh` to mirror it
 * into /docs/data before the changes will appear on the site.
 */
(function (root) {
  'use strict';

  // RFC-4180-ish CSV parser: handles quoted fields containing commas,
  // doubled quotes ("") inside quoted fields, and trailing newlines.
  // Does NOT handle multi-line fields (no CSV in this repo uses them).
  function parseCSV(text) {
    const rows = [];
    const lines = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n');
    for (const line of lines) {
      if (line === '') continue;
      const fields = [];
      let cur = '';
      let inQuote = false;
      for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (inQuote) {
          if (c === '"' && line[i + 1] === '"') { cur += '"'; i++; }
          else if (c === '"') { inQuote = false; }
          else { cur += c; }
        } else {
          if (c === ',') { fields.push(cur); cur = ''; }
          else if (c === '"' && cur === '') { inQuote = true; }
          else { cur += c; }
        }
      }
      fields.push(cur);
      rows.push(fields);
    }
    return rows;
  }

  function rowsToObjects(rows) {
    if (rows.length === 0) return [];
    const keys = rows[0].map(k => k.trim());
    return rows.slice(1).map(vals => {
      const o = {};
      keys.forEach((k, i) => { o[k] = (vals[i] != null ? vals[i].trim() : ''); });
      return o;
    });
  }

  const _cache = new Map();

  function loadCSV(url) {
    if (_cache.has(url)) return _cache.get(url);
    const p = fetch(url)
      .then(r => {
        if (!r.ok) throw new Error('Failed to load ' + url + ': HTTP ' + r.status);
        return r.text();
      })
      .then(t => rowsToObjects(parseCSV(t)));
    _cache.set(url, p);
    return p;
  }

  // Convenience: load several CSVs and yield an object keyed by short name.
  // Example: loadAll({ olas: 'data/seattle-olas.csv', peers: 'data/peer-cities.csv' })
  //   -> Promise<{ olas: [...], peers: [...] }>
  function loadAll(spec) {
    const keys = Object.keys(spec);
    return Promise.all(keys.map(k => loadCSV(spec[k])))
      .then(results => Object.fromEntries(keys.map((k, i) => [k, results[i]])));
  }

  // Coercion helpers — CSVs are all strings; charts want numbers.
  function num(v) {
    if (v == null || v === '') return null;
    const n = parseFloat(v);
    return Number.isNaN(n) ? null : n;
  }
  function intOr(v, fallback) {
    if (v == null || v === '') return fallback != null ? fallback : null;
    const n = parseInt(v, 10);
    return Number.isNaN(n) ? (fallback != null ? fallback : null) : n;
  }

  root.SDPD = root.SDPD || {};
  root.SDPD.data = { loadCSV, loadAll, parseCSV, rowsToObjects, num, intOr };
})(this);

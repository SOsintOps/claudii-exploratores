#!/usr/bin/env node
/**
 * extract_catalog.js
 * Parses the Exploratores toolkit `search-library.js` (URL-template catalog) and
 * enriches every entry with the human-readable button label harvested from the
 * `pages/*.html` files. Emits a language-neutral `catalog.json`.
 *
 * Usage:  node extract_catalog.js <exploratores_root> <output_json>
 */
const fs = require('fs');
const path = require('path');

const ROOT = process.argv[2];
const OUT = process.argv[3];
if (!ROOT || !OUT) {
  console.error('Usage: node extract_catalog.js <exploratores_root> <output_json>');
  process.exit(1);
}

// --- 1. Load the SearchLibrary object by evaluating the JS file in a sandbox ---
const libSrc = fs.readFileSync(path.join(ROOT, 'assets/js/search-library.js'), 'utf8');
// The file declares `const SearchLibrary = {...};`. Turn it into a value we can grab.
const SearchLibrary = eval('(' + libSrc.replace(/^\s*const\s+SearchLibrary\s*=\s*/, '').replace(/;\s*$/, '') + ')');

// --- 2. Harvest data-search-id -> label from every HTML page ---
const labels = {};
const pagesDir = path.join(ROOT, 'pages');
for (const file of fs.readdirSync(pagesDir)) {
  if (!file.endsWith('.html')) continue;
  const html = fs.readFileSync(path.join(pagesDir, file), 'utf8');
  const re = /data-search-id="([^"]+)"[^>]*>([^<]*)</g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const id = m[1];
    const label = m[2].replace(/\s+/g, ' ').trim();
    if (label && !labels[id]) labels[id] = label;
  }
}

// --- 3. Build enriched catalog ---
const catalog = [];
const categories = {};
for (const [id, cfg] of Object.entries(SearchLibrary)) {
  if (!cfg || typeof cfg !== 'object' || !cfg.urlTemplate) continue;
  const parts = id.split('-');
  const category = parts[0];
  const subcategory = parts.length > 2 ? parts[1] : null;
  const placeholders = [...new Set((cfg.urlTemplate.match(/\{[a-zA-Z0-9_]+\}/g) || []))];
  catalog.push({
    id,
    category,
    subcategory,
    label: labels[id] || id,
    urlTemplate: cfg.urlTemplate,
    validator: cfg.validator || null,
    placeholders,
  });
  categories[category] = (categories[category] || 0) + 1;
}

catalog.sort((a, b) => a.id.localeCompare(b.id));

const meta = {
  source: 'Exploratores OSINT Toolkit 3.4.1 (https://github.com/SOsintOps/Exploratores)',
  generated: new Date().toISOString(),
  total: catalog.length,
  categories,
};

fs.writeFileSync(OUT, JSON.stringify({ meta, entries: catalog }, null, 2));
console.log(`Wrote ${catalog.length} entries across ${Object.keys(categories).length} categories to ${OUT}`);
console.log('Labels resolved:', catalog.filter(e => e.label !== e.id).length, '/', catalog.length);

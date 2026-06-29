# CLAUDE.md  
Context for Claude Code sessions working on this project. **Read `AGENTS.md` first** — it is the canonical shared context (Codex and Claude Code both use it), carrying the current file layout, methodology, and decisions. This file mirrors it plus the Claude-Code-specific operational notes below (generated-file discipline, the updates-log workflow, page-template conventions). **If anything here conflicts with `AGENTS.md` or the committed repo, AGENTS.md and the repo win** — treat this file as stale until reconciled. Then skim README.md and TODO.md.  
## What this is  
A civic-data project about Seattle's off-leash dog area (OLA) system: a neutral **public data reference** plus one clearly-labeled **opinion page**. It lives at **seattledogparkdata.com** (Cloudflare Pages, served from `docs/`); the repo is **github.com/avrignaud/seattledogparkdata** (private). Data is in `/data` as plain CSVs; primary sources are cataloged in `/sources/SOURCES.md`.  
## Framing — facts first  
The site is (1) a neutral data reference — numbers, charts, maps, sources, methodology, with every chart block linking its primary source — and (2) **one clearly-labeled opinion page, `docs/opinion.html`** (principles, counter-arguments, a signed policy recommendation; visually distinct). Keep new factual claims on the report pages and link them to primary sources; opinion goes on the opinion page — don't mix them. This facts-first pivot is **done**: earlier editorial drafts of Parts I/II were de-editorialized and the opinion content moved to `opinion.html`, so don't reintroduce pull quotes or opinionated takeaways on the data pages.  
## File layout  
The **repo itself is authoritative** (`AGENTS.md` has a fuller annotated tree, though its PRR/MOA/script counts lag slightly). Current shape:  
* `docs/` — the site, served by **Cloudflare Pages**. Nine public pages: `index`, `part1-the-gap`, `part2-access`, `part3`, `enforcement`, `budget`, `peer-cities`, `opinion`, `updates`. Plus `print.html` (feeds the PDF), `_headers` (CSP/security), and `docs/data/` (a runtime mirror of `data/`). `mockup-*.html` and `proposal-*.html` are scratch — not public, never audited.  
* `data/` — 21 CSVs, plus `walkshed/` (osmnx isochrones + population coverage), `moas/` (4 signed SPR/FAS MOAs: 2016, 2021, 2023, 2026), `prr-responses/` (6 raw PRR dirs), and `tpl-parkserve/`.  
* `scripts/` — 17 builders/analysis scripts (enforcement page + datasets + metrics + hotspots, walkshed, licensing, TPL overlay, hero image, PDF, and the verifiers `verify_enforcement_data.py` / `verify_site_data.py`).  
* `prrs/` — 10 PRR drafts (`01`–`10`) + README. `sources/` — `SOURCES.md` + archived threads.  
* Root: `AGENTS.md`, `README.md`, `TODO.md`, `CHANGELOG.md`, `METHODOLOGY.md`, `DATA-AUDIT.md`, `DEPLOYMENT.md`, `LICENSE`, `package.json`, and the `*-AUDIT*.md` prompts/reports.  
## Working style  
Andre's preferences (from conversation history):  
* **Direct, no preamble.** Get to the point. Don't recap what was just said.  
* **Informal but substantive.** Not chatty, not stiff.  
* **Honest pushback valued.** If a proposed change is wrong or a data point is weak, say so. Don't agree reflexively.  
* **No trailing follow-up questions.** End responses when they're done.  
* **Praise is fine when warranted**, but don't flatter.  
## Tech conventions already established  
* **No build step.** Everything is static HTML + vanilla CSS + Chart.js/Leaflet from CDN. Don't introduce React, Vue, Webpack, Next.js, Vite, or any other framework without a clear reason.  
* **Fonts:** Fraunces (serif display) + IBM Plex Sans (body) + IBM Plex Mono (metadata). Loaded from Google Fonts.  
* **Color palette** (in CSS vars at top of each HTML file):  
    * --bg: #F6F2E9 (warm off-white paper)  
    * --ink: #121820 (near-black)  
    * --accent: #C04A1E (signal orange, used for Seattle data)  
    * --accent-2: #4C6B54 (sage, used for peer cities/positive)  
    * --accent-3: #2C4A6E (navy)  
    * --danger: #8B2518 (deep red, used for Kinnear)  
* **Charts:** Chart.js v4.4.0 with the datalabels plugin. Never overload a chart with more than ~10 data points unless necessary. Source attribution line goes at the bottom of every chart block.  
* **Map:** Leaflet v1.9.4 with CARTO light_all tiles. The Part II coverage map draws **network-distance isochrones** (osmnx-computed, from `data/walkshed/ola_isochrones.geojson`); planned/in-design sites with no isochrone yet fall back to straight-line half-mile circles. The enforcement-page gap map still uses straight-line circles (legacy). Don't conflate the two.  
* **CSV format:** Plain CSV, no comment headers in data files (the monolithic #-commented CSV in /mnt/user-data/outputs/was intentionally consolidated out). Preserve column names and don't add/reorder columns without updating any code that reads them.  
* **Writing voice:** Editorial but restrained. Fraunces italic for emphasis. Short sentences preferred over long ones. No em-dashes used as commas when a comma would do.  
## Data methodology — things that will bite you  
## 1. The walkshed coverage figure (now 11.7%, network-distance)  
The headline Part II number is **11.7% of Seattle residents within a 10-minute (0.5-mi) network walk of an OLA** (76.6% within SPR's 2.5-mi standard), population-weighted. This **supersedes** the earlier "~33%" straight-line author estimate, which is gone from the site — don't reintroduce it. The current figure is computed in-repo by `scripts/compute_walkshed.py` (osmnx against Seattle's OSM walk network, alpha-shape isochrones, α=0.003) + `scripts/population_coverage.py` (2020 Census block-group overlay clipped to the city boundary). It is still a **modeled estimate**, not a citable TPL number — TPL publishes the 99%-of-residents-near-any-park figure but no dog-park-specific version. Do not claim more precision than the model supports, and keep both figures (11.7% / 76.6%) consistent across pages.  
## 2. Peer-city OLA counts use different definitions  
Portland counts 30+ DOLAs but most are **unfenced voice-control areas**. Seattle counts only fully-fenced dedicated OLAs. SF mixes both. Vancouver BC includes time-restricted beach/field access. Every peer-city comparison chart should have a methodology caveat nearby. Don't quietly normalize these to make any one city look better or worse.  
## 3. The OLA budget is not really the OLA budget  
Seattle Park District's "Maintaining Parks & Facilities" Budget Summary Level (BC-PR-50000) funds **both** OLAs and P-Patch community gardens. Post-2022 numbers in seattle-timeseries.csv reflect the combined total. SPR doesn't publish the OLA-only split. The $100K/year figure for 2016-2020 is OLA-only because SPR publicly stated it was. If anyone asks for exact OLA-only spending for 2023+, the honest answer is "we don't know, SPR doesn't break it out" — a PRR is on the TODO.  
## 4. Dog population estimates range wildly  
The "150,000+" number is the conservative floor, cited since ~2013 (Seattle Humane, Cascade PBS). SPR's own 2023 Expansion Study cites estimates up to 400,000. Use 150K for floor calculations. If higher numbers are used anywhere, cite SPR's Expansion Study explicitly.  
## 5. Austin's 682-acre figure is misleading  
Austin shows up in some sources with ~682 acres of "off-leash area" — this is inflated by Walnut Creek Metropolitan Park (293 ac voice-control) and other natural-area sites, not fenced dog parks. Red Bud Isle is a *different* Austin dog park (~13 ac); earlier drafts of this project confused the two. When citing Austin, the fenced/traditional OLA acreage is closer to 80. The peer-cities.csv has both numbers — use the adjusted one for apples-to-apples.  
## 6. OLA coordinates in seattle-olas.csv are now authoritative  
As of April 2026 they were pulled from SPR's Dog Off-Leash Areas ArcGIS FeatureServer, replacing the earlier address-derived approximations (several points moved 0.3–1.5 km). They seed the walkshed analysis, so don't revert them to address guesses. Still display-grade, not survey-grade — don't use them for legal or engineering purposes.  
## Known-incomplete work (on TODO, don't re-invent)  
See TODO.md for the full list. The highest-value items:  
1. ~~**Replace straight-line walkshed with network analysis**~~ **DONE (April 2026).** The network-distance walkshed (osmnx + 2020 Census block groups) shipped and replaced the old 33% straight-line estimate with 11.7% (10-min) / 76.6% (2.5-mi). Remaining refinement: geocode the ~695 street-address citation rows and spatial-join against park polygons; recompute as Seattle's OSM walk network improves.  
2. **PRR to SPR** for the OLA-only share of the Maintaining Parks & Facilities BSL, 2023-2026.  
3. **PRR to Seattle Animal Control** for annual off-leash ticket counts 2016-2025.  
4. **PRR to SPU** for Find It Fix It "dog in a park" complaints by year.  
5. **Contact COLA** (Citizens for Off-Leash Areas, seattlecola.info) — they've been advocating on this for years and may have data I don't.  
6. **Contact Colin Campbell at SPR** — project lead on West Seattle Stadium OLA; can confirm 2026 opening dates and potentially the OLA-only budget split.  
## Decisions already made (don't relitigate unless asked)  
* **License: MIT.** For the code and analysis. Data is public-record and not separately licensed.  
* **Domain: seattledogparkdata.com.** Factual register, matches the facts-first framing.  
* **Repo: `avrignaud/seattledogparkdata`** (private). Earlier `SyrinxVentures` references are stale.  
* **Deployment: Cloudflare Pages** from `docs/` on `main` (see DEPLOYMENT.md; GitHub Pages was considered earlier, then switched).  
* **Static HTML only.** No framework, no build step, no bundler. Deliberate choice.  
* **Chart.js + Leaflet.** No D3, no Plotly, no Observable notebooks. Unless there's a clear reason to upgrade.  
* **Pages: nine public + print.** Landing, Part I (the gap), Part II (access), Part III, Enforcement, Budget, Peer Cities, Opinion, Updates — plus `print.html` which feeds the PDF. This set is deliberate; don't add pages reflexively.  
* **Analytics: Cloudflare Web Analytics only** (uptime / load-time). No cookies, no personal tracking — keep it clean.  
## Updates log and date conventions

The site has a user-facing updates log at `docs/updates.html` and a "Recent updates" panel near the top of `docs/index.html`. Both are hand-maintained, kept in sync manually. The threshold for what counts as a logged update is **internal-only** — do not document it on the public site.

### When to log a new entry and bump page dates

**Always check with Andre first** before logging an update or bumping site-wide dates. If you're not sure whether a change is significant enough to log, ask. Better to over-ask than to either bury a meaningful change or clutter the log with noise.

**Likely worth logging** (confirm before acting):
- A new page, new finding, or new chart ships
- A methodology change that affects how a number reads (e.g., the straight-line → network walkshed pivot)
- A PRR response is ingested into the dataset
- A material data correction changes a headline figure or a chart's reading
- A peer-city addition or substantive revision
- An editorial framing change that affects tone or structure

**Not logged** (don't bump dates either):
- Typo fixes, link repairs, prose polish
- CSS/layout adjustments
- Wording changes that don't change meaning
- Sub-headline data corrections that don't move a chart's reading
- Internal refactors, audit pass-throughs, script reorganization that don't surface new findings
- PDF regenerations, infrastructure changes

### Workflow when a logged update lands

1. Update the affected page(s).
2. Bump the masthead month/year (`<span>APRIL 2026</span>` style) on every public page in `docs/`.
3. Bump the byline "Updated [Month Year]" line on each page that has one (most content pages do).
4. Bump the footer "Data current as of [Month Year]" line where present (enforcement.html, opinion.html).
5. Prepend an entry to `docs/updates.html` using the existing entry pattern (`<article class="note-box">` with date + headline + body + page-anchor link).
6. Prepend the same entry to the homepage "Recent updates" panel; drop the oldest of the three entries when the panel reaches three.
7. Public pages to touch: `index.html`, `part1-the-gap.html`, `part2-access.html`, `part3.html`, `enforcement.html`, `budget.html`, `peer-cities.html`, `opinion.html`, `updates.html`. Don't touch `mockup-*.html`, `mockups.html`, `print.html`.

### Things NOT to bump on a site-wide date update

- **Inline factual references to specific dates** (e.g., "April 2026 ArcGIS pull", "as of April 2026 search", "Axios reported in April 2026"). These are content claims about when something was checked or reported, not site metadata. Updating them is a separate, deliberate act.
- **Editorial publication marks on `opinion.html`**: the "Signed editorial · April 2026" kicker (line ~291) and the "Queen Anne, Seattle · April 2026" signature (line ~595) are publication-date marks for the editorial itself. Don't bump unless the editorial substantively changed.

### Entry format for `updates.html`

Each entry uses an `<article class="note-box">` with:
- `id="<month-yyyy>-<topic-slug>"` for deep linking
- `border-left-color` set to a brand variable (`--orange` for new findings/data, `--sage` for site/methodology, `--gold` for corrections, `--navy` for PRR responses or methodology). Pick a sensible match.
- A `<strong class="tag">` line in the form `<strong class="tag" style="color: var(--xxx);">Month YYYY &middot; Topic</strong>`
- An `<h3>` headline
- 1-3 short paragraphs of body
- A closing line in IBM Plex Mono with `&rarr; <a href="page.html#anchor">page.html &middot; section name</a>`

The homepage panel uses a tighter format: `<strong>Month YYYY</strong> &middot; <a href="page.html#anchor">Headline</a>` plus a one-paragraph blurb. See `index.html` for the current pattern.

## Running locally  
```
cd docs/
python3 -m http.server 8000
# Then open http://localhost:8000/

```
That's it. No node, no install, no config.  
## Generated files — build discipline (DO NOT hand-edit)  
Some files in this repo are **generated by scripts** and must never be edited by hand. If you hand-edit a generated artifact, the next person who runs the builder silently reverts your change — and the builder and the live file drift apart. This already happened once: a data refresh hand-edited `docs/enforcement.html` directly, leaving `scripts/build_enforcement_page.py` ~50 lines stale until it was re-synced (June 2026). Don't repeat it.  
**The rule:** to change a generated file, edit its **builder and/or its inputs**, then re-run the builder and `git diff` the output. Never edit the generated file directly.  
Generated artifacts and their sources:  
* **`docs/enforcement.html`** ← `scripts/build_enforcement_page.py` (template) + `scripts/enforcement_page_data.json` (data, derived from the CSVs). This is the **only HTML page that is generated**. After editing, run the builder and then `python3 scripts/verify_enforcement_data.py` (it recomputes every load-bearing figure and greps the rendered prose against the data). The builder is idempotent — a second run must produce no diff.  
* **`data/enforcement-citations.csv`, `enforcement-by-park-year.csv`** ← `build_enforcement_datasets.py` (from the PRR xlsx in `data/prr-responses/`).  
* **`data/enforcement-year-metrics.csv`** ← `build_enforcement_metrics.py` (staffing/cost model lives here).  
* **`data/enforcement-hotspots*.csv`** ← `build_enforcement_hotspots.py`.  
* **`data/licensing-*.csv`** ← `build_licensing_datasets.py` (needs `pandas`).  
* **`data/tpl-parkserve/*.csv`** ← `build_tpl_overlay.py` (needs `geopandas`).  
* **`data/walkshed/*.geojson`** ← `compute_walkshed.py` (needs `osmnx`; heavy, one-time).  
* **`docs/images/enforcement-{hero,card}.png`** ← `build_hero_image.py` (needs `matplotlib`; note: PNG bytes are not reproducible across matplotlib versions, so a binary-only diff there is usually environment noise, not content drift).  
* **`docs/data/*`** ← `scripts/sync-data.sh` mirrors `data/*` so Cloudflare Pages can serve them at runtime. Re-run after editing any `data/*.csv` or walkshed GeoJSON.  
* **`docs/seattle-dog-parks-report.pdf`** ← `build-pdf.mjs` (also stamps a cache-bust version into `docs/index.html`).  
**The other HTML pages are hand-maintained** (no generator): `index.html`, `part1-the-gap.html`, `part2-access.html`, `part3.html`, `budget.html`, `peer-cities.html`, `opinion.html`, `updates.html`. Edit those directly.  
## Page template & UX conventions (keep consistent; don't drift)  
Design context for `/impeccable` lives in [`.agents/context/PRODUCT.md`](.agents/context/PRODUCT.md) and [`DESIGN.md`](.agents/context/DESIGN.md). The agreed page template:  
* **Date:** the masthead strip carries `UPDATED <MONTH> <YEAR>` (uppercase) on every page. That is the page's update stamp.  
* **No author byline** on factual pages. There is no per-page "Andre Vrignaud · … · Updated …" block. Authorship lives in the footer; the **only** signed byline/signature is on `opinion.html` (it's a signed editorial).  
* **"About this data" is not a top box.** It lives at the **bottom**, as the first `<h3>About this data</h3>` section inside the collapsible Data Notes (`<details class="data-notes" id="data-notes">`). The top of every page goes masthead → hero (kicker, title, deck) → content.  
* **Data Notes** = one `<details class="data-notes" id="data-notes">` per content page, summary text `Data notes`, closed on screen, forced open in print (CSS handles the chevron, accent color, "expand for sources & methodology" hint, and print rule). Keep `id="data-notes"` so `#data-notes` anchors resolve.  
* **Type scale** (use classes, never inline `font-size`): `.lead` 18.5 / body 16.5 / `.note` 15 / `.fineprint` 13.5. Defined in `site.css`.  
* **Numbers:** spell out sub-$1M figures and counts in full ($100,000, 150,000); millions as `$X.XXM`; chart axis/legend unit labels may keep `($M)`/`per 100K`. No `($K)`/`($M)` in table headers.  
* **Acronyms:** spell out on first use per page, then abbreviate.  
* **Em-dashes and the left-border callouts** (`.note-box`/`.takeaway`/`.fair-note`) are intentional house style — keep them even though generic design linters flag them.  
* The `enforcement.html` equivalents of all the above live in the builder `scripts/build_enforcement_page.py` (regenerate after editing).  
## Git / GitHub conventions  
* **Main branch:** main.  
* **Commit style:** Imperative mood, scoped. Example: Add network-distance walkshed analysis not Added walkshed stuff. Subject under 72 chars; body paragraphs if needed.  
* **Don't force-push main.** Standard discipline.  
* **Don't commit .DS_Store or editor configs.** .gitignore is set up.  
* **CHANGELOG.md is versioned.** Increment on material updates to data or analysis. Bump the version in SemVer-ish style (0.2.0 currently).  
## What "good" looks like for the next session  
If asked "what should we work on?", good answers draw from `TODO.md`. Live priorities:  
* Geocode the ~695 street-address enforcement rows and spatial-join against park polygons; recompute the access × citation overlap as the OSM walk network improves.  
* Citation-density backfill — ensure every bare number on Part I/II links to its primary source.  
* Ingest pending PRR responses (SPR ranger-pairing cost #10; SPU FiFi complaints) as they land.  
* Deepen peer-city per-city detail, or refine the walkshed / TPL overlays.  
Bad answers (asked and settled before):  
* "Let's rewrite this in React / add a CMS / a bundler." No — static HTML is deliberate.  
* "Let's scrape SPR nightly." No — the data changes on multi-year timescales; a quarterly manual refresh is correct.  
* "Let's add behavioral analytics / tracking cookies." No — Cloudflare's basic uptime analytics is the only telemetry, by design.  
## Communication context  
Andre (the project owner) lives in Queen Anne — which is the neighborhood whose only nearby OLA is Kinnear (the 0.1-acre case study in Part II). This is personal for him as well as civic. That context matters for tone calibration, but the reports themselves should remain neutral.  
The existing reports were drafted collaboratively via claude.ai; the expectation from here is that Claude Code will extend and refine the work from the repo directly.  

# AGENTS.md  
Context for Codex sessions working on this project. Read this first, then README.md for the public-facing summary and TODO.md for planned work.  
## What this is  
A civic-data project about Seattle's off-leash dog area (OLA) system. Two HTML reports are already built (Part I: The Gap, Part II: Access) and render as GitHub Pages from /docs. The data behind them is in /data as plain CSVs. Primary sources are cataloged in /sources/SOURCES.md.  
The domain will be **seattledogparkdata.com**. The GitHub org is **SyrinxVentures**.  
The domain will be **seattledogparkdata.com**. The GitHub org is **SyrinxVentures**.  
## The framing pivot (important — read this)  
The earlier drafts (Parts I and II as they exist) were written in a somewhat editorial register — with pull quotes, rhetorical headers ("99% of Seattleites live within a ten-minute walk of a park. *Almost none of them* can legally use it with their dog"), and takeaway boxes that are frankly opinionated.  
**The new direction is facts-first.** The site should be:  
1. **A public data reference.** Numbers, charts, maps, sources, methodology.  
2. **One clearly demarcated opinion section** with recommendations, flagged unmistakably as opinion (a separate page, or a visually-distinct "Editorial" section at the end of the report). Everything else stays neutral.  
This means the existing Part I and Part II reports need editorial tone-adjustment — especially the chart-takeaway boxes and pull quotes, which should either be (a) rewritten as neutral factual observations, (b) moved to the opinion section, or (c) removed.  
This is near-term priority-one work. Flag it proactively if asked "what should we do first."  
## Current file layout  
```
./                              # Repo root
├── AGENTS.md                   # This file
├── README.md                   # Public-facing overview
├── TODO.md                     # Planned work, ranked by value/effort
├── CHANGELOG.md                # Version log
├── LICENSE                     # MIT
├── .gitignore
├── docs/                       # GitHub Pages publishes from here
│   ├── index.html              # Landing page
│   ├── part1-the-gap.html      # Report Part I
│   └── part2-access.html       # Report Part II (has Leaflet map)
├── data/
│   ├── seattle-olas.csv        # 14 existing OLAs with coordinates + acreage
│   ├── seattle-timeseries.csv  # Pop/budget/OLA count by year 2010-2026
│   ├── peer-cities.csv         # Portland, SF, Vancouver BC, Austin, etc.
│   ├── illegal-use-indicators.csv
│   ├── kinnear-timeline.csv    # 20-year Kinnear incident chronology
│   └── planned-olas.csv        # Under-construction + in-planning sites
└── sources/
    └── SOURCES.md              # All primary sources with URLs

```
## Directory setup note (if the files look wrong)  
The tarball extracts to a seattle-dog-parks/ subdirectory. If the repo is at /Developer/seattledogparkdata.com/seattle-dog-parks/instead of directly at /Developer/seattledogparkdata.com/, move the contents up one level:  
```
cd /Developer/seattledogparkdata.com
mv seattle-dog-parks/* seattle-dog-parks/.* . 2>/dev/null
rmdir seattle-dog-parks

```
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
* **Map:** Leaflet v1.9.4 with CARTO light_all tiles. Half-mile walksheds are straight-line circles, not network polygons.  
* **CSV format:** Plain CSV, no comment headers in data files (the monolithic #-commented CSV in /mnt/user-data/outputs/was intentionally consolidated out). Preserve column names and don't add/reorder columns without updating any code that reads them.  
* **Writing voice:** Editorial but restrained. Fraunces italic for emphasis. Short sentences preferred over long ones. No em-dashes used as commas when a comma would do.  
## Data methodology — things that will bite you  
## 1. The 33% walkshed estimate  
In Part II, "~33% of Seattle residents within 10-min walk of an OLA" is my calculation, not TPL's. It's a straight-line half-mile buffer around each OLA coordinate, overlaid on 2020 Census block groups. A proper network analysis (accounting for I-5, the Ship Canal, hills) would produce a **smaller** number, not larger. Do not upgrade this to a bigger number or claim precision it doesn't have. The TODO has "replace with real network analysis" as the single highest-value methodological improvement — that would be QGIS + TPL ParkServe data + shapely or similar.  
## 2. Peer-city OLA counts use different definitions  
Portland counts 30+ DOLAs but most are **unfenced voice-control areas**. Seattle counts only fully-fenced dedicated OLAs. SF mixes both. Vancouver BC includes time-restricted beach/field access. Every peer-city comparison chart should have a methodology caveat nearby. Don't quietly normalize these to make any one city look better or worse.  
## 3. The OLA budget is not really the OLA budget  
Seattle Park District's "Maintaining Parks & Facilities" Budget Summary Level (BC-PR-50000) funds **both** OLAs and P-Patch community gardens. Post-2022 numbers in seattle-timeseries.csv reflect the combined total. SPR doesn't publish the OLA-only split. The $100K/year figure for 2016-2020 is OLA-only because SPR publicly stated it was. If anyone asks for exact OLA-only spending for 2023+, the honest answer is "we don't know, SPR doesn't break it out" — a PRR is on the TODO.  
## 4. Dog population estimates range wildly  
The "150,000+" number is the conservative floor, cited since ~2013 (Seattle Humane, Cascade PBS). SPR's own 2023 Expansion Study cites estimates up to 400,000. Use 150K for floor calculations. If higher numbers are used anywhere, cite SPR's Expansion Study explicitly.  
## 5. Austin's 682-acre figure is misleading  
Austin shows up in some sources with ~682 acres of "off-leash area" — this is inflated by Red Bud Isle and similar shared-use hiking areas, not fenced dog parks. When citing Austin, the fenced/traditional OLA acreage is closer to 80. The peer-cities.csv has both numbers — use the adjusted one for apples-to-apples.  
## 6. OLA coordinates in seattle-olas.csv are approximations  
They were derived from SPR address data, not from an official GeoJSON layer. Good enough for display on a Leaflet map at city scale; don't use them for legal or engineering purposes. If someone wants canonical geometry, they're on Seattle's ArcGIS Open Data portal somewhere.  
## Known-incomplete work (on TODO, don't re-invent)  
See TODO.md for the full list. The highest-value items:  
1. **Replace straight-line walkshed with network analysis** (QGIS + TPL ParkServe data). Would upgrade the key 33% number from an estimate to a citable figure.  
2. **PRR to SPR** for the OLA-only share of the Maintaining Parks & Facilities BSL, 2023-2026.  
3. **PRR to Seattle Animal Control** for annual off-leash ticket counts 2016-2025.  
4. **PRR to SPU** for Find It Fix It "dog in a park" complaints by year.  
5. **Contact COLA** (Citizens for Off-Leash Areas, seattlecola.org) — they've been advocating on this for years and may have data I don't.  
6. **Contact Colin Campbell at SPR** — project lead on West Seattle Stadium OLA; can confirm 2026 opening dates and potentially the OLA-only budget split.  
## Decisions already made (don't relitigate unless asked)  
* **License: MIT.** For the code and analysis. Data is public-record and not separately licensed.  
* **Domain: seattledogparkdata.com.** Factual register, matches the facts-first framing.  
* **GitHub org: SyrinxVentures.** Andre's S-Corp org.  
* **GitHub Pages from /docs folder on main branch.** Standard setup.  
* **Static HTML only.** No framework, no build step, no bundler. Deliberate choice.  
* **Chart.js + Leaflet.** No D3, no Plotly, no Observable notebooks. Unless there's a clear reason to upgrade.  
* **Two reports, not ten.** Part I and Part II are the current structure. A Part III is conceivable (see TODO) but shouldn't be created reflexively.  
* **No analytics, no cookies, no tracking.** Civic data project, keep it clean.  
## Running locally  
```
cd docs/
python3 -m http.server 8000
# Then open http://localhost:8000/

```
That's it. No node, no install, no config.  
## Git / GitHub conventions  
* **Main branch:** main.  
* **Commit style:** Imperative mood, scoped. Example: Add network-distance walkshed analysis not Added walkshed stuff. Subject under 72 chars; body paragraphs if needed.  
* **Don't force-push main.** Standard discipline.  
* **Don't commit .DS_Store or editor configs.** .gitignore is set up.  
* **CHANGELOG.md is versioned.** Increment on material updates to data or analysis. Bump the version in SemVer-ish style (0.2.0 currently).  
## What "good" looks like for the next session  
If the next Codex session is asked "what should we work on?", good answers are any of:  
* Refactor Part I and Part II to separate neutral factual content from opinion (the pivot described above). Create a new docs/opinion.html or equivalent for recommendations.  
* Implement the network-distance walkshed analysis (TODO #1). This would be the single biggest methodological upgrade available.  
* Add a dedicated docs/data.html page that presents the CSVs as interactive tables (DataTables.js or similar) so the "data site" framing is reinforced.  
* Draft the PRRs from the TODO list as markdown files in a new /prrs directory, ready to send.  
* Expand the peer-city data with deeper per-city pages (currently peer cities are only aggregate).  
* Add a simple site header/footer template shared across the three HTML files (currently each file has its own complete styling).  
Bad answers:  
* "Let's rewrite this in React." No.  
* "Let's add a CMS." No.  
* "Let's write a script that scrapes SPR nightly." No — the data changes on multi-year timescales; a quarterly manual refresh is correct.  
* "Let's add analytics so we can see who's reading." No.  
## Communication context  
Andre (the project owner) lives in Queen Anne — which is the neighborhood whose only nearby OLA is Kinnear (the 0.1-acre case study in Part II). This is personal for him as well as civic. That context matters for tone calibration, but the reports themselves should remain neutral.  
The existing reports were drafted collaboratively via Codex.ai; the expectation from here is that Codex will extend and refine the work from the repo directly.  

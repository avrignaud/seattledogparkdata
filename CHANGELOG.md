# Changelog

## [1.0.0] — 2026-04-19

First complete version. The site as of 1.0 is a coherent public-data reference on Seattle's off-leash area system — overview, Part I (The Gap), Part II (Access), Part III (Forward), Enforcement, Budget, Peer Cities, Opinion, and a single-file print PDF — with every factual claim linking back to its source and the underlying dataset pipeline fully reproducible from committed scripts.

### Added since 0.3.0

- **Part II access-gap analysis.** Network walkshed via `scripts/compute_walkshed.py` (osmnx alpha-shape α=0.003 with a 0.3 km² area floor and convex-hull fallback for edge-of-OSM-coverage OLAs). 11.7% of Seattle residents within a 10-minute walk of an OLA vs 99% for any park; 76.6% within SPR's 2.5-mile standard. Replaces the earlier straight-line estimate.
- **Part II Finding 02b.** Citation × walkshed overlay — 69.6% of park-named citations fall outside any OLA walkshed (72.1% with street-addresses included). Reproducible via `scripts/citation_walkshed_analysis.py` + `scripts/geocode_street_addresses.py`.
- **Part II Finding 02c.** TPL ParkServe priority-tier overlay. 606 Seattle block groups cross-tabbed against walkshed union. Reproducible via `scripts/build_tpl_overlay.py`.
- **Part II space-per-dog visual.** Resident's share of parkland (355 sq ft, studio apartment) vs. dog's share of OLA (~5.4 sq ft, doormat). Drawn to scale; the boxes are 300×300 and 37×37 pixels respectively. 66× ratio.
- **Part III — Forward.** New page at `docs/part3.html` with three findings: what works (Magnuson / Genesee / Westcrest profiles), shared-use deep-dive (NYC off-leash hours formally since April 2007), and non-SPR land options (WSDOT / City Light / Port of Seattle). Data gaps flagged inline on blocks where specific primary sources aren't publicly indexed.
- **Peer Cities** (`docs/peer-cities.html`). Eight detail sections: Portland, SF, Vancouver BC, Washington DC, Minneapolis, NYC, Austin, Boise. Each carries a tile layout where the value notes lead with a multiplier or design choice vs Seattle, not a raw source citation.
- **Budget deep-dive** (`docs/budget.html`). Includes a "Scale of it" triptych — giant ratio card ($339M : $1.8M), 1,000-dot waffle chart with the OLA share highlighted, and a linear-scale bar chart (complement to the log chart below). Plus a peer-city space-per-dog comparison (Option 1 of the space-per-dog analysis across five cities) and a Minneapolis Enterprise-Fund head-to-head callout (the only peer where OLA operating spend is separately reported).
- **Giant-number landing hero.** 11.7% at display scale in Fraunces, paired with a right-column headline and foot-note frame; four stat tiles below.
- **Part I scatter-plot inline labels.** Every point on the investment-per-resident vs dog-parks-per-100K scatter is labeled inline.
- **Opinion page voice pass.** Rewritten top-to-bottom in first-person warm-professional register, AI-style constructions removed.
- **Voice-style memory.** `~/.claude/projects/.../memory/user_voice.md` distills the voice profile from ~175 sent emails 2023–2026 for consistent first-person drafts.

### Changed since 0.3.0

- **park-coordinates.csv** reconciled to SPR ArcGIS FeatureServer for all 14 OLA host parks (prior data had up to 928m drift on Lower Woodland).
- **seattle-olas.csv** Magnuson year_opened 1998 → 1999 (permanent designation per HistoryLink; 1996 was pilot/trial).
- **peer-cities.csv** `population_year` split into `population_estimate_year` + `metric_reference_year`. Austin provenance corrected: the inflating acreage is Walnut Creek Metropolitan Park (293 ac voice-control), not Red Bud Isle (13 ac).
- **Citation-rate headline** unified across Part II + print to the script output (69.6% / 2,035 of 2,925 park-named; 72.1% / 2,563 of 3,554 combined).
- **Auditing pipeline.** Three third-pass audits committed to `audits/` (`AUDIT-INTERNAL.md`, `AUDIT-INTERNAL-2.md`, `AUDIT-PASS3-2026-04-18.md`, `AUDIT-PART3-2026-04-18.md`). Every SEVERE and MODERATE finding resolved.
- **Data-notes headings** consolidated to just "Data notes" + "Primary sources" across pages (previous "New Data Notes" / "Data Notes & Caveats" / "Primary Sources Added" naming was pre-launch scaffolding).
- **Kinnear/Denny size comparator** "two tennis courts" → "a basketball court" (cleaner, less ambiguous comparator; basketball court is 4,700 sq ft, Denny is 4,574 sq ft, Kinnear is 5,401 sq ft).
- **TPL priority-tier section** rewritten with an explicit explanation of what the Park Priority Index measures (low-income density, POC density, CDC health indicators, heat/environment stress) and what the cross-tab actually asks.
- **"Zero in 17 years"** rationalization replaced the prior "one in fifteen years" prose across Part I hero, Part II takeaway, Opinion P1, index Part I card, and README.

### Fixed since 0.3.0

- Westcrest 0.5-mi walkshed regression (0.260 km² under tight alpha-shape → 0.765 km² after the area-floor + convex-hull fallback landed).
- NYC Off-Leash Hours press-release URL `?id=19895` → `?id=19877` on Part III and Peer Cities.
- Westcrest OLA renovation scope corrected to the Parkways-blog primary source (drainage / erosion / access / accessibility; $505K from the Park District Major Maintenance Fund, not pure capital).
- Small-dog-area count 2 → 5 (matches seattle-olas.csv: Magnuson, Westcrest, Genesee, Golden Gardens, Magnolia Manor).
- Several 404'd external URLs (Austin PARD, Boise P&R, COLA) replaced with live canonical domains.

## [0.3.0] — 2026-04-17

### Added — Overview, Enforcement, Editorial, PRR infrastructure

- `docs/index.html`: new landing page. Stat grid, four report cards (Part I, Part II, Enforcement, Editorial), primary-data index linking every CSV, methodology caveats, corrections-welcome block. Full print CSS.
- `docs/enforcement.html`: new page covering 4,803 off-leash citations 2014–2019 from PRR C049204.
  - Interactive Leaflet hotspot map with circle markers sized by citation count, color-coded by OLA status.
  - Top-20 cited-parks bar chart — six of the top ten have no designated OLA.
  - Year-trend chart 2014–2019 with 2019 flagged as partial-year (Jan–Oct).
  - Citations-by-offense-level breakdown (~90% first-offense warnings).
  - Full top-20 table with "nearest OLA if none" column.
  - Prominent data-currency banner noting October 2019 cutoff and follow-up PRR filed.
  - Full print CSS.
- `docs/opinion.html`: new clearly-marked editorial/opinion page. Six principles, three opinions, one detailed policy recommendation (time-zoned shared-use model based on NYC's off-leash-hours policy). Signed by Andre Vrignaud. Visually distinct navy band, different accent colors. Explicit data-gap flags where claims lack primary sources. Full print CSS.
- `data/prr-responses/C049204/`: raw SPR public records request response (5 xlsx) with README documenting request text, response dates, and caveats.
- `data/enforcement-citations.csv`: 4,803 consolidated citation rows with canonical park names, offense level, fee, timestamp, zip.
- `data/enforcement-by-park-year.csv`: citation counts aggregated by park × year.
- `data/park-coordinates.csv`: approximate geocoded coordinates for 43 parks appearing in the enforcement data (both OLA hosts and non-OLA parks), used for the hotspot map.
- `prrs/`: four drafted public-records-request markdown files + COLA outreach email:
  - `01-spr-offleash-citations-post-2019.md` (filed)
  - `02-spu-fifi-dog-complaints.md`
  - `03-spr-ola-budget-split.md`
  - `04-spr-access-methodology.md` (the 2.5-mile standard)
  - `05-spr-ola-usage-counts.md`
  - `outreach-cola.md`
- `sources/andre-qacc-thread-2019.md`: full primary-source thread from 2019 Queen Anne community discussion, preserved with data-points-to-cross-verify table.

### Added — Part II

- New "What 'too small' means, quantified" block in Part II with AKC 1-acre minimum, industry design consensus (1–5 acres), 75–100 sq ft per dog capacity standard, and a full capacity table for all 14 Seattle OLAs showing which fall below the AKC floor and their implied peak-use capacity.
- Data-currency banner at top of Part II noting the 2016 SPR survey is a decade stale and that exact FIFI complaint counts have been requested via PRR.

### Added — Part I

- Data-currency banner at top of Part I clarifying which figures are current and which are approximate.

### Changed

- Consistent top-nav across all docs pages (Overview · Part I · Part II · Enforcement · Editorial) with the current page marked active.
- Print CSS added to index, part1, part2, enforcement, opinion — each page paginates cleanly to PDF via browser Print → Save as PDF. Interactive charts render at fixed in-print sizes; maps print as static bitmaps.
- Corrections-welcome block on index and opinion — email `seattledogparkdata@ozymandi.as` or file a repo issue.
- Updated all GitHub references from `SyrinxVentures/seattledogparkdata.com` to `avrignaud/seattledogparkdata` (repo moved to personal org, private).
- Updated opinion O1 to include the April 2026 Axios Seattle reporting on SPR expanding enforcement to two full-time seven-day positions — framed as "doubling down on the part that isn't working."

## [0.2.0] — 2026-04-17

### Added — Part II: Access

- `docs/part2-access.html`: new report covering walkability, mapping, and the Kinnear Park case study.
  - Walkability paradox chart: 99% (any park) vs. ~33% (OLA) 10-minute walkshed coverage.
  - Interactive Leaflet map of all 14 existing OLAs + 2 under-construction + 4 planned, with half-mile walksheds.
  - Peer-city OLA acreage comparison (per 10K residents): Seattle vs. Vancouver BC, Portland, SF, Austin.
  - Kinnear Park case study with 20-year incident timeline (1999–2025).
  - Section on illegal off-leash use as a symptom of system failure: SPR's own 2016 survey data (39% weekly-to-monthly), Find It Fix It complaint counts, enforcement ticket volume.
- `data/kinnear-timeline.csv`: structured chronology of Kinnear encampment/safety events.
- `data/illegal-use-indicators.csv`: SPR survey results, walkshed estimates, ParkScore amenity sub-scores.
- `data/planned-olas.csv`: in-construction and planning-phase OLAs with coordinates.

### Changed

- `data/seattle-olas.csv`: added coordinates and safety_notes columns to the existing OLA inventory.

## [0.1.0] — 2026-04-17

### Initial Release — Part I: The Gap

- `docs/part1-the-gap.html`: initial editorial-style report with 7 Chart.js visualizations.
  - Residents per OLA over time (2010–2026).
  - Peer-city dog parks per 100K comparison.
  - Park investment per capita vs. dog-park density scatter.
  - SPR total budget vs. OLA improvement budget dual-axis.
  - OLA spending by Park District cycle.
  - Playgrounds vs. OLAs (kids vs. dogs ratio).
  - OLA acreage concentration (top 4 = 78% of total).
- `data/seattle-olas.csv`: 14 existing OLAs with names, acres, neighborhoods.
- `data/seattle-timeseries.csv`: year-by-year population, SPR budget, OLA budget 2010–2026.
- `data/peer-cities.csv`: TPL ParkScore 2025 data for 13 comparison cities.
- `sources/SOURCES.md`: primary source list with URLs.

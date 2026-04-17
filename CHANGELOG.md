# Changelog

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

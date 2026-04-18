# TODO

Concrete next-work ideas, organized by effort and value. Kept up-to-date as work progresses.

## Filed / awaiting response

- [x] **PRR C049204** — off-leash citations 2014–2019. Responded Oct 2019; data at `data/prr-responses/C049204/` and consolidated as `data/enforcement-citations.csv`.
- [x] **PRR #1 (filed)** — off-leash citations Oct 2019 to present. Draft at `prrs/01-spr-offleash-citations-post-2019.md`. Awaiting SPR response.
- [x] **PRR #2 to SPU** for Find-It-Fix-It "dog in a park" complaint counts by year and park. Filed. Awaiting response.
- [x] **PRR #3 to SPR** for OLA-only share of the Maintaining Parks & Facilities BSL. Filed. Awaiting response.
- [x] **PRR #4 to SPR** for the 2.5-mile OLA access standard methodology. Filed. Awaiting response.
- [x] **PRR #5 to SPR** for per-OLA usage/headcount data. Filed. Awaiting response.
- [x] **PRR #6 to SAS** for Seattle Animal Shelter dog-license history + compliance estimate. Filed. Awaiting response.

## Outreach sent

- [x] Email to COLA (Citizens for Off-Leash Areas) — usage-count data, corrections, coordination.
- [x] Email to QACC / Don Harper — Queen Anne hilltop OLA priority.
- [x] Email to Colin Campbell (SPR, project lead on West Seattle Stadium OLA) — confirmed 2026 opening, final site acreages, updated OLA-only budget.

## High value, low effort

- [x] **Network walkshed (osmnx + Census).** `scripts/compute_walkshed.py` + `scripts/population_coverage.py`. Current: 9.5% of residents within 0.5-mi network walk; 78.3% within SPR's 2.5-mi standard.
- [x] **Reconcile OLA coordinates to SPR authoritative GIS.** Pulled April 2026 from the Dog Off-Leash Areas ArcGIS FeatureServer. Walkshed rerun with new coords.
- [x] **Dog-population triangulation.** Three-tier estimate now on site — licensed floor (Seattle Open Data), AVMA-derived (~248K), SPR Expansion Study range.
- [x] **Peer-city detail pages.** Six cities (Portland, SF, Vancouver BC, DC, Minneapolis, NYC) at `docs/peer-cities.html`, verified via live WebFetch.
- [x] **Funding-mechanism comparison.** `docs/budget.html` Finding 08 table covering Portland / SF / Vancouver / DC / Minneapolis, with Minneapolis permit-fee outlier callout.
- [x] **Consolidated print PDF.** Dedicated template at `docs/print.html` with charts, maps, and data tables; regenerated on every `main` push to `docs/seattle-dog-parks-report.pdf`.
- [x] **CI lint.** `.github/workflows/lint.yml` validates every CSV parses with consistent columns and every HTML file parses cleanly on PR and push.

## High value, more effort

- [ ] **TPL park-need overlay chart on Part II.** ParkServe shapefile already imported to `data/tpl-parkserve/`; cross-tab CSVs published (`ola-walkshed-by-tpl-rank.csv`, `ola-walkshed-by-tpl-priority-tier.csv`). Next step: render as a chart/map callout showing the bimodal pattern (highest-priority and middle-priority BGs).
- [ ] **Historical OLA timeline map.** Animated year-opened visualization. Current site has a year-opened bar chart; an actual map over time would make the 1997–2009 build-out + 2010–2025 drought visually concrete.
- [ ] **Per-OLA usage/density estimates.** From MOLG/COLA volunteer counts or direct observation. Would convert the Kinnear capacity argument from theoretical to empirical.
- [ ] **Citation-density backfill pass on Part I and Part II.** Every bare number should link to a primary source, a CSV row, or be marked as derived/approximate. New pages (enforcement, opinion, peer-cities, print) already follow this rule.
- [ ] **Alpha-shape refinement of the walkshed isochrones.** Current implementation uses convex hulls, slightly overstates walkable area at OLA boundaries. Would shift 9.5% down by 1–2 pts.

## Part III ideas (new report)

- [ ] **"What works"** — profile Magnuson (MOLG 501(c)(3)), Genesee (COLA steward), Westcrest (2021–2022 $505K renovation, HPAC partnership). Positive counterweight to the Kinnear case. Verified research material is queued in earlier session notes.
- [ ] **Comp Plan angle.** Seattle's 2024 Comprehensive Plan proposes denser residential development. More density without new OLAs = worse per-capita access. Chart the projection.
- [ ] **Shared-use policy deep-dive.** NYC off-leash hours (19 years formal operation), Boston's variants, Chicago's DFAs. Operational details for the recommendation in `docs/opinion.html`.
- [ ] **Legal off-leash on WSDOT / Seattle City Light / Port of Seattle land.** COLA flagged this in the 2023 Expansion Study — that SPR didn't consider non-SPR public land.

## Data quality / maintenance

- [x] **OLA coordinates** reconciled to SPR ArcGIS FeatureServer (April 2026 pull).
- [x] **Provenance column** added to reference CSVs. `DATA-AUDIT.md` records the audit trail.
- [x] **C049204 README** per-file sheet breakdown published.
- [x] **location_type column** in `enforcement-citations.csv` classifies each row: 4,020 park_named / 672 street_address / 111 unknown.
- [x] **Dog-population estimate** triangulated (licensed floor, AVMA-derived, SPR ceiling). 150K floor retained as conservative working value.
- [ ] **Full geocode** of the 672 street-address enforcement rows. Currently flagged but not mapped.

## Infrastructure / repo

- [x] Repo at `avrignaud/seattledogparkdata`.
- [x] Site deployed via Cloudflare Pages at `seattledogparkdata.com` from `docs/`.
- [x] CI for CSV/HTML lint on PR + push.
- [x] PDF build pipeline (puppeteer + `docs/print.html`), commit-on-main.
- [ ] Shared-CSS extraction across `docs/*.html` (currently duplicated per file, ~300 lines of near-identical style blocks). Deferred due to visual-regression risk.

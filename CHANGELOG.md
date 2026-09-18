# Changelog

## [1.3.0] — 2026-09-17

SPR answered [PRR C264837](data/prr-responses/C264837/README.md) on 15 July 2026 with four
years of budget and spending for the two Master Projects inside BSL BC-PR-50000. The answer
retires a claim this project has carried since 2019, corrects the OLA-only budget figure by a
factor of 2.6, removes a double-count, and supplies the strongest new finding on the budget
page. Site restructure: a tenth page, `docs/data-methods.html`, now holds the reference
material that was making the report pages too long.

### Corrections (stated plainly)

- **"SPR doesn't publish the OLA-only split, so we don't know" was wrong.** Not published is
  not the same as not tracked. SPR books `MC-PR-51002` "Improve Dog Off Leash Areas" and
  `MC-PR-51001` "Rejuvenate P-Patches" separately and produced both on request. The two
  exhaust the budget line: their adopted budgets sum to the combined figure already on file,
  to the dollar in 2023 and within rounding in 2025–26.
- **The OLA-only figure was wrong by 2.6×, and was never sourced.** The site carried $126,000
  (2023) and $129,000 (2024), attributed to "Parkways blog / Seattle Times coverage." No such
  source could be located in September 2026 (both cited Parkways posts and the Mayor's Cycle 2
  fact sheet were checked). The record gives **$328,345** and **$333,478**, then $1,568,818
  (2025) and $1,574,370 (2026).
- **"P-Patch is the larger share" is retired.** It rested on the withdrawn figure. Which
  Master Project is larger depends on the measure and the three disagree: OLA leads on adopted
  budget in all four years, P-Patch leads on revised budget in 2023–24, and spending
  alternates. The page now names the measure.
- **The Cycle 2 capital was double-counted.** SPR states the ~$3.1M sits *inside*
  BC-PR-50000 within MC-PR-51002. `data-methods.html` rendered it as "$1,845,706 +$3.46M",
  which reads as a sum. The separate capital series is gone from the budget chart.
- **A $3.46M figure cited a document that does not contain it.** The Mayor's Park District
  Cycle 2 fact sheet has no OLA capital line; its only off-leash entry is $450K for
  seven-day enforcement. Replaced with the **$3,103,000** on SPR's own project pages, with
  Ravenna Park's design-only status described separately.
- **Cycle 1 tightened from $100,000 to $106,000.** The round figure was a floor from a public
  statement; the 2017 *People, Dogs & Parks Plan* costs it at $106,000/year through 2020
  (p. 19), with a range of $103,000–$117,000 (pp. 3, 5).

### Added

- **Budget finding: appropriated vs spent.** $1,053,037 of a $5,625,926 revised budget across
  2023 to 7 July 2026, 18.7%, leaving $4,362,265. Burn by year: 75.7%, 50.4%, 20.6%, 5.0%.
  The page states both cautions: 2026 is a partial year, and P-Patch burns at 32.0% against
  OLA's 34.2% over the closed years, so this is not a claim of uniquely poor execution.
- **`data/ola-ppatch-master-projects.csv`** — per-year, per-Master-Project adopted budget,
  revised budget, expenses, encumbrances and available balance. The tables arrived as embedded
  EMF images inside the .docx and were recovered from the EMF text records; the method is in
  the archive README.
- **`docs/data-methods.html`** — tenth public page, holding the primary-data list, the
  methodology, and every page's data notes.

### Changed

- `budget-detail.csv` drops `one_time_capital_k` and `capital_source`; the capital is not
  separate from the BSL. `ola_only_k` is now a **declared cache** of the Master Project file
  for 2023+ and of the 2017 plan for 2016–18, with the refresh path written at the column.
  `ola_ppatch_combined_k` is blanked for 2016–18, where no joint line was reported.
- `seattle-timeseries.csv` splits `ola_improvement_budget_k`, which held OLA-only for 2016–18
  and the *combined* figure from 2019 on under a name that read as OLA-only throughout, into
  `ola_only_budget_k` and `ola_ppatch_combined_k`.
- `verify_site_data.py` gains an `absent()` helper and guards for the new figures, the
  Master-Project row identities, the sum-to-BSL identity, the burn rates, and the
  measure-dependence claim. The basis-point peak moves from 6.4 bp (2016) to 46.2 bp (2025).

## [1.2.0] — 2026-09-13

A second full-site audit ([`SITE-AUDIT-2026-09.md`](SITE-AUDIT-2026-09.md)) found the
arithmetic sound and three headline claims wrong. This release corrects them, ingests the July
2026 records release (PRR C266465), splits citations from warnings, and cuts every page to its
finding. Nothing in the underlying citation, walkshed, or budget data changed.

### Corrections (stated plainly)

- **"Zero net OLAs since 2009, seventeen years" was wrong.** SPR's own *People, Dogs & Parks
  Plan* (Aug 2017) dates the last openings to 2012–13 (Denny, Magnolia Manor, Kinnear) and
  puts the 2010 count at 11, not 14. `seattle-olas.csv` `year_opened` now follows the plan
  on 12 of 14 rows (the old values came from unarchived SPR park pages), with a new
  `year_permanent` column (Kinnear 2014, Magnolia Manor 2015). The headline is now
  **thirteen years, since 2013**; the 2010 residents-per-OLA baseline moves from 43,476 to
  55,333, so "+34% since 2010" becomes +16% since 2016.
- **"Two new OLAs open fall 2026" was wrong.** SPR's project pages (archived in
  `sources/spr-ola-project-status-2026.md`) put Othello at fall 2027 and West Seattle
  Stadium at winter 2028; neither is under construction. `planned-olas.csv` status/dates
  and the 2026 time-series row (16 → 14 OLAs) corrected.
- **"The City hasn't spent the three-officer money" was wrong for 2023–24.** SPR's ledger
  (C266465) shows $456,173 billed in 2024 and $226,528 in H1 2023 for three ACOs on
  calendar-derived invoices, while FAS reported capacity for 1.5–2.0. Eight sentences across
  the enforcement, budget, opinion and updates pages said otherwise; all corrected, and the
  opinion page's "$176,000" spend figure removed. Funded ≠ deployed still holds; billed
  tracked funded.
- **"7,015 citations" were 3,151 citations and 3,191 verbal warnings.** Every page now says
  contacts/records for the total and reserves "citation" for `case_result = Citation`.
  Actual citations fell 95% from 2018 to 2024 (441 → 21).
- Smaller corrections: Part II's "two largest deficits are SLU and Queen Anne" (they rank
  10th and 12th by acre shortfall; 1st and 2nd by dogs per acre); Kinnear "smallest"
  (Denny is smaller); amenity counts (water: 1 of 14 per FAS to Council; lighting: 3 per a
  2021 COLA survey); Genesee opened 1999 not 2005; "2019 reporting shift is half the
  jump" (it is about a quarter); the opinion page's "25% of residents use OLAs" (the
  survey covered dog owners only) and "0.06% of the city's land" (0.46% of parkland);
  San Francisco does require dog licenses; Boise fenced-only multiple 1.7×; the 2016
  Mar–Aug ticket count 435 → 543 (recomputed from the citation CSV).

### Cost model (`scripts/build_enforcement_metrics.py`)

- `annual_cost()` is the single owner both verifiers call. 2023–24 use billed actuals
  ($453,056 annualized; $456,173). The paired maintenance worker ($140,000 estimate) ends in
  2022 (vacant from 2023 per SPR memo, Bates 00360). 2025–26 use one officer at the 2025 and
  2026 MOA rates. Fee revenue is summed over DLP-only rows ($294,885, was $351,099).
  Cumulative cost $3.38M (was $3.30M); recovery 8.7%.
- New columns: `cost_basis`, `result_citation`, `result_verbal`, `result_other`,
  `cost_per_actual_citation`.

### Site

- Every page cut to its finding: plain-language headings replace "Finding 0N" (old ids kept),
  duplicated material has one home (playgrounds vs OLAs and Cycle 1/2 on Budget only; NYC
  evidence on Part III; per-capita peers on Part I/Peer Cities), supporting detail moved into
  Data notes. Opinion page cut by about a third and dated September 2026.
- Enforcement page: new "funded / billed / deployed" framing, a citations-vs-warnings chart,
  and a section recording that neither SPR (C266465) nor FAS (C266744) holds any evaluation
  of the program, with SPR's 2024 recommendation to cut it and the February 2025 override.
- Part II adds the FAS Director's 2022 statement to Council on why owners run dogs off
  leash; Part I adds the City's own peer table (1.9 / 4.9 / 6.5 per 100k); Part III adds
  SPR's named gaps (Capitol Hill, Ballard, Northgate) and East Queen Anne Playfield as a
  recommended future site; Budget adds the $1.15M–$2.22M OLA capital backlog.
- Peer Cities: dated recency caveats on Portland's levy and Vancouver's Park Board; sourcing
  note that external facts are linked, not archived.
- `verify_site_data.py` gains guards for opening years, the 2010 baseline, planned-site
  status, the citation/warning split, billed cost, DLP-only revenue, and the retired phrases.
- `licensing-revenue.csv` 2025 carries a "not partial; 1-year-license transition" note;
  `illegal-use-indicators.csv` drops the retired ~1,100 complaint row.

### Infrastructure

- **Basemap moved from CARTO to Esri World Light Gray.** CARTO began burning an
  "API KEY REQUIRED" watermark into its keyless `light_all` tiles in September 2026, so every
  map on the site was serving defaced tiles. All six Leaflet maps now call a single new owner,
  `SDPD.basemap(map, { maxZoom })` in `docs/chart-defaults.js`, which layers Esri's label-free
  Base with its transparent Reference layer in a pane beneath the data overlays. Esri's host was
  already in the Content Security Policy; the dead CARTO host was removed from it and added to
  `DEAD_TILE_HOSTS` in `verify_enforcement_data.py`, so a future page that hard-codes a tile URL
  fails the build.

### New data

- **PRR C266465 (SPR, July 2026)** — program-evaluation, deployment and decision records for
  the "Making Parks Safer" ACO park-patrol program. 112 files / ~720 Bates pages / 90 unique
  documents, archived at `data/prr-responses/C266465/` (17 load-bearing originals plus
  OCR text for all 101 distinct documents). Fulfils [PRR #8](prrs/08-spr-program-evaluation-2016-expansion.md).
  - **No program-effectiveness evaluation exists.** Patrol deployment logs and
    compliance/complaint-trend analysis produced *nothing*. Read with PRR C266744 (the FAS-side
    twin), both custodians have now separately confirmed the absence.
  - **First actual-spend records for the ACO line.** Quarterly ledger backup →
    `data/prr-responses/C266465/documents/enforcement-moa-billing.csv`. FY2024 billed
    **$456,173** for three staff, on invoices computed from a flat 40-hour week rather than
    hours worked. This contradicts a spend figure currently on `docs/opinion.html`.
  - **Complete decision record** for the three-officer program: Council funds two added ACOs
    (Oct 2022) → SPR's own manager recommends cutting to 2 or 1 (Sep 2024) → leadership
    overrides to 3 (Feb 2025) → FAS says it can staff 1.5–2.0 (Feb 2025) → MOA funds "up to
    three … any number of positions" (Jul 2025).
- **`data/enforcement-program-activity.csv`** — SPR/FAS internal contact tracking, 2023–24
  (ACO: 880/586 verbal warnings, 42/28 citations, 0 park exclusions). *Different record system
  from `enforcement-citations.csv`; same shape once `case_result` is read (35/21 citations vs the memo's 42/28), but a different universe of contacts, so the two must not be merged.*
- **`data/moas/SPR-FAS-ACO2-MOA-2025.pdf`** — the missing 2025 agreement, completing the MOA
  series (2016 / 2021 / 2023 / 2025 / 2026). It is the document that introduced the "up to
  three … any number of positions" language and actual-hours billing.

## [1.1.0] — 2026-06-18

Ingests three public-records responses and weaves the new data across the site. The complaint and licensing datasets move from "filed, awaiting response" to primary sources.

### New data and findings

- **Resident complaints (PRR C263990).** Find It Fix It "Nuisance Dogs in a Park" reports — ~3,010 in 2025 (the first full year of the record), roughly 11 per off-leash citation. New Enforcement Finding 07 sets complaint volume against citation output: the two series move independently (monthly r = 0.13), shown as stacked panels rather than a dual-axis chart. A "Complaints 2024–26" column is added to the per-park enforcement table.
- **Dog licensing (PRR C264029).** Annual license issuance fell ~21% over 2014–2025 (24,309 → 19,219); ~26,650 dogs hold current licenses, an estimated 7–18% of the 150,000–400,000 dog population. New Part I licensing/compliance finding; Seattle Animal Shelter confirmed it holds no internal compliance or dog-population estimate.
- **License revenue vs. OLA spending (Budget).** New finding: the city collects ~$1.24M/yr in dog-license fees vs. a ~$129K OLA-only operating budget (~10×), with an explicit cross-department caveat (license revenue funds the Seattle Animal Shelter under FAS, not SPR) — a scale contrast, not an accounting claim.

### Site changes

- **Part II** complaint figure updated (~1,100 → ~3,010, now primary); licensing-trend note added; the citation-vs-walkshed and TPL priority-tier detail moved to the Enforcement page; the 14-row OLA capacity table condensed to prose; Finding 07 summary expanded.
- **Updates page + homepage panel** carry two new June 2026 entries (complaints received; licensing received).
- **Site-wide date** advanced to June 2026 across all public pages.
- **Sub-$1M dollar formatting** standardized to plain dollars (e.g. $100,000 / $126,000 / $129,000) instead of decimal-millions notation.

### Data and scripts

- New datasets: `data/licensing-revenue.csv`, `data/licensing-by-year.csv`, `data/licensing-by-zip.csv`, `data/complaints-citations-monthly.csv`, `data/complaints-vs-citations-by-park.csv`, plus raw PRR responses under `data/prr-responses/C263990/` and `data/prr-responses/C264029/`.
- New build scripts: `scripts/build_licensing_datasets.py`, `scripts/compare_complaints_citations.py`.

## [1.0.0] — 2026-04-19

First complete version. The site is a coherent public-data reference on Seattle's off-leash area system — overview, Part I (The Gap), Part II (Access), Part III (Forward), Enforcement, Budget, Peer Cities, Opinion, and a single-file print PDF — with every factual claim linking back to its source and the underlying dataset pipeline fully reproducible from committed scripts. History tracks forward from here.

### Shipped in 1.0

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

### Methodology and data reconciliation

- **park-coordinates.csv** reconciled to SPR ArcGIS FeatureServer for all 14 OLA host parks (prior data had up to 928m drift on Lower Woodland).
- **seattle-olas.csv** Magnuson year_opened 1998 → 1999 (permanent designation per HistoryLink; 1996 was pilot/trial).
- **peer-cities.csv** `population_year` split into `population_estimate_year` + `metric_reference_year`. Austin provenance corrected: the inflating acreage is Walnut Creek Metropolitan Park (293 ac voice-control), not Red Bud Isle (13 ac).
- **Citation-rate headline** unified across Part II + print to the script output (69.6% / 2,035 of 2,925 park-named; 72.1% / 2,563 of 3,554 combined).
- **Auditing pipeline.** Three third-pass audits committed to `audits/` (`AUDIT-INTERNAL.md`, `AUDIT-INTERNAL-2.md`, `AUDIT-PASS3-2026-04-18.md`, `AUDIT-PART3-2026-04-18.md`). Every SEVERE and MODERATE finding resolved.
- **Data-notes headings** consolidated to just "Data notes" + "Primary sources" across pages (previous "New Data Notes" / "Data Notes & Caveats" / "Primary Sources Added" naming was pre-launch scaffolding).
- **Kinnear/Denny size comparator** "two tennis courts" → "a basketball court" (cleaner, less ambiguous comparator; basketball court is 4,700 sq ft, Denny is 4,574 sq ft, Kinnear is 5,401 sq ft).
- **TPL priority-tier section** rewritten with an explicit explanation of what the Park Priority Index measures (low-income density, POC density, CDC health indicators, heat/environment stress) and what the cross-tab actually asks.
- **"Zero in 17 years"** rationalization replaced the prior "one in fifteen years" prose across Part I hero, Part II takeaway, Opinion P1, index Part I card, and README.

### Fixed during audit passes

- Westcrest 0.5-mi walkshed regression (0.260 km² under tight alpha-shape → 0.765 km² after the area-floor + convex-hull fallback landed).
- NYC Off-Leash Hours press-release URL `?id=19895` → `?id=19877` on Part III and Peer Cities.
- Westcrest OLA renovation scope corrected to the Parkways-blog primary source (drainage / erosion / access / accessibility; $505K from the Park District Major Maintenance Fund, not pure capital).
- Small-dog-area count 2 → 5 (matches seattle-olas.csv: Magnuson, Westcrest, Genesee, Golden Gardens, Magnolia Manor).
- Several 404'd external URLs (Austin PARD, Boise P&R, COLA) replaced with live canonical domains.

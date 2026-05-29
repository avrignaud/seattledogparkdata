# Methodology

How each derived number and chart on [seattledogparkdata.com](https://seattledogparkdata.com) was produced, and how to reproduce it. Every derived dataset in this repo is the output of a documented, re-runnable pipeline. Every primary source has a publicly resolvable URL or a documented public-records-request reference.

This file is the site's "show your work" index. If a number on the site isn't listed here, that's a bug — please [file an issue](https://github.com/avrignaud/seattledogparkdata/issues).

## Source data (inputs)

| File | Origin | How to verify |
|---|---|---|
| [`data/seattle-olas.csv`](data/seattle-olas.csv) | Coordinates pulled April 2026 from SPR's authoritative [Dog Off-Leash Areas ArcGIS feature service](https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Dog_Off_Leash_Areas/FeatureServer/0). Acreages reconciled the same month to each OLA's individual SPR park page. Supersedes earlier address-derived approximations. | Each row maps 1-to-1 to a feature in SPR's ArcGIS dataset; the feature service is the canonical source. |
| [`data/seattle-timeseries.csv`](data/seattle-timeseries.csv) | WA OFM April 1 population estimates; Seattle 2018/2021/2025-26 budget books; Seattle Park District Cycle 1 & 2 financial plans. | Each year's row cites a specific budget-book page or OFM table. |
| [`data/peer-cities.csv`](data/peer-cities.csv) | [Trust for Public Land 2025 ParkScore](https://www.tpl.org/parkscore) city-level PDFs. Vancouver BC from its own [People, Parks & Dogs Strategy](https://vancouver.ca/parks-recreation-culture/people-parks-dogs-strategy.aspx) (2017). | Each row has `parkscore_rank` tying back to TPL's published table. |
| [`data/planned-olas.csv`](data/planned-olas.csv) | Seattle Park District Cycle 2 project pages + 2023–24 OLA Expansion Study. | Each entry cross-references an SPR project page. |
| [`data/kinnear-timeline.csv`](data/kinnear-timeline.csv) | Contemporaneous reporting (Seattle Times, Seattle Weekly, KOMO, Fix Homelessness, dog-owner blogs). Every row has a source column. | Follow the source URL in each row. |
| [`data/illegal-use-indicators.csv`](data/illegal-use-indicators.csv) | SPR owner survey (2016) published in the 2017 [*People, Dogs and Parks Strategic Plan*](https://www.seattle.gov/parks/about-us/policies-and-plans/people-dogs-and-parks-strategic-plan); TPL 2025 ParkScore amenity sub-scores; Seattle Animal Control 6-month ticket figure from published SPR communications. | Each metric has a `source` column. |
| [`data/park-coordinates.csv`](data/park-coordinates.csv) | Per-park centroids used for citation spatial analysis. OLA host-park rows for Westcrest and Genesee were reconciled April 2026 to the SPR ArcGIS OLA point after an audit found ~1.17 km and ~650 m coordinate errors, respectively. Non-OLA parks geocoded by hand from Seattle geography. Every row has a `provenance` column. | For OLA host parks, cross-reference with SPR's ArcGIS feature service. Non-OLA parks cross-reference with SPR's individual park pages. |
| [`data/prr-responses/C049204/*.xlsx`](data/prr-responses/C049204/) | Seattle public records request **C049204**, filed 2019-08-29 by Andre Vrignaud, produced 2019-10-15 by SPR. Covers Animal Control off-leash citations 2014-01-01 through 2019-10-15. Scope: Dog-Loose-in-Park (DLP) violations only. | Original request text preserved in [`data/prr-responses/C049204/README.md`](data/prr-responses/C049204/README.md). Raw XLSX preserved unmodified. |
| [`data/prr-responses/C263949/*.xlsx`](data/prr-responses/C263949/) | Seattle public records request **C263949**, filed 2026-04-17, produced 2026-05-08 through 2026-05-15 by Seattle FAS (Animal Shelter). Covers parks-related Animal Control violations 2019-01-01 through 2026-04-17, four SSRS-exported workbooks. Scope: all parks-related violation types (DLP + license + scoop + permit + vaccinate + other). | Per-file row counts verified against the in-row `Total Violations: N` sentinel that SSRS embeds on every data row. Original request and response preserved in [`data/prr-responses/C263949/README.md`](data/prr-responses/C263949/README.md). |
| [`sources/andre-qacc-thread-2019.md`](sources/andre-qacc-thread-2019.md) | First-person community-thread response by Andre Vrignaud, 2019. Retained for the first-person material on the opinion page and as a data cross-reference index. | Every data claim in the thread is flagged in the file's "needs citation from" table. |
| [`sources/SOURCES.md`](sources/SOURCES.md) | Master list of primary sources cited across the site. | Self-referential — this is the entry point. |

## Derived data (outputs)

These files are built by scripts. Do not hand-edit them — edit the inputs and re-run the script.

### `data/enforcement-citations.csv` and `data/enforcement-by-park-year.csv`

**Script:** [`scripts/build_enforcement_datasets.py`](scripts/build_enforcement_datasets.py)

**Inputs:**
- The five XLSX workbooks in [`data/prr-responses/C049204/`](data/prr-responses/C049204/) — DLP-only, 2014-01-01 through 2019-10-15.
- The four SSRS-exported XLSX workbooks in [`data/prr-responses/C263949/`](data/prr-responses/C263949/) — all parks-related violations, 2019-01-01 through 2026-04-17.

**Process:**
1. Load each C049204 workbook. Each has four sheets — `1st Offense`, `2nd Offense`, `3rd Offense`, `4th Offense` — covering a particular year or year-range. Read header row 0, then every data row.
2. Load each C263949 workbook. Each has one sheet with an SSRS report layout: rows 0–1 are report parameters, row 3 is the data header, row 4 onward is data. Parse by column position (the column map is documented inline in the build script).
3. Each row from either PRR is normalized into a common schema with these key fields: `year`, `offense_level` (1-4 for DLP rows; 0 for non-DLP), `violation_item`, `violation_category` (dog_loose_in_park, license, scoop, permit_at_large, vaccinate, false_statement, voided, other), `dlp_only` (True/False), `district` (new C263949 field), `officer` (new C263949 field), `location_raw`, `location_canon`, `zip`, `issued_at`, `fee`, `case_result`, plus provenance fields (`source_file`, `source_sheet`, `source_prr`).
4. **2019 overlap rule.** Both PRRs contain 2019 rows. C049204's 2019 is Jan 1 – Oct 15, DLP-only; C263949's 2019 is the full year, all categories. The build drops C049204's 2019 rows and treats C263949 as authoritative for 2019. This is logged on stdout when the build runs and asserted by `scripts/verify_enforcement_data.py`.
5. Park-name **canonicalization**: apply an ordered list of case-insensitive regular expressions (see [`CANONICAL_PARKS`](scripts/build_enforcement_datasets.py) in the script) to collapse known spelling variants. First match wins. Rows whose raw location doesn't match any pattern pass through with their raw value as the canonical name. The same map applies to both PRRs.
6. Write the full citation table to `data/enforcement-citations.csv` (one row per violation, 7,532 rows).
7. Aggregate by `(location_canon, year, dlp_only)` and write `data/enforcement-by-park-year.csv`. The `dlp_only` dimension lets downstream consumers request the apples-to-apples DLP series across both PRRs without re-reading the wide CSV.

**Headline data-quality numbers after the May 2026 build:**
- 7,532 all-category violations across 2014-01-01 → 2026-04-17; 7,015 DLP-only across the same window once 2019 is sourced from C263949.
- 3,774 rows from C049204 retained (2014-2018 DLP-only); 1,029 dropped (2019 partial DLP-only, superseded by C263949).
- 3,758 rows from C263949 ingested across four workbooks (1,806 / 758 / 799 / 395). Each file's row count matches its in-row `Total Violations: N` sentinel exactly.
- Fee-tier consistency (DLP-only paid rows): 100% of 1st-offense rows at $54, 100% of 2nd at $109, 100% of 3rd at $136, 100% of 4th+ at $162 — all matching SMC 18.12.080(A).

**Reconciling same location, different descriptions.** Same-location-different-description variants are collapsed via explicit regex patterns in the script, reviewable per-line. Examples:

| Canonical | Raw-string variants observed |
|---|---|
| Magnuson Park | 6+ — "Warren G Magnuson Park", "Warren G. Magnuson Park", "Magnuson park", etc. |
| Alki Beach Park | 6+ — "Alki Beach @ 52nd Ave SW", "Alki Beach near 53rd Av SW", "Alki Beach Park", etc. |
| Woodland Park | 5+ — "Lower Woodland Park ball field", "Woodland Park Off-Leash", "woodland park", etc. This fold is *intentionally lossy*: the raw records don't reliably distinguish citations inside the Lower Woodland OLA (0.75 ac) from citations in the rest of the larger Woodland Park. Classified as "partial" on the map. |
| West Queen Anne Playfield | 3+ — "W. Queen Anne Playfield", "West Queen Anne Playfield", "W Queen Anne Playfield" |

**Reproduce + verify:**
```
python3 -m venv .venv
.venv/bin/pip install openpyxl
.venv/bin/python3 scripts/build_enforcement_datasets.py
.venv/bin/python3 scripts/verify_enforcement_data.py
```
The build prints a verification summary. The separate verifier asserts ~120 invariants across raw XLSX, consolidated CSV, the four small derived CSVs, and the per-year metrics CSV. Both should exit 0; if not, open an issue.

### `data/enforcement-year-metrics.csv`

**Script:** [`scripts/build_enforcement_metrics.py`](scripts/build_enforcement_metrics.py)

**Input:** `data/enforcement-citations.csv` plus the staffing + cost model defined in the script.

**Process:** For each year 2014–2026, computes DLP citations, all-category citations, the assumed ACO+FMW FTE, annual program cost, cost per citation, citations per FTE, first-offense share, repeat-offense share, and assessed fee revenue. The staffing FTE schedule and the FMW cost estimate ($140K/yr) are **assumptions** stated explicitly in the script header; the FAS-side ACO II cost ($152,399/yr) is sourced from the 2021 MOA. 2026 is a partial year (through April 17): its `cost_per_citation` and `citations_per_fte` are emitted blank and `partial_year=true`, because the partial-year denominator would inflate those ratios.

**Honest-use note:** Pre-2016 cost and FTE are imputed (part-time staffing, no documented cost basis). The enforcement page therefore begins the cost-per-citation and per-FTE charts at **2016** — the first MOA-documented year — while the raw citation-volume charts keep the full 2014–2026 history. The metrics CSV still emits the pre-2016 rows (they are accurate given the stated assumption), but downstream charts treat them as not directly comparable.

**Reproduce + verify:**
```
.venv/bin/python3 scripts/build_enforcement_metrics.py
.venv/bin/python3 scripts/verify_enforcement_data.py
```
The verifier recomputes every metric from the consolidated CSV + the model and asserts equality, plus cross-checks the cumulative cost (~$3.34M), revenue ($351,099), and cost-recovery (10.5%) headline figures.

### `data/walkshed/citation-rate-by-walkshed-status.csv`

**Script:** [`scripts/citation_walkshed_analysis.py`](scripts/citation_walkshed_analysis.py)

**Input:** `data/walkshed/ola_isochrones.geojson`, `data/enforcement-citations.csv`, `data/park-coordinates.csv`.

**Classification rule (explicit):** for each uniquely-named park that appears in the citation data with `location_type == 'park_named'`, the script looks up its single lat/lng in `data/park-coordinates.csv` and tests whether the UNION of all 0.5-mile OLA isochrone polygons `.contains()` that point. No buffer, no tolerance, no block-group or centroid step. A park is "inside walkshed" iff that point-in-polygon test returns True.

**Reproduce:**
```
.venv/bin/python3 scripts/citation_walkshed_analysis.py
```
Output should byte-match the committed CSV; if it doesn't, open an issue.

## Charts and page-level methodology

### Part I: The Gap

| Chart | Methodology notes |
|---|---|
| Residents per OLA, 2010–2026 | Population from OFM April 1 estimates; OLA count from `seattle-olas.csv` + `planned-olas.csv` for 2026 projection (16 OLAs). Simple division, `seattle-timeseries.csv` pre-computes. |
| Dog parks per 100K residents | TPL 2025 ParkScore city PDFs. Vancouver BC from its own Park Board strategy doc (not in ParkScore because it's in Canada). |
| Park investment vs. dog-park density scatter | TPL 2025 ParkScore three-year average spending. |
| SPR total budget vs. OLA improvement | 2018 General Fund + operating number ($168M); 2019+ all-funds ("Maintaining Parks and Facilities" BSL BC-PR-50000). Note: post-2022 numbers are combined OLA+P-Patch and overstate OLA-specific spending. Separation request in `prrs/03-spr-ola-budget-split.md`. |
| OLA improvement spending by Cycle | Same source as above. |
| Playgrounds vs OLAs | TPL 2025 ParkScore (157 playgrounds in Seattle); OLA count from `seattle-olas.csv`; kids count from OFM estimate; dogs = 150K floor from Seattle Humane/Cascade PBS. |
| OLA acreage concentration | `seattle-olas.csv`. Acreage estimates vary ±10% across sources; midpoint used. |

### Part II: Access

| Chart | Methodology notes |
|---|---|
| 10-minute walkshed coverage | 99% figure from [TPL 2025 ParkScore Seattle](https://www.tpl.org/city/seattle-washington) — formal network-based walkshed. OLA figure is repo-computed: **11.7%** at 10-min (0.5-mi) network walk, **76.6%** at SPR's published 2.5-mi standard, both population-weighted. Pipeline: `scripts/compute_walkshed.py` runs [osmnx](https://github.com/gboeing/osmnx) against Seattle's OpenStreetMap walk network (110,383 nodes · 305,582 edges, projected to UTM 10N, physical barriers respected). For each OLA it seeds a multi-source ego-graph traversal from every network node within 100 m of the OLA's SPR ArcGIS coordinate (rather than a single nearest node — that single-seed approach produced malformed hulls at OLAs on the edge of the walk network), builds an **alpha-shape** of the reachable-node cloud plus the OLA's own point at `alpha=0.003` (tight enough to hug the walk-network's actual concavities instead of bridging them the way a convex hull would, loose enough to avoid holes on sparse point clouds), and unions the resulting polygon with a 25 m buffer around the OLA point as a safety net. Alpha-shape shrinks each isochrone by 1–2 percentage points of city-wide coverage vs. the earlier convex-hull version. `scripts/population_coverage.py` intersects the union of isochrones with 2020 Census block-group geometry (TIGER 2020 via [pygris](https://walker-data.com/pygris/)) clipped to the Seattle city Places boundary, attributes population area-weighted. Output: `data/walkshed/population_coverage.csv`. The alpha-shape step (alpha=0.003) hugs walk-network concavities instead of bridging them the way the earlier convex-hull implementation did. This shrinks each isochrone by roughly a percentage point on city-wide coverage — the 11.7% figure is the post-alpha-shape number. Supersedes the earlier straight-line 33% author estimate. |
| Seattle OLA coverage map | OLA coords from `seattle-olas.csv` (authoritative SPR ArcGIS). Walkshed polygons are the network-derived 0.5-mi isochrones from `data/walkshed/ola_isochrones.geojson` (output of `scripts/compute_walkshed.py`). Planned/future sites fall back to straight-line half-mile circles because their isochrones are not yet computed. |
| Peer-city OLA acreage per 10K | Per-city acreage from municipal inventories (SPR, Portland P&R, SF Rec & Parks, Vancouver Park Board). Methodology caveat callout explicitly flags that city definitions differ (fenced vs. unfenced, time-restricted vs. dedicated). |
| Dog-park-size standards | [AKC 1-acre recommendation](https://images.akc.org/pdf/GLEG01.pdf); [Parks & Rec Business industry guidance](https://www.parksandrecbusiness.com/articles/2011/08/01/designing-dog-parks); [Ann Arbor](https://www.a2gov.org/media/hvqhrksg/recommendations-and-guidelines-for-dog-park-site-selection-updated-4-10-15.pdf) and [Fairfax County](https://www.fairfaxcounty.gov/parks/sites/parks/files/assets/documents/plandev/dog%20park%20study/dog%20park%20study%20appendices.pdf) municipal design guidelines; 75–100 sq ft per dog capacity standard from [Dog Park Size Guide](https://outdoorworkoutsupply.com/blogs/ows-blog/dog-park-size-guide-square-footage-requirements-by-facility-type-and-dog-capacity). Capacity table: area in sq ft = acres × 43,560; capacity = area / sq-ft-per-dog. |

### Enforcement

| Chart | Methodology notes |
|---|---|
| Hotspot circle-marker map | `HOTSPOTS` data embedded in the HTML; derived from `enforcement-by-park-year.csv` + `park-coordinates.csv`. Marker radius = `max(6, sqrt(count) × 1.6)`. |
| Walkshed-gap heatmap | [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat) kernel density estimate. Points: top-40 geocoded parks (HOTSPOTS + HEATMAP_EXTRA arrays in `enforcement.html`), weighted by citation count. Walksheds on the enforcement-page gap map are still straight-line circles (legacy); the newer merged Part II map uses the network isochrones from `data/walkshed/ola_isochrones.geojson`. |
| Top-20 cited parks | Direct aggregate from `enforcement-by-park-year.csv`. |
| Citations per year | Direct aggregate from `enforcement-by-park-year.csv`. 2019 is now a full year (sourced from C263949 under the overlap rule). 2026 is the partial year (Jan 1 – Apr 17, day 107, ~29%); its annualized equivalent = count ÷ 0.293, shown as a dashed marker, not treated as actual. |
| Offense-mix | Derived counts from `enforcement-citations.csv` grouped by `offense_level`. Fees per offense level reference SMC 18.12.080(A). |

### Editorial (opinion.html)

The opinion page is clearly marked as author opinion. Every factual claim inside it links back to:
- A factual page on this site, or
- A primary-source URL (SPR plan, SMC, TPL methodology), or
- An explicit data-gap callout if a citable source is not yet on hand.

No bare numbers appear without one of the above.

## Methodology upgrades — completed + planned

**Completed**

1. **Network walkshed in Python (April 2026).** Implemented at `scripts/compute_walkshed.py` + `scripts/population_coverage.py`. Replaces the earlier straight-line 33% straight-line estimate with population-weighted network-distance figures: 11.7% at 10-min / 0.5-mi, 76.6% at SPR's 2.5-mi, using 2020 Census block-group population. Output at `data/walkshed/population_coverage.csv` + `data/walkshed/ola_isochrones.geojson`.

**Planned (priority order)**

1. **Alpha-shape refinement of the walkshed isochrones.** COMPLETED: the walkshed pipeline uses an alpha-shape of reachable-node clouds (α=0.003) rather than a convex hull, with a 0.3 km² area floor and a convex-hull fallback for any OLA at the edge of OSM coverage (Westcrest is the one that trips this). Alpha-shape hugs walk-network concavities, shrinking each isochrone vs. convex-hull by roughly a percentage point on city-wide coverage. The 11.7% figure is the post-alpha-shape number.
2. **Geocoding pass on the 672 street-address rows** in `enforcement-citations.csv`. Use an offline pipeline (US Census Geocoder API or Seattle's address points dataset) + spatial join against Seattle's park-boundary polygon layer. Could recover a meaningful share of the currently-excluded 14% of citations.
3. **Dog population update.** Replace the 150,000 conservative floor with a defensibly current number from AVMA state estimates or King County license data (PRR if necessary).
4. **OLA-only budget split** via `prrs/03-spr-ola-budget-split.md`. Separate OLA from P-Patch in the post-2022 "Maintaining Parks & Facilities" BSL.
5. **FIFI complaint trend** via `prrs/02-spu-fifi-dog-complaints.md`. Replace the approximate ~1,100/year figure.

## Repository conventions

- All inputs are plain CSVs or primary XLSX responses; no binary build artifacts.
- All derived outputs are rebuildable from the inputs by scripts in `scripts/`.
- Pages are static HTML + vanilla CSS + CDN-loaded Chart.js / Leaflet; no build step.
- Every chart has a `chart-source` line at the bottom linking to the underlying data and the method.
- Every derived number on a page is reproducible by reading the cited CSV.

If you want to verify any claim on this site:
1. Find the claim on a page.
2. Follow the `source` link under the chart (or the inline link in prose) to the CSV.
3. If the CSV is derived, follow the script reference here to regenerate it.
4. If the number still looks wrong, [open an issue](https://github.com/avrignaud/seattledogparkdata/issues) — the site will be updated.

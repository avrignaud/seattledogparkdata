# Methodology

How each derived number and chart on [seattledogparkdata.com](https://seattledogparkdata.com) was produced, and how to reproduce it. Every derived dataset in this repo is the output of a documented, re-runnable pipeline. Every primary source has a publicly resolvable URL or a documented public-records-request reference.

This file is the site's "show your work" index. If a number on the site isn't listed here, that's a bug — please [file an issue](https://github.com/avrignaud/seattledogparkdata/issues).

## Source data (inputs)

| File | Origin | How to verify |
|---|---|---|
| [`data/seattle-olas.csv`](data/seattle-olas.csv) | Derived from SPR's individual OLA pages under [seattle.gov/parks](https://www.seattle.gov/parks) and [Citizens for Off-Leash Areas](https://seattlecola.org) biennial reports. Coordinates geocoded by hand from addresses. | Each row maps to a named park; cross-reference with the SPR page for each. Not canonical GIS; use Seattle's [ArcGIS Open Data portal](https://data-seattlecitygis.opendata.arcgis.com/) for authoritative geometry. |
| [`data/seattle-timeseries.csv`](data/seattle-timeseries.csv) | WA OFM April 1 population estimates; Seattle 2018/2021/2025-26 budget books; Seattle Park District Cycle 1 & 2 financial plans. | Each year's row cites a specific budget-book page or OFM table. |
| [`data/peer-cities.csv`](data/peer-cities.csv) | [Trust for Public Land 2025 ParkScore](https://www.tpl.org/parkscore) city-level PDFs. Vancouver BC from its own [People, Parks & Dogs Strategy](https://vancouver.ca/parks-recreation-culture/peoples-parks-and-dogs-strategy.aspx) (2017). | Each row has `parkscore_rank` tying back to TPL's published table. |
| [`data/planned-olas.csv`](data/planned-olas.csv) | Seattle Park District Cycle 2 project pages + 2023–24 OLA Expansion Study. | Each entry cross-references an SPR project page. |
| [`data/kinnear-timeline.csv`](data/kinnear-timeline.csv) | Contemporaneous reporting (Seattle Times, Seattle Weekly, KOMO, Fix Homelessness, dog-owner blogs). Every row has a source column. | Follow the source URL in each row. |
| [`data/illegal-use-indicators.csv`](data/illegal-use-indicators.csv) | SPR owner survey (2016) published in the 2017 [*People, Dogs and Parks Strategic Plan*](https://www.seattle.gov/parks/about-us/policies-and-plans/people-dogs-and-parks-strategic-plan); TPL 2025 ParkScore amenity sub-scores; Seattle Animal Control 6-month ticket figure from published SPR communications. | Each metric has a `source` column. |
| [`data/park-coordinates.csv`](data/park-coordinates.csv) | Geocoded by hand from Seattle park names appearing in the enforcement data. City-scale approximate — not GIS-precise. | For the 14 OLAs, cross-reference with SPR's individual park pages. Non-OLA parks geocoded by author from Seattle geography. |
| [`data/prr-responses/C049204/*.xlsx`](data/prr-responses/C049204/) | Seattle public records request **C049204**, filed 2019-08-29 by Andre Vrignaud, produced 2019-10-15 by SPR. Covers Animal Control off-leash citations 2014-01-01 through 2019-10-15. | Original request text preserved in [`data/prr-responses/C049204/README.md`](data/prr-responses/C049204/README.md). Raw XLSX preserved unmodified. Anyone can file their own PRR to independently verify; see `prrs/01-spr-offleash-citations-post-2019.md` for an extension request format. |
| [`sources/andre-qacc-thread-2019.md`](sources/andre-qacc-thread-2019.md) | First-person community-thread response by Andre Vrignaud, 2019. Retained for the first-person material on the opinion page and as a data cross-reference index. | Every data claim in the thread is flagged in the file's "needs citation from" table. |
| [`sources/SOURCES.md`](sources/SOURCES.md) | Master list of primary sources cited across the site. | Self-referential — this is the entry point. |

## Derived data (outputs)

These files are built by scripts. Do not hand-edit them — edit the inputs and re-run the script.

### `data/enforcement-citations.csv` and `data/enforcement-by-park-year.csv`

**Script:** [`scripts/build_enforcement_datasets.py`](scripts/build_enforcement_datasets.py)

**Input:** The five XLSX workbooks in `data/prr-responses/C049204/`.

**Process:**
1. Load each workbook. Each has four sheets — `1st Offense`, `2nd Offense`, `3rd Offense`, `4th Offense` — covering a particular year or year-range.
2. Iterate every row. Extract: date/time, offense level, fee, case result, raw location string, zip code, source file+sheet.
3. Park-name **canonicalization**: apply an ordered list of case-insensitive regular expressions (see [`CANONICAL_PARKS`](scripts/build_enforcement_datasets.py) in the script) to collapse known spelling variants. First match wins. Rows whose raw location doesn't match any pattern pass through with their raw value as the canonical name.
4. Write the full citation table to `data/enforcement-citations.csv` (one row per citation, 4,803 rows).
5. Aggregate by `(location_canon, year)` and write `data/enforcement-by-park-year.csv`.

**Data-quality summary** (output of the verification step of the script):
- **4,803 total citations** across 2014-01-01 → 2019-10-15.
- **854 unique raw address strings** collapse to **811 unique canonical names** after regex reconciliation.
- **2,679 citations (55.8%)** folded into one of the 43 canonical named-park entries (e.g. "Warren G. Magnuson Park" and "Magnuson park" both → "Magnuson Park").
- **1,341 citations (27.9%)** pass through as named parks that the canonicalizer didn't know about — these are smaller, less-cited parks; they still appear in the aggregate CSV under their as-recorded names.
- **672 citations (14.0%)** have a street address rather than a park name. These are excluded from per-park counts and the hotspot map. They remain in `enforcement-citations.csv` under `location_raw`.
- **111 citations (2.3%)** have a blank location field. These are lost for spatial analysis but still count in the year trend and offense-level breakdown.
- **Combined, 16.3% of citations (783 rows)** are not spatially attributable. The hotspot/heatmap analysis covers the remaining **4,020 citations (83.7%)**.

**Reconciling same location, different descriptions.** Same-location-different-description variants are collapsed via explicit regex patterns in the script, reviewable per-line. Examples:

| Canonical | Raw-string variants observed |
|---|---|
| Magnuson Park | 6 — "Warren G Magnuson Park", "Warren G. Magnuson Park", "Magnuson park", etc. |
| Alki Beach Park | 6 — "Alki Beach @ 52nd Ave SW", "Alki Beach near 53rd Av SW", "Alki Beach Park", etc. |
| Woodland Park | 5 — "Lower Woodland Park ball field", "Woodland Park Off-Leash", "woodland park", etc. This fold is *intentionally lossy*: the raw records don't reliably distinguish citations inside the Lower Woodland OLA (0.75 ac) from citations in the rest of the larger Woodland Park. Classified as "partial" on the map. |
| West Queen Anne Playfield | 3 — "W. Queen Anne Playfield", "West Queen Anne Playfield", "W Queen Anne Playfield" |

Only 43 of the 811 canonical entries required multi-variant reconciliation; the other 768 came through the raw data with a single spelling.

**Reproduce:**
```
python3 -m venv .venv
.venv/bin/pip install openpyxl
.venv/bin/python3 scripts/build_enforcement_datasets.py
```
The output CSVs should byte-match the versions in the repo. If they don't, something upstream changed; open an issue.

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
| 10-minute walkshed coverage | 99% figure from [TPL 2025 ParkScore Seattle](https://www.tpl.org/city/seattle-washington) — formal network-based walkshed. OLA figure is repo-computed: **9.5%** at 10-min (0.5-mi) network walk, **78.3%** at SPR's published 2.5-mi standard, both population-weighted. Pipeline: `scripts/compute_walkshed.py` runs [osmnx](https://github.com/gboeing/osmnx) against Seattle's OpenStreetMap walk network (110,383 nodes · 305,582 edges, projected to UTM 10N, physical barriers respected) and builds per-OLA isochrones as convex hulls of reachable network nodes; `scripts/population_coverage.py` intersects the union of isochrones with 2020 Census block-group geometry (TIGER 2020 via [pygris](https://pygris.readthedocs.io/)) clipped to the Seattle city Places boundary, attributes population area-weighted. Output: `data/walkshed/population_coverage.csv`. The convex-hull step tends to slightly overstate walkable area at the boundary of each OLA's reach; a true alpha-shape or TPL ParkServe-equivalent computation would likely shift the 9.5% figure a percentage point or two down. Supersedes the earlier straight-line 33% author estimate. |
| Seattle OLA coverage map | OLA coords from `seattle-olas.csv`. 0.5-mile walksheds are straight-line circles (`L.circle` with `radius: 804.67` meters). Label "actual walksheds are smaller in practice" is prominent in the chart subtitle. |
| Peer-city OLA acreage per 10K | Per-city acreage from municipal inventories (SPR, Portland P&R, SF Rec & Parks, Vancouver Park Board). Methodology caveat callout explicitly flags that city definitions differ (fenced vs. unfenced, time-restricted vs. dedicated). |
| Dog-park-size standards | [AKC 1-acre recommendation](https://images.akc.org/pdf/GLEG01.pdf); [Parks & Rec Business industry guidance](https://www.parksandrecbusiness.com/articles/2011/08/01/designing-dog-parks); [Ann Arbor](https://www.a2gov.org/media/hvqhrksg/recommendations-and-guidelines-for-dog-park-site-selection-updated-4-10-15.pdf) and [Fairfax County](https://www.fairfaxcounty.gov/parks/sites/parks/files/assets/documents/plandev/dog%20park%20study/dog%20park%20study%20appendices.pdf) municipal design guidelines; 75–100 sq ft per dog capacity standard from [Dog Park Size Guide](https://outdoorworkoutsupply.com/blogs/ows-blog/dog-park-size-guide-square-footage-requirements-by-facility-type-and-dog-capacity). Capacity table: area in sq ft = acres × 43,560; capacity = area / sq-ft-per-dog. |

### Enforcement

| Chart | Methodology notes |
|---|---|
| Hotspot circle-marker map | `HOTSPOTS` data embedded in the HTML; derived from `enforcement-by-park-year.csv` + `park-coordinates.csv`. Marker radius = `max(6, sqrt(count) × 1.6)`. |
| Walkshed-gap heatmap | [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat) kernel density estimate. Points: top-40 geocoded parks (HOTSPOTS + HEATMAP_EXTRA arrays in `enforcement.html`), weighted by citation count. Walksheds: 0.5-mile (804.67 m) straight-line circles around each of the 14 existing OLAs. |
| Top-20 cited parks | Direct aggregate from `enforcement-by-park-year.csv`. |
| Citations per year | Direct aggregate from `enforcement-by-park-year.csv`. 2019 is partial (Jan 1 – Oct 15, 288 days); naive annualization = count × 365 / 288. |
| Offense-mix | Derived counts from `enforcement-citations.csv` grouped by `offense_level`. Fees per offense level reference SMC 18.12.080(A). |

### Editorial (opinion.html)

The opinion page is clearly marked as author opinion. Every factual claim inside it links back to:
- A factual page on this site, or
- A primary-source URL (SPR plan, SMC, TPL methodology), or
- An explicit data-gap callout if a citable source is not yet on hand.

No bare numbers appear without one of the above.

## Methodology upgrades — completed + planned

**Completed**

1. **Network walkshed in Python (April 2026).** Implemented at `scripts/compute_walkshed.py` + `scripts/population_coverage.py`. Replaces the earlier straight-line 33% straight-line estimate with population-weighted network-distance figures: 9.5% at 10-min / 0.5-mi, 78.3% at SPR's 2.5-mi, using 2020 Census block-group population. Output at `data/walkshed/population_coverage.csv` + `data/walkshed/ola_isochrones.geojson`.

**Planned (priority order)**

1. **Alpha-shape refinement of the walkshed isochrones.** Current implementation uses convex hulls of reachable network nodes, which slightly overstates walkable area near OLA boundaries. An alpha-shape or ParkServe-equivalent computation would tighten this. Would shift the 9.5% figure a percentage point or two down.
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

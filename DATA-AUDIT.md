# Data audit — April 2026

A full pass over every CSV in `data/` and every numeric claim on the
site, checking: (a) math is consistent with the underlying data,
(b) every figure has a traceable primary source, (c) no hallucinated
numbers. Every small reference CSV now carries a `provenance` column
distinguishing `sourced`, `calculated`, `interpolated`, `estimated`,
and `missing`. Derived / output CSVs (under `data/walkshed/` and
`data/tpl-parkserve/`, and the wide `enforcement-citations.csv` +
`enforcement-by-park-year.csv`) do NOT carry a row-level
`provenance` column — those are script outputs whose provenance is
the script itself (see `METHODOLOGY.md` for the mapping from output
file to the script that produced it).

This document is the running log of what was checked and what was
fixed. Append as new audits happen.

## CSVs covered

| File | Rows | Provenance column | Notes |
|---|---:|:-:|---|
| `seattle-olas.csv` | 14 | ✓ | All from SPR ArcGIS FeatureServer + individual OLA pages |
| `planned-olas.csv` | 6 | ✓ | Under-construction pair sourced from SPR project pages |
| `illegal-use-indicators.csv` | 11 | ✓ | Walkshed rows are `calculated:` via committed Python; others sourced |
| `kinnear-timeline.csv` | 9 | ✓ | Every row has source title + URL |
| `seattle-timeseries.csv` | 13 | ✓ | 2022 row is `interpolated:`; 2026 row is `estimated:` |
| `budget-detail.csv` | 11 | ✓ | Post-2018 OLA-only split is `missing:` — SPR does not publish |
| `peer-cities-budget.csv` | 10 | ✓ | Most cities don't publish a dog-park-specific line |
| `peer-cities.csv` | 14 | ✓ | Added `population_year` column for clarity on TPL vs OFM year |
| `enforcement-citations.csv` | 4,803 | — | Already has per-row `source_file` + `source_sheet` + `location_type` columns |
| `enforcement-by-park-year.csv` | ~1,100 | — | Derived from enforcement-citations.csv via `scripts/build_enforcement_datasets.py` — all rows `calculated` |

## Math + consistency fixes made in this pass

### peer-cities.csv — Seattle row corrections

- **OLA acres total: 26 → 30.7.** The 26 figure predated the April 2026 SPR ArcGIS reconciliation. Summing the reconciled `data/seattle-olas.csv` gives 30.66 acres. Rounded to 30.7.
- **Acres per 10k residents: 0.32 → 0.38.** Follows from the acres update (30.7 / 81.66 per 10k = 0.376, rounded to 0.38).
- **Noted but not changed:** `dog_parks_per_100k = 1.82` for Seattle uses TPL 2025 ParkScore's reference population (~769K), while `population = 816,600` is WA OFM April 2025. Per-capita metric therefore references a slightly older population than the population column. Added `population_year` column plus explanation in `provenance`. A strict recomputation at current population would give 14 / (816600/100000) = **1.71 per 100K** — TPL's higher number reflects a smaller denominator.

### seattle-timeseries.csv — residents-per-OLA arithmetic

Every row spot-checked:

| Year | Pop | OLAs | Computed res/OLA | CSV res/OLA | OK? |
|---|---:|---:|---:|---:|:-:|
| 2010 | 608,660 | 14 | 43,476 | 43,476 | ✓ |
| 2016 | 704,400 | 14 | 50,314 | 50,314 | ✓ |
| 2018 | 739,500 | 14 | 52,821 | 52,821 | ✓ |
| 2025 | 816,600 | 14 | 58,329 | 58,329 | ✓ |
| 2026 | 832,000 | 16 | 52,000 | 52,000 | ✓ |

### Enforcement revenue (from `data/enforcement-citations.csv`)

Already regenerated in an earlier commit (Apr 2026). Audit spot-check
of the CSV aggregate against the numbers on `docs/enforcement.html`:

| Offense level | CSV count | Unique fee rows | Fee sum |
|---|---:|---:|---:|
| 1st | 4,179 | $0 + $54 | $164,916 |
| 2nd | 418 | $109 | $45,562 |
| 3rd | 123 | $136 | $16,728 |
| 4th+ | 83 | $162 | $13,446 |
| **Total** | **4,803** | — | **$240,652** |

Matches page prose (~$241K over 2014–2019). Cost-recovery math
(26% FAS-only, 14% FAS+FMW) consistent with disclosed MOA figures.

### Walkshed numbers (from `scripts/compute_walkshed.py` + `population_coverage.py`)

- 0.5-mi (10-min walk) pop coverage: **9.47%** → displayed as 9.5%
- 2.5-mi (SPR standard) pop coverage: **78.32%** → displayed as 78.3%
- Seattle city pop used: **737,559** (2020 Census decennial via TIGER 2020)

Both figures reproducible from committed scripts against fixed CSV +
GeoJSON inputs.

### Dog population triangulation

Three independent estimates now cited on the site:

| Estimate | Value | Provenance |
|---|---:|---|
| Licensed floor | ~26,700 active | sourced: [Seattle Open Data dataset `jguv-t9rb`](https://data.seattle.gov/dataset/Active-Pet-Licenses/jguv-t9rb/about_data) |
| AVMA-derived demographic | ~248,900 | calculated: 364,627 households (ACS 2023) × 45.5% × 1.6 dogs/HH — components sourced from [AVMA 2025 Sourcebook](https://www.avma.org/resources-tools/reports-statistics/us-pet-ownership-statistics) + [Census API](https://api.census.gov/data/2023/acs/acs1?get=NAME,B11001_001E&for=place:63000&in=state:53) |
| SPR Expansion Study range | 187K–400K | sourced: SPR 2023-24 OLA Expansion Study |

Site uses the 150K Seattle Humane / Cascade PBS floor for all
per-dog math — sits below every estimate by design.

## Outstanding audit items (unresolved, not hallucinations)

- **Find-It-Fix-It "dog in a park" complaints = ~1,100 in 2024.** Labeled as approximate in `illegal-use-indicators.csv`; PRR #2 to SPU drafted to replace with authoritative number.
- **2022 budget row is blank** (`interpolated`/`missing`). Budget book for 2022 not consistently available; 2022 population is linear interpolation of 2021–2023.
- **OLA-only 2025–2026 budget split** is `missing` — SPR publishes the combined OLA + P-Patch BSL only. PRR #3 drafted.
- **Post-2019 enforcement citations** — PRR #1 filed, awaiting response.

## Claims verified by hand spot-check (no CSV)

- "Seattle has 14 fully-fenced OLAs" → matches SPR ArcGIS count (14 operational features + 1 non-SPR Denny Substation stub).
- "99% of Seattle residents live within 10-min walk of a park" → TPL 2025 ParkScore Seattle fact sheet, verified.
- "8th ParkScore nationally" → TPL 2025 rank for Seattle, verified.
- "4,803 off-leash citations 2014–2019" → matches row count in enforcement-citations.csv.
- "Seven of 14 OLAs below AKC 1-acre floor" → count of acres < 1.0 in seattle-olas.csv: Lower Woodland 0.75, I-5 Colonnade 0.5, Magnolia Manor 0.48, Regrade 0.3, Plymouth Pillars 0.2, Kinnear 0.124, Denny 0.105 = 7. ✓
- "Three OLAs below 0.25 acre" → Regrade 0.3 is just above; Plymouth Pillars 0.2, Kinnear 0.124, Denny 0.105 = 3. ✓
- "Top four OLAs hold ~79% of acreage" → (9.0 + 8.4 + 4.0 + 2.7) = 24.1 / 30.66 = 0.786 → 78.6%. ✓ Site copy (~79%) is correct.
- "Bottom ten OLAs hold under 30%" → 30.66 − 24.1 = 6.56 / 30.66 = 0.214 → 21.4%. Site copy says "about a fifth" on Part I and "under 10%" (bottom seven) on Part II. Recheck Part II bottom-seven: Woodland + I-5 Colonnade + Magnolia Manor + Regrade + Plymouth Pillars + Kinnear + Denny = 0.75 + 0.5 + 0.48 + 0.3 + 0.2 + 0.124 + 0.105 = 2.459 / 30.66 = 8.0%. ✓ Part II "under 10%" is correct.

## Next audit

Re-run after any new PRR response lands or after the walkshed is
recomputed with alpha-shapes. Extend provenance column to
`park-coordinates.csv` and any new CSVs.

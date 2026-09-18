# Seattle Off-Leash Areas: A Data Story

Data-driven research on Seattle's 14 designated off-leash areas (OLAs), how they compare to peer cities, and why a system that serves ~150,000+ dogs with about 30.7 acres of fenced space produces measurable system failures — including rampant illegal off-leash use and one of the worst per-capita dog park ratios on the West Coast.

This is a civic advocacy research project. Everything here is sourced from public data: Seattle Parks & Recreation budget books, the Seattle Park District financial plans, Trust for Public Land ParkScore, WA OFM population estimates, and contemporaneous reporting.

## Findings at a glance

- Seattle has been stuck at **14 OLAs since 2013** (last opening: Kinnear, per SPR's 2017 plan) while population grew **+34%** since 2010. The two funded sites are expected in 2027 and 2028.
- Seattle's dog-park density is **1.82 per 100,000 residents** — one-third of Portland (5.74), SF (5.03), and Vancouver BC (5.44).
- **99% of Seattle residents** live within a 10-minute walk of a park. Only **11.7%** live within a 10-minute network walk of an OLA (repo-computed April 2026; see Methodology).
- Of Seattle's 14 OLAs, **7 are under 1 acre** and **3 are under a quarter-acre**. The smallest (Kinnear) is 0.1 ac.
- SPR's own 2016 survey: **39% of dog owners** admit illegally off-leashing in parks monthly or more often. SPR acknowledges this in its own planning documents as a supply problem.
- Peer-city OLA acreage per 10K residents: Vancouver BC 2.54, Portland 1.29, Seattle **0.38** (6.7× and 3.4× gaps respectively).
- It's **not a money problem** — Seattle spends $418/resident on parks (near the top nationally). Portland spends less and has 3× the dog park density. This is an allocation issue, not a funding issue.
- Park District Cycle 2 (2023–2028) is the first meaningful OLA capital investment since 2013, with $3,103,000 for two new OLAs (West Seattle Stadium, Othello) plus design for a third. SPR released the OLA-only budget in July 2026 (PRR C264837): $328,345 in 2023 rising to about $1.57M in 2025 once that capital lands inside the same budget line. Through 7 July 2026, $1,053,037 of a $5,625,926 revised budget had been spent; construction is now estimated to begin in early 2027.

## The reports

- **[Part I — The Gap](https://seattledogparkdata.com/part1-the-gap.html)** — population growth vs. OLA count, peer-city comparison, budget reality.
- **[Part II — Access](https://seattledogparkdata.com/part2-access.html)** — walkability analysis with interactive Seattle map, peer-city acreage comparison, illegal off-leash use, and the Kinnear Park case study.
- **[Enforcement](https://seattledogparkdata.com/enforcement.html)** — 7,015 Dog-Loose-in-Park (DLP) off-leash citations 2014–2026 (7,532 all-category rows; PRRs C049204 + C263949), year trend, cost-recovery math, walkshed overlay.
- **[Peer cities](https://seattledogparkdata.com/peer-cities.html)** — deeper per-city comparisons against Portland, SF, Vancouver BC, Austin, Boise, and others.
- **[Budget](https://seattledogparkdata.com/budget.html)** — SPR and Seattle Park District line items.
- **[Opinion & Recommendation](https://seattledogparkdata.com/opinion.html)** — clearly marked author recommendations.
- **[PDF report](https://seattledogparkdata.com/seattle-dog-parks-report.pdf)** — all of the above as one file, rebuilt on every content change.

Both render as standalone HTML with Chart.js and Leaflet. No build step, no backend — open the files in a browser, or serve the `docs/` directory.

## Repo layout

```
.
├── docs/                           # Deployed to seattledogparkdata.com (Cloudflare)
│   ├── index.html                  # Landing page
│   ├── part1-the-gap.html          # Population / budget / peer-city analysis
│   ├── part2-access.html           # Walkability, mapping, Kinnear case study
│   ├── enforcement.html            # 7,015 DLP citations 2014–2026, year trend, walkshed overlay
│   ├── peer-cities.html            # Per-city comparison pages
│   ├── budget.html                 # SPR + Park District line items
│   ├── opinion.html                # Clearly-marked author recommendations
│   └── print.html                  # Single-file layout for PDF build
├── data/
│   ├── seattle-olas.csv            # 14 existing OLAs: coordinates (SPR ArcGIS), acreage, neighborhood
│   ├── seattle-timeseries.csv      # Population, SPR budget, OLA budget by year
│   ├── peer-cities.csv             # Portland, SF, Vancouver BC, Austin, Boise, etc.
│   ├── enforcement-citations.csv   # 7,532 all-category rows (7,015 DLP) from PRRs C049204 + C263949 (2014-01 → 2026-04)
│   ├── enforcement-by-park-year.csv
│   ├── kinnear-timeline.csv        # 20-year chronology of Kinnear encampment/safety
│   ├── planned-olas.csv            # Under-construction + planning-phase OLAs
│   ├── park-coordinates.csv        # Canonical coords for every park named in citation data
│   ├── walkshed/                   # osmnx + Census outputs (isochrones, coverage CSVs)
│   ├── tpl-parkserve/              # TPL ParkServe 2025 Seattle slice + OLA cross-tabs
│   └── prr-responses/              # Raw public-records-request workbooks
├── scripts/                        # Reproducible build pipeline
│   ├── build_enforcement_datasets.py
│   ├── compute_walkshed.py
│   ├── population_coverage.py
│   ├── citation_walkshed_analysis.py
│   ├── geocode_street_addresses.py
│   ├── build_tpl_overlay.py
│   └── build-pdf.mjs               # Puppeteer + pdf-lib
├── sources/
│   └── SOURCES.md                  # All primary sources with URLs, organized by category
├── METHODOLOGY.md                  # Single source of truth for derived numbers
├── CHANGELOG.md                    # Version log
├── TODO.md                         # Known gaps / planned work
├── LICENSE                         # MIT
└── README.md
```

## Methodology notes

A few places where I had to estimate or normalize — all documented in the reports' footnotes, but worth highlighting here:

- **11.7% walkshed (Part II, computed April 2026)** — the "residents within a 10-minute walk of an OLA" figure is produced by `scripts/compute_walkshed.py` (osmnx against Seattle's OpenStreetMap walk network, projected to UTM 10N, physical barriers respected) and `scripts/population_coverage.py` (2020 Census block-group overlay clipped to Seattle city boundary, area-weighted). Output at `data/walkshed/population_coverage.csv`. The isochrone uses an alpha-shape of reachable network nodes (α=0.003 with a 100 m multi-seed neighborhood around each OLA and a 0.3 km² area floor that falls back to convex-hull for edge-of-OSM-coverage OLAs like Westcrest), which replaces the earlier convex-hull implementation. Supersedes the earlier ~33% straight-line estimate.
- **Peer-city OLA acreage** — cities define "off-leash area" differently. Portland counts unfenced voice-control areas; Seattle only counts fully fenced. The per-capita gap holds up under several normalization approaches; the specific numbers shift 10-20% depending on methodology. See Part II Finding 04.
- **OLA improvement budget post-2022** — the Park District's "Maintaining Parks & Facilities" BSL funds both OLAs AND P-Patch community gardens, and SPR doesn't publish the split. Numbers after 2022 include both; the OLA share is some fraction smaller.
- **Dog population** — "150,000+" is the conservative figure cited since ~2013. SPR's 2023 Expansion Study cites estimates up to 400,000. I use the conservative floor throughout.

## License

Code and analysis: MIT (see LICENSE).
Underlying data is all from public government sources and is not separately licensed by this project.

## Contact

Project maintained by Andre Vrignaud. Issues and pull requests welcome.

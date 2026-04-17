# Seattle Off-Leash Areas: A Data Story

Data-driven research on Seattle's 14 designated off-leash areas (OLAs), how they compare to peer cities, and why a system that serves ~150,000+ dogs with ~26 acres of fenced space produces measurable system failures — including rampant illegal off-leash use and one of the worst per-capita dog park ratios on the West Coast.

This is a civic advocacy research project. Everything here is sourced from public data: Seattle Parks & Recreation budget books, the Seattle Park District financial plans, Trust for Public Land ParkScore, WA OFM population estimates, and contemporaneous reporting.

## Findings at a glance

- Seattle has been stuck at **14 OLAs since ~2009** while population grew **+34%**. First net increase (to 16) opens fall 2026.
- Seattle's dog-park density is **1.82 per 100,000 residents** — one-third of Portland (5.74), SF (5.03), and Vancouver BC (5.44).
- **99% of Seattle residents** live within a 10-minute walk of a park. Only an estimated **33%** live within 10 minutes of an OLA.
- Of Seattle's 14 OLAs, **7 are under 1 acre** and **4 are under a quarter-acre**. The smallest (Kinnear) is 0.1 ac.
- SPR's own 2016 survey: **39% of dog owners** admit illegally off-leashing in parks monthly or more often. SPR acknowledges this in its own planning documents as a supply problem.
- Peer-city OLA acreage per 10K residents: Vancouver BC 2.54, Portland 1.29, Seattle **0.32** (~8× and ~4× gaps respectively).
- It's **not a money problem** — Seattle spends $418/resident on parks (near the top nationally). Portland spends less and has 3× the dog park density. This is an allocation issue, not a funding issue.
- Park District Cycle 2 (2023–2028) is the first meaningful OLA investment in 15 years: $3.1M capital for two new OLAs plus ~$1.8M/yr operational. Real progress, but still <1% of SPR's total budget, and SPR has said additional OLAs will require future funding requests.

## The reports

- **[Part I — The Gap](https://syrinxventures.github.io/seattle-dog-parks/part1-the-gap.html)** — population growth vs. OLA count, peer-city comparison, budget reality.
- **[Part II — Access](https://syrinxventures.github.io/seattle-dog-parks/part2-access.html)** — walkability analysis with interactive Seattle map, peer-city acreage comparison, illegal off-leash use, and the Kinnear Park case study.

Both render as standalone HTML with Chart.js and Leaflet. No build step, no backend — open the files in a browser.

> Update these URLs after the first GitHub Pages build, or replace `syrinxventures` with your own org/user.

## Repo layout

```
.
├── docs/                           # GitHub Pages publishes from here
│   ├── index.html                  # Landing page linking both reports
│   ├── part1-the-gap.html          # Population / budget / peer-city analysis
│   └── part2-access.html           # Walkability, mapping, Kinnear case study
├── data/
│   ├── seattle-olas.csv            # 14 existing OLAs: coordinates, acreage, neighborhood
│   ├── seattle-timeseries.csv      # Population, SPR budget, OLA budget by year
│   ├── peer-cities.csv             # Portland, SF, Vancouver BC, Austin, Boise, etc.
│   ├── illegal-use-indicators.csv  # SPR survey data, enforcement stats, walkshed
│   ├── kinnear-timeline.csv        # 20-year chronology of Kinnear encampment/safety
│   └── planned-olas.csv            # Under-construction + planning-phase OLAs
├── sources/
│   └── SOURCES.md                  # All primary sources with URLs, organized by category
├── CHANGELOG.md                    # Version log
├── TODO.md                         # Known gaps / planned work
├── LICENSE                         # MIT
└── README.md
```

## Methodology notes

A few places where I had to estimate or normalize — all documented in the reports' footnotes, but worth highlighting here:

- **33% walkshed estimate (Part II)** — the "residents within 10 minutes of an OLA" number is a straight-line half-mile buffer around each OLA's coordinates, overlaid on 2020 Census block groups. TPL uses network analysis that accounts for barriers (I-5, Ship Canal, etc.), which would produce a *smaller* number, not larger. The 33% is the optimistic version.
- **Peer-city OLA acreage** — cities define "off-leash area" differently. Portland counts unfenced voice-control areas; Seattle only counts fully fenced. The per-capita gap holds up under several normalization approaches; the specific numbers shift 10-20% depending on methodology. See Part II Finding 04.
- **OLA improvement budget post-2022** — the Park District's "Maintaining Parks & Facilities" BSL funds both OLAs AND P-Patch community gardens, and SPR doesn't publish the split. Numbers after 2022 include both; the OLA share is some fraction smaller.
- **Dog population** — "150,000+" is the conservative figure cited since ~2013. SPR's 2023 Expansion Study cites estimates up to 400,000. I use the conservative floor throughout.

## License

Code and analysis: MIT (see LICENSE).
Underlying data is all from public government sources and is not separately licensed by this project.

## Contact

Project maintained by Andre Vrignaud. Issues and pull requests welcome.

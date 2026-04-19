# Changelog

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

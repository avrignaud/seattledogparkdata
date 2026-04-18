# TODO

Concrete next-work ideas, organized by effort and value. Kept up-to-date as work progresses.

## Filed / in progress

- [x] **PRR C049204** — off-leash citations 2014–2019. Responded Oct 2019; data at `data/prr-responses/C049204/` and consolidated as `data/enforcement-citations.csv`.
- [ ] **PRR #1 (filed, awaiting response)** — off-leash citations Oct 2019 to present. Draft at `prrs/01-spr-offleash-citations-post-2019.md`.

## Ready-to-file, drafted

- [ ] **PRR #2 to SPU** for Find-It-Fix-It "dog in a park" complaint counts by year and park. Draft at `prrs/02-spu-fifi-dog-complaints.md`. Replaces the approximate ~1,100/year figure in Part II.
- [ ] **PRR #3 to SPR** for OLA-only share of the Maintaining Parks & Facilities BSL (BC-PR-50000), 2023–present. Draft at `prrs/03-spr-ola-budget-split.md`. Separates OLA from P-Patch so Cycle 2 numbers on Part I are honest.
- [ ] **PRR #4 to SPR** for the methodology behind the 2.5-mile OLA access standard. Draft at `prrs/04-spr-access-methodology.md`. Either exposes a real methodology we can compare to TPL's 0.5-mile network walkshed, or shows there isn't one.
- [ ] **PRR #5 to SPR** for per-OLA usage/headcount data. Draft at `prrs/05-spr-ola-usage-counts.md`. Low-probability return; absence of data is itself a finding.
- [ ] **Outreach to COLA** — asks for usage-count data, corrections, and coordination. (Email handled off-site; not in repo.)

## High value, low effort

- [x] **Real TPL-style network walkshed for OLAs.** Implemented via `scripts/compute_walkshed.py` + `scripts/population_coverage.py` (osmnx + Census block groups). Current result: 9.6% of residents within a 0.5-mile network walk, rendered on the Part II map and cited throughout the site.
- [ ] **Reach out to Colin Campbell** (SPR, project lead on West Seattle Stadium OLA) for confirmed 2026 opening dates, final site acreages, and any updated OLA-only budget data.

## High value, more effort

- [ ] **Real TPL-style "park need" overlay on the Part II map.** TPL publishes block-group-level priority scores for where new parks would most reduce inequity. Overlaying OLA walksheds against TPL's priority layer would produce the "where SPR should be building next" chart.
- [ ] **Historical OLA timeline map.** Show OLAs by year-opened. Would make the "nothing for 15 years" visual more vivid.
- [ ] **Per-OLA usage/density estimates.** From MOLG/COLA volunteer counts (pending response) or direct observation. Would convert the Kinnear capacity argument from theoretical to empirical.
- [ ] **Citation-density backfill pass on Part I and Part II.** Every bare number should link to a primary source, a CSV row, or be marked as derived/approximate. New pages (enforcement, opinion) already follow this rule.
- [ ] **Expand peer-city list** — add Minneapolis, DC, Boston, Chicago with more detail (beyond the single data-point-per-city currently). Currently these are in `peer-cities.csv` as data but not featured in either report.
- [ ] **Consolidated `docs/report.html`** that stitches all pages into one long PDF-optimized document for printing as a single multi-page report.

## Part III ideas (new report)

- [ ] **"What works"** — profile 2–3 OLAs that are functioning well (Magnuson MOLG, Genesee, Westcrest). Community governance, programming, volunteer infrastructure. Positive counterweight to the Kinnear case.
- [ ] **The Comp Plan angle.** Seattle's Comprehensive Plan proposes denser residential development. More density without new OLAs = even worse per-capita access. Chart this projection.
- [ ] **Funding mechanism comparison.** How Portland, SF, Vancouver BC fund their OLA systems. Is there a model Seattle should copy?
- [ ] **Shared-use policy deep-dive.** The NYC off-leash hours policy (20+ years running), Boston's variants, Chicago's DFAs. Operational details for the recommendation in `docs/opinion.html`.
- [ ] **Legal off-leash on WSDOT / Seattle City Light / Port of Seattle land.** COLA flagged this in the 2023 Expansion Study — that SPR didn't consider non-SPR public land. Worth exploring.

## Data quality / maintenance

- [ ] Verify OLA coordinates in `data/seattle-olas.csv` against SPR official GIS layer (if one exists). Current coordinates are approximations from addresses.
- [ ] Add a `provenance` column to each CSV indicating whether a value is sourced, calculated, or estimated.
- [ ] Document sheet-level breakdown inside `data/prr-responses/C049204/README.md` (date ranges, column notes — partially done).
- [ ] Park-name canonicalization in `enforcement-citations.csv` covers the top ~40 named locations. Remaining ~110 rows with street-address-only locations are unassigned — geocode them or flag as "street location."
- [ ] Update dog-population estimate — currently using 150K floor. Find a defensible current count (AVMA, Seattle Humane, King County licensing) to replace the "153K vs 107K kids" claim from community discussion, which attributes to "2021 Census" but the Census does not count dogs.

## Infrastructure / repo

- [x] Repo moved to `avrignaud/seattledogparkdata` (private).
- [ ] Enable GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/docs`). Confirm Pro plan or higher if private-repo Pages is intended.
- [ ] Configure Cloudflare DNS for `seattledogparkdata.com` to point at GitHub Pages.
- [ ] Consider a small build script that regenerates shared CSS across the docs pages (currently duplicated per file).
- [ ] Set up basic CI (GitHub Actions) to lint CSV files and validate HTML on PR.

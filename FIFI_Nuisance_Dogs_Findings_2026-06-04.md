# Find It Fix It "Nuisance Dogs in a Park" — data review & recommendations

**Source:** Seattle Open Data, *Customer Service Requests* dataset, service type
`Nuisance Dogs in a Park` (portal id `5ngg-rpne`), delivered via PRR
**C263990-041726** (Sarah Stark, FAS, June 2026). Filtered export: 4,865 records,
2 Apr 2024 – 3 Jun 2026.
**Analysis date:** 2026-06-04. Reproducible from the CSV + repo data
(`data/seattle-olas.csv`, `data/walkshed/seattle_block_groups.geojson`,
`data/ParkScore_2025_.../ParkServe_Parks.shp`).

---

## TL;DR

There is a clean, publishable finding here and a tempting one that **does not survive
a baseline check**. Recommend we add a modest, descriptive panel built on the robust
findings and explicitly *not* make the proximity-to-OLA argument this data can't support.

**Robust / publishable:**
1. Real complaint volume — **3,010 in 2025** (first full year), updating the stale
   "≈1,100 (2024)" placeholder in `illegal-use-indicators.csv`.
2. Resident-reported complaints concentrate at **neighborhood playfields and
   playgrounds**, not destination parks. 47% of in-park complaints land at a park
   named "Playfield" or "Playground."
3. **Queen Anne is the epicenter of resident reports** — ~516 complaints across its
   playfields, with the 0.12-acre Kinnear as the only legal OLA. Direct tie to the
   existing Kinnear case study.
4. This map **diverges from our enforcement-citation hotspot map** (Discovery,
   Magnuson, Volunteer). Two proxies, two pictures.

**Does NOT survive scrutiny — do not publish:**
- "Complaints cluster in OLA deserts / far from OLAs." The complaint distribution
  tracks Seattle's population almost exactly (see §3). This dataset cannot carry a
  proximity-to-OLA argument.

---

## 1. What the dataset is (and isn't)

- **One service type only:** `Nuisance Dogs in a Park`. Per FAS, this is the only
  FIFI type specific to dogs, and **it was created in 2024** — so there is no
  pre-2024 history here. The free-text `General Inquiry – Animal Shelter` type
  (still pending from FAS) may add more but has no species/category fields.
- **Fields we can use:** created date, full address + lat/lon (100% populated),
  ZIP, Council District, police precinct, method received, status.
- **Fields we don't get:** the complaint narrative, reporter identity, outcome
  beyond status. So we know *where and when* a complaint was filed, not *what
  happened* or whether a dog was actually off-leash.
- **Status:** 99% Closed. Method: 83% Find It Fix It app, 17% web intake, 1 phone.

## 2. Volume and trend — report as volume, NOT as a rising trend

| Year | Complaints | Note |
|------|-----------|------|
| 2024 | 853 | Partial — category launched, first record April; adoption ramp |
| 2025 | 3,010 | First full year |
| 2026 | 1,002 | Through ~3 June (run-rate ≈ 200/mo, tracking **below** 2025) |

The 2024→2025 jump is largely category maturation (people discovering a new FIFI
option) plus a Jan–Feb 2025 reporting surge, **not** evidence that off-leash
behavior tripled. Frame as "~3,000 resident complaints in 2025, ~250/month," with
the category-age caveat. **Don't chart a rising trendline** — it would misread.

Seasonality (all years pooled) skews to winter/early spring (Jan highest, summer
lowest), which is counterintuitive for dog-park use and most likely reflects
*reporting* behavior, not actual activity. Another reason not to over-read the curve.

## 3. The proximity-to-OLA claim is a null — kill it before it ships

Tempting story: "complaints happen where there's no legal off-leash option."
The check that decides it — compare the complaint distribution to a
**population baseline** (2020 Census block-group centroids, population-weighted,
from our walkshed pipeline):

| Distance to nearest OLA | Population | Complaints |
|---|---|---|
| within 0.5 mi | 16.9% | 18.6% |
| within 1.0 mi | 40.6% | 46.2% |
| beyond 1.0 mi | 59.4% | 53.8% |
| **median distance** | **1.14 mi** | **1.10 mi** |

Complaints track the population almost exactly — if anything marginally *closer* to
OLAs. There is **no "OLA desert" signal** here. This makes sense: complaints happen
at parks, parks are near people, OLAs are near people. We should state this honestly
(it's a credibility win) and not argue the gap on a proximity basis from this data.

## 4. Where complaints actually concentrate (robust — point-in-polygon)

Spatial join of every complaint against the TPL ParkServe Seattle park-boundary
layer: **65% fall inside a named park polygon**, 35% on adjacent streets/sidewalks.
Top hotspots:

| Complaints | Park | Nearest OLA |
|---|---|---|
| 255 | **West Queen Anne Playfield** | Kinnear 0.7 mi |
| 147 | Maple Leaf Reservoir Park | Lower Woodland 1.9 mi |
| 140 | Warren G. Magnuson Park | *(has the OLA)* 0.2 mi |
| 132 | **East Queen Anne Playground** | Kinnear 0.9 mi |
| 111 | Delridge Playfield | Westcrest 2.8 mi |
| 109 | Discovery Park | Magnolia Manor 1.3 mi |
| 109 | E Harrison St (Madrona/Denny Blaine lakefront strip) | I-5 Colonnade 2.1 mi |
| 108 | Beacon Hill Playground | Dr. Jose Rizal 0.5 mi |
| 100 | Rainier Playfield | Genesee 0.5 mi |
| 99 | Volunteer Park | I-5 Colonnade 0.5 mi |

Two things stand out:

- **47% of in-park complaints are at "Playfields" / "Playgrounds."** These are
  sports fields and kids' play areas — exactly where off-leash dogs collide with the
  intended use. That's a plausible, concrete reason residents file, and it's a
  different phenomenon than off-leash use in a big natural-area park.
- **Magnuson (140) has the city's largest OLA.** Complaints there are off-leash use
  *outside* the fenced OLA (beach, fields). A useful nuance: an on-site OLA does not
  zero out complaints in a large multi-use park. Don't oversimplify "OLA = no problem."

Concentration is real but tail-heavy: top 10 addresses = 16% of all complaints, top
100 = 50%. And some single addresses are episodic — e.g. the top single address
(3925 E Harrison) had **zero** complaints until May 2025, spiked Jun–Sep 2025, then
went quiet. That pattern is the fingerprint of a repeat reporter or an acute local
dispute, not steady demand.

## 5. Queen Anne — the strongest narrative tie

Queen Anne playfields aggregate to **~516 complaints** (West QA Playfield #1
citywide, East QA Playground #4, QA Bowl 66, David Rodgers 47), and the only legal
OLA in the neighborhood is the **0.124-acre Kinnear** at 0.7–0.9 mi. This is a clean
extension of the existing Part II Kinnear case study, and it's resident-generated
rather than author-asserted. (Caveat in §6 still applies — QA is also an affluent,
civically engaged area that over-reports.)

By Council District (districts are ~equal population by design, so counts are roughly
per-capita): **CD6 1,056** (Ballard/Fremont/Greenwood) and **CD7 766**
(downtown/QA/Magnolia) lead; CD5 528 and CD4 543 trail. North/central-west Seattle
reports far more.

## 6. The bias caveat that must ride along with everything

FIFI is **self-reported 311 data**. It measures *who files complaints*, which
correlates with affluence, civic engagement, smartphone use, and neighborhood
conflict norms — not just where off-leash dogs are. The episodic single-address
spikes (§4) are direct evidence of this. Every number above is "complaints filed,"
never "off-leash incidents." Any panel we publish must say so plainly.

## 7. How this complements the enforcement page (divergence is the insight)

Our enforcement-citation hotspots (Animal Control PRRs, 2014–26): **Discovery 564,
Magnuson 367, Volunteer 328, Woodland 291** — big destination/natural-area parks
where officers patrol. The FIFI resident-report hotspots are **neighborhood
playfields** (West QA, Maple Leaf, East QA, Delridge, Beacon Hill). Discovery is #1
for citations but #6 for complaints; West Queen Anne Playfield is #1 for complaints
but absent from the citation top tier.

The two datasets measure different things — **where the city enforces** vs. **where
neighbors object** — and the gap between them is itself a finding worth a sentence or
two. (Honest limit: different time windows, 12 yr vs 2 yr, so frame as complementary
lenses, not a controlled comparison.)

---

## Recommendations

**Do:**
1. **Update `data/illegal-use-indicators.csv`** — replace the "1100 / 2024" FIFI row
   with the real figures (3,010 in 2025; 4,865 total Apr 2024–Jun 2026), cite the
   open-data portal `5ngg-rpne` so it's reproducible, and add the "category created
   2024" caveat in the notes column. *(Low-risk data correction; ready to do on your
   word.)*
2. **Add a compact "Resident complaints" panel** — to the enforcement page or as a
   short section — built on §2, §4, §5, §7: the volume number, the
   playfield-concentration finding, the Queen Anne tie, and the
   enforcement-vs-complaints divergence. Descriptive register, bias caveat inline.
3. **Optionally add a hotspot map layer** — the in-park complaint points are clean
   enough to map; pairs naturally with the existing enforcement gap map.

**Don't:**
4. Don't publish any proximity-to-OLA / "OLA desert" claim from this data (§3).
5. Don't chart 2024→2025 as a rising trend (§2).
6. Don't name parks from raw addresses without the polygon join — earlier
   centroid-distance matching was radius-sensitive and unreliable.

**Pending:** the `General Inquiry – Animal Shelter` free-text export from FAS may let
us separate genuine dogs-in-parks complaints from the rest; worth parsing when it
arrives, but it has no structured location/category fields so expect it to be noisier.

---

## 8. Complaints vs. enforcement — did one drive the other?

Direct comparison of FIFI complaints (2024–26) against Animal Control off-leash
citations (`data/enforcement-citations.csv`, PRRs C049204 + C263949; the 2025–26 file
is complete through 17 Apr 2026, sentinel-verified). The answer is the interesting part:
**neither drives the other in time, but they share geography.**

**Temporally: no relationship visible.** Monthly complaint–citation correlation over
the 27-month overlap is r = 0.13 (dog-loose-in-park citations only); complaints-lead
and citations-lead correlations are both ≈ 0.1. Neither direction is visible in the
data — note this is the honest claim, *not* "complaints don't convert to enforcement"
(we can't see complaint outcomes, only citation volume).

| | 2024 | 2025 | 2026 (to ~Jun) |
|---|---|---|---|
| FIFI complaints | 853* | **3,010** | 1,002 |
| Dog-loose-in-park citations | 447 | **267** | 65* |

\*partial years. Complaints rose ~3.5× from 2024 to 2025 while citations *fell* ~40%.
Two distinct mechanisms are doing the work here — keep them separate:
- **A supply ceiling.** Animal Control runs ≈1.0 FTE (budget data). Citations
  structurally *cannot* 10× to match a 3.5× jump in complaints, regardless of demand.
- **A mid-2025 drop-off.** Monthly DLP citations fell to near-zero after June 2025
  (Jul–Dec ran 1, 1, 5, 4, 5, 1) while complaints held at 150–250/month. The 2025–26
  citation file is sentinel-verified complete through 17 Apr 2026, so this is real in
  the record, **not** a pull-date truncation. Cause is unknown (officer vacancy? policy?
  a records gap upstream at FAS?) — a candidate for a PRR follow-up. Don't assert
  "enforcement collapsed"; say citations fell sharply and the reason isn't in the data.
- **A 2026 partial recovery, consistent with the capacity story:** FTE rises to 1.3 in
  2026 and monthly citations tick back up (19/14/18/18).

Because citations go near-zero for the back half of the series, the low r is partly
*overdetermined* by that drop-off — it's not clean evidence of structural independence
on its own. The supply ceiling is the load-bearing argument; the correlation corroborates.

**Spatially: modest overlap that dissolves at the top.** Now computed apples-to-apples
in the overlap window (2024–26), both attributed via the ParkServe layer. (The 2024–26
citations turned out to be *park-named* in the record — `location_type == park_named` —
so no geocoding was needed; they reconcile to ParkServe names directly, 98% matched.
Script: `scripts/compare_complaints_citations.py`; per-park output:
`data/complaints-vs-citations-by-park.csv`.)

| Parks included | n | Spearman | Pearson |
|---|---|---|---|
| all with ≥1 combined | 182 | 0.62 | 0.71 |
| ≥5 combined | 90 | 0.52 | 0.64 |
| ≥10 combined (busiest) | 66 | **0.36** | 0.58 |

A modest **downgrade** from the all-time ρ = 0.74 (which compared 12-yr citation
geography to 2-yr complaints), but not a collapse: in the overlap window the rank
correlation is still **moderate (≈0.5–0.6 across parks, ≈0.36 among the busiest)**. Both
systems do light up the same off-leash hotspots. What diverges is the *intensity ratio*,
not the ranking — complaints outrun citations most at neighborhood playfields, because
complaints follow where people live and citations follow where officers patrol.

(Data note: this required clipping the national ParkServe layer to Seattle's city
bounding box — it contains same-named parks elsewhere in WA, e.g. a Tacoma "Lincoln
Park," that otherwise stole citations from the real Seattle parks and understated the
correlation. Handled in `load_seattle_parks()`.)

**The complaint:citation ratio diverges by park type, and that's the insight:**

Same window now (2024–26, both via ParkServe), complaints : citations:

| Park | Complaints | Citations | Ratio | Lean |
|---|---|---|---|---|
| Discovery Park | 109 | 59 | 1.8 | balanced — **enforcement-leaning** (remote, patrolled) |
| Woodland Park | 62 | 35 | 1.8 | balanced |
| Golden Gardens | 44 | 24 | 1.8 | balanced |
| Warren G. Magnuson | 140 | 51 | 2.7 | balanced (has the OLA) |
| Volunteer Park | 99 | 25 | 4.0 | mixed |
| West Queen Anne Playfield | **255** | 53 | 4.8 | **complaint-leaning** |
| Maple Leaf Reservoir | 147 | 21 | 7.0 | complaint-leaning |
| Lincoln Park | 97 | 11 | 8.8 | complaint-leaning |
| Cal Anderson Park | 95 | 8 | 11.9 | complaint-leaning |
| East Queen Anne Playground | 132 | 10 | 13.2 | complaint-leaning |
| Beacon Hill Playground | 108 | 2 | 54 | complaints only, in effect |
| Rainier Playfield | 100 | 1 | 100 | complaints only, in effect |

Destination and natural-area parks (Discovery, Woodland, Golden Gardens, Magnuson) stay
roughly balanced — officers patrol them. Dense-neighborhood playfields run 5:1 to 100:1
complaints-over-citations. Patrol geography and reporting geography are structurally
different, and that ratio is the readout.

**Bottom line for the causal question:** the two systems run in **parallel, not in
sequence**. Residents filed ~3,000 complaints in 2025; citations fell to 267 and went
nearly silent for half the year. The complaint channel does not visibly convert into
enforcement. That is a defensible, evidence-backed finding — and a more interesting one
than either "complaints drive enforcement" or the proximity story that didn't survive.

---

## Visualization recommendations (answering the map / chart questions)

**1. Divergence time series — the strongest single chart. But NOT a dual-axis one.**
A dual-axis chart invites the eye to "correlate" two lines, and the apparent
relationship is just an artifact of how you scale the two axes — a foot-gun on a
neutrality-first site, especially for a finding whose whole point is *non*-correlation.
Two honest alternatives, pick one:
- **Index both series to a common baseline on one axis** (e.g. each =100 at its 2024
  monthly average): complaints climb, citations fall — divergence is unmanipulable.
- **Two vertically-stacked panels sharing one time x-axis** — complaints on top,
  citations below, same months lined up.
Either way, monthly Apr 2024–present, captioned with the ≈1.0→1.3 FTE constraint. This
is the chart that answers your causal question at a glance.

**2. Bivariate hotspot map — useful, and it reuses the existing Leaflet setup.**
One map, complaint and citation layers. Best version: one marker per top park, **size =
total off-leash activity, color = complaint:citation ratio** (one hue = enforcement-
dominant like Discovery, the other = complaint-dominant like West QA Playfield). That
visualizes "where the city patrols vs. where neighbors object" in a single view. A
simpler two-toggle-layer map also works. Either pairs naturally with the enforcement
page's existing gap map. *Don't* draw OLA-proximity rings on it — that's the dead claim.

**3. Per-park scatter (optional) — citations (x) vs complaints (y), top-20 parks,
diagonal reference line, a few labeled outliers.** Shows the same-places overlap *and*
the Discovery / West QA divergence in one frame. Label the axes with their windows
(12-yr citations vs 2-yr complaints) or, better, geocode the ~200 recent citations
first so it's a clean overlap-window scatter. Nice supporting exhibit, not essential.

Skip a rising-trend bar chart of complaints by year (§2 — misreads category maturation).

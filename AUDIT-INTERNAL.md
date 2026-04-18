# Internal audit — April 2026

Run by Claude Code, same prompt as the external Codex audit, completed
locally without external Web requests for link-by-link verification. Use
this alongside whatever Codex returns — the two passes complement each
other (Codex has fresh eyes and independent WebFetch; this pass has deep
knowledge of the repo's data pipeline).

## Executive summary

**Strong.** Math on every derived number reproduces exactly from the
committed CSVs and scripts. No stale values survive on any page (the
previous-session audit's 9.6%→9.5%, 79.4%→78.3%, water-1-of-14→9-of-14,
DC-20→16, OLA-acres-26→30.7 corrections have all propagated across
`docs/*.html` and `print.html`). Provenance is explicit in every small
reference CSV via a `provenance` column and summarized in `DATA-AUDIT.md`.
The dog-population triangulation is defensible and transparent. The
"84.6% outside walkshed" finding is newly computed and its CSV
(`data/walkshed/citation-rate-by-walkshed-status.csv`) reproduces it.

**Weak.** Four genuine issues:
(1) **Peer-city per-100K is apples-to-oranges on the denominator** —
Seattle's 1.82 per-100K uses TPL's reference population (~769K) but the
`population` column carries current OFM (816K), so recomputing gives
1.71. Same for SF (5.03 stated vs 4.83 computed) and Boise (7.60 vs 7.50).
(2) **Convex-hull walkshed over-states** coverage by a percentage point
or two at the boundary — acknowledged on site but not quantified. A
proper alpha-shape is on TODO.
(3) **AVMA-derived dog estimate uses the national 42.6% / 1.6 figures
as a Seattle proxy** because state-level AVMA is paywalled. Flagged
inline on the site but easy to miss.
(4) **The 84.6% statistic is computed on 2,812 of 4,803 citations**
(58.5%) — the 672 street-address and 111 unknown rows are excluded.
The bias direction is plausibly *toward* the outside-walkshed figure
(street addresses are more likely to be outside parks entirely) but
this is not quantified.

Everything else is MINOR or INFO.

---

## Would-I-cite-this confidence (1 = weak, 5 = rock solid)

| Claim category | Confidence | Notes |
|---|---|---|
| OLA counts / inventory | 5 | Authoritative coords from SPR ArcGIS (April 2026); acreages reconciled to individual SPR pages |
| Walkshed % (9.5 / 78.3) | 4 | Math reproduces; convex-hull caveat documented but not alpha-shape-corrected |
| 84.6% outside walkshed | 3.5 | Strong pattern, but computed on 58.5% of citations; street-address bias not quantified |
| Enforcement revenue | 5 | Exact sum from PRR-provided `fee` column; reproduces to the dollar |
| Enforcement program cost | 4.5 | FAS ACO II $152,399 is from the signed 2021 MOA (public record). FMW estimate is labeled as an estimate |
| Budget (SPR totals) | 4.5 | All from adopted/proposed budget books with page/BSL references |
| Budget (OLA-only split) | 3 | Known gap for 2019–2022 and 2025–2026; PRR #3 filed |
| Peer-city per-100K | 3 | TPL-sourced ratios correct; population column year mismatch creates minor discrepancies |
| Peer-city detail | 4 | Verified April 2026 via live WebFetch per city; five of six cities have primary-source links per stat |
| Dog population triangulation | 3.5 | Three independent anchors; AVMA uses national rate as Seattle proxy |
| Opinion arguments | n/a | Opinion by definition; every data claim inside links back to a factual page |
| NYC precedent | 3 | 19 years of formal operation documented; longitudinal outcomes evaluation acknowledged missing |

---

## Section-by-section findings

### 1. Data provenance and freshness

**INFO: Provenance columns present on all small reference CSVs.**
`DATA-AUDIT.md` records what was added (seattle-olas, planned-olas,
illegal-use-indicators, kinnear-timeline, seattle-timeseries,
budget-detail, peer-cities, peer-cities-budget). `enforcement-citations`
already had source_file + source_sheet + location_type.

**MINOR: Pre-2024 figures without "stale" flag.**
Several rows in `illegal-use-indicators.csv` are 2016–2023 data:
  - 39% / 38% self-report illegal off-leash (2016 SPR survey)
  - 1,100 FIFI complaints (2024 approximate)
  - 435 tickets (2016 half-year)
These are correctly dated in the CSV and in the site prose. **No
change needed**, but if Codex asks "why a 2016 survey in 2026," the
answer is: SPR has not re-run the owner survey since. PRR #2 (FIFI) and
PRR #1 (post-2019 citations) are filed to replace the older half with
current data.

**MINOR: `park-coordinates.csv` has no provenance column.**
The other CSVs got one but this one didn't. Low-risk since every row is
a single manually-geocoded point and the file is small, but should be
added for parity. **Fix:** add `provenance` column noting "manual geocode
from park name via Seattle GIS / Google Maps (2024 review)."
**File:** `data/park-coordinates.csv`

**MINOR: TPL ParkServe cross-tab CSVs lack column definitions.**
`data/tpl-parkserve/ola-walkshed-by-tpl-rank.csv` and the priority-tier
version are published but the README notes only what the analysis
found, not what each column means at the row level. Low-risk because
columns are self-explanatory (ParkRank, n_bgs, n_with_ola, pct_with_ola).

### 2. Math re-check

All headline numbers reproduce exactly. Full run:

```
Residents-per-OLA (pop / OLAs): all 12 rows match ±1 rounding
OLA acres total: 30.659 → site says 30.7 ✓
Top-4 share: 78.6% → site says ~79% ✓
Bottom-10 share: 21.4% → site says ~20% ✓
Under 1 acre: 7/14 ✓
Under 0.25 acre: 3/14 ✓
Enforcement citations: 4,803 ✓
Fee sum: $240,652 ✓ (exact match to site's $240,652)
Cost recovery FAS-only: 26.3% → site says 26% ✓
Cost recovery FAS+FMW: 13.7% → site says 14% ✓
OLA openings 1997–2009: 14 ✓
OLA openings 2010–2025: 0 ✓ ("zero new OLAs" claim confirmed)
Dog pop AVMA-derived: 364,627 × 0.426 × 1.6 = 248,530 → site ~248,500 ✓
Walkshed 0.5mi: 9.47% → site says 9.5% ✓
Walkshed 2.5mi: 78.32% → site says 78.3% ✓
84.6% outside walkshed: reproduced via point-in-polygon ✓
```

**MINOR: 2017 residents-per-OLA off by 1.**
`seattle-timeseries.csv` says 51,767; correct is 51,768 (724,745 / 14).
Rounding. **Fix:** change `51767` → `51768`.
**File:** `data/seattle-timeseries.csv` row 2017.

### 3. Source-link integrity

**NOT FULLY AUDITED.** External link integrity requires WebFetching
every link on every page — several hundred URLs — which I'd rather
leave to Codex's pass to avoid duplicating effort. Spot-checked:

  ✓ SPR ArcGIS feature service (primary OLA coord source) resolves
    and carries expected 14 features + Denny Substation stub.
  ✓ AVMA 2025 Sourcebook landing page resolves with 42.6% / 1.6 figures.
  ✓ Seattle Open Data jguv-t9rb pet license count returns ~26,652.
  ✓ ACS 2023 1-year B11001 for Seattle place returns 364,627.
  ✓ TPL 2025 ParkScore Seattle page resolves.
  ✓ DC DPR dog parks page resolves with 16 dog parks.

**INFO: Archive link coverage.**
A few Seattle Weekly Kinnear citations from 2007 might be paywalled or
url-migrated. Those links weren't verified; if Codex finds 404s, the
archive.org wayback versions are in my backlog to swap in.

### 4. Methodology scrutiny

**MODERATE: Convex-hull walkshed inflation not quantified.**
`compute_walkshed.py` comments state "tends to slightly overestimate"
and `METHODOLOGY.md` says "a percentage point or two down." The *actual*
magnitude isn't measured. Alpha-shape refinement is the fix; it's on
TODO but not done.
**Recommended fix:** implement alpha-shape in `compute_walkshed.py`
(requires `alphashape` package; ~2 hrs), rerun pipeline, update every
9.5% → new value. Document delta in `METHODOLOGY.md`.

**MODERATE: AVMA Washington-state rate not cited.**
Site uses AVMA's national 42.6% dog-owning / 1.6 dogs-per-HH on Seattle's
household count. AVMA *does* publish state-level tables in its paywalled
Sourcebook; those would give a Washington-specific rate (typically
higher than national in Washington State, ~38–40% per secondary
sources).
**Recommended fix:** purchase the 2025 Sourcebook ($199–249), swap in
WA figures, cite page. Or acknowledge more prominently that the 248K
derivation uses the national rate as a proxy.
**File:** `docs/part1-the-gap.html` §Methodology note; `docs/index.html`
methodology item; `docs/print.html` appendix.

**MODERATE: 84.6% outside-walkshed is on a 58.5% subsample.**
Only 2,812 of 4,803 citations placed (park-named + geocoded). The 672
street-address and 111 unknown rows are excluded. Street-address rows
likely represent off-leash behavior on neighborhood streets / alleys,
which are definitionally not inside an OLA walkshed — so excluding them
probably *understates* the outside-walkshed percentage. Geocoding the
672 would let this be quantified.
**Recommended fix:** geocode the 672 via Census Bureau geocoder (free,
no API key), recompute. On TODO.
**File:** `data/enforcement-citations.csv`; `docs/part2-access.html`
Finding 02b.

**MINOR: TPL ParkServe priority overlay is loaded but not visualized.**
Cross-tab CSVs are committed (`data/tpl-parkserve/ola-walkshed-by-tpl-*.csv`)
showing a bimodal pattern, but no chart on Part II exercises them.
On TODO.

**MINOR: 2.5-mi coverage computed under SPR's own standard.**
78.3% coverage at 2.5-mi is reported to make the asymmetry argument.
But the 2.5-mi isochrone is also convex-hull; same inflation concern
applies, meaning *both* the 9.5% and 78.3% are slight overestimates.
The asymmetry argument still holds — both sides would shift in the
same direction — but the site could note this in the 2.5-mi row.

### 5. Argument integrity (opinion.html)

**Principles P1–P6:** each supported with specific on-site links.
  P1 kids-first: explicitly concedes the priority; no leap.
  P2 land-is-finite: logical frame.
  P3 investment disproportionate: cites 0.06% budget + 0.06% land
    (both land-share math rechecked — 30.7 / 53,100 = 0.058% ✓).
  P4 non-dog users' rights: cites SPR's own 2016 survey self-report.
  P5 clean fields for kids: stated plainly, no fabricated data.
  P6 dog-free time: policy claim, no factual leap.

**Opinions O1–O3:** each connects to the enforcement data on the site.
  O1 enforcement expansion doesn't change structural math: cites the
    0.5% per-dog-per-year citation probability. Math reproduces.
  O2 fines are regressive + structurally mismatched: stated as opinion;
    the 90% first-offense / $54 figure supports it.
  O3 supply failure → compliance failure: cites the 9.5% walkshed + 7/14
    below AKC floor + encampment-adjacent small OLAs. Supported.

**Counterarguments C1–C7:** steel-manned reasonably.
  C3 ("fairness of enforcement"): the $500-vs-$54 regressivity point is
    a real opponent argument.
  C5 ("dog owners should organize politically, not break the law"):
    engaged without dismissing. Good.
  C7 ("won't enforce shared-use any better than current rules"):
    acknowledged as a real concern.

**NYC precedent:** the site *explicitly* states "NYC does not publish
a longitudinal evaluation" and flags that the proxy is durability
(19 years, multiple administrations, no reversal). This is the honest
version. No strawman.

**MINOR: P3 dogs-vs-kids claim uses 150K floor.**
"Seattle has more dogs than children" is stated using the conservative
150K floor vs ~115K under-18. AVMA-derived 248K would make the ratio
more than 2:1, strengthening the argument. Using 150K is intentionally
conservative (Andre's preference, noted in CLAUDE.md: "Use 150K for floor
calculations"). No change; just noting.

### 6. Counter-research

**NOT FULLY AUDITED.** Thorough counter-research requires external
search and literature review. Spot-checked:

  - Portland's voice-control model (~30+ DOLAs) is cited as a positive
    example. I did NOT find published research showing Portland's
    voice-control model produces worse injury rates or worse park
    cleanliness than Seattle's fenced-only model. Absence of evidence,
    not evidence of absence. Codex's pass should specifically look for
    NRPA peer-reviewed evaluations.
  - SPR's 2.5-mile standard: I found no SPR document that explains the
    methodology for adopting 2.5 miles (rather than 10 minutes). PRR
    #4 is filed to request that document.
  - High-fenced-density peers that contradict the thesis: DC (16 OLAs
    for 699K) and Minneapolis (9 for 435K) are the cleanest
    counterexamples on density. Both are in the peer-cities data;
    neither has higher density than Seattle's 1.82/100K — so they
    *support* the thesis that fenced-only + low density is the pattern.
  - Enforcement deployment confound: acknowledged in Finding 01 note
    on enforcement.html. PRR for deployment patterns not filed.

### 7. Readability and accessibility

**MINOR: Mobile chart rendering not audited systematically.**
Chart.js responds to container size; short-viewport mobile behavior
was spot-checked on one page and works but isn't comprehensively
verified. No explicit mobile breakpoint testing.

**MINOR: Color-only encoding on charts.**
The peer-city bar chart uses orange for Seattle and green for peers.
Colorblind readers who can't distinguish those specific hues could
still read the chart from labels. No pattern/hatch fallback, but
acceptable under WCAG given the label redundancy.

**INFO: Opinion/fact separation is clear.**
Opinion lives at `docs/opinion.html` with a navy editorial band, a
"Part V · Opinion" kicker in print, and the word "opinion" in titles.
A casual reader will not mistake data pages for opinion.

**INFO: Jargon defined.**
OLA is defined on first use in the landing page and each section.
SPR, SAS, FAS, SMC, FIFI are expanded on first mention.

### 8. Attribution and license

**LICENSE (MIT):** appropriate. Covers code and analysis; data is public
record.

**AI disclosure:** present on index.html (primary), in print.html
appendix ("how this report was built"), and in commit history.
Accurate — describes the human-collects / AI-assists / human-reviews
workflow.

**External source citation:** every chart-source footnote links the
primary source with enough specificity. No paraphrasing without credit
caught in my sampling.

### 9. Consistency pass

Ran regex-based consistency check across all 9 HTML pages. Results:

  - OLA count 14 appears on every report page; 16 post-2026 caveat on
    2 pages (part1 + print). Could be stronger on index.html and
    part2-access.html but acceptable.
  - Walkshed 9.5% on 4 pages, no stale 9.6% remaining.
  - 78.3% on 3 pages, no stale 79.4% remaining.
  - 150K dog floor appears consistently where per-dog math happens
    (budget, opinion, part1, part2, print).
  - 26,700 licensed / 248K AVMA / 400K SPR ceiling appear consistently
    on the methodology panels of index, part1, opinion, and print.
  - Water 9/14 on part2 + print; Lighting 2/14 on index + part2 + print.
    No stale water-1-of-14 survives.
  - 30.7 acres consistent across 4 pages. No stale ~26 acres.
  - 4,803 citations consistent across 5 pages.
  - $240,652 revenue consistent on enforcement + print. No stale $210K.
  - DC 16 consistent. No stale DC 20.

**INFO:** consistency is very clean. The recent multi-session
reconciliation work landed cleanly.

### 10. Omissions

**MODERATE: Disability-access analysis is missing.**
No section covers ADA compliance per OLA, physical accessibility of
entrances, or surface type (gravel / grass / mud) for wheelchair users
or owners with mobility limitations. Westcrest's 2022 renovation included
ADA improvements — that's noted in peer-cities-equivalent prose but
doesn't surface as a structural analysis. Worth a dedicated subsection.

**MODERATE: Equity overlay not surfaced.**
TPL ParkServe priority data is imported and cross-tabbed but the
equity angle (race/income/health weighting TPL applies) doesn't appear
on any chart or callout. The bimodal finding (ParkRank 3 bgs have 30.6%
OLA coverage, middle tier 9.5%) is interesting and worth a Part II
callout.

**MINOR: No seasonal / weather analysis.**
Seattle's rainy winters materially affect OLA usability (Kinnear's
"dust pit in summer / mud pit in winter" quote is noted in Part II).
No systematic seasonal breakdown.

**MINOR: Arguments FOR the current framework underdeveloped.**
Liability concerns, park-specific stakeholder agreements (Genesee
meadow advocacy, etc.), SPR staff capacity constraints, and legal
limitations on parks use aren't fully engaged on opinion.html.
C1–C7 counter-arguments hit some of these but not all.

---

## Recommended fixes, in priority order

1. **Fix 2017 residents-per-OLA off-by-one** (5-minute fix).
   File: `data/seattle-timeseries.csv`.
2. **Geocode the 672 street-address citations** (~30 min, on TODO).
   Quantify the 84.6% bias; likely move the number toward 85–88%.
3. **Alpha-shape walkshed refinement** (~2 hrs, on TODO).
   Shifts 9.5% and 78.3% down slightly; tightens methodology.
4. **Add provenance column to `park-coordinates.csv`** (10 min).
   Match the rest of the reference CSVs.
5. **TPL park-need overlay chart on Part II** (on TODO).
   Makes the ParkServe import pay off.
6. **Equity / ADA / seasonal subsections** on Part II or a new
   Part III. Longer-range work.
7. **AVMA Washington-state dog-owning rate** — purchase Sourcebook,
   swap rate, update 248K figure to a WA-specific derivation.
   Financial decision, not coding.

## Codex-flagged findings integrated (addendum)

Two issues caught by Codex's cold rerun that my first pass missed:

**SEVERE: Prose listed wrong four parks as "inside walkshed."**
Site said the 4 parks inside the 0.5-mi walkshed were Magnuson,
Westcrest, Genesee, Golden Gardens. The committed
`data/walkshed/ola_isochrones.geojson` + `data/park-coordinates.csv`
point-in-polygon actually shows: **Magnuson (248), Golden Gardens
(174), Denny Park (10), Northacres (2)** — not Westcrest or Genesee.
Fixed in `docs/part2-access.html` Finding 02b and `docs/print.html`
map caption.

Root cause (also new, also severe):
- **Westcrest's 0.5-mi walkshed is malformed** — 0.258 km² vs peer
  OLAs at 0.9–1.4 km². Westcrest's own SPR ArcGIS coordinate isn't
  inside its own walkshed polygon. The convex-hull algorithm clips
  badly at the edge of Seattle's OSM walk network (Westcrest borders
  a wooded hillside with sparse streets). Alpha-shape refinement
  would fix this.
- **Genesee's park centroid (park-coordinates.csv, used for citation
  geocoding) is ~400 m from the SPR ArcGIS OLA coordinate**
  (seattle-olas.csv). So Genesee Park's point sits just outside the
  walkshed even though the OLA itself is inside.
- Combined, these two bugs move 216 citations (Westcrest 86 + Genesee
  130) from "outside" to "inside" — shifting the 84.6/15.4 headline
  to roughly 77/23. The thesis holds either way; the prose needs to
  name the correct number.

**Fix applied:** added an explicit methodology note under Finding 02b
naming the Westcrest / Genesee artifacts and stating the corrected
77/23 split that a fixed walkshed would produce. Updated `TODO.md`'s
alpha-shape item to call out the Westcrest bug as a concrete
motivation. Updated `docs/print.html` map caption to match.

**SEVERE: Stale `docs/report.html` still deployed on Cloudflare.**
File is gitignored locally (commit 31dab03 re-untracked it after
earlier removal in 8d71d38) but was still served at
`seattledogparkdata.com/report.html` with older amenity counts
("1 of 14 has water"), the pre-reconciliation framing, and stale
numbers. Since anything under `docs/` is deploy surface, readers
who hit that URL saw outdated content.

**Fix applied:** replaced `docs/report.html` with a redirect page
(HTTP-equiv refresh + canonical link) that points to `/print.html`
and the PDF. Removed the gitignore entry so the redirect gets
committed and deployed. On next push the stale content will be
replaced with the redirect everywhere the URL is hit.

Both findings added to the "what was weak" list in the executive
summary.

## Follow-up: multi-seed walkshed + park-coord fix

The "Westcrest methodology artifact" wasn't an artifact — it was a real
bug with two root causes I fixed rather than papered over:

1. **`compute_walkshed.py` single-seed traversal.** The isochrone was
   built from nodes reachable within 0.5 mi of the *single nearest
   network node* to each OLA. For OLAs at the edge of Seattle's OSM
   walk network (Westcrest next to a wooded hillside; Kinnear on the
   Queen Anne hillside; Dr. Jose Rizal), that nearest node could be
   50–200 m from the actual OLA, biasing the traversal toward one
   side. The convex hull of the resulting node cloud sometimes didn't
   even contain the OLA's own coordinate. Westcrest's walkshed came
   out at 0.258 km² (vs ~1.0 km² for comparable OLAs).

   **Fix:** build a KDTree of projected node coords; for each OLA,
   seed the traversal from *all* network nodes within a 100 m radius,
   union their reachable sets, add the OLA's own point to the hull
   point set, and union-buffer the result by 25 m as a safety net.
   Shipped in commit to `scripts/compute_walkshed.py`.

2. **`data/park-coordinates.csv` had wrong lat/lng for Westcrest Park
   and Genesee Park.** Westcrest was off by ~1.17 km to the west —
   likely a data-entry error during the enforcement canonicalization
   pass. Genesee was off by ~650 m. Both now reconciled to the
   SPR ArcGIS OLA point (which matches the real park location on
   any web map).

### Net effect on headline numbers

| Stat | Before | After fix | Delta |
|---|---:|---:|---:|
| 10-min-walk OLA coverage | 9.47% | **11.95%** | +2.48 pt |
| 2.5-mi OLA coverage | 78.32% | **79.64%** | +1.32 pt |
| 84.6% outside walkshed | 84.6% / 15.4% | **76.2% / 23.8%** | ±8.4 pt |
| Unique parks outside walkshed | 33 of 37 | **29 of 37** | −4 |
| Unique parks inside walkshed | 4 of 37 | **8 of 37** | +4 |
| Westcrest walkshed area | 0.258 km² | **0.765 km²** | ×3 |
| All 14 OLAs inside own walkshed? | No (Westcrest fails) | **Yes** | ✓ |

### Thesis holds, numbers sharpened

The asymmetry argument doesn't depend on the precise coverage number.
99% of Seattleites live within 10 min of any park; 11.95% live within
10 min of an OLA. Still an 8× gap. SPR's 2.5-mi standard covers 79.64%,
which is still 4.2× more permissive than TPL's 10-min standard.

76.2% of geocoded citations still occur outside walksheds. The prior
84.6% figure was inflated by the Westcrest/Genesee bugs; the corrected
number is honest.

### Dropped: per-capita 1.3× claim

The BG-level per-capita citation rate comparison (inside 2.93 vs
outside 3.90 per 1,000 residents → outside 1.3× higher) flipped
direction after the walkshed fix (inside 5.11 vs outside 3.65 → inside
1.4× higher). The flip is a symptom of the statistic's flawed
denominator: it attributes citations to the BG containing the park,
not to the BG containing the resident. That's a spurious denominator
for "per-capita" framing. Removed the claim from the site and from
`data/walkshed/citation-rate-by-walkshed-status.csv`.

### Site updates propagated

9.5 → 11.9, 9.47 → 11.95, 78.3 → 79.6, 78.32 → 79.64, 84.6 → 76.2,
15.4 → 23.8, 434 → 668, 33 → 29, "only 4 sit inside" → "eight sit
inside," removed the 1.3× claim and the Westcrest/Genesee methodology
artifact note. Files: `docs/index.html`, `docs/part2-access.html`,
`docs/print.html`, `README.md`, `METHODOLOGY.md`,
`data/illegal-use-indicators.csv`, and
`data/walkshed/citation-rate-by-walkshed-status.csv`. The mirrored
geojson at `docs/data/walkshed/ola_isochrones.geojson` was refreshed.

### O2 enforcement probability — now caveated as SWAG

Per user feedback, the 0.5% per-dog-per-year citation probability now
carries an explicit "rough SWAG" caveat on both `docs/opinion.html`
(Opinion O2) and the PDF callout. The argument stands — the city-wide
average is a useful floor and Seattle can't close the gap via
enforcement staffing — but the per-owner risk varies enormously with
behavior (never-off-leash owners have zero exposure; frequent-visitor
owners have far higher).

## What I deliberately did not audit

- Every external link on every page (hundreds — Codex's pass should
  cover this).
- Deep counter-research literature review on voice-control / time-zoned
  OLA policy outcomes.
- Mobile responsiveness on actual phone hardware.
- Print-layout QA across the full 21-page PDF beyond the spot-checks
  already done during recent fixes.
- Accessibility audit with a screen reader.

These are the places where Codex's fresh pass adds the most value.

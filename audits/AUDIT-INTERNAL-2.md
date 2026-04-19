# Internal audit pass 3 — April 2026

Second internal audit, running the updated prompt that incorporates
lessons from the prior pass and Codex's first-pass findings. Use
alongside Codex's pass-3 when it lands.

## Executive summary

**Strong.** Math on headline enforcement + budget numbers still
reproduces exactly. OLA acres sum to 30.66 (site rounds to 30.7).
Enforcement fee sum is $240,652 to the cent. Cost-recovery 26.32% /
13.72%. AVMA derivation 364,627 × 0.455 × 1.5 = 248,858. Dog-pop
triangulation is defensible.

**Weak (four new issues that prior audits didn't look for).**
(1) `citation_walkshed_analysis.py` no longer reproduces the
committed CSV — re-running it gives 77.2% outside / 22.8% inside,
not 76.2% / 23.8%. Root cause: the expanded canonicalization in
`build_enforcement_datasets.py` captures 113 more park-named
citations, shifting the distribution. Site prose still cites the
old figures.
(2) Westcrest's walkshed has regressed to 0.260 km² — below the
0.3 km² sanity threshold. The alpha-shape alpha=0.003 I set is too
tight at the edge of the OSM walk network; the same structural bug
the multi-seed fix was supposed to close has re-opened.
(3) Twelve of fourteen OLA host parks in `park-coordinates.csv`
have coordinate deltas > 100 m from the authoritative SPR ArcGIS
point. Codex's prior audit only fixed Westcrest and Genesee; the
rest still drift. Worst offenders: I-5 Colonnade 1,530 m, Woodland
922 m, Magnolia Manor 890 m.
(4) `METHODOLOGY.md` canonicalization breakdown (2,679 / 1,341) is
stale; actual after the expanded regex list is 3,449 / 571.

No SEVERE that invalidates the thesis. Three SEVERE that need
structural fixes this cycle.

## Would-I-cite-this

| Claim category | Confidence | Notes |
|---|---|---|
| OLA counts / inventory | 5 | SPR ArcGIS authoritative |
| Walkshed % (11.6 / 76.6) | 3 | Westcrest polygon regressed under alpha-shape — the union figure is an over-tight approximation at edges |
| 76.2% outside walkshed | 2 | Script output is now 77.2%; prose stale after canonicalization expansion |
| Enforcement revenue | 5 | Reproduces to the cent |
| Cost recovery 26% / 14% | 5 | Reproduces |
| Budget (SPR totals) | 4.5 | |
| Peer-city per-100K | 3 | TPL-reference denominator ≠ population column; documented inline but column name `population_year=2025` is misleading |
| Opinion arguments | n/a | Every data claim links |
| NYC precedent | 3 | Documented caveat |
| Spatial analysis | 2 | Westcrest bug back; park-coords drift not fixed |
| Reproducibility | 3 | 2 of 4 scripts reproduce; citation-rate drifted; Westcrest polygon depends on unpinned alphashape version |
| Dog-pop triangulation | 4 | Math reproduces; AVMA figures current |

---

## Findings

### SEVERE

**S1. `citation_walkshed_analysis.py` output drift.**
Committed CSV says 668 inside / 2,144 outside = 76.2% outside.
Re-running the script gives **668 inside / 2,257 outside = 77.2%
outside**, with 8 parks inside / 27 parks outside (not 29).

Root cause: `build_enforcement_datasets.py` was re-run after the
canonicalization list was expanded. The new canon collapses 113
additional rows that previously passed through as small-park names
(Gilman Playground/Playfield → Gilman Playground, Wallingford
Playground → Wallingford Playfield, Greenlake → Green Lake Park,
etc.). Those extra 113 citations are almost all outside walksheds
(77.2% vs 76.2%).

Every prose reference to **76.2% outside / 23.8% inside / 2,144 /
2,812 / 29 of 37 / eight sit inside** is now stale.

Files with stale numbers:
- `docs/part2-access.html` lines 757, 769, 787 — the Finding 02b
  stat-card and methodology footnote carry the 76.2/23.8/2,812.
- `docs/print.html` lines 502–503 — Part III stat row.
- `docs/part2-access.html` line 713 — chart aria-label still says
  "78.3% within SPR's 2.5-mile standard" (78.3% was the pre-alpha-
  shape 2.5-mi figure; current is 76.6%).
- `docs/print.html` line 414 — same chart aria-label mirror.

Fix: re-run `citation_walkshed_analysis.py`, update the six prose
callouts, update the chart aria-labels to 76.6%.

**S2. Westcrest walkshed regressed to 0.260 km² under alpha-shape.**
Section 5a/5b of the audit produced:

    Westcrest area=0.260 sqkm ✗  (sanity floor is 0.3)

Alpha-shape (α=0.003) is too aggressive for edge-of-OSM-network
OLAs whose reachable node cloud is sparse on one side. The bug the
multi-seed fix closed is back, just via a different tightening
step. Westcrest's OLA coordinate is still inside the polygon
(the 25 m buffer safety net holds), but the area is ~1/4 of peer
OLAs (range 0.7–1.8 km²).

Fix options:
- Loosen alpha: try 0.001 or 0.0005 and compare areas.
- Dynamic alpha: fall back to convex hull (or a looser alpha) when
  area < 0.5 km² for a specific OLA.
- Accept convex-hull results for OLAs with sparse node clouds,
  alpha-shape otherwise.

Downstream: the 11.6% / 76.6% walkshed population coverage is
slightly low because Westcrest and potentially other edge-of-network
OLAs are under-represented. A proper fix would shift these upward.

**S3. `park-coordinates.csv` still drifts from SPR ArcGIS for 12 of 14
OLA host parks.**

Section 5c result:
```
Magnuson Park              ✗  delta=201 m
Woodland Park              ✗  delta=922 m
Golden Gardens Park        ✗  delta=206 m
Dr. Jose Rizal Park        ✗  delta=588 m
Kinnear Park               ✗  delta=286 m
Denny Park                 ✗  delta=322 m
Plymouth Pillars           ✗  delta=398 m
Regrade                    ✗  delta=264 m
Blue Dog Pond              ✗  delta=444 m
Northacres Park            ✗  delta=152 m
I-5 Colonnade              ✗  delta=1,530 m
Magnolia Manor             ✗  delta=890 m
Genesee Park               ✓  delta=0 m
Westcrest Park             ✓  delta=0 m
```

Only Westcrest and Genesee were fixed in the prior audit (the two
Codex flagged). The remaining 12 still carry hand-geocoded
approximations that disagree with the authoritative SPR ArcGIS
point. Worst case — I-5 Colonnade — is 1.5 km off, which is almost
certainly dropping citations into the wrong walkshed category.

This is likely the real reason the 76.2 / 77.2 analysis is
imprecise: when a citation at a park is attributed to the OLA
walkshed, we check if the park's centroid (from park-coordinates.csv)
is inside any walkshed — but the park centroid may be 150–1,500 m
from the actual OLA. For I-5 Colonnade specifically, the park-coord
point could easily fall outside I-5 Colonnade's own walkshed.

Fix: reconcile all 14 OLA host park rows in `park-coordinates.csv`
to the `data/seattle-olas.csv` coords (same as I did for Westcrest
and Genesee). Add a provenance note per row.

### MODERATE

**M1. `METHODOLOGY.md` canonicalization breakdown is stale.**
Current text says "2,679 citations (55.8%) folded into one of the
43 canonical named-park entries" and "1,341 citations (27.9%) pass
through as named parks that the canonicalizer didn't know about."

Reality after the expanded regex list:
- 3,449 (71.8%) folded into canonical entries
- 571 (11.9%) pass through

Street-address (672 / 14.0%) and unknown (111 / 2.3%) rows are
unchanged. Combined not-spatially-attributable 16.3% still correct.

Fix: update both numbers in METHODOLOGY.md. The "43 canonical named-
park entries" count is also stale — current list has ~75 entries
after the expansion.

**M2. peer-cities.csv `population_year=2025` misleading.**
Every row has `population_year=2025`, but TPL 2025 ParkScore uses
ACS 2023 population for its per-100K metric (not the current OFM
April 2025 figure). So columns mix 2023-TPL (per_100k_tpl) with
2025-OFM (population). Seattle computed ratio is 1.71, stated 1.82.
The `note_on_per_100k` explains this, but the `population_year`
value itself is a foot-gun: it reads like "the denominator TPL
used," but actually means "when the population column was sourced."

Fix: rename to `population_year_column` or add a separate
`tpl_reference_population_year` column. Or, simplest, set
`population_year` to "2023" (matching TPL's actual reference) and
note in the column definition.

**M3. AVMA derivation rounding inconsistency.**
Several pages say "~248,500" (old 42.6% × 1.6 result) or "~248K" in
ambiguous places. Recomputed: 364,627 × 0.455 × 1.5 = **248,858**.
Site footprint per grep: 
- `docs/index.html` says ~248,500 (not updated to 248,900)
- `docs/opinion.html` says ~248,500
- `docs/part1-the-gap.html` shows 248,500 in two places
- `docs/print.html` shows 248,500 in two places

Fix: replace 248,500 → 248,900 (or 249,000) everywhere.

**M4. Sitemap.xml is out of date.**
`docs/sitemap.xml` lists 6 URLs. Missing: `peer-cities.html`,
`print.html`, `report.html` (redirect). `peer-cities.html` should
be in the sitemap (it's a full content page). `print.html` and
`report.html` can stay out if intentionally excluded from search
indexing; if so, `<meta name="robots" content="noindex">` should be
on both (it is on report.html; not checked on print.html).

Fix: add `peer-cities.html` to sitemap. Optionally confirm print.html
has noindex or add it to the sitemap too.

### MINOR

**m1. Chart aria-label on chartWalkshed shows stale 78.3%.**
`docs/part2-access.html:713` and `docs/print.html:414` both say
`aria-label="Horizontal bar chart: 99% ... 11.6% ... 78.3% within
SPR's 2.5-mile OLA standard."` The 78.3% was the pre-alpha-shape
figure; current is 76.6%. A screen-reader user hears the stale
value. Fix: 78.3 → 76.6 in both aria-label attributes.

**m2. AI disclosure present only on index.html.**
Audit prompt asked for consistent presence across reader-facing
pages. It's only on index.html (landing), not on part1/part2/
enforcement/budget/peer-cities/opinion. The print.html colophon
does carry a version of it. Borderline — the landing page is the
entry point for most readers, but an arriving-via-deep-link reader
on, say, enforcement.html doesn't see it without clicking to index.

Fix (optional): add a small "AI-assisted · human-verified" badge
or link in the footer of each content page pointing back to the
full disclosure on index.

**m3. `seattlecola.org` link returns SSL / connection error.**
Persistent TLS or server-name issue (observed through three audit
passes now). The site is real; cert is the problem. No action from
us, but worth noting.

**m4. Peer-city per-100K mismatches in Seattle, SF, Boise rows are
already documented but still round-trip ✗ under the audit's
"within rounding" check:**
- Seattle: 1.82 stated / 1.71 computed
- SF: 5.03 stated / 4.83 computed
- Boise: 7.60 stated / 7.50 computed

These are mixed-method on purpose (TPL denominator ≠ population
column). The `note_on_per_100k` column explains. Not a bug, but
the auditing script would flag these again on pass 4. Consider
splitting TPL's population into a separate column so the
round-trip check passes mechanically.

### INFO

- PDF cache-bust: `docs/index.html` query string `?v=3614056-1776549716`
  matches the committed PDF's size and mtime. ✓
- Live PDF byte-equivalent to repo PDF (content-length matches). ✓
- Enforcement fee sum, cost recovery, AVMA derivation, OLA acreage,
  residents-per-OLA all reproduce. ✓
- 14 OLAs / 30.7 acres / water 9 of 14 / three under 0.25 acre /
  $100,000 2018 budget / AVMA 45.5%/1.5 all consistent across
  pages after recent reconciliation. ✓
- No occurrences of the previously-stale figures (9.5%, 78.3%
  except the two aria-labels, 9.6%, 79.4%, 84.6%, 15.4%, $106,000,
  "four under 0.25", "4 sit inside", $210K, DC 20). ✓
- report.html redirect is live and correct. ✓
- build_enforcement_datasets.py + population_coverage.py reproduce. ✓
- citation_walkshed_analysis.py runs successfully but output
  differs from committed file (S1).

## Section 10: counter-research (not advanced this pass)

Skipped — Codex's prior pass covered Seattle 2016 Recreation
Demand Study and Fairfax County; I made the "no universal
consensus" softening already. No new NYC longitudinal evaluation
has surfaced between pass 1 and pass 3 that I'm aware of.

## Section 11c: mobile rendering

Not live-device-tested this pass. CSS inspection confirms the
480 px breakpoint was committed in the prior audit response.
Actual phone test still outstanding.

## What I deliberately did not audit

- Full external-link HEAD/GET pass (covered in prior audit;
  13 problematic URLs were fixed or documented as bot-blocked).
- Phone hardware test (CSS-only check last time).
- Accessibility screen-reader walkthrough (only added aria-labels;
  not verified against NVDA/VoiceOver).
- Counter-research beyond what Codex covered.
- Full search for paraphrase / plagiarism concerns on opinion.html.

## Recommended fix order

1. **S3 park-coordinates.csv drift** (mechanical, 10 min) — bulk-
   update all 14 OLA host rows to match seattle-olas.csv.
2. **S1 citation_walkshed drift** — re-run
   `scripts/citation_walkshed_analysis.py`, update six prose
   callouts + two aria-labels.
3. **S2 Westcrest walkshed regression** — tune alpha (try 0.001)
   or add per-OLA convex-hull fallback. Re-run downstream.
4. **M1 METHODOLOGY.md staleness** — update canonicalization
   breakdown 2,679/1,341 → 3,449/571.
5. **M3 AVMA rounding** — 248,500 → 248,900 across index, opinion,
   part1, print.
6. **M2 peer-cities `population_year`** — rename or add separate
   TPL-reference column.
7. **M4 sitemap** — add peer-cities.html.
8. **m1 aria-label 78.3 → 76.6** — two-line fix.
9. **m2 AI disclosure** (optional) — small footer badge on content
   pages.

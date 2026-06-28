# Full-site audit findings — seattledogparkdata.com

**Date:** June 28, 2026 · **Scope:** all nine public pages (`docs/*.html`) + the
data and scripts behind them, per `SITE-AUDIT-PROMPT.md`.

**Method:** read-only multi-agent discovery (per-page inventory of 996 numeric
claims → 10 per-dimension auditors → adversarial refutation of every substantive
finding → synthesis), then a lead-auditor verification pass that recomputed each
load-bearing figure from the committed CSVs before any fix was applied. 29 raw
findings; 6 were adversarially refuted as false positives (listed at the end).

**Status: COMPLETE.** Both verifiers pass; enforcement builder idempotent; all
mechanical fixes applied and re-verified; `verify_site_data.py` extended with 33
new checks (73 total) covering numbers neither verifier asserted before.

**Owner decisions now applied (June 28):** budget Finding 02 **Fix A** (one-time
capital removed from the disclosed bars) and the canonical-acreage choice (use
the most recent TPL vintage, **6,662**) — both were P0/P2 report-only findings
below, now resolved and guarded by the verifier. The one remaining open item is
confirming the paywalled Axios article's figures (awaiting pasted text).

---

## Headline result: the staffing-framing invariant is clean

The priority / most-error-prone dimension produced **zero** substantive
violations. The funded (**$528,279**) vs. attributable (**$152,399**) vs.
deployed (**~1 officer**) framing is stated consistently on `enforcement.html`,
`opinion.html`, `budget.html`, and `index.html`. No survivor of any retired
overclaim (`3× scale-up`, `even at 3× staffing`, `tripled cost`, `$700K–$1M`,
`about one`, `one patrols`, `funded staffing tripled`). The `2027` reference on
`updates.html` is correct (the 2023 MOA term runs through 2027-12-31; the 2026
MOA is a separate agreement). The JSON's 2026 `cost_per_citation` (4498) and
`per_total_fte` (32.5) are never rendered — every chart consumer filters 2026 —
so the partial-year ratios cannot mislead.

---

## Mechanical fixes applied (and re-verified)

| # | File:line | What | Before → After |
|---|-----------|------|----------------|
| 1 | `scripts/build_enforcement_page.py:104` → `docs/enforcement.html:86` | Dead Axios slug in staffing byline (canonical URL already used at `:191` and `opinion.html`) | `…/more-paw-patrols-seattle-ramping-up-dog-related-enforcement` → `…/seattle-animal-control-staffing-increase-off-leash-dogs-parks-enforcement` |
| 2 | `scripts/build_enforcement_page.py:171` → `docs/enforcement.html` | Cost-recovery window label was 12 years but the figures (`$351,099`, `$3.30M`) are the full 2014–2026 sums; sibling line and `<title>` say "13 years" | `Across 2014–2025` → `Across 2014–2026` |
| 3 | `scripts/build_enforcement_page.py:219` → `docs/enforcement.html:201` | First-offense chart aria lower bound contradicts chart data (2014 = 83.6%) and the page's own card/prose ("84% to 96%") | aria `consistently 85-96%` → `consistently 84-96%` |
| 4 | `docs/part2-access.html:825` | Quarter-acre OLA count: `seattle-olas.csv` has exactly 3 < 0.25 ac (Denny 0.105, Kinnear 0.124, Plymouth Pillars 0.2); page says "three" at L467/L584 | `four are under a quarter-acre` → `three are under a quarter-acre` |
| 5 | `docs/part1-the-gap.html:199` | Dogs:children ratio recompute: 150,000 ÷ 115,000 = 1.30 (chart/takeaway use the same inputs) | `roughly 1.4 to 1` → `roughly 1.3 to 1` |
| 6 | `docs/part2-access.html:688` | SF per-capita multiple: 1.38 ÷ 0.38 = 3.63 (Portland 1.29 ÷ 0.38 = 3.39 stays ~3.4×) | `San Francisco and Portland, ~3.4× and ~3.4×` → `San Francisco ~3.6× and Portland ~3.4×` |
| 7 | `docs/budget.html:150` | Space-per-dog aria: 168 ac × 43,560 ÷ (662,000 × 0.30) = 36.85 → 36.8 | Vancouver BC `36.7` → `36.8` |
| 8 | `docs/peer-cities.html:452` | NYC citation-label misdates the linked press release (lead L430, `opinion.html`, `part3.html` all say April 10; May 10 is the *effective* date) | `Off-Leash Hours Policy Approved (May 10, 2007)` → `(April 10, 2007)` |
| 9 | `docs/peer-cities.html` (L249, 256, 284, 291×2, 367, 416) | Millions-format drift: forced `.00` on round millions; rest of site is 17:0 against trailing zeros (`$168M`, `$507M`) | `$47.00M`/`$487.00M`/`$195.00M`/`$1.00M`/`$7.00M` → `$47M`/`$487M`/`$195M`/`$1M`/`$7M` |

Fixes 1–3 were made in the **builder** (never hand-edited the generated page),
which was then re-run; output is byte-identical on a second run (idempotent).

**Verifier extended:** `verify_site_data.py` gained two new sections (**+33
checks**). Section [5] covers acreage (6,662), the 14.6×/39× facilities ratios,
the per-capita multiples (SF 3.6× / Portland 3.4× / Vancouver 6.7×), the
quarter-acre count (3), the 22%-of-combined OLA share, the 5.37-sq-ft AVMA
space-per-dog reconciliation, and the budget Finding 02 basis-point series
(disclosed peak = 6.4 bp in 2016; 2024 disclosed bar = 4.0 bp) — with regression
guards that fail if `1.4 to 1`, `four are under a quarter-acre`, or `6,400 acres`
reappear, or if one-time capital is re-folded into the disclosed bars (which
would push 2024 back to 58.0 bp). Section [6] adds the complaint series the
enforcement verifier didn't assert (2025 total **3,010**, complaints-to-citations
**11**, Pearson **r = 0.13** recomputed over the page's 2024-04…2026-06 window).
The existing Vancouver expected value was synced 36.7 → 36.8.

> **Sanity-check requested on fix #8:** the change rests on the linked NYC Parks
> press release (id=19877) being dated April 10, 2007. That aligns with the four
> other on-site references, but the external document wasn't opened during the
> audit. Worth a 30-second confirm.

---

## Substantive findings — report only (not changed)

Ordered by severity. These touch wording, an argument, a judgment call, or
`opinion.html` voice, so per the ground rules they are reported, not auto-fixed.

### P0 — `docs/budget.html` Finding 02 chart contradicts its own prose
**Lines:** 107 (lead), 112 (aria), 118 (takeaway), 426 (annotation); chart JS 380–385.
**Issue:** The basis-point chart folds one-time Cycle 2 capital into each year's
bar. 2024 has a disclosed `ola_only_k=129`, so `IS_DISCLOSED[2024]=true` → it
renders as a **solid** "disclosed" bar at **(129+1730)/320,700 = 58.0 bp** — ~9×
the "6.4 bp 2016 disclosed peak" that the lead, aria-label, annotation, and
takeaway all assert is the maximum. The datalabel prints "58 bp" on it. The
takeaway's "dashed bars 2025–2026 reach 36–54 bp" is also stale: 2025 renders at
**104.9 bp**; "54" matches the *pre-capital* 2025 value. The prose predates the
capital-fold in the chart code.
**Verified:** independent recompute of all 11 bars reproduces 2016=6.4 (solid),
2024=58.0 (solid), 2025=104.9 (dashed), 2026=36.4 (dashed).
**RESOLVED — Fix A applied (June 28).** Removed `+ capK` from the `BP_VALUES`
formula so one-time Cycle 2 capital is no longer folded into the bars; reworded
the L111 subtitle and the L118 takeaway (the tall 2025–26 dashed bars are now
attributed to the combined OLA + P-Patch BSL tripling to ~$1.83M, not capital).
Post-fix: 2016 = 6.4 bp stays the tallest disclosed bar, the 2024 disclosed bar
drops 58.0 → **4.0 bp**, dashed 2025/2026 = 53.9/36.4 bp ("36–54" now accurate),
and all four prose claims hold. Locked by `verify_site_data.py` [5] (fails if any
disclosed bar exceeds 6.4 bp or capital is re-folded). `budget.html` is
hand-maintained (no builder).

### P1 — `docs/part3.html` stale per-park citation counts
**Lines:** 253, 267, 281.
**Issue:** States Magnuson **248** / Genesee **130** / Westcrest **86** for
2014–2019. The linked source (`enforcement.html` ← `data/enforcement-hotspots.csv`,
top-20 DLP 2014–2026) shows **367 / 152 / 122**. A reader who clicks through sees
different numbers. The part3 figures reconcile to *neither* the current window
*nor* a 2014–2019 recompute from `enforcement-citations.csv` (which gives ~260 /
151 / 89) — they predate the C263949 PRR ingest. The window itself also
mismatches (part3 says 2014–2019; the linked page uses 2014–2026).
**Primary source:** `data/enforcement-hotspots.csv` (367 / 152 / 122).
**Recommend:** Update to 367 / 152 / 122 and the window to 2014–2026 to match
`enforcement.html`; add the Enforcement cross-link to the Genesee (L267) and
Westcrest (L281) sentences (currently unsourced, while the L359 footer promises
every claim links to its source). `part3.html` is hand-maintained. *Reported
rather than auto-fixed because it changes a stated analysis window and the
surrounding interpretive prose — a substantive edit.*

### P2 — `docs/opinion.html:509` "6,400 acres" vs. canonical 6,662
**Issue:** The rhetorical line "drive 6,400 acres hoping to catch someone" uses
6,400 where the site's sourced figure is **6,662** (TPL 2025 ParkScore;
`peer-cities.csv`; used on part1 ×2, part2 ×2). **Conflicting dimension verdicts:**
the consistency auditor flagged it; the source auditor *refuted* it because 6,400
is a sourced rhetorical round of the **6,414** acres in the repo's own 2016 MOA
(`sources/aco-moa-2016.md`) and `sources/andre-qacc-thread-2019.md` uses the exact
phrase "over 6,400 acres." Net: a cross-page consistency wrinkle on a rhetorical
line in the signed editorial, **not a hard error**.
**RESOLVED — set to 6,662 (June 28).** Per the owner's call to use the most
recent TPL vintage, `opinion.html:509` now reads "drive 6,662 acres." The site
is now consistent on 6,662 everywhere; the older 6,414 figure remains only inside
`sources/aco-moa-2016.md`, where it correctly records what the 2016 MOA said.
Guarded by `verify_site_data.py` [5] (fails if "6,400 acres" reappears).

### P3 — minor sourcing / clarity (report only)
- **`docs/part3.html:250, 266`** — MOLG IRS EIN `91-2059268` and the "1997 City
  Council vote made OLAs permanent" claim have no adjacent source, while the L359
  footer promises full sourcing. Add an IRS/990 link and the Council ordinance
  record, or soften the footer claim.
- **`docs/peer-cities.html:416`** — Minneapolis revenue hypothetical uses a
  180,000-dog figure with no citation (not in `peer-cities.csv`). Cite it or
  label it an illustrative assumption.
- **`docs/peer-cities.html:490`** — Boise "~1.6× per capita" is **correct** on the
  page's TPL per-100k basis ((7/18 × 7.60)/1.82 = 1.62); a naïve raw-population
  division gives 1.7×. Optional one-line note that the multiple uses the per-100k
  basis, to prevent reader confusion. No numeric change.
- **House style (CLAUDE.md "spell out acronyms on first use per page"):**
  `peer-cities.html` uses bare "OLA" from L249 but doesn't expand "off-leash area
  (OLA)" until L528; `part1-the-gap.html:61` shows the "OLAs" stat-tile label two
  lines above its L64 expansion. Minor; expand at first use if you want strict
  compliance. *Left for review since they touch prose wording.*

### Verified correct — no change (was a suspected error)
- **`enforcement.html:241/259` "top 10 parks … 46% before COVID and 40% after."**
  The synthesizer flagged 40% as "no matching JSON value / not machine-checked."
  That was a conflation: it is **not in the page-data JSON, but it *is* already
  asserted** by `verify_enforcement_data.py:611–612`, which recomputes both
  shares from the raw `enforcement-citations.csv` (each period's own top-10 over
  park-named citations) and greps the prose. Independent recompute confirms
  **pre = 46.3%** and **post = 40.0% exactly**. Both correct and both guarded.
  No change and no new check needed — the existing one already covers it.

---

## Reproducibility status

| Check | Result |
|-------|--------|
| `verify_enforcement_data.py` | **ALL CHECKS PASSED** (post-fix) |
| `verify_site_data.py` | **ALL CHECKS PASSED** (post-fix; +29 new checks across sections [5] and [6]) |
| Enforcement builder idempotent | **Yes** — identical SHA on second run |
| JSON `year_trend` ↔ `enforcement-year-metrics.csv` ↔ `build_enforcement_metrics.py` | **Agree** on 2026 staffing (funded 528279 / traceable 152399 / aco_fte 1.0 / funded_aco_fte 3.0); funded-vs-attributable band reconciles (528279−152399 = 375,880; 454652−152399 = 302,253 → the "$300K–$376K" band) |
| JSON 2026 `cost_per_citation` 4498 / `per_total_fte` 32.5 | **Harmless** — never rendered (all chart consumers filter year ≠ 2026) |
| `docs/data/*` mirrors `data/*` | **In sync**; no CSV changed, so `sync-data.sh` not required |
| All repo-internal blob/tree links | **Resolve** to existing local files (4 MOAs, 10 PRRs, 6 PRR-response dirs, all CSVs) |
| Cumulative cost / recovery | **$3,295,689 ≈ $3.30M**, fee revenue **$351,099**, recovery **10.7%** ("~11%") — all on the full 2014–2026 basis (consistent after fix #2) |

---

## Open questions for the owner

1. **Parkland acreage — RESOLVED.** Owner chose the most recent TPL vintage
   (6,662); `opinion.html:509` updated and the site is now consistent on 6,662.
   Optional: update `CLAUDE.md`'s "resolve which is canonical" note to record it.
2. **Budget Finding 02 — RESOLVED.** Fix A applied (see the P0 entry above).
3. **part3 per-park counts:** confirm the update to 367 / 152 / 122 and window
   2014–2026 (matches `enforcement.html`).
4. **Residual verifier hardening (optional):** the 46%/40% top-10 shares are
   already asserted (`verify_enforcement_data.py:611–612`), and the complaint
   figures (3,010; 11:1; r=0.13) are now asserted (`verify_site_data.py` [6]).
   Still unguarded: the full per-year JSON series (offense_mix counts, per-year
   cost/per-FTE for years beyond 2018/2022/2024, top-20 ranks 6–20) — all
   recompute correctly today but aren't pinned against a future data refresh.
   Low priority.
5. **Axios provenance — VERIFIED (owner supplied the text).** Article: "Seattle
   expands dog-rule patrols before summer," Christine Clarridge, Apr 17 2026
   (spokesperson Kasey Smith, SPR). It **does** support every claim the site pins
   to it: "one officer assigned to parks (Wednesday–Saturday)… plans to expand to
   two full-time seven-day positions plus backup," "filling and training the two
   vacant positions," and "26 park rangers patrolling more than 460 parks." What
   is **NOT** in Axios — the three-FTE funded count, the dollar figures
   ($152,399 / $454,652 / $528,279 / per-hour rates), "funded in 2023," and "~33%
   of calls for service (2021)" — traces to the 2023/2026 MOAs and PRR C265341,
   and the site cites them there (byline L86, chart-source L169, the headcount
   footnote, and opinion.html:395 which explicitly frames it as "Axios reported
   [2 seven-day + backup], **but the records show** [3 approved in 2023]").
   Provenance is intact; no misattribution to Axios.
   **One citation to confirm — `opinion.html:404`:** cites the piece as
   `"More paw patrols," April 2026 (print edition)`. The current web headline is
   "Seattle expands dog-rule patrols before summer"; "More paw patrols" matches
   the *original URL slug* (`/more-paw-patrols-…`), which strongly suggests Axios
   first published under that headline and later retitled it. So the citation may
   have been accurate at access time. Decide: update to the current title, or
   keep the as-accessed headline (optionally noting "as published April 2026").
6. **Park count — no drift.** The audit's "485+/460 parks" worry is moot: the
   public site states **no** Seattle park count ("485" and "460" appear nowhere;
   the lone "997 parks" is a peer city). Axios's "more than 460 parks" is
   available if you ever want to add one, but there's nothing to reconcile.
7. **Stale PDF:** `docs/seattle-dog-parks-report.pdf` predates current site copy
   — regenerate via `build-pdf.mjs` (separate, deliberate step; not done here).

Per the ground rules I did **not** bump site-wide dates, the editorial
signature, `CHANGELOG.md`, or `updates.html` — those are separate,
human-approved steps.

---

## False positives caught and dropped (adversarial pass)

- **A5** (`opinion.html` "unsourced" numbers) — Smith Cove 55,000→25,000 sq ft *is*
  in the linked `sources/nextdoor-qa-playfield-2021.md`; the ranger count cites
  Axios in-line; "city of 8 million" (NYC) is a correct round.
- **A6** (`index.html` summary tiles) — figures reconcile to linked pages;
  cross-links are adequate for a homepage; pure citation-density opinion.
- **B4** (`peer-cities.html` Boise 1.6×) — correct on the page's per-100k basis
  (retained only as an optional clarity note).
- **C3 / C4** (enforcement complaint figures + per-year JSON "not machine-checked")
  — all recompute exactly; moved to the hardening list, not errors.
- **J1** (`updates.html` "through 2027") — accurate; the 2023 MOA term ends
  2027-12-31.

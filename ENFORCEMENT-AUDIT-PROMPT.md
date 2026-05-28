# Independent audit prompt — Seattle off-leash enforcement dataset

Copy everything below the line into a fresh LLM session that has read access to this
repository (`seattledogparkdata.com`). It is written to be self-contained: it tells the
auditor what to reproduce, what the expected answers are, and — critically — which
assumptions to *distrust* rather than take on faith.

---

You are auditing a civic-data analysis of Seattle's off-leash dog-area (OLA) enforcement,
2014–2026. Your job is to **independently reproduce every number** from the **raw source
files** and report discrepancies. Do not trust the consolidated CSVs or the HTML prose —
they are the thing under test. Recompute from the raw XLSX upward.

Treat this as adversarial verification. A passing check is only meaningful if you computed
the expected value yourself from primary data. If you find yourself copying a number from a
derived file to "confirm" it matches that same derived file, stop — that proves nothing.

## What the data is

Two Seattle public-records requests, combined to cover the full period:

- **C049204** — `data/prr-responses/C049204/*.xlsx` (5 files). Covers **2014 – Oct 2019**.
  DLP-only (Dog Loose in Park, SMC 18.12.080(A)). Old format: one worksheet *per offense
  level per year-range* (e.g. sheet "1st Offense 2014-15"), ~14 columns, a date column
  (`issued_at`), a fee column, an address column. One citation per row.
- **C263949** — `data/prr-responses/C263949/*.xlsx` (4 files). Covers **2019 – 2026-04-17**.
  *All* parks-related violation types, not just DLP. SSRS report export, so the layout is
  awkward: report parameters occupy rows 0–1, the real **header is on row 3** (0-indexed),
  data starts **row 4**, there are ~49 columns, and the final column carries a
  `"Total Violations: N"` sentinel string on a trailing row that is **not** a data record.
  Column map (0-indexed): CaseID=2, Violation Item=10, Fee=18, Officer=19, Issue Date=20,
  Result=21, District=34, Location=42, ZIP=45. **CaseID is not unique** — do not dedupe on it.

### The 2019 overlap rule (load-bearing)

2019 appears in *both* PRRs. C049204's 2019 is partial (Jan–Oct) and DLP-only; C263949's
2019 is the full calendar year and all-category. The pipeline **drops C049204's 2019 rows
entirely** and uses C263949's 2019 as authoritative. Verify this is done correctly: there
should be **no** C049204-sourced rows with `year == 2019` in the consolidated output, and
2019's DLP count should come from C263949.

## The pipeline (what you're checking)

- `scripts/build_enforcement_datasets.py` → `data/enforcement-citations.csv` (one row per
  citation, both PRRs merged, extended schema) + `data/enforcement-by-park-year.csv`.
- `scripts/build_enforcement_metrics.py` → `data/enforcement-year-metrics.csv` (per-year
  derived metrics + the staffing/cost model).
- `scripts/verify_enforcement_data.py` → ~120 invariant checks (the existing harness).
- `scripts/build_draft.py` + `scripts/draft_page_data.json` → `docs/enforcement-draft.html`.

Run `.venv/bin/python scripts/verify_enforcement_data.py` and confirm it passes — but then
go *beyond* it, because the verifier shares code and constants with the builders and so
cannot catch a wrong shared assumption. Your value is in the things the harness can't see.

## Ground truth to reproduce (recompute these from raw XLSX, don't read them back)

Consolidated row counts: **7,532** total citations = **3,774** from C049204 + **3,758**
from C263949. DLP-only rows: **7,015**.

Per-year `data/enforcement-year-metrics.csv` (DLP-only series unless noted):

| year | dlp | all | aco_fte | fmw_fte | annual_cost | cost/cit | cit/FTE | 1st-off % | fee_rev | partial |
|------|-----|-----|---------|---------|-------------|----------|---------|-----------|---------|---------|
| 2014 | 183 | 183 | 0.5 | 0.0 | 76,200 | 416 | 366.0 | 83.6 | 11,746 | no |
| 2015 | 519 | 519 | 0.5 | 0.0 | 76,200 | 147 | 1038.0 | 88.8 | 31,881 | no |
| 2016 | 952 | 952 | 0.75 | 0.75 | 219,299 | 230 | 634.7 | 87.5 | 59,634 | no |
| 2017 | 844 | 844 | 1.0 | 1.0 | 292,399 | 346 | 422.0 | 85.9 | 53,750 | no |
| 2018 | 1276 | 1276 | 1.0 | 1.0 | 292,399 | 229 | 638.0 | 85.5 | 52,547 | no |
| 2019 | 1181 | 1360 | 1.0 | 1.0 | 292,399 | 248 | 590.5 | 87.9 | 56,176 | no |
| 2020 | 393 | 446 | 1.0 | 1.0 | 292,399 | 744 | 196.5 | 91.9 | 16,663 | no |
| 2021 | 471 | 559 | 1.0 | 1.0 | 292,399 | 621 | 235.5 | 91.5 | 24,716 | no |
| 2022 | 169 | 199 | 1.0 | 1.0 | 292,399 | 1730 | 84.5 | 91.7 | 7,497 | no |
| 2023 | 248 | 285 | 1.0 | 1.0 | 292,399 | 1179 | 124.0 | 94.0 | 10,714 | no |
| 2024 | 447 | 514 | 1.0 | 1.0 | 292,399 | 654 | 223.5 | 96.4 | 14,446 | no |
| 2025 | 267 | 326 | 1.0 | 1.0 | 292,399 | 1095 | 133.5 | 95.9 | 10,121 | no |
| 2026 | 65 | 69 | 1.3 | 1.0 | 338,119 | — | — | 90.8 | 1,208 | yes |

Totals: DLP **7,015**; cumulative cost **$3,341,409**; fee revenue **$351,099**;
cost-recovery **10.5%**. 2026 is partial (through 2026-04-17, day 107/365 ≈ 29.3%, annualize
×3.41) and intentionally emits **blank** cost/citation and cit/FTE so the partial denominator
doesn't inflate the ratios.

## Assumptions to SCRUTINIZE, not accept

These are the soft spots. Spend your time here.

1. **Cost constants.** `FAS_ACO_ANNUAL = 152399` should match
   `data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf` Attachment A
   ($43.07/hr × 1.45 × 2,088 + $3,000 + $19,000 = $152,398.73). **`FMW_ANNUAL = 140000` is
   an author estimate, not sourced** — SPR publishes no per-FMW off-leash line. This is the
   single most load-bearing soft number; the whole 10.5% cost-recovery headline moves with
   it. Run a sensitivity: at $80K it's ~13.5%, at $200K ~9%. Decide whether the page is
   honest about this uncertainty.

2. **The FTE schedule** (`STAFFING` dict in `build_enforcement_metrics.py`): 0.5 ACO pre-2016,
   0.75+0.75 in the 2016 transition, 1.0+1.0 for 2017–2025, 1.3+1.0 for 2026 YTD. Pre-2016
   and the 2016 transition are **imputed from PRR context**, not documented. Note that the
   cost-per-citation and cit/FTE *charts* deliberately start at **2016** because the imputed
   pre-2016 FTEs produce artifacts (2015 would otherwise show the lowest cost/citation and
   highest per-FTE, contradicting the narrative). Check that the charts honor this cutoff
   while the raw *volume* bars still span 2014–2026.

3. **DLP classification.** The old PRR is DLP by construction (sheet names). The new PRR
   mixes violation types; `dlp_only` is derived by pattern-matching the Violation Item text.
   Pull the distinct Violation Item strings from C263949 yourself and judge whether the
   regex/patterns correctly partition DLP from scoop/other. A misclassification here shifts
   every per-year DLP count.

4. **Location canonicalization.** `location_canon` is normalized from free-text addresses for
   the hotspot map and per-park rollups. Spot-check that distinct spellings of the same park
   collapse together and that distinct parks don't collapse into one.

5. **2026 annualization.** Confirm the cutoff date, the day-count (107/365), and that the
   annualization factor is only ever applied to the *projection*, never silently baked into
   a reported actual.

6. **2014 completeness.** Confirm 2014 is a full calendar year (it spans 2014-01-06 →
   2014-12-20, all 12 months) — the low 183 count is real, not a partial/startup artifact.

7. **Prose vs. data.** The verifier checks the CSVs but does **not** parse `enforcement-draft.html`
   prose against the data. Manually grep the HTML for every hardcoded number (cost-per-citation
   values, percentages, peak/low years, the "X% cost recovery" line, top-park counts) and
   confirm each against your recomputed figures. Past audits caught hand-typed prose errors
   here ($1,716 vs. correct $1,730; a "85–96%" range whose floor is actually 83.6%).

## Deliverable

A discrepancy report: for each checked claim, state (a) the value on the page / in the CSV,
(b) the value you computed from raw XLSX, (c) match or mismatch, and (d) if mismatch, the
likely cause. Call out any place the analysis claims more precision than the underlying data
supports, and any assumption that, if wrong, would flip a headline conclusion.

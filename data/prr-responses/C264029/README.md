# PRR C264029 — Seattle dog-licensing counts & revenue, 2014–2025

## Request

Sent by Andre Vrignaud via the Seattle Public Records Request Center on **2026-04-18**
(C264029-041826). Requested from the Seattle Animal Shelter (SAS):
1. Annual count of **active dog licenses**, 2014–present, by year, ZIP, and altered status.
2. Annual count of **new** licenses (vs. renewals), to distinguish enrollment from renewal.
3. SAS's **compliance-rate** estimate (licensed vs. unlicensed dogs) + methodology.
4. Annual **dog-license fee revenue**, broken out from other animal licenses.
5. Any internal **dog-population** estimate (licensed + unlicensed), 2020 or later.

## Response

- **PRR number:** C264029-041826
- **Responding agency:** Seattle Animal Shelter (Dept. of Finance & Administrative Services)
- **Released:** June 2026

| Item | Status | File |
|---|---|---|
| #1, #2 | provided | `2014-2025PDR.xlsx` |
| #4 | provided | `SAS_Licensing_Data_2014-25_revenue.xlsx` |
| #3 (compliance estimate) | **no responsive records** | — |
| #5 (population estimate) | **no responsive records** | — |

That SAS holds **no** compliance or dog-population estimate (items #3, #5) is itself a
finding: the city does not publish, or apparently maintain, a figure for what share of
Seattle dogs are licensed.

## Files

- **`2014-2025PDR.xlsx`** — 265,741 rows, one per **dog license issued** 2014–2025.
  Columns: `Renewal Yes/No` (Yes = renewal, No = new), `Date Issued`, `Species` (all Dog),
  `Altered` (spayed/neutered Yes/No), `Postal Code` (home), `Mailing Postal Code`,
  `Prev Postal Code`. Each row is an **issuance on a date — not a snapshot of active
  licenses**; active counts can only be estimated (no license-term field).
  **2025 caveat (per SAS):** the city moved to 1-year-only licenses and the portal could
  not renew 2-year licenses, so renewals were reissued as "new" — the 2025 new-vs-renewal
  split is unreliable; the 2025 total is fine.
- **`SAS_Licensing_Data_2014-25_revenue.xlsx`** — annual dog-license General Fund revenue.
  **2015** = actuals through Nov + projected Dec; **2017** = incomplete (excluded from
  trend). This revenue funds the **entire** Seattle Animal Shelter, not the off-leash
  program.

## Derived datasets

`scripts/build_licensing_datasets.py` produces, in `data/`:
- `licensing-by-year.csv` — issuances/year, new vs. renewal, altered share.
- `licensing-by-zip.csv` — issuances by home ZIP (pooled), with neighborhood labels.
- `licensing-revenue.csv` — annual revenue with partial-year flags.

## Headline figures (see `Dog_Licensing_Findings_2026-06-08.md`)

- Dog licenses issued fell ~21% (24,309 in 2014 → 19,219 in 2025).
- Active licensed dogs (modeled): ~20,000–41,000.
- Estimated licensing compliance: **~10–27%** of the 150,000–400,000 dog-population range
  (our estimate; SAS publishes none).
- Dog-license revenue ≈ **$1.24M/year** (2018–2024 average).

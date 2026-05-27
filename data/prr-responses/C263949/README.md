# PRR C263949 — Park enforcement violations, January 2019 through April 17, 2026

## Request

Sent by Andre Vrignaud via the Seattle Public Records Request Center on **2026-04-17**. The request is a date-range extension of the original 2019 PRR (C049204) — it asks for parks-related off-leash violations from the end of the previous response onward.

> Hello, I previously made the request below, and received data for 2014 -> part of 2019. I would like to request the same data, but for all of 2019 -> as current as we can get… [Original 2019 request text follows; see the PRR copy at `prrs/01-spr-offleash-citations-post-2019.md`.]

The 2019 PRR was narrowly scoped to **Dog Loose in Park** offenses across four offense levels. The 2026 request was interpreted by SAS/FAS more broadly as "parks-related violations," and the response therefore includes additional violation types (Fail to Obtain License, Permit Animal at Large, Failure to Vaccinate, Fail to Have Scoop Equipment, etc.) alongside Dog Loose in Park. Year-over-year comparisons against C049204 should restrict the new data to the `Parks Code - Dog Loose in Park (Nth Offense)` rows to stay apples-to-apples; the broader denominator is useful but is a different denominator than the prior response provided.

## Response

- **PRR number:** C263949-041726
- **Responding agency:** Seattle Department of Finance & Administrative Services (Seattle Animal Shelter)
- **Public Disclosure Officer:** Sarah Stark
- **Release date:** May 8 – May 15, 2026 (file mtimes; cover letter dated May 26, 2026)
- **Records released:** four Excel workbooks covering the four two-year windows below.

## Files

The release is a SQL Server Reporting Services (SSRS) export. Each workbook has one sheet with the structure:

- Row 0: SSRS internal column names (`textbox3`, `Textbox127`, etc.)
- Row 1: report parameter values (date range, filters)
- Row 2: blank
- Row 3: data column headers (CaseID, CaseType, CaseResolution, etc., plus 41 cryptic `Textbox###` columns)
- Row 4 onward: one row per violation. Some columns contain ragged/merged values because the report serializes nested groups; column positions are stable but not all columns are populated on every row.

A "Total Violations: N" sentinel appears in column 48 of every data row in each file as a built-in row-count check.

| File | Sheet | Period | Data rows | Sentinel |
|---|---|---|---:|---:|
| `CaseViolationDetail-2019-2020_Release.xlsx` | `CaseViolationDetail 2019-2020` | 2019-01-01 – 2020-12-31 | 1,806 | 1,806 |
| `CaseViolationDetail-2021-2022_Release.xlsx` | `CaseViolationDetail 2021-2022` | 2021-01-01 – 2022-12-31 | 758 | 758 |
| `CaseViolationDetail-2023-2024_Release.xlsx` | `CaseViolationDetail 2023-2024` | 2023-01-01 – 2024-12-31 | 799 | 799 |
| `CaseViolationDetail-2025-2026YTD_Release.xlsx` | `CaseViolationDetail 2025-4.17.2` | 2025-01-01 – 2026-04-17 | 395 | 395 |
| **Total** | | | **3,758** | |

Original filenames (with spaces) were renamed on import to use hyphens for shell compatibility; raw bytes are preserved unchanged.

## Column map (column index → meaning)

The SSRS export's `Textbox###` column headers are not self-describing. Position-based mapping derived from data inspection — see `scripts/build_enforcement_datasets.py` for the canonical version used by the build pipeline:

| Index | Meaning | Example values |
|---:|---|---|
| 2 | CaseID | `5392060` (one case can have multiple violation rows) |
| 8 | Violation # | `12575181` for citations, placeholder `1` for warnings |
| 9 | Violation type label | `Citation` (always) |
| 10 | Violation Item | `Parks Code - Dog Loose in Park (1st Offense)`, `Fail to Obtain License`, `Permit Animal at Large or Trespass`, etc. |
| 11 | Violation Status | `Issued`, `Closed` |
| 13 | Statute / Code | `18.12.080(A)`, `9.25.080(A)`, etc. |
| 18 | Fee | `$0` (warning), `$54` (1st), `$109` (2nd), `$125` (license fail), `$136` (3rd), `$162` (4th+) |
| 19 | Issuing officer (short form) | `Rogers Brett` |
| 20 | Issue date / time | datetime |
| 21 | Result | `Warning`, `Citation`, `Voided Citation`, `Pending`, `Guilty`, `Dismissed` |
| 29 | Incident date / time | datetime |
| 32 | Issuing officer (formal) | `Rogers, Brett` |
| 34 | Patrol district | `Central`, `Southwest`, `Northwest`, `Northeast`, `South`, `North` |
| 42 | Location (free text) | `Lincoln Park`, `West Queen Anne Playfield`, sometimes a street address |
| 44 | State | `WA` |
| 45 | ZIP | `98136` |
| 48 | File-level sentinel | `Total Violations: 1806` repeated on every row |

## CaseID is not a row key

CaseID repeats across multiple violation rows whenever a single case produced multiple violations (e.g. dog loose **plus** fail to obtain license on the same encounter). Of 3,758 rows, only 583 distinct CaseIDs are present — most cases produced multiple violation rows. Do not dedupe by CaseID. The natural row key is `(source_file, row_index)` — every row in the export is a distinct violation record.

## Overlap with PRR C049204

The 2019-2020 file overlaps with C049204's 2019 rows (which ran Jan 1 – Oct 15, 2019). The two PRRs are **not row-level interchangeable** because:

1. C049204 returned only `Parks Code - Dog Loose in Park` rows. C263949 returned all parks-related violations.
2. The 2019 C049204 data was sliced into four sheets (one per offense level). C263949's 2019 rows live in one flat sheet.

`scripts/build_enforcement_datasets.py` handles the overlap by **dropping all 2019 rows from C049204 and using C263949's full-year 2019 as the authoritative source**, then preserving an explicit `dlp_only` flag on each row so the page can render the historical DLP-only series and the broader all-violations series independently.

## Relevance to the site

This response closes the multi-year gap that the site has flagged since launch in `prrs/01-spr-offleash-citations-post-2019.md`. Charts and findings primarily affected:

- `docs/enforcement.html` — Finding 02 year trend, Finding 01 hotspot map, Finding 05 offense mix, Finding 06 revenue vs. cost. All of these need to be re-built against the extended dataset.
- `docs/index.html` — citation-related landing-page summary.
- `docs/opinion.html` — enforcement program cost framing.

## Caveats

- **Different scope from C049204.** The 2026 PRR was answered with all parks-related violation types, not just Dog Loose in Park. Pre-2019 numbers and post-2019 numbers therefore have different denominators unless filtered to DLP-only. The build script preserves this distinction in the `dlp_only` column.
- **COVID confounds the 2020 dip.** Park access patterns and patrol staffing both changed in 2020. The drop from 1,360 (2019) to 446 (2020) reflects both fewer violations and fewer patrols.
- **Pending and voided rows.** ~299 rows have `result = Pending` (not yet adjudicated). ~33 rows have `result = Voided Citation` or `Canceled Citation`. The build script preserves them with their flagged status so the page can report enforcement output (officer issued the record) vs. revenue-realized (fee actually collected) separately.
- **Officer concentration.** Across 2019–2026, two officers (Brett Rogers, Jon Wieringa) account for ~44% of all violations. The named officer in the original 2019 PRR context (Rand Hillman) does not appear in any 2019+ records. Program output is highly dependent on a small number of individual rangers.
- **Location free-text.** Same field, same caveats as the C049204 response: park names are inconsistently formatted ("Warren G. Magnuson Park" vs "Magnuson"), street addresses appear for ~10% of rows. The canonicalization regex in `scripts/build_enforcement_datasets.py` handles both PRRs uniformly.

## Reproducibility

Every row of every workbook is folded into the consolidated CSV at `data/enforcement-citations.csv` by `scripts/build_enforcement_datasets.py`. The verification harness at `scripts/verify_enforcement_data.py` re-derives all summary statistics from that CSV and asserts they match the per-file sentinels and the prior-version row counts. Run both end-to-end to confirm a clean rebuild:

```bash
.venv/bin/python scripts/build_enforcement_datasets.py
.venv/bin/python scripts/verify_enforcement_data.py
```

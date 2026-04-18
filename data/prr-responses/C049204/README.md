# PRR C049204 — Seattle Parks & Recreation off-leash violation enforcement data

## Request

Sent by Andre Vrignaud to `PKS_PDR@seattle.gov` on **2019-08-29**.

> In 2014 the Seattle Parks and Recreation (SPR) department created a new People, Dogs, and Parks plan at the request of the Seattle City Council. A common complaint of non-dog owners was that dogs were often run offleash at city parks, and data was collected and shown that showed a heatmap of violations. As a response, SPR hired two additional staffers (one named Rand Hillman) to patrol parks and issue citations.
>
> I would like to formally request any data, reports, or presentations (even if just discussed in email) that exists showing changes in the frequency or location of these sorts of citations since these two staffers began patrolling. To be a bit more specific, I am hoping to understand whether or not this investment in additional enforcement has had an effect, and if so, how much.

## Response

- **PRR number:** C049204
- **Response date stamp in filename:** 2019-10-15 (`101519`)
- **Files released to requester:** 2020-01 (five xlsx files, produced in rolling batches per file mtimes)

## Files

Every sheet across all five files shares the same 14-column header:
`Total Violations · Case Result · Violation # · Violation Type · Violation Item · Violation Status · Item Code · Fee · …`

| File | Sheet | Rows | Period covered |
|---|---|---:|---|
| `C049204-101519_Final-1.xlsx` | 1st Offense 1.1.19–10.15.19 | 917 | 2019 Jan 1 – Oct 15 |
| | 2nd Offense 1.1.19–10.15.19 | 75 | 2019 Jan 1 – Oct 15 |
| | 3rd Offense 1.1.19–10.15.19 | 25 | 2019 Jan 1 – Oct 15 |
| | 4th Offense 1.1.19–10.15.19 | 16 | 2019 Jan 1 – Oct 15 |
| `C049204-101519_Final-2.xlsx` | 1st Offense 2018 | 1,092 | 2018 |
| | 2nd Offense 2018 | 126 | 2018 |
| | 3rd Offense 2018 | 43 | 2018 |
| | 4th Offense 2018 | 19 | 2018 |
| `C049204-101519_Final-3.xlsx` | 1st Offense 2017 | 726 | 2017 |
| | 2nd Offense 2017 | 77 | 2017 |
| | 3rd Offense 2017 | 26 | 2017 |
| | 4th Offense 2017 | 19 | 2017 |
| `C049204-101519_Final-4.xlsx` | 1st Offense 2016 | 834 | 2016 |
| | 2nd Offense 2016 | 77 | 2016 |
| | 3rd Offense 2016 | 24 | 2016 |
| | 4th Offense 2016 | 21 | 2016 |
| `C049204-101519_Final-5.xlsx` | 1st Offense 2014-15 | 615 | 2014 Jan 1 – 2015 Dec 31 |
| | 2nd Offense 2014-15 | 68 | 2014–2015 |
| | 3rd Offense 2014-15 | 10 | 2014–2015 |
| | 4th Offense 2014-15 | 13 | 2014–2015 |

Header rows included in the row counts above. Total data rows after header subtraction is 4,803, matching the consolidated `data/enforcement-citations.csv`.

## Column notes

- `Fee` — 1st-offense rows are typically `$0` (verbal warning) or `$54` (citation). Escalation steps are `$109` (2nd), `$136` (3rd), `$162` (4th+). SMC 18.12.080(A) is the legal reference.
- `Violation Item` — free-text location label (park name, street address, or blank). This is the `location_raw` source in the consolidated CSV; `location_canon` is a manual canonicalization for the top ~40 parks, and `location_type` (`park_named` | `street_address` | `unknown`) classifies each row.
- `Case Result` — `Verbal` (warning), `Citation`, `Dismissed`, etc.
- `Violation #` / `Violation Type` / `Violation Status` / `Item Code` — SPR-internal codes preserved in `enforcement-citations.csv` but not currently used in any analysis.

## Relevance to site

Primary source for every chart and number on [docs/enforcement.html](../../../docs/enforcement.html):
- Citation hotspot map (Finding 01)
- Year-by-year trend (Finding 02)
- Offense-mix (Finding 05)
- Revenue vs cost (Finding 06)

Complements the 2016 SPR owner-survey data cited in `part2-access.html` (the "39% admit monthly+ illegal off-leash" figure), which measures self-reported behavior rather than enforcement output.

## Caveats to watch for

- Citation counts reflect **enforcement activity**, not underlying violation rates. A drop could mean fewer violations *or* fewer patrols.
- Geographic distribution may reflect where rangers were deployed, not where violations concentrate. SPR deployment patterns over 2014–2019 are not in this dataset; a separate PRR would be needed.
- `location_raw` is free-text with inconsistent formatting ("Warren G. Magnuson Park" vs "Magnuson park" vs "Magnuson Park - Athletic Fields"). The canonicalization step in `scripts/build_enforcement_datasets.py` collapses the top ~40 parks to stable names; 672 rows remain as street addresses and 111 rows have no location at all.
- The PRR's cutoff is 2019-10-15; citations issued 2019-10-16 onward are **not** in this dataset. A follow-up PRR for 2019-10 through present has been filed (draft at `prrs/01-spr-offleash-citations-post-2019.md`).

## Consolidated output

Every row of every sheet is flattened into a single long-format CSV for analysis:

- `data/enforcement-citations.csv` — 4,803 rows, one per citation, with `year`, `offense_level`, `location_raw`, `location_canon`, `location_type`, `zip`, `issued_at`, `fee`, `case_result`, `source_file`, `source_sheet`.

Build the CSV from the raw xlsx files with:

```bash
.venv/bin/python scripts/build_enforcement_datasets.py
```

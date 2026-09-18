# PRR C264837 — OLA-only vs P-Patch spending inside BSL BC-PR-50000 (2023–2026)

## Request

Filed by Andre Vrignaud via the Seattle Public Records Request Center (**C264837-042426**),
April 2026, as the SPR leg of [PRR #3](../../../prrs/03-spr-ola-budget-split.md). The City
routed the same request to three departments; the other two closed with no responsive
records (City Budget Office `C263991-041726`, Department of Neighborhoods `C264838-042426`).
SPR owns BC-PR-50000, so this is the response that matters.

The request asked four things: OLA-only spending inside the BSL, P-Patch-only spending inside
the same BSL, the internal allocation methodology used to split the two, and the Cycle 2
one-time OLA capital handled separately from the BSL.

## Response

- **PRR number:** C264837-042426
- **Responding agency:** Seattle Parks and Recreation (SPR)
- **Author of record:** Gerald Asp (document properties; created 2026-07-15T23:11Z)
- **Released:** 15 July 2026
- **Volume:** one Word document, two budget tables

### What's committed here

- [`documents/`](documents/) — the response `.docx` as received (31 KB).
- [`text/response-and-tables.txt`](text/response-and-tables.txt) — the response prose plus
  both tables as plain text.

**The tables are not text in the original.** SPR pasted them as embedded EMF vector images
(`word/media/image1.emf`, `image2.emf`), so `pdftotext`, `textutil`, and every ordinary docx
reader return the surrounding prose and nothing else. The figures in `text/` and in
[`data/ola-ppatch-master-projects.csv`](../../ola-ppatch-master-projects.csv) were recovered
by parsing the `EMR_EXTTEXTOUTW` records out of the EMF streams. If you re-derive them, that
is the method; do not assume a blank table means an empty table.

## What it says

**1. The split is tracked, as two Master Projects.** This is the direct answer to the
question the site has been carrying as unanswerable. Inside BC-PR-50000 there are two Master
Projects, and SPR reports budget and spend against each:

| Master Project | Name |
|---|---|
| `MC-PR-51002` | Improve Dog Off Leash Areas |
| `MC-PR-51001` | Rejuvenate P-Patches |

On methodology (request item 3) SPR wrote, verbatim: *"They are different Master Projects
within BC-PR-50000, and the budget and spending is split out as per the above."* There is no
staff-hours or acreage allocation formula, because nothing is being allocated: the two are
booked separately at source.

**2. The two Master Projects are the whole BSL.** Their adopted budgets sum to the combined
BC-PR-50000 figure already in [`data/budget-detail.csv`](../../budget-detail.csv) for three of
the four years, to the dollar:

| Year | OLA adopted | P-Patch adopted | Sum | `ola_ppatch_combined_k` | Delta |
|---|---:|---:|---:|---:|---:|
| 2023 | 328,345 | 241,216 | 569,561 | 569,561 | 0 |
| 2024 | 333,478 | 280,865 | 614,343 | 584,343 | **30,000** |
| 2025 | 1,568,818 | 260,899 | 1,829,717 | 1,829,700 | 17 (rounding) |
| 2026 | 1,574,370 | 271,335 | 1,845,705 | 1,845,700 | 5 (rounding) |

The 2024 gap is exactly $30,000 and is a vintage difference, not a discrepancy: the repo's
2024 figure is the **endorsed** number from the 2023-Adopted/2024-Endorsed budget book
(PRR C265589); this response gives the **adopted** number. Both are recorded. Do not
"reconcile" one into the other.

**3. The $3.1M capital is inside the BSL, not beside it.** On request item 4 SPR wrote:
*"The $3.1M is included in the BC-PR-50000 above, within the MC-PR-51002 Improve Dog Off
Leash Areas Master project."* This is why the OLA line jumps from ~$330K in 2023–24 to
~$1.57M in 2025–26. Any presentation that adds a separate capital line **on top of** the
combined BSL double-counts it.

**4. Roughly $600K of that capital has been spent, all of it on paper.** Verbatim: *"Of the
amount spent so far within the MC-PR-51002 Master project roughly $600K has been spent
towards planning and design for the West Seattle Stadium OLA and Othello Playground OLA
projects between January 1st 2023 and July 7th, 2026. Construction at these two sites is
currently estimated to begin in Early 2027."*

**5. The money is largely unspent, and the shortfall opens exactly when the money arrives.**
Across 2023 through 7 July 2026, MC-PR-51002 carried a revised budget of **$5,625,926** and
recorded **$1,053,037** in expenses: **18.7%**, leaving **$4,362,265** available.

The year-by-year burn is the more informative series:

| Year | Revised budget | Expenses | Burn |
|---|---:|---:|---:|
| 2023 | 416,256 | 315,049 | 75.7% |
| 2024 | 434,685 | 218,996 | 50.4% |
| 2025 | 1,784,507 | 368,398 | 20.6% |
| 2026 (to 7 Jul) | 2,990,479 | 150,593 | 5.0% |

2025 is the inflection: the revised budget quadrupled and the burn rate fell by more than
half. 2026 carries that forward, with the revised budget nearly double the adopted.

**Do not claim OLA is uniquely bad at spending.** P-Patch burned 32.0% across the closed
years 2023–25 against OLA's 34.2% — effectively the same. The distinctive facts are the
**absolute** balance ($4.36M) and the **direction** of the OLA series, not a comparison
against P-Patch execution.

Both 2026 columns are **year-to-date through 7 July 2026** and are not comparable to a closed
year. The 2026 revised budget ($2,990,479) is nearly double the 2026 adopted ($1,574,370),
consistent with carryforward of unspent prior-year appropriation, though the response does
not say so explicitly.

## What this supersedes

The site has carried an OLA-only figure of **$126,000 (2023)** and **$129,000 (2024)**,
attributed in `data/budget-detail.csv` to "Parkways blog / Seattle Times 2023-24 coverage."
**No source for those figures has ever been identified.** Searched September 2026: the two
Parkways posts cited in [`sources/SOURCES.md`](../../../sources/SOURCES.md) (the Feb 2024
Expansion Study recommendations and the Sept 2022 Cycle 2 financial plan) contain no OLA
dollar figure at all, and the Mayor's Park District Cycle 2 fact sheet contains no OLA line
beyond $450K for seven-day off-leash and scoop-law enforcement.

Because MC-PR-51002 plus MC-PR-51001 exhaust the BSL, $126,000 cannot be the OLA share of
BC-PR-50000. The primary record puts it at **$328,345 (2023)** and **$333,478 (2024)**,
about 2.6× higher.

The site's companion inference, that P-Patch is therefore the larger share, does not survive
either, but the correct answer depends on which measure you use, and the three disagree:

| Measure | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Adopted budget | OLA 57.6% | OLA 54.3% | OLA 85.7% | OLA 85.3% |
| Revised budget | P-Patch 60.5% | P-Patch 64.7% | OLA 69.9% | OLA 79.2% |
| Actually spent | OLA 66.3% | P-Patch 56.9% | OLA 59.0% | OLA 63.9% |

Any sentence on the site that names one of these must name which one. The Cycle 2 capital
lands inside the OLA Master Project in 2025–26, which is what drives OLA to ~85% of the
adopted BSL in those years; it is not a maintenance increase.

Correcting the site is a separate, deliberate act and had not been made when this README was
written. See the recommendations attached to this ingest.

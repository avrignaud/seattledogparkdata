# PRR C265589 — 2026 SPR/FAS Animal Control Officer MOA + Park District budget book

## Request

Sent by Andre Vrignaud via the Seattle Public Records Request Center
(**C265589-050126**). Requested the **current (2025–2026)** inter-departmental agreements
and expenditure authorizations under which SPR is expanding Animal Control Officer (ACO)
coverage for park-based dog enforcement — the documents that supersede or amend the signed
2021 MOA (AG21-PRF03-032) and the 2023 MOA (PRF1602). Specifically: (1) the current
MOU/MOA, (2) its Attachment A / per-FTE cost basis, (3) total authorized FTE and annual
cost, (4) the 2025–2026 budget line items (BSL / program / ledger codes), and (5) any
internal planning memos or council presentations.

Filed after the [Axios Seattle report (2026-04-17)](https://www.axios.com/local/seattle/2026/04/17/seattle-animal-control-staffing-increase-off-leash-dogs-parks-enforcement)
that the program was moving from one park-assigned officer toward two full-time seven-day
positions plus backup.

## Response

- **PRR number:** C265589-050126
- **Responding agency:** Seattle Parks and Recreation (SPR)
- **Public Disclosure Officer:** Rachel Acosta
- **Released:** June 2026 (request closed; "all responsive records" provided)

SPR provided two records:

1. **"FAS PARKS_ACO MOA_2026.pdf"** — the signed 2026 SPR/FAS MOA. Canonical copy archived
   in [`data/moas/`](../../moas/SPR-FAS-ACO2-MOA-2026.pdf).
2. **"SPR_2023Adopted_2024Endorsed.pdf"** — the City of Seattle 2023 Adopted / 2024
   Endorsed budget book (responsive to items #4–5). This is a published public document;
   not re-committed here to avoid a 1.6 MB binary. Key responsive pages:
   - p.107 — **Park Safety Program** (Park District Cycle 2): Expenditures **$448,640**,
     Position Allocation 2.00, "adds funding to hire **2 additional Animal Control Officers
     (ACOs) in FAS and 2 Maintenance Laborers in SPR**, supporting 2 additional teams
     dedicated to enforcement on SPR property." This is the 2023 authority behind the 1→3
     ACO expansion and confirms the 2023-era SPR-side paired role was a Maintenance Laborer
     (FMW).
   - **BC-PR-50000 Maintaining Parks and Facilities** BSL purpose statement: funds "to
     improve existing P-Patches and dog off-leash areas" — confirms OLA budget is bundled
     with P-Patches.
   - Off-leash planning line: "$200,000 in both 2023 and 2024 for planning related to three
     new off-leash areas, with funding for construction of two of them planned later in
     Cycle 2."

## Key findings (vs. the 2023 MOA)

| | 2023 MOA (PRF1602) | 2026 MOA |
|---|---|---|
| Term | through 2027-12-31 | through **2026-12-31** (one year) |
| Signed | AP Diaz (SPR) / K. Grove (FAS), Apr 2023 | **M. Finnegan, Interim Supt.** (SPR) / K. Grove, Director (FAS), 2026-05-29 |
| Top hourly rate | $44.79 | **$54.46** (with AWI) |
| Per-FTE | $151,551 | **$176,093** |
| 3-FTE FAS-side | $454,652 | **$528,279** (authorized maximum) |
| Billing | flat 240 hr/pay period | **variable labor on actual hours worked** + fixed costs regardless |
| Headcount language | "three ACO II positions" | "**up to** three ACO II FTE … any number of positions" (6,264 hr cap) |
| SPR-side paired role | Facilities Maintenance Worker (FMW) | **Park Ranger** |
| Reporting | Parks Code Violation Dashboard | + **PetPoint**; rangers trained on PetPoint |
| Budget codes | Paying Org FAI01; Billing Project FA4MSSASENF | Paying Org **PRF20**; Billing Project **FA4000130** |

**Bottom line:** the 2026 MOA does not expand scope — it re-prices the 2023-authorized
three-ACO program for wage growth and (per the Axios reporting and SPR's own statement)
the program is still filling positions authorized in 2023. The corps was **funded** at
three since 2023; **actual** deployment was ≈one officer as of April 2026.

> **Update (July 2026) — where the "up to three" language came from.** This README noted the
> 2026 MOA's vague headcount language without being able to explain it. PRR
> [C266465](../C266465/README.md) supplies the drafting history, and it also fills the gap in
> the MOA series: the intervening **[2025 MOA](../../moas/SPR-FAS-ACO2-MOA-2025.pdf)** (signed
> 2025-07-28, cap $508,695) is the document that actually introduced "up to three … any number
> of positions" and actual-hours billing. The 2026 MOA inherits it.
>
> The sequence: Sep 2024, SPR's own Community Services manager recommends **cutting** the
> program to 2 or 1 ACO; Jan 2025, a 2-ACO MOA is drafted; **2025-02-24** the Interim Deputy
> Superintendent sends it back to 3 "given AP's priority with off leash"; **2025-02-26** FAS
> replies it can staff "closer to 2 FTEs," possibly "1.5 – 2.0." The flexible headcount is the
> compromise. C266465 also produced quarterly **ledger backup** confirming SPR was billed
> **$456,173 in FY2024** for three staff on flat calendar-derived invoices — so the
> funded-vs-deployed gap is now documented on the spend side, not just inferred.

## Why this matters for the site

Drives the June 2026 update to the [Enforcement page](../../../docs/enforcement.html#finding-02)
(Finding 02 funded-vs-deployed band, cost footnote) and [Opinion O1](../../../docs/opinion.html#O1).
The cost model constants live in
[`scripts/build_enforcement_metrics.py`](../../../scripts/build_enforcement_metrics.py)
(`FAS_ACO_ANNUAL_2026`, `FAS_ACO_TOTAL_2026`). Open thread on the SPR-side Park Ranger
cost is filed as [PRR #10](../../../prrs/10-spr-ranger-pairing-cost.md).

# PRR C266465 — "Making Parks Safer" program evaluation, deployment and decision records (2016–present)

## Request

Filed by Andre Vrignaud via the Seattle Public Records Request Center (**C266465-050826**),
May 2026. Requested the records that would let a member of the public assess whether the
joint SPR/FAS Animal Control Officer park-patrol program ("Making Parks Safer") **produced
an outcome** — evaluations, briefings, deployment logs, trend analysis, the decision record
for the 2026 staffing expansion, community-partner correspondence, and any prior audit.

The 2019 PRR [C049204](../C049204/) returned the program's *citation output*. This request
asked for everything on the other side of the ledger: what the City knew about whether the
program worked, and what it decided as a result.

## Response

- **PRR number:** C266465-050826
- **Responding agency:** Seattle Parks and Recreation (SPR)
- **Public Disclosure Officer:** Rachel Acosta
- **Released:** July 2026 (single installment; request closed, "all responsive records")
- **Volume:** 112 files / ~720 Bates pages (`PKS_C266465_01_00001`–`00720`), of which
  **90 are unique documents** — the release contains 16 duplicate copies, mostly of the
  2021-generation MOA circulated as an email attachment across many threads.

### What's committed here, and why

- [`documents/`](documents/) — the 17 load-bearing records as original PDF/XLSX (12 MB).
- [`text/`](text/) — `pdftotext -layout` output for **all 101 distinct documents** in the
  release, named by Bates number (1.5 MB). This is OCR, not a substitute for the original,
  but it makes every Bates citation in the index below checkable.

**These binaries are committed deliberately.** The [C265589 README](../C265589/README.md)
declined to commit a 1.6 MB budget book because that document is published on seattle.gov and
retrievable any time. These records are not: they exist only because of this request, the
City's download link expires 30 days after closure, and the records may be downloaded only
three times. Do not "clean up" these files on the strength of the C265589 precedent — it does
not apply.

The full 105 MB release (including duplicate copies and the two 164-page scans of the draft
plan) is not committed.

## Responsiveness matrix

| # | Requested | Produced? | What actually came back |
|---|---|---|---|
| 1 | Internal evaluations / after-action reviews of the 2016 expansion | **Partial** | No program-*effectiveness* evaluation exists. One internal review does: the **Jainga memo** (`00353`, Aug 2024) and its expanded version (`00360`, Sep 2024). It tracks raw output counts, finds them falling, and recommends **shrinking** the program. Nothing measures compliance, complaint volume, or deterrence. |
| 2 | Council / commissioner / executive briefings on effectiveness | **Partial** | Three Council/Board decks (`00681` Aug 2022, `00451`/`00635` Dec 2021, `00416` Feb 2024) and the **FAS SLI response** (`00524`, Jun 2022). All describe activity and staffing; none report an effectiveness measure. |
| 3 | **Patrol deployment logs / dispatch records / shift summaries by location** | **No** | Nothing responsive produced. The MOAs require monthly location-level reporting (§5) and a Parks Code Violation Dashboard; no such report appears in the release. This absence is the finding. |
| 4 | Compliance / behavior / complaint-trend analysis beyond raw citations | **No** | Nothing responsive. |
| 5 | Decision record for the 2026 staffing expansion | **Yes — the strongest material in the release** | A complete Oct 2022 → Feb 2025 paper trail (see chronology below), including the Council budget action, the staff recommendation to cut, the override, and FAS's statement that it lacked the capacity to staff what the MOA funds. |
| 6 | Correspondence with community partners (COLA, MOLG, etc.) | **Partial** | Standing SPR↔COLA bi-monthly OLA meeting minutes (`00613`, Apr 2023) and Colonnade OLA threads (`00557`, `00563`, `00700`). Maintenance coordination, not effectiveness analysis. |
| 7 | Prior PRR / council request / audit asking similar questions | **Partial** | The 2022 Council **SLI FAS-003-B-001** (`00491`, `00524`) is the closest prior instrument. No City Auditor or performance-audit record was produced. |

**Bottom line:** items 3 and 4 produced nothing. The City funds this program, bills for it
monthly, and reports headcount to Council — but the release contains no record of anyone
measuring whether it changes behavior. The one internal review that exists recommended
cutting the program in half.

## Chronology: how the three-officer program was decided

| Date | Event | Source |
|---|---|---|
| 2014 | Council SLI 69-1-B-1 requests an OLA master plan; SPR defers pending Park District approval | `00002` |
| Jun 2016 | Draft *People, Dogs & Parks Plan* to Council. Park District funds a **two-person dog-park patrol team** from **late March 2016** — "the first time since the mid-1990s the City has had staff dedicated to enforcing the Animal Code in parks" | `00002`, `00004` |
| Jun 2022 | FAS Director's **SLI response** to Council: enforcement is failing for structural reasons; recommends OLA expansion + education alongside enforcement | `00524` |
| **Oct 2022** | Council budget action **FAS 128_SAS_P** adds **two 1.0 FTE ACO II** positions, Park District Levy funded — **$315,231 (2023) / $319,978 (2024)**. This is the 1→3 expansion authority | `00603` |
| Apr 2023 | 2023 MOA (PRF1602) signed — three ACO II, flat **240 hr/pay period** billing, term through 2027-12-31 | [`moas/`](../../moas/) |
| 2023 | The paired SPR **Facilities Maintenance Worker accepts a Park Ranger post and is never backfilled**. "There is no current FMW working with the Animal Control Officers." The program's paired-team design is broken from this point | `00360` |
| Dec 2023 | SPR budget staff notice the MOA bills a flat annual rate: "we pay on an annual hourly basis not on actual work performed (i.e., section 7 does not say 'up to' 240 hour/pay period)" | `00469` |
| Aug–Sep 2024 | **Jainga memo**: output down year over year; proposes **Option 1** — cut to 2 ACO (save $151,550) — or **Option 2** — cut to 1 ACO (save $303,101) | `00353`, `00360` |
| Jan 2025 | SPR circulates a draft MOA "scaled to 2 ACOs" | `00359` |
| **Feb 24 2025** | Interim Deputy Superintendent Daisy Catague overrides: "I would like to update MOA to reflect **3 ACO (instead of 2)** given AP's priority with off leash." The attached draft (`00475`) is the 2-ACO version — $169,565/FTE, **$339,130** for two — carrying her tracked comment on the cost table: *"This section needs to be updated to reflect 3 ACO"* | `00474`, `00475` |
| **Feb 26–28 2025** | FAS replies it can commit "closer to 2 FTEs," possibly "only … 1.5 – 2.0 FTEs." Resolution: keep the MOA at **"up to 3 based on actual hours worked"** | `00541` |
| Jul 28 2025 | **2025 MOA signed** (AP Diaz / K. Grove) — first MOA with "up to three … any number of positions," 6,264 hr cap, actual-hours billing, max **$508,695**. Term ends five months later | [`SPR-FAS-ACO2-MOA-2025.pdf`](../../moas/SPR-FAS-ACO2-MOA-2025.pdf) |
| Sep 2025 | SPR notices **no FAS/ACO charge** has posted; internal scramble over who supplies data to FAS | `00648`, `00507`, `00513` |
| May 29 2026 | 2026 MOA signed — same structure, re-priced to $528,279 | [`moas/`](../../moas/) |

The **"up to three … any number of positions"** language that the
[C265589 README](../C265589/README.md) flagged in the 2026 MOA originates here: it is the
drafting resolution of a February 2025 disagreement between what SPR wanted to fund (3) and
what FAS could staff (1.5–2).

## What the program produced

From the Jainga memo (`00353`), SPR's and FAS's own tracking — archived as
[`data/enforcement-program-activity.csv`](../../enforcement-program-activity.csv):

| Year | Staff | Verbal warnings | Written warnings | Citations | Revenue | Park exclusions |
|---|---|---|---|---|---|---|
| 2023 | ACO II | 880 | 2 | **42** | $2,652 | **0** |
| 2024 | ACO II | 586 | 2 | **28** | $1,704 | **0** |
| 2023 | SPR Park Ranger (Jun–Dec) | 307 | 4 | 0 | — | 0 |
| 2024 | SPR Park Ranger (Jan–Aug) | 366 | 3 | 1 | — | 0 |

> **Do not merge these counts with `data/enforcement-citations.csv`.** They are different
> record systems counting different universes. The citation dataset (PRR C263949) holds 248
> dog-loose-in-park records for 2023 and 447 for 2024, of which 35 and 21 carry
> `case_result = Citation`. The memo's figures come from the SAS/SPR internal data-tracking
> app. The two systems have the same shape once `case_result` is read: the citation dataset's 2023/2024 rows marked `Citation` are 35 and 21 against the memo's 42 and 28, and its verbal warnings 159 and 350 against 880 and 586 (the app logs contacts the citation system never records). Neither the citation counts nor the verbal-warning counts
> (880 vs 159; 586 vs 350) reconcile. The memo's value is that it supplies a **contact
> denominator the citation record does not have** — roughly 1,235 documented program
> contacts in 2023 against 42 citations.

## What the program cost — actuals, not authorizations

Three quarterly ledger workbooks (`00480`, `00485`, `00653`, extracted to
[`documents/enforcement-moa-billing.csv`](documents/enforcement-moa-billing.csv)) are the
first **actual-expenditure** records the project has for this line:

- **FY2024 billed: $456,173** for three staff.
- **H1 2023 billed: $226,528** (Q3/Q4 2023 not produced) — annualizing to ~$453,000.

The invoices are **calendar-derived, not timesheet-derived**: every week is billed at a flat
40 hours × $44.79 per staff × 3 staff, computed from the number of weekdays in the month.
There is no record of hours actually worked. A Sep 2023 SPR email confirms the pattern —
"It appears we are getting charged every quarter for that $113K" (`00479`).

So for 2024: **$456,173 billed, 28 citations written, $1,704 collected, 0 park exclusions**
— while FAS was internally stating it could field 1.5–2.0 officers, not 3.

## Other findings in this release

- **SPR could not source its own access claim.** SPR told Council in Dec 2021 and Aug 2022:
  "Among the top 12 park systems in the country, TPL ranks Seattle in the top 5 in terms of
  access to dog parks per capita" (`00635`, `00681`). On 2022-07-21 an SPR policy staffer
  asked the deck's author to "point me to the source of that info" (`00634`). **No reply
  appears in the release**, and the claim was presented to Council on Aug 3 2022 unchanged.
  (Absence of a reply in this production is not proof no reply was sent.)
- **The City's own peer comparison.** The FAS SLI response (`00524`) puts Seattle at **1.9
  OLAs per 100k residents** against Portland 4.9 and San Francisco 6.5 — the same
  directional gap the site reports, from the City's own report to Council. Uses the loose
  peer-city counting conventions noted in `CLAUDE.md` §2.
- **FAS attributes non-compliance to OLA supply.** "The lack of available Off Leash Areas
  could encourage pet owners to take their dogs off leash in regular City parks … Dog owners
  consistently share with SAS that OLAs aren't within walking distance and are overcrowded"
  (`00524`).
- **Enforcement is structurally broken.** Park users refuse to identify themselves; SPD
  response times to ACO assistance requests run **60–120 minutes**; without ID no citation
  can issue (`00524`).
- **2021 patrol baseline.** ACO IIs patrolled **344 of 489 parks (70%)** in 2021; parks
  patrols were 1,850 responses, 33% of all Field Services calls (`00524`).
- **OLA capital backlog.** The plan's Section 7 (`00168`) prices deferred capital work at
  every OLA: **$1,150,000–$2,220,000 (2016 dollars)**, against Park District OLA maintenance
  of $103,000–$117,000/year. Kinnear: $6,000–$11,000, ranked **LOW** priority.
- **Draft-vs-final plan discrepancy.** The June 2016 draft summary quotes the capital range
  as **$718,000–$1,363,000**, contradicting its own Section 7 total of $1,150,000–$2,220,000.
  The Aug 2017 final drops the $718K figure and keeps only the Section 7 total.
- **Park District OLA funding, precisely.** Draft summary: "$106,000 annually through 2020."
  Final: "between $103,000 and $117,000 annually" (pp. 3, 5) **and** "$106,000 annually
  through 2020" (Cost of Services, p. 19) — both figures survive into the final. The site's
  round "$100,000/year" is a floor. *(Corrected 2026-09-12; an earlier version of this line
  wrongly implied the final carried only the range.)*
- **2024 OLA Expansion Study** (`00416`): 32 candidate sites → 9 meeting criteria → 4,753
  survey responses → 3 recommended (West Seattle Stadium 87% support, Othello 73%, Ravenna
  61%). Ravenna's stated rationale includes that the park is "already experiencing
  unsanctioned off leash activity." SPR names **Capitol Hill, Ballard, Northgate** as
  unaddressed gaps, and flags that the "current MPD budget only includes funding for design
  of [the] 3rd OLA." **East Queen Anne Playfield** is listed as a recommended future site.

## Bates index — documents not archived here

`00001` Aguirre transmittal · `00004`/`00177` June 2016 **draft** People, Dogs & Parks Plan
(the Aug 2017 final is in [`sources/`](../../../sources/)) · `00341`/`00343`/`00348`/`00355`/
`00372`/`00446`/`00465`/`00470`/`00481`/`00486`/`00654` 2021-generation MOA copies ·
`00352`/`00376`/`00530` Jainga memo transmittals · `00359` "scaled to 2 ACOs" draft ·
`00370`/`00444` 2023 MOA Adobe Sign records · `00387`/`00411` BPRC agendas ·
`00389`/`00400` BPRC minutes (Feb/Mar 2024) · `00413`/`00414`/`00415` unrelated ARC invite ·
`00430` 2025 MOA signature completion · `00436`/`00438`/`00590`/`00662`/`00670` 2021 MOA
routing form (AG21-PRF03-032) · `00450`/`00451`/`00635` Dec 2021 Council OLA deck ·
`00464`/`00469`/`00474`/`00493`/`00494`/`00498`/`00503`/`00507`/`00509`/`00513`/`00516`/
`00545`/`00658`/`00695`/`00696` MOA revision email chain 2023–2025 (`00475`/`00494`/`00503`/
`00545`/`00696` are successive 2025-MOA drafts; `00475` is the 2-ACO version Catague marked
up to 3) · `00490`/`00491`/`00520`/`00549` SLI drafting chain · `00521` SAS case-view report
(Attachment A) · `00523` Nextdoor/Facebook screenshots (Attachment B) · `00551` duplicate SLI
response · `00557`/`00563`/`00700` Colonnade OLA threads · `00577`–`00584` signage photos ·
`00596`/`00599`/`00706`/`00710`/`00715` Park District
vs General Fund appropriation confusion for the two new ACO posts · `00606` constituent
complaint · `00585`/`00586` the unsigned **21 Dec 2022 three-team draft** MOA ($46.58 top
rate; $468,422 for 3 FTE), circulated Mar 2023 alongside "the signed one team" agreement ·
`00612` COLA minutes transmittal · `00616`/`00617` Feb 2017 Mayor's briefing
paper on the plan · `00625`/`00627`/`00629`/`00630`/`00632` Lake City / Little Brook dog
outreach packet · `00676` Aug 2022 deck transmittal · `00720` 2017 park-exclusions thread.

## Follow-on requests this release justifies

1. **Monthly parks-data summary reports** required by MOA §5 — already filed as
   [PRR #9](../../../prrs/09-spr-aco-monthly-parks-reports.md). This release confirms the
   reports are the only route to location-level deployment data, since item 3 produced none.
2. **Q3/Q4 2023 and 2025–2026 ledger backup** — completes the actual-spend series.
3. **FAS/SAS-held records** for items 3 and 4 — **already filed as PRR C266744**, the
   FAS-side twin of this request. The two responses interlock: FAS states its *only*
   responsive records are officer truck logs and dispatch broadcast logs, and SPR (here)
   produced none of those but did produce the decision record. Between them, both custodians
   have now confirmed **no program-effectiveness evaluation exists anywhere in the City**.
   The narrowed July-2025 truck-log installment on C266744 remains pending.

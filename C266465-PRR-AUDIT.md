# PRR C266465 — findings and proposed site changes

**Status: draft for review. Nothing on the site has been changed.**
Repo archiving is done ([`data/prr-responses/C266465/`](data/prr-responses/C266465/),
[`data/moas/SPR-FAS-ACO2-MOA-2025.pdf`](data/moas/SPR-FAS-ACO2-MOA-2025.pdf),
[`data/enforcement-program-activity.csv`](data/enforcement-program-activity.csv)).
Site edits below are proposals, per the review-before-publishing rule.

---

## The one-sentence version

The City has run this enforcement program for ten years, bills roughly $455,000 a year for
it on invoices computed from a calendar rather than from hours worked, has never measured
whether it changes behavior, and when its own manager reviewed the output in 2024 and
recommended cutting the program in half, leadership overrode him and kept funding three
officers that the staffing agency said it could not supply.

---

## What's genuinely new

### 1. There is no effectiveness evaluation — and now that's documented, not inferred

Request items 3 (deployment logs) and 4 (compliance/complaint-trend analysis) produced
**nothing**. Item 1 produced one internal review, the Aug/Sep 2024 Jainga memo, which counts
raw output and recommends shrinking.

This is a tighter claim than "SPR never looked," and it pairs with what
[PRR C266744](data/prr-responses/) established about the dispatch logs. The precise,
defensible statement:

> Across ten years and on the order of $3 million in ACO-side billing, the City produced one
> internal review of this program. It counted warnings and citations, found both falling,
> and recommended cutting the program by one-third to two-thirds. No record of a compliance,
> deterrence, or complaint-trend analysis exists.

### 2. Actual spend, not just authorization — closing a gap the project has had since the start

`CLAUDE.md` §3 says the honest answer on OLA-only spending is "we don't know." That's still
true for the *OLA maintenance* line. But for the **ACO enforcement** line, we now have
ledger backup:

| Period | Billed (3 staff) |
|---|---|
| 2023 Q1 | $113,455 |
| 2023 Q2 | $113,073 (net of a −$190.70 adjustment) |
| 2023 Q3–Q4 | *not produced* |
| 2024 Q1 | $113,391 |
| 2024 Q2 | $113,073 |
| 2024 Q3 | $114,855 |
| 2024 Q4 | $114,855 |
| **FY2024 total** | **$456,173** |

The invoices are **calendar-derived**: 40 hours × $44.79 × 3 staff per week, computed from
the number of weekdays in each month. Not one line reflects hours actually worked. Meanwhile
FAS was telling SPR it could field 1.5–2.0 officers.

**This is the strongest single finding in the release** because it converts the site's
cost-per-citation figure from *authorized* to *spent*, and because the billing mechanism is
independently verifiable from the spreadsheet arithmetic.

### 3. A contact denominator the citation record never had

| 2023 | Verbal | Written | Citations | Revenue | Exclusions |
|---|---|---|---|---|---|
| ACO II | 880 | 2 | 42 | $2,652 | 0 |
| Park Ranger (Jun–Dec) | 307 | 4 | 0 | — | 0 |
| **Total contacts** | **~1,235** | | **42** | | **0** |

⚠️ **Reconciliation caveat — this matters.** These figures do **not** match
`data/enforcement-citations.csv`. That dataset (PRR C263949) holds 248 dog-loose-in-park
records for 2023 (35 marked `Citation`) and 447 for 2024 (21 marked `Citation`). The memo
says 42 and 28. Verbal warnings diverge far more: 880 vs 159 in 2023.

Two different record systems, two different universes. **Do not put these numbers in the
same chart.** The correct use is as an independent second source that supplies a denominator
— total documented enforcement contacts — which the citation dataset cannot provide.

The reason this is worth the trouble: it pre-empts the obvious rebuttal to the site's
cost-per-citation framing, that the program's product is *education*, not tickets. The
City's own tracking answers that. Across 2023–2024 the ACOs logged **1,540 contacts**, of
which 70 were citations and **4 were written warnings**, with **zero park exclusions**
(2,221 contacts and 5 written warnings including the Park Rangers). Whatever the product is,
essentially nothing in the record escalates past a verbal warning.

### 4. The decision record — the expansion was a preference, not a finding

The chronology in the
[PRR README](data/prr-responses/C266465/README.md#chronology-how-the-three-officer-program-was-decided)
is the whole story. Compressed:

- Oct 2022 — Council funds two more ACOs from the Park District Levy ($315,231/yr).
- 2023 — the paired SPR maintenance worker leaves and is never replaced. The two-person-team
  design, which is the entire premise of the program going back to 2016, is broken from
  here on.
- Sep 2024 — SPR's manager reviews output, proposes cutting to 2 or 1 officer.
- Jan 2025 — a 2-ACO MOA is drafted.
- **Feb 24 2025** — the Interim Deputy Superintendent sends it back: 3, not 2, "given AP's
  priority with off leash." Her tracked comment sits on the cost table of the draft itself.
- **Feb 26 2025** — FAS: we can commit "closer to 2 FTEs," maybe "1.5 – 2.0."
- Jul 2025 — the MOA is signed funding "up to three … any number of positions," billed on
  actual hours.

That last line is the answer to the question the C265589 README left open about why the 2026
MOA's headcount language went vague. It's the drafting compromise between a number leadership
wanted and a workforce that didn't exist.

**Careful with attribution.** "AP's priority" is Catague characterizing AP Diaz's priorities
in an internal email. Diaz signed the 2025 MOA; by the 2026 signing the Superintendent is
M. Finnegan (Interim). Quote the email; don't build a narrative about any individual beyond
what it says.

### 5. SPR could not source its own access claim

SPR told Council twice — Dec 2021 and Aug 2022 — that "among the top 12 park systems in the
country, TPL ranks Seattle in the top 5 in terms of access to dog parks per capita."

On 2022-07-21, thirteen days before the Council presentation, SPR's own policy staffer asked
the deck's author: *"Can you point me to the source of that info?"*

**No reply appears in this release.** The claim went to Council unchanged on Aug 3.

Given that SPR's access claims are the project's stated methodology target, this is the
single most quotable document in the release. It must be stated carefully: absence of a reply
in this production is **not** proof no reply was sent. The defensible framing is that the
claim was questioned internally and the release contains no sourcing for it — which is
exactly true, and is enough.

### 6. The City's own words on why people run dogs off leash

From the FAS Director's June 2022 report **to Council** (`00524`):

- "The lack of available Off Leash Areas could encourage pet owners to take their dogs off
  leash in regular City parks where other park users are affected."
- "Dog owners consistently share with SAS that OLAs aren't within walking distance and are
  overcrowded."
- "the limited number of OLAs could be a barrier to residents living in underserved
  communities, who may need access to public transportation to visit an OLA."
- "Achieving compliance … requires a holistic approach, involving enforcement, an increase in
  Off Leash Areas and more robust educational campaigns. No one approach alone achieves the
  goal."
- Seattle **1.9 OLAs per 100k** vs Portland 4.9, San Francisco 6.5 — *the City's own table*.

The site has been arguing the supply-gap-drives-non-compliance thesis from its own analysis.
The City's enforcement agency told Council the same thing in 2022. That changes the register
of the argument from "here is my inference" to "here is the City's finding, which it then
did not act on."

The 2024 Expansion Study reinforces it: SPR's stated rationale for the Ravenna site includes
that the park is "already experiencing unsanctioned off leash activity."

### 7. Enforcement is structurally broken, per FAS

Park users refuse to identify themselves; without ID no citation can issue; SPD response to
ACO assistance requests runs **60–120 minutes**; officers are "routinely verbally berated."
SAS's stated policy is a verbal warning on all first contacts.

This explains the citation numbers mechanically — 880 contacts, 42 citations — and it's the
City's own explanation, not a hostile inference.

### 8. Budget and capital findings

- **OLA capital backlog: $1,150,000–$2,220,000 (2016 dollars)** across 14 OLAs, itemized per
  site with priority rankings (`00168`). Against $103,000–$117,000/year of Park District OLA
  maintenance, that is an **11–22 year backlog at 2016 prices** — before inflation, and
  before the four OLAs added since.
- **Kinnear: $6,000–$11,000, ranked LOW.** Direct material for the Part II case study.
- **Park District OLA funding, precisely:** the 2017 final plan says "between $103,000 and
  $117,000 annually" (pp. 3, 5) and, at Cost of Services (p. 19), "$106,000 annually through
  2020" — both figures are in the final. The site's round "$100,000/year" is a floor and can be
  tightened.
- **$635,000 spent 2017–2021** on OLA major maintenance, ~$110,000 projected for 2022
  (`00681`, SPR to Council).
- **Draft-vs-final discrepancy:** the June 2016 draft's summary quotes $718,000–$1,363,000,
  contradicting its own Section 7 total. The Aug 2017 final drops it. Worth a methodology
  footnote if the capital figure is used.

### 9. Gap areas SPR itself names

Capitol Hill, Ballard, Northgate — SPR's own "future expansion options" slide (`00416`).
**East Queen Anne Playfield** is on SPR's recommended-future-sites list, pending "further
discussions with community … on field scheduling capacity."

---

## Proposed site changes

Ranked by value. **None applied.**

### P0 — one interpretation, wrong in five places

The site's "funded ≠ spent" move is **correct for 2025–26 and wrong for 2023–24**. The 2023
MOA billed a flat 240 hours per pay period for three FTE with no actual-hours qualifier;
actual-hours billing only began with the **2025** MOA. The ledger confirms SPR was invoiced
accordingly: **$453,056 (2023, annualized from H1) and $456,173 (FY2024)**.

Against a 2022 baseline of one officer at $152,399, that is a **2.97× / 2.99× increase** —
actual billed spend *did* approximately triple, in **2023**, not 2026.

This is one belief replicated across three pages. All five need the same period-scoping:

| # | File | Current text | Problem |
|---|---|---|---|
| 1 | `docs/enforcement.html` (Finding 01) | "the rise reflects falling output — **not money spent on officers who were never hired**" | Backwards for 2023–24. SPR *was* billed for three regardless of who was hired. Sharpest of the five. |
| 2 | `docs/updates.html` (June 2026 entry) | "the city's **actual spend has not tripled**" | Wrong. It tripled in 2023. The rest of the entry — "not a new budget expansion" — stands. |
| 3 | `docs/opinion.html` (~397) | "actual FAS-side spend has tracked roughly one officer (**about $176,000**), not the ceiling" | Understates 2023–24 by ~2.6×. |
| 4 | `docs/enforcement.html` (cost chart caption) | "How much of that extra actually reaches park patrols **isn't public**" | Half-answered: it was *billed* in full. What reached patrols is still unknown — keep that half. |
| 5 | `docs/enforcement.html` (Data Notes, ~317) | "What SPR was actually invoiced and paid … **is not stated in either MOA**" | Answered for 2023 H1 + FY2024 by the ledger. Narrow the open question to 2025–26. |

**The correction is period-scoping, not reversal.** "Funded ≠ deployed" remains true and
well-evidenced throughout. What changed is that a third category — *billed and paid* — tracked
**funded**, not **deployed**, for 2023–24. That is a stronger version of the site's argument,
not a retreat from it: the City paid for three officers it did not field.

**Twin check.** There is no `docs/print.html` (CLAUDE.md says otherwise; the repo wins —
`scripts/build-pdf.mjs` drives the PDF off a `PAGES` list of the real pages). So fixing the
three source pages fixes the PDF. Re-run the PDF build after the edits and confirm.

**Memory conflict.** The note `project_aco_moa_2026` records "'tripled' = funded only, not
actual spend (positions vacant)" as settled. That reading is now refuted for 2023–24 and
should be corrected in place rather than left to contradict the C266465 note.

### P0a — `opinion.html` states a spend figure the ledger contradicts

**This is a live factual error on the signed editorial and should be fixed before anything
else here.** `docs/opinion.html` (~line 397) currently reads:

> "…billing is on hours actually worked and only one of the three positions has been filled
> — so **actual FAS-side spend has tracked roughly one officer (about $176,000)**, not the
> ceiling."

Actual-hours billing began with the **2025** MOA. The **2023** MOA — which governed 2023 and
2024 — billed a flat 240 hours per pay period for three FTE with no actual-hours qualifier,
and the enforcement page already says so correctly. The ledger confirms it was billed that
way in practice: **$456,173 in FY2024**, ~$453,000 annualized for 2023.

So for 2023–2024 the sentence understates actual FAS-side spend by roughly 2.6×. The
vacancy-means-lower-spend inference is sound only from 2025 forward.

Suggested correction — this arguably *strengthens* the editorial's argument, since the money
was spent whether or not officers were in the truck:

> The Park District approved three officers in 2023, and SPR was billed for three from the
> start — $456,173 in 2024 alone, on invoices computed from a flat 40-hour week rather than
> from hours worked, while FAS was internally reporting it could field one and a half to two
> officers. Only the 2025 MOA switched to billing on actual hours.

### P0b — `enforcement.html` asks a question this release answers

The Data Notes (~line 317) say:

> "What SPR was actually invoiced and paid — especially in 2023–2025 while positions were
> vacant — is not stated in either MOA; the §7 monthly cost-calculation spreadsheets would
> show it (requested via PRR #9)."

Partly answered now. C266465 produced quarterly ledger backup covering 2023 H1 and all four
quarters of 2024 — not the §7 monthly spreadsheets, but the same underlying figures. The note
should record what's known (2023 H1 $226,528; FY2024 $456,173; calendar-derived) and narrow
the open question to 2025–2026, where actual-hours billing might genuinely have reduced the
bill.

**Both P0 items require the generated-page workflow** (edit `enforcement_page_data.json`
and/or `build_enforcement_page.py`, re-run, verify, confirm no-op second run). `opinion.html`
is hand-maintained and can be edited directly.

### P1 — Enforcement page: cost is now *actual*, not authorized

`docs/enforcement.html` is generated. This means editing
`scripts/enforcement_page_data.json` and/or `scripts/build_enforcement_page.py`, re-running
the builder, running `verify_enforcement_data.py`, and confirming a second builder run is a
no-op. Per the enforcement-build-chain note, a cost change touches **both** the page-data
JSON and `data/enforcement-year-metrics.csv`.

Substance: Finding 01 currently reasons about cost per citation against staffing "that
actually existed — roughly one officer throughout." That inference is now replaceable with a
documented fact: **$456,173 billed in FY2024 on flat calendar-derived invoices for three
officers, while FAS internally reported capacity for 1.5–2.0.** The funded-vs-deployed gap
stops being an estimate.

### P2 — Enforcement page: a new finding on the absent evaluation

A short section stating what the City does *not* have, sourced to this PRR's non-production.
The strength here is that it's an argument the City cannot rebut with a document, because the
request asked for the document and none came back. Pair with the Jainga memo's
recommendation-to-shrink.

### P3 — Part I / Part II: swap author inference for City statement

Anywhere the site argues that inadequate OLA supply drives off-leash use in regular parks,
add the FAS Director's June 2022 statement to Council. Same conclusion, primary source,
different register.

### P4 — Peer cities: add the City's own comparison table

`peer-cities.html` already frames this metric as "dog-parks-per-100,000 (TPL)" and quotes
**TPL's** counts from `data/peer-cities.csv` (Seattle 1.82, Portland 5.74, SF 5.03). The FAS
SLI table (`00524`) is an **independent second count** — SPR's own, using 14/32/53 OLAs
against 2021 populations: Seattle **1.9**, Portland **4.9**, SF **6.5**.

The interesting part is where the two agree and where they don't:

| | TPL (site today) | City's own (2022) |
|---|---|---|
| Seattle | 1.82 | 1.9 |
| Portland | 5.74 | 4.9 |
| San Francisco | 5.03 | 6.5 |

**Seattle's number is robust across both methods; the peers' are not.** So the right framing
isn't "here's a corroborating row" — it's that two independent counts, one of them the City's
own, put Seattle at ~1.8–1.9 per 100k while disagreeing by ±20–30% about the peers. That
makes Seattle's position the *stable* fact in the comparison, which is a stronger and more
honest use of the table than treating it as confirmation.

Keep the existing counting-convention caveat (`CLAUDE.md` §2): Portland's 32 includes unfenced
voice-control areas, and the City's table does not correct for it either.

### P5 — Budget page: the capital backlog

$1.15M–$2.22M identified need vs ~$110K/year funded. This is a clean, well-sourced chart and
the site does not currently have it.

### P6 — Part II / Kinnear: the LOW ranking

SPR's own 2016 capital list ranks Kinnear LOW at $6,000–$11,000 of identified need. Factual,
verifiable, and it belongs on the data page rather than the opinion page.

### P7 — Methodology / opinion: the unsourced TPL claim

Best used on `opinion.html`, where the register allows it, and stated exactly as the record
supports: the claim was made to Council twice, was questioned internally by SPR's own staff
thirteen days before the second presentation, and no sourcing for it appears in the release.

### P8 — MOA archive is now complete

2016 / 2021 / 2023 / **2025** / 2026. Done — already committed to the repo.

---

## Follow-on PRRs this justifies

1. **Q3/Q4 2023 and 2025–2026 ledger backup** — completes the actual-spend series and would
   show whether the 2025 shift to actual-hours billing reduced what was billed. New, and
   cheap to ask for now that we know the workbooks exist and what they're called.
2. **The monthly §5 summary reports** — already filed as PRR #9. This release confirms it is
   the only remaining route to location-level deployment data.
3. **C266744 (FAS-side) July-2025 truck-log installment** — already filed and narrowed; still
   pending. Nothing new needed.

**Note:** no new FAS/SAS request is required for items 3–4. **C266744 is already that request**,
and the two responses interlock usefully: FAS says its only responsive records are officer
truck logs and dispatch broadcast logs; SPR says it holds none of those. Both custodians have
now separately confirmed that no program-effectiveness evaluation exists. That's a stronger
claim than either response supports alone, and it's worth stating that way on the site.

---

## Things to be careful about

- **Don't merge the 42/28 counts into the citation dataset.** Different systems. Stated above
  and in the PRR README; worth repeating because it's the easiest mistake to make here.
- **The TPL non-reply is not proof of a non-response.** State what the release contains.
- **"AP's priority" is one staffer characterizing another's priorities in internal email.**
  Quote it; don't extrapolate.
- **The 2024 ledger workbook carries a stale "JAN 2023" sheet header.** The weekly dates are
  genuinely 2024 and leap-year correct, so the totals are sound, but anyone re-checking the
  spreadsheet will notice the header and should be told why.
- **Park District OLA maintenance ($103–117K/yr) and the ACO enforcement line (~$455K/yr) are
  different money.** Both are Park District, both touch dogs; they are not the same budget and
  the site should keep them visibly separate.
- **Three categories, not two.** The site currently reasons about *funded* vs *deployed*. The
  ledger adds *billed and paid*, which for 2023–2024 tracked funded, not deployed. Any
  sentence that collapses this back to two categories now reads as wrong. This is what the P0
  correction is really about.
- **There are two versions of the FAS SLI response.** The enforcement page cites a **Sept 30
  2022** version (via PRR C265341) and quotes language about sworn officers and compelling
  identification. The copy in *this* release is dated **June 30 2022**, signed by FAS Director
  Calvin W. Goings, and does **not** contain those phrases. Both appear legitimate — the June
  document matches the SLI's stated June 30 due date; the September one is presumably revised.
  **The site's existing citation is not wrong and should not be "corrected."** But the two
  should be distinguished where cited, and the June version carries material the September one
  may not (the OLA-per-100k peer table, the 344-of-489-parks patrol baseline, the
  OLA-scarcity-drives-non-compliance language).

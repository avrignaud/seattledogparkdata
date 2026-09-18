# PRR C264837 — findings and proposed site changes

**Status: APPLIED, 17 September 2026.** Andre reviewed the twelve recommendations below,
a verification pass corrected five of them (recorded in "What the verification pass changed"
at the foot of this file), and all twelve were then executed. This document is kept as the
reasoning record for the change, not as a to-do list. The site now matches it.

---

## The one-sentence version

The budget split the site has called unpublished since 2019 was answerable the whole time and
nobody had asked SPR directly: it books OLAs and P-Patches as two separate Master Projects and
produced four years of both on request, showing Seattle funded off-leash areas at roughly 2.6×
what this site reports, then spent under a fifth of it.

**The methodology lesson generalizes.** The unknowability was inferred from the published budget
books, which aggregate. "Not published" is not the same as "not tracked," and the site should
assume nothing else it has parked in that category is genuinely unanswerable.

---

## What's genuinely new

### 1. The question `CLAUDE.md` §3 calls unanswerable is answered

§3 currently reads: *"SPR doesn't publish the OLA-only split. If anyone asks for exact
OLA-only spending for 2023+, the honest answer is 'we don't know, SPR doesn't break it out.'"*

That is now wrong, and the correction is not subtle. Inside BC-PR-50000 there are two Master
Projects, budgeted and expensed separately:

| Master Project | Name |
|---|---|
| `MC-PR-51002` | Improve Dog Off Leash Areas |
| `MC-PR-51001` | Rejuvenate P-Patches |

SPR's answer on allocation methodology, verbatim: *"They are different Master Projects within
BC-PR-50000, and the budget and spending is split out as per the above."* No formula, because
nothing is being allocated. The distinction the site has been treating as a reporting
limitation was an artifact of reading published budget books rather than asking.

**The published books are not wrong, they are just aggregated.** The two Master Projects'
adopted budgets sum to the combined BSL figure already in `data/budget-detail.csv` to the
dollar in 2023, and to within rounding in 2025 and 2026. That is a strong corroboration of
the existing data, and it means there is no third bucket hiding inside the BSL.

### 2. The site's OLA-only figure is wrong by 2.6×, and was never sourced

`data/budget-detail.csv` carries `ola_only_k` of **126** (2023) and **129** (2024),
attributed to "Parkways blog / Seattle Times 2023-24 coverage." **No such source exists, as
far as I can establish.** Searched September 2026:

- Parkways, *Announcing the recommendations from the OLA Expansion Study* (Feb 2024) — no
  dollar figure for OLAs at all.
- Parkways, *Park District Governing Board passes 2023–2028 financial plan* (Sept 2022) — no
  OLA dollar figure, no P-Patch mention.
- Mayor Harrell's Park District Cycle 2 fact sheet (the PDF `part1-the-gap.html` links) — the
  only off-leash line is **$450K for seven-day off-leash and scoop-law enforcement**. There is
  no $3.46M OLA capital line in it either (see finding 5).

The primary record gives **$328,345 (2023)** and **$333,478 (2024)**. Because the two Master
Projects exhaust the BSL, $126,000 cannot be the OLA share of BC-PR-50000 — there is no
room for it to be.

One candidate origin, offered as a lead and not a finding: PRR C266465 established
**$635,000 of OLA major maintenance spend across 2017–2021**, which averages $127,000/year.
If someone read that as a current-year OLA budget, $126K/$129K would follow. Unconfirmed.

### 3. Which project is "larger" depends on the measure, and the three disagree

The site currently infers from the $126K figure that *"P-Patch is the larger share."* That
inference has to go, but it must not simply be flipped:

| Measure | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Adopted budget | OLA 57.6% | OLA 54.3% | OLA 85.7% | OLA 85.3% |
| Revised budget | P-Patch 60.5% | P-Patch 64.7% | OLA 69.9% | OLA 79.2% |
| Actually spent | OLA 66.3% | P-Patch 56.9% | OLA 59.0% | OLA 63.9% |

Any replacement sentence must name its measure. My recommendation is to use **adopted
budget** for budget claims (it is the appropriation, and it is what the existing combined
series already uses) and to introduce **expenses** as a separate, clearly-labelled series
rather than blending the two.

### 4. The strongest finding: the money arrived and the spending fell

| Year | Revised budget | Expenses | Burn |
|---|---:|---:|---:|
| 2023 | 416,256 | 315,049 | 75.7% |
| 2024 | 434,685 | 218,996 | 50.4% |
| 2025 | 1,784,507 | 368,398 | 20.6% |
| 2026 (to 7 Jul) | 2,990,479 | 150,593 | 5.0% |
| **2023–26** | **5,625,926** | **1,053,037** | **18.7%** |

Available balance: **$4,362,265**.

2025 is the inflection. The revised budget quadrupled and the burn rate fell by more than
half. 2026 carries the unspent balance forward: its revised budget ($2.99M) is nearly double
its adopted ($1.57M), which is what carryforward looks like.

This reframes the project's central budget claim. The current framing is *Seattle underfunds
OLAs.* The record supports something sharper and better sourced: **Seattle funded OLAs at
roughly 3× the Cycle 1 rate in Cycle 2 and has not spent it.** That is the same shape as the
enforcement finding already on the site (funded ≠ deployed), which makes it a coherent thesis
rather than a new direction.

**Two guardrails.** 2026 is year-to-date through 7 July and is not comparable to a closed
year. And P-Patch burned 32.0% across the closed years 2023–25 against OLA's 34.2%, so do
**not** claim OLA is uniquely badly executed; the distinctive facts are the absolute balance
and the direction of the OLA series.

### 5. The $3.1M capital is inside the BSL, so the site double-counts it

Verbatim: *"The $3.1M is included in the BC-PR-50000 above, within the MC-PR-51002 Improve
Dog Off Leash Areas Master project."* This is exactly why the OLA line jumps from ~$330K
(2023–24) to ~$1.57M (2025–26).

`data/budget-detail.csv` carries `one_time_capital_k` = 1730 in **2024 and 2025**, described
as capital "separate from" the BSL. Both the placement and the treatment are now wrong:

- **Wrong years.** 2024's OLA adopted budget was $333,478. There is no $1.73M of capital in
  2024. The capital ramp is 2025–26.
- **Wrong relationship.** It is not additive to the combined BSL. `docs/data-methods.html:198`
  renders *"$1,845,706 +$3.46M Cycle 2 capital"*, which reads as a sum and is a double-count.

`docs/budget.html:344-347` already excludes capital from the basis-point chart with a comment
explaining why (June 2026 audit). That call was right for a reason nobody had the record for
at the time; it can now be restated as fact instead of caution.

### 6. Only ~$600K of the capital has been spent, all of it on paper

Verbatim: *"roughly $600K has been spent towards planning and design for the West Seattle
Stadium OLA and Othello Playground OLA projects between January 1st 2023 and July 7th, 2026.
Construction at these two sites is currently estimated to begin in Early 2027."*

This corroborates `sources/spr-ola-project-status-2026.md` from an independent direction: the
project pages said construction slips to late 2026/early 2027, and the ledger shows no
construction money moving. The site can now say the schedule slip and the spending pattern
agree.

### 7. A $30,000 vintage difference, to be recorded and not reconciled

2024 adopted (this response) is $614,343; the repo's 2024 figure is $584,343, the **endorsed**
number from the 2023-Adopted/2024-Endorsed budget book (PRR C265589). The gap is exactly
$30,000. Both are correct for what they are. Keep both, label both, reconcile neither.

---

## Proposed site changes

Ordered by how wrong the current page is, not by effort.

### P0 — the $126K/$129K figure, on seven pages

This is one figure repeated across the site, so it is one decision applied in seven places,
not seven decisions. Current sites:

| File | What it says |
|---|---|
| `docs/index.html:137` | "SPR has disclosed $126,000 (2023) and $129,000 (2024)" |
| `docs/part1-the-gap.html:140` | "confirmed OLA-only figures of $126,000 (2023) and $129,000 (2024) but nothing for 2025–26" |
| `docs/budget.html:56` | deck: "went from $100,000 to $129,000 through 2024, after which SPR no longer breaks the OLA share out" |
| `docs/budget.html:77` | stat tile: `$129K` |
| `docs/budget.html:103` | "disclosed OLA-only markers sit at $100,000 … and $126,000–$129,000" |
| `docs/budget.html:134,141` | license-revenue contrast: "ten times the ~$100,000–129,000" |
| `docs/budget.html:178` | Cycle 1 vs Cycle 2: "roughly $129,000/year OLA-only operating" |
| `docs/peer-cities.html:417` | Minneapolis permit comparison: "$100,000–$129,000 a year" |
| `docs/data-methods.html:311,312,325,326` | methodology table rows and the OLA-only line note |
| `docs/updates.html:98` | July 2026 entry — **historical, do not edit** |

Two of these change meaning, not just digits:

- **`budget.html:141`** — dog licence revenue is "about **ten times**" OLA spending. Against
  $328,345 the multiple is **3.8×**. The sentence survives; the number does not.
- **`peer-cities.html:417`** — a hypothetical $7M Minneapolis permit yield is called "a full
  order of magnitude above" Seattle's OLA line. Against $328K it is ~21×, which is still
  more than an order of magnitude, so this one holds. Verify rather than assume.

**Recommendation:** replace with the adopted-budget series ($328,345 / $333,478 / $1,568,818 /
$1,574,370), re-cite to PRR C264837, and delete every clause saying the split is not
published. Keep $100,000 for Cycle 1 — it is a different source and still stands.

### P0a — `data-methods.html:326` states an inference the record refutes

> "the 2023 and 2024 disclosed OLA-only portions ($126,000, $129,000) are roughly 22% of the
> combined BSL, suggesting P-Patch is the larger share."

Both halves fail. Replace with the measure table from finding 3, or with a single sentence
that names its measure.

**This one has a live guard.** `scripts/verify_site_data.py:221-226` computes the 22% share
from hardcoded `126`/`129` and greps the page for the string `"22%"`. Changing the prose
without the guard fails the verifier; changing the guard without the prose leaves a false
claim up. They move together.

### P0b — the capital double-count

`docs/data-methods.html:198` renders "$1,845,706 +$3.46M Cycle 2 capital". Drop the addend
and state that the capital is inside the BSL line. Then decide what `one_time_capital_k`
means (see the data-model note below) before touching any chart that reads it.

### P1 — `$3.46M` is cited to a document that does not contain it

`docs/part1-the-gap.html:140` links the Mayor's Park District Cycle 2 fact sheet for the
$3.46M capital figure. That PDF has no such line; its only off-leash entry is $450K for
enforcement. SPR's own project pages give **$3,103,000** for the two OLAs, which the site
already cites elsewhere (`budget.html:180`, `data-methods.html:211`).

To be precise about the claim: this is a **mis-citation**, not evidence that $3.46M is
invented. The figure may well come from the six-year Cycle 2 financial plan rather than this
two-page fact sheet; I checked the fact sheet's full extractable text and it is not there.

This is independent of the new PRR — a pre-existing bad citation that the fact-check for this
ingest turned up. Either find the document that does carry $3.46M, or fall back to the
$3,103,000 SPR's own project pages give and describe the Ravenna design increment separately.

### P2 — new Budget finding: appropriated vs spent

The burn table in finding 4 is the best new chart material in this release: two series
(revised budget, expenses) over 2023–26, with 2026 marked partial. It belongs on
`docs/budget.html` as a finding in its own right, and it is the piece that turns this from a
correction into a story.

### P3 — Cycle 1 vs Cycle 2 can now be spend-to-spend

`budget.html:177` compares Cycle 1's $100,000/year *stated budget* to Cycle 2's *budget*.
With PRR C266465's $635,000 of OLA major maintenance across 2017–2021 (~$127,000/year actual)
and this release's expenses column, the comparison can run actual-to-actual. Flag the scope
difference: "major maintenance" is not necessarily the whole Master Project.

### P4 — `CLAUDE.md` §3 and `AGENTS.md`

§3's "the honest answer is 'we don't know, SPR doesn't break it out'" must be rewritten, and
the TODO item it points at is closed. Whoever applies P0 should do this in the same pass or
the next session will re-derive the old claim from the instructions file.

### P5 — updates log

By the logged-worthy list this qualifies twice: a PRR response ingested, and a material data
correction that changes a headline figure. It needs an entry and a date bump. Your call.

---

## Data-model decisions to make before applying any of this

**Who owns "the OLA-only number."** `data/ola-ppatch-master-projects.csv` is the primary
record. `budget-detail.csv:ola_only_k` is secondary reporting with no findable source. They
must not both stand as owners. Options: retire `ola_only_k` and have charts read the new
file; or keep it as a declared **cache** of the new file's `adopted_budget_usd` with the
refresh path named. I recommend the first, but it touches chart code, so it is a decision
rather than a cleanup.

I have left `ola_only_k` numerically untouched and written the supersession note into its
`provenance` cells, so the site and its verifier remain self-consistent until you choose.

**`seattle-timeseries.csv:ola_improvement_budget_k` is the same problem with a worse name.**
It holds 100 for 2016–2018 (genuinely OLA-only) and the *combined* OLA+P-Patch figure from 2019
on (160.8 … 1829.7, 1845.7). The column name is now literally the name of `MC-PR-51002`
("Improve Dog Off Leash Areas"), so it reads as OLA-only for every year and is not. This
predates the PRR; the new file makes it visible. Rename it, split it into two columns, or point
it at the new file — but it needs the same ownership ruling as `ola_only_k`, and it must not be
left as the second name for a thing that now has a primary record.

**What `one_time_capital_k` means.** The name says "one-time capital, separate from the BSL."
The record says it is not separate. Either rename it to reflect that it is a memo figure
carved out of the BSL, or drop it and derive the capital story from the Master Project series.

**The new file is not in `sync-data.sh`.** No chart fetches it yet, so it stays out of
`docs/data/`. Add it to the allowlist in the same change that adds a chart reading it.

---

## Things to be careful about

- **2026 is a partial year.** Every 2026 cell is YTD through 7 July 2026. A 5% burn is not a
  finding on its own.
- **Adopted, revised and spent are three different questions.** The site's existing combined
  series is adopted/endorsed. Do not silently mix in revised or actuals.
- **Do not flip "P-Patch is larger" to "OLA is larger" without naming the measure.** On
  revised budget in 2023–24, P-Patch genuinely is larger.
- **Do not claim OLA execution is worse than P-Patch.** Closed-year burn is 34.2% vs 32.0%.
- **The $30,000 is adopted-vs-endorsed, not an error.** Do not average them or pick one.
- **`updates.html` entries are historical.** The July 2026 entry's "$100,000–129,000" was
  accurate to what the site knew then. Leave it.


---

## What the verification pass changed

An adversarial re-derivation before execution reproduced every arithmetic claim above and
refuted five statements about scope. Recorded here because the corrected versions are what
was actually built.

1. **"Ten sites across six files" was wrong.** The real blast radius was 18 occurrences on
   12 lines across 5 live files, plus `updates.html`, which is historical and was left alone.
2. **"Keep $100,000 for Cycle 1, still good" was wrong** and was reversed. Correcting Cycle 2
   to the primary record while leaving Cycle 1 on a round secondary figure reproduces the
   defect the correction exists to remove. Cycle 1 is now $106,000, the Cost-of-Services
   figure at p. 19 of the 2017 plan, with the $103,000-$117,000 range stated in the notes.
3. **`ola_only_k` drives two charts, not one** — `budget.html` and `part1-the-gap.html:632`.
4. **`one_time_capital_k` was a rendered chart series**, not just a column. Dropping it
   removed a visible series, which is why the Finding 01 subtitle and takeaway were rewritten
   rather than just edited.
5. **Item 9 gated nothing.** `seattle-timeseries.csv:ola_improvement_budget_k` has no
   consumer anywhere in the repo. It was still split, but as hygiene, not as a prerequisite.

One thing the audit missed entirely: **2025 and 2026 flip from "not disclosed" to disclosed**
in the `data-methods.html` methodology table, which is the more interesting half of the
change, because those are the capital years. 2019-2022 stay genuinely unavailable.

### One deliberate departure from the approved plan

Item 7 was approved as "retire `ola_only_k`, have charts read the new file." That is not
quite what was built, because Cycle 1 has no Master Project record: `ola-ppatch-master-projects.csv`
starts in 2023, and a pure retirement would either leave the 2016-2018 points homeless or
force a fabricated row into a primary-source file. Instead `ola_only_k` survives as a
**declared cache** with its refresh path written at the column: 2023+ copied from the Master
Project file, 2016-2018 from the 2017 plan, 2019-2022 blank because no record exists. The
Named-Data Principle permits a cache that declares itself; it forbids an undeclared second
owner. `one_time_capital_k` was retired outright, as approved.

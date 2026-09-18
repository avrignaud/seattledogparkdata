# Site audit — September 2026

**Status: report for discussion. No site page was changed.** Two audits in one: (1) every
factual claim on the nine public pages checked against the repo's own data and the July 2026
records release (PRR C266465), and (2) a structural read of the site with an eye to
simplifying it. Method: five parallel claim-by-claim page auditors plus a cross-page pass
for the things a single page can't see; every finding below that changes a headline was
recomputed a second time by hand before it went in.

**One repo change was made:** three lines in `data/prr-responses/C266465/README.md`,
`C266465-PRR-AUDIT.md`, and `sources/SOURCES.md` wrongly said the 2017 plan dropped the
"$106,000 annually" figure. It didn't (p. 19). Corrected, marked as corrected.

---

## The verdict in four sentences

The arithmetic is sound: nearly 390 quantitative claims were recomputed from the CSVs and
matched. The site's **two headline claims are wrong**: "zero net OLAs since 2009, seventeen
years" is contradicted by SPR's own 2017 plan (last additions 2012–2013), and "two new OLAs
open fall 2026" is contradicted by SPR's March 2026 statement that construction starts in
2027. A **third systemic error** — that the City hasn't actually spent the three-officer money
— appears in eight sentences across four pages and is refuted by the July ledger data. And
the word "citations" is doing work it can't bear: **45% of the 7,015 "citations" are $0
verbal warnings**, and in the post-2019 data only 7% are actual citations.

The site is also long. Twenty-nine thousand words, about 109 minutes of visible reading, with
the opinion page alone at 6,150 words. The July audit's cut-list was never applied.

---

## Part 1 — Accuracy

### Tier A: headline claims that are wrong (fix first)

**A1. "Zero net off-leash areas since 2009 / seventeen years."**
Stated on index (×2), Part I hero and Finding 01, Part II Finding 07, opinion P1, README,
CHANGELOG. SPR's own *People, Dogs & Parks Plan* (Aug 2017, committed at `sources/`) says:
eight original sites, then six added — I-5 Colonnade 2005, Plymouth Pillars 2005, Regrade
2005, **Denny 2012, Magnolia Manor 2012, Kinnear 2013** — and that the 2011 study covered
"the 11 off-leash areas in existence at the time." `kinnear-timeline.csv` corroborates
(2007: "approved as 12th OLA").

Correct: **zero net since 2013, thirteen years.** The 2010 baseline is 11 OLAs, not 14, so
Part I Finding 01's residents-per-OLA "+34% since 2010" becomes roughly **+5%**. The "when
Seattle's 14 OLAs opened" chart is wrong on most bars.

Root cause is the data model: `seattle-olas.csv` `year_opened` disagrees with SPR's plan on
**11 of 12** matchable sites (Kinnear 1997 vs 2013; Denny 2000 vs 2012; Blue Dog Pond 2009 vs
1999; Genesee 2005 vs 1999; Golden Gardens 2003 vs 1996 …). Its provenance is unarchived "SPR
individual OLA pages"; the plan is a committed primary source. Owner ruling needed on which
wins, but the plan should. Note the plan itself distinguishes *opened* from *made permanent*
(Kinnear 2014, Magnolia Manor 2015); the site should say which it means.

**A2. "Two new OLAs open fall 2026."**
Stated eight times on index, Part I (×4), Part II, opinion; baked into `planned-olas.csv`
("Under construction, Fall 2026"), `park-coordinates.csv`, `seattle-timeseries.csv` (the 2026
row counts **16** OLAs, which drives the residents-per-OLA chart), and README.

Seattle Parks to the West Seattle Blog, **March 24 2026**: "Construction is now expected to
start in early 2027 and be complete by Fall 2027 … expect to go to bid in December of this
year." Neither site is under construction; both are at ~60% design. Othello's page blocked
direct fetch; the search summary of it says Fall 2027 as well — **verify directly**.

Correct: "two new OLAs funded, now expected Fall 2027." The 2026 time-series row should say
14, and the "first net increase in 17 years" line goes away with A1.

**A3. "The City hasn't actually spent the three-officer money."** (Eight sentences.)
The 2023 MOA billed a flat 240 hours/pay period for three FTE with no actual-hours qualifier;
actual-hours billing began only with the 2025 MOA. Ledger backup (C266465) shows SPR billed
**$456,173 in FY2024** and $226,528 in H1 2023 — 2.99× the 2022 one-officer baseline, and
*above* the $454,652 "ceiling" the enforcement page says "has never been fully spent."

| # | File | Sentence | Problem |
|---|---|---|---|
| 1 | `enforcement.html:92` (builder :110) | "That ceiling has never been fully spent … bills labor on hours actually worked" | FY2024 billing exceeded it. Sharpest of the eight. |
| 2 | `enforcement.html:153` (builder :171) | "not money spent on officers who were never hired" | Backwards for 2023–24 |
| 3 | `enforcement.html:191` (builder :209) | "not money the city has spent"; "isn't public" | Billed in full; what reached patrols is still unknown |
| 4 | `enforcement.html:191` | "the added officers largely don't exist yet" | FAS reported 2.0 parks FTE in 2022 and "closer to 2" in Feb 2025 |
| 5 | `enforcement.html:317` (builder :335) | "What SPR was actually invoiced … is not stated" | Known for 2023 H1 + FY2024 |
| 6 | `updates.html:66` | "the city's actual spend has not tripled" | It tripled in 2023 |
| 7 | `opinion.html:397` | "spend has tracked roughly one officer (about $176,000)" | Understates 2023–24 by ~2.6× |
| 8 | `budget.html:140` | "actual spend has tracked roughly one officer" | Same belief, no dollar figure |

The correction is period-scoping, not reversal. Funded ≠ deployed remains true and is the
stronger story: the City paid for three officers it did not field, on invoices computed from
a calendar. `verify_site_data.py` guards the retired phrase "about one officer" but the live
pages say "roughly one officer," so the guard never fires.

**A4. "7,015 citations."**
`case_result` in the citation dataset: **3,151 Citation / 3,191 Verbal / 648 blank / 25
voided-dismissed.** Nowhere on the site is this stated; every "citations issued" reads as
tickets. It matters most after 2019, where only 7% of records in the FAS dataset are actual citations:

| Year | Records ("citations" on site) | Actual citations | Verbal | Site cost/citation | Cost per actual citation |
|---|---|---|---|---|---|
| 2018 | 1,276 | 441 | 835 | $229 | $663 |
| 2022 | 169 | 18 | 130 | $1,730 | $16,244 |
| 2024 | 447 | **21** | 350 | $654 | $13,924 |
| 2025 | 267 | 23 | 230 | $1,095 | $12,713 |

Real citations fell **95%** from 2018 to 2024, not 65%. This also means the SAS internal
tracking from C266465 (2024: 28 citations, 586 verbal) reconciles with the dataset *far*
better than my July audit doc says (21 citations, 350 verbal + 73 blank). The "do not merge"
caveat stands, but "does not reconcile" should be softened to "different systems, same
shape." I'll correct that in `C266465-PRR-AUDIT.md` if you agree.

Two honest options: rename the metric to "enforcement contacts" site-wide, or split every
chart into citations vs. warnings. The second is more work and much more informative — the
warning-only era is the finding.

### Tier B: data-model defects behind the errors

- **B1** `seattle-olas.csv` `year_opened` — see A1. Eleven wrong rows.
- **B2** `seattle-timeseries.csv` 2026 row: 16 OLAs, "open fall 2026." Should be 14.
- **B3** `planned-olas.csv` status "Under construction" for both; should be "In design" with
  the 2027 dates and a dated source.
- **B4** `build_enforcement_metrics.py` `FMW_ANNUAL = 140000` × 1.0 FTE through 2026. SPR's
  Sept 2024 memo: "There is no current FMW working with the Animal Control Officers" — vacant
  since 2023, never backfilled. The model carries ~$560K of phantom cost across 2023–26 while
  omitting ~$300K/yr of real ACO billing. The page itself concedes $73K is the better FMW
  figure and doesn't use it.
- **B5** `illegal-use-indicators.csv` still carries the retired "~1,100 complaints, 2024" row
  (real Apr–Dec 2024 count: 853) and an unsourced "435 tickets Mar–Aug 2016" (repo's own data:
  **543**).
- **B6** Fee revenue: "$351,099" includes $56,214 from non-DLP violations while every
  denominator is DLP-only. DLP-only fees = $294,885.
- **B7** `licensing-revenue.csv` 2025 = $866,430, down 26%, no partial-year flag. Will bite the
  "$1.24M/yr" figure on budget.html when 2025 enters the average.
- **B8** `seattle-timeseries.csv` 2025 notes still say "+$3.1M one-time capital" (retired
  figure; CSV sums to $3.46M).

### Tier C: sentence-level contradictions (one location each)

| Page | Claim | Reality |
|---|---|---|
| Part II 02d | "Two largest deficits are South Lake Union and Queen Anne" (also Finding 07) | By the page's own fair-share formula they rank 13th and 11th. Top deficits: 98103 Wallingford, 98122 Capitol Hill, 98107 Ballard, 98116 Alki, 98105 U District. Prose was written about dogs-per-acre; chart plots acre shortfall. |
| Part II Kinnear | "Seattle's smallest at 0.124 acres" | Denny is 0.105. Same page says so in Finding 03. |
| Part II Kinnear | "only OLA within a 10-minute walk of most of Queen Anne" | Kinnear's isochrone covers the lower SW slope only; most of Queen Anne is outside every walkshed. Say "closest," not "within." |
| Part II amenities | "2 of 14 lighting (Westcrest, Denny); 9 of 14 water" | The cited in-repo source says 3 lighting (Plymouth, Regrade, Golden Gardens) and **1** water (Magnuson); FAS told Council in 2022 "only one OLA provides water access." |
| Opinion C2, C4; Budget | "SPR's 2015 survey found ~25% of residents use OLAs" | Plan: ~25% of residents **own a dog** (150K/662K, an estimate); 25% of *dog-owner respondents* visit monthly; general-population OLA use = 11%. Three-way conflation carried since the 2019 thread. |
| Opinion P3 | "OLAs get 0.06% of … the city's land" | Anchor has no land figure; site's own parkland share is 0.46%. |
| Enforcement 03 | "West Queen Anne Playfield is the only top-10 pre-COVID park whose volume did not fall" | WQA ranks 15th pre-COVID (80). Alki also didn't fall. |
| Index, Budget | "about half the apparent jump is a 2019 reporting shift" | 2019 step is $79.7M of a $338.9M jump = **24%**. Budget's data note scopes "half" to 2018→19 only; index generalizes it. |
| Index | "3,089 of 4,299 park-named citations" | 4,299 is park-named rows *at the 37 geocoded parks*; all park-named = 6,225. Also: 71.9% (index) vs 73% (Part II) are two passes of the same analysis, and the "full analysis on the Enforcement page" isn't there. |
| Part III Genesee | "Opened 2005" | Plan: 1999. |
| Part III 03c | SCL/WSDOT/Port "not historically partnered with on this use" | Two City Light sites were considered in the 1996–97 pilot; Colonnade is on WSDOT land; Magnolia Manor is SPU land. |
| Peer-cities | "3.2× … using each city's own published count" (caption) | Paragraph above says TPL. Own counts give 2.65×. |
| Peer-cities | "$100,000–130,000 … Cycle 1 window" | $126K/$129K are Cycle 2. |
| Peer-cities | "Seattle counts only fully-fenced" (×3) | CSV: 12 fenced, Magnuson and Colonnade partial. |
| Peer-cities Boise | "~1.6× per capita" | 1.70 on consistent denominators. |
| Updates | "2023 Park District budget book" | It's the City's 2023 Adopted / 2024 Endorsed budget book. |
| Index | "SPR PRRs C049204 + C263949" | C263949 was answered by FAS, not SPR. |
| Part III footer | "June 2026" under a July masthead | — |
| Budget | Findings numbered 01–05, then 08 | — |

### Tier D: unsourced, stale, or over-precise (act on selectively)

- **Rounding drift on hub figures:** licensed dogs 26,650 / 26,652 / 26,700; dog population
  248,858 / 248,900; complaints 3,000 / 3,010. Pick one form each.
- **Licensing compliance:** site says 7–18% from the Open Data snapshot; the C264029 README
  says 10–27% from modeled active licenses; updates.html attributes the snapshot figure to
  the PRR. Two ranges, two methods, mislabeled once.
- **Peer-cities:** roughly two-thirds of the page (NYC hours, Minneapolis fees, SF bonds, DC
  statute, Vancouver capital, Portland levy) rests on external URLs, none archived in
  `sources/`. Three with active recency risk: Portland's 2020 five-year levy (expired 2025;
  renewal on the Nov 2025 ballot — *memory, unverified*); Vancouver's elected Park Board
  (council voted to seek abolition Dec 2023 — *memory, unverified*); "SF has no mandatory dog
  license" (*I believe wrong — SF requires licensing at four months; memory, unverified*).
- **Part III:** ~10 narrative assertions with no repo backing (MOLG "raised compliance," "most
  Magnuson citations are off-OLA" — the data can't locate citations inside vs outside the
  fence, "only OLA with lake access," "seven months of closure," COLA "since 1996" — plan
  says the umbrella agreement was 1998). The page footer promises "every other claim links to
  its source." It doesn't.
- **Budget CIP comparators** ($1.8M Gas Works, $2.0M restrooms, $2.7M Green Lake) and
  Minneapolis $66 non-resident permit — no row or source entry anywhere.
- **Over-precision:** "86,207 of 737,559 residents" states a modeled estimate to five
  figures; METHODOLOGY calls it modeled and notes the alpha-shape step alone moves it ~1 pt.
  "r = 0.13" includes two months with no citation data because the PRR ends 2026-04-17
  (excluding them: 0.08). "Complaints tripled 2024→2025" compares a 9-month year to a full one.
- **Stale statuses:** enforcement "PRR #8, filed; SPR responding" (answered July); "as of April
  2026 … one of three filled" is five months old on a July masthead in September; nothing
  from C266465 is logged on updates or the index panel.
- **Docs stale:** AGENTS.md (lists 2 MOAs, 6 PRRs, `print.html`, "6 public pages"); CLAUDE.md
  says `print.html` exists (it doesn't; the PDF builds from a `PAGES` list) and the editorial
  is signed April (it's June); DATA-AUDIT "outstanding" still lists the answered complaints PRR.

### What the July release lets the site say from a primary source

Fully worked in `C266465-PRR-AUDIT.md`. The short list, in order of value:

1. **No effectiveness evaluation exists** — now confirmed by *both* custodians (C266465 SPR,
   C266744 FAS). Stronger than either alone.
2. **Billed spend tripled in 2023**, on calendar-derived invoices, while FAS said it could
   staff 1.5–2.0. The funded/billed/deployed distinction is the enforcement page's real story.
3. **The City told Council in 2022** that OLA scarcity drives off-leash use in regular parks,
   and gave its own peer table (Seattle 1.9 / Portland 4.9 / SF 6.5 per 100k). Seattle's
   number is stable across TPL and the City's count; the peers' aren't.
4. **The decision record:** staff recommended cutting the program (Sep 2024); leadership sent
   it back to three "given AP's priority" (Feb 2025); FAS said 1.5–2.0 (two days later).
5. **Contact denominator:** 2023–24, 1,540 ACO contacts → 70 citations, 4 written warnings,
   0 park exclusions. Answers "the product is education."
6. **SPR's unsourced "top 5 in dog-park access (TPL)" claim to Council**, questioned
   internally 13 days before, no sourcing in the record.
7. **OLA capital backlog** $1.15M–$2.22M (2016$) vs $103–117K/yr; Kinnear ranked LOW at
   $6–11K; SPR names Capitol Hill / Ballard / Northgate as gaps and East Queen Anne
   Playfield as a future site.

---

## Part 2 — Simplification

### The numbers

| Page | Words | Visible | Read-min | Sections | Charts+maps | Callouts | Numbers/100 words |
|---|---|---|---|---|---|---|---|
| index | 1,700 | 1,700 | 7 | 4 | 0 | 2 | 6.6 |
| Part I | 2,930 | 2,300 | 10 | 10+3 | 9 | 10 | **13.2** |
| Part II | 4,460 | 3,820 | 16 | 9+10 | 8 | 8 | 8.0 |
| Part III | 2,050 | 2,050 | 9 | 4+11 | 0 | 4 | 4.3 |
| Enforcement | 4,700 | 3,490 | 15 | 4+11 | 10 | 15 | 9.1 |
| Budget | 2,430 | 1,950 | 8 | 7+1 | 5 | 6 | 11.9 |
| Peer cities | 3,390 | 3,310 | 14 | 9+18 | 0 | 2 | 5.6 |
| Opinion | 6,150 | 6,150 | **26** | 8+25 | 0 | 1 | 3.0 |
| Updates | 1,390 | 1,390 | 6 | 7 | 0 | 7 | 7.5 |
| **Total** | **29,200** | **26,150** | **109** | | 32 | 55 | |

Sentence length averages 17–27 words; the enforcement page has 19% of sentences over 35
words, updates 29%. Part I carries 13 numbers per 100 words — a number every eight words.

### What's structurally wrong

**1. The site has four layers and the reader meets them in the wrong order.**
The index "in short" block is a good 300-word summary. Then each page opens with a hero, then
7–10 numbered findings, then Data Notes. The findings layer is where the length lives, and
it mixes load-bearing with supporting. Every page auditor independently sorted its page's
sections and came back with the same ratio: about **40% supporting material** that could
collapse or move.

**2. The same point is made on several pages.**
Playgrounds-vs-OLAs (Part I 06 and Budget 04). SPR budget vs OLA budget (Part I 04/05 and the
whole Budget page). Peer-city per-capita (Part I 02, Part II 04, Peer Cities, Opinion P1).
Walkshed × citations (index, Part II 02, Enforcement 03, with three different percentages).
Dog population triangulation (index, Part I, Part II, Opinion, Updates — with two roundings).
The July audit listed the first three as cuts; none were made.

**3. Labels have become a taxonomy.**
Finding 01–07, 02b, 02d, 03a–c, 08; Peer 01–08; P1–P6, O1–O3, C1–C7; "New" tags. Forty
labelled units. They read as a filing system, not a story. A reader can't tell which of
Finding 02b and Finding 03 matters more.

**4. The opinion page is a 26-minute essay with the recommendation on page 20.**
Six principles, three opinions, seven counterarguments, an access-standard section, an NYC
section, a seven-point recommendation, a Council ask, six acknowledgment blocks. The
auditor's read: the argument is carried by the broader-argument frame → P1/P2/P4 → O1–O3 →
C3/C7 → Part Four → recommendation → Council ask. That's about 3,500 words. The rest is
elaboration, restatement (P6 restates P4; C5 restates P2), or credit.

**5. Numbers substitute for sentences.**
Part I Finding 01's observation paragraph has ~24 figures. Enforcement Finding 01 has two
such paragraphs. The July audit flagged this ("~3 figures per paragraph"); unchanged.

### Recommended shape (for discussion, not a plan)

- **Fix the reading order.** Each page: hero → *one* paragraph stating the finding → the two
  or three charts that prove it → everything else collapsed. Target visible prose ~1,500
  words per data page, ~2,500 for opinion. That halves the site without removing a chart.
- **One home per point.** Playgrounds-vs-OLAs → Budget only. Budget preview → one teaser
  sentence on Part I. Peer per-capita → Peer Cities only, with one number quoted elsewhere.
  Walkshed × citations → Enforcement only, one percentage (pick 71.9% or 73.4% and say which).
- **Retire the taxonomy.** Headings that say what the finding *is* ("Half of Seattle's OLAs
  are under an acre") instead of "Finding 03." Keep anchors for inbound links.
- **Opinion: cut to the spine.** Keep the frame, P1/P2/P4, O1–O3, C3/C7, the access-standard
  section, the recommendation, the Council ask. Fold P5/P6 into P4, C1/C2/C4/C5/C6 into a
  single "objections" paragraph, acknowledgments to a short list. Move the NYC evidence to
  Part III where it already partly lives.
- **Peer Cities: decide what it's for.** Eight cards × three sub-sections is the longest
  page after opinion, and it's the least sourced. Either archive the sources or cut each city
  to the one design choice Seattle hasn't tried, which is what the index says the page does.
- **Numbers: one per sentence.** Move the rest to Data Notes or the CSV.

### Sequence I'd suggest

1. **Tier A + B together** (they're the same fixes) — chronology, 2027 dates, the eight spend
   sentences, citations-vs-warnings. These change headlines, so this is a logged update and a
   date bump. The enforcement changes go through the builder and both verifiers.
2. **Tier C** in the same pass, since the pages are open anyway.
3. **Then simplify**, page by page, opinion first (biggest, most personal, needs your voice).
   Doing simplification before the accuracy fixes would mean rewriting wrong sentences twice.
4. Tier D and the doc hygiene whenever.

---

## Could not verify

- Othello schedule directly (page 403 / cert error); Fall 2027 is from a search summary.
- `seattle-olas.csv` `year_opened` provenance — SPR's individual park pages returned
  navigation only; the CSV-vs-plan conflict is settled inside the repo, not outside it.
- Whether 2 or 3 officers were actually on parks in 2023–24 (record shows ~2 in 2022 and Feb
  2025, 1 in Apr 2026).
- 2025–26 ACO billing (ledger not produced; SPR noticed no charge had posted in Sept 2025).
- All external-only peer-city facts (list above); NYC operational detail; AVMA inputs; QACC
  officers; Andrew Lewis's term; the softball quote.

## Method notes

Five page auditors ran in parallel with instructions to recompute from CSVs and open the
primary documents; their findings are in this session's task outputs. Every Tier A/B item
and the three sharpest Tier C items were recomputed by me before inclusion. Web lookups: two
searches and four fetches on the OLA opening dates (research-adapter budget); no other
external sources consulted. Scratch text extracts live in the session scratchpad and are not
in the repo.

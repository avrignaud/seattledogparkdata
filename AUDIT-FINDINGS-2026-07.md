# Full-site audit findings — July 2026

Run against `SITE-AUDIT-PROMPT.md` (v2, three-track: accuracy & reproducibility ·
consistency · readability & defensibility). The June 28 pass is preserved in
`AUDIT-FINDINGS.md`; this file is the July record. Method: nine per-page readers +
14 dimension auditors (multi-agent), deterministic re-verification of every
mechanical finding against the committed CSVs, live external-source fetches, a
three-persona hostile-reader red team, and a second discovery round on the fixed
site. Every mechanical fix below was confirmed against primary data before applying.

**Headline:** `part1-the-gap.html`'s methodology time-series table was still
carrying three **retired pre-C265589 budget figures** (2021 $346,680 · 2023
$475,142 · 2024 $614,343) — two of them on the audit's own "must-not-survive"
list — while every other page used the corrected values. Neither verifier caught
it, because their presence-based prose checks can't detect a *contradictory*
number living elsewhere on a page. That blind spot is now closed (see §Reproducibility).

At completion: both verifiers print `ALL CHECKS PASSED`, the enforcement builder
is idempotent, and `docs/data` mirrors `data/`. The second discovery round's
regression pass confirmed the applied edits introduced no new inconsistency; its
fresh-eyes pass surfaced one further self-consistency defect — the 2016-survey
"39%" figure, described as **"weekly-to-monthly"** in the committed data file
(`illegal-use-indicators.csv`) and on the enforcement page, but as **"monthly or
more"** on Part II (4 places) and Opinion. **RESOLVED (July 4):** the owner supplied
the plan, now committed at `sources/people-dogs-and-parks-plan-august-2017.pdf`;
p.17 confirms "weekly to monthly" verbatim, so the alignment was correct and the
merge gate is lifted. Reading the plan added two more verified corrections — the
survey was **2015** (not 2016), and the "38% trails" stat was actually large parks
(trails is 36%) — and, per the owner, the three settings are now **blended to
~38%** (see §1, §7 #2).

---

## 1. Fixes applied

Every clarity rewrite is shown verbatim for voice-check. Categories: **M** = mechanical
(wrong number / stale figure / format), **C** = clarity (gloss / denominator / plain-language).
Site-wide dates, the masthead (JUNE 2026), `CHANGELOG.md`, and `updates.html` entries were
**not** bumped, per the settled owner decision.

### Accuracy / stale-figure corrections (M)

| File:line | Before → After | Source of truth |
|---|---|---|
| part1-the-gap.html:288 | `$346,680` → `$322,912` (2021 combined BSL) | budget-detail.csv (C265589; retired 2021-proposed) |
| part1-the-gap.html:289 | `$475,142` → `$569,561` (2023 combined BSL) | budget-detail.csv (adopted; on retired list) |
| part1-the-gap.html:290 | `$614,343` → `$584,343` (2024 combined BSL) | budget-detail.csv (endorsed; on retired list) |
| part1-the-gap.html:194 | `$3.1M for two new OLA construction projects` → `$3.46M in capital for two new OLAs plus design of a third` | budget-detail.csv (no $3.1M breakout exists; $3.46M canonical) |
| part1-the-gap.html:292 | table `+$3.1M capital` → `+$3.46M Cycle 2 capital` | same |
| part3.html:253 | `248 citations logged at Magnuson 2014–2019` → `367 … 2014–2026` | raw recompute (see below) |
| part3.html:267 | `130 citations logged there 2014–2019` → `152 … 2014–2026` | raw recompute |
| part3.html:281 | `Westcrest's 86 … citations 2014–2019` → `122 … 2014–2026` | raw recompute |
| part3.html:262 | Genesee `Third-largest Seattle OLA` → `Fourth-largest Seattle OLA` | seattle-olas.csv (Magnuson 9.0 / Westcrest 8.4 / Dr. Jose Rizal 4.0 / Genesee 2.7) |
| part2-access.html:467 | `hold roughly three-quarters` → `hold roughly 70%` | top-3 acreage 21.4/30.7 = 69.8%; self-contradicted the page's top-4 ~79% |
| part2-access.html:671 | Austin table cell `~680*` / `6.63*` → `~80*` / `0.78*` | peer-cities.csv (80 ac / 0.78); matched the chart + footnote, which already say "the figure used here" is ~80 |
| part2-access.html:867 | footer `Data current as of April 2026.` → `June 2026.` | sibling footers (enforcement.html, opinion.html) + JUNE 2026 masthead |
| index.html:98 | `about one officer was actually on park patrol` → `only one of the three positions was filled` | staffing invariant (exactly "one"); matches enforcement.html:92 |
| opinion.html:393 | `added two full-time animal-control officers` → `added one full-time animal-control officer` | contradicted the site's own "~1 officer" enforcement thesis (2016 MOA = 1 ACO + 1 FMW, not 2 ACOs) |
| README.md:3 | `~26 acres of fenced space` → `about 30.7 acres` | canonical 30.7 |
| README.md:12 | `4 are under a quarter-acre` → `3 are under a quarter-acre` | verify_site_data.py [5] |
| README.md:14 | Seattle `0.32` (`~8×`/`~4×`) → `0.38` (`6.7×`/`3.4×`) | peer-cities.csv ola_acres_per_10k |
| README.md:16 | `$3.1M capital for two new OLAs` → `$3.46M capital for two new OLAs plus design of a third` | budget-detail.csv |
| METHODOLOGY.md:83 | `~$3.34M` / `10.5%` → `~$3.30M` / `~11%` | enforcement year_trend cost sum = $3.30M; recovery 10.65% |
| DATA-AUDIT.md:122, :164 | `$3.34M` / `10.5%` → `$3.30M` / `~11%` | same |
| AGENTS.md:189 | `69.6%` / `72.1%` → `71.9%` / `73.4%` (gitignored file; fixed in working tree) | citation-rate-by-walkshed-status.csv (park-named 3,089/4,299; combined 3,631/4,948) |
| part2-access.html, opinion.html, budget.html, enforcement builder (multiple) | **2015 survey / illegal-off-leash figure, resolved against the primary source.** (a) Dropped the stale `monthly or more` / `monthly-or-more` / `monthly+` framing; (b) corrected survey year `2016`→`2015` (~11 spots); (c) blended the plan's three settings (39% local parks, 38% large parks, 36% trails) to a single **~38%** headline; (d) relabeled the "38% trails" stat (that value is *large parks*; trails is 36%). | Verified verbatim against committed `sources/people-dogs-and-parks-plan-august-2017.pdf` **p.17** (owner-supplied). Blend + components documented on part2 Finding 05 and in the data notes. |

**Part III per-park recompute (owner decision).** Recomputed directly from the raw
`data/enforcement-citations.csv` (filter `dlp_only=True AND location_type=park_named`,
grouped by `location_canon`): **Magnuson 367 · Genesee 152 · Westcrest 122** over the
full 2014–Apr 2026 window — matching the enforcement top-20. Note for the record: the
site's old numbers (248/130/86) were wrong *even for their stated 2014–2019 window* —
the true pre-COVID slice is 257/131/89 — so this was a double error (wrong count **and**
wrong window), not merely a stale window. Window labels aligned to the enforcement page's
"2014–2026".

### Clarity fixes (C) — rewrites shown verbatim

- **index.html:74 — gloss "walkshed" on first homepage use.**
  Before: `3,089 of 4,299 park-named citations, 2014–2026 (via public records request, PRR).`
  After: `3,089 of 4,299 park-named citations fell outside the walkshed — the area within a 10-minute walk — 2014–2026 (via public records request, PRR).`
- **index.html:102 — gloss "Find-It-Fix-It".**
  Before: `Find-It-Fix-It "Nuisance Dogs in a Park" complaints (C263990)`
  After: `Find-It-Fix-It (Seattle's report-a-problem app) "Nuisance Dogs in a Park" complaints (C263990)`
- **part2-access.html:418 — add missing denominator** (resolves an index-vs-part2 71.9%/73% surface inconsistency; see §2).
  Before: `73% of off-leash citations (2014–2026) fall outside any OLA's 10-minute walkshed`
  After: `73% of mapped off-leash citations (2014–2026) fall outside any OLA's 10-minute walkshed`
- **peer-cities.html:253 — spell out MOU on first use.**
  Before: `there are no formal co-management MOUs at the scale of Seattle's`
  After: `there are no formal co-management Memoranda of Understanding (MOUs) at the scale of Seattle's`
- **scripts/build_enforcement_page.py (regenerates enforcement.html) — three glosses on first use:**
  - `(FAS) + FMW program cost` → `(FAS) + Facilities Maintenance Worker (FMW) program cost` (builder :164)
  - `attributable FTE` → `attributable full-time equivalent (FTE)` (builder :166)
  - `under SMC 18.12.080's escalation schedule` → `under Seattle Municipal Code (SMC) 18.12.080's escalation schedule` (builder :218)

---

## 2. Substantive findings — report-only (severity-ranked)

These are structural, editorial, or framing issues where a fix would change meaning,
argument, or page structure — out of scope for auto-apply. Each has a concrete recommendation.

### P1

- **part1-the-gap.html:279 — the "OLA improvement $" column conflates two measures.**
  The methodology time-series column headed "OLA improvement $" holds OLA-only figures for
  2016–2018 ($100,000) and then silently switches to the **combined OLA + P-Patch** BC-PR-50000
  line from 2019 on ($569,561 … $1,845,706). Read top-to-bottom it looks like OLA spending grew
  ~18×, when OLA-only was roughly flat and is only ~22% of the combined line. The budget page
  itself labels this figure "combined OLA + P-Patch" and warns it "overstates OLA-specific
  spending." Independently flagged by dimension L **and** the red-team SPR persona ("lands: yes").
  The three stale cells are now corrected, but the header still mislabels the series.
  **Recommend:** rename to "OLA + P-Patch combined $" and either add a disclosed OLA-only column
  (blank where SPR doesn't publish it, as budget.html does) or footnote the OLA-only share.

- **part2-access.html:~418, ~461, ~1181 — dangling references to charts/maps that no longer render.**
  The JS defines `chartTplPriority` (44%/15% equity tiers), `chartDeficit`, and a
  `walkshed-citation-map`, each behind an `if(element)` guard — but **no matching
  `<canvas>`/`<div>` exists in the page body**, so all three silently no-op. The prose still
  references them: the "Equity: … (Method and sources in Data notes)" pointer (line 418) leads to
  a Data-notes section that contains no priority-tier method, and the fineprint (line 461) lists 6
  excluded ZIPs while the (non-rendering) deficit JS excludes 10. The 44%/15% figures themselves
  verify against `tpl-priority-coverage.csv` (High 43.7, Medium 14.5). This is consolidation
  debris — the citation-vs-access map was intentionally moved to the Enforcement page, but the
  dead JS and dangling pointers stayed. **Recommend:** either restore the charts + the methodology
  note, or remove the dead JS blocks and the "(Method and sources in Data notes)" pointer, and
  reconcile the excluded-ZIP fineprint to the code.

- **index.html:72 vs part2-access.html:418 — 71.9% (park-named) vs 73% (combined).**
  The homepage stat tile shows 71.9% of *park-named* citations outside the walkshed; part2's
  summary line uses the *combined* (park-named + geocoded street-address) 73.4%→73%. Both are
  correct but read as the same claim with different numbers. Partially addressed this pass by
  adding "mapped" to the part2 line. **Recommend:** the owner decide whether to feature one figure
  consistently or keep both with explicit labels.

### P2

- **index.html:51–55 (hero) — 11.7% is paired against 99% under different standards.**
  The hero sets the 11.7% (10-minute walk) OLA figure against TPL's 99% (any park, 10-minute walk),
  while SPR's *own* published OLA standard is 2.5 miles, under which coverage is 76.6% — disclosed
  in the deck but at smaller weight. Red-team SPR persona ("partly lands"): reframes an SPR
  methodology choice as failure without adopting SPR's methodology. **Recommend:** show 11.7%
  (10-min) / 76.6% (SPR's 2.5-mi) / 99% (any park) at comparable weight, or label in the hero that
  11.7% applies a stricter standard than SPR's OLA standard.
- **index.html:55 — "For dogs, it's one of the worst" is an unsourced superlative** on the landing
  hero, one line above "every number links back to where it came from," and partially undercut by
  the site's own peer table (Austin 1.28 < Seattle 1.82 per 100k). **Recommend:** replace with the
  sourced comparative it stands in for (e.g. "ranks below every major West Coast peer") and link it.
- **budget.html:118 — normative clause on a factual page.** "…a constituency whose budget share
  would be orders of magnitude higher if it tracked usage" asserts a funding norm (spend ∝ usage)
  under an "Observation" kicker. Red-team ("partly lands"): opinion leaking onto a neutral page.
  **Recommend:** cut the "if it tracked usage" clause or move it to opinion.html; state the two
  numbers and let the reader infer.
- **Number-density (dimension M):** enforcement.html Finding 01's two Observation paragraphs
  (~2 dozen and 7+ figures), budget.html Finding 02 Observation (6 figures), and opinion.html O1
  (states "the constraint is authority, not headcount" three times in one passage) exceed the
  ~3-figures-per-paragraph readability smell. **Recommend:** thin to the load-bearing figures.
- **part1-the-gap.html:286/291/292 vs budget.html — column precision mismatch (low).** Part I's
  appendix "OLA improvement $" column prints full-dollar precision on three rows that budget.html
  and the CSVs render rounded, so the same combined BSL line reads as two numbers between the two
  pages: 2019 $160,757 (part1) vs $160,800 (budget/CSV); 2025 $1,829,717 vs 1829.7; 2026 $1,845,706
  vs 1845.7. (The 2021/2023/2024 rows agree because the CSV stores those at full precision.) Part I
  is the *more* precise side, so this is a presentation-consistency call, not a data error — **do
  not blindly round Part I to match the CSV.** **Recommend:** standardize precision across the
  column (either carry the exact figures on budget.html too, or footnote that budget.html rounds).

---

## 3. Per-page key points & cut lists (report-only)

All nine pages have a coherent key point stated in the hero/deck (verified). Cut candidates,
ranked — the owner decides:

1. **part1 Finding 03** (investment-vs-density scatter) — weakest support for Part I's
   "supply flatlined" point; it's really a Budget/peer-cities argument. Relocate.
2. **Duplicate facilities point** — the playgrounds-vs-OLAs comparison (157 vs 14; 14.6×/39×)
   runs near-identically on **both** part1 Finding 06 and budget Finding 04. Pick one home.
3. **part1 Findings 04+05** (SPR budget vs OLA budget; Cycle 1 vs Cycle 2) substantially preview
   the Budget page — compress Part I to a single budget teaser.
4. **updates.html** — the two adjacent June-2026 ACO-MOA entries document the same three-officer
   program (two records releases). Consolidation candidate.

Also flagged (M): part1 Finding 03's scatter has a descriptive title with no takeaway annotation —
an average adult can't state its point in ten seconds.

---

## 4. Red-team report (hostile-reader personas)

Three personas (SPR communications staffer, skeptical data journalist, motivated Reddit poster).
Attacks that **land** are folded into §2. Attacks that **fail** (site is right) — worth recording
because they're the ones a challenger will try first:

- **"Zero net OLAs in 17 years hides the 2026 openings" (fails).** The claim is literally true and
  the 2026 openings + $3.46M Cycle 2 capital are disclosed in the same breath (hero deck, stat
  tiles, Finding 05). "Net" is accurate accounting, not a dodge.
- **"Rising cost, falling output = SPR wasted money" (turns back on the attacker).** The enforcement
  page repeatedly measures cost against the ~1 officer that actually existed, notes billing is on
  hours worked, and states the data "cannot prove or disprove" behavior change — so the honest
  reading isn't "three officers produced nothing." The invariant framing holds.

Strongest landed attacks (all in §2): the "OLA improvement $" column (yes), the 11.7%/99% hero
pairing (partly), the "one of the worst" superlative (partly), the budget "if it tracked usage"
clause (partly), and the 71.9%/73% cross-page pair (partly, now clarified).

---

## 5. Manual-check list — external sources that could not be fetched and verified

Live `WebFetch` was attempted on all claim-bearing external URLs. Confirmed unfetchable — the owner
should verify these in a browser:

- **All Trust for Public Land pages** (`tpl.org/*`) — HTTP 403 (bot-blocked). Covers: Seattle 99%
  10-min-walk, dog-parks-per-100k (1.82 / 5.74 / etc.), $/resident ($418 / $274 / $561), ParkScore
  rank, the 0.5-mi/10-min standard, and the Austin/Boise/Portland/SF per-100k figures.
- **Axios Seattle** (`axios.com/…`) — HTTP 403 (known bot-block). Sources deployment status only
  (one filled / two vacant, 26 rangers, 460+ parks). Confirmed the site attributes **no** dollar
  figure or the three-FTE count to Axios.
- **historylink.org/File/2281** — 403 (Magnuson June 15, 1996 trial opening).
- **nycgovparks.org** (`/facilities/dogareas`, press release `id=19877`) — 403 (9pm–9am off-leash
  hours; April 10, 2007 codification).
- **vancouver.ca** people-parks-dogs-strategy — 403 (36 OLAs; 168-ac time-restricted total).
- **library.municode.com** SMC 18.12.080 — 403 ($162 fourth-offense ceiling).
- **seattle.gov PDFs** — returned as unreadable binary via WebFetch: `seattlerecreationdemandstudy2016.pdf`
  (2.5-mi standard), `Seattle-Park-District-Fact-sheet.pdf` (Cycle 2 $3.46M), `images.akc.org/pdf/GLEG01.pdf`
  (AKC 1-acre minimum).
- **seattle.gov landing pages** — off-leash-area-study (187k–400k dog range) and the People, Dogs
  and Parks Strategic Plan page are navigation shells; the cited detail isn't on the page itself.
- **ofm.wa.gov / data.census.gov / data.seattle.gov** — landing/SPA shells; the figures live in
  linked Excel/table exports (Seattle 2010→2025 population; 364,627 households; ~26,700 dog licenses).
- **web.archive.org** (qacc.net Smith Cove 55k→25k sq ft) — WebFetch cannot reach archive.org at all.
- **council.nyc.gov** dog-run locations — page renders borough headings only, no counts.

**Verified live (for the record):** AVMA 42.6% of households own dogs, 1.6 dogs/household · Portland
"over 30 dog off-leash areas – both fenced and unfenced" · Minneapolis $38 resident / $66 non-resident
first-dog permit · Westcrest reopened "by the end of day, June 10" 2022.

**Link-integrity issue — RESOLVED (July 4):** `magnusondogpark.org` 301-redirects to
`cpbetweenthelakes.com` (dead), and MOLG's alternate domain `magnusonolg.org` no longer resolves.
Research (ProPublica EIN 91-2059268; live domain checks; a Dec 2023 blog post that has since gone
dark) showed the **Magnuson Off-Leash Group is a real 501(c)(3) that went dormant after ~2023**, not
long-defunct. Per owner decision, Part III's Magnuson case study was **recast from "the volunteer-
steward model" to "the site-specific steward model, now dormant"** (past tense; dead links removed;
stat-card "founded 1999" corrected — the 501(c)(3) dates to 2011), the live stewardship exemplar
recentered on **COLA** (still-active; SPR credited COLA's "ongoing stewardship" in a June 2022 post,
EIN 91-1682685 confirmed 501(c)(3)), and MOLG removed from Opinion's *current*-advocates list while
kept as a past-tense historical credit. A verifier guard now fails if `magnusondogpark.org` reappears.
(My earlier note that the dead link was in the `enforcement.html` byline was wrong — it never was.)
The `nrpa.org` 2018 courtesy-hours article URL now returns the current magazine homepage (possible rot).

---

## 6. Reproducibility status

- **verify_site_data.py — extended and passing.** Added three guard blocks:
  - **[7] Part III per-park counts** — recomputes Magnuson/Genesee/Westcrest from the *raw*
    `enforcement-citations.csv` (not a derived file) and asserts 367/152/122, plus checks the
    full-window count+label is present in part3.html and the retired 2014–2019 phrases are gone.
  - **[8] year_trend JSON integrity** — recomputes DLP-by-year from the raw CSV and asserts the
    committed `enforcement_page_data.json` `year_trend` matches every year (this series was
    previously guarded by **neither** verifier); pins total = 7,015 and the 2026-row invariant
    anchors (funded 528279 / attributable 152399 / actual FTE 1.0).
  - **[9] Retired-figure & wording regression guards** — fails if `$346,680`, `$475,142`,
    `$614,343`, `$3.34M`, `+$3.1M`, `$3.1M for two`, or `about one officer` reappears anywhere in
    the public site (closes the presence-check blind spot the part1 table exploited), and — for the
    2016-survey frequency band — **derives** the wording from `illegal-use-indicators.csv` and
    asserts every page matches whatever the CSV says (it does **not** hardcode "weekly-to-monthly",
    so a later source-corrected CSV propagates instead of tripping the guard).
- **verify_enforcement_data.py** — `ALL CHECKS PASSED` (unchanged).
- **build_enforcement_page.py** — idempotent (identical SHA on a second run); the only diff vs HEAD
  is the three intended glosses. Fixes to enforcement.html were made in the **builder**, per
  generated-file discipline.
- **docs/data** mirrors **data/** — no `data/*.csv` was changed this pass, so no `sync-data.sh` needed.
- **Known verifier limits still open** (dimension Q): `verify_enforcement_data.py` imports the
  staffing/cost constants from the same builder it checks (a wrong constant would pass both) — the
  new [8] block mitigates this for the DLP series and the 2026 cost anchors but not the full model;
  and the presence-based prose checks remain fundamentally string-existence, now backstopped by the
  [9] negative guards for the specific retired figures.
- **AGENTS.md** is gitignored (untracked); its fix (69.6→71.9 / 72.1→73.4) is applied to the working
  file but will not appear in the commit. **Flag for the owner:** CLAUDE.md calls AGENTS.md the
  "canonical shared context (Codex and Claude Code both use it)," yet it is untracked — a canonical
  doc that silently isn't versioned. Worth deciding whether to track it or confirm the ignore is
  intentional.
- **Second discovery round** (on the fixed site): the regression pass returned CLEAN — the applied
  edits introduced no new inconsistency. The fresh-eyes pass surfaced the 39% self-contradiction
  (aligned this pass; direction gated on the manual source check — §2 #2), the part1/budget
  precision mismatch (§2, report-only), and re-surfaced the 71.9%/73% pair (§2, P1). This was **one
  fix in round 2, then converged** — not a zero-finding round; a further round would re-surface only
  the report-only items and the pending source check.

---

## 7. Open questions for the owner

1. **AVMA inputs.** The live AVMA page now shows 42.6% ownership × 1.6 dogs/household; the site's
   ~248,900 derivation cites 45.5% × 1.5. The product lands within ~0.2% either way, but the per-
   household inputs differ — reconcile against the AVMA edition/table you intend to cite.
2. **The 39% survey figure — RESOLVED (merge gate lifted).** The owner supplied the primary source;
   it is now committed at `sources/people-dogs-and-parks-plan-august-2017.pdf`. Page 17 states the
   figures verbatim: "39 percent illegally use local parks weekly to monthly," "38 percent … large
   parks weekly to monthly," "36 percent illegally use park trails." So **"weekly to monthly" is
   confirmed correct** (the plan never says "monthly or more"), and the earlier Part II/Opinion
   drift was the error. Reading the plan surfaced two further corrections, both now applied and
   verified against p.17: **(a)** the survey was conducted in **2015**, not 2016 (the site said
   "2016 survey" in ~11 places); **(b)** the site's "38% on park trails" stat actually reported the
   *large-parks* figure — trails was 36%. Per the owner's direction the three settings are now
   **blended to ~38%** (unweighted mean of 39/38/36 = 37.7%, rounded) and documented on Part II
   Finding 05 and in the data notes. See §1 and §6.
3. **magnusondogpark.org / MOLG — RESOLVED (July 4).** MOLG is a dormant-since-~2023 501(c)(3); Part
   III recast as "site-specific steward model, now dormant," dead links removed, COLA made the live
   exemplar, Opinion updated, and a verifier guard added (see §5). Optional follow-up: add a Wayback
   snapshot of the old MOLG site as an archival citation if desired.
4. **"OLA improvement $" column** (§2 P1) — relabel, split, or footnote? Editorial/structural call.
5. **part2 equity charts** (44%/15%, deficit, walkshed-citation map) — restore the visualizations
   and the method note, or remove the dead JS and dangling pointers?
6. **Cut-list decisions** (§3) — relocate part1 Finding 03; de-duplicate the playgrounds-vs-OLAs
   point; compress part1's budget preview; consolidate the two June-2026 update entries.
7. **Hero framing** (§2 P2) — equal-weight 11.7% / 76.6% / 99%, and swap the "one of the worst"
   superlative for its sourced comparative?

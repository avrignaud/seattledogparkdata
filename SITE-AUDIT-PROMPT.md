# Full-site audit prompt v2 — accuracy, defensibility, readability

> **July 2026.** Supersedes the June 28 version of this file (in git history) and
> folds in `SITE-CLARITY-AUDIT-PROMPT.md`. Written for a Fable-class agent using
> the Workflow tool at the repo root. Read `CLAUDE.md` first.

---

## Mission

Audit the entire public site (`docs/*.html`) plus the data and scripts behind
it, against three goals that together mean **nobody can successfully challenge
this site**:

1. **Accuracy & reproducibility.** Every number traces to a primary source, is
   arithmetically correct, and recomputes from committed scripts and CSVs.
2. **Consistency.** Every figure is stated identically and fairly everywhere it
   appears; every reference to the data is accurate.
3. **Readability & defensibility.** A smart average adult — an engaged resident,
   a councilmember's staffer, a skeptical journalist — can read any page top to
   bottom without a glossary, take away the key point, and find nothing to
   screenshot and dunk on. The site has been deliberately consolidated down to
   key points and what falls out of them; verify the consolidation worked and
   finish it where it didn't.

The site is honest and truthful by design. Opinion lives **only** on
`docs/opinion.html`, and even there every factual premise must meet the same
accuracy bar as the data pages.

## Owner decisions for this pass (settled July 2026 — don't re-ask)

- **Fix authority:** apply **mechanical fixes** (wrong numbers, dead links,
  format drift, alt-text contradicting its chart) **and low-risk clarity
  rewrites** (glossing an acronym on first use, splitting a run-on, adding a
  missing denominator or caveat, plain-language paraphrase of method jargon)
  directly — **in Andre's voice** (see below). Anything that changes meaning,
  structure, an argument, a page's framing, or `opinion.html`'s editorial voice
  is **report-only** with exact suggested replacement text.
- **Cut lists: yes**, report-only (see dimension M).
- **Part III per-park counts: update to the full window.** `part3.html` cites
  Magnuson 248 / Genesee 130 / Westcrest 86 citations for 2014–2019 — never
  verified against raw data. Recompute per-park full-window (2014–Apr 2026)
  counts from `data/enforcement-citations.csv` (not a derived CSV), update the
  prose and window labels on `part3.html` to match the enforcement page's
  window, preserve the surrounding contextual argument, and add the counts to
  `verify_site_data.py`.
- **External sources: fetch live.** WebFetch each cited URL and confirm the
  cited figure/title/date actually appears on the page. Any source you cannot
  fetch and verify by viewing (403s, paywalls, JS-only pages — Axios is known
  bot-blocked) goes on a **manual-check list** for the owner; don't guess.
- **Don't bump** site-wide dates, the editorial signature, `CHANGELOG.md`, or
  `updates.html` — that's a separate, human-approved step. (The masthead
  currently says JUNE 2026; leave it.)

## Andre's voice (for applied rewrites)

Editorial but restrained. Short declarative sentences preferred over long ones.
Plain language; no hype, and no hedging beyond what the data requires. No
em-dashes where a comma would do. Acronyms spelled out on first use per page.
Numbers per house style (below). When a rewrite can't preserve this voice,
report instead of applying.

## Prior audit state (June 28, 2026) — re-verify, don't trust

The June pass (`AUDIT-FINDINGS.md`) applied 9 mechanical fixes, extended
`verify_site_data.py` to 73 checks, and found the staffing-framing invariant
clean. Treat that file as a **hypothesis to attack, not ground truth** —
re-derive from primary sources. At the start of this pass both verifiers pass,
the enforcement builder is idempotent, and `docs/data` mirrors `data/` — a fresh
failure is a regression to localize. Known carryovers: the Part III counts
(owner decision above) and the per-year enforcement JSON series still lacking a
verifier guard (add one).

## How to run (Fable workflow)

Use the Workflow tool. Suggested shape — adapt as needed:

1. **Per-page readers** — one agent per public page: `index.html`,
   `part1-the-gap.html`, `part2-access.html`, `part3.html`, `enforcement.html`,
   `budget.html`, `peer-cities.html`, `opinion.html`, `updates.html`. Each
   extracts every number/claim with `file:line`, what it asserts, its linked
   source, plus the page's apparent key point and structure. (Skip `mockup-*`,
   `mockups.html`, `print.html`.)
2. **Dimension auditors** (A–Q below) run against the whole corpus.
3. **Adversarial refutation** — every substantive finding is attacked by
   independent skeptics (majority vote) before it survives; the report must
   contain no false positives.
4. **Red team** (dimension N) runs against the *whole site*, not per-finding.
5. **Synthesis** — dedupe, resolve cross-page contradictions per primary source,
   severity-rank.
6. **Apply** the in-scope fixes, re-run builders + both verifiers, then run a
   **second discovery round on the fixed site** (loop until a round finds
   nothing new — don't stop at one pass).

## Ground rules

- **Generated files — never hand-edit.** `docs/enforcement.html` is generated by
  `scripts/build_enforcement_page.py` from `scripts/enforcement_page_data.json`;
  edit the builder/inputs and re-run. `docs/data/*` is mirrored by
  `scripts/sync-data.sh`. The PDF is built by `build-pdf.mjs`. Full list in
  `CLAUDE.md` → "Generated files." All other HTML pages are hand-maintained.
- **After any fix:** re-run `.venv/bin/python scripts/build_enforcement_page.py`
  (if the builder changed), then **both** verifiers —
  `.venv/bin/python scripts/verify_enforcement_data.py` and
  `.venv/bin/python scripts/verify_site_data.py` (each must print
  `ALL CHECKS PASSED`) — and `bash scripts/sync-data.sh` (if any `data/*`
  changed). The enforcement builder must be idempotent (second run = no diff).
- **Cite-everything:** every factual claim links a primary source; flag bare
  numbers.

## The staffing-framing invariant (CRITICAL — most error-prone)

Three distinct concepts must never be conflated:

- **Funded / approved** — what the Park District authorized. Three ACO IIs since
  the **2023** MOA; FAS-side max **$454,652/yr** (2023) → **$528,279/yr** (2026
  MOA, wage re-pricing). An *authorization*, not spending.
- **Hired / filled** — bodies actually employed. As of **April 2026, one** of
  three positions filled; the two added in 2023 still being hired (Axios).
  Always exactly **one** — never "about one."
- **Deployed** — time the filled officer actually spends on off-leash patrol
  (parks were ~**33%** of these officers' calls in 2021).

Rules the whole site must obey:
1. Measure output and cost-per-citation against staffing that **actually existed
   (~1 officer)** — never against the funded three.
2. Never imply the city "tripled cost/output and got nothing."
3. **Actual spend ≈ one officer (~$176K) today**, billed on hours worked, rising
   toward $528,279 only as positions fill. More officers won't raise citations
   much because the cap is **authority** (can't compel ID), not headcount.
4. The SPR-side partner changed from net-new FMWs (2023) to existing/retasked
   Park Rangers (2026 MOA) — no phantom "additional ranger cost." SPR-side cost
   is undocumented (PRR #10 pending).
5. Retire any survivor of: "3× scale-up," "even at 3× staffing," "tripled
   cost," "$700K–$1M," "about one patrols."

## Canonical figures (verify each against its primary source AND that it appears
## identically everywhere)

> The **primary source is truth**, not this list — the list is the consistency
> target and may itself contain an error to catch.

- Enforcement: **7,015** DLP citations (2014–Apr 2026); peak **1,276** (2018);
  **447** (2024), **267** (2025), **393** (2020), **183** (2014), **1,181**
  (2019); cost/citation **$229** (2018), **$1,730** (2022), **$654** (2024);
  per-FTE **638** (2018), **224** (2024); cumulative cost **$3.30M**, recovery
  **~11%**, fee revenue **$351,099**; baseline full-team **$292,399**; first-
  offense **84–96%**; named-park **89%**; Discovery **564**, Magnuson **367**,
  Volunteer **328**, Woodland **291**, Golden Gardens **227**, Lincoln **173**;
  top-10 share **46%** pre / **40%** post-COVID; 2025 complaints **~3,010**,
  ~**11:1**, r=**0.13**. (Part III per-park counts move to this window per the
  owner decision above.)
- ACO cost: **$152,399** (2021, 1 ACO) · **$151,551**/FTE & **$454,652** (2023)
  · **$176,093**/FTE & **$528,279** (2026) · top rate **$44.79 → $54.46**.
- Budget: SPR total **$168M** (2018) → **$507M** (2026 proposed); OLA-only
  **$100,000** (Cycle 1), **$126,000** (2023), **$129,000** (2024); combined
  BC-PR-50000 (City-adopted, PRR C265589): 2021 **$322,912**, 2022 **$355,347**,
  2023 **$569,561**, 2024 **$584,343**, 2025 **$1.83M**, 2026 **$1.85M**;
  OLA-only ≈ **22%** of combined; **0.06%** of land and of budget; Cycle 2
  capital **$3.46M**; license revenue **$1.24M/yr**; fines **~$29K/yr**.
- Access/peer: walkshed **11.7%** (0.5-mi) / **76.6%** (2.5-mi); OLAs **14**
  (→**16** fall 2026); acreage **30.7**; per-dog **5.4–5.5 sq ft** (Seattle),
  **~11** (Austin fenced), **~19** (Portland), **~20** (SF), **~37** (Vancouver
  BC); playgrounds **157** vs **115,000** kids; citywide park acreage **6,662**.
- Dog population: **150,000** floor / up to **400,000** (SPR 2023 study) /
  **~248,900** household-derived. Floor for floor-claims; cite the study for
  higher.

## Audit dimensions

### Track 1 — Accuracy & reproducibility

**A. Numbers → source.** Every load-bearing number links a primary source that
actually contains it. **Fetch the linked source live** and confirm the cited
fact, title, and date appear; unfetchable sources go on the manual-check list.
Flag bare numbers.

**B. Calculations reproduce.** Recompute every derived figure from stated
inputs: cost-per-citation, recovery %, per-FTE, basis points, sq-ft-per-dog,
residents-per-OLA, the 0.06% shares, 22%-of-combined, the $300K–$376K band, the
14.6×/39× ratios, the $3.30M cumulative, and every "N×"/"a third of"/"doubled"
in prose. Note any that don't reconcile.

**C. Reproducibility / build chain.** Run builders + both verifiers; confirm
idempotency. **Gotcha:** `enforcement_page_data.json` is committed source the
page renders from — not auto-generated, not cross-checked by verify — so confirm
the JSON `year_trend`, `data/enforcement-year-metrics.csv`, and
`build_enforcement_metrics.py` agree (esp. the 2026 row: funded 528279,
attributable 152399, aco_fte 1.0). Add a verifier guard for the per-year JSON
series. Confirm `docs/data/*` mirrors `data/*`. Grep both verifier scripts
before flagging anything "not machine-checked."

**D. Staffing framing.** Apply the invariant to every page. Priority dimension.

### Track 2 — Consistency

**E. Cross-page consistency.** Any figure on >1 page matches exactly and is
phrased compatibly ($528,279; 7,015; 150,000; 0.06%; 11.7%; 14 OLAs; 30.7 ac;
6,662 ac). Same thing named the same way everywhere ("Lower Woodland" vs
"Woodland Park"; "off-leash area" vs "dog park" vs "OLA"). Internal `#anchor`
links resolve (enforcement keeps `finding-02`/`finding-07` IDs for back-compat).

**F. Links & sources.** No 404s; MOA/PRR blob links resolve to committed files;
**check link *text*, not just URLs** — a citation's article title and date must
match the linked document. Axios is HTTP-403/bot-blocked: confirm the URL is
canonical only, and confirm it sources *only* deployment-status facts (one
officer now, two vacant, "two full-time seven-day positions plus backup," 26
rangers, "more than 460 parks") — the three-FTE count and every dollar figure
are MOA/PRR; flag any attributed to Axios.

**G. Charts vs prose vs alt-text.** Chart data matches surrounding prose and the
CSV behind it; every `aria-label`/alt text describes the *current* data.

**H. Dates / temporal / partial-year.** Date references internally consistent;
2026 is partial (through Apr 17, ~29%) — every chart/figure marks or excludes it
correctly, with annualization caveats where needed.

**I. House style / formatting.** Per `CLAUDE.md`: spell out sub-$1M and counts
($100,000; 150,000); millions as `$X.XXM` (no forced `.00`); no `($K)/($M)` in
table headers; acronyms defined on first use per page; type classes not inline
font-size.

**J. Stale-claims sweep.** Grep for survivors of every retired claim (invariant
rule 5), the old `$475,100`/`$614,300` figures, `$3.34M`, `6,414`/`6,400` acres,
stray `2014–2019` enforcement windows (Part III moves to full-window this pass),
and any pre-consolidation phrasing the June restructure was supposed to remove.

### Track 3 — Readability & defensibility

**K. Jargon & acronyms.** Every acronym/domain term expanded in plain language
on first use **on each page** (readers land mid-site from shared links). Track:
OLA, DLP, SPR, FAS, ACO/ACO II, FMW, MOA, SMC, PRR, Find-It-Fix-It, TPL, AVMA,
BSL, P-Patch, COLA, MOLG, walkshed, isochrone, and any method jargon
("alpha-shape," "point-in-polygon," "kernel density" — paraphrase in body prose
or push to a methodology note). Gloss-on-first-use fixes are in-scope to apply.

**L. Misreadable claims & statistics.** Find every figure or sentence that
invites a *wrong* reading and check it's caveated **where it appears**, not in a
far-off footnote. The template case: "cost per citation" reads as a per-ticket
production cost but is total-program-cost ÷ citations for a program the MOA
calls primarily educational. Hunt the same class: ratios read as unit costs;
correlations read as causes; percentages without denominators; peer-city
comparisons whose definitions differ (Portland voice-control vs Seattle fenced;
Austin ~80 fenced vs 682 inflated; Vancouver beach access — caveat near every
peer chart); modeled estimates reading as measured facts (the walkshed %; the
$140K FMW author estimate — labeled every time they appear?); full-window counts
reading as current-year values.

**M. Key points & cut lists (report-only).** Per page: state the page's one key
point. Verify the hero/deck/takeaway states it and every section, chart, and
callout either supports it or falls out of it. Deliver a ranked **cut list** of
content that does neither, one-line rationale each — the owner decides what
goes. Also flag: any paragraph carrying more than ~3 figures (number-density
smell); any chart whose takeaway an average adult couldn't state in one sentence
after ten seconds, and whether its title/annotation states it for them; the same
point made twice on one page.

**N. Red team (report-only).** An agent (or several, with different personas)
plays a hostile reader — an SPR communications staffer, a skeptical data
journalist, a motivated Reddit poster — whose only job is to find the sentence
they'd screenshot and challenge. Technically-true-but-misleading phrasing,
unstated assumptions, cherry-pick-shaped comparisons, the weakest sourced claim
on each page, anywhere the site's own methodology caveats (in `METHODOLOGY.md` /
`CLAUDE.md`) aren't honored on-page. Also flag **over-hedging**: qualifiers the
data doesn't require, which make the site read unsure of itself. For each hit:
the attack, why it lands (or doesn't), and the fix that closes it.

**O. Opinion-page integrity.** On `opinion.html`: classify every sentence as
fact or opinion. Every factual premise must trace to a data page or primary
source and match it **exactly**; no factual claim may exist *only* on the
opinion page; opinion must be signposted as opinion (recommendation, judgment,
"should"). Voice and argument are report-only; factual-premise corrections
follow the normal fix rules.

**P. Precision calibration.** Every number's stated precision matches its
confidence: MOA/PRR dollar figures can be exact ($528,279); modeled estimates
(11.7%) and author estimates ($140K FMW) must read as estimates every time;
derived ratios shouldn't carry more significant figures than their inputs
support. Flag false precision and spurious exactness in prose.

**Q. Docs & verifier blind spots.** `METHODOLOGY.md`, `DATA-AUDIT.md`,
`sources/SOURCES.md`, `README.md` consistent with the current site and data
window; no stale references to removed files. Scrutinize both verifiers for
blind spots (shared constants with builders; presence-based prose checks that
can't catch a contradictory number elsewhere on a page); list what they still
don't guard, and extend `verify_site_data.py` with any load-bearing number the
audit had to hand-check.

## Output

Write `AUDIT-FINDINGS-2026-07.md` at repo root (leave the June
`AUDIT-FINDINGS.md` as the prior record):

- **Fixes applied** — table: file:line · category (mechanical / clarity) ·
  before → after. Clarity rewrites shown verbatim so the owner can voice-check.
- **Substantive findings (report-only)** — severity-ranked: P0 wrong,
  contradictory, or actively misleading · P1 unsourced, misreadable, or
  cross-page inconsistent · P2 clarity/consistency friction · P3 nit. Each with
  file:line, the issue, the primary source, and exact suggested replacement
  text where wording is the fix.
- **Per-page key points & cut lists** (dimension M).
- **Red-team report** (dimension N) — the attacks, which land, the fixes.
- **Manual-check list** — every external source that couldn't be fetched and
  verified by viewing, with the claim it supports.
- **Reproducibility status** — verifier results, idempotency, JSON/CSV/model
  agreement, mirror status, verifier extensions made.
- **Open questions for the owner.**

## Definition of done

Both verifiers pass; enforcement builder idempotent; every in-scope fix applied,
re-verified, and voice-consistent; Part III counts moved to the full window and
verifier-guarded; `verify_site_data.py` extended to cover any load-bearing
number it didn't already; a second discovery round found nothing new; every
substantive finding adversarially checked (no false positives); the report
complete with cut lists, red-team results, and the manual-check list.

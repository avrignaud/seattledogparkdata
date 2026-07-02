# Site audit prompt — clarity, consistency, and correctness across the whole site

> **SUPERSEDED (July 2026):** folded into `SITE-AUDIT-PROMPT.md` v2 (Track 3,
> dimensions K–L). Kept for reference; don't run standalone.

Paste everything below the line into a capable LLM/agent running in this repo
(`seattledogparkdata.com`) with read/execute access. It asks for a single
whole-site pass that finds anything making the site hard to **read, parse, or
trust** — then a concrete clean-up plan.

This was written after a sharp reader got "mired in acronyms" and misread a
metric ("cost per citation") as something it wasn't. Treat that as the bar: a
smart non-expert (an engaged resident or a councilmember's staffer) should be
able to read any page top to bottom without a glossary and without being misled.
An undefined acronym or a misreadable statistic erodes trust as much as a wrong
number does.

---

You are auditing **seattledogparkdata.com**, a static, sourced civic-data site
about Seattle's off-leash dog-area system. Your job: produce a prioritized
punch-list of everything that makes the site hard to read, parse, understand, or
verify — then propose fixes. Be exhaustive and specific (cite `file:line`).

## Orientation

- **Public pages** (the audit surface): `docs/index.html`, `part1-the-gap.html`,
  `part2-access.html`, `part3.html`, `enforcement.html`, `budget.html`,
  `peer-cities.html`, `opinion.html`, `updates.html`. (`opinion.html` is a
  clearly-marked editorial; everything else is meant to be neutral and factual.)
- **Data**: `data/*.csv`, `data/walkshed/`, raw records in
  `data/prr-responses/{C049204,C263949}/*.xlsx`, cost source in
  `data/moas/*.pdf`.
- **Scripts**: `scripts/*.py` (notably `build_enforcement_datasets.py`,
  `build_enforcement_metrics.py`, `build_enforcement_page.py`,
  `build_enforcement_hotspots.py`, `citation_walkshed_analysis.py`,
  `geocode_street_addresses.py`, `compute_walkshed.py`,
  `population_coverage.py`, `verify_enforcement_data.py`) and the PDF builder
  `scripts/build-pdf.mjs`.
- **Docs**: `METHODOLOGY.md`, `DATA-AUDIT.md`, `sources/SOURCES.md`, `README.md`,
  `CLAUDE.md`. The pages are generated/served statically (no build step); the
  PDF report is rendered from the live pages.
- **Verifier**: `.venv/bin/python scripts/verify_enforcement_data.py` should end
  with `ALL CHECKS PASSED`. Two companion prompts already cover deep data
  reproduction — `ENFORCEMENT-AUDIT-PROMPT.md` (per-year ground truth, the 2019
  overlap rule, the cost model) and `CODEX-AUDIT-PROMPT.md` (whole-site data +
  auditing the verifier itself). Use their ground-truth tables, but **treat them
  as claims to confirm, not as answer keys**, and don't re-derive everything they
  cover — your focus is clarity + consistency on top of correctness.

Work the five layers below. Don't stop at correctness; clarity is the point.

## Layer 1 — Jargon & acronyms (lead with this)

For every page, list each acronym or domain term and check it is expanded in
plain language **on first use on that page** (a reader landing mid-site from a
shared link shouldn't have to hunt). Known terms to track — flag any used bare:

`OLA` (off-leash area), `DLP` ("Dog Loose in Park"), `SPR` (Seattle Parks &
Recreation), `FAS` (Finance & Administrative Services), `ACO`/`ACO II` (Animal
Control Officer), `FMW` (Facilities Maintenance Worker), `MOA` (Memorandum of
Agreement), `SMC` (Seattle Municipal Code), `PRR` (public records request),
`FIFI` / Find-It-Fix-It, `TPL` (Trust for Public Land), `AVMA`, `BSL` (Budget
Summary Level), `P-Patch`, `COLA`, `WSDOT`, `OFM`, `ArcGIS`, `walkshed`,
`isochrone`, `point-in-polygon`, `kernel density`.

Report: (a) every bare/undefined first use with `file:line`; (b) terms expanded
inconsistently (e.g., spelled out on one page, bare on another); (c) a
recommendation — gloss-on-first-use per page, and/or a single shared glossary /
expand-on-hover pattern. Method jargon in body prose ("kernel density,"
"point-in-polygon," "alpha-shape") should be either plain-language paraphrased
or pushed into a methodology footnote.

## Layer 2 — Misreadable claims & statistics

Find every figure or sentence that invites a *wrong* reading, and check each is
caveated where it appears (not only in a far-off footnote). The template case:
"cost per citation" reads as a per-ticket production cost, but it's
total-program-cost ÷ citations for a program the MOA calls "primarily
educational." Hunt for the same class of trap elsewhere, e.g.:

- ratios presented as unit costs or causes presented as correlations;
- percentages without a stated denominator ("X% of citations" — of what total?);
- per-capita / "N× fewer than Portland" comparisons whose base or definition
  differs between cities (peer-city OLA counts use different definitions — see
  `CLAUDE.md`);
- "seven-fold," "a third of peak," "doubles" — verify the arithmetic and that
  the baseline is stated;
- estimates stated with false precision (the walkshed % is a modeled estimate;
  the $140K FMW figure is an author estimate — are both labeled as such every
  time they appear?);
- counts that changed with the 2014→2026 data extension but might read as
  current-year values.

For each: the claim, the likely misreading, whether it's caveated, and a fix.

## Layer 3 — Cross-page consistency

Build a table of every figure that appears on more than one page (total
citations, walkshed %, OLA count and acreage, dog-population floor, per-capita
ratios, cost figures, date windows) and confirm they agree with each other **and**
with the data. Flag:

- the same number stated two ways on two pages;
- inconsistent date windows (enforcement claims should be uniformly 2014–2026 —
  flag any stray "2014–2019");
- the same place/thing named differently (e.g., "Lower Woodland" vs "Woodland
  Park," "off-leash area" vs "dog park" vs "OLA"), and inconsistent number/date
  formatting.

## Layer 4 — Verify statements, math, and sources

- Run the verifier; confirm `ALL CHECKS PASSED`, then trace a sample of on-page
  numbers back to the raw data/scripts yourself (recompute from
  `data/enforcement-citations.csv` / the raw XLSX, not from a derived CSV).
- Check each factual, non-derived claim against `sources/SOURCES.md` and the
  linked primary source; flag dead links, mismatches, or claims with no source.
- Confirm the methodology caveats in `CLAUDE.md` are actually honored on-page
  (peer-city definitions; the OLA budget being a combined OLA+P-Patch line; the
  150K dog-population floor; Austin's adjusted ~80-acre figure; the walkshed
  being a modeled estimate, not a citable TPL number).

## Layer 5 — Scripts, docs, and the verifier itself

- Do the build scripts run cleanly, and do the committed CSVs match a fresh
  rebuild (no hand-edited data)? Are docstrings/comments accurate, with no stale
  references to removed files (e.g. `print.html`, the retired
  `enforcement-offense-mix.csv` / `enforcement-program-economics.csv`)?
- Are `METHODOLOGY.md`, `DATA-AUDIT.md`, `SOURCES.md`, and `README.md` consistent
  with the current site and data window?
- Scrutinize `verify_enforcement_data.py` for blind spots: it shares
  constants/helpers with the build scripts (so it can't catch a wrong shared
  assumption), and its HTML prose check is presence-based (it can't catch a
  *contradictory* number elsewhere on a page, and only checks figures it knows to
  compute). List what it does **not** guard.

## Deliverable

A prioritized punch-list, grouped by page and tagged by category
(`jargon` / `misreadable` / `inconsistency` / `accuracy` / `scripts-docs`), with
severity:

- **P0** — wrong, contradictory, or actively misleading (fix before anything ships)
- **P1** — confusing or unsourced enough that a careful reader would stumble or distrust
- **P2** — clarity/consistency friction (jargon, formatting, naming)
- **P3** — nitpick / polish

For each item: `file:line`, the problem, why it hurts readability or trust, and a
concrete suggested fix (exact wording where you can). End with a short **clean-up
plan**: the order to fix things in, and which fixes are mechanical (safe to apply
directly) vs. which touch editorial/narrative and need author review.

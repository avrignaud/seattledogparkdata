# Codex audit prompt — whole-site data, math, prose, AND the audit harness itself

Paste everything below the line into Codex running in this repo
(`seattledogparkdata.com`) with read/execute access. It asks Codex to verify the
published numbers *and* to audit the verification scripts that claim those
numbers are correct — because a green test suite is worthless if the suite is
circular, under-covers, or silently passes on bad data.

---

You are auditing **seattledogparkdata.com**, a static civic-data site about
Seattle's off-leash dog-area (OLA) system. Every published claim is supposed to
trace to primary data (CSVs in `data/`, public-records XLSX in
`data/prr-responses/`, PDFs in `data/moas/`) and be reproducible from committed
scripts in `scripts/`. Your job is to find anything that is wrong, unsupported,
or only *appears* verified.

Work in three layers. Do not stop at layer 1.

## Layer 1 — Reproduce the data and math from raw sources

The Python venv is `.venv/bin/python`. Start by running the existing harness:

```
.venv/bin/python scripts/verify_enforcement_data.py
```

It should print `ALL CHECKS PASSED`. **Treat that as a hypothesis, not a result**
(see Layer 3). Then independently re-derive — with your *own* code, not the
project's helper functions — and compare:

- **Enforcement citations.** Re-read every XLSX under
  `data/prr-responses/C049204/` (old format: one worksheet per offense level per
  year-range, has an `Issue Date/Time` column) and `data/prr-responses/C263949/`
  (SSRS export: header on row 3 / data from row 4, ~49 cols, CaseID col 2 is NOT
  unique, a `"Total Violations: N"` sentinel sits in col 48 on a trailing
  non-data row). Confirm per-year and per-source counts against
  `data/enforcement-citations.csv` (expected: 7,532 rows = 3,774 C049204 +
  3,758 C263949; 7,015 are DLP-only). The **2019 overlap rule**: C049204's
  partial 2019 must be dropped and C263949's full-year 2019 used — verify zero
  C049204 rows have `year==2019`.
- **Per-year metrics.** Recompute `data/enforcement-year-metrics.csv` yourself
  (DLP counts, fee revenue, cost = aco_fte×$152,399 + fmw_fte×$140,000,
  cost/citation, citations/FTE, first-offense %). The detailed ground-truth
  table lives in `ENFORCEMENT-AUDIT-PROMPT.md` — **treat that table as one more
  claim to verify, not as an answer key.** Cumulative figures should be
  $3,341,409 cost, $351,099 revenue, 10.5% recovery.
- **Determinism.** Re-run `scripts/build_enforcement_datasets.py` and
  `scripts/build_enforcement_metrics.py` and confirm the committed CSVs match a
  fresh build byte-for-byte (i.e., nobody hand-edited a committed CSV).
- **Cost anchor.** Open `data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf`,
  Attachment A, and confirm $43.07/hr × 1.45 × 2,088 + $3,000 + $19,000 =
  $152,398.73 → the $152,399 constant. Confirm `$140,000` FMW is labeled an
  *estimate* everywhere it appears (it is not sourced).
- **Rest of the site's data.** Don't stop at enforcement. Verify against their
  CSVs + `sources/SOURCES.md`: the **network walkshed** figures (run
  `scripts/compute_walkshed.py` + `scripts/population_coverage.py`; the site
  claims ~11.7% of residents within a 10-min walk of an OLA and 76.6% within
  SPR's 2.5-mile standard), the **14-OLA count and acreages** in
  `seattle-olas.csv` (7 below the AKC 1-acre floor; top-4 ≈ 79% of acreage),
  the **timeseries** (`seattle-timeseries.csv`: zero net OLAs since 2009,
  +34% population), and the **peer-city** table.

## Layer 2 — Audit every text/prose statement against the data

The numbers can be right in the CSV and wrong on the page. Go page by page
through `docs/*.html` (the public set: index, part1-the-gap, part2-access,
part3, enforcement, enforcement-draft, budget, peer-cities, opinion, updates)
and extract **every** numeric or factual claim — stat cards, chart captions,
prose, table cells, footnotes — and check each against the data and sources.
Known traps documented in `CLAUDE.md` that the prose must honor, not paper over:

- The walkshed number is an estimate from a specific method; a network analysis
  gives a *smaller* number than the old straight-line 33%. Flag any over-claim.
- **Peer-city OLA counts use different definitions** (Portland counts unfenced
  voice-control areas; Austin's 682-acre figure is inflated — the apples-to-
  apples fenced number is ~80). Confirm caveats are present and the adjusted
  Austin number is the one used.
- The post-2022 OLA "budget" is a **combined BSL** that also funds P-Patch
  gardens — SPR doesn't break out OLA-only. Confirm the site says so.
- Dog-population floor is 150K (SPR's own study cites up to 400K). Confirm which
  number is used where.
- OLA coordinates are approximate.

Also confirm the **opinion** content is confined to `opinion.html` and the page
prose elsewhere stays factual (the project's stated facts-first framing).

## Layer 3 — Audit the audit scripts and safety checks (the important part)

A passing harness only matters if the harness can actually fail. Scrutinize
`scripts/verify_enforcement_data.py` and the build scripts for false confidence:

1. **Circularity.** The verifier imports the build scripts' own constants and
   helpers (e.g. `STAFFING`, `FAS_ACO_ANNUAL`, `FMW_ANNUAL` from
   `build_enforcement_metrics.py`; `canonicalize()`, `OLD_SHEET_RE` from
   `build_enforcement_datasets.py`). Anywhere the verifier recomputes a value
   using the same code/constant that produced it, it **cannot** catch a wrong
   assumption — it will agree with itself. List every such spot and re-derive
   that value from first principles independently. Pay special attention to the
   hand-pinned `GROUND_TRUTH_*` dicts: confirm each against raw XLSX.
2. **Prose check coverage and weakness.** `verify_html_prose()` is
   *presence-based*: it asserts a computed string appears *somewhere* in the
   site corpus. Enumerate its blind spots: (a) it cannot detect a *contradictory*
   wrong number elsewhere on a page; (b) a value can match coincidentally;
   (c) any claim it doesn't compute is unguarded. Produce the list of on-page
   claims that the ~35 checks do **not** cover, and check those by hand.
3. **Mutation test the safety checks.** Prove the harness fails when it should.
   In a scratch copy or with a git-stashable edit: (i) change one value in
   `data/enforcement-citations.csv`, (ii) change one prose number in a docs page,
   (iii) change a cost constant — and confirm `verify_enforcement_data.py` FAILS
   on each, then revert. Report any mutation that slips through silently; each is
   a hole in the safety net.
4. **Corpus/allowlist correctness.** The prose check scans an explicit
   `PUBLIC_PAGES` + `STAGED_PAGES` allowlist and is supposed to FAIL if a
   canonical public page is missing. Confirm that behavior, and confirm
   scaffolding (`*preview*`, `proposal-*`, mockups, print) is correctly excluded
   so it can't mask an error on a real page.
5. **Tolerances and skips.** Find every `tolerance`, `>=`, range check, or
   early `return`/skip in the verifier and judge whether it's hiding real drift
   (e.g. the legacy derived-CSV ±30 count tolerance — is that masking a
   canonicalization bug?).

## Deliverable

A discrepancy report. For each finding: (a) the claim/value as published or as
asserted by a script, (b) what you independently derived, (c) match/mismatch,
(d) root cause, and (e) severity. Separately, list every weakness you found in
the audit scripts themselves, and the result of the mutation test (which
deliberate breakages were caught vs. missed). Call out anything that claims more
precision or certainty than the underlying data supports.

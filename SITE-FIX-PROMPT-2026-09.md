# Prompt: implement the September 2026 site audit, section by section, with approval

Paste everything below the line into a fresh session.

---

Implement every fix in `SITE-AUDIT-2026-09.md` (accuracy, Tiers A–D) and then the
simplification pass it recommends, walking me through the site one section at a time so I
approve each change before it lands. Read `SITE-AUDIT-2026-09.md`, `C266465-PRR-AUDIT.md`,
`data/prr-responses/C266465/README.md`, `CLAUDE.md`, and `AGENTS.md` first. Today's date is
whatever the system says; the site masthead currently says July 2026.

## How we work

**Walkthrough format.** Go page by page in this order: `index`, `part1-the-gap`,
`part2-access`, `part3`, `enforcement`, `budget`, `peer-cities`, `opinion`, `updates`. On
each page, go section by section from the top. For every section that needs a change, show
me one block in exactly this shape and then stop and wait:

> **[page] › [section heading]** — *why:* one line, citing the audit item (A1, C-table row,
> etc.) and the primary source.
> **Now says:** the existing sentence(s), quoted verbatim.
> **Proposed:** the replacement, in the house voice.
> **Also touches:** any CSV, script, or other page that must change with it (twins).

I reply with *ok*, an edit, or *skip*. Apply only what I approve. If a section needs no
change, say so in one line and move on; don't make me approve nothing. Batch trivially
mechanical items (a date, a rounding, a label) into one block per page so we're not
approving commas one at a time.

**Ground rules.**
- `docs/enforcement.html` is generated. Never edit it directly: change
  `scripts/enforcement_page_data.json` and/or `scripts/build_enforcement_page.py`, re-run the
  builder, run `python3 scripts/verify_enforcement_data.py`, and confirm a second builder run
  is a no-op. Cost changes touch **both** the page-data JSON and
  `data/enforcement-year-metrics.csv` via `build_enforcement_metrics.py`.
- After any `data/*.csv` change, run `scripts/sync-data.sh` and both verifiers. Any new
  hub figure gets a guard added to `scripts/verify_site_data.py` (the audit found the
  biggest errors were invisible to it: opening years, the 2010 OLA count, "roughly one
  officer").
- Every changed factual sentence links to its source. New primary sources from the July
  release are already archived under `data/prr-responses/C266465/documents/` and indexed
  in `sources/SOURCES.md`; cite by Bates number where the audit does.
- Keep the house voice and the facts-first split: corrected facts go on the data pages,
  argument stays on `opinion.html`. Do not reintroduce editorial takeaways on data pages.
- **Do not commit or push.** Leave everything in the working tree; I'll commit. Do not bump
  mastheads or write the updates-log entry until Phase 3, when I say.
- If the data contradicts the audit, or two sources disagree, stop and show me both. Don't
  pick silently.

## Phase 0 — decisions I make before you touch anything

Ask me these four, one message, then wait:

1. **OLA chronology.** `seattle-olas.csv` `year_opened` disagrees with SPR's 2017 plan on 11
   of 12 sites. Recommend adopting the plan's years (opened), with a `year_permanent` column
   for Kinnear 2014 / Magnolia Manor 2015, and re-provenancing the column to the plan. That
   changes the headline to "zero net since 2013, thirteen years" and the 2010 baseline to 11.
   Confirm, or tell me which source wins.
2. **Citations vs. warnings.** 45% of the 7,015 records are $0 verbal warnings; post-2019
   only 7% are actual citations. Option A: rename the metric "enforcement contacts"
   site-wide and add one sentence explaining the split. Option B: split every chart and
   figure into citations vs. warnings (cost per *actual* citation in 2024 is ~$13,900). B is
   the real finding; A is a day's work less. Which?
3. **Enforcement cost model.** Drop the paired-maintenance-worker cost ($140K/yr) from 2023
   onward (the position was vacant, per SPR's own memo) and replace the modeled ACO cost for
   2023–24 with the billed figures ($453K / $456K)? This changes the cost-per-citation series
   and the $3.30M program total. Recommend yes.
4. **Opinion length.** The audit proposes cutting `opinion.html` from ~6,150 to ~3,500 words
   by folding P5/P6 into P4, collapsing C1/C2/C4/C5/C6 into one objections paragraph,
   moving the NYC evidence to Part III, and trimming acknowledgments. That's your signed
   piece: do the full cut, a lighter trim, or accuracy-only?

## Phase 1 — data model first (Tier B)

Before any page: show me each CSV/script change as a diff block (old row → new row, with
source), one block per file. `seattle-olas.csv` years; `seattle-timeseries.csv` 2026 row
(16 → 14, note) and 2025 note ("+$3.1M" → "$3.46M"); `planned-olas.csv` status and dates
(Fall 2027, sourced to SPR's 2026-03-24 statement; Othello marked "verify directly");
`park-coordinates.csv` Lincoln note; `illegal-use-indicators.csv` (drop the ~1,100 row, fix
435 → 543 or re-source it); `build_enforcement_metrics.py` FMW schedule and billed-cost
override; `licensing-revenue.csv` 2025 partial-year check; the fee-revenue DLP-only fix.
Then regenerate everything downstream and show me the verifier output.

## Phase 2 — the page walkthrough (Tiers A, C, D, and the new primary sources)

Use the audit's tables as the checklist. Per page, cover in this order: (a) the Tier A
headline twins on that page; (b) the Tier C rows for that page; (c) the Tier D items I
haven't skipped; (d) the "opportunities" where a City statement replaces author inference
(the C266465 audit §P3–P7 and each page auditor's list). For enforcement, the eight
spend-sentences come first and every proposal names its builder line. For opinion, separate
fact fixes (the $176,000 sentence, the 25% conflation, the 0.06% land claim, the 2023
approval date) from the length cut, and do the facts first.

Anywhere a peer-city claim rests on an external URL with recency risk (Portland levy,
Vancouver Park Board, SF licensing), propose either a dated caveat or a fetch-and-archive;
don't rewrite from memory.

## Phase 3 — simplification, same mechanic

Only after Phase 2 is approved on every page. Per page, propose the cut in one block:
which sections become one paragraph plus charts, which move into Data Notes, which
duplicate another page and get replaced by a one-line pointer, and the new plain-language
headings replacing "Finding 0N" (keep the old `id` anchors). Show a before/after word count.
Wait for approval per page. Opinion last, per my Phase 0 answer.

## Phase 4 — close out

When I say: add the `updates.html` entry and index-panel entry (this is a logged update:
headline figures changed and C266465 is ingested), bump mastheads and bylines per
`CLAUDE.md`, bump `CHANGELOG.md` to a new version with the accuracy corrections stated
plainly, update `METHODOLOGY.md` and `DATA-AUDIT.md` for the chronology ruling and the
citations/warnings definition, correct the stale lines in `AGENTS.md` and `CLAUDE.md` the
audit lists, run both verifiers and the PDF build, and give me the final `git diff --stat`.

Before you report any phase done: re-run the named verification and show the real output,
`git diff --stat` against the scope you declared, and list anything you skipped and why.

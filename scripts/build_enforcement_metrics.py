#!/usr/bin/env python3
"""
Build data/enforcement-year-metrics.csv — the per-year derived metrics that
drive the enforcement page's fiscal and productivity charts.

Input:
  - data/enforcement-citations.csv  (consolidated, built by build_enforcement_datasets.py)
  - the staffing + cost model defined below (assumptions, documented inline)

Output:
  - data/enforcement-year-metrics.csv

The staffing FTE schedule and the FMW cost estimate are ASSUMPTIONS, not raw
records. They are stated here explicitly so the derived metrics are auditable.
Sources:
  - FAS-side ACO II annual cost $152,399: 2021 MOA AG21-PRF03-032 Attachment A (sourced).
  - FMW pairing $140,000/yr: author estimate; SPR does not publish a per-FMW
    off-leash line. Flagged as estimate. Applies 2016-2022 only: the paired
    Facilities Maintenance Worker left for a Park Ranger post in 2023 and was never
    backfilled ("There is no current FMW working with the Animal Control Officers",
    SPR Jainga memo Sep 2024, PRR C266465 Bates PKS_C266465_01_00360).
  - Billed ACO cost 2023-2024: SPR's quarterly ledger backup (PRR C266465, Bates
    00485 / 00653; data/prr-responses/C266465/documents/enforcement-moa-billing.csv).
    The 2023 MOA billed a flat 240 hr/pay period for three FTE regardless of hours
    worked, so what SPR paid tracked the FUNDED headcount, not deployment:
    FY2024 $456,173; H1 2023 $226,528 (Q3/Q4 not produced; annualized x2).
  - Per-FTE ACO rate by MOA year: 2021 MOA $152,399 (2014-2022); 2025 MOA
    $169,565 (2025); 2026 MOA $176,093 (2026). 2023-2024 use billed actuals.
  - FTE schedule: 1 part-time ACO pre-2016 (imputed from PRR context); the April
    2016 MOA brought a full-time ACO II + paired FMW online mid-2016; the 2021
    MOA continued that structure. Three categories from 2023 on: FUNDED (three
    ACO II under the 2023/2025/2026 MOAs), BILLED (three, on calendar-derived
    invoices, 2023-2024; actual-hours billing only from the 2025 MOA), and
    DEPLOYED (FAS reported it could field 1.5-2.0 in Feb 2025, Bates 00541;
    ~1 on parks as of Apr 2026 per Axios Seattle 2026-04-17). annual_cost() uses
    billed where a ledger exists and the deployed model elsewhere.
    Pre-2016 and the 2016 transition year are the softest assumptions and are flagged.
  - Fee revenue is summed over DLP-only rows (the same universe as every
    denominator); non-DLP violations in the PRR files are excluded.
  - Case results: the PRR records carry case_result (Citation / Verbal / blank /
    Voided / Dismissed). Verbal warnings only appear from 2018, so
    cost_per_actual_citation is blank before 2018 (warnings were not recorded in
    the C049204 files, not absent).

2026 is a partial year (through 2026-04-17). cost_per_citation and
citations_per_fte are emitted as blank for 2026 to avoid the partial-year
denominator inflating those ratios; the partial flag is set instead.

Usage: .venv/bin/python scripts/build_enforcement_metrics.py
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CITATIONS = REPO_ROOT / "data" / "enforcement-citations.csv"
OUT = REPO_ROOT / "data" / "enforcement-year-metrics.csv"

FAS_ACO_ANNUAL = 152399      # sourced: 2021 MOA Attachment A (per ACO II FTE)
FAS_ACO_ANNUAL_2023 = 151551 # sourced: 2023 MOA PRF1602 (per ACO II FTE; 3 FTE = $454,652)
FAS_ACO_TOTAL_2023 = 454652  # sourced: 2023 MOA PRF1602 (3 ACO II FTE, FAS-side)
FAS_ACO_ANNUAL_2026 = 176093 # sourced: 2026 MOA (per ACO II FTE; top rate $54.46/hr; 3 FTE = $528,279)
FAS_ACO_TOTAL_2026 = 528279  # sourced: 2026 MOA (3 ACO II FTE, FAS-side authorized maximum)
FAS_ACO_ANNUAL_2025 = 169565 # sourced: 2025 MOA (per ACO II FTE; 3 FTE max $508,695 on actual hours)
FMW_ANNUAL = 140000          # estimated: author triangulation (2016-2022 FMW pairing; position vacant from 2023, Bates 00360)

# Billed ACO cost where SPR's ledger backup exists (PRR C266465). Calendar-derived
# invoices for three staff; see documents/enforcement-moa-billing.csv.
BILLED_ACO = {
    "2023": 453056,  # H1 2023 $226,528 (Q1 $113,454.64 + Q2 $113,073.24) x 2 — ANNUALIZED, Q3/Q4 not produced
    "2024": 456173,  # FY2024 actual: $113,391.08 + $113,073.24 + $114,854.56 + $114,854.56
}


def aco_rate(year: str) -> int:
    """Per-FTE ACO II annual cost under the MOA in force that year."""
    y = int(year)
    if y >= 2026:
        return FAS_ACO_ANNUAL_2026
    if y == 2025:
        return FAS_ACO_ANNUAL_2025
    return FAS_ACO_ANNUAL


def annual_cost(year: str) -> int:
    """Single owner of the program's annual cost: billed actuals where the ledger
    exists (2023-2024), otherwise the deployed-staffing model. verify_enforcement_data.py
    calls this rather than re-deriving it."""
    aco, fmw = STAFFING[year]
    if year in BILLED_ACO:
        return BILLED_ACO[year] + round(fmw * FMW_ANNUAL)
    return round(aco * aco_rate(year) + fmw * FMW_ANNUAL)

# (aco_fte, fmw_fte) attributable to OFF-LEASH enforcement, by year. This is the
# conservative, output-anchored measure used for cost-per-citation and per-FTE —
# deliberately NOT the funded headcount (see FUNDED_ACO below). It is held flat
# because parks patrols are a minority of these officers' duties (33% of Field
# Services calls in 2021) and citation output never corroborated a larger field
# deployment. See verify/docs notes.
STAFFING = {
    "2014": (0.5, 0.0),
    "2015": (0.5, 0.0),
    "2016": (0.75, 0.75),
    "2017": (1.0, 1.0),
    "2018": (1.0, 1.0),
    "2019": (1.0, 1.0),
    "2020": (1.0, 1.0),
    "2021": (1.0, 1.0),
    "2022": (1.0, 1.0),
    "2023": (1.0, 0.0),   # FMW vacant from 2023 (Bates 00360); ACO cost overridden by BILLED_ACO
    "2024": (1.0, 0.0),   # same; BILLED_ACO
    "2025": (1.0, 0.0),   # actual-hours billing from the 2025 MOA; ledger not produced; ~1-2 deployed
    "2026": (1.0, 0.0),   # ~1 on parks as of Apr 2026 (Axios); 2026 MOA rate
}

# FUNDED ACO headcount, by year — what the Park District actually pays for under
# the SPR/FAS MOAs, regardless of how much lands on off-leash. DOCUMENTED, not
# estimated: one ACO II 2016–2022 (2016 & 2021 MOAs); three ACO IIs from 2023
# (2023 MOA PRF1602, term through 2027). Pre-2016 mirrors STAFFING. The gap
# between this and STAFFING is the "funded vs. traceable" band on Finding 02.
FUNDED_ACO = {
    "2014": 0.5, "2015": 0.5, "2016": 0.75,
    "2017": 1.0, "2018": 1.0, "2019": 1.0, "2020": 1.0, "2021": 1.0, "2022": 1.0,
    "2023": 3.0, "2024": 3.0, "2025": 3.0, "2026": 3.0,
}


def funded_aco_cost(year: str, fte: float) -> int:
    """FAS-side funded ACO cost (authorized annual maximum, 3 FTE). 2026+ uses the
    2026 MOA total; 2023-2025 the 2023 MOA total; earlier years the 2021 MOA
    per-FTE rate."""
    if int(year) >= 2026:
        return FAS_ACO_TOTAL_2026
    if int(year) >= 2023:
        return FAS_ACO_TOTAL_2023
    return round(fte * FAS_ACO_ANNUAL)

# 2026 partial-year cutoff (inclusive day count for annualization).
Y2026_CUTOFF = date(2026, 4, 17)
PARTIAL_YEARS = {"2026"}


def partial_year(year: str) -> bool:
    return year in PARTIAL_YEARS


def result_bucket(case_result: str) -> str:
    """Collapse case_result into citation / verbal / other (blank, Voided, Dismissed)."""
    v = (case_result or "").strip().lower()
    if v == "citation":
        return "citation"
    if v == "verbal":
        return "verbal"
    return "other"


def main() -> None:
    rows = list(csv.DictReader(CITATIONS.open()))

    dlp_by_year = Counter()
    all_by_year = Counter()
    offense_by_year: dict[str, Counter] = defaultdict(Counter)
    revenue_by_year: dict[str, float] = defaultdict(float)
    result_by_year: dict[str, Counter] = defaultdict(Counter)

    for r in rows:
        y = r["year"]
        if not y:
            continue
        all_by_year[y] += 1
        if r["dlp_only"] == "True":
            dlp_by_year[y] += 1
            if r["offense_level"]:
                try:
                    offense_by_year[y][int(r["offense_level"])] += 1
                except ValueError:
                    pass
            result_by_year[y][result_bucket(r["case_result"])] += 1
            fee = r["fee"]
            if fee not in ("", None):
                try:
                    revenue_by_year[y] += float(fee)
                except (TypeError, ValueError):
                    pass

    years = sorted(STAFFING)
    out_rows = []
    for y in years:
        aco, fmw = STAFFING[y]
        total_fte = aco + fmw
        cost = annual_cost(y)
        dlp = dlp_by_year.get(y, 0)
        res = result_by_year.get(y, Counter())
        n_cit, n_verb, n_other = res.get("citation", 0), res.get("verbal", 0), res.get("other", 0)
        # Verbal warnings are absent from the records before 2018 (not recorded, not zero),
        # so a per-actual-citation cost is only meaningful from 2018.
        cost_per_actual = "" if (partial_year(y) or int(y) < 2018 or not n_cit) else round(cost / n_cit)
        off = offense_by_year.get(y, Counter())
        off_total = sum(off.values())
        first_pct = round(100 * off.get(1, 0) / off_total, 1) if off_total else ""
        repeat_pct = round(100 * (off_total - off.get(1, 0)) / off_total, 1) if off_total else ""
        partial = y in PARTIAL_YEARS
        cost_per_citation = "" if (partial or not dlp) else round(cost / dlp)
        per_fte = "" if (partial or not total_fte) else round(dlp / total_fte, 1)
        funded_aco = FUNDED_ACO[y]
        funded_aco_cost_y = funded_aco_cost(y, funded_aco)
        out_rows.append({
            "year": y,
            "dlp_citations": dlp,
            "all_citations": all_by_year.get(y, 0),
            "aco_fte": aco,
            "fmw_fte": fmw,
            "annual_cost": cost,
            "cost_per_citation": cost_per_citation,
            "citations_per_fte": per_fte,
            "first_offense_pct": first_pct,
            "repeat_offense_pct": repeat_pct,
            "fee_revenue": round(revenue_by_year.get(y, 0.0)),
            "partial_year": "true" if partial else "false",
            "funded_aco_fte": funded_aco,
            "funded_aco_cost": funded_aco_cost_y,
            "traceable_aco_cost": BILLED_ACO[y] if y in BILLED_ACO else round(aco * aco_rate(y)),
            "cost_basis": "billed" if y in BILLED_ACO else "modeled",
            "result_citation": n_cit,
            "result_verbal": n_verb,
            "result_other": n_other,
            "cost_per_actual_citation": cost_per_actual,
        })

    fields = list(out_rows[0].keys())
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {OUT.relative_to(REPO_ROOT)} ({len(out_rows)} rows).")

    # Summary
    total_dlp = sum(dlp_by_year.values())
    cum_cost = sum(r["annual_cost"] for r in out_rows)
    cum_rev = sum(r["fee_revenue"] for r in out_rows)
    print(f"Total DLP: {total_dlp}")
    print(f"Cumulative cost: ${cum_cost:,}  revenue (DLP-only): ${cum_rev:,}  recovery: {100*cum_rev/cum_cost:.1f}%")
    print("Cost per actual citation: " + ", ".join(f"{r['year']} ${r['cost_per_actual_citation']:,}" for r in out_rows if r['cost_per_actual_citation'] != ''))
    print(f"Peak per-FTE: {max((r['citations_per_fte'] for r in out_rows if r['citations_per_fte'] != ''))}")


if __name__ == "__main__":
    main()

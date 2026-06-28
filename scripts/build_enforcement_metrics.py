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
    off-leash line. Flagged as estimate.
  - FTE schedule: 1 part-time ACO pre-2016 (imputed from PRR context); the April
    2016 MOA brought a full-time ACO II + paired FMW online mid-2016; the 2021
    MOA continued that structure. The 2023 MOA *funded* three ACO IIs, but the
    added positions were largely unfilled: as of April 2026 SPR said two of the
    three were still being hired/trained, with roughly one officer working parks
    (Axios Seattle, 2026-04-17). So attributable deployment is held at ~1.0 ACO
    through 2026 — the funded-vs-deployed gap lives in FUNDED_ACO, not here.
    Pre-2016 and the 2016 transition year are the softest assumptions and are flagged.

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
FMW_ANNUAL = 140000          # estimated: author triangulation (2016-2023 FMW pairing; the 2026 MOA pairs ACOs with Park Rangers instead)

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
    "2023": (1.0, 1.0),
    "2024": (1.0, 1.0),
    "2025": (1.0, 1.0),
    "2026": (1.0, 1.0),   # 2023-funded positions still being filled as of Apr 2026 (Axios); ~1 deployed, not 3
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


def main() -> None:
    rows = list(csv.DictReader(CITATIONS.open()))

    dlp_by_year = Counter()
    all_by_year = Counter()
    offense_by_year: dict[str, Counter] = defaultdict(Counter)
    revenue_by_year: dict[str, float] = defaultdict(float)

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
        cost = round(aco * FAS_ACO_ANNUAL + fmw * FMW_ANNUAL)
        dlp = dlp_by_year.get(y, 0)
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
            "traceable_aco_cost": round(aco * FAS_ACO_ANNUAL),
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
    print(f"Cumulative cost: ${cum_cost:,}  revenue: ${cum_rev:,}  recovery: {100*cum_rev/cum_cost:.1f}%")
    print(f"Peak per-FTE: {max((r['citations_per_fte'] for r in out_rows if r['citations_per_fte'] != ''))}")


if __name__ == "__main__":
    main()

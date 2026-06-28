#!/usr/bin/env python3
"""
Verify the NON-enforcement load-bearing numbers on the public site.

scripts/verify_enforcement_data.py already machine-checks the enforcement page.
This companion covers the rest: walkshed/access, peer-city space-per-dog, the
budget figures, facilities ratios, and a few cross-page-consistency anchors.
Like its sibling it is deliberately string-based ("recompute from the committed
CSVs, then grep the rendered public pages for the value the data implies") so it
stays dependency-free and catches stale or fat-fingered prose numbers.

Run from repo root:  .venv/bin/python scripts/verify_site_data.py
Exit code is non-zero if any check fails.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DOCS = REPO / "docs"

# Public pages (same allowlist as verify_enforcement_data.py).
PUBLIC_PAGES = [
    "index.html", "part1-the-gap.html", "part2-access.html", "part3.html",
    "enforcement.html", "budget.html", "peer-cities.html", "opinion.html",
    "updates.html",
]

_FAILS = 0


def check(cond: bool, msg: str) -> None:
    global _FAILS
    print(f"  {'PASS' if cond else 'FAIL'}  {msg}")
    if not cond:
        _FAILS += 1


def approx(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def load_csv(name: str) -> list[dict]:
    return list(csv.DictReader((DATA / name).open()))


def site_html() -> tuple[str, list[str]]:
    parts, missing = [], []
    for n in PUBLIC_PAGES:
        p = DOCS / n
        if p.exists():
            parts.append(p.read_text())
        else:
            missing.append(n)
    return "\n".join(parts), missing


def main() -> None:
    html, missing = site_html()
    for n in missing:
        check(False, f"public page present: {n}")

    def present(needle: str, label: str) -> None:
        check(needle in html, f"prose: {label} ({needle!r}) present in public site")

    # ---- [1] Walkshed / access coverage -----------------------------------
    print("\n[1] Walkshed coverage (data/walkshed/population_coverage.csv)")
    cov = {r["distance"]: r for r in load_csv("walkshed/population_coverage.csv")}
    half = round(float(cov["0.5mi"]["population_coverage_pct"]), 1)
    full = round(float(cov["2.5mi"]["population_coverage_pct"]), 1)
    check(approx(half, 11.7, 0.05), f"0.5-mi population coverage == 11.7% (got {half})")
    check(approx(full, 76.6, 0.05), f"2.5-mi population coverage == 76.6% (got {full})")
    present("11.7", "headline 0.5-mi walkshed %")
    present("76.6", "2.5-mi walkshed %")

    cw = load_csv("walkshed/citation-rate-by-walkshed-status.csv")
    named = {r["walkshed_status"]: r for r in cw if r["pass"] == "park-named"}
    inside = int(named["Inside 0.5-mi OLA walkshed"]["total_citations"])
    outside = int(named["Outside 0.5-mi OLA walkshed"]["total_citations"])
    out_pct = round(100 * outside / (inside + outside), 1)
    check(out_pct == 71.9, f"citations outside walkshed == 71.9% (got {out_pct})")
    check(inside + outside == 4299, f"park-named placed citations == 4,299 (got {inside + outside})")
    present("71.9", "citations-outside-walkshed %")
    present("3,089", "citations outside walkshed count")

    # ---- [2] Peer-city off-leash space per dog ----------------------------
    print("\n[2] Peer-city space per dog (data/peer-cities.csv @ 0.30 dogs/resident)")
    peers = {r["city"]: r for r in load_csv("peer-cities.csv")}
    SQFT_AC = 43560
    expect = {  # city -> the precise figure printed in the chart aria-label
        "Seattle WA": 5.5, "Austin TX": 11.3, "Portland OR": 18.7,
        "San Francisco CA": 20.0, "Vancouver BC": 36.7,
    }
    for city, shown in expect.items():
        r = peers[city]
        acres = float(r["ola_acres_total_est"])
        pop = float(r["population"])
        calc = acres * SQFT_AC / (pop * 0.30)
        check(approx(calc, shown, 0.2),
              f"{city} sq-ft/dog: page {shown} vs recompute {calc:.1f} (tol 0.2)")
    present("5.5 sq ft", "Seattle space-per-dog (peer 0.30 rate)")
    present("doormat", "doormat framing")

    # dog-parks per 100k ratio (TPL-as-reported columns, not recomputed from pop)
    sea = float(peers["Seattle WA"]["dog_parks_per_100k_tpl"])
    por = float(peers["Portland OR"]["dog_parks_per_100k_tpl"])
    check(approx(round(por / sea, 1), 3.2, 0.05), f"Portland/Seattle per-100k ratio == 3.2x (got {por/sea:.2f})")
    present("1.82", "Seattle dog-parks per 100k")
    present("5.74", "Portland dog-parks per 100k")
    present("3.2", "Portland-vs-Seattle multiple")

    # ---- [3] Budget figures ----------------------------------------------
    print("\n[3] Budget (data/budget-detail.csv, data/licensing-revenue.csv)")
    rev = [int(r["dog_license_revenue"]) for r in load_csv("licensing-revenue.csv")
           if 2018 <= int(r["year"]) <= 2024]
    avg = sum(rev) / len(rev)
    check(approx(avg, 1_240_000, 15_000), f"2018-24 license revenue avg ~= $1.24M (got ${avg:,.0f})")
    present("$1.24M", "license revenue / yr")
    present("$29,000", "annual off-leash citation fines")

    bud = {r["year"]: r for r in load_csv("budget-detail.csv")}
    # 2023/2024 combined OLA+P-Patch are now the City-adopted figures (PRR C265589)
    check(bud["2023"]["ola_ppatch_combined_k"] == "569.561", "2023 combined BSL == $569,561 (adopted)")
    check(bud["2024"]["ola_ppatch_combined_k"] == "584.343", "2024 combined BSL == $584,343 (endorsed)")
    check(bud["2022"]["ola_ppatch_combined_k"] == "355.347", "2022 combined BSL filled == $355,347")
    present("569,561", "2023 adopted combined BSL")
    present("584,343", "2024 endorsed combined BSL")
    # 2016 OLA-only as basis points of SPR total: 100,000 / 156,000,000 = 0.064%
    bp2016 = round(100 * 100_000 / 156_000_000, 3)
    check(bp2016 == 0.064, f"2016 OLA-only share == 0.064% (got {bp2016})")
    present("0.064%", "2016 OLA-only basis-point peak")
    present("$100,000", "Cycle 1 OLA-only budget")
    present("$3.46M", "Cycle 2 one-time OLA capital")
    present("$528,279", "2026 MOA FAS-side max (cross-page anchor)")

    # ---- [4] Facilities / access counts ----------------------------------
    print("\n[4] Facilities & access (data/seattle-olas.csv, seattle-timeseries.csv)")
    olas = load_csv("seattle-olas.csv")
    check(len(olas) == 14, f"existing OLA count == 14 (got {len(olas)})")
    peer_sea_count = int(peers["Seattle WA"]["dog_parks"])
    check(peer_sea_count == 14, f"peer-cities.csv Seattle dog_parks == 14 (got {peer_sea_count})")
    ts = {r["year"]: r for r in load_csv("seattle-timeseries.csv")}
    for yr in ("2010", "2025"):
        pop = int(ts[yr]["population"]); n = int(ts[yr]["olas"])
        rpo = round(pop / n)
        shown = int(ts[yr]["residents_per_ola"])
        check(abs(rpo - shown) <= 1, f"{yr} residents-per-OLA: col {shown} vs recompute {rpo}")
    present("58,329", "2025 residents per OLA")
    present("150,000", "dog-population floor (cross-page anchor)")
    present("157 playground", "playground count")
    present("115,000", "under-18 population")

    # ---- summary ----------------------------------------------------------
    print("\n" + "=" * 64)
    if _FAILS:
        print(f"FAILURES: {_FAILS}")
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

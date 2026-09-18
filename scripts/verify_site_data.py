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
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DOCS = REPO / "docs"

# Public pages (same allowlist as verify_enforcement_data.py).
PUBLIC_PAGES = [
    "index.html", "part1-the-gap.html", "part2-access.html", "part3.html",
    "enforcement.html", "budget.html", "peer-cities.html", "opinion.html",
    "data-methods.html", "updates.html",
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

    # Retired figures must not reappear. updates.html is excluded on purpose: its
    # entries are a dated historical record of what the site said at the time, and
    # rewriting them would falsify the log.
    live_html = "\n".join(
        (DOCS / n).read_text(encoding="utf-8")
        for n in PUBLIC_PAGES if n != "updates.html" and (DOCS / n).exists()
    )

    def absent(needle: str, label: str) -> None:
        check(needle not in live_html,
              f"prose: {label} ({needle!r}) gone from the live pages")

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
        "San Francisco CA": 20.0, "Vancouver BC": 36.8,
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
    present("$24,500", "annual off-leash fine revenue (DLP-only, 2014-2025 avg)")

    bud = {r["year"]: r for r in load_csv("budget-detail.csv")}
    # 2023/2024 combined OLA+P-Patch are now the City-adopted figures (PRR C265589)
    check(bud["2023"]["ola_ppatch_combined_k"] == "569.561", "2023 combined BSL == $569,561 (adopted)")
    check(bud["2024"]["ola_ppatch_combined_k"] == "584.343", "2024 combined BSL == $584,343 (endorsed)")
    check(bud["2022"]["ola_ppatch_combined_k"] == "355.347", "2022 combined BSL filled == $355,347")
    present("569,561", "2023 adopted combined BSL")
    present("584,343", "2024 endorsed combined BSL")
    # Cycle 1 OLA-only is the 2017 plan's Cost-of-Services figure, $106,000/yr
    # (pp. 3,5 give the range $103,000-$117,000). The earlier round $100,000 was a
    # floor from a public statement and is retired; so is the unsourced $126K/$129K.
    bp2016 = round(100 * 106_000 / 156_000_000, 3)
    check(bp2016 == 0.068, f"2016 OLA-only share == 0.068% (got {bp2016})")
    present("0.068%", "Cycle 1 OLA-only basis-point level")
    present("$106,000", "Cycle 1 OLA-only budget (2017 plan, Cost of Services)")
    present("$3,103,000", "Cycle 2 two-OLA construction line")
    # The retired figures may still be NAMED, once, in the data-methods correction
    # notice: a correction that cannot say what it corrects is not a correction.
    # What must be gone is every form that asserts them as current.
    for stale in ("$126,000&ndash;$129,000", "$100,000&ndash;129,000",
                  "$100,000&ndash;$129,000", "$100,000 to $129,000",
                  "disclosed $126,000", "roughly $129,000/year"):
        absent(stale, "retired OLA-only claim (PRR C264837)")
    absent("$3.46M", "retired capital figure with no findable source")
    absent("SPR no longer breaks the OLA share out", "retired 'split unpublished' claim")
    present("previously carried $126,000", "the correction notice naming what was withdrawn")

    # --- OLA/P-Patch Master Projects (PRR C264837) ------------------------
    mp = {(r["year"], r["master_project_id"]): r
          for r in load_csv("ola-ppatch-master-projects.csv")}
    OLA, PP = "MC-PR-51002", "MC-PR-51001"
    i = lambda y, m, k: int(mp[(y, m)][k])
    yrs = ["2023", "2024", "2025", "2026"]

    # Row identity: revised - expenses - encumbrances == available balance.
    for y in yrs:
        for m in (OLA, PP):
            lhs = i(y, m, "revised_budget_usd") - i(y, m, "ytd_expenses_usd") - i(y, m, "encumbrances_usd")
            check(abs(lhs - i(y, m, "available_balance_usd")) <= 1,
                  f"{m} {y} revised - spent - encumbered == balance")

    # The two Master Projects exhaust BSL BC-PR-50000. 2024 differs by exactly
    # $30,000 because budget-detail carries the ENDORSED figure and this the ADOPTED.
    for y, tol in (("2023", 1), ("2024", 30_001), ("2025", 20), ("2026", 10)):
        both = i(y, OLA, "adopted_budget_usd") + i(y, PP, "adopted_budget_usd")
        combined = float(bud[y]["ola_ppatch_combined_k"]) * 1000
        check(abs(both - combined) <= tol,
              f"{y} OLA+P-Patch adopted == combined BSL (got ${both:,.0f} vs ${combined:,.0f})")

    spent = sum(i(y, OLA, "ytd_expenses_usd") for y in yrs)
    revised = sum(i(y, OLA, "revised_budget_usd") for y in yrs)
    check(abs(spent - 1_053_037) <= 2, f"OLA 2023-26 spend == $1,053,037 (got ${spent:,})")
    check(abs(revised - 5_625_926) <= 2, f"OLA 2023-26 revised budget == $5,625,926 (got ${revised:,})")
    burn = round(100 * spent / revised, 1)
    check(burn == 18.7, f"OLA 2023-26 burn == 18.7% (got {burn}%)")
    present("$1,053,037", "OLA money spent 2023-26")
    present("$5,625,926", "OLA revised budget 2023-26")
    present("$4,362,265", "OLA unspent balance")

    # Closed-year burn: OLA 34.2% vs P-Patch 32.0%. The site must not claim OLA
    # execution is uniquely bad; these are within ~2 points of each other.
    closed = ["2023", "2024", "2025"]
    cb = {m: round(100 * sum(i(y, m, "ytd_expenses_usd") for y in closed)
                   / sum(i(y, m, "revised_budget_usd") for y in closed), 1) for m in (OLA, PP)}
    check(cb[OLA] == 34.2 and cb[PP] == 32.0,
          f"closed-year burn OLA 34.2% / P-Patch 32.0% (got {cb[OLA]}% / {cb[PP]}%)")
    check(abs(cb[OLA] - cb[PP]) < 5,
          "OLA and P-Patch burn within 5 points: do not claim OLA is uniquely unspent")
    present("32.0%", "P-Patch closed-year burn")
    present("34.2%", "OLA closed-year burn")
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

    # ---- [5] Audit-pass additions (June 2026) -----------------------------
    # Load-bearing numbers neither verifier asserted before the June 2026
    # full-site audit, plus regression guards on figures corrected in that pass.
    print("\n[5] Audit additions (acreage, facilities ratios, per-capita multiples, quarter-acre)")

    # Canonical Seattle parkland acreage = 6,662 (TPL 2025 ParkScore; peer-cities.csv).
    acreage = peers["Seattle WA"]["parkland_acres"]
    check(acreage == "6662", f"peer-cities.csv Seattle parkland_acres == 6662 (got {acreage})")
    present("6,662", "canonical Seattle parkland acreage")
    legal_share = round(100 * 30.7 / 6662, 2)  # 30.7 legal OLA ac / 6,662 parkland ac
    check(approx(legal_share, 0.46, 0.005), f"legal off-leash share of parkland == 0.46% (got {legal_share})")
    present("0.46%", "legal off-leash share of parkland")
    present("99.5%", "share of parkland off-limits to off-leash")
    check("6,400 acres" not in html, "stale '6,400 acres' figure removed (audit June 2026; canonical 6,662)")

    # Budget Finding 02 (Fix A, audit June 2026): OLA-only operating share in basis
    # points, with one-time Cycle 2 capital EXCLUDED from the disclosed (solid) bars.
    # There is no separate capital term any more: PRR C264837 established the Cycle 2
    # OLA capital is booked inside MC-PR-51002, so it is already in ola_only_k for
    # 2025-26. That is why the peak is 2025, not 2016.
    def _bp(numer_k: float, spr_m: float) -> float:
        return round(numer_k * 1000 / (spr_m * 1_000_000) * 10000 * 10) / 10
    ola_bp = {y: _bp(float(r["ola_only_k"]), float(r["spr_total_budget_m"]))
              for y, r in bud.items() if r["ola_only_k"]}
    peak_y = max(ola_bp, key=ola_bp.get)
    check(peak_y == "2025" and ola_bp["2025"] == 46.2,
          f"budget Finding 02 peak == 46.2 bp in 2025 (got {ola_bp[peak_y]} bp in {peak_y})")
    check(ola_bp["2016"] == 6.8, f"2016 Cycle 1 bar == 6.8 bp (got {ola_bp['2016']})")
    check(ola_bp["2023"] == 10.0 and ola_bp["2024"] == 10.4,
          f"2023/24 bars == 10.0/10.4 bp (got {ola_bp['2023']}/{ola_bp['2024']})")
    check(max(ola_bp.values()) < 100,
          "no OLA bar reaches 1% of SPR spending (the Finding 02 headline)")
    present("6.8 bp", "Cycle 1 basis-point level")
    present("46.2", "2025 basis-point peak")

    # Facilities-per-constituent ratios (part1 Finding 06): playgrounds vs OLAs.
    fac = {r["facility"]: r for r in load_csv("seattle-facility-counts.csv")}
    kids_per_play = int(fac["Playgrounds"]["constituent_count"]) / int(fac["Playgrounds"]["count"])
    n_ola = int(fac["Off-leash areas"]["count"])
    ratio_floor = (int(fac["Off-leash areas"]["constituent_count"]) / n_ola) / kids_per_play  # 150K floor
    ratio_high = (400_000 / n_ola) / kids_per_play  # 400K SPR 2023 study high
    check(approx(ratio_floor, 14.6, 0.1), f"facilities ratio at 150,000-dog floor == 14.6x (got {ratio_floor:.1f})")
    check(approx(ratio_high, 39.0, 0.2), f"facilities ratio at 400,000 SPR-study est == 39x (got {ratio_high:.1f})")
    present("14.6&times;", "facilities ratio (150,000-dog floor)")
    present("39&times;", "facilities ratio (400,000 SPR-study estimate)")

    # dogs:children ratio uses the 150,000 floor and 115,000 under-18 (Finding 06 lead).
    dk = round(150_000 / 115_000, 1)
    check(dk == 1.3, f"dogs:children ratio (150K floor / 115K kids) == 1.3 (got {dk})")
    present("1.3 to 1", "dogs-outnumber-children ratio")
    check("1.4 to 1" not in html, "stale '1.4 to 1' dogs:children ratio removed (audit June 2026)")

    # Per-capita OLA-acreage multiples vs Seattle (ola_acres_per_10k ratios, part2 takeaway).
    sea10 = float(peers["Seattle WA"]["ola_acres_per_10k"])
    sf_mult = round(float(peers["San Francisco CA"]["ola_acres_per_10k"]) / sea10, 1)
    por_mult = round(float(peers["Portland OR"]["ola_acres_per_10k"]) / sea10, 1)
    van_mult = round(float(peers["Vancouver BC"]["ola_acres_per_10k"]) / sea10, 1)
    check(sf_mult == 3.6, f"San Francisco per-capita multiple == 3.6x (got {sf_mult})")
    check(por_mult == 3.4, f"Portland per-capita multiple == 3.4x (got {por_mult})")
    check(van_mult == 6.7, f"Vancouver per-capita multiple == 6.7x (got {van_mult})")
    present("3.6&times;", "San Francisco per-capita OLA-acreage multiple")

    # Quarter-acre OLA count = 3 (Denny 0.105, Kinnear 0.124, Plymouth Pillars 0.2 < 0.25 ac).
    qa = [r for r in olas if r["acres"] and float(r["acres"]) < 0.25]
    check(len(qa) == 3, f"OLAs under a quarter-acre == 3 (got {len(qa)})")
    check("four are under a quarter-acre" not in html, "stale 'four are under a quarter-acre' removed (audit June 2026)")

    # Which Master Project is larger depends on the measure, and the three disagree.
    # Guards the data-methods sentence that replaced the retired "P-Patch is the
    # larger share" inference (which rested on the unsourced $126,000 figure).
    share = lambda y, k: round(100 * i(y, OLA, k) / (i(y, OLA, k) + i(y, PP, k)), 1)
    check(share("2023", "adopted_budget_usd") == 57.6 and share("2025", "adopted_budget_usd") == 85.7,
          f"OLA adopted share 2023/2025 == 57.6/85.7% (got {share('2023','adopted_budget_usd')}/{share('2025','adopted_budget_usd')})")
    check(share("2023", "revised_budget_usd") < 50 and share("2024", "revised_budget_usd") < 50,
          "P-Patch is larger than OLA on REVISED budget in 2023-24 (the measure-dependence claim)")
    present("57.6%", "OLA share of the adopted BSL, 2023")
    present("60.5%", "P-Patch share of the revised BSL, 2023")
    absent("suggesting P-Patch is the larger share", "retired inference (PRR C264837)")

    # Space-per-dog reconciliation: 5.37 sq ft (AVMA 248,858 dogs) vs 5.5 (0.30 peer rate).
    avma_sqft = round(30.7 * SQFT_AC / 248_858, 2)
    check(approx(avma_sqft, 5.37, 0.02), f"space-per-dog at AVMA 248,858 dogs == 5.37 (got {avma_sqft})")
    present("5.37", "space-per-dog at AVMA dog estimate")
    present("248,858", "AVMA-estimated Seattle dog count")

    # ---- [6] Complaint-side enforcement figures ---------------------------
    # Enforcement-page figures that verify_enforcement_data.py does not yet
    # assert (it covers citations, not the complaint series). Added here per the
    # audit's "machine-check the whole site" directive. Source:
    # data/complaints-citations-monthly.csv (FiFi nuisance-dog complaints).
    print("\n[6] Complaint series (data/complaints-citations-monthly.csv)")
    cm = load_csv("complaints-citations-monthly.csv")
    comp_2025 = sum(int(r["complaints"]) for r in cm if r["month"].startswith("2025"))
    check(comp_2025 == 3010, f"2025 complaint total == 3,010 (got {comp_2025:,})")
    present("3,010", "2025 nuisance-dog complaint total")
    # complaints-to-citations ratio vs 2025 DLP citations (enforcement-year-metrics.csv)
    ym = {r["year"]: r for r in load_csv("enforcement-year-metrics.csv")}
    dlp_2025 = int(ym["2025"]["dlp_citations"])
    ratio = round(comp_2025 / dlp_2025)
    check(ratio == 11, f"2025 complaints-to-citations ratio == 11 (got {comp_2025}/{dlp_2025} = {ratio})")
    present("11 complaints", "complaints-to-citations ratio prose")
    # Pearson r over the page's co-availability window (2024-04..2026-06 = CMP_MONTHLY).
    win = [r for r in cm if "2024-04" <= r["month"] <= "2026-06"]
    r_corr = round(statistics.correlation(
        [float(r["complaints"]) for r in win], [float(r["dlp_citations"]) for r in win]), 2)
    check(r_corr == 0.13, f"complaint/citation Pearson r (2024-04..2026-06) == 0.13 (got {r_corr})")
    present("0.13", "complaint/citation correlation r")

    # ---- [7] Part III per-park citation counts (raw recompute, full window) --
    # Owner decision (July 2026 audit): part3.html per-park counts move from the
    # never-verified 2014-2019 slice (248/130/86 -- itself wrong; the true slice
    # is 257/131/89) to the full 2014-Apr 2026 window, recomputed from the RAW
    # citations CSV (not a derived file): DLP-only, park-named, grouped by
    # canonical location -- the same filter build_enforcement_hotspots relies on.
    print("\n[7] Part III per-park counts (raw enforcement-citations.csv, DLP park-named)")
    cites = load_csv("enforcement-citations.csv")
    park_ct = Counter(r["location_canon"] for r in cites
                      if r["dlp_only"] == "True" and r["location_type"] == "park_named")
    for park, want in (("Magnuson Park", 367), ("Genesee Park", 152), ("Westcrest Park", 122)):
        check(park_ct[park] == want,
              f"{park} full-window DLP park-named citations == {want} (got {park_ct[park]})")
    p3 = (DOCS / "part3.html").read_text()
    for needle in ("367 citations logged at Magnuson 2014&ndash;2026",
                   "152 citations logged there 2014&ndash;2026",
                   "122 enforcement-data citations 2014&ndash;2026"):
        check(needle in p3, f"part3 shows the full-window count+label ({needle!r})")
    for retired in ("248 citations logged at Magnuson", "130 citations logged there",
                    "86 enforcement-data citations"):
        check(retired not in p3, f"part3 retired 2014-2019 count phrase removed ({retired!r})")

    # ---- [8] Enforcement per-year JSON series (year_trend) integrity ---------
    # scripts/enforcement_page_data.json is committed source the enforcement page
    # renders from; neither verifier guarded its per-year series before this pass.
    # Recompute DLP-by-year from the raw citations CSV, assert the JSON agrees,
    # and pin the 2026-row staffing-invariant anchors (funded vs attributable vs
    # actual FTE) so a bad edit to the JSON cost model can't slip through.
    print("\n[8] Enforcement year_trend JSON vs raw citations")
    epd = json.loads((REPO / "scripts" / "enforcement_page_data.json").read_text())
    dlp_year = Counter(r["year"] for r in cites if r["dlp_only"] == "True")
    jt = {row["year"]: int(row["dlp"]) for row in epd["year_trend"]}
    bad = {y: (jt[y], dlp_year.get(y, 0)) for y in jt if jt[y] != dlp_year.get(y, 0)}
    check(not bad, f"year_trend dlp matches raw citations every year (mismatches: {bad})")
    check(sum(dlp_year.values()) == 7015, f"raw DLP citations total == 7,015 (got {sum(dlp_year.values())})")
    r26 = next(r for r in epd["year_trend"] if r["year"] == "2026")
    check(r26["funded_aco_cost"] == 528279 and r26["traceable_aco_cost"] == 176093
          and r26["aco_fte"] == 1.0 and r26["fmw_fte"] == 0.0,
          "2026 year_trend: funded 528279 / attributable 176093 (2026 MOA rate) / actual FTE 1.0 / FMW 0 "
          f"(got {r26['funded_aco_cost']}/{r26['traceable_aco_cost']}/{r26['aco_fte']}/{r26['fmw_fte']})")
    # The JSON year_trend is hand-maintained and decoupled from the metrics CSV
    # (see the enforcement build chain); pin every cost cell to the CSV so a
    # cost-model change that lands in one but not the other fails here.
    ym = {r["year"]: r for r in load_csv("enforcement-year-metrics.csv")}
    drift = {r["year"]: (r["cost"], ym[r["year"]]["annual_cost"]) for r in epd["year_trend"]
             if str(r["cost"]) != ym[r["year"]]["annual_cost"]}
    check(not drift, f"year_trend cost matches enforcement-year-metrics.csv every year (drift: {drift})")
    for y, billed in (("2023", 453056), ("2024", 456173)):
        check(ym[y]["cost_basis"] == "billed" and int(ym[y]["annual_cost"]) == billed,
              f"{y} cost is BILLED ${billed:,} (PRR C266465 ledger), not modeled")
    check(epd["totals"]["revenue_full"] == 294885, "page-data cumulative revenue is DLP-only $294,885")
    # Citations vs warnings (Sept 2026 audit A4): the split must reconcile to the raw file
    raw_cit = sum(1 for r in cites if r["dlp_only"] == "True" and r["case_result"].strip().lower() == "citation")
    check(raw_cit == 3151 and epd["totals"]["result_citation_full"] == 3151,
          f"actual citations (case_result=Citation) == 3,151 site-wide (raw {raw_cit}, json {epd['totals']['result_citation_full']})")
    r24 = ym["2024"]
    check(int(r24["result_citation"]) == 21 and int(r24["cost_per_actual_citation"]) == 21723,
          f"2024: 21 actual citations, $21,723 per actual citation (got {r24['result_citation']}/{r24['cost_per_actual_citation']})")

    # ---- [9] Retired-figure regression guards (July 2026 audit) --------------
    # Cross-page contradictions the presence-based checks cannot catch: a
    # superseded number surviving on ONE page while the corrected value lives
    # elsewhere (part1's methodology table had drifted from budget.html). These
    # fail if any retired figure/phrase reappears anywhere in the public site.
    print("\n[9] Retired-figure regression guards (July 2026)")
    for stale in ("$346,680", "$475,142", "$614,343", "$3.34M",
                  "+$3.1M", "$3.1M for two", "about one officer",
                  "magnusondogpark.org",  # dead MOLG domain (redirects off-site; group dormant)
                  # Sept 2026 audit: retired headline phrasings (A1/A2/A3/A4/B5)
                  "since 2009", "seventeen years", "17 years", "fall 2026", "Fall 2026",
                  "roughly one officer", "never been fully spent", "has not tripled",
                  "$351,099", "$3.30M", ">435<", "~1,100"):
        check(stale not in html, f"retired figure/dead link absent site-wide ({stale!r})")

    # ---- [9b] OLA chronology + planned-site schedule guards (Sept 2026 audit A1/A2) --
    # These were the audit's biggest misses: nothing asserted opening years, the
    # 2010 baseline, or the planned sites' status.
    print("\n[9b] OLA chronology and planned-site guards (Sept 2026)")
    yrs = sorted(int(o["year_opened"]) for o in olas)
    check(yrs[-1] == 2013, f"most recent OLA opened 2013 (Kinnear) per SPR 2017 plan (got {yrs[-1]})")
    check(sum(1 for y in yrs if y <= 2010) == 11, f"11 OLAs open by 2010 (got {sum(1 for y in yrs if y <= 2010)})")
    check(int(ts["2010"]["olas"]) == 11, f"timeseries 2010 OLA count == 11 (got {ts['2010']['olas']})")
    check(int(ts["2026"]["olas"] or 0) == 14, f"timeseries 2026 OLA count == 14, no opening in 2026 (got {ts['2026']['olas']})")
    perm = {o["ola_name"]: o["year_permanent"] for o in olas if o["year_permanent"]}
    check(perm == {"Magnolia Manor": "2015", "Kinnear": "2014"}, f"year_permanent set only for Kinnear 2014 / Magnolia Manor 2015 (got {perm})")
    planned = {r["ola_name"]: r for r in load_csv("planned-olas.csv")}
    check(planned["West Seattle Stadium"]["expected_open"] == "Winter 2028"
          and planned["Othello Playground"]["expected_open"] == "Fall 2027"
          and not any(r["status"].startswith("Under construction") for r in planned.values()),
          "planned-olas: WSS Winter 2028 / Othello Fall 2027, neither under construction (SPR pages, Apr/Jul 2026)")
    present("2013", "last OLA opening year appears on site")
    ind = {r["metric"]: r for r in load_csv("illegal-use-indicators.csv")}
    check(ind["Off-leash tickets issued by Seattle Animal Control"]["value"] == "543",
          "2016 Mar-Aug ticket row == 543 (recomputed from citations CSV, replaces unsourced 435)")
    mar_aug = sum(1 for r in cites if r["dlp_only"] == "True" and r["year"] == "2016" and r["issued_at"][5:7] in ("03","04","05","06","07","08"))
    check(mar_aug == 543, f"citations CSV Mar-Aug 2016 DLP rows == 543 (got {mar_aug})")
    check(not any(m.startswith("Find It Fix It") for m in ind), "retired ~1,100 FiFi row removed from illegal-use-indicators.csv")
    lic = {r["year"]: r for r in load_csv("licensing-revenue.csv")}
    check(lic["2025"]["partial_flag"].startswith("not partial"), "2025 licensing revenue carries the 1-year-transition note")
    # 2015-survey illegal-off-leash figure. The primary source (People, Dogs and
    # Parks Plan, Aug 2017, p.17 -- committed at sources/) reports three settings:
    # 39% local parks + 38% large parks (weekly to monthly) + 36% trails. The site
    # blends them into one headline, ~38%. This guard DERIVES the components and
    # the blend from illegal-use-indicators.csv (source of record) so a corrected
    # CSV propagates instead of tripping a hardcoded value.
    low = html.lower()
    iu = load_csv("illegal-use-indicators.csv")
    comps = sorted((int(r["value"].rstrip("%")) for r in iu
                    if "illegal off-leash" in r["metric"].lower()
                    and "blended" not in r["metric"].lower()
                    and r["value"].rstrip("%").isdigit()), reverse=True)
    check(comps == [39, 38, 36], f"2015-survey settings from CSV == 39/38/36 (got {comps})")
    blend = round(sum(comps) / len(comps))
    check(blend == 38, f"blended illegal-off-leash figure == 38% (mean {sum(comps)/len(comps):.1f})")
    stated = next((r for r in iu if "blended illegal off-leash" in r["metric"].lower()), None)
    check(stated is not None and int(stated["value"].rstrip("%")) == blend,
          "CSV 'blended' row matches the derived mean (38%)")
    present("about 38%", "blended illegal-off-leash headline figure")
    # The two park components are weekly-to-monthly per the plan; the site must not
    # revert to the non-equivalent 'monthly or more' / 'monthly+' mischaracterization,
    # nor mislabel the survey year (the plan says a 2015 survey, published in 2017).
    check("monthly or more" not in low and "monthly-or-more" not in low and "monthly+" not in low,
          "2015-survey figure not mischaracterized as 'monthly or more'/'monthly+' (plan: weekly to monthly)")
    check("weekly to monthly" in low or "weekly-to-monthly" in low,
          "2015-survey park components documented as 'weekly to monthly' (plan wording)")
    check("2016 survey" not in low and "2016 owner survey" not in low,
          "SPR owner survey dated 2015 (plan), not mislabeled '2016 survey'")

    # ---- summary ----------------------------------------------------------
    print("\n" + "=" * 64)
    if _FAILS:
        print(f"FAILURES: {_FAILS}")
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

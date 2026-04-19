#!/usr/bin/env python3
"""
Cross-tabulate Seattle block groups (TPL ParkServe priority layer) against
the union of 0.5-mile OLA walksheds.

Produces the two CSVs used on Part II Finding 02c:

    data/tpl-parkserve/ola-walkshed-by-tpl-rank.csv
    data/tpl-parkserve/ola-walkshed-by-tpl-priority-tier.csv

Method:
  1. Load data/tpl-parkserve/seattle-park-priority-areas.geojson (606
     block-group polygons filtered to Seattle city proper, derived from
     the ParkServe 2025 nationwide shapefile — see the sibling README).
  2. Load the OLA walkshed union from data/walkshed/ola_isochrones.geojson
     and take the spatial union of all 0.5-mile isochrones.
  3. A block group is classified as "has OLA walkshed coverage" iff its
     geometry intersects the walkshed union. (Using `intersects` rather
     than `within` or `contains` — the walkshed union rarely covers a
     full BG, but any overlap counts as partial access.)
  4. Group by `ParkRank` (TPL's discrete 1-3 priority bucket) and by the
     continuous `ParkPriori` tier (binned at 1-2, 2-3, 3-4, 4-5).

Input:  data/tpl-parkserve/seattle-park-priority-areas.geojson
        data/walkshed/ola_isochrones.geojson
Output: data/tpl-parkserve/ola-walkshed-by-tpl-rank.csv
        data/tpl-parkserve/ola-walkshed-by-tpl-priority-tier.csv

Usage:  .venv/bin/python3 scripts/build_tpl_overlay.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import geopandas as gpd

REPO_ROOT = Path(__file__).resolve().parent.parent
BG_PATH = REPO_ROOT / "data/tpl-parkserve/seattle-park-priority-areas.geojson"
ISO_PATH = REPO_ROOT / "data/walkshed/ola_isochrones.geojson"
OUT_RANK = REPO_ROOT / "data/tpl-parkserve/ola-walkshed-by-tpl-rank.csv"
OUT_TIER = REPO_ROOT / "data/tpl-parkserve/ola-walkshed-by-tpl-priority-tier.csv"


def tier_label(v: float) -> str:
    """Bin ParkPriori (1.0–5.0) into tier labels with inclusive upper
    bounds: (1,2] → 1-2, (2,3] → 2-3, (3,4] → 3-4, (4,5] → 4-5. The
    minimum observed value in the Seattle ParkServe slice is 1.08, so
    nothing falls below the 1-2 bin."""
    if v <= 2:
        return "1-2"
    if v <= 3:
        return "2-3"
    if v <= 4:
        return "3-4"
    return "4-5"


def main() -> None:
    bgs = gpd.read_file(BG_PATH)
    iso = gpd.read_file(ISO_PATH)
    iso05 = iso[(iso["distance"] == "0.5mi") & (iso["ola"] != "__UNION_ALL_OLAS__")]

    # Bring both layers into a consistent projected CRS for stable
    # geometry operations (Washington State Plane North, ft), then back.
    bgs_p = bgs.to_crs(epsg=2926)
    iso_p = iso05.to_crs(epsg=2926)
    walkshed_union = iso_p.geometry.union_all()

    bgs_p["has_ola"] = bgs_p.geometry.intersects(walkshed_union)
    print(f"Block groups total: {len(bgs_p)}")
    print(f"Block groups with any OLA walkshed coverage: {bgs_p['has_ola'].sum()}")

    # By discrete ParkRank (1-3).
    with open(OUT_RANK, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ParkRank", "n_bgs", "n_with_ola", "pct_with_ola"])
        for rank, sub in bgs_p.groupby("ParkRank"):
            n = len(sub)
            n_ola = int(sub["has_ola"].sum())
            w.writerow([int(rank), n, n_ola, round(n_ola / n * 100, 1)])
    print(f"Wrote {OUT_RANK.relative_to(REPO_ROOT)}")

    # By continuous ParkPriori binned.
    bgs_p["tier"] = bgs_p["ParkPriori"].apply(tier_label)
    with open(OUT_TIER, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["priori_tier", "n_bgs", "n_with_ola", "pct_with_ola"])
        for tier in ["1-2", "2-3", "3-4", "4-5"]:
            sub = bgs_p[bgs_p["tier"] == tier]
            n = len(sub)
            if not n:
                continue
            n_ola = int(sub["has_ola"].sum())
            w.writerow([tier, n, n_ola, round(n_ola / n * 100, 1)])
    print(f"Wrote {OUT_TIER.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

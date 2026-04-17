#!/usr/bin/env python3
"""
Compute population-weighted walkshed coverage for Seattle OLAs.

Extends the area-based results from compute_walkshed.py into a true
TPL-comparable percentage: what share of Seattle *residents* live within
a 10-minute walk of an existing off-leash area.

Methodology:
1. Load the walkshed union GeoJSON from data/walkshed/ola_isochrones.geojson
   (produced by compute_walkshed.py).
2. Download 2020 Census block-group geometries + total population for
   King County, WA via pygris + Census API.
3. Download Seattle city boundary (Census TIGER Places).
4. Clip block groups to Seattle.
5. For each walkshed distance (0.5, 1.0, 2.5 mi), intersect with the
   Seattle-clipped block groups, and apply area-weighted population
   attribution: if X% of a block group's land area overlaps the walkshed,
   attribute X% of its population to walkshed coverage.
6. Sum across block groups → population within walkshed.
7. Divide by Seattle total population → coverage %.

Inputs:
  data/walkshed/ola_isochrones.geojson  (from compute_walkshed.py)

Outputs:
  data/walkshed/population_coverage.csv — per-distance coverage %
  data/walkshed/seattle_block_groups.geojson — BGs clipped to Seattle (for reuse)

Usage: .venv/bin/python3 scripts/population_coverage.py

Dependencies: pygris, geopandas, shapely, pandas, requests.
CENSUS API KEY is optional but recommended for higher rate limits; set via
CENSUS_API_KEY env var. Without a key, pygris can still fetch geometries;
population data comes from the decennial API which works without a key for
small queries.

Projections: all spatial math done in EPSG:32610 (UTM zone 10N, meters).
GeoJSON output is EPSG:4326 per the GeoJSON spec.

Caveats:
- Area-weighted attribution assumes population is uniformly distributed
  within each block group. For Seattle at block-group granularity (~1,500
  residents per BG, typically 4-10 city blocks), this is a reasonable
  approximation but does introduce small error for BGs with concentrated
  housing or large non-residential tracts. A dasymetric refinement using
  land-use or building-footprint data would be more precise.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.ops import unary_union

import pygris

REPO_ROOT = Path(__file__).resolve().parent.parent
ISOCHRONE_GEOJSON = REPO_ROOT / "data" / "walkshed" / "ola_isochrones.geojson"
OUT_DIR = REPO_ROOT / "data" / "walkshed"
OUT_COVERAGE = OUT_DIR / "population_coverage.csv"
OUT_BGS = OUT_DIR / "seattle_block_groups.geojson"

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY", "")

# 2020 Decennial P1: total population
# Docs: https://api.census.gov/data/2020/dec/pl/variables.html
CENSUS_API_URL = (
    "https://api.census.gov/data/2020/dec/pl"
    "?get=NAME,P1_001N"
    "&for=block%20group:*"
    "&in=state:53%20county:033"
)

# CRS for distance/area operations — UTM zone 10N covers western Washington.
METRIC_CRS = "EPSG:32610"


def load_union_walksheds() -> dict[str, gpd.GeoDataFrame]:
    """Return {distance_label: GeoDataFrame-of-one-union-polygon} in metric CRS."""
    if not ISOCHRONE_GEOJSON.exists():
        raise SystemExit(
            f"Missing {ISOCHRONE_GEOJSON}. Run scripts/compute_walkshed.py first."
        )
    raw = json.loads(ISOCHRONE_GEOJSON.read_text())
    unions: dict[str, gpd.GeoDataFrame] = {}
    for feat in raw["features"]:
        if feat["properties"].get("ola") != "__UNION_ALL_OLAS__":
            continue
        label = feat["properties"]["distance"]
        geom = shape(feat["geometry"])
        gdf = gpd.GeoDataFrame([{"distance": label}], geometry=[geom], crs="EPSG:4326")
        unions[label] = gdf.to_crs(METRIC_CRS)
    if not unions:
        raise SystemExit("No union features found in isochrone GeoJSON.")
    return unions


def fetch_seattle_boundary() -> gpd.GeoDataFrame:
    """Seattle city boundary from Census TIGER Places (2020)."""
    print("Fetching Seattle city boundary (TIGER Places)...")
    places = pygris.places(state="WA", year=2020, cache=False)
    seattle = places[places["NAME"] == "Seattle"]
    if seattle.empty:
        raise SystemExit("Seattle boundary not found in Places layer.")
    seattle_m = seattle.to_crs(METRIC_CRS)
    area_sqkm = float(seattle_m.geometry.area.sum()) / 1_000_000
    print(f"  Seattle boundary: {area_sqkm:.2f} sq km")
    return seattle_m


def fetch_king_county_block_groups() -> gpd.GeoDataFrame:
    """Block-group geometries for King County (FIPS 033) in Washington (FIPS 53)."""
    print("Fetching King County block-group geometries (TIGER 2020)...")
    bgs = pygris.block_groups(state="WA", county="King", year=2020, cache=False)
    bgs_m = bgs.to_crs(METRIC_CRS)
    # pygris returns GEOID (12-char block-group identifier) + geometry + etc.
    print(f"  {len(bgs_m)} block groups loaded for King County")
    return bgs_m[["GEOID", "geometry"]]


def fetch_block_group_populations() -> pd.DataFrame:
    """2020 Decennial P1_001N (total population) for King County block groups."""
    print("Fetching 2020 Decennial block-group populations from Census API...")
    url = CENSUS_API_URL
    if CENSUS_API_KEY:
        url += f"&key={CENSUS_API_KEY}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    header, rows = data[0], data[1:]
    df = pd.DataFrame(rows, columns=header)
    df["P1_001N"] = pd.to_numeric(df["P1_001N"])
    # GEOID = state + county + tract + block_group (12 chars)
    df["GEOID"] = df["state"] + df["county"] + df["tract"] + df["block group"]
    df = df[["GEOID", "P1_001N"]].rename(columns={"P1_001N": "population"})
    print(f"  {len(df)} population rows")
    return df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load walkshed unions
    walksheds = load_union_walksheds()
    print(f"Loaded walkshed unions: {list(walksheds.keys())}")

    # 2. Seattle boundary
    seattle = fetch_seattle_boundary()

    # 3. King County BGs + populations
    bgs_geom = fetch_king_county_block_groups()
    pops = fetch_block_group_populations()
    bgs = bgs_geom.merge(pops, on="GEOID", how="left")
    bgs["population"] = bgs["population"].fillna(0).astype(int)

    # 4. Clip to Seattle: BGs whose area intersects Seattle get their intersecting
    #    portion only. Need to attribute population proportionally.
    print("Clipping block groups to Seattle boundary...")
    bgs["area_total"] = bgs.geometry.area
    seattle_union = seattle.geometry.union_all()
    clipped_geom = bgs.geometry.intersection(seattle_union)
    bgs["geom_in_seattle"] = clipped_geom
    bgs["area_in_seattle"] = clipped_geom.area
    # Drop BGs with no overlap
    bgs_seattle = bgs[bgs["area_in_seattle"] > 0].copy()
    bgs_seattle["fraction_in_seattle"] = bgs_seattle["area_in_seattle"] / bgs_seattle["area_total"]
    bgs_seattle["pop_in_seattle"] = bgs_seattle["population"] * bgs_seattle["fraction_in_seattle"]
    total_pop = float(bgs_seattle["pop_in_seattle"].sum())
    print(f"  {len(bgs_seattle)} BGs intersect Seattle; est. population = {total_pop:,.0f}")

    # 5. For each walkshed, area-weighted population
    print("\nComputing population coverage per walkshed distance:")
    rows: list[dict] = []
    for label, wgdf in walksheds.items():
        w_union = wgdf.geometry.union_all()
        # Intersect each BG's Seattle-clipped geometry with the walkshed
        inter = bgs_seattle["geom_in_seattle"].intersection(w_union)
        inter_area = inter.area
        frac_in_walkshed = (inter_area / bgs_seattle["area_in_seattle"]).fillna(0)
        pop_in_walkshed = (bgs_seattle["pop_in_seattle"] * frac_in_walkshed).sum()
        pct = pop_in_walkshed / total_pop * 100
        rows.append({
            "distance": label,
            "walkshed_area_sqkm": round(float(w_union.area) / 1_000_000, 3),
            "seattle_area_sqkm": round(float(seattle_union.area) / 1_000_000, 3),
            "area_coverage_pct": round(float(w_union.area) / float(seattle_union.area) * 100, 2),
            "population_total": int(total_pop),
            "population_in_walkshed": int(pop_in_walkshed),
            "population_coverage_pct": round(float(pct), 2),
        })
        print(
            f"  {label:>6s}: {pop_in_walkshed:>9,.0f} / {total_pop:>9,.0f} residents "
            f"= {pct:5.2f}% (area-only = "
            f"{float(w_union.area)/float(seattle_union.area)*100:5.2f}%)"
        )

    # 6. Write outputs
    with OUT_COVERAGE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {OUT_COVERAGE.relative_to(REPO_ROOT)}")

    # Export Seattle-clipped block groups (4326) for reuse
    bgs_out = bgs_seattle.copy()
    bgs_out["geometry"] = bgs_out["geom_in_seattle"]
    bgs_out = bgs_out.set_geometry("geometry")
    bgs_out = bgs_out[["GEOID", "population", "pop_in_seattle", "area_in_seattle", "geometry"]]
    bgs_out = bgs_out.to_crs("EPSG:4326")
    bgs_out.to_file(OUT_BGS, driver="GeoJSON")
    print(f"Wrote {OUT_BGS.relative_to(REPO_ROOT)} ({len(bgs_out)} BGs)")


if __name__ == "__main__":
    main()

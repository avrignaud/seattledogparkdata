#!/usr/bin/env python3
"""
Cross-tabulate enforcement citations against OLA walksheds.

Reproduces the headline "76.2% of geocoded park-named citations fall outside
any OLA's 0.5-mi walkshed" statistic on Part II Finding 02b and in the print
PDF, and writes the supporting CSV.

Method (point-in-polygon, explicit classification rule):
  1. Load data/walkshed/ola_isochrones.geojson (output of compute_walkshed.py).
  2. Union all per-OLA 0.5-mile isochrone polygons into a single geometry.
  3. Aggregate data/enforcement-citations.csv by location_canon, keeping only
     rows with location_type == 'park_named' (4,020 of 4,803 citations).
  4. For each uniquely-named park, look up its lat/lng in
     data/park-coordinates.csv.
  5. Count the park as "inside walkshed" iff the UNION geometry.contains()
     that single point. No buffer, no tolerance, no BG centroids.
  6. Sum citations per category.

The 672 street-address-only rows and 111 unknown-location rows are excluded
from this classification (they are flagged in enforcement-citations.csv via
the location_type column); filling those in would likely push the outside-
walkshed share up, since street addresses are definitionally not inside a
park polygon.

Input:  data/walkshed/ola_isochrones.geojson
        data/enforcement-citations.csv
        data/park-coordinates.csv
Output: data/walkshed/citation-rate-by-walkshed-status.csv

Usage: .venv/bin/python3 scripts/citation_walkshed_analysis.py
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

REPO_ROOT = Path(__file__).resolve().parent.parent
ISO_PATH = REPO_ROOT / "data/walkshed/ola_isochrones.geojson"
CITS_PATH = REPO_ROOT / "data/enforcement-citations.csv"
PARKS_PATH = REPO_ROOT / "data/park-coordinates.csv"
OUT_PATH = REPO_ROOT / "data/walkshed/citation-rate-by-walkshed-status.csv"


def main() -> None:
    iso = gpd.read_file(ISO_PATH)
    iso05 = iso[iso["distance"] == "0.5mi"]
    # Drop the pre-computed union feature if the geojson carries one;
    # we rebuild it here so the result is script-reproducible end-to-end.
    iso05 = iso05[iso05["ola"] != "__UNION_ALL_OLAS__"]
    union05 = iso05.geometry.union_all()
    print(f"OLA 0.5-mi isochrones loaded: {len(iso05)} polygons")

    cits = pd.read_csv(CITS_PATH)
    parks = pd.read_csv(PARKS_PATH)
    park_coords = dict(
        zip(parks["park_name"], zip(parks["latitude"], parks["longitude"]))
    )
    print(f"Citations: {len(cits):,} rows "
          f"({(cits['location_type']=='park_named').sum()} park-named, "
          f"{(cits['location_type']=='street_address').sum()} street, "
          f"{(cits['location_type']=='unknown').sum()} unknown)")

    # Count citations per canonical park name, keeping only park-named rows
    park_counts = Counter(
        r["location_canon"]
        for _, r in cits.iterrows()
        if r["location_type"] == "park_named"
    )

    inside_parks: list[tuple[str, int]] = []
    outside_parks: list[tuple[str, int]] = []
    inside_cits = outside_cits = unmatched_cits = 0

    for park, count in park_counts.items():
        if park not in park_coords:
            unmatched_cits += count
            continue
        lat, lng = park_coords[park]
        pt = Point(lng, lat)
        if union05.contains(pt):
            inside_parks.append((park, count))
            inside_cits += count
        else:
            outside_parks.append((park, count))
            outside_cits += count

    total_placed = inside_cits + outside_cits
    total_cits = len(cits)
    print(f"\nPark-named citations placed: {total_placed:,} "
          f"(of {total_cits:,} total = {total_placed/total_cits*100:.1f}%)")
    print(f"  Inside 0.5-mi walkshed:  {inside_cits:>5} "
          f"({inside_cits/total_placed*100:.1f}%)  [{len(inside_parks)} parks]")
    print(f"  Outside 0.5-mi walkshed: {outside_cits:>5} "
          f"({outside_cits/total_placed*100:.1f}%)  [{len(outside_parks)} parks]")
    if unmatched_cits:
        print(f"  Canon-named but no park-coord row: {unmatched_cits}")

    print("\nParks inside walkshed (sorted by citation count):")
    for p, c in sorted(inside_parks, key=lambda x: -x[1]):
        print(f"  {c:>4}  {p}")

    # Write the authoritative summary CSV
    with open(OUT_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "walkshed_status", "n_parks", "total_citations_2014_2019",
            "share_of_placed_citations",
        ])
        w.writerow([
            "Inside 0.5-mi OLA walkshed", len(inside_parks), inside_cits,
            f"{inside_cits/total_placed*100:.1f}%",
        ])
        w.writerow([
            "Outside 0.5-mi OLA walkshed", len(outside_parks), outside_cits,
            f"{outside_cits/total_placed*100:.1f}%",
        ])
    print(f"\nWrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

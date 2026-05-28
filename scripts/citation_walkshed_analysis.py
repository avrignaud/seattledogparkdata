#!/usr/bin/env python3
"""
Cross-tabulate enforcement citations against OLA walksheds.

Reproduces the two headline statistics cited on Part II Finding 02b and in
the print PDF, and writes the supporting CSV:

  * Park-named-only: share of park-named citations whose canonical park
    sits outside the union of 0.5-mi OLA walksheds.
  * Combined: same, plus street-address citations geocoded point-in-polygon
    via scripts/geocode_street_addresses.py.

Method (point-in-polygon, explicit classification rule):
  1. Load data/walkshed/ola_isochrones.geojson (output of compute_walkshed.py).
  2. Union all per-OLA 0.5-mile isochrone polygons into a single geometry.
  3. Park-named pass: aggregate data/enforcement-citations.csv by
     location_canon, keeping only rows with location_type == 'park_named'.
     For each uniquely-named park, look up its lat/lng in
     data/park-coordinates.csv — OLA host parks use the authoritative SPR
     ArcGIS OLA point so the lookup aligns with the walkshed seed — and
     test whether the UNION geometry.contains() that single point.
  4. Combined pass: also include location_type == 'street_address' rows,
     using data/walkshed/street-address-geocodes.csv (produced by the
     companion geocode_street_addresses.py script, 449/481 unique
     addresses geocoded via the Census Bureau's batch geocoder at last
     run, or rerun it to refresh).
  5. Sum citations per category and emit both headlines.

Input:  data/walkshed/ola_isochrones.geojson
        data/enforcement-citations.csv
        data/park-coordinates.csv
        data/walkshed/street-address-geocodes.csv
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
GEOCODE_PATH = REPO_ROOT / "data/walkshed/street-address-geocodes.csv"
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
    # DLP-only, to match the enforcement page's "Dog Loose in Park" framing and
    # the original analysis (C049204 was DLP-only by construction). Without this
    # filter the post-C263949 dataset would mix in license/scoop/other-category
    # citations and inflate the placed counts.
    before = len(cits)
    cits = cits[cits["dlp_only"].astype(str) == "True"].copy()
    print(f"Filtered to DLP-only: {len(cits):,} of {before:,} rows")
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

    # Combined pass: also include geocoded street-address citations.
    addr_pt: dict[str, tuple[float, float]] = {}
    if GEOCODE_PATH.exists():
        with open(GEOCODE_PATH) as f:
            for r in csv.DictReader(f):
                if r.get("lat") and r.get("lng"):
                    try:
                        addr_pt[r["location_raw"]] = (float(r["lat"]), float(r["lng"]))
                    except ValueError:
                        pass

    st_inside = st_outside = st_nogeo = 0
    for _, r in cits.iterrows():
        if r["location_type"] != "street_address":
            continue
        canon = (r.get("location_canon") or "").strip()
        pt_ll = addr_pt.get(canon)
        if pt_ll is None:
            st_nogeo += 1
            continue
        lat, lng = pt_ll
        if union05.contains(Point(lng, lat)):
            st_inside += 1
        else:
            st_outside += 1

    combined_in = inside_cits + st_inside
    combined_out = outside_cits + st_outside
    combined_tot = combined_in + combined_out
    print(
        f"\nCombined (park-named + geocoded street addresses): "
        f"inside={combined_in}, outside={combined_out}, "
        f"total={combined_tot}, outside={combined_out/combined_tot*100:.1f}%"
    )
    print(f"  Street-address citations with no geocode match: {st_nogeo}")

    # Write the authoritative summary CSV: both passes, one row each.
    with open(OUT_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "walkshed_status", "pass", "n_parks_or_addrs",
            "total_citations", "share_of_placed_citations",
        ])
        w.writerow([
            "Inside 0.5-mi OLA walkshed", "park-named",
            len(inside_parks), inside_cits,
            f"{inside_cits/total_placed*100:.1f}%",
        ])
        w.writerow([
            "Outside 0.5-mi OLA walkshed", "park-named",
            len(outside_parks), outside_cits,
            f"{outside_cits/total_placed*100:.1f}%",
        ])
        w.writerow([
            "Inside 0.5-mi OLA walkshed", "combined",
            "", combined_in,
            f"{combined_in/combined_tot*100:.1f}%",
        ])
        w.writerow([
            "Outside 0.5-mi OLA walkshed", "combined",
            "", combined_out,
            f"{combined_out/combined_tot*100:.1f}%",
        ])
    print(f"\nWrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

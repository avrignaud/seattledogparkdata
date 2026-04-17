#!/usr/bin/env python3
"""
Compute proper network walksheds (isochrones) around each Seattle OLA.

Produces three 0.5-, 1.0-, and 2.5-mile isochrones per OLA using the walkable
road network from OpenStreetMap (via osmnx). Saves as GeoJSON and a coverage
summary CSV.

The 0.5-mile (~10-minute walk) figure is Trust for Public Land's industry
standard and is directly comparable to the 99% "any park" walkshed TPL cites
for Seattle. The 2.5-mile isochrone replicates SPR's published OLA access
standard from the People, Dogs and Parks Strategic Plan for side-by-side
comparison.

Input:  data/seattle-olas.csv — existing 14 OLAs with coordinates
Output: data/walkshed/ola_isochrones.geojson — one MultiPolygon per OLA per distance
        data/walkshed/ola_walkshed_coverage.csv — union-area coverage stats

Usage: .venv/bin/python3 scripts/compute_walkshed.py

Dependencies: osmnx, geopandas, shapely, pandas. Install:
    python3 -m venv .venv && .venv/bin/pip install osmnx geopandas shapely pandas

Runtime: ~2–5 minutes depending on network speed; osmnx downloads Seattle's
walkable OSM network on first run and caches it.

Methodology:
1. Load walkable road network for Seattle (city bbox).
2. For each OLA: project to nearest network node.
3. Use osmnx.routing.ego_graph_networkx equivalent — traverse network within
   a given walking distance (computed in meters). 0.5 mi = 804.67 m;
   1.0 mi = 1609.34 m; 2.5 mi = 4023.36 m.
4. Build a convex hull (or alpha-shape) of reachable nodes → isochrone polygon.
5. Union all 14 OLA isochrones per distance → total city coverage.
6. Report total coverage area and (if census data is supplied) population.

Caveats:
- Isochrones are built from the convex hull of reachable nodes, which
  slightly overestimates reachable area compared to a true alpha-shape.
- Walking speed is assumed constant; does not model elevation. Seattle's
  hills would reduce real-world walkability further.
- Physical barriers (I-5, Ship Canal) are respected because the walkable
  road network doesn't cross them without bridges.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import geopandas as gpd
import networkx as nx
import osmnx as ox
import pandas as pd
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union

REPO_ROOT = Path(__file__).resolve().parent.parent
OLA_CSV = REPO_ROOT / "data" / "seattle-olas.csv"
OUT_DIR = REPO_ROOT / "data" / "walkshed"
OUT_GEOJSON = OUT_DIR / "ola_isochrones.geojson"
OUT_COVERAGE = OUT_DIR / "ola_walkshed_coverage.csv"

# Walking distance thresholds in meters.
# 0.5 mi = TPL industry standard (10-minute walk)
# 1.0 mi = intermediate reference
# 2.5 mi = SPR's published standard from People, Dogs and Parks Plan
DISTANCES_M = {
    "0.5mi": 804.67,
    "1.0mi": 1609.34,
    "2.5mi": 4023.36,
}

# Seattle bounding box for the OSM network fetch. (north, south, east, west)
# Wide enough to contain the full 2.5-mile walkshed around every OLA.
SEATTLE_BBOX = (47.80, 47.40, -122.20, -122.50)  # (N, S, E, W)


def load_olas() -> pd.DataFrame:
    df = pd.read_csv(OLA_CSV)
    # seattle-olas.csv columns: ola_name, latitude, longitude, acres, neighborhood, ...
    need = {"ola_name", "latitude", "longitude"}
    missing = need - set(df.columns)
    if missing:
        raise RuntimeError(f"{OLA_CSV} missing columns: {missing}")
    df = df[df["latitude"].notna() & df["longitude"].notna()].copy()
    return df


def isochrone_polygon(G: nx.MultiDiGraph, center_node: int, distance_m: float) -> Polygon | MultiPolygon | None:
    """Return the convex hull of all nodes reachable within `distance_m` from center_node."""
    # ego_graph using the 'length' attribute (meters) as the weight
    sub = nx.ego_graph(G, center_node, radius=distance_m, distance="length")
    if len(sub) < 3:
        return None
    # Collect point geometries for reachable nodes
    xs = [G.nodes[n]["x"] for n in sub.nodes]
    ys = [G.nodes[n]["y"] for n in sub.nodes]
    points = gpd.GeoSeries([Point(x, y) for x, y in zip(xs, ys)], crs="EPSG:4326")
    hull = points.union_all().convex_hull
    return hull


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    olas = load_olas()
    print(f"Loaded {len(olas)} OLAs from {OLA_CSV.relative_to(REPO_ROOT)}")

    # Download the walkable Seattle network. Cached in osmnx's cache dir after first run.
    print("Fetching Seattle walkable road network from OSM (cached after first run)...")
    ox.settings.use_cache = True
    ox.settings.log_console = False
    # network_type='walk' gives us the pedestrian network with sidewalks, paths, etc.
    # Use graph_from_place which is simpler and more reliable in osmnx 2.x than bbox.
    G = ox.graph_from_place(
        "Seattle, Washington, USA",
        network_type="walk",
        simplify=True,
    )
    # Ensure each edge has a 'length' attribute in meters (osmnx adds this by default)
    edges_data = list(G.edges(data=True))
    if edges_data and "length" not in edges_data[0][2]:
        G = ox.distance.add_edge_lengths(G)
    print(f"Network: {len(G.nodes)} nodes, {len(G.edges)} edges")

    # Project to UTM. nearest_nodes on an unprojected graph would require scikit-learn;
    # projected graphs use simple euclidean distance and are more accurate anyway.
    print("Projecting graph to UTM zone 10N (EPSG:32610)...")
    G_proj = ox.project_graph(G, to_crs="EPSG:32610")

    features: list[dict] = []
    coverage_rows: list[dict] = []

    # Pre-project OLA points to match the projected graph CRS (EPSG:32610)
    ola_points_4326 = gpd.GeoSeries(
        [Point(float(r["longitude"]), float(r["latitude"])) for _, r in olas.iterrows()],
        crs="EPSG:4326",
    )
    ola_points_proj = ola_points_4326.to_crs("EPSG:32610")

    for idx, (_, ola) in enumerate(olas.iterrows()):
        name = ola["ola_name"]
        lat = float(ola["latitude"])
        lng = float(ola["longitude"])
        pt_proj = ola_points_proj.iloc[idx]
        try:
            center_node = ox.distance.nearest_nodes(G_proj, X=pt_proj.x, Y=pt_proj.y)
        except Exception as e:
            print(f"  ! {name}: could not find nearest node — {e}")
            continue

        for label, dist_m in DISTANCES_M.items():
            poly = isochrone_polygon(G_proj, center_node, dist_m)
            if poly is None or poly.is_empty:
                continue
            # poly is in EPSG:32610 (meters); convert back to WGS84 for GeoJSON output
            poly_4326 = gpd.GeoSeries([poly], crs="EPSG:32610").to_crs("EPSG:4326").iloc[0]
            area_sqkm = gpd.GeoSeries([poly], crs="EPSG:32610").area.iloc[0] / 1_000_000
            poly = poly_4326  # replace with the 4326 version for downstream GeoJSON + union
            features.append({
                "type": "Feature",
                "geometry": poly.__geo_interface__,
                "properties": {
                    "ola": name,
                    "distance": label,
                    "distance_meters": dist_m,
                    "center_lat": lat,
                    "center_lng": lng,
                    "area_sqkm": round(area_sqkm, 3),
                },
            })
            coverage_rows.append({
                "ola": name,
                "distance": label,
                "area_sqkm": round(area_sqkm, 3),
                "center_lat": lat,
                "center_lng": lng,
            })
            print(f"  {name:25s} {label:>6s}: {area_sqkm:6.3f} sq km")

    # Union-per-distance for total coverage
    for label in DISTANCES_M:
        polys = [
            Polygon(feat["geometry"]["coordinates"][0]) if feat["geometry"]["type"] == "Polygon"
            else MultiPolygon([Polygon(p[0]) for p in feat["geometry"]["coordinates"]])
            for feat in features
            if feat["properties"]["distance"] == label
        ]
        if not polys:
            continue
        merged = unary_union(polys)
        area_sqkm = gpd.GeoSeries([merged], crs="EPSG:4326").to_crs(epsg=32610).area.iloc[0] / 1_000_000
        features.append({
            "type": "Feature",
            "geometry": merged.__geo_interface__,
            "properties": {
                "ola": "__UNION_ALL_OLAS__",
                "distance": label,
                "area_sqkm": round(area_sqkm, 3),
            },
        })
        coverage_rows.append({
            "ola": "__UNION_ALL_OLAS__",
            "distance": label,
            "area_sqkm": round(area_sqkm, 3),
            "center_lat": "",
            "center_lng": "",
        })
        print(f"  {'UNION 14 OLAs':25s} {label:>6s}: {area_sqkm:6.3f} sq km")

    # Seattle total land area ≈ 217 sq km (83.9 sq mi)
    SEATTLE_SQKM = 217.0
    print()
    print("Coverage summary (OLA-union walkshed / Seattle total area):")
    for row in coverage_rows:
        if row["ola"] == "__UNION_ALL_OLAS__":
            pct = row["area_sqkm"] / SEATTLE_SQKM * 100
            print(f"  {row['distance']:>6s}: {row['area_sqkm']:7.2f} / {SEATTLE_SQKM:.1f} sq km = {pct:5.2f}%")

    # Write GeoJSON
    geojson = {"type": "FeatureCollection", "features": features}
    OUT_GEOJSON.write_text(json.dumps(geojson, separators=(",", ":")))
    print(f"\nWrote {OUT_GEOJSON.relative_to(REPO_ROOT)}  ({len(features)} features)")

    # Write coverage CSV
    with OUT_COVERAGE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["ola", "distance", "area_sqkm", "center_lat", "center_lng"])
        writer.writeheader()
        writer.writerows(coverage_rows)
    print(f"Wrote {OUT_COVERAGE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

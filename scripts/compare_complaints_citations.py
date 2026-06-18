#!/usr/bin/env python3
"""
Compare Find It Fix It "Nuisance Dogs in a Park" complaints (PRR C263990) against
Animal Control off-leash citations (PRRs C049204 + C263949), in the overlapping
window where both exist (2024-2026).

Two questions:
  1. Spatial — do the same parks generate complaints and citations?
  2. Temporal — does complaint volume track citation volume month to month?

Method
------
Complaints carry lat/lon -> point-in-polygon against the TPL ParkServe Seattle
park-boundary layer to assign each to a park.

Citations: the 2024-2026 records (C263949) are already *park-named*
(location_type == 'park_named'), so they are reconciled to ParkServe names by
string normalization + a small alias table — no geocoding needed. The handful of
street-address citations in the window are placed via the existing geocode lookup
(data/walkshed/street-address-geocodes.csv) and the same polygon join.

Only dog-loose-in-park citations are counted (dlp_only / violation_category) so the
comparison is apples-to-apples with the dog-specific complaint type.

Outputs (with provenance columns, repo convention):
  data/complaints-vs-citations-by-park.csv   one row per park, overlap window
  data/complaints-citations-monthly.csv      monthly complaint & citation counts

Usage: .venv/bin/python3 scripts/compare_complaints_citations.py
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

REPO = Path(__file__).resolve().parent.parent
COMPLAINTS = REPO / "data/prr-responses/C263990/Customer_Service_Requests_NuisanceDogsInAPark_2024-2026.csv"
CITATIONS = REPO / "data/enforcement-citations.csv"
GEOCODES = REPO / "data/walkshed/street-address-geocodes.csv"
PARKS_SHP = REPO / "data/ParkScore_2025_DataDownloads_shapefiles05212025/data/ParkServe_Parks.shp"
OUT_PARK = REPO / "data/complaints-vs-citations-by-park.csv"
OUT_MONTH = REPO / "data/complaints-citations-monthly.csv"

OVERLAP_START_YEAR = 2024

# ParkServe names that string-normalization alone misses.
ALIAS = {
    "Magnuson Park": "WARREN G. MAGNUSON PARK",
    "Miller Playfield": "PENDLETON MILLER PLAYFIELD",
    "Jefferson Playield": "JEFFERSON PARK",  # sic, source typo
    "Interbay Athletic Complex": "INTERBAY ATHLETIC COMPLEX",
}
_STOP = r"\b(park|playfield|playground|and|the|reserve|preserve|athletic|complex|field|fields)\b"


def norm(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    s = re.sub(_STOP, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_complaint_date(d: str):
    try:
        return datetime.strptime(d, "%m/%d/%Y %I:%M:%S %p")
    except ValueError:
        return None


def parse_citation_date(d: str):
    try:
        return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


# Seattle city bounding box (WGS84). The ParkServe "Seattle, WA" urban area is much
# larger than the city and contains duplicate park names (a "Volunteer Park" near Gig
# Harbor, a "Lincoln Park" in Tacoma, etc.). Clip to the city so name matches and
# centroids resolve to the right polygon. west, south, east, north:
SEA_BBOX = (-122.47, 47.48, -122.22, 47.75)


def load_seattle_parks() -> gpd.GeoDataFrame:
    g = gpd.read_file(PARKS_SHP)
    sea = g[g["Park_State"] == "Washington"].copy()
    mask = sea["Park_Urban"].astype(str).str.contains("Seattle", na=False) | sea[
        "Park_Place"
    ].astype(str).str.contains("Seattle", na=False)
    sea = sea[mask]
    sea = sea[sea["Park_Name"].notna()].copy()
    sea["geometry"] = sea.geometry.buffer(0)  # repair invalid rings
    # Clip to Seattle city bbox by centroid to drop out-of-city same-name duplicates.
    cen = sea.geometry.to_crs("EPSG:4326").centroid
    w, s, e, n = SEA_BBOX
    keep = (cen.x >= w) & (cen.x <= e) & (cen.y >= s) & (cen.y <= n)
    sea = sea[keep.values].copy()
    return sea


def join_points_to_parks(pts, sea) -> Counter:
    if not pts:
        return Counter()
    gp = gpd.GeoDataFrame(
        geometry=[Point(lon, lat) for lon, lat in pts], crs="EPSG:4326"
    ).to_crs(sea.crs)
    j = gpd.sjoin(gp, sea[["Park_Name", "geometry"]], how="left", predicate="within")
    return Counter(j["Park_Name"].dropna())


def build_park_matcher(sea):
    names = set(sea["Park_Name"])
    ps_norm = {}
    for n in names:
        ps_norm.setdefault(norm(n), n)

    def match(name: str):
        if name in ALIAS and ALIAS[name] in names:
            return ALIAS[name]
        if name in names:
            return name
        n = norm(name)
        if n in ps_norm:
            return ps_norm[n]
        cands = [psn for pn, psn in ps_norm.items() if n and (n in pn or pn in n) and abs(len(pn) - len(n)) <= 8]
        if cands:
            return min(cands, key=lambda x: abs(len(norm(x)) - len(n)))
        return None

    return match


def pearson(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    mx, my = sum(x) / n, sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = sum((a - mx) ** 2 for a in x) ** 0.5
    dy = sum((b - my) ** 2 for b in y) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0] * len(xs)
    for rk, i in enumerate(order):
        r[i] = rk
    return r


def main() -> None:
    sea = load_seattle_parks()
    match = build_park_matcher(sea)
    centroids = {
        r["Park_Name"]: (r.geometry.centroid.y, r.geometry.centroid.x)
        for _, r in sea.to_crs("EPSG:4326").iterrows()
    }

    # ---- Complaints ----
    com_pts, com_month = [], Counter()
    com_year = Counter()
    with open(COMPLAINTS) as f:
        for r in csv.DictReader(f):
            d = parse_complaint_date(r["Created Date"])
            if d:
                com_month[(d.year, d.month)] += 1
                com_year[d.year] += 1
            try:
                com_pts.append((float(r["Longitude"]), float(r["Latitude"])))
            except (ValueError, KeyError):
                pass
    comp_pk = join_points_to_parks(com_pts, sea)

    # ---- Citations (dog-loose-in-park only) ----
    geo = {}
    with open(GEOCODES) as f:
        for r in csv.DictReader(f):
            try:
                geo[r["location_raw"]] = (float(r["lat"]), float(r["lng"]))
            except ValueError:
                pass

    cit_month, cit_year = Counter(), Counter()
    cit_named, cit_street_pts = Counter(), []
    with open(CITATIONS) as f:
        for r in csv.DictReader(f):
            if not (r.get("dlp_only") == "True" or r.get("violation_category") == "dog_loose_in_park"):
                continue
            d = parse_citation_date(r["issued_at"])
            if not d:
                continue
            if d.year >= OVERLAP_START_YEAR:
                cit_month[(d.year, d.month)] += 1
                cit_year[d.year] += 1
                if r["location_type"] == "park_named":
                    cit_named[r["location_canon"].strip()] += 1
                else:
                    g = geo.get(r["location_canon"].strip())
                    if g:
                        cit_street_pts.append((g[1], g[0]))

    # fold street-address citations into the park counter via polygon join
    for name in join_points_to_parks(cit_street_pts, sea).elements():
        cit_named[name] += 1

    cit_pk, unmatched = Counter(), []
    for name, c in cit_named.items():
        m = match(name)
        if m:
            cit_pk[m] += c
        else:
            unmatched.append((name, c))

    matched = sum(cit_pk.values())
    print(f"Recent DLP citations matched to a park: {matched} "
          f"({100*matched/max(1,sum(cit_named.values())):.1f}%); "
          f"unmatched {sum(c for _, c in unmatched)} cites / {len(unmatched)} names")

    # ---- Per-park output ----
    parks = sorted(set(comp_pk) | set(cit_pk), key=lambda p: -(comp_pk.get(p, 0) + cit_pk.get(p, 0)))
    prov = ("calculated: complaints PRR C263990 (point-in-polygon vs ParkServe) "
            "vs DLP citations PRR C263949 (park-named), 2024-2026; "
            "scripts/compare_complaints_citations.py")
    with open(OUT_PARK, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["park", "complaints_2024_26", "citations_2024_26",
                    "complaint_citation_ratio", "latitude", "longitude", "provenance"])
        for p in parks:
            co, ci = comp_pk.get(p, 0), cit_pk.get(p, 0)
            lat, lon = centroids.get(p, ("", ""))
            ratio = round(co / ci, 2) if ci else ""
            w.writerow([p, co, ci, ratio,
                        round(lat, 6) if lat != "" else "", round(lon, 6) if lon != "" else "",
                        prov])
    print(f"Wrote {OUT_PARK.relative_to(REPO)} ({len(parks)} parks)")

    # ---- Monthly output ----
    months = sorted(k for k in set(com_month) | set(cit_month) if k >= (OVERLAP_START_YEAR, 1))
    prov_m = ("calculated: monthly counts, complaints PRR C263990 + DLP citations "
              "PRR C263949; scripts/compare_complaints_citations.py")
    with open(OUT_MONTH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "complaints", "dlp_citations", "provenance"])
        for y, m in months:
            w.writerow([f"{y}-{m:02d}", com_month[(y, m)], cit_month[(y, m)], prov_m])
    print(f"Wrote {OUT_MONTH.relative_to(REPO)} ({len(months)} months)")

    # ---- Correlations (printed, for the writeup) ----
    print("\nYearly:")
    for y in sorted(set(com_year) | set(cit_year)):
        print(f"  {y}: complaints={com_year[y]:>5}  dlp_citations={cit_year[y]:>4}")

    overlap_months = [k for k in months if k >= (2024, 4)]
    cm = [com_month[k] for k in overlap_months]
    cc = [cit_month[k] for k in overlap_months]
    print(f"\nTemporal: monthly complaint-citation Pearson r (n={len(cm)}): {pearson(cm, cc):.2f}")

    print("\nSpatial (overlap window, both via ParkServe):")
    for thr in (1, 5, 10):
        rows = [(comp_pk.get(p, 0), cit_pk.get(p, 0)) for p in (set(comp_pk) | set(cit_pk))
                if comp_pk.get(p, 0) + cit_pk.get(p, 0) >= thr]
        co = [r[0] for r in rows]
        ci = [r[1] for r in rows]
        print(f"  parks with >= {thr:>2} combined (n={len(rows):>3}): "
              f"Spearman {pearson(ranks(co), ranks(ci)):.2f}  Pearson {pearson(co, ci):.2f}")


if __name__ == "__main__":
    main()

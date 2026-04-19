#!/usr/bin/env python3
"""
Geocode the street-address-only citation rows.

Primary pass: Census Bureau batch geocoder (free, no API key,
batchable via CSV upload). Covers ~93% of the 481 unique addresses.

Fallback pass: Nominatim (OpenStreetMap) one-at-a-time for addresses
the Census pass couldn't resolve. Rate-limited to 1 request/second
per Nominatim's usage policy, with a descriptive User-Agent. Typical
fallback yield is another 5-7% of the total.

Takes every row in data/enforcement-citations.csv where
location_type == 'street_address' and writes results to:

    data/walkshed/street-address-geocodes.csv

Columns: location_raw, lat, lng, match_quality, census_geoid.

The main citation file is not mutated — downstream analyses join
by location_raw when they want to include these rows.

Rate limits: Census batch accepts up to 10,000 addresses per request.
Typical response time ~30-60 seconds per batch. Nominatim per its
ToU allows one request per second with proper User-Agent identifying
the application.

Usage: .venv/bin/python3 scripts/geocode_street_addresses.py
"""
from __future__ import annotations

import csv
import io
import sys
import time
from pathlib import Path
from typing import Iterable

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
CITS_PATH = REPO_ROOT / "data/enforcement-citations.csv"
OUT_PATH = REPO_ROOT / "data/walkshed/street-address-geocodes.csv"
CENSUS_URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
BENCHMARK = "Public_AR_Current"  # Most-recent street centerlines

# Nominatim fallback config.
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_UA = "seattledogparkdata.com citation-geocode script (contact: seattledogparkdata@ozymandi.as)"
# Seattle city bounding box — clips Nominatim results to city limits.
# Format: viewbox is west,north,east,south in WGS84.
SEATTLE_VIEWBOX = "-122.4596,47.7341,-122.2244,47.4810"


def unique_street_addresses() -> list[str]:
    addrs: set[str] = set()
    with open(CITS_PATH) as f:
        for r in csv.DictReader(f):
            if r.get("location_type") == "street_address":
                a = (r.get("location_canon") or "").strip()
                if a:
                    addrs.add(a)
    return sorted(addrs)


def build_batch_csv(addresses: Iterable[str]) -> bytes:
    """Census addressbatch CSV: Unique ID, Street, City, State, Zip (city/state/zip optional)."""
    buf = io.StringIO()
    w = csv.writer(buf)
    for i, addr in enumerate(addresses):
        # All addresses here are Seattle, WA (enforcement data is city-scoped).
        w.writerow([i, addr, "Seattle", "WA", ""])
    return buf.getvalue().encode("utf-8")


def post_batch(batch: bytes) -> str:
    files = {"addressFile": ("batch.csv", batch, "text/csv")}
    data = {"benchmark": BENCHMARK}
    r = requests.post(CENSUS_URL, files=files, data=data, timeout=300)
    r.raise_for_status()
    return r.text


def parse_response(text: str) -> dict[int, dict]:
    """Response is CSV keyed by our submitted row ID (column 0).
    Columns: ID, input_address, match_status, match_type,
    matched_address, longitude,latitude, tigerlineid, side."""
    results: dict[int, dict] = {}
    reader = csv.reader(io.StringIO(text))
    for row in reader:
        if len(row) < 3:
            continue
        try:
            rid = int(row[0])
        except ValueError:
            continue
        status = row[2] if len(row) > 2 else ""
        match_type = row[3] if len(row) > 3 else ""
        if status != "Match":
            results[rid] = {"lat": None, "lng": None, "quality": status, "census_geoid": ""}
            continue
        coord = row[5] if len(row) > 5 else ""
        lat, lng = None, None
        if "," in coord:
            lng_s, lat_s = coord.split(",", 1)
            try:
                lng, lat = float(lng_s), float(lat_s)
            except ValueError:
                pass
        tigerline = row[7] if len(row) > 7 else ""
        results[rid] = {
            "lat": lat, "lng": lng, "quality": match_type or "Match",
            "census_geoid": tigerline,
        }
    return results


def nominatim_lookup(addr: str) -> dict:
    """Single-address Nominatim lookup, scoped to Seattle city limits.
    Returns {lat, lng, quality} or {None, None, 'NoResponse'}.
    Caller is responsible for the 1-second rate-limit sleep between calls."""
    params = {
        "q": f"{addr}, Seattle, WA",
        "format": "json",
        "limit": "1",
        "viewbox": SEATTLE_VIEWBOX,
        "bounded": "1",
        "countrycodes": "us",
    }
    try:
        r = requests.get(
            NOMINATIM_URL,
            params=params,
            headers={"User-Agent": NOMINATIM_UA},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
    except Exception:
        return {"lat": None, "lng": None, "quality": "NoResponse", "census_geoid": ""}
    if not data:
        return {"lat": None, "lng": None, "quality": "Nominatim_NoMatch", "census_geoid": ""}
    hit = data[0]
    try:
        return {
            "lat": float(hit["lat"]),
            "lng": float(hit["lon"]),
            "quality": "Nominatim",
            "census_geoid": "",
        }
    except (KeyError, ValueError):
        return {"lat": None, "lng": None, "quality": "Nominatim_ParseError", "census_geoid": ""}


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    addrs = unique_street_addresses()
    print(f"Unique street addresses to geocode: {len(addrs)}")

    # ---- Pass 1: Census batch geocoder ----
    # Chunk into batches of 1,000 to stay well under the 10k limit. We
    # re-key each batch's response by the submitted row ID 0..N-1 and then
    # map back to the original address via `addrs` + offset.
    CHUNK = 1000
    addr_results: dict[str, dict] = {}
    for i in range(0, len(addrs), CHUNK):
        batch = addrs[i : i + CHUNK]
        print(f"Census batch {i // CHUNK + 1}: {len(batch)} addresses...")
        csv_bytes = build_batch_csv(batch)
        try:
            text = post_batch(csv_bytes)
        except Exception as e:
            print(f"  error: {e}", file=sys.stderr)
            raise
        batch_by_id = parse_response(text)
        for rid, rec in batch_by_id.items():
            if 0 <= rid < len(batch):
                addr_results[batch[rid]] = rec
        matched = sum(1 for v in batch_by_id.values() if v.get("lat") is not None)
        print(f"  Census matched {matched}/{len(batch)}")
        time.sleep(2)  # be polite

    census_matched = sum(1 for v in addr_results.values() if v.get("lat") is not None)
    print(f"\nCensus pass: {census_matched}/{len(addrs)} ({census_matched/len(addrs)*100:.1f}%)")

    # ---- Pass 2: Nominatim fallback on Census misses ----
    unresolved = [a for a in addrs if addr_results.get(a, {}).get("lat") is None]
    if unresolved:
        print(f"\nNominatim fallback on {len(unresolved)} unresolved addresses...")
        nom_hits = 0
        for i, addr in enumerate(unresolved, 1):
            rec = nominatim_lookup(addr)
            addr_results[addr] = rec
            if rec.get("lat") is not None:
                nom_hits += 1
            if i % 10 == 0 or i == len(unresolved):
                print(f"  {i}/{len(unresolved)} requested, {nom_hits} matched")
            time.sleep(1.1)  # Nominatim ToU: max 1 req/sec

        print(f"Nominatim pass: {nom_hits}/{len(unresolved)} ({nom_hits/len(unresolved)*100:.1f}%)")

    total_matched = sum(1 for v in addr_results.values() if v.get("lat") is not None)
    print(
        f"\nTotal: {total_matched}/{len(addrs)} "
        f"({total_matched/len(addrs)*100:.1f}%) unique addresses geocoded"
    )

    with open(OUT_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["location_raw", "lat", "lng", "match_quality", "census_geoid"])
        for addr in addrs:
            r = addr_results.get(addr, {})
            w.writerow([addr, r.get("lat") or "", r.get("lng") or "",
                        r.get("quality") or "NoResponse", r.get("census_geoid") or ""])
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

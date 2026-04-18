#!/usr/bin/env python3
"""
Geocode the street-address-only citation rows via the Census Bureau
geocoder (free, no API key, rate-limited but batchable via CSV upload).

Takes every row in data/enforcement-citations.csv where
location_type == 'street_address' (~672 rows, ~481 unique addresses),
submits them in batches to the Census Geocoder's addressbatch endpoint,
and writes results back as a new CSV:

    data/walkshed/street-address-geocodes.csv

Columns: location_raw, lat, lng, match_quality, census_geoid.

The main citation file is not mutated — downstream analyses can join
by location_raw when they want to include these rows.

Rate limits: Census batch accepts up to 10,000 addresses per request.
Typical response time ~30-60 seconds per batch; we submit one batch.

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


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    addrs = unique_street_addresses()
    print(f"Unique street addresses to geocode: {len(addrs)}")

    # Chunk into batches of 1,000 to stay well under the 10k limit. We
    # re-key each batch's response by the submitted row ID 0..N-1 and then
    # map back to the original address via `addrs` + offset.
    CHUNK = 1000
    addr_results: dict[str, dict] = {}
    for i in range(0, len(addrs), CHUNK):
        batch = addrs[i : i + CHUNK]
        print(f"Submitting batch {i // CHUNK + 1}: {len(batch)} addresses...")
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
        print(f"  matched {matched}/{len(batch)}")
        time.sleep(2)  # be polite

    matched = sum(1 for v in addr_results.values() if v.get("lat") is not None)
    print(f"\nMatched: {matched}/{len(addrs)} ({matched/len(addrs)*100:.1f}%)")

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

#!/usr/bin/env python3
"""
Reproduce summary aggregates from the Seattle Pet Licenses snapshot.

Input:  data/seattle-pet-licenses/Seattle-Pet-Licenses-<DATE>.csv
          (snapshot of Seattle Open Data dataset jguv-t9rb, current as
          of the filename date)
Output: data/seattle-pet-licenses/summary.csv
        data/seattle-pet-licenses/dogs-by-zip.csv
        data/seattle-pet-licenses/top-dog-breeds.csv

The analyses are trivial counts + group-bys — this script exists so
the aggregates on the site are reproducible from the committed
snapshot, not claims pulled from a one-off notebook.

Usage: .venv/bin/python3 scripts/analyze_pet_licenses.py
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data/seattle-pet-licenses"


def find_snapshot() -> Path:
    """Pick the newest Seattle-Pet-Licenses-YYYY-MM-DD.csv in DATA_DIR."""
    candidates = sorted(DATA_DIR.glob("Seattle-Pet-Licenses-*.csv"))
    if not candidates:
        raise SystemExit(
            f"No snapshot found in {DATA_DIR}. "
            "Refresh via curl per the directory README."
        )
    return candidates[-1]


def main() -> None:
    snapshot = find_snapshot()
    print(f"Reading {snapshot.relative_to(REPO_ROOT)}")

    species = Counter()
    dog_breeds = Counter()
    dog_zips = Counter()
    rows = 0

    with open(snapshot) as f:
        for r in csv.DictReader(f):
            rows += 1
            s = (r["Species"] or "").strip()
            species[s] += 1
            if s == "Dog":
                dog_breeds[r["Primary Breed"] or "(blank)"] += 1
                z = (r["ZIP Code"] or "").strip()[:5]
                if z.isdigit():
                    dog_zips[z] += 1

    print(f"  {rows:,} rows total")

    # --- summary.csv ---
    path = DATA_DIR / "summary.csv"
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["species", "count"])
        for k, v in species.most_common():
            w.writerow([k, v])
    print(f"Wrote {path.relative_to(REPO_ROOT)}")

    # --- dogs-by-zip.csv ---
    path = DATA_DIR / "dogs-by-zip.csv"
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zip_code", "active_dog_licenses"])
        for z, n in sorted(dog_zips.items(), key=lambda x: -x[1]):
            w.writerow([z, n])
    print(f"Wrote {path.relative_to(REPO_ROOT)}")

    # --- top-dog-breeds.csv ---
    path = DATA_DIR / "top-dog-breeds.csv"
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["primary_breed", "count", "share_of_licensed_dogs"])
        total_dogs = sum(dog_breeds.values())
        for breed, n in dog_breeds.most_common():
            w.writerow([breed, n, f"{n/total_dogs*100:.2f}%"])
    print(f"Wrote {path.relative_to(REPO_ROOT)}")

    print()
    print(f"Total licenses: {sum(species.values()):,}")
    print(f"  Dogs: {species.get('Dog', 0):,}")
    print(f"  Cats: {species.get('Cat', 0):,}")
    print(f"  Other: {sum(v for k, v in species.items() if k not in ('Dog', 'Cat')):,}")
    print(f"  Unique dog breeds: {len(dog_breeds):,}")
    print(f"  Unique ZIPs w/ dogs: {len(dog_zips):,}")


if __name__ == "__main__":
    main()

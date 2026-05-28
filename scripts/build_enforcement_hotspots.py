#!/usr/bin/env python3
"""
Build the two citation-hotspot CSVs that drive the Part II walkshed-citation map:

  data/enforcement-hotspots.csv        top-20 cited parks (DLP, 2014–2026)
  data/enforcement-hotspots-extra.csv  ranks 21–40

These were previously hand-maintained against the 2014–2019 C049204 slice. They
are now generated from scripts/enforcement_page_data.json (the same top-20/21-40
the enforcement page renders), so the Part II map stays in lockstep with the
enforcement page and the consolidated dataset.

Run from repo root:  .venv/bin/python scripts/build_enforcement_hotspots.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT / "scripts" / "enforcement_page_data.json"))
TOP = ROOT / "data" / "enforcement-hotspots.csv"
EXTRA = ROOT / "data" / "enforcement-hotspots-extra.csv"

PROV_TOP = ("calculated: enforcement-citations.csv top-20 DLP park-named, "
            "2014-2026 (PRRs C049204 + C263949)")
PROV_EXTRA = ("calculated: enforcement-citations.csv DLP park-named ranks 21-40, "
              "2014-2026 (PRRs C049204 + C263949)")


def main() -> None:
    with TOP.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["park", "count", "latitude", "longitude",
                    "neighborhood", "ola_status", "nearest_ola", "provenance"])
        for p in DATA["top20_full"]:
            w.writerow([p["park"], p["count"], p["lat"], p["lng"],
                        p.get("neighborhood", ""), p.get("ola_status", ""),
                        p.get("nearest_ola", "—"), PROV_TOP])

    with EXTRA.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["park", "count", "latitude", "longitude", "provenance"])
        for p in DATA["top21_40"]:
            w.writerow([p["park"], p["count"], p["lat"], p["lng"], PROV_EXTRA])

    print(f"Wrote {TOP.relative_to(ROOT)} ({len(DATA['top20_full'])} parks)")
    print(f"Wrote {EXTRA.relative_to(ROOT)} ({len(DATA['top21_40'])} parks)")


if __name__ == "__main__":
    main()

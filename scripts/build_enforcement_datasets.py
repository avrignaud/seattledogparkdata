#!/usr/bin/env python3
"""
Build the enforcement CSVs from the raw SPR public-records-request response.

Input:  data/prr-responses/C049204/*.xlsx
        Five Excel workbooks produced by Seattle Parks & Recreation in response
        to public records request C049204 (filed 2019-08-29, produced 2019-10-15).
        Each workbook contains four sheets — one per offense level — for a
        date range covering 2014-01-01 through 2019-10-15.

Output: data/enforcement-citations.csv
          One row per citation. Columns: year, offense_level, location_raw,
          location_canon, zip, issued_at, fee, case_result, source_file,
          source_sheet.
        data/enforcement-by-park-year.csv
          Aggregate. Columns: park, year, citations.

Usage:  cd <repo root> && python3 scripts/build_enforcement_datasets.py

Dependencies: openpyxl. Install in a venv:
    python3 -m venv .venv && .venv/bin/pip install openpyxl

Notes:
  * Row count output should be 4,803 citations unless the input workbooks change.
  * Park-name canonicalization covers the top ~40 named locations. Remaining
    rows (~111, ~2.3% of total) are street addresses rather than named parks;
    these are preserved in location_raw but not mapped into location_canon.
  * The SPR workbooks include a first-column "Total Violations" header and a
    "Violations: N" summary value repeated on every data row. This field is
    ignored; we count actual rows.
"""

from __future__ import annotations

import csv
import os
import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

REPO_ROOT = Path(__file__).resolve().parent.parent
PRR_DIR = REPO_ROOT / "data" / "prr-responses" / "C049204"
CITATIONS_OUT = REPO_ROOT / "data" / "enforcement-citations.csv"
BY_PARK_YEAR_OUT = REPO_ROOT / "data" / "enforcement-by-park-year.csv"

# Canonicalization map: regex → canonical name.
# Applied left-to-right; first match wins. Patterns are case-insensitive,
# anchored at the start of the address string (everything after the first
# comma or hyphen is typically a sub-location like "baseball diamond").
CANONICAL_PARKS = [
    (r"^Warren G\.?\s*Magnuson.*", "Magnuson Park"),
    (r"^Magnuson.*", "Magnuson Park"),
    (r"^Golden Gardens.*", "Golden Gardens Park"),
    (r"^Cal Anderson.*", "Cal Anderson Park"),
    (r"^Genesee Park.*", "Genesee Park"),
    (r"^Woodland Park.*", "Woodland Park"),
    (r"^Lower Woodland.*", "Woodland Park"),
    (r"^Green Lake.*", "Green Lake Park"),
    (r"^Volunteer Park.*", "Volunteer Park"),
    (r"^Discovery Park.*", "Discovery Park"),
    (r"^Lincoln Park.*", "Lincoln Park"),
    (r"^Seward Park.*", "Seward Park"),
    (r"^Martha Washington.*", "Martha Washington Park"),
    (r"^Westcrest.*", "Westcrest Park"),
    (r"^Ravenna Park.*", "Ravenna Park"),
    (r"^Wallingford Playfield.*", "Wallingford Playfield"),
    (r"^Rogers Playground.*", "Rogers Playground"),
    (r"^Maple Leaf Reservoir.*", "Maple Leaf Reservoir Park"),
    (r"^Meridian Playground.*", "Meridian Playground"),
    (r"^Soundview Playfield.*", "Soundview Playfield"),
    (r"^Ballard Playground.*", "Ballard Playground"),
    (r"^W\.?\s*Queen Anne Playfield.*", "West Queen Anne Playfield"),
    (r"^Kinnear.*", "Kinnear Park"),
    (r"^Denny Park.*", "Denny Park"),
    (r"^Gas Works.*", "Gas Works Park"),
    (r"^Matthews Beach.*", "Matthews Beach Park"),
    (r"^Madrona.*", "Madrona Park"),
    (r"^Kerry.*", "Kerry Park"),
    (r"^Alki Beach.*", "Alki Beach Park"),
    (r"^Dr\.?\s*Jose Rizal.*|^Jose Rizal.*", "Dr. Jose Rizal Park"),
    (r"^I-5 Colonnade.*|^I5 Colonnade.*", "I-5 Colonnade"),
    (r"^Blue Dog Pond.*", "Blue Dog Pond"),
    (r"^Northacres.*", "Northacres Park"),
]


def canonicalize(raw: str | None) -> str:
    if raw is None:
        return ""
    s = re.sub(r"\s+", " ", str(raw).strip()).rstrip(".").rstrip(",")
    for pattern, canon in CANONICAL_PARKS:
        if re.match(pattern, s, re.IGNORECASE):
            return canon
    return s


def main() -> None:
    rows: list[dict] = []

    for xlsx_path in sorted(PRR_DIR.glob("*.xlsx")):
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        for sheet_name in wb.sheetnames:
            m = re.match(r"(\d)(?:st|nd|rd|th) Offense\s+(.+)", sheet_name)
            if not m:
                continue
            offense_level = int(m.group(1))
            ws = wb[sheet_name]

            headers: list[str] | None = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(c).strip() if c is not None else "" for c in row]
                    continue
                if all(c is None for c in row):
                    continue
                d = dict(zip(headers, row))
                addr_raw = str(d.get("Address") or "").strip()
                dt = d.get("Issue Date/Time")
                year = str(dt)[:4] if dt else ""

                rows.append(
                    {
                        "year": year,
                        "offense_level": offense_level,
                        "location_raw": addr_raw,
                        "location_canon": canonicalize(addr_raw),
                        "zip": str(d.get("Zip Code") or "").strip(),
                        "issued_at": str(dt) if dt else "",
                        "fee": d.get("Fee") or "",
                        "case_result": str(d.get("Case Result") or "").strip(),
                        "source_file": xlsx_path.name,
                        "source_sheet": sheet_name,
                    }
                )
        wb.close()

    # Write the consolidated CSV.
    CITATIONS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CITATIONS_OUT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {CITATIONS_OUT.relative_to(REPO_ROOT)} ({len(rows)} rows).")

    # Aggregate counts per canonical park per year.
    years = sorted({r["year"] for r in rows if r["year"]})
    parks = sorted({r["location_canon"] for r in rows if r["location_canon"]})
    with BY_PARK_YEAR_OUT.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["park", "year", "citations"])
        for park in parks:
            for year in years:
                n = sum(1 for r in rows if r["location_canon"] == park and r["year"] == year)
                if n:
                    writer.writerow([park, year, n])
    print(f"Wrote {BY_PARK_YEAR_OUT.relative_to(REPO_ROOT)}.")

    # Summary stats for verification.
    yc = Counter(r["year"] for r in rows if r["year"])
    lc = Counter(r["location_canon"] for r in rows if r["location_canon"])
    print()
    print(f"Total citations: {len(rows)}")
    print("By year:")
    for y in sorted(yc):
        print(f"  {y}: {yc[y]}")
    print(f"Unique canonical locations: {len(lc)}")
    print("Top 10 locations:")
    for loc, n in lc.most_common(10):
        print(f"  {n:5d}  {loc}")


if __name__ == "__main__":
    main()

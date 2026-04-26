#!/usr/bin/env bash
# Mirror /data CSVs into /docs/data so GitHub Pages can serve them.
#
# The site is published from /docs (no build step). Charts on the site
# fetch CSVs at runtime from data/* relative to the page, which resolves
# to /docs/data/*. The canonical files live at /data/*; this script
# copies them into /docs/data/* so the runtime fetches see them.
#
# Run this any time you edit a CSV in /data. CI does not run it for you.
#
# Usage: ./scripts/sync-data.sh

set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p docs/data docs/data/walkshed docs/data/seattle-zips

# Top-level data CSVs that the site fetches at runtime.
csvs=(
  data/seattle-olas.csv
  data/planned-olas.csv
  data/peer-cities.csv
  data/peer-cities-budget.csv
  data/budget-detail.csv
  data/seattle-timeseries.csv
  data/illegal-use-indicators.csv
  data/kinnear-timeline.csv
  data/enforcement-hotspots.csv
  data/enforcement-hotspots-extra.csv
  data/enforcement-offense-mix.csv
  data/enforcement-program-economics.csv
  data/seattle-facility-counts.csv
  data/neighborhood-centers.csv
)
for f in "${csvs[@]}"; do
  if [[ -f "$f" ]]; then
    cp "$f" "docs/$f"
  else
    echo "WARN: missing $f (skipping)" >&2
  fi
done

# Walkshed CSVs (fetched by the access map + walkshed charts).
for f in data/walkshed/*.csv; do
  [[ -f "$f" ]] || continue
  cp "$f" "docs/$f"
done

echo "synced $(ls docs/data/*.csv docs/data/walkshed/*.csv 2>/dev/null | wc -l | tr -d ' ') CSV files into docs/data/"

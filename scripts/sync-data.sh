#!/usr/bin/env bash
# Mirror /data CSVs and walkshed GeoJSON into /docs/data so GitHub Pages
# can serve them.
#
# The site is published from /docs (no build step). Charts on the site
# fetch CSVs at runtime from data/* relative to the page, which resolves
# to /docs/data/*. The Part II and Enforcement maps also fetch
# data/walkshed/ola_isochrones.geojson at runtime. The canonical files
# live at /data/*; this script copies them into /docs/data/* so the
# runtime fetches see them.
#
# Run this any time you edit a CSV or GeoJSON in /data. CI runs it for
# you before the PDF build (.github/workflows/build-pdf.yml).
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

# Walkshed GeoJSON files fetched at runtime by Part II and Enforcement
# maps. Skipping this previously caused docs/data/walkshed/ola_isochrones.geojson
# to drift stale. Only the ones the browser actually fetches are listed
# here — `seattle_block_groups.geojson` is only used by
# scripts/population_coverage.py at compute time, so it stays out of /docs.
geojsons=(
  data/walkshed/ola_isochrones.geojson
)
for f in "${geojsons[@]}"; do
  if [[ -f "$f" ]]; then
    cp "$f" "docs/$f"
  else
    echo "WARN: missing $f (skipping)" >&2
  fi
done

n_csv=$(ls docs/data/*.csv docs/data/walkshed/*.csv 2>/dev/null | wc -l | tr -d ' ')
n_geo=$(ls docs/data/walkshed/*.geojson 2>/dev/null | wc -l | tr -d ' ')
echo "synced $n_csv CSV + $n_geo GeoJSON files into docs/data/"

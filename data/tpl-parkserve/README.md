# TPL ParkServe — Seattle slice

Derived from the nationwide ParkServe 2025 shapefile download
(`ParkScore_2025_DataDownloads_shapefiles05212025/`, 6.7 GB, not checked in
— see the root `.gitignore`).

## Files

- **seattle-park-priority-areas.geojson** — 606 block-group polygons inside
  Seattle city proper (FIPS place `5363000`), reprojected from Albers
  Equal Area to WGS84 (EPSG:4326). Fields inherited from the TPL schema;
  the ones we use here are:
  - `ParkNeed` — 1 if BG is outside a 10-minute walk of any park, else 0.
    For Seattle, every BG is `0` (TPL's 99% figure in practice).
  - `ParkRank` — 1 (lower priority) to 3 (higher priority), a composite
    of low-income density, POC density, heat, health, LPA, etc.
  - `TPL_Acres`, `PopPerAcre` — BG area and density.
  - `LowInc_Den`, `POC_Dens`, `HeatRank`, `MentalRank`, etc. — individual
    equity inputs to the rank.

Source license: TPL ParkServe Terms of Use (redistribution of this
derived Seattle subset is per TPL's data-use policy; see
https://www.tpl.org/park-data-downloads).

## How this was produced

```bash
.venv/bin/python -c "
import geopandas as gpd
g = gpd.read_file('data/ParkScore_2025_DataDownloads_shapefiles05212025/data/Parkserve_ParkPriorityAreas.shp')
seattle = g[g['PlaceID'].astype(str) == '5363000'].to_crs('EPSG:4326')
seattle.to_file('data/tpl-parkserve/seattle-park-priority-areas.geojson', driver='GeoJSON')
"
```

## Intended use

The OLA walkshed analysis (`data/walkshed/`) tells us which residents
live near an OLA. This ParkServe slice tells us TPL's equity-weighted
priority score for each block group. Overlaying the two answers:
**do Seattle's existing OLAs concentrate in high-priority BGs or
low-priority ones?** A forthcoming analysis will attribute each BG's
`ParkRank` against whether it falls inside the 0.5-mile OLA walkshed
union and publish the table.

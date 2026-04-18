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
priority score for each block group. Overlaying the two answers the
question **"do Seattle's existing OLAs concentrate in high-priority
BGs or low-priority ones?"**

## Initial overlay result

`ola-walkshed-by-tpl-rank.csv` and `ola-walkshed-by-tpl-priority-tier.csv`
cross each BG's TPL rank against whether it intersects the union of
0.5-mile OLA walksheds (data/walkshed/ola_isochrones.geojson):

| ParkRank (1 = lowest priority, 3 = highest) | BGs | With OLA walkshed | % |
|---:|---:|---:|---:|
| 1 | 219 | 31 | 14.2% |
| 2 | 201 | 19 |  9.5% |
| 3 | 186 | 57 | 30.6% |

Splitting more finely by TPL's continuous `ParkPriori` index (0–5):

| ParkPriori tier | BGs | With OLA walkshed | % |
|---:|---:|---:|---:|
| 1–2 | 122 | 18 | 14.8% |
| 2–3 | 227 | 21 |  9.3% |
| 3–4 | 170 | 34 | 20.0% |
| 4–5 |  87 | 34 | 39.1% |

**Reading:** Seattle's OLAs land in a bimodal pattern. The highest-
priority block groups (those TPL ranks most acutely in need of new
parks on equity/health grounds) actually have *above-average* OLA
walkshed coverage — Magnuson/Sand Point, Westcrest/Highland Park, and
Blue Dog Pond/Mt. Baker all sit in high-priority areas. But the
middle tier — BGs with moderate priority on TPL's composite — has
*the lowest* OLA access at 9.3%. Those are where the gap lives.


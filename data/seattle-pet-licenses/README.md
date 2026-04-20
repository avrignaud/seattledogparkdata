# Seattle Pet Licenses — snapshot and analysis

## Source

Seattle Open Data dataset [`jguv-t9rb`](https://data.seattle.gov/City-Administration/Seattle-Pet-Licenses/jguv-t9rb/about_data), published by **FAS / Seattle Animal Shelter**. Public-domain license.

> A list of active/current Seattle pet licenses, including animal type (species), pet's name, breed and the owner's ZIP code. (List current as of April 1, 2026.)

The city publishes a full dump, rebuilt periodically. This directory holds a dated snapshot so site analyses are reproducible even if the city refreshes the dataset.

## Files

| File | What | Produced by |
|---|---|---|
| `Seattle-Pet-Licenses-2026-04-01.csv` | Raw city snapshot. 39,654 rows. 7 columns: `License Issue Date`, `License Number`, `Animal's Name`, `Species`, `Primary Breed`, `Secondary Breed`, `ZIP Code`. | Seattle Open Data export, 2026-04-20 |
| `summary.csv` | Totals by species | `scripts/analyze_pet_licenses.py` |
| `dogs-by-zip.csv` | Active dog licenses per Seattle ZIP code, sorted | `scripts/analyze_pet_licenses.py` |
| `top-dog-breeds.csv` | Active dog licenses per primary breed, sorted | `scripts/analyze_pet_licenses.py` |

## Headline figures (April 1, 2026 snapshot)

- **26,652 active dog licenses** (previously cited on the site as "~26,700" — this is the precise number).
- **12,978 active cat licenses** (dogs outnumber licensed cats roughly 2:1).
- **282 distinct primary-breed values** among licensed dogs.
- **138 distinct ZIP codes** represented among licensed dogs.
- **Top-5 dog-owning ZIP codes**: 98115 (2,597), 98103 (2,179), 98117 (1,860), 98125 (1,514), 98118 (1,483).

## What this dataset does and doesn't answer

**Answers:**
- Current count of licensed dogs city-wide.
- Current ZIP-level distribution of licensed dogs.
- Current breed distribution.

**Does not answer:**
- Historical license counts over time. The `License Issue Date` column records the *most recent renewal* date for each currently-active license, not a time series of enrollment. Many licenses in the snapshot were last renewed 2022–2026; the oldest renewal visible is 2015-10-21, but that reflects a single stale multi-year license, not 2015's total.
- Compliance rate (what fraction of actual Seattle dogs are licensed).
- New-license vs renewal rates.

Those gaps are the remainder of what [PRR #6](../../prrs/06-sas-dog-license-history.md) asks SAS for.

## Privacy note

The source dataset is published publicly by the City of Seattle under public-domain terms. Rows include pet names and owner ZIP codes, but no owner names, street addresses, or other PII. This snapshot mirrors the city's public release with no additional processing applied to the raw file.

## Refresh

To refresh the snapshot from the city source:

```bash
curl -sSL "https://data.seattle.gov/api/views/jguv-t9rb/rows.csv?accessType=DOWNLOAD" \
  -o data/seattle-pet-licenses/Seattle-Pet-Licenses-YYYY-MM-DD.csv
.venv/bin/python3 scripts/analyze_pet_licenses.py
```

# PRR C263990 — Find It Fix It "Nuisance Dogs in a Park" complaints, April 2024 – June 2026

## Request

Sent by Andre Vrignaud via the Seattle Public Records Request Center on **2026-04-17**
(C263990-041726). Requested complaints filed through the City's **Find It Fix It** app
and web portal relating to dogs in parks — counts by year, complaint category, and
location, plus the list of dog-related FIFI categories and any summary reports.

## Response

- **PRR number:** C263990-041726
- **Responding agency:** Seattle Department of Finance & Administrative Services (FAS)
- **Public Disclosure Officer:** Sarah Stark
- **Released:** June 2026 (pointer to Open Data; CSV delivered by FAS)

FAS interpreted the request against the **Motorola Customer Service Request system**
(which includes Find It Fix It), not the Seattle Animal Shelter PetPoint database. Of
the request types FAS flagged as dog-related (Nuisance Dogs in a Park; General Inquiry –
Animal Shelter; Animal Noise; Dead Animal; Found a Pet; Lost a Pet), only **"Nuisance
Dogs in a Park"** is dog-specific and the most responsive. FAS noted this request type
**was created in 2024** — so there is no pre-2024 history.

The responsive data is published free on the City Open Data portal:
**`Customer Service Requests`, dataset id `5ngg-rpne`**
(https://data.seattle.gov/City-Administration/Customer-Service-Requests/5ngg-rpne).
The file here is the `Nuisance Dogs in a Park` slice as delivered.

**Still pending:** the `General Inquiry – Animal Shelter` free-text export. That type
has no species/category fields — only free-text — and the text is not in Open Data, so
FAS would supply it separately. It may contain additional dogs-in-parks complaints but
will be noisier (no structured location/category).

## File

| File | Type | Period | Rows |
|---|---|---|---:|
| `Customer_Service_Requests_NuisanceDogsInAPark_2024-2026.csv` | CSV | 2 Apr 2024 – 3 Jun 2026 | 4,865 |

Columns: Service Request Number, Service Request Type (all `Nuisance Dogs in a Park`),
City Department, Created Date, Method Received, Status, Location (street address),
X/Y, Latitude, Longitude, ZIP Code, Council District, Police Precinct, Community
Reporting Area. Latitude/Longitude populated on 100% of rows.

## Analysis

`scripts/compare_complaints_citations.py` joins these complaints to the TPL ParkServe
Seattle park-boundary layer (point-in-polygon) and compares them against the Animal
Control off-leash citations from PRRs C049204 + C263949. Outputs:
`data/complaints-vs-citations-by-park.csv` and `data/complaints-citations-monthly.csv`.
Findings writeup: `FIFI_Nuisance_Dogs_Findings_2026-06-04.md` (repo root).

Note on geography: the 2024-26 citation records are themselves **park-named**
(`location_type == park_named`), so they need no geocoding — they are matched to
ParkServe names directly. The 2014-19 citations (C049204) are street addresses and are
geocoded in `data/walkshed/street-address-geocodes.csv`.

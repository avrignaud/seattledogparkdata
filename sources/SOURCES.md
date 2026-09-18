# Sources

All primary sources used in the Seattle Off-Leash Areas data analysis, organized by category.

## Seattle Parks & Recreation (SPR)

- [SPR Dog Off-Leash Areas main page](https://www.seattle.gov/parks/recreation/dog-off-leash-areas)
- [SPR Off-Leash Area Expansion Study](https://www.seattle.gov/parks/about-us/plans-and-reports/recreation-plans-and-reports/off-leash-area-study)
- [People, Dogs and Parks Strategic Plan (2017)](https://www.seattle.gov/parks/about-us/plans-and-reports/recreation-plans-and-reports/people-dogs-and-parks-strategic-plan) — [full PDF (Aug 2017)](https://www.seattle.gov/documents/departments/parksandrecreation/policiesplanning/peopledogsandparksplan-august2017.pdf), committed locally at [`sources/people-dogs-and-parks-plan-august-2017.pdf`](people-dogs-and-parks-plan-august-2017.pdf). The **2015** owner survey (3,970 dog owners) is summarized on **p.17**: illegal off-leash use is 39% in local parks and 38% in large parks (weekly to monthly), 36% on park trails — blended to ~38% on the site.
- [West Seattle Stadium OLA Development](https://www.seattle.gov/parks/about-us/projects/west-seattle-stadium-off-leash-area-development)
- [Othello Playground OLA Development](https://www.seattle.gov/parks/about-us/projects/othello-playground-off-leash-area-development)
- **SPR project-page schedule status for both funded OLAs, archived 2026-09-13** — [`spr-ola-project-status-2026.md`](spr-ola-project-status-2026.md). West Seattle Stadium: construction spring 2027, completion winter 2028 (Engage page updated 2026-07-29); Othello: construction late 2026/early 2027, completion fall 2027 (seattle.gov page updated 2026-04-03). Both pages state the Park District two-OLA line as $3,103,000. Supersedes the "fall 2026" opening the site carried through July 2026.
- [Georgetown OLA Development](https://www.seattle.gov/parks/about-us/projects/georgetown-off-leash-area-development)
- Individual OLA pages (Magnuson, Westcrest, Kinnear, etc.) under `/parks/allparks/<name>`
- [SPR Dog Off-Leash Areas ArcGIS feature service](https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Dog_Off_Leash_Areas/FeatureServer/0) — authoritative point geometry + attributes for all OLAs. Portal: [Seattle GeoData — Dog Off-Leash Areas](https://data-seattlecitygis.opendata.arcgis.com/datasets/a195df348c00489ca557fced74f1aa62). Source for coordinates in `data/seattle-olas.csv` (pulled 2026-04).
- **People, Dogs & Parks Plan — June 2016 DRAFT.** Released via PRR C266465 (Bates `PKS_C266465_01_00004`, `_00177`). Differs from the Aug 2017 final in two ways worth citing: its summary states Park District OLA funding as "**$106,000 annually through 2020**" (the final keeps that figure at p. 19 and adds "between $103,000 and $117,000 annually" at pp. 3, 5), and its summary quotes the OLA capital range as $718,000–$1,363,000, contradicting its own Section 7 total of **$1,150,000–$2,220,000** (2016 dollars) — the final drops the $718K figure. Section 7's per-site capital list is archived at [`data/prr-responses/C266465/documents/00168-ola-capital-priority-list-2016.pdf`](../data/prr-responses/C266465/documents/00168-ola-capital-priority-list-2016.pdf).
- **SPR budget and spend for BC-PR-50000 by Master Project, 2023 to 7 July 2026** (PRR **C264837-042426**, responded 15 July 2026, Gerald Asp). The record that answers whether the OLA share of "Maintaining Parks & Facilities" is knowable: it is, because SPR books `MC-PR-51002` "Improve Dog Off Leash Areas" and `MC-PR-51001` "Rejuvenate P-Patches" as separate Master Projects, with no allocation formula between them. OLA-only adopted budget $328,345 (2023), $333,478 (2024), $1,568,818 (2025), $1,574,370 (2026); $1,053,037 spent against a $5,625,926 revised budget; the ~$3.1M Cycle 2 capital sits inside this BSL, and ~$600K of it has gone to planning and design with construction estimated for early 2027. **The two tables are embedded EMF images in the .docx, not text** — extracted to [`data/prr-responses/C264837/text/response-and-tables.txt`](../data/prr-responses/C264837/text/response-and-tables.txt) and [`data/ola-ppatch-master-projects.csv`](../data/ola-ppatch-master-projects.csv). Archive and full reading: [`data/prr-responses/C264837/`](../data/prr-responses/C264837/README.md).
- **SPR OLA program presentations to City Council** — Dec 7 2021 and Aug 3 2022 (PRR C266465, Bates `_00635`, `_00681`). Source of SPR's "top 5 in access to dog parks per capita (TPL)" claim, of the "$100K annually / $635,000 spent 2017–2021" OLA major-maintenance figures, and of the 15-OLA / 28-acre inventory as of Aug 2022.
- **SPR Off-Leash Area Expansion Study — recommendations deck to the Board of Park Commissioners, Feb 22 2024** (PRR C266465, Bates `_00416`). 32 candidate sites → 9 meeting criteria → 4,753 survey responses → 3 recommended (West Seattle Stadium 87% support, Othello 73%, Ravenna 61%). Names Capitol Hill, Ballard and Northgate as unaddressed gaps; lists East Queen Anne Playfield as a recommended future site.

## Finance & Administrative Services / Seattle Animal Shelter (FAS/SAS)

- **FAS response to Council SLI FAS-003-B-001 — "Seattle Animal Shelter Report on Challenges and Opportunities to Increase Animal Control Patrolling in City Parks," June 30 2022.** Signed by FAS Director Calvin W. Goings. Released via PRR C266465 (Bates `PKS_C266465_01_00524`), archived at [`data/prr-responses/C266465/documents/`](../data/prr-responses/C266465/documents/00524-fas-sli-response-animal-control-parks-2022-06-30.pdf). The City's own statement that OLA scarcity drives off-leash use in regular parks; the City's own OLA-per-100k peer table (Seattle 1.9 / Portland 4.9 / San Francisco 6.5); 2021 patrol baseline (344 of 489 parks, 70%; 1,850 parks-patrol responses = 33% of Field Services calls); and the structural enforcement failures (refused ID, 60–120 minute SPD response times).
- **SPR internal ACO program review — Jon Jainga memo to the Interim Deputy Superintendent, Aug 30 / Sep 6 2024** (PRR C266465, Bates `_00353`, `_00360`). The only internal review of the "Making Parks Safer" program in the release. Output tracking for 2023–24 and options to reduce the program from three ACO IIs to two or one. Extracted to [`data/enforcement-program-activity.csv`](../data/enforcement-program-activity.csv).
- **Council Budget Action FAS 128_SAS_P, Oct 4 2022** — "Park District Animal Control Officer Positions." Adds two 1.0 FTE ACO II positions, Park District Levy funded, $315,231 (2023) / $319,978 (2024). PRR C266465, Bates `_00603`.
- **SPR↔FAS MOA quarterly ledger backup, 2023–2024** (PRR C266465, Bates `_00480`, `_00485`, `_00653`). The first actual-expenditure records for the ACO enforcement line: FY2024 billed $456,173 for three staff, on invoices computed from a flat 40 hr/week calendar rather than hours worked. Extracted to [`data/prr-responses/C266465/documents/enforcement-moa-billing.csv`](../data/prr-responses/C266465/documents/enforcement-moa-billing.csv).

## Budget Documents

- [2021 Proposed Budget — SPR section](https://www.seattle.gov/Departments/FinanceDepartment/21proposedbudget/SPR.pdf)
- [2025-26 Proposed Budget — SPR section](https://www.seattle.gov/documents/departments/financedepartment/2526proposedbudget/spr.pdf)
- Seattle Park District Cycle 1 (2015–2022) financial plan
- Seattle Park District Cycle 2 (2023–2028) financial plan

## Trust for Public Land (TPL)

- [TPL 2025 ParkScore — Seattle PDF](https://parkserve.tpl.org/downloads/pdfs/Seattle_WA.pdf)
- [TPL 2025 ParkScore — Portland PDF](https://parkserve.tpl.org/downloads/pdfs/Portland_OR.pdf)
- [TPL 2025 ParkScore — San Francisco PDF](https://parkserve.tpl.org/downloads/pdfs/San%20Francisco_CA.pdf)
- [TPL 2025 ParkScore — Austin PDF](https://parkserve.tpl.org/downloads/pdfs/Austin_TX.pdf)
- [TPL ParkServe methodology documentation](https://www.tpl.org/parkserve/about)
- [TPL ParkScore methodology](https://parkscore.tpl.org/methodology.php)

## Population Data

- [WA Office of Financial Management — April 1 Official Population Estimates](https://ofm.wa.gov/washington-data-research/population-demographics/population-estimates/april-1-official-population-estimates)
- [WA OFM — Historical estimates 1990–2020](https://ofm.wa.gov/washington-data-research/population-demographics/population-estimates/historical-estimates-april-1-population-and-housing-state-counties-and-cities)
- U.S. Census Bureau 2000, 2010, 2020 decennial counts

## Peer Cities

- [Portland — Find a dog off-leash area](https://www.portland.gov/parks/find-dog-off-leash-area)
- [Portland — Park Rules for Dogs](https://www.portland.gov/parks/dogs)
- [Vancouver BC — Dog off-leash areas](https://vancouver.ca/parks-recreation-culture/dog-off-leash-areas.aspx)
- [Vancouver BC — People, Parks and Dogs Strategy (2017)](https://vancouver.ca/files/cov/people-parks-dogs-strategy-report.pdf)

## Kinnear Park / Encampment Coverage

- [Seattle Weekly — Ruff Trade (2007)](https://www.seattleweekly.com/news/ruff-trade/)
- [Seattle Times — Clearing Queen Anne Hill homeless encampments (2008)](https://www.seattletimes.com/seattle-news/clearing-queen-anne-hill-homeless-encampments-is-big-job/)
- [Aussiedoodle Adventures — Kinnear Off-Leash Park review (Dec 2020)](https://aussiedoodleadventures.com/2020/12/25/kinnear-off-leash-dog-park/)
- [Fix Homelessness — Hidden encampment network (2023)](https://fixhomelessness.org/2023/hidden-encampment-network-in-seattles-forests/)
- [KOMO News — City clears Kinnear Park camp (April 2025)](https://komonews.com/news/local/city-clears-homeless-camp-in-seattles-kinnear-park-but-tents-reappear-within-days-drugs-unified-care-team-we-heart-seattle-andrea-suarez)
- [KOMO News — We Heart Seattle cleans Kinnear Park (May 2025)](https://komonews.com/news/local/we-heart-seattle-cleans-kinnear-park-with-help-from-former-homeless-volunteers-tents-drugs-fires-fentanyl-services-recovery)

## Advocacy & Community

- [Citizens for Off-Leash Areas (COLA) Seattle](https://www.seattlecola.info)
- [COLA email campaign](https://www.seattlecola.info)
- [Queen Anne & Magnolia News — OLA expansion coverage (Nov 2023)](https://queenannenews.com/news/2023/nov/01/new-off-leash-areas-planning-raises-concerns/)
- [Parkways (SPR blog) — Expansion Study recommendations (Feb 2024)](https://parkways.seattle.gov/2024/02/23/announcing-the-recommendations-from-the-off-leash-area-expansion-study/)
- [Parkways — TPL names Seattle 8th best parks system (2025)](https://parkways.seattle.gov/2025/05/22/trust-for-public-land-names-seattle-8th-best-parks-and-recreation-system-in-the-nation/)

## Aggregator / Supporting Sources

- [Seattle Dog Spot](https://www.seattledogspot.com) (OLA inventories)
- [BringFido — Seattle parks](https://www.bringfido.com/attraction/parks/city/seattle_wa_us/)
- [The Urbanist — Seattle's Park System Rated 9th (2021)](https://www.theurbanist.org/2021/06/01/seattles-park-system-rated-9th-best-in-new-national-ranking/)
- [Axios Seattle — best park systems (2024)](https://www.axios.com/local/seattle/2024/05/24/seattle-parks-ranking-trust-for-public-land)

## Dog Population Estimates

- [Seattle Pet Licenses dataset](https://data.seattle.gov/City-Administration/Seattle-Pet-Licenses/jguv-t9rb/about_data) on Seattle Open Data (published by FAS / Seattle Animal Shelter). 26,652 active dog licenses as of April 1, 2026 — the licensed floor. Dated snapshot committed at [`data/seattle-pet-licenses/`](../data/seattle-pet-licenses/) with an analysis script at [`scripts/analyze_pet_licenses.py`](../scripts/analyze_pet_licenses.py).
- [AVMA U.S. Pet Ownership Statistics](https://www.avma.org/resources-tools/reports-statistics/us-pet-ownership-statistics). 2025 Sourcebook figures: 45.5% of U.S. households own a dog; average 1.5 dogs per dog-owning household. Used with ACS household count to derive Seattle estimate.
- [U.S. Census ACS 1-year 2023, Seattle households (table B11001)](https://api.census.gov/data/2023/acs/acs1?get=NAME,B11001_001E&for=place:63000&in=state:53). 364,627 occupied households.
- [Seattle Humane](https://www.seattlehumane.org) / [Cascade PBS](https://www.cascadepbs.org) coverage — original source for the long-cited 150,000-dog floor.
- [SPR 2023-24 OLA Expansion Study](https://www.seattle.gov/parks/about-us/plans-and-reports/recreation-plans-and-reports/off-leash-area-study) — cites 187K to "upwards of 400,000" dogs.

## Geographic Data

- [Seattle GeoData 2023 SPR Walkability Gap Analysis](https://data-seattlecitygis.opendata.arcgis.com/maps/6ae790444cbd404f9e8421e2bd89eebc) (referenced; data not yet extracted)
- TPL ParkServe dataset (publicly downloadable for the 100 largest U.S. cities)

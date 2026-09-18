# SPR project-page status for the two funded OLAs — archived 2026-09-13

Verbatim schedule text captured from Seattle Parks and Recreation's own project pages,
because the live pages are updated in place and the earlier "Fall 2026" timeline has
already been overwritten on two of the three. Fetched 2026-09-13 with a plain HTTP GET;
HTML tags stripped, nothing else altered.

## West Seattle Stadium OLA — Engage Seattle Parks page

URL: https://engageseattleparks.com/west-seattle-stadium-leash-area-development
Page stamp: "Summer 2026 · Updated July 29th, 2026"

> "Thanks to everyone who helped shape the design for your future off-leash area. We are
> working on construction documents and expect to begin the bidding process in late 2026.
> We are approaching the 90% Construction Documentation and expect to begin the bidding
> process in late 2026."

Schedule block: "Planning: Summer 2024 (complete) · Design: Spring 2025 (complete) ·
**Construction: Spring 2027** (incomplete) · **Completion: Winter 2028** (incomplete)"

Budget block: "The Seattle Park District provides $3,103,000 for the planning, design, and
construction of two OLAs, one at West Seattle Stadium and one at Othello Playground."

Earlier statement, superseded by the above: Seattle Parks to the West Seattle Blog,
2026-03-24 (https://westseattleblog.com/2026/03/followup-schedule-slides-for-west-seattles-next-off-leash-area/):
"We are currently preparing review of 60% Design documents … expect to go to bid in
December of this year … Construction is now expected to start in early 2027 and be
complete by Fall 2027." The same article notes "the last update had suggested
construction would start this spring" (i.e., spring 2026).

## Othello Playground OLA — seattle.gov project page

URL: https://www.seattle.gov/parks/about-us/projects/othello-playground-off-leash-area-development
Page stamp: "Updated: April 3, 2026"

> "Spring 2026 — Thanks to everyone to helped shape the design for your future off-leash
> area. As of Spring 2026 we are approaching 60% Construction Documentation and expect to
> begin the bidding process in late 2026."

Schedule block: "Planning: Summer 2024 · Design: Summer 2025 · **Construction: Late
2026/Early 2027** · **Completion: Fall 2027**"

Budget block: same $3,103,000 two-OLA sentence.

The Engage Seattle Parks page for Othello
(https://engageseattleparks.com/othello-playground-leash-area-development) still showed
the stale "Construction: Spring 2026 · Completion: Fall 2026" timeline on the fetch date;
it carries no update stamp and is treated as superseded by the seattle.gov page.

## How the site uses this

- `data/planned-olas.csv`: West Seattle Stadium → Winter 2028 (Engage, Jul 2026);
  Othello → Fall 2027 (seattle.gov, Apr 2026). Neither site is under construction.
- `data/seattle-timeseries.csv` 2026 row: OLA count stays 14.
- The $3,103,000 is the two-OLA construction line. The site used to carry $3.46M for this, cited to the Mayor's Park District Cycle 2 fact sheet, which does not contain it; that figure was retired in September 2026 in favour of the $3,103,000 on SPR's own project pages. PRR C264837 establishes that the money is booked inside BSL BC-PR-50000 within Master Project MC-PR-51002, not as a separate appropriation.
  (2022 Park District fact sheet) additionally covers Ravenna Park design.

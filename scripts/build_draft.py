#!/usr/bin/env python3
"""
Build docs/enforcement-draft.html from scripts/draft_page_data.json.

This is the working-draft generator for the post-PRR-C263949 enforcement
page refresh. It is NOT part of the production data pipeline — it exists so
the draft can be regenerated as the data or copy evolves during review.

Run from repo root:  .venv/bin/python scripts/build_draft.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "scripts" / "draft_page_data.json"))
DATA_JS = json.dumps(D)

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>13 years of off-leash enforcement: rising cost, falling output [DRAFT] — Seattle Dog Park Data</title>
<meta name="description" content="Seattle's off-leash dog enforcement program 2014–2026: where citations were issued, what the program costs, and whether the available data shows it reducing violations.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
<link rel="stylesheet" href="site.css">
<style>
  .draft-banner { background: #FFF4D1; border: 2px solid #B8872B; padding: 12px 18px; margin: 0 0 22px; border-radius: 6px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; line-height: 1.6; color: #5A3E10; }
  .draft-banner strong { color: #8B2518; text-transform: uppercase; letter-spacing: 0.08em; }
  .data-currency { background: var(--surface); border: 1px solid var(--rule); border-left: 3px solid var(--navy); border-radius: 6px; padding: 18px 22px; margin: 0 0 28px; font-size: 14px; line-height: 1.55; color: var(--ink); }
  .data-currency .banner-label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--navy); display: block; margin-bottom: 6px; font-weight: 500; }
  table.data { width: 100%; border-collapse: collapse; margin: 18px 0 12px; font-size: 14.5px; background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; font-variant-numeric: tabular-nums; }
  table.data th, table.data td { text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--rule-soft); }
  table.data th { font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-soft); background: var(--rule-soft); font-weight: 500; }
  table.data th.num, table.data td.num { text-align: right; font-variant-numeric: tabular-nums; }
  table.data td.ola-yes { color: var(--sage); font-weight: 500; }
  table.data td.ola-no  { color: var(--orange); font-weight: 500; }
  table.data td.ola-partial { color: var(--gold); font-weight: 500; }
  table.data td.ola-planned { color: var(--ink-faint); font-weight: 500; }
  table.data tr:last-child td { border-bottom: 0; }
  .sdpd-map-legend { background: rgba(250,248,243,0.96); border: 1px solid var(--rule); border-radius: 10px; padding: 10px 12px; font-family: 'Inter', sans-serif; font-size: 12px; line-height: 1.7; color: var(--ink); box-shadow: 0 6px 20px -10px rgba(26,23,18,0.18); }
  .sdpd-map-legend .hdr { font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-faint); margin-bottom: 6px; }
  .sdpd-map-legend .row { display: flex; align-items: center; gap: 8px; }
  .sdpd-map-legend .dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; box-shadow: 0 0 0 2px #fff; flex: none; }
  .sdpd-map-legend .ring { display: inline-block; width: 12px; height: 12px; border-radius: 50%; border: 1.5px solid var(--sage); background: rgba(76,107,84,0.12); flex: none; }
  .sdpd-map-legend .heat-grad { display: inline-block; width: 34px; height: 10px; border-radius: 2px; background: linear-gradient(to right, rgba(249,231,219,0.85), #F5B78E, #E07839, #B83F14, #6E1A0E); box-shadow: 0 0 0 1px var(--rule); flex: none; }
  .footnotes { margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--rule); }
  .footnotes h3 { font-size: 20px; margin-top: 24px; }
  .footnotes p { font-size: 14px; color: var(--ink-soft); max-width: 74ch; }
  .footnotes ul { font-size: 14px; color: var(--ink-soft); line-height: 1.6; max-width: 74ch; }
  .footnotes ul li { max-width: none; }
  .gap-callout { background: rgba(139, 37, 24, 0.07); border-left: 3px solid var(--danger); padding: 18px 22px; margin: 22px 0; border-radius: 0 6px 6px 0; font-size: 14.5px; line-height: 1.6; }
  .gap-callout strong.head { display: block; color: var(--danger); font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }
  .gap-callout ul { margin: 10px 0 0 22px; padding: 0; }
  .gap-callout li { margin-bottom: 4px; }
  .fair-note { background: rgba(31,58,95,0.05); border-left: 3px solid var(--navy); padding: 16px 20px; margin: 18px 0; border-radius: 0 6px 6px 0; font-size: 14px; line-height: 1.6; }
  .fair-note strong.head { display: block; color: var(--navy); font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }
  .supporting { background: var(--surface); border: 1px solid var(--rule); border-radius: 6px; padding: 22px; margin: 18px 0; }
  .supporting .supporting-title { font-family: 'Fraunces', serif; font-size: 17px; font-weight: 600; margin: 0 0 8px; }
  .supporting .supporting-note { color: var(--ink-soft); font-size: 13.5px; margin-bottom: 12px; max-width: 80ch; }
  .supporting .chart-wrap { height: 260px; }
  .hero-glyph { text-align: center; margin: 8px auto 40px; opacity: 0.75; }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<main id="main"><div class="wrap">

<div class="topbar">
  <a class="brand" href="index.html"><img class="mark" src="favicon.svg" alt=""><span>Seattle Dog Park Data</span></a>
  <nav class="nav" aria-label="Site navigation">
    <a href="index.html">Overview</a>
    <a href="part1-the-gap.html">The Gap</a>
    <a href="part2-access.html">Access</a>
    <a href="part3.html">Forward</a>
    <a href="enforcement.html" class="active">Enforcement</a>
    <a href="budget.html">Budget</a>
    <a href="peer-cities.html">Peer Cities</a>
    <a href="opinion.html">Opinion</a>
    <a href="updates.html">Updates</a>
  </nav>
</div>

<div class="masthead">
  <span class="dateline">Enforcement &middot; seattledogparkdata.com</span>
  <span>MAY 2026</span>
</div>

<div class="draft-banner">
  <strong>Private working draft.</strong> Not linked from the site; <code>noindex,nofollow</code> set. Numbers and narrative are pending review &mdash; do not cite. Production version is at <a href="enforcement.html">enforcement.html</a> (unchanged). Reflects PRR C263949 ingest + the editorial reshape: lead with the fiscal story (cost per citation), then temporal arc, then deterrence signals, then geography.
</div>

<div class="data-currency">
  <strong class="banner-label">About this data</strong>
  Citations on this page run from <strong>January 1, 2014 through April 17, 2026</strong>, combining two Seattle public records requests to cover the full period: <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C049204">C049204</a> for 2014&ndash;2018 and <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C263949">C263949</a> for 2019 through April 17, 2026. Headline figures use <strong>&ldquo;Dog Loose in Park&rdquo; (DLP)</strong> citations &mdash; Seattle's off-leash violation under <a href="https://library.municode.com/wa/seattle/codes/municipal_code?nodeId=TIT18PALA_CH18.12GEPRRE_SUBCHAPTER_IIOFPRPA_18.12.080DORELI">SMC 18.12.080(A)</a> &mdash; so every year is measured the same way. Where 2019 appears in both requests, the fuller C263949 record is used. 2026 is a partial year (through April 17) and is marked as such on every chart.
</div>

<header class="hero">
  <span class="kicker orange">Enforcement</span>
  <h1 class="hed">13 years of off-leash enforcement in Seattle: <em>rising cost, falling output</em>.</h1>
  <p class="deck">Seattle Animal Control's records cover 13 years of off-leash (&ldquo;Dog Loose in Park,&rdquo; DLP) enforcement. Citation output peaked in 2018, fell sharply during the COVID period, and has not recovered. The cost of issuing each citation has risen. Across the full record, the available data does not show the program reducing violations &mdash; first-time offenders remain the overwhelming majority of citations every year. The 2026 staffing expansion is being implemented without a published evaluation of the 2016 expansion's results.</p>
  <div class="byline">Source: Seattle Animal Control PRRs <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C049204">C049204</a> (2014&ndash;2018) and <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C263949">C263949</a> (2019&ndash;2026-04-17) &middot; staffing: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2016-04-02.pdf">2016 MOA</a>, <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf">signed 2021 MOA</a>, <a href="https://www.axios.com/local/seattle/2026/04/17/more-paw-patrols-seattle-ramping-up-dog-related-enforcement">Axios Seattle April 2026</a> &middot; coordinates approximate from park names</div>
</header>

<section>
  <div class="stats">
    <div class="stat orange">
      <div><div class="label">DLP citations 2014&ndash;2026</div><div class="num">7,015</div></div>
      <div class="note">Dog Loose in Park, all offense levels, both PRRs. <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">src</a></div>
    </div>
    <div class="stat orange">
      <div><div class="label">2024 output vs 2018 peak</div><div class="num">35<span class="unit">%</span></div></div>
      <div class="note">The strongest year since the COVID period (2024, 447) is 35% of the 2018 peak (1,276).</div>
    </div>
    <div class="stat gold">
      <div><div class="label">First-time offenders, every year</div><div class="num">84&ndash;96<span class="unit">%</span></div></div>
      <div class="note">Share of citations that are 1st offenses. The mix never shifted toward repeat offenders.</div>
    </div>
    <div class="stat navy">
      <div><div class="label">2026 cost increase</div><div class="num">~2&times;</div></div>
      <div class="note">Annual baseline rises from $292K to ~$585K under the <a href="https://www.axios.com/local/seattle/2026/04/17/more-paw-patrols-seattle-ramping-up-dog-related-enforcement">announced expansion</a>.</div>
    </div>
  </div>
</section>

<figure class="hero-glyph" aria-hidden="true">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 100" width="140" height="100" fill="none" stroke="#1F3A5F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <line x1="10" y1="90" x2="130" y2="90" stroke-dasharray="3,4"/>
    <path d="M30 65 Q50 45 80 50 Q100 55 108 65"/>
    <path d="M35 65 L30 80 M45 65 L50 82 M95 65 L92 82 M105 65 L110 80"/>
    <circle cx="108" cy="55" r="8"/><path d="M103 48 L100 40 M113 48 L116 40"/><circle cx="110" cy="54" r="1" fill="#1F3A5F"/>
    <path d="M30 65 Q20 55 24 45"/><circle cx="128" cy="42" r="5"/><path d="M123 42 Q128 38 133 42 M128 37 L128 47"/>
  </svg>
</figure>

<!-- ============ FINDING 01 — FISCAL LEAD ============ -->
<h2 class="finding" id="finding-01"><span class="num">Finding 01</span><span>Fewer citations, each costing more to produce.</span></h2>
<p class="lead">Citation volume has fallen well below its 2018 peak, while the program's staffing cost has held roughly flat (and is set to roughly double in 2026). The result: the cost of producing each citation has risen. The bars show citations issued per year; the line shows the program's annual cost divided by that year's citations.</p>

<div class="chart-block">
  <div class="chart-title">DLP citations vs. cost per citation, 2014&ndash;2025</div>
  <div class="chart-subtitle">Green bars (left axis): DLP citations per year, 2014&ndash;2025. Orange line (right axis): annual FAS+FMW program cost &divide; that year's citations. The cost-per-citation line begins in 2016 &mdash; the first year with a documented cost basis (the April 2016 MOA) &mdash; because pre-2016 part-time staffing has no separately documented cost. COVID period shaded. The line stops at 2025 because 2026 is a partial year (see Finding 02). All dollars nominal.</div>
  <div class="chart-wrap"><canvas id="chartCostPerCit" role="img" aria-label="Dual-axis chart: DLP citations per year as bars and cost per citation as a line, 2014-2025."></canvas></div>
  <div class="chart-source">Citations: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; FAS cost: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf">2021 MOA Attachment A</a> ($152,399/yr per ACO II) &middot; FMW pairing ~$140K/yr (author estimate, documented in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-program-economics.csv">enforcement-program-economics.csv</a>)</div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Across 2014&ndash;2025, fee revenue ($351,099 cumulative) covered roughly 11% of the program's estimated $3.34M FAS+FMW cost. In the MOA-documented era (2016 on), cost per citation was lowest in the peak-output years &mdash; $229 in 2018 &mdash; and highest in the trough &mdash; $1,730 in 2022. Even the 2024 partial recovery to 447 citations leaves cost-per-citation at $654, nearly triple the 2018 figure. Because the announced 2026 expansion roughly doubles staffing cost, holding the existing cost-per-citation ratio would require citation output to roughly double from current levels &mdash; which it has not approached in any year since 2019.</p>
</div>

<div class="fair-note">
  <strong class="head">On cost recovery</strong>
  Public-safety programs are not generally expected to pay for themselves through fees &mdash; police patrols, fire response, and park rangers all run at a net cost by design, and that is a legitimate use of public money. Cost recovery is included here as one measurable input, not as a standard the program is failing to meet. The question this page raises is narrower: the program's cost is rising while its measurable output falls and its offense mix shows no shift away from first-time violations &mdash; and that combination is worth examining before doubling the program's size. Policy recommendations are on the <a href="opinion.html">opinion page</a>; this page stays with the data.
</div>

<!-- ============ FINDING 02 — TEMPORAL ARC ============ -->
<h2 class="finding" id="finding-02"><span class="num">Finding 02</span><span>The arc: 2016 build-up, COVID crater, 2026 expansion.</span></h2>
<p class="lead">Annual DLP citations rose roughly seven-fold from 2014 to 2018 after the April 2016 Animal Control Officer + paired Facilities Maintenance Worker team went full-time. Output cratered during the COVID period and has not returned to anything near peak. The shaded box at right shows the range of plausible 2027&ndash;2028 output if the announced 2026 expansion (roughly double the staffing) is fully deployed.</p>

<div class="chart-block">
  <div class="chart-title">Annual DLP citations, 2014&ndash;2026, with projected 2027&ndash;2028 range</div>
  <div class="chart-subtitle">Orange bars: actual DLP citations. 2026 (lighter) is partial-year through April 17; the dashed marker shows its annualized full-year equivalent (~222). The shaded box at right is the 2027&ndash;2028 projection range at the announced 4-FTE staffing &mdash; floor = current (2024) per-officer rate, ceiling = 2018 peak rate. COVID period shaded.</div>
  <div class="chart-wrap"><canvas id="chartYearTrend" role="img" aria-label="Bar chart of DLP citations per year 2014-2026 with COVID shading and a 2027-2028 projection range box."></canvas></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; projection staffing baselines: 2016 MOA, 2021 MOA, Axios Seattle April 2026</div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Three phases are visible. The 2016&ndash;2019 build-up: citations climbed from 183 (2014) to a 1,276 peak (2018). The COVID-era crater: 2020 fell to 393 (&minus;67% from 2019), and output has not recovered &mdash; the strongest year since the COVID period (2024) reached 447, about a third of peak. The 2026 expansion: doubling staffing produces a projected 2027&ndash;2028 range of roughly 894 citations/year (if per-officer output stays at the 2024 rate) to 2,552/year (if it returns to the 2018 peak rate). Per-officer output has not exceeded ~225 in any year since 2019, so the lower half of that range is the more likely outcome absent a change in approach.</p>
</div>

<!-- ============ FINDING 03 — DETERRENCE ============ -->
<h2 class="finding" id="finding-03"><span class="num">Finding 03</span><span>No measurable shift away from first-time offenders.</span></h2>
<p class="lead">If enforcement were deterring repeat violations, the share of citations going to people cited before would be expected to grow over time as a stable population of repeat offenders accumulates contacts. Instead, first-time offenses have stayed the overwhelming majority every year &mdash; and their share has risen, not fallen.</p>

<div class="chart-block">
  <div class="chart-title">First-offense share of DLP citations, 2014&ndash;2026</div>
  <div class="chart-subtitle">Share of each year's DLP citations that are first offenses (vs. 2nd, 3rd, or 4th+ under SMC 18.12.080's escalation schedule). COVID period shaded. 2026 partial-year.</div>
  <div class="chart-wrap short"><canvas id="chartFirstOffense" role="img" aria-label="Line chart of first-offense share of DLP citations per year, consistently 85-96%."></canvas></div>
  <div class="chart-source">Source: offense levels in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; <a href="https://library.municode.com/wa/seattle/codes/municipal_code?nodeId=TIT18PALA_CH18.12GEPRRE_SUBCHAPTER_IIOFPRPA_18.12.080DORELI">SMC 18.12.080(A)</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>First offenses have ranged from about 84% to 96% of DLP citations in every year of the record, rising over time rather than falling. One reading is that enforcement is deterring repeat offenses. A second reading is that lower total citation volume mechanically reduces the chance of an officer encountering the same person twice, which would push the first-offense share up regardless of behavior. The two cannot be separated here: neither PRR includes owner identifiers that would let us track individuals across citations. What the data does show is that the offense mix never shifted toward repeat offenders &mdash; the pattern is consistent with a program issuing fresh first-time contacts year after year, not one drawing down a shrinking pool of repeat violators. SPR's own 2016 owner survey found 39% of dog owners admit weekly-to-monthly illegal off-leash use; no follow-up survey has been published (see <a href="#gap">what SPR has not measured</a>).</p>
</div>

<div class="supporting" id="per-fte-supporting">
  <p class="supporting-title">Citations per officer-FTE per year</p>
  <p class="supporting-note">A productivity view of the same record: DLP citations divided by the total ACO+FMW FTE attributable to off-leash enforcement. Shown from 2016 on (the MOA-documented full-team era); pre-2016 part-time FTE is imputed and not directly comparable. Among these years, per-FTE output peaked at 638 in 2018 and fell to 224 by 2024 &mdash; about a third of peak. 2026 partial-year excluded.</p>
  <div class="chart-wrap"><canvas id="chartPerFTE" role="img" aria-label="Line chart of DLP citations per officer-FTE per year, peaking at 638 in 2018."></canvas></div>
</div>

<!-- ============ FINDING 04 — GEOGRAPHY ============ -->
<h2 class="finding" id="finding-04"><span class="num">Finding 04</span><span>Enforcement concentrates in a few large parks.</span></h2>
<p class="lead">Citations are not spread evenly across the city. A small number of large, heavily-used parks account for most citations in every year. The records do not say <em>why</em> these parks were chosen &mdash; whether because violations concentrate there, because patrols were directed there, or both.</p>

<div class="map-block">
  <div class="chart-title">Where off-leash citations were issued, 2014&ndash;2026</div>
  <div class="chart-subtitle">Circles sized by DLP citation count at the cited park. Green dots mark all 14 existing OLAs. Hover a marker for details.</div>
  <div id="hotspot-map" role="img" aria-label="Map of Seattle off-leash citation hotspots 2014 to 2026 with existing OLA locations overlaid."></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; coordinates <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/park-coordinates.csv">park-coordinates.csv</a> (approximate) &middot; tiles: <a href="https://carto.com/">CARTO</a> / <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a></div>
</div>

<div class="chart-block">
  <div class="chart-title">Top 20 cited parks: pre-COVID (2014&ndash;2019) vs post-COVID (2020&ndash;2026)</div>
  <div class="chart-subtitle">Orange bars: 2014&ndash;2019 DLP citations. Navy bars: 2020&ndash;2026 DLP citations. Parks ordered by combined total.</div>
  <div class="chart-wrap tall"><canvas id="chartPersistence" role="img" aria-label="Paired bar chart: top 20 cited parks pre-COVID vs post-COVID."></canvas></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-by-park-year.csv">enforcement-by-park-year.csv</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Citations cluster where designated OLAs aren't. Discovery, Volunteer, Cal Anderson, Lincoln, Martha Washington, Wallingford Playfield, Seward, and Maple Leaf Reservoir all rank in the top 20 and none has a dedicated OLA on site. Magnuson and Westcrest appear as hotspots because the non-OLA portions of those large host parks are used off-leash. The top 10 parks accounted for 46% of citations before COVID and 40% after &mdash; concentration eased somewhat but the same handful of parks still dominate. <strong>The data records where citations were issued, not why officers were there</strong>, so it cannot establish whether a given park is a hotspot because of higher violation rates or because patrols were directed to it. One post-COVID shift is worth noting without over-reading: West Queen Anne Playfield is the only top-10 pre-COVID park whose citation volume did not fall with the citywide decline &mdash; consistent with enforcement attention following community complaints in that area, though the data alone cannot confirm the cause.</p>
</div>

<!-- ============ FINDING 05 — WALKSHED GAP ============ -->
<h2 class="finding" id="finding-05"><span class="num">Finding 05</span><span>Citation density vs. walkable OLA coverage.</span></h2>
<p class="lead">Overlaying citation density on the half-mile walksheds around every existing OLA (the <a href="https://www.tpl.org/parkscore/about">Trust for Public Land 10-minute-walk standard</a>) shows citation activity concentrating in areas without walkable OLA coverage.</p>

<div class="map-block">
  <div class="chart-title">Citation density and 0.5-mile OLA walksheds</div>
  <div class="chart-subtitle">Heat = DLP citation density (kernel density across geocoded park locations, weighted by count). Green rings = 0.5-mile walksheds around each of the 14 OLAs. Green dots = OLA locations. Grey dots = neighborhood reference points.</div>
  <div id="gap-map" role="img" aria-label="Heatmap of off-leash citation density with 0.5-mile OLA walksheds overlaid."></div>
  <div class="chart-source">Sources: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/seattle-olas.csv">seattle-olas.csv</a> &middot; walksheds per <a href="https://www.tpl.org/parkscore/about">TPL ParkScore</a> &middot; <a href="https://github.com/Leaflet/Leaflet.heat">Leaflet.heat</a> &middot; tiles: <a href="https://carto.com/">CARTO</a> / <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Citation density concentrates outside OLA walksheds. North of the Ship Canal &mdash; Wallingford, Ravenna, Maple Leaf, Green Lake, Laurelhurst &mdash; shows heavy density with little walkable OLA coverage. The Queen Anne / Magnolia core has Kinnear (0.124 acre) and Magnolia Manor (0.48 acre), both below the <a href="https://images.akc.org/pdf/GLEG01.pdf">AKC one-acre minimum</a>, and a citation band through Discovery, West Queen Anne Playfield, and Smith Cove. Lincoln Park (West Seattle) carries 173 cumulative citations; the nearest OLA, Westcrest, is <a href="https://www.openstreetmap.org/directions?from=47.5300%2C-122.3936&to=47.5262%2C-122.3574">3.4 miles</a> away.</p>
</div>

<!-- ============ FINDING 06 — TABLE ============ -->
<h2 class="finding" id="finding-06"><span class="num">Finding 06</span><span>The full top-20 table.</span></h2>
<table class="data">
  <thead><tr><th class="num">Rank</th><th>Park</th><th>Neighborhood</th><th class="num">Total 2014&ndash;2026</th><th class="num">Pre-COVID</th><th class="num">Post-COVID</th><th>OLA?</th></tr></thead>
  <tbody id="topTable"></tbody>
</table>

<!-- ============ GAP CALLOUT ============ -->
<div class="gap-callout" id="gap">
  <strong class="head">What SPR has not measured</strong>
  <p>Citation counts measure <em>enforcement activity</em>, not underlying violation rates. A drop in citations could mean fewer violations <em>or</em> fewer patrols. SPR's 2016 <em>People, Dogs and Parks</em> owner survey found 39% of dog owners admit weekly-to-monthly illegal off-leash use; <strong>no follow-up survey has been published.</strong> The 2026 staffing expansion is being implemented without a publicly-released review of the 2016 expansion's effect on behavior. Pending public-records requests that would help close these gaps:</p>
  <ul>
    <li>SPR program evaluation, deployment logs, and 2026 expansion decision record (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/prrs/08-spr-program-evaluation-2016-expansion.md">PRR #8</a>, filed; SPR responding)</li>
    <li>Find-It-Fix-It &ldquo;dog in a park&rdquo; complaints by year &mdash; an independent behavior proxy (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/prrs/02-spu-fifi-dog-complaints.md">PRR #2</a>, pending)</li>
    <li>Current SPR/SAS MOA and 2026 budget lines for the expanded staffing (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/prrs/07-spr-fas-aco-staffing-expansion.md">PRR #7</a>, partial &mdash; CBO closed with no records; SPR responding)</li>
  </ul>
  <p>Until these land, this page can describe enforcement output and cost but cannot prove or disprove that the program changed behavior. Policy implications are discussed on the <a href="opinion.html">opinion page</a>.</p>
</div>

<!-- ============ FOOTNOTES ============ -->
<div class="footnotes">
  <h3>Source &amp; method</h3>
  <p>Citation records come from two Seattle public records requests. <strong>C049204</strong> (filed 2019-08-29, produced 2019-10-15 by SPR) covers Dog Loose in Park citations 2014-01-01 through 2019-10-15. <strong>C263949</strong> (filed 2026-04-17, produced May 2026 by Seattle FAS) covers all parks-related violations 2019-01-01 through 2026-04-17. Raw files and documenting READMEs are at <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/"><code>data/prr-responses/</code></a>. The consolidated CSV (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv"><code>enforcement-citations.csv</code></a>) is built by <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/scripts/build_enforcement_datasets.py"><code>build_enforcement_datasets.py</code></a> and checked by <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/scripts/verify_enforcement_data.py"><code>verify_enforcement_data.py</code></a>.</p>

  <h3>Why DLP-only, and the 2019 overlap</h3>
  <p>This page restricts to Dog Loose in Park citations across both requests so each year is measured identically. C263949's broader categories (license, scoop, permit-at-large, etc. &mdash; 517 additional post-2019 rows) stay in the consolidated CSV under <code>violation_category</code> but are not in the year series. Both PRRs contain 2019: C049204 ends 2019-10-15 (partial), C263949 covers the full year. The build uses C263949's full-year 2019 as authoritative, so the rebuilt 2019 figure (1,181 DLP) is higher than the legacy site's 1,029 (which was Jan&ndash;Oct only).</p>

  <h3>2026 is a partial year</h3>
  <p>C263949 ends April 17, 2026 &mdash; day 107 of the year, about 29%. Charts mark 2026 as partial. Where a full-year comparison is needed, the annualized equivalent (YTD &divide; 0.293) is shown as a dashed marker, not treated as actual. The cost-per-citation and per-FTE lines stop at 2025 to avoid the partial-year denominator inflating the most recent point.</p>

  <h3>Headcount &amp; cost assumptions</h3>
  <p>Annual ACO+FMW FTE attributable to off-leash enforcement: 0.5 ACO (2014&ndash;2015, imputed from PRR context); 0.75 ACO + 0.75 FMW for the 2016 transition year; 1.0 ACO + 1.0 FMW (2017&ndash;2025, per the 2016 and 2021 MOAs); doubling to 2.0 ACO under the 2026 expansion. FAS-side ACO II cost = <strong>$152,399/yr</strong> (sourced, 2021 MOA Attachment A). FMW pairing = <strong>$140,000/yr</strong> (author estimate; SPR does not publish a per-FMW off-leash line). The exact 2026 MOA terms are pending <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/prrs/07-spr-fas-aco-staffing-expansion.md">PRR #7</a>. Pre-2016 and 2016-transition FTE are the softest assumptions here and are flagged accordingly.</p>

  <h3>Location quality</h3>
  <p>Of the 7,015 DLP citations, about 89% are confidently attributable to a named park (top contributors: Discovery 564, Magnuson 367, Volunteer 328, Woodland 291, Golden Gardens 227). The rest are street-address citations (geocoded separately, used in the Finding 05 heatmap) or blank locations (excluded from spatial analysis). Park-name canonicalization is documented in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/METHODOLOGY.md">METHODOLOGY.md</a>.</p>
</div>

<nav class="paginate">
  <a href="part3.html" class="prev"><span class="kicker">&larr; Previous</span><span class="title">Part III &mdash; Forward</span></a>
  <a href="budget.html" class="next"><span class="kicker">Next &rarr;</span><span class="title">Budget</span></a>
</nav>

<footer>
  <p>Data current as of May 2026 (PRR C263949 ingest). Source code and all underlying data: <a href="https://github.com/avrignaud/seattledogparkdata">github.com/avrignaud/seattledogparkdata</a>. MIT license covers author-written code and analysis; primary data is public record. Corrections: <a href="https://github.com/avrignaud/seattledogparkdata/issues">issue tracker</a>.</p>
</footer>

</div></main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
<script src="chart-defaults.js"></script>
<script src="site-data.js"></script>
<script>
const D = __DATA__;
const P = SDPD.palette;
const FONT = "'Inter', sans-serif";
const FONT_MONO = "'IBM Plex Mono', monospace";

const covidAnn = () => ({
  type: 'box', xMin: 5.5, xMax: 7.5,
  backgroundColor: 'rgba(139, 37, 24, 0.10)', borderWidth: 0, drawTime: 'beforeDatasetsDraw',
  label: { display: true, content: 'COVID', position: { x: 'center', y: 'start' }, yAdjust: 4,
    backgroundColor: 'transparent', color: 'rgba(139, 37, 24, 0.85)',
    font: { family: FONT_MONO, size: 11, weight: '600' } }
});

const fullYears = D.full_years; // 2014-2025

// ===== Finding 01 — cost per citation lead (volume bars + cost/cit line), full years =====
(function() {
  const yt = D.year_trend.filter(t => t.year !== '2026');
  // Cost-per-citation line begins 2016 (documented MOA cost basis); pre-2016
  // part-time cost is imputed and would create a misleading low point in 2015.
  const costLine = yt.map(t => parseInt(t.year) >= 2016 ? t.cost_per_citation : null);
  new Chart(document.getElementById('chartCostPerCit'), {
    type: 'bar',
    data: { labels: yt.map(t => t.year), datasets: [
      { label: 'DLP citations (left axis)', data: yt.map(t => t.dlp), backgroundColor: P.sage, yAxisID: 'y' },
      { label: 'Cost per citation $, 2016+ (right axis)', data: costLine, spanGaps: false,
        type: 'line', borderColor: P.orange, backgroundColor: P.orange, tension: 0.18, pointRadius: 4, borderWidth: 2.5, fill: false, yAxisID: 'y1' }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } }, annotation: { annotations: { covid: covidAnn() } } },
      scales: {
        x: { ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { position: 'left', title: { display: true, text: 'DLP citations', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } } },
        y1: { position: 'right', title: { display: true, text: '$ per citation', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 }, callback: v => '$' + v.toLocaleString() }, grid: { drawOnChartArea: false } }
      } }
  });
})();

// ===== Finding 02 — year trend with COVID + 2027-28 projection region =====
(function() {
  const labels = D.years.concat(['2027', '2028']); // 2014..2026,2027,2028
  const actual = labels.map(y => {
    const t = D.year_trend.find(x => x.year === y);
    return t ? t.dlp : null;
  });
  const idx2026 = labels.indexOf('2026');
  const barColors = labels.map((y,i) => i === idx2026 ? 'rgba(209,72,26,0.45)' : P.orange);
  // 2026 annualized dashed marker (within historical scale)
  const annualized2026 = labels.map(y => y === '2026' ? D.y2026.dlp_annualized : null);
  const projLow = D.projection.low_2027_28, projHigh = D.projection.high_2027_28;

  // COVID region box
  const covid = covidAnn();
  // Projection region box (2027-2028), shaded like COVID, with the numeric
  // range as a text label. We do NOT draw full-height floating bars for the
  // projection: the high case (~2,552) is 2x the historical peak (1,276) and
  // would blow out the y-axis, making the actual data unreadable and giving a
  // speculative figure undue visual weight. The shaded region + label conveys
  // "future zone, projected range" honestly without distorting the scale.
  const projBox = { type: 'box', xMin: idx2026 + 0.5, xMax: idx2026 + 2.5,
    backgroundColor: 'rgba(31,58,95,0.07)', borderWidth: 0, drawTime: 'beforeDatasetsDraw',
    label: { display: true,
      content: ['Projected 2027–28', `${projLow.toLocaleString()}–${projHigh.toLocaleString()}/yr`, '(2× staffing)'],
      position: { x: 'center', y: 'center' },
      backgroundColor: 'transparent', color: 'rgba(31,58,95,0.85)',
      font: { family: FONT_MONO, size: 10, weight: '600' } } };
  // Low-case projection reference line (visible within scale)
  const projLowLine = { type: 'line', yMin: projLow, yMax: projLow,
    xMin: idx2026 + 0.5, xMax: idx2026 + 2.5,
    borderColor: 'rgba(31,58,95,0.55)', borderWidth: 2, borderDash: [4,3], drawTime: 'beforeDatasetsDraw' };

  new Chart(document.getElementById('chartYearTrend'), {
    type: 'bar',
    data: { labels, datasets: [
      { label: 'DLP citations (actual; 2026 partial-year)', data: actual, backgroundColor: barColors, order: 2 },
      { label: '2026 annualized estimate (YTD ÷ 0.29)', data: annualized2026, type: 'scatter',
        pointStyle: 'line', pointRadius: 12, borderColor: P.inkSoft, borderWidth: 2, borderDash: [3,3], order: 1 }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } },
        annotation: { annotations: { covid, proj: projBox, projLow: projLowLine } } },
      scales: {
        x: { ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { title: { display: true, text: 'DLP citations', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } }, beginAtZero: true, suggestedMax: 1400 }
      } }
  });
})();

// ===== Finding 03 — first-offense share =====
(function() {
  const r = D.first_offense_share;
  new Chart(document.getElementById('chartFirstOffense'), {
    type: 'line',
    data: { labels: r.map(t => t.year), datasets: [
      { label: '% of DLP citations that are first offenses', data: r.map(t => t.pct_first),
        borderColor: P.gold, backgroundColor: P.gold, tension: 0.18, pointRadius: 4, borderWidth: 2.5, fill: false }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } }, annotation: { annotations: { covid: covidAnn() } } },
      scales: {
        x: { ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { title: { display: true, text: '% first offenses', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 }, callback: v => v + '%' }, min: 70, max: 100 }
      } }
  });
})();

// ===== Finding 03 supporting — per-FTE (full years) =====
(function() {
  // Per-FTE: 2016+ only (documented full-team era); pre-2016 imputed FTE excluded.
  const yt = D.year_trend.filter(t => t.year !== '2026' && parseInt(t.year) >= 2016);
  new Chart(document.getElementById('chartPerFTE'), {
    type: 'line',
    data: { labels: yt.map(t => t.year), datasets: [
      { label: 'DLP citations per total-FTE', data: yt.map(t => t.per_total_fte),
        borderColor: P.orange, backgroundColor: P.orange, tension: 0.18, pointRadius: 4, borderWidth: 2.5, fill: false },
      { label: '2018 peak (638)', data: yt.map(() => 638), borderColor: P.inkSoft, borderDash: [4,4], borderWidth: 1, pointRadius: 0 }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } }, annotation: { annotations: { covid: covidAnn() } } },
      scales: {
        x: { ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { title: { display: true, text: 'Citations / FTE', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } } }
      } }
  });
})();

// ===== Finding 04 — persistence paired bars =====
(function() {
  const t = D.top20_full;
  new Chart(document.getElementById('chartPersistence'), {
    type: 'bar',
    data: { labels: t.map(p => p.park), datasets: [
      { label: 'Pre-COVID (2014–2019)', data: t.map(p => p.pre), backgroundColor: P.orange },
      { label: 'Post-COVID (2020–2026)', data: t.map(p => p.post), backgroundColor: P.navy }
    ]},
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } } },
      scales: {
        y: { ticks: { font: { family: FONT, size: 12 } }, grid: { display: false } },
        x: { title: { display: true, text: 'DLP citations', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } } }
      } }
  });
})();

// ===== Finding 06 — top 20 table =====
(function() {
  const tbody = document.getElementById('topTable');
  const olaCell = (s) => s === 'has' ? '<td class="ola-yes">Yes</td>' : s === 'partial' ? '<td class="ola-partial">Partial</td>' : s === 'planned' ? '<td class="ola-planned">Planned</td>' : '<td class="ola-no">No</td>';
  D.top20_full.forEach((p, i) => {
    tbody.insertAdjacentHTML('beforeend', `<tr><td class="num">${i+1}</td><td>${p.park}</td><td>${p.neighborhood||'—'}</td><td class="num">${p.count.toLocaleString()}</td><td class="num">${p.pre.toLocaleString()}</td><td class="num">${p.post.toLocaleString()}</td>${olaCell(p.ola_status)}</tr>`);
  });
})();

// ===== Maps =====
(async function maps() {
  const csv = await SDPD.data.loadAll({ olas: 'data/seattle-olas.csv', neighborhoods: 'data/neighborhood-centers.csv' });
  const OLAS = csv.olas.map(o => ({ name: o.ola_name, lat: parseFloat(o.latitude), lng: parseFloat(o.longitude), acres: parseFloat(o.acres) }));
  const NEIGH = csv.neighborhoods.map(n => ({ name: n.name, lat: parseFloat(n.latitude), lng: parseFloat(n.longitude) }));
  const CENTER = [47.6300, -122.3500];
  const HOTSPOTS = D.top20_full.filter(h => h.lat && h.lng);
  const EXTRA = D.top21_40.filter(h => h.lat && h.lng);
  const fill = s => s === 'has' ? P.sage : s === 'partial' ? P.gold : s === 'planned' ? P.inkFaint : P.orange;

  function legend(rows) {
    const c = L.control({ position: 'topright' });
    c.onAdd = () => { const d = L.DomUtil.create('div', 'sdpd-map-legend'); d.innerHTML = rows; return d; };
    return c;
  }

  // Map 1 — hotspots
  const m1 = L.map('hotspot-map', { scrollWheelZoom: false }).setView(CENTER, 11);
  L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png', { attribution: '© OpenStreetMap © CARTO', subdomains: 'abcd', maxZoom: 18 }).addTo(m1);
  OLAS.forEach(o => L.circleMarker([o.lat, o.lng], { radius: 4, fillColor: P.sage, fillOpacity: 0.95, color: '#fff', weight: 1.5 }).bindTooltip(`<strong>${o.name}</strong><br>${o.acres} ac OLA`).addTo(m1));
  HOTSPOTS.forEach(h => L.circleMarker([h.lat, h.lng], { radius: Math.sqrt(h.count)*1.1 + 4, fillColor: fill(h.ola_status), fillOpacity: 0.5, color: '#fff', weight: 1.5 }).bindTooltip(`<strong>${h.park}</strong><br>${h.count} DLP citations · ${h.neighborhood}`).addTo(m1));
  legend(`<div class="hdr">Legend</div>
    <div class="row"><span class="dot" style="background:${P.sage}"></span> Existing OLA</div>
    <div class="row"><span class="dot" style="background:${P.orange}"></span> Cited park — no OLA</div>
    <div class="row"><span class="dot" style="background:${P.gold}"></span> Cited park — partial OLA</div>
    <div class="row"><span class="dot" style="background:${P.inkFaint}"></span> Planned OLA</div>
    <div class="row" style="margin-top:4px;color:var(--ink-faint)">Circle size = citation count</div>`).addTo(m1);

  // Map 2 — walkshed gap
  const m2 = L.map('gap-map', { scrollWheelZoom: false }).setView(CENTER, 11);
  L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png', { attribution: '© OpenStreetMap © CARTO', subdomains: 'abcd', maxZoom: 18 }).addTo(m2);
  OLAS.forEach(o => { L.circle([o.lat, o.lng], { radius: 804.67, fillColor: P.sage, fillOpacity: 0.08, color: P.sage, weight: 1 }).addTo(m2); L.circleMarker([o.lat, o.lng], { radius: 4, fillColor: P.sage, fillOpacity: 1, color: '#fff', weight: 1 }).addTo(m2); });
  L.heatLayer([...HOTSPOTS, ...EXTRA].map(h => [h.lat, h.lng, h.count]), { radius: 28, blur: 22, gradient: {0.2:'#F5B78E',0.5:'#E07839',0.8:'#B83F14',1:'#6E1A0E'} }).addTo(m2);
  NEIGH.forEach(n => L.circleMarker([n.lat, n.lng], { radius: 2, color: P.inkFaint, fillOpacity: 0.4 }).bindTooltip(n.name).addTo(m2));
  legend(`<div class="hdr">Legend</div>
    <div class="row"><span class="heat-grad"></span> Citation density</div>
    <div class="row"><span class="ring"></span> 0.5-mi OLA walkshed</div>
    <div class="row"><span class="dot" style="background:${P.sage}"></span> OLA location</div>
    <div class="row"><span class="dot" style="background:${P.inkFaint}"></span> Neighborhood reference</div>`).addTo(m2);
})();
</script>

</body>
</html>
'''
HTML = HTML.replace('__DATA__', DATA_JS)
out = ROOT / "docs" / "enforcement-draft.html"
out.write_text(HTML)
print(f"Wrote {out} ({len(HTML):,} chars)")

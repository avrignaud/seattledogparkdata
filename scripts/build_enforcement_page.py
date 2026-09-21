#!/usr/bin/env python3
"""
Build docs/enforcement.html from scripts/enforcement_page_data.json.

Generator for the production enforcement page (2014–2026 record, post-PRR
C263949 ingest). The page data is itself derived from the consolidated CSV, so
every number on the page is reproducible from committed scripts and checked by
scripts/verify_enforcement_data.py.

Run from repo root:  .venv/bin/python scripts/build_enforcement_page.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "scripts" / "enforcement_page_data.json"))
DATA_JS = json.dumps(D)

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>13 years of off-leash enforcement: rising cost, falling output — Seattle Dog Park Data</title>
<meta name="description" content="Seattle's off-leash dog enforcement program 2014–2026: where citations were issued, what the program costs, and whether the available data shows it reducing violations.">
<meta property="og:title" content="13 years of off-leash enforcement: rising cost, falling output">
<meta property="og:description" content="Seattle's off-leash enforcement, 2014–2026: contacts peaked in 2018, actual citations fell 95% by 2024, the City billed for three officers it did not field, and nobody has measured whether any of it changes behavior.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://seattledogparkdata.com/enforcement">
<meta property="og:site_name" content="Seattle Dog Park Data">
<meta property="og:image" content="https://seattledogparkdata.com/images/enforcement-card.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://seattledogparkdata.com/images/enforcement-card.png">
<link rel="canonical" href="https://seattledogparkdata.com/enforcement">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
<link rel="stylesheet" href="site.css?v=f49414dc">
<style>
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
  .sdpd-map-legend { background: rgba(250,248,243,0.96); border: 1px solid var(--rule); border-radius: 10px; padding: 10px 12px; font-family: 'IBM Plex Sans', sans-serif; font-size: 12px; line-height: 1.7; color: var(--ink); box-shadow: 0 6px 20px -10px rgba(26,23,18,0.18); }
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
  .gap-callout { background: rgba(139, 37, 24, 0.07); border: 1px solid var(--rule); padding: 18px 22px; margin: 22px 0; border-radius: 12px; font-size: 14.5px; line-height: 1.6; }
  .gap-callout strong.head { display: block; color: var(--danger); font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }
  .gap-callout ul { margin: 10px 0 0 22px; padding: 0; }
  .gap-callout li { margin-bottom: 4px; }
  .fair-note { background: var(--navy-soft); border: 1px solid var(--rule); padding: 18px 22px; margin: 18px 0; border-radius: 12px; font-size: 14px; line-height: 1.6; }
  .fair-note p { max-width: 86ch; }
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
    <a href="data-methods.html">Data &amp; Methods</a>
    <a href="updates.html">Updates</a>
  </nav>
</div>

<div class="masthead">
  <span class="dateline">Enforcement &middot; seattledogparkdata.com</span>
  <span>UPDATED SEPTEMBER 2026</span>
</div>

<header class="hero">
  <h1 class="hed">13 years of off-leash enforcement in Seattle: <em>rising cost, falling output</em>.</h1>
  <p class="deck">Seattle Animal Control's records cover 13 years of off-leash (&ldquo;Dog Loose in Park,&rdquo; DLP) enforcement: 7,015 contacts, of which 3,151 were citations and 3,191 verbal warnings. Contacts peaked in 2018 and never recovered; actual citations fell 95% from 2018 to 2024. From 2023 the City was billed for three officers on invoices computed from a calendar, while the staffing agency reported it could field one and a half to two. And in ten years the City has produced no evaluation of whether any of it changes behavior: both agencies, asked directly, hold none.</p>
  <div class="byline">Source: Seattle Animal Control PRRs <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C049204">C049204</a> (2014&ndash;2018) and <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C263949">C263949</a> (2019&ndash;2026-04-17) &middot; staffing and cost: the <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/moas">2016, 2021, 2023, 2025 and 2026 Memoranda of Agreement (MOAs)</a> and the SPR decision record and ledger backup in <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C266465">PRR C266465</a> &middot; deployment status: <a href="https://www.axios.com/local/seattle/2026/04/17/seattle-animal-control-staffing-increase-off-leash-dogs-parks-enforcement">Axios Seattle, April 2026</a> &middot; coordinates approximate from park names</div>
</header>

<!-- ============ COST-FRAMING CONTEXT (top, sets the frame) ============ -->
<div class="fair-note" id="cost-context" style="border-left-color: var(--navy);">
  <strong class="head">Three numbers that are easy to conflate: funded, billed, deployed.</strong>
  <p><strong>Funded.</strong> The Seattle Park District approved three park-patrol officers in <strong>2023</strong>, a maximum of $454,652/year, re-priced to <strong>$528,279</strong> by the 2026 MOA. <strong>Billed.</strong> The 2023 agreement charged a flat 240 hours per pay period for three officers regardless of hours worked, and SPR's ledger shows it paid accordingly: <strong>$456,173 in 2024</strong> and $226,528 in the first half of 2023, on invoices built from the number of weekdays in each month (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/documents/enforcement-moa-billing.csv">PRR C266465 ledger</a>). Only the 2025 MOA switched to billing on actual hours. <strong>Deployed.</strong> Seattle Animal Shelter told SPR in February 2025 it could commit "closer to 2 FTEs," possibly 1.5 (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/README.md">Bates 00541</a>); as of April 2026 SPR said one officer was working parks with two still being hired (<a href="https://www.axios.com/local/seattle/2026/04/17/seattle-animal-control-staffing-increase-off-leash-dogs-parks-enforcement">Axios</a>); and parks are a minority of these officers' work (33% of calls in 2021). The maintenance worker the program was designed to pair with each officer left in 2023 and was never replaced (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/README.md">SPR memo, Sept 2024</a>).</p>
  <p style="margin:10px 0 0;">So for 2023&ndash;24 the City paid for three officers it did not field. Through July 2026 this page said the three-officer ceiling had not been reached; the ledger released that month shows it was exceeded in 2024. The funded-versus-deployed gap is real; the money was spent anyway. Wherever this page shows program cost, 2023&ndash;24 is what SPR was billed, and every other year is the one-officer deployment model described in the <a href="data-methods.html#headcount-cost">cost note</a>.</p>
</div>

<section>
  <div class="stats">
    <div class="stat orange">
      <div><div class="label">Off-leash enforcement records, 2014&ndash;2026</div><div class="num">7,015</div></div>
      <div class="note">&ldquo;Dog Loose in Park&rdquo; (DLP) contacts: <strong>3,151 citations</strong>, <strong>3,191 verbal warnings</strong>, 673 blank, voided or dismissed. Warnings appear in the record only from 2018. <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">src</a></div>
    </div>
    <div class="stat gold">
      <div><div class="label">First-time offenders, every year</div><div class="num">84&ndash;96<span class="unit">%</span></div></div>
      <div class="note">Share of citations that are 1st offenses. The mix never shifted toward repeat offenders.</div>
    </div>
    <div class="stat orange">
      <div><div class="label">Actual citations, 2018 &rarr; 2024</div><div class="num">&minus;95<span class="unit">%</span></div></div>
      <div class="note">441 citations in 2018, 21 in 2024, 23 in 2025. Total contacts fell less (1,276 &rarr; 447, then 267) because most contacts now end in a verbal warning.</div>
    </div>
    <div class="stat navy">
      <div><div class="label">Billed for 3 officers in 2024</div><div class="num">$456<span class="unit">K</span></div></div>
      <div class="note">$456,173 on calendar-derived invoices, while the staffing agency said it could field 1.5&ndash;2 and about one worked parks. See the cost note above.</div>
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

<!-- ============ PLAIN-LANGUAGE SUMMARY ============ -->
<div class="takeaway" id="summary" style="border-left-color: var(--orange);">
  <span class="kicker">What this page found</span>
  <ul style="margin:8px 0 0; padding-left:20px; line-height:1.65;">
    <li><strong>Contacts fell and never recovered; actual citations collapsed.</strong> Off-leash (&ldquo;Dog Loose in Park&rdquo;) contacts peaked at 1,276 in 2018; the best year since (2024) reached 447. Citations, as distinct from verbal warnings, went from 441 to 21. <a href="#finding-01">&darr; cost and output</a></li>
    <li><strong>Cost per citation keeps rising.</strong> Fee revenue ($294,885 over 13 years) has covered ~9% of the program&rsquo;s ~$3.38M cost; the cost per contact ran $229 in 2018 and $1,021 in 2024, and the cost per actual citation $663 and $21,723. <a href="#finding-01">&darr; cost and output</a></li>
    <li><strong>The city paid for three officers it did not field.</strong> Billed $456,173 in 2024 on calendar-derived invoices for three officers; the staffing agency said it could supply 1.5&ndash;2. <a href="#finding-02">&darr; funded, billed, deployed</a></li>
    <li><strong>Officers can&rsquo;t compel ID, so most contacts end in a warning</strong>, which caps citation output no matter how many officers patrol. <a href="#finding-02">&darr; funded, billed, deployed</a></li>
    <li><strong>Contacts cluster where there&rsquo;s no nearby legal off-leash area</strong>, and residents now file about 11 complaints for every contact. <a href="#finding-04">&darr; geography and complaints</a></li>
    <li><strong>Nobody has measured whether any of it works.</strong> Asked directly, neither SPR nor the Animal Shelter holds an evaluation; the one internal review recommended cutting the program, and leadership overrode it. <a href="#gap">&darr; what the City never measured</a></li>
  </ul>
</div>

<!-- ============ FINDING 05 — WALKSHED GAP (hero map; id kept for back-compat) ============ -->
<h2 class="finding" id="finding-05">Enforcement concentrates in the areas without a walkable off-leash area.</h2>
<p class="lead">The clearest single picture of this program. Citation density is overlaid on the half-mile walksheds around every existing off-leash area (OLA), the <a href="https://www.tpl.org/parkscore/about">Trust for Public Land 10-minute-walk standard</a>. The heat sits where the coverage does not. Everything after this section is the cost, the output and the record behind it.</p>

<div class="map-block">
  <div class="chart-title">Citation density and 0.5-mile OLA walksheds</div>
  <div class="chart-subtitle">Heat = DLP citation density (a smoothed heat surface across geocoded park locations, weighted by citation count). Green rings = 0.5-mile walksheds around each of the 14 OLAs. Green dots = OLA locations. Grey dots = neighborhood reference points.</div>
  <div id="gap-map" role="img" aria-label="Heatmap of off-leash citation density with 0.5-mile OLA walksheds overlaid."></div>
  <div class="chart-source">Sources: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/seattle-olas.csv">seattle-olas.csv</a> &middot; walksheds per <a href="https://www.tpl.org/parkscore/about">TPL ParkScore</a> &middot; <a href="https://github.com/Leaflet/Leaflet.heat">Leaflet.heat</a> &middot; tiles: <a href="https://www.esri.com/">Esri</a> / <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Citation density concentrates outside OLA walksheds. North of the Ship Canal (Wallingford, Ravenna, Maple Leaf, Green Lake and Laurelhurst) shows heavy density with little walkable OLA coverage. The Queen Anne / Magnolia core has Kinnear (0.124 acre) and Magnolia Manor (0.48 acre), both below the <a href="https://images.akc.org/pdf/GLEG01.pdf">AKC one-acre minimum</a>, and a citation band through Discovery, West Queen Anne Playfield, and Smith Cove. Lincoln Park (West Seattle) carries 173 cumulative citations; the nearest OLA, Westcrest, is <a href="https://www.openstreetmap.org/directions?from=47.5300%2C-122.3936&to=47.5262%2C-122.3574">3.4 miles</a> away.</p>
</div>

<!-- ============ FINDING 01 — FISCAL LEAD ============ -->
<h2 class="finding" id="finding-01">Contacts fell, citations collapsed, and the cost of each one rose.</h2>
<p class="lead">Two things happened to the program's output. Total enforcement contacts fell well below their 2018 peak and stayed there. And within those contacts, the share that were actual citations, rather than $0 verbal warnings, fell from about a third in 2018 to under 5% by 2024, because officers cannot compel identification and now warn on every first contact (<a href="data-methods.html#authority-detail">detail</a>). Set against what the program cost, one officer and a maintenance worker through 2022 and the billed three-officer invoices from 2023, the cost per contact rose from $229 to $1,021 and the cost per actual citation from $663 to $21,723. The lines below are ratios (annual program cost &divide; that year's contacts or citations), not the price of writing one ticket.</p>

<div class="chart-block">
  <div class="chart-title">DLP citations vs. program cost per published citation, 2014&ndash;2025</div>
  <div class="chart-subtitle">Green bars (left axis): DLP enforcement contacts per year, 2014&ndash;2025. Orange line (right axis): annual program cost &divide; that year's contacts. Cost basis: 2016&ndash;2022, one Animal Control Officer at the 2021 MOA rate plus a paired Facilities Maintenance Worker (author estimate); 2023&ndash;2024, what SPR was actually billed for three officers; 2025, one officer at the 2025 MOA rate (ledger not produced). The line begins in 2016, the first year with a documented cost basis. COVID period shaded; 2026 is partial and omitted. All dollars nominal.</div>
  <div class="chart-wrap"><canvas id="chartCostPerCit" role="img" aria-label="Dual-axis chart: DLP citations per year as bars and program cost per published citation as a line, 2014-2025."></canvas></div>
  <div class="chart-source">Contacts: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; cost: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf">2021 MOA Attachment A</a> ($152,399/yr per ACO II), <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/documents/enforcement-moa-billing.csv">SPR ledger backup 2023&ndash;24</a> (PRR C266465), 2025 MOA ($169,565/yr per ACO II) &middot; FMW pairing ~$140,000/yr through 2022 (author estimate) &middot; model and per-year values in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-year-metrics.csv">enforcement-year-metrics.csv</a></div>
</div>

<div class="chart-block">
  <div class="chart-title">Citations vs. verbal warnings, 2014&ndash;2026</div>
  <div class="chart-subtitle">Each year's DLP contacts split by recorded result. Orange = citation issued. Green = verbal warning ($0). Grey = blank, voided or dismissed. Verbal warnings first appear in the 2018 records; the 2014&ndash;2017 files (PRR C049204) record citations only, so the absence of warnings there means unrecorded, not zero. 2026 partial-year.</div>
  <div class="chart-wrap"><canvas id="chartResultMix" role="img" aria-label="Stacked bar chart of DLP contacts per year split into citations, verbal warnings, and other results; citations dominate through 2018 and verbal warnings dominate from 2019."></canvas></div>
  <div class="chart-source">Source: <code>case_result</code> in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; per-year split in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-year-metrics.csv">enforcement-year-metrics.csv</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Across 2014&ndash;2026, fee revenue ($294,885 cumulative, off-leash violations only) covered roughly 9% of the program&rsquo;s estimated $3.38M cost. Cost per contact was lowest in the peak-output years ($229 in 2018) and highest in the trough ($1,730 in 2022); 2024&rsquo;s recovery to 447 contacts (35% of the 2018 peak), priced at what SPR was actually billed that year, still comes to $1,021. Cost per actual citation is the sharper series: $663 in 2018, $16,244 in 2022, $21,723 in 2024, $7,372 in 2025. The 2023&ndash;24 figures are real invoices for three officers, not a model; how that came about is just below.</p>
</div>

<div class="fair-note">
  <strong class="head">On cost recovery</strong>
  Public-safety programs are not generally expected to pay for themselves through fees: police patrols, fire response, and park rangers all run at a net cost by design, and that is a legitimate use of public money. Cost recovery is included here as one measurable input, not as a standard the program is failing to meet. The question this page raises is narrower: the program's cost is rising while its measurable output falls and its offense mix shows no shift away from first-time violations, and that combination is worth examining before doubling the program's size. Policy recommendations are on the <a href="opinion.html">opinion page</a>; this page stays with the data.
</div>

<!-- ---- merged into Finding 01: the arc + funding (id=finding-02 kept for inbound links) ---- -->
<h3 id="finding-02" style="margin-top:40px;">The arc over time, and what the city funded, billed, and deployed</h3>
<p>COVID was a clean break in this series, so the story that matters now is what happened <em>after</em> it. Before COVID, the 2016 officer team drove contacts to a 2018 peak; since 2021 output has stayed low and flat, and the 2023 decision to fund and bill for three officers did not change that. The chart marks 2027&ndash;2028 as an outlook zone with no numeric projection.</p>

<div class="chart-block">
  <div class="chart-title">Annual DLP enforcement contacts, 2014&ndash;2026</div>
  <div class="chart-subtitle">Orange bars: DLP contacts (citations plus warnings). 2026 (lighter) is partial-year through April 17; the dashed marker shows its annualized full-year equivalent (~222). The shaded zone at right marks 2027&ndash;2028: neither prior staffing increase produced sustained output growth, so the page shows no numeric projection. COVID period shaded.</div>
  <div class="chart-wrap"><canvas id="chartYearTrend" role="img" aria-label="Bar chart of DLP citations per year 2014-2026 with COVID shading and a 2027-2028 outlook note (no numeric projection)."></canvas></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; staffing baselines: 2016 MOA, 2021 MOA, <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2023-PRF1602.pdf">2023 MOA</a>, Axios Seattle April 2026</div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Read the two eras separately. <strong>Before COVID</strong>, the 2016 officer team drove contacts from 183 (2014) to a 1,276 peak (2018). <strong>COVID was the break</strong>: 2020 fell to 393 (&minus;67% from 2019). <strong>Since then is the live story:</strong> output has stayed low and flat, with 2022&ndash;2025 at 169, 248, 447, and 267, at or below the old single-officer years, even though the city funded and was billed for three officers from 2023. The money rose; contacts did not, and deployment (per the cost note above) reached at most two. So this page makes no 2027&ndash;28 projection. For scale: Seattle dog-license issuance fell about 21% from 2014 to 2025 (<a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C264029">PRR C264029</a>) while contacts fell roughly 80% from peak. One documented reason output stays low regardless of patrol effort is below: officers can&rsquo;t compel identification, so a contact that yields no name ends in a warning, not a citation.</p>
</div>

<div class="fair-note" style="border-left-color: var(--navy);">
  <strong class="head">Why citation output can fall while patrols continue.</strong>
  <p>Animal Control Officers are not police: they cannot compel identification from someone who refuses, and cannot detain, and a name is required to write an infraction. By Finance &amp; Administrative Services&rsquo; own September 2022 report to Council, Seattle Police &ldquo;recently&hellip; have been unable to assist&rdquo; in obtaining IDs, so officers now &ldquo;issue verbal warnings on all first contacts.&rdquo; When refusing to identify yourself carries no consequence, and residents share patrol locations online, fewer contacts become citations regardless of how many dogs are off-leash. <a href="data-methods.html#authority-detail">Full quotes and source &rarr;</a></p>
</div>

<div class="chart-block">
  <div class="chart-title">What the Park District funded, and what SPR was billed, 2016&ndash;2026</div>
  <div class="chart-subtitle">FAS-side Animal Control Officer dollars. Navy = the cost this page carries each year: one officer at the MOA rate through 2022 and in 2025&ndash;26, and the actual billed amount in 2023&ndash;24 ($453,056 annualized from the first half of 2023; $456,173 for 2024). Light blue = funded authority above that. In 2023&ndash;24 the two are the same, because the 2023 MOA billed the full three-officer amount whether or not officers were fielded. For 2025&ndash;26 the ledger was not produced, so the gap between the $508,695 / $528,279 caps and actual-hours billing is unknown. Officer cost only; the maintenance-worker pairing ended in 2023.</div>
  <div class="chart-wrap"><canvas id="chartFundedVsDeployed" role="img" aria-label="Stacked bar chart of funded Animal Control Officer cost versus off-leash-attributable cost per year, 2016 to 2026, with a funded-but-undisclosed band opening in 2023."></canvas></div>
  <div class="chart-source">Funded: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2026.pdf">2026 MOA</a> ($528,279/yr, 3 ACO II), <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2023-PRF1602.pdf">2023 MOA</a> ($454,652/yr) and <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/moas/SPR-FAS-ACO2-MOA-2021-AG21-PRF03-032.pdf">2021 MOA</a> ($152,399/yr, 1 ACO II) &middot; attributable floor &amp; method: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-year-metrics.csv">enforcement-year-metrics.csv</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Through 2022 the funded program and the actual program were the same: one officer at $152,399. In 2023 the city <strong>tripled the funding</strong> ($454,652/yr; $528,279 under the 2026 MOA) <strong>and was billed for all of it</strong>: the 2023 agreement charged 240 hours per pay period for three officers with no actual-hours qualifier, and SPR's own budget staff noticed in December 2023 that "we pay on an annual hourly basis not on actual work performed" (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/README.md">Bates 00469</a>). What the money bought is a separate question: the Animal Shelter told SPR in February 2025 it could field "closer to 2 FTEs," possibly 1.5, and SPR said one officer was on parks as of April 2026. Contacts in 2023&ndash;25 (248, 447, 267) sat at or below the single-officer years. In September 2024 SPR's own manager reviewed the output and recommended cutting to two officers or one; in February 2025 the Interim Deputy Superintendent sent the draft back at three "given AP's priority with off leash" (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/prr-responses/C266465/README.md">chronology, PRR C266465</a>). The 2025 and 2026 MOAs fund "up to three" and bill on actual hours; what SPR has been billed since is not yet in the record. Because the cap on citations is officer <em>authority</em> (they can&rsquo;t compel identification), not headcount, filling the positions is unlikely to raise output in step. Officer dollars only; the SPR-side partner (a maintenance worker through 2022, vacant from 2023, an existing Park Ranger under the 2026 MOA) is carried separately (see <a href="opinion.html#O1">opinion O1</a>).</p>
</div>

<!-- ============ FINDING 03 — DETERRENCE ============ -->
<h2 class="finding" id="finding-03">No measurable shift away from first-time offenders.</h2>
<p class="lead">If enforcement were deterring repeat violations, the share of citations going to people cited before would be expected to grow over time as a stable population of repeat offenders accumulates contacts. Instead, first-time offenses have stayed the overwhelming majority every year, and their share has risen, not fallen.</p>

<div class="chart-block">
  <div class="chart-title">First-offense share of DLP citations, 2014&ndash;2026</div>
  <div class="chart-subtitle">Share of each year's DLP citations that are first offenses (vs. 2nd, 3rd, or 4th+ under Seattle Municipal Code (SMC) 18.12.080's escalation schedule). COVID period shaded. 2026 partial-year.</div>
  <div class="chart-wrap short"><canvas id="chartFirstOffense" role="img" aria-label="Line chart of first-offense share of DLP citations per year, consistently 84-96%."></canvas></div>
  <div class="chart-source">Source: offense levels in <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; <a href="https://library.municode.com/wa/seattle/codes/municipal_code?nodeId=TIT18PALA_CH18.12GEPRRE_SUBCHAPTER_IIOFPRPA_18.12.080DORELI">SMC 18.12.080(A)</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>First offenses have ranged from about 84% to 96% of DLP citations in every year of the record, rising over time rather than falling. One reading is that enforcement is deterring repeat offenses. A second reading is that lower total citation volume mechanically reduces the chance of an officer encountering the same person twice, which would push the first-offense share up regardless of behavior. The two cannot be separated here: neither PRR includes owner identifiers that would let us track individuals across citations. What the data does show is that the offense mix never shifted toward repeat offenders. The pattern is consistent with a program issuing fresh first-time contacts year after year, not one drawing down a shrinking pool of repeat violators. Seattle Parks &amp; Recreation's (SPR) own 2015 owner survey found about 38% of dog owners admit illegal off-leash use (39% local parks and 38% large parks weekly to monthly, 36% trails); no follow-up survey has been published (see <a href="#gap">what SPR has not measured</a>).</p>
</div>

<div class="fair-note" style="border-left-color: var(--navy);">
  <strong class="head">A key limit.</strong>
  <p>The citation records carry <em>no owner identity</em>, partly by privacy design and partly because officers usually can&rsquo;t obtain identification (<a href="#finding-02">Finding 1</a>). &ldquo;First offense&rdquo; is only what the officer recorded; we cannot follow individuals across years. So we can describe the offense <em>mix</em> the city recorded, but cannot tell genuine deterrence apart from simply not catching the same person twice. <a href="data-methods.html#repeat-detail">Why several explanations fit &rarr;</a></p>
</div>

<div class="supporting" id="per-fte-supporting">
  <p class="supporting-title">Citations per officer-FTE per year</p>
  <p class="supporting-note">A productivity view of the same record: DLP contacts divided by the total ACO+FMW FTE attributable to off-leash enforcement. Shown from 2016 on (the MOA-documented full-team era); pre-2016 part-time FTE is imputed and not directly comparable. Per-FTE output peaked at 638 in 2018 on a two-person team. From 2023 the denominator is one officer, because the paired maintenance worker left and was never replaced, so 2024's 447 per FTE is on a smaller team, not a recovery in output. 2026 partial-year excluded.</p>
  <div class="chart-wrap"><canvas id="chartPerFTE" role="img" aria-label="Line chart of DLP citations per officer-FTE per year, peaking at 638 in 2018."></canvas></div>
</div>

<!-- ============ FINDING 04 — GEOGRAPHY ============ -->
<h2 class="finding" id="finding-04">Where contacts happen, and where residents complain.</h2>
<p class="lead">Citations cluster in a handful of large, heavily-used parks, mostly ones without a nearby legal off-leash area, while resident complaints concentrate somewhere else entirely. This section maps both: the citation hotspots and their pre/post-COVID persistence, and the full per-park table. Throughout, the records show <em>where</em> citations were issued, not <em>why</em> officers were there.</p>

<div class="map-block">
  <div class="chart-title">Where off-leash citations were issued, 2014&ndash;2026</div>
  <div class="chart-subtitle">Circles sized by DLP citation count at the cited park. Green dots mark all 14 existing off-leash areas (OLAs). Hover a marker for details.</div>
  <div id="hotspot-map" role="img" aria-label="Map of Seattle off-leash citation hotspots 2014 to 2026 with existing OLA locations overlaid."></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a> &middot; coordinates <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/park-coordinates.csv">park-coordinates.csv</a> (approximate) &middot; tiles: <a href="https://www.esri.com/">Esri</a> / <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a></div>
</div>

<div class="chart-block">
  <div class="chart-title">Top 20 cited parks: pre-COVID (2014&ndash;2019) vs post-COVID (2020&ndash;2026)</div>
  <div class="chart-subtitle">Orange bars: 2014&ndash;2019 DLP citations. Navy bars: 2020&ndash;2026 DLP citations. Parks ordered by combined total.</div>
  <div class="chart-wrap tall"><canvas id="chartPersistence" role="img" aria-label="Paired bar chart: top 20 cited parks pre-COVID vs post-COVID."></canvas></div>
  <div class="chart-source">Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-by-park-year.csv">enforcement-by-park-year.csv</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Citations cluster in areas without a designated OLA. Discovery, Volunteer, Cal Anderson, Lincoln, Martha Washington, Wallingford Playfield, Seward, and Maple Leaf Reservoir all rank in the top 20 and none has a dedicated OLA on site. Magnuson and Westcrest appear as hotspots because the non-OLA portions of those large host parks are used off-leash. The top 10 parks accounted for 46% of citations before COVID and 40% after. Concentration eased somewhat but the same handful of parks still dominate. <strong>The data records where citations were issued, not why officers were there</strong>, so it cannot establish whether a given park is a hotspot because of higher violation rates or because patrols were directed to it.</p>
  <p><strong>Complaints by park type.</strong> The 2024&ndash;26 complaint data (<a href="#finding-07">Finding 4</a>) sharpens this: destination and natural-area parks (Discovery, Woodland, Golden Gardens, Magnuson) stay roughly balanced between complaints and citations (the ones Animal Control patrols) while dense-neighborhood playfields run 5:1 to 100:1 complaints-over-citations (West Queen Anne Playfield 255 complaints, Maple Leaf Reservoir 147, Beacon Hill 108). Where officers go and where neighbors object are structurally different places.</p>
</div>

<!-- ---- sub: full table (kept at id=finding-06 for back-compat links) ---- -->
<h3 id="finding-06" style="margin-top:40px;">The full top-20 table</h3>
<table class="data">
  <thead><tr><th class="num">Rank</th><th>Park</th><th>Neighborhood</th><th class="num">Citations 2014&ndash;2026</th><th class="num">Pre-COVID</th><th class="num">Post-COVID</th><th class="num">Complaints 2024&ndash;26</th><th>OLA?</th></tr></thead>
  <tbody id="topTable"></tbody>
</table>
<p class="fineprint" style="margin:4px 0 0;"><strong>New column.</strong> Citation columns span 2014&ndash;2026; the complaint column is 2024&ndash;26 only (the complaint record begins in 2024), so the two are not the same window. Read the column for the within-park <em>contrast</em> between enforcement and resident reporting, not as a like-for-like total. Source: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/complaints-vs-citations-by-park.csv">complaints-vs-citations-by-park.csv</a> (PRR C263990).</p>

<!-- ============ FINDING 07 — RESIDENT COMPLAINTS (NEW) ============ -->
<h2 class="finding" id="finding-07">More complaints, fewer contacts, and no link between the two.</h2>
<p class="lead">In 2025, the first full year of the complaint record, residents filed about <strong>3,010</strong> &ldquo;Nuisance Dogs in a Park&rdquo; reports through Find It Fix It, roughly <strong>11 for every dog-loose-in-park citation</strong> the city issued that year. As complaints rose, citations fell, and after mid-2025 citations went nearly silent while complaints held steady. Complaints are resident-reported, tracking who files rather than only where dogs run off-leash, so they are read here as a behavior proxy, not an incident count. This is the independent proxy the <a href="#gap">data-gap note below</a> had flagged as pending.</p>

<div class="chart-block">
  <div class="chart-title">Resident complaints vs. dog-loose-in-park citations, 2024&ndash;2026</div>
  <div class="chart-subtitle">Top panel (orange bars): monthly Find It Fix It complaints. Bottom panel (navy line): monthly DLP citations, same months. Two stacked panels on one shared timeline, deliberately not a dual-axis chart, which would imply a correlation the data does not support.</div>
  <p style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink-faint);margin:8px 0 4px;">Monthly resident complaints</p>
  <div class="chart-wrap short"><canvas id="chartCmpTop" role="img" aria-label="Monthly Find It Fix It nuisance-dog complaints, April 2024 to June 2026."></canvas></div>
  <p style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink-faint);margin:14px 0 4px;">Monthly dog-loose-in-park citations</p>
  <div class="chart-wrap short"><canvas id="chartCmpBot" role="img" aria-label="Monthly dog-loose-in-park citations over the same period, falling to near zero after mid-2025."></canvas></div>
  <div class="chart-source">Complaints: <a href="https://data.seattle.gov/City-Administration/Customer-Service-Requests/5ngg-rpne/about_data">Open Data 5ngg-rpne</a> (PRR C263990) &middot; citations: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-citations.csv">enforcement-citations.csv</a>, DLP only &middot; monthly series: <a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/complaints-citations-monthly.csv">complaints-citations-monthly.csv</a></div>
</div>

<div class="takeaway neutral">
  <span class="kicker">Observation</span>
  <p>Month to month, complaint volume and citation volume <strong>move independently</strong>: a heavy month for complaints is no more (and no less) likely to be a heavy month for citations. <span style="color:var(--ink-faint);">(For the statistically inclined: the correlation is r&nbsp;=&nbsp;0.13 over April 2024 to June 2026, near zero on a scale where 1.0 would mean the two rise and fall in lockstep; the last two months carry no citation data because that record ends April 17, 2026, and excluding them gives 0.08.)</span> Complaints roughly <strong>tripled</strong> from 2024's nine recorded months to 2025's full year, while contacts <em>fell</em> about 40% (447 to 267), then dropped to near zero for the second half of 2025. With one to two officers on parks, enforcement output cannot scale to complaint volume; the two systems operate in parallel, not in sequence. This neither proves nor disproves that complaints lead to enforcement: the records show citation volume, not what happened after any individual complaint.</p>
</div>

<!-- ============ GAP CALLOUT ============ -->
<h2 class="finding" id="gap">No one has measured whether the program works.</h2>
<div class="gap-callout">
  <strong class="head">What the City never measured, now confirmed by both agencies</strong>
  <p>Contact counts measure <em>enforcement activity</em>, not violation rates. A drop could mean fewer violations <em>or</em> fewer patrols. SPR's 2015 owner survey found about 38% of dog owners admit illegal off-leash use; no follow-up survey has been published. In 2026 two records requests asked each agency directly for any evaluation, deployment log, or trend analysis of the program. <strong>SPR</strong> (<a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C266465">PRR C266465</a>, answered July 2026) produced no deployment logs and no compliance or complaint-trend analysis; its one internal review, a September 2024 memo, counted raw output, found it falling, and recommended cutting the program to two officers or one. <strong>FAS / the Animal Shelter</strong> (<a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/">PRR C266744</a>) said its only responsive records are officer truck logs and dispatch broadcasts. Across ten years and roughly $3 million in officer billing, no evaluation exists anywhere in the City. The Animal Shelter's own tracking for 2023&ndash;24 shows what the program produces: 1,540 officer contacts, 70 citations, 4 written warnings, 0 park exclusions (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/data/enforcement-program-activity.csv">enforcement-program-activity.csv</a>; a different record system from the citation data on this page, kept separate on purpose). Still open:</p>
  <ul>
    <li><s>SPR program evaluation, deployment logs, and 2026 expansion decision record (PRR #8)</s> &mdash; <strong>received</strong> as <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C266465">C266465</a>: no evaluation or deployment logs exist; the decision record and 2023&ndash;24 ledger backup did. Still open: Q3&ndash;Q4 2023 and 2025&ndash;26 billing.</li>
    <li><s>Find-It-Fix-It &ldquo;dog in a park&rdquo; complaints by year &mdash; an independent behavior proxy</s> &mdash; <strong>received</strong> (<a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C263990">PRR C263990</a>); see <a href="#finding-07">Finding 4</a> above. Still open: the free-text &ldquo;General Inquiry &ndash; Animal Shelter&rdquo; export, and the cause of the mid-2025 citation drop-off.</li>
    <li><s>Current SPR/SAS MOA and budget lines for the expanded staffing</s> &mdash; <strong>received</strong> (<a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C265341">PRR C265341</a> and <a href="https://github.com/avrignaud/seattledogparkdata/tree/main/data/prr-responses/C265589">C265589</a>): the 2023 Park District MOA funds three ACO IIs at $454,652/yr, re-priced to $528,279/yr by the 2026 MOA; see the cost footnote below. Still open: the MOA &sect;5 monthly parks-data reports (<a href="https://github.com/avrignaud/seattledogparkdata/blob/main/prrs/09-spr-aco-monthly-parks-reports.md">PRR #9</a>, filed; SPR responding), which would show per-park patrol activity, and the narrowed July-2025 truck-log installment on C266744.</li>
  </ul>
  <p>This page can describe enforcement output and cost. It cannot prove or disprove that the program changed behavior, and neither, on its own records, can the City. Policy implications are on the <a href="opinion.html">opinion page</a>.</p>
</div>

<!-- ============ FOOTNOTES ============ -->
<p class="data-methods-link" id="data-notes">Sources, methodology and caveats for this page: <a href="data-methods.html#notes-enforcement">Data &amp; Methods</a>.</p>

<nav class="paginate">
  <a href="part3.html" class="prev"><span class="kicker">&larr; Previous</span><span class="title">Part III &mdash; Forward</span></a>
  <a href="budget.html" class="next"><span class="kicker">Next &rarr;</span><span class="title">Budget</span></a>
</nav>

<footer>
  <p>Data current as of September 2026 (PRR C266465 ingest). Source code and all underlying data: <a href="https://github.com/avrignaud/seattledogparkdata">github.com/avrignaud/seattledogparkdata</a>. MIT license covers author-written code and analysis; primary data is public record. Corrections: <a href="https://github.com/avrignaud/seattledogparkdata/issues">issue tracker</a>.</p>
</footer>

</div></main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
<script src="chart-defaults.js?v=c060db2a"></script>
<script src="site-data.js?v=47e1a65b"></script>
<script>
const D = __DATA__;
const P = SDPD.palette;
const FONT = "'IBM Plex Sans', sans-serif";
const FONT_MONO = "'IBM Plex Mono', monospace";

// NEW — resident complaint data (PRR C263990), 2024-26
const CMP_MONTHLY = [["2024-04", 68, 39], ["2024-05", 73, 48], ["2024-06", 109, 40], ["2024-07", 106, 34], ["2024-08", 117, 35], ["2024-09", 100, 44], ["2024-10", 89, 28], ["2024-11", 86, 28], ["2024-12", 105, 29], ["2025-01", 420, 32], ["2025-02", 363, 58], ["2025-03", 299, 62], ["2025-04", 276, 51], ["2025-05", 219, 26], ["2025-06", 249, 21], ["2025-07", 214, 1], ["2025-08", 209, 1], ["2025-09", 236, 5], ["2025-10", 206, 4], ["2025-11", 168, 5], ["2025-12", 151, 1], ["2026-01", 206, 19], ["2026-02", 127, 13], ["2026-03", 157, 17], ["2026-04", 248, 16], ["2026-05", 236, 0], ["2026-06", 28, 0]];
const CMP_BYPARK = {"Discovery Park": 109, "Magnuson Park": 140, "Volunteer Park": 99, "Woodland Park": 62, "Golden Gardens Park": 44, "Cal Anderson Park": 95, "Lincoln Park": 97, "West Queen Anne Playfield": 255, "Maple Leaf Reservoir Park": 147, "Genesee Park": 68, "Martha Washington Park": 8, "Green Lake Park": 93, "Seward Park": 26, "Westcrest Park": 28, "Gilman Playground": 24, "Wallingford Playfield": 35, "Alki Beach Park": 23, "Soundview Playfield": 9, "Rogers Playground": 35, "Ravenna Park": 9};

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
      { label: 'Program cost per published citation $, 2016+ (right axis)', data: costLine, spanGaps: false,
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

// ===== Finding 01 supporting — citations vs verbal warnings by year =====
(function() {
  const yt = D.year_trend;
  new Chart(document.getElementById('chartResultMix'), {
    type: 'bar',
    data: { labels: yt.map(t => t.year), datasets: [
      { label: 'Citations', data: yt.map(t => t.result_citation), backgroundColor: P.orange, stack: 's' },
      { label: 'Verbal warnings ($0)', data: yt.map(t => t.result_verbal), backgroundColor: P.sage, stack: 's' },
      { label: 'Blank / voided / dismissed', data: yt.map(t => t.result_other), backgroundColor: P.inkFaint, stack: 's' }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } }, annotation: { annotations: { covid: covidAnn() } } },
      scales: {
        x: { stacked: true, ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { stacked: true, title: { display: true, text: 'DLP records', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } } }
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
  // COVID region box
  const covid = covidAnn();
  // 2027-2028 "outlook" zone. We deliberately show NO numeric projection: the
  // two prior staffing increases (2016, 2023) did not produce sustained output
  // growth, so a citations-per-year forecast would assert a scaling the record
  // doesn't support. The shaded zone carries a flat factual note instead.
  const projBox = { type: 'box', xMin: idx2026 + 0.5, xMax: idx2026 + 2.5,
    backgroundColor: 'rgba(31,58,95,0.07)', borderWidth: 0, drawTime: 'beforeDatasetsDraw',
    label: { display: true,
      content: ['2027–28', 'no numeric', 'projection'],
      position: { x: 'center', y: 'center' },
      backgroundColor: 'transparent', color: 'rgba(31,58,95,0.85)',
      font: { family: FONT_MONO, size: 10, weight: '600' } } };

  new Chart(document.getElementById('chartYearTrend'), {
    type: 'bar',
    data: { labels, datasets: [
      { label: 'DLP citations (actual; 2026 partial-year)', data: actual, backgroundColor: barColors, order: 2 },
      { label: '2026 annualized estimate (YTD ÷ 0.29)', data: annualized2026, type: 'scatter',
        pointStyle: 'line', pointRadius: 12, borderColor: P.inkSoft, borderWidth: 2, borderDash: [3,3], order: 1 }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } },
        annotation: { annotations: { covid, proj: projBox } } },
      scales: {
        x: { ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { title: { display: true, text: 'DLP citations', font: { family: FONT_MONO, size: 11 } }, ticks: { font: { family: FONT_MONO, size: 11 } }, beginAtZero: true, suggestedMax: 1400 }
      } }
  });
})();

// ===== Finding 02 supporting — funded vs. off-leash-attributable ACO cost =====
(function() {
  // FAS-side ACO dollars, 2016-2026. traceable = the cost this page carries:
  // aco_fte x MOA rate (2016-22, 2025-26) or the BILLED amount (2023-24, PRR
  // C266465 ledger); funded = MOA totals (1 ACO $152,399 -> 3 ACO $454,652
  // from the 2023 MOA PRF1602, re-priced to $528,279 by the 2026 MOA). Both
  // fields come from data/enforcement-year-metrics.csv via the page-data JSON.
  const rows = D.year_trend.filter(t => parseInt(t.year, 10) >= 2016);
  const labels = rows.map(t => t.year);
  const traceable = rows.map(t => t.traceable_aco_cost);
  const gap = rows.map(t => Math.max(0, t.funded_aco_cost - t.traceable_aco_cost));
  new Chart(document.getElementById('chartFundedVsDeployed'), {
    type: 'bar',
    data: { labels, datasets: [
      { label: 'Cost carried: billed 2023-24, one-officer model otherwise', data: traceable, backgroundColor: P.navy, stack: 'cost',
        borderSkipped: false,
        borderRadius: (c) => { const g = gap[c.dataIndex] || 0; return { topLeft: g > 0 ? 0 : 6, topRight: g > 0 ? 0 : 6, bottomLeft: 6, bottomRight: 6 }; } },
      { label: 'Funded authority above that', data: gap, backgroundColor: P.navySoft, borderColor: P.navyMute, borderWidth: 1, stack: 'cost',
        borderSkipped: false, borderRadius: { topLeft: 6, topRight: 6, bottomLeft: 0, bottomRight: 0 } }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { labels: { font: { family: FONT, size: 12 } } },
        tooltip: { callbacks: { label: c => c.dataset.label.split(' (')[0] + ': $' + c.parsed.y.toLocaleString() } },
        annotation: { annotations: {
          undisclosed: { type: 'label', xValue: '2025', yValue: 340000,
            content: ['2025-26 billing', 'not yet produced'],
            color: P.navyMute, font: { family: FONT_MONO, size: 10, weight: '600' } }
        } } },
      scales: {
        x: { stacked: true, ticks: { font: { family: FONT_MONO, size: 11 } }, grid: { display: false } },
        y: { stacked: true, beginAtZero: true,
          title: { display: true, text: 'FAS-side ACO cost', font: { family: FONT_MONO, size: 11 } },
          ticks: { font: { family: FONT_MONO, size: 11 }, callback: v => '$' + Math.round(v/1000) + 'K' } }
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
    const cmp = CMP_BYPARK[p.park];
    const cmpCell = (cmp != null) ? cmp.toLocaleString() : '&mdash;';
    tbody.insertAdjacentHTML('beforeend', `<tr><td class="num">${i+1}</td><td>${p.park}</td><td>${p.neighborhood||'—'}</td><td class="num">${p.count.toLocaleString()}</td><td class="num">${p.pre.toLocaleString()}</td><td class="num">${p.post.toLocaleString()}</td><td class="num">${cmpCell}</td>${olaCell(p.ola_status)}</tr>`);
  });
})();

// ===== Finding 07 — complaints vs citations, monthly (NEW) =====
(function() {
  const labels = CMP_MONTHLY.map(r => r[0]);
  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const fmt = m => { const a = m.split('-'); return MON[parseInt(a[1],10)-1] + " '" + a[0].slice(2); };
  const xcfg = (show) => ({ grid: { display: false }, ticks: { display: show, autoSkip: true, maxRotation: 0,
    font: { family: FONT_MONO, size: 10 }, callback: (v,i) => (labels[i].slice(-2) === '01' || labels[i].slice(-2) === '07') ? fmt(labels[i]) : '' } });
  const topEl = document.getElementById('chartCmpTop');
  if (topEl) new Chart(topEl, { type: 'bar',
    data: { labels, datasets: [{ label: 'Complaints', data: CMP_MONTHLY.map(r => r[1]), backgroundColor: P.orange }] },
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: { title: i => fmt(i[0].label), label: c => c.parsed.y + ' complaints' } } },
      scales: { x: xcfg(false), y: { beginAtZero: true, ticks: { font: { family: FONT_MONO, size: 10 } } } } } });
  const botEl = document.getElementById('chartCmpBot');
  if (botEl) new Chart(botEl, { type: 'line',
    data: { labels, datasets: [{ label: 'DLP citations', data: CMP_MONTHLY.map(r => r[2]), borderColor: P.navy, backgroundColor: 'rgba(31,58,95,0.09)', fill: true, tension: 0.25, pointRadius: 2, pointBackgroundColor: P.navy, borderWidth: 2 }] },
    options: { responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: { title: i => fmt(i[0].label), label: c => c.parsed.y + ' citations' } } },
      scales: { x: xcfg(true), y: { beginAtZero: true, suggestedMax: 80, ticks: { font: { family: FONT_MONO, size: 10 } } } } } });
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
  SDPD.basemap(m1, { maxZoom: 18 });
  OLAS.forEach(o => L.circleMarker([o.lat, o.lng], { radius: 4, fillColor: P.sage, fillOpacity: 0.95, color: '#fff', weight: 1.5 }).bindTooltip(`<strong>${o.name}</strong><br>${o.acres} ac OLA`).addTo(m1));
  HOTSPOTS.forEach(h => L.circleMarker([h.lat, h.lng], { radius: Math.sqrt(h.count)*1.1 + 4, fillColor: fill(h.ola_status), fillOpacity: 0.5, color: '#fff', weight: 1.5 }).bindTooltip(`<strong>${h.park}</strong><br>${h.count} DLP citations · ${h.neighborhood}`).addTo(m1));
  legend(`<div class="hdr">Legend</div>
    <div class="row"><span class="dot" style="background:${P.sage}"></span> Existing OLA</div>
    <div class="row"><span class="dot" style="background:${P.orange}"></span> Cited park, no OLA</div>
    <div class="row"><span class="dot" style="background:${P.gold}"></span> Cited park, partial OLA</div>
    <div class="row"><span class="dot" style="background:${P.inkFaint}"></span> Planned OLA</div>
    <div class="row" style="margin-top:4px;color:var(--ink-faint)">Circle size = citation count</div>`).addTo(m1);

  // Map 2 — walkshed gap
  const m2 = L.map('gap-map', { scrollWheelZoom: false }).setView(CENTER, 11);
  SDPD.basemap(m2, { maxZoom: 18 });
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
out = ROOT / "docs" / "enforcement.html"
out.write_text(HTML, encoding='utf-8')
print(f"Wrote {out} ({len(HTML):,} chars)")

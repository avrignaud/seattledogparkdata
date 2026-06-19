# DESIGN.md — Seattle Dog Park Data

> Documented from the live `docs/site.css` and pages.

## Color (warm-paper editorial palette)
- Surfaces: `--bg #FAF8F3` (warm off-white paper), `--surface #FFFFFF`.
- Ink: `--ink #1A1712`, `--ink-soft #4C4A44`, `--ink-faint #8A877E`. Rules: `--rule #E8E5DC`, `--rule-soft #F1EFE7`.
- Accents (each with a `-soft` tint): `--orange #D1481A` (Seattle data, primary accent), `--navy #1F3A5F`, `--sage #4C6B54` (peer/positive), `--gold #B8872B`, `--danger #8B2518`.
- Strategy: restrained — tinted neutrals + orange as the lead accent; navy/sage/gold used as semantic roles (peer cities, budget, etc.), not decoration.

## Typography
- Display: **Space Grotesk**. Body: **Inter**. Metadata/labels: **IBM Plex Mono** (uppercase, letter-spaced kickers, masthead, source lines).
- Type scale (use classes, not inline sizes): `.lead` 18.5px / body 16.5px / `.note` 15px (secondary, ink-soft) / `.fineprint` 13.5px (captions, sources, methodology). Headings via Space Grotesk weight+scale.
- Body line length capped ~62–72ch.

## Layout & components
- `.wrap` max-width 1180px. Masthead strip (mono): page · site · domain | date.
- Stat cards (`.stat` in `.orange/.navy/.sage/.gold`): label + big number + `.note`.
- Callouts: `.note-box` and `.takeaway` use a left brand-color border + soft tint (established house pattern). `.fair-note` for hedged caveats.
- `.chart-block` (Chart.js) with `.chart-title` / `.chart-subtitle` / `.chart-source`. `table.data` for data tables.
- **Collapsible `details.data-notes`** for end-of-page methodology (closed on screen, open in print).

## Conventions
- Em-dashes are house style. Acronyms spelled out on first use per page. Sub-$1M numbers written in full; millions as `$X.XXM`; chart axis unit labels may keep `($M)`.
- Note: CLAUDE.md's older "Fraunces / IBM Plex Sans" note is stale — the live stack is Space Grotesk / Inter / IBM Plex Mono.

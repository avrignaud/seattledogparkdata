# Dog-licensing data (PRR C264029) — review & recommendations

**Source:** Seattle Animal Shelter, PRR **C264029-041826** (June 2026). Two files:
- `2014-2025PDR.xlsx` — 265,741 individual dog-license issuances, 2014–2025, with
  renewal flag, issue date, altered status, and home/mailing/previous ZIP (items #1, #2).
- `SAS Licensing Data 2014-25 as of 5.4.2026.xlsx` — annual dog-license **revenue** (item #4).
- Items #3 (compliance estimate) and #5 (population analysis): **no responsive records.**

**Analysis date:** 2026-06-08. All dog (species pre-filtered). Reproducible from the
two files + `data/enforcement-year-metrics.csv`.

---

## TL;DR

The single best thing in this data is a **compliance** finding, not an enforcement one:
**most Seattle dogs are not licensed, and the licensed share is falling.** SAS publishes
no compliance figure (item #3: no records), so this would be ours to establish.

For the **enforcement page** specifically, only two pieces belong, and both as context:
1. Licenses fell ~21% (2014→2025) while citations fell ~80% from their 2018 peak —
   enforcement dropped far faster than any plausible change in the dog base.
2. A scale point: one officer against a dog population that is mostly *unlicensed and
   invisible* to the city — reinforces the existing first-offense "scale" bullet.

Everything else (compliance rate, revenue, altered share, ZIP geography) is a **licensing
/ population story**, not enforcement output. It deserves its own home (a short licensing
section, or a feed into the Access/population material) — folding it all into the
enforcement page would dilute its tight "rising cost, falling output" thesis.

**Do NOT** build a "citations per 1,000 licenses" chart — see §4.

---

## 1. What the data is (and isn't)

- Each row is a **license issued** on a date — not a snapshot of active licenses. With
  pre-2025 1- and 2-year terms (and no term column in the data), "active licenses at a
  point in time" can only be **estimated**, not read off.
- **2025 is distorted**: SAS moved to 1-year-only licenses and the portal couldn't renew
  2-year licenses, so renewals were reissued as "new." The new-vs-renewal split for 2025
  is unreliable (FAS flagged this); the *total* count is still usable.
- ZIP is the **owner's home address**, not where anything happened — so it speaks to where
  dogs are *owned*, not where off-leash use or citations occur.

## 2. The headline: licensing compliance is low and falling (the strongest finding)

Dog licenses **issued** per year:

| 2014 | 2018 | 2024 | 2025 |
|---|---|---|---|
| 24,309 | 23,618 | 20,694 | 19,219 |

Down ~21% from 2014. **Active** licensed dogs (modeled estimate, since term isn't in the
data) sit between `issued this year` (if all 1-year) and `issued this year + last year`
(if all 2-year) — roughly **20,000–41,000** in 2024.

SAS publishes no compliance estimate. Against the dog-population range the site already
uses (**150,000 floor to ~400,000** per SPR's 2023 Expansion Study), even the generous
~41,000-active figure implies **only ~10–27% of Seattle dogs are licensed** — and the
licensed share is *trending down* while the human population grew. This is genuinely new
(the city doesn't publish it) and defensible **as a range, explicitly labeled our
estimate**, never a point figure.

*Why it matters:* the licensed dogs the city can see are a small, shrinking slice of the
actual dog population. Both licensing and off-leash enforcement operate on that slice.

## 3. Enforcement-relevant context (the only two pieces for that page)

**a. The divergence — enforcement fell far faster than the dog base.** From 2014 to 2025
dog licenses fell ~21%; DLP citations fell ~80% from their 2018 peak (1,276 → 267).
However you estimate the dog population, enforcement output dropped several times faster.
This strengthens the page's existing "falling output" thesis without needing a confounded
ratio.

**b. Scale.** One full-time officer faces a dog population that is ~75–90% **unlicensed**
— i.e., not even in the city's basic registry, let alone reachable by patrol. This is a
concrete number for the first-offense "scale" bullet (Finding 03): the violating pool
isn't just large, it's largely invisible to the city.

## 4. Why NOT a "citations per 1,000 licenses" chart

It's tempting and it's a trap. Licenses-issued is itself a **compliance** trend, not a dog
**population** trend — it fell ~21% even as dog ownership almost certainly rose
(pandemic puppies, population growth). So a per-1,000-licenses ratio divides one declining
series (citations) by another declining series (licensing enrollment), quite possibly both
falling for the same post-COVID administrative-capacity reason. The ratio would conflate
two different declines and invite the fair objection that licensed dogs aren't the right
base anyway (violations come from all dogs, most unlicensed). The clean, unkillable
version is the raw divergence in §3a. Use that; skip the ratio chart.

## 5. The revenue figure — one sentence of scale context, or cut it

Dog-license revenue (computed from the file; 2015 and 2017 are flagged partial/incomplete
and excluded):

| 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| $1.27M | $1.29M | $1.29M | $1.27M | $1.23M | $1.17M | $1.18M | $0.87M* |

≈ **$1.24M/year** average (2018–2024); 2025 lower (1-year-license transition).

**Caveat that gates any use:** this funds the **entire** Seattle Animal Shelter — shelter,
cruelty, adoptions, licensing, all animal control — **not** the off-leash program. It is
*not* cost recovery for enforcement and must not be framed as such. The only honest use is
narrow scale context: citation fines (~$29K/year average, the $351K total over 12 years
already on the page) are a rounding error next to the ~$1.2M/year the city collects in dog
licenses — so if there's a fiscal lever in the dog program, it's **licensing compliance,
not citation fines.** Keep it to that one sentence, or leave it out.

## 6. Secondary observations (licensing story, lower priority)

- **Altered (spayed/neutered) share** of licensed dogs slipped from ~94% (2014) to ~89%
  (2025) — a small, steady rise in licensed intact dogs. Mildly interesting, not enforcement.
- **Geography.** Top license ZIPs — 98115 (NE/Wedgwood), 98103 (Wallingford/Fremont),
  98117 (Ballard), 98125 (Lake City), 98118 (Columbia City) — overlap substantially with
  the top *complaint* ZIPs (98115, 98103, 98117, 98118 appear in both). Useful as a
  **normalization caveat**: complaint/citation hotspots partly track where dogs are owned,
  not only where OLAs are absent. Mind the mismatch (license ZIP = owner home; complaints/
  citations = incident location) — it roughly aligns at neighborhood scale; don't claim
  more. One note: 98119 (Queen Anne) is a top *complaint* ZIP but only mid-tier for
  licenses — consistent with the earlier read that QA complaints run above what dog density
  alone would predict.

## Recommendations

**Weave into the enforcement prototype (small, in-context):**
1. Add the **§3a divergence** to Finding 02 or 03 as a sentence (licenses −21% vs citations
   −80%), framed as "enforcement fell faster than the dog base."
2. Strengthen the **first-offense "scale" bullet** (Finding 03) with §3b: the mostly-
   unlicensed, city-invisible dog population.
3. *Optionally* the one-sentence revenue scale-context (§5) in the Finding 01 cost-recovery
   fair-note — only if it earns its place; otherwise skip.

**Spin up separately (its own licensing/population story — review first):**
4. A short **"How many dogs, and how many licensed?"** treatment: the compliance estimate
   (§2), the licensing trend, altered share, and ZIP density. This is the natural home for
   the population denominator the site has long approximated as "150K+." Could live on the
   Access page or a new small page — not the enforcement page.
5. Bring the licensing files into the repo under `data/prr-responses/C264029/` with a README
   (the established PRR pattern) so any of the above is reproducible.

**Don't:**
6. No per-1,000-licenses chart (§4). No revenue-as-cost-recovery framing (§5). No point
   compliance figure — always the labeled range.

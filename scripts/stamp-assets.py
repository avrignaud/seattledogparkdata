#!/usr/bin/env python3
"""Stamp a content hash onto the shared CSS/JS includes.

The site has no build step, so `site.css`, `chart-defaults.js` and `site-data.js`
are served under fixed names. A browser that cached them keeps using its copy
after they change, and the page silently runs old code against new markup. That
is not hypothetical: after the September 2026 CARTO-to-Esri basemap swap, Safari
kept a `chart-defaults.js` with no `SDPD.basemap` in it, the map script threw,
and every Leaflet map rendered as an empty grey box.

This rewrites `?v=<hash>` on those includes across the public pages and the
enforcement builder's template. Run it after editing any shared asset, then
re-run `build_enforcement_page.py` so the generated page picks the new value up.
Idempotent: a second run produces no diff.

Usage: python3 scripts/stamp-assets.py [--check]
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
ASSETS = ["site.css", "chart-defaults.js", "site-data.js"]
TARGETS = sorted(DOCS.glob("*.html")) + [REPO / "scripts" / "build_enforcement_page.py"]
SKIP = ("mockup", "proposal")


def short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def main() -> int:
    check = "--check" in sys.argv
    versions = {a: short_hash(DOCS / a) for a in ASSETS}
    changed, stale = [], []

    for target in TARGETS:
        if any(s in target.name for s in SKIP):
            continue
        text = original = target.read_text(encoding="utf-8")
        for asset, ver in versions.items():
            # href="site.css" / href="site.css?v=abc12345" -> href="site.css?v=<ver>"
            text = re.sub(
                r'((?:href|src)=")' + re.escape(asset) + r'(?:\?v=[0-9a-f]+)?(")',
                r'\g<1>' + asset + "?v=" + ver + r'\g<2>',
                text,
            )
        if text != original:
            (stale if check else changed).append(target.relative_to(REPO))
            if not check:
                target.write_text(text, encoding="utf-8")

    for asset, ver in versions.items():
        print(f"  {asset:<20} v={ver}")
    if check:
        if stale:
            print("\nSTALE (run without --check):")
            for f in stale:
                print(f"  {f}")
            return 1
        print("\nall asset stamps current")
        return 0
    print(f"\nstamped {len(changed)} file(s)" if changed else "\nall asset stamps already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

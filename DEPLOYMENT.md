# Deployment — Cloudflare Pages

Hosting mirrors the Siegewords setup: private GitHub repo as source, Cloudflare Pages as the build/CDN, Cloudflare DNS for the apex domain `seattledogparkdata.com`.

## One-time setup (~10 minutes)

### 1. Connect the repo to Cloudflare Pages

In the Cloudflare dashboard → **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.

First time connecting a repo to Pages:
- GitHub → **Install & Authorize Cloudflare Pages** on the `avrignaud` account.
- When prompted to choose repository access, **either** grant access to all repos **or** specifically select `avrignaud/seattledogparkdata`. The latter is tighter; Siegewords can stay isolated.

Back in Cloudflare, select `avrignaud/seattledogparkdata` from the list and click **Begin setup**.

### 2. Build configuration

Use these exact values:

| Field | Value |
|---|---|
| Project name | `seattledogparkdata` |
| Production branch | `main` |
| Framework preset | **None** |
| Build command | *(leave blank)* |
| Build output directory | `docs` |
| Root directory | *(leave blank — repo root)* |
| Environment variables | *(none needed)* |

Click **Save and deploy**. Cloudflare should finish in about 30 seconds because there is no build — just a static-file deploy from `docs/`.

The first build produces a `seattledogparkdata.pages.dev` URL (or a variant). Verify the site works there before attaching the custom domain.

### 3. Attach the custom domain

In the Pages project → **Custom domains** → **Set up a custom domain** → enter `seattledogparkdata.com`.

Cloudflare detects that the domain already has a zone in your account and adds the correct DNS records automatically:
- `seattledogparkdata.com` → CNAME to `seattledogparkdata.pages.dev` (flattened at apex)
- `www.seattledogparkdata.com` → CNAME (optional — add via the same flow if you want `www` to work)

SSL provisions automatically via Cloudflare's Universal SSL. Usually live within a minute or two.

### 4. Verify

- `curl -I https://seattledogparkdata.com` → should return `200` with `server: cloudflare`.
- Visit in a browser; check that all five pages render and the Leaflet maps + Chart.js charts load.
- Check print view: File → Print → Save as PDF in Chrome, on each page.

## Ongoing workflow

- Push to `main` → Cloudflare Pages automatically rebuilds and deploys, typically within 1 minute.
- Preview branches get their own `*.seattledogparkdata.pages.dev` URLs if you want to share drafts without affecting production.
- Rollbacks: Pages dashboard → **Deployments** → pick any prior deployment and click **Rollback**. Instant.

## Cache headers (optional)

A `_headers` file in `docs/` can tune cache behavior. For now the defaults are fine — Cloudflare caches static HTML, CSS, JS aggressively, and since this site has no build step the cache-busting concern is minimal. If we add versioned asset filenames later, we can set longer max-age on them here.

## If something goes wrong

- **Build fails immediately.** Check the Cloudflare build log — usually a config typo (wrong output directory, wrong branch). The build command should be blank.
- **Site loads but map/charts don't render.** Open the browser console. Most likely a mixed-content warning (http://→https://) on a CDN URL. Everything in the current HTML uses https:// so this should not happen.
- **Custom domain says "unverified".** Check that Cloudflare's DNS is the authoritative nameserver for `seattledogparkdata.com` (it should be, matching Siegewords). If not, update the registrar to point at Cloudflare's nameservers.

## What's in the repo that supports this

- `docs/` — static HTML, CSS, JS (CDN-loaded Chart.js, Leaflet). Zero build step.
- No `package.json`, no Node config, no build tooling.
- Pages served as-is from `docs/`.

If we ever add a build step (e.g., for a Python-generated walkshed GeoJSON or a consolidated report.html generated from the individual pages), the build command in Cloudflare Pages should be set to whatever script produces the output, and the build output directory should remain `docs`.

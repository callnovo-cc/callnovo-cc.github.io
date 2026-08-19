# callnovo-cc.github.io — GitHub Pages User Site

This repo exists solely to serve three files at the **root** of `callnovo-cc.github.io`:

- `/robots.txt` — points crawlers to the real sitemap at `/blog/sitemap.xml`
- `/sitemap.xml` — sitemap index redirecting to `/blog/sitemap.xml`
- `/index.html` — meta-refresh + JS redirect to `/blog/`, with `noindex` to prevent duplicate-content indexing

**Do not add content here.** All Callnovo blog content lives in `callnovo-cc/blog`, published at `https://callnovo-cc.github.io/blog/`.

## Setup (one-time)

1. This repo must be named exactly `callnovo-cc.github.io` under the `callnovo-cc` organization.
2. Upload these files to the `main` branch.
3. Repo → Settings → Pages → Source: Deploy from a branch → `main`, folder: `/ (root)`. Save.
4. Wait ~60 seconds. `https://callnovo-cc.github.io/robots.txt` should return 200.

## Why this exists

GitHub Pages **project sites** (like `callnovo-cc/blog` published at `/blog/`) cannot serve files at the parent domain root. Google Search Console's sitemap health check requires a reachable `robots.txt` and `sitemap.xml` at the property root, otherwise it reports "cannot fetch." This user-site repo provides both.

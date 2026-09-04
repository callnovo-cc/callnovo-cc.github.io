# Callnovo Contact Center GitHub Pages Root Site

## Purpose

This repository owns the organization-level GitHub Pages root site at `https://callnovo-cc.github.io/`.

It is the compact gateway for **Callnovo Contact Center Insights**, directing readers to the canonical editorial library at `https://callnovo-cc.github.io/blog/` and, where appropriate, to the commercial Callnovo website at `https://callnovo.ai/`.

## Site Architecture

| Property | Role | Publishing rule |
|---|---|---|
| `https://callnovo-cc.github.io/` | Root publication gateway | Maintain only the compact gateway page and its crawler/discovery files in this repository. |
| `https://callnovo-cc.github.io/blog/` | Canonical editorial library | Publish all Insights articles, article images, Jekyll configuration, layouts, categories, and editorial SEO/schema work in the separate `callnovo-cc/blog` repository. |
| `https://callnovo.ai/` | Commercial website | Own service, product, industry, pricing, contact, and conversion pages. Editorial links may direct qualified readers here contextually. |

## Non-Negotiable Boundaries

- Do not delete this repository: its name gives it control of the `callnovo-cc.github.io` organization Pages hostname.
- Do not publish articles, article templates, duplicate service pages, Jekyll layouts, or a second content library here.
- Do not redirect the root site wholesale to `callnovo.ai`; the root page is the front door to the independent canonical Insights library.
- Do not add URL-rewrite or path-catching behavior that can affect `/blog/` or article URLs beneath it.
- Do not treat `callnovo.ai` as the canonical location for an article unless that same article is intentionally governed as a separate publishing decision. The first-published GitHub Pages article remains canonical at its own self-referencing blog URL.
- Keep root-page copy focused on the publication gateway role; do not duplicate commercial-site claims or use thin SEO-only content.

## Routine Maintenance

This repository normally requires no changes when an article is published. Normal publishing occurs in `callnovo-cc/blog`:

1. Commit the new `_posts/YYYY-MM-DD-slug.md` article and its verified image assets.
2. Verify the rendered blog post and self-referencing canonical URL.
3. Use relevant contextual links to Callnovo.ai service or contact pages.

Change this root repository only for a deliberate gateway, brand, destination, or root-domain technical update. After every root-site change, verify all of the following:

- `https://callnovo-cc.github.io/` renders correctly.
- `https://callnovo-cc.github.io/blog/` remains reachable and serves the independent Insights library.
- A representative live article under `/blog/YYYY/MM/DD/slug/` remains reachable and retains its self-referencing canonical URL.
- The root page has accurate title, description, canonical URL, and Organization/WebSite schema.

## Crawler and Sitemap Files

- `robots.txt` allows crawlers to access the root gateway and points them to this root-site sitemap.
- `sitemap.xml` lists the root gateway URL only. The independent `callnovo-cc/blog` repository owns the editorial sitemap for article discovery.

## Change Control

Any structural change to this repository must be reviewed against the live `callnovo-cc/blog` repository before it is committed. The root Pages site and the blog are separate deployments that share a hostname; changes here must never undermine the blog's canonical editorial URLs.

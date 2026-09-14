#!/usr/bin/env python3
"""Regenerate the Latest Insights list on the host-root homepage.

Reads the Jekyll-generated Atom feed for the Insights library and rewrites the
block between the POSTS:START / POSTS:END markers in index.html, plus the
<lastmod> values in the root sitemaps.

The Insights library at /blog/ generates its own sitemap (jekyll-sitemap) and
its own index listing on every build, so those need no maintenance. This script
exists solely because the host-root homepage is plain static HTML in a separate
repository and would otherwise go stale as articles are published, costing new
posts their direct crawl path from the root.

Run: python3 scripts/refresh_insights.py
Exit 0 whether or not anything changed; the workflow checks git for changes.
"""

from __future__ import annotations

import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

FEED_URL = "https://callnovo-cc.github.io/blog/feed.xml"
SITE = "https://callnovo-cc.github.io"
LIBRARY = f"{SITE}/blog/"
# Library pages that are not articles. Everything else under /blog/ in the feed
# is treated as a post, so a change to the permalink scheme in the blog's
# _config.yml does not strand entries the way a hardcoded date pattern would.
NON_ARTICLE_PATHS = {
    LIBRARY,
    f"{LIBRARY}about.html",
    f"{LIBRARY}categories/",
    f"{LIBRARY}editorial-standards/",
}
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITEMAPS = [ROOT / "sitemap.xml", ROOT / "sitemap-site.xml"]
ATOM = "{http://www.w3.org/2005/Atom}"
# The feed carries the 20 most recent posts (feed.posts_limit in the blog's
# _config.yml). Older articles keep their crawl paths through the /blog/ index,
# which lists every post, and through /blog/sitemap.xml, which contains them all.
MAX_ITEMS = 20
START = "<!-- POSTS:START"
END = "<!-- POSTS:END -->"


def fetch_feed(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "callnovo-insights-refresh/1.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 200:
            raise RuntimeError(f"feed returned HTTP {resp.status}")
        return resp.read()


def parse_entries(raw: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(raw)
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        link = entry.find(f'{ATOM}link[@rel="alternate"]')
        if link is None:
            link = entry.find(f"{ATOM}link")
        href = (link.get("href") or "").strip() if link is not None else ""
        if not href.startswith(LIBRARY) or href in NON_ARTICLE_PATHS:
            continue

        title_el = entry.find(f"{ATOM}title")
        title = "".join(title_el.itertext()).strip() if title_el is not None else ""

        # jekyll-feed emits <summary> from the post's `description` front matter,
        # which the article template already requires. If a post ever ships
        # without one, fall back to trimmed body text rather than dropping the
        # entry - the link itself is what matters for crawl discovery.
        summary = ""
        for tag in ("summary", "content"):
            el = entry.find(f"{ATOM}{tag}")
            if el is not None:
                text = "".join(el.itertext())
                summary = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()
                if summary:
                    break
        if len(summary) > 240:
            summary = summary[:240].rsplit(" ", 1)[0].rstrip(".,;:") + "..."

        published = entry.find(f"{ATOM}published")
        updated = entry.find(f"{ATOM}updated")
        stamp = (published if published is not None else updated)
        day = ""
        if stamp is not None and stamp.text:
            day = stamp.text.strip()[:10]

        if not (href and title and day):
            continue

        entries.append(
            {"url": href, "title": title, "desc": summary, "date": day}
        )

    # Newest first, de-duplicated by URL.
    seen: set[str] = set()
    unique = []
    for e in sorted(entries, key=lambda x: x["date"], reverse=True):
        if e["url"] in seen:
            continue
        seen.add(e["url"])
        unique.append(e)
    return unique[:MAX_ITEMS]


def render(entries: list[dict[str, str]]) -> str:
    lines = [
        f"{START} — generated from /blog/feed.xml by "
        ".github/workflows/refresh-insights.yml. Do not edit by hand. -->",
        '        <ul class="post-list">',
    ]
    for e in entries:
        lines.append("        <li>")
        lines.append(
            f'          <a href="{html.escape(e["url"], quote=True)}">'
            f'{html.escape(e["title"])}</a>'
        )
        if e["desc"]:
            lines.append(f'          <p>{html.escape(e["desc"])}</p>')
        lines.append(
            f'          <time datetime="{e["date"]}">{e["date"]}</time>'
        )
        lines.append("        </li>")
    lines.append("        </ul>")
    lines.append(f"        {END}")
    return "\n".join(lines)


def main() -> int:
    try:
        entries = parse_entries(fetch_feed(FEED_URL))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not read {FEED_URL}: {exc}", file=sys.stderr)
        return 1

    if not entries:
        print("ERROR: feed contained no article entries; refusing to empty the "
              "homepage list", file=sys.stderr)
        return 1

    original = INDEX.read_text(encoding="utf-8")
    start = original.find(START)
    end = original.find(END)
    if start == -1 or end == -1:
        print("ERROR: POSTS:START / POSTS:END markers missing from index.html",
              file=sys.stderr)
        return 1

    updated = original[:start] + render(entries) + original[end + len(END):]

    today = datetime.now(timezone.utc).date().isoformat()
    changed = []

    if updated != original:
        INDEX.write_text(updated, encoding="utf-8")
        changed.append("index.html")

        # Only touch <lastmod> when the article set actually changed. Bumping it
        # on every scheduled run would misreport freshness to crawlers and
        # produce a daily no-op commit.
        for path in SITEMAPS:
            text = path.read_text(encoding="utf-8")
            bumped = re.sub(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
                            f"<lastmod>{today}</lastmod>", text)
            if bumped != text:
                path.write_text(bumped, encoding="utf-8")
                changed.append(path.name)

    print(f"{len(entries)} articles in feed; newest {entries[0]['date']}")
    print("changed: " + (", ".join(changed) if changed else "nothing"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

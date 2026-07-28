#!/usr/bin/env python3
"""Tell the search engines that take a push notification that pages changed.

IndexNow is a single POST that Bing, Yandex, Naver, Seznam and Yep all read,
and they share submissions with each other. Google does not participate at
all - for Google there is Search Console and nothing else, which needs a
human with a Google account.

Ownership is proved by hosting a file named after the key, containing the key.
That file lives in public/, so it ships with the site.

Run from the repo root:  python tools/indexnow.py [url ...]
With no arguments it submits every URL in the built sitemap.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "hoijun-kim.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"


def key() -> str:
    files = list((ROOT / "public").glob("*.txt"))
    for f in files:
        if re.fullmatch(r"[0-9a-f]{8,128}", f.stem):
            return f.stem
    sys.exit("no IndexNow key file in public/ - expected <key>.txt")


def sitemap_urls() -> list[str]:
    """Prefer the sitemap just built; fall back to the deployed one, so this
    can run straight after a deploy without rebuilding the site to read it."""
    path = ROOT / "dist" / "sitemap-0.xml"
    if path.exists():
        xml = path.read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(f"https://{HOST}/sitemap-0.xml", timeout=30) as r:
            xml = r.read().decode("utf-8")
    return re.findall(r"<loc>(.*?)</loc>", xml)


def submit(urls: list[str], k: str) -> None:
    body = json.dumps(
        {"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt", "urlList": urls}
    ).encode()
    req = urllib.request.Request(
        ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            # 200 accepted, 202 accepted but the key is still being checked
            print(f"{r.status} {r.reason} for {len(urls)} url(s)")
    except urllib.error.HTTPError as e:
        print(f"{e.code} {e.reason}: {e.read().decode(errors='replace')[:200]}")
        sys.exit(1)


def main() -> None:
    k = key()
    urls = sys.argv[1:] or sitemap_urls()
    for u in urls:
        print("  ", u)
    submit(urls, k)


if __name__ == "__main__":
    main()

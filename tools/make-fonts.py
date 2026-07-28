#!/usr/bin/env python3
"""Fetch IBM Plex from Google Fonts and subset it for this site.

The page ships its own type instead of falling back to whatever the OS
provides, so that it renders the same on Windows and macOS. Only the four
faces the page actually uses are downloaded, and each one is cut down to the
characters the page can contain.

Needs: fonttools + brotli (`pip install fonttools brotli`).
Writes: fonts/*.woff2 - commit the result, this is not run at build time.
Also caches the unsubset TTFs under tools/.fonts/ (untracked), because
tools/make-icons.py draws the Open Graph card in the same faces and Pillow
cannot read woff2.
"""

import io
import pathlib
import re
import subprocess
import sys
import urllib.request

# Google serves woff2 only to browsers that ask for it.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

FACES = [
    ("IBM Plex Sans", 400, "plex-sans-400"),
    ("IBM Plex Sans", 600, "plex-sans-600"),
    ("IBM Plex Mono", 400, "plex-mono-400"),
    ("IBM Plex Mono", 500, "plex-mono-500"),
]

# Everything the page can hold: ASCII, Latin-1 (c, middot, times), the
# typographic dashes and quotes, bullet, ellipsis and the two arrows.
UNICODES = ",".join(
    [
        "U+0020-007E",
        "U+00A0-00FF",
        "U+2010-2015",
        "U+2018-201D",
        "U+2022",
        "U+2026",
        "U+2192",
        "U+2193",
        "U+2212",
    ]
)

OUT = pathlib.Path(__file__).resolve().parent.parent / "fonts"
TTF_CACHE = pathlib.Path(__file__).resolve().parent / ".fonts"

# The v1 css endpoint still answers an ancient UA with plain TrueType; css2
# only ever offers woff/woff2, which Pillow cannot open.
UA_TTF = "Mozilla/4.0"


def fetch(url: str, ua: str = UA) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def latin_url(family: str, weight: int) -> str:
    """The css2 reply is split by unicode-range; we only want the latin block."""
    sheet = fetch(
        "https://fonts.googleapis.com/css2?family="
        + family.replace(" ", "+")
        + f":wght@{weight}&display=swap"
    ).decode("utf-8")
    blocks = re.findall(r"/\*\s*([\w\[\]-]+)\s*\*/\s*(@font-face\s*\{.*?\})", sheet, re.S)
    for name, block in blocks:
        if name == "latin":
            m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
            if m:
                return m.group(1)
    raise SystemExit(f"no latin block for {family} {weight}")


def cache_ttf(family: str, weight: int, stem: str) -> None:
    """Keep a full TrueType copy for the Pillow-drawn Open Graph card."""
    sheet = fetch(
        "https://fonts.googleapis.com/css?family="
        + family.replace(" ", "+")
        + f":{weight}",
        UA_TTF,
    ).decode("utf-8")
    m = re.search(r"url\((https://[^)]+\.ttf)\)", sheet)
    if not m:
        raise SystemExit(f"no ttf for {family} {weight}")
    TTF_CACHE.mkdir(exist_ok=True)
    (TTF_CACHE / f"{stem}.ttf").write_bytes(fetch(m.group(1), UA_TTF))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    total = 0
    for family, weight, stem in FACES:
        url = latin_url(family, weight)
        raw = fetch(url)

        src = OUT / f".{stem}.src.woff2"
        dst = OUT / f"{stem}.woff2"
        src.write_bytes(raw)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "fontTools.subset",
                str(src),
                f"--unicodes={UNICODES}",
                "--layout-features=kern,liga,calt,tnum",
                "--flavor=woff2",
                "--desubroutinize",
                f"--output-file={dst}",
            ],
            check=True,
        )
        src.unlink()

        cache_ttf(family, weight, stem)

        size = dst.stat().st_size
        total += size
        print(f"{dst.name:<20} {len(raw)/1024:6.1f} KB -> {size/1024:5.1f} KB")

    print(f"{'total':<20} {'':>9} {total/1024:5.1f} KB")
    print(f"ttf cache: {TTF_CACHE}")


if __name__ == "__main__":
    main()

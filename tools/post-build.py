#!/usr/bin/env python3
"""Two things Astro cannot do, run over dist/ after `astro build`.

1. Korean type, per page. A whole Korean face is megabytes, so each page that
   contains Hangul gets its own subset cut to the characters that page actually
   uses, declared under the same family name as the latin faces with a Hangul
   `unicode-range`. The browser then picks it per character and the page's font
   stack needs no changes. A page with no Hangul downloads nothing.

2. An Open Graph card per post, drawn in the same faces as the site.

Needs: fonttools, brotli, Pillow, and the caches left by tools/make-fonts.py.
Run from the repo root:  python tools/post-build.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
CACHE = ROOT / "tools" / ".fonts"

sys.path.insert(0, str(ROOT / "tools"))

HANGUL = re.compile(
    "[ᄀ-ᇿ㄰-㆏ꥠ-꥿가-힣ힰ-퟿]"
)
# what the injected @font-face claims to cover
HANGUL_RANGE = "U+1100-11FF,U+3130-318F,U+A960-A97F,U+AC00-D7A3,U+D7B0-D7FF"

TAGS = re.compile(r"<(script|style)\b.*?</\1>|<[^>]+>", re.S | re.I)

PAPER = "#FAF9F6"
INK = "#1A1917"
INK_2 = "#46433D"
MUTED = "#6E695F"
LINE = "#E6E2DA"
ACCENT = "#0E6E5E"

BARS = [(14, 13, 22.5, 51), (41.5, 13, 50, 51), (11.5, 27.75, 52.5, 36.25)]


def visible_text(markup: str) -> str:
    return html.unescape(TAGS.sub(" ", markup))


def font(stem: str, size: int) -> ImageFont.FreeTypeFont:
    path = CACHE / f"{stem}.ttf"
    if not path.exists():
        sys.exit(f"missing {path} - run `python tools/make-fonts.py` first")
    return ImageFont.truetype(str(path), size)


# ---------------------------------------------------------------- Korean type


def subset_korean(by_weight: dict[str, set[str]], stem: str) -> dict[str, Path]:
    """Cut each weight to the characters that can actually render at it.

    A weight with nothing to show is not written at all: the home page, for
    instance, only ever shows Korean inside a 600-weight post title.
    """
    out_dir = DIST / "fonts" / "ko"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    for weight, chars in by_weight.items():
        if not chars:
            continue
        src = CACHE / f"plex-sans-kr-{weight}.ttf"
        if not src.exists():
            sys.exit(f"missing {src} - run `python tools/make-fonts.py` first")
        dst = out_dir / f"{stem}-{weight}.woff2"
        subprocess.run(
            [
                sys.executable, "-m", "fontTools.subset", str(src),
                "--unicodes=" + ",".join(f"U+{ord(c):04X}" for c in sorted(chars)),
                "--layout-features=kern,liga",
                "--flavor=woff2",
                f"--output-file={dst}",
            ],
            check=True,
        )
        written[weight] = dst
    return written


# Which weight a run of text will be asked for. Per-character font matching
# falls through to the next family in the stack, not to the site's other
# weight, so a character in the wrong bucket renders in the OS font - the two
# lists below have to match the stylesheets, and tools/check-fonts.py proves
# in a real browser that they do.
BOLD_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "strong", "b", "th"}
BOLD_CLASSES = {"row-name", "post-title", "part-title", "run-name", "ttl", "btn"}
NORMAL_CLASSES = {"q"}  # the mono chip inside the hero h1
SKIP_TAGS = {"script", "style"}


class WeightedText(HTMLParser):
    """Collects the page's text split by the weight it will be rendered at."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.bold = [False]
        self.skip = 0
        self.chars: dict[str, set[str]] = {"400": set(), "600": set()}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag in VOID_TAGS:
            return
        classes = set((dict(attrs).get("class") or "").split())
        bold = self.bold[-1]
        if tag in BOLD_TAGS or classes & BOLD_CLASSES:
            bold = True
        if classes & NORMAL_CLASSES:
            bold = False
        self.bold.append(bold)

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        if tag not in VOID_TAGS and len(self.bold) > 1:
            self.bold.pop()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        found = set(HANGUL.findall(data))
        if found:
            self.chars["600" if self.bold[-1] else "400"] |= found


VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


def face_css(stem: str, weight: str, family: str) -> str:
    return (
        f'@font-face{{font-family:"{family}";font-style:normal;'
        f"font-weight:{weight};font-display:swap;"
        f'src:url("/fonts/ko/{stem}-{weight}.woff2") format("woff2");'
        f"unicode-range:{HANGUL_RANGE}}}"
    )


def add_korean(page: Path) -> tuple[dict[str, int], int] | None:
    markup = page.read_text(encoding="utf-8")
    parser = WeightedText()
    parser.feed(markup)
    by_weight = parser.chars
    if not any(by_weight.values()):
        return None

    stem = "-".join(page.relative_to(DIST).parts[:-1]) or "index"
    files = subset_korean(by_weight, stem)

    # The mono family reuses the regular face: nothing on the site sets Korean
    # in bold mono, and a code block quoting Korean would otherwise fall out of
    # the shipped type entirely.
    css = "".join(
        face_css(stem, w, family)
        for w in files
        for family in (("Plex Sans", "Plex Mono") if w == "400" else ("Plex Sans",))
    )
    page.write_text(markup.replace("</head>", f"<style>{css}</style></head>", 1), encoding="utf-8")
    return {w: len(c) for w, c in by_weight.items() if c}, sum(f.stat().st_size for f in files.values())


# ------------------------------------------------------------------ OG cards


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int, limit: int) -> list[str]:
    """Greedy wrap that also breaks Korean, which has no spaces to break on."""
    lines: list[str] = []
    line = ""
    for word in re.findall(r"\S+\s*", text):
        probe = line + word
        if draw.textlength(probe.strip(), font=fnt) <= width or not line:
            line = probe
            continue
        lines.append(line.strip())
        line = word
        if len(lines) == limit:
            break
    if line and len(lines) < limit:
        lines.append(line.strip())

    # a single unbroken run (Korean, or a long identifier) still needs cutting
    fixed: list[str] = []
    for candidate in lines:
        while draw.textlength(candidate, font=fnt) > width and len(candidate) > 1:
            cut = candidate
            while draw.textlength(cut, font=fnt) > width and len(cut) > 1:
                cut = cut[:-1]
            fixed.append(cut)
            candidate = candidate[len(cut):]
        fixed.append(candidate)
    return fixed[:limit]


def mark(size: int, colour: str, bg: str) -> Image.Image:
    ss = 8
    px = size * ss
    k = px / 64.0
    img = Image.new("RGB", (px, px), bg)
    d = ImageDraw.Draw(img)
    for x0, y0, x1, y1 in BARS:
        d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=2.5 * k, fill=colour)
    return img.resize((size, size), Image.LANCZOS)


def og_card(title: str, date: str, korean: bool) -> Image.Image:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([36, 36, W - 37, H - 37], outline=LINE, width=2)

    x = 92
    img.paste(mark(52, INK, PAPER), (x, 92))
    label = font("plex-mono-500", 22)
    ex = x + 72
    for text, colour in (("HOIJUN KIM", INK), ("  /  WRITING", MUTED)):
        for ch in text:
            d.text((ex, 130), ch, font=label, fill=colour, anchor="ls")
            ex += d.textlength(ch, font=label) + 4

    face = font("plex-sans-kr-600" if korean else "plex-sans-600", 60)
    lines = wrap(d, title, face, W - 2 * x, 3)
    y = 340 - (len(lines) - 1) * 38  # the block grows around a fixed centre
    for line in lines:
        d.text((x, y), line, font=face, fill=INK, anchor="ls")
        y += 76

    d.rounded_rectangle([x, H - 150, x + 44, H - 146], radius=2, fill=ACCENT)
    d.text((x, H - 96), date, font=font("plex-mono-400", 24), fill=INK_2, anchor="ls")
    d.text(
        (W - x, H - 96),
        "hoijun-kim.github.io",
        font=font("plex-mono-400", 24),
        fill=MUTED,
        anchor="rs",
    )
    return img


META = {
    "title": re.compile(r'<meta property="og:title" content="([^"]*)"'),
    "date": re.compile(r'<meta property="article:published_time" content="([^"]*)"'),
    "image": re.compile(r'<meta property="og:image" content="[^"]*/og/([^"]+)\.png"'),
}


def add_card(page: Path) -> str | None:
    markup = page.read_text(encoding="utf-8")
    named = META["image"].search(markup)
    if not named:
        return None
    title = html.unescape(META["title"].search(markup).group(1))
    title = re.sub(r"\s*-\s*Hoijun Kim$", "", title)
    stamp = META["date"].search(markup)
    date = stamp.group(1)[:10] if stamp else ""

    out = DIST / "og" / f"{named.group(1)}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    og_card(title, date, bool(HANGUL.search(title))).save(out, optimize=True)
    return out.name


def main() -> None:
    if not DIST.is_dir():
        sys.exit("no dist/ - run `astro build` first")

    pages = sorted(DIST.rglob("*.html"))
    for page in pages:
        card = add_card(page)
        if card:
            print(f"og   {card}")
        korean = add_korean(page)
        if korean:
            counts, size = korean
            rel = page.relative_to(DIST)
            spread = " + ".join(f"{n}@{w}" for w, n in sorted(counts.items()))
            print(f"ko   {rel}  {spread} glyphs -> {size/1024:.1f} KB")

    print(f"post-build done over {len(pages)} page(s)")


if __name__ == "__main__":
    main()

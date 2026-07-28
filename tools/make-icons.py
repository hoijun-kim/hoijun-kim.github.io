"""Render the raster icons and the Open Graph card from favicon.svg's geometry.

Run from the repo root:  python tools/make-icons.py

Outputs favicon.ico, apple-touch-icon.png and og.png. The mark geometry is a
copy of favicon.svg (a 64-unit square); keep the two in step by hand if the
mark ever changes. The card is set in the same IBM Plex the page ships, so run
tools/make-fonts.py first - it leaves the TrueType copies Pillow needs under
tools/.fonts/. Pillow is the only other dependency.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / ".fonts"

IVORY = "#F4F1EA"
PAPER = "#FAF9F6"
INK = "#1A1917"
INK_2 = "#46433D"
MUTED = "#6E695F"
LINE = "#E6E2DA"
LINE_STRONG = "#C4BEB0"
SURFACE_2 = "#F3F1EB"
SHAPE_ORANGE = "#E07C15"
FLEET_BLUE = "#2F6BFF"

# The mark, in favicon.svg's 64-unit coordinate space: an H of three bars.
FRAME = (3, 3, 61, 61, 13)  # x0, y0, x1, y1, radius
FRAME_STROKE = 4.5
BARS = [
    (14, 13, 22.5, 51),  # left stem
    (41.5, 13, 50, 51),  # right stem
    (11.5, 27.75, 52.5, 36.25),  # crossbar, overshooting both stems
]
BAR_RADIUS = 2.5

SS = 8  # supersampling factor, for smooth corners at small sizes


def draw_mark(size, framed=True, bg=None, ink=INK, tile=IVORY, cut=False):
    """Return an image of the mark at `size` px, rendered supersampled.

    `cut` drops the canvas behind the frame so the rounded silhouette survives
    - favicon.svg has no background element, and a tab strip is often dark.
    """
    px = size * SS
    k = px / 64.0
    img = (
        Image.new("RGBA", (px, px), (0, 0, 0, 0))
        if cut
        else Image.new("RGB", (px, px), bg or tile)
    )
    d = ImageDraw.Draw(img)
    if framed:
        x0, y0, x1, y1, r = FRAME
        d.rounded_rectangle(
            [x0 * k, y0 * k, x1 * k, y1 * k],
            radius=r * k,
            fill=tile,
            outline=ink,
            width=max(1, round(FRAME_STROKE * k)),
        )
    for x0, y0, x1, y1 in BARS:
        d.rounded_rectangle(
            [x0 * k, y0 * k, x1 * k, y1 * k], radius=BAR_RADIUS * k, fill=ink
        )
    return img.resize((size, size), Image.LANCZOS)


def font(stem, size):
    path = FONTS / f"{stem}.ttf"
    if not path.exists():
        sys.exit(f"missing {path} - run `python tools/make-fonts.py` first")
    return ImageFont.truetype(str(path), size)


def tracked(draw, xy, text, fnt, fill, tracking):
    """draw.text with letter-spacing; returns the advance width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += draw.textlength(ch, font=fnt) + tracking
    return x - tracking - xy[0]


# The headline, as the page sets it: the fiddly half in a mono chip, the payoff
# underlined. Each token is (text, kind) and kinds never break across lines.
HEADLINE = [
    ("Work", "plain"),
    ("that", "plain"),
    ("usually", "plain"),
    ("needs", "plain"),
    ("a", "plain"),
    ("query language", "chip"),
    (", turned", "tight"),
    ("into", "plain"),
    ("something", "plain"),
    ("you", "plain"),
    ("can", "plain"),
    ("see and click", "under"),
    (".", "tight"),
]


def layout(draw, tokens, sans, mono, max_width, space):
    """Greedily wrap tokens; returns lines of (text, kind, x, width)."""
    lines, line, x = [], [], 0.0
    for text, kind in tokens:
        fnt = mono if kind == "chip" else sans
        w = draw.textlength(text, font=fnt)
        if kind == "chip":
            w += 26  # chip padding
        lead = 0.0 if (kind == "tight" or not line) else space
        if line and x + lead + w > max_width:
            lines.append(line)
            line, x, lead = [], 0.0, 0.0
        line.append((text, kind, x + lead, w))
        x += lead + w
    if line:
        lines.append(line)
    return lines


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([36, 36, W - 37, H - 37], outline=LINE, width=2)

    x = 92
    img.paste(draw_mark(64, bg=PAPER), (x, 88))
    ex = x + 88
    ex += tracked(d, (ex, 137), "HOIJUN KIM", font("plex-mono-500", 25), INK, 4.5) + 26
    tracked(d, (ex, 137), "/  SOFTWARE ENGINEER", font("plex-mono-400", 25), MUTED, 4.5)

    sans = font("plex-sans-600", 54)
    mono = font("plex-mono-400", 45)
    lines = layout(d, HEADLINE, sans, mono, W - x - 92, d.textlength(" ", font=sans))

    y = 268
    for line in lines:
        for text, kind, dx, w in line:
            tx = x + dx
            if kind == "chip":
                d.rounded_rectangle(
                    [tx, y - 44, tx + w, y + 14], radius=10, fill=SURFACE_2, outline=LINE
                )
                d.text((tx + 13, y), text, font=mono, fill=INK_2, anchor="ls")
            else:
                d.text((tx, y), text, font=sans, fill=INK, anchor="ls")
                if kind == "under":
                    d.rectangle([tx, y + 11, tx + w, y + 15], fill=LINE_STRONG)
        y += 72

    # The two projects, each behind its own colour - the same bars the site uses.
    name = font("plex-sans-600", 30)
    note = font("plex-mono-400", 22)
    y = H - 118
    for label, colour, blurb in (
        ("shape", SHAPE_ORANGE, "any data file, no jq or SQL"),
        ("fleet", FLEET_BLUE, "every git repo, one board"),
    ):
        d.rounded_rectangle([x, y - 24, x + 4, y + 6], radius=2, fill=colour)
        d.text((x + 20, y), label, font=name, fill=INK, anchor="ls")
        d.text((x + 20 + d.textlength(label, font=name) + 18, y), blurb, font=note, fill=MUTED, anchor="ls")
        y += 48

    d.text(
        (W - 92, H - 76),
        "hoijun-kim.github.io",
        font=font("plex-mono-400", 24),
        fill=MUTED,
        anchor="rs",
    )
    return img


def main():
    # iOS masks the corners itself, so the touch icon is full-bleed and unframed.
    touch = Image.new("RGB", (180, 180), IVORY)
    touch.paste(draw_mark(140, framed=False), (20, 20))
    touch.save(ROOT / "apple-touch-icon.png")

    ico = draw_mark(64, cut=True)
    ico.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    make_og().save(ROOT / "og.png", optimize=True)
    print("wrote favicon.ico, apple-touch-icon.png, og.png")


if __name__ == "__main__":
    main()

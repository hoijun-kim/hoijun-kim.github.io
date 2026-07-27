"""Render the raster icons and the Open Graph card from favicon.svg's geometry.

Run from the repo root:  python tools/make-icons.py

Outputs favicon.ico, apple-touch-icon.png and og.png. The mark geometry is a
copy of favicon.svg (a 64-unit square); keep the two in step by hand if the
mark ever changes. Pillow is the only dependency - no SVG rasteriser needed.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("C:/Windows/Fonts")

IVORY = "#F4F1EA"
PAPER = "#FAF9F6"
INK = "#1A1917"
INK_2 = "#45423C"
MUTED = "#8A8478"
LINE = "#E6E2DA"
SHAPE_ORANGE = "#E07C15"
FLEET_BLUE = "#2F6BFF"

# The mark, in favicon.svg's 64-unit coordinate space.
FRAME = (3, 3, 61, 61, 13)  # x0, y0, x1, y1, radius
FRAME_STROKE = 4.5
LETTER = [
    (20.5, 15, 27.5, 49),  # left stem
    (36.5, 15, 43.5, 49),  # right stem
    (27.5, 28, 36.5, 34),  # crossbar
    (16.5, 15, 31.5, 18.75),  # serifs, clockwise from top left
    (32.5, 15, 47.5, 18.75),
    (16.5, 45.25, 31.5, 49),
    (32.5, 45.25, 47.5, 49),
]

SS = 8  # supersampling factor, for smooth corners at small sizes


def draw_mark(size, framed=True, bg=None):
    """Return an RGB image of the mark at `size` px, rendered supersampled."""
    px = size * SS
    k = px / 64.0
    img = Image.new("RGB", (px, px), bg or IVORY)
    d = ImageDraw.Draw(img)
    if framed:
        x0, y0, x1, y1, r = FRAME
        d.rounded_rectangle(
            [x0 * k, y0 * k, x1 * k, y1 * k],
            radius=r * k,
            fill=IVORY,
            outline=INK,
            width=max(1, round(FRAME_STROKE * k)),
        )
    for x0, y0, x1, y1 in LETTER:
        d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=INK)
    return img.resize((size, size), Image.LANCZOS)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def tracked(draw, xy, text, fnt, fill, tracking):
    """draw.text with letter-spacing; returns the advance width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += draw.textlength(ch, font=fnt) + tracking
    return x - tracking - xy[0]


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([36, 36, W - 37, H - 37], outline=LINE, width=2)

    img.paste(draw_mark(96, bg=PAPER), (972, 96))

    x = 100
    tracked(d, (x, 186), "SOFTWARE ENGINEER", font("segoeuib.ttf", 26), MUTED, 6)
    d.text((x, 320), "Hoijun Kim", font=font("georgiab.ttf", 118), fill=INK, anchor="ls")
    d.rectangle([x, 360, x + 96, 364], fill=INK)
    d.text(
        (x, 434),
        "Fast, friendly developer tools.",
        font=font("georgiai.ttf", 40),
        fill=INK_2,
        anchor="ls",
    )

    # The two projects, each behind its own colour - the same dots the site uses.
    fnt = font("georgia.ttf", 34)
    y = 522
    for label, colour in (("shape", SHAPE_ORANGE), ("fleet", FLEET_BLUE)):
        d.ellipse([x, y - 16, x + 13, y - 3], fill=colour)
        d.text((x + 26, y), label, font=fnt, fill=INK_2, anchor="ls")
        x += 26 + d.textlength(label, font=fnt) + 44
    d.text(
        (W - 100, y),
        "hoijun-kim.github.io",
        font=font("segoeui.ttf", 27),
        fill=MUTED,
        anchor="rs",
    )
    return img


def main():
    # iOS masks the corners itself, so the touch icon is full-bleed and unframed.
    touch = Image.new("RGB", (180, 180), IVORY)
    inner = draw_mark(140, framed=False)
    touch.paste(inner, (20, 20))
    touch.save(ROOT / "apple-touch-icon.png")

    ico = draw_mark(64)
    ico.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    make_og().save(ROOT / "og.png", optimize=True)
    print("wrote favicon.ico, apple-touch-icon.png, og.png")


if __name__ == "__main__":
    main()

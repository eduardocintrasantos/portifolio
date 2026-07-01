"""Generate LinkedIn profile cover banner (1584 x 396 px)."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH, HEIGHT = 1584, 396
OUT = Path(__file__).resolve().parent.parent / "img" / "linkedin-banner.png"

BG_TOP = (8, 12, 22)
BG_BOTTOM = (15, 22, 38)
ACCENT = (59, 130, 246)
ACCENT_SOFT = (96, 165, 250)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)
SURFACE = (22, 30, 48)

SAFE_LEFT = 420

TECH = [
    ("Java", (244, 114, 36)),
    ("Spring Boot", (110, 180, 64)),
    ("PostgreSQL", (59, 130, 246)),
    ("Docker", (56, 189, 248)),
    ("Flyway", (167, 139, 250)),
    ("Git", (248, 113, 113)),
    ("Railway", (129, 140, 248)),
    ("JDBC", (52, 211, 153)),
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def vertical_gradient(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def add_glow_layer(base: Image.Image) -> Image.Image:
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)

    for r in range(220, 0, -3):
        alpha = int(22 * (r / 220) ** 1.6)
        draw.ellipse(
            [WIDTH - 180 - r, -120 - r // 2, WIDTH + 60 + r, 200 + r],
            fill=(ACCENT[0], ACCENT[1], ACCENT[2], alpha),
        )

    for r in range(160, 0, -3):
        alpha = int(10 * (r / 160) ** 1.8)
        draw.ellipse(
            [520 - r, 80 - r, 820 + r, 320 + r],
            fill=(ACCENT_SOFT[0], ACCENT_SOFT[1], ACCENT_SOFT[2], alpha),
        )

    glow = glow.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")


def draw_tech_chip(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    color: tuple[int, int, int],
    font: ImageFont.FreeTypeFont,
) -> int:
    pad_x = 16
    text_w = draw.textlength(label, font=font)
    w = int(text_w + pad_x * 2)
    h = 34

    draw.rounded_rectangle([x, y, x + w, y + h], radius=17, fill=SURFACE, outline=(50, 62, 86), width=1)
    dot_r = 4
    dot_x = x + 12
    dot_y = y + h // 2
    draw.ellipse([dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r], fill=color)
    draw.text((x + 24, y + 8), label, fill=TEXT, font=font)
    return w + 12


def draw_coffee_cup(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    """Minimal coffee cup with steam."""
    s = scale
    cup_w, cup_h = int(44 * s), int(34 * s)
    cx, cy = x, y

    steam_color = (ACCENT_SOFT[0], ACCENT_SOFT[1], ACCENT_SOFT[2], 160)
    for i, dx in enumerate((-8, 0, 8)):
        sx = cx + cup_w // 2 + int(dx * s)
        points = []
        for step in range(6):
            sy = cy - int((10 + step * 7) * s)
            sway = int(math.sin(step * 1.2 + i) * 4 * s)
            points.append((sx + sway, sy))
        if len(points) >= 2:
            draw.line(points, fill=steam_color, width=max(2, int(2 * s)), joint="curve")

    draw.ellipse(
        [cx - int(4 * s), cy + cup_h - int(2 * s), cx + cup_w + int(4 * s), cy + cup_h + int(10 * s)],
        fill=(180, 140, 100, 220),
        outline=(210, 170, 130, 240),
        width=max(1, int(2 * s)),
    )

    draw.rounded_rectangle(
        [cx, cy, cx + cup_w, cy + cup_h],
        radius=int(6 * s),
        fill=(245, 235, 220),
        outline=(210, 190, 170),
        width=max(1, int(2 * s)),
    )

    draw.rounded_rectangle(
        [cx + int(4 * s), cy + int(4 * s), cx + cup_w - int(4 * s), cy + int(12 * s)],
        radius=int(4 * s),
        fill=(120, 72, 48),
    )

    hx = cx + cup_w - int(2 * s)
    hy = cy + int(8 * s)
    draw.arc(
        [hx, hy, hx + int(18 * s), hy + int(22 * s)],
        start=270,
        end=90,
        fill=(210, 190, 170),
        width=max(2, int(3 * s)),
    )


def draw_server_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0) -> None:
    w, h, gap = int(52 * scale), int(14 * scale), int(8 * scale)
    x0 = cx - w // 2
    color = (ACCENT[0], ACCENT[1], ACCENT[2], 180)
    border = (ACCENT_SOFT[0], ACCENT_SOFT[1], ACCENT_SOFT[2], 120)

    for i in range(3):
        y = cy - (h * 3 + gap * 2) // 2 + i * (h + gap)
        draw.rounded_rectangle([x0, y, x0 + w, y + h], radius=4, outline=border, width=2)
        dot_y = y + h // 2
        for dx in (10, 20):
            draw.ellipse([x0 + dx - 2, dot_y - 2, x0 + dx + 2, dot_y + 2], fill=color)
        bar_w = int(w * 0.45)
        draw.rounded_rectangle(
            [x0 + w - bar_w - 8, y + 4, x0 + w - 8, y + h - 4],
            radius=2,
            fill=(ACCENT[0], ACCENT[1], ACCENT[2], 50),
        )


def main() -> None:
    img = vertical_gradient((WIDTH, HEIGHT))
    img = add_glow_layer(img)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    draw_server_icon(odraw, WIDTH - 130, HEIGHT // 2 - 10, scale=1.15)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)

    title_font = load_font(42, bold=True)
    sub_font = load_font(17)
    chip_font = load_font(14)
    url_font = load_font(15, bold=True)

    draw.text((SAFE_LEFT, 48), "Backend", fill=TEXT, font=title_font)
    draw.text((SAFE_LEFT, 100), "Developer", fill=ACCENT_SOFT, font=title_font)

    dev_w = draw.textlength("Developer", font=title_font)
    cup_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cup_draw = ImageDraw.Draw(cup_overlay)
    draw_coffee_cup(cup_draw, int(SAFE_LEFT + dev_w + 20), 78, scale=1.1)
    img = Image.alpha_composite(img.convert("RGBA"), cup_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.text(
        (SAFE_LEFT, 160),
        "Construindo APIs robustas, seguras e escaláveis",
        fill=MUTED,
        font=sub_font,
    )

    chip_y = 206
    chip_x = SAFE_LEFT
    max_x = WIDTH - 320
    row = 0
    for label, color in TECH:
        chip_w = int(draw.textlength(label, font=chip_font) + 52)
        if chip_x + chip_w > max_x:
            row += 1
            chip_x = SAFE_LEFT
            chip_y = 206 + row * 44
        chip_x += draw_tech_chip(draw, chip_x, chip_y, label, color, chip_font)

    url = "portifolio-production-1d5f.up.railway.app"
    url_w = draw.textlength(url, font=url_font)
    pill_x = WIDTH - url_w - 56
    pill_y = HEIGHT - 54
    draw.rounded_rectangle(
        [pill_x - 20, pill_y - 10, pill_x + url_w + 20, pill_y + 28],
        radius=20,
        fill=(26, 36, 58),
        outline=ACCENT,
        width=1,
    )
    draw.text((pill_x, pill_y), url, fill=TEXT, font=url_font)

    draw.rectangle([0, HEIGHT - 3, WIDTH, HEIGHT], fill=ACCENT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Saved: {OUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()

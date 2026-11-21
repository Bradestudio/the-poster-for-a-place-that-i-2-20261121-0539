#!/usr/bin/env python3
"""Build the VELMORA travel poster (1024x1024 PNG).

Drawn procedurally with Pillow at 2x supersampling, then downscaled.
Fully deterministic: fixed seed, no clock, no network, no external
assets -- only fonts already on the machine.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2                      # supersample factor
W, H = 1024 * S, 1024 * S
OUT = "entry.png"

rng = random.Random(20261121)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(w, h):
    stops = [
        (0.00, (16, 12, 54)),     # deep indigo night top
        (0.30, (58, 32, 92)),     # violet
        (0.52, (146, 62, 96)),    # rose dusk
        (0.68, (226, 122, 74)),   # amber horizon
        (0.78, (250, 178, 105)),  # golden band
        (1.00, (252, 214, 150)),  # warm haze at the bottom
    ]
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                px[0, y] = lerp(c0, c1, (t - t0) / (t1 - t0) if t1 > t0 else 0)
                break
    return img.resize((w, h))


def tracked_width(draw, text, font, tracking):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=font) + tracking
    return w - tracking


def draw_tracked(draw, cx, y, text, font, fill, tracking):
    w = tracked_width(draw, text, font, tracking)
    x = cx - w / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def soft_circle(layer, cx, cy, r, color):
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def cloud(layer, cx, cy, rx, ry, color, n=9):
    """A soft cloud built from overlapping ellipses, blurred later."""
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        ox = rng.uniform(-rx * 0.75, rx * 0.75)
        oy = rng.uniform(-ry * 0.45, ry * 0.45)
        ex = rng.uniform(rx * 0.35, rx * 0.62)
        ey = rng.uniform(ry * 0.5, ry * 0.95)
        d.ellipse([cx + ox - ex, cy + oy - ey, cx + ox + ex, cy + oy + ey],
                  fill=color)


img = sky_gradient(W, H)
draw = ImageDraw.Draw(img, "RGBA")

# ---- stars in the upper sky ----
for _ in range(150):
    x = rng.uniform(0, W)
    y = rng.uniform(0, H * 0.34)
    r = rng.uniform(0.8, 2.6) * S
    a = rng.randint(90, 230)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, a))

# ---- big golden moon, upper right (below the name band) ----
moon_cx, moon_cy, moon_r = int(W * 0.84), int(H * 0.335), int(82 * S)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
soft_circle(glow, moon_cx, moon_cy, int(moon_r * 1.7), (255, 214, 140, 60))
soft_circle(glow, moon_cx, moon_cy, int(moon_r * 1.25), (255, 220, 150, 70))
glow = glow.filter(ImageFilter.GaussianBlur(18 * S))
img = Image.alpha_composite(img.convert("RGBA"), glow)
draw = ImageDraw.Draw(img, "RGBA")
draw.ellipse([moon_cx - moon_r, moon_cy - moon_r,
              moon_cx + moon_r, moon_cy + moon_r], fill=(255, 233, 176, 255))
for _ in range(14):  # faint craters
    a = rng.uniform(0, math.tau)
    d = rng.uniform(0, moon_r * 0.72)
    cx, cy = moon_cx + math.cos(a) * d, moon_cy + math.sin(a) * d
    cr = rng.uniform(moon_r * 0.05, moon_r * 0.13)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                 fill=(238, 205, 140, 110))

# ---- distant birds ----
for bx, by, s in [(0.20, 0.30, 1.0), (0.27, 0.26, 0.8), (0.33, 0.33, 0.9),
                  (0.62, 0.36, 0.7), (0.15, 0.40, 0.75)]:
    x, y, k = int(W * bx), int(H * by), 14 * S * s
    draw.arc([x - k, y - k * 0.7, x, y + k * 0.7], 200, 340,
             fill=(30, 18, 50, 220), width=int(3 * S))
    draw.arc([x, y - k * 0.7, x + k, y + k * 0.7], 200, 340,
             fill=(30, 18, 50, 220), width=int(3 * S))

# ---- sea of clouds, lower third (soft layers) ----
cloud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
for cx, cy, rx, ry, col in [
        (0.12, 0.86, 0.34, 0.075, (255, 226, 196, 235)),
        (0.45, 0.90, 0.40, 0.085, (250, 205, 175, 240)),
        (0.80, 0.87, 0.36, 0.075, (255, 230, 200, 235)),
        (0.30, 0.96, 0.42, 0.09, (244, 196, 168, 245)),
        (0.68, 0.97, 0.44, 0.09, (255, 220, 188, 245)),
        (0.50, 0.78, 0.30, 0.05, (255, 214, 178, 200)),
        (0.08, 0.76, 0.20, 0.04, (255, 210, 175, 170)),
        (0.92, 0.75, 0.18, 0.04, (255, 212, 176, 170)),
]:
    cloud(cloud_layer, int(W * cx), int(H * cy), int(W * rx), int(H * ry), col)
cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(9 * S))
img = Image.alpha_composite(img, cloud_layer)
draw = ImageDraw.Draw(img, "RGBA")

# ---- floating island ----
# plateau top
ix0, ix1 = int(W * 0.16), int(W * 0.84)
plateau_y = int(H * 0.47)
# rocky underside: jagged inverted cone down to a point
rock = [(ix0, plateau_y), (ix1, plateau_y)]
tip_x, tip_y = int(W * 0.50), int(H * 0.74)
nseg = 9
for i in range(1, nseg):
    t = i / nseg
    x = ix1 - (ix1 - tip_x) * t + rng.uniform(-14, 14) * S
    y = plateau_y + (tip_y - plateau_y) * t
    rock.append((x, y))
rock.append((tip_x, tip_y))
for i in range(nseg - 1, 0, -1):
    t = i / nseg
    x = ix0 + (tip_x - ix0) * t + rng.uniform(-14, 14) * S
    y = plateau_y + (tip_y - plateau_y) * t
    rock.append((x, y))
draw.polygon(rock, fill=(74, 44, 66, 255))
# rock shading facets
for _ in range(26):
    t = rng.uniform(0.05, 0.95)
    x = ix0 + (ix1 - ix0) * t
    wdt = rng.uniform(6, 26) * S
    y0 = plateau_y + rng.uniform(0, (tip_y - plateau_y) * 0.55)
    y1 = y0 + rng.uniform(30, 110) * S
    col = (96, 60, 84, 160) if rng.random() < 0.5 else (52, 30, 52, 180)
    draw.polygon([(x - wdt, y0), (x + wdt, y0), (x + wdt * 0.4, y1),
                  (x - wdt * 0.4, y1)], fill=col)
# grassy plateau cap
draw.ellipse([ix0 - 8 * S, plateau_y - 26 * S, ix1 + 8 * S, plateau_y + 14 * S],
             fill=(46, 94, 58, 255))
draw.ellipse([ix0 - 8 * S, plateau_y - 26 * S, ix1 + 8 * S, plateau_y + 2 * S],
             fill=(86, 140, 74, 255))

# ---- waterfalls pouring off the island edges ----
fall_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(fall_layer)
for fx, ftop, fbot, fwid in [(0.205, 0.475, 0.68, 10),
                             (0.795, 0.475, 0.70, 9),
                             (0.50, 0.478, 0.64, 5)]:
    x0 = int(W * fx)
    pts = []
    for i in range(25):
        t = i / 24
        pts.append((x0 + math.sin(t * 4.2) * 22 * S * (1 if fx < 0.5 else -1),
                    int(H * ftop) + (int(H * fbot) - int(H * ftop)) * t))
    # taper + fade toward the bottom: draw in segments, alpha falling
    for i in range(len(pts) - 1):
        t = i / (len(pts) - 1)
        a = int(215 * (1 - t * 0.75))
        wdt = max(1, int(fwid * S * (1 - t * 0.45)))
        fd.line([pts[i], pts[i + 1]], fill=(235, 246, 255, a), width=wdt)
fall_layer = fall_layer.filter(ImageFilter.GaussianBlur(2 * S))
img = Image.alpha_composite(img, fall_layer)
draw = ImageDraw.Draw(img, "RGBA")

# ---- village on the plateau: whitewashed houses, terracotta roofs ----
def house(x, y, w, h, roof_h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 240, 220, 255))
    draw.polygon([(x - 4 * S, y), (x + w + 4 * S, y),
                  (x + w / 2, y - roof_h)], fill=(178, 74, 52, 255))
    # glowing windows
    for wx in (x + w * 0.28, x + w * 0.68):
        draw.rectangle([wx - 4 * S, y + h * 0.35, wx + 4 * S, y + h * 0.62],
                       fill=(255, 196, 110, 255))

base = plateau_y - 16 * S
house(int(W * 0.20), base - 34 * S, 52 * S, 34 * S, 20 * S)
house(int(W * 0.27), base - 46 * S, 62 * S, 46 * S, 24 * S)
house(int(W * 0.35), base - 30 * S, 46 * S, 30 * S, 18 * S)
house(int(W * 0.56), base - 40 * S, 56 * S, 40 * S, 22 * S)
house(int(W * 0.63), base - 30 * S, 44 * S, 30 * S, 17 * S)
# cypress trees
for tx, th in [(0.245, 52), (0.42, 64), (0.475, 46), (0.70, 58)]:
    x = int(W * tx)
    draw.polygon([(x - 9 * S, base), (x + 9 * S, base),
                  (x, base - th * S)], fill=(28, 66, 44, 255))
    draw.rectangle([x - 2 * S, base - 6 * S, x + 2 * S, base],
                   fill=(60, 40, 30, 255))

# ---- lighthouse on the right end of the plateau ----
lx = int(W * 0.755)
lh = 96 * S
lw = 30 * S
draw.rectangle([lx - lw // 2, base - lh, lx + lw // 2, base],
               fill=(250, 244, 230, 255))
for i, y0 in enumerate(range(0, lh, lh // 4)):
    if i % 2 == 0:
        draw.rectangle([lx - lw // 2, base - lh + y0,
                        lx + lw // 2, base - lh + y0 + lh // 4],
                       fill=(178, 52, 48, 255))
draw.polygon([(lx - lw // 2 - 4 * S, base - lh),
              (lx + lw // 2 + 4 * S, base - lh),
              (lx, base - lh - 22 * S)], fill=(40, 32, 54, 255))
draw.rectangle([lx - 9 * S, base - lh - 12 * S, lx + 9 * S, base - lh + 2 * S],
               fill=(255, 214, 130, 255))
# light beam sweeping left across the dusk: narrow, soft, low alpha
beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bx, by = lx - 10 * S, base - lh + 2 * S
bd.polygon([(bx, by), (int(W * 0.10), by - 34 * S),
            (int(W * 0.10), by + 12 * S)], fill=(255, 226, 150, 42))
beam = beam.filter(ImageFilter.GaussianBlur(6 * S))
img = Image.alpha_composite(img, beam)
draw = ImageDraw.Draw(img, "RGBA")
# lamp glow (small, tight to the lamp so it does not read as a second moon)
glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
soft_circle(glow2, lx, base - lh, 26 * S, (255, 220, 140, 90))
img = Image.alpha_composite(img, glow2)
draw = ImageDraw.Draw(img, "RGBA")

# ---- soft shadow under the island ----
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sh)
sd.ellipse([int(W * 0.22), int(H * 0.755), int(W * 0.78), int(H * 0.815)],
           fill=(60, 30, 70, 90))
sh = sh.filter(ImageFilter.GaussianBlur(12 * S))
img = Image.alpha_composite(img, sh)
draw = ImageDraw.Draw(img, "RGBA")

# ---- typography ----
cream = (255, 243, 214, 255)
gold = (255, 205, 120, 255)
f_name = ImageFont.truetype(SERIF_BLACK, 118 * S)
f_tag = ImageFont.truetype(SANS_BOLD, 27 * S)
f_small = ImageFont.truetype(SANS, 22 * S)

# name with soft drop shadow
name = "VELMORA"
nw = tracked_width(draw, name, f_name, 26 * S)
nx = (W - nw) / 2
draw_tracked(draw, W // 2 + 3 * S, 62 * S + 4 * S, name, f_name,
             (20, 10, 40, 160), 26 * S)
draw_tracked(draw, W // 2, 62 * S, name, f_name, cream, 26 * S)
# gold rule under the name
ry = 62 * S + 118 * S + 26 * S
draw.line([(W // 2 - 150 * S, ry), (W // 2 + 150 * S, ry)],
          fill=gold, width=3 * S)
draw.ellipse([W // 2 - 5 * S, ry - 5 * S, W // 2 + 5 * S, ry + 5 * S],
             fill=gold)
# tagline
draw_tracked(draw, W // 2, ry + 22 * S, "THE ISLAND ABOVE THE CLOUDS",
             f_tag, cream, 12 * S)
# warm rim light along the rock's left edge (tip -> top-left)
draw.line(rock[nseg + 1:] + [rock[0]], fill=(255, 176, 110, 200),
          width=3 * S)
# bottom line (dark warm brown so it reads on the pale clouds)
draw_tracked(draw, W // 2, H - 78 * S, "REACHED ONLY BY SKY FERRY",
             ImageFont.truetype(SANS, 24 * S), (122, 64, 58, 255), 8 * S)

# ---- poster border ----
m = 26 * S
draw.rectangle([m, m, W - m, H - m], outline=(255, 243, 214, 220),
               width=3 * S)
draw.rectangle([m + 10 * S, m + 10 * S, W - m - 10 * S, H - m - 10 * S],
               outline=(255, 243, 214, 110), width=1 * S)

img = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("saved", OUT)

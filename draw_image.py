#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page: one 1024x1024 PNG.

Stories verified on the morning of 21 Nov 2026 (UTC) from AP, Reuters,
Al Jazeera, the Financial Times, BBC and Euronews. Run: python3 draw_image.py
writes entry.png next to this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (16, 32, 58)
NAVY2 = (24, 48, 84)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
PAPER = (250, 247, 240)
INK = (22, 22, 22)
GREY = (88, 88, 88)
CARD = (255, 255, 255)
SKY = (18, 38, 74)
GREEN = (28, 120, 70)
BLUE = (28, 80, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box, edge):
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=edge, width=3)


# ---------------------------------------------------------------- scene art
# Each scene draws inside a box (x, y, w, h) about 288 x 74 px.
def scene_poland(d, x, y, w, h):
    """Night sky over Poland: missile trails and an explosion."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for sx, sy in [(18, 18), (70, 40), (150, 14), (210, 34), (255, 52)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    for tx, ty, ln in [(16, 40, 80), (90, 48, 100), (180, 34, 70)]:
        d.line([x + tx, y + ty, x + tx + ln, y + ty + 12], fill=(255, 200, 90), width=4)
        d.ellipse([x + tx + ln - 4, y + ty + 8, x + tx + ln + 8, y + ty + 20],
                  fill=(255, 240, 180))
    cx, cy = x + w - 55, y + h - 52
    for r, col in [(36, (255, 120, 20)), (24, (255, 170, 40)), (13, (255, 230, 120))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.text((x + 10, y + h - 26), "POLAND", font=font(SANS_B, 18), fill=(255, 255, 255))


def scene_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(246, 236, 236))
    pts = [(x + 10, y + 26), (x + 60, y + 32), (x + 105, y + 30),
           (x + 150, y + 42), (x + 195, y + 50), (x + 240, y + 60),
           (x + w - 12, y + h - 6)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.polygon(pts + [(x + w - 12, y + h), (x + 10, y + h)], fill=(214, 48, 49))
    d.text((x + 10, y + 4), "S&P 500  -3.7%", font=font(SANS_B, 20), fill=RED)


def scene_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    base = y + h
    for bx, bw, bh in [(8, 30, 40), (44, 24, 56), (74, 34, 34), (114, 26, 60),
                       (146, 32, 38), (184, 26, 52), (216, 30, 42)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(12, 12, 20))
        for wy in range(base - bh + 6, base - 4, 14):
            d.rectangle([x + bx + 6, wy, x + bx + 11, wy + 6], fill=(255, 200, 80))
    for cx, cy in [(x + 56, y + 24), (x + 190, y + 22)]:
        for r, col in [(17, (255, 110, 20)), (11, (255, 180, 60)), (5, (255, 240, 150))]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.text((x + 10, y + h - 24), "KYIV  ·  KRYVYI RIH", font=font(SANS_B, 16),
           fill=(255, 255, 255))


def scene_denmark(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 248))
    for px in range(x + 12, x + w - 8, 20):
        d.line([px, y + 12, px, y + h - 10], fill=(70, 90, 120), width=3)
    d.line([x + 8, y + 18, x + w - 8, y + 18], fill=(70, 90, 120), width=3)
    d.rounded_rectangle([x + 38, y + 24, x + w - 38, y + h - 10], radius=6,
                        fill=CARD, outline=RED, width=4)
    d.text((x + 62, y + 30), "EXPELLED", font=font(SANS_B, 24), fill=RED)


def scene_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 22, 14))
    cx, cy = x + w // 2, y + h - 4
    for r, col in [(24, (220, 60, 10)), (17, (245, 130, 20)), (10, (255, 210, 60))]:
        d.ellipse([cx - r, cy - r - 10, cx + r, cy + r], fill=col)
    d.polygon([(cx - 6, cy - 20), (cx + 6, cy - 20), (cx, cy - 36)], fill=(255, 210, 60))
    d.text((x + 10, y + 6), "GUILTY  ·  2 COUNTS", font=font(SANS_B, 18),
           fill=(255, 255, 255))


def scene_peace(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 240, 228))
    cx, cy = x + w // 2, y + h // 2 + 2
    d.ellipse([cx - 46, cy - 12, cx + 38, cy + 14], fill=(255, 255, 255),
              outline=(110, 130, 110), width=2)
    d.ellipse([cx + 22, cy - 20, cx + 44, cy - 2], fill=(255, 255, 255),
              outline=(110, 130, 110), width=2)
    d.polygon([(cx + 40, cy - 14), (cx + 56, cy - 9), (cx + 40, cy - 5)],
              fill=(230, 140, 40))
    d.polygon([(cx - 38, cy - 10), (cx - 76, cy - 32), (cx - 16, cy - 18)],
              fill=(150, 185, 150), outline=(90, 120, 90))
    d.ellipse([cx + 32, cy - 16, cx + 37, cy - 11], fill=INK)
    d.line([cx - 60, cy + 20, cx - 18, cy + 30], fill=GREEN, width=3)
    for lx, ly in [(-54, 22), (-40, 26), (-26, 30)]:
        d.ellipse([cx + lx, cy + ly, cx + lx + 10, cy + ly + 6], fill=GREEN)
    d.text((x + 10, y + 4), "PEACE BY JANUARY?", font=font(SANS_B, 18), fill=GREEN)


def scene_eu_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 238, 250))
    d.rectangle([x + 16, y + 8, x + 96, y + 44], fill=(0, 51, 153))
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = x + 56 + int(12 * math.cos(a))
        sy = y + 26 + int(12 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.rectangle([x + w - 96, y + 8, x + w - 16, y + 44], fill=(1, 33, 105))
    d.line([x + w - 96, y + 8, x + w - 16, y + 44], fill=(255, 255, 255), width=5)
    d.line([x + w - 96, y + 44, x + w - 16, y + 8], fill=(255, 255, 255), width=5)
    d.line([x + w - 56, y + 8, x + w - 56, y + 44], fill=(200, 16, 46), width=7)
    d.line([x + w - 96, y + 26, x + w - 16, y + 26], fill=(200, 16, 46), width=7)
    d.text((x + w // 2 - 46, y + 46), "DEAL SIGNED", font=font(SANS_B, 15), fill=NAVY)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 14), "THE WORLD IN ONE IMAGE", font=font(SANS_B, 26), fill=GOLD)
    d.text((32, 46), "SATURDAY 21 NOVEMBER 2026",
           font=font(SERIF_B, 46), fill=(255, 255, 255))
    d.rectangle([0, 112, W, 118], fill=GOLD)

    # ---------------- lead story ----------------
    card(d, [24, 134, 1000, 452], RED)
    d.text((44, 152), "LEAD  ·  EUROPE  ·  NATO ON ALERT",
           font=font(SANS_B, 17), fill=RED)
    d.text((44, 180), "RUSSIAN MISSILES", font=font(SERIF_B, 46), fill=INK)
    d.text((44, 232), "LAND IN POLAND", font=font(SERIF_B, 46), fill=INK)
    para(d, (44, 306),
         "Two Russian missiles and a suspected drone came down in "
         "Poland during a huge overnight attack on Ukraine. "
         "Warsaw calls it a deliberate provocation; NATO calls it a "
         "\u201cgrave violation\u201d of allied airspace. No one was hurt.",
         font(SANS, 21), INK, 496, 28)
    scene_poland(d, 580, 152, 400, 282)

    # ---------------- story panels ----------------
    panels = [
        (24, 468, 316, 248, "MARKETS  ·  USA", "Wall Street slides into correction",
         "S&P 500 and Dow enter correction; Nasdaq falls 5.3% as AI "
         "shares plunge.",
         scene_market, RED),
        (354, 468, 316, 248, "WAR  ·  UKRAINE", "Overnight barrage kills eight",
         "400+ drones and 110 missiles hit Kyiv and Kryvyi Rih "
         "\u2014 two dead, 42 hurt.",
         scene_ukraine, NAVY2),
        (684, 468, 316, 248, "EUROPE  ·  ESPIONAGE", "Denmark expels envoy; Estonia shuts border",
         "Copenhagen expels Russia\u2019s defence attach\u00e9 over an alleged "
         "plot to kill rapper Kyivstoner.",
         scene_denmark, NAVY2),
        (24, 732, 316, 248, "JUSTICE  ·  USA", "Guilty: man who lit the Palisades Fire",
         "A Los Angeles jury convicts Jonathan Rinderknecht, 30, on two "
         "arson counts.",
         scene_fire, RED),
        (354, 732, 316, 248, "DIPLOMACY", "Trump pushes Ukraine peace by January",
         "The White House wants a Kyiv\u2013Moscow deal by early January, "
         "the FT reports.",
         scene_peace, GREEN),
        (684, 732, 316, 248, "BRITAIN  ·  EUROPE", "UK and EU sign three deals",
         "London and Brussels agree deals on food trade, carbon markets "
         "and youth mobility.",
         scene_eu_uk, BLUE),
    ]
    for (x, y, w, h, kick, head, body, scene, accent) in panels:
        card(d, [x, y, x + w, y + h], accent)
        d.rectangle([x, y, x + w, y + 6], fill=accent)
        d.text((x + 14, y + 16), kick, font=font(SANS_B, 17), fill=accent)
        hy = para(d, (x + 14, y + 40), head, font(SANS_B, 23), INK, w - 28, 28)
        para(d, (x + 14, hy + 6), body, font(SANS, 17), (60, 60, 60), w - 28, 21)
        scene(d, x + 14, y + h - 80, w - 28, 66)

    # footer
    d.text((24, 994), "Sources: AP · Reuters · Al Jazeera · Financial Times · BBC · Euronews",
           font=font(SANS, 15), fill=GREY)
    d.text((700, 994), "21 NOV 2026", font=font(SANS_B, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Render entry.png: a 1024x1024 infographic summing up 24 November 2026's world news.

Own work, drawn with PIL shapes and DejaVu fonts only. No photos, no copied art.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

PAPER = (247, 245, 239)
INK = (20, 20, 20)
NAVY = (18, 34, 64)
WHITE = (255, 255, 255)
MUTED = (110, 110, 105)

PANELS = [
    {
        "tag": "BUSINESS  ·  USA",
        "color": (16, 110, 84),
        "tint": (224, 240, 234),
        "headline": "NVIDIA BRINGS BACK HUANG",
        "caption": "Board reinstates Jensen Huang as CEO after Trump intervened; shares jump about 31%.",
        "pic": "chip",
    },
    {
        "tag": "TECH & LAW  ·  USA",
        "color": (124, 42, 42),
        "tint": (244, 228, 228),
        "headline": "STATES SUE MUSK OVER GROK",
        "caption": "Virginia and Oregon sue SpaceX firms, saying the AI chatbot made sexualised images of real people.",
        "pic": "bubble",
    },
    {
        "tag": "WAR  ·  UKRAINE",
        "color": (146, 74, 18),
        "tint": (246, 234, 220),
        "headline": "14 KILLED IN KYIV REGION STRIKES",
        "caption": "Russian drones hit a block of flats in Dymer and a supermarket in Vyshneve; rescuers search rubble.",
        "pic": "building",
    },
    {
        "tag": "CLIMATE  ·  TURKEY",
        "color": (34, 96, 62),
        "tint": (226, 240, 230),
        "headline": "COP31 CLIMATE TALKS COLLAPSE",
        "caption": "Antalya summit ends with no deal as the EU rejects a text that never mentions fossil fuels.",
        "pic": "globe",
    },
    {
        "tag": "DISASTER  ·  INDONESIA",
        "color": (150, 58, 22),
        "tint": (248, 230, 222),
        "headline": "24 DEAD IN INDONESIA FACTORY FIRE",
        "caption": "Candy factory near Jakarta burns; about 30 workers still missing.",
        "pic": "factory",
    },
    {
        "tag": "SPORT  ·  GENEVA",
        "color": (38, 68, 140),
        "tint": (228, 234, 248),
        "headline": "CHESS CROWN BATTLE BEGINS",
        "caption": "Gukesh defends his world title against Sindarov in Geneva - the youngest final ever.",
        "pic": "chess",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real font metrics."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_chip(d, cx, cy, c):
    s = 46
    d.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                        radius=8, fill=c)
    d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], outline=WHITE, width=3)
    for dx in (-1, 0, 1):
        for dy in (-1, 1):
            d.line([cx + dx * 14, cy + dy * s // 2, cx + dx * 14, cy + dy * (s // 2 + 12)],
                   fill=c, width=4)
    for dy in (-1, 0, 1):
        for dx in (-1, 1):
            d.line([cx + dx * s // 2, cy + dy * 14, cx + dx * (s // 2 + 12), cy + dy * 14],
                   fill=c, width=4)
    d.text((cx, cy), "AI", font=font(BOLD, 20), fill=WHITE, anchor="mm")


def draw_bubble(d, cx, cy, c):
    d.rounded_rectangle([cx - 42, cy - 36, cx + 42, cy + 22], radius=14, fill=c)
    d.polygon([(cx - 30, cy + 20), (cx - 8, cy + 20), (cx - 30, cy + 42)], fill=c)
    d.text((cx, cy - 6), "!", font=font(BOLD, 44), fill=WHITE, anchor="mm")


def draw_building(d, cx, cy, c):
    d.rectangle([cx - 34, cy - 34, cx + 6, cy + 34], fill=c)
    d.rectangle([cx + 10, cy - 12, cx + 38, cy + 34], fill=c)
    d.polygon([(cx - 34, cy - 34), (cx - 14, cy - 48), (cx + 6, cy - 34)], fill=c)
    for x in (-24, -6):
        for y in (-20, 0, 20):
            d.rectangle([cx + x - 5, cy + y - 5, cx + x + 5, cy + y + 5], fill=WHITE)
    # flame on the broken roof
    d.polygon([(cx + 24, cy - 12), (cx + 16, cy - 30), (cx + 24, cy - 24),
               (cx + 30, cy - 38), (cx + 34, cy - 22), (cx + 40, cy - 30),
               (cx + 38, cy - 12)], fill=(214, 96, 20))


def draw_globe(d, cx, cy, c):
    r = 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)
    d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=c, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=c, width=3)
    d.arc([cx - r, cy - 20, cx + r, cy + 20], start=200, end=340, fill=c, width=3)
    # crack through the globe
    d.line([cx - 26, cy - 30, cx - 4, cy - 6, cx - 18, cy + 12, cx + 8, cy + 32],
           fill=(190, 40, 30), width=5)


def draw_factory(d, cx, cy, c):
    d.rectangle([cx - 40, cy - 6, cx + 40, cy + 34], fill=c)
    d.polygon([(cx - 40, cy - 6), (cx - 20, cy - 24), (cx, cy - 6),
               (cx + 20, cy - 24), (cx + 40, cy - 6)], fill=c)
    d.rectangle([cx + 26, cy - 44, cx + 38, cy - 6], fill=c)
    for x in (-28, -6, 16):
        d.rectangle([cx + x - 6, cy + 12, cx + x + 6, cy + 24], fill=WHITE)
    d.polygon([(cx + 32, cy - 52), (cx + 24, cy - 68), (cx + 32, cy - 62),
               (cx + 38, cy - 76), (cx + 42, cy - 60), (cx + 48, cy - 68),
               (cx + 46, cy - 52)], fill=(214, 96, 20))


def draw_chess(d, cx, cy, c):
    cell = 19
    x0, y0 = cx - 2 * cell, cy - 2 * cell
    for r in range(4):
        for col in range(4):
            if (r + col) % 2 == 0:
                d.rectangle([x0 + col * cell, y0 + r * cell,
                             x0 + (col + 1) * cell, y0 + (r + 1) * cell], fill=c)
    d.rectangle([x0, y0, x0 + 4 * cell, y0 + 4 * cell], outline=c, width=3)
    # crown above the board
    d.polygon([(cx - 26, cy - 52), (cx - 26, cy - 34), (cx - 13, cy - 42),
               (cx, cy - 54), (cx + 13, cy - 42), (cx + 26, cy - 34),
               (cx + 26, cy - 52)], fill=(196, 148, 20))
    d.rectangle([cx - 26, cy - 34, cx + 26, cy - 28], fill=(196, 148, 20))


PICS = {"chip": draw_chip, "bubble": draw_bubble, "building": draw_building,
        "globe": draw_globe, "factory": draw_factory, "chess": draw_chess}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=(196, 40, 40))
    f_day = font(BOLD, 74)
    d.text((512, 66), "24 NOVEMBER 2026", font=f_day, fill=WHITE, anchor="mm")
    f_sub = font(REG, 26)
    d.text((512, 122), "TUESDAY  ·  THE WORLD IN ONE PICTURE",
           font=f_sub, fill=(200, 208, 224), anchor="mm")

    # ---- panels: 2 cols x 3 rows ----
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 262
    top0 = 172
    f_tag = font(BOLD, 17)
    f_head = font(BOLD, 26)
    f_cap = font(REG, 19)

    for i, p in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top0 + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE,
                            outline=(210, 208, 198), width=2)
        d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=p["color"])
        # pictogram in a tinted disc
        cx, cy = x0 + 74, y0 + 118
        d.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], fill=p["tint"])
        PICS[p["pic"]](d, cx, cy, p["color"])
        # text block
        tx = x0 + 146
        tw = x1 - tx - 18
        d.text((tx, y0 + 26), p["tag"], font=f_tag, fill=p["color"])
        head_lines = wrap(d, p["headline"], f_head, tw)
        y = y0 + 56
        for ln in head_lines:
            d.text((tx, y), ln, font=f_head, fill=INK)
            y += 32
        cap_lines = wrap(d, p["caption"], f_cap, tw)
        y += 8
        for ln in cap_lines:
            d.text((tx, y), ln, font=f_cap, fill=(60, 60, 58))
            y += 25

    # ---- footer ----
    d.text((512, 1002), "Top stories reported on 24 November 2026  ·  Sources: AP, Reuters, CNN, Al Jazeera, FIDE",
           font=font(REG, 17), fill=MUTED, anchor="mm")

    img.save("/tmp/news24-w/entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

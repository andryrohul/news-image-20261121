#!/usr/bin/env python3
"""Draw SATURDAY ATLAS: the 21 November 2026 world-news front page.

Fresh drawing for the make.fun bounty news-image-20261121. Every story
(1-36) gets its own drawn illustration or pictogram and its own accent
colour. Output: entry.png, 1024x1024, deterministic (no timestamps,
no randomness, fixed font files).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
PAPER = (250, 246, 236)
INK = (28, 26, 23)
RED = (179, 35, 27)
DARKRED = (143, 26, 20)
GREY = (90, 86, 80)
LIGHT = (232, 224, 208)
SEA = (214, 228, 232)
LAND = (205, 214, 176)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

# One unique accent colour per story, stories 1..36.
ACCENTS = [
    (14, 124, 123),    # 1 COP31 teal
    (232, 89, 12),     # 2 Bahrain fire orange
    (212, 160, 23),    # 3 Riyadh gold
    (192, 57, 43),     # 4 Peru quake red
    (59, 74, 107),     # 5 Kryvyi Rih slate
    (30, 125, 50),     # 6 Mexico green
    (91, 42, 134),     # 7 Mercury purple
    (2, 136, 209),     # 8 Davao sky
    (247, 147, 26),    # 9 Bitcoin orange
    (55, 71, 79),      # 10 Trump AI tax charcoal
    (183, 28, 28),     # 11 China-Japan crimson
    (85, 139, 47),     # 12 Cricket lime green
    (21, 101, 192),    # 13 Nigeria boat blue
    (40, 53, 147),     # 14 Denmark denim
    (191, 54, 12),     # 15 Hormuz drones rust
    (255, 143, 0),     # 16 Kyiv amber
    (0, 105, 92),      # 17 Tehran emerald
    (173, 20, 87),     # 18 COP Panama magenta
    (51, 105, 30),     # 19 PLN clean power leaf
    (106, 27, 154),    # 20 Yemen violet
    (121, 85, 72),     # 21 Vance brown
    (0, 96, 100),      # 22 SpaceX funding cyan dark
    (97, 97, 97),      # 23 Texas execution grey
    (230, 81, 0),      # 24 Palisades fire deep orange
    (123, 31, 162),    # 25 Roundup purple
    (46, 125, 50),     # 26 Climate trial green
    (141, 110, 99),    # 27 Pyongyang taupe
    (69, 90, 100),     # 28 Train derail blue grey
    (0, 121, 107),     # 29 Taipei teal dark
    (156, 39, 176),    # 30 Bangkok rivers orchid
    (191, 108, 0),     # 31 SCO forum ochre
    (41, 98, 168),     # 32 Akvan rain steel blue
    (136, 14, 79),     # 33 Myanmar wine
    (0, 77, 64),       # 34 African rating agency pine
    (245, 124, 0),     # 35 Cummins amber orange
    (48, 63, 159),     # 36 Verstappen indigo
]

REGION_COLOURS = {
    "Europe": (47, 111, 178),
    "Asia": (198, 64, 32),
    "Middle East": (214, 148, 16),
    "Africa": (46, 125, 50),
    "Americas": (14, 124, 123),
    "Oceania": (106, 27, 154),
    "Global": (97, 97, 97),
}


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, line_h=None):
    """Draw wrapped text; returns y just below the last line."""
    if line_h is None:
        line_h = fnt.size + 3
    for line in wrap(text, fnt, max_w, draw):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def fit_one_line(draw, text, fnt, max_w):
    """Shorten with an ellipsis until the text fits one line."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while len(text) > 4 and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


HEROES = [
    {
        "n": 1, "title": "COP31 OVERTIME",
        "place": "ANTALYA, TURKIYE  ·  CLIMATE",
        "body": "Day 13 of the talks, meant to close on day 12. No deal yet: a draft "
                "with no fossil-fuel mention splits nearly 200 countries, with a "
                "third text promised on Saturday morning.",
        "src": "AP · AFP · Al Jazeera", "badge": "CONFIRMED",
    },
    {
        "n": 2, "title": "BAHRAIN: IRAN STRIKES",
        "place": "MANAMA, BAHRAIN  ·  CONFLICT",
        "body": "Iran's IRGC says drones and missiles hit US bases at al-Riffa and "
                "Awali. Bahrain says its defences stopped several; a fire broke out "
                "at a civilian industrial site, no injuries. Three tankers were also "
                "hit near Hormuz, none hurt.",
        "src": "Euronews · Fars · Bahrain MOI · UKMTO", "badge": "REPORTED",
    },
    {
        "n": 3, "title": "RIYADH MISSILES",
        "place": "RIYADH, SAUDI ARABIA  ·  CONFLICT",
        "body": "The coalition downs three Houthi ballistic missiles over Riyadh "
                "before dawn on Saturday, the third straight night of alerts. Two "
                "more are downed over Jizan — five in all — with no damage or "
                "casualties reported.",
        "src": "Reuters · AFP · Coalition statement", "badge": "OFFICIAL",
    },
]

CARDS = [
    {
        "n": 4, "title": "PERU QUAKE",
        "place": "JUNIN, PERU  ·  EARTHQUAKE",
        "body": "Magnitude 6.7 at 00:09 UTC Saturday, 108 km deep, 9 km NE of "
                "Carhuamayo; felt in Lima. First reports: no deaths, no tsunami risk.",
        "src": "USGS · IGP · AP", "badge": "OFFICIAL",
    },
    {
        "n": 5, "title": "KRYVYI RIH",
        "place": "UKRAINE  ·  WAR",
        "body": "A Russian ballistic double-tap strike on Friday night in "
                "Zelenskyy's hometown kills 2 — a 7-year-old boy and a 20-year-old "
                "woman — and injures 42, including 6 children.",
        "src": "Kyiv Independent · AP", "badge": "OFFICIAL",
    },
    {
        "n": 6, "title": "MEXICO: CHAPO ISIDRO",
        "place": "GUASAVE, SINALOA  ·  JUSTICE",
        "body": "FBI Top 10 fugitive Fausto Isidro Meza Flores is captured on Friday "
                "night with US intelligence, announced Saturday morning. Four "
                "soldiers and seven gunmen are killed; roadblocks and fires follow.",
        "src": "Reuters · CNN", "badge": "CONFIRMED",
    },
    {
        "n": 7, "title": "BEPICOLOMBO",
        "place": "SPACE  ·  ESA / JAXA",
        "body": "Fires thrusters at 19:24 CET on Saturday to enter Mercury orbit "
                "after an 8-year voyage — the first mission to put two orbiters there.",
        "src": "ESA", "badge": "OFFICIAL",
    },
    {
        "n": 8, "title": "DAVAO JET SAFE",
        "place": "DAVAO, PHILIPPINES  ·  AVIATION",
        "body": "An Air Niugini 767 diverts after midnight on an engine-fire alert. "
                "All 146 people aboard are safe.",
        "src": "AP · CAAP", "badge": "OFFICIAL",
    },
    {
        "n": 9, "title": "BITCOIN",
        "place": "WORLD  ·  MARKETS",
        "body": "Bitcoin slips below $59,000 on Saturday: $58,983 early in the day, "
                "down 3.9% in 24 hours. Ether is at $1,625.",
        "src": "CoinGecko", "badge": "CONFIRMED",
    },
    {
        "n": 10, "title": "TRUMP AI TAX",
        "place": "WASHINGTON  ·  TECHNOLOGY",
        "body": "Trump vows a tax on data centres abroad, a \"tremendous\" penalty, "
                "with no details yet.",
        "src": "ABC", "badge": "REPORTED",
    },
    {
        "n": 11, "title": "CHINA–JAPAN",
        "place": "BEIJING  ·  DIPLOMACY",
        "body": "Beijing tells Tokyo to \"correct\" its Taiwan words; Tokyo says its "
                "stance is unchanged.",
        "src": "Ministry · AFP", "badge": "OFFICIAL",
    },
    {
        "n": 12, "title": "RAHUL 124*",
        "place": "WELLINGTON  ·  CRICKET",
        "body": "KL Rahul is 124 not out at tea; India are 344 for 2 replying to 368.",
        "src": "AFP", "badge": "CONFIRMED",
    },
    {
        "n": 13, "title": "NIGERIA BOAT",
        "place": "BAYELSA, NIGERIA  ·  DISASTER",
        "body": "A funeral boat capsizes; at least 4 are dead and the search goes on.",
        "src": "Reuters", "badge": "REPORTED",
    },
]

# Also on Saturday: (number, place, one line, source). Kept terse so each
# row fits on a single line in its column.
ALSO = [
    (14, "DENMARK", "Two charged over rapper-kill plot", "Al Jazeera"),
    (15, "HORMUZ", "Iran claims it downed a US MQ-9, MQ-1", "IRIB"),
    (16, "KYIV", "Zelenskyy: Crimea bridge \"will not stay\"", "NBC"),
    (17, "TEHRAN", "Uranium stays at home", "Times of Israel"),
    (18, "ANTALYA", "Panama threatens to block COP31 text", "Al Jazeera"),
    (19, "ANTALYA", "Indonesia's PLN signs clean-power deals", "Antara"),
    (20, "YEMEN", "Houthis threaten Jeddah, Red Sea ports", "Al Jazeera"),
    (21, "WASHINGTON", "Vance: Iran strikes were Trump's call", "Reuters"),
    (22, "WASHINGTON", "Lawmaker threatens SpaceX funding", "CNN"),
    (23, "TEXAS", "Execution of a man, 70, takes 63 minutes", "ABC"),
    (24, "LOS ANGELES", "Jury convicts Palisades fire starter", "ABC"),
    (25, "MISSOURI", "Judge approves $7.25bn Roundup deal", "AFP"),
    (26, "VANCOUVER", "Canada rests defence in climate trial", "AFP"),
    (27, "PYONGYANG", "Kim tours factories; no Trump talks", "AFP"),
    (28, "SEJONG", "Freight train derails; no one hurt", "Korea Herald"),
    (29, "TAIPEI", "Budget and cash payout passed", "Taipei Times"),
    (30, "BANGKOK", "Six-point plan on arsenic in rivers", "The Nation"),
    (31, "NEW DELHI", "Pakistani minister joins SCO forum", "Dawn"),
    (32, "EASTERN INDIA", "Rain alerts as Akvan remnants move in", "ETV"),
    (33, "MYANMAR", "Rights groups urge sanctions after ruling", "AP"),
    (34, "PORT LOUIS", "Rating agency talks to 15 states", "Al Jazeera"),
    (35, "MELBOURNE", "Cummins keeps Australian captaincy", "ABC"),
    (36, "LAS VEGAS", "Verstappen to stewards after contact", "Autosport"),
]

NUMBERS = [
    ("5", "missiles downed\nover Riyadh & Jizan"),
    ("6.7", "Peru quake\nmagnitude"),
    ("146", "safe after the\nDavao landing"),
    ("3", "tankers hit\nin Hormuz"),
    ("$58,983", "bitcoin early\nSaturday"),
    ("124*", "Rahul's score\nat tea"),
]

REGIONS = [
    ("Europe", 3), ("Asia", 10), ("Middle East", 5), ("Africa", 2),
    ("Americas", 10), ("Oceania", 2), ("Global", 4),
]

DATE_CHECK = (
    "LEFT OUT — Friday 20 November news: Russian missiles land in Poland; Kyiv's bridges "
    "hit; Wall Street enters correction; the UK–EU reset deal; Cyclone Akvan's landfall. "
    "Thursday 19 November: the ICJ Myanmar ruling; the Shenzhen Trump–Xi–Putin summit; "
    "Anthropic's $2tn debut. The Chapo raid was Friday night, announced Saturday; the Peru "
    "quake struck Friday 19:09 local, 00:09 UTC Saturday — both dated here as Saturday by "
    "first report / UTC. Not yet known when drawn: the final COP31 text; any Bahrain toll "
    "beyond the industrial fire."
)


# ---------------------------------------------------------------- illustrations

def hero_scene(draw, n, x, y, w, h):
    """Draw the hero illustration panel for story n."""
    if n == 1:
        # Teal globe + thermometer + clock.
        draw.rectangle([x, y, x + w, y + h], fill=(16, 92, 96))
        draw.ellipse([x + 18, y + 8, x + 78, y + h - 8], fill=(247, 242, 231),
                     outline=(14, 124, 123), width=2)
        draw.ellipse([x + 30, y + 16, x + 66, y + h - 16], outline=(14, 124, 123), width=1)
        draw.line([x + 48, y + 8, x + 48, y + h - 8], fill=(14, 124, 123), width=1)
        draw.arc([x + 26, y + 12, x + 70, y + h - 12], 200, 340, fill=(14, 124, 123), width=2)
        # Thermometer.
        draw.rounded_rectangle([x + w - 52, y + 10, x + w - 38, y + h - 22],
                               radius=6, fill=(255, 255, 255), outline=RED, width=2)
        draw.ellipse([x + w - 56, y + h - 30, x + w - 34, y + h - 8], fill=RED)
        draw.rectangle([x + w - 48, y + 22, x + w - 42, y + h - 24], fill=RED)
        # Clock.
        draw.ellipse([x + w - 118, y + 12, x + w - 84, y + 46], fill=(255, 255, 255),
                     outline=INK, width=2)
        draw.line([x + w - 101, y + 29, x + w - 101, y + 18], fill=INK, width=2)
        draw.line([x + w - 101, y + 29, x + w - 92, y + 33], fill=INK, width=2)
        draw.text((x + 92, y + h - 24), "COP31", font=font(SANS_B, 11), fill=(255, 255, 255))
    elif n == 2:
        # Deep navy night, orange fire, tanker, stars.
        draw.rectangle([x, y, x + w, y + h], fill=(13, 27, 62))
        for sx, sy in [(x + 20, y + 12), (x + 90, y + 8), (x + 170, y + 16),
                       (x + 250, y + 10), (x + 300, y + 20)]:
            star(draw, sx, sy, 3, (255, 255, 255))
        draw.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 16], fill=(40, 44, 52))
        for i in range(4):
            cx = x + 48 + i * 58
            draw.rectangle([cx, y + h - 52, cx + 44, y + h - 34],
                           fill=[(232, 89, 12), (14, 124, 123), (247, 242, 231),
                                 (212, 160, 23)][i])
        # Flames.
        for fx, fh in [(x + 60, 22), (x + 150, 30), (x + 250, 24)]:
            draw.polygon([(fx, y + h - 16), (fx + 12, y + h - 16 - fh),
                          (fx + 24, y + h - 16)], fill=(232, 89, 12))
            draw.polygon([(fx + 6, y + h - 16), (fx + 12, y + h - 16 - fh + 10),
                          (fx + 18, y + h - 16)], fill=(255, 200, 40))
        draw.line([x + 20, y + 14, x + 90, y + 40], fill=(255, 200, 40), width=2)
    else:
        # Midnight city, gold missile trails, stars.
        draw.rectangle([x, y, x + w, y + h], fill=(22, 35, 63))
        for sx, sy in [(x + 24, y + 10), (x + 120, y + 16), (x + 210, y + 8),
                       (x + 290, y + 14), (x + 70, y + 26)]:
            star(draw, sx, sy, 3, (255, 255, 255))
        base = y + h
        for bx, bw, bh in [(x + 16, 34, 34), (x + 58, 26, 48), (x + 92, 40, 30),
                           (x + 140, 30, 56), (x + 178, 36, 38), (x + 222, 28, 50),
                           (x + 258, 34, 32)]:
            draw.rectangle([bx, base - bh, bx + bw, base], fill=(10, 18, 36))
            for wy in range(base - bh + 6, base - 4, 10):
                draw.rectangle([bx + 5, wy, bx + 11, wy + 5], fill=(255, 200, 40))
        draw.arc([x + 60, y - 6, x + 260, y + 62], 200, 330, fill=(212, 160, 23), width=3)
        draw.arc([x + 120, y + 2, x + 300, y + 58], 210, 320, fill=(255, 255, 255), width=2)


def card_icon(draw, n, x, y, w, h):
    """Draw the small pictogram for card story n inside its strip."""
    accent = ACCENTS[n - 1]
    draw.rectangle([x, y, x + w, y + h], fill=accent)
    cx, cy = x + w // 2, y + h // 2
    if n == 4:
        # Seismograph zigzag.
        pts = [(x + 8, cy), (x + w // 4, cy - 12), (x + w // 2 - 6, cy + 12),
               (x + w // 2 + 6, cy - 14), (x + 3 * w // 4, cy + 10), (x + w - 8, cy)]
        draw.line(pts, fill=(255, 255, 255), width=3, joint="curve")
    elif n == 5:
        draw.line([x + 10, y + h - 10, x + w - 14, y + 12], fill=(255, 255, 255), width=3)
        star(draw, x + w - 18, y + 14, 8, (255, 200, 40))
    elif n == 6:
        star(draw, cx, cy, 12, (255, 255, 255))
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=accent)
    elif n == 7:
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(247, 147, 26))
        draw.ellipse([cx - 18, cy - 7, cx + 18, cy + 7], outline=(255, 255, 255), width=2)
        draw.polygon([(cx + 16, cy - 16), (cx + 26, cy - 10), (cx + 16, cy - 6)],
                     fill=(255, 255, 255))
    elif n == 8:
        draw.polygon([(x + 8, cy + 2), (x + w - 12, cy - 8), (x + w - 6, cy - 2),
                      (x + w - 12, cy + 4), (x + 22, cy + 8)], fill=(255, 255, 255))
        draw.line([x + 10, y + h - 6, x + w - 10, y + h - 6], fill=(255, 255, 255), width=2)
    elif n == 9:
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 255, 255))
        draw.text((cx - 6, cy - 11), "B", font=font(SANS_B, 18), fill=accent)
    elif n == 10:
        for i in range(3):
            draw.rectangle([x + 10 + i * 12, y + 8, x + 20 + i * 12, y + h - 8],
                           outline=(255, 255, 255), width=1)
        draw.text((x + w - 22, cy - 9), "$", font=font(SANS_B, 16), fill=(255, 200, 40))
    elif n == 11:
        draw.rectangle([x + 10, y + 8, x + 34, y + h - 8], fill=(183, 28, 28))
        draw.rectangle([x + 40, y + 8, x + 64, y + h - 8], fill=(255, 255, 255))
        draw.ellipse([x + w - 24, y + 6, x + w - 8, y + 22], fill=(255, 255, 255))
    elif n == 12:
        draw.line([x + 12, cy + 10, x + w - 24, cy - 12], fill=(255, 255, 255), width=4)
        draw.ellipse([x + w - 20, cy - 16, x + w - 8, cy - 4], fill=(255, 200, 40))
    elif n == 13:
        draw.polygon([(x + 10, cy + 2), (x + w - 10, cy + 2), (x + w - 18, cy + 10),
                      (x + 18, cy + 10)], fill=(255, 255, 255))
        draw.line([x + w // 2, cy + 2, x + w // 2, cy - 12], fill=(255, 255, 255), width=2)
        draw.arc([x + 8, cy + 8, x + w - 8, cy + 18], 0, 180, fill=(255, 255, 255), width=2)


def badge_width(badge):
    fnt = font(SANS_B, 8)
    return ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(
        "✓ " + badge, font=fnt) + 10


def badge_chip(draw, x, y, badge):
    """Small badge chip; returns its width."""
    fnt = font(SANS_B, 8)
    label = "✓ " + badge
    w = draw.textlength(label, font=fnt) + 10
    fill = (30, 125, 50) if badge == "CONFIRMED" else (
        (21, 101, 192) if badge == "OFFICIAL" else (191, 54, 12))
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=fill)
    draw.text((x + 5, y + 1), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- layout

def draw_masthead(draw, x, y, w):
    draw.rectangle([0, 0, W, 6], fill=RED)
    draw.text((x, y), "THE WORLD IN ONE DAY",
              font=font(SANS_B, 13), fill=RED)
    right = "36 STORIES  ·  7 REGIONS  ·  SATURDAY ATLAS"
    rw = draw.textlength(right, font=font(SANS_B, 11))
    draw.text((x + w - rw, y + 2), right, font=font(SANS_B, 11), fill=GREY)
    y += 22
    title = "Saturday 21 November 2026"
    tf = font(SERIF, 46)
    tw = draw.textlength(title, font=tf)
    draw.text((x + (w - tw) // 2, y), title, font=tf, fill=INK)
    y += 58
    sub = "Bahrain under fire  •  Riyadh's missiles downed  •  COP31 talks run past deadline"
    sf = font(SERIF_R, 16)
    sw = draw.textlength(sub, font=sf)
    draw.text((x + (w - sw) // 2, y), sub, font=sf, fill=INK)
    y += 26
    draw.line([x, y, x + w, y], fill=INK, width=2)
    draw.line([x, y + 4, x + w, y + 4], fill=INK, width=1)
    return y + 10


def draw_numbers_fixed(draw, x, y, w):
    """Numbers strip: big number on top, two-line label beneath it."""
    gap = 6
    bw = (w - gap * 5) // 6
    box_h = 52
    for i, (num, label) in enumerate(NUMBERS):
        bx = x + i * (bw + gap)
        draw.rectangle([bx, y, bx + bw, y + box_h], outline=INK, width=1, fill=PAPER)
        draw.rectangle([bx, y, bx + bw, y + 4], fill=ACCENTS[i])
        nf = font(SERIF, 18)
        nw = draw.textlength(num, font=nf)
        draw.text((bx + (bw - nw) // 2, y + 5), num, font=nf, fill=INK)
        lf = font(SANS, 8)
        lines = label.split("\n")
        ly = y + 27
        for ln in lines:
            lw = draw.textlength(ln, font=lf)
            draw.text((bx + (bw - lw) // 2, ly), ln, font=lf, fill=GREY)
            ly += 9
    return y + box_h


def draw_regions(draw, x, y, w):
    draw.text((x, y + 2), "WHERE THE NEWS FELL",
              font=font(SANS_B, 11), fill=INK)
    label_w = draw.textlength("WHERE THE NEWS FELL  ", font=font(SANS_B, 11))
    rx = x + label_w + 8
    total_w = w - (rx - x)
    seg_w = total_w // len(REGIONS)
    for i, (name, count) in enumerate(REGIONS):
        sx = rx + i * seg_w
        colour = REGION_COLOURS[name]
        draw.rectangle([sx, y, sx + seg_w - 3, y + 20], fill=colour)
        txt = "%s %d" % (name, count)
        tf = font(SANS_B, 10)
        tw = draw.textlength(txt, font=tf)
        draw.text((sx + (seg_w - 3 - tw) // 2, y + 4), txt, font=tf,
                  fill=(255, 255, 255))
    return y + 26


def draw_hero(draw, x, y, w, h, hero):
    n = hero["n"]
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=PAPER)
    illo_h = 72
    hero_scene(draw, n, x + 1, y + 1, w - 2, illo_h)
    by = y + illo_h
    draw.rectangle([x, by, x + w, by + 24], fill=RED)
    tf = font(SANS_B, 14)
    title = "%d  %s" % (n, hero["title"])
    draw.text((x + 8, by + 4), title, font=tf, fill=(255, 255, 255))
    ty = by + 28
    draw.text((x + 8, ty), hero["place"], font=font(SANS_B, 9), fill=RED)
    ty += 13
    ty = text_block(draw, x + 8, ty, hero["body"], font(SANS, 11),
                    INK, w - 16, line_h=13)
    bw = badge_width(hero["badge"])
    src = fit_one_line(draw, hero["src"], font(SANS, 8), w - 16 - bw - 6)
    draw.text((x + 8, y + h - 16), src, font=font(SANS, 8), fill=GREY)
    badge_chip(draw, x + w - 8 - bw, y + h - 17, hero["badge"])
    return y + h


def draw_card(draw, x, y, w, h, card):
    n = card["n"]
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=PAPER)
    strip_h = 30
    card_icon(draw, n, x + 1, y + 1, w - 2, strip_h)
    num = str(n)
    nf = font(SANS_B, 11)
    draw.ellipse([x + w - 24, y + 6, x + w - 6, y + 24], fill=(255, 255, 255))
    nw = draw.textlength(num, font=nf)
    draw.text((x + w - 15 - nw // 2, y + 8), num, font=nf, fill=INK)
    ty = y + strip_h + 5
    draw.text((x + 7, ty), card["title"], font=font(SANS_B, 12), fill=INK)
    ty += 16
    draw.text((x + 7, ty), card["place"], font=font(SANS_B, 8), fill=ACCENTS[n - 1])
    ty += 11
    ty = text_block(draw, x + 7, ty, card["body"], font(SANS, 10),
                    INK, w - 14, line_h=11)
    bw = badge_width(card["badge"])
    src = fit_one_line(draw, card["src"], font(SANS, 8), w - 14 - bw - 6)
    draw.text((x + 7, y + h - 14), src, font=font(SANS, 8), fill=GREY)
    badge_chip(draw, x + w - 7 - bw, y + h - 15, card["badge"])
    return y + h


# ---------------------------------------------------------------- map + also list

def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    px = mx + (lon + 180.0) / 360.0 * mw
    py = my + (90.0 - lat) / 180.0 * mh
    return px, py


CONTINENTS = [
    # North America (lon, lat)
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-105, 20),
     (-120, 30), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-60, 5), (-50, 0), (-40, -10), (-35, -20), (-50, -30),
     (-60, -40), (-70, -50), (-75, -35), (-80, -20), (-80, 0)],
    # Europe
    [(-10, 36), (0, 40), (10, 44), (20, 45), (28, 45), (30, 40),
     (20, 36), (10, 38), (0, 36), (-10, 40), (-5, 48), (0, 52),
     (10, 58), (20, 60), (30, 65), (20, 70), (5, 60), (-5, 55)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (50, 10), (45, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -25), (12, -15), (10, -5), (0, 5), (-8, 5)],
    # Asia
    [(30, 65), (40, 70), (60, 70), (90, 75), (120, 75), (150, 70),
     (170, 65), (160, 60), (140, 55), (130, 45), (120, 35), (110, 25),
     (100, 15), (90, 10), (80, 8), (70, 15), (60, 25), (50, 30),
     (40, 35), (30, 40)],
    # Australia
    [(113, -22), (120, -15), (130, -12), (140, -15), (150, -20),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -35), (114, -30)],
]

# Story number -> (lon, lat, region) for map pins 1-13.
PINS = {
    1: (30.7, 36.9, "Middle East"),
    2: (50.6, 26.2, "Middle East"),
    3: (46.7, 24.6, "Middle East"),
    4: (-75.9, -11.2, "Americas"),
    5: (33.4, 47.9, "Europe"),
    6: (-108.5, 25.6, "Americas"),
    8: (125.6, 7.1, "Asia"),
    9: (-0.1, 51.5, "Global"),
    10: (-77.0, 38.9, "Americas"),
    11: (116.4, 39.9, "Asia"),
    12: (174.8, -41.3, "Oceania"),
    13: (6.3, 4.9, "Africa"),
}


# Small display offsets (degrees) so the three close Middle East pins
# (Antalya, Riyadh, Bahrain) do not sit on top of each other.
PIN_OFFSETS = {
    1: (-4.0, 3.0),
    2: (5.0, -3.0),
    3: (-2.0, 2.0),
}


def draw_map(draw, x, y, w, h):
    draw.text((x, y), "WHERE IT HAPPENED — 1 TO 13",
              font=font(SANS_B, 11), fill=INK)
    my = y + 18
    mh = h - 18
    draw.rectangle([x, my, x + w, my + mh], fill=SEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x + 2, my + 2, w - 4, mh - 4)
               for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=(120, 130, 100))
    # Mercury: an orbit arc above the map with its pin.
    draw.arc([x + w - 78, my + 2, x + w - 18, my + 34], 180, 360,
             fill=(91, 42, 134), width=2)
    draw.ellipse([x + w - 30, my + 4, x + w - 18, my + 16],
                 fill=(247, 147, 26), outline=(91, 42, 134))
    draw.text((x + w - 62, my + 20), "7 MERCURY", font=font(SANS_B, 8),
              fill=(91, 42, 134))
    for n, (lon, lat, region) in sorted(PINS.items()):
        dlon, dlat = PIN_OFFSETS.get(n, (0.0, 0.0))
        px, py = lonlat_to_xy(lon + dlon, lat + dlat, x + 2, my + 2, w - 4, mh - 4)
        colour = REGION_COLOURS[region]
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=colour,
                     outline=(255, 255, 255), width=1)
        label = str(n)
        lf = font(SANS_B, 8)
        lw = draw.textlength(label, font=lf)
        draw.text((px - lw / 2, py - 6), label, font=lf, fill=(255, 255, 255))
    return y + h


def draw_also(draw, x, y, w, h):
    draw.text((x, y), "ALSO ON SATURDAY 21 NOVEMBER",
              font=font(SANS_B, 11), fill=INK)
    draw.text((x + w - 130, y), "14–36 · ONE LINE EACH",
              font=font(SANS_B, 9), fill=GREY)
    top = y + 18
    rows = h - 18
    left = ALSO[:11]
    right = ALSO[11:]
    col_w = (w - 10) // 2
    row_h = rows // 12
    for col_i, items in enumerate([left, right]):
        cx = x + col_i * (col_w + 10)
        for i, (n, place, line, src) in enumerate(items):
            ry = top + i * row_h
            accent = ACCENTS[n - 1]
            draw.rectangle([cx, ry, cx + 16, ry + 14], fill=accent)
            nf = font(SANS_B, 8)
            num = str(n)
            nw = draw.textlength(num, font=nf)
            draw.text((cx + (16 - nw) / 2, ry + 2), num, font=nf,
                      fill=(255, 255, 255))
            full = "%s — %s (%s)" % (place, line, src)
            txt = fit_one_line(draw, full, font(SANS, 9), col_w - 20)
            draw.text((cx + 20, ry + 2), txt, font=font(SANS, 9), fill=INK)
    return y + h


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    x = 14
    w = W - 28
    y = 10
    y = draw_masthead(draw, x, y, w)
    y = draw_numbers_fixed(draw, x, y, w)
    y += 6
    y = draw_regions(draw, x, y, w)
    y += 6
    hero_h = 196
    gap = 6
    hw = (w - gap * 2) // 3
    for i, hero in enumerate(HEROES):
        draw_hero(draw, x + i * (hw + gap), y, hw, hero_h, hero)
    y += hero_h + 6
    # Cards, row 1: 4 (double) + 5 + 6; row 2: 7-13 in one row of 7.
    card_h = 152
    row1_w = (w - gap * 2) // 4
    draw_card(draw, x, y, row1_w * 2 + gap, card_h, CARDS[0])
    draw_card(draw, x + row1_w * 2 + gap * 2, y, row1_w, card_h, CARDS[1])
    draw_card(draw, x + row1_w * 3 + gap * 3, y, row1_w, card_h, CARDS[2])
    y += card_h + 6
    row2_w = (w - gap * 6) // 7
    for i, card in enumerate(CARDS[3:]):
        draw_card(draw, x + i * (row2_w + gap), y, row2_w, card_h, card)
    y += card_h + 6
    # Map (left) + also list (right).
    map_w = 330
    section_h = 178
    draw_map(draw, x, y, map_w, section_h)
    draw_also(draw, x + map_w + 10, y, w - map_w - 10, section_h)
    y += section_h + 6
    # Date check box.
    box_h = 80
    draw.rectangle([x, y, x + w, y + box_h], outline=RED, width=2, fill=PAPER)
    draw.text((x + 8, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE",
              font=font(SANS_B, 11), fill=RED)
    text_block(draw, x + 8, y + 22, DATE_CHECK, font(SANS, 10), INK,
               w - 16, line_h=12)
    y += box_h + 6
    foot = ("Every story here happened, or was first reported, on Saturday 21 November 2026 "
            "in at least one time zone. Sources named beside each story. Original drawings.")
    ff = font(SANS, 9)
    fw = draw.textlength(foot, font=ff)
    draw.text((x + (w - fw) // 2, y), foot, font=ff, fill=GREY)
    return img


if __name__ == "__main__":
    out = os.environ.get("ATLAS_OUT", "entry.png")
    build().save(out, "PNG", optimize=True)
    print("wrote", out)

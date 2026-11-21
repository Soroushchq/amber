#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مولد PNGهای legacy سه برند جدید آمبرگرام v0.9.11 — الگوی generate_mario_icons.py:
#   icon_16 «هم‌آهنگ» (اکولایزر + هواپیما)  |  icon_17 «سمت تاریک» (ستارهٔ مرگ + شمشیر نوری)
#   icon_18 «اسلینگ‌شات» (تله‌پرتاب + پرندهٔ خشمگین)
# فوق‌نمونه‌برداری ۴×، دو شکل (تمام‌صفحه + دایره)، پنج تراکم
# هندسه عیناً همان مسیرهای {harmony,sw,sling}_icon_*.xml
import math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
SS = 4  # فوق‌نمونه‌برداری
DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

# ── هواپیمای کاغذی آمبرگرام (عیناً مسیر mario_icon_fg.xml) ──
PLANE = [(61.10, 64.90), (84.10, 46.50), (75.48, 62.03), (78.35, 70.65), (69.15, 65.48)]


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def hexc(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def vgrad(size_px, y0, y1, c0, c1):
    """گرادیان خطی عمودی — y بر حسب بستر ۱۰۸"""
    g = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    steps = 128
    k = size_px / 108.0
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        y_a = y0 + (y1 - y0) * t0
        y_b = y0 + (y1 - y0) * t1
        c = lerp(c0, c1, t0)
        gd.rectangle([0, y_a * k - 1, size_px, y_b * k + 1], fill=c + (255,))
    return g


def radial_fill(size_px, cx, cy, radius, stops, steps=72):
    """گرادیان رادیالی کامل (مات) — مختصات بر حسب بستر ۱۰۸؛
    stops: [(t, color), ...] با t=0 در مرکز و t=1 در لبه"""
    g = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    k = size_px / 108.0

    def color_at(t):
        for i in range(len(stops) - 1):
            ta, ca = stops[i]
            tb, cb = stops[i + 1]
            if t <= tb:
                f = 0.0 if tb <= ta else (t - ta) / (tb - ta)
                return lerp(ca, cb, min(1.0, max(0.0, f)))
        return stops[-1][1]

    for i in range(steps, 0, -1):
        t = i / steps
        r = radius * t
        gd.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k],
                   fill=color_at(t) + (255,))
    return g


def capped_line(d, p0, p1, color, w):
    """خط با کلاهک گرد (عین strokeLineCap=round) — مختصات پیکسلی"""
    d.line([p0, p1], fill=color, width=w)
    r = w / 2.0
    for (x, y) in (p0, p1):
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def bez(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def rot_rect(cx, cy, w, h, deg):
    """چهارگوشهٔ مستطیل چرخیده (عین group rotation وکتور)"""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for dx, dy in ((-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)):
        pts.append((cx + dx*ca - dy*sa, cy + dx*sa + dy*ca))
    return pts


def star_pts(cx, cy, r_out, r_in, points=5):
    pts = []
    for i in range(points * 2):
        ang = math.radians(-90 + i * 180.0 / points)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def plane_glyph(d, u, color):
    """هالهٔ نور + هواپیما — عین الگوی ماریو"""
    pts = [(x * u, y * u) for (x, y) in PLANE]
    halo_w = max(1, round(2.2 * u))
    d.line(pts + [pts[0]], fill=color + (0x40,), width=halo_w * 2, joint="curve")
    d.polygon(pts, fill=color + (255,))


# ════════════════════ برند ۱: هم‌آهنگ (icon_16) ════════════════════
HAR_BG_C = hexc("232438")
HAR_BG_E = hexc("191A26")
HAR_BARS = [(44, 14, hexc("5865F2")), (52, 22, hexc("8A57F0")), (60, 16, hexc("EB459E"))]
HAR_PLANE = hexc("F2F3FF")


def render_harmony(size):
    s = size * SS
    u = s / 108.0
    img = radial_fill(s, 54, 54, 76, [(0.0, HAR_BG_C), (1.0, HAR_BG_E)])
    d = ImageDraw.Draw(img)
    # سه میلهٔ اکولایزر — استادیوم عمودی (عرض ۵، ارتفاع h، مرکز y=54)
    for (cx, h, col) in HAR_BARS:
        x0, x1 = (cx - 2.5) * u, (cx + 2.5) * u
        y0, y1 = (54 - h / 2) * u, (54 + h / 2) * u
        d.rounded_rectangle([x0, y0, x1, y1], radius=2.5 * u, fill=col + (255,))
    plane_glyph(d, u, HAR_PLANE)
    return img


# ════════════════════ برند ۲: سمت تاریک (icon_17) ════════════════════
SW_TOP = hexc("101A38")
SW_BOT = hexc("05070D")
SW_HI = hexc("9BA3B8")
SW_MID = hexc("5E6478")
SW_LO = hexc("3E4356")
SW_TRENCH = hexc("2E3346")
SW_DISH = hexc("474E60")
SW_DISH_IN = hexc("333949")
SW_BEAM = hexc("E5484D")
SW_STARS = [(28, 22, hexc("FFE81F")), (48, 14, hexc("EAF0FF")), (86, 16, hexc("F2C14E"))]
SW_PLANE = hexc("EAF0FF")


def render_sw(size):
    s = size * SS
    u = s / 108.0
    img = vgrad(s, 0, 108, SW_TOP, SW_BOT)
    # گوی ستارهٔ مرگ — گرادیان رادیالی با هایلایت بالا-چپ، ماسک دایره
    mask = Image.new("L", (s, s), 0)
    cx, cy, r = 54 * u, 47 * u, 22 * u
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    sphere = radial_fill(s, 46, 39, 34, [(0.0, SW_HI), (0.55, SW_MID), (1.0, SW_LO)])
    img.paste(sphere, (0, 0), mask)
    d = ImageDraw.Draw(img)
    # ترنچ استوایی
    d.rectangle([32.1 * u, 45.75 * u, 75.9 * u, 48.25 * u], fill=SW_TRENCH + (255,))
    # بشقاب ابرتوزیع
    d.ellipse([41 * u, 34 * u, 53 * u, 46 * u], fill=SW_DISH + (255,))
    d.ellipse([44 * u, 37 * u, 50 * u, 43 * u], fill=SW_DISH_IN + (255,))
    # شمشیر نوری سرخ با هستهٔ سفید
    capped_line(d, (66 * u, 58 * u), (84 * u, 30 * u), SW_BEAM + (255,), max(1, round(4 * u)))
    capped_line(d, (66 * u, 58 * u), (84 * u, 30 * u), (255, 255, 255, 255), max(1, round(1.5 * u)))
    # ستاره‌های پراکنده
    for (x, y, col) in SW_STARS:
        d.ellipse([(x-1)*u, (y-1)*u, (x+1)*u, (y+1)*u], fill=col + (255,))
    plane_glyph(d, u, SW_PLANE)
    return img


# ════════════════════ برند ۳: اسلینگ‌شات (icon_18) ════════════════════
SL_TOP = hexc("8FD1F5")
SL_BOT = hexc("C8ECFF")
SL_HILL = hexc("7DBB42")
SL_WOOD = hexc("9A6633")
SL_BIRD = hexc("E8443A")
SL_BROW = hexc("5A1613")
SL_BEAK = hexc("FFB03A")
SL_STAR = hexc("FFC53D")
SL_STARS = [(72, 30), (78, 24), (84, 32)]


def render_sling(size):
    s = size * SS
    u = s / 108.0
    img = vgrad(s, 0, 108, SL_TOP, SL_BOT)
    d = ImageDraw.Draw(img)
    # تپهٔ سبز — دایرهٔ بزرگ r=80 با مرکز (54,153.21)؛ عین مسیر A80,80 وکتور
    d.ellipse([(54-80)*u, (153.21-80)*u, (54+80)*u, (153.21+80)*u], fill=SL_HILL + (255,))
    # تله‌پرتاب چوبی Y — شاخه‌های بِزیه + تنه، کلاهک گرد
    w = max(1, round(5 * u))
    prong_l = bez((40, 72), (36, 66), (34, 58), (34, 44))
    prong_r = bez((40, 72), (44, 66), (46, 58), (46, 44))
    for pts in (prong_l, prong_r):
        d.line([(x * u, y * u) for (x, y) in pts], fill=SL_WOOD + (255,), width=w, joint="curve")
    capped_line(d, (40 * u, 72 * u), (40 * u, 82 * u), SL_WOOD + (255,), w)
    for pts in (prong_l, prong_r):
        for (x, y) in (pts[0], pts[-1]):
            rr = w / 2.0
            d.ellipse([x * u - rr, y * u - rr, x * u + rr, y * u + rr], fill=SL_WOOD + (255,))
    # پرندهٔ خشمگین
    d.ellipse([38 * u, 32 * u, 54 * u, 48 * u], fill=SL_BIRD + (255,))
    # ابروهای چرخیده
    for (bx, by, deg) in ((43.2, 34.75, 15), (48.8, 34.75, -15)):
        corners = [(x * u, y * u) for (x, y) in rot_rect(bx, by, 4.4, 1.5, deg)]
        d.polygon(corners, fill=SL_BROW + (255,))
    # منقار طلایی
    d.polygon([(43.8 * u, 40.4 * u), (48.2 * u, 40.4 * u), (46 * u, 43.8 * u)], fill=SL_BEAK + (255,))
    # سه ستارهٔ طلایی
    for (sx, sy) in SL_STARS:
        pts = [(x * u, y * u) for (x, y) in star_pts(sx, sy, 2.3, 0.95)]
        d.polygon(pts, fill=SL_STAR + (255,))
    return img


def circle_clip(img_ss):
    s = img_ss.width
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, s - 1, s - 1], fill=255)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.paste(img_ss, (0, 0), mask)
    return out


def main():
    brands = [("icon_16", render_harmony), ("icon_17", render_sw), ("icon_18", render_sling)]
    made = 0
    for name, render in brands:
        for dpi, size in DENSITIES.items():
            folder = os.path.join(RES, f"mipmap-{dpi}")
            os.makedirs(folder, exist_ok=True)
            ss_img = render(size)
            ss_img.resize((size, size), Image.LANCZOS).save(
                os.path.join(folder, f"{name}_launcher.png"))
            round_img = circle_clip(ss_img).resize((size, size), Image.LANCZOS)
            round_img.save(os.path.join(folder, f"{name}_launcher_round.png"))
            made += 2
            print(f"OK {name} mipmap-{dpi}: {size}px")
    print(f"OK summary: {made} PNGs — 3 brands x 5 densities x 2 shapes")


if __name__ == "__main__":
    main()

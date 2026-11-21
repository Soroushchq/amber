#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مولد PNGهای legacy آیکون لانچر «شب اکران» (icon_14) — الگوی آئورورا:
# فوق‌نمونه‌برداری ۴×، دو شکل (تمام‌صفحه + دایره)، پنج تراکم
# هندسه عیناً همان مسیرهای premiere_icon_fg.xml (ستارهٔ طرح تاییدشده)
import math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
SS = 4  # فوق‌نمونه‌برداری

# ── رنگ‌های سینمایی (عیناً AmberTokens.PREMIERE_*) ──
HALL      = (0x0C, 0x0A, 0x12)   # تاریکی تالار
GOLD      = (0xF0, 0xB4, 0x49)   # طلای مارکی
GOLD_HI   = (0xFF, 0xE9, 0xB0)   # سر گرادیان تندیس
GOLD_MID  = (0xF0, 0xB4, 0x49)
GOLD_LO   = (0xC7, 0x7E, 0x14)   # ته گرادیان تندیس
CRIMSON   = (0xD6, 0x38, 0x52)   # ولت کریمسون
IVORY     = (0xFF, 0xFF, 0xFF)
BULB      = (0xFF, 0xF6, 0xDC)

# ── هندسهٔ دقیق (مقیاس ۱٫۱۵ + انتقال ۱۷٫۲/۱۹٫۵ در بستر ۱۰۸) ──
STAR = [(54.00, 32.15), (60.22, 47.74), (76.97, 48.84), (64.06, 59.57), (68.19, 75.84),
        (54.00, 66.88), (39.81, 75.84), (43.94, 59.57), (31.03, 48.84), (47.78, 47.74)]
BULBS = [(54.00, 32.15), (76.97, 48.84), (68.19, 75.84), (39.81, 75.84), (31.03, 48.84)]
TRAIL1 = [(36.46, 68.97), (42.49, 65.80)]   # سوراخ‌های خط اول
TRAIL2 = [(34.70, 73.58), (41.19, 70.39)]   # سوراخ‌های خط دوم
PLANE = [(47.10, 60.90), (70.10, 42.50), (61.48, 58.03), (64.35, 66.65), (55.15, 61.48)]
GRAD_A, GRAD_B = (33.30, 33.30), (70.10, 77.00)  # جهت گرادیان تندیس

def radial_glow(size_px, cx, cy, radius, color, max_alpha):
    """گرادیان شعاعی نرم — حلقه‌های آلفای حاشیه‌ای (بدون انباشتهٔ مرکز)"""
    glow = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    steps = 36
    prev_a = 0.0
    for i in range(steps, 0, -1):
        t = i / steps                      # 1 → بزرگ
        r = radius * t
        a_frac = max_alpha * (1 - t) ** 2  # افت درجه‌۲ به سمت بیرون
        marginal = a_frac - prev_a
        prev_a = a_frac
        if marginal <= 0:
            continue
        alpha = max(0, min(255, round(marginal * 255)))
        bbox = [(cx - r) * size_px, (cy - r) * size_px, (cx + r) * size_px, (cy + r) * size_px]
        gdraw.ellipse(bbox, fill=color + (alpha,))
    return glow

def grad_color(t):
    """گرادیان سه‌توقفهٔ تندیس: GOLD_HI → GOLD_MID (۴۵٪) → GOLD_LO"""
    if t < 0.45:
        u = t / 0.45
        return lerp(GOLD_HI, GOLD_MID, u)
    u = (t - 0.45) / 0.55
    return lerp(GOLD_MID, GOLD_LO, u)

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def render(size):
    s = size * SS
    u = s / 108.0  # واحد بستر ۱۰۸ → پیکسل
    img = Image.new("RGBA", (s, s), HALL + (255,))
    # هاله‌های پس‌زمینه — طلای مارکی بالا-چپ، کریمسون پایین-راست
    img.alpha_composite(radial_glow(s, 34/108, 12/108, 62/108, GOLD, 0.42))
    img.alpha_composite(radial_glow(s, 90/108, 94/108, 56/108, CRIMSON, 0.34))
    draw = ImageDraw.Draw(img)

    # ستاره — گرادیان تندیس با ماسک ستاره و چرخش ۳۸ درجه
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).polygon([(x*u, y*u) for (x, y) in STAR], fill=255, outline=255)
    grad = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    steps = 96
    # بند‌های مورب: پروجکشن روی محور گرادیان
    ax, ay = GRAD_B[0] - GRAD_A[0], GRAD_B[1] - GRAD_A[1]
    alen = math.hypot(ax, ay)
    # برای هر بند تصویر، آلفای پروجکشن نقاط بند روی محور — ساده: بند مورب با چرخش
    band = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(band)
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        c = grad_color(t0)
        bdraw.rectangle([0, int(t0 * s) - 1, s, int(t1 * s) + 1], fill=c + (255,))
    band = band.rotate(-38, center=(s/2, s/2), resample=Image.BICUBIC)
    img.paste(band, (0, 0), mask)

    # لبهٔ نازک ستاره (حدود ۱٫۵dp)
    draw.line([(x*u, y*u) for (x, y) in STAR] + [(STAR[0][0]*u, STAR[0][1]*u)],
              fill=(255, 244, 214, 140), width=max(1, round(1.5 * SS * size / 108)))

    # دنبالهٔ نگاتیو — سوراخ‌های فیلم
    for i, (x, y) in enumerate(TRAIL1):
        r = 1.3 * u
        draw.ellipse([x*u - r, y*u - r, x*u + r, y*u + r], fill=IVORY + (0xB3 if i == 0 else 0x80,))
    for i, (x, y) in enumerate(TRAIL2):
        r = 1.15 * u
        draw.ellipse([x*u - r, y*u - r, x*u + r, y*u + r], fill=IVORY + (0x73 if i == 0 else 0x47,))

    # بولت‌های مارکی نوک ستاره
    for (bx, by) in BULBS:
        r = 1.7 * u
        draw.ellipse([bx*u - r, by*u - r, bx*u + r, by*u + r], fill=BULB + (0xE6,))

    # هالهٔ نور پشت هواپیما — چند-خط موازی نازک
    halo_w = max(1, round(2.2 * SS * size / 108))
    draw.line([(x*u, y*u) for (x, y) in PLANE] + [(PLANE[0][0]*u, PLANE[0][1]*u)],
              fill=IVORY + (0x40,), width=halo_w * 2, joint="curve")

    # هواپیما
    draw.polygon([(x*u, y*u) for (x, y) in PLANE], fill=IVORY + (255,))
    return img.resize((size, size), Image.LANCZOS)

def main():
    densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for dpi, size in densities.items():
        folder = os.path.join(RES, f"mipmap-{dpi}")
        os.makedirs(folder, exist_ok=True)
        img = render(size)
        img.save(os.path.join(folder, "icon_14_launcher.png"))
        # دایره — ماسک دایره‌ای
        s = size * SS
        big = render(size).resize((s, s), Image.LANCZOS)
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, s - 1, s - 1], fill=255)
        round_img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        round_img.paste(big, (0, 0), mask)
        round_img.resize((size, size), Image.LANCZOS).save(os.path.join(folder, "icon_14_launcher_round.png"))
        print(f"OK mipmap-{dpi}: {size}px")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مولد PNGهای legacy آیکون لانچر «دنیای ماریو» (icon_15) — الگوی شب اکران:
# فوق‌نمونه‌برداری ۴×، دو شکل (تمام‌صفحه + دایره)، پنج تراکم
# هندسه عیناً همان مسیرهای mario_icon_fg.xml (قارچ طرح تأییدشده)
import math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
SS = 4  # فوق‌نمونه‌برداری

# ── رنگ‌های سرزمین ماریو (عیناً AmberTokens.MARIO_*) ──
SKY_TOP   = (0x5C, 0x94, 0xFC)   # آسمان NES
SKY_BOT   = (0x8F, 0xB4, 0xFF)
COIN_HI   = (0xFF, 0xE0, 0x63)   # سکه
COIN_LO   = (0xC2, 0x8C, 0x1E)
CAP_TOP   = (0xE8, 0x5B, 0x50)   # کلاهک قارچ
CAP_BOT   = (0xC6, 0x28, 0x1C)
STEM_TOP  = (0xFF, 0xF3, 0xD9)   # ساقه
STEM_BOT  = (0xF2, 0xDC, 0xA8)
PIPE      = (0x43, 0xB0, 0x47)   # لوله
PIPE_DEEP = (0x2E, 0x9E, 0x3E)
INK       = (0x3D, 0x2E, 0x00)   # چشم‌ها/حکاکی
IVORY     = (0xFF, 0xFF, 0xFF)

# ── هندسهٔ دقیق (مقیاس ۱٫۱۵ + انتقال مطابق fg) ──
CAP = [(21, 58), (29, 30), (51, 30), (59, 58), (55.5, 61.2), (24.5, 61.2)]
# کلاهک به‌صورت مسیر بِزیه — با چندضلعی تقریب نمی‌زنیم؛ قوس را با نقاط فرا می‌سازیم
SPOTS = [(40, 36.5, 3.6, 0xFF), (32, 44.5, 3.0, 0xF2), (48, 44.5, 3.0, 0xF2),
         (26.5, 53.0, 2.2, 0xE6), (53.5, 53.0, 2.2, 0xE6)]
STEM = [(33.5, 61.2), (46.5, 61.2), (46, 72.5), (42, 76.2), (38, 76.2), (34, 72.5)]
EYES = [(37.6, 66.8, 1.5), (42.4, 66.8, 1.5)]
COIN_C, COIN_R, COIN_R2 = (76, 30), 8.0, 4.8
SPARKS = [(86.5, 19.5, 1.3, 0xB3), (90.5, 16.5, 1.1, 0x99), (93.5, 12.5, 0.9, 0x80)]
PLANE = [(61.10, 64.90), (84.10, 46.50), (75.48, 62.03), (78.35, 70.65), (69.15, 65.48)]

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def cap_outline():
    """قوس بِزیهٔ کلاهک → چندضلعی فرانمونه (دقیق برای پیکسل‌زنی)"""
    pts = []
    # سه قطعهٔ بِزیهٔ کلاهک مطابق pathData fg
    segs = [((21, 58), (21, 41), (29, 30), (40, 30)),
            ((40, 30), (51, 30), (59, 41), (59, 58))]
    for p0, p1, p2, p3 in segs:
        for i in range(48):
            t = i / 48
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
            pts.append((x, y))
    pts += [(55.5, 61.2), (24.5, 61.2)]
    return pts

def stem_outline():
    pts = []
    segs = [((46.5, 61.2), (46, 72.5), (45.85, 74.6), (42, 76.2)),
            ((42, 76.2), (38, 76.2), (34.15, 74.6), (34, 72.5))]
    for p0, p1, p2, p3 in segs:
        for i in range(36):
            t = i / 36
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
            pts.append((x, y))
    pts += [(33.5, 61.2)]
    return pts

def vgrad(size_px, y0, y1, c0, c1):
    """باند گرادیان عمودی — y بر حسب واحد بستر ۱۰۸ (دقت: تقسیم بر ۱۰۸!)"""
    g = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    steps = 128
    k = size_px / 108.0  # واحد بستر ۱۰۸ → پیکسل
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        y_a = y0 + (y1 - y0) * t0
        y_b = y0 + (y1 - y0) * t1
        c = lerp(c0, c1, t0)
        gd.rectangle([0, y_a * k - 1, size_px, y_b * k + 1], fill=c + (255,))
    return g

def radial_glow(size_px, cx, cy, radius, color, max_alpha):
    glow = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    steps = 36
    prev_a = 0.0
    for i in range(steps, 0, -1):
        t = i / steps
        r = radius * t
        a_frac = max_alpha * (1 - t) ** 2
        marginal = a_frac - prev_a
        prev_a = a_frac
        if marginal <= 0:
            continue
        alpha = max(0, min(255, round(marginal * 255)))
        bbox = [(cx - r) * size_px, (cy - r) * size_px, (cx + r) * size_px, (cy + r) * size_px]
        gdraw.ellipse(bbox, fill=color + (alpha,))
    return glow

def hill_path(scale, size_px):
    pts = []
    steps = 96
    for i in range(steps + 1):
        x = 108 * i / steps
        # Q27,74 54,86 — تپهٔ اول؛ Q81,98 108,86 — تپهٔ دوم
        if x <= 54:
            t = x / 54
            y = (1-t)**2 * 86 + 2*(1-t)*t * 74 + t**2 * 86
        else:
            t = (x - 54) / 54
            y = (1-t)**2 * 86 + 2*(1-t)*t * 98 + t**2 * 86
        pts.append((x * scale, y * scale))
    pts += [(108 * scale, 108 * scale), (0, 108 * scale)]
    return pts

def hill_path2(scale, size_px):
    pts = []
    steps = 96
    for i in range(steps + 1):
        x = 108 * i / steps
        if x <= 72:
            t = x / 72
            y = (1-t)**2 * 94 + 2*(1-t)*t * 84 + t**2 * 94
        else:
            t = (x - 72) / 36
            y = (1-t)**2 * 94 + 2*(1-t)*t * 98 + t**2 * 94
        pts.append((x * scale, y * scale))
    pts += [(108 * scale, 108 * scale), (0, 108 * scale)]
    return pts

def render(size):
    s = size * SS
    u = s / 108.0
    img = Image.new("RGBA", (s, s), SKY_BOT + (255,))
    # گرادیان عمودی آسمان
    sky = vgrad(s, 0, 108, SKY_TOP, SKY_BOT)
    img.alpha_composite(sky)
    # هاله‌ها
    img.alpha_composite(radial_glow(s, 78/108, 24/108, 55/108, COIN_HI, 0.30))
    img.alpha_composite(radial_glow(s, 26/108, 96/108, 62/108, PIPE, 0.30))
    draw = ImageDraw.Draw(img)
    # تپه‌ها
    draw.polygon(hill_path(u, s), fill=PIPE + (0x4D,))
    draw.polygon(hill_path2(u, s), fill=PIPE_DEEP + (0x66,))

    # کلاهک قارچ — گرادیان عمودی با ماسک کلاهک
    cap_pts = [(x*u, y*u) for (x, y) in cap_outline()]
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).polygon(cap_pts, fill=255, outline=255)
    cap_grad = vgrad(s, 30, 61.2, CAP_TOP, CAP_BOT)
    img.paste(cap_grad, (0, 0), mask)
    # لبهٔ نازک کلاهک
    draw.line(cap_pts + [cap_pts[0]], fill=(255, 241, 214, 140),
              width=max(1, round(1.4 * SS * size / 108)), joint="curve")

    # لکه‌های سفید
    for (x, y, r, a) in SPOTS:
        rr = r * u
        draw.ellipse([x*u - rr, y*u - rr, x*u + rr, y*u + rr], fill=IVORY + (a,))

    # ساقه — گرادیان با ماسک ساقه
    stem_pts = [(x*u, y*u) for (x, y) in stem_outline()]
    mask2 = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask2).polygon(stem_pts, fill=255, outline=255)
    stem_grad = vgrad(s, 61.2, 76.2, STEM_TOP, STEM_BOT)
    img.paste(stem_grad, (0, 0), mask2)

    # چشم‌ها
    for (x, y, r) in EYES:
        rr = r * u
        draw.ellipse([x*u - rr, y*u - rr, x*u + rr, y*u + rr], fill=INK + (255,))

    # سکه — گرادیان عمودی با ماسک دایره
    cx, cy = COIN_C[0]*u, COIN_C[1]*u
    rr = COIN_R * u
    mask3 = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask3).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=255)
    coin_grad = vgrad(s, 22, 38, COIN_HI, COIN_LO)
    img.paste(coin_grad, (0, 0), mask3)
    ring = COIN_R2 * u
    draw.ellipse([cx - ring, cy - ring, cx + ring, cy + ring], outline=INK + (0x99,),
                 width=max(1, round(1.4 * SS * size / 108)))
    # حکاکی عمودی سکه
    draw.rectangle([cx - 0.7*u, cy - 2.9*u, cx + 0.7*u, cy + 2.9*u], fill=INK + (0x99,))

    # جرقه‌ها
    for (x, y, r, a) in SPARKS:
        rr = r * u
        draw.ellipse([x*u - rr, y*u - rr, x*u + rr, y*u + rr], fill=IVORY + (a,))

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
        img.save(os.path.join(folder, "icon_15_launcher.png"))
        s = size * SS
        big = render(size).resize((s, s), Image.LANCZOS)
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, s - 1, s - 1], fill=255)
        round_img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        round_img.paste(big, (0, 0), mask)
        round_img.resize((size, size), Image.LANCZOS).save(os.path.join(folder, "icon_15_launcher_round.png"))
        print(f"OK mipmap-{dpi}: {size}px")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AmberGram UI 3.0 "Solstice" — نشان برند: گم کهربایی (faceted amber gem).

یک هندسهٔ ریاضی -> همهٔ دارایی‌ها:
  mipmap-*/ic_launcher.png            مربع گرد full-bleed (48..192)
  mipmap-*/ic_launcher_round.png      دایره (48..192)
  mipmap-*/icon_foreground*.png       گم تنها در سِیف‌زون (108..432)
  drawable-nodpi/icon_gem_mono.png    سیلوئت تک‌رنگ برای themed icons
  mipmap-*/icon_background_clip*.png  هالهٔ گرم پس‌زمینهٔ adaptive
  drawable/icon_background_clip*.webp همان هاله (webp)
  drawable-*/logo_middle.*            لوگوی دایره‌ای داخل اپ
  drawable/amber_gem.xml              وکتور چندوجهی با رنگ پخته‌شده (UI/splash)
  Tools/solstice/master_*.png         پیش‌نمایش مستر

هندسه: کوشن‌کات (superellipse n=4.6) + ۱۶ وجه تاج (بادبزن مثلثی) + ۸ گُوهٔ
میزِ sunburst + قیرِ پولیش‌شدهٔ دور. رنگ‌ها از پالت AmberTokens (روز/شب).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
OUT = os.path.join(ROOT, "Tools/solstice")

# ───────────────────────────── پالت (هم‌خانوادهٔ AmberTokens 3.0) ─────────────
BG_CENTER = (34, 26, 17)      # #221A11
BG_EDGE = (14, 11, 7)         # #0E0B07
HALO = (240, 154, 42)         # هالهٔ گرم پشت گم
GIRDLE = (122, 62, 8)         # #7A3E06 قیر پولیش
GIRDLE_HI = (176, 102, 20)    # نور بالای قیر
# پایهٔ عمودی: شامپاینی بالا -> کهربا -> نارنجی عمیق پایین
BASE_STOPS = [
    (-1.00, (255, 240, 205)),
    (-0.45, (252, 196, 100)),
    (0.10, (247, 163, 36)),
    (0.60, (224, 120, 20)),
    (1.00, (198, 92, 12)),
]
SPECULAR = (255, 250, 235)
CORE_GLOW = (255, 246, 214)

# روشنایی وجه‌ها — دستی، برای حس «برش واقعی» (deterministic) — کنتراست عمیق
FACET_LIGHT = [1.00, 0.85, 1.09, 0.91, 1.07, 0.83, 1.00, 0.89,
               1.11, 0.87, 0.97, 1.06, 0.85, 1.05, 0.90, 0.94]
TABLE_LIGHT = [1.09, 0.94, 1.03, 0.88, 0.96, 1.06, 0.90, 1.00]

SS = 4  # سوپرسمپل


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))


def base_color(y_norm):
    """رنگ پایه بر اساس ارتفاع نرمال‌شده (-1 بالا .. +1 پایین)."""
    y = max(-1.0, min(1.0, y_norm))
    for i in range(len(BASE_STOPS) - 1):
        y0, c0 = BASE_STOPS[i]
        y1, c1 = BASE_STOPS[i + 1]
        if y0 <= y <= y1:
            return lerp_color(c0, c1, (y - y0) / (y1 - y0))
    return BASE_STOPS[-1][1]


def scale_color(c, k):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c)


def cushion(cx, cy, r, n=4.6, steps=192):
    """نقاط سوپرالیپس (کوشن)."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = cx + r * (abs(ct) ** (2.0 / n)) * (1 if ct >= 0 else -1)
        y = cy + r * (abs(st) ** (2.0 / n)) * (1 if st >= 0 else -1)
        pts.append((x, y))
    return pts


def anchor(cx, cy, r, n, ang_deg):
    """نقطهٔ سوپرالیپس در زاویهٔ مشخص."""
    t = math.radians(ang_deg)
    ct, st = math.cos(t), math.sin(t)
    x = cx + r * (abs(ct) ** (2.0 / n)) * (1 if ct >= 0 else -1)
    y = cy + r * (abs(st) ** (2.0 / n)) * (1 if st >= 0 else -1)
    return (x, y)


def build_facets(cx, cy, R, n=4.6):
    """ساخت همهٔ وجه‌ها. خروجی: (girdle_pts, crown_polys, table_polys, ring_polys)"""
    girdle = cushion(cx, cy, R, n)
    tR = R * 0.60          # شعاع میز
    gR = R * 0.93          # شروع قیر

    # ۱۶ نقطهٔ لبهٔ بیرونی (هر ۲۲.۵ درجه) و ۸ راس میز (هر ۴۵ درجه، آفست ۲۲.۵)
    outer = [anchor(cx, cy, gR, n, 22.5 * k) for k in range(16)]
    table = [anchor(cx, cy, tR, n, 22.5 + 45 * k) for k in range(8)]

    # وجه‌های تاج: بین هر دو راس مجاور میز، یک نقطهٔ بیرونی وسط → دو مثلث
    crown = []
    for k in range(8):
        t0 = table[k]
        t1 = table[(k + 1) % 8]
        o_mid = outer[(2 * k + 1) % 16]          # نقطهٔ بیرونی بین دو راس میز
        o0 = outer[2 * k]                         # نقطهٔ بیرونی هم‌راستای راس t0
        o1 = outer[(2 * k + 2) % 16]              # نقطهٔ بیرونی هم‌راستای راس t1
        crown.append([o0, t0, o_mid])             # مثلث چپ
        crown.append([o_mid, t1, o1])             # مثلث راست

    # میز: ۸ گُوه از مرکز تا هر ضلع میز
    table_polys = []
    for k in range(8):
        t0 = table[k]
        t1 = table[(k + 1) % 8]
        table_polys.append([(cx, cy), t0, t1])

    return girdle, crown, table_polys, table


def facet_color(poly, idx, light_table, extra=1.0):
    ys = [p[1] for p in poly]
    cy = sum(ys) / len(ys)
    y_norm = (cy - 512) / 512.0 * 2  # -1..1 در مختصات مستر ۱۰۲۴
    k = light_table[idx % len(light_table)] * extra
    return scale_color(base_color(y_norm), k)


def draw_gem(draw, cx, cy, R, glow_layer=None):
    """رسم گم روی ImageDraw (مختصات مستر). glow_layer: لایهٔ اختیاری هاله."""
    girdle_pts, crown, table_polys, table = build_facets(cx, cy, R)

    # قیر (حلقهٔ بیرونی پولیش)
    outer_full = cushion(cx, cy, R)
    inner_full = cushion(cx, cy, R * 0.93)
    draw.polygon(outer_full, fill=GIRDLE)
    # نور بالای قیر
    top_arc = [p for p in outer_full if p[1] < cy - R * 0.55] + \
              [p for p in inner_full if p[1] < cy - R * 0.45]
    if len(top_arc) >= 3:
        draw.polygon(top_arc, fill=GIRDLE_HI)

    # وجه‌های تاج — نورپردازی متقارن: بالا روشن‌تر، پایین تاریک‌تر (چپ=راست)
    for i, poly in enumerate(crown):
        ex = 1.0
        my = sum(p[1] for p in poly) / 3
        if my < cy - R * 0.42:
            ex = 1.13
        elif my > cy + R * 0.42:
            ex = 0.82
        draw.polygon(poly, fill=facet_color(poly, i, FACET_LIGHT, ex))

    # گُوه‌های میز
    for i, poly in enumerate(table_polys):
        draw.polygon(poly, fill=facet_color(poly, i, TABLE_LIGHT))

    return table


def add_specular(img, cx, cy, R, glints=True, crisp=False):
    """فلش اسپکولار ۴پر؛ حالت crisp برای سایزهای کوچک (بدون بلور، ضخیم‌تر)."""
    spec = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    # ستارهٔ ۴پر: دو لوزی کشیده عمودی/افقی + هستهٔ کوچک
    def star4(x, y, r_long, r_short, col, alpha):
        pts = []
        for k in range(8):
            ang = math.pi / 4 * k
            rr = r_long if k % 2 == 0 else r_short
            pts.append((x + rr * math.sin(ang), y - rr * math.cos(ang)))
        sd.polygon(pts, fill=col + (alpha,))
    if crisp:
        # اسپارکل پیکسل‌پذیر: ستارهٔ ضخیم بدون بلور
        star4(cx, cy, R * 0.30, R * 0.10, SPECULAR, 255)
        star4(cx, cy, R * 0.15, R * 0.065, (255, 255, 255), 255)
        return Image.alpha_composite(img, spec)
    star4(cx, cy, R * 0.34, R * 0.075, SPECULAR, 246)
    star4(cx, cy, R * 0.17, R * 0.055, (255, 255, 255), 255)
    # گلینت‌های کوچک روی دو وجه تاج بالا (متقارن) — فقط رندرهای بزرگ
    if glints:
        for gx in (cx - R * 0.62, cx + R * 0.62):
            gy = cy - R * 0.52
            star4(gx, gy, R * 0.13, R * 0.042, SPECULAR, 235)
    # نرمی حداقلی لبه‌ها (۱-۲px در مقیاس مستر) برای حذف دندانه
    spec = spec.filter(ImageFilter.GaussianBlur(R * 0.012))
    return Image.alpha_composite(img, spec)


def add_soft_shadow(img, cx, cy, R):
    """سایهٔ نرم زیر گم (عمق)."""
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    r = R * 1.04
    d.ellipse([cx - r, cy - r * 0.98, cx + r, cy + r * 1.02], fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.10))
    return Image.alpha_composite(img, sh)


def make_background(size, with_halo=True, halo_center=None, halo_alpha=0.09):
    """پس‌زمینهٔ شعاعی گرم + هاله."""
    w = size
    img = Image.new("RGBA", (w, w), BG_EDGE + (255,))
    px = img.load()
    cx = cy = w / 2
    maxd = math.hypot(cx, cy)
    # گرادیان شعاعی با گام‌های درشت + blur برای سرعت
    steps = 64
    for i in range(steps + 1):
        t = i / steps
        col = lerp_color(BG_CENTER, BG_EDGE, t)
        r = t * maxd
        bbox = [cx - r, cy - r, cx + r, cy + r]
        tmp = Image.new("RGBA", (w, w), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        td.ellipse(bbox, fill=col + (255,))
        img = Image.alpha_composite(tmp, img) if t == 0 else img
    # روش ساده‌تر و دقیق: بازساخت با numpy-free خطی
    img = Image.new("RGBA", (w, w))
    d = ImageDraw.Draw(img)
    for i in range(steps, -1, -1):
        t = i / steps
        col = lerp_color(BG_CENTER, BG_EDGE, t)
        r = (t ** 0.85) * maxd
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,))
    if with_halo:
        hx, hy = halo_center or (cx, cy)
        halo = Image.new("RGBA", (w, w), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        hr = w * 0.46
        hd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=HALO + (int(255 * halo_alpha),))
        halo = halo.filter(ImageFilter.GaussianBlur(w * 0.14))
        img = Image.alpha_composite(img, halo)
    return img


def squircle_mask(size, n=4.6):
    """ماسک سوپرالیپس برای آیکون مربع‌گرد — دقیقاً در سایز هدف."""
    m = Image.new("L", (size * SS, size * SS), 0)
    d = ImageDraw.Draw(m)
    pts = cushion(size * SS / 2, size * SS / 2, size * SS / 2 - SS, n)
    d.polygon(pts, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def circle_mask(size):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([0, 0, size - 1, size - 1], fill=255)
    return m


def render_master(glints=True, crisp=False):
    """مستر ۱۰۲۴×۱۰۲۴: پس‌زمینه + هالهٔ سبک + گم."""
    w = 1024
    img = make_background(w, with_halo=True, halo_alpha=0.10)
    img = img.resize((w * SS, w * SS), Image.LANCZOS).convert("RGBA")
    # گم با سایه
    img = add_soft_shadow(img, 512 * SS, 512 * SS, 348 * SS)
    gem = Image.new("RGBA", (w * SS, w * SS), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gem)
    draw_gem(gd, 512 * SS, 512 * SS, 348 * SS)
    img = Image.alpha_composite(img, gem)
    img = add_specular(img, 512 * SS, 512 * SS, 348 * SS, glints, crisp)
    return img.resize((w, w), Image.LANCZOS)


def render_gem_only(size, gem_ratio=0.55, glints=False):
    """گمِ تنها با سایه — برای icon_foreground."""
    w = size * SS
    img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    R = w * gem_ratio / 2 * 0.98
    cx = cy = w / 2
    img = add_soft_shadow(img, cx, cy, R)
    gem = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gem)
    draw_gem(gd, cx, cy, R)
    img = Image.alpha_composite(img, gem)
    img = add_specular(img, cx, cy, R, glints)
    return img.resize((size, size), Image.LANCZOS)


def render_mono(size=432):
    """سیلوئت سفید گم با برش‌های پیوسته — برای themed icons.
    ۸ پرهٔ پیوسته (مرکز → راس میز → لنگر بیرونی) + حلقهٔ مرز میز."""
    w = size * SS
    img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = w / 2
    R = w * 0.42
    n = 4.6
    girdle, crown, table_polys, table = build_facets(cx, cy, R, n)
    d.polygon(cushion(cx, cy, R, n), fill=(255, 255, 255, 255))
    cut = max(2, int(w * 0.011))
    # ۸ پرهٔ پیوسته از مرکز تا لنگر بیرونی (هم‌زاویه با راس‌های میز)
    for k in range(8):
        ang = 22.5 + 45 * k
        tv = anchor(cx, cy, R * 0.60, n, ang)
        og = anchor(cx, cy, R * 0.93, n, ang)
        d.line([(cx, cy), tv], fill=(255, 255, 255, 0), width=cut)
        d.line([tv, og], fill=(255, 255, 255, 0), width=cut)
        # پوشش مفصل‌ها
        for p in (tv, og):
            d.ellipse([p[0] - cut / 2, p[1] - cut / 2, p[0] + cut / 2, p[1] + cut / 2],
                      fill=(255, 255, 255, 0))
        d.ellipse([cx - cut / 2, cy - cut / 2, cx + cut / 2, cy + cut / 2],
                  fill=(255, 255, 255, 0))
    # حلقهٔ مرز میز — چندضلعی توپیر با خط شفاف
    ring = cushion(cx, cy, R * 0.60, n)
    for i in range(len(ring)):
        d.line([ring[i], ring[(i + 1) % len(ring)]], fill=(255, 255, 255, 0), width=cut)
    return img.resize((size, size), Image.LANCZOS)


def render_logo_middle(size):
    """لوگوی دایره‌ای داخل اپ: دایرهٔ گرادیان آمبر + گم سفید."""
    w = size * SS
    img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    # دایرهٔ گرادیان
    grad = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    steps = 48
    for i in range(steps):
        t = i / (steps - 1)
        col = lerp_color((232, 135, 30), (194, 94, 0), t)
        y0 = int(w * t / 2)
        gd.rectangle([0, y0, w, w], fill=col + (255,))
    mask = Image.new("L", (w, w), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, w - 1, w - 1], fill=255)
    img.paste(grad, (0, 0), mask)
    # گم سفید کوچک در مرکز — با حاشیهٔ تنفس از حلقهٔ سفید
    R = w * 0.368
    cx = cy = w / 2
    white_gem = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    wd = ImageDraw.Draw(white_gem)
    girdle, crown, table_polys, table = build_facets(cx, cy, R)
    wd.polygon(cushion(cx, cy, R), fill=(255, 255, 255, 255))
    # خطوط برش کهربایی
    cut = max(1, int(w * 0.011))
    for poly in crown + table_polys:
        for i in range(len(poly)):
            p0 = poly[i]
            p1 = poly[(i + 1) % len(poly)]
            wd.line([p0, p1], fill=(219, 134, 30, 235), width=cut)
    img = Image.alpha_composite(img, white_gem)
    return img.resize((size, size), Image.LANCZOS)


def emit_vector_xml(path, viewport=432.0):
    """همان هندسه به‌صورت وکتور اندروید با رنگ‌های پخته — برای UI/splash."""
    cx = cy = viewport / 2
    R = viewport * 0.42
    girdle, crown, table_polys, table = build_facets(cx, cy, R)
    paths = []

    def fmt(v):
        return ("%0.1f" % v).rstrip("0").rstrip(".")

    def poly_path(poly):
        d = "M" + ",".join(fmt(p[0]) + "," + fmt(p[1]) for p in poly)
        return d + "Z"

    # قیر
    paths.append((cushion(cx, cy, R), GIRDLE))
    paths.append((cushion(cx, cy, R * 0.93), scale_color(GIRDLE_HI, 1.0)))
    # تاج + میز
    for i, poly in enumerate(crown):
        my = sum(p[1] for p in poly) / 3
        ex = 1.0
        if my < cy - R * 0.42:
            ex = 1.13
        elif my > cy + R * 0.42:
            ex = 0.82
        paths.append((poly, facet_color(poly, i, FACET_LIGHT, ex)))
    for i, poly in enumerate(table_polys):
        paths.append((poly, facet_color(poly, i, TABLE_LIGHT)))
    # هایلایت مرکزی (دایرهٔ نیمه‌شفاف)
    glow = (255, 246, 214)

    out = []
    out.append('<vector xmlns:android="http://schemas.android.com/apk/res/android"')
    out.append('    android:width="112dp"')
    out.append('    android:height="112dp"')
    out.append('    android:viewportWidth="%d"' % int(viewport))
    out.append('    android:viewportHeight="%d">' % int(viewport))
    out.append('    <!-- AmberGram UI 3.0 "Solstice": نشان گم کهربایی — هندسهٔ ریاضی -->')
    for poly, col in paths:
        r, g, b = col
        out.append('    <path')
        out.append('        android:pathData="%s"' % poly_path(poly))
        out.append('        android:fillColor="#FF%02X%02X%02X" />' % (r, g, b))
    # درخشش اسپکولار مرکزی — ستارهٔ ۴پر (به‌جای لکهٔ محو)
    star_pts = []
    rl, rs = R * 0.34, R * 0.075
    for k in range(8):
        ang = math.pi / 4 * k
        rr = rl if k % 2 == 0 else rs
        star_pts.append((cx + rr * math.sin(ang), cy - rr * math.cos(ang)))
    out.append('    <path')
    out.append('        android:pathData="%s"' % poly_path(star_pts))
    out.append('        android:fillColor="#FFF6FEFB" />')
    out.append('</vector>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)

    # ── مستر ──
    master = render_master(glints=True)
    master.save(os.path.join(OUT, "master_icon.png"))
    master_small = render_master(glints=False, crisp=True)

    # ── آیکون‌های legacy ──
    densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    fg_sizes = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
    for d, s in densities.items():
        base = master if s >= 96 else master_small
        sq = base.resize((s * SS, s * SS), Image.LANCZOS)
        # مربع گرد
        big = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
        big.paste(sq, (0, 0), squircle_mask(s * SS))
        img = big.resize((s, s), Image.LANCZOS)
        img.save(os.path.join(RES, "mipmap-%s/ic_launcher.png" % d))
        # دایره
        big = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
        big.paste(sq, (0, 0), circle_mask(s * SS))
        img = big.resize((s, s), Image.LANCZOS)
        img.save(os.path.join(RES, "mipmap-%s/ic_launcher_round.png" % d))

    # ── foreground ها ──
    for d, s in fg_sizes.items():
        fg = render_gem_only(s, gem_ratio=0.55, glints=(s >= 432))
        fg.save(os.path.join(RES, "mipmap-%s/icon_foreground.png" % d))
        fg.save(os.path.join(RES, "mipmap-%s/icon_foreground_round.png" % d))
        fg.save(os.path.join(RES, "mipmap-%s/icon_foreground_sa.png" % d))

    # ── مونوکروم ──
    mono = render_mono(432)
    mono.save(os.path.join(RES, "drawable-nodpi/icon_gem_mono.png"))
    mono.save(os.path.join(OUT, "preview_mono.png"))

    # ── هالهٔ پس‌زمینهٔ adaptive (clip) — بسیار ظریف ──
    for d, s in fg_sizes.items():
        clip = make_background(s, with_halo=True, halo_alpha=0.12)
        clip.save(os.path.join(RES, "mipmap-%s/icon_background_clip.png" % d))
        clip.save(os.path.join(RES, "mipmap-%s/icon_background_clip_round.png" % d))
    clip432 = make_background(432, with_halo=True, halo_alpha=0.12)
    clip432.convert("RGB").save(os.path.join(RES, "drawable/icon_background_clip.webp"), "WEBP", quality=90)
    clip432.convert("RGB").save(os.path.join(RES, "drawable/icon_background_clip_round.webp"), "WEBP", quality=90)

    # ── لوگوی دایره‌ای داخل اپ ──
    lm = render_logo_middle(204)
    lm.save(os.path.join(RES, "drawable-xxhdpi/logo_middle.png"))
    lm.resize((136, 136), Image.LANCZOS).save(os.path.join(RES, "drawable-xhdpi/logo_middle.png"))
    lm.resize((102, 102), Image.LANCZOS).convert("RGB").save(os.path.join(RES, "drawable-hdpi/logo_middle.webp"), "WEBP", quality=92)
    lm.resize((68, 68), Image.LANCZOS).convert("RGB").save(os.path.join(RES, "drawable-mdpi/logo_middle.webp"), "WEBP", quality=92)
    lm.save(os.path.join(OUT, "preview_logo_middle.png"))

    # ── وکتور UI ──
    emit_vector_xml(os.path.join(RES, "drawable/amber_gem.xml"))

    print("OK: همهٔ دارایی‌های گم تولید شد")


if __name__ == "__main__":
    main()

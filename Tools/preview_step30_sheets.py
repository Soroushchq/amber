#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UI2 قدم ۳۰ — باتم‌شیت‌ها: هندل، رادیوس، پس‌زمینه
# همهٔ رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
#
# کارهای این قدم:
#   ۱) رادیوس — ۹-پچ پوستهٔ باتم‌شیت (sheet_shadow_round؛ پوستهٔ مشترک BottomSheet و ۱۸ مصرف‌کننده)
#      بازتولید شد: قوس نرم مؤثر آپستریم ~۲۰dp با فلر جانبی (لبهٔ کارت از x=۳۰ در بالا تا x=۸ در
#      پایین سُر می‌خورد — گوشهٔ غیردایره‌ای دست‌ساز) ← قوس دایره‌ای تمیز SHAPE_SHEET=۲۸dp
#      (هم‌زبانهٔ SHAPE_DIALOG قدم ۲۹). حاشیه‌های کارت (جانبی ~۸px / بالایی ~۱۲px @mdpi) و
#      معناشناسی پدینگ محتوا (کارت±۱ افقی / کاردِ بالا−۱ عمودی / پایین ممتد) به‌ازای هر density
#      عیناً از asset قدیم حفظ شد — دلتای چیدمان صفر (backgroundPaddingLeft/Top دست نخورد).
#   ۲) پس‌زمینه — تأیید (بدون تغییر): پوستهٔ سفید asset با فیلتر MULTIPLY روی key_dialogBackground
#      رنگ می‌شود (فاز ۰ پالتی: dialogBackground = fieldBg — روز FFFFFF / شب 241D14)؛ سایهٔ
#      مشکی نرم (چگالی ≤ ۴٪) بی‌رنگ است و روی هر تم کار می‌کند.
#   ۳) هندل — سند: در آپستریم ۷۳۰۵ هیچ هندل/درگ‌پیل در BottomSheet وجود ندارد (شیت با کشیدن کل
#      محتوا درگ می‌شود؛ جست‌وجوی DraggableView/dragger/handle صفر نتیجه) — افزودن پیل M3 به همهٔ
#      شیت‌ها ریسک چیدمان دارد و خارج از محدودهٔ این قدم؛ به‌عنوان پیشنهاد پالیش مستند شد.
#
# نکته‌های ممیزی (بدون تغییر):
#   • نوار کشش افقی مارکر قدیم x∈[۳۳,۴۰] بود (هم‌پوشان با پایان قوس در شعاع ۲۸) — در asset جدید
#     دور از قوس بازچینش شد؛ نوار عمودی زیر پایان قوس تا کف ممتد.
#   • درافت پدینگ آپستریم بین densityها ±۱px ناهمخوان بود (mdpi کارت±۱ / xxhdpi کارت±۰) —
#     مدل کارت±۱ یکدست شد (دلتا ≤ ۰٫۳dp — نامرئی).
#   • AttachAlert/ShareAlert و بقیهٔ ۱۸ مصرف‌کننده همان پوستهٔ مشترک‌اند — با یک asset همه ارتقا یافتند.
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
OLD_ASSET = "/tmp/sheet_backup/xxhdpi.9.png"
NEW_ASSET = os.path.join(ROOT, "TMessagesProj/src/main/res/drawable-xxhdpi/sheet_shadow_round.9.png")
FONT = os.path.join(ROOT, "TMessagesProj/src/main/assets/fonts/ambergramui-med.ttf")
S = 2  # px per dp


def parse_theme(path):
    m = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if "=" in line and not line.startswith(("WLS", "WPS")):
                k, v = line.split("=", 1)
                v = int(v)
                m[k] = (v & 0xFFFFFFFF) if v >= 0 else (v + 0x100000000)
    return m


def rgb(c):
    return (c >> 16 & 255, c >> 8 & 255, c & 255)


def lum(c):
    def ch(x):
        x /= 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(c)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def nine_slice(path, out_w, out_h):
    """کشش درست ۹-پچ: مارکرها از لبه خوانده می‌شوند و پیکسل‌های مارکر از تکه‌ها حذف می‌شوند."""
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = im.load()
    xs = [x for x in range(w) if px[x, 0][3] > 128]
    ys = [y for y in range(h) if px[0, y][3] > 128]
    x0, x1 = xs[0], xs[-1] + 1
    y0, y1 = ys[0], ys[-1] + 1
    rw = w - 1 - x1  # عرض ناحیهٔ راست (بدون ستون مارکر)
    bh = max(h - 1 - y1, 0)  # بلندی ناحیهٔ پایین (شیت ممتد: صفر)
    out = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    mid_w = out_w - (x0 - 1) - rw
    mid_h = out_h - (y0 - 1) - bh
    out.paste(im.crop((1, 1, x0, y0)), (0, 0))
    out.paste(im.crop((x0, 1, x1, y0)).resize((mid_w, y0 - 1), Image.NEAREST), (x0 - 1, 0))
    out.paste(im.crop((x1, 1, w - 1, y0)), (out_w - rw, 0))
    out.paste(im.crop((1, y0, x0, y1)).resize((x0 - 1, mid_h), Image.NEAREST), (0, y0 - 1))
    out.paste(im.crop((x0, y0, x1, y1)).resize((mid_w, mid_h), Image.NEAREST), (x0 - 1, y0 - 1))
    out.paste(im.crop((x1, y0, w - 1, y1)).resize((rw, mid_h), Image.NEAREST), (out_w - rw, y0 - 1))
    if bh > 0:
        out.paste(im.crop((1, y1, x0, h - 1)), (0, out_h - bh))
        out.paste(im.crop((x0, y1, x1, h - 1)).resize((mid_w, bh), Image.NEAREST), (x0 - 1, out_h - bh))
        out.paste(im.crop((x1, y1, w - 1, h - 1)), (out_w - rw, out_h - bh))
    return out


def draw_sheet_panel(theme, caption, dark):
    pw = 448
    ph = 300
    panel = Image.new("RGBA", (pw, ph), (255, 255, 255, 255))
    d = ImageDraw.Draw(panel)
    f_cap = ImageFont.truetype(FONT, 21)
    f_title = ImageFont.truetype(FONT, 21)
    f_body = ImageFont.truetype(FONT, 18)
    f_note = ImageFont.truetype(FONT, 14)

    backdrop = rgb(theme["windowBackgroundGray"])
    d.rectangle([0, 30, pw, ph], fill=backdrop)

    surf = theme["dialogBackground"]
    sheet_w = 300
    sheet_h = 210
    shell = nine_slice(NEW_ASSET, sheet_w, sheet_h)
    sr, sg, sb = rgb(surf)
    tinted = Image.new("RGBA", shell.size, (sr, sg, sb, 255))
    comp = Image.composite(tinted, Image.new("RGBA", shell.size, (0, 0, 0, 0)), shell.split()[3])
    sx = (pw - shell.size[0]) // 2
    sy = ph - shell.size[1]
    panel.alpha_composite(comp, (sx, sy))

    # متن RTL — لنگر به راستِ شیت
    rx = sx + shell.size[0] - 16
    ty = sy + 20
    def rtext(y, txt, color, font):
        tw = d.textlength(txt, font=font)
        d.text((rx - tw, y), txt, font=font, fill=color)
    rtext(ty, "عنوان شیت", rgb(theme["dialogTextBlack"]), f_title)
    rtext(ty + 30, "متن ثانویهٔ شیت", rgb(theme["dialogTextGray"]), f_body)
    rtext(ty + 58, "متن کنشی/لینک", rgb(theme["dialogTextBlue"]), f_body)
    rtext(ty + 88, "بدون هندل درگ در آپستریم ۷۳۰۵", rgb(theme["dialogTextGray"]), f_note)

    d.text((8, 6), caption, font=f_cap, fill=(25, 25, 25))
    return panel


def draw_corner_zoom(path, label, box_w, box_h, scale):
    """بزرگ‌نمایی گوشهٔ بالا-چپ کارت از ۹-پچ (حاشیهٔ مارکر کنار می‌رود)."""
    im = Image.open(path).convert("RGBA")
    im = im.crop((1, 1, im.size[0] - 1, im.size[1] - 1))
    w, h = im.size
    px = im.load()
    ys = range(int(h * 0.72), h - 1)
    L = None
    for y in ys:
        for x in range(1, w - 1):
            if px[x, y][3] >= 250:
                L = x if L is None else min(L, x)
                break
    T = None
    for y in range(1, h - 1):
        if any(px[x, y][3] >= 250 for x in range(w // 3, 2 * w // 3)):
            T = y
            break
    crop = im.crop((0, 0, min(w, L + int(h * 0.42)), min(h, T + int(h * 0.55))))
    out = crop.resize((crop.size[0] * scale, crop.size[1] * scale), Image.NEAREST)
    canvas = Image.new("RGBA", (box_w, box_h), (250, 250, 250, 255))
    canvas.alpha_composite(out, (6, 6))
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(FONT, 19)
    d.text((6, box_h - 26), label, font=f, fill=(30, 30, 30))
    return canvas


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W = 908
GAP = 12
corner_h = 170
panel_h = 300
report_h = 230
H = 40 + corner_h + GAP + panel_h + GAP + report_h

img = Image.new("RGBA", (W, H), (245, 245, 245, 255))
d = ImageDraw.Draw(img)
f_head = ImageFont.truetype(FONT, 26)
f_r = ImageFont.truetype(FONT, 19)

d.text((10, 6), "قدم ۳۰ — باتم‌شیت: رادیوس ۲۸dp (SHAPE_SHEET)",
       font=f_head, fill=(25, 25, 25))

cz_old = draw_corner_zoom(OLD_ASSET, "قدیم — قوس نرم ~۲۰dp با فلر جانبی", W // 2 - GAP, corner_h, 2)
cz_new = draw_corner_zoom(NEW_ASSET, "جدید — قوس دایره‌ای ۲۸dp (SHAPE_SHEET)", W // 2 - GAP, corner_h, 2)
img.alpha_composite(cz_old, (0, 40))
img.alpha_composite(cz_new, (W // 2 + GAP // 2, 40))

y = 40 + corner_h + GAP
p_night = draw_sheet_panel(night, "شب — پوستهٔ شیت r=۲۸ روی بستر وایپرپ", True)
p_day = draw_sheet_panel(day, "روز — پوستهٔ شیت r=۲۸ روی بستر روشن", False)
img.alpha_composite(p_night, (0, y))
img.alpha_composite(p_day, (W // 2 + GAP // 2, y))

y += panel_h + GAP
d.text((10, y), "گزارش کنتراست (از attheme)", font=f_head, fill=(25, 25, 25))
y += 36
rows = [
    ("شب", "عنوان روی پوسته", ratio(night["dialogTextBlack"], night["dialogBackground"]), True),
    ("روز", "عنوان روی پوسته", ratio(day["dialogTextBlack"], day["dialogBackground"]), True),
    ("شب", "ثانویه روی پوسته", ratio(night["dialogTextGray"], night["dialogBackground"]), True),
    ("روز", "ثانویه روی پوسته", ratio(day["dialogTextGray"], day["dialogBackground"]), True),
    ("شب", "کنش/لینک روی پوسته", ratio(night["dialogTextBlue"], night["dialogBackground"]), True),
    ("روز", "کنش/لینک روی پوسته", ratio(day["dialogTextBlue"], day["dialogBackground"]), True),
    ("شب", "پوسته/بستر (شکل)", ratio(night["dialogBackground"], night["windowBackgroundGray"]), False),
    ("روز", "پوسته/بستر (شکل)", ratio(day["dialogBackground"], day["windowBackgroundGray"]), False),
]
for i, (mode, label, r, aa) in enumerate(rows):
    col = 0 if i % 2 == 0 else 1
    yy = y + (i // 2) * 44
    xx = 10 + col * (W // 2)
    d.text((xx, yy), f"{mode}: {label}", font=f_r, fill=(30, 30, 30))
    if aa:
        if r >= 4.5:
            verdict = "PASS ≥ ۴٫۵"
            color = (20, 120, 60)
        elif r >= 3.0:
            verdict = "PASS متن درشت/کامپوننت ≥ ۳"
            color = (20, 120, 60)
        else:
            verdict = "کمتر از AA"
            color = (170, 60, 30)
    else:
        verdict = "اطلاعاتی — نشانهٔ ارتفاع شکل است"
        color = (110, 110, 110)
    d.text((xx, yy + 22), f"{r:.2f}:۱ — {verdict}", font=f_r, fill=color)

out = os.path.join(ROOT, "download/ui2-step30-sheets-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out, img.size)

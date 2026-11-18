#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UI2 قدم ۲۹ — دیالوگ‌ها: رادیوس ۲۸ + سطح روشن
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
#
# کارهای این قدم:
#   ۱) شعاع کارت دیالوگ: ۹-پچ popup_fixed_alert4 بازتولید شد (آپستریم ~۱۶dp) ← SHAPE_DIALOG=۲۸dp
#      + سه مسیر بلور AlertDialog که ناهمخوان بودند (خروجی ۲۰dp / بومی ۱۲dp / اوت‌لاین ۲۰dp)
#      به یک توکن بایند شدند — سه زبان → یک زبان. اسپینر (قرص بارگذاری کوچک) ۱۸dp خودش می‌ماند.
#   ۲) سطح روشن — دو کلید شیت هدیه در پالت نبودند:
#      dialogGiftsBackground: روز پیش‌فرض سرد بی‌سند F5F6F7؛ شب fallback به windowBackgroundGray =
#      بسترهٔ وایپرپ (۱۷۱۳۰E) — یعنی «شیت تیره‌تر از پس‌زمینه»، خلاف پلهٔ M3 ← سطح دیالوگ fieldBg
#      (روز FFFFFF — هم‌زبانهٔ پیش‌فرض BottomSheet که خودش key_dialogBackground است؛ آپستریم F5F6F7
#      همین مایهٔ نزدیک‌به‌سفید بود / شب 241D14 یک پله بالاتر از وایپرپ)
#      dialogGiftsTabText: آپستریم سرد 56595C ← dim (روی سطح دیالوگ ۵٫۰۹/۶٫۲۰ ≥ ۴٫۵).
#   ۳) سطح روشنِ خانوادهٔ اصلی تأیید شد (بدون تغییر): dialogBackground = fieldBg
#      (روز FFFFFF = روشن‌ترین سطح روی کاغذ / شب 241D14 = یک پله بالاتر از وایپرپ ۱۷۱۳۰E)؛
#      dialogBackgroundGray (سکشن خاکستری درون دیالوگ) = یک پله پایین‌تر از کارت در هر دو حالت.
#
# نکته‌های ممیزی (بدون تغییر):
#   • popup_fixed_alert2 (کارت منوها) اندازه‌گیری شد: ~۱۶dp — قصد قدم ۱۶ (SHAPE_MENU=۲۰) در asset
#     محقق نشده بود؛ خارج از محدودهٔ این قدم (خانوادهٔ منو = قدم ۱۶/۲۷) — یادداشت برای پالیش بعدی.
#   • popup_fixed_alert (سبک قدیمی ~۶dp — AvatarPreviewer/Topics/Profile/GroupCall/Translate) و
#     popup_fixed_alert3 (~۹dp — PaintView استوری) سبک قدیمی‌اند — کاندیدای پاک‌سازی فاز ۶ (قدم ۴۷).
#   • dialogTextBlue2 آپستریم آبی 3a95d5 از فاز ۰ اکسنت است (سربرگ‌های تنظیمات) — تأیید.
#   • انتخابگر دکمه‌های متنی دیالوگ dp(20) آپستریم = قدم ۳۲ (دکمه‌ها) رسیدگی می‌کند.
#   • progressViewContainer اسپینر dp(18) + مسیر بلورش dp(18) خودسازگارند (قرص کوچک، نیم‌ارتفاع≈۱۸).
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
OLD_ASSET = "/tmp/alert4_backup/xxhdpi.png"
NEW_ASSET = os.path.join(ROOT, "TMessagesProj/src/main/res/drawable-xxhdpi/popup_fixed_alert4.9.png")
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
    l1, l2 = lum(a), lum(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def composite(fg, bg):
    """ColorUtils.compositeColors (SRC_OVER)"""
    faa = (fg >> 24) & 255
    r1, g1, b1 = rgb(fg)
    r2, g2, b2 = rgb(bg)
    ch = lambda f, b: int(round((f * faa + b * (255 - faa)) / 255.0))
    return (ch(r1, r2) << 16) | (ch(g1, g2) << 8) | ch(b1, b2)


def mix(c1, c2, t):
    r = int((c1 >> 16 & 255) * (1 - t) + (c2 >> 16 & 255) * t)
    g = int((c1 >> 8 & 255) * (1 - t) + (c2 >> 8 & 255) * t)
    b = int((c1 & 255) * (1 - t) + (c2 & 255) * t)
    return (r << 16) | (g << 8) | b


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 380, 344
STRIP_DP = 118
TBL_DP = 150
TOTAL_DP = 6 + H_DP + 10 + STRIP_DP + 8 + TBL_DP + 10
img = Image.new("RGB", (W_DP * S * 2 + 24, TOTAL_DP * S), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)
f_title = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 15 * S)

PANEL_X = [12, 12 + W_DP * S + 24]


def draw_panel(pi, theme, caption, note, dark):
    x0 = PANEL_X[pi]
    wt = theme.get("chat_wallpaper_gradient_top1", theme["chat_wallpaper"])
    wb = theme.get("chat_wallpaper_gradient_bottom1", theme["chat_wallpaper"])
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        c = mix(wt & 0xFFFFFF, wb & 0xFFFFFF, t)
        y0 = (6 + i * H_DP / steps) * S
        d.rectangle([x0, y0, x0 + W_DP * S, (6 + (i + 1) * H_DP / steps) * S], fill=rgb(c))
    # کپشن روی چیپ اسکریم (خوانا روی هر دو وایپرپ — هم‌الگوی قدم ۲۴)
    d.rounded_rectangle([x0 + 8 * S, 9 * S, x0 + W_DP * S - 8 * S, 36 * S], radius=6 * S,
                        fill=rgb(composite(0x99000000, wt & 0xFFFFFF)))
    d.text((x0 + 14 * S, 11 * S), caption, font=f_small, fill=(255, 250, 242))
    d.text((x0 + 14 * S, 23 * S), note, font=f_small, fill=(255, 250, 242))

    bg = theme["dialogBackground"]
    gray = theme["dialogBackgroundGray"]
    text = theme["dialogTextBlack"]
    dim = theme["dialogTextGray"]
    timec = theme["dialogTextGray3"]
    acc = theme["dialogTextBlue"]
    sel = composite(theme["dialogButtonSelector"], bg)

    # ── کارت دیالوگ با شعاع توکن SHAPE_DIALOG=۲۸ ──
    dx, dy, dw, dh = 28, 46, 324, 240
    for off, al in [(6, 14), (4, 22), (2, 30)]:
        d.rounded_rectangle([x0 + (dx - off) * S, (dy - off) * S, x0 + (dx + dw + off) * S, (dy + dh + off) * S],
                            radius=(28 + off) * S, fill=(0, 0, 0, al))
    d.rounded_rectangle([x0 + dx * S, dy * S, x0 + (dx + dw) * S, (dy + dh) * S],
                        radius=28 * S, fill=rgb(bg))

    d.text((x0 + (dx + 20) * S, (dy + 16) * S), "Delete chat?", font=f_title, fill=rgb(text))
    d.text((x0 + (dx + 20) * S, (dy + 42) * S), "This will clear all messages", font=f_row, fill=rgb(dim))
    d.text((x0 + (dx + 20) * S, (dy + 60) * S), "History can not be restored.", font=f_row, fill=rgb(dim))

    # سکشن خاکستری درون دیالوگ (یک پله پایین‌تر از کارت)
    sy = dy + 88
    d.rounded_rectangle([x0 + (dx + 12) * S, sy * S, x0 + (dx + dw - 12) * S, (sy + 44) * S],
                        radius=16 * S, fill=rgb(gray))
    d.text((x0 + (dx + 24) * S, (sy + 6) * S), "Ask a question", font=f_row, fill=rgb(text))
    d.text((x0 + (dx + 24) * S, (sy + 26) * S), "hint — dialogTextHint", font=f_small, fill=rgb(timec))

    # فیلد جستجوی درون دیالوگ
    fy = sy + 52
    d.rounded_rectangle([x0 + (dx + 12) * S, fy * S, x0 + (dx + dw - 12) * S, (fy + 34) * S],
                        radius=17 * S, fill=rgb(theme["dialogSearchBackground"]))
    d.ellipse([x0 + (dx + 24) * S, (fy + 12) * S, x0 + (dx + 32) * S, (fy + 20) * S],
              outline=rgb(theme["dialogSearchIcon"]), width=S)
    d.text((x0 + (dx + 40) * S, (fy + 10) * S), "Search", font=f_row, fill=rgb(theme["dialogSearchHint"]))

    # دکمه‌های متنی (انتخابگر پرس ۱۰٪ اکسنت روی کارت)
    bx = dx + dw - 176
    d.rounded_rectangle([x0 + bx * S, (dy + 194) * S, x0 + (bx + 76) * S, (dy + 222) * S],
                        radius=14 * S, fill=rgb(sel))
    d.text((x0 + (bx + 14) * S, (dy + 200) * S), "CANCEL", font=f_row, fill=rgb(acc))
    d.text((x0 + (bx + 94) * S, (dy + 200) * S), "DELETE", font=f_row, fill=rgb(theme["dialogButton"]))

    # ── نوار تب شیت هدیه (دو کلید جدید قدم ۲۹) ──
    gbg = theme["dialogGiftsBackground"]
    gtab = theme["dialogGiftsTabText"]
    gx, gy = 28, dy + dh + 8
    d.rounded_rectangle([x0 + gx * S, gy * S, x0 + (gx + 324) * S, (gy + 34) * S],
                        radius=14 * S, fill=rgb(gbg))
    d.rounded_rectangle([x0 + (gx + 10) * S, (gy + 5) * S, x0 + (gx + 148) * S, (gy + 29) * S],
                        radius=12 * S, fill=rgb(composite(0x17000000 | (0 << 16), gbg)))
    d.text((x0 + (gx + 40) * S, (gy + 11) * S), "Featured", font=f_row, fill=rgb(gtab))
    d.text((x0 + (gx + 180) * S, (gy + 11) * S), "All gifts", font=f_row, fill=rgb(composite(0x89000000 | (gtab & 0xFFFFFF), gbg)))
    d.text((x0 + (gx + 10) * S, (gy + 38) * S), "gift sheet tabs — dialogGiftsBackground / dialogGiftsTabText (new)",
           font=f_small, fill=rgb(composite(0xA0000000 | (gtab & 0xFFFFFF), gbg)))


def draw_assets(y_dp):
    """مقایسهٔ ۹-پچ قدیم (آپستریم ~۱۶dp) و جدید (توکن ۲۸dp) — بدون ردیف/ستون مارکر"""
    cap_y = y_dp
    for idx, (path, cap) in enumerate([(OLD_ASSET, "9-patch corner — old (upstream ~16dp)"),
                                       (NEW_ASSET, "9-patch corner — new (SHAPE_DIALOG 28dp)")]):
        if not os.path.exists(path):
            continue
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        im = im.crop((1, 1, w - 1, h - 1))  # حذف مارکرهای ۹-پچ
        scale = (STRIP_DP - 22) * S / im.height
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
        x0 = PANEL_X[idx] + 40 * S
        d.text((x0, (cap_y + 2) * S), cap, font=f_small, fill=(210, 200, 185))
        base = img.crop((x0, (cap_y + 16) * S, x0 + im.width, (cap_y + 16) * S + im.height)).convert("RGBA")
        base.alpha_composite(im)
        img.paste(base, (x0, (cap_y + 16) * S))


draw_panel(0, day, "Amber Day — dialogs", "dialogBackground = fieldBg FFFFFF · gray = surface F3ECE2", False)
draw_panel(1, night, "Amber Night — dialogs", "dialogBackground = surface 241D14 · gray = 17130E", True)

strip_y = 6 + H_DP + 10
draw_assets(strip_y)

# ── جدول کنتراست (یک خط در هر سطر — روز · شب) ──
y = strip_y + STRIP_DP + 6
d.text((12, y * S), "WCAG contrast (parsed from attheme):", font=f_small, fill=(235, 225, 210))
rows = [
    ("title/message  dialogTextBlack / bg", "dialogTextBlack", "dialogBackground", 4.5, False),
    ("secondary  dialogTextGray / bg", "dialogTextGray", "dialogBackground", 4.5, False),
    ("time  dialogTextGray3 / bg", "dialogTextGray3", "dialogBackground", 3.0, False),
    ("buttons  dialogTextBlue / bg", "dialogTextBlue", "dialogBackground", 3.0, False),
    ("press tint  dialogButtonSelector ◦ bg (shape)", "dialogButtonSelector", "dialogBackground", 1.05, True),
    ("search hint  dialogSearchHint / field", "dialogSearchHint", "dialogSearchBackground", 3.0, False),
    ("gift tabs  dialogGiftsTabText / giftsBg (new)", "dialogGiftsTabText", "dialogGiftsBackground", 4.5, False),
    ("section  dialogTextBlack / bgGray", "dialogTextBlack", "dialogBackgroundGray", 4.5, False),
]
for i, (label, k1, k2, req, comp) in enumerate(rows):
    ry = (y + 18 + i * 15) * S
    rd_t = day[k1]
    rn_t = night[k1]
    if comp:
        rd_v = ratio(composite(rd_t, day[k2]), day[k2])
        rn_v = ratio(composite(rn_t, night[k2]), night[k2])
        lbl = "shape" if req == 1.05 else f"req {req}"
        okd = okn = rd_v >= req
    else:
        rd_v = ratio(rd_t, day[k2])
        rn_v = ratio(rn_t, night[k2])
        lbl = f"req {req}"
        okd, okn = rd_v >= req, rn_v >= req
    ok = okd and okn
    color = (140, 200, 120) if ok else (230, 120, 100)
    d.text((16, ry), f"{label}", font=f_small, fill=(195, 185, 170))
    d.text((16 + 520, ry), f"day {rd_v:.2f} · night {rn_v:.2f}  ({lbl})  {'PASS' if ok else 'LOW!'}",
           font=f_small, fill=color)

out = os.path.join(ROOT, "download/ui2-step29-dialogs-preview.png")
img.save(out)
print("saved", out)

print("\n--- contrast report ---")
for label, k1, k2, req, comp in rows:
    if comp:
        rd_v = ratio(composite(day[k1], day[k2]), day[k2])
        rn_v = ratio(composite(night[k1], night[k2]), night[k2])
    else:
        rd_v = ratio(day[k1], day[k2])
        rn_v = ratio(night[k1], night[k2])
    print(f"{label}: day {rd_v:.2f} night {rn_v:.2f} (req {req})")

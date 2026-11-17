#!/usr/bin/env python3
# UI2 قدم ۱۸ — پیش‌نمایش حالت انتخاب/آرشیو (نوار اکشن‌مود + خانواده سوییچ/چک‌باکس)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# نوار اکشن‌مود: روی کانتینر FFE9CF (قدم ۱۱) با آیکون/شمارنده outText و ripple×۱۰٪ (کلیدهای پالت — از قبل سالم).
# رفع‌های رنگی این قدم (۶ کلید):
#   ۱) switch2Track: روز قرمز آپستریم F57480 / شب خاکستری سرد 3A3A3E ← هم‌زبانه switchTrack (DCCFB8/382C1C)
#   ۲) switch2TrackChecked: روز آبی آپستریم 229AF0 / شب F97316 خارج‌ازتوکن ← اکسنت
#      + مسیر پیش‌فرض Switch از fill_RedNormal به switch2Track رفت (تاگل‌های متن‌دار: قرمز←آبی به خنثی←اکسنت)
#   ۳) groupcreate_sectionText: خاکستری سرد 7C8288 ← dim (متن فرعی ردیف‌های منوی اکشن‌مود قدم ۱۶)
#   ۴) groupcreate_spanBackground: خاکستری سرد F2F2F2/1D1D21 ← سطح گرم (چیپ‌های فیلتر جستجو)
#   ۵) featuredStickers_buttonText: سفید هاردکد (شب روی اکسنت ۲٫۰۳:۱) ← onAccent (چیپ انتخاب‌شده + آواتار ترکیبی)
#   ۶) chat_TextSelectionCursor: آبی آپستریم 63C8FF ← اکسنت (دستگیره انتخاب متن)
# چک‌مارک حباب انتخاب ردیف (CheckBoxBase) از قبل accent/onAccent است — سالم.
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
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


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 250
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 14 * S)
f_count = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 13 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)


def screen(x0, theme, caption, dark):
    header = theme["actionBarDefault"]
    listbg = theme["windowBackgroundWhite"]
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 56 * S], radius=14 * S, fill=rgb(header))
    d.rectangle([x0, 6 + 40 * S, x0 + W_DP * S, 6 + 56 * S], fill=rgb(header))
    # ── نوار اکشن‌مود ──
    d.text((x0 + 70 * S, 22 * S), "3 chats", font=f_count, fill=rgb(theme["actionBarActionModeDefaultIcon"]))
    # close (back rotated)
    d.line([x0 + 22 * S, 20 * S, x0 + 38 * S, 36 * S], fill=rgb(theme["actionBarActionModeDefaultIcon"]), width=2 * S)
    d.line([x0 + 38 * S, 20 * S, x0 + 22 * S, 36 * S], fill=rgb(theme["actionBarActionModeDefaultIcon"]), width=2 * S)
    # آیتم‌های pin/mute/archive/delete (آیکون outText)
    for i, ix in enumerate((W_DP - 172, W_DP - 132, W_DP - 92, W_DP - 52)):
        d.rounded_rectangle([x0 + ix * S, 22 * S, x0 + ix * S + 16 * S, 22 * S + 16 * S], radius=4 * S,
                            fill=rgb(theme["actionBarActionModeDefaultIcon"]))
    # ── ردیف انتخاب‌شده با حباب چک‌مارک اکسنت (از قبل سالم) ──
    ry = 70
    d.ellipse([x0 + 16 * S, (ry + 6) * S, x0 + 16 * S + 36 * S, (ry + 6 + 36) * S], fill=rgb(theme["chats_unreadCounter"]))
    cx, cy, rad = x0 + (16 + 30) * S, (ry + 6 + 30) * S, 9 * S
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=rgb(theme["checkbox"]))
    d.line([cx - 4 * S, cy, cx - 1 * S, cy + 3 * S], fill=rgb(theme["checkboxCheck"]), width=2 * S)
    d.line([cx - 1 * S, cy + 3 * S, cx + 4 * S, cy - 3 * S], fill=rgb(theme["checkboxCheck"]), width=2 * S)
    d.text((x0 + 64 * S, (ry + 8) * S), "Selected chat", font=f_row, fill=rgb(theme["chats_name"]))
    # ── تاگل سوییچ (مسیر جدید: خنثی ← اکسنت) ──
    ty = 128
    d.rounded_rectangle([x0 + (W_DP - 52) * S, ty * S, x0 + (W_DP - 14) * S, (ty + 14) * S], radius=7 * S, fill=rgb(theme["switch2Track"]))
    d.ellipse([x0 + (W_DP - 50) * S, (ty - 4) * S, x0 + (W_DP - 50) * S + 22 * S, (ty - 4) * S + 22 * S], fill=rgb(theme["windowBackgroundWhite"]))
    d.rounded_rectangle([x0 + (W_DP - 52) * S, (ty + 22) * S, x0 + (W_DP - 14) * S, (ty + 36) * S], radius=7 * S, fill=rgb(theme["switch2TrackChecked"]))
    d.ellipse([x0 + (W_DP - 36) * S, (ty + 18) * S, x0 + (W_DP - 36) * S + 22 * S, (ty + 18) * S + 22 * S], fill=rgb(theme["windowBackgroundWhite"]))
    d.text((x0 + 16 * S, (ty + 2) * S), "Toggle (was RED→BLUE)", font=f_row, fill=rgb(theme["windowBackgroundWhiteBlackText"]))
    d.text((x0 + 16 * S, (ty + 24) * S), "Now neutral→accent", font=f_small, fill=rgb(theme["groupcreate_sectionText"]))
    # ── چیپ فیلتر جستجو (spanBackground جدید + متن انتخاب‌شده onAccent) ──
    cy2 = 186
    d.rounded_rectangle([x0 + 16 * S, cy2 * S, x0 + 110 * S, (cy2 + 30) * S], radius=15 * S, fill=rgb(theme["groupcreate_spanBackground"]))
    d.text((x0 + 30 * S, (cy2 + 8) * S), "Media  filter", font=f_small, fill=rgb(theme["windowBackgroundWhiteBlackText"]))
    d.rounded_rectangle([x0 + 122 * S, cy2 * S, x0 + 216 * S, (cy2 + 30) * S], radius=15 * S, fill=rgb(theme["featuredStickers_addButton"]))
    d.text((x0 + 136 * S, (cy2 + 8) * S), "Selected", font=f_small, fill=rgb(theme["featuredStickers_buttonText"]))
    # دستگیره انتخاب متن (اکسنت)
    d.ellipse([x0 + 230 * S, (cy2 + 8) * S, x0 + 242 * S, (cy2 + 20) * S], fill=rgb(theme["chat_TextSelectionCursor"]))
    d.ellipse([x0 + 228 * S, (cy2 + 10) * S, x0 + 234 * S, (cy2 + 16) * S], fill=rgb(theme["windowBackgroundWhite"]))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


screen(12, day, "DAY  toggle DCCFB8->C25E00 (was F57480->229AF0), chip surface, cursor accent", False)
screen(12 + W_DP * S + 12, night, "NIGHT  toggle 382C1C->F5A623 (was 3A3A3E->F97316), chip 241D14", True)

out = os.path.join(ROOT, "download/ui2-step18-actionmode-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    thumb = t["windowBackgroundWhite"]
    print(f"{name_} toggle: thumb-on-accent(checked)   = {ratio(thumb, t['switch2TrackChecked']):5.2f}:1  (UI >= 3.0)")
    print(f"{name_} toggle: track-neutral vs card      = {ratio(t['switch2Track'], t['windowBackgroundWhite']):5.2f}:1  (track boundary)")
    print(f"{name_} actionmode icon on bar container   = {ratio(t['actionBarActionModeDefaultIcon'], t['actionBarActionModeDefault']):5.2f}:1  (icons >= 3.0)")
    print(f"{name_} count text on bar container        = {ratio(t['actionBarActionModeDefaultIcon'], t['actionBarActionModeDefault']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} selection bubble accent on row bg  = {ratio(t['checkbox'], t['windowBackgroundWhite']):5.2f}:1  (UI >= 3.0)")
    print(f"{name_} checkmark onAccent-on-accent       = {ratio(t['checkboxCheck'], t['checkbox']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} chip text ink-on-surface           = {ratio(t['windowBackgroundWhiteBlackText'], t['groupcreate_spanBackground']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} selected chip text onAccent-accent  = {ratio(t['featuredStickers_buttonText'], t['featuredStickers_addButton']):5.2f}:1  (AA >= 4.5)  [night was 2.03]")
    print(f"{name_} sectionText on menu card           = {ratio(t['groupcreate_sectionText'], t['actionBarDefaultSubmenuBackground']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} textSelectionCursor on window      = {ratio(t['chat_TextSelectionCursor'], t['windowBackgroundWhite']):5.2f}:1  (UI >= 3.0)")

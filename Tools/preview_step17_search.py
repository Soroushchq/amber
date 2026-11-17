#!/usr/bin/env python3
# UI2 قدم ۱۷ — پیش‌نمایش حالت جستجو (بار جستجوی شناور + نتایج)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# بار جستجو: FragmentSearchField — شعاع از ۲۰dp هاردکد به SHAPE_FIELD (۱۶dp) بایند شد؛
# پس‌زمینه تونال: جوهر ×۵٪ روز / ×۷٪ شب روی کانتینر هدر (کلیید windowBackgroundWhiteBlackText).
# رفع‌های رنگی این قدم:
#   ۱) actionBarDefaultSearch: fieldBg (روز سفید روی کرم ۱٫۱۳:۱ / شب تیره روی تیره ~۱٫۰۵:۱ = نامرئی) ← جوهر
#   ۲) groupcreate_cursor (کرسر): F97A20 خارج از توکن ← اکسنت
#   ۳) listSelector (ripple دکمه پاک‌کردن/آیکون‌های اضافه): 0x0f000000 سرد ← اکسنت×۸٪/۱۰٪
#   ۴) graySection/graySectionText (سرستون نتایج): 121213 سرد ← سطح گرم surface + متن dim
#   ۵) ProfileSearchCell دکمه Open: متن سفید هاردکد روی اکسنت (شب ۲٫۰۳:۱) ← onAccent
#   ۶) چیپ «جستجوی همه»: شعاع ۶px هاردکد ← SHAPE_BADGE (۱۲dp = پیل)
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


def blend(fg, bg, a):
    def ch(f, b):
        return int(round(f * a + b * (1 - a)))
    r, g, b = rgb(fg)
    br, bgc, bb = rgb(bg)
    return (ch(r, br) << 16) | (ch(g, bgc) << 8) | ch(b, bb)


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 250
FIELD_R = 16   # SHAPE_FIELD
CHIP_R = 12    # SHAPE_BADGE
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 15 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 13 * S)
f_sec = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)


def screen(x0, theme, caption, dark):
    header = theme["actionBarDefault"]
    listbg = theme["windowBackgroundWhite"]
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    # هدر (کانتینر قدم ۱۱)
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 56 * S], radius=14 * S, fill=rgb(header))
    d.rectangle([x0, 6 + 40 * S, x0 + W_DP * S, 6 + 56 * S], fill=rgb(header))
    d.text((x0 + 16 * S, 14 * S), "Chats", font=f_word, fill=rgb(theme["actionBarDefaultTitle"]))
    # آیکون‌های هدر (dim)
    for i, ix in enumerate((W_DP - 92, W_DP - 60, W_DP - 28)):
        d.rounded_rectangle([x0 + ix * S, 12 * S + 6, x0 + ix * S + 18 * S, 12 * S + 6 + 18 * S], radius=4 * S,
                            fill=rgb(theme["actionBarDefaultIcon"]))
    # ── بار جستجوی شناور (FragmentSearchField) ──
    # پس‌زمینه تونال: جوهر ×۵٪ روز / ×۷٪ شب روی هدر
    field_bg = blend(theme["windowBackgroundWhiteBlackText"], header, 0.05 if not dark else 0.07)
    fx, fy, fw, fh = 12, 64, W_DP - 24, 44
    d.rounded_rectangle([x0 + fx * S, fy * S, x0 + (fx + fw) * S, (fy + fh) * S], radius=FIELD_R * S, fill=rgb(field_bg))
    # آیکون جستجو (جوهر ×۶۰٪)
    icon_col = blend(theme["windowBackgroundWhiteBlackText"], header, 0.60)
    d.ellipse([x0 + (fx + 12) * S, (fy + 14) * S, x0 + (fx + 12 + 12) * S, (fy + 14 + 12) * S], outline=rgb(icon_col), width=2 * S)
    d.line([x0 + (fx + 22) * S, (fy + 24) * S, x0 + (fx + 27) * S, (fy + 29) * S], fill=rgb(icon_col), width=2 * S)
    # متن جستجو (جوهر) + کرسر (اکسنت) + placeholder (جوهر ×۵۰٪)
    d.text((x0 + (fx + 48) * S, (fy + 14) * S), "amber", font=f_row, fill=rgb(theme["windowBackgroundWhiteBlackText"]))
    d.line([x0 + (fx + 108) * S, (fy + 13) * S, x0 + (fx + 108) * S, (fy + 31) * S], fill=rgb(theme["groupcreate_cursor"]), width=2 * S)
    d.text((x0 + (fx + 118) * S, (fy + 14) * S), "| placeholder dim", font=f_row,
           fill=rgb(blend(theme["windowBackgroundWhiteBlackText"], header, 0.50)))
    # دکمه پاک‌کردن با ripple اکسنت×۸٪ (listSelector جدید — با آلفای واقعی)
    cx = x0 + (fx + fw - 40) * S
    a = (theme["listSelector"] >> 24) & 255
    d.ellipse([cx, (fy + 6) * S, cx + 32 * S, (fy + 38) * S], fill=rgb(theme["listSelector"]) + (a,))
    d.line([cx + 11 * S, (fy + 17) * S, cx + 21 * S, (fy + 27) * S], fill=rgb(icon_col), width=2 * S)
    d.line([cx + 21 * S, (fy + 17) * S, cx + 11 * S, (fy + 27) * S], fill=rgb(icon_col), width=2 * S)
    # ── نتایج: سرستون بخش (GraySectionCell) + ردیف + دکمه Open ──
    sy = 122
    d.rounded_rectangle([x0 + 8 * S, sy * S, x0 + (W_DP - 8) * S, (sy + 24) * S], radius=8 * S, fill=rgb(theme["graySection"]))
    d.text((x0 + 16 * S, (sy + 5) * S), "CHATS AND CONTACTS", font=f_sec, fill=rgb(theme["graySectionText"]))
    d.text((x0 + (W_DP - 130) * S, (sy + 5) * S), "3 found", font=f_sec, fill=rgb(theme["windowBackgroundWhiteValueText"]))
    # ردیف نتیجه پروفایل با دکمه Open (اکسنت + onAccent — رفع سفید هاردکد)
    ry = 154
    d.ellipse([x0 + 16 * S, (ry + 6) * S, x0 + 16 * S + 36 * S, (ry + 6 + 36) * S], fill=rgb(theme["chats_unreadCounter"]))
    d.text((x0 + 64 * S, (ry + 6) * S), "Amber Bot", font=f_row, fill=rgb(theme["windowBackgroundWhiteBlackText"]))
    d.text((x0 + 64 * S, (ry + 26) * S), "bot", font=f_small, fill=rgb(theme["windowBackgroundWhiteGrayText"]))
    bx = x0 + (W_DP - 120) * S
    d.rounded_rectangle([bx, (ry + 10) * S, bx + 100 * S, (ry + 10 + 28) * S], radius=14 * S, fill=rgb(theme["featuredStickers_addButton"]))
    d.text((bx + 30 * S, (ry + 16) * S), "OPEN", font=f_small, fill=rgb(theme["featuredStickers_addButtonIcon"]))
    # ردیف دوم: چیپ «جستجوی همه» (SHAPE_BADGE پیل + fill اکسنت×۱۵٪)
    cy = 200
    chip_w = 150
    d.rounded_rectangle([x0 + 16 * S, cy * S, x0 + (16 + chip_w) * S, (cy + 26) * S], radius=CHIP_R * S,
                        fill=rgb(blend(theme["featuredStickers_addButton"], listbg, 0.15)))
    d.text((x0 + 32 * S, (cy + 5) * S), "Search All Chats", font=f_row, fill=rgb(theme["featuredStickers_addButton"]))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


screen(12, day, "DAY  field r=16 (SHAPE_FIELD), cursor accent, sections warm F3ECE2", False)
screen(12 + W_DP * S + 12, night, "NIGHT  field r=16, cursor F5A623, sections 241D14", True)

out = os.path.join(ROOT, "download/ui2-step17-search-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t, dark in (("DAY  ", day, False), ("NIGHT", night, True)):
    header = t["actionBarDefault"]
    field_bg = blend(t["windowBackgroundWhiteBlackText"], header, 0.05 if not dark else 0.07)
    print(f"{name_} header = #{header:06X}  fieldBg(tonal) = #{field_bg:06X}")
    print(f"{name_} search-text-on-header    = {ratio(t['actionBarDefaultSearch'], header):5.2f}:1  (AA >= 4.5)  [was {ratio(t['windowBackgroundWhite'] if not dark else t['windowBackgroundWhite'], header):.2f}:1]")
    print(f"{name_} placeholder-on-header    = {ratio(t['actionBarDefaultSearchPlaceholder'], header):5.2f}:1  (AA large >= 3.0)")
    print(f"{name_} cursor-on-field (accent) = {ratio(t['groupcreate_cursor'], field_bg):5.2f}:1  (UI >= 3.0)")
    print(f"{name_} section-text-on-section = {ratio(t['graySectionText'], t['graySection']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} sectionBg-on-list        = {ratio(t['graySection'], t['windowBackgroundWhite']):5.2f}:1  (band signal)")
    print(f"{name_} onAccent-on-accent(Open) = {ratio(t['featuredStickers_addButtonIcon'], t['featuredStickers_addButton']):5.2f}:1  (AA >= 4.5)  [night was 2.03]")
    print(f"{name_} chipText-accent-on-fill  = {ratio(t['featuredStickers_addButton'], blend(t['featuredStickers_addButton'], t['windowBackgroundWhite'], 0.15)):5.2f}:1  (chip label)")

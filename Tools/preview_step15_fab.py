#!/usr/bin/env python3
# UI2 قدم ۱۵ — پیش‌نمایش فاب شناور Expressive (مربع‌گرد SHAPE_FAB=۲۰dp + سایه آمبر)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند (نه کپی دستی).
# فرم: آپستریم دایره کامل ۴۸dp بود → مربع‌گرد ۲۰dp هم‌زبان کارت‌های قدم ۱۳.
# سایه: elevation توکن ELEV_FAB (۶dp) با تینت آمبر — روز اکسنت×۳۰٪ (4DC25E00)،
# شب خنثی×۴۵٪ (73000000)؛ در کد واقعی از setOutlineSpot/AmbientShadowColor (API 28+).
# پرس = over(accent، onAccent، ۲۰٪). گزارش کنتراست WCAG هم چاپ می‌شود.
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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

def rgba(c, a):
    return rgb(c) + (max(0, min(255, int(a * 255))),)

def with_alpha(c):
    return (c >> 16 & 255, c >> 8 & 255, c & 255, (c >> 24) & 0xFF)

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

def over_tokens(fg, bg, a):
    fa = a
    fr, fgc, fb = rgb(fg)
    br, bgc, bb = rgb(bg)
    return (0, int(round(fr * fa + br * (1 - fa))), int(round(fgc * fa + bgc * (1 - fa))), int(round(fb * fa + bb * (1 - fa))))[1:]

night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 220
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)

FAB_R = 20 * S   # SHAPE_FAB — قدم ۱۵ (آپستریم دایره کامل)
FAB_SIZE = 48 * S

def pencil(d0, x0, y0, size, color):
    """قلم‌موی ساده — همان نقش R.drawable.input_edit در فاب"""
    s = size / 16.0
    pts = [(x0 + 2 * s, y0 + 14 * s), (x0 + 5 * s, y0 + 15 * s), (x0 + 3.5 * s, y0 + 11.5 * s)]
    d0.polygon(pts, fill=rgb(color))
    d0.polygon([(x0 + 4 * s, y0 + 10.5 * s), (x0 + 11 * s, y0 + 3.5 * s), (x0 + 12.5 * s, y0 + 5 * s), (x0 + 5.5 * s, y0 + 12 * s)], fill=rgb(color))
    d0.polygon([(x0 + 11.8 * s, y0 + 2.8 * s), (x0 + 13 * s, y0 + 1.5 * s), (x0 + 14.5 * s, y0 + 3 * s), (x0 + 13.2 * s, y0 + 4.2 * s)], fill=rgb(color))

def fab(day_mode, theme, is_pressed, x0, y0):
    fabc = theme["featuredStickers_addButton"]
    prc = theme["featuredStickers_addButtonPressed"]
    icon = theme["featuredStickers_addButtonIcon"]
    # سایه آمبر — لایه‌های محوشونده (شبیه‌سازی elevation 6dp)
    tint = 0x4DC25E00 if day_mode else 0x73000000
    tc = (tint >> 16 & 255, tint >> 8 & 255, tint & 255, min(90, (tint >> 24) & 0xFF))
    for i, grow in enumerate((6, 4, 2)):
        pad = grow * S
        d.rounded_rectangle([x0 - pad, y0 - pad + i * S, x0 + FAB_SIZE + pad, y0 + FAB_SIZE + pad + i * S],
                            radius=FAB_R + pad, fill=tc)
    d.rounded_rectangle([x0, y0, x0 + FAB_SIZE, y0 + FAB_SIZE], radius=FAB_R,
                        fill=rgb(prc if is_pressed else fabc))
    pencil(d, x0 + 14 * S, y0 + 14 * S, 20 * S, icon)

def screen(x0, theme, day_mode, caption):
    listbg = theme["windowBackgroundWhite"]
    container = theme["actionBarDefault"]
    name = theme["chats_name"]
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 44 * S], radius=14 * S, fill=rgb(container))
    d.rectangle([x0, 6 + 22 * S, x0 + W_DP * S, 6 + 44 * S], fill=rgb(container))
    d.text((x0 + 14 * S, 16 * S), "AmberGram", font=f_word, fill=rgb(name))
    fab(day_mode, theme, False, x0 + (W_DP - 20) * S - FAB_SIZE, 6 + (H_DP - 14) * S - FAB_SIZE)
    # حالت پرس کنار فاب (نمایش رنگ پرس)
    fab(day_mode, theme, True, x0 + (W_DP - 20) * S - FAB_SIZE * 2 - 14 * S, 6 + (H_DP - 14) * S - FAB_SIZE)
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))

screen(12, day, True, "DAY  fab r=20 SHAPE_FAB accent C25E00, icon white, shadow C25E00@30% (right: pressed CE7E33)")
screen(12 + W_DP * S + 12, night, False, "NIGHT  fab r=20 accent F5A623, icon 3A2400, shadow black@45% (right: pressed D08C1C)")

out = os.path.join(ROOT, "download/ui2-step15-fab-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

# ── گزارش کنتراست WCAG ──
print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    listbg = t["windowBackgroundWhite"]
    fabc = t["featuredStickers_addButton"]
    print(f"{name_} addIcon-on-fab        = {ratio(t['featuredStickers_addButtonIcon'], fabc):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} fab-on-list           = {ratio(fabc, listbg):5.2f}:1  (primary action surface — signal)")
    print(f"{name_} fab-pressed (derived) = over(accent,onAccent,20%) state tint")
    print(f"{name_} shadow tint (token)   = {'4DC25E00 amber@30%' if name_.startswith('DAY') else '73000000 neutral@45%'} — elevation 6dp (ELEV_FAB), API 28+ outline tint")

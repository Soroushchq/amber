#!/usr/bin/env python3
# UI2 قدم ۱۲ — پیش‌نمایش تب‌های فولدر با پیل شناور فعال Expressive (روز/شب)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند (نه کپی دستی).
# پیل فعال = key_actionBarTabLine (AmberTokens.DAY_NAV_PILL #FFDDB8 / NIGHT_NAV_PILL #5C4000)
# متن فعال = key_actionBarTabActiveText (DAY_OUT_TEXT #331E00 / NIGHT_OUT_TEXT #FFDDB8)
# گزارش کنتراست WCAG هم چاپ می‌شود.
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

def rgba(c, a):
    return rgb(c) + (int(a * 255),)

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

W_DP, H_DP = 360, 190
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)

def screen(x0, theme, caption):
    listbg = theme["windowBackgroundWhite"]
    container = theme["actionBarDefault"]
    text = theme["actionBarDefaultTitle"]
    dim = theme["actionBarDefaultIcon"]
    pill = theme["actionBarTabLine"]        # پیل فعال — قدم ۱۲
    act_txt = theme["actionBarTabActiveText"]
    unact_txt = theme["actionBarTabUnactiveText"]
    # بدنه صفحه
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    # ناحیه هدر (کانتینر قدم ۱۱)
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 104 * S], radius=14 * S, fill=rgb(container))
    d.rectangle([x0, 6 + 14 * S, x0 + W_DP * S, 6 + 104 * S], fill=rgb(container))
    # لوگوی هدر
    plane_fill = act_txt if lum(act_txt) < lum(pill) else dim
    d.text((x0 + 14 * S, 26 * S), "AmberGram", font=f_word, fill=rgb(text))
    for i in range(3):
        cx = x0 + (W_DP - 18 - i * 24) * S
        cy = 30 * S
        d.ellipse([cx - 8 * S, cy - 8 * S, cx + 8 * S, cy + 8 * S], outline=rgba(dim, 0.18), width=S)
    # ── نوار تب‌ها با پیل شناور فعال (قدم ۱۲) ──
    ty = 104 * S
    tabs = [("All", True), ("Personal", False), ("Groups", False), ("Channels", False)]
    x = x0 + 10 * S
    widths = [36, 64, 56, 66]
    for (lbl, active), w in zip(tabs, widths):
        if active:
            # پیل توپر NAV_PILL — همان چیزی که FilterTabsView.drawSelector با آلفای کامل می‌کشد
            d.rounded_rectangle([x, ty + 11 * S, x + w * S, ty + 39 * S], radius=14 * S, fill=rgb(pill))
            d.text((x + 10 * S, ty + 17 * S), lbl, font=f_small, fill=rgb(act_txt))
        else:
            d.text((x + 10 * S, ty + 17 * S), lbl, font=f_small, fill=rgb(unact_txt))
        x += w * S + 8 * S
    # ردیف‌های لیست (استایل فعلی — کارت‌ها = قدم ۱۳)
    for r in range(2):
        ry = (150 + r * 40) * S
        d.ellipse([x0 + 12 * S, ry, x0 + 12 * S + 34 * S, ry + 34 * S], fill=rgba(text, 0.10))
        d.rounded_rectangle([x0 + 56 * S, ry + 6 * S, x0 + (W_DP - 60) * S, ry + 14 * S], radius=4 * S, fill=rgba(text, 0.14))
        d.rounded_rectangle([x0 + 56 * S, ry + 22 * S, x0 + (W_DP - 110) * S, ry + 28 * S], radius=3 * S, fill=rgba(text, 0.07))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))

screen(12, day, "DAY  pill FFDDB8 on container FFE9CF / active ink 331E00")
screen(12 + W_DP * S + 12, night, "NIGHT  pill 5C4000 on container 1F1912 / active ink FFDDB8")

out = os.path.join(ROOT, "download/ui2-step12-tabs-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

# ── گزارش کنتراست WCAG ──
print("\n== contrast report ==")
for name, t in (("DAY  ", day), ("NIGHT", night)):
    pill = t["actionBarTabLine"]
    act = t["actionBarTabActiveText"]
    unact = t["actionBarTabUnactiveText"]
    cont = t["actionBarDefault"]
    print(f"{name} activeText-on-pill   = {ratio(act, pill):5.2f}:1  (WCAG text AA >= 4.5)")
    print(f"{name} pill-on-container    = {ratio(pill, cont):5.2f}:1  (M3 tonal container — state carried by ink)")
    print(f"{name} unactiveText-on-hdr  = {ratio(unact, cont):5.2f}:1  (AA >= 4.5)")

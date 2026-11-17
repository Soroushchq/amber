#!/usr/bin/env python3
# UI2 قدم ۱۳ — پیش‌نمایش ردیف‌های چت Expressive (کارت رادیوس ۲۰ + پرس گرم)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند (نه کپی دستی).
# شعاع کارت = AmberTokens.SHAPE_CARD (۲۰dp) — همان چیزی که DialogCell.cornersRadius و
# RecyclerListView.setSelectorRadius از توکن می‌خوانند؛ حالت پرس = listSelectorSDK21
# (اکسنت×۸٪ روز / ×۱۰٪ شب). گزارش کنتراست WCAG هم چاپ می‌شود.
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

def with_alpha(c):
    """رنگ ARGB فایل تم با آلفای واقعی خودش — مثل ripple واقعی"""
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

night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 210
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)

CARD_R = 20 * S  # SHAPE_CARD — قدم ۱۳ (قبلاً ۸dp آپستریم)

def screen(x0, theme, caption):
    listbg = theme["windowBackgroundWhite"]
    container = theme["actionBarDefault"]
    press = theme["listSelectorSDK21"]     # کارت پرس — قدم ۱۳
    name = theme["chats_name"]
    msg = theme["chats_message"]
    timec = theme["chats_date"]
    badge = theme["chats_unreadCounter"]
    badge_txt = theme["chats_unreadCounterText"]
    # بدنه صفحه
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    # ناحیه هدر (کانتینر قدم ۱۱)
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 44 * S], radius=14 * S, fill=rgb(container))
    d.rectangle([x0, 6 + 22 * S, x0 + W_DP * S, 6 + 44 * S], fill=rgb(container))
    d.text((x0 + 14 * S, 16 * S), "AmberGram", font=f_word, fill=rgb(name))
    # ── ردیف‌های چت به‌صورت کارت (قدم ۱۳) ──
    rows = [("Sara", "سلام! فایل رو فرستادم", "14:02", 2),
            ("AmberGram", "کارت پرس گرم — اکسنت×۸٪", "12:40", 0),
            ("Dev Group", "مرج: پیل تب‌ها سبز شد", "10:15", 1)]
    for r, (nm, m, tm, unread) in enumerate(rows):
        ry = (52 + r * 50) * S
        pressed = r == 1
        if pressed:
            # ماسک رادیوس ۲۰ — همان که RecyclerListView.setSelectorRadius(SHAPE_CARD) می‌کشد
            d.rounded_rectangle([x0, ry, x0 + W_DP * S, ry + 48 * S], radius=CARD_R, fill=with_alpha(press))
        ax = x0 + 13 * S
        acy = ry + 24 * S
        d.ellipse([ax, acy - 17 * S, ax + 34 * S, acy + 17 * S], fill=rgba(name, 0.10 if not pressed else 0.14))
        d.text((ax + 9 * S, acy - 8 * S), nm[0], font=f_word, fill=rgb(name))
        d.text((x0 + 56 * S, ry + 7 * S), nm, font=f_small, fill=rgb(name))
        d.text((x0 + 56 * S, ry + 26 * S), m, font=f_small, fill=rgb(msg))
        d.text((x0 + (W_DP - 40) * S, ry + 9 * S), tm, font=f_small, fill=rgb(timec))
        if unread:
            bx = x0 + (W_DP - 26) * S
            d.rounded_rectangle([bx, ry + 28 * S, bx + 22 * S, ry + 42 * S], radius=7 * S, fill=rgb(badge))
            d.text((bx + 6 * S, ry + 30 * S), str(unread), font=f_small, fill=rgb(badge_txt))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))

screen(12, day, "DAY  card r=20 press C25E00@8% on paper FFF8F1 / rows standard spacing")
screen(12 + W_DP * S + 12, night, "NIGHT  card r=20 press F5A623@10% on 1C1710 / rows standard spacing")

out = os.path.join(ROOT, "download/ui2-step13-rows-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

# ── گزارش کنتراست WCAG ──
print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    listbg = t["windowBackgroundWhite"]
    print(f"{name_} name-on-list      = {ratio(t['chats_name'], listbg):5.2f}:1  (WCAG text AA >= 4.5)")
    print(f"{name_} message-on-list   = {ratio(t['chats_message'], listbg):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} time-on-list      = {ratio(t['chats_date'], listbg):5.2f}:1  (metadata, AA large >= 3)")
    print(f"{name_} pressCard-on-list = subtle state tint (alpha {((t['listSelectorSDK21'] >> 24) & 0xFF) / 255.0:.2f}) — state signal, not text bg")
    print(f"{name_} badgeText-on-badge= {ratio(t['chats_unreadCounterText'], t['chats_unreadCounter']):5.2f}:1  (AA >= 4.5)")

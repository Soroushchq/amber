#!/usr/bin/env python3
# UI2 قدم ۱۴ — پیش‌نمایش شمارنده/بج‌ها (accent/onAccent + رادیوس ۱۲ + بج بی‌صدای خوانا)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند (نه کپی دستی).
# شعاع بج = AmberTokens.SHAPE_BADGE (۱۲dp ≥ نصف ارتفاع ۲۰٫۶۶۶dp → پیل کامل؛
# اندروید در drawRoundRect شعاع بزرگ‌تر را clamp می‌کند — اینجا هم همین‌طور).
# حالت‌ها: شمارنده نخوانده، بج بی‌صدا، منشن بی‌صدا (سلول پوشه)، بج شبح تاپیک.
# گزارش کنتراست WCAG چاپ می‌شود.
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

night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 236
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_badge = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 11 * S)

BADGE_R = 12 * S  # SHAPE_BADGE — قدم ۱۴ (آپستریم ۱۱٫۵)

def pill(x0, y0, x1, y1, fill):
    """پیل کامل مثل drawRoundRect با شعاع clamp‌شده ۱۲dp"""
    r = min(BADGE_R, (y1 - y0) / 2)
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill)

def badge_text(cx, cy, txt, color):
    bb = d.textbbox((0, 0), txt, font=f_badge)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, font=f_badge, fill=rgb(color))

def screen(x0, theme, caption):
    listbg = theme["windowBackgroundWhite"]
    container = theme["actionBarDefault"]
    cnt = theme["chats_unreadCounter"]
    cnt_txt = theme["chats_unreadCounterText"]
    mut = theme["chats_unreadCounterMuted"]
    mut_txt = theme["chats_unreadCounterMutedText"]
    tp = theme["topics_unreadCounter"]
    tp_mut = theme["topics_unreadCounterMuted"]
    name = theme["chats_name"]
    msg = theme["chats_message"]
    timec = theme["chats_date"]
    # بدنه صفحه
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 44 * S], radius=14 * S, fill=rgb(container))
    d.rectangle([x0, 6 + 22 * S, x0 + W_DP * S, 6 + 44 * S], fill=rgb(container))
    d.text((x0 + 14 * S, 16 * S), "AmberGram", font=f_word, fill=rgb(name))

    def row(ry, nm, m, tm):
        d.text((x0 + 56 * S, ry + 7 * S), nm, font=f_small, fill=rgb(name))
        d.text((x0 + 56 * S, ry + 26 * S), m, font=f_small, fill=rgb(msg))
        d.text((x0 + (W_DP - 40) * S, ry + 9 * S), tm, font=f_small, fill=rgb(timec))

    # ── ردیف ۱: شمارنده نخوانده — accent/onAccent پیل کامل ──
    ry = 54 * S
    row(ry, "Sara", "شمارنده پرایمری — اکسنت", "14:02")
    bx, by = x0 + (W_DP - 28) * S, ry + 26 * S
    pill(bx, by, bx + 24 * S, by + 20 * S, rgb(cnt))
    badge_text(bx + 12 * S, by + 10 * S, "۲", cnt_txt)

    # ── ردیف ۲: بج بی‌صدا — کانتینر تونال + جوهر dim (قدم ۱۴؛ قبلاً نامرئی) ──
    ry = 100 * S
    row(ry, "News Feed", "کانال بی‌صدا — خوانا شد", "12:40")
    bx, by = x0 + (W_DP - 40) * S, ry + 26 * S
    pill(bx, by, bx + 36 * S, by + 20 * S, rgb(mut))
    badge_text(bx + 18 * S, by + 10 * S, "۹۹+", mut_txt)

    # ── ردیف ۳: منشن بی‌صدا در سلول پوشه (countGrayPaint + متن dim) ──
    ry = 146 * S
    row(ry, "P folder", "منشن بی‌صدا — پیل کامل", "10:15")
    bx, by = x0 + (W_DP - 28) * S, ry + 26 * S
    pill(bx, by, bx + 24 * S, by + 20 * S, rgb(mut))
    badge_text(bx + 12 * S, by + 10 * S, "@", mut_txt)

    # ── ردیف ۴: بج شبح تاپیک — پر α۴۰/۳۰٪ + متن هم‌رنگ (قدم ۱۴: متن dim) ──
    ry = 192 * S
    row(ry, "Forum", "شبح تاپیک: فعال/بی‌صدا", "09:30")
    bx, by = x0 + (W_DP - 76) * S, ry + 26 * S
    pill(bx, by, bx + 24 * S, by + 20 * S, rgba(tp, 40 / 255.0))
    badge_text(bx + 12 * S, by + 10 * S, "۳", tp)
    bx = x0 + (W_DP - 40) * S
    pill(bx, by, bx + 36 * S, by + 20 * S, rgba(tp_mut, 30 / 255.0))
    badge_text(bx + 18 * S, by + 10 * S, "۱۲", tp_mut)

    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))

screen(12, day, "DAY  badge r=12 (SHAPE_BADGE) accent C25E00/white + muted E9DFD0/7A6C5B")
screen(12 + W_DP * S + 12, night, "NIGHT  badge r=12 accent F5A623/3A2400 + muted 382C1C/A99C8B")

out = os.path.join(ROOT, "download/ui2-step14-counters-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

# ── گزارش کنتراست WCAG ──
print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    listbg = t["windowBackgroundWhite"]
    print(f"{name_} counterText-on-accent = {ratio(t['chats_unreadCounterText'], t['chats_unreadCounter']):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} mutedText-on-muted     = {ratio(t['chats_unreadCounterMutedText'], t['chats_unreadCounterMuted']):5.2f}:1  (pre-step14: {ratio(t['chats_unreadCounterText'], t['chats_unreadCounterMuted']):5.2f}:1 — invisible)")
    print(f"{name_} mutedFill-on-row       = {ratio(t['chats_unreadCounterMuted'], listbg):5.2f}:1  (tonal container, subtle by design)")
    print(f"{name_} topicGhostText-on-row  = {ratio(t['topics_unreadCounter'], listbg):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} topicMutedText-on-row  = {ratio(t['topics_unreadCounterMuted'], listbg):5.2f}:1  (pre-step14: {ratio(0xFFF3ECE2 if name_.startswith('DAY') else 0xFF241D14, listbg):5.2f}:1 — invisible)")

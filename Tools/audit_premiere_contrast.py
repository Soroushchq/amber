#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ممیزی کنتراست WCAG 2.x تم «شب اکران» — الگوی ممیزی‌های قدم‌های UI2
# همهٔ جفت‌های معنایی متن-روی-بستر در شب و روز + ترکیب چیپ سرویس
import math

def lum(c):
    r, g, b = [(c >> s) & 0xFF for s in (16, 8, 0)]
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else (((v / 255) + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def over(fg, bg, a):
    mix = lambda x, y: round(x * a + y * (1 - a))
    fr, fgc, fb = [(fg >> s) & 0xFF for s in (16, 8, 0)]
    br, bgc, bb = [(bg >> s) & 0xFF for s in (16, 8, 0)]
    return (0xFF << 24) | (mix(fr, br) << 16) | (mix(fgc, bgc) << 8) | mix(fb, bb)

def hexs(c): return f"#{c & 0xFFFFFF:06X}"

NIGHT = dict(
    BG=0x0C0A12, SURFACE=0x181326, HEADER=0x120F1B, IN=0x1F1930, OUT=0xE9A93A,
    TEXT=0xF7F0E1, DIM=0x9C92AF, TIME=0x8B80A0, ACCENT=0xF0B449, ACCENT_B=0xF7C96B,
    OUT_TEXT=0x2A1704, OUT_TIME=0x5C3D02, SENT_READ=0x4A3202, BADGE=0xD63852,
    BADGE_TEXT=0xFFFFFFFF, SVC=0xCBBDE0, NAV_PILL=0x6B4A08, NAV_TEXT=0xFFD37A,
)
DAY = dict(
    BG=0xF8F1E3, SURFACE=0xFFFBEF, HEADER=0xFFFBEF, IN=0xFFF3D9, OUT=0xF2CE7F,
    TEXT=0x2E2513, DIM=0x8A7B5C, TIME=0x94855E, ACCENT=0xA76F0F, ACCENT_B=0xC88A1E,
    OUT_TEXT=0x3A2A08, OUT_TIME=0x7A5A08, SENT_READ=0x8A5C06, BADGE=0xC42B4B,
    BADGE_TEXT=0xFFFFFFFF, SVC=0xFFFFFFFF, NAV_PILL=0xF2CE7F, NAV_TEXT=0x3A2A08,
)

def audit(mode, t):
    svc_bg = over(t["SURFACE"] if not mode == "day" else t["TEXT"], t["BG"], 0.70 if mode != "day" else 0.65)
    rows = [
        ("متن روی پس‌زمینه (windowBackgroundWhiteBlackText)", t["TEXT"], t["BG"], 4.5),
        ("متن روی حباب ورودی (chat_inText)", t["TEXT"], t["IN"], 4.5),
        ("متن روی حباب خروجی (chat_outText)", t["OUT_TEXT"], t["OUT"], 4.5),
        ("ساعت خروجی (chat_outTimeText)", t["OUT_TIME"], t["OUT"], 3.0),
        ("تیک خوانده‌شده (sentCheckRead)", t["SENT_READ"], t["OUT"], 3.0),
        ("متن ثانویه روی پس‌زمینه (GrayText)", t["DIM"], t["BG"], 3.0),
        ("متن ثانویه روی سطح (GrayText)", t["DIM"], t["SURFACE"], 3.0),
        ("زمان روی سطح (Time)", t["TIME"], t["SURFACE"], 3.0),
        ("متن بج روی فرش قرمز (unreadCounterText)", t["BADGE_TEXT"], t["BADGE"], 4.5),
        ("اکسنت به‌عنوان متن روی پس‌زمینه (subtitle/accent)", t["ACCENT"], t["BG"], 3.0),
        ("متن سرویس روی چیپ ترکیبی (serviceText)", t["SVC"], svc_bg, 4.5),
        ("متن روی هدر (actionBarDefaultTitle)", t["TEXT"], t["HEADER"], 4.5),
        ("متن روی پیل ناوبری (nav pill)", t["NAV_TEXT"], t["NAV_PILL"], 4.5),
    ]
    print(f"\n── {'شب اکران' if mode == 'night' else 'ماتینه'} ──")
    fails = 0
    for name, fg, bg, need in rows:
        r = ratio(fg, bg)
        mark = "✓" if r >= need else "✗ FAIL"
        if r < need: fails += 1
        print(f"  {r:5.2f}:1 (نیاز {need}) {mark}  {name}  [{hexs(fg)} روی {hexs(bg)}]")
    return fails

f1 = audit("night", NIGHT)
f2 = audit("day", DAY)
print(f"\nنتیجه: {f1 + f2} جفت ناکام" if f1 + f2 else "\nنتیجه: همهٔ جفت‌ها سالم — AA شبانه/روزانه ✓")
raise SystemExit(1 if (f1 + f2) else 0)

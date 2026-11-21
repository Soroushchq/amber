#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ممیزی کنتراست WCAG 2.x تم «دنیای ماریو» — الگوی ممیزی شب اکران
# همهٔ جفت‌های معنایی متن-روی-بستر در شب و روز + ترکیب چیپ سرویس

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
    BG=0x0B0F1E, SURFACE=0x111731, HEADER=0x0D1226, IN=0x141B3C, OUT=0x43B047,
    TEXT=0xF6F2E6, DIM=0x9BA7C8, TIME=0x7C88A8, ACCENT=0xFBD000, ACCENT_B=0xFFFFDF60,
    OUT_TEXT=0x0C2A12, OUT_TIME=0x123A1A, SENT_READ=0x0F3A1E, BADGE=0xDC2418,
    BADGE_TEXT=0xFFFFFFFF, SVC=0xF6F2E6, NAV_PILL=0x5E4A04, NAV_TEXT=0xFFFFDF60,
)
DAY = dict(
    BG=0xF2F7FF, SURFACE=0xF5F8FF, HEADER=0xE7F0FF, IN=0xFFFFFF, OUT=0xFFE382,
    TEXT=0x16243E, DIM=0x5C6E90, TIME=0x70819E, ACCENT=0xC6281C, ACCENT_B=0xE52521,
    OUT_TEXT=0x3D2E00, OUT_TIME=0x6E5605, SENT_READ=0x7A5E06, BADGE=0xC6281C,
    BADGE_TEXT=0xFFFFFFFF, SVC=0xFFFFFFFF, NAV_PILL=0xFFE382, NAV_TEXT=0x3D2E00,
)

def audit(mode, t):
    svc_bg = over(t["SURFACE"] if mode != "day" else t["TEXT"], t["BG"], 0.70 if mode != "day" else 0.65)
    rows = [
        ("متن روی پس‌زمینه (windowBackgroundWhiteBlackText)", t["TEXT"], t["BG"], 4.5),
        ("متن روی حباب ورودی (chat_inText)", t["TEXT"], t["IN"], 4.5),
        ("متن روی حباب خروجی (chat_outText)", t["OUT_TEXT"], t["OUT"], 4.5),
        ("ساعت خروجی (chat_outTimeText)", t["OUT_TIME"], t["OUT"], 3.0),
        ("تیک خوانده‌شده (sentCheckRead)", t["SENT_READ"], t["OUT"], 3.0),
        ("متن ثانویه روی پس‌زمینه (GrayText)", t["DIM"], t["BG"], 3.0),
        ("متن ثانویه روی سطح (GrayText)", t["DIM"], t["SURFACE"], 3.0),
        ("زمان روی سطح (Time)", t["TIME"], t["SURFACE"], 3.0),
        ("متن بج روی قرمز قارچ (unreadCounterText)", t["BADGE_TEXT"], t["BADGE"], 4.5),
        ("اکسنت به‌عنوان متن روی پس‌زمینه (subtitle/accent)", t["ACCENT"], t["BG"], 3.0),
        ("متن سرویس روی چیپ ترکیبی (serviceText)", t["SVC"], svc_bg, 4.5),
        ("متن روی هدر (actionBarDefaultTitle)", t["TEXT"], t["HEADER"], 4.5),
        ("متن روی پیل ناوبری (nav pill)", t["NAV_TEXT"], t["NAV_PILL"], 4.5),
    ]
    print(f"\n── {'دنیای زیرزمینی' if mode == 'night' else 'سرزمین ماریو'} ──")
    fails = 0
    for name, fg, bg, need in rows:
        r = ratio(fg, bg)
        mark = "OK" if r >= need else "FAIL"
        if r < need: fails += 1
        print(f"  {r:5.2f}:1 (نیاز {need}) {mark}  {name}  [{hexs(fg)} روی {hexs(bg)}]")
    return fails

f1 = audit("night", NIGHT)
f2 = audit("day", DAY)
print(f"\nنتیجه: {f1 + f2} جفت ناکام" if f1 + f2 else "\nنتیجه: همهٔ جفت‌ها سالم — AA شبانه/روزانه OK")
raise SystemExit(1 if (f1 + f2) else 0)

#!/usr/bin/env python3
# UI2 قدم ۳۱ — پیش‌نمایش سوییچ/چک‌باکس/رادیو M3
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند؛ همهٔ مختصات در فضای dp (ضرب در S فقط یک‌بار).
# کارهای این قدم (ممیزی کامل + رفع):
#   ۱) حلقهٔ رادیو غیرفعال (radioBackground/dialogRadioBackground) outline بود:
#      روز E9DFD0 روی کاغذ FFF8F1 فقط ۱٫۲۵:۱ و شب 382C1C روی وایپرپ ۱٫۳۱:۱ = حلقهٔ نامرئی
#      (آپستریم b3b3b3 ~۲٫۱) ← dim هم‌زبانهٔ checkboxSquareUnchecked (M3: مرز غیرفعال = onSurfaceVariant).
#   ۲) انگشت سوییچ خاموش شب نامرئی بود: TextCheckCell/NotificationsCheckCell انگشت را از
#      windowBackgroundWhite می‌گرفتند (شب 1C1710 روی ریل 382C1C = ۱٫۳۱:۱) و خانوادهٔ Blue از
#      onAccent (شب 3A2400 روی ریل تیره ~۱٫۰:۱) ← کلید مشترک switchTrackBlueThumb:
#      روز FFF8F1 (سفید M3-light) / شب dim (هندل روشن M3-dark — روی ریل ۵٫۰۶:۱)؛
#      دو Cell هم به این جفت وصل شدند (انگشت روشن = onAccent ثابت ماند).
#   ۳) چک‌باکس غیرفعال گرد و مربعی (checkboxDisabled / checkboxSquareDisabled /
#      dialogCheckboxSquareDisabled): بسترهٔ DCCFB8/outline با تیک onAccent نامرئی
#      (روز ۱٫۴۶/۱٫۲۵، شب ~۱٫۰) ← dim (تیک روی آن: روز ۴٫۸۴ / شب ۵٫۰۶ — آپستریم خاکستری میانی b0b9c2).
#   نکتهٔ ابزار: مولد فقط m.putهای تمام‌شده با ");" را ارزیابی می‌کند — کامنت انتهای خط کلید را بی‌صدا حذف می‌کرد.
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
S = 2  # px per dp

# مقادیر «قبل» برای ستون مقایسه (از پالت قبل از این قدم)
OLD = {
    "night": {"radioRing": 0xFF382C1C, "cbDisabled": 0xFF382C1C, "thumbSettings": 0xFF1C1710, "thumbBlue": 0xFF3A2400},
    "day":   {"radioRing": 0xFFE9DFD0, "cbDisabled": 0xFFDCCFB8, "thumbSettings": 0xFFFFF8F1, "thumbBlue": 0xFFFFFFFF},
}


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

W_DP, H_DP = 360, 320
STRIP = 30  # نوار کپشن پایین
img = Image.new("RGB", ((W_DP * 2 + 36) * S, (H_DP + 6) * S + STRIP), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_cap = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)


def lcol(theme):
    return rgb(theme["windowBackgroundWhiteGrayText"]) if "windowBackgroundWhiteGrayText" in theme else (150, 140, 128)


def draw_switch(px, py, checked, theme, thumb_off, thumb_on, lbl):
    """سوییچ TextCheckCell — عیناً طبق Switch.java: ریل ۳۱×۱۴ (r=۷)، هالهٔ ۱۰dp هم‌رنگ ریل، انگشت ۸dp"""
    x, y = px * S, py * S
    tr = theme["switchTrackChecked"] if checked else theme["switchTrack"]
    tx = x + 7 * S + 17 * S * (1 if checked else 0)
    ty = y + 7 * S
    d.rounded_rectangle([x, y, x + 31 * S, y + 14 * S], radius=7 * S, fill=rgb(tr))
    d.ellipse([tx - 10 * S, ty - 10 * S, tx + 10 * S, ty + 10 * S], fill=rgb(tr))
    th = thumb_on if checked else thumb_off
    d.ellipse([tx - 8 * S, ty - 8 * S, tx + 8 * S, ty + 8 * S], fill=rgb(th))
    if lbl:
        d.text((x + 36 * S, y + 3 * S), lbl, font=f_small, fill=lcol(theme))


def draw_radio(px, py, checked, theme):
    """رادیو RadioCells — طبق RadioButton.java: خاموش = حلقهٔ ۱dp، روشن = دایرهٔ توپر"""
    x, y = px * S, py * S
    size = 22
    rad = size / 2 - (1 + (1 if checked else 0)) * S
    cx, cy = x + size * S / 2, y + size * S / 2
    col = theme["radioBackgroundChecked"] if checked else theme["radioBackground"]
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=rgb(col))
    if not checked:
        inner = rad - 1 * S
        d.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], fill=rgb(theme["windowBackgroundWhite"]))


def draw_square(px, py, state, theme):
    """چک‌باکس مربعی CheckBoxSquare — ۱۸×۱۸ (r=۴): خاموش=حلقه، روشن=پر+تیک، غیرفعال=پر کم‌رنگ"""
    x, y = px * S, py * S
    fill = {"off": theme["checkboxSquareUnchecked"], "on": theme["checkboxSquareBackground"], "dis": theme["checkboxSquareDisabled"]}[state]
    tick = theme["checkboxSquareCheck"]
    d.rounded_rectangle([x, y, x + 18 * S, y + 18 * S], radius=4 * S, fill=rgb(fill))
    if state == "off":
        inner = 1.33 * S
        d.rounded_rectangle([x + inner, y + inner, x + 18 * S - inner, y + 18 * S - inner], radius=3 * S, fill=rgb(theme["windowBackgroundWhite"]))
    else:
        d.line([x + 3 * S, y + 9 * S, x + 7 * S, y + 13 * S], fill=rgb(tick), width=S)
        d.line([x + 7 * S, y + 13 * S, x + 14 * S, y + 6 * S], fill=rgb(tick), width=S)


def draw_tick_old(px, py, fill, tick, circle=False):
    """نسخهٔ «قبل»: بسترهٔ قدیمی + تیک onAccent"""
    x, y = px * S, py * S
    if circle:
        cx, cy, r = x + 9 * S, y + 9 * S, 9 * S
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(fill))
        d.line([cx - 4 * S, cy, cx - 1 * S, cy + 3 * S], fill=rgb(tick), width=S + 1)
        d.line([cx - 1 * S, cy + 3 * S, cx + 4 * S, cy - 3 * S], fill=rgb(tick), width=S + 1)
    else:
        d.rounded_rectangle([x, y, x + 18 * S, y + 18 * S], radius=4 * S, fill=rgb(fill))
        d.line([x + 3 * S, y + 9 * S, x + 7 * S, y + 13 * S], fill=rgb(tick), width=S)
        d.line([x + 7 * S, y + 13 * S, x + 14 * S, y + 6 * S], fill=rgb(tick), width=S)


def label(px, py, txt, theme):
    d.text((px * S, py * S), txt, font=f_small, fill=lcol(theme))


def section(x0, theme, mode, caption):
    """x0 در فضای dp"""
    bg = theme["windowBackgroundWhite"]
    d.rectangle([x0 * S, 0, (x0 + W_DP) * S, (H_DP + 6) * S], fill=rgb(bg))
    old = OLD[mode]
    rowy = 12

    # ── ردیف ۱: سوییچ خاموش تنظیمات — انگشت قبل (windowBackgroundWhite؛ شب تیره روی ریل تیره) / بعد ──
    label(x0 + 12, rowy, "سوییچ خاموش — تنظیمات (قبل ← بعد)", theme)
    draw_switch(x0 + 12, rowy + 14, False, theme, old["thumbSettings"], None, "قبل")
    draw_switch(x0 + 78, rowy + 14, False, theme, theme["switchTrackBlueThumb"], None, "بعد")
    rowy += 46

    # ── ردیف ۲: سوییچ روشن — اکسنت + onAccent (ثابت) ──
    label(x0 + 12, rowy, "سوییچ روشن — اکسنت + onAccent (ثابت)", theme)
    draw_switch(x0 + 12, rowy + 14, True, theme, None, theme["switchTrackBlueThumbChecked"], "")
    rowy += 46

    # ── ردیف ۳: سوییچ خاموش خانوادهٔ Blue (۸ سایت) — انگشت قبل onAccent / بعد ──
    label(x0 + 12, rowy, "سوییچ خاموش — خانوادهٔ Blue (قبل ← بعد)", theme)
    draw_switch(x0 + 12, rowy + 14, False, theme, old["thumbBlue"], None, "قبل")
    draw_switch(x0 + 78, rowy + 14, False, theme, theme["switchTrackBlueThumb"], None, "بعد")
    rowy += 46

    # ── ردیف ۴: رادیو — حلقهٔ خاموش قبل/بعد + روشن ──
    label(x0 + 12, rowy, "رادیو — حلقهٔ خاموش (قبل ← بعد) و روشن", theme)
    # قبل: حلقه با رنگ قدیمی outline
    x, y = (x0 + 12) * S, (rowy + 16) * S
    rad = (22 / 2 - 1) * S
    cx, cy = x + 22 * S / 2, y + 22 * S / 2
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=rgb(old["radioRing"]))
    d.ellipse([cx - rad + S, cy - rad + S, cx + rad - S, cy + rad - S], fill=rgb(bg))
    label(x0 + 38, rowy + 22, "قبل", theme)
    draw_radio(x0 + 66, rowy + 16, False, theme)
    label(x0 + 92, rowy + 22, "بعد", theme)
    draw_radio(x0 + 120, rowy + 16, True, theme)
    label(x0 + 146, rowy + 22, "روشن", theme)
    rowy += 50

    # ── ردیف ۵: چک‌باکس مربعی — خاموش/روشن/غیرفعال بعد + غیرفعال قبل ──
    label(x0 + 12, rowy, "چک‌باکس مربعی — خاموش، روشن، غیرفعال (قبل ← بعد)", theme)
    draw_square(x0 + 12, rowy + 14, "off", theme)
    draw_square(x0 + 40, rowy + 14, "on", theme)
    draw_square(x0 + 68, rowy + 14, "dis", theme)
    label(x0 + 90, rowy + 20, "بعد", theme)
    draw_tick_old(x0 + 116, rowy + 14, old["cbDisabled"], theme["checkboxSquareCheck"])
    label(x0 + 138, rowy + 20, "قبل", theme)
    rowy += 50

    # ── ردیف ۶: چک‌باکس گرد غیرفعال — بعد / قبل ──
    label(x0 + 12, rowy, "چک‌باکس گرد غیرفعال (قبل ← بعد)", theme)
    draw_tick_old(x0 + 12, rowy + 14, theme["checkboxDisabled"], theme["checkboxCheck"], circle=True)
    label(x0 + 34, rowy + 20, "بعد", theme)
    draw_tick_old(x0 + 62, rowy + 14, old["cbDisabled"], theme["checkboxCheck"], circle=True)
    label(x0 + 84, rowy + 20, "قبل", theme)

    d.text((x0 * S + 4, (H_DP + 6) * S + 8), caption, font=f_cap, fill=(140, 125, 105))


cap_day = "DAY  radio ring 1.25->4.84 | thumb-off = M3-light white | disabled tick ->4.84"
cap_night = "NIGHT  ring 1.31->6.63 | thumb-off ->5.06 M3-dark | disabled tick ->5.06"

section(12, day, "day", cap_day)
section(12 + W_DP + 12, night, "night", cap_night)

out = os.path.join(ROOT, "download/ui2-step31-switches-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report (old → new) ==")
for name_, t, old in (("DAY  ", day, OLD["day"]), ("NIGHT", night, OLD["night"])):
    bgw = t["windowBackgroundWhite"]
    track = t["switchTrack"]
    rows = [
        ("radio ring OFF (old=outline)", t["radioBackground"], bgw, old["radioRing"]),
        ("radio checked fill vs bg", t["radioBackgroundChecked"], bgw, None),
        ("switch thumb OFF settings (old=winWhite)", t["switchTrackBlueThumb"], track, old["thumbSettings"]),
        ("switch thumb OFF blue family (old=onAccent)", t["switchTrackBlueThumb"], track, old["thumbBlue"]),
        ("switch thumb ON (onAccent, unchanged)", t["switchTrackBlueThumbChecked"], t["switchTrackChecked"], None),
        ("checked track vs bg (informational)", t["switchTrackChecked"], bgw, None),
        ("track vs bg (M3-subtle, informational)", track, bgw, None),
        ("round cb disabled fill + check (old fill)", t["checkboxCheck"], t["checkboxDisabled"], ("oldfill_check", old["cbDisabled"])),
        ("square cb disabled fill + tick (old fill)", t["checkboxSquareCheck"], t["checkboxSquareDisabled"], ("oldfill_check", old["cbDisabled"])),
        ("square cb unchecked border", t["checkboxSquareUnchecked"], bgw, None),
    ]
    for lbl, fg, bgc, oldc in rows:
        newr = ratio(fg, bgc)
        if isinstance(oldc, tuple):  # قدیم = همان رنگ تیک روی بستر قدیمی
            print(f"{name_} {lbl:44s} old {ratio(fg, oldc[1]):5.2f}:1 → new {newr:5.2f}:1")
        elif oldc is not None:
            print(f"{name_} {lbl:44s} old {ratio(oldc, bgc):5.2f}:1 → new {newr:5.2f}:1")
        else:
            print(f"{name_} {lbl:44s} {newr:5.2f}:1")

#!/usr/bin/env python3
# UI2 قدم ۱۹ — پیش‌نمایش پس‌زمینه صفحه چت (وایپرپ گرادیانی + مسیر کم‌حجم)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# وایپرپ: ۴ توقف گرادیان متحرک MotionBackgroundDrawable از توکن‌ها (از فاز صفر سالم) —
#   روز: FFF6EA→FBEEDC→FFF8F1→FFE9CF   شب: 17130E→1C1710→12100B→241D14
# کارهای این قدم:
#   ۱) chat_wallpaper_gradient_rotation=45 — کلید پنجم وایپرپ حالا صریح در attheme (کامل بودن ۵/۵)
#   ۲) chat_compact_background — بوم حالت کم‌حجم از fallback (windowBackgroundWhite) به پایهٔ وایپرپ تخت
#   ۳) chat_compact_backgroundGradient — پردهٔ محو گرم
#   ۴) chat_compact_actionBackground/Text/Icon — قرص سرویس روی بوم کم‌حجم؛ آپستریم ۵٪ مشکی + متن مشکی
#      روی بوم تیرهٔ شب عملاً نامرئی بود ← پیل تونال (شب جوهر روشن×۱۰٪) + متن جوهر
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


def composite(fg, bg):
    """ColorUtils.compositeColors (SRC_OVER)"""
    fa = (fg >> 24) & 255
    if fa == 255:
        return fg & 0xFFFFFF
    ba = (bg >> 24) & 255 if len(bin(bg)) > 10 else 255
    def ch(f, b):
        return int(round((f * fa + b * (255 - fa)) / 255.0))
    r1, g1, b1 = rgb(fg)
    r2, g2, b2 = rgb(bg)
    return (ch(r1, r2) << 16) | (ch(g1, g2) << 8) | ch(b1, b2)


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 240
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)


def grad4(x0, colors, y0, y1, w):
    """نمونهٔ گرادیان ۴رنگ مثل MotionBackgroundDrawable (خطی ساده برای پیش‌نمایش)"""
    n = len(colors)
    for yy in range((y1 - y0) * S):
        t = yy / float((y1 - y0) * S - 1)
        seg = min(int(t * (n - 1)), n - 2)
        lt = t * (n - 1) - seg
        c1, c2 = colors[seg], colors[seg + 1]
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * lt) for i in range(3))
        d.line([x0, y0 * S + yy, x0 + w * S, y0 * S + yy], fill=col)


def screen(x0, theme, caption, dark):
    wp = [theme["chat_wallpaper"], theme["chat_wallpaper_gradient_to"],
          theme["key_chat_wallpaper_gradient_to2"], theme["key_chat_wallpaper_gradient_to3"]]
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(theme["windowBackgroundWhite"]))
    # بوم وایپرپ گرادیانی
    grad4(x0 + 12, [rgb(c) for c in wp], 12, 100, W_DP - 24)
    d.text((x0 + 20 * S, 16 * S), "wallpaper gradient (4 phases)", font=f_small,
           fill=rgb(theme["chat_serviceText"]))
    # مسیر کم‌حجم: بوم تخت + قرص سرویس کامپوزیت‌شده
    comp_bg = theme["chat_compact_background"]
    pill = composite(theme["chat_compact_actionBackground"], comp_bg)
    d.rectangle([x0 + 12 * S, 112 * S, x0 + (W_DP - 12) * S, 170 * S], fill=rgb(comp_bg))
    d.text((x0 + 20 * S, 116 * S), "compact flat canvas", font=f_small, fill=rgb(theme["chat_compact_actionIcon"]))
    # قرص تاریخ سرویس روی بوم کم‌حجم
    px, py, pw, ph = 30, 132, 120, 26
    d.rounded_rectangle([x0 + px * S, py * S, x0 + (px + pw) * S, (py + ph) * S], radius=13 * S, fill=rgb(pill))
    d.text((x0 + (px + 28) * S, (py + 6) * S), "July 17  12:40", font=f_small, fill=rgb(theme["chat_compact_actionText"]))
    d.text((x0 + (px + pw + 12) * S, (py + 6) * S), "pill", font=f_small, fill=rgb(theme["chat_compact_actionIcon"]))
    # نمودار توقف‌های گرادیان
    for i, c in enumerate(wp):
        swx = x0 + (12 + i * ((W_DP - 24) // 4)) * S
        d.rounded_rectangle([swx, 178 * S, swx + 20 * S, 198 * S], radius=4 * S, fill=rgb(c))
        d.text((swx, 200 * S), f"#{c:06X}"[-6:], font=f_small, fill=rgb(theme["windowBackgroundWhiteGrayText"]))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


screen(12, day, "DAY  wallpaper 4 phases warm cream; compact FFF6EA + ink-pill", False)
screen(12 + W_DP * S + 12, night, "NIGHT  phases warm dark; compact 17130E + tonal pill (was invisible)", True)

out = os.path.join(ROOT, "download/ui2-step19-wallpaper-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    comp_bg = t["chat_compact_background"]
    pill = composite(t["chat_compact_actionBackground"], comp_bg)
    print(f"{name_} compact canvas      = #{comp_bg:06X}   action pill = #{pill:06X}")
    print(f"{name_} pill text ink       = {ratio(t['chat_compact_actionText'], pill):5.2f}:1  (AA >= 4.5)  [was black-on-dark night]")
    print(f"{name_} pill icon dim        = {ratio(t['chat_compact_actionIcon'], pill):5.2f}:1  (icons >= 3.0)")
    print(f"{name_} pill vs canvas lift = {ratio(pill, comp_bg):5.2f}:1  (container signal)")
    avg = (t["chat_wallpaper"] & 0xFFFFFF)
    print(f"{name_} wallpaper base      = #{avg:06X}  (motion 4-phase: all token-driven)")
    print(f"{name_} inBubble on canvas  = {ratio(t['chat_inBubble'], comp_bg):5.2f}:1  (lift signal — step 20 refines)")

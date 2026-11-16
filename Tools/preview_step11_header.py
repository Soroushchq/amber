#!/usr/bin/env python3
# UI2 قدم ۱۱ — پیش‌نمایش هدر لیست چت اکسپرسیو (روز/شب)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند (نه کپی دستی).
# ناحیه هدر = خروجی actionBarDefaultPaint جدید (key_actionBarDefault)؛
# تب‌ها فقط برای نمایش جایگاه فعلی هستند (استایل پیل = قدم ۱۲).
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

night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 240
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)

def plane(cx, cy, s, fill):
    d.polygon([(cx - s, cy - s * .62), (cx + s, cy + s * .08), (cx - s, cy + s * .62), (cx - s * .4, cy)], fill=fill)
    d.polygon([(cx - s, cy - s * .62), (cx - s * .4, cy), (cx - s, cy + s * .62)], fill=fill)

def screen(x0, theme, caption, night_mode):
    listbg = theme["windowBackgroundWhite"]
    container = theme["actionBarDefault"]
    text = theme["actionBarDefaultTitle"]
    dim = theme["actionBarDefaultIcon"]
    hint = theme["windowBackgroundWhiteHintText"]
    # بدنه صفحه
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    # ── ناحیه هدر رنگ‌شده (actionBarDefaultPaint قدم ۱۱) ──
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + 104 * S], radius=14 * S, fill=rgb(container))
    d.rectangle([x0, 6 + 14 * S, x0 + W_DP * S, 6 + 104 * S], fill=rgb(container))
    # نوار وضعیت (ساعت + باتری ساده)
    d.text((x0 + 14 * S, 8), "12:45", font=f_small, fill=rgba(dim, 0.9))
    d.rounded_rectangle([x0 + (W_DP - 22) * S, 10, x0 + (W_DP - 10) * S, 20], radius=2 * S, outline=rgba(dim, 0.8), width=S)
    # لوگو: هواپیما + کلمه‌نگاره — تینت MULTIPLY (روز=جوهری از fallback، شب=مقدار صریح فایل)
    if night_mode:
        tint = theme["telegram_color_dialogsLogo"]
    else:
        tint = theme["windowBackgroundWhiteBlackText"]  # fallbackKeys روز
    plane(x0 + 20 * S, 30 * S, 7 * S, rgb(tint))
    d.text((x0 + 30 * S, 30 * S - 12 * S), "AmberGram", font=f_word, fill=rgb(tint))
    # آیکون‌های هدر — muted (dim) قدم ۱۱
    for i in range(3):
        cx = x0 + (W_DP - 18 - i * 24) * S
        cy = 30 * S
        d.ellipse([cx - 8 * S, cy - 8 * S, cx + 8 * S, cy + 8 * S], outline=rgba(dim, 0.18), width=S)
        if i == 0:  # ذره‌بین
            d.ellipse([cx - 5 * S, cy - 5 * S, cx + 1 * S, cy + 1 * S], outline=rgb(dim), width=S)
            d.line([cx + 1 * S, cy + 1 * S, cx + 5 * S, cy + 5 * S], fill=rgb(dim), width=S)
        elif i == 1:  # قفل
            d.rounded_rectangle([cx - 4 * S, cy - 1 * S, cx + 4 * S, cy + 5 * S], radius=2 * S, outline=rgb(dim), width=S)
            d.arc([cx - 3 * S, cy - 6 * S, cx + 3 * S, cy], 180, 360, fill=rgb(dim), width=S)
        else:  # سپر
            d.polygon([(cx, cy - 6 * S), (cx + 5 * S, cy - 4 * S), (cx + 4 * S, cy + 3 * S), (cx, cy + 6 * S), (cx - 4 * S, cy + 3 * S), (cx - 5 * S, cy - 4 * S)], outline=rgb(dim), width=S)
    # باند فیلد جستجو (بخش رنگ‌شده ناحیه؛ فیلد در حالت عادی پنهان است)
    d.rounded_rectangle([x0 + 12 * S, 56 * S, x0 + (W_DP - 12) * S, 84 * S], radius=14 * S,
                        fill=rgba(text, 0.04), outline=rgba(dim, 0.35), width=S)
    d.ellipse([x0 + 20 * S, 62 * S, x0 + 32 * S, 74 * S], outline=rgb(dim), width=S)
    d.line([x0 + 30 * S, 72 * S, x0 + 34 * S, 76 * S], fill=rgb(dim), width=S)
    d.text((x0 + 42 * S, 63 * S), "Search", font=f_small, fill=rgb(hint))
    # ── نوار تب‌ها: پیل شیشه‌ای شناور موجود (استایلش = قدم ۱۲) ──
    tabs_tint = theme["glass_targetMainTabs"]
    ty = 104 * S
    d.rounded_rectangle([x0 + 4 * S, ty + 7 * S, x0 + (W_DP - 4) * S, ty + 43 * S], radius=18 * S,
                        fill=rgba(tabs_tint, 0.88), outline=rgba(dim, 0.16), width=S)
    # پیل فعال (فعلاً glass_tabSelected موجود؛ هدف قدم ۱۲ = FFDDB8)
    act = theme["glass_tabSelected"]
    act_txt = theme["glass_tabSelectedText"]
    d.rounded_rectangle([x0 + (W_DP - 74) * S, ty + 11 * S, x0 + (W_DP - 12) * S, ty + 39 * S], radius=14 * S, fill=rgba(act, 0.95))
    d.text((x0 + (W_DP - 62) * S, ty + 17 * S), "All", font=f_small, fill=rgb(act_txt))
    for i, lbl in enumerate(["Personal", "Groups"]):
        px = x0 + (W_DP - 140 - i * 62) * S
        d.rounded_rectangle([px, ty + 11 * S, px + 56 * S, ty + 39 * S], radius=14 * S, fill=rgba(text, 0.05))
        d.text((px + 10 * S, ty + 17 * S), lbl, font=f_small, fill=rgb(dim))
    # ردیف‌های لیست (رنگ فعلی — کارت‌ها = قدم ۱۳)
    for r in range(2):
        ry = (150 + r * 44) * S
        d.ellipse([x0 + 12 * S, ry, x0 + 12 * S + 36 * S, ry + 36 * S], fill=rgba(text, 0.10))
        d.rounded_rectangle([x0 + 58 * S, ry + 6 * S, x0 + (W_DP - 60) * S, ry + 14 * S], radius=4 * S, fill=rgba(text, 0.14))
        d.rounded_rectangle([x0 + 58 * S, ry + 22 * S, x0 + (W_DP - 110) * S, ry + 28 * S], radius=3 * S, fill=rgba(text, 0.07))
        d.ellipse([x0 + (W_DP - 40) * S, ry + 4 * S, x0 + (W_DP - 26) * S, ry + 18 * S], fill=rgb(theme["chats_unreadCounter"]))
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))

screen(12, day, "DAY  container FFE9CF / list FFF8F1 / icons muted 7A6C5B", False)
screen(12 + W_DP * S + 12, night, "NIGHT  container 1F1912 / list 1C1710 / icons muted A99C8B", True)

out = os.path.join(ROOT, "download/ui2-step11-header-preview.png")
img.save(out)
print("saved", out)
def night_mode_true(t):
    return "telegram_color_dialogsLogo" in t
for name, t in (("DAY  ", day), ("NIGHT", night)):
    print(name, "container=", "#%06X" % (t["actionBarDefault"] & 0xFFFFFF),
          "listBg=", "#%06X" % (t["windowBackgroundWhite"] & 0xFFFFFF),
          "icon=", "#%06X" % (t["actionBarDefaultIcon"] & 0xFFFFFF),
          "logoTint=", ("#%06X" % (t["telegram_color_dialogsLogo"] & 0xFFFFFF)) if night_mode_true(t) else "ink-fallback")

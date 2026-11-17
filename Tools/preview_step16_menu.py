#!/usr/bin/env python3
# UI2 قدم ۱۶ — پیش‌نمایش منوی اصلی/دراور (کارت ItemOptions با SHAPE_MENU=۲۰dp)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کانتینر: همان ۹-پیچ popup_fixed_alert4 بازتولیدشده (شعاع ۲۰dp) با تینت MULTIPLY
# از actionBarDefaultSubmenuBackground — دقیقاً مثل مسیر ActionBarPopupWindowLayout.
# روز قبلاً سفید هاردکد بود (نشتی رنگ) ← DAY_SURFACE گرم؛ شب NIGHT_SURFACE حفظ.
# ردیف‌ها: متن ink / آیکون dim / آیتم قرمز / gap دیوایدر — همان کلیدهای پالت.
# قانون گردش تو‌در‌تو M3: کانتینر ۲۰ − پدینگ ۸ = ripple ردیف ۱۲ (SHAPE_MENU_ROW).
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
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


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))


def load_popup_patch():
    """۹-پیچ واقعی بازتولیدشده (بدون بوردر راهنما)"""
    arr = Image.open(os.path.join(RES, "drawable-xxhdpi/popup_fixed_alert4.9.png")).convert("RGBA")
    w, h = arr.size
    return arr.crop((1, 1, w - 1, h - 1))


PATCH = load_popup_patch()


def tinted_patch(color, w_dp, h_dp):
    """تینت MULTIPLY مثل ActionBarPopupWindowLayout.setBackgroundColor + کشش"""
    patch = PATCH.resize((w_dp * S // 3, h_dp * S // 3), Image.LANCZOS)  # xxhdpi→px
    patch = patch.resize((w_dp * S, h_dp * S), Image.LANCZOS)
    arr = __import__("numpy").array(patch).astype(np.float32) if False else None
    import numpy as np
    a = np.array(patch).astype(np.float32)
    r, g, b = rgb(color)
    a[..., 0] = a[..., 0] * r / 255.0
    a[..., 1] = a[..., 1] * g / 255.0
    a[..., 2] = a[..., 2] * b / 255.0
    return Image.fromarray(a.astype("uint8"), "RGBA")


W_DP, H_DP = 360, 210
CARD_W, CARD_H = 168, 150
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_word = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui.ttf"), 17 * S)
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 13 * S)


def icon_square(d0, x0, y0, size, color):
    d0.rounded_rectangle([x0, y0, x0 + size, y0 + size], radius=3 * S, fill=rgb(color))


def screen(x0, theme, caption):
    listbg = theme["windowBackgroundWhite"]
    d.rounded_rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], radius=14 * S, fill=rgb(listbg))
    # دو ردیف چت شبیه‌سازی‌شده زیر منو
    for i, dy in enumerate((56, 116)):
        avatar_bg = theme["chats_unreadCounter"]
        d.ellipse([x0 + 14 * S, 6 + dy * S // 1 - 10 * S, x0 + 14 * S + 36 * S, 6 + dy * S // 1 + 26 * S], fill=rgb(avatar_bg))
    # کارت منو — ۹-پیچ تینت‌شده
    card_x = x0 + (W_DP - CARD_W) * S - 10 * S
    card_y = 14 * S
    card_img = tinted_patch(theme["actionBarDefaultSubmenuBackground"], CARD_W, CARD_H)
    img.paste(card_img, (card_x, card_y), card_img)
    # ردیف‌ها داخل کارت (پدینگ ۸dp — قانون گردش تو‌در‌تو: ripple 12 = 20-8)
    tx = card_x + 40 * S
    rows = [
        ("SwitchTheme", theme["actionBarDefaultSubmenuItem"], theme["actionBarDefaultSubmenuItemIcon"], False),
        ("NewGroup", theme["actionBarDefaultSubmenuItem"], theme["actionBarDefaultSubmenuItemIcon"], False),
        ("SavedMessages", theme["actionBarDefaultSubmenuItem"], theme["actionBarDefaultSubmenuItemIcon"], False),
        ("DeleteAccount", theme["text_RedRegular"], theme["text_RedRegular"], True),
    ]
    ry = card_y + 14 * S
    for i, (label, tcol, icol, is_red) in enumerate(rows):
        icon_square(d, card_x + 14 * S, ry + 3 * S, 13 * S, icol)
        d.text((tx, ry + 1 * S), label, font=f_row, fill=rgb(tcol))
        ry += 30 * S
        if i == 2:  # gap دیوایدر
            d.rectangle([card_x + 10 * S, ry, card_x + CARD_W * S - 10 * S, ry + 1 * S],
                        fill=rgb(theme["actionBarDefaultSubmenuSeparator"]))
            ry += 8 * S
    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


screen(12, day, "DAY  card r=20 bg F3ECE2 (was white), ripple 12=20-8")
screen(12 + W_DP * S + 12, night, "NIGHT  card r=20 bg 241D14, ripple 12")

out = os.path.join(ROOT, "download/ui2-step16-menu-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    bg = t["actionBarDefaultSubmenuBackground"]
    print(f"{name_} menuBg               = #{bg:06X}")
    print(f"{name_} text-on-menuBg       = {ratio(t['actionBarDefaultSubmenuItem'], bg):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} icon-on-menuBg (dim) = {ratio(t['actionBarDefaultSubmenuItemIcon'], bg):5.2f}:1  (icons >= 3.0)")
    print(f"{name_} red-on-menuBg        = {ratio(t['text_RedRegular'], bg):5.2f}:1  (AA >= 4.5)")
    print(f"{name_} menuBg-on-list       = {ratio(bg, t['windowBackgroundWhite']):5.2f}:1  (surface lift — signal)")

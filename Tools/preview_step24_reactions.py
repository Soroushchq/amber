#!/usr/bin/env python3
# UI2 قدم ۲۴ — پیش‌نمایش ری‌اکشن‌ها (پیل ری‌اکشن و شمارنده)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم:
#   ۱) دو کلید سرویس ری‌اکشن (chat_reactionServiceButton{Background,Text}Selected — چیپ ری‌اکشن
#      انتخاب‌شدهٔ روی چیپ سرویس/تاریخ ChatActionCell) در پالت نبودند:
#      شب F97316 نارنجی خارج‌ازتوکن (بازماندهٔ مولد کهربایی قدیمی) و روز اصلاً کلید نداشت
#      (پیش‌فرض سفید/مشکی آپستریم) ← قرص اکسنت + onAccent (هم‌الگوی چیپ انتخاب‌شدهٔ معمولی).
#   ۲) باگ واقعی پیل ری‌اکشن پولی (ستاره‌ها) در ReactionsLayoutInBubble — رنگ‌های هاردکد E8AB02/سفید:
#      انتخاب‌شده: سفید روی E8AB02 در هر دو حالت ۲٫۰۵:۱ ← قرص اکسنت + onAccent (۴٫۲۹ روز / ۷٫۲۳ شب)
#      غیرانتخاب‌شده: متن E8AB02 روی حباب خروجی روز فقط ۱٫۵۹:۱ ← اکسنت (۳٫۳۳ روز / ۴٫۷۳ شب)
#      بسترهٔ ۲۵٪ اکسنت هم‌وزن 0x40 آپستریم؛ سرویس از کلید پالتی chat_serviceText به‌جای سفید هاردکد.
#   ۳) شمارندهٔ چیپ همان متن پیل است (textColor) — با این قدم کل ۱۲ کلید ری‌اکشن پالتی شدند.
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
S = 2  # px per dp

BUBBLE_R = 26  # AmberTokens.SHAPE_BUBBLE


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
    r1, g1, b1 = rgb(fg)
    r2, g2, b2 = rgb(bg)
    ch = lambda f, b: int(round((f * fa + b * (255 - fa)) / 255.0))
    return (ch(r1, r2) << 16) | (ch(g1, g2) << 8) | ch(b1, b2)


def alpha_of(c, k):
    a = int(round(((c >> 24) & 255) * k))
    return (a << 24) | (c & 0xFFFFFF)


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 300
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)


def star(cx_px, cy_px, r_px, color):
    """ستارهٔ ۵پر — گلیف پیل پولی"""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r_px if i % 2 == 0 else r_px * 0.42
        pts.append((cx_px + rr * math.cos(ang), cy_px + rr * math.sin(ang)))
    d.polygon(pts, fill=rgb(color))


def chip(x_px, ydp, wdp, hdp, bg, fg, label, counter, emoji=None):
    """پیل ری‌اکشن: گلیف + شمارندهٔ متن (متن = textColor همان پیل)"""
    ys = ydp * S
    d.rounded_rectangle([x_px, ys, x_px + wdp * S, ys + hdp * S],
                        radius=hdp * S // 2, fill=rgb(bg))
    tx = x_px + 10 * S
    if emoji:
        d.ellipse([tx, ys + 5 * S, tx + 13 * S, ys + 18 * S], fill=rgb(fg))
        tx += 18 * S
        d.text((tx, ys + 5 * S), label, font=f_small, fill=rgb(fg))
        return
    d.text((tx, ys + 5 * S), label, font=f_small, fill=rgb(fg))
    tx += int(d.textlength(label, font=f_small))
    d.text((tx + 5 * S, ys + 5 * S), counter, font=f_small, fill=rgb(fg))


def draw_section(x0, theme, caption):
    margin = 12 * S
    canvas = theme["chat_wallpaper"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + (H_DP - 56) * S], fill=rgb(canvas))
    d.text((x0 + 12 * S, 10 * S), "reactions — pill + counter (step 24)",
           font=f_small, fill=rgb(theme["chat_serviceText"]))

    xr = x0 + W_DP * S - margin

    # ── چیپ سرویس/تاریخ (ChatActionCell) با ری‌اکشن انتخاب‌شدهٔ زیر آن ──
    # والد ChatActionCell: serviceTextColor/serviceBackgroundColor از دو کلید جدید قدم ۲۴
    pill = theme["chat_serviceBackground"]
    sw, sh = 130, 26
    sx0 = x0 + margin + 30 * S
    d.rounded_rectangle([sx0, 30 * S, sx0 + sw * S, 30 * S + sh * S],
                        radius=sh * S // 2, fill=rgb(pill))
    d.text((sx0 + 40 * S, (30 + 7) * S), "March 14", font=f_small,
           fill=rgb(theme["chat_serviceText"]))
    svc_bg = theme["chat_reactionServiceButtonBackgroundSelected"]
    svc_tx = theme["chat_reactionServiceButtonTextSelected"]
    chip(sx0 + 34 * S, 18, 62, 24, svc_bg, svc_tx, "8", "", emoji=True)

    # ── حباب خروجی با پیل پولی (ستاره‌ها) انتخاب‌شده + غیرانتخاب‌شده ──
    out = theme["chat_outBubble"]
    by, bw, bh = 72, 300, 88
    d.rounded_rectangle([xr - bw * S, by * S, xr, (by + bh) * S],
                        radius=BUBBLE_R * S, fill=rgb(out))
    d.rectangle([xr - BUBBLE_R * S, (by + bh) * S - BUBBLE_R * S, xr, (by + bh) * S], fill=rgb(out))
    d.polygon([(xr, (by + bh - 14) * S), (xr + 7 * S, (by + bh) * S), (xr - 8 * S, (by + bh) * S)],
              fill=rgb(out))
    d.text((xr - (bw - 14) * S, (by + 10) * S), "thanks for the stars!",
           font=f_row, fill=rgb(theme["chat_messageTextOut"]))
    # پیل پولی انتخاب‌شده: اکسنت جامد + onAccent (قبلاً E8AB02 + سفید ۲٫۰۵:۱)
    paid_bg = theme["chat_outReactionButtonBackground"]
    paid_tx = theme["chat_outReactionButtonTextSelected"]
    cy = by + 30
    chip(xr - 112 * S, cy, 100, 24, paid_bg, paid_tx, "", "5", emoji=False)
    star(xr - 112 * S + 14 * S, (cy + 12) * S, 7 * S, paid_tx)
    d.text((xr - 112 * S + 24 * S, (cy + 6) * S), "stars 5", font=f_small, fill=rgb(paid_tx))
    # پیل پولی غیرانتخاب‌شده: بسترهٔ ۲۵٪ اکسنت + متن اکسنت (قبلاً متن E8AB02 روی حباب روز ۱٫۵۹:۱)
    upaid_tx = theme["chat_outReactionButtonText"]
    upaid_bg = composite(alpha_of(paid_bg, 0.25), out)
    chip(xr - 104 * S, cy + 30, 92, 24, upaid_bg, upaid_tx, "", "2", emoji=False)
    star(xr - 104 * S + 14 * S, (cy + 42) * S, 7 * S, upaid_tx)
    d.text((xr - 104 * S + 24 * S, (cy + 36) * S), "stars 2", font=f_small, fill=rgb(upaid_tx))

    # ── چیپ معمولی روی حباب ورودی + شمارنده (textColor مشترک) ──
    in_b = theme["chat_inBubble"]
    iy = by + 62
    d.rounded_rectangle([x0 + margin, iy * S, x0 + margin + 120 * S, (iy + 44) * S],
                        radius=BUBBLE_R * S, fill=rgb(in_b))
    d.rectangle([x0 + margin, (iy + 44) * S - BUBBLE_R * S, x0 + margin + BUBBLE_R * S, (iy + 44) * S],
                fill=rgb(in_b))
    d.text((x0 + margin + 10 * S, (iy + 8) * S), "nice!", font=f_row,
           fill=rgb(theme["chat_messageTextIn"]))
    acc = theme["chat_inReactionButtonBackground"]
    u_bg = composite(alpha_of(acc, 0.156), in_b)
    chip(x0 + margin + 10 * S, iy + 52, 62, 22, u_bg, theme["chat_inReactionButtonText"],
         "3", "", emoji=True)
    chip(x0 + margin + 80 * S, iy + 52, 66, 22, acc, theme["chat_inReactionButtonTextSelected"],
         "12", "", emoji=True)

    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


draw_section(12, day, "DAY  service+paid pill accent 4.29 (was 2.05) / unselected 3.33 (was 1.59)")
draw_section(12 + W_DP * S + 12, night, "NIGHT  service pill was orange F97316; paid 7.23 onAccent")

out = os.path.join(ROOT, "download/ui2-step24-reactions-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    out_b = t["chat_outBubble"]
    in_b = t["chat_inBubble"]
    acc = t["chat_inReactionButtonBackground"]
    u_bg = composite(alpha_of(acc, 0.156), in_b)
    upaid_bg = composite(alpha_of(t["chat_outReactionButtonBackground"], 0.25), out_b)
    rows = [
        ("service chosen text (NEW key, onAccent)", t["chat_reactionServiceButtonTextSelected"], t["chat_reactionServiceButtonBackgroundSelected"]),
        ("service chosen pill bg vs wallpaper", t["chat_reactionServiceButtonBackgroundSelected"], t["chat_wallpaper"]),
        ("paid chosen text (was white 2.05)", t["chat_outReactionButtonTextSelected"], t["chat_outReactionButtonBackground"]),
        ("paid unselected text (was E8AB02 1.59 day)", t["chat_outReactionButtonText"], out_b),
        ("paid unselected bg (x0.25) vs bubble", upaid_bg, out_b),
        ("chip unselected text on tint", t["chat_inReactionButtonText"], u_bg),
        ("counter = chip text (selected)", t["chat_inReactionButtonTextSelected"], acc),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:44s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")

#!/usr/bin/env python3
# UI2 قدم ۲۱ — پیش‌نمایش حباب خروجی (Expressive)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم:
#   ۱) رنگ‌های اصلی حباب خروجی از فاز صفر توکنی بودند و تأیید شد
#      (chat_outBubble = FFDDB8 روز / 5C4000 شب؛ متن 331E00 / FFDDB8 = primary-container).
#   ۲) رفع هم‌الگوی قدم ۲۰ در سمت خروجی: بسترهٔ چیپ ری‌اکشن خروجی آپستریم «جامد» است و
#      مصرف‌کننده‌ها خودشان آلفا می‌سازند (×۰٫۱۵۶ / آلفا۳۸ / blend) — chat_outReactionButtonBackground
#      ← اکسنت جامد؛ متن چیپ انتخاب‌شده از اکسنت (روی اکسنت نامرئی!) ← onAccent.
#   ۳) تیک خوانده‌شدهٔ روز از accentBright (۲٫۰۶:۱ روی حباب) ← کهربای برشته 9C5200 (۴٫۵۰:۱).
#   ۴) لینک داخل حباب خروجی از آبی آپستریم 2678b6 (در پالت نبود) ← اکسنت.
#   ۵) زنجیرهٔ کم‌حجم حباب خروجی: ۱۲ کلید chat_compact_out* + ۴ کلید چیپ ری‌اکشن کم‌حجم +
#      آیکون دکمهٔ کناری — همگی آپستریم سرد (808384 / 1A1D21) و خارج از پالت بودند.
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


def draw_check(x_px, y_px, color, double):
    """تیک ارسال/خوانده‌شده — دو پاره‌خط؛ double = تیک دوم برای «خوانده‌شده»"""
    s = 5 * S
    d.line([(x_px, y_px + s * 0.6), (x_px + s * 0.45, y_px + s), (x_px + s * 1.3, y_px - s * 0.4)],
           fill=rgb(color), width=S + 1)
    if double:
        d.line([(x_px - s * 0.75, y_px + s * 0.6), (x_px - s * 0.3, y_px + s), (x_px + s * 0.55, y_px - s * 0.4)],
               fill=rgb(color), width=S + 1)


def draw_out_bubble(x_right_px, ydp, wdp, hdp, color):
    """حباب خروجی: rounded ۲۶dp + گوشهٔ پایین-راست مربع (نزدیک دُم) + دُم کوچک سمت راست"""
    ys = ydp * S
    r = BUBBLE_R * S
    xs = x_right_px - wdp * S
    x1 = x_right_px
    y1 = ys + hdp * S
    d.rounded_rectangle([xs, ys, x1, y1], radius=r, fill=rgb(color))
    d.rectangle([x1 - r, y1 - r, x1, y1], fill=rgb(color))
    d.polygon([(x1, y1 - 14 * S), (x1 + 7 * S, y1), (x1 - 8 * S, y1)], fill=rgb(color))


def draw_out_section(x0, theme, caption):
    margin = 12 * S
    xr = x0 + W_DP * S - margin  # لبهٔ راست حباب‌ها
    canvas = theme["chat_wallpaper"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + (H_DP - 110) * S], fill=rgb(canvas))
    d.text((x0 + 12 * S, 10 * S), "regular  out bubble r=26 (SHAPE_BUBBLE) — primary-container",
           font=f_small, fill=rgb(theme["chat_serviceText"]))

    # ── حباب خروجی متنی با لینک ──
    by, bw, bh = 30, 258, 58
    draw_out_bubble(xr, by, bw, bh, theme["chat_outBubble"])
    d.text((xr - (bw - 14) * S, (by + 10) * S), "This is the outgoing message",
           font=f_row, fill=rgb(theme["chat_messageTextOut"]))
    linky = (by + 30) * S
    d.text((xr - (bw - 14) * S, linky), "with a link inside", font=f_row, fill=rgb(theme["chat_messageLinkOut"]))
    tw = d.textlength("with a link inside", font=f_row)
    d.line([(xr - (bw - 14) * S, linky + 15 * S), (xr - (bw - 14) * S + tw, linky + 15 * S)],
           fill=rgb(theme["chat_messageLinkOut"]), width=S)
    # زمان + تیک خوانده‌شده (دوتایی)
    d.text((xr - 48 * S, (by + bh - 21) * S), "12:40", font=f_small, fill=rgb(theme["chat_outTimeText"]))
    draw_check(xr - 58 * S, (by + bh - 14) * S, theme["chat_outSentCheckRead"], double=True)

    # ── چیپ‌های ری‌اکشن خروجی ──
    chip_solid = theme["chat_outReactionButtonBackground"]
    chip_bg = composite(alpha_of(chip_solid, 0.156), theme["chat_outBubble"])  # آپستریم: ×۰٫۱۵۶
    chh = 24
    cy = 100
    d.rounded_rectangle([xr - 64 * S, cy * S, xr, (cy + chh) * S],
                        radius=chh * S // 2, fill=rgb(chip_bg))
    d.text((xr - 54 * S, (cy + 5) * S), "thumbs 3", font=f_small, fill=rgb(theme["chat_outReactionButtonText"]))
    sx = xr - 134 * S
    d.rounded_rectangle([sx, cy * S, sx + 70 * S, (cy + chh) * S],
                        radius=chh * S // 2, fill=rgb(chip_solid))
    d.text((sx + 10 * S, (cy + 5) * S), "heart 12", font=f_small, fill=rgb(theme["chat_outReactionButtonTextSelected"]))
    d.text((sx - 176 * S, (cy + 5) * S), "selected = solid accent + onAccent",
           font=f_small, fill=rgb(theme["chat_serviceText"]))

    # ── حباب صوتی خروجی (سیکبار) ──
    vy, vw, vh = 136, 230, 52
    draw_out_bubble(xr, vy, vw, vh, theme["chat_outBubble"])
    d.rounded_rectangle([xr - (vw - 20) * S, (vy + 18) * S, xr - 66 * S, (vy + 34) * S],
                        radius=8 * S, fill=rgb(theme["chat_outVoiceSeekbar"]))
    d.rounded_rectangle([xr - (vw - 20) * S, (vy + 18) * S, xr - 124 * S, (vy + 34) * S],
                        radius=8 * S, fill=rgb(theme["chat_outVoiceSeekbarFill"]))
    d.text((xr - 60 * S, (vy + 18) * S), "1:08", font=f_small, fill=rgb(theme["chat_outAudioDurationText"]))

    # ── بوم کم‌حجم: زنجیرهٔ compact_out* ──
    cbg = theme["chat_compact_background"]
    cbub = theme["chat_compact_outBackground"]
    y0c = 206
    d.rectangle([x0, y0c * S, x0 + W_DP * S, 292 * S], fill=rgb(cbg))
    d.text((x0 + 12 * S, (y0c + 3) * S), "compact canvas — outgoing bubble flattened",
           font=f_small, fill=rgb(theme["chat_compact_actionIcon"]))
    # حباب خروجی کم‌حجم (بدون دُم، رادیوس کامل)
    bx1 = xr
    by1, bw1, bh1 = (y0c + 20), 216, 44
    d.rounded_rectangle([bx1 - bw1 * S, by1 * S, bx1, (by1 + bh1) * S], radius=26 * S, fill=rgb(cbub))
    d.text((bx1 - (bw1 - 12) * S, (by1 + 6) * S), "compact outgoing text", font=f_row,
           fill=rgb(theme["chat_compact_outReplyText"]))
    d.text((bx1 - 46 * S, (by1 + bh1 - 18) * S), "12:40", font=f_small, fill=rgb(theme["chat_compact_outTimeText"]))
    draw_check(bx1 - 56 * S, (by1 + bh1 - 11) * S, theme["chat_compact_outCheck"], double=True)
    # چیپ ری‌اکشن کم‌حجم (in/out مشترک؛ under = بستر حباب)
    chip_bg2 = composite(theme["chat_compact_reactionBackground"], cbub)
    cy2 = (y0c + 68)
    d.rounded_rectangle([xr - 62 * S, cy2 * S, xr, (cy2 + 22) * S], radius=11 * S, fill=rgb(chip_bg2))
    d.text((xr - 52 * S, (cy2 + 4) * S), "fire 5", font=f_small, fill=rgb(theme["chat_compact_reactionText"]))
    d.rounded_rectangle([xr - 132 * S, cy2 * S, xr - 68 * S, (cy2 + 22) * S], radius=11 * S,
                        fill=rgb(theme["chat_compact_reactionBackgroundSelected"]))
    d.text((xr - 122 * S, (cy2 + 4) * S), "heart 12", font=f_small, fill=rgb(theme["chat_compact_reactionTextSelected"]))

    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


draw_out_section(12, day, "DAY  FFDDB8 bubble; solid-accent chips + onAccent; compact chain warm")
draw_out_section(12 + W_DP * S + 12, night, "NIGHT  5C4000 bubble; compact chain visible on dark canvas")

out = os.path.join(ROOT, "download/ui2-step21-outbubble-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    bub = t["chat_outBubble"]
    cbub = t["chat_compact_outBackground"]
    cbg = t["chat_compact_background"]
    chip_bg = composite(alpha_of(t["chat_outReactionButtonBackground"], 0.156), bub)
    cchip_bg = composite(t["chat_compact_reactionBackground"], cbub)
    rows = [
        ("out text", t["chat_messageTextOut"], bub),
        ("out link (was blue 2678b6)", t["chat_messageLinkOut"], bub),
        ("out time", t["chat_outTimeText"], bub),
        ("sentCheckRead (was 2.06 day)", t["chat_outSentCheckRead"], bub),
        ("chip unselected bg (x0.156)", chip_bg, bub),
        ("chip unselected text", t["chat_outReactionButtonText"], chip_bg),
        ("chip selected text (onAccent)", t["chat_outReactionButtonTextSelected"], t["chat_outReactionButtonBackground"]),
        ("voice seekbar fill", t["chat_outVoiceSeekbarFill"], bub),
        ("compact out bubble vs canvas", cbub, cbg),
        ("compact out text", t["chat_compact_outReplyText"], cbub),
        ("compact out time", t["chat_compact_outTimeText"], cbub),
        ("compact out check", t["chat_compact_outCheck"], cbub),
        ("compact chip bg", cchip_bg, cbub),
        ("compact chip text", t["chat_compact_reactionText"], cchip_bg),
        ("compact chip selected text", t["chat_compact_reactionTextSelected"], t["chat_compact_reactionBackgroundSelected"]),
        ("compact accent icon (onAccent)", t["chat_compact_outAccentIcon"], t["chat_compact_outAccentFill"]),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:34s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")

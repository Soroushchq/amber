#!/usr/bin/env python3
# UI2 قدم ۲۰ — پیش‌نمایش حباب ورودی (Expressive)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم:
#   ۱) شعاع حباب ورودی: پیش‌فرض SharedConfig.bubbleRadius از ۱۷ آپستریم به توکن SHAPE_BUBBLE (۲۶dp)
#      بایند شد (مصرف‌کنندهٔ اول این توکن) + سقف اسلایدر «Message corners» هم توکن شد.
#   ۲) زنجیرهٔ کم‌حجمِ حباب ورودی (میراث قدم ۱۹): ۵ کلید chat_compact_in* پالت‌سازی شد
#      (ساعت/مدت/پر موج/بسترهٔ موج/دکمهٔ پیاده‌سازی) — قبلاً سرد و خارج از پالت بودند.
#   ۳) رفع باگ واقعی خانوادهٔ ری‌اکشن: chat_inReactionButtonBackground باید «جامد» می‌بود
#      (آپستریم جامد است و مصرف‌کننده‌ها خودشان ×۰٫۱۵۶/۰x10 می‌سازند) — اکسنت×۱۰٪ قبلی
#      چیپ را ۱٫۶٪ و آیکون transcribe را تقریباً نامرئی می‌کرد؛ + متن چیپ انتخاب‌شده ← onAccent.
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
S = 2  # px per dp

BUBBLE_R = 26  # AmberTokens.SHAPE_BUBBLE
UPSTREAM_R = 17


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


def draw_bubble(x0, ydp, wdp, hdp, color):
    """حباب ورودی: rounded ۲۶dp + گوشهٔ پایین-چپ مربع (نزدیک دُم) + دُم کوچک"""
    ys, xs = ydp * S, x0
    r = BUBBLE_R * S
    x1, y1 = xs + wdp * S, ys + hdp * S
    d.rounded_rectangle([xs, ys, x1, y1], radius=r, fill=rgb(color))
    # مربع‌کردن گوشهٔ پایین-چپ (گوشهٔ دُم، مثل near corner آپستریم)
    d.rectangle([xs, y1 - r, xs + r, y1], fill=rgb(color))
    # دُم کوچک
    d.polygon([(xs, y1 - 14 * S), (xs - 7 * S, y1), (xs + 8 * S, y1)], fill=rgb(color))


def draw_in_bubble(x0, theme, caption, dark):
    bx, by, bw, bh = 28, 28, 240, 56
    canvas = theme["chat_wallpaper"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + (H_DP - 120) * S], fill=rgb(canvas))
    d.text((x0 + 12 * S, 10 * S), "regular  bubble r=%ddp (SHAPE_BUBBLE, was %d)" % (BUBBLE_R, UPSTREAM_R),
           font=f_small, fill=rgb(theme["chat_serviceText"]))

    # ── حباب ورودی متنی ──
    draw_bubble(x0 + bx * S, by, bw, bh, theme["chat_inBubble"])
    d.text((x0 + (bx + 18) * S, (by + 12) * S), "Salam! Expressive incoming bubble.",
           font=f_row, fill=rgb(theme["chat_messageTextIn"]))
    d.text((x0 + (bx + bw - 52) * S, (by + bh - 22) * S), "12:40",
           font=f_small, fill=rgb(theme["chat_inTimeText"]))

    # ── چیپ‌های ری‌اکشن روی حباب ──
    chip_solid = theme["chat_inReactionButtonBackground"]
    chip_bg = composite(alpha_of(chip_solid, 0.156), theme["chat_inBubble"])  # آپستریم: ×۰٫۱۵۶
    cx, cy, chh = 28, 92, 24
    d.rounded_rectangle([x0 + cx * S, cy * S, x0 + (cx + 64) * S, (cy + chh) * S],
                        radius=chh * S // 2, fill=rgb(chip_bg))
    d.text((x0 + (cx + 10) * S, (cy + 5) * S), "thumbs 3", font=f_small, fill=rgb(theme["chat_inReactionButtonText"]))
    # چیپ انتخاب‌شده: جامد اکسنت + متن onAccent
    sx = cx + 72
    d.rounded_rectangle([x0 + sx * S, cy * S, x0 + (sx + 70) * S, (cy + chh) * S],
                        radius=chh * S // 2, fill=rgb(chip_solid))
    d.text((x0 + (sx + 10) * S, (cy + 5) * S), "heart 12", font=f_small, fill=rgb(theme["chat_inReactionButtonTextSelected"]))
    d.text((x0 + (sx + 78) * S, (cy + 5) * S), "selected chip = solid accent + onAccent",
           font=f_small, fill=rgb(theme["chat_serviceText"]))

    # ── حباب صوتی ورودی ──
    vy, vw, vh = 126, 230, 52
    draw_bubble(x0 + 28 * S, vy, vw, vh, theme["chat_inBubble"])
    # بسترهٔ موج = outline، پر = اکسنت
    d.rounded_rectangle([x0 + 48 * S, (vy + 18) * S, x0 + 172 * S, (vy + 34) * S],
                        radius=8 * S, fill=rgb(theme["chat_inVoiceSeekbar"]))
    d.rounded_rectangle([x0 + 48 * S, (vy + 18) * S, x0 + 118 * S, (vy + 34) * S],
                        radius=8 * S, fill=rgb(theme["chat_inVoiceSeekbarFill"]))
    d.text((x0 + 180 * S, (vy + 18) * S), "0:42", font=f_small, fill=rgb(theme["chat_inAudioDurationText"]))
    # دکمهٔ پیاده‌سازی: بستره = اکسنت×۱۵٫۶٪ (مثل آپستریم از رنگ جامد می‌سازد) + آیکون اکسنت جامد
    tb = composite(alpha_of(chip_solid, 0.156), theme["chat_inBubble"])
    d.rounded_rectangle([x0 + 186 * S, (vy + 12) * S, x0 + 216 * S, (vy + 40) * S],
                        radius=12 * S, fill=rgb(tb))
    d.text((x0 + 193 * S, (vy + 18) * S), "Aa", font=f_row, fill=rgb(chip_solid))

    # ── بوم کم‌حجم: زنجیرهٔ compact_in* ──
    cbg = theme["chat_compact_background"]
    y0c = 196
    d.rectangle([x0, y0c * S, x0 + W_DP * S, 288 * S], fill=rgb(cbg))
    d.text((x0 + 12 * S, (y0c + 3) * S), "compact canvas (chat_compact_background)",
           font=f_small, fill=rgb(theme["chat_compact_actionIcon"]))
    # ساعت compact
    d.text((x0 + 40 * S, (y0c + 22) * S), "12:40  views 1.2K", font=f_small,
           fill=rgb(theme["chat_compact_inTimeText"]))
    d.text((x0 + 150 * S, (y0c + 22) * S), "compact inTime (was cold 0x80A1AAB3)",
           font=f_small, fill=rgb(theme["chat_compact_actionIcon"]))
    # موج compact
    track = composite(theme["chat_compact_inWaveformBackground"], cbg)
    d.rounded_rectangle([x0 + 40 * S, (y0c + 44) * S, x0 + 180 * S, (y0c + 60) * S],
                        radius=8 * S, fill=rgb(track))
    d.rounded_rectangle([x0 + 40 * S, (y0c + 44) * S, x0 + 120 * S, (y0c + 60) * S],
                        radius=8 * S, fill=rgb(theme["chat_compact_inWaveform"]))
    d.text((x0 + 188 * S, (y0c + 44) * S), "0:42", font=f_small, fill=rgb(theme["chat_compact_inAudioDuration"]))
    # دکمهٔ پیاده‌سازی compact: بستره = اکسنت×۱۵٫۶٪ روی بوم + آیکون اکسنت
    tb2 = composite(alpha_of(theme["chat_compact_inTranscribeButton"], 0.156), cbg)
    d.rounded_rectangle([x0 + 226 * S, (y0c + 40) * S, x0 + 256 * S, (y0c + 64) * S],
                        radius=12 * S, fill=rgb(tb2))
    d.text((x0 + 233 * S, (y0c + 46) * S), "Aa", font=f_row, fill=rgb(theme["chat_compact_inTranscribeButton"]))
    d.text((x0 + 262 * S, (y0c + 46) * S), "transcribe", font=f_small, fill=rgb(theme["chat_compact_inTimeText"]))

    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


draw_in_bubble(12, day, "DAY  r=26 warm cream bubble; chips tonal/solid; compact chain warm", False)
draw_in_bubble(12 + W_DP * S + 12, night, "NIGHT  r=26 warm dark bubble; compact chain visible (was invisible)", True)

out = os.path.join(ROOT, "download/ui2-step20-bubble-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    cbg = t["chat_compact_background"]
    bub = t["chat_inBubble"]
    rows = [
        ("bubble text", t["chat_messageTextIn"], bub),
        ("inTime on bubble", t["chat_inTimeText"], bub),
        ("chip unselected bg(x0.156)", composite(alpha_of(t["chat_inReactionButtonBackground"], 0.156), bub), bub),
        ("chip unselected text", t["chat_inReactionButtonText"], composite(alpha_of(t["chat_inReactionButtonBackground"], 0.156), bub)),
        ("chip selected text (onAccent)", t["chat_inReactionButtonTextSelected"], t["chat_inReactionButtonBackground"]),
        ("waveform fill on bubble", t["chat_inVoiceSeekbarFill"], bub),
        ("transcribe icon (solid accent)", t["chat_inReactionButtonBackground"], bub),
        ("compact inTime", t["chat_compact_inTimeText"], cbg),
        ("compact duration", t["chat_compact_inAudioDuration"], cbg),
        ("compact waveform fill", t["chat_compact_inWaveform"], cbg),
        ("compact waveform track", composite(t["chat_compact_inWaveformBackground"], cbg), cbg),
        ("compact transcribe icon", t["chat_compact_inTranscribeButton"], cbg),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:32s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")

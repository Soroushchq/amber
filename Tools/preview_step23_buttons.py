#!/usr/bin/env python3
# UI2 قدم ۲۳ — پیش‌نمایش دکمه‌های ارسال/پیوست/ضبط (Expressive)
# کارهای این قدم:
#   ۱) فرم: شعاع دکمهٔ ارسال/ضبط از ۱۹dp هاردکد ← توکن SHAPE_FAB (۲۰dp؛ دومین مصرف‌کننده) —
#      روی مربع ۳۸dp همان دایره، فقط انتهای قرص ستاره‌ها گردتر.
#   ۲) رنگ آیکون دکمهٔ ارسال: سفید هاردکد (شب روی کهربا ۲٫۳۶:۱!) ← onAccent (۷٫۲۳ شب / ۴٫۲۹ روز)
#      + متن قیمت ستاره‌ها + آیکون معکوس (که به تینت ۸٪ خوانده می‌شد).
#   ۳) باگ واقعی: chat_messagePanelVoicePressed آپستریم «سفید» است و همهٔ مصرف‌کننده‌هایش آیکون‌اند
#      (تینت پرس میک/ویدیو/ارسال، menuPaint فرستنده، چک‌مارک کپشن) — جوهر×۸٪ قبلی همه را نامرئی می‌کرد ← جوهر جامد.
#   ۴) نقطهٔ ضبط صوتی از اکسنت کهربایی ← قرمز معنایی پالت (آپستریم da564d؛ روز ۵٫۰۳ / شب ۵٫۲۲).
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "TMessagesProj/src/main/assets")
S = 2


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

W_DP, H_DP = 360, 250
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 30), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)


def draw_send(x0, t, cx, cy, sz=38):
    """قرص/دایرهٔ ارسال: اکسنت + آیکون onAccent (شعاع SHAPE_FAB=۲۰)"""
    r = 20 * S
    d.rounded_rectangle([cx * S, cy * S, (cx + sz) * S, (cy + sz) * S], radius=r,
                        fill=rgb(t["chat_messagePanelSend"]))
    # هواپیمای کاغذی ساده (مثلث)
    ix, iy = cx + 10, cy + 11
    d.polygon([(ix * S, (iy + 8) * S), ((ix + 17) * S, (iy + 8) * S), (ix * S, iy * S), (ix * S, (iy + 15) * S)],
              fill=rgb(t["featuredStickers_addButtonIcon"]))


def draw_section(x0, t, caption):
    panel = t["chat_messagePanelBackground"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + (H_DP - 26) * S], fill=rgb(t["chat_wallpaper"]))
    d.text((x0 + 12 * S, 10 * S), "send/attach/record — SHAPE_FAB 20dp + onAccent glyph",
           font=f_small, fill=rgb(t["chat_serviceText"]))

    # ── شیت فیلد سفید + دکمهٔ ارسال ──
    sy = 34
    d.rectangle([x0, sy * S, x0 + W_DP * S, (sy + 50) * S], fill=rgb(panel))
    d.text((x0 + 56 * S, (sy + 17) * S), "Message", font=f_row, fill=rgb(t["chat_messagePanelHint"]))
    d.rounded_rectangle([x0 + 20 * S, (sy + 9) * S, x0 + 44 * S, (sy + 33) * S], radius=6 * S,
                        outline=rgb(t["chat_messagePanelIcons"]), width=S + 1)
    draw_send(x0, t, W_DP - 54, sy + 6)
    d.text((x0 + (W_DP - 50) * S, (sy + 52) * S), "send  r=20 (was 19 hardcode)",
           font=f_small, fill=rgb(t["chat_serviceText"]))

    # ── حالت ضبط: پیل کرم + نقطهٔ قرمز + تایمر dim ──
    ry = 92
    d.rectangle([x0, ry * S, x0 + W_DP * S, (ry + 46) * S], fill=rgb(t["chat_messagePanelVoiceBackground"]))
    d.ellipse([x0 + 16 * S, (ry + 13) * S, x0 + 36 * S, (ry + 33) * S], fill=rgb(t["chat_recordedVoiceDot"]))
    d.text((x0 + 44 * S, (ry + 14) * S), "0:15   slide to cancel ‹", font=f_row, fill=rgb(t["chat_recordTime"]))
    d.text((x0 + 190 * S, (ry + 14) * S), "dot = semantic red", font=f_small, fill=rgb(t["chat_serviceText"]))

    # ── میک حالت پرس (تینت جوهر جامد — قبلاً ۸٪ نامرئی) ──
    py = 148
    d.rounded_rectangle([x0 + 16 * S, py * S, x0 + 60 * S, (py + 40) * S], radius=20 * S,
                        fill=rgb(t["chat_messagePanelVoicePressed"] if False else t["chat_inBubble"]))
    d.text((x0 + 30 * S, (py + 10) * S), "mic", font=f_small, fill=rgb(t["chat_messagePanelVoicePressed"]))
    d.text((x0 + 68 * S, (py + 10) * S), "pressed mic tint = solid ink (was 8% ghost)",
           font=f_small, fill=rgb(t["chat_serviceText"]))

    # ── پیل ضبط‌شده: قرص هدر + نقطهٔ قرمز + پخش ──
    qy = 196
    d.rounded_rectangle([x0 + 16 * S, qy * S, x0 + 220 * S, (qy + 40) * S], radius=12 * S,
                        fill=rgb(t["chat_recordedVoiceBackground"]))
    d.ellipse([x0 + 26 * S, (qy + 10) * S, x0 + 46 * S, (qy + 30) * S], fill=rgb(t["chat_recordedVoiceDot"]))
    d.text((x0 + 54 * S, (qy + 10) * S), "▶", font=f_row, fill=rgb(t["chat_recordedVoicePlayPause"]))
    d.text((x0 + 76 * S, (qy + 10) * S), "0:04", font=f_row, fill=rgb(t["chat_recordedVoiceProgressInner"]))

    d.text((x0, 6 + H_DP * S + 4), caption, font=f_small, fill=(210, 200, 190))


draw_section(12, day, "DAY  accent circle + white plane (4.29); red dot; ink pressed tints")
draw_section(12 + W_DP * S + 12, night, "NIGHT  onAccent glyph 7.23 (was white 2.36); red dot 5.22")

out = os.path.join(ROOT, "download/ui2-step23-buttons-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    panel = t["chat_messagePanelBackground"]
    pill = t["chat_messagePanelVoiceBackground"]
    rpill = t["chat_recordedVoiceBackground"]
    rows = [
        ("send glyph (onAccent)", t["featuredStickers_addButtonIcon"], t["chat_messagePanelSend"]),
        ("send pill (accent)", t["chat_messagePanelSend"], panel),
        ("record timer", t["chat_recordTime"], pill),
        ("record dot (semantic red)", t["chat_recordedVoiceDot"], pill),
        ("pressed tint (solid ink)", t["chat_messagePanelVoicePressed"], panel),
        ("recorded dot on pill", t["chat_recordedVoiceDot"], rpill),
        ("recorded play", t["chat_recordedVoicePlayPause"], rpill),
        ("recorded duration", t["chat_recordedVoiceProgressInner"], rpill),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:34s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")

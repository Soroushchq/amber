#!/usr/bin/env python3
# UI2 قدم ۲۲ — پیش‌نمایش ورودی پیام (Expressive)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم:
#   ۱) شیت پایین = فیلد سفید: chat_messagePanelBackground از FFEFC9 خارج‌ازتوکن (روز) و
#      هدر (شب) ← توکن fieldBg (روز FFFFFF هم‌زبانهٔ کارت دیالوگ‌ها؛ شب 241D14 سطح فیلد).
#   ۲) مرز بالای شیت: chat_messagePanelShadow صفر بود (کاملاً بی‌مرز) ← روز جوهر گرم
#      (گرادیان مویی MULTIPLY روی کاغذ ≈ ECE3D7 = خانوادهٔ مرز E9DFD0) / شب مشکی آپستریم.
#   ۳) باگ واقعی: تایمر ضبط (chat_recordTime) سفید روی پیل کرم = نامرئی (۱٫۱۴:۱) ← dim گرم.
#   ۴) پیل صدای ضبط‌شده از FFEFC9/332717 خارج‌ازتوکن ← توکن هدر و بوردر هدر شب.
#   ۵) قفل ضبط صوتی: ۳ کلید با قرارداد عجیب آپستریم (پیشوند key_) — آیکون سرد A4A4A4 ← dim؛
#      بسترهٔ اکسنت! ← fieldBg؛ سایهٔ صفر ← مشکی آپستریم. + chat_attachContactText (کلید مرده) ← زمان.
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

# گرادیان مویی مرز — شبیه‌سازی compose_panel_shadow (آلفا ۲..۲۲ از پایین به بالا)
EDGE_ALPHAS = [22, 12, 12, 2, 2]  # از نزدیک پنل به بالا


def draw_edge_border(x0, y_px, w_dp, tint):
    """مرز بالای شیت = گرادیان مویی رنگ‌آمیزی‌شده (MULTIPLY ≈ همان رنگ با آلفای PNG)"""
    for i, a in enumerate(EDGE_ALPHAS):
        row = composite((a << 24) | (tint & 0xFFFFFF), theme_bg(x0))
        d.rectangle([x0, y_px + i * S, x0 + w_dp * S, y_px + (i + 1) * S], fill=rgb(row))


_theme_by_x = {}


def theme_bg(x0):
    return _theme_by_x[x0]["chat_wallpaper"]


def draw_input(x0, t, caption, dark):
    _theme_by_x[x0] = t
    panel = t["chat_messagePanelBackground"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + (H_DP - 108) * S], fill=rgb(t["chat_wallpaper"]))
    d.text((x0 + 12 * S, 10 * S), "input sheet = field white (was FFEFC9, off-token)",
           font=f_small, fill=rgb(t["chat_serviceText"]))

    # ── یک حباب ورودی + یک حباب خروجی برای زمینه ──
    d.rounded_rectangle([x0 + 20 * S, 30 * S, x0 + 220 * S, 74 * S], radius=26 * S, fill=rgb(t["chat_inBubble"]))
    d.text((x0 + 34 * S, 44 * S), "incoming context", font=f_row, fill=rgb(t["chat_messageTextIn"]))

    # ── شیت پایین: مرز مویی + فیلد سفید ──
    sheet_y = 120
    draw_edge_border(x0, sheet_y * S - 5 * S, W_DP, t["chat_messagePanelShadow"])
    d.rectangle([x0, sheet_y * S, x0 + W_DP * S, (sheet_y + 62) * S], fill=rgb(panel))
    d.text((x0 + 12 * S, (sheet_y + 3) * S), "E9DFD0-family hairline border (was invisible)",
           font=f_small, fill=rgb(t["chat_serviceText"]))
    # فیلد متن: رسنگ + متن + کرسر
    d.text((x0 + 56 * S, (sheet_y + 24) * S), "Message", font=f_row, fill=rgb(t["chat_messagePanelHint"]))
    d.line([(x0 + 118 * S, (sheet_y + 22) * S), (x0 + 118 * S, (sheet_y + 40) * S)],
           fill=rgb(t["chat_messagePanelCursor"]), width=S + 1)
    # آیکون‌ها: کلیپ = accent، استیکر/دوربین dim-ish؛ دکمهٔ ارسال = قرص اکسنت
    d.rounded_rectangle([x0 + (W_DP - 54) * S, (sheet_y + 17) * S, x0 + (W_DP - 14) * S, (sheet_y + 47) * S],
                        radius=20 * S, fill=rgb(t["chat_messagePanelSend"]))
    d.text((x0 + (W_DP - 43) * S, (sheet_y + 24) * S), ">", font=f_row, fill=rgb(t["key_chat_messagePanelVoiceLockBackground" if False else "chat_attachCheckBoxCheck"]))
    d.text((x0 + 22 * S, (sheet_y + 22) * S), "[]", font=f_row, fill=rgb(t["chat_messagePanelIcons"]))
    d.text((x0 + 44 * S, (sheet_y + 22) * S), "()", font=f_row, fill=rgb(t["chat_messagePanelIcons"]))

    # ── حالت ضبط صوتی: پیل header + تایمر dim (باگ نامرئی رفع شد) ──
    rec_y = sheet_y + 66
    d.rectangle([x0, rec_y * S, x0 + W_DP * S, (rec_y + 46) * S], fill=rgb(t["chat_messagePanelVoiceBackground"]))
    d.ellipse([x0 + 16 * S, (rec_y + 13) * S, x0 + 36 * S, (rec_y + 33) * S], fill=rgb(t["chat_recordedVoiceDot"]))
    d.text((x0 + 44 * S, (rec_y + 14) * S), "0:15   slide to cancel ‹", font=f_row,
           fill=rgb(t["chat_recordTime"]))
    d.text((x0 + 190 * S, (rec_y + 14) * S), "(was invisible white!)", font=f_small,
           fill=rgb(t["chat_serviceText"]))

    # ── قفل ضبط صوتی شناور (لبهٔ راست صفحه، روی وایپرپ) ──
    lb = t["key_chat_messagePanelVoiceLockBackground"]
    d.ellipse([x0 + (W_DP - 46) * S, (sheet_y - 30) * S, x0 + (W_DP - 14) * S, (sheet_y + 2) * S], fill=rgb(lb))
    d.text((x0 + (W_DP - 33) * S, (sheet_y - 22) * S), "L", font=f_row, fill=rgb(t["key_chat_messagePanelVoiceLock"]))

    d.text((x0, 6 + H_DP * S + 12), caption, font=f_small, fill=(210, 200, 190))


draw_input(12, day, "DAY  white field sheet + warm ink hairline border (E9DFD0 family) + dim timer", False)
draw_input(12 + W_DP * S + 12, night, "NIGHT  field surface 241D14 lifted from wallpaper; timer visible", True)

out = os.path.join(ROOT, "download/ui2-step22-input-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
INK_BORDER = day["chat_messagePanelShadow"] & 0xFFFFFF
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    panel = t["chat_messagePanelBackground"]
    wp = t["chat_wallpaper"]
    pill = t["chat_messagePanelVoiceBackground"]
    rpill = t["chat_recordedVoiceBackground"]
    rows = [
        ("panel text", t["chat_messageTextOut"] if False else t["chat_messagePanelText"], panel),
        ("panel hint", t["chat_messagePanelHint"], panel),
        ("panel icons (accent)", t["chat_messagePanelIcons"], panel),
        ("panel send (accent bg)", t["chat_attachCheckBoxCheck"], t["chat_messagePanelSend"]),
        ("hairline border vs wallpaper", composite((22 << 24) | (t["chat_messagePanelShadow"] & 0xFFFFFF), wp), wp),
        ("voice pill timer (was white!)", t["chat_recordTime"], pill),
        ("voice cancel arrow", t["chat_recordVoiceCancel"], pill),
        ("recorded pill bg vs panel", rpill, panel),
        ("recorded dot (accent)", t["chat_recordedVoiceDot"], rpill),
        ("voice lock icon on lock bg", t["key_chat_messagePanelVoiceLock"], t["key_chat_messagePanelVoiceLockBackground"]),
        ("voice lock bg vs wallpaper", t["key_chat_messagePanelVoiceLockBackground"], wp),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:34s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")

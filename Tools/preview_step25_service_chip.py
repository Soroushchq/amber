#!/usr/bin/env python3
# UI2 قدم ۲۵ — پیش‌نمایش پیام‌های سیستم/دیت (چیپ مرکزی ChatActionCell)
# همهٔ رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم:
#   ۱) باگ اصلی — مسیر «گرادیان سرویس»: روی وایپرپ متحرک، چیپ از پچِ بلورِ خود وایپرپ با ماتریس
#      روشنایی ساخته می‌شد (روز ×۰٫۹۲−۶٪ روی کرم روشن) و متنِ سفیدِ اجباری فقط ~۱٫۵:۱ می‌گرفت.
#      رفع: در applyChatServiceMessageColor اگر تم کلید chat_serviceBackground را صریح تعریف کرده باشد
#      (attheme کهربایی)، چیپ از همان اسکریم توکنی می‌آید — بدون کلید صریح، رفتار آپستریم حفظ می‌شود.
#   ۲) اسکریم روز از DAY_TEXT_DIM×۷۰٪ (متن سفید ۳٫۰۴:۱) ← جوهر ۶۵٪ (۵٫۸۸:۱)؛ شب بدون تغییر (۱۵٫۱:۱)
#   ۳) chat_serviceBackgroundSelected قبلاً همان رنگ عادی بود (بدون بازخورد فشردگی) ← روز جوهر ۷۸٪ / شب تیره‌تر
#   ۴) chat_serviceBackgroundSelector (ریپل دکمه‌های بات) قبلاً = رنگ خود چیپ (ریپل نامرئی) ← سفید ۱۴٪
#   ۵) chat_botButtonText اکسنت بود (روی قرص تیرهٔ روز ۱٫۳۷:۱ نامرئی) ← هم‌زبانهٔ serviceText
#   ۶) chat_compact_botButtonText آپستریم مشکی (شب روی پیل تونالِ جوهر روشن ۱٫۴۵:۱) ← هم‌زبانهٔ compact_actionText
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


def argb_tuple(c):
    return (c >> 16 & 255, c >> 8 & 255, c & 255, (c >> 24) & 255)


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


def blend(c1, c2, t):
    r1, g1, b1 = rgb(c1)
    r2, g2, b2 = rgb(c2)
    m = lambda a, b: int(round(a + (b - a) * t))
    return (m(r1, r2) << 16) | (m(g1, g2) << 8) | m(b1, b2)


def saturate_matrix(c, s):
    """ColorMatrix.setSaturation(s) استاندارد اندروید"""
    lr, lg, lb = 0.213, 0.715, 0.072
    r, g, b = rgb(c)
    rr = r * (lr * (1 - s) + s) + g * (lg * (1 - s)) + b * (lb * (1 - s))
    gr = r * (lr * (1 - s)) + g * (lg * (1 - s) + s) + b * (lb * (1 - s))
    br = r * (lr * (1 - s)) + g * (lg * (1 - s)) + b * (lb * (1 - s) + s)
    cl = lambda v: max(0, min(255, int(round(v))))
    return (cl(rr) << 16) | (cl(gr) << 8) | cl(br)


def patch_color(wall_avg, dark):
    """شبیه‌سازی ماتریس پچ سرویس آپستریم روی میانگین وایپرپ متحرک"""
    c = saturate_matrix(wall_avg, 1.6)
    m = 0.97 if dark else 0.92
    adj = +0.12 if dark else -0.06
    r, g, b = rgb(c)
    cl = lambda v: max(0, min(255, int(round(v))))
    r = cl(r * m + adj * 255); g = cl(g * m + adj * 255); b = cl(b * m + adj * 255)
    return (r << 16) | (g << 8) | b


def motion_gradient(colors, w_px, h_px):
    """تقریب بلیند ۴رنگ MotionBackgroundDrawable (base/to/to2/to3 = چهار گوشه)"""
    c0, c1, c2, c3 = colors
    img = Image.new("RGB", (w_px, h_px))
    px = img.load()
    for y in range(h_px):
        v = y / max(1, h_px - 1)
        for x in range(w_px):
            u = x / max(1, w_px - 1)
            px[x, y] = rgb(blend(blend(c0, c1, u), blend(c2, c3, u), v))
    return img


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 332
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
FONT = os.path.join(ASSETS, "fonts/ambergramui-med.ttf")
f_small = ImageFont.truetype(FONT, 10 * S)
f_row = ImageFont.truetype(FONT, 12 * S)
f_bot = ImageFont.truetype(FONT, 11 * S)


def draw_panel(x0, theme, caption, old_note, new_note):
    wp = motion_gradient(
        [theme["chat_wallpaper"], theme["chat_wallpaper_gradient_to"],
         theme["key_chat_wallpaper_gradient_to2"], theme["key_chat_wallpaper_gradient_to3"]],
        W_DP * S, H_DP * S)
    img.paste(wp, (x0, 6))

    scrim = theme["chat_serviceBackground"]
    sel = theme["chat_serviceBackgroundSelected"]
    ripple = theme["chat_serviceBackgroundSelector"]
    stx = theme["chat_serviceText"]
    slink = theme["chat_serviceLink"]
    bot_tx = theme["chat_botButtonText"]

    def service_chip(cx_dp, cy_dp, w_dp, h_dp, label, link=None, pressed=False, show_ripple=False):
        x, y = x0 + cx_dp * S, cy_dp * S
        d.rounded_rectangle([x, y, x + w_dp * S, y + h_dp * S], radius=h_dp * S // 2,
                            fill=argb_tuple(sel if pressed else scrim))
        tw = d.textlength(label, font=f_small)
        tx = x + (w_dp * S - tw) / 2
        d.text((tx, y + (h_dp - 10) * S / 2), label, font=f_small, fill=rgb(stx))
        if link:
            lw = d.textlength(link, font=f_small)
            d.text((x + (w_dp * S - lw) / 2, y + (h_dp - 10) * S / 2 + 12 * S), link,
                   font=f_small, fill=rgb(slink))
        if show_ripple:
            d.rounded_rectangle([x + 2 * S, y + 2 * S, x + w_dp * S - 2 * S, y + h_dp * S - 2 * S],
                                radius=(h_dp - 4) * S // 2, fill=argb_tuple(ripple))

    # چیپ تاریخ (مرکز)
    service_chip(130, 26, 100, 24, "March 14")
    # چیپ پیام سرویس با لینک (متن سفید + لینک serviceLink)
    service_chip(84, 66, 192, 40, "Parsa joined the group", link="t.me/ambergram")

    # دکمه‌های بات روی چیپ سرویس: متن botButtonText + ریپل (الان دیده می‌شود)
    bx, by = 96, 128
    for i, (lbl, rip) in enumerate((("Open Bot", True), ("Start", False))):
        x = x0 + (bx + i * 92) * S
        d.rounded_rectangle([x, by * S, x + 88 * S, (by + 30) * S], radius=15 * S,
                            fill=argb_tuple(scrim))
        if rip:
            d.rounded_rectangle([x + 2 * S, (by + 2) * S, x + 86 * S, (by + 28) * S],
                                radius=13 * S, fill=argb_tuple(ripple))
        tw = d.textlength(lbl, font=f_bot)
        d.text((x + (88 * S - tw) / 2, (by + 9) * S), lbl, font=f_bot, fill=rgb(bot_tx))

    # BEFORE/AFTER — پچ قدیمی وایپرپ در برابر اسکریم توکنی
    wall_avg = blend(blend(theme["chat_wallpaper"], theme["chat_wallpaper_gradient_to"], 0.5),
                     blend(theme["key_chat_wallpaper_gradient_to2"], theme["key_chat_wallpaper_gradient_to3"], 0.5), 0.5)
    old = patch_color(wall_avg, theme is night)
    py = 188
    d.rounded_rectangle([x0 + 40 * S, py * S, x0 + 160 * S, (py + 26) * S], radius=13 * S, fill=rgb(old))
    d.text((x0 + 56 * S, (py + 8) * S), "old patch", font=f_small, fill=(255, 255, 255))
    d.rounded_rectangle([x0 + 200 * S, py * S, x0 + 320 * S, (py + 26) * S], radius=13 * S,
                        fill=argb_tuple(scrim))
    d.text((x0 + 216 * S, (py + 8) * S), "new scrim", font=f_small, fill=(255, 255, 255))
    d.text((x0 + 12 * S, (py + 32) * S), old_note, font=f_small, fill=(215, 170, 120))
    d.text((x0 + 12 * S, (py + 46) * S), new_note, font=f_small, fill=(180, 210, 150))

    # زنجیرهٔ کم‌حجم: پیل اکشن + متن بات (قبلاً مشکی/شب نامرئی)
    cbg = theme["chat_compact_background"]
    pill = composite(theme["chat_compact_actionBackground"], cbg)
    cy2 = 276
    d.rectangle([x0, cy2 * S, x0 + W_DP * S, (cy2 + 34) * S], fill=rgb(cbg))
    d.rounded_rectangle([x0 + 24 * S, (cy2 + 2) * S, x0 + 160 * S, (cy2 + 32) * S],
                        radius=15 * S, fill=rgb(pill))
    d.text((x0 + 34 * S, (cy2 + 11) * S), "sticker · March 14", font=f_small,
           fill=rgb(theme["chat_compact_actionText"]))
    d.rounded_rectangle([x0 + 172 * S, (cy2 + 2) * S, x0 + 248 * S, (cy2 + 32) * S],
                        radius=15 * S, fill=rgb(pill))
    d.text((x0 + 184 * S, (cy2 + 11) * S), "Open Bot", font=f_small,
           fill=rgb(theme["chat_compact_botButtonText"]))

    d.text((x0 + 12 * S, 10 * S), caption, font=f_small, fill=rgb(theme["chat_messageTextIn"]))


draw_panel(12, day, "DAY  — service/date chip over motion wallpaper",
           "was: wallpaper patch, white text ~1.5:1",
           "now: token scrim, white text 5.9:1")
draw_panel(12 + W_DP * S + 12, night, "NIGHT  — service/date chip over motion wallpaper",
           "patch was 12.3:1 (ok, but device-dependent)",
           "now: uniform token scrim 15.1:1 + visible ripple")

out = os.path.join(ROOT, "download/ui2-step25-service-chip-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t, dark in (("DAY  ", day, False), ("NIGHT", night, True)):
    stops = [t["chat_wallpaper"], t["chat_wallpaper_gradient_to"],
             t["key_chat_wallpaper_gradient_to2"], t["key_chat_wallpaper_gradient_to3"]]
    scrim_c = t["chat_serviceBackground"]
    worst = min(ratio(t["chat_serviceText"], composite(scrim_c, w)) for w in stops)
    wall_avg = blend(blend(stops[0], stops[1], 0.5), blend(stops[2], stops[3], 0.5), 0.5)
    old = patch_color(wall_avg, dark)
    rows = [
        ("service text on token scrim (worst stop)", t["chat_serviceText"], min((composite(scrim_c, w) for w in stops), key=lambda c: ratio(t["chat_serviceText"], c))),
        ("service text on OLD wallpaper patch", (0xFFFFFF | 0xFF000000), old),
        ("service link on scrim", t["chat_serviceLink"], composite(scrim_c, wall_avg)),
        ("bot button text on scrim (was accent 1.37 day)", t["chat_botButtonText"], composite(scrim_c, wall_avg)),
        ("selected scrim vs normal (feedback delta)", composite(t["chat_serviceBackgroundSelected"], wall_avg), composite(scrim_c, wall_avg)),
        ("ripple 14% on scrim (was invisible)", t["chat_serviceBackgroundSelector"], composite(scrim_c, wall_avg)),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:48s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")
    # کم‌حجم
    cbg = t["chat_compact_background"]
    pill = composite(t["chat_compact_actionBackground"], cbg)
    print(f"{name_} {'compact bot text on pill (was black 1.45 night)':48s} #{t['chat_compact_botButtonText'] & 0xFFFFFF:06X} on #{pill:06X}  {ratio(t['chat_compact_botButtonText'], pill):5.2f}:1")

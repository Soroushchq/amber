#!/usr/bin/env python3
# UI2 قدم ۲۸ — ریشه‌کنی دکمه‌های نامشخص (ممیزی آیکون‌های کم‌کنتراست صفحه چت)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
#
# ممیزی این قدم — ۸۲ کلید chat_* بدون پالت بررسی شد و ۷۳ کلید صریح شد:
#   ۱) خانوادهٔ msgIvButton (۳۲ کلید — دکمه‌های InstantView/اینلاین‌بات داخل حباب):
#      روز چهار زبان ناهمگون بی‌سند (خاکستری EDEDED / سبزفام DCF4CB / آبی 229AF0 / سبز 53AB49)
#      و شب چیپ Default 17171A روی حباب 262017 = ۱٫۰۵:۱ (دکمهٔ نامرئی!) ←
#      زبان یکپارچهٔ M3: Default = چیپ تُنال جوهر×۱۲٪ روی بستر حباب خودش (پرس ×۲۰٪) با متن پیام؛
#      Primary = قرص اکسنت + onAccent (هم‌الگوی قدم ۱۵/۱۷/۲۰)؛ Danger/Success = تینت رنگ معنایی ×۱۲٪/×۲۰٪ با متن هم‌رنگ.
#   ۲) بج خطای ارسال: روز FF0000 خام ← قرمز معنایی B4382C؛ شب تعجب E5646C روی بج F6574E = ۱٫۰۸:۱ ← تعجب سفید.
#   ۳) آبی‌های خارج‌ازتوکن روز ← اکسنت: addContact 308ED0 / editMediaButton 1A9CFF /
#      messageLinkIn 127ACA / emojiPanelNewTrending 3FA4F0 (و SetNameHighlight از fallback آبی).
#   ۴) خانوادهٔ «رنگ روی مدیا» (۱۲ کلید): سفید/اسکریم خنثی آپستریم صریح شد؛ شب mediaViews
#      junk تیرهٔ 1A1A1C روی اسکریم تیره بود ← سفید. + previewDuration/Game + gifSaveHint + BlurAlpha.
#   ۵) پنل ایموجی (۸ کلید): روز خاکستری-آبی سرد بی‌سند (آیکون پک b1b6bc روی کرم ۱٫۷:۱!) ← dim/accent/text.
#   ۶) تماس سبز in/out (آپستریم 00C853 خارج‌ازتوکن) ← سبز معنایی پالت؛ برچسب‌های inAdmin صریح.
#   ۷) کروم کم‌حجم (۹ کلید): فید = رنگ بستر کم‌حجم (نه 121213 قدیمی)، محتوا = text/dim، خط گلس = روز ۲۴٪/شب صفر.
#   ۸) قفل هدر ← dim هم‌زبان آیکون‌های هدر.
#
# نکته‌های ممیزی (بدون تغییر):
#   • key_chat_messagePanelVoiceLock/Background/Shadow و key_chat_wallpaper_gradient_to2/to3 —
#     پیشوند key_ در attheme قرارداد عجیبِ خودِ colorKeysMap آپستریم است (کلید زنده؛ باگ نیست).
#   • key_chat_wallpaper_gradient_to1 در colorKeysMap به «chat_wallpaper_gradient_to» مپ می‌شود (پوشش داده شد).
#   • key_chat_outBubbleGradient1 صفرِ آگاهانه است: RichMessageLayout فقط به‌عنوان «آشکارساز حالت
#     گرادیان متن» مصرفش می‌کند؛ حباب ما جامد است و صفر = خاموشی مسیر گرادیان.
#   • chat_inAudioPerfomerText خانوادهٔ ۴گانه با املای آپستریم (Perfomer) از قدم ۲۶ در پالت است.
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
    r1, g1, b1 = rgb(fg)
    r2, g2, b2 = rgb(bg)
    ch = lambda f, b: int(round((f * fa + b * (255 - fa)) / 255.0))
    return (ch(r1, r2) << 16) | (ch(g1, g2) << 8) | ch(b1, b2)


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 340
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)
f_tiny = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 9 * S)


def draw_panel(x0, theme, caption, note):
    wall = theme["chat_wallpaper"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], fill=rgb(wall))
    cap = theme["actionBarDefaultSubtitle"]
    d.text((x0 + 12 * S, 10 * S), caption, font=f_small, fill=rgb(cap))
    d.text((x0 + 12 * S, 24 * S), note, font=f_small, fill=rgb(cap))

    text = theme["chat_messageTextIn"]
    out_text = theme["chat_messageTextOut"]
    in_bub = theme["chat_inBubble"]
    out_bub = theme["chat_outBubble"]
    accent = theme["chat_messageLinkIn"]  # اکسنت — با messageLinkOut/addContact یکی است
    on_accent = theme["chat_msgIvButtonPrimaryInText"]
    red = theme["chat_msgIvButtonDangerInText"]
    green = theme["chat_inGreenCall"]
    dim = theme["chat_emojiBottomPanelIcon"]
    hdr = theme["actionBarDefault"]
    hdr_txt = theme["actionBarDefaultTitle"]

    def chip(mxd, ydp, wdp, hdp, bgc, radius=10):
        d.rounded_rectangle([x0 + mxd * S, ydp * S, x0 + (mxd + wdp) * S, (ydp + hdp) * S],
                            radius=radius * S, fill=rgb(bgc))

    # ── ۱) هدر با قفل (گفت‌وگوی پنهان) — قفل = dim هم‌زبان آیکون‌های هدر ──
    d.rectangle([x0, 40 * S, x0 + W_DP * S, 66 * S], fill=rgb(hdr))
    d.text((x0 + 14 * S, 48 * S), "Secret chat", font=f_row, fill=rgb(hdr_txt))
    d.rounded_rectangle([x0 + 116 * S, 49 * S, x0 + 122 * S, 57 * S], radius=2 * S, fill=rgb(theme["chat_lockIcon"]))
    d.arc([x0 + 114.5 * S, 47 * S, x0 + 123.5 * S, 55 * S], 180, 360, fill=rgb(theme["chat_lockIcon"]), width=S)

    # ── ۲) حباب ورودی (سمت چپ) با ۴ دکمهٔ msgIv: Default/پرس/Primary/Danger ──
    bx, by, bw, bh = 12, 76, 196, 96
    d.rounded_rectangle([x0 + bx * S, by * S, x0 + (bx + bw) * S, (by + bh) * S], radius=13 * S, fill=rgb(in_bub))
    d.text((x0 + (bx + 12) * S, (by + 8) * S), "Open the article?", font=f_row, fill=rgb(text))
    chip(bx + 12, by + 30, 84, 24, theme["chat_msgIvButtonDefaultIn"], radius=12)
    d.text((x0 + (bx + 20) * S, (by + 36) * S), "Instant", font=f_row, fill=rgb(theme["chat_msgIvButtonDefaultInText"]))
    chip(bx + 104, by + 30, 80, 24, theme["chat_msgIvButtonDefaultInPressed"], radius=12)
    d.text((x0 + (bx + 114) * S, (by + 36) * S), "press 20%", font=f_row, fill=rgb(theme["chat_msgIvButtonDefaultInText"]))
    chip(bx + 12, by + 62, 84, 24, theme["chat_msgIvButtonPrimaryIn"], radius=12)
    d.text((x0 + (bx + 26) * S, (by + 68) * S), "Open", font=f_row, fill=rgb(on_accent))
    chip(bx + 104, by + 62, 80, 24, theme["chat_msgIvButtonDangerIn"], radius=12)
    d.text((x0 + (bx + 122) * S, (by + 68) * S), "Danger", font=f_row, fill=rgb(red))

    # ── ۳) مدیا (سمت راست، کنار حباب ورودی): چیپ‌های سفید خنثی + ویرایش اکسنت ──
    mx, my, mw, mh = 220, 76, 128, 96
    d.rounded_rectangle([x0 + (mx + 2) * S, (my + 2) * S, x0 + (mx + mw) * S + 2 * S, (my + mh) * S + 2 * S],
                        radius=13 * S, fill=rgb(composite(0x33000000, wall)))
    photo_top, photo_bot = (146, 122, 96), (94, 78, 62)
    for i in range(mh * S):
        t = i / (mh * S)
        col = tuple(int(photo_top[j] + (photo_bot[j] - photo_top[j]) * t) for j in range(3))
        d.line([x0 + mx * S, (my * S) + i, x0 + (mx + mw) * S, (my * S) + i], fill=col)
    tbg = theme["chat_mediaTimeBackground"]
    chip(mx + 8, my + 8, 40, 16, composite(tbg, (photo_top[0] << 16) | (photo_top[1] << 8) | photo_top[2]), radius=8)
    d.text((x0 + (mx + 14) * S, (my + 11) * S), "0:14", font=f_tiny, fill=rgb(theme["chat_mediaTimeText"]))
    d.text((x0 + (mx + 54) * S, (my + 11) * S), "12.4K views", font=f_tiny, fill=rgb(theme["chat_mediaViews"]))
    d.ellipse([x0 + (mx + mw - 30) * S, (my + mh - 30) * S, x0 + (mx + mw - 10) * S, (my + mh - 10) * S],
              fill=rgb(composite(0x66000000, 0x000000)))
    d.polygon([(x0 + (mx + mw - 22) * S, (my + mh - 24) * S), (x0 + (mx + mw - 22) * S, (my + mh - 16) * S),
               (x0 + (mx + mw - 15) * S, (my + mh - 20) * S)], fill=rgb(theme["chat_editMediaButton"]))
    d.text((x0 + (mx + 8) * S, (my + mh - 32) * S), "gif save hint", font=f_tiny, fill=rgb(theme["chat_gifSaveHintText"]))

    # ── ۴) ردیف تماس سبز (چپ) — سبز معنایی پالت ──
    cy = 182
    d.rounded_rectangle([x0 + 12 * S, cy * S, x0 + 140 * S, (cy + 62) * S], radius=13 * S, fill=rgb(in_bub))
    d.ellipse([x0 + 24 * S, (cy + 10) * S, x0 + 38 * S, (cy + 24) * S], outline=rgb(green), width=S)
    d.polygon([(x0 + 27.5 * S, (cy + 14.5) * S), (x0 + 34.5 * S, (cy + 14.5) * S), (x0 + 31 * S, (cy + 19) * S)], fill=rgb(green))
    d.text((x0 + 46 * S, (cy + 11) * S), "Missed call", font=f_row, fill=rgb(green))
    d.text((x0 + 46 * S, (cy + 29) * S), "Callback", font=f_row, fill=rgb(accent))
    d.text((x0 + 46 * S, (cy + 47) * S), "green = semantic", font=f_tiny, fill=rgb(dim))

    # ── ۵) حباب خروجی (راست) با Danger/Success خروجی + بج خطای ارسال ──
    ox, oy, ow, oh = 152, 182, 196, 62
    d.rounded_rectangle([x0 + ox * S, oy * S, x0 + (ox + ow) * S, (oy + oh) * S], radius=13 * S, fill=rgb(out_bub))
    d.text((x0 + (ox + 12) * S, (oy + 8) * S), "Retry sending?", font=f_row, fill=rgb(out_text))
    chip(ox + 12, oy + 30, 84, 24, theme["chat_msgIvButtonDangerOut"], radius=12)
    d.text((x0 + (ox + 28) * S, (oy + 36) * S), "Delete", font=f_row, fill=rgb(theme["chat_msgIvButtonDangerOutText"]))
    chip(ox + 104, oy + 30, 80, 24, theme["chat_msgIvButtonSuccessOut"], radius=12)
    d.text((x0 + (ox + 120) * S, (oy + 36) * S), "Retry", font=f_row, fill=rgb(theme["chat_msgIvButtonSuccessOutText"]))
    # بج خطا: مربع‌گرد sentError + تعجب سفید sentErrorIcon (۱۴dp — جای تایم در پایین حباب)
    ex, ey = ox + ow - 22, oy + oh - 22
    d.rounded_rectangle([x0 + ex * S, ey * S, x0 + (ex + 14) * S, (ey + 14) * S], radius=1 * S, fill=rgb(theme["chat_sentError"]))
    d.rectangle([x0 + (ex + 6) * S, (ey + 3) * S, x0 + (ex + 8) * S, (ey + 8) * S], fill=rgb(theme["chat_sentErrorIcon"]))
    d.rectangle([x0 + (ex + 6) * S, (ey + 10) * S, x0 + (ex + 8) * S, (ey + 12) * S], fill=rgb(theme["chat_sentErrorIcon"]))

    # ── ۶) چیپ «افزودن مخاطب» (اکسنت + تینت ×۱۰٪) و چیپ کم‌حجم (فید = بستر کم‌حجم) ──
    acy = 254
    d.rounded_rectangle([x0 + 12 * S, acy * S, x0 + 122 * S, (acy + 30) * S], radius=15 * S,
                        fill=rgb(composite((theme["chat_addContact"] & 0xFFFFFF) | (0x19 << 24), wall)))
    d.text((x0 + 30 * S, (acy + 8) * S), "Add contact", font=f_row, fill=rgb(theme["chat_addContact"]))
    cx2 = 134
    d.rounded_rectangle([x0 + cx2 * S, acy * S, x0 + (cx2 + 122) * S, (acy + 30) * S], radius=15 * S,
                        fill=rgb(theme["chat_compact_background"]))
    d.rectangle([x0 + cx2 * S, (acy + 24) * S, x0 + (cx2 + 122) * S, (acy + 30) * S], fill=rgb(theme["chat_compact_fadeEdge"]))
    d.text((x0 + (cx2 + 22) * S, (acy + 8) * S), "pull down", font=f_row, fill=rgb(theme["chat_compact_pullingDownText"]))
    d.text((x0 + 268 * S, (acy + 8) * S), "compact", font=f_tiny, fill=rgb(dim))

    # ── ۷) پنل ایموجی: تب‌های dim + نام پک + آیکون پک + ترندینگ اکسنت + متن خالی ──
    py = 296
    d.rectangle([x0, py * S, x0 + W_DP * S, (py + 38) * S], fill=rgb(theme["chat_emojiPanelBackground"]))
    for i in range(4):
        cxi = 24 + i * 30
        d.ellipse([x0 + (cxi - 4) * S, (py + 10) * S, x0 + (cxi + 4) * S, (py + 18) * S],
                  fill=rgb(theme["chat_emojiPanelIconSelected"] if i == 0 else theme["chat_emojiBottomPanelIcon"]))
    d.text((x0 + 150 * S, (py + 4) * S), "Amber Pack", font=f_row, fill=rgb(theme["chat_emojiPanelStickerSetName"]))
    d.rounded_rectangle([x0 + 246 * S, (py + 7) * S, x0 + 252 * S, (py + 17) * S], radius=2 * S,
                        outline=rgb(theme["chat_emojiPanelStickerSetNameIcon"]), width=S)
    d.text((x0 + 268 * S, (py + 4) * S), "New", font=f_row, fill=rgb(theme["chat_emojiPanelNewTrending"]))
    d.text((x0 + 150 * S, (py + 22) * S), "empty text dim / trending accent", font=f_tiny, fill=rgb(theme["chat_emojiPanelEmptyText"]))


draw_panel(12, day, "DAY  — unclear buttons eradicated (M3 one language)",
           "tonal chips / accent pill / semantic danger+success / white error badge")
draw_panel(12 + W_DP * S + 12, night, "NIGHT  — unclear buttons eradicated (M3 one language)",
           "default chip 3F3930 on 262017 was 1.05:1 before / now ~9:1")

out = os.path.join(ROOT, "download/ui2-step28-buttons-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    in_bub = t["chat_inBubble"]
    out_bub = t["chat_outBubble"]
    panel = t["chat_emojiPanelBackground"]
    rows = [
        ("msgIv Default text on tonal chip (in)", t["chat_msgIvButtonDefaultInText"], t["chat_msgIvButtonDefaultIn"]),
        ("msgIv Default text on tonal chip (out)", t["chat_msgIvButtonDefaultOutText"], t["chat_msgIvButtonDefaultOut"]),
        ("msgIv Default chip vs inBubble (shape)", t["chat_msgIvButtonDefaultIn"], in_bub),
        ("msgIv Primary text on accent pill", t["chat_msgIvButtonPrimaryInText"], t["chat_msgIvButtonPrimaryIn"]),
        ("msgIv Danger text on tint chip (in)", t["chat_msgIvButtonDangerInText"], t["chat_msgIvButtonDangerIn"]),
        ("msgIv Danger text on tint chip (out)", t["chat_msgIvButtonDangerOutText"], t["chat_msgIvButtonDangerOut"]),
        ("msgIv Success text on tint chip (in)", t["chat_msgIvButtonSuccessInText"], t["chat_msgIvButtonSuccessIn"]),
        ("msgIv Success text on tint chip (out)", t["chat_msgIvButtonSuccessOutText"], t["chat_msgIvButtonSuccessOut"]),
        ("sentError badge vs outBubble (shape)", t["chat_sentError"], out_bub),
        ("sentErrorIcon exclamation on badge", t["chat_sentErrorIcon"], t["chat_sentError"]),
        ("lock icon on header", t["chat_lockIcon"], t["actionBarDefault"]),
        ("addContact text on chip accent10% (wall)", t["chat_addContact"],
         composite(t["chat_addContact"] & 0x19FFFFFF | (0x19 << 24), t["chat_wallpaper"])),
        ("green call icon on inBubble (shape)", t["chat_inGreenCall"], in_bub),
        ("mediaViews on scrim worst (photo black)", t["chat_mediaViews"], 0x000000),
        ("emoji bottom tab on panel", t["chat_emojiBottomPanelIcon"], panel),
        ("sticker set name on panel", t["chat_emojiPanelStickerSetName"], panel),
        ("sticker set icon on panel (shape)", t["chat_emojiPanelStickerSetNameIcon"], panel),
        ("new trending on panel", t["chat_emojiPanelNewTrending"], panel),
        ("compact pull-down text on compact bg", t["chat_compact_pullingDownText"], t["chat_compact_background"]),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:44s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")
    print()

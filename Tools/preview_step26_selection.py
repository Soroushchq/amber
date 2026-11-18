#!/usr/bin/env python3
# UI2 قدم ۲۶ — پیش‌نمایش اکشن‌مود انتخاب پیام
# همهٔ رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
# کارهای این قدم (۹ کلید — صفر تغییر کد):
#   ۱) باگ اصلی — chat_selectedBackground در پالت نبود: آپستریم آبی 0x280a90f0 خارج‌ازتوکن؛ در
#      دستگاه‌های پرقدرت با والپیپر متحرک مسیر «پچ گرادیانِ خود والپیپر» جانشین می‌شد (هم‌الگوی
#      باگ چیپ سرویس قدم ۲۵ — ظاهر ناهمگون بین دستگاه‌ها). با تعریف صریح کلید، مسیر توکنی قطعی
#      می‌رود ← تینت اکسنت ×۰٫۱۵۶ (هم‌زبانهٔ چیپ ری‌اکشن غیرانتخاب‌شده)
#   ۲) chat_adminText/Selected (برچسب «مدیر» زیر نام) — آپستریم روز c0c6cb روی حباب کرم ۱٫۴۵:۱
#      ← dim (۴٫۲۹/۶٫۰۱)
#   ۳) chat_tagCreator/tagAdmin (نشان نقش) — بنفش/سبز خارج‌ازتوکن ← اکسنت (۳٫۶۲/۷٫۹۶)
#   ۴) خانوادهٔ mediaLoaderPhoto (اسکریم رادیال‌پروگرس روی مدیا) — مقادیر خنثی آپستریم صریح‌سازی شد
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


night = parse_theme(os.path.join(ASSETS, "amber.attheme"))
day = parse_theme(os.path.join(ASSETS, "amber_day.attheme"))

W_DP, H_DP = 360, 336
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
FONT = os.path.join(ASSETS, "fonts/ambergramui-med.ttf")
f_small = ImageFont.truetype(FONT, 10 * S)
f_row = ImageFont.truetype(FONT, 12 * S)
f_bar = ImageFont.truetype(FONT, 13 * S)


def checkmark(x, y, size, color):
    """تیک ساده داخل چک‌باکس"""
    s = size
    d.line([x + s * 0.22, y + s * 0.52, x + s * 0.42, y + s * 0.72], fill=color, width=S + 1)
    d.line([x + s * 0.42, y + s * 0.72, x + s * 0.80, y + s * 0.28], fill=color, width=S + 1)


def draw_panel(x0, theme, caption, wall_note):
    wp = Image.new("RGB", (W_DP * S, H_DP * S))
    c0, c1 = theme["chat_wallpaper"], theme["chat_wallpaper_gradient_to"]
    c2, c3 = theme["key_chat_wallpaper_gradient_to2"], theme["key_chat_wallpaper_gradient_to3"]
    px = wp.load()
    for yy in range(H_DP * S):
        v = yy / (H_DP * S - 1)
        for xx in range(0, W_DP * S, 4):
            u = xx / (W_DP * S - 1)
            col = rgb(blend(blend(c0, c1, u), blend(c2, c3, u), v))
            for k in range(4):
                if xx + k < W_DP * S:
                    px[xx + k, yy] = col
    img.paste(wp, (x0, 6))
    X = lambda dp: x0 + dp * S          # مختصات افقی dp → px
    Y = lambda dp: 6 + dp * S           # مختصات عمودی dp → px (پنل از y=6px)

    sel = theme["chat_selectedBackground"]
    inb = theme["chat_inBubble"]
    outb = theme["chat_outBubble"]
    inb_sel = composite(sel, inb)
    outb_sel = composite(sel, outb)
    accent = theme["chat_tagAdmin"]
    dim = theme["chat_adminText"]
    in_tx = theme["chat_messageTextIn"]
    out_tx = theme["chat_outFileInfoText"]
    bar_bg = theme["actionBarActionModeDefault"]
    bar_tx = theme["actionBarActionModeDefaultIcon"]

    # ── ۱) نوار اکشن‌مود (انتخاب پیام) — y ۰..۵۲dp ────────────────────
    d.rectangle([X(0), Y(0), X(W_DP), Y(52)], fill=rgb(bar_bg))
    cx = X(14)
    d.line([cx, Y(12), cx + 14 * S, Y(26)], fill=rgb(bar_tx), width=S + 1)
    d.line([cx + 14 * S, Y(12), cx, Y(26)], fill=rgb(bar_tx), width=S + 1)
    d.text((X(38), Y(13)), "3 selected", font=f_bar, fill=rgb(bar_tx))
    icons_x = X(W_DP - 116)
    d.rectangle([icons_x, Y(14), icons_x + 11 * S, Y(25)], outline=rgb(bar_tx), width=S)
    d.rectangle([icons_x + 4 * S, Y(10), icons_x + 15 * S, Y(21)], outline=rgb(bar_tx), width=S)
    fx = icons_x + 44 * S
    d.polygon([(fx, Y(12)), (fx + 18 * S, Y(19)), (fx, Y(26))], outline=rgb(bar_tx), width=S)
    tx = icons_x + 84 * S
    d.rectangle([tx, Y(12), tx + 14 * S, Y(26)], outline=rgb(bar_tx), width=S)
    d.line([tx - 2 * S, Y(12), tx + 16 * S, Y(12)], fill=rgb(bar_tx), width=S + 1)
    d.text((X(12), Y(56)), caption, font=f_small, fill=rgb(in_tx))

    # ── ۲) پیام ورودی انتخاب‌شده + برچسب «مدیر» + چک‌باکس + هایلایت پرش ──
    d.rectangle([X(0), Y(74), X(W_DP), Y(144)], fill=argb_tuple(sel))
    bx0, by0, bx1, by1 = X(44), Y(80), X(300), Y(138)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=14 * S, fill=rgb(inb_sel))
    d.text((X(56), Y(87)), "Sara", font=f_small, fill=rgb(accent))
    d.text((X(88), Y(87)), "admin", font=f_small, fill=rgb(dim))
    d.text((X(56), Y(104)), "message selected — jump highlight", font=f_row, fill=rgb(in_tx))
    cbx, cby, cbs = X(310), Y(92), 20 * S
    d.rounded_rectangle([cbx, cby, cbx + cbs, cby + cbs], radius=6 * S,
                        fill=rgb(theme["chat_attachCheckBoxBackground"]))
    checkmark(cbx, cby, cbs, rgb(theme["chat_attachCheckBoxCheck"]))

    # ── ۳) پیام صوتی خروجی انتخاب‌شده + خط performer ─────────────────
    ox0, oy0, ox1, oy1 = X(60), Y(152), X(316), Y(212)
    d.rounded_rectangle([ox0, oy0, ox1, oy1], radius=14 * S, fill=rgb(outb_sel))
    d.text((X(72), Y(158)), "AmberGram UI · voice note", font=f_small,
           fill=rgb(theme["chat_outAudioPerfomerText"]))
    d.text((X(72), Y(172)), "0:42", font=f_row, fill=rgb(out_tx))
    for i in range(14):
        wx = X(132) + i * 9 * S
        wh = (6 + (i * 7) % 18) * S
        d.line([wx, Y(182) - wh // 2, wx, Y(182) + wh // 2],
               fill=rgb(theme["chat_outAudioSeekbarFill"]), width=S + 1)
    cbs2 = 20 * S
    cbx2, cby2 = X(326), Y(164)
    d.rounded_rectangle([cbx2, cby2, cbx2 + cbs2, cby2 + cbs2], radius=6 * S,
                        fill=rgb(theme["chat_attachCheckBoxBackground"]))
    checkmark(cbx2, cby2, cbs2, rgb(theme["chat_attachCheckBoxCheck"]))

    # ── ۴) مقایسهٔ قدیم/جدید بسترهٔ انتخاب ────────────────────────────
    old = composite(0x280A90F0, inb)  # آبی آپستریم
    new = inb_sel
    py = 226
    d.rounded_rectangle([X(40), Y(py), X(160), Y(py + 26)], radius=13 * S, fill=rgb(old))
    d.text((X(62), Y(py + 8)), "old blue", font=f_small, fill=(255, 255, 255))
    d.rounded_rectangle([X(200), Y(py), X(320), Y(py + 26)], radius=13 * S, fill=rgb(new))
    d.text((X(226), Y(py + 8)), "new token", font=f_small, fill=rgb(in_tx))
    d.text((X(12), Y(py + 32)), wall_note, font=f_small, fill=(215, 170, 120))

    # ── ۵) اسکریم رادیال‌پروگرس روی مدیا + نشان نقش ───────────────────
    mx0, my0, mx1, my1 = X(40), Y(272), X(148), Y(328)
    for yy in range(my0, my1):
        t = (yy - my0) / (my1 - my0)
        d.line([mx0, yy, mx1, yy], fill=rgb(blend(theme["chat_outFileBackground"], theme["chat_inFileBackground"], t)))
    d.rectangle([mx0, my0, mx1, my1], fill=argb_tuple(theme["chat_mediaLoaderPhoto"]))
    d.arc([mx0 + 40 * S, my0 + 14 * S, mx0 + 66 * S, my0 + 40 * S], 0, 300,
          fill=rgb(theme["chat_mediaLoaderPhotoIcon"]), width=S + 1)
    d.text((mx0 + 8 * S, my1 - 14 * S), "media scrim", font=f_small,
           fill=rgb(theme["chat_mediaLoaderPhotoIcon"]))
    d.text((X(170), Y(280)), "admin role badge", font=f_small, fill=rgb(accent))
    d.text((X(170), Y(296)), "creator / admin label", font=f_small, fill=rgb(dim))


draw_panel(12, day, "DAY  — selection action mode (9 keys, zero code change)",
           "was: upstream blue 0x280a90f0 / gradient patch on motion wallpaper")
draw_panel(12 + W_DP * S + 12, night, "NIGHT  — selection action mode (uniform token tint)",
           "was: blue overlay off-brand + admin label c0c6cb cold gray")

out = os.path.join(ROOT, "download/ui2-step26-selection-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    sel = t["chat_selectedBackground"]
    inb_sel = composite(sel, t["chat_inBubble"])
    outb_sel = composite(sel, t["chat_outBubble"])
    old_inb = composite(0x280A90F0, t["chat_inBubble"])
    rows = [
        ("selected in-bubble text (was upstream blue)", t["chat_messageTextIn"], inb_sel),
        ("selected out-bubble secondary text", t["chat_outFileInfoText"], outb_sel),
        ("OLD upstream blue overlay + text", t["chat_messageTextIn"], old_inb),
        ("admin label on in-bubble (was c0c6cb 1.45 day)", t["chat_adminText"], t["chat_inBubble"]),
        ("tag/badge accent on in-bubble (was 955CDB/40A920)", t["chat_tagAdmin"], t["chat_inBubble"]),
        ("action-mode title/count on bar", t["actionBarActionModeDefaultIcon"], t["actionBarActionModeDefault"]),
        ("action-mode icon on bar", t["actionBarActionModeDefaultIcon"], t["actionBarActionModeDefault"]),
        ("media loader icon on 40% scrim", t["chat_mediaLoaderPhotoIcon"], 0x33000000),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:50s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")
    print()

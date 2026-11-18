#!/usr/bin/env python3
# UI2 قدم ۲۷ — پیش‌نمایش منوهای سه‌نقطهٔ چت (ساب‌منو با سطح پله‌ای)
# همه رنگ‌ها مستقیم از فایل‌های attheme تازه‌ساخته پارس می‌شوند.
#
# ممیزی این قدم:
#   خانوادهٔ منو از قدم ۱۶ پالتی بود و تأیید شد — popup ۹-پیچ با MULTIPLY تینت
#   actionBarDefaultSubmenuBackground=سطح کارت (روز F3ECE2 / شب 241D14)، متن/آیکون آیتم
#   = text/dim، ساب‌منوی تو در تو (PopupSwipeBackLayout) همان کلید بستره + دیم ۲۵٪ مشکی،
#   GapView = جداکنندهٔ مشتق (بستره−۱۰) + سایهٔ greydivider (windowBackgroundGrayShadow پالتی)،
#   منوی اورلی گلس چت = تینت هدر ۸۵٪ روی بلور (topPanelChatActivity — از توکن هدر می‌آید)،
#   انتخابگر آیتم = dialogButtonSelector (اکسنت×۱۰٪) / مسیر ItemOptions = متن×۱۲٪،
#   آیتم قرمز = text_RedRegular پالتی، گپ = متن×۶٪ مشتق، دیم اورلی = مشکی ۱۰٪ ثابت نوری.
#
# رفع این قدم — سه کلید گلس کم‌حجم (chat_compact_glass{Shadow,Outline,Hairline}):
#   در پالت نبودند؛ شب صریحاً صفر بود ولی روز اصلاً کلید نداشت و پیش‌فرض‌های آپستریم
#   (Outline 14٪ / Shadow 8٪ / Hairline 5٪ مشکی) بی‌سند اعمال می‌شد؛ حالا هر دو حالت صریح‌اند:
#   روز همان تینت‌های خنثی آپستریم (تعریف قرص تخت هدر روی کرم) / شب صفرِ سندشده.
#   این سه کلید در حالت کم‌حجم، سایه/خط منوی اورلی را هم کنترل می‌کنند (isCompactMode override
#   در topPanelChatActivity) — پس خانوادهٔ «سطح پله‌ای منو» کامل شد.
#
# نکتهٔ ممیزی: actionBarDefaultSubmenuSeparator در attheme می‌آید ولی Theme.java همیشه موقع
# اعمال تم آن را از بستره (−۱۰RGB) بازنویسی می‌کند → کلیدِ مرده؛ ارزش پالتش فقط سندِ صدای مشتق است.
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

W_DP, H_DP = 360, 320
img = Image.new("RGB", (W_DP * S * 2 + 24, H_DP * S + 40), (14, 12, 10))
d = ImageDraw.Draw(img, "RGBA")
f_small = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 10 * S)
f_row = ImageFont.truetype(os.path.join(ASSETS, "fonts/ambergramui-med.ttf"), 12 * S)


def draw_panel(x0, theme, caption, note):
    wall = theme["chat_wallpaper"]
    d.rectangle([x0, 6, x0 + W_DP * S, 6 + H_DP * S], fill=rgb(wall))
    cap = theme["actionBarDefaultSubtitle"]  # dim — خوانا روی هر دو وایپرپ
    d.text((x0 + 12 * S, 10 * S), caption, font=f_small, fill=rgb(cap))
    d.text((x0 + 12 * S, 24 * S), note, font=f_small, fill=rgb(cap))

    text = theme["actionBarDefaultSubmenuItem"]
    dim = theme["actionBarDefaultSubmenuItemIcon"]
    surface = theme["actionBarDefaultSubmenuBackground"]
    red = theme["text_RedRegular"]
    press = composite(theme["dialogButtonSelector"], surface)

    def row(mxd, ydp, label, color, ic=dim, pressed=False):
        """ردیف آیتم؛ mxd مطلق نسبت به x0 است"""
        if pressed:
            d.rounded_rectangle([x0 + (mxd + 8) * S, (ydp - 5) * S, x0 + (mxd + mw - 8) * S, (ydp + 17) * S],
                                radius=12 * S, fill=rgb(press))
        d.ellipse([x0 + (mxd + 16) * S, (ydp + 4) * S, x0 + (mxd + 22) * S, (ydp + 10) * S], fill=rgb(ic))
        d.text((x0 + (mxd + 30) * S, ydp * S), label, font=f_row, fill=rgb(color))

    # ── ۱) پاپ‌آپ کلاسیک (سطح پلهٔ کارت — SHAPE_MENU=20 / ردیف=12) ──
    mx, my, mw, mh = 20, 54, 168, 190
    d.rounded_rectangle([x0 + (mx + 3) * S, (my + 3) * S, x0 + (mx + mw) * S + 3 * S, (my + mh) * S + 3 * S],
                        radius=20 * S, fill=rgb(composite(0x28000000, wall)))  # سایهٔ ۹-پیچ
    d.rounded_rectangle([x0 + mx * S, my * S, x0 + (mx + mw) * S, (my + mh) * S],
                        radius=20 * S, fill=rgb(surface))

    row(mx, my + 14, "Select messages", text, pressed=True)
    row(mx, my + 46, "Change wallpaper", text)
    # گپ سکشن (GapView): بستره = جداکنندهٔ مشتق (بستره−۱۰RGB، آلفای خود بستره) + سایهٔ greydivider پالتی
    sep = 0xFF000000 | ((max((surface >> 16 & 255) - 10, 0)) << 16) | ((max((surface >> 8 & 255) - 10, 0)) << 8) | (max((surface & 255) - 10, 0))
    gy = my + 74
    d.rectangle([x0 + mx * S, gy * S, x0 + (mx + mw) * S, (gy + 20) * S],
                fill=rgb(composite(0x14211A12 if theme is day else 0x28000000, sep)))
    d.text((x0 + (mx + 12) * S, (gy + 4) * S), "chat settings", font=f_small, fill=rgb(dim))
    row(mx, my + 102, "Autodelete", text)
    row(mx, my + 134, "Delete chat", red)

    # ── ۲) ساب‌منوی پله‌ای: والد دیم ۲۵٪ (ردیف‌ها زیر دیم دیده می‌شوند) + صفحهٔ تو در تو ──
    nx, ny, nw, nh = mx + mw + 14, my + 24, 132, 130
    d.rounded_rectangle([x0 + mx * S, my * S, x0 + (mx + mw) * S, (my + mh) * S],
                        radius=20 * S, fill=(0, 0, 0, 64))  # دیم انتقال ۲۵٪ (ترکیب نرم)
    d.rounded_rectangle([x0 + (nx + 3) * S, (ny + 3) * S, x0 + (nx + nw) * S + 3 * S, (ny + nh) * S + 3 * S],
                        radius=20 * S, fill=rgb(composite(0x28000000, wall)))
    d.rounded_rectangle([x0 + nx * S, ny * S, x0 + (nx + nw) * S, (ny + nh) * S],
                        radius=20 * S, fill=rgb(surface))
    row(nx, ny + 14, "1 hour", text)
    row(nx, ny + 42, "1 day", text)
    row(nx, ny + 70, "1 week", text)
    row(nx, ny + 100, "Off", dim)

    # ── ۳) منوی اورلی گلس چت (⋮): تینت هدر ۸۵٪ روی بلور وایپرپ ──
    gx, gy2, gw, gh = 20, 246, 190, 56
    hdr = theme["chat_topPanelBackground"]
    glass = composite((217 << 24) | (hdr & 0xFFFFFF), wall)  # آلفا ۸۵٪ = 217/255
    d.rounded_rectangle([x0 + gx * S, gy2 * S, x0 + (gx + gw) * S, (gy2 + gh) * S],
                        radius=22 * S, fill=rgb(glass))
    d.ellipse([x0 + (gx + 12) * S, (gy2 + 10) * S, x0 + (gx + 18) * S, (gy2 + 16) * S], fill=rgb(dim))
    d.text((x0 + (gx + 26) * S, (gy2 + 8) * S), "Add to home screen", font=f_row, fill=rgb(text))
    d.ellipse([x0 + (gx + 12) * S, (gy2 + 36) * S, x0 + (gx + 18) * S, (gy2 + 42) * S], fill=rgb(dim))
    d.text((x0 + (gx + 26) * S, (gy2 + 34) * S), "Clear history", font=f_row, fill=rgb(text))

    # ── ۴) گلس کم‌حجم (رفع این قدم): قرص تخت هدر + خط‌های صریح ──
    cx, cy2, cw, chh = 230, 250, 110, 40
    comp_canvas = theme["chat_compact_background"]
    d.rounded_rectangle([x0 + cx * S, cy2 * S, x0 + (cx + cw) * S, (cy2 + chh) * S],
                        radius=23 * S, fill=rgb(comp_canvas))
    sh_key = theme["chat_compact_glassShadow"]
    ol_key = theme["chat_compact_glassOutline"]
    if (sh_key & 0xFF000000) > 0 or (ol_key & 0xFF000000) > 0:
        d.rounded_rectangle([x0 + cx * S, cy2 * S, x0 + (cx + cw) * S, (cy2 + chh) * S],
                            radius=23 * S, outline=rgb(composite(ol_key, comp_canvas)), width=S)
        d.rounded_rectangle([x0 + (cx + 1) * S, (cy2 + 2) * S, x0 + (cx + cw + 1) * S, (cy2 + chh + 1) * S],
                            radius=23 * S, fill=rgb(composite(sh_key, comp_canvas)))
    d.rounded_rectangle([x0 + cx * S, cy2 * S, x0 + (cx + cw) * S, (cy2 + chh) * S],
                        radius=23 * S, fill=rgb(hdr))
    d.ellipse([x0 + (cx + 12) * S, (cy2 + 15) * S, x0 + (cx + 20) * S, (cy2 + 23) * S],
              fill=rgb(theme["actionBarDefaultIcon"]))
    d.ellipse([x0 + (cx + cw - 26) * S, (cy2 + 15) * S, x0 + (cx + cw - 18) * S, (cy2 + 23) * S],
              fill=rgb(theme["actionBarDefaultIcon"]))
    d.text((x0 + cx * S, (cy2 + chh + 6) * S),
           "compact glass explicit" if theme is day else "compact glass zeros",
           font=f_small, fill=rgb(cap))
    d.text((x0 + gx * S, (gy2 + gh + 6) * S),
           "glass menu = header 85% over blur",
           font=f_small, fill=rgb(cap))


draw_panel(12, day, "DAY  — chat three-dot menus (tiered surfaces)",
           "popup = card tier on paper / glass = header tier / nested = own tier")
draw_panel(12 + W_DP * S + 12, night, "NIGHT  — chat three-dot menus (tiered surfaces)",
           "popup 241D14 lighter than bg / glass = header 85% over blur")

out = os.path.join(ROOT, "download/ui2-step27-menus-preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("saved", out)

print("\n== contrast report ==")
W_TOP, W_MID = 0xFFF6EA, 0xFF17130E
for name_, t in (("DAY  ", day), ("NIGHT", night)):
    surface = t["actionBarDefaultSubmenuBackground"]
    press = composite(t["dialogButtonSelector"], surface)
    hdr = t["chat_topPanelBackground"]
    glass = composite((217 << 24) | (hdr & 0xFFFFFF), t["chat_wallpaper"])
    worst_glass = composite((217 << 24) | (hdr & 0xFFFFFF), W_MID if t is day else 0xFFF5EFE4)
    rows = [
        ("submenu item text on popup surface", t["actionBarDefaultSubmenuItem"], surface),
        ("submenu item icon on popup surface", t["actionBarDefaultSubmenuItemIcon"], surface),
        ("pressed item text on surface+accent10%", t["actionBarDefaultSubmenuItem"], press),
        ("red item on popup surface", t["text_RedRegular"], surface),
        ("item text on glass menu (85% header)", t["actionBarDefaultSubmenuItem"], glass),
        ("item text on glass WORST stop", t["actionBarDefaultSubmenuItem"], worst_glass),
        ("gap hairline vs surface (decorative)",
         0xFF000000 | ((max((surface >> 16 & 255) - 10, 0)) << 16) | ((max((surface >> 8 & 255) - 10, 0)) << 8) | (max((surface & 255) - 10, 0)),
         surface),
    ]
    for label, fg, bg in rows:
        print(f"{name_} {label:48s} #{fg & 0xFFFFFF:06X} on #{bg & 0xFFFFFF:06X}  {ratio(fg, bg):5.2f}:1")
    print()

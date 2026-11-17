#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
قدم ۱۶ — بازتولید ۹-پیچ‌های کارت منو (popup_fixed_alert4 / popup_fixed_alert2)

کانسپت C — Expressive Material:
  · شعاع کارت منو از ۱۲dp آپستریم به توکن SHAPE_MENU (۲۰dp) — هم‌زبان کارت ردیف چت (قدم ۱۳)
  · هندسه (حاشیه سایه، عرض کارت نمونه، راهنمای کشسانی) حفظ/کالیبره می‌شود
  · بدنه کارت سفید خالص می‌ماند — تینت MULTIPLY با key_actionBarDefaultSubmenuBackground
    رنگ نهایی (روز DAY_SURFACE گرم / شب NIGHT_SURFACE) و سایه را خودکار گرم می‌کند
  · پروفایل آلفای سایه از هر فایل اصلی همان density نمونه‌برداری و بازسازی می‌شود

همه مقادیر از AmberTokens.java پارس می‌شود (تک منبع حقیقت).
"""
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'TMessagesProj', 'src', 'main', 'res')
TOKENS = os.path.join(ROOT, 'TMessagesProj', 'src', 'main', 'java', 'org', 'telegram', 'messenger', 'AmberTokens.java')

DENSITIES = [('mdpi', 1.0), ('hdpi', 1.5), ('xhdpi', 2.0), ('xxhdpi', 3.0)]
ASSETS = ['popup_fixed_alert4', 'popup_fixed_alert2']
SS = 4  # سوپرسمپلینگ


def parse_shape_menu():
    src = open(TOKENS, encoding='utf-8').read()
    m = re.search(r'SHAPE_MENU\s*=\s*([\d.]+)f', src)
    if not m:
        sys.exit('SHAPE_MENU not found in AmberTokens.java')
    return float(m.group(1))


def guides(img_arr):
    """راهنماهای ۹-پیچ از بوردر ۱px"""
    h, w = img_arr.shape[:2]
    top = np.where((img_arr[0, :, 3] > 0) & (img_arr[0, :, 0] < 60))[0]
    left = np.where((img_arr[:, 0, 3] > 0) & (img_arr[:, 0, 1] < 60))[0]
    bottom = np.where((img_arr[h - 1, :, 3] > 0) & (img_arr[h - 1, :, 0] < 60))[0]
    right = np.where((img_arr[:, w - 1, 3] > 0) & (img_arr[:, w - 1, 1] < 60))[0]
    return (int(top.min()), int(top.max())) if len(top) else None, \
           (int(left.min()), int(left.max())) if len(left) else None, \
           (int(bottom.min()), int(bottom.max())) if len(bottom) else None, \
           (int(right.min()), int(right.max())) if len(right) else None


def shadow_profile(inner, x0, y0, x1, y1):
    """پروفایل آلفای سایه از لبه چپ کارت در ارتفاع میانی (خارج‌رو)"""
    y = (y0 + y1) // 2
    prof = []
    for x in range(x0 - 1, 0, -1):
        a = int(inner[y, x, 3])
        if a == 0:
            break
        prof.append(a)
    return prof or [0]


def build_card_and_shadow(card_w, card_h, radius, profile, M):
    """لایه آلفا: بدنه کارت + سایه (سوپرسمپلینگ 4x)"""
    w_in = (M * 2 + card_w) * SS
    h_in = (M * 2 + card_h) * SS
    ss_radius = radius * SS
    ss_M = M * SS

    shadow = Image.new('L', (w_in, h_in), 0)
    sd = ImageDraw.Draw(shadow)
    # مستطیل‌های هم‌مرکز از بیرونی‌ترین (کم‌آلفا) به درونی‌ترین (پرآلفا) — جایگزینی max
    L = len(profile)
    for k in range(L - 1, -1, -1):
        a = profile[k]
        if a <= 0:
            continue
        grow = (k + 1) * SS  # فاصله از لبه کارت (d = k+1)
        box = [ss_M - grow, ss_M - grow, ss_M + card_w * SS + grow - 1, ss_M + card_h * SS + grow - 1]
        sd.rounded_rectangle(box, radius=ss_radius + grow, fill=a)

    card = Image.new('L', (w_in, h_in), 0)
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([ss_M, ss_M, ss_M + card_w * SS - 1, ss_M + card_h * SS - 1],
                         radius=ss_radius, fill=255)

    shadow = shadow.resize((M * 2 + card_w, M * 2 + card_h), Image.LANCZOS)
    card = card.resize((M * 2 + card_w, M * 2 + card_h), Image.LANCZOS)

    s_arr = np.array(shadow).astype(np.int32)
    c_arr = np.array(card).astype(np.int32)
    alpha = np.maximum(s_arr, c_arr)
    rgb = np.where(c_arr > 0, 255, 0)  # بدنه سفید، سایه خاکستری-سیاه (تینت MULTIPLY بعداً)
    out = np.zeros((M * 2 + card_h, M * 2 + card_w, 4), dtype=np.uint8)
    out[..., 0] = rgb
    out[..., 1] = rgb
    out[..., 2] = rgb
    out[..., 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    return out


def write_9patch(path, inner_arr, guides_xy, size):
    """نوشتن فایل نهایی با بوردر راهنما"""
    g_top, g_left, g_bottom, g_right = guides_xy
    h, w = size
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[1:h - 1, 1:w - 1] = inner_arr

    def paint_line(arr, coords):
        for i in coords:
            arr[i] = (0, 0, 0, 255)

    if g_top:
        paint_line(out[0, :, :], range(g_top[0], g_top[1] + 1))
    if g_left:
        paint_line(out[:, 0, :], range(g_left[0], g_left[1] + 1))
    if g_bottom:
        paint_line(out[h - 1, :, :], range(g_bottom[0], g_bottom[1] + 1))
    if g_right:
        paint_line(out[:, w - 1, :], range(g_right[0], g_right[1] + 1))

    Image.fromarray(out).save(path)
    return h, w


def main():
    shape_menu = parse_shape_menu()
    print(f'SHAPE_MENU = {shape_menu}dp (از AmberTokens)')

    report = []
    for name in ASSETS:
        for density, s in DENSITIES:
            src_path = os.path.join(RES, f'drawable-{density}', f'{name}.9.png')
            if not os.path.exists(src_path):
                report.append(f'{name}/{density}: MISSING — skip')
                continue
            orig = np.array(Image.open(src_path).convert('RGBA'))
            H, W = orig.shape[:2]
            inner = orig[1:H - 1, 1:W - 1]
            alpha = inner[..., 3]
            ys, xs = np.where(alpha == 255)
            x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
            M = x0  # حاشیه سایه (بالا/چپ == پایین/راست در آپستریم)
            card_w = x1 - x0 + 1
            card_h = y1 - y0 + 1

            R = int(round(shape_menu * s))
            min_h = 2 * R + int(round(12 * s))  # ۱۲dp فضای کشسانی عمودی
            new_card_h = max(card_h, min_h)

            g_top_o, g_left_o, g_bottom_o, g_right_o = guides(orig)
            prof = shadow_profile(inner, x0, y0, x1, y1)

            # راهنمای کشسانی افقی: داخل کارت و بیرون از قوس گوشه‌ها (full coords)
            cx0 = x0 + 1  # full coords (بوردر ۱px)
            cx1 = cx0 + card_w - 1
            h_lo, h_hi = cx0 + R + 1, cx1 - R - 1
            if g_top_o and h_lo <= h_hi and h_lo <= g_top_o[0] and g_top_o[1] <= h_hi:
                g_top = g_top_o
            else:
                mid = (h_lo + h_hi) // 2
                g_top = (mid - 8, mid + 8) if h_hi - h_lo >= 16 else (h_lo, h_hi)
                g_top = (max(h_lo, g_top[0]), min(h_hi, g_top[1]))

            cy0 = y0 + 1
            cy1 = cy0 + new_card_h - 1
            v_lo, v_hi = cy0 + R + 1, cy1 - R - 1
            if g_left_o and v_lo <= v_hi and v_lo <= g_left_o[0] and g_left_o[1] <= v_hi:
                g_left = g_left_o
            else:
                mid = (v_lo + v_hi) // 2
                g_left = (max(v_lo, mid - 16), min(v_hi, mid + 16))

            g_bottom = (cx0, cx1)
            g_right = (cy0, cy1)

            inner_arr = build_card_and_shadow(card_w, new_card_h, R, prof, M)
            new_H = new_card_h + 2 * M + 2
            new_W = card_w + 2 * M + 2
            write_9patch(src_path, inner_arr, (g_top, g_left, g_bottom, g_right), (new_H, new_W))
            report.append(f'{name}/{density}: card {card_w}x{card_h} → {card_w}x{new_card_h} (R={R}, M={M}) '
                          f'total {W}x{H} → {new_W}x{new_H} | guides T{g_top} L{g_left}')

    for line in report:
        print(line)

    # ── راستی‌آزمایی ──
    print('\n── verification ──')
    ok = True
    for name in ASSETS:
        for density, s in DENSITIES:
            path = os.path.join(RES, f'drawable-{density}', f'{name}.9.png')
            if not os.path.exists(path):
                continue
            arr = np.array(Image.open(path).convert('RGBA'))
            H, W = arr.shape[:2]
            inner = arr[1:H - 1, 1:W - 1]
            alpha = inner[..., 3]
            ys, xs = np.where(alpha >= 240)  # بدنه کارت (LANCZOS لبه را کمی نرم می‌کند)
            x0, y0 = int(xs.min()), int(ys.min())
            x1, y1 = int(xs.max()), int(ys.max())
            R = int(round(shape_menu * s))
            # شعاع: نسبت حذف‌شده بلوک گوشه بالا-چپ باید ≈ π/4 (ربع‌دایره) باشد — بی‌مقیاس
            block = alpha[y0:y0 + R, x0:x0 + R]
            removed = float((block < 240).mean())
            radius_ok = abs(removed - (1 - np.pi / 4)) < 0.06
            gt, gl, gb, gr = guides(arr)
            checks = [
                ('fill white', inner[(y0 + y1) // 2, (x0 + x1) // 2, 0] == 255 and inner[(y0 + y1) // 2, (x0 + x1) // 2, 3] == 255),
                ('radius≈SHAPE_MENU', radius_ok),
                (f'corner-removed={removed:.3f}≈{1-np.pi/4:.3f}', radius_ok),
                ('guides exist', all([gt, gl, gb, gr])),
                ('h-guide in card', gb[0] <= gt[0] and gt[1] <= gb[1]),
                ('v-guide in card', gr[0] <= gl[0] and gl[1] <= gr[1]),
                ('shadow margin', x0 >= int(6 * s) and y0 >= int(6 * s)),
            ]
            line = f'{name}/{density}: '
            for label, passed in checks:
                line += f'{label}={"OK" if passed else "FAIL"} '
                if not passed:
                    ok = False
            print(line)
    print('\nRESULT:', 'ALL OK' if ok else 'FAILURES PRESENT')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UI2 قدم ۲۹ — ابزار بازتولید ۹-پچ کارت پاپ‌آپ/دیالوگ (popup_fixed_alert*)
#
# شعاع کارت در asset آپستریم (~۱۶dp) به توکن SHAPE_DIALOG (۲۸dp) ارتقا می‌یابد.
# مدل بازسازی از خودِ asset فعلی استخراج می‌شود:
#   کارت = مستطیل‌گرد سفید مات + لبهٔ AA + هالهٔ سفید (~۳px) + سایهٔ مشکی نرم (~۱۷px @3x)
# پروفایل‌های H[d] (هاله) و B[d] (سایه) از چهار خط میانی لبهٔ کارت asset فعلی
# نمونه‌برداری و برای شکل جدید (شعاع بزرگ‌تر + ابعاد بزرگ‌تر برای جا گرفتن گوشه‌ها)
# بازاعمال می‌شوند. ابرنمونه‌برداری ۴x برای AA تمیز؛ مارکرهای ۹-پچ با نرخ فعلی بازساخته می‌شوند.
#
# کاربرد:
#   python3 Tools/regenerate_popup_9patch.py popup_fixed_alert4 28
import math
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
SCALES = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0}
SS = 4  # supersample


def ranges(markers):
    if not markers:
        return []
    out = []
    s = markers[0]
    p = markers[0]
    for v in markers[1:]:
        if v == p + 1:
            p = v
        else:
            out.append((s, p))
            s = v
            p = v
    out.append((s, p))
    return out


def marker_pixels(px, w, h):
    top = [x for x in range(w) if px[x, 0][3] > 128]
    left = [y for y in range(h) if px[0, y][3] > 128]
    bottom = [x for x in range(w) if px[x, h - 1][3] > 128]
    right = [y for y in range(h) if px[w - 1, y][3] > 128]
    return ranges(top), ranges(left), ranges(bottom), ranges(right)


def card_box(px, w, h):
    # مستطیل کارت: ردیف‌هایی که بیش از ۳۰٪ عرضشان مات کامل است
    rows = []
    for y in range(1, h - 1):
        cnt = sum(1 for x in range(1, w - 1) if px[x, y][3] >= 250)
        if cnt > (w - 2) * 0.30:
            rows.append(y)
    cols = []
    top, bot = rows[0], rows[-1]
    for x in range(1, w - 1):
        cnt = sum(1 for y in range(top, bot + 1) if px[x, y][3] >= 250)
        if cnt > (bot - top) * 0.30:
            cols.append(x)
    return cols[0], top, cols[-1], bot


def is_white(p):
    r, g, b, a = p
    return r > 180 and g > 180 and b > 180


def is_black(p):
    r, g, b, a = p
    return r < 90 and g < 90 and b < 90


def sample_profiles(px, w, h, box):
    # پروفایل فاصله‌محور از چهار خط میانی؛ H = هالهٔ سفید، B = سایهٔ مشکی
    L, T, R, B = box
    midy = (T + B) // 2
    midx = (L + R) // 2
    maxd = 64
    Hs, Bs = [0.0] * (maxd + 1), [0.0] * (maxd + 1)
    cnts = [0] * (maxd + 1)
    dirs = [
        ("left", lambda d: (L - d, midy)),
        ("right", lambda d: (R + d, midy)),
        ("top", lambda d: (midx, T - d)),
        ("bottom", lambda d: (midx, B + d)),
    ]
    lastB = 18.0  # مقدار اولیهٔ سایهٔ زیر هاله (نامرئی زیر هالهٔ مات است)
    for name, pt in dirs:
        lb = None
        for d in range(1, maxd + 1):
            x, y = pt(d)
            if not (0 <= x < w and 0 <= y < h):
                break
            p = px[x, y]
            if p[3] == 0:
                break
            if is_white(p):
                Hs[d] += p[3]
                Bs[d] += lb if lb is not None else lastB  # سایهٔ پنهان زیر هاله
            elif is_black(p):
                Bs[d] += p[3]
                Hs[d] += 0
                lb = p[3]
            cnts[d] += 1
        if lb is not None:
            lastB = lb
    B_arr = [Bs[d] / cnts[d] if cnts[d] else 0 for d in range(maxd + 1)]
    H_arr = [Hs[d] / cnts[d] if cnts[d] else 0 for d in range(maxd + 1)]
    return H_arr, B_arr


def sdf_round_rect(px, py, half_w, half_h, r):
    # فاصلهٔ علامت‌دار؛ خروجی مثبت = بیرون کارت
    qx = abs(px) - (half_w - r)
    qy = abs(py) - (half_h - r)
    outside = math.hypot(max(qx, 0.0), max(qy, 0.0))
    inside = min(max(qx, qy), 0.0)
    return outside + inside - r


def interp(arr, x):
    i = int(x)
    if i >= len(arr) - 1:
        return arr[-1]
    f = x - i
    return arr[i] * (1 - f) + arr[i + 1] * f


def rebuild(src_path, radius_dp):
    dpi = src_path.split("/")[-2].replace("drawable-", "")
    s = SCALES[dpi]
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    px = im.load()
    box = card_box(px, w, h)
    L, T, R, B = box
    old_margin = min(L, T, w - 1 - R, h - 1 - B)
    H_arr, B_arr = sample_profiles(px, w, h, box)
    shadow_d = max(d for d in range(len(B_arr)) if H_arr[d] > 2 or B_arr[d] > 2)
    r_new = int(round(radius_dp * s))

    # ابعاد جدید: کارت باید بزرگ‌تر باشد تا گوشه‌های ۲۸dp + باند کشش جا شوند
    band = int(12 * s)
    card_w = 2 * r_new + band
    card_h = 2 * r_new + band
    margin = max(int(shadow_d) + 3, old_margin)
    W = card_w + 2 * margin
    HH = card_h + 2 * margin
    cl = margin
    ct = margin
    cr = margin + card_w - 1
    cb = margin + card_h - 1

    half_w = (card_w - 1) / 2.0
    half_h = (card_h - 1) / 2.0
    cx = W / 2.0 - 0.5
    cy = HH / 2.0 - 0.5

    out = Image.new("RGBA", (W, HH), (0, 0, 0, 0))
    opx = out.load()
    # ابرنمونه‌برداری ۴x — رندر مستقیم روی شبکهٔ ۴x و کوچک‌سازی جعبه‌ای
    big = Image.new("RGBA", (W * SS, HH * SS), (0, 0, 0, 0))
    bpx = big.load()
    half_w4 = half_w * SS + (SS - 1) / 2.0
    half_h4 = half_h * SS + (SS - 1) / 2.0
    cx4 = cx * SS + (SS - 1) / 2.0
    cy4 = cy * SS + (SS - 1) / 2.0
    r4 = r_new * SS + (SS - 1) / 2.0
    for y4 in range(HH * SS):
        dy = y4 - cy4
        for x4 in range(W * SS):
            dx = x4 - cx4
            d = sdf_round_rect(dx, dy, half_w4, half_h4, r4)
            if d <= 0:
                bpx[x4, y4] = (255, 255, 255, 255)
            else:
                df = d / SS
                Ha = interp(H_arr, df) / 255.0
                Ba = interp(B_arr, df) / 255.0
                if Ha <= 0 and Ba <= 0:
                    continue
                # سفید روی مشکی (straight alpha over)
                oa = Ha + Ba * (1 - Ha)
                if oa <= 0:
                    continue
                orb = 255.0 * Ha / oa
                bpx[x4, y4] = (int(round(orb)), int(round(orb)), int(round(orb)), int(round(oa * 255)))
    out = big.resize((W, HH), Image.BOX)

    # مارکرهای ۹-پچ — ردیف بالا/ستون چپ = کشش؛ ردیف پایین/ستون راست = پدینگ محتوا (کارت ± ۱)
    opx = out.load()
    black = (0, 0, 0, 255)
    sx0 = cl + r_new + 2
    sx1 = W - 2 - (r_new + (W - 1 - cr))
    sy0 = ct + r_new + 2
    sy1 = HH - 2 - (r_new + (HH - 1 - cb))
    for x in range(sx0, sx1 + 1):
        opx[x, 0] = black
    for y in range(sy0, sy1 + 1):
        opx[0, y] = black
    px0 = max(cl - 1, 0)
    px1 = min(cr + 1, W - 2)
    py0 = max(ct - 1, 0)
    py1 = min(cb + 1, HH - 2)
    for x in range(px0, px1 + 1):
        opx[x, HH - 1] = black
    for y in range(py0, py1 + 1):
        opx[W - 1, y] = black
    return out, box, (cl, ct, cr, cb), (sx0, sx1), (sy0, sy1), r_new, s


def measure_radius(path):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    box = card_box(px, w, h)
    L, T, R, B = box
    firstx = {}
    for y in range(T, B + 1):
        for x in range(1, w - 1):
            if px[x, y][3] >= 250:
                firstx[y] = x
                break
    left = min(firstx.values())
    r = None
    for y in sorted(firstx):
        if firstx[y] == left:
            r = y - T
            break
    return r, box


def main():
    if len(sys.argv) < 3:
        print("usage: regenerate_popup_9patch.py <asset-name-without-ext> <radius-dp>")
        return
    name, rdp = sys.argv[1], float(sys.argv[2])
    for dpi in ["mdpi", "hdpi", "xhdpi", "xxhdpi"]:
        src = os.path.join(RES, f"drawable-{dpi}/{name}.9.png")
        if not os.path.exists(src):
            continue
        out, old_box, new_box, sx, sy, r_new, s = rebuild(src, rdp)
        out.save(src, optimize=True)
        r_m, b_m = measure_radius(src)
        print(
            f"{dpi}: old_card={old_box} new_card={new_box} size={out.size} "
            f"R={r_new}px({r_new/s:.1f}dp) stretch_x={sx} stretch_y={sy} "
            f"measured_radius={r_m}px({r_m/s if r_m else 0:.1f}dp)"
        )


if __name__ == "__main__":
    main()

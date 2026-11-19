#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UI2 قدم ۳۰ — ابزار بازتولید ۹-پچ پوستهٔ باتم‌شیت (sheet_shadow_round)
#
# شعاع قوس گوشهٔ بالای کارت شیت در asset آپستریم (قوس نرم مؤثر ~۲۰px @mdpi) به توکن
# SHAPE_SHEET (۲۸dp — هم‌زبانهٔ SHAPE_DIALOG) ارتقا می‌یابد.
# تفاوت‌های کلیدی شیت با پاپ‌آپ (regenerate_popup_9patch.py):
#   ۱) کارت شیت تا لبهٔ پایین asset ممتد است (بدون حاشیه و سایهٔ پایین — شیت به کف صفحه چسبیده است)
#   ۲) حاشیهٔ جانبی (~۸px) و حاشیهٔ بالایی (~۱۲px) متفاوت‌اند و به‌ازای هر density عیناً از asset قدیم حفظ می‌شوند
#      (دلتای چیدمان صفر: backgroundPaddingLeft/Top عیناً آپستریم)
#   ۳) نوار کشش عمودی زیر پایان قوس تا کف ممتد کارت است
# مدل بازسازی از خود asset فعلی استخراج می‌شود:
#   کارت = مستطیل‌گرد سفید مات + لبهٔ AA + هالهٔ سفید (~۱px) + سایهٔ مشکی نرم (~۸-۱۰px، چگالی ≤ ۴٪)
# پروفایل‌های H (هاله) و B (سایه) فقط از سه لبهٔ چپ/راست/بالا نمونه‌برداری می‌شوند (پایین ممتد است)
# و تا حاشیهٔ asset محدود می‌شوند تا سایه در لبه بریده نشود.
# معناشناسی پدینگ محتوا (کارت±۱ افقی / کاردِ بالا−۱ تا کف ممتد عمودی) بازتولید می‌شود.
# ابرنمونه‌برداری ۴x برای AA تمیز.
#
# کاربرد:
#   python3 Tools/regenerate_sheet_9patch.py sheet_shadow_round 28
import math
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "TMessagesProj/src/main/res")
SCALES = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0}
SS = 4     # ابرنمونه‌برداری
BAND = 8   # پهنای نوار کشش (px @mdpi)
GAP = 2    # فاصلهٔ نوار کشش از پایان قوس


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


def card_edges(px, w, h):
    # لبهٔ کارت عیناً از asset قدیم:
    #   چپ = نخستین ستون مات کامل در یک‌چهارم پایینی (زیر قوس)
    #   راست = آخرین ستون مات کامل در همان ردیف‌ها
    #   بالا = نخستین ردیف مات کامل در ستون‌های میانه (رأس قوس)
    #   پایین = ممتد تا آخرین ردیف محتوا
    ys = range(int(h * 0.72), h - 1)
    L = R = None
    for y in ys:
        fx = lx = None
        for x in range(1, w - 1):
            if px[x, y][3] >= 250:
                if fx is None:
                    fx = x
                lx = x
        if fx is not None:
            L = fx if L is None else min(L, fx)
            R = lx if R is None else max(R, lx)
    mid0, mid1 = int(w / 3), int(2 * w / 3)
    T = None
    for y in range(1, h - 1):
        if any(px[x, y][3] >= 250 for x in range(mid0, mid1)):
            T = y
            break
    B = None
    for y in range(h - 2, 0, -1):
        if all(px[x, y][3] >= 250 for x in range(mid0, mid1)):
            B = y
            break
    return L, T, R, B


def is_white(p):
    r, g, b, a = p
    return r > 180 and g > 180 and b > 180


def is_black(p):
    r, g, b, a = p
    return r < 90 and g < 90 and b < 90


def sample_profiles(px, w, h, box):
    # پروفایل فاصله‌محور از سه لبهٔ چپ/راست/بالا؛ H = هالهٔ سفید، B = سایهٔ مشکی
    # (لبهٔ پایین ممتد است — نمونه‌برداری نمی‌شود)
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
    ]
    lastB = 10.0  # مقدار اولیهٔ سایهٔ زیر هاله (نامرئی زیر هالهٔ مات)
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


def sdf_sheet(dx, dy, half_w, half_h, r):
    # کارت شیت: دو گوشهٔ بالا گرد (r) و دو گوشهٔ پایین تیز (ممتد به کف)
    # r می‌تواند از half_h بزرگ‌تر باشد (SDF متقارن در این حالت منحل می‌شود)
    y_c = -half_h + r  # خط مرکز قوس‌های بالا
    if dy <= y_c:
        # بالای خط قوس: لبهٔ بالا یا قوس گوشه‌ها
        if abs(dx) <= half_w - r:
            return -dy - half_h
        return math.hypot(abs(dx) - (half_w - r), dy - y_c) - r
    # پایین خط قوس: لبه‌های جانبی و کف تیز
    qx = abs(dx) - half_w
    qy = dy - half_h
    outside = math.hypot(max(qx, 0.0), max(qy, 0.0))
    inside = min(max(qx, qy), 0.0)
    return outside + inside


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
    L, T, R, B = card_edges(px, w, h)
    # حاشیه‌ها عیناً از asset قدیم (دلتای چیدمان صفر)
    margin_side = min(L, w - 1 - R)
    margin_top = T
    H_arr, B_arr = sample_profiles(px, w, h, (L, T, R, B))
    shadow_d = max(d for d in range(len(B_arr)) if H_arr[d] > 2 or B_arr[d] > 2)
    # سایه تا حاشیهٔ asset محدود می‌شود تا در لبه بریده نشود
    lim = max(margin_side, margin_top) - 1
    for d in range(lim + 1, len(B_arr)):
        H_arr[d] = 0.0
        B_arr[d] = 0.0
    r_new = int(round(radius_dp * s))

    band = int(BAND * s)
    gap = int(GAP * s)
    # پهنای کارت: قوس‌ها + نوار کشش افقی دور از قوس‌ها؛ بلندی کارت: قوس بالا + فاصله + نوار کشش عمودی
    card_w = 2 * r_new + band + gap
    card_h = r_new + gap + band
    W = card_w + 2 * margin_side
    HH = margin_top + card_h + 1  # + ردیف مارکر پایین
    cl = margin_side
    ct = margin_top
    cr = margin_side + card_w - 1
    cb = HH - 2  # کف ممتد — آخرین ردیف محتوا

    half_w = (card_w - 1) / 2.0
    half_h = (cb - ct) / 2.0
    cx = W / 2.0 - 0.5
    cy = (ct + cb) / 2.0

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
            d = sdf_sheet(dx, dy, half_w4, half_h4, r4)
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

    # مارکرهای ۹-پچ — مدل آپستریم شیت:
    #   ردیف بالا = نوار کشش افقی (میانهٔ کارت، دور از قوس‌ها)
    #   ستون چپ = نوار کشش عمودی (زیر پایان قوس تا کف ممتد کارت)
    #   ردیف پایین = پدینگ افقی (کارت±۱) — مدل آپستریم mdpi
    #   ستون راست = پدینگ عمودی (کارت بالا−۱ تا کف ممتد) — عیناً آپستریم
    opx = out.load()
    black = (0, 0, 0, 255)
    sx0 = cl + r_new + gap
    sx1 = cr - r_new - gap
    sy0 = ct + r_new + gap
    sy1 = cb
    for x in range(sx0, sx1 + 1):
        opx[x, 0] = black
    for y in range(sy0, sy1 + 1):
        opx[0, y] = black
    bx0 = max(cl - 1, 0)
    bx1 = min(cr + 1, W - 2)
    for x in range(bx0, bx1 + 1):
        opx[x, HH - 1] = black
    for y in range(max(ct - 1, 0), cb + 1):
        opx[W - 1, y] = black
    return out, (L, T, R, B), (cl, ct, cr, cb), (sx0, sx1), (sy0, sy1), (bx0, bx1), r_new, s


AAPT2_BORDER_BLACK = (0, 0, 0, 255)


def sanitize_border(im):
    # قانون نهایی aapt2 (با ماتریس ترکیبی سنتتیک + باینری aapt2 واقعی ۲.۲۰ اثبات شد):
    #   مرز = فقط (0,0,0,0) شفاف | (0,0,0,255) سیاهِ کاملاً مات | (255,0,0,255) قرمز مات (layout bounds)
    #   هر آلفای میانی (۱ تا ۲۵۴) حتی برای سیاه = «found an invalid color» — سیاهِ نیمه‌شفاف مجاز نیست!
    # هالهٔ سایهٔ SDF کل بوم را می‌پوشاند و پیش از مارکرکشی در ردیف مرزی (به‌ویژه پایین — کارت ممتد)
    # هم خاکستری نیمه‌شفاف و هم سیاهِ نیمه‌شفاف (۰,۰,۰,آلفای ۱-۷) باقی می‌گذارد — همه باید صفر شوند.
    px = im.load()
    w, h = im.size
    fixed = 0
    coords = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] \
        + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    for c in coords:
        p = px[c]
        if p != (0, 0, 0, 255) and p != (255, 0, 0, 255):
            px[c] = (0, 0, 0, 0)
            fixed += 1
    return fixed


def validate_aapt2(path):
    # راستی‌آزمایی پس از ذخیره با قانون دقیق aapt2 (شفاف | سیاهِ مات | قرمز مات) + وجود مارکر کشش بالا/چپ
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    coords = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] \
        + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    bad = [c for c in coords if not (
        px[c][3] == 0
        or px[c] == (0, 0, 0, 255)
        or px[c] == (255, 0, 0, 255)
    )]
    top_black = sum(1 for x in range(w) if px[x, 0] == AAPT2_BORDER_BLACK)
    left_black = sum(1 for y in range(h) if px[0, y] == AAPT2_BORDER_BLACK)
    if bad or top_black == 0 or left_black == 0:
        raise AssertionError(
            f"AAPT2 validation FAILED for {path}: bad_border={len(bad)} "
            f"top_markers={top_black} left_markers={left_black}"
        )
    return len(bad), top_black, left_black


def measure_card(path, expect_r_px=None):
    # راستی‌آزمایی هندسی asset تولیدشده: انحراف لبهٔ قوس از دایرهٔ موردانتظار
    # (مرکز قوس گوشهٔ بالا-چپ = (cl + r, ct + r))
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    L, T, R, B = card_edges(px, w, h)
    if expect_r_px is None:
        return L, T, R, B, None, None
    cx = L + expect_r_px
    cy = T + expect_r_px
    devs = []
    for y in range(T, T + expect_r_px + 1):
        fx = None
        for x in range(1, w - 1):
            if px[x, y][3] >= 250:
                fx = x
                break
        if fx is not None:
            # لبهٔ AA: نیم‌پیکسل تحمل
            devs.append(math.hypot(fx - cx, y - cy) - expect_r_px)
    dev_mean = sum(devs) / len(devs) if devs else 0.0
    dev_max = max(abs(v) for v in devs) if devs else 0.0
    return L, T, R, B, (dev_mean, dev_max), (cx, cy)


def main():
    if len(sys.argv) < 3:
        print("usage: regenerate_sheet_9patch.py <asset-name-without-ext> <radius-dp>")
        return
    name, rdp = sys.argv[1], float(sys.argv[2])
    for dpi in ["mdpi", "hdpi", "xhdpi", "xxhdpi"]:
        src = os.path.join(RES, f"drawable-{dpi}/{name}.9.png")
        if not os.path.exists(src):
            continue
        out, old_box, new_box, sx, sy, bx, r_new, s = rebuild(src, rdp)
        n_fixed = sanitize_border(out)
        out.save(src, optimize=True)
        bad, top_m, left_m = validate_aapt2(src)
        L, T, R, B, dev, c_fit = measure_card(src, expect_r_px=r_new)
        dev_s = f"dev_mean={dev[0]:+.2f}px dev_max={dev[1]:.2f}px" if dev else ""
        print(
            f"{dpi}: old_card={old_box} new_card={new_box} size={out.size} "
            f"R_set={r_new}px({r_new/s:.1f}dp) stretch_x={sx} stretch_y={sy} pad_bottom={bx} "
            f"border_fixed={n_fixed} aapt2_ok(bad={bad},top={top_m},left={left_m}) "
            f"{dev_s} (center={c_fit})"
        )


if __name__ == "__main__":
    main()

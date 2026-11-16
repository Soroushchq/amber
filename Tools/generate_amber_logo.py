"""AmberGram UI 2.0 — step 8: brand logo (amber paper plane + AmberGram wordmark).

Replaces the leaked "Telegram" wordmark vectors and the blue Telegram circle
logo (Terms of Service) with the Amber brand lockup:

  drawable/amber_logo.xml      (viewport 249x57, intro — same metrics as the
                                old telegram_logo: 83dp x 19dp)
  drawable/amber_logo_2.xml    (viewport 269x61, dialogs header / stories —
                                same metrics as the old telegram_logo_2:
                                90dp x 20.408922dp)
  drawable-{mdpi,hdpi}/logo_middle.webp + drawable-{xhdpi,xxhdpi}/logo_middle.png
                               (amber gradient circle + white plane, same
                                pixel sizes as the old blue Telegram circle)

Construction (everything derived, nothing hand-drawn):
  * plane outline traced from the repo's brand art
    (mipmap-xxxhdpi/icon_foreground.png, alpha threshold) via crack-following
    boundary walk + Douglas-Peucker simplification
  * "AmberGram" lettering extracted from the app's own brand font
    (assets/fonts/ambergramui.ttf, Baloo Bhaijaan 2, OFL) as vector outlines
  * accent gradient parsed from AmberTokens.java: ACCENT_NIGHT[0] #F5A623 ->
    ACCENT_NIGHT[2] #EA580C (single source of truth)
"""
import re

import numpy as np
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

REPO = "/home/z/amber"
RES = f"{REPO}/TMessagesProj/src/main/res"
PLANE_SRC = f"{RES}/mipmap-xxxhdpi/icon_foreground.png"
FONT = f"{REPO}/TMessagesProj/src/main/assets/fonts/ambergramui.ttf"
TOKENS = f"{REPO}/TMessagesProj/src/main/java/org/telegram/messenger/AmberTokens.java"

ALPHA_THRESHOLD = 20
DP_EPSILON = 2.2          # px at 432 scale
TEXT = "AmberGram"
_POLY_CACHE = {}


def cached_plane_polygon():
    if "poly" not in _POLY_CACHE:
        raw = plane_polygon()
        _POLY_CACHE["poly"] = simplify(raw, DP_EPSILON)
    return _POLY_CACHE["poly"]


def parse_tokens():
    src = open(TOKENS, encoding="utf-8").read()
    body = re.search(r"public\s+static\s+final\s+int\[\]\s+ACCENT_NIGHT\s*=\s*\{([^}]*)\}", src).group(1)
    vals = [int(h, 16) for h in re.findall(r"0x([0-9A-Fa-f]{8})", body)]
    def rgb(v):
        return [(v >> 16) & 255, (v >> 8) & 255, v & 255]
    return rgb(vals[0]), rgb(vals[2])


ACC0, ACC2 = parse_tokens()
ACC0_HEX, ACC2_HEX = "#FF%02X%02X%02X" % tuple(ACC0), "#FF%02X%02X%02X" % tuple(ACC2)
print("accent gradient:", ACC0_HEX, "->", ACC2_HEX)


# ------------------------------------------------------- plane outline -----
def plane_polygon():
    """Trace the brand plane silhouette as an ordered polygon (crack following,
    outer boundary clockwise with the region kept on the right)."""
    mask = np.array(Image.open(PLANE_SRC).convert("RGBA"))[..., 3] > ALPHA_THRESHOLD
    y0 = int(np.argmax(mask.any(axis=1)))          # first row containing the region
    x0 = int(np.where(mask[y0])[0].min())          # leftmost pixel of that row
    # start: topmost-leftmost set pixel, vertex at its NW corner, walking E
    start_px = (x0, y0)
    start_v = (x0, y0)
    N_, E_, S_, W_ = (0, -1), (1, 0), (0, 1), (-1, 0)
    # pixels adjacent to edge v -> v+d (region kept on the RIGHT)
    LEFT_PX = {E_: (0, -1), W_: (-1, 0), N_: (-1, -1), S_: (0, 0)}
    RIGHT_PX = {E_: (0, 0), W_: (-1, -1), N_: (0, -1), S_: (-1, 0)}

    def isset(px):
        x, y = px
        return 0 <= x < mask.shape[1] and 0 <= y < mask.shape[0] and mask[y, x]

    def edge_ok(v, d):
        lo = LEFT_PX[d]
        ro = RIGHT_PX[d]
        return isset((v[0] + ro[0], v[1] + ro[1])) and not isset((v[0] + lo[0], v[1] + lo[1]))

    assert edge_ok(start_v, E_), "invalid start edge"
    turn_left = {E_: N_, N_: W_, W_: S_, S_: E_}
    turn_right = {E_: S_, S_: W_, W_: N_, N_: E_}
    v, d = start_v, E_
    poly = [v]
    for _ in range(20000):
        for nd in (turn_right[d], d, turn_left[d]):
            if edge_ok(v, nd):
                d = nd
                break
        else:
            d = turn_left[turn_left[d]]  # dead end: turn back
        v = (v[0] + d[0], v[1] + d[1])
        if v == start_v and edge_ok(v, E_):
            break
        poly.append(v)
    assert poly[0] == poly[-1] or v == start_v, "boundary walk did not close"
    area = abs(sum(poly[i][0] * poly[i + 1][1] - poly[i + 1][0] * poly[i][1]
                   for i in range(len(poly) - 1))) / 2
    print(f"plane polygon: {len(poly)} crack vertices, area {area:.0f}px^2")
    return np.array(poly, dtype=np.float64)


def simplify(pts, eps):
    def dp(seg):
        if len(seg) < 3:
            return seg
        a, b = seg[0], seg[-1]
        ab = b - a
        n = np.hypot(*ab) or 1.0
        dist = np.abs(np.cross(np.broadcast_to(ab, (len(seg) - 2, 2)), seg[1:-1] - a)) / n
        if dist.max() < eps:
            return np.array([a, b])
        k = int(dist.argmax()) + 1
        return np.concatenate([dp(seg[:k + 1])[:-1], dp(seg[k:])])
    # closed polygon: split at the two points farthest apart
    i0 = 0
    i1 = int(np.argmax(np.hypot(*(pts - pts[0]).T)))
    left = dp(pts[i0:i1 + 1])
    right = dp(np.concatenate([pts[i1:], pts[:2]]))
    out = np.concatenate([left[:-1], right[:-1]])
    print(f"after Douglas-Peucker(eps={eps}): {len(out)} vertices")
    return out


# ----------------------------------------------------------- lettering -----
def wordmark_path(target_cap, baseline_y, origin_x):
    """'AmberGram' outlines from the brand font, scaled so 'A' cap = target_cap."""
    ft = TTFont(FONT)
    glyph_set = ft.getGlyphSet()
    cmap = ft.getBestCmap()
    hmtx = ft["hmtx"]
    bp = BoundsPen(glyph_set)
    glyph_set[cmap[ord("A")]].draw(bp)
    cap_font = bp.bounds[3]
    scale = target_cap / cap_font
    ntos = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    x = 0.0
    parts = []
    for ch in TEXT:
        g = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set, ntos=ntos)
        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, origin_x + x * scale, baseline_y))
        glyph_set[g].draw(tpen)
        parts.append(pen.getCommands())
        x += hmtx[g][0]
    return " ".join(parts), x * scale


def fmt_poly(poly):
    pts = [f"{p[0]:.1f},{p[1]:.1f}".rstrip("0").rstrip(",").replace(".0,", " ").replace(".0 ", " ")
           for p in poly]
    # simpler robust: rebuild manually
    out = []
    for p in poly:
        sx = f"{p[0]:.1f}".rstrip("0").rstrip(".")
        sy = f"{p[1]:.1f}".rstrip("0").rstrip(".")
        out.append(f"{sx},{sy}")
    return "M" + "L".join(out) + "Z"


def compose(viewport_w, viewport_h):
    """Return (plane_path, gradient_y0, gradient_y1, text_path) for a viewport."""
    poly = cached_plane_polygon()   # simplified px coords in 432-space
    bbox = poly.min(axis=0), poly.max(axis=0)
    pw_raw, ph_raw = bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1]

    cap = viewport_h * 0.635        # 'A' cap height in viewport units
    baseline = viewport_h * 0.845
    plane_h = cap * 1.16
    gap = cap * 0.30
    margin = viewport_h * 0.085

    text0, tw0 = wordmark_path(cap, baseline, 0)
    plane_scale = plane_h / ph_raw
    plane_w = pw_raw * plane_scale
    total = margin + plane_w + gap + tw0 + margin
    if total > viewport_w:          # shrink uniformly to fit
        k = viewport_w / total
        cap *= k; baseline *= k; plane_h *= k; gap *= k; margin *= k
        text0, tw0 = wordmark_path(cap, baseline, 0)
        plane_scale = plane_h / ph_raw
        plane_w = pw_raw * plane_scale
        total = margin + plane_w + gap + tw0 + margin
    print(f"viewport {viewport_w}x{viewport_h}: cap {cap:.1f} planeW {plane_w:.1f} textW {tw0:.1f} total {total:.1f}")

    # place plane: optical center aligned to lettering mid (cap/2 above baseline)
    plane_top = baseline - cap * 0.5 - plane_h * 0.52
    plane_x = margin
    scaled = (poly - np.array(bbox[0])) * plane_scale
    scaled[:, 0] += plane_x
    scaled[:, 1] += plane_top
    plane_path = fmt_poly(scaled)
    text_path, _ = wordmark_path(cap, baseline, plane_x + plane_w + gap)
    return plane_path, plane_top, plane_top + plane_h, text_path


def vector_xml(width_dp, height_dp, vw, vh, plane_path, gy0, gy1, text_path):
    return (
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    xmlns:aapt="http://schemas.android.com/aapt"\n'
        f'    android:width="{width_dp}dp"\n'
        f'    android:height="{height_dp}dp"\n'
        f'    android:viewportWidth="{vw}"\n'
        f'    android:viewportHeight="{vh}">\n'
        '    <path\n'
        '        android:pathData="' + plane_path + '">\n'
        '        <aapt:attr name="android:fillColor">\n'
        '            <gradient\n'
        '                android:type="linear"\n'
        f'                android:startX="0"\n'
        f'                android:startY="{gy0:.1f}"\n'
        f'                android:endX="0"\n'
        f'                android:endY="{gy1:.1f}">\n'
        f'                <item android:offset="0.0" android:color="{ACC0_HEX}" />\n'
        f'                <item android:offset="1.0" android:color="{ACC2_HEX}" />\n'
        '            </gradient>\n'
        '        </aapt:attr>\n'
        '    </path>\n'
        '    <path\n'
        '        android:fillColor="#FFFFFFFF"\n'
        '        android:fillType="nonZero"\n'
        '        android:pathData="' + text_path + '" />\n'
        '</vector>\n'
    )


# ------------------------------------------------------------ build ------
p1, g0, g1, t1 = compose(249, 57)
open(f"{RES}/drawable/amber_logo.xml", "w", encoding="utf-8").write(
    vector_xml(83, 19, 249, 57, p1, g0, g1, t1))
print("amber_logo.xml written (intro, 83x19dp)")

p2, h0, h1, t2 = compose(269, 61)
open(f"{RES}/drawable/amber_logo_2.xml", "w", encoding="utf-8").write(
    vector_xml(90, 20.408922, 269, 61, p2, h0, h1, t2))
print("amber_logo_2.xml written (dialogs/stories, 90x20.408922dp)")

# logo_middle: amber gradient circle + white plane (same pixel sizes as before)
poly = cached_plane_polygon()
bbox = (poly.min(axis=0), poly.max(axis=0))
for px, path in [
    (68, f"{RES}/drawable-mdpi/logo_middle.webp"),
    (102, f"{RES}/drawable-hdpi/logo_middle.webp"),
    (136, f"{RES}/drawable-xhdpi/logo_middle.png"),
    (204, f"{RES}/drawable-xxhdpi/logo_middle.png"),
]:
    t = np.linspace(0.0, 1.0, px)[:, None]
    a0 = np.array(ACC0, dtype=np.float64)
    a2 = np.array(ACC2, dtype=np.float64)
    col = a0[None, None, :] * (1 - t[..., None]) + a2[None, None, :] * t[..., None]
    img = np.repeat(col, px, axis=1)
    yy, xx = np.mgrid[0:px, 0:px]
    half = (px - 1) / 2.0
    outside = (xx - half) ** 2 + (yy - half) ** 2 > (half + 0.5) ** 2
    img[outside] = 0
    canvas = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    plane_fill = (poly - np.array(bbox[0])) / (bbox[1] - bbox[0]).max()
    size = px * 0.54
    pw = (bbox[1][0] - bbox[0][0]) * (size / (bbox[1] - bbox[0]).max())
    ph = (bbox[1][1] - bbox[0][1]) * (size / (bbox[1] - bbox[0]).max())
    plane_fill[:, 0] *= pw
    plane_fill[:, 1] *= ph
    plane_fill[:, 0] += (px - pw) / 2
    plane_fill[:, 1] += (px - ph) / 2
    d = ImageDraw.Draw(canvas)
    d.polygon([tuple(p) for p in plane_fill], fill=(255, 255, 255, 255))
    if path.endswith(".webp"):
        canvas.save(path, "WEBP", quality=90, method=4)
    else:
        canvas.save(path, optimize=True)
    print(f"{path.split('res/')[1]}: {px}px written")

print("OK")

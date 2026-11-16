# -*- coding: utf-8 -*-
"""AmberGram UI 2.0 — step 10: brand-safe splash / launch experience.

Builds, from AmberTokens.java (single source of truth) and the committed
brand plane (drawable/amber_logo.xml — step 8 geometry):

    drawable/splash_plane.xml         brand mark: accent-gradient circle +
                                      white plane  (day stops)
    drawable-night/splash_plane.xml   same vector, night stops
    drawable/splash_amber.xml         cold-start windowBackground (day paper)
    drawable-night/splash_amber.xml   cold-start windowBackground (night warm)

Wiring (done by hand in styles, verified here):
  values/styles.xml            Theme.TMessages.Start -> @drawable/splash_amber
                               Theme.TMessages -> @color/app_window_bg
                               Theme.TMessages.Dark -> #17130E
  values-night/styles.xml      Start -> splash refs + @color/splash_bg + plane icon
  values-v31/styles.xml        Start -> splash refs + @drawable/splash_plane icon
                               + @color/splash_bg  (fixes upstream bug: Android 12+
                               dark mode used to show a WHITE system splash,
                               because values-v31 beat values-night and
                               windowSplashScreenBackground = ?windowBackground
                               resolved to a white literal; @color refs resolve
                               per uiMode, so no values-v31-night is needed)
  ThemeColors.java             TELEGRAM_COLOR 0xFF229AF0 (upstream blue) ->
                               0xFFF5A623, TELEGRAM_COLOR_TEXT -> 0xFFC25E00
                               (intro GL plane, intro page dots, dialog defaults)

Previews (rendered from the written XMLs, not re-derived):
  public/icons/ui2-splash-night.png   cold start, night
  public/icons/ui2-splash-day.png     cold start, day
  public/icons/ui2-splash-icon.png    Android 12+ system splash (icon on splash_bg)
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

REPO = "/home/z/amber"
RES = f"{REPO}/TMessagesProj/src/main/res"
TOKENS = f"{REPO}/TMessagesProj/src/main/java/org/telegram/messenger/AmberTokens.java"
UTILS = f"{RES}/../java/org/telegram/ui/ActionBar/ThemeColors.java"
OUT = "/home/z/my-project/public/icons"

errors = []


def check(cond, msg):
    tag = "OK " if cond else "FAIL"
    print(f"[{tag}] {msg}")
    if not cond:
        errors.append(msg)


def parse_tokens():
    src = open(TOKENS, encoding="utf-8").read()
    ints = dict(re.findall(r"public\s+static\s+final\s+int\s+(\w+)\s*=\s*0x([0-9A-Fa-f]{8})", src))
    arrays = {n: [int(h, 16) for h in re.findall(r"0x([0-9A-Fa-f]{8})", b)]
              for n, b in re.findall(r"public\s+static\s+final\s+int\[\]\s+(\w+)\s*=\s*\{([^}]*)\}", src)}
    def rgb(name):
        v = int(ints[name], 16) & 0xFFFFFF
        return f"#{v >> 16:02X}{(v >> 8) & 255:02X}{v & 255:02X}"
    acc = [v & 0xFFFFFF for v in arrays["ACCENT_NIGHT"]]
    return {
        "DAY_WALLPAPER_TOP": rgb("DAY_WALLPAPER_TOP"),
        "DAY_WALLPAPER_BOTTOM": rgb("DAY_WALLPAPER_BOTTOM"),
        "NIGHT_TOP": rgb("NIGHT_WALLPAPER_TOP"),
        "NIGHT_MID": rgb("NIGHT_WALLPAPER_MID"),
        "NIGHT_BOTTOM": rgb("NIGHT_WALLPAPER_BOTTOM"),
        "DAY_ACCENT": rgb("DAY_ACCENT"),
        "DAY_ACCENT_BRIGHT": rgb("DAY_ACCENT_BRIGHT"),
        "DAY_WINDOW": rgb("DAY_BG"),
        "ACC_NIGHT0": f"#{acc[0] >> 16:02X}{(acc[0] >> 8) & 255:02X}{acc[0] & 255:02X}",
        "ACC_NIGHT2": f"#{acc[2] >> 16:02X}{(acc[2] >> 8) & 255:02X}{acc[2] & 255:02X}",
        "TELEGRAM_COLOR": 0xFFF5A623,
        "TELEGRAM_COLOR_TEXT": 0xFFC25E00,
    }


T = parse_tokens()
print("tokens:", {k: v for k, v in T.items() if isinstance(v, str)})


# ----------------------------------------------------- plane from step 8 ---
def plane_path_from_logo():
    src = open(f"{RES}/drawable/amber_logo.xml", encoding="utf-8").read()
    path = re.findall(r'android:pathData="([^"]+)"', src)[0]
    pts = [float(v) for v in re.findall(r"-?\d+\.?\d*", path)]
    assert path.startswith("M") and "L" in path and path.rstrip().endswith("Z")
    poly = list(zip(pts[0::2], pts[1::2]))
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return poly, (min(xs), min(ys), max(xs), max(ys))


PLANE, PB = plane_path_from_logo()
pw, ph = PB[2] - PB[0], PB[3] - PB[1]
print(f"brand plane from amber_logo.xml: {len(PLANE)} pts, bbox {pw:.1f}x{ph:.1f}")


# ------------------------------------------------------------ build ------
def build_splash_plane(mode):
    """viewport 320: gradient circle r=100 at center + white plane (0.54 ratio,
    same proportions as the step-8 logo_middle circle)."""
    if mode == "day":
        c0, c1 = T["DAY_ACCENT_BRIGHT"], T["DAY_ACCENT"]
    else:
        c0, c1 = T["ACC_NIGHT0"], T["ACC_NIGHT2"]
    r = 100.0
    circle = (f"M{160 - r:.0f},160a{r:.0f},{r:.0f} 0 1,0 {2*r:.0f},0"
              f"a{r:.0f},{r:.0f} 0 1,0 {-2*r:.0f},0Z")
    target = 0.54 * 2 * r
    s = target / max(pw, ph)
    plane = [(160 - pw * s / 2 + (x - PB[0]) * s, 160 - ph * s / 2 + (y - PB[1]) * s)
             for x, y in PLANE]
    d = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    plane_path = "M" + "L".join(f"{d(x)},{d(y)}" for x, y in plane) + "Z"
    return (
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    xmlns:aapt="http://schemas.android.com/aapt"\n'
        '    android:width="288dp"\n'
        '    android:height="288dp"\n'
        '    android:viewportWidth="320"\n'
        '    android:viewportHeight="320">\n'
        '    <!-- AmberGram UI 2.0 (قدم ۱۰): نشان برند — دایره گرادیان اکسنت + هواپیمای سفید\n'
        '         هندسه هواپیما = همان مسیر amber_logo.xml (قدم ۸) فیت‌شده در دایره؛\n'
        '         دید سیستم‌اسپلش: دایره ۲۴۰dp از باکس ۲۸۸dp → دایره ما (۱۸۰dp) کامل داخل است -->\n'
        '    <path\n'
        f'        android:pathData="{circle}">\n'
        '        <aapt:attr name="android:fillColor">\n'
        '            <gradient\n'
        '                android:type="linear"\n'
        '                android:startX="0"\n'
        '                android:startY="60"\n'
        '                android:endX="0"\n'
        '                android:endY="260">\n'
        f'                <item android:offset="0.0" android:color="#FF{c0[1:]}" />\n'
        f'                <item android:offset="1.0" android:color="#FF{c1[1:]}" />\n'
        '            </gradient>\n'
        '        </aapt:attr>\n'
        '    </path>\n'
        '    <path\n'
        '        android:fillColor="#FFFFFFFF"\n'
        '        android:fillType="nonZero"\n'
        f'        android:pathData="{plane_path}" />\n'
        '</vector>\n')


def build_splash_bg(mode):
    """layer-list: window background gradient + centered brand mark."""
    if mode == "day":
        stops = (T["DAY_WALLPAPER_TOP"], None, T["DAY_WALLPAPER_BOTTOM"])
        note = "کاغذ روز (توقف‌های وایپرپ روز)"
    else:
        stops = (T["NIGHT_TOP"], T["NIGHT_MID"], T["NIGHT_BOTTOM"])
        note = "شب گرم (توقف‌های وایپرپ شب)"
    center = (f'android:centerColor="#FF{stops[1][1:]}"\n            '
              if stops[1] else "")
    return (
        '<layer-list xmlns:android="http://schemas.android.com/apk/res/android">\n'
        f'    <!-- AmberGram UI 2.0 (قدم ۱۰): اسپلش سرد-استارت — {note} -->\n'
        '    <item>\n'
        '        <shape android:shape="rectangle">\n'
        '            <gradient\n'
        '                android:angle="270"\n'
        f'                android:startColor="#FF{stops[0][1:]}"\n'
        f'                {center}endColor="#FF{stops[2][1:]}"/>\n'
        '        </shape>\n'
        '    </item>\n'
        '    <item\n'
        '        android:width="150dp"\n'
        '        android:height="150dp"\n'
        '        android:gravity="center"\n'
        '        android:drawable="@drawable/splash_plane"/>\n'
        '</layer-list>\n')


files = {
    f"{RES}/drawable/splash_plane.xml": build_splash_plane("day"),
    f"{RES}/drawable-night/splash_plane.xml": build_splash_plane("night"),
    f"{RES}/drawable/splash_amber.xml": build_splash_bg("day"),
    f"{RES}/drawable-night/splash_amber.xml": build_splash_bg("night"),
}
os.makedirs(f"{RES}/drawable-night", exist_ok=True)
for path, xml in files.items():
    open(path, "w", encoding="utf-8").write(xml)
    ET.fromstring(xml)  # well-formed
    print("written:", os.path.relpath(path, RES))


# --------------------------------------------------------- validation ----
print("\n== validate wiring ==")
styles = {
    f"{RES}/values/styles.xml": open(f"{RES}/values/styles.xml", encoding="utf-8").read(),
    f"{RES}/values-night/styles.xml": open(f"{RES}/values-night/styles.xml", encoding="utf-8").read(),
    f"{RES}/values-v31/styles.xml": open(f"{RES}/values-v31/styles.xml", encoding="utf-8").read(),
}
for path, src in styles.items():
    if "Theme.TMessages.Start" in src:
        check("@drawable/splash_amber" in src, f"{os.path.basename(os.path.dirname(path))}: Start windowBackground -> splash_amber")
    if "values-night" in path or "values-v31" in path:
        check("@drawable/splash_plane" in src, f"{os.path.basename(os.path.dirname(path))}: splash icon -> splash_plane")
        check("@color/splash_bg" in src, f"{os.path.basename(os.path.dirname(path))}: splashScreenBackground -> @color/splash_bg")

all_styles = "\n".join(styles.values())
check("tg_splash_320" not in all_styles, "tg_splash_320 no longer referenced anywhere in styles")

cv = open(f"{RES}/values/colors.xml", encoding="utf-8").read()
cn = open(f"{RES}/values-night/colors.xml", encoding="utf-8").read()
check(f'<color name="splash_bg">{T["DAY_WALLPAPER_TOP"]}</color>' in cv, "values/colors: splash_bg == DAY_WALLPAPER_TOP")
check(f'<color name="app_window_bg">{T["DAY_WINDOW"]}</color>' in cv, "values/colors: app_window_bg == DAY_BG")
check(f'<color name="splash_bg">{T["NIGHT_MID"]}</color>' in cn, "values-night/colors: splash_bg == NIGHT_WALLPAPER_MID")
check(f'<color name="app_window_bg">{T["NIGHT_MID"]}</color>' in cn, "values-night/colors: app_window_bg == NIGHT_WALLPAPER_MID")

v31 = styles[f"{RES}/values-v31/styles.xml"]
check("#C25E00" in v31 and "#426482" not in v31 and "#527da3" not in v31, "values-v31: upstream blue primaries removed -> amber")
check("#33000000" in v31, "values-v31: scrim colorPrimaryDark kept (neutral)")
vn = styles[f"{RES}/values-night/styles.xml"]
check("#1f2732" not in vn and "#1c242e" not in vn and "#232d3a" not in vn and "#ff232d3a" not in vn,
      "values-night: upstream slate-blue removed -> warm night")
vs = styles[f"{RES}/values/styles.xml"]
check("@android:color/white\" /><!--" not in vs and vs.count('@android:color/white') <= 8, "values/styles: whites reduced")

print("\n== validate ThemeColors ==")
tc = open(UTILS, encoding="utf-8").read()
m1 = re.search(r"TELEGRAM_COLOR\s*=\s*0x([0-9A-Fa-f]{8})", tc)
m2 = re.search(r"TELEGRAM_COLOR_TEXT\s*=\s*0x([0-9A-Fa-f]{8})", tc)
check(m1 and int(m1.group(1), 16) == T["TELEGRAM_COLOR"], "TELEGRAM_COLOR == 0xFFF5A623 (ACCENT_NIGHT[0])")
check(m2 and int(m2.group(1), 16) == T["TELEGRAM_COLOR_TEXT"], "TELEGRAM_COLOR_TEXT == 0xFFC25E00 (DAY_ACCENT)")

print("\n== javalang ==")
r = os.system('python3 /home/z/my-project/amber-git/syntax_check.py '
              f'"{REPO}/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/ThemeColors.java"')
check(r == 0, "javalang green: ThemeColors.java")

print("\n== brand geometry ==")
src = open(f"{RES}/drawable-night/splash_plane.xml", encoding="utf-8").read()
plane_xml = re.findall(r'android:pathData="([^"]+)"', src)[1]
pts = [float(v) for v in re.findall(r"-?\d+\.?\d*", plane_xml)]
poly = list(zip(pts[0::2], pts[1::2]))
xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
check(abs(cx - 160) < 1 and abs(cy - 160) < 1, f"plane centered in circle ({cx:.1f}, {cy:.1f})")
ratio = (max(xs) - min(xs)) / 200.0
check(0.50 < ratio < 0.58, f"plane/circle ratio {ratio:.2f} (logo_middle-like)")
check("F5A623" in src and "EA580C" in src, "night plane gradient == ACCENT_NIGHT[0..2]")
sd = open(f"{RES}/drawable/splash_plane.xml", encoding="utf-8").read()
check("E8871E" in sd and "C25E00" in sd, "day plane gradient == DAY_ACCENT_BRIGHT->DAY_ACCENT")

if errors:
    print(f"\n{len(errors)} FAILURES — aborting previews")
    sys.exit(1)


# ------------------------------------------------------------ previews ---
def parse_splash(mode):
    d = "drawable-night" if mode == "night" else "drawable"
    src = open(f"{RES}/{d}/splash_amber.xml", encoding="utf-8").read()
    stops = re.findall(r'android:(?:start|center|end)Color="#FF([0-9A-F]{6})"', src)
    mark = open(f"{RES}/{d}/splash_plane.xml", encoding="utf-8").read()
    gcols = re.findall(r'android:color="#FF([0-9A-F]{6})"', mark)
    circle = re.findall(r'android:pathData="([^"]+)"', mark)[0]
    cp = [float(v) for v in re.findall(r"-?\d+\.?\d*", circle)]
    plane = re.findall(r'android:pathData="([^"]+)"', mark)[1]
    pp = [float(v) for v in re.findall(r"-?\d+\.?\d*", plane)]
    return stops, gcols, cp, pp


def render_coldstart(mode, path):
    stops, gcols, cp, pp = parse_splash(mode)
    W, H = 720, 1520
    scale = 150 / 320  # 150dp item, 1px=1dp preview
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    n = len(stops)
    for y in range(H):
        t = y / (H - 1)
        seg = min(int(t * (n - 1)), n - 2)
        lt = t * (n - 1) - seg
        a = [int(stops[seg][i:i + 2], 16) for i in (0, 2, 4)]
        b = [int(stops[seg + 1][i:i + 2], 16) for i in (0, 2, 4)]
        col = tuple(round(a[i] * (1 - lt) + b[i] * lt) for i in range(3))
        d.line([(0, y), (W, y)], fill=col)
    # centered mark: 320 viewport -> 150dp box; center of screen
    cx, cy = W / 2, H / 2
    r = 100 * scale
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(int(gcols[0][i:i + 2], 16) for i in (0, 2, 4)),
              outline=None)
    # vertical gradient inside circle: approximate with two halves is ugly; draw
    # scanline-clipped circle
    c0 = [int(gcols[0][i:i + 2], 16) for i in (0, 2, 4)]
    c1 = [int(gcols[1][i:i + 2], 16) for i in (0, 2, 4)]
    for y in range(int(cy - r), int(cy + r) + 1):
        t = min(max((y - (cy - r)) / (2 * r), 0), 1)
        col = tuple(round(c0[i] * (1 - t) + c1[i] * t) for i in range(3))
        half = max(r * r - (y - cy) * (y - cy), 0.0) ** 0.5
        if half <= 0:
            continue
        d.line([(cx - half, y), (cx + half, y)], fill=col)
    poly = [(cx + (x - 160) * scale, cy + (y - 160) * scale) for x, y in zip(pp[0::2], pp[1::2])]
    d.polygon(poly, fill=(255, 255, 255))
    bg.save(path, optimize=True)
    print("preview:", path)


def render_sysicon(mode, path):
    _, gcols, _, pp = parse_splash(mode)
    bgc = T["NIGHT_MID"] if mode == "night" else T["DAY_WALLPAPER_TOP"]
    W = 600
    bg = Image.new("RGB", (W, W), tuple(int(bgc.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)))
    d = ImageDraw.Draw(bg)
    # system: 288dp box in 240dp visible circle -> we draw box 320u -> visible 266.7u
    box = 320.0
    vis = 240 / 288 * box            # visible circle diameter in viewport units
    s = W / box
    cx = cy = W / 2
    # icon drawable centered: our circle r=100 at 160,160
    r = 100 * s
    c0 = [int(gcols[0][i:i + 2], 16) for i in (0, 2, 4)]
    c1 = [int(gcols[1][i:i + 2], 16) for i in (0, 2, 4)]
    for y in range(int(cy - r), int(cy + r) + 1):
        t = min(max((y - (cy - r)) / (2 * r), 0), 1)
        col = tuple(round(c0[i] * (1 - t) + c1[i] * t) for i in range(3))
        half = max(r * r - (y - cy) * (y - cy), 0.0) ** 0.5
        if half <= 0:
            continue
        d.line([(cx - half, y), (cx + half, y)], fill=col)
    scale = s
    poly = [(cx + (x - 160) * scale, cy + (y - 160) * scale) for x, y in zip(pp[0::2], pp[1::2])]
    d.polygon(poly, fill=(255, 255, 255))
    # visible-circle guide (faint)
    rv = vis / 2 * s
    d.ellipse([cx - rv, cy - rv, cx + rv, cy + rv], outline=(128, 128, 128), width=2)
    bg.save(path, optimize=True)
    print("preview:", path)


render_coldstart("night", f"{OUT}/ui2-splash-night.png")
render_coldstart("day", f"{OUT}/ui2-splash-day.png")
render_sysicon("night", f"{OUT}/ui2-splash-icon.png")
print("\nALL GREEN")

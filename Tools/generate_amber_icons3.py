"""AmberGram UI 2.0 — step 7: regenerate ALL main launcher icon densities
with the Expressive Material (concept C) palette, keeping the current
v0.8 minimal paper-plane brand art.

Source of the brand art: the repo's own adaptive foreground
(mipmap-xxxhdpi/icon_foreground.png, flat paper plane with alpha).
Every color comes from AmberTokens.java (single source of truth):
  * background = warm night gradient NIGHT_WALLPAPER_TOP -> MID -> BOTTOM
    (replaces the old cool near-black #08080A / #151518)
  * a soft amber halo (ACCENT_NIGHT[0]) glows behind the plane
  * the plane itself is mapped onto ACCENT_NIGHT[0], preserving its
    relative luminance shading
  * legacy ic_launcher.png is cut with a squircle (superellipse n=5) mask;
    ic_launcher_round.png keeps the circle mask
  * the monochrome themed-icon layer is re-cut from the same plane
    (replacing the stale v0.2.5 phoenix silhouette)

Outputs (all 5 densities, overwrites in place):
  mipmap-{mdpi..xxxhdpi}/ic_launcher.png            (squircle, legacy)
  mipmap-*/ic_launcher_round.png                    (circle, legacy)
  mipmap-*/icon_foreground.png / _round / _sa       (recolored plane)
  mipmap-*/icon_background_clip.png / _round        (warm gradient)
  drawable/icon_background_clip.webp / _round.webp  (warm gradient)
  drawable-nodpi/icon_phoenix_mono.png              (white plane silhouette)
  drawable/icon_background_sa.xml                   (fallback bg color)
"""
import re

import numpy as np
from PIL import Image, ImageDraw

REPO = "/home/z/amber"
RES = f"{REPO}/TMessagesProj/src/main/res"
PLANE_SRC = f"{RES}/mipmap-xxxhdpi/icon_foreground.png"  # brand art, 432px, alpha
TOKENS = f"{REPO}/TMessagesProj/src/main/java/org/telegram/messenger/AmberTokens.java"

SQUIRCLE_N = 5.0          # superellipse exponent (iOS-style squircle)
HALO_MAX_ALPHA = 34       # ~13% amber halo peak (255 scale)
HALO_CENTER = (0.50, 0.44)
HALO_RADIUS = 0.62        # fraction of canvas half-diagonal
LEGACY_FILL = 0.62        # plane width relative to legacy tile (HEAD legacy: ~0.60)
LUM = np.array([0.2126, 0.7152, 0.0722])  # Rec.709 luminance weights

DENSITIES = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
LAUNCHER = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
ADAPTIVE = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}


def parse_tokens():
    """Read palette constants from AmberTokens.java (single source of truth)."""
    src = open(TOKENS, encoding="utf-8").read()
    ints = dict(re.findall(r"public\s+static\s+final\s+int\s+(\w+)\s*=\s*0x([0-9A-Fa-f]{8})", src))

    def rgba(name):
        v = int(ints[name], 16)
        return ((v >> 16) & 255, (v >> 8) & 255, v & 255)

    arrays = {
        name: [((v >> 16) & 255, (v >> 8) & 255, v & 255)
               for v in (int(h, 16) for h in re.findall(r"0x([0-9A-Fa-f]{8})", body))]
        for name, body in re.findall(
            r"public\s+static\s+final\s+int\[\]\s+(\w+)\s*=\s*\{([^}]*)\}", src)
    }
    return {
        "NIGHT_WALLPAPER_TOP": rgba("NIGHT_WALLPAPER_TOP"),
        "NIGHT_WALLPAPER_MID": rgba("NIGHT_WALLPAPER_MID"),
        "NIGHT_WALLPAPER_BOTTOM": rgba("NIGHT_WALLPAPER_BOTTOM"),
        "ACCENT_NIGHT_0": arrays["ACCENT_NIGHT"][0],
    }


T = parse_tokens()
print("tokens:", {k: "#%02X%02X%02X" % v for k, v in T.items()})


def hexs(rgb):
    return "#%02X%02X%02X" % rgb


# ---------------------------------------------------------------- masks -----
def squircle_mask(size, n=SQUIRCLE_N):
    """Superellipse |x|^n + |y|^n = 1, binary-sampled at 4x then box-downsampled
    for a clean ~1px antialiased edge (a direct (1-d) ramp is far too wide on a
    near-vertical squircle wall)."""
    hi = size * 4
    ys, xs = np.mgrid[0:hi, 0:hi].astype(np.float64)
    nx = (2.0 * xs / (hi - 1)) - 1.0
    ny = (2.0 * ys / (hi - 1)) - 1.0
    inside = (np.abs(nx) ** n + np.abs(ny) ** n) <= 1.0
    hi_mask = Image.fromarray((inside * 255).astype(np.uint8))
    return hi_mask.resize((size, size), Image.BOX)


def circle_mask(size):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    return m


# ------------------------------------------------------------- background ---
def warm_background(size):
    """Vertical 3-stop night gradient + amber halo, both from tokens."""
    t = np.linspace(0.0, 1.0, size, dtype=np.float64)
    top, mid, bot = (np.array(T[k], dtype=np.float64) for k in
                     ("NIGHT_WALLPAPER_TOP", "NIGHT_WALLPAPER_MID", "NIGHT_WALLPAPER_BOTTOM"))
    up = np.clip(t * 2.0, 0.0, 1.0)[:, None, None]
    down = np.clip((t - 0.5) * 2.0, 0.0, 1.0)[:, None, None]
    col = np.where(t[:, None, None] < 0.5, top + (mid - top) * up, mid + (bot - mid) * down)
    img = np.repeat(col, size, axis=1)  # (size, size, 3) rows constant -> vertical

    yy, xx = np.mgrid[0:size, 0:size].astype(np.float64)
    half = (size - 1) / 2.0
    r = np.sqrt(((xx - half) / half - (HALO_CENTER[0] * 2 - 1)) ** 2 +
                ((yy - half) / half - (HALO_CENTER[1] * 2 - 1)) ** 2) / (HALO_RADIUS * 2 ** 0.5)
    glow = np.clip(1.0 - r, 0.0, 1.0) ** 2 * (HALO_MAX_ALPHA / 255.0)
    accent = np.array(T["ACCENT_NIGHT_0"], dtype=np.float64)
    img = img * (1.0 - glow[..., None]) + accent * glow[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


# ------------------------------------------------------------------ plane ---
def load_plane():
    """Brand art from the repo itself: adaptive foreground, 432px, alpha."""
    return Image.open(PLANE_SRC).convert("RGBA")


def recolor_to_accent(plane):
    """Map the plane onto ACCENT_NIGHT[0], keeping relative luminance shading."""
    arr = np.array(plane).astype(np.float64)
    rgb, alpha = arr[..., :3], arr[..., 3]
    lum = rgb @ LUM
    mean = lum[alpha > 200].mean() if (alpha > 200).any() else lum.max()
    accent = np.array(T["ACCENT_NIGHT_0"], dtype=np.float64)
    scale = np.clip((lum / max(mean, 1.0))[..., None], 0.0, 1.6)
    new_rgb = np.clip(accent[None, None, :] * scale, 0, 255)
    arr[..., :3] = np.where(alpha[..., None] > 0, new_rgb, 0)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def plane_bbox(plane, thresh=20):
    a = np.array(plane)[..., 3]
    ys, xs = np.where(a > thresh)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def fit_plane(plane, tile, fill=LEGACY_FILL):
    """Crop to the plane and scale it to `fill` of the tile, centered."""
    x0, y0, x1, y1 = plane_bbox(plane)
    crop = plane.crop((x0, y0, x1, y1))
    w, h = crop.size
    scale = (fill * tile) / max(w, h)
    fw, fh = max(1, int(w * scale)), max(1, int(h * scale))
    s = crop.resize((fw, fh), Image.LANCZOS)
    out = Image.new("RGBA", (tile, tile), (0, 0, 0, 0))
    out.alpha_composite(s, ((tile - fw) // 2, (tile - fh) // 2))
    return out


# ------------------------------------------------------------------- build --
PLANE = load_plane()
PLANE_ACCENT = recolor_to_accent(PLANE)
print("plane source:", PLANE.size, "bbox:", plane_bbox(PLANE_ACCENT))

SQ1024, CI1024 = squircle_mask(1024), circle_mask(1024)

for d in DENSITIES:
    lm, ad = LAUNCHER[d], ADAPTIVE[d]
    ldir = f"{RES}/mipmap-{d}"

    # adaptive foreground: recolored plane, downsampled per density
    fg = PLANE_ACCENT.resize((ad, ad), Image.LANCZOS)
    fg.save(f"{ldir}/icon_foreground.png", optimize=True)
    fg.save(f"{ldir}/icon_foreground_round.png", optimize=True)
    fg.save(f"{ldir}/icon_foreground_sa.png", optimize=True)

    # legacy: plane on warm gradient, squircle / circle mask
    art = fit_plane(PLANE_ACCENT, 432)
    art432 = warm_background(432)
    art432.alpha_composite(art)
    masked = art432.copy()
    masked.putalpha(SQ1024.resize((432, 432), Image.LANCZOS))
    masked.resize((lm, lm), Image.LANCZOS).save(f"{ldir}/ic_launcher.png", optimize=True)
    masked_r = art432.copy()
    masked_r.putalpha(CI1024.resize((432, 432), Image.LANCZOS))
    masked_r.resize((lm, lm), Image.LANCZOS).save(f"{ldir}/ic_launcher_round.png", optimize=True)

    # adaptive background clip: warm gradient
    bg = warm_background(ad)
    bg.save(f"{ldir}/icon_background_clip.png", optimize=True)
    bg.save(f"{ldir}/icon_background_clip_round.png", optimize=True)
    print(f"mipmap-{d}: launcher {lm}px + adaptive {ad}px written")

b432 = warm_background(432)
b432.save(f"{RES}/drawable/icon_background_clip.webp", "WEBP", quality=90, method=4)
b432.save(f"{RES}/drawable/icon_background_clip_round.webp", "WEBP", quality=90, method=4)
print("drawable webp clips written")

# monochrome themed-icon layer: white silhouette of the same plane
mono = np.array(PLANE_ACCENT)
mono[..., :3] = np.where(mono[..., 3:] > 0, 255, 0)
Image.fromarray(mono, "RGBA").save(f"{RES}/drawable-nodpi/icon_phoenix_mono.png", optimize=True)
print("icon_phoenix_mono (plane silhouette) written")

# fallback background xml — color from tokens, no hardcoded value
with open(f"{RES}/drawable/icon_background_sa.xml", "w", encoding="utf-8") as f:
    f.write(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<shape xmlns:android=\"http://schemas.android.com/apk/res/android\">\n"
        f"    <solid android:color=\"{hexs(T['NIGHT_WALLPAPER_MID'])}\" />\n"
        "</shape>\n")
print("icon_background_sa.xml ->", hexs(T["NIGHT_WALLPAPER_MID"]))

# --------------------------------------------------------------- previews ---
art1024 = fit_plane(PLANE_ACCENT, 1024)
base = warm_background(1024)
base.alpha_composite(art1024)
prev = base.copy()
prev.putalpha(SQ1024)
prev.resize((512, 512), Image.LANCZOS).save("/home/z/my-project/public/icons/ui2-squircle.png")
prev_r = base.copy()
prev_r.putalpha(CI1024)
prev_r.resize((512, 512), Image.LANCZOS).save("/home/z/my-project/public/icons/ui2-round.png")
comp = warm_background(512)
comp.alpha_composite(PLANE_ACCENT.resize((512, 512), Image.LANCZOS))
comp.putalpha(circle_mask(512))
comp.save("/home/z/my-project/public/icons/ui2-adaptive-circle.png")
mono_prev = Image.new("RGBA", (512, 512), (24, 19, 14, 255))
mono_prev.alpha_composite(Image.fromarray(mono, "RGBA").resize((512, 512), Image.LANCZOS))
mono_prev.save("/home/z/my-project/public/icons/ui2-mono.png")
print("previews written")
print("OK")

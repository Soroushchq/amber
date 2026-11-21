#!/usr/bin/env python3
# AmberGram UI 2.0 — مولد فایل تم از پالت مرکزی (قدم ۳/۴ نقشه راه)
# تک منبع حقیقت: AmberTokens.java + AmberPalette.java — این اسکریپت آنها را
# واقعاً تفسیر و ارزیابی می‌کند (بدون تکرار هیچ رنگی) و فایل attheme می‌سازد.
#
# مصرف:
#   python3 Tools/generate_amber_theme2.py night  TMessagesProj/src/main/assets/amber.attheme
#   python3 Tools/generate_amber_theme2.py day    TMessagesProj/src/main/assets/amber_day.attheme [BASE]
#   python3 Tools/generate_amber_theme2.py aurora-night TMessagesProj/src/main/assets/aurora.attheme
#   python3 Tools/generate_amber_theme2.py aurora-day   TMessagesProj/src/main/assets/aurora_day.attheme
#   python3 Tools/generate_amber_theme2.py premiere-night TMessagesProj/src/main/assets/premiere.attheme
#   python3 Tools/generate_amber_theme2.py premiere-day   TMessagesProj/src/main/assets/premiere_day.attheme
#   python3 Tools/generate_amber_theme2.py mario-night TMessagesProj/src/main/assets/mario.attheme
#   python3 Tools/generate_amber_theme2.py mario-day   TMessagesProj/src/main/assets/mario_day.attheme
#
# منطق: فایل شب/روز = کلیدهای پایه (فایل تم فعلی برای پوشش کامل) + overlay کامل پالت جدید.
# کلیدهای پالت بازنویسی می‌شوند؛ بقیه از پایه حفظ می‌شوند تا هیچ صفحه‌ای به
# پیش‌فرض روشن تلگرام برنگردد (سقوط به defaultColors = فاجعه شب روشن).
# برند آئورورا (v0.9.7): شاخه au در build(boolean d, boolean au, boolean pr) + کلید برند
# telegram_color_dialogsLogo که فقط برای فایل‌های آئورورا تزریق می‌شود
# (کهربا مقدار موروثی از base را حفظ می‌کند تا رفتار فعلی تغییر نکند).
# برند شب اکران (v0.9.9): شاخه pr + همان کلید برند (عاج تیتراژ/جوهر پوستر).
# برند دنیای ماریو (v0.9.10): شاخه ma + همان کلید برند (عاج سکه/جوهر اورال).
import re, sys, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "TMessagesProj/src/main/java/org/telegram/messenger")

def jround(x):
    return math.floor(x + 0.5)  # Math.round(float) جاوا

def mask32(v):
    return int(v) & 0xFFFFFFFF

def signed(v):
    v = mask32(v)
    return v - 0x100000000 if v > 0x7FFFFFFF else v

def f_alpha(color, a):
    a8 = jround(a * 255.0) & 0xFF
    return mask32((a8 << 24) | (int(color) & 0xFFFFFF))

def f_over(fg, bg, a):
    fa = float(a)
    fr, fgc, fb = (int(fg) >> 16) & 0xFF, (int(fg) >> 8) & 0xFF, int(fg) & 0xFF
    br, bgc, bb = (int(bg) >> 16) & 0xFF, (int(bg) >> 8) & 0xFF, int(bg) & 0xFF
    r = jround(fr * fa + br * (1 - fa))
    g = jround(fgc * fa + bgc * (1 - fa))
    b = jround(fb * fa + bb * (1 - fa))
    return mask32((0xFF << 24) | (r << 16) | (g << 8) | b)

# ── ۱) ثابت‌های AmberTokens ────────────────────────────────────────────────
def load_tokens():
    toks = {}
    with open(os.path.join(SRC, "AmberTokens.java"), encoding="utf-8") as fh:
        src = fh.read()
    for m in re.finditer(r"public static final int (\w+) = (0x[0-9A-Fa-f]+);", src):
        toks[m.group(1)] = mask32(int(m.group(2), 16))
    for m in re.finditer(r"public static final float (\w+) = ([0-9.]+)f?;", src):
        toks[m.group(1)] = float(m.group(2))
    if len(toks) < 40:
        sys.exit(f"FATAL: only {len(toks)} tokens parsed from AmberTokens.java")
    return toks

# ── ۲) تبدیل عبارت جاوا به پایتون ─────────────────────────────────────────
def translate_ternaries(s):
    # فقط یک سطح ternary با شرط d یا au یا pr یا ma — اسکن دقیق مرزها با ردیابی عمق پرانتز
    while True:
        m = re.search(r"\b(d|au|pr|ma) \?", s)
        if not m:
            return s
        i = m.start() + len(m.group(0))
        # A: تا ' : ' هم‌سطح
        depth = 0
        j = i
        while j < len(s):
            c = s[j]
            if c in "([":
                depth += 1
            elif c in ")]":
                depth -= 1
            elif depth == 0 and s[j:j+3] == " : ":
                break
            j += 1
        if j >= len(s):
            sys.exit(f"FATAL: ternary A-boundary not found in: {s}")
        a_branch = s[i:j]
        # B: تا مرز هم‌سطح (پرانتز بسته بیرونی / کاما / سمی‌کالن)
        depth = 0
        k = j + 3
        while k < len(s):
            c = s[k]
            if c in "([":
                depth += 1
            elif c in ")]":
                if depth == 0:
                    break
                depth -= 1
            elif (c == "," and depth == 0) or c == ";":
                break
            k += 1
        b_branch = s[j+3:k]
        s = s[:m.start()] + f"({a_branch} if {m.group(1)} else {b_branch})" + s[k:]

def java_to_py(expr):
    s = translate_ternaries(expr.strip())
    s = s.replace("AmberTokens.alpha(", "f_alpha(")
    s = s.replace("AmberTokens.over(", "f_over(")
    s = s.replace("AmberTokens.", "")
    s = re.sub(r"(\d+\.\d+)f", r"\1", s)  # پسوند float
    return s

# ── ۳) ارزیابی build() برای d/au/pr/ma مشخص ──────────────────────────────
def eval_palette(d_value, au_value, pr_value, ma_value, tokens):
    ns = dict(tokens)
    ns["f_alpha"] = f_alpha
    ns["f_over"] = f_over
    ns["d"] = d_value
    ns["au"] = au_value
    ns["pr"] = pr_value
    ns["ma"] = ma_value
    palette = {}
    in_build = False
    with open(os.path.join(SRC, "AmberPalette.java"), encoding="utf-8") as fh:
        for line in fh:
            t = line.strip()
            if "private static Map<String, Integer> build" in t:
                in_build = True
                continue
            if not in_build:
                continue
            if t.startswith("return m;"):
                break
            mloc = re.match(r"final (?:boolean|int) (\w+)\s+= (.*);$", t)
            if mloc and mloc.group(1) not in ("d", "au", "pr", "ma"):
                name, expr = mloc.group(1), java_to_py(mloc.group(2))
                ns[name] = mask32(eval(expr, {"__builtins__": {}}, ns))
                continue
            mput = re.match(r'm\.put\("([^"]+)", (.*)\);$', t)
            if mput:
                key, expr = mput.group(1), java_to_py(mput.group(2))
                palette[key] = mask32(eval(expr, {"__builtins__": {}}, ns))
    if len(palette) < 400:
        sys.exit(f"FATAL: only {len(palette)} palette entries evaluated")
    return palette

# ── ۴) فایل پایه ──────────────────────────────────────────────────────────
def parse_theme_value(v):
    v = v.strip()
    if v.startswith("#"):  # #RRGGBB یا #AARRGGBB — مثل Color.parseColor
        h = v[1:]
        if len(h) == 6:
            h = "FF" + h
        return int(h, 16)
    return int(v)

def load_base(path):
    base = {}
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line or "=" not in line or line.startswith(("WLS=", "WPS")):
                continue
            k, v = line.split("=", 1)
            base[k] = parse_theme_value(v)
    return base

# ── ۵) تولید ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 3:
        sys.exit("usage: generate_amber_theme2.py night|day|aurora-night|aurora-day|premiere-night|premiere-day|mario-night|mario-day OUT [BASE]")
    mode, out_path = sys.argv[1], sys.argv[2]
    asset_dir = os.path.join(ROOT, "TMessagesProj/src/main/assets")
    if len(sys.argv) > 3:
        base_path = sys.argv[3]
    elif mode == "day":
        base_path = os.path.join(asset_dir, "amber_day.attheme")
    elif mode == "aurora-night":
        base_path = os.path.join(asset_dir, "amber.attheme")
    elif mode == "aurora-day":
        base_path = os.path.join(asset_dir, "amber_day.attheme")
    elif mode == "premiere-night":
        base_path = os.path.join(asset_dir, "amber.attheme")
    elif mode == "premiere-day":
        base_path = os.path.join(asset_dir, "amber_day.attheme")
    elif mode == "mario-night":
        base_path = os.path.join(asset_dir, "amber.attheme")
    elif mode == "mario-day":
        base_path = os.path.join(asset_dir, "amber_day.attheme")
    else:
        base_path = os.path.join(asset_dir, "amber.attheme")
    d = mode in ("day", "aurora-day", "premiere-day", "mario-day")
    au = mode.startswith("aurora")
    pr = mode.startswith("premiere")
    ma = mode.startswith("mario")
    tokens = load_tokens()
    palette = eval_palette(d, au, pr, ma, tokens)
    base = load_base(base_path)
    if not au and not pr and not ma:
        # قرارداد برند (v0.9.7): برای فایل‌های کهربا فقط کلیدهای موجود در پایه نوشته
        # می‌شوند — بخش «اکسنت‌های مکمل» پالت کلیدهای جدیدی دارد که شاخهٔ کهربایشان
        # مقدار فایل شب است و نباید فایل روز کهربا (که این کلیدها را ندارد و به
        # پیش‌فرض آپستریم برمی‌گردد) را تغییر دهد. فایل‌های کهربا فrozen هستند.
        palette = {k: v for k, v in palette.items() if k in base}
    merged = dict(base)
    replaced = sum(1 for k in palette if k in merged)
    added = sum(1 for k in palette if k not in merged)
    merged.update(palette)
    if au:
        # کلید برند لوگو — تینت MULTIPLY لوگوی هدر؛ فقط برای فایل‌های آئورورا
        # (کهربا: مقدار موروثی از base حفظ می‌شود تا رفتار فعلی تغییر نکند)
        merged["telegram_color_dialogsLogo"] = 0xFF171B26 if d else 0xFFF2F1F7
    if pr:
        # کلید برند لوگو برای شب اکران — عاج تیتراژ در شب / جوهر پوستر در روز
        merged["telegram_color_dialogsLogo"] = 0xFF2E2513 if d else 0xFFF7F0E1
    if ma:
        # کلید برند لوگو برای دنیای ماریو — عاج سکه در شب / جوهر اورال در روز
        merged["telegram_color_dialogsLogo"] = 0xFF16243E if d else 0xFFF6F2E6
    lines = [f"{k}={signed(merged[k])}" for k in sorted(merged)]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    # ── راستی‌آزمایی رفت‌وبرگشت ──
    back = load_base(out_path)
    errs = []
    for k, v in palette.items():
        if k not in back or mask32(back[k]) != mask32(v):
            errs.append(k)
    if au or pr or ma:
        k = "telegram_color_dialogsLogo"
        if k not in back or mask32(back[k]) != mask32(merged[k]):
            errs.append(k)
    if errs:
        sys.exit(f"FATAL: round-trip mismatch for {len(errs)} keys: {errs[:8]}")
    print(f"OK {mode}: base={len(base)} palette={len(palette)} replaced={replaced} added={added} total={len(merged)}")
    for k in ("windowBackgroundWhite", "chat_inBubble", "chat_outBubble", "divider", "chats_unreadCounterText", "chat_wallpaper", "chat_wallpaper_gradient_to", "key_chat_wallpaper_gradient_to2", "key_chat_wallpaper_gradient_to3", "avatar_backgroundBlue", "telegram_color_dialogsLogo"):
        v = merged.get(k)
        if v is not None:
            print(f"  {k} = 0x{mask32(v):08X}")

if __name__ == "__main__":
    main()

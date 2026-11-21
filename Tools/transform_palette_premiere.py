#!/usr/bin/env python3
# مبدل یک‌بارمصرف — تزریق برند «شب اکران» به AmberPalette.java (v0.9.9-ui2)
# الگوی عیناً transform_palette_aurora.py:
# ۱) پوشش مکانیکی هر ternary هم‌پسوندِ آئورورا:
#    au ? (d ? AURORA_DAY_X : AURORA_NIGHT_X) : (d ? DAY_X : NIGHT_X)
#    → au ? (...) : pr ? (d ? PREMIERE_DAY_X : PREMIERE_NIGHT_X) : (d ? DAY_X : NIGHT_X)
# ۲) جدول جایگزینی صریح برای شاخه‌های اختصاصی (کد/جدول/سوییچ/آواتار/شیشه/سینما)
# ۳) بخش «اکسنت‌های مکمل» — بازنویسی با مپ کلید→رنگ سینمایی
# هر جایگزینی باید دقیقاً یک‌بار رخ دهد؛ وگرنه اسکریپت FATAL می‌دهد.
import re, sys

PATH = "TMessagesProj/src/main/java/org/telegram/messenger/AmberPalette.java"
src = open(PATH, encoding="utf-8").read()

EXPLICIT = []

# ── ۱) سرِ کلاس: کش‌ها + mode‌های شب اکران + امضای build ──────────────────────
EXPLICIT.append((
    """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا) و MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا).
     * برند دوم v0.9.7 — «شیشه و نور». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false, false);
            }
            return nightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_NIGHT) {
            if (auroraNightCache == null) {
                auroraNightCache = build(false, true);
            }
            return auroraNightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_DAY) {
            if (auroraDayCache == null) {
                auroraDayCache = build(true, true);
            }
            return auroraDayCache;
        }
        if (dayCache == null) {
            dayCache = build(true, false);
        }
        return dayCache;
    }""",
    """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;
    private static Map<String, Integer> premiereDayCache;
    private static Map<String, Integer> premiereNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا)، MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا)
     * و MODE_PREMIERE_NIGHT / MODE_PREMIERE_DAY (شب اکران).
     * برند سوم v0.9.9 — «عصر طلایی هالیوود». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false, false, false);
            }
            return nightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_NIGHT) {
            if (auroraNightCache == null) {
                auroraNightCache = build(false, true, false);
            }
            return auroraNightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_DAY) {
            if (auroraDayCache == null) {
                auroraDayCache = build(true, true, false);
            }
            return auroraDayCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_NIGHT) {
            if (premiereNightCache == null) {
                premiereNightCache = build(false, false, true);
            }
            return premiereNightCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_DAY) {
            if (premiereDayCache == null) {
                premiereDayCache = build(true, false, true);
            }
            return premiereDayCache;
        }
        if (dayCache == null) {
            dayCache = build(true, false, false);
        }
        return dayCache;
    }"""
))

EXPLICIT.append((
    "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) در برابر برند کهربا */\n"
    "    private static Map<String, Integer> build(boolean d, boolean au) {",
    "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) — pr = برند شب اکران (عصر طلایی هالیوود) در برابر برند کهربا */\n"
    "    private static Map<String, Integer> build(boolean d, boolean au, boolean pr) {"
))

# ── ۲) پوشش مکانیکی هم‌پسوند ─────────────────────────────────────────────────
def wrap(m):
    sfx = m.group(1)
    return (f"au ? (d ? AmberTokens.AURORA_DAY_{sfx} : AmberTokens.AURORA_NIGHT_{sfx})"
            f" : pr ? (d ? AmberTokens.PREMIERE_DAY_{sfx} : AmberTokens.PREMIERE_NIGHT_{sfx})"
            f" : (d ? AmberTokens.DAY_{sfx} : AmberTokens.NIGHT_{sfx})")

mech = re.compile(
    r"au \? \(d \? AmberTokens\.AURORA_DAY_([A-Za-z_]+) : AmberTokens\.AURORA_NIGHT_\1\)"
    r" : \(d \? AmberTokens\.DAY_\1 : AmberTokens\.NIGHT_\1\)")
src, mech_count = mech.subn(wrap, src)

# ── ۳) جدول صریح — شاخه‌های نامتقارن (پسوند متفاوت دو سو) ──────────────────
# اتم white: شب شب‌اکران = پس‌زمینهٔ اصلی تالار (نه توقف والپیپر)
EXPLICIT.append((
    "        final int white = au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_BG) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP);",
    "        final int white = au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_BG : AmberTokens.PREMIERE_NIGHT_BG) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP);"
))
# divider: خطوط مرئی — شب آلفای اوتلاین، روز اوتلاین جامد
EXPLICIT.append((
    "        final int divider = au ? (d ? AmberTokens.AURORA_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.AURORA_NIGHT_OUTLINE, 0.55f)) : (d ? AmberTokens.DAY_OUTLINE : AmberTokens.alpha(AmberTokens.NIGHT_OUTLINE, 0.55f));",
    "        final int divider = au ? (d ? AmberTokens.AURORA_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.AURORA_NIGHT_OUTLINE, 0.55f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.PREMIERE_NIGHT_OUTLINE, 0.55f)) : (d ? AmberTokens.DAY_OUTLINE : AmberTokens.alpha(AmberTokens.NIGHT_OUTLINE, 0.55f));"
))
EXPLICIT.append((
    'm.put("windowBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));',
    'm.put("windowBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));'
))
EXPLICIT.append((
    'm.put("actionBarDefaultArchived", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));',
    'm.put("actionBarDefaultArchived", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));'
))
# حالت کم‌حجم چت (کامپکت) — بستر = وایپرپ
EXPLICIT.append((
    'm.put("chat_compact_background", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));',
    'm.put("chat_compact_background", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));'
))
EXPLICIT.append((
    'm.put("chat_compact_backgroundGradient", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000), 0.03f));',
    'm.put("chat_compact_backgroundGradient", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000), 0.03f));'
))
EXPLICIT.append((
    'm.put("chat_compact_outBackground", AmberTokens.over(outBubble, au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), d ? 0.85f : 0.55f));',
    'm.put("chat_compact_outBackground", AmberTokens.over(outBubble, au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), d ? 0.85f : 0.55f));'
))
EXPLICIT.append((
    'm.put("chat_compact_fadeEdge", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));',
    'm.put("chat_compact_fadeEdge", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));'
))
EXPLICIT.append((
    'm.put("chat_compact_fadeMiddle", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), 0.64f));',
    'm.put("chat_compact_fadeMiddle", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), 0.64f));'
))
EXPLICIT.append((
    'm.put("chat_recordedVoiceBackground", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_HEADER_BORDER) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_HEADER_BORDER));',
    'm.put("chat_recordedVoiceBackground", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_HEADER_BORDER) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER : AmberTokens.PREMIERE_NIGHT_HEADER_BORDER) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_HEADER_BORDER));'
))
EXPLICIT.append((
    'm.put("chat_messagePanelShadow", au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000));',
    'm.put("chat_messagePanelShadow", au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000));'
))
EXPLICIT.append((
    'm.put("dialogBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));',
    'm.put("dialogBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));'
))
EXPLICIT.append((
    'm.put("profile_actionBackground", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));',
    'm.put("profile_actionBackground", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));'
))

# ── ۳ب) جدول صریح — مشتق‌های اختصاصی ─────────────────────────────────────────
# svcBg: چیپ سرویس — شب: سطح مخمل (نه متن) مثل آئورورا؛ روز: جوهر
EXPLICIT.append((
    "final int svcBg = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_SURFACE), d ? 0.65f : 0.70f);",
    "final int svcBg = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_SURFACE), d ? 0.65f : 0.70f);"
))
EXPLICIT.append((
    "final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);",
    "final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.over(AmberTokens.PREMIERE_NIGHT_TEXT, AmberTokens.PREMIERE_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);"
))
EXPLICIT.append((
    "final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);",
    "final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);"
))
EXPLICIT.append((
    "final int goDown = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE), d ? 0.90f : 0.80f);",
    "final int goDown = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE), d ? 0.90f : 0.80f);"
))
# deepFile — بستر فایل/مخاطب/موقعیت داخل حباب‌ها: مخمل عمیق‌تر شب / کرم پوستر روز
EXPLICIT.append((
    "final int deepFile = au ? (d ? 0xFFE9EEF6 : 0xFF1B2430) : (d ? 0xFFF7E3C8 : 0xFF2E2618);",
    "final int deepFile = au ? (d ? 0xFFE9EEF6 : 0xFF1B2430) : pr ? (d ? 0xFFFFF0D2 : 0xFF241C36) : (d ? 0xFFF7E3C8 : 0xFF2E2618);"
))
# outTime — ساعت/متن ثانویه روی حباب خروجی: برنز تیره روی طلای اکران
EXPLICIT.append((
    "final int outTime = au ? (d ? 0xFF0E7260 : 0xFF7FE8D0) : (d ? 0xFFA8701E : 0xFFD9BC7A);",
    "final int outTime = au ? (d ? 0xFF0E7260 : 0xFF7FE8D0) : pr ? (d ? 0xFF7A5A08 : 0xFF5C3D02) : (d ? 0xFFA8701E : 0xFFD9BC7A);"
))
# sentCheckRead — تیک خوانده‌شده روی حباب خروجی: برنز برشته روی طلای روز / برنز عمیق روی طلای شب
EXPLICIT.append((
    "final int sentCheckRead = au ? (d ? 0xFF06503F : AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT) : (d ? 0xFF9C5200 : AmberTokens.NIGHT_ACCENT_BRIGHT);",
    "final int sentCheckRead = au ? (d ? 0xFF06503F : AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT) : pr ? (d ? 0xFF8A5C06 : 0xFF4A3202) : (d ? 0xFF9C5200 : AmberTokens.NIGHT_ACCENT_BRIGHT);"
))

# سایهٔ پنجرهٔ روز — سایه گرم بنفش‌فام شب اکران
EXPLICIT.append((
    'm.put("windowBackgroundGrayShadow", au ? (d ? 0x14171B26 : 0x28000000) : (d ? 0x14211A12 : 0x28000000));',
    'm.put("windowBackgroundGrayShadow", au ? (d ? 0x14171B26 : 0x28000000) : pr ? (d ? 0x14332A18 : 0x28000000) : (d ? 0x14211A12 : 0x28000000));'
))

# وایپرپ گرادیانی «پرتوهای افکتور» — توقف‌های چهاررنگ سینمایی
EXPLICIT.append((
    'm.put("chat_wallpaper", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));',
    'm.put("chat_wallpaper", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));'
))
EXPLICIT.append((
    'm.put("chat_wallpaper_gradient_to", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_BOTTOM : AmberTokens.AURORA_NIGHT_WALLPAPER_TOP) : (d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP));',
    'm.put("chat_wallpaper_gradient_to", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_BOTTOM : AmberTokens.AURORA_NIGHT_WALLPAPER_TOP) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_BOTTOM : AmberTokens.PREMIERE_NIGHT_WALLPAPER_TOP) : (d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP));'
))
EXPLICIT.append((
    'm.put("key_chat_wallpaper_gradient_to2", au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_WALLPAPER_BOTTOM) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM));',
    'm.put("key_chat_wallpaper_gradient_to2", au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_WALLPAPER_BOTTOM) : pr ? (d ? AmberTokens.PREMIERE_DAY_BG : AmberTokens.PREMIERE_NIGHT_WALLPAPER_BOTTOM) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM));'
))
EXPLICIT.append((
    'm.put("key_chat_wallpaper_gradient_to3", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE));',
    'm.put("key_chat_wallpaper_gradient_to3", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE));'
))

# سوییچ‌ها
for key in ("switch2Track", "switchTrack", "switchTrackBlue"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));',
        f'm.put("{key}", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : pr ? (d ? 0xFFE7DBBE : AmberTokens.PREMIERE_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));'
    ))
EXPLICIT.append((
    'm.put("switchTrackBlueThumb", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT_DIM) : (d ? 0xFFFFF8F1 : AmberTokens.NIGHT_TEXT_DIM));',
    'm.put("switchTrackBlueThumb", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT_DIM) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT_DIM) : (d ? 0xFFFFF8F1 : AmberTokens.NIGHT_TEXT_DIM));'
))

# جدول/کد داخل حباب‌ها
EXPLICIT.append((
    'm.put("chat_inTableBackground", au ? (d ? 0xFFF4F6FA : 0xFF212A38) : (d ? 0xFFFFFDF8 : 0xFF2E2618));',
    'm.put("chat_inTableBackground", au ? (d ? 0xFFF4F6FA : 0xFF212A38) : pr ? (d ? 0xFFFFF8E8 : 0xFF241C36) : (d ? 0xFFFFFDF8 : 0xFF2E2618));'
))
for key in ("chat_inCodeBackground", "chat_inArticleCodeBackground"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : 0xFF1B2430) : (d ? 0xFFF7EFE4 : 0xFF211B12));',
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : 0xFF1B2430) : pr ? (d ? 0xFFFFF6E0 : 0xFF1E1730) : (d ? 0xFFF7EFE4 : 0xFF211B12));'
    ))
# داخل حباب خروجی طلایی: بستر تیره‌تر از طلای اکران (کنتراست فایل/کد داخل حباب)
for key in ("chat_outFileBackground", "chat_outContactBackground"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFBEEBDF : 0xFF17544A) : (d ? 0xFFFBCE8F : 0xFF6E5200));',
        f'm.put("{key}", au ? (d ? 0xFFBEEBDF : 0xFF17544A) : pr ? (d ? 0xFFE0B25A : 0xFFC7891B) : (d ? 0xFFFBCE8F : 0xFF6E5200));'
    ))
EXPLICIT.append((
    'm.put("chat_outTableBackground", au ? (d ? 0xFFC4EFE4 : 0xFF17544A) : (d ? 0xFFFBF1DD : 0xFF6E5200));',
    'm.put("chat_outTableBackground", au ? (d ? 0xFFC4EFE4 : 0xFF17544A) : pr ? (d ? 0xFFEDC468 : 0xFFD0911F) : (d ? 0xFFFBF1DD : 0xFF6E5200));'
))
for key in ("chat_outCodeBackground", "chat_outArticleCodeBackground"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFB8E9DC : 0xFF12463E) : (d ? 0xFFF6E3C2 : 0xFF524000));',
        f'm.put("{key}", au ? (d ? 0xFFB8E9DC : 0xFF12463E) : pr ? (d ? 0xFFE8BE55 : 0xFFC28218) : (d ? 0xFFF6E3C2 : 0xFF524000));'
    ))
EXPLICIT.append((
    'm.put("chat_outPollCorrectAnswer", au ? (d ? 0xFF0E8A6E : 0xFF8AD9BC) : (d ? 0xFF3D7A2B : 0xFF9BC77E));',
    'm.put("chat_outPollCorrectAnswer", au ? (d ? 0xFF0E8A6E : 0xFF8AD9BC) : pr ? (d ? 0xFF0C8A7E : 0xFF3FD2C7) : (d ? 0xFF3D7A2B : 0xFF9BC77E));'
))

# سرویس/دکمهٔ بات/پنل‌ها
for key in ("chat_serviceText", "chat_serviceIcon", "chat_fieldOverlayText", "chat_botButtonText"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));',
        f'm.put("{key}", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));'
    ))
EXPLICIT.append((
    'm.put("chat_serviceLink", au ? (d ? 0xFFDCF7F0 : 0xFFDCFFF4) : (d ? 0xFFFFEFC9 : 0xFFFFDDB8));',
    'm.put("chat_serviceLink", au ? (d ? 0xFFDCF7F0 : 0xFFDCFFF4) : pr ? (d ? 0xFFFFF1CC : 0xFFFFF6DC) : (d ? 0xFFFFEFC9 : 0xFFFFDDB8));'
))
for key in ("chat_stickersHintPanel", "chat_emojiPanelBackground", "chat_emojiPanelStickerPackSelector"):
    EXPLICIT.append((
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));',
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? 0xFFFFF6E4 : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));'
    ))

# دکمه‌های ضمیمه — سینما: صدا = کریمسون تند (پرده)، مخاطب = برنز تندیس
EXPLICIT.append((
    'm.put("chat_attachAudioBackground", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : (d ? 0xFFB4382C : 0xFFE2695B));',
    'm.put("chat_attachAudioBackground", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : pr ? (d ? 0xFFC42B4B : 0xFFE8445E) : (d ? 0xFFB4382C : 0xFFE2695B));'
))
EXPLICIT.append((
    'm.put("chat_attachContactBackground", au ? (d ? 0xFFB3651F : 0xFFFFB454) : (d ? 0xFF8C6A1D : 0xFFC79A3E));',
    'm.put("chat_attachContactBackground", au ? (d ? 0xFFB3651F : 0xFFFFB454) : pr ? (d ? 0xFF8A5E0C : 0xFFC77E14) : (d ? 0xFF8C6A1D : 0xFFC79A3E));'
))

# شیشهٔ ناوبری اصلی — مخمل شب اکران
EXPLICIT.append((
    'm.put("glass_targetMainTabs", au ? (d ? 0xE6F5F5FA : 0xE60B0F16) : (d ? 0xE6FFF6EA : 0xE6241D14));',
    'm.put("glass_targetMainTabs", au ? (d ? 0xE6F5F5FA : 0xE60B0F16) : pr ? (d ? 0xE6FFF6E4 : 0xE6181326) : (d ? 0xE6FFF6EA : 0xE6241D14));'
))
EXPLICIT.append((
    'm.put("glass_targetMainTopPanel", au ? (d ? 0xE6FFFFFF : 0xE612151B) : (d ? 0xE6FFE9CF : 0xE61F1912));',
    'm.put("glass_targetMainTopPanel", au ? (d ? 0xE6FFFFFF : 0xE612151B) : pr ? (d ? 0xE6FFFBEF : 0xE6120F1B) : (d ? 0xE6FFE9CF : 0xE61F1912));'
))
# Instant View پس‌زمینهٔ خاکستری
EXPLICIT.append((
    'm.put("iv_backgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));',
    'm.put("iv_backgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));'
))
# آواتار پس‌زمینهٔ پروفایل (پسوند نامتقارن — مکانیکی نمی‌شود)
EXPLICIT.append((
    'm.put("avatar_backgroundInProfileBlue", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));',
    'm.put("avatar_backgroundInProfileBlue", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));'
))

# ── ۴) آواتارها — بازنویسی کامل بخش با جفت‌های سینمایی ──────────────────────
# شب اکران: طلای اکران/فیروزه مارکی/بنفش رگالی/کریمسون/مرجانی/برنز
AVATAR_KEYS = [
    ("avatar_backgroundBlue",        "0xFF16.54".replace("16.54",""),  None),  # placeholder — replaced below
]
OLD_AVATARS = []
NEW_AVATARS = []
AVATAR_MAP = {
    "avatar_backgroundBlue":         ("0xFFFFD37A", "0xFFF0B449"),
    "avatar_background2Blue":        ("0xFFB96A0B", "0xFF8A5606"),
    "avatar_backgroundCyan":         ("0xFF7FE6D8", "0xFF3FD2C7"),
    "avatar_background2Cyan":        ("0xFF0F8A7E", "0xFF1B7F76"),
    "avatar_backgroundGreen":        ("0xFFD3BDF2", "0xFFA86BE0"),
    "avatar_background2Green":       ("0xFF5C2E8C", "0xFF3F2064"),
    "avatar_backgroundOrange":       ("0xFFF4A0AE", "0xFFE8445E"),
    "avatar_background2Orange":      ("0xFF8C1F35", "0xFF6E1224"),
    "avatar_backgroundPink":         ("0xFFE8445E", "0xFFD63852"),
    "avatar_background2Pink":        ("0xFF6E1224", "0xFF8C1F35"),
    "avatar_backgroundRed":          ("0xFFFFB38E", "0xFFFF8A5C"),
    "avatar_background2Red":         ("0xFFC24B23", "0xFFA03D18"),
    "avatar_backgroundViolet":       ("0xFF5C2E8C", "0xFF3F2064"),
    "avatar_background2Violet":      ("0xFFD3BDF2", "0xFFA86BE0"),
    "avatar_backgroundSaved":        ("0xFFC77E14", "0xFF8A5606"),
    "avatar_background2Saved":       ("0xFF8A5606", "0xFF5C3D02"),
    "avatar_nameInMessageBlue":      ("0xFF8A5E0C", "0xFFF0B449"),
    "avatar_nameInMessageCyan":      ("0xFF5C2E8C", "0xFFD3BDF2"),
    "avatar_nameInMessageGreen":     ("0xFF0C8A7E", "0xFF7FE6D8"),
    "avatar_nameInMessageOrange":    ("0xFFA76F0F", "0xFFF0B449"),
    "avatar_nameInMessagePink":      ("0xFFC42B4B", "0xFFF4A0AE"),
    "avatar_nameInMessageRed":       ("0xFFA03D18", "0xFFFFB38E"),
    "avatar_nameInMessageViolet":    ("0xFF4A3E8C", "0xFFC9B8F5"),
    "avatar_backgroundArchived":     ("0xFFB5A88E", "0xFF5E5570"),
    "avatar_backgroundArchivedHidden": ("0xFFE4DAC4", "0xFF2E2440"),
}

def avatar_transform(line_src):
    # هر خط آواتار au ? (d ? X : Y) : (d ? Z : W)); → pr branch اضافه می‌شود
    m = re.match(
        r'(\s*m\.put\("(avatar_[A-Za-z2]+)", )au \? \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\) : \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\)\);\s*$',
        line_src)
    if m:
        key = m.group(2)
        if key in AVATAR_MAP:
            pd, pn = AVATAR_MAP[key]
            return (f'{m.group(1)}au ? (d ? {m.group(3)} : {m.group(4)})'
                    f' : pr ? (d ? {pd} : {pn})'
                    f' : (d ? {m.group(5)} : {m.group(6)}));')
    m2 = re.match(r'(\s*m\.put\("avatar_text", )au \? (0x[0-9A-F]+) : \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\)\);\s*$', line_src)
    if m2:
        return f'{m2.group(1)}au ? {m2.group(2)} : pr ? (d ? 0xFFFFFFFF : 0xFFFFF6EC) : (d ? {m2.group(3)} : {m2.group(4)}));'
    return None

lines = src.split("\n")
avatar_hits = 0
for i, ln in enumerate(lines):
    if "m.put(\"avatar_" in ln and "au ?" in ln and "pr ?" not in ln:
        new = avatar_transform(ln)
        if new is not None:
            lines[i] = new
            avatar_hits += 1
src = "\n".join(lines)
if avatar_hits != 26:
    sys.exit(f"FATAL: avatar branch transform expected 26 lines, got {avatar_hits}")

# ── ۵) بخش «اکسنت‌های مکمل» — مپ کلید → جفت سینمایی ─────────────────────────
# اکسنت اصلی (طلای مارکی) / متن روی اکسنت / بنفش رگالی / کریمسون / برنز
GOLD      = ("0xFFA76F0F", "0xFFF0B449")   # اکسنت اصلی
GOLD_TEXT = ("0xFF7A5A0C", "0xFFF3BC55")   # متن روی بستر اکسنت/تیره
GOLD_SOFT = ("0xFF8A5E0C", "0xFFC88A1E")   # اکسنت ملایم‌تر
PURPLE    = ("0xFF5C2E8C", "0xFFA86BE0")   # جایگزین آبی/بنفش
CRIMSON   = ("0xFFC42B4B", "0xFFE8445E")   # جایگزین طلایی/زرد شاخص
VELVET_L  = ("0xFFF1E4C8", "0xFF241C36")   # سطح روشن مخمل/تیره
VELVET_L2 = ("0xFFF4E8D0", "0xFF1E1730")
VELVET_L3 = ("0xFFF0E2C2", "0xFF2A2040")
SUPPLEMENT = {
    "avatar_actionBarSelectorGreen": ("0xFFE8DCC2", "0xFF2E2440"),
    "botKeyboard_button_primary": GOLD,
    "buttonNeutralText": GOLD_TEXT,
    "changephoneinfo_image2": GOLD,
    "chat_emojiPanelBadgeBackground": GOLD,
    "chats_tabUnreadActiveBackground": GOLD,
    "color_blue": GOLD,
    "color_lightblue": PURPLE,
    "color_orange": ("0xFFC77E14", "0xFFF0B449"),
    "color_yellow": CRIMSON,
    "contacts_inviteBackground": GOLD,
    "contextProgressInner2": VELVET_L,
    "contextProgressInner3": ("0xFFB96A0B", "0xFF8A5606"),
    "contextProgressInner4": GOLD,
    "contextProgressOuter1": GOLD,
    "fastScrollActive": GOLD,
    "featuredStickers_addButton2": GOLD_SOFT,
    "featuredStickers_addedIcon": GOLD,
    "featuredStickers_buttonProgress": GOLD_TEXT,
    "featuredStickers_unread": GOLD,
    "files_folderIconBackground": GOLD_SOFT,
    "fill_RedDark": ("0xFFB42B45", "0xFFCC4A3A"),
    "gift_ribbon": ("0xFFE8DCC2", "0xFF2E2440"),
    "inappPlayerPlayPause": GOLD,
    "key_player_progressCachedBackground": ("0xFFE8D4B0", "0xFF33294A"),
    "location_actionBackground": GOLD,
    "location_liveLocationProgress": GOLD_SOFT,
    "location_placeLocationBackground": GOLD_SOFT,
    "location_sendLiveLocationBackground": GOLD,
    "location_sendLiveLocationText": GOLD,
    "location_sendLocationBackground": GOLD,
    "location_sendLocationIcon": GOLD,
    "location_sendLocationText": GOLD,
    "login_progressInner": GOLD,
    "passport_authorizeBackground": GOLD,
    "passport_authorizeBackgroundSelected": GOLD,
    "passport_authorizeText": GOLD_TEXT,
    "picker_badge": GOLD,
    "picker_enabledButton": GOLD,
    "player_buttonActive": GOLD,
    "player_progress": GOLD,
    "pollCreateIcons": GOLD_TEXT,
    "premiumCoinGradient1": ("0xFF8A5E0C", "0xFF6E4A08"),
    "premiumCoinGradient2": GOLD,
    "premiumGradient0": ("0xFF4A3208", "0xFF2E1F06"),
    "premiumGradient1": ("0xFF5C3D08", "0xFF3A2808"),
    "premiumGradient2": ("0xFF8A5E0C", "0xFF6E4A08"),
    "premiumGradient3": ("0xFFB96A0B", "0xFF8A5606"),
    "premiumGradient4": GOLD,
    "premiumGradientBottomSheet1": ("0xFF5C3D08", "0xFF3A2808"),
    "premiumGradientBottomSheet2": ("0xFF8A5E0C", "0xFF6E4A08"),
    "premiumGradientBottomSheet3": GOLD,
    "premiumStarGradient1": ("0xFFA76F0F", "0xFFE9A93A"),
    "premiumStartSmallStarsColor": ("0x71A76F0F", "0x71E9A93A"),
    "progressCircle": GOLD,
    "reactionStarSelector": GOLD,
    "returnToCallBackground": GOLD_SOFT,
    "sessions_devicesImage": ("0xFFEDE2CC", "0xFF14101F"),
    "sharedMedia_startStopLoadIcon": ("0xFFC77E14", "0xFFF0B449"),
    "statisticChartActivePickerChart": ("0xD8E7DCC2", "0xD8332A48"),
    "statisticChartBackZoomColor": GOLD,
    "statisticChartLine_blue": GOLD,
    "statisticChartLine_golden": CRIMSON,
    "statisticChartLine_lightblue": PURPLE,
    "statisticChartLine_orange": ("0xFFC77E14", "0xFFF0B449"),
    "statisticChartRipple": ("0x2CA76F0F", "0x2CF0B449"),
    "stickers_menu": ("0xFFE8DCC2", "0xFF2E2440"),
    "telegram_color": GOLD,
    "telegram_color_text": GOLD_TEXT,
    "undo_cancelColor": GOLD_TEXT,
    "voipgroup_checkMenu": GOLD_TEXT,
    "voipgroup_connectingProgress": GOLD,
    "voipgroup_listeningText": GOLD_TEXT,
    "voipgroup_muteButton": GOLD,
    "voipgroup_muteButton2": GOLD_SOFT,
    "voipgroup_muteButton3": GOLD_SOFT,
    "voipgroup_overlayBlue1": VELVET_L,
    "voipgroup_overlayBlue2": VELVET_L2,
    "voipgroup_overlayGreen1": VELVET_L2,
    "voipgroup_overlayGreen2": VELVET_L,
    "voipgroup_rtmpButton": GOLD,
    "voipgroup_soundButtonActive": GOLD,
    "voipgroup_soundButtonActive2": GOLD_SOFT,
    "voipgroup_soundButtonActive2Scrolled": GOLD_SOFT,
    "voipgroup_soundButtonActiveScrolled": GOLD,
    "voipgroup_speakingText": GOLD_TEXT,
    "voipgroup_topPanelBlue1": VELVET_L,
    "voipgroup_topPanelBlue2": VELVET_L2,
    "voipgroup_topPanelGray": ("0xFFE4D5B4", "0xFF38304E"),
    "voipgroup_topPanelGreen1": VELVET_L2,
    "voipgroup_topPanelGreen2": VELVET_L,
    "voipgroup_unmuteButton": GOLD,
    "voipgroup_unmuteButton2": GOLD_SOFT,
    "voipgroup_windowBackgroundWhiteInputFieldActivated": GOLD,
    "wallet_out_commentBorder": ("0xFFE2D5B8", "0xFF33294A"),
}

# الگوهای سه‌گانهٔ بخش مکمل (پرانتز پایانی م.put حساب می‌شود):
#  A) au ? (d ? X : Y) : (d ? Z : W));
#  B) au ? (d ? X : Y) : CONST);
#  C) au ? CONST : (d ? Z : W));
pat_A = re.compile(r'(m\.put\("([a-zA-Z_0-9]+)", )au \? \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\) : \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\)\);')
pat_B = re.compile(r'(m\.put\("([a-zA-Z_0-9]+)", )au \? \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\) : (0x[0-9A-F]+)\);')
pat_C = re.compile(r'(m\.put\("([a-zA-Z_0-9]+)", )au \? (0x[0-9A-F]+) : \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\)\);')
# خصوصی: premiumStartSmallStarsColor با آلفا 0x71 داخلی au — پایهٔ CONST
pat_D = re.compile(r'(m\.put\("premiumStartSmallStarsColor", )au \? \(d \? (0x[0-9A-F]+) : (0x[0-9A-F]+)\) : (0x[0-9A-F]+)\);')

supp_hits = set()
out_lines = []
for ln in src.split("\n"):
    s = ln
    md = pat_D.match(s.strip())
    ma = pat_A.match(s.strip())
    mb = pat_B.match(s.strip())
    mc = pat_C.match(s.strip())
    key = None
    if md:
        key = "premiumStartSmallStarsColor"
    elif ma:
        key = ma.group(2)
    elif mb:
        key = mb.group(2)
    elif mc:
        key = mc.group(2)
    if key and key in SUPPLEMENT and "pr ?" not in s:
        pd, pn = SUPPLEMENT[key]
        if md:
            s = f'{md.group(1)}au ? (d ? {md.group(2)} : {md.group(3)}) : pr ? (d ? {pd} : {pn}) : {md.group(4)});'
        elif ma:
            s = f'{ma.group(1)}au ? (d ? {ma.group(3)} : {ma.group(4)}) : pr ? (d ? {pd} : {pn}) : (d ? {ma.group(5)} : {ma.group(6)}));'
        elif mb:
            s = f'{mb.group(1)}au ? (d ? {mb.group(3)} : {mb.group(4)}) : pr ? (d ? {pd} : {pn}) : {mb.group(5)});'
        elif mc:
            s = f'{mc.group(1)}au ? {mc.group(3)} : pr ? (d ? {pd} : {pn}) : (d ? {mc.group(4)} : {mc.group(5)}));'
        supp_hits.add(key)
    out_lines.append(s)
src = "\n".join(out_lines)

missing = set(SUPPLEMENT.keys()) - supp_hits
if missing:
    sys.exit(f"FATAL: supplement keys not found/transformed: {sorted(missing)[:10]}")

# ── اجرا ────────────────────────────────────────────────────────────────────
for old, new in EXPLICIT:
    n = src.count(old)
    if n != 1:
        sys.exit(f"FATAL: expected 1 occurrence, found {n} for:\n---\n{old[:150]}\n---")
    src = src.replace(old, new)

open(PATH, "w", encoding="utf-8").write(src)
print(f"OK: mechanical wraps = {mech_count}, avatars = {avatar_hits}, supplement = {len(supp_hits)}, explicit = {len(EXPLICIT)}")

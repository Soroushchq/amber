#!/usr/bin/env python3
# مبدل یک‌بارمصرف — تزریق برند آئورورا به AmberPalette.java (v0.9.7-ui2)
# ۱) پوشش مکانیکی هر ternary هم‌پسوند: d ? AmberTokens.DAY_X : AmberTokens.NIGHT_X
#    → au ? (d ? AURORA_DAY_X : AURORA_NIGHT_X) : (d ? DAY_X : NIGHT_X)
# ۲) جدول جایگزینی صریح برای شاخه‌های اختصاصی گرم (کد/جدول/سوییچ/آواتار/شیشه/...)
# هر جایگزینی باید دقیقاً یک‌بار رخ دهد؛ وگرنه اسکریپت FATAL می‌دهد.
import re, sys

PATH = "TMessagesProj/src/main/java/org/telegram/messenger/AmberPalette.java"
src = open(PATH, encoding="utf-8").read()

# ── ۱) سرِ کلاس: کش‌ها + mode‌های آئورورا + امضای build ──────────────────────
EXPLICIT = []

EXPLICIT.append((
    """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;

    private AmberPalette() {}

    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false);
            }
            return nightCache;
        }
        if (dayCache == null) {
            dayCache = build(true);
        }
        return dayCache;
    }""",
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
    }"""
))

EXPLICIT.append((
    "    private static Map<String, Integer> build(boolean d) {",
    "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) در برابر برند کهربا */\n"
    "    private static Map<String, Integer> build(boolean d, boolean au) {"
))

# ── ۲) پوشش مکانیکی هم‌پسوند ─────────────────────────────────────────────────
def wrap(m):
    sfx = m.group(1)
    return (f"au ? (d ? AmberTokens.AURORA_DAY_{sfx} : AmberTokens.AURORA_NIGHT_{sfx})"
            f" : (d ? AmberTokens.DAY_{sfx} : AmberTokens.NIGHT_{sfx})")

mech = re.compile(r"d \? AmberTokens\.DAY_([A-Za-z_]+) : AmberTokens\.NIGHT_\1")
src, mech_count = mech.subn(wrap, src)

# ── ۳) جدول صریح ────────────────────────────────────────────────────────────
# اتم white: شب آئورورا = پس‌زمینهٔ اصلی 070A10 (نه توقف والپیپر)
EXPLICIT.append((
    "        final int white = d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP;",
    "        final int white = au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_BG)"
    " : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP);"
))

# مشتق‌های اختصاصی گرم
EXPLICIT.append((
    "final int svcBgSel = AmberTokens.alpha(d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f), d ? 0.78f : 0.72f);",
    "final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);"
))
EXPLICIT.append((
    "final int svcSel = AmberTokens.alpha(d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT, 0.14f);",
    "final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);"
))
EXPLICIT.append((
    "final int deepFile = d ? 0xFFF7E3C8 : 0xFF2E2618;",
    "final int deepFile = au ? (d ? 0xFFE9EEF6 : 0xFF1B2430) : (d ? 0xFFF7E3C8 : 0xFF2E2618);"
))
EXPLICIT.append((
    "final int outTime = d ? 0xFFA8701E : 0xFFD9BC7A;",
    "final int outTime = au ? (d ? 0xFF0E7260 : 0xFF7FE8D0) : (d ? 0xFFA8701E : 0xFFD9BC7A);"
))
EXPLICIT.append((
    "final int sentCheckRead = d ? 0xFF9C5200 : AmberTokens.NIGHT_ACCENT_BRIGHT;",
    "final int sentCheckRead = au ? (d ? 0xFF06503F : AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT) : (d ? 0xFF9C5200 : AmberTokens.NIGHT_ACCENT_BRIGHT);"
))

# سایهٔ پنجرهٔ روز
EXPLICIT.append((
    'm.put("windowBackgroundGrayShadow", d ? 0x14211A12 : 0x28000000);',
    'm.put("windowBackgroundGrayShadow", au ? (d ? 0x14171B26 : 0x28000000) : (d ? 0x14211A12 : 0x28000000));'
))

# وایپرپ گرادیانی — توقف‌های روبان آئورورا (بنفش/فیروزه عمیق روی شب یخی)
EXPLICIT.append((
    'm.put("chat_wallpaper", d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID);',
    'm.put("chat_wallpaper", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));'
))
EXPLICIT.append((
    'm.put("chat_wallpaper_gradient_to", d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP);',
    'm.put("chat_wallpaper_gradient_to", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_BOTTOM : AmberTokens.AURORA_NIGHT_WALLPAPER_TOP) : (d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP));'
))
EXPLICIT.append((
    'm.put("key_chat_wallpaper_gradient_to2", d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM);',
    'm.put("key_chat_wallpaper_gradient_to2", au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_WALLPAPER_BOTTOM) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM));'
))
EXPLICIT.append((
    'm.put("key_chat_wallpaper_gradient_to3", d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE);',
    'm.put("key_chat_wallpaper_gradient_to3", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE));'
))

# سوییچ‌ها
for key in ("switch2Track", "switchTrack", "switchTrackBlue"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE);',
        f'm.put("{key}", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));'
    ))
EXPLICIT.append((
    'm.put("switchTrackBlueThumb", d ? 0xFFFFF8F1 : AmberTokens.NIGHT_TEXT_DIM);',
    'm.put("switchTrackBlueThumb", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT_DIM) : (d ? 0xFFFFF8F1 : AmberTokens.NIGHT_TEXT_DIM));'
))

# جدول/کد/فایل داخل حباب‌ها
EXPLICIT.append((
    'm.put("chat_inTableBackground", d ? 0xFFFFFDF8 : 0xFF2E2618);',
    'm.put("chat_inTableBackground", au ? (d ? 0xFFF4F6FA : 0xFF212A38) : (d ? 0xFFFFFDF8 : 0xFF2E2618));'
))
for key in ("chat_inCodeBackground", "chat_inArticleCodeBackground"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFF7EFE4 : 0xFF211B12);',
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : 0xFF1B2430) : (d ? 0xFFF7EFE4 : 0xFF211B12));'
    ))
for key in ("chat_outFileBackground", "chat_outContactBackground"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFFBCE8F : 0xFF6E5200);',
        f'm.put("{key}", au ? (d ? 0xFFBEEBDF : 0xFF17544A) : (d ? 0xFFFBCE8F : 0xFF6E5200));'
    ))
EXPLICIT.append((
    'm.put("chat_outTableBackground", d ? 0xFFFBF1DD : 0xFF6E5200);',
    'm.put("chat_outTableBackground", au ? (d ? 0xFFC4EFE4 : 0xFF17544A) : (d ? 0xFFFBF1DD : 0xFF6E5200));'
))
for key in ("chat_outCodeBackground", "chat_outArticleCodeBackground"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFF6E3C2 : 0xFF524000);',
        f'm.put("{key}", au ? (d ? 0xFFB8E9DC : 0xFF12463E) : (d ? 0xFFF6E3C2 : 0xFF524000));'
    ))
EXPLICIT.append((
    'm.put("chat_outPollCorrectAnswer", d ? 0xFF3D7A2B : 0xFF9BC77E);',
    'm.put("chat_outPollCorrectAnswer", au ? (d ? 0xFF0E8A6E : 0xFF8AD9BC) : (d ? 0xFF3D7A2B : 0xFF9BC77E));'
))

# سرویس/دکمهٔ بات/پنل‌ها
for key in ("chat_serviceText", "chat_serviceIcon", "chat_fieldOverlayText", "chat_botButtonText"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);',
        f'm.put("{key}", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));'
    ))
EXPLICIT.append((
    'm.put("chat_serviceLink", d ? 0xFFFFEFC9 : 0xFFFFDDB8);',
    'm.put("chat_serviceLink", au ? (d ? 0xFFDCF7F0 : 0xFFDCFFF4) : (d ? 0xFFFFEFC9 : 0xFFFFDDB8));'
))
for key in ("chat_stickersHintPanel", "chat_emojiPanelBackground", "chat_emojiPanelStickerPackSelector"):
    EXPLICIT.append((
        f'm.put("{key}", d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE);',
        f'm.put("{key}", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));'
    ))

# دکمه‌های ضمیمه (صدای ارغوانی / مخاطب کهربایی — روبان‌های آئورورا)
EXPLICIT.append((
    'm.put("chat_attachAudioBackground", d ? 0xFFB4382C : 0xFFE2695B);',
    'm.put("chat_attachAudioBackground", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : (d ? 0xFFB4382C : 0xFFE2695B));'
))
EXPLICIT.append((
    'm.put("chat_attachContactBackground", d ? 0xFF8C6A1D : 0xFFC79A3E);',
    'm.put("chat_attachContactBackground", au ? (d ? 0xFFB3651F : 0xFFFFB454) : (d ? 0xFF8C6A1D : 0xFFC79A3E));'
))

# آواتارها — بازنویسی کامل بخش با هویت روبانی آئورورا
OLD_AVATAR = '''        m.put("avatar_backgroundBlue", d ? 0xFFFFB25E : 0xFFB45309);
        m.put("avatar_background2Blue", d ? 0xFFE8871E : 0xFF8A3E06);
        m.put("avatar_backgroundCyan", d ? 0xFFDD8A5B : 0xFF9E4632);
        m.put("avatar_background2Cyan", d ? 0xFFB4382C : 0xFF6E2A1E);
        m.put("avatar_backgroundGreen", d ? 0xFFC2A25E : 0xFF8C6A1D);
        m.put("avatar_background2Green", d ? 0xFF8C6A1D : 0xFF5E470F);
        m.put("avatar_backgroundOrange", d ? 0xFFF0C08A : 0xFFB06428);
        m.put("avatar_background2Orange", d ? 0xFFC25E00 : 0xFF74400E);
        m.put("avatar_backgroundPink", d ? 0xFFE8871E : 0xFF8A3E06);
        m.put("avatar_background2Pink", d ? 0xFFFFB25E : 0xFFB45309);
        m.put("avatar_backgroundRed", d ? 0xFFB4382C : 0xFF6E2A1E);
        m.put("avatar_background2Red", d ? 0xFFDD8A5B : 0xFF9E4632);
        m.put("avatar_backgroundViolet", d ? 0xFF8C6A1D : 0xFF5E470F);
        m.put("avatar_background2Violet", d ? 0xFFC2A25E : 0xFF8C6A1D);
        m.put("avatar_backgroundSaved", d ? 0xFFC25E00 : 0xFF74400E);
        m.put("avatar_background2Saved", d ? 0xFFF0C08A : 0xFFB06428);
        m.put("avatar_nameInMessageBlue", d ? 0xFFB4561A : 0xFFE8A45C);
        m.put("avatar_nameInMessageCyan", d ? 0xFF9C7A1E : 0xFFD6B25C);
        m.put("avatar_nameInMessageGreen", d ? 0xFF6E8C2A : 0xFFB6C25E);
        m.put("avatar_nameInMessageOrange", d ? 0xFFC25E00 : 0xFFF5A623);
        m.put("avatar_nameInMessagePink", d ? 0xFFB4382C : 0xFFE06A5B);
        m.put("avatar_nameInMessageRed", d ? 0xFFA03A2A : 0xFFE08573);
        m.put("avatar_nameInMessageViolet", d ? 0xFF8C5A3C : 0xFFD69A78);
        m.put("avatar_backgroundArchived", d ? 0xFFA8A094 : 0xFF6B6257);
        m.put("avatar_backgroundArchivedHidden", d ? 0xFFD8D0C4 : 0xFF3A332A);
        m.put("avatar_text", d ? 0xFFFFFFFF : 0xFFFFF1DC);
        m.put("avatar_actionBarIconBlue", text);
        m.put("avatar_actionBarSelectorBlue", AmberTokens.alpha(text, 0.10f));
        m.put("avatar_backgroundActionBarBlue", header);
        m.put("avatar_backgroundInProfileBlue", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP);
        m.put("avatar_subtitleInProfileBlue", dim);'''
NEW_AVATAR = '''        // آئورورا: جفت‌های روبانی (فیروزه/ارغوانی/کهربا/بنفش/نقره‌ای/مرجانی)؛ کهربا: جفت‌های گرم
        m.put("avatar_backgroundBlue", au ? (d ? 0xFF98F2DE : 0xFF2DE4C4) : (d ? 0xFFFFB25E : 0xFFB45309));
        m.put("avatar_background2Blue", au ? (d ? 0xFF0F9B80 : 0xFF0E8A78) : (d ? 0xFFE8871E : 0xFF8A3E06));
        m.put("avatar_backgroundCyan", au ? (d ? 0xFF0F9B80 : 0xFF0E8A78) : (d ? 0xFFDD8A5B : 0xFF9E4632));
        m.put("avatar_background2Cyan", au ? (d ? 0xFF98F2DE : 0xFF2DE4C4) : (d ? 0xFFB4382C : 0xFF6E2A1E));
        m.put("avatar_backgroundGreen", au ? (d ? 0xFFB9AFF2 : 0xFF8B7CF6) : (d ? 0xFFC2A25E : 0xFF8C6A1D));
        m.put("avatar_background2Green", au ? (d ? 0xFF6A5CC4 : 0xFF4A3E8C) : (d ? 0xFF8C6A1D : 0xFF5E470F));
        m.put("avatar_backgroundOrange", au ? (d ? 0xFFFFD08A : 0xFFFFB454) : (d ? 0xFFF0C08A : 0xFFB06428));
        m.put("avatar_background2Orange", au ? (d ? 0xFFC97A26 : 0xFFB3651F) : (d ? 0xFFC25E00 : 0xFF74400E));
        m.put("avatar_backgroundPink", au ? (d ? 0xFFF4AFE9 : 0xFFE86BD8) : (d ? 0xFFE8871E : 0xFF8A3E06));
        m.put("avatar_background2Pink", au ? (d ? 0xFFA8459B : 0xFF7A2F6E) : (d ? 0xFFFFB25E : 0xFFB45309));
        m.put("avatar_backgroundRed", au ? (d ? 0xFFFFB3A6 : 0xFFFF8A7A) : (d ? 0xFFB4382C : 0xFF6E2A1E));
        m.put("avatar_background2Red", au ? (d ? 0xFFD4574A : 0xFFC24238) : (d ? 0xFFDD8A5B : 0xFF9E4632));
        m.put("avatar_backgroundViolet", au ? (d ? 0xFF6A5CC4 : 0xFF4A3E8C) : (d ? 0xFF8C6A1D : 0xFF5E470F));
        m.put("avatar_background2Violet", au ? (d ? 0xFFB9AFF2 : 0xFF8B7CF6) : (d ? 0xFFC2A25E : 0xFF8C6A1D));
        m.put("avatar_backgroundSaved", au ? (d ? 0xFFD7E0E8 : 0xFFC9D6DF) : (d ? 0xFFC25E00 : 0xFF74400E));
        m.put("avatar_background2Saved", au ? (d ? 0xFF6E7E8A : 0xFF5A6B75) : (d ? 0xFFF0C08A : 0xFFB06428));
        m.put("avatar_nameInMessageBlue", au ? (d ? 0xFF0B8A72 : 0xFF4DE8C8) : (d ? 0xFFB4561A : 0xFFE8A45C));
        m.put("avatar_nameInMessageCyan", au ? (d ? 0xFF6A5CC4 : 0xFFB9AFF2) : (d ? 0xFF9C7A1E : 0xFFD6B25C));
        m.put("avatar_nameInMessageGreen", au ? (d ? 0xFF4E8C64 : 0xFF8AE0B0) : (d ? 0xFF6E8C2A : 0xFFB6C25E));
        m.put("avatar_nameInMessageOrange", au ? (d ? 0xFF0A8A74 : 0xFF2DE4C4) : (d ? 0xFFC25E00 : 0xFFF5A623));
        m.put("avatar_nameInMessagePink", au ? (d ? 0xFFB84A9E : 0xFFF08BD0) : (d ? 0xFFB4382C : 0xFFE06A5B));
        m.put("avatar_nameInMessageRed", au ? (d ? 0xFFA8433C : 0xFFFFA08F) : (d ? 0xFFA03A2A : 0xFFE08573));
        m.put("avatar_nameInMessageViolet", au ? (d ? 0xFF7A6ED0 : 0xFFC9B8F5) : (d ? 0xFF8C5A3C : 0xFFD69A78));
        m.put("avatar_backgroundArchived", au ? (d ? 0xFF9AA2B2 : 0xFF5E6675) : (d ? 0xFFA8A094 : 0xFF6B6257));
        m.put("avatar_backgroundArchivedHidden", au ? (d ? 0xFFC9CFDA : 0xFF333A46) : (d ? 0xFFD8D0C4 : 0xFF3A332A));
        m.put("avatar_text", au ? 0xFFFFFFFF : (d ? 0xFFFFFFFF : 0xFFFFF1DC));
        m.put("avatar_actionBarIconBlue", text);
        m.put("avatar_actionBarSelectorBlue", AmberTokens.alpha(text, 0.10f));
        m.put("avatar_backgroundActionBarBlue", header);
        m.put("avatar_backgroundInProfileBlue", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));
        m.put("avatar_subtitleInProfileBlue", dim);'''
EXPLICIT.append((OLD_AVATAR, NEW_AVATAR))

# شیشهٔ ناوبری اصلی
EXPLICIT.append((
    'm.put("glass_targetMainTabs", d ? 0xE6FFF6EA : 0xE6241D14);',
    'm.put("glass_targetMainTabs", au ? (d ? 0xE6F5F5FA : 0xE60B0F16) : (d ? 0xE6FFF6EA : 0xE6241D14));'
))
EXPLICIT.append((
    'm.put("glass_targetMainTopPanel", d ? 0xE6FFE9CF : 0xE61F1912);',
    'm.put("glass_targetMainTopPanel", au ? (d ? 0xE6FFFFFF : 0xE612151B) : (d ? 0xE6FFE9CF : 0xE61F1912));'
))

# ── اجرا ────────────────────────────────────────────────────────────────────
for old, new in EXPLICIT:
    n = src.count(old)
    if n != 1:
        sys.exit(f"FATAL: expected 1 occurrence, found {n} for:\n---\n{old[:120]}\n---")
    src = src.replace(old, new)

open(PATH, "w", encoding="utf-8").write(src)
print(f"OK: mechanical wraps = {mech_count}, explicit replacements = {len(EXPLICIT)}")

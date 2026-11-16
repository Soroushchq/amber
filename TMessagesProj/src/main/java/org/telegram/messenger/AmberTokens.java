package org.telegram.messenger;

/**
 * AmberGram UI 2.0 — مرکز توکن‌های طراحی (تک منبع حقیقت مقادیر).
 *
 * کانسپت C — Expressive Material:
 *  روز: کاغذ گرم (#FFF8F1 / #FFE9CF / پرایمری #C25E00)
 *  شب: تونال گرم M3 بدون مشکی خالص (#17130E..#241D14، اکسنت #F5A623)
 *
 * قاعده مصرف: هیچ رنگ آمبر جدیدی نباید مستقیم در UI نوشته شود؛ همه از این کلاس.
 * مشتق‌ها (انتخاب/پرس/دیوایدر/سرویس) در AmberPalette با alpha/over ساخته می‌شوند.
 * لایه رنگ فقط مصرف می‌کند — منطق شبکه/صف/پروکسی/شبح/Morphe دست‌نخورده.
 */
public final class AmberTokens {

    private AmberTokens() {}

    /** نسخه سند توکن — با هر تغییر ناپایه‌ای bump می‌شود */
    public static final String DESIGN_VERSION = "2.0-c-step1";

    /** رژیم تم — قدم ۴ روز/شب را در ThemeInfo جدا می‌کند */
    public static final int MODE_DAY = 0;
    public static final int MODE_NIGHT = 1;

    // ─────────────────────────────────────────────────────────────────────────
    // روز — Expressive Material (کانسپت C تأییدشده)
    // ─────────────────────────────────────────────────────────────────────────

    /** پس‌زمینه اصلی لیست/تنظیمات (کاغذ گرم) */
    public static final int DAY_BG = 0xFFFFF8F1;
    /** وایپرپ چت — توقف‌های گرادیان ۱۶۰ درجه */
    public static final int DAY_WALLPAPER_TOP = 0xFFFFF6EA;
    public static final int DAY_WALLPAPER_BOTTOM = 0xFFFBEEDC;
    /** کانتینر هدر/اکشن‌بار */
    public static final int DAY_HEADER = 0xFFFFE9CF;
    public static final int DAY_HEADER_BORDER = 0xFFF3DDBC;
    /** سطح کارت‌ها، دیالوگ‌ها، شیت‌ها */
    public static final int DAY_SURFACE = 0xFFF3ECE2;
    /** اوت‌لاین مرئی — مرزهای نامشخص ریشه‌کن می‌شود */
    public static final int DAY_OUTLINE = 0xFFE9DFD0;
    public static final int DAY_TEXT = 0xFF211A12;
    public static final int DAY_TEXT_DIM = 0xFF7A6C5B;
    public static final int DAY_TIME = 0xFF9A8B78;
    /** پرایمری M3 — اکسنت اصلی روز (قهوه‌ای-نارنجی اشباع) */
    public static final int DAY_ACCENT = 0xFFC25E00;
    /** سر گرادیان اکسنت (روشن‌تر) */
    public static final int DAY_ACCENT_BRIGHT = 0xFFE8871E;
    public static final int DAY_ON_ACCENT = 0xFFFFFFFF;
    /** حباب ورودی */
    public static final int DAY_IN_BUBBLE = 0xFFF1EBE1;
    public static final int DAY_IN_TEXT = 0xFF211A12;
    /** حباب خروجی = primary-container */
    public static final int DAY_OUT_BUBBLE = 0xFFFFDDB8;
    public static final int DAY_OUT_TEXT = 0xFF331E00;
    public static final int DAY_BADGE_BG = 0xFFC25E00;
    public static final int DAY_BADGE_TEXT = 0xFFFFFFFF;
    /** فیلد پیام/جستجو */
    public static final int DAY_FIELD_BG = 0xFFFFFFFF;
    public static final int DAY_FIELD_BORDER = 0xFFE9DFD0;
    /** پیل فعال ناوبری شناور */
    public static final int DAY_NAV_PILL = 0xFFFFDDB8;
    /** رنگ سایه FAB/ناوبری + آلفا */
    public static final int DAY_SHADOW_TINT = 0xFFC25E00;
    public static final float DAY_SHADOW_ALPHA = 0.30f;

    // ─────────────────────────────────────────────────────────────────────────
    // شب — تونال گرم M3؛ بدون مشکی خالص، سطوح پله‌ای
    // ─────────────────────────────────────────────────────────────────────────

    public static final int NIGHT_BG = 0xFF17130E;
    public static final int NIGHT_WALLPAPER_TOP = 0xFF1C1710;
    public static final int NIGHT_WALLPAPER_MID = 0xFF17130E;
    public static final int NIGHT_WALLPAPER_BOTTOM = 0xFF12100B;
    public static final int NIGHT_HEADER = 0xFF1F1912;
    public static final int NIGHT_HEADER_BORDER = 0xFF332818;
    public static final int NIGHT_SURFACE = 0xFF241D14;
    public static final int NIGHT_OUTLINE = 0xFF382C1C;
    public static final int NIGHT_TEXT = 0xFFF5EFE4;
    public static final int NIGHT_TEXT_DIM = 0xFFA99C8B;
    public static final int NIGHT_TIME = 0xFF8B7F6F;
    public static final int NIGHT_ACCENT = 0xFFF5A623;
    public static final int NIGHT_ACCENT_BRIGHT = 0xFFFFB84D;
    public static final int NIGHT_ON_ACCENT = 0xFF3A2400;
    public static final int NIGHT_IN_BUBBLE = 0xFF262017;
    public static final int NIGHT_IN_TEXT = 0xFFF5EFE4;
    public static final int NIGHT_OUT_BUBBLE = 0xFF5C4000;
    public static final int NIGHT_OUT_TEXT = 0xFFFFDDB8;
    public static final int NIGHT_BADGE_BG = 0xFFF5A623;
    public static final int NIGHT_BADGE_TEXT = 0xFF3A2400;
    public static final int NIGHT_FIELD_BG = 0xFF241D14;
    public static final int NIGHT_FIELD_BORDER = 0xFF382C1C;
    /** پیل فعال ناوبری شناور شب = primary-container تیره */
    public static final int NIGHT_NAV_PILL = 0xFF5C4000;
    public static final int NIGHT_SHADOW_TINT = 0xFF000000;
    public static final float NIGHT_SHADOW_ALPHA = 0.45f;

    // ─────────────────────────────────────────────────────────────────────────
    // بذرهای اکسنت — قدم ۶ (سیستم اکسنت) از این‌ها تغذیه می‌شود
    // ─────────────────────────────────────────────────────────────────────────

    /** ۳ اکسنت روز: پرایمری، زنگاری، زیتونی */
    public static final int[] ACCENT_DAY = { 0xFFC25E00, 0xFFB4382C, 0xFF8C6A1D };
    /** ۳ اکسنت شب: کهربا، کهربای روشن، نارنجی سوخته */
    public static final int[] ACCENT_NIGHT = { 0xFFF5A623, 0xFFFFB84D, 0xFFEA580C };

    // ─────────────────────────────────────────────────────────────────────────
    // گرادیان آواتار — ۴ گرادیان × ۲ رژیم؛ ایندکس پایدار از dialogId
    // ─────────────────────────────────────────────────────────────────────────

    public static final int[][] AVATAR_GRADS_DAY = {
            { 0xFFFFB25E, 0xFFE8871E },   // کهربایی
            { 0xFFDD8A5B, 0xFFB4382C },   // زنگاری
            { 0xFFC2A25E, 0xFF8C6A1D },   // زیتونی
            { 0xFFF0C08A, 0xFFC25E00 },   // شنی
    };
    public static final int[][] AVATAR_GRADS_NIGHT = {
            { 0xFFB45309, 0xFF8A3E06 },   // کهربای عمیق
            { 0xFF9E4632, 0xFF6E2A1E },   // زنگاری شب
            { 0xFF8C6A1D, 0xFF5E470F },   // زیتونی شب
            { 0xFFB06428, 0xFF74400E },   // شنی شب
    };

    public static int[][] avatarGradients(int mode) {
        return mode == MODE_NIGHT ? AVATAR_GRADS_NIGHT : AVATAR_GRADS_DAY;
    }

    /** ایندکس گرادیان پایدار برای هر گفت‌وگو (بدون ناهنجاری دیالوگ‌های منفی/گروهی) */
    public static int avatarGradientIndex(long dialogId, int count) {
        int n = count <= 0 ? 1 : Math.min(count, AVATAR_GRADS_DAY.length);
        long v = dialogId % n;
        if (v < 0) v += n;
        return (int) v;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Shape — Expressive Material (حباب ۲۶، کارت ۲۰، پیل ۳۲، دیالوگ ۲۸، فیلد ۱۶)
    // ─────────────────────────────────────────────────────────────────────────

    public static final float SHAPE_BUBBLE = 26f;
    public static final float SHAPE_CARD = 20f;
    public static final float SHAPE_NAV_PILL = 32f;
    public static final float SHAPE_DIALOG = 28f;
    public static final float SHAPE_FIELD = 16f;

    // ─────────────────────────────────────────────────────────────────────────
    // Motion — 150/250/400ms + فنر (stiffness 380 / damping 0.78)
    // ─────────────────────────────────────────────────────────────────────────

    public static final int MOTION_FAST = 150;
    public static final int MOTION_BASE = 250;
    public static final int MOTION_SLOW = 400;
    public static final float SPRING_STIFFNESS = 380f;
    public static final float SPRING_DAMPING = 0.78f;

    // ─────────────────────────────────────────────────────────────────────────
    // Elevation — پله‌های سایه (dp)
    // ─────────────────────────────────────────────────────────────────────────

    public static final float ELEV_CARD = 2f;
    public static final float ELEV_FAB = 6f;
    public static final float ELEV_NAV = 8f;
    public static final float ELEV_SHEET = 16f;

    // ─────────────────────────────────────────────────────────────────────────
    // هلپرها — مشتق‌گیری پالت و ممیزی WCAG (قدم ۴۵)
    // ─────────────────────────────────────────────────────────────────────────

    /** رنگ با آلفای جدید (هسته رنگ دست‌نخورده) */
    public static int alpha(int color, float alphaFraction) {
        int a8 = Math.round(alphaFraction * 255.0f) & 0xFF;
        return (a8 << 24) | (color & 0x00FFFFFF);
    }

    /** رویی روی پس‌زمینه با آلفا — خروجی همیشه مات (مثل پیش‌رندر) */
    public static int over(int foreground, int background, float alphaFraction) {
        float fa = alphaFraction;
        int fr = (foreground >> 16) & 0xFF, fg = (foreground >> 8) & 0xFF, fb = foreground & 0xFF;
        int br = (background >> 16) & 0xFF, bgc = (background >> 8) & 0xFF, bb = background & 0xFF;
        int r = Math.round(fr * fa + br * (1f - fa));
        int g = Math.round(fg * fa + bgc * (1f - fa));
        int b = Math.round(fb * fa + bb * (1f - fa));
        return 0xFF000000 | (r << 16) | (g << 8) | b;
    }

    /** luminance نسبی sRGB (WCAG 2.x) */
    public static float luminance(int rgb) {
        float r = ((rgb >> 16) & 0xFF) / 255f;
        float g = ((rgb >> 8) & 0xFF) / 255f;
        float b = (rgb & 0xFF) / 255f;
        r = r <= 0.03928f ? r / 12.92f : (float) Math.pow((r + 0.055f) / 1.055f, 2.4);
        g = g <= 0.03928f ? g / 12.92f : (float) Math.pow((g + 0.055f) / 1.055f, 2.4);
        b = b <= 0.03928f ? b / 12.92f : (float) Math.pow((b + 0.055f) / 1.055f, 2.4);
        return 0.2126f * r + 0.7152f * g + 0.0722f * b;
    }

    /** نسبت کنتراست WCAG — برای ممیزی AA در قدم ۴۵ */
    public static float contrastRatio(int colorA, int colorB) {
        float la = luminance(colorA);
        float lb = luminance(colorB);
        float lighter = Math.max(la, lb);
        float darker = Math.min(la, lb);
        return (lighter + 0.05f) / (darker + 0.05f);
    }
}

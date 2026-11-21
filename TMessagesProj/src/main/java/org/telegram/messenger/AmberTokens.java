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
    public static final String DESIGN_VERSION = "2.0-c-mario";

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
    // آئورورا — تم «شیشه و نور» (v0.9.7-ui2) — دومین هویت بصری AmberGram
    //
    // کانسپت: شبِ عمیق یخی (#070A10) با سه روبان نور — فیروزه (#2DE4C4)،
    // ارغوانی (#E86BD8) و کهربایی (#FFB454) — حباب‌های بلوری، وایپرپِ گرادیانی
    // زنده و فونت استعداد (Estedad) که با سوییچ تم عوض می‌شود.
    // نام‌گذاری دقیقاً هم‌پسوند با اتم‌های Amber (DAY_*/NIGHT_*) تا مبدل
    // generate_amber_theme2.py بتواند شاخه au را مکانیکی بپیچد.
    // روز = «آئورورای روشن»: سپیدار (#F5F5FA) با روبان‌های پاستلی.
    // ─────────────────────────────────────────────────────────────────────────

    public static final int MODE_AURORA_DAY = 2;
    public static final int MODE_AURORA_NIGHT = 3;

    /** آیا نام تم به خانواده آئورورا تعلق دارد (فونت/لوگوی آئورورا) */
    public static boolean isAuroraName(String name) {
        return "Aurora".equals(name) || "Aurora Day".equals(name);
    }

    // شب
    public static final int AURORA_NIGHT_BG = 0xFF070A10;
    public static final int AURORA_NIGHT_WALLPAPER_TOP = 0xFF1B1E3E;
    public static final int AURORA_NIGHT_WALLPAPER_MID = 0xFF070A10;
    public static final int AURORA_NIGHT_WALLPAPER_BOTTOM = 0xFF0C3230;
    public static final int AURORA_NIGHT_HEADER = 0xFF12151B;
    public static final int AURORA_NIGHT_HEADER_BORDER = 0xFF1E2530;
    public static final int AURORA_NIGHT_SURFACE = 0xFF0B0F16;
    public static final int AURORA_NIGHT_OUTLINE = 0xFF232B36;
    public static final int AURORA_NIGHT_TEXT = 0xFFF2F1F7;
    public static final int AURORA_NIGHT_TEXT_DIM = 0xFF9BA3B7;
    public static final int AURORA_NIGHT_TIME = 0xFF767E92;
    public static final int AURORA_NIGHT_ACCENT = 0xFF2DE4C4;
    public static final int AURORA_NIGHT_ACCENT_BRIGHT = 0xFF54F1D6;
    public static final int AURORA_NIGHT_ON_ACCENT = 0xFF04211B;
    /** حباب ورودی = معادل ماتِ شیشه سفید ۸٫۵٪ روی پس‌زمینه شب */
    public static final int AURORA_NIGHT_IN_BUBBLE = 0xFF1D232B;
    public static final int AURORA_NIGHT_IN_TEXT = 0xFFF2F1F7;
    /** حباب خروجی = معادل ماتِ شیشه فیروزه ۱۵٪ (روبان آئورورا) */
    public static final int AURORA_NIGHT_OUT_BUBBLE = 0xFF0E2E2C;
    public static final int AURORA_NIGHT_OUT_TEXT = 0xFFDCFFF4;
    public static final int AURORA_NIGHT_BADGE_BG = 0xFF2DE4C4;
    public static final int AURORA_NIGHT_BADGE_TEXT = 0xFF04211B;
    public static final int AURORA_NIGHT_FIELD_BG = 0xFF10151E;
    public static final int AURORA_NIGHT_FIELD_BORDER = 0xFF232B36;
    public static final int AURORA_NIGHT_NAV_PILL = 0xFF0E2E2C;
    public static final int AURORA_NIGHT_SHADOW_TINT = 0xFF000000;
    public static final float AURORA_NIGHT_SHADOW_ALPHA = 0.45f;

    // روز — «آئورورای روشن»
    public static final int AURORA_DAY_BG = 0xFFF5F5FA;
    public static final int AURORA_DAY_WALLPAPER_TOP = 0xFFF7F8FD;
    public static final int AURORA_DAY_WALLPAPER_MID = 0xFFF5F5FA;
    public static final int AURORA_DAY_WALLPAPER_BOTTOM = 0xFFE9F6F1;
    public static final int AURORA_DAY_HEADER = 0xFFFFFFFF;
    public static final int AURORA_DAY_HEADER_BORDER = 0xFFE3E6EF;
    public static final int AURORA_DAY_SURFACE = 0xFFFFFFFF;
    public static final int AURORA_DAY_OUTLINE = 0xFFD9DDE7;
    public static final int AURORA_DAY_TEXT = 0xFF171B26;
    public static final int AURORA_DAY_TEXT_DIM = 0xFF5E6675;
    public static final int AURORA_DAY_TIME = 0xFF8A92A2;
    /** اکسنت روز عمیق‌تر از پیش‌نمایش (#0FB89A) تا کنتراست AA روی سپیدار حفظ شود (۴٫۳:۱ مثل کهربای روز) */
    public static final int AURORA_DAY_ACCENT = 0xFF08806B;
    public static final int AURORA_DAY_ACCENT_BRIGHT = 0xFF12C9A8;
    public static final int AURORA_DAY_ON_ACCENT = 0xFFFFFFFF;
    public static final int AURORA_DAY_IN_BUBBLE = 0xFFFFFFFF;
    public static final int AURORA_DAY_IN_TEXT = 0xFF171B26;
    public static final int AURORA_DAY_OUT_BUBBLE = 0xFFDCF7F0;
    public static final int AURORA_DAY_OUT_TEXT = 0xFF0B3B33;
    public static final int AURORA_DAY_BADGE_BG = 0xFF08806B;
    public static final int AURORA_DAY_BADGE_TEXT = 0xFFFFFFFF;
    public static final int AURORA_DAY_FIELD_BG = 0xFFFFFFFF;
    public static final int AURORA_DAY_FIELD_BORDER = 0xFFD9DDE7;
    public static final int AURORA_DAY_NAV_PILL = 0xFFDCF7F0;
    public static final int AURORA_DAY_SHADOW_TINT = 0xFF08806B;
    public static final float AURORA_DAY_SHADOW_ALPHA = 0.25f;

    /** روبان‌های آئورورا — هویت رنگی تم (اکسنت‌ها، لوگو و آیکون از این‌ها تغذیه می‌شوند) */
    public static final int AURORA_RIBBON_TEAL = 0xFF2DE4C4;
    public static final int AURORA_RIBBON_VIOLET = 0xFF8B7CF6;
    public static final int AURORA_RIBBON_PINK = 0xFFE86BD8;
    public static final int AURORA_RIBBON_AMBER = 0xFFFFB454;

    /** ۳ اکسنت شب آئورورا: فیروزه (نوشتار اصلی)، ارغوانی، کهربایی */
    public static final int[] ACCENT_AURORA_NIGHT = { 0xFF2DE4C4, 0xFFE86BD8, 0xFFFFB454 };
    /** ۳ اکسنت روز آئورورا: فیروزه عمیق، ارغوانی عمیق، کهربایی عمیق */
    public static final int[] ACCENT_AURORA_DAY = { 0xFF08806B, 0xFFB84A9E, 0xFFB3651F };

    // ─────────────────────────────────────────────────────────────────────────
    // شب اکران — تم «شب اکران» (v0.9.9-ui2) — سومین هویت بصری AmberGram
    //
    // کانسپت: تالارِ سینما در شبِ اکران — عصر طلایی هالیوود و انیمیشن کلاسیک.
    // تاریکی تالار (#0C0A12) با مخمل بنفش‌فام (#1F1930)، حباب خروجی طلای اکران
    // (#E9A93A با گرادیان تندیس)، فرش قرمز ولت کریمسون (#D63852) برای بج‌ها و
    // طلای مارکی (#F0B449) به‌عنوان اکسنت — کاغذدیوار «پرتوهای افکتور» با
    // گرادیان چهاررنگ رسمی و نقش ستاره‌های چشمک‌زن.
    // نام‌گذاری دقیقاً هم‌پسوند با اتم‌های Amber (DAY_*/NIGHT_*) و آئورورا تا
    // مبدل generate_amber_theme2.py شاخه pr را مکانیکی بپیچد.
    // روز = «ماتینه»: نمایش بعدازظهر — کاغذ پوستر کرم (#F8F1E3)، طلای عمیق
    // (#A76F0F) و کریمسون چاپی (#C42B4B)؛ همان تئاتر در نور روز.
    // ─────────────────────────────────────────────────────────────────────────

    public static final int MODE_PREMIERE_DAY = 4;
    public static final int MODE_PREMIERE_NIGHT = 5;

    /** آیا نام تم به خانواده شب اکران تعلق دارد (فونت استعداد/لوگوی ستاره) */
    public static boolean isPremiereName(String name) {
        return "Premiere".equals(name) || "Premiere Day".equals(name);
    }

    // شب — «شب اکران»
    public static final int PREMIERE_NIGHT_BG = 0xFF0C0A12;
    /** پرتو بنفش مخمل — توقف بالای وایپرپ (پرتو افکتور چپ) */
    public static final int PREMIERE_NIGHT_WALLPAPER_TOP = 0xFF2A1230;
    public static final int PREMIERE_NIGHT_WALLPAPER_MID = 0xFF0C0A12;
    /** پرتو کریمسون گرم — توقف پایین وایپرپ (پرتو افکتور راست) */
    public static final int PREMIERE_NIGHT_WALLPAPER_BOTTOM = 0xFF471B2C;
    /** مخمل شب — هدر/اکشن‌بار */
    public static final int PREMIERE_NIGHT_HEADER = 0xFF120F1B;
    public static final int PREMIERE_NIGHT_HEADER_BORDER = 0xFF2E2440;
    /** مخمل پنلی — سطح کارت‌ها */
    public static final int PREMIERE_NIGHT_SURFACE = 0xFF181326;
    /** بنفش خفته — خطوط مرئی */
    public static final int PREMIERE_NIGHT_OUTLINE = 0xFF38304E;
    /** عاج تیتراژ — متن اصلی */
    public static final int PREMIERE_NIGHT_TEXT = 0xFFF7F0E1;
    public static final int PREMIERE_NIGHT_TEXT_DIM = 0xFF9C92AF;
    public static final int PREMIERE_NIGHT_TIME = 0xFF8B80A0;
    /** طلای مارکی — اکسنت اصلی */
    public static final int PREMIERE_NIGHT_ACCENT = 0xFFF0B449;
    /** شمع مارکی — اکسنت روشن */
    public static final int PREMIERE_NIGHT_ACCENT_BRIGHT = 0xFFF7C96B;
    public static final int PREMIERE_NIGHT_ON_ACCENT = 0xFF241303;
    /** مخمل بنفش‌فام — حباب ورودی */
    public static final int PREMIERE_NIGHT_IN_BUBBLE = 0xFF1F1930;
    public static final int PREMIERE_NIGHT_IN_TEXT = 0xFFF7F0E1;
    /** طلای اکران — حباب خروجی (پایهٔ گرادیان تندیس) */
    public static final int PREMIERE_NIGHT_OUT_BUBBLE = 0xFFE9A93A;
    public static final int PREMIERE_NIGHT_OUT_TEXT = 0xFF2A1704;
    /** ولت کریمسون — بج/فرش قرمز */
    public static final int PREMIERE_NIGHT_BADGE_BG = 0xFFD63852;
    public static final int PREMIERE_NIGHT_BADGE_TEXT = 0xFFFFFFFF;  // سفید خالص — کنتراست ۵٫۹۷ روی ولت کریمسون
    public static final int PREMIERE_NIGHT_FIELD_BG = 0xFF120F1B;
    public static final int PREMIERE_NIGHT_FIELD_BORDER = 0xFF33294A;
    /** طلای عمیق — پیل فعال ناوبری */
    public static final int PREMIERE_NIGHT_NAV_PILL = 0xFF6B4A08;
    public static final int PREMIERE_NIGHT_SHADOW_TINT = 0xFF000000;
    public static final float PREMIERE_NIGHT_SHADOW_ALPHA = 0.45f;

    // روز — «ماتینه»
    /** سپیده‌ی پوستر */
    public static final int PREMIERE_DAY_BG = 0xFFF8F1E3;
    public static final int PREMIERE_DAY_WALLPAPER_TOP = 0xFFFBEFD6;
    public static final int PREMIERE_DAY_WALLPAPER_MID = 0xFFF8F1E3;
    public static final int PREMIERE_DAY_WALLPAPER_BOTTOM = 0xFFF7E3C2;
    /** کاغذ روشن */
    public static final int PREMIERE_DAY_HEADER = 0xFFFFFBEF;
    public static final int PREMIERE_DAY_HEADER_BORDER = 0xFFEBDCC0;
    public static final int PREMIERE_DAY_SURFACE = 0xFFFFFBEF;
    public static final int PREMIERE_DAY_OUTLINE = 0xFFE2D5B8;
    /** جوهری پوستر */
    public static final int PREMIERE_DAY_TEXT = 0xFF2E2513;
    public static final int PREMIERE_DAY_TEXT_DIM = 0xFF8A7B5C;
    public static final int PREMIERE_DAY_TIME = 0xFF94855E;  // ≥۳٫۰ روی کاغذ روشن
    /** طلای عمیق — اکسنت روز (AA روی کرم) */
    public static final int PREMIERE_DAY_ACCENT = 0xFFA76F0F;
    public static final int PREMIERE_DAY_ACCENT_BRIGHT = 0xFFC88A1E;
    public static final int PREMIERE_DAY_ON_ACCENT = 0xFFFFFFFF;
    public static final int PREMIERE_DAY_IN_BUBBLE = 0xFFFFF3D9;
    public static final int PREMIERE_DAY_IN_TEXT = 0xFF2E2513;
    /** طلایی ملایم — حباب خروجی روز */
    public static final int PREMIERE_DAY_OUT_BUBBLE = 0xFFF2CE7F;
    public static final int PREMIERE_DAY_OUT_TEXT = 0xFF3A2A08;
    /** کریمسون پوستر — بج روز */
    public static final int PREMIERE_DAY_BADGE_BG = 0xFFC42B4B;
    public static final int PREMIERE_DAY_BADGE_TEXT = 0xFFFFFFFF;
    public static final int PREMIERE_DAY_FIELD_BG = 0xFFFFFBEF;
    public static final int PREMIERE_DAY_FIELD_BORDER = 0xFFE2D5B8;
    public static final int PREMIERE_DAY_NAV_PILL = 0xFFF2CE7F;
    public static final int PREMIERE_DAY_SHADOW_TINT = 0xFFA76F0F;
    public static final float PREMIERE_DAY_SHADOW_ALPHA = 0.25f;

    /** روبان‌های سینمایی — هویت رنگی تم (اکسنت‌ها، لوگو و آیکون از این‌ها تغذیه می‌شوند) */
    public static final int PREMIERE_GOLD_MARQUEE = 0xFFF0B449;
    public static final int PREMIERE_GOLD_TROPHY = 0xFFE9A93A;
    public static final int PREMIERE_CARPET_CRIMSON = 0xFFD63852;
    public static final int PREMIERE_CRIMSON_HOT = 0xFFE8445E;
    public static final int PREMIERE_MARQUEE_TEAL = 0xFF3FD2C7;
    public static final int PREMIERE_ROYAL_PURPLE = 0xFF8C5ADC;
    public static final int PREMIERE_BULB_WARM = 0xFFF7D488;
    public static final int PREMIERE_TROPHY_BRONZE = 0xFFC77E14;

    /** ۳ اکسنت شب شب اکران: طلای مارکی (نوشتار اصلی)، کریمسون، فیروزه مارکی */
    public static final int[] ACCENT_PREMIERE_NIGHT = { 0xFFF0B449, 0xFFE8445E, 0xFF3FD2C7 };
    /** ۳ اکسنت روز ماتینه: طلای عمیق، کریمسون پوستر، فیروزه چاپی */
    public static final int[] ACCENT_PREMIERE_DAY = { 0xFFA76F0F, 0xFFC42B4B, 0xFF0FA397 };

    // ─────────────────────────────────────────────────────────────────────────
    // دنیای ماریو — تم «دنیای ماریو» (v0.9.10-ui2) — چهارمین هویت بصری AmberGram
    //
    // کانسپت: سرزمین شاد پلتفرمر کلاسیک — بانمک، پرانرژی و پُر سکه.
    // شب = «دنیای زیرزمینی» (مرحلهٔ ۱-۲): آبی‌نفتیِ غار (#0B0F1E) با گنبد آبی
    // بریکی (#18265C) در بالا و تابش گدازهٔ قهوه‌ای‌سوخته (#3A1B0A) در پایین،
    // حباب خروجی سبزِ لولهٔ پُرشتاب (#43B047 با متن سایهٔ لوله)، بج قرمزِ قارچ
    // (#DC2418) و اکسنت طلای سکه (#FBD000) — کاغذدیوار «زیرزمین سکه‌ها» با
    // گرادیان غار و گدازه.
    // نام‌گذاری دقیقاً هم‌پسوند با اتم‌های Amber (DAY_*/NIGHT_*)، آئورورا و
    // شب اکران تا مبدل generate_amber_theme2.py شاخه ma را مکانیکی بپیچد.
    // روز = «سرزمین ماریو» (مرحلهٔ ۱-۱): کاغذ آسمان (#F2F7FF) با وایپرپِ
    // آسمان-تپه (آبی آسمان روشن → سبز پاستلی لوله)، اکسنت قرمز عمیق ماریو
    // (#C6281C، AA روی کاغذ آسمان) و حباب خروجی طلای سکهٔ ملایم (#FFE382).
    // ─────────────────────────────────────────────────────────────────────────

    public static final int MODE_MARIO_DAY = 6;
    public static final int MODE_MARIO_NIGHT = 7;

    /** آیا نام تم به خانواده دنیای ماریو تعلق دارد (لوگوی قارچ/انیمیشن پرش) */
    public static boolean isMarioName(String name) {
        return "Mario".equals(name) || "Mario Day".equals(name);
    }

    // شب — «دنیای زیرزمینی»
    public static final int MARIO_NIGHT_BG = 0xFF0B0F1E;
    /** گنبد آبی بریکی غار — توقف بالای وایپرپ */
    public static final int MARIO_NIGHT_WALLPAPER_TOP = 0xFF18265C;
    public static final int MARIO_NIGHT_WALLPAPER_MID = 0xFF0B0F1E;
    /** تابش گدازه — توقف پایین وایپرپ */
    public static final int MARIO_NIGHT_WALLPAPER_BOTTOM = 0xFF3A1B0A;
    /** آجر آبی تیره — هدر/اکشن‌بار */
    public static final int MARIO_NIGHT_HEADER = 0xFF0D1226;
    public static final int MARIO_NIGHT_HEADER_BORDER = 0xFF20305C;
    /** بلوک بریکی پنلی — سطح کارت‌ها */
    public static final int MARIO_NIGHT_SURFACE = 0xFF111731;
    /** آبی خفته — خطوط مرئی */
    public static final int MARIO_NIGHT_OUTLINE = 0xFF253260;
    /** عاج سکه — متن اصلی */
    public static final int MARIO_NIGHT_TEXT = 0xFFF6F2E6;
    public static final int MARIO_NIGHT_TEXT_DIM = 0xFF9BA7C8;
    public static final int MARIO_NIGHT_TIME = 0xFF7C88A8;
    /** طلای سکه — اکسنت اصلی */
    public static final int MARIO_NIGHT_ACCENT = 0xFFFBD000;
    /** سکهٔ براق — اکسنت روشن */
    public static final int MARIO_NIGHT_ACCENT_BRIGHT = 0xFFFFDF60;
    public static final int MARIO_NIGHT_ON_ACCENT = 0xFF332200;
    /** بلوک آبی بریکی — حباب ورودی */
    public static final int MARIO_NIGHT_IN_BUBBLE = 0xFF141B3C;
    public static final int MARIO_NIGHT_IN_TEXT = 0xFFF6F2E6;
    /** سبز لوله — حباب خروجی (متن = سایهٔ لوله) */
    public static final int MARIO_NIGHT_OUT_BUBBLE = 0xFF43B047;
    public static final int MARIO_NIGHT_OUT_TEXT = 0xFF0C2A12;
    /** قرمز قارچ — بج/شمارنده */
    public static final int MARIO_NIGHT_BADGE_BG = 0xFFDC2418;
    public static final int MARIO_NIGHT_BADGE_TEXT = 0xFFFFFFFF;  // سفید خالص — کنتراست ۴٫۸۶ روی قرمز قارچ
    public static final int MARIO_NIGHT_FIELD_BG = 0xFF111731;
    public static final int MARIO_NIGHT_FIELD_BORDER = 0xFF253260;
    /** طلای عمیق — پیل فعال ناوبری */
    public static final int MARIO_NIGHT_NAV_PILL = 0xFF5E4A04;
    public static final int MARIO_NIGHT_SHADOW_TINT = 0xFF000000;
    public static final float MARIO_NIGHT_SHADOW_ALPHA = 0.45f;

    // روز — «سرزمین ماریو»
    /** کاغذ آسمان */
    public static final int MARIO_DAY_BG = 0xFFF2F7FF;
    public static final int MARIO_DAY_WALLPAPER_TOP = 0xFFB9D6FF;
    public static final int MARIO_DAY_WALLPAPER_MID = 0xFFF2F7FF;
    /** تپهٔ پاستلی لوله — توقف پایین وایپرپ */
    public static final int MARIO_DAY_WALLPAPER_BOTTOM = 0xFFD3EFC9;
    /** آسمان روشن */
    public static final int MARIO_DAY_HEADER = 0xFFE7F0FF;
    public static final int MARIO_DAY_HEADER_BORDER = 0xFFCBDCF5;
    public static final int MARIO_DAY_SURFACE = 0xFFF5F8FF;
    public static final int MARIO_DAY_OUTLINE = 0xFFD5E1F4;
    /** جوهر اورال — متن اصلی */
    public static final int MARIO_DAY_TEXT = 0xFF16243E;
    public static final int MARIO_DAY_TEXT_DIM = 0xFF5C6E90;
    public static final int MARIO_DAY_TIME = 0xFF70819E;  // ≥۳٫۰ روی کاغذ آسمان
    /** قرمز عمیق ماریو — اکسنت روز (AA روی کاغذ آسمان: ۵٫۸۷) */
    public static final int MARIO_DAY_ACCENT = 0xFFC6281C;
    public static final int MARIO_DAY_ACCENT_BRIGHT = 0xFFE52521;
    public static final int MARIO_DAY_ON_ACCENT = 0xFFFFFFFF;
    public static final int MARIO_DAY_IN_BUBBLE = 0xFFFFFFFF;
    public static final int MARIO_DAY_IN_TEXT = 0xFF16243E;
    /** طلای سکهٔ ملایم — حباب خروجی روز */
    public static final int MARIO_DAY_OUT_BUBBLE = 0xFFFFE382;
    public static final int MARIO_DAY_OUT_TEXT = 0xFF3D2E00;
    /** قرمز قارچ — بج روز */
    public static final int MARIO_DAY_BADGE_BG = 0xFFC6281C;
    public static final int MARIO_DAY_BADGE_TEXT = 0xFFFFFFFF;
    public static final int MARIO_DAY_FIELD_BG = 0xFFFFFFFF;
    public static final int MARIO_DAY_FIELD_BORDER = 0xFFD5E1F4;
    public static final int MARIO_DAY_NAV_PILL = 0xFFFFE382;
    public static final int MARIO_DAY_SHADOW_TINT = 0xFFC6281C;
    public static final float MARIO_DAY_SHADOW_ALPHA = 0.25f;

    /** روبان‌های سرزمین ماریو — هویت رنگی تم (اکسنت‌ها، لوگو و آیکون از این‌ها تغذیه می‌شوند) */
    public static final int MARIO_COIN_GOLD = 0xFFFBD000;
    public static final int MARIO_MUSHROOM_RED = 0xFFE52521;
    public static final int MARIO_PIPE_GREEN = 0xFF43B047;
    public static final int MARIO_SKY_BLUE = 0xFF5C94FC;
    public static final int MARIO_FIRE_HOT = 0xFFFF8A3C;
    public static final int MARIO_WARP_PURPLE = 0xFFA077E8;
    public static final int MARIO_CLOUD_WHITE = 0xFFF8F8F8;
    public static final int MARIO_GROUND_BROWN = 0xFFC84C0C;

    /** ۳ اکسنت شب دنیای ماریو: طلای سکه (نوشتار اصلی)، گدازهٔ آتش، سبز لوله */
    public static final int[] ACCENT_MARIO_NIGHT = { 0xFFFBD000, 0xFFFF8A3C, 0xFF43B047 };
    /** ۳ اکسنت روز سرزمین ماریو: قرمز عمیق، سبز عمیق لوله، طلای عمیق سکه */
    public static final int[] ACCENT_MARIO_DAY = { 0xFFC6281C, 0xFF2E7D32, 0xFFB3651F };

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
    // Shape — Expressive Material (حباب ۲۶، کارت ۲۰، پیل ۳۲، دیالوگ ۲۸، فیلد ۱۶، بج ۱۲، فاب ۲۰، منو ۲۰)
    // ─────────────────────────────────────────────────────────────────────────

    public static final float SHAPE_BUBBLE = 26f;
    public static final float SHAPE_CARD = 20f;
    public static final float SHAPE_NAV_PILL = 32f;
    /** قدم ۲۹ — شعاع کارت دیالوگ Expressive: ۹-پیچ popup_fixed_alert4 بازتولید شد (آپستریم ~۱۶dp بود)
     *  + سه مسیر بلور AlertDialog (خروجی ۲۰/۱۲dp ناهمخوان) به همین توکن بایند شد؛ اسپینر ۱۸ خودش سطح کوچک است */
    public static final float SHAPE_DIALOG = 28f;
    /** قدم ۳۰ — شعاع قوس بالای پوستهٔ باتم‌شیت Expressive: ۹-پچ sheet_shadow_round با
     *  Tools/regenerate_sheet_9patch.py بازتولید شد (قوس نرم مؤثر آپستریم ~۲۰dp بود)؛ هم‌زبانهٔ SHAPE_DIALOG.
     *  مصرف‌کننده: asset ۹-پچ (۱۸ مصرف‌کنندهٔ BottomSheet) — حاشیه‌های کارت و پدینگ محتوا عیناً آپستریم حفظ شد */
    public static final float SHAPE_SHEET = 28f;
    public static final float SHAPE_FIELD = 16f;
    /** قدم ۱۴ — شعاع شمارنده/بج لیست چت (آپستریم ۱۱٫۵ بود؛ ۱۲ ≥ نصف ارتفاع بج = پیل کامل) */
    public static final float SHAPE_BADGE = 12f;
    /** قدم ۱۵ — شعاع فاب شناور Expressive (مربع‌گرد ۲۰dp؛ آپستریم دایره کامل بود) */
    public static final float SHAPE_FAB = 20f;
    /** قدم ۱۶ — شعاع کارت منوی اصلی/پاپ‌آپ Expressive (۹-پیچ popup_fixed_alert؛ آپستریم ۱۲ بود؛ هم‌زبان کارت قدم ۱۳) */
    public static final float SHAPE_MENU = 20f;
    /** قدم ۱۶ — شعاع ردیف‌های منو؛ قانون گردش تو‌در‌تو M3: SHAPE_MENU − پدینگ پاپ‌آپ (۸dp) = ۱۲ */
    public static final float SHAPE_MENU_ROW = 12f;

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
    // مقیاس نوع M3 — قدم ۹ (روی فونت برند Baloo Bhaijaan 2 / AmberGram UI)
    //
    // هر نقش یک int[12]: [سایز، ارتفاع‌خط، ترکینگ×۱۰۰، وزن] × (بزرگ، متوسط، کوچک)
    // واحد سایز/ارتفاع‌خط = sp، ترکینگ = ×۱۰۰sp (۵۰ یعنی ۰.۵sp)، وزن = کلاس OS/2.
    // محور وزن برند روی همان خانواده (OFL، بدون RFN): ۴۰۰/۵۰۰/۶۰۰/۷۰۰ —
    //   ۴۰۰ → fonts/ambergramui-regular.ttf، ۵۰۰ → ambergramui-med.ttf،
    //   ۶۰۰ → ambergramui-semibold.ttf، ۷۰۰ → ambergramui.ttf (صدای برند موجود)
    //   (نام فایل «med» عمداً کوتاه است تا در getTypeface به تلهٔ
    //    contains("medium") → setWeight(700) تکان نخورد؛ مپ صریح در getTypeface)
    //
    // نقشه مصرف درون‌اپ (مصرف تدریجی از قدم ۱۱ / فاز ۲ به بعد):
    //   TITLE_LARGE   → عنوان اکشن‌بار (مقصد ۲۲/۲۸)
    //   TITLE_MEDIUM  → عنوان ردیف‌ها (۱۶/۲۴)
    //   BODY_LARGE    → متن پیام پیش‌فرض (۱۶)
    //   BODY_MEDIUM   → زیرعنوان ردیف‌ها (۱۴)
    //   LABEL_MEDIUM  → زمان/بج/متادیتا (۱۲)
    //   LABEL_LARGE   → سربرگ‌های بخش تنظیمات (۱۴)
    // ─────────────────────────────────────────────────────────────────────────

    /** نمایش (Display) — لارج ۵۷/۶۴؛ مدیوم ۴۵/۵۲؛ اسمال ۳۶/۴۴ */
    public static final int[] TYPE_DISPLAY = { 57, 64, -25, 400,  45, 52, 0, 400,  36, 44, 0, 400 };
    /** سرفصل (Headline) — لارج ۳۲/۴۰؛ مدیوم ۲۸/۳۶؛ اسمال ۲۴/۳۲ */
    public static final int[] TYPE_HEADLINE = { 32, 40, 0, 400,  28, 36, 0, 400,  24, 32, 0, 400 };
    /** عنوان (Title) — لارج ۲۲/۲۸؛ مدیوم ۱۶/۲۴؛ اسمال ۱۴/۲۰ */
    public static final int[] TYPE_TITLE = { 22, 28, 0, 400,  16, 24, 15, 500,  14, 20, 10, 500 };
    /** متن (Body) — لارج ۱۶/۲۴؛ مدیوم ۱۴/۲۰؛ اسمال ۱۲/۱۶ */
    public static final int[] TYPE_BODY = { 16, 24, 50, 400,  14, 20, 25, 400,  12, 16, 40, 400 };
    /** برچسب (Label) — لارج ۱۴/۲۰؛ مدیوم ۱۲/۱۶؛ اسمال ۱۱/۱۶ */
    public static final int[] TYPE_LABEL = { 14, 20, 10, 500,  12, 16, 50, 500,  11, 16, 50, 500 };

    /** شاخص فیلد در int[12] هر نقش */
    public static final int TYPE_SIZE = 0, TYPE_LINE = 1, TYPE_TRACK = 2, TYPE_WEIGHT = 3;

    /** اندازه نمونه در نقش (۰=لارج، ۱=متوسط، ۲=اسمال) — خروجی sp */
    public static int typeSizeSp(int[] role, int variant) {
        return role[variant * 4 + TYPE_SIZE];
    }

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

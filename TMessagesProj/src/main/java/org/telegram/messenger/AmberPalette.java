package org.telegram.messenger;

import androidx.core.graphics.ColorUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * AmberGram UI 2.0 — موتور پالت (مصرف‌کننده AmberTokens).
 *
 * هر کلید به‌صورت ternary روز/شب از توکن‌ها + مشتق‌های alpha/over ساخته می‌شود.
 * نام کلیدها از ThemeColors.createColorKeysMap واقعی استخراج و اعتبارسنجی شده‌اند
 * (۸۶۲ نام معتبر؛ شامل قراردادهای عجیب مثل chat_wallpaper_gradient_to).
 *
 * مصرف: مولد Tools/generate_amber_theme2.py این فایل را واقعاً تفسیر و ارزیابی
 * می‌کند (بدون تکرار رنگ) و فایل‌های attheme را می‌سازد.
 */
public final class AmberPalette {

    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;
    private static Map<String, Integer> premiereDayCache;
    private static Map<String, Integer> premiereNightCache;
    private static Map<String, Integer> marioDayCache;
    private static Map<String, Integer> marioNightCache;
    private static Map<String, Integer> harmonyDayCache;
    private static Map<String, Integer> harmonyNightCache;
    private static Map<String, Integer> swDayCache;
    private static Map<String, Integer> swNightCache;
    private static Map<String, Integer> slingDayCache;
    private static Map<String, Integer> slingNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا)، MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا)،
     * MODE_PREMIERE_NIGHT / MODE_PREMIERE_DAY (شب اکران)، MODE_MARIO_NIGHT / MODE_MARIO_DAY (دنیای ماریو)،
     * MODE_HARMONY_NIGHT / MODE_HARMONY_DAY (هم‌آهنگ)، MODE_SW_NIGHT / MODE_SW_DAY (سمت تاریک/روشن)
     * و MODE_SLING_NIGHT / MODE_SLING_DAY (اسلینگ‌شات/حملهٔ شبانه).
     * برندهای پنجم تا هفتم v0.9.11 — «دیسکورد، جنگ ستاره‌ها، انگری بردز». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_HARMONY_NIGHT) {
            if (harmonyNightCache == null) {
                harmonyNightCache = build(false, false, false, false, false, false, true);
            }
            return harmonyNightCache;
        }
        if (mode == AmberTokens.MODE_HARMONY_DAY) {
            if (harmonyDayCache == null) {
                harmonyDayCache = build(true, false, false, false, false, false, true);
            }
            return harmonyDayCache;
        }
        if (mode == AmberTokens.MODE_SW_NIGHT) {
            if (swNightCache == null) {
                swNightCache = build(false, false, false, false, false, true, false);
            }
            return swNightCache;
        }
        if (mode == AmberTokens.MODE_SW_DAY) {
            if (swDayCache == null) {
                swDayCache = build(true, false, false, false, false, true, false);
            }
            return swDayCache;
        }
        if (mode == AmberTokens.MODE_SLING_NIGHT) {
            if (slingNightCache == null) {
                slingNightCache = build(false, false, false, false, true, false, false);
            }
            return slingNightCache;
        }
        if (mode == AmberTokens.MODE_SLING_DAY) {
            if (slingDayCache == null) {
                slingDayCache = build(true, false, false, false, true, false, false);
            }
            return slingDayCache;
        }
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false, false, false, false, false, false, false);
            }
            return nightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_NIGHT) {
            if (auroraNightCache == null) {
                auroraNightCache = build(false, true, false, false, false, false, false);
            }
            return auroraNightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_DAY) {
            if (auroraDayCache == null) {
                auroraDayCache = build(true, true, false, false, false, false, false);
            }
            return auroraDayCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_NIGHT) {
            if (premiereNightCache == null) {
                premiereNightCache = build(false, false, true, false, false, false, false);
            }
            return premiereNightCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_DAY) {
            if (premiereDayCache == null) {
                premiereDayCache = build(true, false, true, false, false, false, false);
            }
            return premiereDayCache;
        }
        if (mode == AmberTokens.MODE_MARIO_NIGHT) {
            if (marioNightCache == null) {
                marioNightCache = build(false, false, false, true, false, false, false);
            }
            return marioNightCache;
        }
        if (mode == AmberTokens.MODE_MARIO_DAY) {
            if (marioDayCache == null) {
                marioDayCache = build(true, false, false, true, false, false, false);
            }
            return marioDayCache;
        }
        if (dayCache == null) {
            dayCache = build(true, false, false, false, false, false, false);
        }
        return dayCache;
    }

    /** نام نامعتبر = 0 */
    public static int valueOf(String keyName, int mode) {
        Integer v = palette(mode).get(keyName);
        return v == null ? 0 : v;
    }

    /** خروجی فایل attheme مرتب الفبایی — برای مولد قدم ۳/۴ */
    public static String atthemeText(int mode) {
        Map<String, Integer> m = palette(mode);
        ArrayList<String> keys = new ArrayList<>(m.keySet());
        Collections.sort(keys);
        StringBuilder sb = new StringBuilder();
        for (String k : keys) {
            sb.append(k).append('=').append(m.get(k)).append('\n');
        }
        return sb.toString();
    }

    /** d = روز/شب — au = آئورورا — pr = شب اکران — ma = دنیای ماریو — sl = اسلینگ‌شات (انگری بردز) — sw = سمت تاریک (جنگ ستاره‌ها) — ha = هم‌آهنگ (دیسکورد) در برابر برند کهربا */
    private static Map<String, Integer> build(boolean d, boolean au, boolean pr, boolean ma, boolean sl, boolean sw, boolean ha) {
        HashMap<String, Integer> m = new HashMap<>();

        // ── اتم‌ها ───────────────────────────────────────────────────────────
        final int text = au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? AmberTokens.SW_DAY_TEXT : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.SLING_NIGHT_TEXT) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_TEXT);
        final int dim = au ? (d ? AmberTokens.AURORA_DAY_TEXT_DIM : AmberTokens.AURORA_NIGHT_TEXT_DIM) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT_DIM : AmberTokens.PREMIERE_NIGHT_TEXT_DIM) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT_DIM : AmberTokens.MARIO_NIGHT_TEXT_DIM) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT_DIM : AmberTokens.HARMONY_NIGHT_TEXT_DIM) : sw ? (d ? AmberTokens.SW_DAY_TEXT_DIM : AmberTokens.SW_NIGHT_TEXT_DIM) : sl ? (d ? AmberTokens.SLING_DAY_TEXT_DIM : AmberTokens.SLING_NIGHT_TEXT_DIM) : (d ? AmberTokens.DAY_TEXT_DIM : AmberTokens.NIGHT_TEXT_DIM);
        final int navPill = au ? (d ? AmberTokens.AURORA_DAY_NAV_PILL : AmberTokens.AURORA_NIGHT_NAV_PILL) : pr ? (d ? AmberTokens.PREMIERE_DAY_NAV_PILL : AmberTokens.PREMIERE_NIGHT_NAV_PILL) : ma ? (d ? AmberTokens.MARIO_DAY_NAV_PILL : AmberTokens.MARIO_NIGHT_NAV_PILL) : ha ? (d ? AmberTokens.HARMONY_DAY_NAV_PILL : AmberTokens.HARMONY_NIGHT_NAV_PILL) : sw ? (d ? AmberTokens.SW_DAY_NAV_PILL : AmberTokens.SW_NIGHT_NAV_PILL) : sl ? (d ? AmberTokens.SLING_DAY_NAV_PILL : AmberTokens.SLING_NIGHT_NAV_PILL) : (d ? AmberTokens.DAY_NAV_PILL : AmberTokens.NIGHT_NAV_PILL);
        final int time = au ? (d ? AmberTokens.AURORA_DAY_TIME : AmberTokens.AURORA_NIGHT_TIME) : pr ? (d ? AmberTokens.PREMIERE_DAY_TIME : AmberTokens.PREMIERE_NIGHT_TIME) : ma ? (d ? AmberTokens.MARIO_DAY_TIME : AmberTokens.MARIO_NIGHT_TIME) : ha ? (d ? AmberTokens.HARMONY_DAY_TIME : AmberTokens.HARMONY_NIGHT_TIME) : sw ? (d ? AmberTokens.SW_DAY_TIME : AmberTokens.SW_NIGHT_TIME) : sl ? (d ? AmberTokens.SLING_DAY_TIME : AmberTokens.SLING_NIGHT_TIME) : (d ? AmberTokens.DAY_TIME : AmberTokens.NIGHT_TIME);
        final int accent = au ? (d ? AmberTokens.AURORA_DAY_ACCENT : AmberTokens.AURORA_NIGHT_ACCENT) : pr ? (d ? AmberTokens.PREMIERE_DAY_ACCENT : AmberTokens.PREMIERE_NIGHT_ACCENT) : ma ? (d ? AmberTokens.MARIO_DAY_ACCENT : AmberTokens.MARIO_NIGHT_ACCENT) : ha ? (d ? AmberTokens.HARMONY_DAY_ACCENT : AmberTokens.HARMONY_NIGHT_ACCENT) : sw ? (d ? AmberTokens.SW_DAY_ACCENT : AmberTokens.SW_NIGHT_ACCENT) : sl ? (d ? AmberTokens.SLING_DAY_ACCENT : AmberTokens.SLING_NIGHT_ACCENT) : (d ? AmberTokens.DAY_ACCENT : AmberTokens.NIGHT_ACCENT);
        final int accentBright = au ? (d ? AmberTokens.AURORA_DAY_ACCENT_BRIGHT : AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT) : pr ? (d ? AmberTokens.PREMIERE_DAY_ACCENT_BRIGHT : AmberTokens.PREMIERE_NIGHT_ACCENT_BRIGHT) : ma ? (d ? AmberTokens.MARIO_DAY_ACCENT_BRIGHT : AmberTokens.MARIO_NIGHT_ACCENT_BRIGHT) : ha ? (d ? AmberTokens.HARMONY_DAY_ACCENT_BRIGHT : AmberTokens.HARMONY_NIGHT_ACCENT_BRIGHT) : sw ? (d ? AmberTokens.SW_DAY_ACCENT_BRIGHT : AmberTokens.SW_NIGHT_ACCENT_BRIGHT) : sl ? (d ? AmberTokens.SLING_DAY_ACCENT_BRIGHT : AmberTokens.SLING_NIGHT_ACCENT_BRIGHT) : (d ? AmberTokens.DAY_ACCENT_BRIGHT : AmberTokens.NIGHT_ACCENT_BRIGHT);
        final int onAccent = au ? (d ? AmberTokens.AURORA_DAY_ON_ACCENT : AmberTokens.AURORA_NIGHT_ON_ACCENT) : pr ? (d ? AmberTokens.PREMIERE_DAY_ON_ACCENT : AmberTokens.PREMIERE_NIGHT_ON_ACCENT) : ma ? (d ? AmberTokens.MARIO_DAY_ON_ACCENT : AmberTokens.MARIO_NIGHT_ON_ACCENT) : ha ? (d ? AmberTokens.HARMONY_DAY_ON_ACCENT : AmberTokens.HARMONY_NIGHT_ON_ACCENT) : sw ? (d ? AmberTokens.SW_DAY_ON_ACCENT : AmberTokens.SW_NIGHT_ON_ACCENT) : sl ? (d ? AmberTokens.SLING_DAY_ON_ACCENT : AmberTokens.SLING_NIGHT_ON_ACCENT) : (d ? AmberTokens.DAY_ON_ACCENT : AmberTokens.NIGHT_ON_ACCENT);
        final int bg = au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_BG : AmberTokens.PREMIERE_NIGHT_BG) : ma ? (d ? AmberTokens.MARIO_DAY_BG : AmberTokens.MARIO_NIGHT_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_BG : AmberTokens.HARMONY_NIGHT_BG) : sw ? (d ? AmberTokens.SW_DAY_BG : AmberTokens.SW_NIGHT_BG) : sl ? (d ? AmberTokens.SLING_DAY_BG : AmberTokens.SLING_NIGHT_BG) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_BG);
        final int white = au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_BG : AmberTokens.PREMIERE_NIGHT_BG) : ma ? (d ? AmberTokens.MARIO_DAY_BG : AmberTokens.MARIO_NIGHT_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_BG : AmberTokens.HARMONY_NIGHT_BG) : sw ? (d ? AmberTokens.SW_DAY_BG : AmberTokens.SW_NIGHT_BG) : sl ? (d ? AmberTokens.SLING_DAY_BG : AmberTokens.SLING_NIGHT_BG) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP);
        final int header = au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_HEADER) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER : AmberTokens.PREMIERE_NIGHT_HEADER) : ma ? (d ? AmberTokens.MARIO_DAY_HEADER : AmberTokens.MARIO_NIGHT_HEADER) : ha ? (d ? AmberTokens.HARMONY_DAY_HEADER : AmberTokens.HARMONY_NIGHT_HEADER) : sw ? (d ? AmberTokens.SW_DAY_HEADER : AmberTokens.SW_NIGHT_HEADER) : sl ? (d ? AmberTokens.SLING_DAY_HEADER : AmberTokens.SLING_NIGHT_HEADER) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_HEADER);
        final int headerBorder = au ? (d ? AmberTokens.AURORA_DAY_HEADER_BORDER : AmberTokens.AURORA_NIGHT_HEADER_BORDER) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER_BORDER : AmberTokens.PREMIERE_NIGHT_HEADER_BORDER) : ma ? (d ? AmberTokens.MARIO_DAY_HEADER_BORDER : AmberTokens.MARIO_NIGHT_HEADER_BORDER) : ha ? (d ? AmberTokens.HARMONY_DAY_HEADER_BORDER : AmberTokens.HARMONY_NIGHT_HEADER_BORDER) : sw ? (d ? AmberTokens.SW_DAY_HEADER_BORDER : AmberTokens.SW_NIGHT_HEADER_BORDER) : sl ? (d ? AmberTokens.SLING_DAY_HEADER_BORDER : AmberTokens.SLING_NIGHT_HEADER_BORDER) : (d ? AmberTokens.DAY_HEADER_BORDER : AmberTokens.NIGHT_HEADER_BORDER);
        final int surface = au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_SURFACE);
        final int outline = au ? (d ? AmberTokens.AURORA_DAY_OUTLINE : AmberTokens.AURORA_NIGHT_OUTLINE) : pr ? (d ? AmberTokens.PREMIERE_DAY_OUTLINE : AmberTokens.PREMIERE_NIGHT_OUTLINE) : ma ? (d ? AmberTokens.MARIO_DAY_OUTLINE : AmberTokens.MARIO_NIGHT_OUTLINE) : ha ? (d ? AmberTokens.HARMONY_DAY_OUTLINE : AmberTokens.HARMONY_NIGHT_OUTLINE) : sw ? (d ? AmberTokens.SW_DAY_OUTLINE : AmberTokens.SW_NIGHT_OUTLINE) : sl ? (d ? AmberTokens.SLING_DAY_OUTLINE : AmberTokens.SLING_NIGHT_OUTLINE) : (d ? AmberTokens.DAY_OUTLINE : AmberTokens.NIGHT_OUTLINE);
        final int inBubble = au ? (d ? AmberTokens.AURORA_DAY_IN_BUBBLE : AmberTokens.AURORA_NIGHT_IN_BUBBLE) : pr ? (d ? AmberTokens.PREMIERE_DAY_IN_BUBBLE : AmberTokens.PREMIERE_NIGHT_IN_BUBBLE) : ma ? (d ? AmberTokens.MARIO_DAY_IN_BUBBLE : AmberTokens.MARIO_NIGHT_IN_BUBBLE) : ha ? (d ? AmberTokens.HARMONY_DAY_IN_BUBBLE : AmberTokens.HARMONY_NIGHT_IN_BUBBLE) : sw ? (d ? AmberTokens.SW_DAY_IN_BUBBLE : AmberTokens.SW_NIGHT_IN_BUBBLE) : sl ? (d ? AmberTokens.SLING_DAY_IN_BUBBLE : AmberTokens.SLING_NIGHT_IN_BUBBLE) : (d ? AmberTokens.DAY_IN_BUBBLE : AmberTokens.NIGHT_IN_BUBBLE);
        final int inText = au ? (d ? AmberTokens.AURORA_DAY_IN_TEXT : AmberTokens.AURORA_NIGHT_IN_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_IN_TEXT : AmberTokens.PREMIERE_NIGHT_IN_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_IN_TEXT : AmberTokens.MARIO_NIGHT_IN_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_IN_TEXT : AmberTokens.HARMONY_NIGHT_IN_TEXT) : sw ? (d ? AmberTokens.SW_DAY_IN_TEXT : AmberTokens.SW_NIGHT_IN_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_IN_TEXT : AmberTokens.SLING_NIGHT_IN_TEXT) : (d ? AmberTokens.DAY_IN_TEXT : AmberTokens.NIGHT_IN_TEXT);
        final int outBubble = au ? (d ? AmberTokens.AURORA_DAY_OUT_BUBBLE : AmberTokens.AURORA_NIGHT_OUT_BUBBLE) : pr ? (d ? AmberTokens.PREMIERE_DAY_OUT_BUBBLE : AmberTokens.PREMIERE_NIGHT_OUT_BUBBLE) : ma ? (d ? AmberTokens.MARIO_DAY_OUT_BUBBLE : AmberTokens.MARIO_NIGHT_OUT_BUBBLE) : ha ? (d ? AmberTokens.HARMONY_DAY_OUT_BUBBLE : AmberTokens.HARMONY_NIGHT_OUT_BUBBLE) : sw ? (d ? AmberTokens.SW_DAY_OUT_BUBBLE : AmberTokens.SW_NIGHT_OUT_BUBBLE) : sl ? (d ? AmberTokens.SLING_DAY_OUT_BUBBLE : AmberTokens.SLING_NIGHT_OUT_BUBBLE) : (d ? AmberTokens.DAY_OUT_BUBBLE : AmberTokens.NIGHT_OUT_BUBBLE);
        final int outText = au ? (d ? AmberTokens.AURORA_DAY_OUT_TEXT : AmberTokens.AURORA_NIGHT_OUT_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_OUT_TEXT : AmberTokens.PREMIERE_NIGHT_OUT_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_OUT_TEXT : AmberTokens.MARIO_NIGHT_OUT_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_OUT_TEXT : AmberTokens.HARMONY_NIGHT_OUT_TEXT) : sw ? (d ? AmberTokens.SW_DAY_OUT_TEXT : AmberTokens.SW_NIGHT_OUT_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_OUT_TEXT : AmberTokens.SLING_NIGHT_OUT_TEXT) : (d ? AmberTokens.DAY_OUT_TEXT : AmberTokens.NIGHT_OUT_TEXT);
        final int badgeText = au ? (d ? AmberTokens.AURORA_DAY_BADGE_TEXT : AmberTokens.AURORA_NIGHT_BADGE_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_BADGE_TEXT : AmberTokens.PREMIERE_NIGHT_BADGE_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_BADGE_TEXT : AmberTokens.MARIO_NIGHT_BADGE_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_BADGE_TEXT : AmberTokens.HARMONY_NIGHT_BADGE_TEXT) : sw ? (d ? AmberTokens.SW_DAY_BADGE_TEXT : AmberTokens.SW_NIGHT_BADGE_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_BADGE_TEXT : AmberTokens.SLING_NIGHT_BADGE_TEXT) : (d ? AmberTokens.DAY_BADGE_TEXT : AmberTokens.NIGHT_BADGE_TEXT);
        final int fieldBg = au ? (d ? AmberTokens.AURORA_DAY_FIELD_BG : AmberTokens.AURORA_NIGHT_FIELD_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_FIELD_BG : AmberTokens.PREMIERE_NIGHT_FIELD_BG) : ma ? (d ? AmberTokens.MARIO_DAY_FIELD_BG : AmberTokens.MARIO_NIGHT_FIELD_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_FIELD_BG : AmberTokens.HARMONY_NIGHT_FIELD_BG) : sw ? (d ? AmberTokens.SW_DAY_FIELD_BG : AmberTokens.SW_NIGHT_FIELD_BG) : sl ? (d ? AmberTokens.SLING_DAY_FIELD_BG : AmberTokens.SLING_NIGHT_FIELD_BG) : (d ? AmberTokens.DAY_FIELD_BG : AmberTokens.NIGHT_FIELD_BG);
        final int fieldBorder = au ? (d ? AmberTokens.AURORA_DAY_FIELD_BORDER : AmberTokens.AURORA_NIGHT_FIELD_BORDER) : pr ? (d ? AmberTokens.PREMIERE_DAY_FIELD_BORDER : AmberTokens.PREMIERE_NIGHT_FIELD_BORDER) : ma ? (d ? AmberTokens.MARIO_DAY_FIELD_BORDER : AmberTokens.MARIO_NIGHT_FIELD_BORDER) : ha ? (d ? AmberTokens.HARMONY_DAY_FIELD_BORDER : AmberTokens.HARMONY_NIGHT_FIELD_BORDER) : sw ? (d ? AmberTokens.SW_DAY_FIELD_BORDER : AmberTokens.SW_NIGHT_FIELD_BORDER) : sl ? (d ? AmberTokens.SLING_DAY_FIELD_BORDER : AmberTokens.SLING_NIGHT_FIELD_BORDER) : (d ? AmberTokens.DAY_FIELD_BORDER : AmberTokens.NIGHT_FIELD_BORDER);

        // ── مشتق‌ها ──────────────────────────────────────────────────────────
        final int sel = AmberTokens.alpha(text, d ? 0.06f : 0.08f);
        final int selIn = AmberTokens.over(accent, inBubble, d ? 0.14f : 0.16f);
        final int selOut = AmberTokens.over(accent, outBubble, d ? 0.14f : 0.16f);
        final int divider = au ? (d ? AmberTokens.AURORA_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.AURORA_NIGHT_OUTLINE, 0.55f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.PREMIERE_NIGHT_OUTLINE, 0.55f)) : ma ? (d ? AmberTokens.MARIO_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.MARIO_NIGHT_OUTLINE, 0.55f)) : ha ? (d ? AmberTokens.HARMONY_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.HARMONY_NIGHT_OUTLINE, 0.55f)) : sw ? (d ? AmberTokens.SW_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.SW_NIGHT_OUTLINE, 0.55f)) : sl ? (d ? AmberTokens.SLING_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.SLING_NIGHT_OUTLINE, 0.55f)) : (d ? AmberTokens.DAY_OUTLINE : AmberTokens.alpha(AmberTokens.NIGHT_OUTLINE, 0.55f));
        // قدم ۲۵ — چیپ سرویس/تاریخ: با «احترام به کلید» در applyChatServiceMessageColor چیپ همیشه از کلید می‌آید؛
        // روز: اسکریم جوهر ۶۵٪ (متن سفید ۵٫۸۸:۱ روی ترکیب با وایپرپ کرم — قبلاً DAY_TEXT_DIM×۷۰٪ فقط ۳٫۰۴:۱)؛ شب بدون تغییر (۱۵٫۱:۱)
        final int svcBg = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_TEXT : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_SURFACE), d ? 0.65f : 0.70f);
        // انتخاب‌شده/فشرده: روز جوهر ۷۸٪ (تیره‌تر) / شب سطح +۱۲٪ به‌سمت متن (روشن‌تر) — بازخورد محسوس در هر دو (قبلاً همان رنگ عادی بود)
        final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.over(AmberTokens.PREMIERE_NIGHT_TEXT, AmberTokens.PREMIERE_NIGHT_SURFACE, 0.12f)) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.over(AmberTokens.MARIO_NIGHT_TEXT, AmberTokens.MARIO_NIGHT_SURFACE, 0.12f)) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.over(AmberTokens.HARMONY_NIGHT_TEXT, AmberTokens.HARMONY_NIGHT_SURFACE, 0.12f)) : sw ? (d ? AmberTokens.SW_DAY_TEXT : AmberTokens.over(AmberTokens.SW_NIGHT_TEXT, AmberTokens.SW_NIGHT_SURFACE, 0.12f)) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.over(AmberTokens.SLING_NIGHT_TEXT, AmberTokens.SLING_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);
        // ریپل داخل چیپ (دکمه‌های بات): سفید ۱۴٪ روی قرص تیره — قبلاً همان رنگ چیپ بود = ریپل نامرئی
        final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);
        final int goDown = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE), d ? 0.90f : 0.80f);
        final int deepFile = au ? (d ? 0xFFE9EEF6 : 0xFF1B2430) : pr ? (d ? 0xFFFFF0D2 : 0xFF241C36) : ma ? (d ? 0xFFE3EEFF : 0xFF1A2344) : ha ? (d ? 0xFFE9EBFA : 0xFF1D1F38) : sw ? (d ? 0xFFF2EEDA : 0xFF141C30) : sl ? (d ? 0xFFE2F1FC : 0xFF12303E) : (d ? 0xFFF7E3C8 : 0xFF2E2618);
        final int outDim = AmberTokens.alpha(outText, 0.65f);
        final int outTime = au ? (d ? 0xFF0E7260 : 0xFF7FE8D0) : pr ? (d ? 0xFF7A5A08 : 0xFF5C3D02) : ma ? (d ? 0xFF6E5605 : 0xFF123A1A) : ha ? (d ? 0xFFD8DBFA : 0xFFBFC4FA) : sw ? (d ? 0xFFF2D8DC : 0xFFF2D8DC) : sl ? (d ? 0xFF6E4A08 : 0xFFF6C6BE) : (d ? 0xFFA8701E : 0xFFD9BC7A);
        // قدم ۲۱ — تیک خوانده‌شدهٔ حباب خروجی: روز accentBright (E8871E) روی حباب FFDDB8 فقط ۲٫۰۶:۱ بود
        // ← «کهربای برشته» 9C5200 (۴٫۵۰:۱؛ از تیک ارسال اکسنت C25E00 عمیق‌تر و متمایز)؛ شب accentBright سالم است (۵٫۵۸)
        final int sentCheckRead = au ? (d ? 0xFF06503F : AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT) : pr ? (d ? 0xFF8A5C06 : 0xFF4A3202) : ma ? (d ? 0xFF7A5E06 : 0xFF0F3A1E) : ha ? (d ? 0xFF273098 : 0xFFBFC4FA) : sw ? (d ? 0xFF7A1420 : 0xFFFF9BA3) : sl ? (d ? 0xFF6E4A08 : 0xFFF6C6BE) : (d ? 0xFF9C5200 : AmberTokens.NIGHT_ACCENT_BRIGHT);
        final int red = d ? 0xFFB4382C : 0xFFFF6E54;
        // قدم ۲۸ — قرمزِ سمت حباب خروجی (هم‌الگوی تفکیک time/outTime): حباب خروجی شب روشن‌تر است
        // (5C4000) و FF6E54 روی تینت خودش فقط ۲٫۹۶ می‌شد ← سالمون روشن‌تر FF8E78 (۳٫۶۶ روی چیپ)
        final int redOut = d ? 0xFFB4382C : 0xFFFF8E78;
        final int green = d ? 0xFF3D7A2B : 0xFF7DBE72;

        // ── پنجره‌ها و سطوح عمومی ────────────────────────────────────────────
        m.put("windowBackgroundWhite", white);
        m.put("windowBackgroundWhiteBlackText", text);
        m.put("windowBackgroundWhiteGrayText", dim);
        m.put("windowBackgroundWhiteGrayIcon", dim);
        m.put("windowBackgroundWhiteHintText", time);
        m.put("windowBackgroundWhiteValueText", accent);
        m.put("windowBackgroundWhiteLinkText", accent);
        m.put("windowBackgroundWhiteLinkSelection", AmberTokens.alpha(accent, 0.25f));
        m.put("windowBackgroundWhiteBlueText", accent);
        m.put("windowBackgroundWhiteBlueText2", accent);
        m.put("windowBackgroundWhiteBlueText3", accent);
        m.put("windowBackgroundWhiteBlueText4", accent);
        m.put("windowBackgroundWhiteBlueText5", accent);
        m.put("windowBackgroundWhiteBlueText6", accent);
        m.put("windowBackgroundWhiteBlueText7", accent);
        m.put("windowBackgroundWhiteBlueButton", accent);
        m.put("windowBackgroundWhiteBlueHeader", accent);
        m.put("windowBackgroundWhiteBlueIcon", accent);
        m.put("windowBackgroundWhiteGreenText", green);
        m.put("windowBackgroundWhiteGreenText2", green);
        m.put("windowBackgroundWhiteInputField", fieldBorder);
        m.put("windowBackgroundWhiteInputFieldActivated", accent);
        m.put("windowBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_BG) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_BG) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));
        m.put("windowBackgroundGrayShadow", au ? (d ? 0x14171B26 : 0x28000000) : pr ? (d ? 0x14332A18 : 0x28000000) : ma ? (d ? 0x1416243E : 0x28000000) : ha ? (d ? 0x142E3050 : 0x28000000) : sw ? (d ? 0x142B283A : 0x28000000) : sl ? (d ? 0x14233A28 : 0x28000000) : (d ? 0x14211A12 : 0x28000000));
        m.put("windowBackgroundChecked", accent);
        m.put("windowBackgroundUnchecked", outline);
        m.put("windowBackgroundCheckText", text);
        m.put("divider", divider);

        // ── اکشن‌بار ─────────────────────────────────────────────────────────
        m.put("actionBarDefault", header);
        // قدم ۱۱ — آیکون‌های هدر اکسپرسیو: جوهر کم‌رنگ (dim) مثل موک کانسپت C،
        // نه متن کامل — سلسله‌مراتب بصری: لوگو پررنگ، آیکون‌ها ثانویه.
        m.put("actionBarDefaultIcon", dim);
        m.put("actionBarDefaultTitle", text);
        m.put("actionBarDefaultSubtitle", dim);
        m.put("actionBarDefaultSelector", AmberTokens.alpha(text, d ? 0.08f : 0.10f));
        // قدم ۱۷ — متن/کرسر فیلد جستجو روی هدر: قبلاً fieldBg بود (روز سفید روی کرم FFE9CF
        // = ۱٫۱۳:۱ و شب تیره روی تیره ≈ ۱٫۰۵:۱ = عملاً نامرئی) ← جوهر (text) هم‌زبانه actionBarDefaultTitle
        m.put("actionBarDefaultSearch", text);
        m.put("actionBarDefaultSearchPlaceholder", dim);
        m.put("actionBarDefaultSearchArchivedPlaceholder", dim);
        m.put("actionBarDefaultArchived", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));
        m.put("actionBarDefaultArchivedIcon", dim);
        m.put("actionBarDefaultArchivedTitle", text);
        m.put("actionBarDefaultArchivedSelector", AmberTokens.alpha(text, 0.08f));
        // قدم ۱۶ — روز سفید هاردکد نشتی رنگ خارج از توکن بود ← سطح گرم DAY_SURFACE؛ شب NIGHT_SURFACE حفظ
        // سایه ۹-پیچ با MULTIPLY توسط همین رنگ تینت می‌شود → سایه گرم روز / تیره شب خودکار
        m.put("actionBarDefaultSubmenuBackground", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_SURFACE));
        m.put("actionBarDefaultSubmenuItem", text);
        m.put("actionBarDefaultSubmenuItemIcon", dim);
        m.put("actionBarDefaultSubmenuSeparator", divider);
        m.put("actionBarTabActiveText", outText);
        m.put("actionBarTabUnactiveText", dim);
        m.put("actionBarTabLine", navPill);
        m.put("actionBarTabSelector", AmberTokens.alpha(accent, 0.10f));
        m.put("actionBarWhiteSelector", AmberTokens.alpha(accent, 0.12f));
        m.put("actionBarBrowser", bg);
        m.put("actionBarActionModeDefault", outBubble);
        m.put("actionBarActionModeDefaultIcon", outText);
        m.put("actionBarActionModeDefaultTop", outBubble);
        m.put("actionBarActionModeDefaultSelector", AmberTokens.alpha(outText, 0.10f));
        m.put("actionBarActionModeReaction", AmberTokens.alpha(outText, 0.12f));
        m.put("actionBarActionModeReactionText", outText);
        m.put("actionBarActionModeReactionDot", accent);

        // ── لیست چت ──────────────────────────────────────────────────────────
        // UI2 قدم ۱۳ — ripple پرس کارت ردیف گرم شد (اکسنت×۸٪ روز / ×۱۰٪ شب به‌جای
        // خاکستری بی‌هویت پایه) تا کارت پرس Expressive با زبان کانسپت C هم‌خوان باشد.
        m.put("listSelectorSDK21", AmberTokens.alpha(accent, d ? 0.08f : 0.10f));
        // قدم ۱۷ — selector عمومی (کلید پیش‌فرض آپستریم 0x0f000000 سرد = نشتی خاکستری؛
        // فقط چند سایت زنده دارد: ripple دکمه پاک‌کردن جستجو/آیکون‌های اضافه فیلد جستجو +
        // کلیدهای fallback مثل settings/profile-tab) ← هم‌زبانه listSelectorSDK21
        m.put("listSelector", AmberTokens.alpha(accent, d ? 0.08f : 0.10f));
        // قدم ۱۷ — کرسر فیلد جستجوی شناور (FragmentSearchField): قبلاً F97A20 خارج از توکن
        // (میراث پایه قدیمی) ← اکسنت؛ کنتراست روی پس‌زمینه تونال فیلد: روز ۳٫۲۸:۱ / شب ۷٫۲۸:۱
        m.put("groupcreate_cursor", accent);
        // قدم ۱۷ — سرستون‌های بخش‌بندی نتایج جستجو (GraySectionCell): قبلاً 121213 سرد
        // (روز تقریباً مشکی روی لیست روشن = شکاف هویتی) ← سطح گرم surface + متن dim
        m.put("graySection", surface);
        m.put("graySectionText", dim);
        // قدم ۱۸ — خانواده سوییچ/چک‌باکس انتخاب (حالت انتخاب/آرشیو و سوییچ‌های عمومی):
        // switch2Track قبلاً در روز قرمز آپستریم (F57480) و شب خاکستری سرد (3A3A3E) بود ← هم‌زبانه switchTrack
        // switch2TrackChecked در روز آبی آپستریم (229AF0) و شب F97316 خارج‌ازتوکن بود ← اکسنت
        // (سوییچ متن‌دار TextCheckCell2/UniversalAdapter/چیپ‌های چک‌باکس)
        m.put("switch2Track", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : pr ? (d ? 0xFFE7DBBE : AmberTokens.PREMIERE_NIGHT_OUTLINE) : ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE) : ha ? (d ? 0xFFD8DAF0 : AmberTokens.HARMONY_NIGHT_OUTLINE) : sw ? (d ? 0xFFE0D9BF : AmberTokens.SW_NIGHT_OUTLINE) : sl ? (d ? 0xFFD8E8F2 : AmberTokens.SLING_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));
        m.put("switch2TrackChecked", accent);
        // متن فرعی ردیف‌های منوی اکشن‌مود (ActionBarMenuSubItem.subtextView): خاکستری سرد آپستریم 7C8288 روی
        // کارت گرم قدم ۱۶ ← dim (کنتراست ۴٫۳۴/۶٫۲۰)
        m.put("groupcreate_sectionText", dim);
        // پس‌زمینه چیپ‌های فیلتر جستجو (ActionBarMenuItem.SearchFilterView): خاکستری سرد F2F2F2/1D1D21 ← سطح گرم
        m.put("groupcreate_spanBackground", surface);
        // متن/آیکون روی اکسنت (چیپ انتخاب‌شده فیلتر + آواتار ترکیبی): سفید هاردکد آپستریم — شب روی اکسنت روشن ۲٫۰۳:۱ ← onAccent
        m.put("featuredStickers_buttonText", onAccent);
        // دستگیره انتخاب متن فیلد جستجو: آبی آپستریم روز (63C8FF) و F97316 شب ← اکسنت (۴٫۰۸/۸٫۷۹)
        m.put("chat_TextSelectionCursor", accent);
        m.put("chats_name", text);
        m.put("chats_nameMessage", dim);
        m.put("chats_nameMessage_threeLines", dim);
        m.put("chats_message", dim);
        m.put("chats_message_threeLines", dim);
        m.put("chats_nameArchived", dim);
        m.put("chats_messageArchived", dim);
        m.put("chats_nameMessageArchived", dim);
        m.put("chats_nameMessageArchived_threeLines", dim);
        m.put("chats_date", time);
        m.put("chats_date_bold", time);
        m.put("chats_muteIcon", dim);
        m.put("chats_attachMessage", dim);
        m.put("chats_secretName", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chats_secretIcon", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chats_verifiedBackground", accent);
        m.put("chats_verifiedCheck", onAccent);
        m.put("chats_onlineCircle", d ? 0xFF3E9C4B : 0xFF63C26B);
        m.put("chats_actionBackground", deepFile);
        m.put("chats_actionIcon", accent);
        m.put("chats_actionMessage", dim);
        m.put("chats_actionPressedBackground", AmberTokens.alpha(text, 0.08f));
        // UI2 قدم ۱۵ — فاب شناور Expressive (FragmentFloatingButton): پس‌زمینه از
        // featuredStickers_addButton ← اکسنت (روز تا امروز نشتی آبی 4DA0EB و شب F97316 خارج
        // از توکن بود)، پرس = over(accent، onAccent، ۲۰٪) و جوهر آیکون روی کلید جدید
        // featuredStickers_addButtonIcon ← onAccent (کلید chats_actionIcon دست‌نخورده ماند
        // چون فاب‌های کلاسیک دیگر صفحه‌ها با پس‌زمینه deepFile به جوهر اکسنت نیاز دارند).
        // شعاع فرم و سایه آمبر در خود کلاس از SHAPE_FAB/ELEV_FAB/SHADOW_* توکن می‌خواند.
        m.put("featuredStickers_addButton", accent);
        m.put("featuredStickers_addButtonPressed", AmberTokens.over(accent, onAccent, 0.20f));
        m.put("featuredStickers_addButtonIcon", onAccent);
        m.put("chats_archiveBackground", surface);
        m.put("chats_archiveIcon", dim);
        m.put("chats_archiveText", dim);
        m.put("chats_archivePinBackground", headerBorder);
        m.put("chats_archivePullDownBackground", headerBorder);
        m.put("chats_archivePullDownBackgroundActive", accent);
        m.put("chats_unreadCounter", accent);
        m.put("chats_unreadCounterText", onAccent);
        // UI2 قدم ۱۴ — شمارنده/بج‌ها: پرایمری = اکسنت/روی‌اکسنت (مثل مولد توکن)،
        // بی‌صدا = کانتینر تونال خنثی (مرز ظریف) با جوهر dim — پیش از این muted
        // با سطح + متن سفید سراسری رندر می‌شد (روژه ~۱٫۱:۱ نامرئی؛ شب ~۱٫۰۵:۱).
        // متن بی‌صدا کلید جدید chats_unreadCounterMutedText است (ثبت در Theme/ThemeColors).
        m.put("chats_unreadCounterMuted", outline);
        m.put("chats_unreadCounterMutedText", dim);
        m.put("chats_pinnedIcon", dim);
        m.put("chats_pinnedOverlay", AmberTokens.alpha(accent, 0.08f));
        m.put("chats_sentCheck", accent);
        m.put("chats_sentReadCheck", accentBright);
        m.put("chats_sentClock", dim);
        m.put("chats_sentError", red);
        m.put("chats_sentErrorIcon", red);
        m.put("chats_draft", accent);
        m.put("chats_mentionIcon", accent);
        m.put("chats_menuBackground", bg);
        m.put("chats_menuTopBackground", header);
        m.put("chats_menuTopBackgroundCats", header);
        m.put("chats_menuName", text);
        m.put("chats_menuPhone", dim);
        m.put("chats_menuPhoneCats", dim);
        m.put("chats_menuItemIcon", dim);
        m.put("chats_menuItemText", text);
        m.put("chats_menuItemCheck", accent);
        m.put("chats_menuTopShadow", 0x00000000);
        m.put("chats_menuTopShadowCats", 0x00000000);
        m.put("chats_tabletSelectedOverlay", sel);

        // ── صفحه چت: بوم و حباب‌ها ──────────────────────────────────────────
        // وایپرپ گرادیانی متحرک (MotionBackgroundDrawable): پایه + سه توقف؛
        // نام‌های عجیب chat_wallpaper_gradient_to / key_..._to2/to3 عمداً
        // همان قرارداد ThemeColors.createColorKeysMap تلگرام است.
        m.put("chat_wallpaper", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_WALLPAPER_MID) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_WALLPAPER_MID) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));
        m.put("chat_wallpaper_gradient_to", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_BOTTOM : AmberTokens.AURORA_NIGHT_WALLPAPER_TOP) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_BOTTOM : AmberTokens.PREMIERE_NIGHT_WALLPAPER_TOP) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_BOTTOM : AmberTokens.MARIO_NIGHT_WALLPAPER_TOP) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_BOTTOM : AmberTokens.HARMONY_NIGHT_WALLPAPER_TOP) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_BOTTOM : AmberTokens.SW_NIGHT_WALLPAPER_TOP) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_BOTTOM : AmberTokens.SLING_NIGHT_WALLPAPER_TOP) : (d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP));
        m.put("key_chat_wallpaper_gradient_to2", au ? (d ? AmberTokens.AURORA_DAY_BG : AmberTokens.AURORA_NIGHT_WALLPAPER_BOTTOM) : pr ? (d ? AmberTokens.PREMIERE_DAY_BG : AmberTokens.PREMIERE_NIGHT_WALLPAPER_BOTTOM) : ma ? (d ? AmberTokens.MARIO_DAY_BG : AmberTokens.MARIO_NIGHT_WALLPAPER_BOTTOM) : ha ? (d ? AmberTokens.HARMONY_DAY_BG : AmberTokens.HARMONY_NIGHT_WALLPAPER_BOTTOM) : sw ? (d ? AmberTokens.SW_DAY_BG : AmberTokens.SW_NIGHT_WALLPAPER_BOTTOM) : sl ? (d ? AmberTokens.SLING_DAY_BG : AmberTokens.SLING_NIGHT_WALLPAPER_BOTTOM) : (d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM));
        m.put("key_chat_wallpaper_gradient_to3", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_HEADER : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_HEADER : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_HEADER : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_HEADER : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE));
        // قدم ۱۹ — کلید پنجم وایپرپ (زاویه گرادیان دومرحله‌ای؛ مسیر موشن از آن استفاده نمی‌کند
        // ولی برای کامل بودن attheme و ثبات ادیتور تم صریح شد؛ پیش‌فرض آپستریم هم ۴۵ است)
        m.put("chat_wallpaper_gradient_rotation", 45);
        // قدم ۱۹ — پس‌زمینه صفحه چت در حالت کم‌حجم (compact/battery-saver): قبلاً از fallback
        // windowBackgroundWhite می‌آمد؛ حالا پایهٔ وایپرپ به‌صورت تخت = «کم‌حجم یعنی وایپرپ بدون گرادیان»
        m.put("chat_compact_background", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_WALLPAPER_MID) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_WALLPAPER_MID) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));
        // پردهٔ محو لبهٔ پایین: روز جوهر×۳٪ (گرم) / شب مشکی×۳٪ (مثل آپستریم)
        m.put("chat_compact_backgroundGradient", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : 0xFF000000) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : 0xFF000000) : sw ? (d ? AmberTokens.SW_DAY_TEXT : 0xFF000000) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000), 0.03f));
        // قرص اکشن روی بوم کم‌حجم (چیپ سرویس/نام استیکر/ریپلای): آپستریم ۵٪ مشکی بود که
        // روی بوم تیرهٔ شب عملاً نامرئی می‌شد ← روز جوهر×۶٪ / شب جوهر روشن×۱۰٪ (پیل تونال)
        m.put("chat_compact_actionBackground", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? AmberTokens.SW_DAY_TEXT : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.SLING_NIGHT_TEXT) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_TEXT), d ? 0.06f : 0.10f));
        // متن/آیکون قرص: آپستریم مشکی خالص (شب روی پیل تیره نامرئی!) ← جوهر/dim
        m.put("chat_compact_actionText", text);
        m.put("chat_compact_actionIcon", dim);
        // قدم ۲۵ — متن دکمه‌های بات روی قرص کم‌حجم: آپستریم مشکی خالص (شب روی پیل تیرهٔ جوهر روشن ۱۰٪ نامرئی) ← هم‌زبانهٔ compact_actionText
        m.put("chat_compact_botButtonText", text);
        // قدم ۲۷ — سایه/خط گلس کم‌حجم (پنل بالا + منوی اورلی در حالت کم‌حجم): سه کلید در پالت نبودند —
        // شب صریحاً صفر بود (خط مشکی روی گلس تیره نویز است) ولی روز اصلاً کلید نداشت و آپستریمِ
        // خنثی (Outline 14٪ / Shadow 8٪ / Hairline 5٪ مشکی) بی‌سند اعمال می‌شد؛ صریح‌سازی هر دو:
        // روز همان تینت‌های خنثی آپستریم (تعریف قرص تخت هدر روی کرم) / شب صفرِ سندشده
        m.put("chat_compact_glassOutline", d ? 0x24000000 : 0);
        m.put("chat_compact_glassShadow", d ? 0x14000000 : 0);
        m.put("chat_compact_glassHairline", d ? 0x0D000000 : 0);
        // قدم ۲۰ — زنجیرهٔ حباب ورودی در حالت کم‌حجم (میراث قدم ۱۹): ۵ کلید `chat_compact_in*`
        // آپستریم سرد بودند (خاکستری 0x80A1AAB3 / جوهر سرد 1A1D21) و مدت‌ها هیچ‌کدام در پالت نبودند؛
        // صدای هر کلید از منبع mapCompact همان کلید عادی کپی شد:
        m.put("chat_compact_inTimeText", time);
        // ساعت/بازدیدها: آپستریم نیمه‌شفاف سرد (روی کاغذ روز ~۱٫۴:۱) ← «زمان» حباب جامد
        // (بوم کم‌حجم تخت است؛ ترکیب OVER_BACKGROUND با رنگ جامد = هویت)
        m.put("chat_compact_inAudioDuration", dim);
        // مدت صدا: هم‌صدای chat_inAudioDurationText
        m.put("chat_compact_inWaveform", accent);
        // پر موج صدا: هم‌صدای chat_inVoiceSeekbarFill
        m.put("chat_compact_inWaveformBackground", AmberTokens.alpha(inText, d ? 0.30f : 0.35f));
        // بسترهٔ موج: آپستریم ۳۰٪ جوهر سرد (شب روی بوم تیره نامرئی بود) ← جوهر×۳۰٪ روز / ×۳۵٪ شب
        m.put("chat_compact_inTranscribeButton", accent);
        // دکمهٔ پیاده‌سازی صدا: آپستریم سرد جامد 1A1D21 بود؛ این کلید فقط برای دکمهٔ پیاده‌سازی
        // مصرف می‌شود ولی setColor آن رنگ را «رنگ اصلی دکمه» می‌گیرد (آیکون = خودِ رنگ، بستره = ×۱۵٫۶٪) —
        // پس اکسنت جامد (آیکون روی بوم کم‌حجم ۴٫۰۱/۹٫۱۲) نه نسخهٔ شفاف
        // قدم ۲۱ — زنجیرهٔ کم‌حجم حباب خروجی: ۱۲ کلید `chat_compact_out*` + ۴ کلید چیپ ری‌اکشن + آیکون دکمهٔ کناری
        // همگی آپستریم سرد بودند (خاکستری 808384 / جوهر سرد 1A1D21) و در پالت نبودند؛ صدای هر کلید از منبع
        // mapCompact همان کلید عادی کپی شد (میراث قدم ۱۹/۲۰):
        // بستر حباب خروجی کم‌حجم: آپستریم 0F000000 (۹٪ مشکی سرد) ← حباب خروجیِ هموار روی بوم تخت؛
        // روز outBubble×۸۵٪ = FFE1BF (جدایی از بوم ۱٫۱۷ ≈ جدایی آپستریم؛ از حباب ورودی ۱٫۰۶) / شب ×۵۵٪ = 3D2C06 (۱٫۲۰ از ورودی)
        m.put("chat_compact_outBackground", AmberTokens.over(outBubble, au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_WALLPAPER_MID) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_WALLPAPER_MID) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), d ? 0.85f : 0.55f));
        // ساعت/بازدیدهای خروجی: هم‌صدای chat_outTimeText (روی بستر کم‌حجم ۳٫۵۴/۷٫۳۲)
        m.put("chat_compact_outTimeText", outTime);
        // تیک ارسال: هم‌صدای chat_outSentCheck = اکسنت (۳٫۶۲/۶٫۶۴ روی بستر)
        m.put("chat_compact_outCheck", accent);
        // ریپلای خروجی: بسترهٔ تینت اکسنت×۱۰٪ + خط و متن هم‌صدای عادی (متن روی بستر+tint ~۱۳/۱۰)
        m.put("chat_compact_outReplyBackground", AmberTokens.alpha(accent, 0.10f));
        m.put("chat_compact_outReplyLine", accent);
        m.put("chat_compact_outReplyText", outText);
        // اکسنت خروجی (نام فوروارد/از طریق بات/سایت/منو/کوت/ادمین) و پرکننده (لودر/سیکبار صدا): اکسنت
        m.put("chat_compact_outAccent", accent);
        m.put("chat_compact_outAccentFill", accent);
        // آیکون روی پرکنندهٔ اکسنت (دایرهٔ پیشرفت فایل/تماس): onAccent — هم‌الگوی قدم ۱۵/۱۷ (۴٫۲۹/۷٫۲۳)
        m.put("chat_compact_outAccentIcon", onAccent);
        // متن ثانویهٔ خروجی (حجم فایل/مدت صدا): هم‌صدای outTime (۳٫۳۸/۷٫۳۲ — آپستریم 808384 حدود ۲٫۸ بود)
        m.put("chat_compact_outSecondaryText", outTime);
        // تراک سیکبار صوتی/فایل: جوهر×۲۲٪ روز / ×۲۰٪ شب روی بستر کم‌حجم؛ پر = اکسنت
        m.put("chat_compact_outAccentLight", AmberTokens.alpha(outText, d ? 0.22f : 0.20f));
        // بوردر جدول و جداکنندهٔ خروجی: جوهر×۲۵٪ روز / ×۳۰٪ شب (روی بستر ۱٫۶۵/۲٫۲۸)
        m.put("chat_compact_outAccentBorder", AmberTokens.alpha(outText, d ? 0.25f : 0.30f));
        // چیپ ری‌اکشن در حالت کم‌حجم (ورودی/خروجی مشترک؛ under = بستر حباب خودش): بسترهٔ اکسنت×۱۲٪ (متن ۳٫۴۷/۷٫۳۶)
        m.put("chat_compact_reactionBackground", AmberTokens.alpha(accent, 0.12f));
        m.put("chat_compact_reactionText", accent);
        // چیپ انتخاب‌شده = قرص اکسنت جامد + onAccent (۴٫۲۹/۷٫۲۳ — هم‌الگوی قدم ۱۵/۱۷/۲۰)
        m.put("chat_compact_reactionBackgroundSelected", accent);
        m.put("chat_compact_reactionTextSelected", onAccent);
        // آیکون دکمهٔ پیاده‌سازی صدا در کم‌حجم (blend به رنگ اصلی دکمه در ChatMessageAudio): اکسنت — هم‌صدای inTranscribeButton قدم ۲۰
        m.put("chat_compact_sideButtonIcon", accent);
        // قدم ۲۸ — کروم حالت کم‌حجم (فید لبه‌ها، اسپینر، متن پول‌داون/تاپیک/ریپلای): قبلاً روز کلید نداشت
        // و پیش‌فرض‌های سیاه/سفید بی‌سند آپستریم می‌گرفت؛ شب هم مقدارهای قدیمی (121213 نه رنگ بستر) بود ←
        // فید = رنگ بستر کم‌حجم (chat_compact_background قدم ۱۹) تا لبهٔ محتوا در خود بستر محو شود؛
        // محتوا = text/dim هم‌زبان حباب‌ها؛ خط گلس = روز خنثی آپستریم ۲۴٪ / شب صفر (قرارداد گلس قدم ۲۷)
        m.put("chat_compact_fadeEdge", au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_WALLPAPER_MID) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_WALLPAPER_MID) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID));
        m.put("chat_compact_fadeMiddle", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : ha ? (d ? AmberTokens.HARMONY_DAY_WALLPAPER_TOP : AmberTokens.HARMONY_NIGHT_WALLPAPER_MID) : sw ? (d ? AmberTokens.SW_DAY_WALLPAPER_TOP : AmberTokens.SW_NIGHT_WALLPAPER_MID) : sl ? (d ? AmberTokens.SLING_DAY_WALLPAPER_TOP : AmberTokens.SLING_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), 0.64f));
        m.put("chat_compact_progress", text);
        m.put("chat_compact_pullingDownText", text);
        m.put("chat_compact_topicEmptyText", text);
        m.put("chat_compact_topicSeparatorText", text);
        m.put("chat_compact_replyText", dim);
        m.put("chat_compact_inputGlassOutline", d ? 0x24000000 : 0x00000000);
        m.put("chat_compact_buttonGlassOutline", d ? 0x24000000 : 0x00000000);
        m.put("chat_inBubble", inBubble);
        m.put("chat_inBubbleSelected", selIn);
        m.put("chat_inBubbleSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_inBubbleShadow", 0x00000000);
        m.put("chat_inBubbleLocationPlaceholder", outline);
        m.put("chat_outBubble", outBubble);
        // گرد ۲۰ — گِرادیان متحرک حباب‌های خروجی: سه توقف هم‌رنگ (روشن/پایه/تیره) + انیمیشن
        // (هماهنگ با فایل‌های attheme تولیدشده در Tools)
        m.put("chat_outBubbleGradient", outBubble);
        m.put("chat_outBubbleGradient2", ColorUtils.blendARGB(outBubble, 0xFFFFFFFF, d ? 0.10f : 0.13f));
        m.put("chat_outBubbleGradient3", ColorUtils.blendARGB(outBubble, 0xFF000000, d ? 0.12f : 0.14f));
        m.put("chat_outBubbleGradientAnimated", 1);
        m.put("chat_outBubbleSelected", selOut);
        m.put("chat_outBubbleSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_outBubbleGradientSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_outBubbleShadow", 0x00000000);
        m.put("chat_outBubbleLocationPlaceholder", headerBorder);

        // ── متن حباب ورودی ──────────────────────────────────────────────────
        m.put("chat_messageTextIn", inText);
        m.put("chat_inTimeText", time);
        m.put("chat_inTimeSelectedText", dim);
        m.put("chat_inInstant", accent);
        m.put("chat_inInstantSelected", accent);
        m.put("chat_inReplyLine", accent);
        m.put("chat_inReplyNameText", accent);
        m.put("chat_inReplyMessageText", inText);
        m.put("chat_inReplyMediaMessageText", inText);
        m.put("chat_inReplyMediaMessageSelectedText", inText);
        m.put("chat_inForwardedNameText", accent);
        m.put("chat_inViaBotNameText", accent);
        m.put("chat_inSiteNameText", accent);
        m.put("chat_inPsaNameText", accent);
        m.put("chat_inPreviewLine", outline);
        m.put("chat_inPreviewInstantText", accent);
        m.put("chat_inLoader", accent);
        m.put("chat_inLoaderSelected", accent);
        m.put("chat_inLoaderPhoto", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_inMediaIcon", dim);
        m.put("chat_inMediaIconSelected", dim);
        m.put("chat_inMenu", dim);
        m.put("chat_inMenuSelected", dim);
        m.put("chat_inFileNameText", accent);
        m.put("chat_inFileInfoText", dim);
        m.put("chat_inFileInfoSelectedText", dim);
        m.put("chat_inFileProgress", accent);
        m.put("chat_inFileProgressSelected", accent);
        m.put("chat_inFileBackground", deepFile);
        m.put("chat_inFileBackgroundSelected", AmberTokens.over(accent, deepFile, d ? 0.10f : 0.12f));
        m.put("chat_inAudioTitleText", inText);
        m.put("chat_inAudioPerfomerText", accent);
        m.put("chat_inAudioPerfomerSelectedText", accent);
        m.put("chat_inAudioDurationText", dim);
        m.put("chat_inAudioDurationSelectedText", dim);
        m.put("chat_inAudioProgress", accent);
        m.put("chat_inAudioSelectedProgress", accent);
        m.put("chat_inAudioSeekbar", outline);
        m.put("chat_inAudioSeekbarFill", accent);
        m.put("chat_inAudioSeekbarSelected", accent);
        m.put("chat_inAudioCacheSeekbar", AmberTokens.alpha(inText, 0.12f));
        m.put("chat_inVoiceSeekbar", outline);
        m.put("chat_inVoiceSeekbarFill", accent);
        m.put("chat_inVoiceSeekbarSelected", accent);
        m.put("chat_inVenueInfoText", inText);
        m.put("chat_inVenueInfoSelectedText", inText);
        m.put("chat_inContactBackground", deepFile);
        m.put("chat_inContactNameText", inText);
        m.put("chat_inContactPhoneText", dim);
        m.put("chat_inContactPhoneSelectedText", dim);
        m.put("chat_inContactIcon", accent);
        m.put("chat_inLocationBackground", deepFile);
        m.put("chat_inLocationIcon", accent);
        m.put("chat_inTableBackground", au ? (d ? 0xFFF4F6FA : 0xFF212A38) : pr ? (d ? 0xFFFFF8E8 : 0xFF241C36) : ma ? (d ? 0xFFEFF5FF : 0xFF1A2344) : ha ? (d ? 0xFFEDEFFA : 0xFF313455) : sw ? (d ? 0xFFF3F0E2 : 0xFF1B2540) : sl ? (d ? 0xFFEAF4FE : 0xFF1A3850) : (d ? 0xFFFFFDF8 : 0xFF2E2618));
        m.put("chat_inTableBorder", outline);
        m.put("chat_inCodeBackground", au ? (d ? 0xFFF1F4F9 : 0xFF1B2430) : pr ? (d ? 0xFFFFF6E0 : 0xFF1E1730) : ma ? (d ? 0xFFE7F0FF : 0xFF161E3E) : ha ? (d ? 0xFFEDEFFA : 0xFF313455) : sw ? (d ? 0xFFF3F0E2 : 0xFF1B2540) : sl ? (d ? 0xFFEAF4FE : 0xFF1A3850) : (d ? 0xFFF7EFE4 : 0xFF211B12));
        m.put("chat_inArticleCodeBackground", au ? (d ? 0xFFF1F4F9 : 0xFF1B2430) : pr ? (d ? 0xFFFFF6E0 : 0xFF1E1730) : ma ? (d ? 0xFFE7F0FF : 0xFF161E3E) : ha ? (d ? 0xFFEDEFFA : 0xFF313455) : sw ? (d ? 0xFFF3F0E2 : 0xFF1B2540) : sl ? (d ? 0xFFEAF4FE : 0xFF1A3850) : (d ? 0xFFF7EFE4 : 0xFF211B12));
        m.put("chat_inArticleCodeScrollbar", AmberTokens.alpha(text, 0.25f));
        m.put("chat_inArticleCodeScrollbarBackground", outline);
        m.put("chat_inArticleDetailsArrow", dim);
        m.put("chat_inArticleDetailsLine", outline);
        m.put("chat_inPollCorrectAnswer", green);
        m.put("chat_inPollWrongAnswer", red);
        m.put("chat_inReactionButtonBackground", accent);
        // قدم ۲۰ — آپستریم جامد است (TELEGRAM_COLOR) و مصرف‌کننده‌ها خودشان آلفا می‌سازند:
        // چیپ ری‌اکشن غیرانتخاب‌شده ×۰٫۱۵۶، چیپ انتخاب‌شده جامد، transcribe آیکون جامد/بستره ×۰٫۱۵۶،
        // ReactionTabHolderView غیرانتخاب‌شده ۰x10 و TopicsSidePanel/TopicButton/SearchTagsList جامد یا آلفای خودشان —
        // مقدار قبلی (اکسنت×۱۰٪) همهٔ این‌ها را تقریباً نامرئی می‌کرد (چیپ ۱٫۶٪!)
        m.put("chat_inReactionButtonText", accent);
        // متن چیپ غیرانتخاب‌شده روی تینت اکسنت (هم‌صدای آپستریم TELEGRAM_COLOR_TEXT)
        m.put("chat_inReactionButtonTextSelected", onAccent);
        // قدم ۲۰ — متن روی چیپ انتخاب‌شدهٔ جامد اکسنت: آپستریم سفید؛ شب اکسنت روشن با سفید ۲٫۰۳:۱ ← onAccent (۴٫۲۹/۷٫۲۳)
        m.put("chat_inQuote", AmberTokens.alpha(inText, d ? 0.10f : 0.12f));
        m.put("chat_inViews", dim);
        m.put("chat_inViewsSelected", dim);
        m.put("chat_inSentClock", dim);
        m.put("chat_inSentClockSelected", dim);
        m.put("chat_inTextSelectionHighlight", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_inDownCall", accent);
        m.put("chat_inDivider", outline);
        // قدم ۲۸ — تماس سبز داخل حباب ورودی (ردیف تماس ازدست‌رفته): آپستریم 00C853 خارج‌ازتوکن ←
        // سبز معنایی پالت (هم‌صدای attachLocationBackground/پاسخ درست نظرسنجی) — ۴٫۳۰/۷٫۴۰ روی حباب
        m.put("chat_inGreenCall", green);
        // برچسب «مدیر» متن‌سطح ورودی: آپستریم فقط fallback به inTimeText داشت ← صریح‌سازی همان مقدار
        m.put("chat_inAdminText", time);
        m.put("chat_inAdminSelectedText", dim);

        // قدم ۲۸ — ریشه‌کنی دکمه‌های نامشخص: خانوادهٔ msgIvButton (دکمه‌های InstantView/اینلاین‌بات داخل
        // حباب). آپستریم روز چهار زبان ناهمگون بی‌سند داشت (خاکستری EDEDED / سبزفام DCF4CB / آبی 229AF0
        // / سبز 53AB49) و شب چیپ 17171A روی حباب 262017 فقط ۱٫۰۵:۱ بود (دکمهٔ نامرئی!) ← زبان یکپارچه:
        // Default = چیپ تُنال جوهر×۱۲٪ روی بستر حباب خودش (پرس ×۲۰٪) با متن پیام؛ Primary = قرص اکسنت +
        // onAccent (۴٫۲۹/۷٫۲۳ — هم‌الگوی قدم ۱۵/۱۷/۲۰)؛ Danger/Success = تینت ×۱۲٪/×۲۰٪ رنگ معنایی با متن هم‌رنگ
        m.put("chat_msgIvButtonDefaultIn", AmberTokens.over(inText, inBubble, 0.12f));
        m.put("chat_msgIvButtonDefaultInPressed", AmberTokens.over(inText, inBubble, 0.20f));
        m.put("chat_msgIvButtonDefaultInText", inText);
        m.put("chat_msgIvButtonDefaultInlineIn", AmberTokens.over(inText, inBubble, 0.12f));
        m.put("chat_msgIvButtonDefaultInlineInPressed", AmberTokens.over(inText, inBubble, 0.20f));
        m.put("chat_msgIvButtonDefaultInlineInText", inText);
        m.put("chat_msgIvButtonPrimaryIn", accent);
        m.put("chat_msgIvButtonPrimaryInPressed", AmberTokens.over(accent, onAccent, 0.20f));
        m.put("chat_msgIvButtonPrimaryInText", onAccent);
        m.put("chat_msgIvButtonDangerIn", AmberTokens.over(red, inBubble, 0.12f));
        m.put("chat_msgIvButtonDangerInPressed", AmberTokens.over(red, inBubble, 0.20f));
        m.put("chat_msgIvButtonDangerInText", red);
        m.put("chat_msgIvButtonSuccessIn", AmberTokens.over(green, inBubble, 0.12f));
        m.put("chat_msgIvButtonSuccessInPressed", AmberTokens.over(green, inBubble, 0.20f));
        m.put("chat_msgIvButtonSuccessInText", green);

        // ── متن حباب خروجی ──────────────────────────────────────────────────
        m.put("chat_messageTextOut", outText);
        m.put("chat_outTimeText", outTime);
        m.put("chat_outTimeSelectedText", outText);
        m.put("chat_outInstant", accent);
        m.put("chat_outInstantSelected", accent);
        m.put("chat_outReplyLine", accent);
        m.put("chat_outReplyLine2", accent);
        m.put("chat_outReplyNameText", accent);
        m.put("chat_outReplyMessageText", outText);
        m.put("chat_outReplyMediaMessageText", outText);
        m.put("chat_outReplyMediaMessageSelectedText", outText);
        m.put("chat_outForwardedNameText", accent);
        m.put("chat_outViaBotNameText", accent);
        m.put("chat_outSiteNameText", accent);
        m.put("chat_outPsaNameText", accent);
        m.put("chat_outPreviewLine", AmberTokens.alpha(outText, 0.40f));
        m.put("chat_outPreviewInstantText", accent);
        m.put("chat_outLoader", accent);
        m.put("chat_outLoaderSelected", accent);
        m.put("chat_outMediaIcon", outTime);
        m.put("chat_outMediaIconSelected", outTime);
        m.put("chat_outMenu", outTime);
        m.put("chat_outMenuSelected", outTime);
        m.put("chat_outFileNameText", accent);
        m.put("chat_outFileInfoText", outDim);
        m.put("chat_outFileInfoSelectedText", outDim);
        m.put("chat_outFileProgress", accent);
        m.put("chat_outFileProgressSelected", accent);
        m.put("chat_outFileBackground", au ? (d ? 0xFFBEEBDF : 0xFF17544A) : pr ? (d ? 0xFFE0B25A : 0xFFC7891B) : ma ? (d ? 0xFFF2C94C : 0xFF2E7D32) : ha ? (d ? 0xFF8F97F5 : 0xFF373C82) : sw ? (d ? 0xFFE88A94 : 0xFF6E1520) : sl ? (d ? 0xFFF2917F : 0xFF8C1E14) : (d ? 0xFFFBCE8F : 0xFF6E5200));
        m.put("chat_outFileBackgroundSelected", AmberTokens.over(accent, outBubble, d ? 0.08f : 0.10f));
        m.put("chat_outAudioTitleText", outText);
        m.put("chat_outAudioPerfomerText", accent);
        m.put("chat_outAudioPerfomerSelectedText", accent);
        m.put("chat_outAudioDurationText", outDim);
        m.put("chat_outAudioDurationSelectedText", outDim);
        m.put("chat_outAudioProgress", accent);
        m.put("chat_outAudioSelectedProgress", accent);
        m.put("chat_outAudioSeekbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outAudioSeekbarFill", accent);
        m.put("chat_outAudioSeekbarSelected", accent);
        // قدم ۲۸ — تماس سبز خروجی + خانوادهٔ msgIvButton سمت خروجی (هم‌زبانهٔ ورودی؛ چیپ روی بستر حباب خروجی)
        m.put("chat_outGreenCall", green);
        m.put("chat_msgIvButtonDefaultOut", AmberTokens.over(outText, outBubble, 0.12f));
        m.put("chat_msgIvButtonDefaultOutPressed", AmberTokens.over(outText, outBubble, 0.20f));
        m.put("chat_msgIvButtonDefaultOutText", outText);
        m.put("chat_msgIvButtonDefaultInlineOut", AmberTokens.over(outText, outBubble, 0.12f));
        m.put("chat_msgIvButtonDefaultInlineOutPressed", AmberTokens.over(outText, outBubble, 0.20f));
        m.put("chat_msgIvButtonDefaultInlineOutText", outText);
        m.put("chat_msgIvButtonPrimaryOut", accent);
        m.put("chat_msgIvButtonPrimaryOutPressed", AmberTokens.over(accent, onAccent, 0.20f));
        m.put("chat_msgIvButtonPrimaryOutText", onAccent);
        m.put("chat_msgIvButtonDangerOut", AmberTokens.over(red, outBubble, 0.12f));
        m.put("chat_msgIvButtonDangerOutPressed", AmberTokens.over(red, outBubble, 0.20f));
        m.put("chat_msgIvButtonDangerOutText", redOut);
        m.put("chat_msgIvButtonSuccessOut", AmberTokens.over(green, outBubble, 0.12f));
        m.put("chat_msgIvButtonSuccessOutPressed", AmberTokens.over(green, outBubble, 0.20f));
        m.put("chat_msgIvButtonSuccessOutText", green);
        m.put("chat_outAudioCacheSeekbar", AmberTokens.alpha(outText, 0.15f));
        m.put("chat_outVoiceSeekbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outVoiceSeekbarFill", accent);
        m.put("chat_outVoiceSeekbarSelected", accent);
        m.put("chat_outVenueInfoText", outText);
        m.put("chat_outVenueInfoSelectedText", outText);
        m.put("chat_outContactBackground", au ? (d ? 0xFFBEEBDF : 0xFF17544A) : pr ? (d ? 0xFFE0B25A : 0xFFC7891B) : ma ? (d ? 0xFFF2C94C : 0xFF2E7D32) : ha ? (d ? 0xFF8F97F5 : 0xFF373C82) : sw ? (d ? 0xFFE88A94 : 0xFF6E1520) : sl ? (d ? 0xFFF2917F : 0xFF8C1E14) : (d ? 0xFFFBCE8F : 0xFF6E5200));
        m.put("chat_outContactNameText", outText);
        m.put("chat_outContactPhoneText", outDim);
        m.put("chat_outContactPhoneSelectedText", outDim);
        m.put("chat_outContactIcon", accent);
        m.put("chat_outLocationIcon", accent);
        m.put("chat_outTableBackground", au ? (d ? 0xFFC4EFE4 : 0xFF17544A) : pr ? (d ? 0xFFEDC468 : 0xFFD0911F) : ma ? (d ? 0xFFF7D45E : 0xFF2E7D32) : ha ? (d ? 0xFF9AA1F7 : 0xFF393E8C) : sw ? (d ? 0xFFEA8F98 : 0xFF65141E) : sl ? (d ? 0xFFF39A88 : 0xFF872013) : (d ? 0xFFFBF1DD : 0xFF6E5200));
        m.put("chat_outTableBorder", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outCodeBackground", au ? (d ? 0xFFB8E9DC : 0xFF12463E) : pr ? (d ? 0xFFE8BE55 : 0xFFC28218) : ma ? (d ? 0xFFEFC63E : 0xFF29702C) : ha ? (d ? 0xFF7F87F0 : 0xFF31366F) : sw ? (d ? 0xFFE07780 : 0xFF5E111B) : sl ? (d ? 0xFFEE7A66 : 0xFF7A1A12) : (d ? 0xFFF6E3C2 : 0xFF524000));
        m.put("chat_outArticleCodeBackground", au ? (d ? 0xFFB8E9DC : 0xFF12463E) : pr ? (d ? 0xFFE8BE55 : 0xFFC28218) : ma ? (d ? 0xFFEFC63E : 0xFF29702C) : ha ? (d ? 0xFF7F87F0 : 0xFF31366F) : sw ? (d ? 0xFFE07780 : 0xFF5E111B) : sl ? (d ? 0xFFEE7A66 : 0xFF7A1A12) : (d ? 0xFFF6E3C2 : 0xFF524000));
        m.put("chat_outArticleCodeScrollbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outArticleCodeScrollbarBackground", AmberTokens.alpha(outText, 0.25f));
        m.put("chat_outArticleDetailsArrow", outDim);
        m.put("chat_outArticleDetailsLine", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outPollCorrectAnswer", au ? (d ? 0xFF0E8A6E : 0xFF8AD9BC) : pr ? (d ? 0xFF0C8A7E : 0xFF3FD2C7) : ma ? (d ? 0xFF27702F : 0xFF5FCE6A) : ha ? (d ? 0xFF27702F : 0xFF5FCE6A) : sw ? (d ? 0xFF27702F : 0xFF5FCE6A) : sl ? (d ? 0xFF5E8C36 : 0xFF7DBB42) : (d ? 0xFF3D7A2B : 0xFF9BC77E));
        m.put("chat_outPollWrongAnswer", d ? 0xFFB4382C : 0xFFFF8A75);
        // قدم ۲۱ — رفع هم‌الگوی قدم ۲۰ (سمت خروجی): بسترهٔ چیپ ری‌اکشن خروجی آپستریم «جامد» است (78c272 سبز) و
        // مصرف‌کننده‌ها خودشان آلفا می‌سازند (چیپ غیرانتخاب‌شده ×۰٫۱۵۶ در ReactionsLayoutInBubble، تاپیک آلفا۳۸ در
        // MessageTopicButton، blend رنگ اصلی transcribe در ChatMessageAudio، اوورلی ReactionsEffectOverlay) —
        // مقدار قبلی (اکسنت×۱۰٪) بعد از ضرب ۰٫۱۵۶ چیپ را ~۱٪ می‌کرد ← اکسنت جامد (هم‌الگوی chat_inReactionButtonBackground قدم ۲۰)
        m.put("chat_outReactionButtonBackground", accent);
        m.put("chat_outReactionButtonText", accent);
        // متن چیپ انتخاب‌شده روی قرص اکسنت جامد از اکسنت بود (روی اکسنت نامرئی!) ← onAccent (۴٫۲۹/۷٫۲۳)
        m.put("chat_outReactionButtonTextSelected", onAccent);
        // قدم ۲۴ — دو کلید سرویس ری‌اکشن (چیپ ری‌اکشن انتخاب‌شدهٔ روی چیپ سرویس/تاریخ — ChatActionCell) در پالت نبودند:
        // شب F97316 نارنجی خارج‌ازتوکن (بازماندهٔ مولد کهربایی قدیمی) و روز اصلاً کلید نداشت (پیش‌فرض سفید/مشکی آپستریم)
        // ← قرص اکسنت + onAccent (۴٫۲۹/۷٫۲۳ — هم‌الگوی چیپ انتخاب‌شدهٔ معمولی قدم ۲۰/۲۱)
        m.put("chat_reactionServiceButtonBackgroundSelected", accent);
        m.put("chat_reactionServiceButtonTextSelected", onAccent);
        m.put("chat_outQuote", AmberTokens.alpha(outText, 0.12f));
        m.put("chat_outViews", outDim);
        m.put("chat_outViewsSelected", outDim);
        m.put("chat_outSentCheck", accent);
        // قدم ۲۱ — روز از accentBright (روی حباب FFDDB8 فقط ۲٫۰۶:۱) به sentCheckRead؛ شب همان accentBright (۵٫۵۸)
        m.put("chat_outSentCheckRead", sentCheckRead);
        m.put("chat_outSentCheckSelected", accent);
        m.put("chat_outSentCheckReadSelected", sentCheckRead);
        m.put("chat_outSentClock", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outSentClockSelected", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outAdminText", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outAdminSelectedText", AmberTokens.alpha(outText, 0.60f));
        // قدم ۲۱ — لینک داخل حباب خروجی: آپستریم آبی 2678b6 خارج‌ازتوکن بود و اصلاً در پالت نبود ← اکسنت
        m.put("chat_messageLinkOut", accent);
        m.put("chat_outLinkSelectBackground", AmberTokens.alpha(accent, 0.25f));
        m.put("chat_outTextSelectionCursor", accent);
        m.put("chat_outTextSelectionHighlight", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_outUpCall", accent);
        m.put("chat_outDivider", outline);

        // ── قدم ۲۶ — خانوادهٔ انتخاب پیام (اکشن‌مود انتخاب) ─────────────────
        // بسترهٔ پیام انتخاب‌شده + هایلایت پرش به پیام: آپستریم آبی 0x280a90f0 خارج‌ازتوکن و کلید در
        // پالت نبود؛ در دستگاه‌های پرقدرت با والپیپر متحرک، applyChatMessageSelectedBackgroundColor
        // به‌جای کلید از «پچ گرادیانِ خود والپیپر» استفاده می‌کرد (هم‌الگوی باگ چیپ سرویس قدم ۲۵ —
        // ظاهر ناهمگون بین دستگاه‌ها). با تعریف صریح کلید در تم (بدون کلید emoticon، مسیر حذفِ
        // Theme.java فعال نمی‌شود) مسیر توکنی قطعی می‌رود ← تینت اکسنت ×۰٫۱۵۶ (هم‌زبانهٔ چیپ ری‌اکشن
        // غیرانتخاب‌شده)؛ متن روی بسترهٔ تینت‌خورده: روز ۱۲٫۰۵/۱۰٫۳۴، شب ۱۰٫۴۰/۵٫۷۲
        m.put("chat_selectedBackground", AmberTokens.alpha(accent, 0.156f));
        // برچسب «مدیر» زیر نام فرستنده (ChatMessageCell) — آپستریم روز خاکستری-آبی c0c6cb روی حباب
        // کرم فقط ۱٫۴۵:۱ (نامرئی‌وار) و 89b4c1 خارج‌ازتوکن ← dim (۴٫۲۹/۶٫۰۱ — هم‌زبانهٔ برچسب‌های
        // ثانویهٔ حباب)؛ حالت انتخاب‌شده هم‌رنگ می‌ماند (بازخورد حالت را تینت بستره می‌دهد)
        m.put("chat_adminText", dim);
        m.put("chat_adminSelectedText", dim);
        // نشان نقش creator/admin (لِی‌اوت امضای ادمین + تینت اسپن ریپلای) — آپستریم 955CDB بنفش /
        // 40A920 سبز خارج‌ازتوکن ← اکسنت (۳٫۶۲/۷٫۹۶ — هم‌زبانهٔ نام‌ها؛ تمایز نقش با خودِ متن نشان)
        m.put("chat_tagCreator", accent);
        m.put("chat_tagAdmin", accent);
        // اسکریم رادیال‌پروگرس روی مدیا در حال دانلود — مقادیر خنثی آپستریم (مشکی/سفید روی تصویر)
        // درست‌اند و مستقل از تم‌اند؛ صریح‌سازی برای رفت‌وبرگشت کامل و قطعیت
        m.put("chat_mediaLoaderPhoto", 0x66000000);
        m.put("chat_mediaLoaderPhotoIcon", 0xFFFFFFFF);
        m.put("chat_mediaLoaderPhotoSelected", 0x7F000000);
        m.put("chat_mediaLoaderPhotoIconSelected", 0xFFD9D9D9);
        // قدم ۲۸ — خانوادهٔ «رنگ روی مدیا» (تایم/ویوز/منو/پیشرفت/تیک و ساعت ارسال روی عکس/ویدیو):
        // آپستریم مشکی/سفید خنثی روی تصویر مستقل از تم است (هم‌الگوی mediaLoaderPhoto قدم ۲۶) ولی
        // کلیدها در پالت نبودند — روز به پیش‌فرض‌های بی‌سند می‌افتاد و شب mediaViews مقدار junk تیرهٔ
        // 1A1A1C داشت (خاکستری تیره روی اسکریم تیره = ناخوانا) ← صریح‌سازی سفید/اسکریم خنثی در هر دو حالت
        m.put("chat_mediaTimeText", 0xFFFFFFFF);
        m.put("chat_mediaTimeBackground", 0x66000000);
        m.put("chat_mediaViews", 0xFFFFFFFF);
        m.put("chat_mediaMenu", 0xFFFFFFFF);
        m.put("chat_mediaInfoText", 0xFFFFFFFF);
        m.put("chat_mediaProgress", 0xFFFFFFFF);
        m.put("chat_mediaSentCheck", 0xFFFFFFFF);
        m.put("chat_mediaSentClock", 0xB2FFFFFF);
        // مدت ویدیو و متن بازی پیش‌نمایش (روی بستر مدیا): سفید خنثی آپستریم
        m.put("chat_previewDurationText", 0xFFFFFFFF);
        m.put("chat_previewGameText", 0xFFFFFFFF);
        // نوار «ذخیرهٔ GIF» (اسکریم تیره + متن سفید — خنثی روی تصویر؛ روز قبلاً آبی‌فام E21F2B38 داشت)
        m.put("chat_gifSaveHintBackground", 0x82141416);
        m.put("chat_gifSaveHintText", 0xFFFFFFFF);
        // سطوح آلفای بلور روکش چت (خنثی؛ مستقل از تم — روز کلید نداشت)
        m.put("chat_BlurAlpha", 0xB2000000);
        m.put("chat_BlurAlphaSlow", 0xCC000000);
        // قدم ۲۸ — بج خطای ارسال: مربع‌گرد painted با chat_sentError + علامت تعجب tinted با
        // chat_sentErrorIcon. روز FF0000 خام خارج‌ازتوکن بود ← قرمز معنایی پالت B4382C (۴٫۶۰ روی حباب
        // خروجی، تعجب سفید ۵٫۹۳ روی بج)؛ شب هر دو قرمز هم‌خانواده بودند (تعجب E5646C روی بج F6574E فقط
        // ۱٫۰۸:۱ = نامرئی!) ← تعجب سفید شد؛ بج هم F6574E → FF5D50 شد تا هم شکل بج روی حباب ۳٫۱۸ و
        // هم تعجب سفید روی بج ۳٫۰۳ (هر دو ≥۳٫۰ — پنجرهٔ باریک بین دو قید)
        m.put("chat_sentError", d ? 0xFFB4382C : 0xFFFF5D50);
        m.put("chat_sentErrorIcon", 0xFFFFFFFF);
        // قفل هدر (گفت‌وگوی پنهان/بات تأییدشده): آپستریم 222222 و سفیدِ بی‌ربط به هدر ← dim هم‌زبان
        // سایر آیکون‌های هدر (actionBarDefaultIcon قدم ۱۱)
        m.put("chat_lockIcon", dim);
        // دکمهٔ «افزودن مخاطب» (چیپ متن + تینت ×۱۰٪) و دکمهٔ ویرایش مدیا روی تصویر: روز آبی 308ED0/1A9CFF
        // خارج‌ازتوکن ← اکسنت (هم‌زبانهٔ چیپ ری‌اکشن و لینک‌ها)
        m.put("chat_addContact", accent);
        m.put("chat_editMediaButton", accent);
        // لینک داخل حباب ورودی: روز آبی 127ACA خارج‌ازتوکن ← اکسنت هم‌زبان messageLinkOut قدم ۲۱
        m.put("chat_messageLinkIn", accent);

        // ── اشتراکی صفحه چت ─────────────────────────────────────────────────
        m.put("chat_linkSelectBackground", AmberTokens.alpha(accent, 0.25f));
        m.put("chat_textSelectBackground", AmberTokens.alpha(accent, 0.35f));
        m.put("chat_serviceText", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));
        m.put("chat_serviceBackground", svcBg);
        m.put("chat_serviceBackgroundSelected", svcBgSel);
        m.put("chat_serviceBackgroundSelector", svcSel);
        m.put("chat_serviceIcon", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));
        m.put("chat_serviceLink", au ? (d ? 0xFFDCF7F0 : 0xFFDCFFF4) : pr ? (d ? 0xFFFFF1CC : 0xFFFFF6DC) : ma ? (d ? 0xFFFFE9A8 : 0xFFFFF3B8) : ha ? (d ? 0xFFDDE1FF : 0xFFE0E4FF) : sw ? (d ? 0xFFFFE1E6 : 0xFFFFE7EA) : sl ? (d ? 0xFFFFE9A8 : 0xFFFFF3B8) : (d ? 0xFFFFEFC9 : 0xFFFFDDB8));
        m.put("chat_goDownButton", goDown);
        m.put("chat_goDownButtonCounter", badgeText);
        m.put("chat_goDownButtonCounterBackground", accent);
        m.put("chat_status", dim);
        m.put("chat_topPanelBackground", header);
        m.put("chat_topPanelTitle", text);
        m.put("chat_topPanelMessage", dim);
        m.put("chat_topPanelLine", divider);
        m.put("chat_topPanelClose", dim);
        m.put("chat_fieldOverlayText", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));
        m.put("chat_muteIcon", dim);
        m.put("chat_unreadMessagesStartBackground", header);
        m.put("chat_unreadMessagesStartText", accent);
        m.put("chat_unreadMessagesStartArrowIcon", accent);
        m.put("chat_searchPanelText", dim);
        m.put("chat_searchPanelIcons", dim);
        m.put("chat_stickersHintPanel", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? 0xFFFFF6E4 : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? 0xFFEFF2FD : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? 0xFFF6F3E7 : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? 0xFFEDF7FF : AmberTokens.SLING_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));
        // قدم ۲۵ — متن دکمه‌های بات روی چیپ سرویس تیره: اکسنت (روز ۱٫۳۷:۱ نامرئی!) ← هم‌زبانهٔ serviceText (۵٫۸۸/۱۵٫۱)
        m.put("chat_botButtonText", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT));
        m.put("chat_botKeyboardButtonBackground", accent);
        m.put("chat_botKeyboardButtonBackgroundPressed", accentBright);
        m.put("chat_botKeyboardButtonText", onAccent);
        m.put("chat_botSwitchToInlineText", accent);
        m.put("chat_replyPanelClose", dim);
        m.put("chat_replyPanelIcons", dim);
        m.put("chat_replyPanelLine", divider);
        m.put("chat_replyPanelName", accent);
        m.put("chat_recordTime", dim);
        // قدم ۲۲ — باگ واقعی: تایمر ضبط و فلش «لغو» روی پیل صدای کرم (header FFE9CF) سفید بود = نامرئی (۱٫۱۴:۱)!
        // آپستریم خاکستری 8e959b روی آبی خودش هم ~۲٫۰ بود ← dim گرم (روی کرم ۴٫۹۴ روز / روی پیل شب ۵٫۶۱)
        m.put("chat_recordVoiceCancel", dim);
        // قدم ۲۲ — پیل صدای ضبط‌شده: قبلاً FFEFC9/332717 خارج‌ازتوکن ← توکن هدر (FFE9CF) و بوردر هدر شب (332818)
        m.put("chat_recordedVoiceBackground", au ? (d ? AmberTokens.AURORA_DAY_HEADER : AmberTokens.AURORA_NIGHT_HEADER_BORDER) : pr ? (d ? AmberTokens.PREMIERE_DAY_HEADER : AmberTokens.PREMIERE_NIGHT_HEADER_BORDER) : ma ? (d ? AmberTokens.MARIO_DAY_HEADER : AmberTokens.MARIO_NIGHT_HEADER_BORDER) : ha ? (d ? AmberTokens.HARMONY_DAY_HEADER : AmberTokens.HARMONY_NIGHT_HEADER_BORDER) : sw ? (d ? AmberTokens.SW_DAY_HEADER : AmberTokens.SW_NIGHT_HEADER_BORDER) : sl ? (d ? AmberTokens.SLING_DAY_HEADER : AmberTokens.SLING_NIGHT_HEADER_BORDER) : (d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_HEADER_BORDER));
        m.put("chat_recordedVoiceDarkerBackground", headerBorder);
        // قدم ۲۳ — نقطهٔ ضبط صوتی: آپستریم قرمز da564d (معنای «در حال ضبط») ولی اکسنت کهربایی بود ← قرمز پالت
        // (روز B4382C روی فیلد سفید ۶٫۵ / شب E2695B روی پیل ۳٫۱ — لایه‌های Cup Red/Box Red لوتّی و بج تقویم)
        m.put("chat_recordedVoiceDot", red);
        m.put("chat_recordedVoicePlayPause", accent);
        m.put("chat_recordedVoiceProgress", accent);
        // قدم ۲۳ — موج پخش‌نشده/دستگیره/مدتِ پیل ضبط‌شده: آپستریم سفید روی آبی بود؛ پیل ما کرم است و روز
        // سفید روی کرم = نامرئی (۱٫۱۸:۱!) ← جوهر روز (۱۲٫۶+) / شب متن روشن (۱۲٫۵۹)
        m.put("chat_recordedVoiceProgressInner", au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.MARIO_NIGHT_TEXT) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.HARMONY_NIGHT_TEXT) : sw ? (d ? AmberTokens.SW_DAY_TEXT : AmberTokens.SW_NIGHT_TEXT) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.SLING_NIGHT_TEXT) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_TEXT));
        m.put("chat_secretTimeText", dim);
        m.put("chat_secretChatStatusText", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chat_stickerNameText", accent);
        m.put("chat_stickerReplyLine", accent);
        m.put("chat_stickerReplyMessageText", text);
        m.put("chat_stickerReplyNameText", accent);
        m.put("chat_stickerViaBotNameText", accent);
        m.put("chat_inlineResultIcon", dim);

        // ── پنل پیام ── قدم ۲۲ — شیت پایین = فیلد سفید: قبلاً FFEFC9 خارج‌ازتوکن (روز) و هدر (شب) بود ←
        // توکن fieldBg (روز FFFFFF — هم‌زبانهٔ کارت دیالوگ‌ها و فیلد جستجو؛ شب 241D14 = سطح فیلد، یک پله بالاتر از وایپرپ)
        m.put("chat_messagePanelBackground", fieldBg);
        // قدم ۲۲ — مرز بالای شیت: قبلاً صفر = کاملاً بی‌مرز بود؛ این کلید گرادیان مویی بالای پنل را رنگ می‌کند
        // (MULTIPLY روی compose_panel_shadow) — روز جوهر گرم (ترکیب روی کاغذ ≈ ECE3D7 = خانوادهٔ مرز E9DFD0 نقشه‌راه)
        // / شب مشکی آپستریم (روی بوم تیره نامحسوس؛ جدایی از پلهٔ روشن‌تر فیلد می‌آید)
        m.put("chat_messagePanelShadow", au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : 0xFF000000) : ha ? (d ? AmberTokens.HARMONY_DAY_TEXT : 0xFF000000) : sw ? (d ? AmberTokens.SW_DAY_TEXT : 0xFF000000) : sl ? (d ? AmberTokens.SLING_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000));
        m.put("chat_messagePanelText", text);
        m.put("chat_messagePanelHint", dim);
        m.put("chat_messagePanelCursor", accent);
        m.put("chat_messagePanelIcons", accent);
        m.put("chat_messagePanelSend", accent);
        m.put("chat_messagePanelCancelInlineBot", dim);
        m.put("chat_messagePanelVoiceBackground", header);
        m.put("chat_messagePanelVoiceDelete", dim);
        m.put("chat_messagePanelVoiceDuration", text);
        // قدم ۲۳ — آپستریم این کلید «سفید» است و همهٔ مصرف‌کننده‌هایش معنای آیکون دارند نه بستره:
        // تینت MULTIPLY حالت پرس میک/ویدیو/ارسال، menuPaint در SenderSelectView، چک‌مارک کپشن (با ریاضی آلفا)،
        // آیکون معکوس دکمهٔ ارسال (که جدا به onAccent رفت) — مقدار قبلی (جوهر×۸٪) همه را تقریباً نامرئی می‌کرد ← جوهر جامد
        m.put("chat_messagePanelVoicePressed", text);
        // قدم ۲۲ — قفل ضبط صوتی (حباب شناور لبهٔ صفحه؛ نام کلید در attheme طبق قرارداد عجیب آپستریم با پیشوند key_ است):
        // آیکون آپستریم A4A4A4 سرد ← dim گرم؛ بسترهٔ آپستریم سفید (قبلاً اکسنت!) ← fieldBg هم‌زبانهٔ فیلد
        // (DarkThemeResourceProvider اورراید خودش را دارد)؛ سایهٔ صفر ← مشکی آپستریم
        m.put("key_chat_messagePanelVoiceLock", dim);
        m.put("key_chat_messagePanelVoiceLockBackground", fieldBg);
        m.put("key_chat_messagePanelVoiceLockShadow", 0xFF000000);

        // ── پنل پیوست ───────────────────────────────────────────────────────
        m.put("chat_attachAudioBackground", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : pr ? (d ? 0xFFC42B4B : 0xFFE8445E) : ma ? (d ? 0xFFC6281C : 0xFFE85B50) : ha ? (d ? 0xFFC93D93 : 0xFFEB459E) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFE8443A) : (d ? 0xFFB4382C : 0xFFE2695B));
        m.put("chat_attachContactBackground", au ? (d ? 0xFFB3651F : 0xFFFFB454) : pr ? (d ? 0xFF8A5E0C : 0xFFC77E14) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : (d ? 0xFF8C6A1D : 0xFFC79A3E));
        // قدم ۲۲ — متن دکمهٔ مخاطب (کلید مرده در این فورک ولی برای کامل بودن attheme): آپستریم DFA000 طلایی ← «زمان»
        m.put("chat_attachContactText", time);
        m.put("chat_attachGalleryBackground", accent);
        m.put("chat_attachPhotoBackground", accentBright);
        m.put("chat_attachLocationBackground", green);
        m.put("chat_attachPollBackground", dim);
        m.put("chat_attachIcon", dim);
        m.put("chat_attachActiveTab", accent);
        m.put("chat_attachUnactiveTab", dim);
        m.put("chat_attachCheckBoxBackground", accent);
        m.put("chat_attachCheckBoxCheck", onAccent);
        m.put("chat_attachEmptyImage", dim);
        m.put("chat_attachPermissionImage", dim);
        m.put("chat_attachPermissionMark", dim);
        m.put("chat_attachPermissionText", dim);

        // ── پنل ایموجی ──────────────────────────────────────────────────────
        m.put("chat_emojiPanelBackground", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? 0xFFFFF6E4 : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? 0xFFEFF2FD : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? 0xFFF6F3E7 : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? 0xFFEDF7FF : AmberTokens.SLING_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));
        m.put("chat_emojiPanelIcon", dim);
        m.put("chat_emojiPanelIconSelected", accent);
        m.put("chat_emojiPanelBackspace", dim);
        m.put("chat_emojiPanelShadowLine", d ? 0x1E000000 : 0x33000000);
        m.put("chat_emojiPanelStickerPackSelector", au ? (d ? 0xFFF1F4F9 : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? 0xFFFFF6E4 : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? 0xFFEFF2FD : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? 0xFFF6F3E7 : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? 0xFFEDF7FF : AmberTokens.SLING_NIGHT_SURFACE) : (d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE));
        m.put("chat_emojiPanelStickerPackSelectorLine", accent);
        m.put("chat_emojiSearchBackground", fieldBg);
        m.put("chat_emojiSearchIcon", dim);
        // قدم ۲۸ — تکمیل خانوادهٔ ایموجی (تب‌های پنل پایین، نام/آیکون پک استیکر، متن خالی، ترندینگ):
        // روز کلید نداشتند (خاکستری-آبی سرد بی‌سند؛ آیکون پک b1b6bc روی پنل کرم فقط ۱٫۷:۱!) و شب
        // خاکستری 9C9CA1 بی‌سند؛ NewTrending روز آبی 3FA4F0 بود ← همه با dim/accent/text هم‌زبان پنل
        m.put("chat_emojiBottomPanelIcon", dim);
        m.put("chat_emojiPanelEmptyText", dim);
        m.put("chat_emojiPanelTrendingTitle", text);
        m.put("chat_emojiPanelTrendingDescription", dim);
        m.put("chat_emojiPanelNewTrending", accent);
        m.put("chat_emojiPanelStickerSetName", dim);
        m.put("chat_emojiPanelStickerSetNameHighlight", accent);
        m.put("chat_emojiPanelStickerSetNameIcon", dim);

        // ── دیالوگ‌ها ────────────────────────────────────────────────────────
        m.put("dialogBackground", fieldBg);
        m.put("dialogBackgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_BG) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_BG) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));
        m.put("dialogTextBlack", text);
        m.put("dialogTextGray", dim);
        m.put("dialogTextGray2", dim);
        m.put("dialogTextGray3", time);
        m.put("dialogTextGray4", time);
        m.put("dialogTextHint", time);
        m.put("dialogTextBlue", accent);
        m.put("dialogTextBlue2", accent);
        m.put("dialogTextBlue4", accent);
        m.put("dialogTextLink", accent);
        m.put("dialogLinkSelection", AmberTokens.alpha(accent, 0.25f));
        m.put("dialogInputField", fieldBorder);
        m.put("dialogInputFieldActivated", accent);
        m.put("dialogButton", accent);
        m.put("dialogButtonSelector", AmberTokens.alpha(accent, 0.10f));
        // قدم ۲۹ — دو کلید شیت هدیه (GiftSheet) در پالت نبودند: روز پیش‌فرض سرد بی‌سند F5F6F7/56595C آپستریم
        // می‌گرفت و شب fallback به windowBackgroundGray = بسترهٔ وایپرپ (۱۷۱۳۰E) می‌شد — سطح شیت
        // پایین‌تر از پلهٔ M3 (شیت روشن‌تر از بستر است، نه تیره‌تر!) ← سطح دیالوگ (fieldBg):
        // روز FFFFFF (هم‌زبانهٔ پیش‌فرض BottomSheet که خودش key_dialogBackground است) /
        // شب 241D14 یک پله بالاتر از وایپرپ؛ متن تب = dim (روی سطح دیالوگ ۵٫۰۹/۶٫۲۰ ≥ ۴٫۵)
        m.put("dialogGiftsBackground", fieldBg);
        m.put("dialogGiftsTabText", dim);
        m.put("dialogIcon", dim);
        m.put("dialogGrayLine", divider);
        m.put("dialogTopBackground", surface);
        m.put("dialogScrollGlow", AmberTokens.alpha(accent, 0.30f));
        m.put("dialogRoundCheckBox", accent);
        m.put("dialogRoundCheckBoxCheck", onAccent);
        // قدم ۳۱ — حلقهٔ رادیو دیالوگ: outline روز روی کاغذ ۱٫۲۵:۱ و شب روی وایپرپ ۱٫۳۱:۱ بود
        // (حلقهٔ نامرئی — آپستریم b3b3b3 خاکستری میانی ~۲٫۱ داشت) ← dim هم‌زبانهٔ
        // dialogCheckboxSquareUnchecked (روز ۴٫۸۴ / شب ۶٫۶۳ — زبان M3: مرز غیرفعال = onSurfaceVariant)
        m.put("dialogRadioBackground", dim);
        m.put("dialogRadioBackgroundChecked", accent);
        m.put("dialogCheckboxSquareBackground", accent);
        m.put("dialogCheckboxSquareCheck", onAccent);
        m.put("dialogCheckboxSquareUnchecked", dim);
        // قدم ۳۱ — outline ← dim (تیک onAccent نامرئی را می‌ساخت)؛ کامنت باید بالای خط باشد —
        // مولد فقط m.putهای تمام‌شده با ");" را ارزیابی می‌کند
        m.put("dialogCheckboxSquareDisabled", dim);
        m.put("dialogLineProgress", accent);
        m.put("dialogLineProgressBackground", outline);
        m.put("dialogSearchBackground", fieldBg);
        m.put("dialogSearchHint", time);
        m.put("dialogSearchIcon", dim);
        m.put("dialogSearchText", text);
        m.put("dialogFloatingButton", accent);
        m.put("dialogFloatingButtonPressed", accentBright);
        m.put("dialogFloatingIcon", onAccent);
        m.put("dialogEmptyText", dim);
        m.put("dialogEmptyImage", dim);
        m.put("dialogShadowLine", 0x00000000);
        m.put("dialogCardShadow", 0x00000000);
        m.put("dialogSwipeRemove", surface);
        m.put("dialogReactionMentionBackground", AmberTokens.alpha(accent, 0.12f));
        m.put("dialog_inlineProgress", accent);
        m.put("dialog_inlineProgressBackground", outline);
        m.put("dialog_liveLocationProgress", accent);

        // ── کنترل‌ها: سوییچ/چک‌باکس/رادیو (ممیزی کامل قدم ۳۱) ────────────────
        // زبان M3: ریل غیرفعال = سطح بلندتر از بستر (ظریف)، ریل فعال = اکسنت،
        // انگشت خاموش = روشن (روز سفید هم‌زبانهٔ M3-light؛ شب dim هم‌زبانهٔ هندل خاکستری M3-dark)،
        // انگشت روشن = onAccent، مرز غیرفعال چک‌باکس/رادیو = onSurfaceVariant (dim).
        m.put("switchTrack", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : pr ? (d ? 0xFFE7DBBE : AmberTokens.PREMIERE_NIGHT_OUTLINE) : ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE) : ha ? (d ? 0xFFD8DAF0 : AmberTokens.HARMONY_NIGHT_OUTLINE) : sw ? (d ? 0xFFE0D9BF : AmberTokens.SW_NIGHT_OUTLINE) : sl ? (d ? 0xFFD8E8F2 : AmberTokens.SLING_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));
        m.put("switchTrackChecked", accent);
        m.put("switchTrackBlue", au ? (d ? 0xFFDCE0EA : AmberTokens.AURORA_NIGHT_OUTLINE) : pr ? (d ? 0xFFE7DBBE : AmberTokens.PREMIERE_NIGHT_OUTLINE) : ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE) : ha ? (d ? 0xFFD8DAF0 : AmberTokens.HARMONY_NIGHT_OUTLINE) : sw ? (d ? 0xFFE0D9BF : AmberTokens.SW_NIGHT_OUTLINE) : sl ? (d ? 0xFFD8E8F2 : AmberTokens.SLING_NIGHT_OUTLINE) : (d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE));
        m.put("switchTrackBlueChecked", accent);
        m.put("switchTrackBlueSelector", AmberTokens.alpha(accent, 0.12f));
        m.put("switchTrackBlueSelectorChecked", AmberTokens.alpha(accent, 0.12f));
        // قدم ۳۱ — انگشت سوییچ خاموش: قبلاً onAccent بود (شب 3A2400 تیره روی ریل تیرهٔ NIGHT_OUTLINE
        // فقط ~۱٫۰:۱ = انگشت نامرئی در همهٔ سوییچ‌های خانوادهٔ Blue) و روز سفید مطلوب M3-light بود.
        // ← روز FFF8F1 هم‌زبانهٔ windowBackgroundWhite (سفید M3-light، روی ریل DCCFB8 ۱٫۴۶:۱
        // — با ضخامت انگشت ۲۰dp و جابه‌جایی مکانی قابل‌تشخیص، هم‌الگوی آپستریم a6adb3/سفید)،
        // شب dim = هندل روشن M3-dark (روی ریل 382C1C: ۵٫۰۶:۱). مصرف‌کننده‌ها: ۸ سایت خانوادهٔ Blue
        // + از این قدم TextCheckCell/NotificationsCheckCell هم انگشت‌شان از این جفت می‌آید.
        m.put("switchTrackBlueThumb", au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT_DIM) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT_DIM) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT_DIM) : ha ? (d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT_DIM) : sw ? (d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT_DIM) : sl ? (d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT_DIM) : (d ? 0xFFFFF8F1 : AmberTokens.NIGHT_TEXT_DIM));
        m.put("switchTrackBlueThumbChecked", onAccent);
        m.put("checkbox", accent);
        m.put("checkboxCheck", onAccent);
        // قدم ۳۱ — چک‌باکس گرد غیرفعال (CheckBoxBase/GroupCreateCheckBox): DCCFB8/شب NIGHT_OUTLINE
        // با تیک onAccent نامرئی بود (روز سفید روی DCCFB8 ۱٫۴۶:۱، شب 3A2400 روی 382C1C ~۱٫۰:۱)
        // ← dim (تیک onAccent روی آن: روز ۴٫۸۴ / شب ۵٫۰۶ — آپستریم b0b9c2 خاکستری میانی)
        m.put("checkboxDisabled", dim);
        m.put("checkboxSquareBackground", accent);
        m.put("checkboxSquareCheck", onAccent);
        m.put("checkboxSquareUnchecked", dim);
        // قدم ۳۱ — چک‌باکس مربعی غیرفعال: outline با تیک onAccent نامرئی (روز ۱٫۲۵ / شب ~۱٫۰) ← dim
        m.put("checkboxSquareDisabled", dim);
        // قدم ۳۱ — حلقهٔ رادیو غیرفعال: outline حلقهٔ نامرئی می‌ساخت (روز E9DFD0 روی کاغذ ۱٫۲۵:۱،
        // شب 382C1C روی وایپرپ ۱٫۳۱:۱ — آپستریم b3b3b3 ~۲٫۱) ← dim هم‌زبانهٔ checkboxSquareUnchecked
        m.put("radioBackground", dim);
        m.put("radioBackgroundChecked", accent);

        // ── پروفایل ─────────────────────────────────────────────────────────
        m.put("profile_title", text);
        m.put("profile_status", accent);
        m.put("profile_tabText", dim);
        m.put("profile_tabSelectedText", accent);
        m.put("profile_tabSelectedLine", accent);
        m.put("profile_tabSelector", AmberTokens.alpha(accent, 0.10f));
        m.put("profile_actionBackground", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));
        m.put("profile_actionIcon", accent);
        m.put("profile_actionPressedBackground", AmberTokens.alpha(text, 0.08f));
        m.put("profile_creatorIcon", accent);
        m.put("profile_verifiedBackground", accent);
        m.put("profile_verifiedCheck", onAccent);

        // ── آواتارها: ۸ رنگ + توقف دوم گرادیان (هویت گرم) ───────────────────
        // آئورورا: جفت‌های روبانی (فیروزه/ارغوانی/کهربا/بنفش/نقره‌ای/مرجانی)؛ کهربا: جفت‌های گرم
        m.put("avatar_backgroundBlue", au ? (d ? 0xFF98F2DE : 0xFF2DE4C4) : pr ? (d ? 0xFFFFD37A : 0xFFF0B449) : ma ? (d ? 0xFF6FA8FF : 0xFF4066D8) : ha ? (d ? 0xFF9FA7F8 : 0xFF5865F2) : sw ? (d ? 0xFF8FB8E8 : 0xFF3E8EDE) : sl ? (d ? 0xFF6FB9EC : 0xFF5FB0E8) : (d ? 0xFFFFB25E : 0xFFB45309));
        m.put("avatar_background2Blue", au ? (d ? 0xFF0F9B80 : 0xFF0E8A78) : pr ? (d ? 0xFFB96A0B : 0xFF8A5606) : ma ? (d ? 0xFF2E5BC4 : 0xFF2547A0) : ha ? (d ? 0xFF4453D6 : 0xFF3540B8) : sw ? (d ? 0xFF2E77C4 : 0xFF255FA0) : sl ? (d ? 0xFF2E77C4 : 0xFF255FA0) : (d ? 0xFFE8871E : 0xFF8A3E06));
        m.put("avatar_backgroundCyan", au ? (d ? 0xFF0F9B80 : 0xFF0E8A78) : pr ? (d ? 0xFF7FE6D8 : 0xFF3FD2C7) : ma ? (d ? 0xFF7FD9E8 : 0xFF2FA0B8) : ha ? (d ? 0xFFBFC4FA : 0xFF7983F5) : sw ? (d ? 0xFF8FD8E8 : 0xFF2FA0B8) : sl ? (d ? 0xFF7FD9E8 : 0xFF2FA0B8) : (d ? 0xFFDD8A5B : 0xFF9E4632));
        m.put("avatar_background2Cyan", au ? (d ? 0xFF98F2DE : 0xFF2DE4C4) : pr ? (d ? 0xFF0F8A7E : 0xFF1B7F76) : ma ? (d ? 0xFF1782A0 : 0xFF126E88) : ha ? (d ? 0xFF5C63D8 : 0xFF3A3F9E) : sw ? (d ? 0xFF1782A0 : 0xFF126E88) : sl ? (d ? 0xFF1782A0 : 0xFF126E88) : (d ? 0xFFB4382C : 0xFF6E2A1E));
        m.put("avatar_backgroundGreen", au ? (d ? 0xFFB9AFF2 : 0xFF8B7CF6) : pr ? (d ? 0xFFD3BDF2 : 0xFFA86BE0) : ma ? (d ? 0xFF5FCE6A : 0xFF2E9E3E) : ha ? (d ? 0xFF6DBE7F : 0xFF3BA55D) : sw ? (d ? 0xFF6EA858 : 0xFF3BDA7C) : sl ? (d ? 0xFFA4E05B : 0xFF7DBB42) : (d ? 0xFFC2A25E : 0xFF8C6A1D));
        m.put("avatar_background2Green", au ? (d ? 0xFF6A5CC4 : 0xFF4A3E8C) : pr ? (d ? 0xFF5C2E8C : 0xFF3F2064) : ma ? (d ? 0xFF27702F : 0xFF1D5A28) : ha ? (d ? 0xFF2E8C4A : 0xFF256B3A) : sw ? (d ? 0xFF4E7E3A : 0xFF2E6E58) : sl ? (d ? 0xFF5E8C36 : 0xFF4A7028) : (d ? 0xFF8C6A1D : 0xFF5E470F));
        m.put("avatar_backgroundOrange", au ? (d ? 0xFFFFD08A : 0xFFFFB454) : pr ? (d ? 0xFFF4A0AE : 0xFFE8445E) : ma ? (d ? 0xFFFFA94D : 0xFFE86A1C) : ha ? (d ? 0xFFFFC061 : 0xFFFAA61A) : sw ? (d ? 0xFFFFB454 : 0xFFF2A93B) : sl ? (d ? 0xFFFFB03A : 0xFFF2913C) : (d ? 0xFFF0C08A : 0xFFB06428));
        m.put("avatar_background2Orange", au ? (d ? 0xFFC97A26 : 0xFFB3651F) : pr ? (d ? 0xFF8C1F35 : 0xFF6E1224) : ma ? (d ? 0xFFC25414 : 0xFFA04310) : ha ? (d ? 0xFFC97A26 : 0xFFB35F14) : sw ? (d ? 0xFFC97A26 : 0xFFB3651F) : sl ? (d ? 0xFFB3651F : 0xFFA05014) : (d ? 0xFFC25E00 : 0xFF74400E));
        m.put("avatar_backgroundPink", au ? (d ? 0xFFF4AFE9 : 0xFFE86BD8) : pr ? (d ? 0xFFE8445E : 0xFFD63852) : ma ? (d ? 0xFFFFB4C4 : 0xFFE87D94) : ha ? (d ? 0xFFF2A0CF : 0xFFEB459E) : sw ? (d ? 0xFFF2A0C0 : 0xFFE87DAA) : sl ? (d ? 0xFFF2A0C0 : 0xFFE87DAA) : (d ? 0xFFE8871E : 0xFF8A3E06));
        m.put("avatar_background2Pink", au ? (d ? 0xFFA8459B : 0xFF7A2F6E) : pr ? (d ? 0xFF6E1224 : 0xFF8C1F35) : ma ? (d ? 0xFFC25068 : 0xFFA03C54) : ha ? (d ? 0xFFC93D93 : 0xFF9E2E76) : sw ? (d ? 0xFFC25068 : 0xFF9E3C58) : sl ? (d ? 0xFFC25068 : 0xFF9E3C58) : (d ? 0xFFFFB25E : 0xFFB45309));
        m.put("avatar_backgroundRed", au ? (d ? 0xFFFFB3A6 : 0xFFFF8A7A) : pr ? (d ? 0xFFFFB38E : 0xFFFF8A5C) : ma ? (d ? 0xFFE85B50 : 0xFFC63026) : ha ? (d ? 0xFFF08A80 : 0xFFED4245) : sw ? (d ? 0xFFE88A94 : 0xFFE5484D) : sl ? (d ? 0xFFF08A80 : 0xFFE8443A) : (d ? 0xFFB4382C : 0xFF6E2A1E));
        m.put("avatar_background2Red", au ? (d ? 0xFFD4574A : 0xFFC24238) : pr ? (d ? 0xFFC24B23 : 0xFFA03D18) : ma ? (d ? 0xFF9E241C : 0xFF7E1C16) : ha ? (d ? 0xFFC22B2B : 0xFFA02323) : sw ? (d ? 0xFF9E1B2E : 0xFF7A1420) : sl ? (d ? 0xFFC22B1F : 0xFFA02018) : (d ? 0xFFDD8A5B : 0xFF9E4632));
        m.put("avatar_backgroundViolet", au ? (d ? 0xFF6A5CC4 : 0xFF4A3E8C) : pr ? (d ? 0xFF5C2E8C : 0xFF3F2064) : ma ? (d ? 0xFFA077E8 : 0xFF6E48C2) : ha ? (d ? 0xFFB08CF8 : 0xFF8A57F0) : sw ? (d ? 0xFF8B7CF6 : 0xFF7A6ED0) : sl ? (d ? 0xFFB08CF8 : 0xFF8A57F0) : (d ? 0xFF8C6A1D : 0xFF5E470F));
        m.put("avatar_background2Violet", au ? (d ? 0xFFB9AFF2 : 0xFF8B7CF6) : pr ? (d ? 0xFFD3BDF2 : 0xFFA86BE0) : ma ? (d ? 0xFF5C3494 : 0xFF452473) : ha ? (d ? 0xFF5C3494 : 0xFF4A2E7E) : sw ? (d ? 0xFF5C4E9E : 0xFF4A3E8C) : sl ? (d ? 0xFF5C3494 : 0xFF4A2E7E) : (d ? 0xFFC2A25E : 0xFF8C6A1D));
        m.put("avatar_backgroundSaved", au ? (d ? 0xFFD7E0E8 : 0xFFC9D6DF) : pr ? (d ? 0xFFC77E14 : 0xFF8A5606) : ma ? (d ? 0xFFE8B23A : 0xFFC28C1E) : ha ? (d ? 0xFFB0B4CE : 0xFF8C8FB5) : sw ? (d ? 0xFFC0B8A0 : 0xFF8C8470) : sl ? (d ? 0xFFC9C4A8 : 0xFF8C8470) : (d ? 0xFFC25E00 : 0xFF74400E));
        m.put("avatar_background2Saved", au ? (d ? 0xFF6E7E8A : 0xFF5A6B75) : pr ? (d ? 0xFF8A5606 : 0xFF5C3D02) : ma ? (d ? 0xFF8C6414 : 0xFF6E4E10) : ha ? (d ? 0xFF5C5F8C : 0xFF3F4268) : sw ? (d ? 0xFF6E6858 : 0xFF54503F) : sl ? (d ? 0xFF6E6858 : 0xFF54503F) : (d ? 0xFFF0C08A : 0xFFB06428));
        m.put("avatar_nameInMessageBlue", au ? (d ? 0xFF0B8A72 : 0xFF4DE8C8) : pr ? (d ? 0xFF8A5E0C : 0xFFF0B449) : ma ? (d ? 0xFF2E5BC4 : 0xFF7FB3FF) : ha ? (d ? 0xFF4453D6 : 0xFF7983F5) : sw ? (d ? 0xFF2E77C4 : 0xFF86DFFF) : sl ? (d ? 0xFF2E77C4 : 0xFF6FB9EC) : (d ? 0xFFB4561A : 0xFFE8A45C));
        m.put("avatar_nameInMessageCyan", au ? (d ? 0xFF6A5CC4 : 0xFFB9AFF2) : pr ? (d ? 0xFF5C2E8C : 0xFFD3BDF2) : ma ? (d ? 0xFF1782A0 : 0xFF7FD9E8) : ha ? (d ? 0xFF5C63D8 : 0xFFBFC4FA) : sw ? (d ? 0xFF1782A0 : 0xFF8FD8E8) : sl ? (d ? 0xFF1782A0 : 0xFF7FD9E8) : (d ? 0xFF9C7A1E : 0xFFD6B25C));
        m.put("avatar_nameInMessageGreen", au ? (d ? 0xFF4E8C64 : 0xFF8AE0B0) : pr ? (d ? 0xFF0C8A7E : 0xFF7FE6D8) : ma ? (d ? 0xFF27702F : 0xFF5FCE6A) : ha ? (d ? 0xFF2E8C4A : 0xFF6DBE7F) : sw ? (d ? 0xFF4E7E3A : 0xFF7EBF6E) : sl ? (d ? 0xFF4A7028 : 0xFFA4E05B) : (d ? 0xFF6E8C2A : 0xFFB6C25E));
        m.put("avatar_nameInMessageOrange", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC25414 : 0xFFFFA94D) : ha ? (d ? 0xFFB35F14 : 0xFFFFC061) : sw ? (d ? 0xFFC97A26 : 0xFFFFB454) : sl ? (d ? 0xFFA05014 : 0xFFFFB03A) : (d ? 0xFFC25E00 : 0xFFF5A623));
        m.put("avatar_nameInMessagePink", au ? (d ? 0xFFB84A9E : 0xFFF08BD0) : pr ? (d ? 0xFFC42B4B : 0xFFF4A0AE) : ma ? (d ? 0xFFC25068 : 0xFFFFB4C4) : ha ? (d ? 0xFFC93D93 : 0xFFF2A0CF) : sw ? (d ? 0xFFC25068 : 0xFFF2A0C0) : sl ? (d ? 0xFFC25068 : 0xFFF2A0C0) : (d ? 0xFFB4382C : 0xFFE06A5B));
        m.put("avatar_nameInMessageRed", au ? (d ? 0xFFA8433C : 0xFFFFA08F) : pr ? (d ? 0xFFA03D18 : 0xFFFFB38E) : ma ? (d ? 0xFF9E241C : 0xFFE85B50) : ha ? (d ? 0xFFC22B2B : 0xFFF08A80) : sw ? (d ? 0xFF9E1B2E : 0xFFE88A94) : sl ? (d ? 0xFFA02018 : 0xFFF08A80) : (d ? 0xFFA03A2A : 0xFFE08573));
        m.put("avatar_nameInMessageViolet", au ? (d ? 0xFF7A6ED0 : 0xFFC9B8F5) : pr ? (d ? 0xFF4A3E8C : 0xFFC9B8F5) : ma ? (d ? 0xFF5C3494 : 0xFFA077E8) : ha ? (d ? 0xFF5C3494 : 0xFFB08CF8) : sw ? (d ? 0xFF5C4E9E : 0xFF8B7CF6) : sl ? (d ? 0xFF5C3494 : 0xFFB08CF8) : (d ? 0xFF8C5A3C : 0xFFD69A78));
        m.put("avatar_backgroundArchived", au ? (d ? 0xFF9AA2B2 : 0xFF5E6675) : pr ? (d ? 0xFFB5A88E : 0xFF5E5570) : ma ? (d ? 0xFF8C9AB8 : 0xFF4A5878) : ha ? (d ? 0xFFA0A3C0 : 0xFF5C5F8C) : sw ? (d ? 0xFFB5AE96 : 0xFF5E5848) : sl ? (d ? 0xFFA8B4A0 : 0xFF5E6E58) : (d ? 0xFFA8A094 : 0xFF6B6257));
        m.put("avatar_backgroundArchivedHidden", au ? (d ? 0xFFC9CFDA : 0xFF333A46) : pr ? (d ? 0xFFE4DAC4 : 0xFF2E2440) : ma ? (d ? 0xFFDCE4F2 : 0xFF253260) : ha ? (d ? 0xFFDCDEEE : 0xFF2E3050) : sw ? (d ? 0xFFE0D9BF : 0xFF3A3428) : sl ? (d ? 0xFFD8E8F2 : 0xFF2E4A3E) : (d ? 0xFFD8D0C4 : 0xFF3A332A));
        m.put("avatar_text", au ? 0xFFFFFFFF : pr ? (d ? 0xFFFFFFFF : 0xFFFFF6EC) : ma ? 0xFFFFFFFF : ha ? 0xFFFFFFFF : sw ? 0xFFFFFFFF : sl ? 0xFFFFFFFF : (d ? 0xFFFFFFFF : 0xFFFFF1DC));
        m.put("avatar_actionBarIconBlue", text);
        m.put("avatar_actionBarSelectorBlue", AmberTokens.alpha(text, 0.10f));
        m.put("avatar_backgroundActionBarBlue", header);
        m.put("avatar_backgroundInProfileBlue", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_SURFACE) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_SURFACE) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_SURFACE) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP));
        m.put("avatar_subtitleInProfileBlue", dim);

        // ── استوری/تاپیک/شیشه/متن قرمز ──────────────────────────────────────
        m.put("stories_circle1", accent);
        m.put("stories_circle2", accentBright);
        m.put("stories_circle_closeFriends1", d ? 0xFF4E9C4B : 0xFF7DBE72);
        m.put("stories_circle_closeFriends2", d ? 0xFF3D7A2B : 0xFF5E9C52);
        m.put("stories_circle_dialog1", accent);
        m.put("stories_circle_dialog2", accentBright);
        m.put("stories_circle_live1", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("stories_circle_live2", d ? 0xFF8C2E2E : 0xFFB44A3E);
        m.put("topics_unreadCounter", accent);
        // UI2 قدم ۱۴ — بج تاپیک بی‌صدا سبک شبح است (پر α۳۰٪ + متن هم‌رنگ)؛
        // رنگ قبلی surface = متن تقریباً نامرئی روی کاغذ؛ جوهر dim خوانا و آرام است.
        m.put("topics_unreadCounterMuted", dim);
        m.put("glass_defaultIcon", text);
        m.put("glass_defaultText", text);
        m.put("glass_tabSelected", AmberTokens.alpha(accent, 0.30f));
        m.put("glass_tabSelectedText", accent);
        m.put("glass_tabUnselected", dim);
        m.put("glass_targetMainTabs", au ? (d ? 0xE6F5F5FA : 0xE60B0F16) : pr ? (d ? 0xE6FFF6E4 : 0xE6181326) : ma ? (d ? 0xE6F2F7FF : 0xE6111731) : ha ? (d ? 0xE6F4F5FB : 0xE6131424) : sw ? (d ? 0xE6F6F3E7 : 0xE605070D) : sl ? (d ? 0xE6F4FAFF : 0xE60E2430) : (d ? 0xE6FFF6EA : 0xE6241D14));
        m.put("glass_targetMainTopPanel", au ? (d ? 0xE6FFFFFF : 0xE612151B) : pr ? (d ? 0xE6FFFBEF : 0xE6120F1B) : ma ? (d ? 0xE6E7F0FF : 0xE60D1226) : ha ? (d ? 0xE6FFFFFF : 0xE6191A26) : sw ? (d ? 0xE6FBF8EE : 0xE60B1120) : sl ? (d ? 0xE6EDF7FF : 0xE60B1D27) : (d ? 0xE6FFE9CF : 0xE61F1912));
        m.put("text_RedRegular", red);
        m.put("text_RedBold", red);

        // ── Instant View ────────────────────────────────────────────────────
        m.put("iv_background", white);
        m.put("iv_backgroundGray", au ? (d ? AmberTokens.AURORA_DAY_SURFACE : AmberTokens.AURORA_NIGHT_BG) : pr ? (d ? AmberTokens.PREMIERE_DAY_SURFACE : AmberTokens.PREMIERE_NIGHT_BG) : ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG) : ha ? (d ? AmberTokens.HARMONY_DAY_SURFACE : AmberTokens.HARMONY_NIGHT_BG) : sw ? (d ? AmberTokens.SW_DAY_SURFACE : AmberTokens.SW_NIGHT_BG) : sl ? (d ? AmberTokens.SLING_DAY_SURFACE : AmberTokens.SLING_NIGHT_BG) : (d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG));
        m.put("iv_navigationBackground", header);
        m.put("iv_ab_progress", accent);


        // ── برند آئورورا (v0.9.7) — اکسنت‌های مکمل: پوشش کلیدهای برند کهربا خارج از پالت هسته ──
        // شاخهٔ کهربا = مقدار موروثی فایل شب (ثابت؛ فایل‌های کهربا بازتولید نمی‌شوند و کلیدهای غایب در
        // فایل روز کهربا به پیش‌فرض آپستریم برمی‌گردند)؛ شاخهٔ آئورورا = خانوادهٔ روبان + تینت‌های سرد.
m.put("avatar_actionBarSelectorGreen", au ? (d ? 0xFFC3CFDB : 0xFF1F3B46) : pr ? (d ? 0xFFE8DCC2 : 0xFF2E2440) : ma ? (d ? 0xFFDCE4F2 : 0xFF20305C) : ha ? (d ? 0xFFDCDDF0 : 0xFF2E3050) : sw ? (d ? 0xFFEFEAD6 : 0xFF1E2A4A) : sl ? (d ? 0xFFDFF0FA : 0xFF1C3A4A) : 0xFF703D18);
m.put("botKeyboard_button_primary", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("buttonNeutralText", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("changephoneinfo_image2", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("chat_emojiPanelBadgeBackground", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFFF7716);
m.put("chats_tabUnreadActiveBackground", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF66ADE1 : 0xFFF97316));
m.put("color_blue", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFF2E5BC4 : 0xFF5C94FC) : ha ? (d ? 0xFF3D48C4 : 0xFF7983F5) : sw ? (d ? 0xFF2E77C4 : 0xFF3E8EDE) : sl ? (d ? 0xFF2E77C4 : 0xFF5FB0E8) : (d ? 0xFF327FE5 : 0xFFFF7614));
m.put("color_lightblue", au ? (d ? 0xFF6A5CC4 : 0xFF8B7CF6) : pr ? (d ? 0xFF5C2E8C : 0xFFA86BE0) : ma ? (d ? 0xFF5C3494 : 0xFFA077E8) : ha ? (d ? 0xFF6E63D8 : 0xFF8A57F0) : sw ? (d ? 0xFF6A5CC4 : 0xFF86DFFF) : sl ? (d ? 0xFF5FB0E8 : 0xFF8FD1F5) : (d ? 0xFF58A8ED : 0xFFF57214));
m.put("color_orange", au ? (d ? 0xFFC97A26 : 0xFFFFB454) : pr ? (d ? 0xFFC77E14 : 0xFFF0B449) : ma ? (d ? 0xFFC25414 : 0xFFFF8A3C) : ha ? (d ? 0xFFB3541E : 0xFFFF8A3C) : sw ? (d ? 0xFFC25414 : 0xFFF2A93B) : sl ? (d ? 0xFFB3651F : 0xFFFF8A3C) : 0xFFF28C39);
m.put("color_yellow", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : pr ? (d ? 0xFFC42B4B : 0xFFE8445E) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFFC93D93 : 0xFFEB459E) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFFE3B727 : 0xFFDEAC1F));
m.put("contacts_inviteBackground", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("contextProgressInner2", au ? (d ? 0xFFDEE5EF : 0xFF1B2430) : pr ? (d ? 0xFFF1E4C8 : 0xFF241C36) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFE9EBFA : 0xFF1D1F38) : sw ? (d ? 0xFFF2EEDA : 0xFF141C30) : sl ? (d ? 0xFFE2F1FC : 0xFF12303E) : (d ? 0xCEC3DDF6 : 0xFF3F2712));
m.put("contextProgressInner3", au ? (d ? 0xFF0F9B80 : 0xFF0E8A78) : pr ? (d ? 0xFFB96A0B : 0xFF8A5606) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFB45309);
m.put("contextProgressInner4", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("contextProgressOuter1", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF3BA6F4 : 0xFFFF7E21));
m.put("fastScrollActive", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF229AF0 : 0xFFF97316));
m.put("featuredStickers_addButton2", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("featuredStickers_addedIcon", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF32A5F7 : 0xFFF97A20));
m.put("featuredStickers_buttonProgress", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("featuredStickers_unread", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("files_folderIconBackground", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFF27702F : 0xFF5FCE6A) : ha ? (d ? 0xFF27702F : 0xFF5FCE6A) : sw ? (d ? 0xFF27702F : 0xFF5FCE6A) : sl ? (d ? 0xFF5E8C36 : 0xFF7DBB42) : 0xFFF4771D);
m.put("fill_RedDark", au ? (d ? 0xFFB4382C : 0xFFCC4A3A) : pr ? (d ? 0xFFB42B45 : 0xFFCC4A3A) : ma ? (d ? 0xFFB4271C : 0xFFCC4A3A) : ha ? (d ? 0xFFB4382C : 0xFFCC4A3A) : sw ? (d ? 0xFF9E1B2E : 0xFFCC4A3A) : sl ? (d ? 0xFFB42B1F : 0xFFCC4A3A) : 0xFFC2410C);
m.put("gift_ribbon", au ? (d ? 0xFFCBD6E0 : 0xFF182E3A) : pr ? (d ? 0xFFE8DCC2 : 0xFF2E2440) : ma ? (d ? 0xFFDCE4F2 : 0xFF20305C) : ha ? (d ? 0xFFDCDDF0 : 0xFF2E3050) : sw ? (d ? 0xFFEFEAD6 : 0xFF1E2A4A) : sl ? (d ? 0xFFDFF0FA : 0xFF1C3A4A) : 0xFF844518);
m.put("inappPlayerPlayPause", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF229AF0 : 0xFFF97A20));
m.put("key_player_progressCachedBackground", au ? (d ? 0xFFC9D4DE : 0xFF1E3B47) : pr ? (d ? 0xFFE8D4B0 : 0xFF33294A) : ma ? (d ? 0xFFD5E1F4 : 0xFF253260) : ha ? (d ? 0xFFD5D8F5 : 0xFF2E3050) : sw ? (d ? 0xFFE0D9BF : 0xFF2A1420) : sl ? (d ? 0xFFD8E8F2 : 0xFF1C3A4A) : 0xFF874C23);
m.put("location_actionBackground", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("location_liveLocationProgress", au ? (d ? 0xFF0B7E6A : 0xFF0FA084) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFE07325);
m.put("location_placeLocationBackground", au ? (d ? 0xFF0B7E6A : 0xFF0FA084) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFE07325);
m.put("location_sendLiveLocationBackground", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFF27702F : 0xFF5FCE6A) : ha ? (d ? 0xFF27702F : 0xFF5FCE6A) : sw ? (d ? 0xFF27702F : 0xFF5FCE6A) : sl ? (d ? 0xFF5E8C36 : 0xFF7DBB42) : 0xFFF97316);
m.put("location_sendLiveLocationText", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFF27702F : 0xFF5FCE6A) : ha ? (d ? 0xFF27702F : 0xFF5FCE6A) : sw ? (d ? 0xFF27702F : 0xFF5FCE6A) : sl ? (d ? 0xFF5E8C36 : 0xFF7DBB42) : 0xFFF97316);
m.put("location_sendLocationBackground", au ? (d ? 0xFF0B7E6A : 0xFF0FA084) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF50A4F5 : 0xFFE07325));
m.put("location_sendLocationIcon", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("location_sendLocationText", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("login_progressInner", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("passport_authorizeBackground", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFC15C13);
m.put("passport_authorizeBackgroundSelected", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFE06A16);
m.put("passport_authorizeText", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("picker_badge", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF35A3F7 : 0xFFFF7817));
m.put("picker_enabledButton", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF279EF5 : 0xFFF97316));
m.put("player_buttonActive", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF2CA3FE : 0xFFF97A20));
m.put("player_progress", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF219DF4 : 0xFFF97A20));
m.put("pollCreateIcons", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("premiumCoinGradient1", au ? (d ? 0xFF0A5F52 : 0xFF0E6E5E) : pr ? (d ? 0xFF8A5E0C : 0xFF6E4A08) : ma ? (d ? 0xFFB3651F : 0xFF6E4A04) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFC2410C);
m.put("premiumCoinGradient2", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("premiumGradient0", au ? (d ? 0xFF06322B : 0xFF083A32) : pr ? (d ? 0xFF4A3208 : 0xFF2E1F06) : ma ? (d ? 0xFF3A0E0A : 0xFF0A0F1E) : ha ? (d ? 0xFF10112E : 0xFF0B0C22) : sw ? (d ? 0xFF1A060C : 0xFF0A0408) : sl ? (d ? 0xFF5E120C : 0xFF0C2028) : 0xFF7C2D12);
m.put("premiumGradient1", au ? (d ? 0xFF08423A : 0xFF0A4A40) : pr ? (d ? 0xFF5C3D08 : 0xFF3A2808) : ma ? (d ? 0xFF4E1410 : 0xFF0D1528) : ha ? (d ? 0xFF1A1C48 : 0xFF12133A) : sw ? (d ? 0xFF2A0A14 : 0xFF140810) : sl ? (d ? 0xFF7A1A10 : 0xFF122C38) : 0xFF9A3412);
m.put("premiumGradient2", au ? (d ? 0xFF0A5F52 : 0xFF0E6E5E) : pr ? (d ? 0xFF8A5E0C : 0xFF6E4A08) : ma ? (d ? 0xFF8C1A12 : 0xFF14204A) : ha ? (d ? 0xFF262A78 : 0xFF1B1D56) : sw ? (d ? 0xFF4A1020 : 0xFF1C0C18) : sl ? (d ? 0xFF9E2418 : 0xFF17323C) : 0xFFC2410C);
m.put("premiumGradient3", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFFB96A0B : 0xFF8A5606) : ma ? (d ? 0xFFB42018 : 0xFF1A2A5E) : ha ? (d ? 0xFF3A40C0 : 0xFF2A2E88) : sw ? (d ? 0xFF7A1428 : 0xFF2A1024) : sl ? (d ? 0xFFC23A28 : 0xFF1E3E48) : 0xFFEA580C);
m.put("premiumGradient4", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFE52521 : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("premiumGradientBottomSheet1", au ? (d ? 0xFF08423A : 0xFF0A4A40) : pr ? (d ? 0xFF5C3D08 : 0xFF3A2808) : ma ? (d ? 0xFF4E1410 : 0xFF0D1528) : ha ? (d ? 0xFF1A1C48 : 0xFF12133A) : sw ? (d ? 0xFF2A0A14 : 0xFF140810) : sl ? (d ? 0xFF7A1A10 : 0xFF122C38) : 0xFF9A3412);
m.put("premiumGradientBottomSheet2", au ? (d ? 0xFF0A5F52 : 0xFF0E6E5E) : pr ? (d ? 0xFF8A5E0C : 0xFF6E4A08) : ma ? (d ? 0xFF8C1A12 : 0xFF14204A) : ha ? (d ? 0xFF262A78 : 0xFF1B1D56) : sw ? (d ? 0xFF4A1020 : 0xFF1C0C18) : sl ? (d ? 0xFF9E2418 : 0xFF17323C) : 0xFFC2410C);
m.put("premiumGradientBottomSheet3", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFE52521 : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("premiumStarGradient1", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFE9A93A) : ma ? (d ? 0xFFE52521 : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFFF7614);
m.put("premiumStartSmallStarsColor", au ? (d ? 0x7108806B : 0x712DE4C4) : pr ? (d ? 0x71A76F0F : 0x71E9A93A) : ma ? (d ? 0x71E52521 : 0x71FBD000) : ha ? (d ? 0x714453D6 : 0x715865F2) : sw ? (d ? 0x719E1B2E : 0x71E5484D) : sl ? (d ? 0x71C23A28 : 0x71FFB03A) : 0x71FF7B1C);
m.put("progressCircle", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFF3FA5FE : 0xFFF97316));
m.put("reactionStarSelector", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("returnToCallBackground", au ? (d ? 0xFF0B7E6A : 0xFF0FA084) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : (d ? 0xFF50A8ED : 0xFFF0751D));
m.put("sessions_devicesImage", au ? (d ? 0xFFDCE2EA : 0xFF10161F) : pr ? (d ? 0xFFEDE2CC : 0xFF14101F) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFE9EBFA : 0xFF1D1F38) : sw ? (d ? 0xFFF2EEDA : 0xFF141C30) : sl ? (d ? 0xFFE2F1FC : 0xFF12303E) : 0xFF33200E);
m.put("sharedMedia_startStopLoadIcon", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFC77E14 : 0xFFF0B449) : ma ? (d ? 0xFFB3651F : 0xFFFBD000) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFF97A20);
m.put("statisticChartActivePickerChart", au ? (d ? 0xD8B9C8D4 : 0xD82A4A56) : pr ? (d ? 0xD8E7DCC2 : 0xD8332A48) : ma ? (d ? 0xD8E3EEFF : 0xD820305C) : ha ? (d ? 0xD8E9EBFA : 0xD81D1F38) : sw ? (d ? 0xD8F2EEDA : 0xD8141C30) : sl ? (d ? 0xD8E2F1FC : 0xD812303E) : 0xD87E4822);
m.put("statisticChartBackZoomColor", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF87314);
m.put("statisticChartLine_blue", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFF2E5BC4 : 0xFF5C94FC) : ha ? (d ? 0xFF3D48C4 : 0xFF7983F5) : sw ? (d ? 0xFF2E77C4 : 0xFF3E8EDE) : sl ? (d ? 0xFF2E77C4 : 0xFF5FB0E8) : (d ? 0xFF327FE5 : 0xFFF97316));
m.put("statisticChartLine_golden", au ? (d ? 0xFFB84A9E : 0xFFE86BD8) : pr ? (d ? 0xFFC42B4B : 0xFFE8445E) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFFC93D93 : 0xFFEB459E) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : (d ? 0xFFE3B727 : 0xFFDEAC1F));
m.put("statisticChartLine_lightblue", au ? (d ? 0xFF6A5CC4 : 0xFF8B7CF6) : pr ? (d ? 0xFF5C2E8C : 0xFFA86BE0) : ma ? (d ? 0xFF5C3494 : 0xFFA077E8) : ha ? (d ? 0xFF6E63D8 : 0xFF8A57F0) : sw ? (d ? 0xFF6A5CC4 : 0xFF86DFFF) : sl ? (d ? 0xFF5FB0E8 : 0xFF8FD1F5) : (d ? 0xFF58A8ED : 0xFFF57214));
m.put("statisticChartLine_orange", au ? (d ? 0xFFC97A26 : 0xFFFFB454) : pr ? (d ? 0xFFC77E14 : 0xFFF0B449) : ma ? (d ? 0xFFC25414 : 0xFFFF8A3C) : ha ? (d ? 0xFFB3541E : 0xFFFF8A3C) : sw ? (d ? 0xFFC25414 : 0xFFF2A93B) : sl ? (d ? 0xFFB3651F : 0xFFFF8A3C) : 0xFFF28C39);
m.put("statisticChartRipple", au ? (d ? 0x2C08806B : 0x2C2DE4C4) : pr ? (d ? 0x2CA76F0F : 0x2CF0B449) : ma ? (d ? 0x2CC6281C : 0x2CFBD000) : ha ? (d ? 0x2C4453D6 : 0x2C5865F2) : sw ? (d ? 0x2C9E1B2E : 0x2CE5484D) : sl ? (d ? 0x2CC23A28 : 0x2CFFB03A) : 0x2CDA8548);
m.put("stickers_menu", au ? (d ? 0xFFCBD6E0 : 0xFF182E3A) : pr ? (d ? 0xFFE8DCC2 : 0xFF2E2440) : ma ? (d ? 0xFFDCE4F2 : 0xFF20305C) : ha ? (d ? 0xFFDCDDF0 : 0xFF2E3050) : sw ? (d ? 0xFFEFEAD6 : 0xFF1E2A4A) : sl ? (d ? 0xFFDFF0FA : 0xFF1C3A4A) : 0xFF844E27);
m.put("telegram_color", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("telegram_color_text", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("undo_cancelColor", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("voipgroup_checkMenu", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("voipgroup_connectingProgress", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_listeningText", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("voipgroup_muteButton", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_muteButton2", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("voipgroup_muteButton3", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("voipgroup_overlayBlue1", au ? (d ? 0xFFDEE5EF : 0xFF1B2430) : pr ? (d ? 0xFFF1E4C8 : 0xFF241C36) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFDEE0FA : 0xFF1D1F38) : sw ? (d ? 0xFFF0ECD8 : 0xFF131C34) : sl ? (d ? 0xFFDFF0FC : 0xFF12303E) : 0xFF3F2712);
m.put("voipgroup_overlayBlue2", au ? (d ? 0xFFE3E8F0 : 0xFF141C28) : pr ? (d ? 0xFFF4E8D0 : 0xFF1E1730) : ma ? (d ? 0xFFEFF5FF : 0xFF1A2344) : ha ? (d ? 0xFFE8E9FC : 0xFF161830) : sw ? (d ? 0xFFF4F0DE : 0xFF101828) : sl ? (d ? 0xFFE8F6FE : 0xFF0F2836) : 0xFF331F0D);
m.put("voipgroup_overlayGreen1", au ? (d ? 0xFFE8ECF2 : 0xFF10161E) : pr ? (d ? 0xFFF4E8D0 : 0xFF1E1730) : ma ? (d ? 0xFFEFF5FF : 0xFF1A2344) : ha ? (d ? 0xFFE8ECF8 : 0xFF141A28) : sw ? (d ? 0xFFF4EFE0 : 0xFF0F1626) : sl ? (d ? 0xFFE8F4EA : 0xFF0F2430) : 0xFF2A1A0B);
m.put("voipgroup_overlayGreen2", au ? (d ? 0xFFDEE5EF : 0xFF1B2430) : pr ? (d ? 0xFFF1E4C8 : 0xFF241C36) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFDEE0FA : 0xFF1D1F38) : sw ? (d ? 0xFFF0ECD8 : 0xFF131C34) : sl ? (d ? 0xFFDFF0FC : 0xFF12303E) : 0xFF3F2712);
m.put("voipgroup_rtmpButton", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_soundButtonActive", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_soundButtonActive2", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("voipgroup_soundButtonActive2Scrolled", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("voipgroup_soundButtonActiveScrolled", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_speakingText", au ? (d ? 0xFF0B6E5C : 0xFF54F1D6) : pr ? (d ? 0xFF7A5A0C : 0xFFF3BC55) : ma ? (d ? 0xFFA82014 : 0xFFFFDF60) : ha ? (d ? 0xFF3540B8 : 0xFF9BA3FF) : sw ? (d ? 0xFF9E1B2E : 0xFFFF6B70) : sl ? (d ? 0xFF9E2A20 : 0xFFFFC55C) : 0xFFFB923C);
m.put("voipgroup_topPanelBlue1", au ? (d ? 0xFFDEE5EF : 0xFF1B2430) : pr ? (d ? 0xFFF1E4C8 : 0xFF241C36) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFDEE0FA : 0xFF1D1F38) : sw ? (d ? 0xFFF0ECD8 : 0xFF131C34) : sl ? (d ? 0xFFDFF0FC : 0xFF12303E) : 0xFF3F2712);
m.put("voipgroup_topPanelBlue2", au ? (d ? 0xFFE3E8F0 : 0xFF141C28) : pr ? (d ? 0xFFF4E8D0 : 0xFF1E1730) : ma ? (d ? 0xFFEFF5FF : 0xFF1A2344) : ha ? (d ? 0xFFE8E9FC : 0xFF161830) : sw ? (d ? 0xFFF4F0DE : 0xFF101828) : sl ? (d ? 0xFFE8F6FE : 0xFF0F2836) : 0xFF331F0D);
m.put("voipgroup_topPanelGray", au ? (d ? 0xFFBFCBD8 : 0xFF23414E) : pr ? (d ? 0xFFE4D5B4 : 0xFF38304E) : ma ? (d ? 0xFFDCE4F2 : 0xFF253260) : ha ? (d ? 0xFFC9CBEC : 0xFF313455) : sw ? (d ? 0xFFD8D2B8 : 0xFF1E2A4A) : sl ? (d ? 0xFFC2E0F0 : 0xFF1C3A4A) : 0xFF865029);
m.put("voipgroup_topPanelGreen1", au ? (d ? 0xFFE8ECF2 : 0xFF10161E) : pr ? (d ? 0xFFF4E8D0 : 0xFF1E1730) : ma ? (d ? 0xFFEFF5FF : 0xFF1A2344) : ha ? (d ? 0xFFE8ECF8 : 0xFF141A28) : sw ? (d ? 0xFFF4EFE0 : 0xFF0F1626) : sl ? (d ? 0xFFE8F4EA : 0xFF0F2430) : 0xFF2A1A0B);
m.put("voipgroup_topPanelGreen2", au ? (d ? 0xFFDEE5EF : 0xFF1B2430) : pr ? (d ? 0xFFF1E4C8 : 0xFF241C36) : ma ? (d ? 0xFFE7F0FF : 0xFF141B3C) : ha ? (d ? 0xFFDEE0FA : 0xFF1D1F38) : sw ? (d ? 0xFFF0ECD8 : 0xFF131C34) : sl ? (d ? 0xFFDFF0FC : 0xFF12303E) : 0xFF3F2712);
m.put("voipgroup_unmuteButton", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("voipgroup_unmuteButton2", au ? (d ? 0xFF0A7A66 : 0xFF0FB89A) : pr ? (d ? 0xFF8A5E0C : 0xFFC88A1E) : ma ? (d ? 0xFFB3651F : 0xFFE8B23A) : ha ? (d ? 0xFF3540B8 : 0xFF7983F5) : sw ? (d ? 0xFF7A1420 : 0xFFE5484D) : sl ? (d ? 0xFFA03018 : 0xFFF2913C) : 0xFFEA580C);
m.put("voipgroup_windowBackgroundWhiteInputFieldActivated", au ? (d ? 0xFF08806B : 0xFF2DE4C4) : pr ? (d ? 0xFFA76F0F : 0xFFF0B449) : ma ? (d ? 0xFFC6281C : 0xFFFBD000) : ha ? (d ? 0xFF4453D6 : 0xFF5865F2) : sw ? (d ? 0xFF9E1B2E : 0xFFE5484D) : sl ? (d ? 0xFFC23A28 : 0xFFFFB03A) : 0xFFF97316);
m.put("wallet_out_commentBorder", au ? (d ? 0xFFD8DFE8 : 0xFF17222E) : pr ? (d ? 0xFFE2D5B8 : 0xFF33294A) : ma ? (d ? 0xFFD5E1F4 : 0xFF253260) : ha ? (d ? 0xFFD5D8F5 : 0xFF2E3050) : sw ? (d ? 0xFFE0D9BF : 0xFF2A1420) : sl ? (d ? 0xFFD8E8F2 : 0xFF1C3A4A) : 0xFF653D20);

        return m;
    }
}

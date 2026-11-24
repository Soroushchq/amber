package org.telegram.messenger;

/*
 * AmberGram round 21 — «انیمیشن امضای هر تم» (theme signature FX).
 *
 * هر خانوادهٔ برند صحنهٔ متحرک اختصاصی خودش را روی نوار پایین صفحهٔ اصلی دارد:
 *   ماریو → کاراکتر پیکسل‌آرتی که راه می‌رود، می‌پرد و سکه می‌زند
 *   آورورا → شفق قطبی موج‌دار + ستاره‌های چشمک‌زن + شهاب‌سنگ
 *   پریمیر → نورافکن سینما + قرص فیلم غلتان + نوار فیلم
 *   سینگ‌شات/نایت‌رید → تیرکمان و پرتاب کرهٔ پرنده (شب: نئون و رادار)
 *   سوی تاریک/روشن → میدان ستاره‌ای + شمشیر نور
 *   هارمونی → موج‌های نفس‌گیر + حباب‌های شناور
 *   آمبر (پیش‌فرض) → هالهٔ گرم + ذرات اخگر
 *
 * پرچم سراسری (همهٔ اکانت‌ها)، ذخیره در تنظیمات اصلی — هم‌الگوی AmberChatTweaks.
 */
public class AmberThemeFX {

    private static final String KEY_ENABLED = "amberThemeFXEnabled";

    private static Boolean enabled;

    public static boolean enabled() {
        Boolean value = enabled;
        if (value == null) {
            value = MessagesController.getGlobalMainSettings().getBoolean(KEY_ENABLED, true);
            enabled = value;
        }
        return value;
    }

    public static void setEnabled(boolean value) {
        enabled = value;
        MessagesController.getGlobalMainSettings().edit().putBoolean(KEY_ENABLED, value).apply();
    }

    public static void resetCache() {
        enabled = null;
    }
}

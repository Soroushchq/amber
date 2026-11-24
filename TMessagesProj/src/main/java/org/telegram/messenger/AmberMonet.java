package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Build;
import android.os.PatternMatcher;
import android.util.SparseIntArray;

import androidx.annotation.RequiresApi;
import androidx.core.graphics.ColorUtils;

import org.telegram.ui.ActionBar.OKLCH;
import org.telegram.ui.ActionBar.Theme;

/*
 * Amber گرد ۲۰ — Material You / Monet پویا (پورت از سیستم توکن Nagram، بازنویسی به سبک آمبرگرم)
 * رنگ‌های سیستم اندروید ۱۲+ (system_accent و system_neutral) به‌صورت توکن‌های «a1_600»، «n1_50»،
 * «n1_50_64» (با آلفا) یا «monet» در فایل‌های تم خوانده می‌شوند و به رنگ زندهٔ سیستم نگاشت می‌گردند.
 */

@RequiresApi(api = Build.VERSION_CODES.S)
public class AmberMonet {

    private static final SparseIntArray IDS = new SparseIntArray() {{
        put(1_1_0000, android.R.color.system_accent1_0);
        put(1_1_0010, android.R.color.system_accent1_10);
        put(1_1_0050, android.R.color.system_accent1_50);
        put(1_1_0100, android.R.color.system_accent1_100);
        put(1_1_0200, android.R.color.system_accent1_200);
        put(1_1_0300, android.R.color.system_accent1_300);
        put(1_1_0400, android.R.color.system_accent1_400);
        put(1_1_0500, android.R.color.system_accent1_500);
        put(1_1_0600, android.R.color.system_accent1_600);
        put(1_1_0700, android.R.color.system_accent1_700);
        put(1_1_0800, android.R.color.system_accent1_800);
        put(1_1_0900, android.R.color.system_accent1_900);
        put(1_1_1000, android.R.color.system_accent1_1000);
        put(1_2_0000, android.R.color.system_accent2_0);
        put(1_2_0010, android.R.color.system_accent2_10);
        put(1_2_0050, android.R.color.system_accent2_50);
        put(1_2_0100, android.R.color.system_accent2_100);
        put(1_2_0200, android.R.color.system_accent2_200);
        put(1_2_0300, android.R.color.system_accent2_300);
        put(1_2_0400, android.R.color.system_accent2_400);
        put(1_2_0500, android.R.color.system_accent2_500);
        put(1_2_0600, android.R.color.system_accent2_600);
        put(1_2_0700, android.R.color.system_accent2_700);
        put(1_2_0800, android.R.color.system_accent2_800);
        put(1_2_0900, android.R.color.system_accent2_900);
        put(1_2_1000, android.R.color.system_accent2_1000);
        put(1_3_0000, android.R.color.system_accent3_0);
        put(1_3_0010, android.R.color.system_accent3_10);
        put(1_3_0050, android.R.color.system_accent3_50);
        put(1_3_0100, android.R.color.system_accent3_100);
        put(1_3_0200, android.R.color.system_accent3_200);
        put(1_3_0300, android.R.color.system_accent3_300);
        put(1_3_0400, android.R.color.system_accent3_400);
        put(1_3_0500, android.R.color.system_accent3_500);
        put(1_3_0600, android.R.color.system_accent3_600);
        put(1_3_0700, android.R.color.system_accent3_700);
        put(1_3_0800, android.R.color.system_accent3_800);
        put(1_3_0900, android.R.color.system_accent3_900);
        put(1_3_1000, android.R.color.system_accent3_1000);
        put(2_1_0000, android.R.color.system_neutral1_0);
        put(2_1_0010, android.R.color.system_neutral1_10);
        put(2_1_0050, android.R.color.system_neutral1_50);
        put(2_1_0100, android.R.color.system_neutral1_100);
        put(2_1_0200, android.R.color.system_neutral1_200);
        put(2_1_0300, android.R.color.system_neutral1_300);
        put(2_1_0400, android.R.color.system_neutral1_400);
        put(2_1_0500, android.R.color.system_neutral1_500);
        put(2_1_0600, android.R.color.system_neutral1_600);
        put(2_1_0700, android.R.color.system_neutral1_700);
        put(2_1_0800, android.R.color.system_neutral1_800);
        put(2_1_0900, android.R.color.system_neutral1_900);
        put(2_1_1000, android.R.color.system_neutral1_1000);
        put(2_2_0000, android.R.color.system_neutral2_0);
        put(2_2_0010, android.R.color.system_neutral2_10);
        put(2_2_0050, android.R.color.system_neutral2_50);
        put(2_2_0100, android.R.color.system_neutral2_100);
        put(2_2_0200, android.R.color.system_neutral2_200);
        put(2_2_0300, android.R.color.system_neutral2_300);
        put(2_2_0400, android.R.color.system_neutral2_400);
        put(2_2_0500, android.R.color.system_neutral2_500);
        put(2_2_0600, android.R.color.system_neutral2_600);
        put(2_2_0700, android.R.color.system_neutral2_700);
        put(2_2_0800, android.R.color.system_neutral2_800);
        put(2_2_0900, android.R.color.system_neutral2_900);
        put(2_2_1000, android.R.color.system_neutral2_1000);
    }};

    private static final String ACTION_OVERLAY_CHANGED = "android.intent.action.OVERLAY_CHANGED";
    private static final OverlayChangeReceiver overlayChangeReceiver = new OverlayChangeReceiver();
    private static boolean receiverRegistered;

    public static int getColor(String rawColor) {
        return getColor(rawColor, false);
    }

    public static int getColor(String rawColor, boolean amoled) {
        if (rawColor == null || rawColor.length() < 4) {
            return 0;
        }
        Context context = ApplicationLoader.applicationContext;
        if (context == null) {
            return 0;
        }
        try {
            return resolveColor(rawColor, amoled, context);
        } catch (Exception e) {
            // توکن ناشناخته یا بدفرمت — رنگ نامعتبر برگردان تا کلید از والد پالایت شود
            return 0;
        }
    }

    private static int resolveColor(String rawColor, boolean amoled, Context context) {
        if (rawColor.startsWith("monet")) {
            int primaryColor = context.getColor(android.R.color.system_accent1_400);
            if (rawColor.startsWith("monetRed")) {
                return OKLCH.adapt(primaryColor, Color.RED);
            } else {
                return OKLCH.adapt(primaryColor, Color.GREEN);
            }
        }
        int group = rawColor.charAt(0) == 'a' ? 1 : 2;
        int palette = Integer.parseInt(rawColor.substring(1, 2));
        int alphaStart = rawColor.indexOf("_", 3);
        int shade;
        int alpha;
        if (alphaStart > 0) {
            shade = Integer.parseInt(rawColor.substring(3, alphaStart));
            alpha = Integer.parseInt(rawColor.substring(alphaStart + 1));
        } else {
            shade = Integer.parseInt(rawColor.substring(3));
            alpha = -1;
        }
        if (amoled && group == 2 && palette == 1 && shade == 900) {
            shade = 1000;
        }
        int key = group * 1_0_0000 + palette * 1_0000 + shade;
        int id = IDS.get(key);
        if (id == 0) {
            return 0;
        }
        int color = context.getColor(id);
        if (alpha != -1) {
            color = ColorUtils.setAlphaComponent(color, alpha);
        }
        return color;
    }

    public static void registerReceiver(Context context) {
        if (receiverRegistered || context == null || Build.VERSION.SDK_INT < Build.VERSION_CODES.S) {
            return;
        }
        receiverRegistered = true;
        try {
            IntentFilter packageFilter = new IntentFilter(ACTION_OVERLAY_CHANGED);
            packageFilter.addDataScheme("package");
            packageFilter.addDataSchemeSpecificPart("android", PatternMatcher.PATTERN_LITERAL);
            context.registerReceiver(overlayChangeReceiver, packageFilter);
        } catch (Exception e) {
            FileLog.e(e);
        }
    }

    public static void unregisterReceiver(Context context) {
        if (!receiverRegistered || context == null) {
            return;
        }
        receiverRegistered = false;
        try {
            context.unregisterReceiver(overlayChangeReceiver);
        } catch (IllegalArgumentException e) {
            FileLog.e(e);
        }
    }

    private static class OverlayChangeReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (ACTION_OVERLAY_CHANGED.equals(intent.getAction())) {
                if (Theme.getActiveTheme() != null && Theme.getActiveTheme().isMonet()) {
                    Theme.applyTheme(Theme.getActiveTheme(), Theme.isCurrentThemeNight());
                }
            }
        }
    }
}

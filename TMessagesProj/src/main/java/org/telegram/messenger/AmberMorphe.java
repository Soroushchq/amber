package org.telegram.messenger;

/*
 * AmberGram fork: full Morphe patch bundle, inspired by the community
 * "Morphe" patches (HushTelegram, rahul9999xda/morphe-patches,
 * newuser7171/telegram-morphe-patches-). Native ports of every patch that
 * is feasible for a source fork (Morphe targets re-signed APKs via Xposed):
 *  - antiDelete          — incoming deletions (server updates) no longer
 *                          remove messages locally (anti-recall)
 *  - antiDisappearing    — view-once voice notes / round videos stay
 *                          playable and forwardable indefinitely
 *  - noScreenshotNotify  — screenshot-taken notifications are never sent
 *                          to the other user
 *  - bypassNoforwards    — save/copy/forward allowed in chats and channels
 *                          that flag content as protected
 *  - noAutoUpdate        — never query or suggest official in-app updates
 *                          (protects the fork from being replaced)
 *  - noChannelSwitch     — disables the pull-down "next unread channel"
 *                          gesture inside chats
 *  - hideStoriesRead     — stories are marked read locally but no read
 *                          receipt is ever sent
 *  - bypassTranslation   — translation stays available even when the peer
 *                          or chat disables it
 * Already covered by earlier bundles (kept in AmberAntiAds / AmberGhost):
 * remove ads, hide typing indicator (ghost), download speed boost,
 * Morphe-equivalent settings entry point.
 * Patches that are NOT portable are intentionally omitted: Unlock Premium
 * (server-side), Bypass channel restrictions (server-side in this version),
 * signature/certificate/install-source spoofs and Firebase repair (Morphe
 * re-signing infrastructure), rich clipboard patch (not present in this
 * codebase), telemetry (no Firebase Analytics bundled at all).
 * All flags are global (all accounts), stored in the main settings prefs.
 */

import android.content.SharedPreferences;

public class AmberMorphe {

    private static final Object lock = new Object();
    private static Boolean antiDelete;
    private static Boolean antiDisappearing;
    private static Boolean noScreenshotNotify;
    private static Boolean bypassNoforwards;
    private static Boolean noAutoUpdate;
    private static Boolean noChannelSwitch;
    private static Boolean hideStoriesRead;
    private static Boolean bypassTranslation;

    private static boolean load(String key, boolean defaultValue) {
        SharedPreferences preferences = MessagesController.getGlobalMainSettings();
        return preferences.getBoolean(key, defaultValue);
    }

    private static void save(String key, boolean value) {
        MessagesController.getGlobalMainSettings().edit().putBoolean(key, value).apply();
    }

    public static boolean antiDelete() {
        Boolean value = antiDelete;
        if (value == null) {
            synchronized (lock) {
                if (antiDelete == null) {
                    antiDelete = load("amberMorpheAntiDelete", true);
                }
                value = antiDelete;
            }
        }
        return value;
    }

    public static void setAntiDelete(boolean value) {
        synchronized (lock) {
            antiDelete = value;
            save("amberMorpheAntiDelete", value);
        }
    }

    public static boolean antiDisappearing() {
        Boolean value = antiDisappearing;
        if (value == null) {
            synchronized (lock) {
                if (antiDisappearing == null) {
                    antiDisappearing = load("amberMorpheAntiDisappearing", true);
                }
                value = antiDisappearing;
            }
        }
        return value;
    }

    public static void setAntiDisappearing(boolean value) {
        synchronized (lock) {
            antiDisappearing = value;
            save("amberMorpheAntiDisappearing", value);
        }
    }

    public static boolean noScreenshotNotify() {
        Boolean value = noScreenshotNotify;
        if (value == null) {
            synchronized (lock) {
                if (noScreenshotNotify == null) {
                    noScreenshotNotify = load("amberMorpheNoScreenshotNotify", true);
                }
                value = noScreenshotNotify;
            }
        }
        return value;
    }

    public static void setNoScreenshotNotify(boolean value) {
        synchronized (lock) {
            noScreenshotNotify = value;
            save("amberMorpheNoScreenshotNotify", value);
        }
    }

    public static boolean bypassNoforwards() {
        Boolean value = bypassNoforwards;
        if (value == null) {
            synchronized (lock) {
                if (bypassNoforwards == null) {
                    bypassNoforwards = load("amberMorpheBypassNoforwards", true);
                }
                value = bypassNoforwards;
            }
        }
        return value;
    }

    public static void setBypassNoforwards(boolean value) {
        synchronized (lock) {
            bypassNoforwards = value;
            save("amberMorpheBypassNoforwards", value);
        }
    }

    public static boolean noAutoUpdate() {
        Boolean value = noAutoUpdate;
        if (value == null) {
            synchronized (lock) {
                if (noAutoUpdate == null) {
                    noAutoUpdate = load("amberMorpheNoAutoUpdate", true);
                }
                value = noAutoUpdate;
            }
        }
        return value;
    }

    public static void setNoAutoUpdate(boolean value) {
        synchronized (lock) {
            noAutoUpdate = value;
            save("amberMorpheNoAutoUpdate", value);
        }
    }

    public static boolean noChannelSwitch() {
        Boolean value = noChannelSwitch;
        if (value == null) {
            synchronized (lock) {
                if (noChannelSwitch == null) {
                    noChannelSwitch = load("amberMorpheNoChannelSwitch", false);
                }
                value = noChannelSwitch;
            }
        }
        return value;
    }

    public static void setNoChannelSwitch(boolean value) {
        synchronized (lock) {
            noChannelSwitch = value;
            save("amberMorpheNoChannelSwitch", value);
        }
    }

    public static boolean hideStoriesRead() {
        Boolean value = hideStoriesRead;
        if (value == null) {
            synchronized (lock) {
                if (hideStoriesRead == null) {
                    hideStoriesRead = load("amberMorpheHideStoriesRead", true);
                }
                value = hideStoriesRead;
            }
        }
        return value;
    }

    public static void setHideStoriesRead(boolean value) {
        synchronized (lock) {
            hideStoriesRead = value;
            save("amberMorpheHideStoriesRead", value);
        }
    }

    public static boolean bypassTranslation() {
        Boolean value = bypassTranslation;
        if (value == null) {
            synchronized (lock) {
                if (bypassTranslation == null) {
                    bypassTranslation = load("amberMorpheBypassTranslation", true);
                }
                value = bypassTranslation;
            }
        }
        return value;
    }

    public static void setBypassTranslation(boolean value) {
        synchronized (lock) {
            bypassTranslation = value;
            save("amberMorpheBypassTranslation", value);
        }
    }
}

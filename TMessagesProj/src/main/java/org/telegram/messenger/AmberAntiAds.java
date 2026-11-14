package org.telegram.messenger;

/*
 * AmberGram fork: anti-nag bundle, inspired by the community "Morphe"
 * patches (HushTelegram etc.). Central toggles for:
 *  - noSponsored       — never fetch or render sponsored messages (channel ads)
 *  - noRecommendations — never render the channel recommendations card
 *  - noGreetings       — hide greeting sticker suggestions / intro cards in empty chats
 *  - turboDownload     — always use the big 512 KB chunks with 8 parallel requests
 *                        (the params official Telegram reserves for experimental builds)
 * All flags are global (all accounts), stored in the main settings prefs.
 */

import android.content.SharedPreferences;

public class AmberAntiAds {

    private static final Object lock = new Object();
    private static Boolean noSponsored;
    private static Boolean noRecommendations;
    private static Boolean noGreetings;
    private static Boolean turboDownload;

    public static boolean noSponsored() {
        Boolean value = noSponsored;
        if (value == null) {
            synchronized (lock) {
                if (noSponsored == null) {
                    SharedPreferences preferences = MessagesController.getGlobalMainSettings();
                    noSponsored = preferences.getBoolean("amberNoSponsored", true);
                }
                value = noSponsored;
            }
        }
        return value;
    }

    public static void setNoSponsored(boolean value) {
        synchronized (lock) {
            noSponsored = value;
            MessagesController.getGlobalMainSettings().edit().putBoolean("amberNoSponsored", value).apply();
        }
    }

    public static boolean noRecommendations() {
        Boolean value = noRecommendations;
        if (value == null) {
            synchronized (lock) {
                if (noRecommendations == null) {
                    SharedPreferences preferences = MessagesController.getGlobalMainSettings();
                    noRecommendations = preferences.getBoolean("amberNoRecommendations", true);
                }
                value = noRecommendations;
            }
        }
        return value;
    }

    public static void setNoRecommendations(boolean value) {
        synchronized (lock) {
            noRecommendations = value;
            MessagesController.getGlobalMainSettings().edit().putBoolean("amberNoRecommendations", value).apply();
        }
    }

    public static boolean noGreetings() {
        Boolean value = noGreetings;
        if (value == null) {
            synchronized (lock) {
                if (noGreetings == null) {
                    SharedPreferences preferences = MessagesController.getGlobalMainSettings();
                    noGreetings = preferences.getBoolean("amberNoGreetings", true);
                }
                value = noGreetings;
            }
        }
        return value;
    }

    public static void setNoGreetings(boolean value) {
        synchronized (lock) {
            noGreetings = value;
            MessagesController.getGlobalMainSettings().edit().putBoolean("amberNoGreetings", value).apply();
        }
    }

    public static boolean turboDownload() {
        Boolean value = turboDownload;
        if (value == null) {
            synchronized (lock) {
                if (turboDownload == null) {
                    SharedPreferences preferences = MessagesController.getGlobalMainSettings();
                    turboDownload = preferences.getBoolean("amberTurboDownload", false);
                }
                value = turboDownload;
            }
        }
        return value;
    }

    public static void setTurboDownload(boolean value) {
        synchronized (lock) {
            turboDownload = value;
            MessagesController.getGlobalMainSettings().edit().putBoolean("amberTurboDownload", value).apply();
        }
    }
}

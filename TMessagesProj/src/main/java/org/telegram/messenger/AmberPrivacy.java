package org.telegram.messenger;

/*
 * AmberGram fork (round 19 — features from rival forks): privacy pack.
 * Source inspiration: Mercurygram (MgLinkPreview, MgUrlCleaner, disabled
 * global search, disabled AI endpoints), HushTelegram Morphe patches.
 * Flags are global (all accounts), stored in the main settings prefs.
 *  - disableLinkPreviews  — never ask the server for link previews of the
 *                           text being composed (kills account.getWebPagePreview
 *                           before-send leak; the message itself still carries
 *                           the server-side preview when sent)
 *  - disableGlobalSearch  — the chat-list search and the filtered search view
 *                           no longer query messages.searchGlobal; only local
 *                           results are shown
 *  - disableAiFeatures    — hides/disables the AI text editor and the
 *                           summarize endpoints (composeMessageWithAI /
 *                           summarizeText never leave the device)
 *  - stripLinkTracking    — tracking parameters (utm_*, gclid, fbclid, ...)
 *                           are removed from links before they are opened
 *                           in the browser
 */
public class AmberPrivacy {

    private static final Object lock = new Object();
    private static Boolean disableLinkPreviews;
    private static Boolean disableGlobalSearch;
    private static Boolean disableAiFeatures;
    private static Boolean stripLinkTracking;

    private static boolean load(String key, boolean defaultValue) {
        return MessagesController.getGlobalMainSettings().getBoolean(key, defaultValue);
    }

    private static void save(String key, boolean value) {
        MessagesController.getGlobalMainSettings().edit().putBoolean(key, value).apply();
    }

    public static boolean disableLinkPreviews() {
        Boolean value = disableLinkPreviews;
        if (value == null) {
            synchronized (lock) {
                value = load("amberDisableLinkPreviews", false);
                disableLinkPreviews = value;
            }
        }
        return value;
    }

    public static void setDisableLinkPreviews(boolean value) {
        synchronized (lock) {
            disableLinkPreviews = value;
            save("amberDisableLinkPreviews", value);
        }
    }

    public static boolean disableGlobalSearch() {
        Boolean value = disableGlobalSearch;
        if (value == null) {
            synchronized (lock) {
                value = load("amberDisableGlobalSearch", false);
                disableGlobalSearch = value;
            }
        }
        return value;
    }

    public static void setDisableGlobalSearch(boolean value) {
        synchronized (lock) {
            disableGlobalSearch = value;
            save("amberDisableGlobalSearch", value);
        }
    }

    public static boolean disableAiFeatures() {
        Boolean value = disableAiFeatures;
        if (value == null) {
            synchronized (lock) {
                value = load("amberDisableAiFeatures", false);
                disableAiFeatures = value;
            }
        }
        return value;
    }

    public static void setDisableAiFeatures(boolean value) {
        synchronized (lock) {
            disableAiFeatures = value;
            save("amberDisableAiFeatures", value);
        }
    }

    public static boolean stripLinkTracking() {
        Boolean value = stripLinkTracking;
        if (value == null) {
            synchronized (lock) {
                value = load("amberStripLinkTracking", false);
                stripLinkTracking = value;
            }
        }
        return value;
    }

    public static void setStripLinkTracking(boolean value) {
        synchronized (lock) {
            stripLinkTracking = value;
            save("amberStripLinkTracking", value);
        }
    }

    /**
     * Removes common tracking parameters from a URL (MgUrlCleaner-style).
     * Returns the original string when nothing matches or parsing fails.
     */
    public static String cleanTrackingParams(String url) {
        if (url == null || url.isEmpty()) {
            return url;
        }
        try {
            int queryStart = url.indexOf('?');
            if (queryStart < 0) {
                return url;
            }
            String base = url.substring(0, queryStart);
            String query = url.substring(queryStart + 1);
            if (query.isEmpty()) {
                return url;
            }
            String fragment = null;
            int fragmentIndex = query.indexOf('#');
            if (fragmentIndex >= 0) {
                fragment = query.substring(fragmentIndex);
                query = query.substring(0, fragmentIndex);
            }
            StringBuilder kept = new StringBuilder();
            for (String pair : query.split("&")) {
                if (pair.isEmpty()) {
                    continue;
                }
                String name = pair;
                int eq = pair.indexOf('=');
                if (eq >= 0) {
                    name = pair.substring(0, eq);
                }
                String lower = name.toLowerCase();
                boolean tracked = lower.startsWith("utm_")
                        || lower.equals("gclid") || lower.equals("fbclid") || lower.equals("yclid")
                        || lower.equals("msclkid") || lower.equals("mc_eid") || lower.equals("igshid")
                        || lower.equals("igsh") || lower.equals("si") || lower.equals("ref_src")
                        || lower.equals("ref_url") || lower.equals("ref") || lower.equals("spm")
                        || lower.equals("s") && false || lower.equals("twclid") || lower.equals("wbraid")
                        || lower.equals("gbraid") || lower.equals("dclid") || lower.equals("vero_id")
                        || lower.equals("vero_conv") || lower.equals("_hsenc") || lower.equals("_hsmi")
                        || lower.equals("mkt_tok") || lower.equals("pk_campaign") || lower.equals("pk_kwd");
                if (!tracked) {
                    if (kept.length() > 0) {
                        kept.append('&');
                    }
                    kept.append(pair);
                }
            }
            if (kept.length() == 0) {
                return fragment != null ? base + fragment : base;
            }
            return base + "?" + kept + (fragment != null ? fragment : "");
        } catch (Throwable ignore) {
            return url;
        }
    }
}

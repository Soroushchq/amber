package org.telegram.messenger;

/*
 * AmberGram fork (round 19 — features from rival forks): chat UX tweaks.
 * Source inspiration: Nagram (DoubleTap.kt, showRepeat/showNoQuoteForward),
 * forkgram (go to first message), NekoX lineage (showMessageID).
 * Flags are global (all accounts), stored in the main settings prefs.
 *  - doubleTapIncoming / doubleTapOutgoing — action performed on
 *    double-tapping a message instead of the stock reaction:
 *    0 = stock reaction (default), 1 = repeat (send as own message),
 *    2 = forward without quote, 3 = copy text
 */
public class AmberChatTweaks {

    public static final int DOUBLE_TAP_REACTION = 0;
    public static final int DOUBLE_TAP_REPEAT = 1;
    public static final int DOUBLE_TAP_FORWARD_NO_QUOTE = 2;
    public static final int DOUBLE_TAP_COPY = 3;

    private static final String KEY_INCOMING = "amberDoubleTapIncoming";
    private static final String KEY_OUTGOING = "amberDoubleTapOutgoing";

    private static Integer doubleTapIncoming;
    private static Integer doubleTapOutgoing;

    private static int load(String key, int defaultValue) {
        return MessagesController.getGlobalMainSettings().getInt(key, defaultValue);
    }

    private static void save(String key, int value) {
        MessagesController.getGlobalMainSettings().edit().putInt(key, value).apply();
    }

    public static int doubleTapIncoming() {
        Integer value = doubleTapIncoming;
        if (value == null) {
            value = load(KEY_INCOMING, DOUBLE_TAP_REACTION);
            doubleTapIncoming = value;
        }
        return value;
    }

    public static void setDoubleTapIncoming(int value) {
        doubleTapIncoming = value;
        save(KEY_INCOMING, value);
    }

    public static int doubleTapOutgoing() {
        Integer value = doubleTapOutgoing;
        if (value == null) {
            value = load(KEY_OUTGOING, DOUBLE_TAP_REACTION);
            doubleTapOutgoing = value;
        }
        return value;
    }

    public static void setDoubleTapOutgoing(int value) {
        doubleTapOutgoing = value;
        save(KEY_OUTGOING, value);
    }

    public static void resetCache() {
        doubleTapIncoming = null;
        doubleTapOutgoing = null;
    }
}

package org.telegram.messenger;

import android.content.SharedPreferences;

import java.util.HashSet;
import java.util.Set;

/*
 * AmberGram fork (round 19 — features from rival forks): extras.
 * Source inspiration: Hari-sys786 telegram-patches (upload speed boost,
 * same 512K-chunk trick the Morphe sources use), OctoGram/exteraGram
 * (hidden chats), Nnngram #63 (fork settings backup).
 * Flags are global (all accounts), stored in the main settings prefs.
 *  - turboUpload  — upload chunk sizes are doubled (the same trick the
 *                   download turbo already uses in AmberAntiAds)
 * Hidden chats are stored as a string set of dialog ids; locked dialogs
 * are hidden from the chat list and never raise notifications until the
 * user unlocks them from the management page.
 */
public class AmberExtras {

    private static final Object lock = new Object();
    private static final String KEY_LOCKED_DIALOGS = "amberLockedDialogs";
    private static Boolean turboUpload;
    private static Set<String> lockedDialogs;

    private static boolean load(String key, boolean defaultValue) {
        return MessagesController.getGlobalMainSettings().getBoolean(key, defaultValue);
    }

    private static void save(String key, boolean value) {
        MessagesController.getGlobalMainSettings().edit().putBoolean(key, value).apply();
    }

    public static boolean turboUpload() {
        Boolean value = turboUpload;
        if (value == null) {
            synchronized (lock) {
                value = load("amberTurboUpload", false);
                turboUpload = value;
            }
        }
        return value;
    }

    public static void setTurboUpload(boolean value) {
        synchronized (lock) {
            turboUpload = value;
            save("amberTurboUpload", value);
        }
    }

    private static SharedPreferences preferences() {
        return MessagesController.getGlobalMainSettings();
    }

    public static Set<String> getLockedDialogs() {
        synchronized (lock) {
            if (lockedDialogs == null) {
                lockedDialogs = new HashSet<>(preferences().getStringSet(KEY_LOCKED_DIALOGS, new HashSet<>()));
            }
            return new HashSet<>(lockedDialogs);
        }
    }

    public static boolean isDialogLocked(long dialogId) {
        synchronized (lock) {
            if (lockedDialogs == null) {
                lockedDialogs = new HashSet<>(preferences().getStringSet(KEY_LOCKED_DIALOGS, new HashSet<>()));
            }
            return lockedDialogs.contains(String.valueOf(dialogId));
        }
    }

    public static void setDialogLocked(long dialogId, boolean locked) {
        synchronized (lock) {
            if (lockedDialogs == null) {
                lockedDialogs = new HashSet<>(preferences().getStringSet(KEY_LOCKED_DIALOGS, new HashSet<>()));
            }
            Set<String> updated = new HashSet<>(lockedDialogs);
            if (locked) {
                updated.add(String.valueOf(dialogId));
            } else {
                updated.remove(String.valueOf(dialogId));
            }
            lockedDialogs = updated;
            preferences().edit().putStringSet(KEY_LOCKED_DIALOGS, updated).apply();
        }
    }

    public static int lockedDialogsCount() {
        return getLockedDialogs().size();
    }
}

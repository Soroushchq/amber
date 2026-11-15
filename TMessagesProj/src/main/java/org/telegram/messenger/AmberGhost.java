package org.telegram.messenger;

/*
 * AmberGram fork: ghost mode (v0.7.0 rework).
 *
 * While enabled:
 *  - typing indicators are never sent (MessagesController.sendTyping gate);
 *  - the account never shows as Online (TL_account.updateStatus is sent with
 *    offline=true);
 *  - read receipts are NOT sent to the server, but the unread counters ARE
 *    cleared locally, so the app looks and feels like a normal read for the
 *    user. The ids needed for the real server-side read are stashed here and
 *    replayed (flushRead) ONLY when:
 *      a) the user sends a message in that dialog (MessagesStorage.putMessages
 *         hook), or
 *      b) the user turns ghost mode off (setEnabled(false) flushes everything).
 *    Nothing is flushed on ChatActivity.onPause anymore — that used to flash
 *    the second read tick the moment the user left the chat / locked the screen.
 */

import android.content.SharedPreferences;

import java.util.ArrayList;
import java.util.HashMap;

public class AmberGhost {

    private static final Object lock = new Object();
    private static Boolean enabled;
    private static volatile long openDialog = 0;
    private static final HashMap<Long, PendingRead> pendingReads = new HashMap<>();

    public static class PendingRead {
        public long threadId;
        public int maxPositiveId;
        public int maxNegativeId;
        public int maxDate;
        public int scheduledCount;
    }

    public static boolean isEnabled() {
        Boolean value = enabled;
        if (value == null) {
            synchronized (lock) {
                if (enabled == null) {
                    SharedPreferences preferences = MessagesController.getGlobalMainSettings();
                    enabled = preferences.getBoolean("amberGhostMode", false);
                }
                value = enabled;
            }
        }
        return value;
    }

    public static void setEnabled(boolean value) {
        synchronized (lock) {
            enabled = value;
            MessagesController.getGlobalMainSettings().edit().putBoolean("amberGhostMode", value).apply();
        }
        if (!value) {
            // AmberGram v0.7.0: turning ghost OFF reveals everything the user read while
            // it was on — replay every stashed read receipt to the server.
            int account = UserConfig.selectedAccount;
            ArrayList<Long> dialogIds;
            synchronized (lock) {
                dialogIds = new ArrayList<>(pendingReads.keySet());
            }
            for (int a = 0; a < dialogIds.size(); a++) {
                try {
                    flushRead(dialogIds.get(a), account);
                } catch (Throwable ignore) {
                    // keep flushing the rest even if one replay fails
                }
            }
        }
    }

    public static void chatOpened(long dialogId) {
        openDialog = dialogId;
    }

    public static void chatClosed(long dialogId) {
        if (openDialog == dialogId) {
            openDialog = 0;
        }
    }

    /** Stashes the ids of a read that must not reach the server yet (ghost enabled). */
    public static void stashRead(long dialogId, int maxPositiveId, int maxNegativeId, int maxDate, long threadId, int scheduledCount) {
        synchronized (lock) {
            PendingRead pending = pendingReads.get(dialogId);
            if (pending == null) {
                pending = new PendingRead();
                pendingReads.put(dialogId, pending);
            }
            pending.maxPositiveId = maxPositiveId;
            pending.maxNegativeId = maxNegativeId;
            pending.maxDate = maxDate;
            pending.threadId = threadId;
            pending.scheduledCount = scheduledCount;
        }
    }

    /** True when this dialog has a stashed read waiting to be flushed. */
    public static boolean hasStash(long dialogId) {
        synchronized (lock) {
            return pendingReads.containsKey(dialogId);
        }
    }

    /**
     * Replays the stashed read receipt for one dialog to the server. Safe to call from
     * any thread (the MessagesController posts its work onto the proper queues).
     * Returns true when a stash existed and was flushed.
     */
    public static boolean flushRead(long dialogId, int account) {
        PendingRead pending;
        synchronized (lock) {
            pending = pendingReads.remove(dialogId);
        }
        if (pending == null) {
            return false;
        }
        MessagesController.getInstance(account).amberGhostMarkDialogAsRead(
                dialogId,
                pending.maxPositiveId,
                pending.maxNegativeId,
                pending.maxDate,
                false,
                pending.threadId,
                0,
                true,
                pending.scheduledCount,
                true
        );
        return true;
    }
}

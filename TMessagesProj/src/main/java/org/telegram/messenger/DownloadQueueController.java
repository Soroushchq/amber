package org.telegram.messenger;

import android.app.DownloadManager;
import android.content.ContentValues;
import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.provider.MediaStore;
import android.text.TextUtils;
import android.util.Base64;
import android.webkit.MimeTypeMap;

import org.telegram.tgnet.ConnectionsManager;
import org.telegram.tgnet.SerializedData;
import org.telegram.tgnet.TLRPC;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.nio.channels.FileChannel;
import java.util.ArrayList;

/**
 * Amber fork: strictly sequential download queue, hardened edition.
 *
 * The user selects multiple files in a chat (multi-select -> "sequential download")
 * and they are downloaded ONE AT A TIME, in order, backed by a foreground
 * dataSync service so the queue keeps running while the screen is locked.
 * The queue is persisted to SharedPreferences (the TLRPC.Document itself is
 * serialized) so it survives process death and resumes on next app start.
 *
 * Robustness rules (v0.6.0 rework — fixes the "small attempt then gives up"
 * and "queue ends after the first file" complaints):
 *  - Transient failures are RETRIED automatically: each item gets up to
 *    MAX_ATTEMPTS attempts with exponential backoff (2s .. 120s cap). While an
 *    item waits for its next attempt, the rest of the queue keeps flowing.
 *  - The queue is network-aware: items only start when the MTProto connection
 *    is actually established; otherwise the controller polls every 5 seconds
 *    instead of starting downloads that are doomed to fail immediately.
 *  - A stall watchdog cancels and re-queues the current item when no bytes
 *    arrive for 90 seconds (frozen proxy connections), counting as an attempt.
 *  - Failed items are NEVER silently erased: they stay in the queue marked
 *    FAILED (with a manual Retry button), also after an app restart, until the
 *    user clears them. Only DONE items are removed when the queue drains.
 *  - The currently downloading item is kept OUT of the waiting list, so the
 *    persisted queue never contains duplicates of the active item (the old
 *    build persisted it twice, which re-queued the same file after restart).
 */
public class DownloadQueueController implements NotificationCenter.NotificationCenterDelegate {

    public static final int STATE_PENDING = 0;
    public static final int STATE_DOWNLOADING = 1;
    public static final int STATE_DONE = 2;
    public static final int STATE_FAILED = 3;

    /** AmberGram: listener for UI (AmbergramSettingsActivity) to reflect queue changes live. */
    public interface QueueListener {
        void onQueueUpdated();
    }

    private static volatile DownloadQueueController[] Instance = new DownloadQueueController[UserConfig.MAX_ACCOUNT_COUNT];

    public static DownloadQueueController getInstance(int num) {
        DownloadQueueController localInstance = Instance[num];
        if (localInstance == null) {
            synchronized (DownloadQueueController.class) {
                localInstance = Instance[num];
                if (localInstance == null) {
                    Instance[num] = localInstance = new DownloadQueueController(num);
                }
            }
        }
        return localInstance;
    }

    public static class QueueItem {
        public long dialogId;
        public int messageId;
        public String fileName;
        public String displayName;
        public long size;
        public long loadedBytes;
        public int state = STATE_PENDING;
        /** How many download attempts this item already used (resets on manual retry). */
        public int attempts;
        /** Earliest time (System.currentTimeMillis()) this item may be started again. */
        public long retryAt;
        String documentBase64;

        QueueItem(long dialogId, int messageId, String fileName, String displayName, long size, TLRPC.Document document) {
            this.dialogId = dialogId;
            this.messageId = messageId;
            this.fileName = fileName;
            this.displayName = displayName;
            this.size = size;
            this.documentBase64 = documentToString(document);
        }
    }

    /** Retry policy: up to MAX_ATTEMPTS automatic attempts, exponential backoff (ms). */
    private static final int MAX_ATTEMPTS = 8;
    private static final long[] RETRY_DELAYS_MS = {2000, 4000, 8000, 15000, 30000, 60000, 120000};
    /** How often the controller re-checks the network while it is down (ms). */
    private static final long NETWORK_POLL_MS = 5000;
    /** Watchdog cadence and the no-progress threshold that counts as a stall (ms). */
    private static final long WATCHDOG_INTERVAL_MS = 15000;
    private static final long STALL_THRESHOLD_MS = 90000;

    private final int currentAccount;
    /** Waiting items: PENDING (ready or waiting for retryAt) and FAILED (visible until cleared). */
    private final ArrayList<QueueItem> queue = new ArrayList<>();
    /** The item being downloaded right now — kept OUT of {@link #queue}. */
    private QueueItem current;
    private AmberDownloadService attachedService;
    private long lastNotifyTime;
    private final ArrayList<QueueListener> queueListeners = new ArrayList<>();

    /** Highest loadedBytes seen for the current item; drives the stall watchdog. */
    private long currentLoadedHighWater;
    /** Last time the current item made visible progress. */
    private long lastProgressTime;

    private boolean kickScheduled;
    private boolean networkPollScheduled;
    private boolean watchdogScheduled;

    private final Runnable networkPollRunnable = () -> {
        networkPollScheduled = false;
        startNextIfNeeded();
    };
    private final Runnable watchdogRunnable = () -> {
        watchdogScheduled = false;
        checkCurrentStalled();
    };

    public void addQueueListener(QueueListener listener) {
        synchronized (queueListeners) {
            if (!queueListeners.contains(listener)) {
                queueListeners.add(listener);
            }
        }
        listener.onQueueUpdated();
    }

    public void removeQueueListener(QueueListener listener) {
        synchronized (queueListeners) {
            queueListeners.remove(listener);
        }
    }

    private void notifyQueueListeners() {
        QueueListener[] local;
        synchronized (queueListeners) {
            local = queueListeners.toArray(new QueueListener[0]);
        }
        for (int a = 0; a < local.length; a++) {
            try {
                local[a].onQueueUpdated();
            } catch (Throwable e) {
                FileLog.e(e);
            }
        }
    }

    /** Returns a copy of the queue: the downloading item first, then waiting/failed items. Must be called on the UI thread. */
    public ArrayList<QueueItem> getQueueSnapshot() {
        ArrayList<QueueItem> all = new ArrayList<>();
        if (current != null) {
            all.add(current);
        }
        all.addAll(queue);
        return all;
    }

    /** Removes a PENDING (waiting) item from the queue. Returns true if removed. */
    public boolean cancelPendingItem(QueueItem item) {
        boolean removed = false;
        for (int a = queue.size() - 1; a >= 0; a--) {
            QueueItem queued = queue.get(a);
            if (queued.state == STATE_PENDING && queued.messageId == item.messageId && queued.dialogId == item.dialogId && queued.fileName.equals(item.fileName)) {
                queue.remove(a);
                removed = true;
            }
        }
        if (removed) {
            persist();
            updateNotification(true);
        }
        return removed;
    }

    /** Manual retry: turns a FAILED item back into a fresh PENDING one. */
    public void retryItem(QueueItem item) {
        boolean found = false;
        for (int a = 0; a < queue.size(); a++) {
            QueueItem queued = queue.get(a);
            if (queued.state == STATE_FAILED && queued.messageId == item.messageId && queued.dialogId == item.dialogId && queued.fileName.equals(item.fileName)) {
                queued.state = STATE_PENDING;
                queued.attempts = 0;
                queued.retryAt = 0;
                queued.loadedBytes = 0;
                found = true;
            }
        }
        if (found) {
            persist();
            startNextIfNeeded();
        }
    }

    /** Removes all DONE/FAILED items from the queue. */
    public void removeFinished() {
        boolean removed = false;
        for (int a = queue.size() - 1; a >= 0; a--) {
            QueueItem item = queue.get(a);
            if (item.state == STATE_DONE || item.state == STATE_FAILED) {
                queue.remove(a);
                removed = true;
            }
        }
        if (removed) {
            persist();
            updateNotification(true);
        }
    }

    private DownloadQueueController(int account) {
        currentAccount = account;
        loadQueue();
        NotificationCenter.getInstance(currentAccount).addObserver(this, NotificationCenter.fileLoaded);
        NotificationCenter.getInstance(currentAccount).addObserver(this, NotificationCenter.fileLoadFailed);
        NotificationCenter.getInstance(currentAccount).addObserver(this, NotificationCenter.fileLoadProgressChanged);
    }

    /** Called once on app init: loads persisted queues and resumes any pending downloads. */
    public static void resumeAllQueues() {
        for (int a = 0; a < UserConfig.MAX_ACCOUNT_COUNT; a++) {
            if (!UserConfig.getInstance(a).isClientActivated()) {
                continue;
            }
            DownloadQueueController controller = getInstance(a);
            if (!controller.queue.isEmpty() || controller.current != null) {
                controller.startNextIfNeeded();
            }
        }
    }

    /**
     * Adds the given message objects (documents/videos/music) to the queue.
     * Returns the number of items actually added. Must be called on the UI thread.
     */
    public int enqueue(ArrayList<MessageObject> messageObjects) {
        int added = 0;
        for (int a = 0; a < messageObjects.size(); a++) {
            MessageObject messageObject = messageObjects.get(a);
            TLRPC.Document document = messageObject.getDocument();
            if (document == null) {
                continue;
            }
            String fileName = FileLoader.getAttachFileName(document);
            if (TextUtils.isEmpty(fileName) || fileName.contains("" + Integer.MIN_VALUE)) {
                continue;
            }
            if (hasActiveItemForFileName(fileName)) {
                continue;
            }
            String displayName = FileLoader.getDocumentFileName(document);
            if (TextUtils.isEmpty(displayName)) {
                displayName = fileName;
            }
            queue.add(new QueueItem(messageObject.getDialogId(), messageObject.getId(), fileName, displayName, document.size, document));
            added++;
        }
        if (added > 0) {
            persist();
            startNextIfNeeded();
        }
        return added;
    }

    /** Cancels the whole queue (current download included) and stops the service. */
    public void cancelAll() {
        if (current != null) {
            TLRPC.Document document = stringToDocument(current.documentBase64);
            if (document != null) {
                FileLoader.getInstance(currentAccount).cancelLoadFile(document);
            }
            current = null;
        }
        queue.clear();
        persist();
        AmberDownloadService.stop(ApplicationLoader.applicationContext);
        updateNotification(true);
    }

    /** True if a PENDING/DOWNLOADING/FAILED item with this name exists (so re-selecting a failed file is deduped too). */
    private boolean hasActiveItemForFileName(String fileName) {
        if (current != null && fileName.equals(current.fileName)) {
            return true;
        }
        for (int a = 0; a < queue.size(); a++) {
            QueueItem item = queue.get(a);
            if (fileName.equals(item.fileName)) {
                return true;
            }
        }
        return false;
    }

    /**
     * AmberGram: true when there is nothing actually in flight — no current download
     * and no pending items. FAILED items do not keep the service alive.
     * While idle the app must behave like regular Telegram:
     * no foreground service, no ongoing notification, no battery drain.
     */
    public boolean isIdle() {
        return current == null && !hasPendingItems();
    }

    private boolean hasPendingItems() {
        for (int a = 0; a < queue.size(); a++) {
            QueueItem item = queue.get(a);
            if (item.state == STATE_PENDING) {
                return true;
            }
        }
        return false;
    }

    private boolean isNetworkConnected() {
        try {
            return ConnectionsManager.getInstance(currentAccount).getConnectionState() == ConnectionsManager.ConnectionStateConnected;
        } catch (Throwable e) {
            return true;
        }
    }

    private void scheduleKick(long delayMs) {
        if (kickScheduled) {
            return;
        }
        kickScheduled = true;
        AndroidUtilities.runOnUIThread(() -> {
            kickScheduled = false;
            startNextIfNeeded();
        }, Math.max(500, Math.min(delayMs, 2 * NETWORK_POLL_MS)));
    }

    private long retryDelayFor(int attempts) {
        int idx = Math.min(attempts - 1, RETRY_DELAYS_MS.length - 1);
        return RETRY_DELAYS_MS[Math.max(0, idx)];
    }

    /**
     * Starts the next item when nothing is downloading. Handles three waiting
     * modes: an item ready to start, items waiting for their retry backoff, and
     * no usable network (poll instead of failing instantly).
     */
    private void startNextIfNeeded() {
        if (current != null) {
            ensureWatchdog();
            updateNotification(true);
            return;
        }
        QueueItem next = null;
        long now = System.currentTimeMillis();
        long earliestRetryAt = Long.MAX_VALUE;
        for (int a = 0; a < queue.size(); a++) {
            QueueItem item = queue.get(a);
            if (item.state != STATE_PENDING) {
                continue;
            }
            if (item.retryAt > now) {
                earliestRetryAt = Math.min(earliestRetryAt, item.retryAt);
                continue;
            }
            if (next == null) {
                next = item;
            }
        }
        if (next == null) {
            if (earliestRetryAt != Long.MAX_VALUE) {
                // All pending items are in their backoff window — wake up then.
                updateNotification(true);
                scheduleKick(earliestRetryAt - now);
                return;
            }
            // Queue drained: drop DONE items, keep FAILED ones visible for the user.
            for (int a = queue.size() - 1; a >= 0; a--) {
                if (queue.get(a).state == STATE_DONE) {
                    queue.remove(a);
                }
            }
            persist();
            AmberDownloadService.stop(ApplicationLoader.applicationContext);
            updateNotification(true);
            return;
        }
        if (!isNetworkConnected()) {
            // Do not start downloads that are doomed to fail right now; poll instead.
            updateNotification(true);
            if (!networkPollScheduled) {
                networkPollScheduled = true;
                AndroidUtilities.runOnUIThread(networkPollRunnable, NETWORK_POLL_MS);
            }
            return;
        }
        queue.remove(next);
        current = next;
        current.state = STATE_DOWNLOADING;
        current.attempts++;
        currentLoadedHighWater = 0;
        lastProgressTime = System.currentTimeMillis();
        persist();
        AmberDownloadService.start(ApplicationLoader.applicationContext, currentAccount);
        ensureWatchdog();

        TLRPC.Document document = stringToDocument(current.documentBase64);
        if (document == null) {
            failCurrent(current, false);
            return;
        }
        String checkName = FileLoader.getAttachFileName(document);
        if (TextUtils.isEmpty(checkName) || checkName.contains("" + Integer.MIN_VALUE) || checkName.startsWith("0_0")) {
            // FileLoader would silently refuse this one — mark failed right away
            // instead of leaving a permanently "downloading" item.
            failCurrent(current, false);
            return;
        }
        File cached = FileLoader.getInstance(currentAccount).getPathToAttach(document);
        if (cached != null && cached.exists()) {
            finishCurrentWithFile(cached);
            return;
        }
        FileLoader.getInstance(currentAccount).loadFile(document, null, FileLoader.PRIORITY_NORMAL, 0);
        updateNotification(true);
    }

    /**
     * Finishes or retries the current item. Only acts if {@code item} is still the
     * current one (protects against late/cancel events).
     */
    private void failCurrent(QueueItem item, boolean retriable) {
        if (current != item || item == null) {
            return;
        }
        current = null;
        if (retriable && item.attempts < MAX_ATTEMPTS) {
            requeueForRetry(item);
        } else {
            markItemFailed(item);
        }
        persist();
        updateNotification(true);
        startNextIfNeeded();
        if (item.state == STATE_PENDING) {
            scheduleKick(item.retryAt - System.currentTimeMillis());
        }
    }

    /** Puts an item back into the waiting list with a backoff window (front keeps user order). */
    private void requeueForRetry(QueueItem item) {
        item.state = STATE_PENDING;
        item.retryAt = System.currentTimeMillis() + retryDelayFor(item.attempts);
        queue.add(0, item);
    }

    /** Out of attempts (or fatal error): keep the item visible as FAILED. */
    private void markItemFailed(QueueItem item) {
        item.state = STATE_FAILED;
        item.retryAt = 0;
        queue.add(0, item);
    }

    /** Watchdog: when the current item receives no bytes for a while, cancel and retry it. */
    private void checkCurrentStalled() {
        QueueItem item = current;
        if (item == null) {
            return;
        }
        long now = System.currentTimeMillis();
        if (now - lastProgressTime > STALL_THRESHOLD_MS) {
            TLRPC.Document document = stringToDocument(item.documentBase64);
            if (document != null) {
                FileLoader.getInstance(currentAccount).cancelLoadFile(document);
            }
            // The late fileLoadFailed event is ignored (current is already null / different item).
            failCurrent(item, true);
        } else {
            ensureWatchdog();
        }
    }

    private void ensureWatchdog() {
        if (watchdogScheduled || current == null) {
            return;
        }
        watchdogScheduled = true;
        AndroidUtilities.runOnUIThread(watchdogRunnable, WATCHDOG_INTERVAL_MS);
    }

    private void finishCurrentWithFile(File finalFile) {
        final QueueItem item = current;
        updateNotification(true);
        Utilities.globalQueue.postRunnable(() -> {
            final boolean ok = copyToPublicDownloadsSafely(item, finalFile);
            AndroidUtilities.runOnUIThread(() -> {
                if (current == item) {
                    current = null;
                    if (ok) {
                        item.state = STATE_DONE;
                        item.retryAt = 0;
                        persist();
                        startNextIfNeeded();
                    } else {
                        // The Telegram-side download succeeded but the copy into
                        // public storage failed — same requeue/failed logic as
                        // failCurrent (which cannot be used here: current is gone).
                        if (item.attempts < MAX_ATTEMPTS) {
                            requeueForRetry(item);
                        } else {
                            markItemFailed(item);
                        }
                        persist();
                        updateNotification(true);
                        startNextIfNeeded();
                        if (item.state == STATE_PENDING) {
                            scheduleKick(item.retryAt - System.currentTimeMillis());
                        }
                    }
                }
            });
        });
    }

    private boolean copyToPublicDownloadsSafely(QueueItem item, File finalFile) {
        try {
            return copyToPublicDownloads(item, finalFile);
        } catch (Throwable e) {
            FileLog.e(e);
            return false;
        }
    }

    /** Copies the downloaded file into public Downloads/Telegram and registers it with the system. */
    private boolean copyToPublicDownloads(QueueItem item, File sourceFile) throws Throwable {
        if (sourceFile == null || !sourceFile.exists()) {
            return false;
        }
        String name = !TextUtils.isEmpty(item.displayName) ? item.displayName : item.fileName;
        if (Build.VERSION.SDK_INT >= 29) {
            return copyToPublicDownloadsQ(sourceFile, name);
        }
        return copyToPublicDownloadsLegacy(name, sourceFile);
    }

    private String mimeForName(String name) {
        try {
            MimeTypeMap mimeTypeMap = MimeTypeMap.getSingleton();
            int idx = name.lastIndexOf('.');
            String extension = idx >= 0 ? name.substring(idx + 1) : "";
            String mime = mimeTypeMap.getMimeTypeFromExtension(extension.toLowerCase());
            if (TextUtils.isEmpty(mime)) {
                return "application/octet-stream";
            }
            return mime;
        } catch (Throwable e) {
            return "application/octet-stream";
        }
    }

    /** Scoped storage path for Android 10+: goes through MediaStore.Downloads. */
    private boolean copyToPublicDownloadsQ(File sourceFile, String name) throws Throwable {
        ContentValues values = new ContentValues();
        values.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
        values.put(MediaStore.MediaColumns.MIME_TYPE, mimeForName(name));
        values.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/Telegram");
        Uri uri = ApplicationLoader.applicationContext.getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
        if (uri == null) {
            return false;
        }
        try (FileInputStream inputStream = new FileInputStream(sourceFile); OutputStream outputStream = ApplicationLoader.applicationContext.getContentResolver().openOutputStream(uri)) {
            if (outputStream == null) {
                return false;
            }
            byte[] buffer = new byte[1024 * 512];
            int read;
            while ((read = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, read);
            }
            outputStream.flush();
        }
        return true;
    }

    /** Legacy direct-file path for Android 9 and below. */
    private boolean copyToPublicDownloadsLegacy(String name, File sourceFile) throws Throwable {
        File destDir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "Telegram");
        destDir.mkdirs();
        File destFile = new File(destDir, name);
        if (destFile.exists()) {
            destFile = new File(destDir, System.currentTimeMillis() + "_" + name);
        }
        try (FileInputStream inputStream = new FileInputStream(sourceFile); FileOutputStream outputStream = new FileOutputStream(destFile)) {
            FileChannel source = inputStream.getChannel();
            FileChannel destination = outputStream.getChannel();
            long size = source.size();
            for (long offset = 0; offset < size; offset += destination.transferFrom(source, offset, Math.min(4 * 1024 * 1024, size - offset))) {
                // sequential chunked copy
            }
            destination.force(true);
        }
        try {
            DownloadManager downloadManager = (DownloadManager) ApplicationLoader.applicationContext.getSystemService(Context.DOWNLOAD_SERVICE);
            downloadManager.addCompletedDownload(destFile.getName(), destFile.getName(), false, mimeForName(name), destFile.getAbsolutePath(), destFile.length(), true);
        } catch (Throwable ignore) {
            // best-effort registration only
        }
        return true;
    }

    private void updateNotification(boolean force) {
        AmberDownloadService service = attachedService;
        if (service == null) {
            return;
        }
        if (isIdle()) {
            // AmberGram: queue drained (or empty) — never post a progress notification.
            // The service is being stopped; its onDestroy() cancels the notification,
            // so nothing lingers in the shade while idle.
            return;
        }
        long now = System.currentTimeMillis();
        if (!force && now - lastNotifyTime < 400) {
            return;
        }
        lastNotifyTime = now;

        int total = queue.size() + (current != null ? 1 : 0);
        int finished = 0;
        int failed = 0;
        for (int a = 0; a < queue.size(); a++) {
            QueueItem item = queue.get(a);
            if (item.state == STATE_DONE) {
                finished++;
            } else if (item.state == STATE_FAILED) {
                failed++;
            }
        }
        String name = current != null && !TextUtils.isEmpty(current.displayName) ? current.displayName : "";
        long loaded = current != null ? current.loadedBytes : 0;
        long size = current != null ? current.size : 0;
        service.update(finished, total, name, loaded, size);
    }

    @Override
    public void didReceivedNotification(int id, int account, Object... args) {
        if (account != currentAccount) {
            return;
        }
        if (id == NotificationCenter.fileLoadProgressChanged) {
            if (current != null && current.fileName.equals(args[0])) {
                current.loadedBytes = (Long) args[1];
                if (current.loadedBytes > currentLoadedHighWater) {
                    currentLoadedHighWater = current.loadedBytes;
                    lastProgressTime = System.currentTimeMillis();
                }
                updateNotification(false);
                notifyQueueListeners();
            }
        } else if (id == NotificationCenter.fileLoaded) {
            if (current != null && current.fileName.equals(args[0])) {
                finishCurrentWithFile((File) args[1]);
            }
        } else if (id == NotificationCenter.fileLoadFailed) {
            if (current != null && current.fileName.equals(args[0])) {
                int reason = args.length > 1 && args[1] instanceof Integer ? (Integer) args[1] : 0;
                // reason -1 = out of disk space (fatal); everything else is retried with backoff.
                failCurrent(current, reason != -1);
            }
        }
    }

    private String persistName() {
        return "amber_queue_" + currentAccount;
    }

    private void persist() {
        try {
            SharedPreferences preferences = ApplicationLoader.applicationContext.getSharedPreferences(persistName(), Context.MODE_PRIVATE);
            org.json.JSONArray array = new org.json.JSONArray();
            ArrayList<QueueItem> all = new ArrayList<>();
            if (current != null) {
                all.add(current);
            }
            all.addAll(queue);
            for (int a = 0; a < all.size(); a++) {
                QueueItem item = all.get(a);
                org.json.JSONObject object = new org.json.JSONObject();
                object.put("dialogId", item.dialogId);
                object.put("msgId", item.messageId);
                object.put("fileName", item.fileName);
                object.put("displayName", item.displayName);
                object.put("size", item.size);
                object.put("loaded", item.loadedBytes);
                object.put("state", item.state);
                object.put("attempts", item.attempts);
                object.put("retryAt", item.retryAt);
                object.put("doc", item.documentBase64);
                array.put(object);
            }
            preferences.edit().putString("queue", array.toString()).apply();
        } catch (Throwable e) {
            FileLog.e(e);
        }
        notifyQueueListeners();
    }

    private void loadQueue() {
        try {
            SharedPreferences preferences = ApplicationLoader.applicationContext.getSharedPreferences(persistName(), Context.MODE_PRIVATE);
            String raw = preferences.getString("queue", null);
            if (TextUtils.isEmpty(raw)) {
                return;
            }
            org.json.JSONArray array = new org.json.JSONArray(raw);
            queue.clear();
            current = null;
            for (int a = 0; a < array.length(); a++) {
                org.json.JSONObject object = array.getJSONObject(a);
                QueueItem item = new QueueItem(
                        object.getLong("dialogId"),
                        object.getInt("msgId"),
                        object.getString("fileName"),
                        object.getString("displayName"),
                        object.getLong("size"),
                        stringToDocument(object.getString("doc"))
                );
                item.documentBase64 = object.getString("doc");
                item.state = object.optInt("state", STATE_PENDING);
                item.loadedBytes = object.optLong("loaded", 0);
                item.attempts = object.optInt("attempts", 0);
                item.retryAt = object.optLong("retryAt", 0);
                if (item.state == STATE_DOWNLOADING) {
                    // interrupted by process death: try again from the beginning
                    item.state = STATE_PENDING;
                    item.loadedBytes = 0;
                }
                if (item.state == STATE_PENDING || item.state == STATE_FAILED) {
                    queue.add(item);
                }
            }
        } catch (Throwable e) {
            FileLog.e(e);
            queue.clear();
        }
    }

    private static String documentToString(TLRPC.Document document) {
        if (document == null) {
            return null;
        }
        try {
            SerializedData serializedData = new SerializedData();
            document.serializeToStream(serializedData);
            return Base64.encodeToString(serializedData.toByteArray(), Base64.NO_WRAP);
        } catch (Throwable e) {
            FileLog.e(e);
            return null;
        }
    }

    private static TLRPC.Document stringToDocument(String base64) {
        if (TextUtils.isEmpty(base64)) {
            return null;
        }
        try {
            byte[] bytes = Base64.decode(base64, Base64.NO_WRAP);
            SerializedData serializedData = new SerializedData(bytes);
            return TLRPC.Document.TLdeserialize(serializedData, serializedData.readInt32(false), false);
        } catch (Throwable e) {
            FileLog.e(e);
            return null;
        }
    }

    void attachService(AmberDownloadService service) {
        attachedService = service;
        updateNotification(true);
    }

    void detachService(AmberDownloadService service) {
        if (attachedService == service) {
            attachedService = null;
        }
    }
}

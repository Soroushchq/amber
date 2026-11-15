# مرجع کامل کد سفارشی AmberGram — با توضیحات برای دیباگ

> این فایل «همه چیز» است: هر قابلیتی که از تلگرام رسمی 13.2.1 تا امروز ساخته/تغییر داده شده، با فایل‌ها، کد کامل و کاملِ دیف‌ها.
> وضعیت فعلی ریپو در لحظهٔ تولید این فایل: **v0.6.0-alpha (کد 7302)** — شاخه `master` ریپازیتوری `Soroushchq/amber`.
> بیس: کامیت `7be672ea` «update to 13.2.1 (7291)». همهٔ دیف‌های این سند با دستور `git diff 7be672ead HEAD -- <فایل>` قابل بازتولید هستند.

## فهرست

- بخش ۰ — نقشه کلی: همهٔ فایل‌های جدید و فایل‌های تغییر‌یافته
- بخش ۱ — **صف دانلود ترتیبی** (هدف اصلی دیباگ شما): معماری + کد کامل + گیت‌ها + راهنمای دیباگ
- بخش ۲ — بسته Morphe (`AmberMorphe` + ۸ گیت): ضدحذف، ضدتک‌بار، بدون اعلان اسکرین‌شات، ذخیره همه‌جا، بدون آپدیت، بدون سوییچ کانال، مخفی‌کردن بازدید استوری، ترجمه همیشه فعال
- بخش ۳ — بسته ضدتبلیغ + توربو (`AmberAntiAds`): بدون اسپانسری، بدون کانال پیشنهادی، بدون استیکر خوش‌آمد، توربو دانلود 1MB×12
- بخش ۴ — حالت شبح (`AmberGhost`)
- بخش ۵ — پروکسی رایگان درون‌برنامه‌ای (`AmbergramProxyManager` + `AmbergramProxyReceiver` + `AmbergramProxyActivity`)
- بخش ۶ — هاب تنظیمات (`AmbergramSettingsActivity`) + ردیفش در تنظیمات اصلی
- بخش ۷ — تم آمبر، فونت UI، برندسازی (rebrand)، آیکون‌ها
- بخش ۸ — زیرساخت فورک: api_id، نوع اکانت مخاطبین، `gradle.properties`، workflows کامل
- بخش ۹ — جدول کامل رشته‌های `Amber*` (انگلیسی + نمونه فارسی)
- بخش ۱۰ — آشپزخانه دیباگ: pref ها، ثابت‌ها، نقاط لاگ‌گذاری، سناریوهای تست دستی
- بخش ۱۱ — تاریخچه نسخه‌ها و پروتکل مغز دوم

---

# بخش ۰ — نقشه کلی

## فایل‌های جدید (10 فایل جاوا + منابع)

| # | فایل | نقش |
|---|------|-----|
| 1 | `TMessagesProj/src/main/java/org/telegram/messenger/DownloadQueueController.java` | مغز صف دانلود ترتیبی: صف، retry/backoff، watchdog شبکه، persist |
| 2 | `TMessagesProj/src/main/java/org/telegram/messenger/AmberDownloadService.java` | سرویس foreground (dataSync) برای ادامه صف در قفل صفحه |
| 3 | `TMessagesProj/src/main/java/org/telegram/ui/AmbergramQueueActivity.java` | صفحه اختصاصی صف (پیشرفت زنده، حذف آیتم، Retry، Cancel all) |
| 4 | `TMessagesProj/src/main/java/org/telegram/messenger/AmberMorphe.java` | ۸ toggle پک Morphe |
| 5 | `TMessagesProj/src/main/java/org/telegram/messenger/AmberAntiAds.java` | ۴ toggle ضدتبلیغ + توربو |
| 6 | `TMessagesProj/src/main/java/org/telegram/messenger/AmberGhost.java` | حالت شبح (تعویق رسید خواندن + قطع نشانگر تایپ) |
| 7 | `TMessagesProj/src/main/java/org/telegram/messenger/AmbergramProxyManager.java` | جمع‌آوری/تست/پاکسازی/اتصال پروکسی‌های رایگان |
| 8 | `TMessagesProj/src/main/java/org/telegram/messenger/AmbergramProxyReceiver.java` | گیرنده زنگ ۶ ساعته‌ی آلارم پروکسی |
| 9 | `TMessagesProj/src/main/java/org/telegram/ui/AmbergramProxyActivity.java` | صفحه لیست پروکسی‌ها |
| 10 | `TMessagesProj/src/main/java/org/telegram/ui/AmbergramSettingsActivity.java` | هاب تنظیمات AmberGram (۳ ردیف ناوبری + ۱۲ toggle) |

منابع جدید: `res/drawable/ic_ambergram_proxy.xml`، `res/drawable/ic_ambergram_settings.xml`، `assets/amber.attheme`، `assets/fonts/ambergramui.ttf`، آیکون‌های icon_7..12 (Leopard/Phoenix) در mipmap ها و drawable-nodpi، `.github/workflows/ci.yml` و `.github/workflows/release.yml`.

## فایل‌های اصلی تغییر‌یافته (دیف کامل در همین سند)

**برای صف دانلود:** `ChatActivity.java` (منوی «دانلود ترتیبی» در اکشن‌مود چندانتخابی)، `ApplicationLoader.java` (resumeAllQueues + onAppStart پروکسی)، `AndroidManifest.xml` (سرویس dataSync + receiver).

**برای Morphe:** `MessagesController.java` (antiDelete، bypassNoforwards، noSponsored)، `MessageObject.java` (antiDisappearing، bypassNoforwards)، `MediaController.java` (noScreenshotNotify)، `LaunchActivity.java` (noAutoUpdate)، `ChatActivity.java` (noChannelSwitch، noSponsored)، `StoriesController.java` (hideStoriesRead)، `TranslateController.java` (bypassTranslation).

**برای ضدتبلیغ:** `MessagesController.java`، `ChatActivity.java`، `ChatMessageCell.java` + توربو در `FileLoadOperation.java`.

**برای شبح:** `MessagesController.java` (sendTyping + markDialogAsRead wrapper)، `ChatActivity.java` (onResume/onPause).

**برای تم/برند:** `Theme.java` (تم Amber + پیش‌فرض‌سازی)، `AndroidUtilities.java` (فونت)، `TextStyleSpan.java`، `AlertDialog.java`، `TextCell/TextCheckCell/TextInfoPrivacyCell/TextSettingsCell`، `IntroActivity.java`، `LocaleController.java` (بازنویسی runtime پک‌های زبان)، `SessionsActivity.java`، `ThemePreviewActivity.java`، `LauncherIconController.java`، `AndroidManifest.xml` (۶ activity-alias آیکون).

**برای زیرساخت:** `BuildVars.java`، `ContactsController.java`، `gradle.properties`.

---

# بخش ۱ — صف دانلود ترتیبی (Sequential Download Queue)

## ۱-۱ معماری و جریان کامل

سه بازیگر اصلی + یک نقطه ورود:

```
ChatActivity (اکشن‌مود چندانتخابی)
   │  دکمه amber_queue (id=500، آیکون msg_list، متن AmberQueueMenu)
   ▼
DownloadQueueController.enqueue(messageObjects)      ← صف + persist + startNextIfNeeded
   │
   ▼
startNextIfNeeded()                                  ← تک‌خردی: هر بار فقط یک فایل
   │  سه شرط ورود: آیتم آماده؟ backoff تموم شده؟ شبکه وصل است؟
   ▼
FileLoader.loadFile(document, ...)                   ← دانلود واقعی تلگرام
   │  رویدادها (NotificationCenter):
   │   fileLoadProgressChanged → پیشرفت + watchdog
   │   fileLoaded              → کپی به Downloads/Telegram → DONE → فایل بعدی
   │   fileLoadFailed          → retry با backoff یا FAILED
   ▼
AmberDownloadService (foreground dataSync)           ← نوتیفیکیشن پیشرفت + نگه‌داشتن صف در قفل صفحه
```

قواعد مقاوم‌سازی (بازنویسی v0.6.0 که دقیقاً دو باگ شما را هدف گرفت):

| قاعده | مقدار | شرح |
|-------|-------|-----|
| حداکثر تلاش خودکار | `MAX_ATTEMPTS = 8` | هر آیتم تا ۸ بار خودش دوباره تلاش می‌کند |
| backoff نمایی | `{2000, 4000, 8000, 15000, 30000, 60000, 120000}` میلی‌ثانیه | بعد از هر شکست، مکث تا سقف ۲ دقیقه |
| آگاهی از شبکه | `NETWORK_POLL_MS = 5000` | تا وقتی `ConnectionsManager` متصل نیست، دانلود شروع نمی‌شود؛ هر ۵ ثانیه پول می‌زند |
| watchdog رکود | `WATCHDOG_INTERVAL_MS = 15000` / `STALL_THRESHOLD_MS = 90000` | اگر ۹۰ ثانیه حتی یک بایت نرسد، دانلود لغو و دوباره صف می‌شود |
| FAILED ماندگار | state=3 | آیتم شکست‌خورده هرگز بی‌صدا پاک نمی‌شود؛ در صفحه صف با دکمه Retry می‌ماند (حتی بعد از ری‌استارت) |
| جریان ادامه‌دار | `requeueForRetry` می‌گذارد در `queue.add(0, ...)` | حین انتظارِ یک آیتم، بقیه صف طبق ترتیب کاربر ادامه می‌یابند |
| رفع تکرار persist | current بیرون از list نگه داشته می‌شود | باگ قدیمی: آیتم فعال دوبار ذخیره می‌شد و بعد از ری‌استارت همان فایل دوباره صف می‌شد |

توضیح مهم درباره «صف درست نمی‌کند» قدیمی: قبل از v0.6.0، شکست → حذف بی‌صدا → `startNextIfNeeded` هم به دلیل شبکه قطع سریع fail می‌شد و کل صف در چند ثانیه خالی می‌شد. حالا شکست‌های گذرا به عنوان retry صف می‌شوند و اگر شبکه نیست هیچ دانلودی شروع نمی‌شود (پول ۵ ثانیه‌ای).

## ۱-۲ DownloadQueueController.java — کد کامل (801 خط)

مسیر: `TMessagesProj/src/main/java/org/telegram/messenger/DownloadQueueController.java`

```java
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
```


## ۱-۳ AmberDownloadService.java — کد کامل

مسیر: `TMessagesProj/src/main/java/org/telegram/messenger/AmberDownloadService.java`
سرویس foreground با نوع `dataSync`؛ نوتیف id=91231، کانال `amber_queue`، دکمه Cancel all. وقتی صف خالی شد `stopSelf()` می‌شود (رفتار idle مثل تلگرام معمولی: نه سرویس، نه نوتیف).

```java
package org.telegram.messenger;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;
import android.text.TextUtils;

/**
 * Amber fork: foreground service (dataSync) that keeps the sequential
 * download queue running while the phone is locked / the app is in background.
 */
public class AmberDownloadService extends Service {

    public static final String ACTION_CANCEL = "org.telegram.amber.QUEUE_CANCEL";
    public static final String EXTRA_ACCOUNT = "account";

    private static final int NOTIFICATION_ID = 91231;
    private static final String CHANNEL_ID = "amber_queue";

    private NotificationManager notificationManager;
    private int account = 0;

    public static void start(Context context, int account) {
        try {
            Intent intent = new Intent(context, AmberDownloadService.class);
            intent.putExtra(EXTRA_ACCOUNT, account);
            if (Build.VERSION.SDK_INT >= 26) {
                context.startForegroundService(intent);
            } else {
                context.startService(intent);
            }
        } catch (Throwable e) {
            // FGS launch restrictions when the app is in background: keep downloading anyway
            FileLog.e(e);
        }
    }

    public static void stop(Context context) {
        try {
            context.stopService(new Intent(context, AmberDownloadService.class));
        } catch (Throwable ignore) {
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        notificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, LocaleController.getString(R.string.AmberQueueNotificationTitle), NotificationManager.IMPORTANCE_LOW);
            channel.setShowBadge(false);
            notificationManager.createNotificationChannel(channel);
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        account = intent != null ? intent.getIntExtra(EXTRA_ACCOUNT, UserConfig.selectedAccount) : UserConfig.selectedAccount;
        if (intent != null && ACTION_CANCEL.equals(intent.getAction())) {
            try {
                startForeground(NOTIFICATION_ID, buildNotification(0, 0, "", 0, 0));
            } catch (Throwable ignore) {
            }
            DownloadQueueController.getInstance(account).cancelAll();
            stopSelf();
            return START_NOT_STICKY;
        }
        startForeground(NOTIFICATION_ID, buildNotification(0, 0, "", 0, 0));
        DownloadQueueController controller = DownloadQueueController.getInstance(account);
        controller.attachService(this);
        if (controller.isIdle()) {
            // AmberGram: sticky restart (or stray start) with nothing left in the queue —
            // do NOT linger as a foreground service with an empty notification.
            // Behave like regular Telegram: no download, no service, no notification.
            stopSelf();
        }
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        // AmberGram: always remove our progress notification when the service dies,
        // so a drained queue never leaves a stale "downloading" notification behind.
        if (notificationManager != null) {
            try {
                notificationManager.cancel(NOTIFICATION_ID);
            } catch (Throwable ignore) {
            }
        }
        DownloadQueueController.getInstance(account).detachService(this);
        super.onDestroy();
    }

    /** Called by the controller whenever queue progress changes. */
    public void update(int finished, int total, String name, long loadedBytes, long totalBytes) {
        try {
            notificationManager.notify(NOTIFICATION_ID, buildNotification(finished, total, name, loadedBytes, totalBytes));
        } catch (Throwable ignore) {
        }
    }

    private Notification buildNotification(int finished, int total, String name, long loadedBytes, long totalBytes) {
        Intent launchIntent = getPackageManager().getLaunchIntentForPackage(getPackageName());
        PendingIntent contentIntent = null;
        if (launchIntent != null) {
            contentIntent = PendingIntent.getActivity(this, 0, launchIntent, PendingIntent.FLAG_IMMUTABLE);
        }
        Intent cancelIntent = new Intent(this, AmberDownloadService.class);
        cancelIntent.setAction(ACTION_CANCEL);
        cancelIntent.putExtra(EXTRA_ACCOUNT, account);
        PendingIntent cancelPendingIntent = PendingIntent.getService(this, 1, cancelIntent, PendingIntent.FLAG_IMMUTABLE);

        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= 26) {
            builder = new Notification.Builder(this, CHANNEL_ID);
        } else {
            builder = new Notification.Builder(this);
        }
        builder.setSmallIcon(R.drawable.notification)
                .setColor(0xFFF97316)
                .setContentTitle(LocaleController.getString(R.string.AmberQueueNotificationTitle))
                .setOngoing(true)
                .setOnlyAlertOnce(true)
                .setContentIntent(contentIntent)
                .addAction(new Notification.Action.Builder(null, LocaleController.getString(R.string.AmberQueueCancelAll), cancelPendingIntent).build());

        StringBuilder text = new StringBuilder();
        if (total > 0) {
            text.append(LocaleController.formatString("AmberQueueProgressLine", R.string.AmberQueueProgressLine, finished, total));
        }
        if (!TextUtils.isEmpty(name)) {
            if (text.length() > 0) {
                text.append(" • ");
            }
            text.append(name);
        }
        boolean indeterminate = totalBytes <= 0;
        if (!indeterminate && totalBytes > 0 && loadedBytes > 0) {
            if (text.length() > 0) {
                text.append(" • ");
            }
            text.append(AndroidUtilities.formatFileSize(loadedBytes)).append(" / ").append(AndroidUtilities.formatFileSize(totalBytes));
        }
        builder.setContentText(text.length() > 0 ? text.toString() : null);
        builder.setProgress(100, indeterminate ? 0 : (int) (loadedBytes * 100 / Math.max(1, totalBytes)), indeterminate);
        return builder.build();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
```


## ۱-۴ AmbergramQueueActivity.java — کد کامل (صفحه صف)

مسیر: `TMessagesProj/src/main/java/org/telegram/ui/AmbergramQueueActivity.java`
رنگ وضعیت‌ها: نارنجی F97316 = در حال دانلود، سبز 27B434 = انجام‌شده، قرمز E13B47 = شکست. دکمه‌ها: Clear finished (نارنجی) و Cancel all (قرمز). رفرش UI با ۳۰۰ms debounce روی `onQueueUpdated`.

```java
package org.telegram.ui;

import android.content.Context;
import android.graphics.PorterDuff;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.DownloadQueueController;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;
import org.telegram.ui.Cells.HeaderCell;
import org.telegram.ui.Cells.TextInfoPrivacyCell;
import org.telegram.ui.Components.LayoutHelper;

import java.util.ArrayList;

/**
 * AmberGram fork: dedicated page for the sequential download queue.
 * Shows live progress of every queued item (per-item removal, clear finished,
 * cancel all). Opened from AmberGram Settings to keep the settings hub clean.
 */
public class AmbergramQueueActivity extends BaseFragment implements DownloadQueueController.QueueListener {

    private static final int BRAND_ORANGE = 0xFFF97316;
    private static final int STATE_GREEN = 0xFF27B434;
    private static final int STATE_RED = 0xFFE13B47;

    private LinearLayout queueContainer;
    private TextView summaryTextView;
    private TextView emptyTextView;
    private boolean updateScheduled;

    @Override
    public boolean onFragmentCreate() {
        DownloadQueueController.getInstance(currentAccount).addQueueListener(this);
        return super.onFragmentCreate();
    }

    @Override
    public void onFragmentDestroy() {
        DownloadQueueController.getInstance(currentAccount).removeQueueListener(this);
        super.onFragmentDestroy();
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(LocaleController.getString(R.string.AmbergramQueueSection));
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        fragmentView = new FrameLayout(context);
        ThemeBind.backgroundColor(fragmentView, Theme.key_windowBackgroundGray);

        ScrollView scrollView = new ScrollView(context);
        scrollView.setFillViewport(true);
        ((FrameLayout) fragmentView).addView(scrollView, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.MATCH_PARENT));

        LinearLayout contentWrapper = new LinearLayout(context);
        contentWrapper.setOrientation(LinearLayout.VERTICAL);
        scrollView.addView(contentWrapper, new ScrollView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        LinearLayout card = new LinearLayout(context);
        card.setOrientation(LinearLayout.VERTICAL);
        ThemeBind.backgroundColor(card, Theme.key_windowBackgroundWhite);
        contentWrapper.addView(card, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        summaryTextView = new TextView(context);
        summaryTextView.setTypeface(AndroidUtilities.bold());
        summaryTextView.setTextSize(13);
        ThemeBind.textColor(summaryTextView, Theme.key_windowBackgroundWhiteGrayText2, null);
        summaryTextView.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(12), AndroidUtilities.dp(21), AndroidUtilities.dp(8));
        summaryTextView.setVisibility(View.GONE);
        card.addView(summaryTextView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        queueContainer = new LinearLayout(context);
        queueContainer.setOrientation(LinearLayout.VERTICAL);
        card.addView(queueContainer, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        emptyTextView = new TextView(context);
        emptyTextView.setTypeface(AndroidUtilities.bold());
        emptyTextView.setTextSize(14);
        ThemeBind.textColor(emptyTextView, Theme.key_windowBackgroundWhiteGrayText2, null);
        emptyTextView.setGravity(Gravity.CENTER);
        emptyTextView.setPadding(AndroidUtilities.dp(28), AndroidUtilities.dp(24), AndroidUtilities.dp(28), AndroidUtilities.dp(28));
        card.addView(emptyTextView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        LinearLayout buttonsRow = new LinearLayout(context);
        buttonsRow.setOrientation(LinearLayout.HORIZONTAL);
        buttonsRow.setGravity((LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT) | Gravity.CENTER_VERTICAL);
        buttonsRow.setPadding(AndroidUtilities.dp(8), AndroidUtilities.dp(4), AndroidUtilities.dp(8), AndroidUtilities.dp(8));
        card.addView(buttonsRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView clearFinishedButton = makeTextButton(context, LocaleController.getString(R.string.AmbergramQueueClearFinished), BRAND_ORANGE);
        clearFinishedButton.setOnClickListener(v -> DownloadQueueController.getInstance(currentAccount).removeFinished());
        buttonsRow.addView(clearFinishedButton, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView cancelAllButton = makeTextButton(context, LocaleController.getString(R.string.AmberQueueCancelAll), STATE_RED);
        cancelAllButton.setOnClickListener(v -> DownloadQueueController.getInstance(currentAccount).cancelAll());
        buttonsRow.addView(cancelAllButton, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextInfoPrivacyCell footerCell = new TextInfoPrivacyCell(context, 24, null);
        footerCell.setText(LocaleController.getString(R.string.AmbergramQueuePageHint));
        contentWrapper.addView(footerCell, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        refreshQueue();
        return fragmentView;
    }

    private TextView makeTextButton(Context context, String text, int color) {
        TextView button = new TextView(context);
        button.setTypeface(AndroidUtilities.bold());
        button.setTextSize(15);
        button.setTextColor(color);
        button.setText(text);
        button.setGravity(Gravity.CENTER);
        button.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(12), AndroidUtilities.dp(16), AndroidUtilities.dp(12));
        return button;
    }

    private View makeQueueRow(Context context, final DownloadQueueController.QueueItem item, boolean showDivider) {
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.VERTICAL);
        row.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(10), AndroidUtilities.dp(21), AndroidUtilities.dp(10));

        LinearLayout topLine = new LinearLayout(context);
        topLine.setOrientation(LinearLayout.HORIZONTAL);
        topLine.setGravity(Gravity.CENTER_VERTICAL);
        row.addView(topLine, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView nameView = new TextView(context);
        nameView.setTypeface(AndroidUtilities.bold());
        nameView.setTextSize(16);
        ThemeBind.textColor(nameView, Theme.key_windowBackgroundWhiteBlackText, null);
        nameView.setLines(1);
        nameView.setMaxLines(1);
        nameView.setSingleLine(true);
        nameView.setEllipsize(android.text.TextUtils.TruncateAt.MIDDLE);
        topLine.addView(nameView, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        if (item.state == DownloadQueueController.STATE_PENDING) {
            TextView removeView = makeTextButton(context, LocaleController.getString(R.string.AmbergramQueueRemove), BRAND_ORANGE);
            removeView.setOnClickListener(v -> DownloadQueueController.getInstance(currentAccount).cancelPendingItem(item));
            topLine.addView(removeView, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        } else if (item.state == DownloadQueueController.STATE_FAILED) {
            TextView retryView = makeTextButton(context, LocaleController.getString(R.string.AmbergramQueueRetry), STATE_GREEN);
            retryView.setOnClickListener(v -> DownloadQueueController.getInstance(currentAccount).retryItem(item));
            topLine.addView(retryView, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        }

        TextView statusView = new TextView(context);
        statusView.setTypeface(AndroidUtilities.bold());
        statusView.setTextSize(13);
        statusView.setText(statusText(item));
        statusView.setTextColor(statusColor(item));
        row.addView(statusView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL, 0, AndroidUtilities.dp(3), 0, 0));

        if (item.state == DownloadQueueController.STATE_DOWNLOADING && item.size > 0) {
            ProgressBar progressBar = new ProgressBar(context, null, android.R.attr.progressBarStyleHorizontal);
            progressBar.getProgressDrawable().setColorFilter(BRAND_ORANGE, PorterDuff.Mode.SRC_IN);
            progressBar.setMax(100);
            progressBar.setProgress((int) Math.min(100, item.loadedBytes * 100 / Math.max(1, item.size)));
            progressBar.setProgressTintMode(PorterDuff.Mode.SRC_IN);
            row.addView(progressBar, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, 0, AndroidUtilities.dp(4), 0, 0));
        }

        if (showDivider) {
            View divider = new View(context);
            divider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
            row.addView(divider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1, 0, AndroidUtilities.dp(4), 0, 0));
        }
        return row;
    }

    private String statusText(DownloadQueueController.QueueItem item) {
        String size = AndroidUtilities.formatFileSize(item.size);
        switch (item.state) {
            case DownloadQueueController.STATE_DOWNLOADING:
                String progress = item.size > 0 ? AndroidUtilities.formatFileSize(item.loadedBytes) + " / " + size : size;
                return LocaleController.getString(R.string.AmbergramQueueStateDownloading) + " • " + progress;
            case DownloadQueueController.STATE_DONE:
                return LocaleController.getString(R.string.AmbergramQueueStateDone) + " • " + size;
            case DownloadQueueController.STATE_FAILED:
                return LocaleController.getString(R.string.AmbergramQueueStateFailed);
            default:
                return LocaleController.getString(R.string.AmbergramQueueStatePending) + " • " + size;
        }
    }

    private int statusColor(DownloadQueueController.QueueItem item) {
        switch (item.state) {
            case DownloadQueueController.STATE_DOWNLOADING:
                return BRAND_ORANGE;
            case DownloadQueueController.STATE_DONE:
                return STATE_GREEN;
            case DownloadQueueController.STATE_FAILED:
                return STATE_RED;
            default:
                return getThemedColor(Theme.key_windowBackgroundWhiteGrayText2);
        }
    }

    private void refreshQueue() {
        if (queueContainer == null || queueContainer.getContext() == null) {
            return;
        }
        Context context = queueContainer.getContext();
        ArrayList<DownloadQueueController.QueueItem> items = DownloadQueueController.getInstance(currentAccount).getQueueSnapshot();

        queueContainer.removeAllViews();
        boolean empty = items.isEmpty();
        emptyTextView.setVisibility(empty ? View.VISIBLE : View.GONE);
        if (empty) {
            emptyTextView.setText(LocaleController.getString(R.string.AmbergramQueueEmpty));
        }

        int waiting = 0, downloading = 0;
        for (int a = 0; a < items.size(); a++) {
            DownloadQueueController.QueueItem item = items.get(a);
            if (item.state == DownloadQueueController.STATE_PENDING) {
                waiting++;
            } else if (item.state == DownloadQueueController.STATE_DOWNLOADING) {
                downloading++;
            }
            queueContainer.addView(makeQueueRow(context, item, a != items.size() - 1));
        }

        if (summaryTextView != null) {
            if (waiting > 0 || downloading > 0) {
                summaryTextView.setText(LocaleController.formatString(R.string.AmbergramQueueSummary, String.valueOf(waiting), String.valueOf(downloading)));
                summaryTextView.setVisibility(View.VISIBLE);
            } else {
                summaryTextView.setVisibility(View.GONE);
            }
        }
    }

    @Override
    public void onQueueUpdated() {
        AndroidUtilities.runOnUIThread(() -> {
            if (!updateScheduled) {
                updateScheduled = true;
                AndroidUtilities.runOnUIThread(() -> {
                    updateScheduled = false;
                    refreshQueue();
                }, 300);
            }
        });
    }
}
```


---

## ۱-۵ نقطه ورود در ChatActivity.java (دیف کامل)

سه تغییر: (الف) import ها، (ب) تعریف id منو `amber_queue = 500` و دکمه‌اش در اکشن‌مود، (ج) هندلر کلیک که پیام‌های انتخابی را با `enqueue` می‌فرستد و Bulletin می‌دهد.

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java
index 1ed161bf7..d25d4ef13 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java
@@ -171,12 +171,16 @@ import org.telegram.messenger.ImageReceiver;
 import org.telegram.messenger.LanguageDetector;
 import org.telegram.messenger.LiteMode;
 import org.telegram.messenger.LocaleController;
+import org.telegram.messenger.DownloadQueueController;
 import org.telegram.messenger.MediaController;
 import org.telegram.messenger.MediaDataController;
 import org.telegram.messenger.SendMessageChatArguments;
 import org.telegram.messenger.MessageObject;
 import org.telegram.messenger.MessagePreviewParams;
 import org.telegram.messenger.MessageSuggestionParams;
+import org.telegram.messenger.AmberAntiAds;
+import org.telegram.messenger.AmberGhost;
+import org.telegram.messenger.AmberMorphe;
 import org.telegram.messenger.MessagesController;
 import org.telegram.messenger.MessagesStorage;
 import org.telegram.messenger.NotificationCenter;
@@ -548,7 +552,7 @@ public class ChatActivity extends BaseFragment implements
     private AlertDialog scheduleNowDialog;
 
     private HintView2 savedMessagesHint;
-	private HintView2 savedMessagesSearchHint;
+        private HintView2 savedMessagesSearchHint;
     private HintView2 savedMessagesTagHint;
     private HintView2 groupEmojiPackHint;
     private HintView2 botMessageHint;
@@ -1686,6 +1690,7 @@ public class ChatActivity extends BaseFragment implements
     private final static int edit = 23;
     private final static int add_shortcut = 24;
     private final static int save_to = 25;
+    private final static int amber_queue = 500;
     private final static int auto_delete_timer = 26;
     private final static int change_colors = 27;
     private final static int tag_message = 28;
@@ -3837,6 +3842,39 @@ public class ChatActivity extends BaseFragment implements
                             BulletinFactory.of(ChatActivity.this).createDownloadBulletin(isMusic ? BulletinFactory.FileType.AUDIOS : BulletinFactory.FileType.UNKNOWNS, count, themeDelegate).show();
                         }
                     });
+                } else if (id == amber_queue) {
+                    ArrayList<MessageObject> amberQueueObjects = new ArrayList<>();
+                    for (int a = 1; a >= 0; a--) {
+                        for (int b = 0; b < selectedMessagesIds[a].size(); b++) {
+                            MessageObject selectedObject = selectedMessagesIds[a].valueAt(b);
+                            if (selectedObject != null && selectedObject.getDocument() != null) {
+                                amberQueueObjects.add(selectedObject);
+                            }
+                        }
+                        selectedMessagesIds[a].clear();
+                        selectedMessagesCanCopyIds[a].clear();
+                        selectedMessagesCanStarIds[a].clear();
+                    }
+                    hideActionMode();
+                    updatePinnedMessageView(true);
+                    updateVisibleRows();
+                    if (getParentActivity() == null) {
+                        return;
+                    }
+                    if (amberQueueObjects.isEmpty()) {
+                        BulletinFactory.of(ChatActivity.this).createSimpleBulletin(R.raw.error, LocaleController.getString(R.string.AmberQueueNoneFound)).show();
+                    } else {
+                        int amberAdded = DownloadQueueController.getInstance(getAccountInstance().getCurrentAccount()).enqueue(amberQueueObjects);
+                        CharSequence amberText;
+                        if (amberAdded == 0) {
+                            amberText = LocaleController.getString(R.string.AmberQueueAlreadyQueued);
+                        } else if (amberAdded == 1) {
+                            amberText = LocaleController.getString(R.string.AmberQueueAddedOne);
+                        } else {
+                            amberText = LocaleController.formatString(R.string.AmberQueueAddedMany, amberAdded);
+                        }
+                        BulletinFactory.of(ChatActivity.this).createSimpleBulletin(amberAdded == 0 ? R.raw.error : R.raw.done, amberText).show();
+                    }
                 } else if (id == chat_enc_timer) {
                     if (getParentActivity() == null) {
                         return;
@@ -8915,14 +8953,14 @@ public class ChatActivity extends BaseFragment implements
                 savedMessagesHint.setJoint(0.5f, 0);
             }
             savedMessagesHint.setCloseButton(true);
-			savedMessagesHint.setOnHiddenListener(() -> {
+                        savedMessagesHint.setOnHiddenListener(() -> {
                 if (searchContainer == null || searchContainer.getVisibility() != View.VISIBLE) {
                     if (savedMessagesSearchHint != null) {
                         savedMessagesSearchHint.show();
                     }
                 }
-			});
-			savedMessagesHint.setDuration(-1);
+                        });
+                        savedMessagesHint.setDuration(-1);
             savedMessagesHint.setPadding(dp(8), 0, dp(8), 0);
             savedMessagesHint.setGlass(glassBackgroundDrawableFactory);
             contentView.addView(savedMessagesHint, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, 120, Gravity.TOP | Gravity.FILL_HORIZONTAL, 0, -8, 0, 0));
@@ -8936,9 +8974,9 @@ public class ChatActivity extends BaseFragment implements
                     .setCloseButton(true)
                     .setJointPx(1, -dp(56))
                     .setRounding(8);
-			savedMessagesSearchHint.setText(LocaleController.getString(R.string.SavedTagSearchTooltipHint));
+                        savedMessagesSearchHint.setText(LocaleController.getString(R.string.SavedTagSearchTooltipHint));
             savedMessagesSearchHint.setGlass(glassBackgroundDrawableFactory);
-			contentView.addView(savedMessagesSearchHint, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, 120, Gravity.TOP | Gravity.FILL_HORIZONTAL, 16, -8, 16, 0));
+                        contentView.addView(savedMessagesSearchHint, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, 120, Gravity.TOP | Gravity.FILL_HORIZONTAL, 16, -8, 16, 0));
 
             if (getUserConfig().isPremium()) {
                 savedMessagesTagHint = new HintView2(context, HintView2.DIRECTION_BOTTOM)
@@ -10806,6 +10844,7 @@ public class ChatActivity extends BaseFragment implements
         if (currentEncryptedChat == null) {
             final boolean isSavedMessages = getDialogId() == getUserConfig().getClientUserId() && (chatMode == 0 || chatMode == MODE_SAVED);
             actionModeViews.add(actionMode.addItemWithWidth(save_to, R.drawable.msg_download, dp(48), LocaleController.getString(R.string.SaveToMusic)));
+            actionModeViews.add(actionMode.addItemWithWidth(amber_queue, R.drawable.msg_list, dp(48), LocaleController.getString(R.string.AmberQueueMenu)));
             actionModeViews.add(actionMode.addItemWithWidth(edit, R.drawable.msg_edit, dp(48), LocaleController.getString(R.string.Edit)));
             if (isSavedMessages) {
                 actionModeViews.add(actionMode.addItemWithWidth(tag_message, R.drawable.menu_tag_edit, dp(48), LocaleController.getString(R.string.AccDescrTagMessage)));
@@ -11676,7 +11715,8 @@ public class ChatActivity extends BaseFragment implements
 
     private ArrayList<TLRPC.Chat> nextChannels;
     public void setNextChannels(ArrayList<TLRPC.Chat> channels) {
-        nextChannels = channels;
+        // AmberMorphe: optionally disable the pull-down "next unread channel" gesture.
+        nextChannels = AmberMorphe.noChannelSwitch() ? null : channels;
     }
 
     private void addToPulledDialogsMyself() {
@@ -25759,7 +25799,7 @@ public class ChatActivity extends BaseFragment implements
     private Pattern sponsoredUrlPattern;
     private MessageObject botSponsoredMessage;
     private void addSponsoredMessages(boolean animated) {
-        if (sponsoredMessagesAdded || chatMode != 0 || !ChatObject.isChannel(currentChat) && !UserObject.isBot(currentUser) || !forwardEndReached[0] || getUserConfig().isPremium() && getMessagesController().isSponsoredDisabled() || isReport()) {
+        if (AmberAntiAds.noSponsored() || sponsoredMessagesAdded || chatMode != 0 || !ChatObject.isChannel(currentChat) && !UserObject.isBot(currentUser) || !forwardEndReached[0] || getUserConfig().isPremium() && getMessagesController().isSponsoredDisabled() || isReport()) {
             return;
         }
         MessagesController.SponsoredMessagesInfo res = getMessagesController().getSponsoredMessages(dialog_id);
@@ -30645,6 +30685,8 @@ public class ChatActivity extends BaseFragment implements
         super.onResume();
         checkShowBlur(false);
         activityResumeTime = System.currentTimeMillis();
+        // AmberGram ghost mode: defer read receipts while this chat is open
+        AmberGhost.chatOpened(dialog_id);
         if (openImport && getSendMessagesHelper().getImportingHistory(dialog_id) != null) {
             ImportingAlert alert = new ImportingAlert(getParentActivity(), null, this, themeDelegate);
             alert.setOnHideListener(dialog -> {
@@ -30860,6 +30902,9 @@ public class ChatActivity extends BaseFragment implements
     public void onPause() {
         super.onPause();
         scrolling = false;
+        // AmberGram ghost mode: chat closed — replay any deferred read receipts now
+        AmberGhost.chatClosed(dialog_id);
+        AmberGhost.flushRead(dialog_id, currentAccount);
         if (scrimPopupWindow != null) {
             scrimPopupWindow.setPauseNotifications(false);
             closeMenu();
@@ -33480,7 +33525,7 @@ public class ChatActivity extends BaseFragment implements
             businessLinksEmptyView = new BusinessLinksEmptyView(getContext(), this, businessLink, getResourceProvider());
             businessLinksEmptyView.setBackground(Theme.createServiceDrawable(AndroidUtilities.dp(24), businessLinksEmptyView, contentView, getThemedPaint(Theme.key_paint_chatActionBackground)));
             emptyViewContainer.addView(businessLinksEmptyView, LayoutHelper.createFrame(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER));
-        } else if (preloadedGreetingsSticker != null && currentUser != null && !userBlocked || userInfo != null && getDialogId() != getUserConfig().getClientUserId() && (userInfo.contact_require_premium && !getUserConfig().isPremium() || userInfo.send_paid_messages_stars > StarsController.getInstance(currentAccount).getBalance().amount)) {
+        } else if (!AmberAntiAds.noGreetings() && (preloadedGreetingsSticker != null && currentUser != null && !userBlocked || userInfo != null && getDialogId() != getUserConfig().getClientUserId() && (userInfo.contact_require_premium && !getUserConfig().isPremium() || userInfo.send_paid_messages_stars > StarsController.getInstance(currentAccount).getBalance().amount))) {
             greetingsViewContainer = new ChatGreetingsView(getContext(), currentUser, currentAccount, preloadedGreetingsSticker, themeDelegate) {
                 @Override
                 protected void onLayout(boolean changed, int l, int t, int r, int b) {
@@ -35371,6 +35416,8 @@ public class ChatActivity extends BaseFragment implements
                         selectedMessagesCanCopyIds[a].clear();
                         selectedMessagesCanStarIds[a].clear();
                         selectedMessagesIds[a].clear();
+                        selectedMessagesCanCopyIds[a].clear();
+                        selectedMessagesCanStarIds[a].clear();
                     }
                     hideActionMode();
                     updatePinnedMessageView(true);
@@ -39523,7 +39570,7 @@ public class ChatActivity extends BaseFragment implements
             searchingUserMessages = null;
             searchingChatMessages = null;
             searchingHashtag = null;
-			searchItem.setSearchFieldHint(isSupportedTags() ? LocaleController.getString(R.string.SavedTagSearchHint) : LocaleController.getString(R.string.Search));
+                        searchItem.setSearchFieldHint(isSupportedTags() ? LocaleController.getString(R.string.SavedTagSearchHint) : LocaleController.getString(R.string.Search));
             searchItem.setSearchFieldCaption(null);
             animatorSearchFieldVisibility.setValue(false, true);
             animatorSearchHashtagHistoryVisibility.setValue(false, true);
@@ -39773,7 +39820,7 @@ public class ChatActivity extends BaseFragment implements
                     searchingForUser = false;
                     searchItem.setSearchFieldText("", true);
                 }
-				searchItem.setSearchFieldHint(isSupportedTags() ? LocaleController.getString(R.string.SavedTagSearchHint) : LocaleController.getString(R.string.Search));
+                                searchItem.setSearchFieldHint(isSupportedTags() ? LocaleController.getString(R.string.SavedTagSearchHint) : LocaleController.getString(R.string.Search));
                 searchCalendarButton.setVisibility(View.VISIBLE);
                 if (searchUserButton != null) {
                     searchUserButton.setVisibility(View.VISIBLE);
@@ -39801,9 +39848,9 @@ public class ChatActivity extends BaseFragment implements
         return searchItemListener;
     }
 
-	private boolean isSupportedTags() {
-		return getUserConfig().getClientUserId() == getDialogId() && !getMessagesController().getSavedMessagesController().unsupported && getUserConfig().isPremium();
-	}
+        private boolean isSupportedTags() {
+                return getUserConfig().getClientUserId() == getDialogId() && !getMessagesController().getSavedMessagesController().unsupported && getUserConfig().isPremium();
+        }
 
     private ChatMessageCellDelegate chatMessageCellDelegate;
     private ChatMessageCellDelegate getChatMessageCellDelegate() {
```


جای دقیق دکمه در اکشن‌مود (برای یافتنش در فایل بزرگ، عبارت `amber_queue` را جست‌وجو کنید — سه موقعیت: تعریف id، `addItemWithWidth`، و شاخه `else if (id == amber_queue)`).

نکته: فقط پیام‌هایی که `getDocument() != null` دارند صف می‌شوند (فیلم/فایل/موزیک). عکس‌های عادی (photo) در این پیاده‌سازی صف نمی‌شوند چون `getDocument()` برایشان null است.

## ۱-۶ هوک‌های راه‌اندازی

**ApplicationLoader.java** — دو خط اضافه شد:

```java
// در پایان initData (پس از حلقه اکانت‌ها):
DownloadQueueController.resumeAllQueues();

// در onFinish (کنار ProxyRotationController.init()):
AmbergramProxyManager.getInstance().onAppStart();
```

دیف کامل:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java b/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java
index 2a18412d7..beaab1292 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java
@@ -274,6 +274,7 @@ public class ApplicationLoader extends Application {
             ContactsController.getInstance(a).checkAppAccount();
             DownloadController.getInstance(a);
         }
+        DownloadQueueController.resumeAllQueues();
         BillingController.getInstance().startConnection();
     }
 
@@ -356,6 +357,7 @@ public class ApplicationLoader extends Application {
 
         LauncherIconController.tryFixLauncherIconIfNeeded();
         ProxyRotationController.init();
+        AmbergramProxyManager.getInstance().onAppStart();
 
         //if (BuildConfig.DEBUG_PRIVATE_VERSION) {
         //    Choreographer60FpsContent.getInstance().addFrameCallback(debugEverySecondChecks, 1);
```


**AndroidManifest.xml** — دو بلوک اضافه شد (دیف کامل انتهای سند در بخش ۷ هم هست):

```xml
<!-- سرویس صف دانلود -->
<service
    android:name=".AmberDownloadService"
    android:exported="false"
    android:foregroundServiceType="dataSync"
/>

<!-- گیرنده آلارم پروکسی -->
<receiver android:name=".AmbergramProxyReceiver" android:enabled="true" android:exported="false"/>
```

## ۱-۷ رشته‌های صف (انگلیسی) — کلیدهای `AmberQueue*` و `AmbergramQueue*`

```xml
<string name="AmberQueueMenu">Sequential download</string>
<string name="AmberQueueNotificationTitle">AmberGram sequential downloads</string>
<string name="AmberQueueAddedOne">1 file added to the sequential download queue</string>
<string name="AmberQueueAddedMany">%1$d files added to the sequential download queue</string>
<string name="AmberQueueNoneFound">No downloadable files in the selection</string>
<string name="AmberQueueCancelAll">Cancel all</string>
<string name="AmberQueueProgressLine">%1$d of %2$d</string>
<string name="AmberQueueAlreadyQueued">Selected files are already in the download queue</string>
<string name="AmbergramQueueSection">Sequential Downloads</string>
<string name="AmbergramQueueEmpty">The queue is empty. Open a chat, long-press to select videos and files, then tap the three-dot menu and choose \"Sequential download\".</string>
<string name="AmbergramQueueStatePending">Waiting</string>
<string name="AmbergramQueueStateDownloading">Downloading</string>
<string name="AmbergramQueueStateDone">Done</string>
<string name="AmbergramQueueStateFailed">Failed</string>
<string name="AmbergramQueueRetry">Retry</string>
<string name="AmbergramQueueClearFinished">Clear finished</string>
<string name="AmbergramQueueRemove">Remove</string>
<string name="AmbergramQueueRemoved">Removed from the queue</string>
<string name="AmbergramQueueSummary">%1$s waiting • %2$s downloading</string>
<string name="AmbergramQueueRowIdle">No active downloads</string>
<string name="AmbergramQueuePageHint">Files are downloaded one at a time and saved to Downloads/AmberGram.</string>
```

معادل‌های فارسی در `values-fa/strings.xml` با همان کلیدها (نمونه):

```xml
<string name="AmberQueueMenu">دانلود ترتیبی</string>
<string name="AmberQueueNotificationTitle">دانلود ترتیبی AmberGram</string>
<string name="AmbergramQueueEmpty">صف خالی است. در یک گفتگو ویدیو یا فایل‌ها را انتخاب کنید، سپس از منوی سه‌نقطه گزینه «دانلود ترتیبی» را بزنید.</string>
<string name="AmbergramQueuePageHint">فایل‌ها یکی‌یکی دانلود و در پوشه Downloads/Telegram ذخیره می‌شوند.</string>
```

> ⚠️ **ناهماهنگی شناخته‌شده برای دیباگ:** رشته انگلیسی `AmbergramQueuePageHint` می‌گوید «Downloads/AmberGram» ولی کد واقعاً در `Downloads/Telegram` ذخیره می‌کند (`RELATIVE_PATH = Environment.DIRECTORY_DOWNLOADS + "/Telegram"` در `copyToPublicDownloadsQ` و `Downloads/Telegram` در مسیر legacy). رشته فارسی درست است. اگر خواستید اصلاح کنید یا مسیر کپی را به `Downloads/AmberGram` تغییر دهید — این یکی از اقلام فهرست دیباگ است.

## ۱-۸ راهنمای دیباگ صف — دقیقاً کجا نگاه کنید

### نقاط بحرانی در DownloadQueueController (برای لاگ‌گذاری)

کد فعلاً فقط خطاها را با `FileLog.e` ثبت می‌کند؛ برای دیباگ عمیق‌تر این‌ها را `FileLog.d` اضافه کنید (تگ‌گذاری با `FileLog.d("AmberQueue ...")` تا در logcat فیلتر شود):

| کجا | چه چیزی لاگ شود |
|-----|----------------|
| اول `enqueue` | `added` و تعداد ورودی‌ها و اسم فایل‌ها |
| `startNextIfNeeded` بعد از انتخاب `next` | اسم فایل، `attempts`، `retryAt`، وضعیت `isNetworkConnected()` |
| شاخه `!isNetworkConnected()` | «شبکه قطع — poll هر ۵s» |
| `failCurrent` | دلیل (retriable؟)، `attempts`، `retryAt` جدید |
| `checkCurrentStalled` | «stall: 90s بدون بایت» |
| `finishCurrentWithFile` | مسیر فایل نهایی + نتیجه کپی (`ok`) |
| `didReceivedNotification` در هر سه رویداد | `args[0]` (fileName) و مطابقت با `current.fileName` |

دستور پیشنهادی:

```java
private static final String TAG = "AmberQueue";
// و بعد در نقاط بالا: FileLog.d(TAG + ": start " + current.displayName + " attempt=" + current.attempts);
```

نمایش لاگ:

```bash
adb logcat -s AmberQueue
# یا برای همه خطاهای فایل:
adb logcat | grep -E "FileLoader|tmessages|AmberQueue"
```

### سناریوهای تست دستی صف (همان شبیه‌سازی ۸ سناریو/۲۰ اظهار v0.6.0)

1. **شبکه قطع موقع شروع**: گوشی را در حالت پرواز بگذارید، چند فایل انتخاب کنید، «دانلود ترتیبی» بزنید. انتظار: هیچ آیتمی FAILED نمی‌شود؛ همه در وضعیت Waiting می‌مانند؛ وقتی نت آمد دانلود شروع می‌شود.
2. **قطعی وسط دانلود**: وسط دانلود فایل اول نت را قطع کنید. انتظار: بعد از رسیدن watchdog (۹۰ ثانیه بی‌بایت) یا شکست FileLoader، آیتم به صف برمی‌گردد و با backoff دوباره تلاش می‌کند؛ فایل دوم در همین فاصله شروع نمی‌شود (تک‌خردی حفظ است) چون current هنوز تعیین تکلیف نشده.
3. **پروکسی متلاشی**: یک پروکسی مرده وصل کنید و صف بدهید. انتظار: تلاش‌های مکرر تا ۸ بار؛ نهایتاً FAILED با دکمه Retry؛ بقیه صف جلو می‌روند.
4. **کشتن پروسه**: حین دانلود، برنامه را از Recents ببندید یا `adb shell am force-stop com.ambergram.app`. انتظار: بعد از باز شدن دوباره، صف از pref بازیابی می‌شود و آیتم فعالِ نیمه‌کاره از اول شروع می‌شود (state DOWNLOADING در persist به PENDING تبدیل می‌شود در `loadQueue`).
5. **آیتم تکراری**: همان فایل را دوباره انتخاب کنید. انتظار: Bulletin «already in queue» (dedup با `hasActiveItemForFileName`).
6. **فایل بدون اسم معتبر**: یک فایل خراب/بدون نام. انتظار: fail فوری بدون قفل‌شدن صف (`checkName.startsWith("0_0")` یا MIN_VALUE).
7. **انصراف از نوتیف**: دکمه Cancel all روی نوتیف. انتظار: صف کامل پاک، سرویس stop، نوتیف حذف.
8. **تمام شدن صف**: انتظار: DONE ها پاک می‌شوند، FAILED ها می‌مانند، سرویس خاموش، نوتیف حذف (`updateNotification` در حالت idle هیچ نمی‌گذارد + `onDestroy` نوتیف را cancel می‌کند).

### ابزارهای بررسی بدون کد

```bash
# وضعیت سرویس foreground:
adb shell dumpsys activity services com.ambergram.app | grep -A 15 AmberDownloadService

# محتوای صف ذخیره‌شده (فقط روی بیلد debuggable؛ release قابل خواندن با root):
adb shell run-as com.ambergram.app cat shared_prefs/amber_queue_0.xml

# تحمیل قطعی شبکه سریع:
adb shell svc wifi disable ; adb shell svc data disable
# برگرداندن:
adb shell svc wifi enable ; adb shell svc data enable
```

نکته درباره turbo و صف: اگر toggle «Turbo download» روشن باشد، دانلودهای صف با پارچه 1MB و ۱۲ درخواست موازی اجرا می‌شوند (`FileLoadOperation`). روی شبکه‌های خیلی ناپایدار این می‌تواند نرخ شکست هر تلاش را بالا ببرد — خود صف این شکست‌ها را retry می‌کند، ولی اگر خواستید مقایسه کنید، turbo را موقتاً خاموش کنید تا ببینید تفاوت پایداری چقدر است.

---

# بخش ۲ — بسته Morphe (AmberMorphe + ۸ گیت)

الهام از پچ‌های جامعه Morphe (HushTelegram و…) ولی به صورت بومی برای فورک سورس. همه flag ها global (همه اکانت‌ها) و در `MessagesController.getGlobalMainSettings()` ذخیره می‌شوند. الگوی هر toggle: کش `Boolean` + `synchronized(lock)` lazy-load + getter/setter.

| toggle | کلید pref | پیش‌فرض | نقطه گیت |
|--------|-----------|---------|----------|
| antiDelete | `amberMorpheAntiDelete` | true | `MessagesController` — بلوک مصرف `deletedMessages` |
| antiDisappearing | `amberMorpheAntiDisappearing` | true | `MessageObject.isVoiceOnce()/isRoundOnce()` |
| noScreenshotNotify | `amberMorpheNoScreenshotNotify` | true | `MediaController` بلوک ارسال اسکرین‌شات |
| bypassNoforwards | `amberMorpheBypassNoforwards` | true | `MessagesController.isPeerNoForwards()` + `MessageObject.canForwardMessage()` |
| noAutoUpdate | `amberMorpheNoAutoUpdate` | true | `LaunchActivity.checkAppUpdate()` |
| noChannelSwitch | `amberMorpheNoChannelSwitch` | **false** | `ChatActivity.setNextChannels()` |
| hideStoriesRead | `amberMorpheHideStoriesRead` | true | `StoriesController` ارسال `readStories` |
| bypassTranslation | `amberMorpheBypassTranslation` | true | `TranslateController.isTranslateDialogHidden()` |

## ۲-۱ AmberMorphe.java — کد کامل

```java
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
```


## ۲-۲ گیت‌ها — دیف‌های کامل فایل به فایل

**MessagesController.java** (این دیف ترکیبی است: هانک اول bypassNoforwards، هانک دوم حالت شبح — بخش ۴، هانک سوم antiDelete، هانک چهارم noSponsored — بخش ۳):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java b/TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java
index 9d0077ffc..981942dd3 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java
@@ -6689,6 +6689,9 @@ public class MessagesController extends BaseController implements NotificationCe
     }
 
     public boolean isPeerNoForwards(long dialogId) {
+        if (AmberMorphe.bypassNoforwards()) {
+            return false;
+        }
         return dialogId > 0 ? isUserNoForwards(dialogId) : isChatNoForwards(-dialogId);
     }
 
@@ -11412,6 +11415,9 @@ public class MessagesController extends BaseController implements NotificationCe
     }
 
     public boolean sendTyping(long dialogId, long threadMsgId, int action, String emojicon, int classGuid) {
+        if (AmberGhost.isEnabled()) {
+            return false;
+        }
         if (action < 0 || action >= sendingTypings.length || dialogId == 0) {
             return false;
         }
@@ -14709,6 +14715,15 @@ public class MessagesController extends BaseController implements NotificationCe
     }
 
     public void markDialogAsRead(long dialogId, int maxPositiveId, int maxNegativeId, int maxDate, boolean popup, long threadId, int countDiff, boolean readNow, int scheduledCount) {
+        // AmberGram ghost mode: defer read receipts while the chat is open, replay on leave
+        if (AmberGhost.shouldDeferRead(dialogId)) {
+            AmberGhost.deferRead(dialogId, maxPositiveId, maxNegativeId, maxDate, threadId, scheduledCount);
+            return;
+        }
+        amberGhostMarkDialogAsRead(dialogId, maxPositiveId, maxNegativeId, maxDate, popup, threadId, countDiff, readNow, scheduledCount);
+    }
+
+    public void amberGhostMarkDialogAsRead(long dialogId, int maxPositiveId, int maxNegativeId, int maxDate, boolean popup, long threadId, int countDiff, boolean readNow, int scheduledCount) {
         boolean createReadTask;
 
         if (threadId != 0) {
@@ -21321,7 +21336,9 @@ public class MessagesController extends BaseController implements NotificationCe
                 getMessagesStorage().markMessagesContentAsRead(key, arrayList, currentTime2, markContentAsReadMessagesDate);
             }
         }
-        if (deletedMessages != null) {
+        // AmberMorphe anti-delete: when the toggle is on, incoming deletion
+        // updates are skipped entirely so messages stay in cache and database.
+        if (deletedMessages != null && !AmberMorphe.antiDelete()) {
             for (int a = 0, size = deletedMessages.size(); a < size; a++) {
                 long key = deletedMessages.keyAt(a);
                 ArrayList<Integer> arrayList = deletedMessages.valueAt(a);
@@ -21724,6 +21741,9 @@ public class MessagesController extends BaseController implements NotificationCe
     }
 
     public SponsoredMessagesInfo getSponsoredMessages(long dialogId) {
+        if (AmberAntiAds.noSponsored()) {
+            return null;
+        }
         SponsoredMessagesInfo info = sponsoredMessages.get(dialogId);
         if (info != null && (info.loading || Math.abs(SystemClock.elapsedRealtime() - info.loadTime) <= 5 * 60 * 1000)) {
             return info;
```


**MessageObject.java** (antiDisappearing در دو متد + bypassNoforwards در انتهای canForwardMessage):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/MessageObject.java b/TMessagesProj/src/main/java/org/telegram/messenger/MessageObject.java
index 373e42357..e069540e8 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/MessageObject.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/MessageObject.java
@@ -11522,10 +11522,16 @@ public class MessageObject {
     }
 
     public boolean isVoiceOnce() {
+        if (AmberMorphe.antiDisappearing()) {
+            return false;
+        }
         return isVoice() && messageOwner != null && messageOwner.media != null && messageOwner.media.ttl_seconds == 0x7FFFFFFF;
     }
 
     public boolean isRoundOnce() {
+        if (AmberMorphe.antiDisappearing()) {
+            return false;
+        }
         return isRoundVideo() && messageOwner != null && messageOwner.media != null && messageOwner.media.ttl_seconds == 0x7FFFFFFF;
     }
 
@@ -11954,7 +11960,7 @@ public class MessageObject {
     public boolean canForwardMessage() {
         if (isQuickReply()) return false;
         if (type == TYPE_GIFT_STARS || type == TYPE_GIFT_THEME_UPDATE || type == TYPE_SUGGEST_BIRTHDAY || type == TYPE_GIFT_OFFER || type == TYPE_SHARING_OFFER || type == TYPE_COMMUNITY_CHANGED) return false;
-        return !(messageOwner instanceof TLRPC.TL_message_secret) && !needDrawBluredPreview() && !isLiveLocation() && type != MessageObject.TYPE_PHONE_CALL && !isSponsored() && !messageOwner.noforwards;
+        return !(messageOwner instanceof TLRPC.TL_message_secret) && !needDrawBluredPreview() && !isLiveLocation() && type != MessageObject.TYPE_PHONE_CALL && !isSponsored() && (AmberMorphe.bypassNoforwards() || !messageOwner.noforwards);
     }
 
     public boolean canEditMedia() {
```


**MediaController.java** (noScreenshotNotify — فقط ارسال اعلان مسدود می‌شود، خود اسکرین‌شات آزاد است):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java b/TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java
index b1e2120af..388df6e11 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java
@@ -1895,7 +1895,7 @@ public class MediaController implements AudioManager.OnAudioFocusChangeListener,
                 }
             }
         }
-        if (send) {
+        if (send && !AmberMorphe.noScreenshotNotify()) {
             if (lastSecretChat != null) {
                 SecretChatHelper.getInstance(lastChatAccount).sendScreenshotMessage(lastSecretChat, lastChatVisibleMessages, null);
             } else {
```


**LaunchActivity.java** (noAutoUpdate):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java
index def777a25..bb2744f8c 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java
@@ -100,6 +100,7 @@ import org.telegram.PhoneFormat.PhoneFormat;
 import org.telegram.messenger.AccountInstance;
 import org.telegram.messenger.AndroidUtilities;
 import org.telegram.messenger.AnimationNotificationsLocker;
+import org.telegram.messenger.AmberMorphe;
 import org.telegram.messenger.ApplicationLoader;
 import org.telegram.messenger.AutoDeleteMediaTask;
 import org.telegram.messenger.BackupAgent;
@@ -6104,6 +6105,10 @@ public class LaunchActivity extends BasePermissionsActivity implements INavigati
 
     private boolean firstAppUpdateCheck = true;
     public void checkAppUpdate(boolean force, Browser.Progress progress) {
+        if (AmberMorphe.noAutoUpdate()) {
+            // AmberMorphe: never query or suggest official in-app updates.
+            return;
+        }
         if (!ApplicationLoader.isStandaloneBuild() && !ApplicationLoader.isBetaBuild()) {
             return;
         }
```


**Stories/StoriesController.java** (hideStoriesRead — فقط درخواست `TL_stories_readStories` به سرور بلاک می‌شود؛ max_read_id محلی و استوریج و نوتیف دست نمی‌خورند):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Stories/StoriesController.java b/TMessagesProj/src/main/java/org/telegram/ui/Stories/StoriesController.java
index 529eb5ca3..db301e0a8 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Stories/StoriesController.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Stories/StoriesController.java
@@ -31,6 +31,7 @@ import org.telegram.messenger.LocaleController;
 import org.telegram.messenger.MediaController;
 import org.telegram.messenger.MediaDataController;
 import org.telegram.messenger.MessageObject;
+import org.telegram.messenger.AmberMorphe;
 import org.telegram.messenger.MessagesController;
 import org.telegram.messenger.MessagesStorage;
 import org.telegram.messenger.NotificationCenter;
@@ -1342,10 +1343,12 @@ public class StoriesController {
             if (!profile) {
                 storiesStorage.updateMaxReadId(dialogId, newReadId);
             }
-            TL_stories.TL_stories_readStories req = new TL_stories.TL_stories_readStories();
-            req.peer = MessagesController.getInstance(currentAccount).getInputPeer(dialogId);
-            req.max_id = storyItem.id;
-            ConnectionsManager.getInstance(currentAccount).sendRequest(req, null);
+            if (!AmberMorphe.hideStoriesRead()) {
+                TL_stories.TL_stories_readStories req = new TL_stories.TL_stories_readStories();
+                req.peer = MessagesController.getInstance(currentAccount).getInputPeer(dialogId);
+                req.max_id = storyItem.id;
+                ConnectionsManager.getInstance(currentAccount).sendRequest(req, null);
+            }
             NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.storiesReadUpdated);
             return true;
         }
```


**TranslateController.java** (bypassTranslation — انتخاب دستی «مخفی کردن ترجمه این دیالوگ» کاربر همچنان محترم است):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/TranslateController.java b/TMessagesProj/src/main/java/org/telegram/messenger/TranslateController.java
index ea658d8af..c5714708a 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/TranslateController.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/TranslateController.java
@@ -205,6 +205,11 @@ public class TranslateController extends BaseController {
         if (hideTranslateDialogs.contains(dialogId)) {
             return true;
         }
+        if (AmberMorphe.bypassTranslation()) {
+            // AmberMorphe: keep translation available even when the peer/chat
+            // disables it, but respect the user's own per-dialog choice above.
+            return false;
+        }
         TLRPC.ChatFull chatFull = getMessagesController().getChatFull(-dialogId);
         if (chatFull != null) {
             return chatFull.translations_disabled;
```


**ChatActivity.java** — هانک `setNextChannels` (noChannelSwitch): در دیف کامل ChatActivity در بخش ۱ آمده؛ خط مربوطه:

```java
// AmberMorphe: optionally disable the pull-down "next unread channel" gesture.
nextChannels = AmberMorphe.noChannelSwitch() ? null : channels;
```

## ۲-۳ دیباگ بسته Morphe

- اگر پیام‌ها با وجود antiDelete حذف می‌شوند: گیت فقط «آپدیت‌های ورودی» را مسدود می‌کند (`processUpdateArray` مسیر `deletedMessages`)؛ اگر خودتان پیامی را حذف کنید طبعاً حذف می‌شود (مسیر `deleteMessages()` مستقل است). مرز دیگر: پاک‌سازی از سمت خودت با «حذف برای همه».
- antiDelete روی پیام‌های عادی/گروه/کانال کار می‌کند؛ حذف «رسانه‌های TTL دار» ممکن است سرور محتوا را واقعاً پاک کند — آن‌وقت پیام می‌ماند ولی مدیا لود نمی‌شود.
- bypassNoforwards دو نقطه دارد: UI来源 (`isPeerNoForwards`) و سطح پیام (`canForwardMessage`). اگر جایی هنوز منع بود، این دو نقطه را grep کنید.
- برای خاموش/روشن کردن در تست: تنظیمات → AmberGram Settings → toggle مربوطه؛ pref در `MessagesController.getGlobalMainSettings()` (فایل default shared prefs با نام پکیج).

---

# بخش ۳ — بسته ضدتبلیغ + توربو (AmberAntiAds)

۴ toggle با پیش‌فرض: noSponsored=true، noRecommendations=true، noGreetings=true، turboDownload=**false**.

## ۳-۱ AmberAntiAds.java — کد کامل

```java
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
```


## ۳-۲ گیت‌ها

**noSponsored — دو نقطه (بدون fetch و بدون رندر):**

1) `MessagesController.getSponsoredMessages()` — اگر روشن باشد اصلاً null برمی‌گرداند یعنی درخواست تبلیغ به سرور هم نمی‌رود (هانک در دیف MessagesController بخش ۲):

```java
public SponsoredMessagesInfo getSponsoredMessages(long dialogId) {
    if (AmberAntiAds.noSponsored()) {
        return null;
    }
    ...
```

2) `ChatActivity.addSponsoredMessages()` — شرط اول:

```java
if (AmberAntiAds.noSponsored() || sponsoredMessagesAdded || chatMode != 0 || ...) {
    return;
}
```

**noRecommendations — ChatMessageCell:** کارت «کانال‌های پیشنهادی» انتهای کانال ساخته نمی‌شود:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java b/TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java
index 4f0508f16..9353c2b56 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java
@@ -103,6 +103,7 @@ import androidx.core.math.MathUtils;
 
 import org.telegram.PhoneFormat.PhoneFormat;
 import org.telegram.messenger.AccountInstance;
+import org.telegram.messenger.AmberAntiAds;
 import org.telegram.messenger.AndroidUtilities;
 import org.telegram.messenger.AppGlobalConfig;
 import org.telegram.messenger.ApplicationLoader;
@@ -6847,10 +6848,16 @@ public class ChatMessageCell extends BaseCell implements SeekBar.SeekBarDelegate
                 forwardedNameLayout[0] = null;
                 forwardedNameLayout[1] = null;
                 drawName = false;
-                if (channelRecommendationsCell == null) {
-                    channelRecommendationsCell = new ChannelRecommendationsCell(this);
+                if (AmberAntiAds.noRecommendations()) {
+                    if (channelRecommendationsCell != null) {
+                        channelRecommendationsCell = null;
+                    }
+                } else {
+                    if (channelRecommendationsCell == null) {
+                        channelRecommendationsCell = new ChannelRecommendationsCell(this);
+                    }
+                    channelRecommendationsCell.setMessageObject(messageObject);
                 }
-                channelRecommendationsCell.setMessageObject(messageObject);
             } else if (messageObject.isExpiredStory()) {
                 if (!messageIdChanged) {
                     requestLayout();
```


**noGreetings — ChatActivity:** استیکر خوش‌آمدگویی در چت‌های خالی:

```java
} else if (!AmberAntiAds.noGreetings() && (preloadedGreetingsSticker != null && ...)) {
    greetingsViewContainer = new ChatGreetingsView(...);
```

(هانک در دیف کامل ChatActivity بخش ۱.)

**turboDownload — FileLoadOperation:** اعداد Morphe: پارچه 1MB و ۱۲ درخواست موازی:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/FileLoadOperation.java b/TMessagesProj/src/main/java/org/telegram/messenger/FileLoadOperation.java
index 70c5e8951..036f43906 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/FileLoadOperation.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/FileLoadOperation.java
@@ -313,6 +313,13 @@ public class FileLoadOperation {
             downloadChunkSizeBig = 1024 * 128;
             maxDownloadRequestsBig = 8;
         }
+        if (AmberAntiAds.turboDownload()) {
+            // AmberGram turbo download with Morphe "Download speed boost" numbers:
+            // 1 MB chunks with 12 parallel requests (Morphe patch defaults).
+            downloadChunkSizeBig = 1024 * 1024;
+            maxDownloadRequests = 12;
+            maxDownloadRequestsBig = 12;
+        }
         maxCdnParts = (int) (FileLoader.DEFAULT_MAX_FILE_SIZE / downloadChunkSizeBig);
     }
```


نکته turbo: این پارامترها در سازنده‌ی `FileLoadOperation` اعمال می‌شوند، یعنی **دانلودهایی که بعد از روشن‌کردن toggle شروع می‌شوند** آن را می‌گیرند؛ دانلود جاریِ نیمه‌کاره با پارامترهای قبلی ادامه می‌یابد. متن رشته `AmberTurboDownloadDesc` هم همین را می‌گوید.

## ۳-۳ دیباگ بسته ضدتبلیغ

- تبلیغ همچنان می‌آید؟ دو نقطه را چک کنید؛ به‌ویژه اگر `isSponsoredDisabled()` و premium تداخل ایجاد کند (شرط ترکیبی در `addSponsoredMessages`).
- توربو کند به‌جای سریع؟ روی پروکسی‌های ضعیف، ۱۲ درخواست موازی می‌تواند تایم‌اوت بدهد — با خاموش‌کردن toggle مقایسه کنید. مقدار `maxCdnParts` هم از `downloadChunkSizeBig` حساب می‌شود (بعد از گیت).
- pref ها: `amberNoSponsored`, `amberNoRecommendations`, `amberNoGreetings`, `amberTurboDownload` در `getGlobalMainSettings()`.

---

# بخش ۴ — حالت شبح (AmberGhost)

رفتار: تا وقتی چت باز است، رسید خواندن به سرور نمی‌رود؛ با خروج از چت (onPause) همه‌ی رسیدهای تعویق‌شده یک‌جا ارسال می‌شوند. نشانگر تایپ هرگز ارسال نمی‌شود.

## ۴-۱ AmberGhost.java — کد کامل

```java
package org.telegram.messenger;

/*
 * AmberGram fork: ghost mode.
 * While enabled, chats that are currently open are NOT marked as read on the
 * server until the user actually leaves the chat, and typing indicators are
 * never sent. Reads triggered while the chat is open are stashed here and
 * replayed once ChatActivity pauses (ghost off or chat closed).
 */

import android.content.SharedPreferences;

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
    }

    public static void chatOpened(long dialogId) {
        openDialog = dialogId;
    }

    public static void chatClosed(long dialogId) {
        if (openDialog == dialogId) {
            openDialog = 0;
        }
    }

    public static boolean shouldDeferRead(long dialogId) {
        return openDialog != 0 && openDialog == dialogId && isEnabled();
    }

    public static void deferRead(long dialogId, int maxPositiveId, int maxNegativeId, int maxDate, long threadId, int scheduledCount) {
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
                pending.scheduledCount
        );
        return true;
    }
}
```


## ۴-۲ گیت‌ها

**MessagesController.sendTyping** — نشانگر تایپ (هانک دوم دیف MessagesController در بخش ۲):

```java
public boolean sendTyping(long dialogId, long threadMsgId, int action, String emojicon, int classGuid) {
    if (AmberGhost.isEnabled()) {
        return false;
    }
    ...
```

**MessagesController.markDialogAsRead** — wrapper: متد اصلی به `amberGhostMarkDialogAsRead` تغییر نام یافت و wrapper تعویق را انجام می‌دهد:

```java
public void markDialogAsRead(long dialogId, int maxPositiveId, int maxNegativeId, int maxDate,
                             boolean popup, long threadId, int countDiff, boolean readNow, int scheduledCount) {
    // AmberGram ghost mode: defer read receipts while the chat is open, replay on leave
    if (AmberGhost.shouldDeferRead(dialogId)) {
        AmberGhost.deferRead(dialogId, maxPositiveId, maxNegativeId, maxDate, threadId, scheduledCount);
        return;
    }
    amberGhostMarkDialogAsRead(dialogId, maxPositiveId, maxNegativeId, maxDate, popup, threadId, countDiff, readNow, scheduledCount);
}

public void amberGhostMarkDialogAsRead(long dialogId, ...) {
    boolean createReadTask;
    ...  // بدنه اصلی دست‌نخورده
}
```

**ChatActivity.onResume / onPause** (هانک‌ها در دیف ChatActivity بخش ۱):

```java
// onResume:
AmberGhost.chatOpened(dialog_id);

// onPause:
AmberGhost.chatClosed(dialog_id);
AmberGhost.flushRead(dialog_id, currentAccount);
```

## ۴-۳ دیباگ حالت شبح

- اگر بازدیدها همچنان ثبت می‌شوند: چک کنید `openDialog == dialogId` — فقط همان دیالوگی که باز است تعویق می‌شود؛ نوتیف/پاپ‌آپ‌ها در همان لحظه تعویق نمی‌شوند و می‌روند.
- در چت‌های محرمانه (secret) مسیر read متفاوت است؛ اگر گزارش شد شبح در secret کار نمی‌کند، مسیر `markDialogAsRead` برای آن دیالوگ را trace کنید.
- خروج غیرمنتظره از برنامه (onPause اجرا نشود): pendingRead ها در حافظه‌اند (نه persist)؛ پس ری‌استارت یعنی رسیدها هرگز نرفتند — این خودش رفتار «شبح‌تر» است نه باگ.
- pref: `amberGhostMode` در `getGlobalMainSettings()`.

---

# بخش ۵ — پروکسی رایگان درون‌برنامه‌ای

سه فایل: مدیر (`AmbergramProxyManager`)، گیرنده آلارم (`AmbergramProxyReceiver`)، صفحه UI (`AmbergramProxyActivity`). جریان: ۶ منبع GitHub → ادغام/dedupe → تست واقعی MTProto با `ConnectionsManager.checkProxy` (بدون قطع اتصال فعال) → مرتب‌سازی با امتیاز → پاکسازی خودکار مرده‌ها → persist در pref با نام `ambergram_proxies`.

ثابت‌های مهم:

| ثابت | مقدار | معنا |
|------|-------|------|
| `UPDATE_INTERVAL` | 6h | فاصله رفرش (آلارم + catch-up موقع باز شدن برنامه +15s) |
| `MAX_PROXIES` / `MAX_PER_SOURCE` | 180 / 400 | سقف لیست و سقف هر منبع |
| `TEST_BATCH` | 20 | هر بچ تست ۲۰ پروکسی موازی |
| `RECHECK_MIN_INTERVAL` | 2min | فاصله حداقلی بین دو تست یک پروکسی |
| `REMOVE_AFTER_FAILS` | 1 | بعد از یک شکست handshake، حذف |
| `OFFLINE_GUARD_MIN_TESTED` | 10 | اگر همه تست‌های یک سیکل شکست خورد و ≥10 تست شده بود، احتمال قطعی اینترنت دستگاه — پاکسازی skip می‌شود |
| requestCode آلارم | 4213 | action: `org.telegram.messenger.AMBERGRAM_PROXY_UPDATE` |

امتیاز مرتب‌سازی (`sortScore`): available با ping → خود ping؛ available بدون ping → 5000+sourcePing؛ تست‌نشده → 100000+؛ مرده → 1000000+.

## ۵-۱ AmbergramProxyManager.java — کد کامل

```java
package org.telegram.messenger;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.SystemClock;

import org.json.JSONArray;
import org.json.JSONObject;
import org.telegram.tgnet.ConnectionsManager;
import org.telegram.utils.proxy.ProxySettings;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Objects;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * AmberGram fork: in-app free MTProto proxy provider.
 * <p>
 * Pulls proxy lists from public GitHub collector repositories every 6 hours
 * (AlarmManager wakeup + app-start catch-up), merges/dedupes them, then runs a
 * REAL MTProto availability test through the native ConnectionsManager
 * (ConnectionsManager.checkProxy) without touching the user's current
 * connection. Results (ping / availability) are persisted locally and shown in
 * AmbergramProxyActivity. Tapping a proxy hands it over to the official proxy
 * system (SharedConfig + ConnectionsManager.setProxySettings).
 */
public class AmbergramProxyManager {

    private static final String TAG = "AmbergramProxy";

    public static final long UPDATE_INTERVAL = 6 * 60 * 60 * 1000L;
    private static final int MAX_PROXIES = 180;
    private static final int MAX_PER_SOURCE = 400;
    private static final int TEST_BATCH = 20;
    private static final int RECHECK_MIN_INTERVAL = 2 * 60 * 1000;

    // Auto-cleanup: a proxy that fails a real MTProto handshake is removed from
    // the list right away. A whole cycle where EVERY tested proxy failed (and at
    // least OFFLINE_GUARD_MIN_TESTED were tested) is treated as a likely device
    // network outage, so nothing is removed in that case.
    private static final int REMOVE_AFTER_FAILS = 1;
    private static final int OFFLINE_GUARD_MIN_TESTED = 10;

    public static final int EVENT_FETCH_STARTED = 0;
    public static final int EVENT_FETCH_DONE = 1;
    public static final int EVENT_TEST_PROGRESS = 2;
    public static final int EVENT_TEST_DONE = 3;
    public static final int EVENT_LIST_CLEANED = 4;

    public interface Listener {
        void onProxyEvent(int event, int done, int total);
    }

    public static class ProxyItem {
        public String host;
        public int port;
        public String secret;
        public String source;
        public int sourcePing = -1;
        public int ping = -1;
        public boolean available;
        public boolean checking;
        public long lastOkAt;
        public long lastCheckElapsed;
        public int deadStreak;

        public String key() {
            return host + ":" + port + ":" + secret;
        }

        public ProxySettings toSettings() {
            return ProxySettings.builder()
                    .setType(ProxySettings.Type.MTPROTO)
                    .setAddress(host)
                    .setPort(port)
                    .setSecret(secret)
                    .build();
        }
    }

    private static class Source {
        final String name;
        final String url;
        final int format;

        Source(String name, String url, int format) {
            this.name = name;
            this.url = url;
            this.format = format;
        }
    }

    private static final int FORMAT_LINKS = 0;
    private static final int FORMAT_JSON = 1;

    private static final Pattern LINK_PATTERN = Pattern.compile(
            "(?:(?:https?://)?t\\.me/proxy\\?|tg://proxy\\?)server=([^&\\s\"']+)&port=(\\d{1,5})&secret=([^&\\s\"']+)");

    private static final Source[] SOURCES = {
            new Source("ALIILAPRO", "https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/mtproto.txt", FORMAT_LINKS),
            new Source("ALIILAPRO-Latency", "https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/proxies.json", FORMAT_JSON),
            new Source("SoliSpirit", "https://raw.githubusercontent.com/SoliSpirit/mtproto/master/all_proxies.txt", FORMAT_LINKS),
            new Source("TG-MTProxy", "https://raw.githubusercontent.com/tgmtproxy/telegram-mtproto-proxy-list/main/proxies.txt", FORMAT_LINKS),
            new Source("Argh94", "https://raw.githubusercontent.com/Argh94/Proxy-List/main/MTProto.txt", FORMAT_LINKS),
            new Source("0xRadikal", "https://raw.githubusercontent.com/0xRadikal/Free-Telegram-Proxy/main/all/tg.txt", FORMAT_LINKS),
    };

    private static volatile AmbergramProxyManager Instance;

    public static AmbergramProxyManager getInstance() {
        AmbergramProxyManager local = Instance;
        if (local == null) {
            synchronized (AmbergramProxyManager.class) {
                local = Instance;
                if (local == null) {
                    Instance = local = new AmbergramProxyManager();
                }
            }
        }
        return local;
    }

    private final ArrayList<ProxyItem> proxies = new ArrayList<>();
    private final ArrayList<Listener> listeners = new ArrayList<>();

    private volatile boolean fetching;
    private volatile boolean testing;
    private volatile int processedCount;
    private volatile int testTotal;
    private volatile int failedSourceCount;
    private volatile int cycleTestedCount;
    private volatile int cycleSuccessCount;
    private volatile int lastRemovedCount;

    private long lastFetchAt;
    private long lastTestAt;
    private boolean started;

    private final Runnable testWatchdog = () -> {
        if (!testing) {
            return;
        }
        testing = false;
        synchronized (proxies) {
            for (int a = 0; a < proxies.size(); a++) {
                proxies.get(a).checking = false;
            }
        }
        autoRemoveDeadProxies();
        synchronized (proxies) {
            sortProxies();
        }
        saveToDisk();
        notifyListeners(EVENT_TEST_DONE, processedCount, testTotal);
    };

    private AmbergramProxyManager() {
    }

    // ---------------------------------------------------------------- lifecycle

    public void onAppStart() {
        if (started) {
            return;
        }
        started = true;
        loadFromDisk();
        AndroidUtilities.runOnUIThread(this::autoCycleIfNeeded, 15000);
        scheduleNextAlarm(UPDATE_INTERVAL);
    }

    public void onAlarmReceived() {
        FileLog.d(TAG + ": alarm fired");
        scheduleNextAlarm(UPDATE_INTERVAL);
        autoCycleIfNeeded();
    }

    private void autoCycleIfNeeded() {
        if (!fetching && System.currentTimeMillis() - lastFetchAt > UPDATE_INTERVAL) {
            runUpdateCycle();
        }
    }

    public void scheduleNextAlarm(long delay) {
        try {
            AlarmManager alarmManager = (AlarmManager) ApplicationLoader.applicationContext.getSystemService(Context.ALARM_SERVICE);
            if (alarmManager == null) {
                return;
            }
            Intent intent = new Intent(ApplicationLoader.applicationContext, AmbergramProxyReceiver.class);
            intent.setAction("org.telegram.messenger.AMBERGRAM_PROXY_UPDATE");
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                    ApplicationLoader.applicationContext, 4213, intent,
                    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            if (Build.VERSION.SDK_INT >= 31 && !alarmManager.canScheduleExactAlarms()) {
                alarmManager.setWindow(AlarmManager.ELAPSED_REALTIME_WAKEUP,
                        SystemClock.elapsedRealtime() + delay, 60 * 60 * 1000L, pendingIntent);
            } else {
                alarmManager.setExactAndAllowWhileIdle(AlarmManager.ELAPSED_REALTIME_WAKEUP,
                        SystemClock.elapsedRealtime() + delay, pendingIntent);
            }
        } catch (Throwable t) {
            FileLog.e(t);
        }
    }

    // ---------------------------------------------------------------- update cycle

    public void runUpdateCycle() {
        if (fetching) {
            return;
        }
        fetching = true;
        failedSourceCount = 0;
        notifyListeners(EVENT_FETCH_STARTED, 0, 0);
        Utilities.globalQueue.postRunnable(() -> {
            LinkedHashMap<String, ProxyItem> merged = new LinkedHashMap<>();
            synchronized (proxies) {
                for (ProxyItem item : proxies) {
                    merged.put(item.key(), item);
                }
            }
            AtomicInteger workingSources = new AtomicInteger();
            CountDownLatch latch = new CountDownLatch(SOURCES.length);
            ExecutorService pool = Executors.newFixedThreadPool(Math.min(4, SOURCES.length));
            for (Source source : SOURCES) {
                pool.execute(() -> {
                    try {
                        String text = httpGet(source.url);
                        int parsed = parseInto(source, text, merged);
                        if (parsed > 0) {
                            workingSources.incrementAndGet();
                        } else {
                            failedSourceCount++;
                        }
                        FileLog.d(TAG + ": source " + source.name + " parsed " + parsed + " proxies");
                    } catch (Throwable t) {
                        failedSourceCount++;
                        FileLog.e(t);
                    } finally {
                        latch.countDown();
                    }
                });
            }
            try {
                latch.await();
            } catch (InterruptedException ignore) {
                Thread.currentThread().interrupt();
            }
            pool.shutdown();

            synchronized (proxies) {
                proxies.clear();
                proxies.addAll(merged.values());
                sortProxies();
                if (proxies.size() > MAX_PROXIES) {
                    proxies.subList(MAX_PROXIES, proxies.size()).clear();
                }
            }
            lastFetchAt = System.currentTimeMillis();
            saveToDisk();
            fetching = false;
            notifyListeners(EVENT_FETCH_DONE, proxies.size(), workingSources.get());
            AndroidUtilities.runOnUIThread(this::startTesting, 500);
        });
    }

    private int parseInto(Source source, String text, LinkedHashMap<String, ProxyItem> out) {
        if (source.format == FORMAT_JSON) {
            return parseJsonSource(source, text, out);
        }
        String clean = text.replace("&amp;", "&");
        Matcher matcher = LINK_PATTERN.matcher(clean);
        int count = 0;
        while (matcher.find() && count < MAX_PER_SOURCE) {
            String host = matcher.group(1);
            int port;
            try {
                port = Integer.parseInt(matcher.group(2));
            } catch (Exception e) {
                continue;
            }
            String secret = decodeSecret(matcher.group(3));
            if (!validProxy(host, port, secret)) {
                continue;
            }
            addMerged(out, newProxy(host, port, secret, source.name, -1));
            count++;
        }
        return count;
    }

    private int parseJsonSource(Source source, String text, LinkedHashMap<String, ProxyItem> out) {
        try {
            JSONArray array = new JSONArray(text);
            int count = 0;
            for (int a = 0; a < array.length() && count < MAX_PER_SOURCE; a++) {
                JSONObject object = array.optJSONObject(a);
                if (object == null) {
                    continue;
                }
                String host = object.optString("host", "");
                int port = object.optInt("port", 0);
                String connectUrl = object.optString("connect_url", "").replace("&amp;", "&");
                String secret = null;
                Matcher matcher = LINK_PATTERN.matcher(connectUrl);
                if (matcher.find()) {
                    secret = decodeSecret(matcher.group(3));
                }
                int latency = object.optInt("latency", -1);
                if (!validProxy(host, port, secret)) {
                    continue;
                }
                addMerged(out, newProxy(host, port, secret, source.name,
                        latency >= 10 && latency < 3000 ? latency : -1));
                count++;
            }
            return count;
        } catch (Throwable t) {
            FileLog.e(t);
            return 0;
        }
    }

    private ProxyItem newProxy(String host, int port, String secret, String source, int sourcePing) {
        ProxyItem item = new ProxyItem();
        item.host = host;
        item.port = port;
        item.secret = secret;
        item.source = source;
        item.sourcePing = sourcePing;
        return item;
    }

    private void addMerged(LinkedHashMap<String, ProxyItem> map, ProxyItem item) {
        ProxyItem existing = map.get(item.key());
        if (existing == null) {
            map.put(item.key(), item);
        } else if (existing.sourcePing < 0 && item.sourcePing >= 0) {
            existing.sourcePing = item.sourcePing;
        }
    }

    private static String decodeSecret(String raw) {
        if (raw == null) {
            return null;
        }
        String value = raw.trim();
        if (value.indexOf('%') >= 0) {
            try {
                value = URLDecoder.decode(value, "UTF-8");
            } catch (Exception ignore) {
            }
        }
        return value;
    }

    private static boolean validProxy(String host, int port, String secret) {
        if (host == null || host.length() == 0 || host.length() > 200 || host.indexOf(' ') >= 0) {
            return false;
        }
        if (port <= 0 || port > 65535) {
            return false;
        }
        if (secret == null || secret.length() < 16 || secret.length() > 150) {
            return false;
        }
        for (int a = 0; a < secret.length(); a++) {
            char c = secret.charAt(a);
            boolean ok = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                    || c == '=' || c == '_' || c == '-' || c == '+';
            if (!ok) {
                return false;
            }
        }
        return true;
    }

    private String httpGet(String url) throws Exception {
        HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
        connection.setConnectTimeout(12000);
        connection.setReadTimeout(15000);
        connection.setRequestProperty("User-Agent", "AmberGram (https://github.com/Soroushchq/amber)");
        int code = connection.getResponseCode();
        if (code != 200) {
            connection.disconnect();
            throw new Exception("HTTP " + code);
        }
        InputStream input = connection.getInputStream();
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int read;
        while ((read = input.read(buffer)) > 0) {
            output.write(buffer, 0, read);
        }
        input.close();
        connection.disconnect();
        return new String(output.toByteArray(), StandardCharsets.UTF_8);
    }

    // ---------------------------------------------------------------- testing

    public void startTesting() {
        if (testing) {
            return;
        }
        final ArrayList<ProxyItem> snapshot;
        synchronized (proxies) {
            snapshot = new ArrayList<>(proxies);
        }
        if (snapshot.isEmpty()) {
            return;
        }
        testing = true;
        processedCount = 0;
        testTotal = snapshot.size();
        cycleTestedCount = 0;
        cycleSuccessCount = 0;
        lastRemovedCount = 0;
        notifyListeners(EVENT_TEST_PROGRESS, 0, testTotal);
        long watchdogDelay = Math.min(testTotal * 6000L + 60000L, 12 * 60 * 1000L);
        AndroidUtilities.cancelRunOnUIThread(testWatchdog);
        AndroidUtilities.runOnUIThread(testWatchdog, watchdogDelay);
        testBatch(snapshot, 0);
    }

    private void testBatch(final ArrayList<ProxyItem> list, final int index) {
        if (!testing) {
            return;
        }
        final int end = Math.min(list.size(), index + TEST_BATCH);
        if (index >= end) {
            finishTesting();
            return;
        }
        final AtomicInteger remaining = new AtomicInteger(end - index);
        for (int a = index; a < end; a++) {
            final ProxyItem item = list.get(a);
            long now = SystemClock.elapsedRealtime();
            if (item.checking || now - item.lastCheckElapsed < RECHECK_MIN_INTERVAL) {
                processedCount++;
                notifyListeners(EVENT_TEST_PROGRESS, processedCount, testTotal);
                if (remaining.decrementAndGet() == 0) {
                    testBatch(list, end);
                }
                continue;
            }
            item.checking = true;
            item.lastCheckElapsed = now;
            final int account = UserConfig.selectedAccount;
            ConnectionsManager.getInstance(account).checkProxy(item.toSettings(), time -> AndroidUtilities.runOnUIThread(() -> {
                item.checking = false;
                if (time == -1) {
                    item.available = false;
                    item.ping = -1;
                    item.deadStreak++;
                    FileLog.d(TAG + ": DEAD " + item.host + ":" + item.port + " (streak " + item.deadStreak + ")");
                } else {
                    item.available = true;
                    item.ping = (int) time;
                    item.lastOkAt = System.currentTimeMillis();
                    item.deadStreak = 0;
                }
                cycleTestedCount++;
                if (time != -1) {
                    cycleSuccessCount++;
                }
                processedCount++;
                notifyListeners(EVENT_TEST_PROGRESS, processedCount, testTotal);
                if (remaining.decrementAndGet() == 0) {
                    synchronized (proxies) {
                        sortProxies();
                    }
                    saveToDisk();
                    testBatch(list, end);
                }
            }));
        }
    }

    private void finishTesting() {
        testing = false;
        lastTestAt = System.currentTimeMillis();
        AndroidUtilities.cancelRunOnUIThread(testWatchdog);
        autoRemoveDeadProxies();
        synchronized (proxies) {
            sortProxies();
            if (proxies.size() > MAX_PROXIES) {
                proxies.subList(MAX_PROXIES, proxies.size()).clear();
            }
        }
        saveToDisk();
        notifyListeners(EVENT_TEST_DONE, processedCount, testTotal);
    }

    // ---------------------------------------------------------------- auto cleanup

    /**
     * AmberGram fork: automatically removes proxies that failed their MTProto
     * handshake. Every removal also cleans the official SharedConfig proxy list
     * so dead entries never accumulate in the system proxy screen, and if the
     * currently active proxy died, the best surviving proxy (lowest ping) is
     * connected automatically instead; if nothing survived, the proxy is
     * switched off cleanly instead of leaving the user with a broken
     * "connected" state.
     */
    private void autoRemoveDeadProxies() {
        final int tested = cycleTestedCount;
        final int successes = cycleSuccessCount;
        boolean massFailure = tested >= OFFLINE_GUARD_MIN_TESTED && successes == 0;
        boolean offlineDevice = successes == 0 && tested > 0 && !isDeviceOnline();
        if (massFailure || offlineDevice) {
            // Not a single proxy answered — most likely the device lost
            // connectivity, not every proxy dying at once. Keep the list intact.
            FileLog.d(TAG + ": cleanup skipped, all " + tested + " tests failed (device offline or network outage)");
            return;
        }
        ArrayList<ProxyItem> removed = new ArrayList<>();
        ProxyItem best = null;
        synchronized (proxies) {
            Iterator<ProxyItem> iterator = proxies.iterator();
            while (iterator.hasNext()) {
                ProxyItem item = iterator.next();
                if (item.checking) {
                    continue;
                }
                if (!item.available && item.deadStreak >= REMOVE_AFTER_FAILS) {
                    removed.add(item);
                    iterator.remove();
                }
            }
            for (int a = 0; a < proxies.size(); a++) {
                ProxyItem item = proxies.get(a);
                if (item.available && item.ping >= 0 && (best == null || item.ping < best.ping)) {
                    best = item;
                }
            }
        }
        if (removed.isEmpty()) {
            return;
        }
        lastRemovedCount = removed.size();
        final ArrayList<ProxyItem> removedFinal = removed;
        final ProxyItem bestFinal = best;
        FileLog.d(TAG + ": auto-removed " + removed.size() + " dead proxies");
        AndroidUtilities.runOnUIThread(() -> cleanupSharedConfig(removedFinal, bestFinal));
        notifyListeners(EVENT_LIST_CLEANED, lastRemovedCount, 0);
    }

    private void cleanupSharedConfig(ArrayList<ProxyItem> removed, ProxyItem bestFallback) {
        try {
            SharedConfig.loadProxyList();
            SharedConfig.ProxyInfo diedCurrent = null;
            for (int a = 0; a < removed.size(); a++) {
                ProxyItem item = removed.get(a);
                SharedConfig.ProxyInfo match = findSharedProxy(item.host, item.port, item.secret);
                if (match == null) {
                    continue;
                }
                if (match == SharedConfig.currentProxy) {
                    diedCurrent = match;
                } else {
                    SharedConfig.deleteProxy(match);
                }
            }
            if (diedCurrent != null) {
                boolean wasEnabled = MessagesController.getGlobalMainSettings().getBoolean("proxy_enabled", false);
                if (wasEnabled && bestFallback != null) {
                    FileLog.d(TAG + ": active proxy died, switching to " + bestFallback.host + ":" + bestFallback.port);
                    connectTo(bestFallback);
                } else {
                    FileLog.d(TAG + ": active proxy died, no replacement — proxy disabled");
                    SharedConfig.deleteProxy(diedCurrent);
                }
            }
            if (diedCurrent != null && SharedConfig.currentProxy != diedCurrent) {
                SharedConfig.deleteProxy(diedCurrent);
            }
        } catch (Throwable t) {
            FileLog.e(t);
        }
    }

    private static SharedConfig.ProxyInfo findSharedProxy(String host, int port, String secret) {
        for (int a = 0; a < SharedConfig.proxyList.size(); a++) {
            SharedConfig.ProxyInfo info = SharedConfig.proxyList.get(a);
            if (info != null && info.settings != null
                    && Objects.equals(info.settings.getAddress(), host)
                    && info.settings.getPort() == port
                    && Objects.equals(info.settings.getSecret(), secret)) {
                return info;
            }
        }
        return null;
    }

    private static boolean isDeviceOnline() {
        try {
            ConnectivityManager manager = (ConnectivityManager) ApplicationLoader.applicationContext.getSystemService(Context.CONNECTIVITY_SERVICE);
            if (manager == null) {
                return true;
            }
            NetworkInfo info = manager.getActiveNetworkInfo();
            return info != null && info.isConnected();
        } catch (Throwable t) {
            return true;
        }
    }

    private void sortProxies() {
        Collections.sort(proxies, (o1, o2) -> Integer.compare(sortScore(o1), sortScore(o2)));
    }

    private int sortScore(ProxyItem item) {
        if (item.available && item.ping >= 0) {
            return item.ping;
        }
        if (item.available) {
            return 5000 + Math.max(0, item.sourcePing);
        }
        if (item.deadStreak > 0) {
            return 1_000_000 + Math.max(0, item.sourcePing);
        }
        return 100_000 + Math.max(0, item.sourcePing);
    }

    // ---------------------------------------------------------------- connect

    public void connectTo(ProxyItem item) {
        try {
            ProxySettings settings = item.toSettings();
            SharedConfig.ProxyInfo info = SharedConfig.addProxy(new SharedConfig.ProxyInfo(settings));
            SharedConfig.currentProxy = info;
            SharedPreferences preferences = MessagesController.getGlobalMainSettings();
            SharedPreferences.Editor editor = preferences.edit();
            editor.putBoolean("proxy_enabled", true);
            settings.toSharedPreferences(editor);
            editor.commit();
            ConnectionsManager.setProxySettings(true, settings);
            NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.proxySettingsChanged);
        } catch (Throwable t) {
            FileLog.e(t);
        }
    }

    // ---------------------------------------------------------------- state

    public ArrayList<ProxyItem> getProxiesSnapshot() {
        synchronized (proxies) {
            return new ArrayList<>(proxies);
        }
    }

    public int getTotalCount() {
        synchronized (proxies) {
            return proxies.size();
        }
    }

    public int getWorkingCount() {
        int count = 0;
        ArrayList<ProxyItem> snapshot = getProxiesSnapshot();
        for (int a = 0; a < snapshot.size(); a++) {
            if (snapshot.get(a).available) {
                count++;
            }
        }
        return count;
    }

    public boolean isFetching() {
        return fetching;
    }

    public boolean isTesting() {
        return testing;
    }

    public int getProcessedCount() {
        return processedCount;
    }

    public int getTestTotal() {
        return testTotal;
    }

    public int getFailedSourceCount() {
        return failedSourceCount;
    }

    public int getLastRemovedCount() {
        return lastRemovedCount;
    }

    public long getLastFetchAt() {
        return lastFetchAt;
    }

    public long getLastTestAt() {
        return lastTestAt;
    }

    public void addListener(Listener listener) {
        synchronized (listeners) {
            if (!listeners.contains(listener)) {
                listeners.add(listener);
            }
        }
    }

    public void removeListener(Listener listener) {
        synchronized (listeners) {
            listeners.remove(listener);
        }
    }

    private void notifyListeners(int event, int done, int total) {
        ArrayList<Listener> copy;
        synchronized (listeners) {
            copy = new ArrayList<>(listeners);
        }
        for (int a = 0; a < copy.size(); a++) {
            Listener listener = copy.get(a);
            AndroidUtilities.runOnUIThread(() -> listener.onProxyEvent(event, done, total));
        }
    }

    // ---------------------------------------------------------------- persistence

    private SharedPreferences prefs() {
        return ApplicationLoader.applicationContext.getSharedPreferences("ambergram_proxies", Context.MODE_PRIVATE);
    }

    private void saveToDisk() {
        try {
            JSONArray array = new JSONArray();
            synchronized (proxies) {
                for (int a = 0; a < proxies.size(); a++) {
                    ProxyItem item = proxies.get(a);
                    JSONObject object = new JSONObject();
                    object.put("h", item.host);
                    object.put("p", item.port);
                    object.put("s", item.secret);
                    object.put("src", item.source);
                    object.put("sp", item.sourcePing);
                    object.put("g", item.ping);
                    object.put("a", item.available ? 1 : 0);
                    object.put("ok", item.lastOkAt);
                    object.put("d", item.deadStreak);
                    array.put(object);
                }
            }
            prefs().edit()
                    .putString("data", array.toString())
                    .putLong("last_fetch", lastFetchAt)
                    .putLong("last_test", lastTestAt)
                    .putInt("failed_sources", failedSourceCount)
                    .putInt("last_removed", lastRemovedCount)
                    .apply();
        } catch (Throwable t) {
            FileLog.e(t);
        }
    }

    private void loadFromDisk() {
        try {
            lastFetchAt = prefs().getLong("last_fetch", 0);
            lastTestAt = prefs().getLong("last_test", 0);
            failedSourceCount = prefs().getInt("failed_sources", 0);
            lastRemovedCount = prefs().getInt("last_removed", 0);
            String raw = prefs().getString("data", null);
            if (raw == null) {
                return;
            }
            JSONArray array = new JSONArray(raw);
            synchronized (proxies) {
                proxies.clear();
                for (int a = 0; a < array.length(); a++) {
                    JSONObject object = array.optJSONObject(a);
                    if (object == null) {
                        continue;
                    }
                    ProxyItem item = new ProxyItem();
                    item.host = object.optString("h", "");
                    item.port = object.optInt("p", 0);
                    item.secret = object.optString("s", "");
                    item.source = object.optString("src", "");
                    item.sourcePing = object.optInt("sp", -1);
                    item.ping = object.optInt("g", -1);
                    item.available = object.optInt("a", 0) == 1;
                    item.lastOkAt = object.optLong("ok", 0);
                    item.deadStreak = object.optInt("d", 0);
                    if (validProxy(item.host, item.port, item.secret)) {
                        proxies.add(item);
                    }
                }
            }
        } catch (Throwable t) {
            FileLog.e(t);
        }
    }
}
```


## ۵-۲ AmbergramProxyReceiver.java — کد کامل

```java
package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * AmberGram fork: fires every 6 hours to refresh + retest the in-app free
 * proxy list (see AmbergramProxyManager).
 */
public class AmbergramProxyReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            AmbergramProxyManager.getInstance().onAlarmReceived();
        } catch (Throwable ignore) {
        }
    }
}
```


## ۵-۳ AmbergramProxyActivity.java — کد کامل

```java
package org.telegram.ui;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.telegram.messenger.AmbergramProxyManager;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;
import org.telegram.ui.Cells.TextInfoPrivacyCell;
import org.telegram.ui.Components.LayoutHelper;

import java.util.ArrayList;

/**
 * AmberGram fork: dedicated page for the in-app free proxy list.
 * Lists proxies fetched from public GitHub collectors, shows live
 * availability/ping and connects through the official proxy system.
 * Opened from AmberGram Settings to keep the settings hub clean.
 */
public class AmbergramProxyActivity extends BaseFragment implements AmbergramProxyManager.Listener {

    private static final int BRAND_ORANGE = 0xFFF97316;
    private static final int STATE_GREEN = 0xFF27B434;
    private static final int STATE_RED = 0xFFE13B47;

    private static final int MAX_VISIBLE_ROWS = 90;

    private LinearLayout listContainer;
    private TextView statusTextView;
    private TextView refreshButton;
    private TextView testButton;
    private TextView emptyTextView;
    private boolean updateScheduled;

    @Override
    public boolean onFragmentCreate() {
        AmbergramProxyManager.getInstance().addListener(this);
        AmbergramProxyManager manager = AmbergramProxyManager.getInstance();
        if (manager.getLastFetchAt() == 0 && !manager.isFetching()) {
            manager.runUpdateCycle();
        }
        return super.onFragmentCreate();
    }

    @Override
    public void onFragmentDestroy() {
        AmbergramProxyManager.getInstance().removeListener(this);
        super.onFragmentDestroy();
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(LocaleController.getString(R.string.AmbergramProxySection));
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        fragmentView = new FrameLayout(context);
        ThemeBind.backgroundColor(fragmentView, Theme.key_windowBackgroundGray);

        ScrollView scrollView = new ScrollView(context);
        scrollView.setFillViewport(true);
        ((FrameLayout) fragmentView).addView(scrollView, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.MATCH_PARENT));

        LinearLayout contentWrapper = new LinearLayout(context);
        contentWrapper.setOrientation(LinearLayout.VERTICAL);
        scrollView.addView(contentWrapper, new ScrollView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        LinearLayout card = new LinearLayout(context);
        card.setOrientation(LinearLayout.VERTICAL);
        ThemeBind.backgroundColor(card, Theme.key_windowBackgroundWhite);
        contentWrapper.addView(card, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        statusTextView = new TextView(context);
        statusTextView.setTypeface(AndroidUtilities.bold());
        statusTextView.setTextSize(13);
        ThemeBind.textColor(statusTextView, Theme.key_windowBackgroundWhiteGrayText2, null);
        statusTextView.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(12), AndroidUtilities.dp(21), AndroidUtilities.dp(8));
        card.addView(statusTextView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        LinearLayout buttonsRow = new LinearLayout(context);
        buttonsRow.setOrientation(LinearLayout.HORIZONTAL);
        buttonsRow.setGravity((LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT) | Gravity.CENTER_VERTICAL);
        buttonsRow.setPadding(AndroidUtilities.dp(8), AndroidUtilities.dp(4), AndroidUtilities.dp(8), AndroidUtilities.dp(8));
        card.addView(buttonsRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        refreshButton = makeTextButton(context, LocaleController.getString(R.string.AmbergramProxyRefresh), BRAND_ORANGE);
        refreshButton.setOnClickListener(v -> AmbergramProxyManager.getInstance().runUpdateCycle());
        buttonsRow.addView(refreshButton, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        testButton = makeTextButton(context, LocaleController.getString(R.string.AmbergramProxyTestAll), BRAND_ORANGE);
        testButton.setOnClickListener(v -> AmbergramProxyManager.getInstance().startTesting());
        buttonsRow.addView(testButton, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        emptyTextView = new TextView(context);
        emptyTextView.setTypeface(AndroidUtilities.bold());
        emptyTextView.setTextSize(14);
        ThemeBind.textColor(emptyTextView, Theme.key_windowBackgroundWhiteGrayText2, null);
        emptyTextView.setGravity(Gravity.CENTER);
        emptyTextView.setPadding(AndroidUtilities.dp(28), AndroidUtilities.dp(24), AndroidUtilities.dp(28), AndroidUtilities.dp(28));
        card.addView(emptyTextView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        listContainer = new LinearLayout(context);
        listContainer.setOrientation(LinearLayout.VERTICAL);
        card.addView(listContainer, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextInfoPrivacyCell footerCell = new TextInfoPrivacyCell(context, 24, null);
        footerCell.setText(LocaleController.getString(R.string.AmbergramProxyHint));
        contentWrapper.addView(footerCell, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        refreshList();
        return fragmentView;
    }

    private TextView makeTextButton(Context context, String text, int color) {
        TextView button = new TextView(context);
        button.setTypeface(AndroidUtilities.bold());
        button.setTextSize(15);
        button.setTextColor(color);
        button.setText(text);
        button.setGravity(Gravity.CENTER);
        button.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(12), AndroidUtilities.dp(16), AndroidUtilities.dp(12));
        return button;
    }

    private View makeProxyRow(Context context, final AmbergramProxyManager.ProxyItem item, boolean showDivider) {
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.VERTICAL);
        row.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(10), AndroidUtilities.dp(21), AndroidUtilities.dp(10));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> {
            AmbergramProxyManager.getInstance().connectTo(item);
            if (getParentActivity() != null) {
                Toast.makeText(getParentActivity(),
                        LocaleController.formatString(R.string.AmbergramProxyConnected, item.host),
                        Toast.LENGTH_SHORT).show();
            }
        });
        row.setOnLongClickListener(v -> {
            try {
                AndroidUtilities.addToClipboard(item.toSettings().getLink());
                if (getParentActivity() != null) {
                    Toast.makeText(getParentActivity(),
                            LocaleController.getString(R.string.AmbergramProxyCopied),
                            Toast.LENGTH_SHORT).show();
                }
            } catch (Exception ignore) {
            }
            return true;
        });

        LinearLayout topLine = new LinearLayout(context);
        topLine.setOrientation(LinearLayout.HORIZONTAL);
        topLine.setGravity(Gravity.CENTER_VERTICAL);
        row.addView(topLine, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView hostView = new TextView(context);
        hostView.setTypeface(AndroidUtilities.bold());
        hostView.setTextSize(15);
        ThemeBind.textColor(hostView, Theme.key_windowBackgroundWhiteBlackText, null);
        hostView.setText(item.host + ":" + item.port);
        hostView.setLines(1);
        hostView.setMaxLines(1);
        hostView.setSingleLine(true);
        hostView.setEllipsize(android.text.TextUtils.TruncateAt.MIDDLE);
        topLine.addView(hostView, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView connectView = makeTextButton(context, LocaleController.getString(R.string.AmbergramProxyConnect), BRAND_ORANGE);
        topLine.addView(connectView, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView statusView = new TextView(context);
        statusView.setTypeface(AndroidUtilities.bold());
        statusView.setTextSize(13);
        statusView.setText(itemStatusText(item));
        statusView.setTextColor(itemStatusColor(item));
        row.addView(statusView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL, 0, AndroidUtilities.dp(3), 0, 0));

        if (showDivider) {
            View divider = new View(context);
            divider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
            row.addView(divider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1, 0, AndroidUtilities.dp(4), 0, 0));
        }
        return row;
    }

    private String itemStatusText(AmbergramProxyManager.ProxyItem item) {
        String source = LocaleController.formatString(R.string.AmbergramProxySource, item.source);
        if (item.checking) {
            return source;
        }
        if (item.available && item.ping >= 0) {
            return source + "  •  " + LocaleController.formatString(R.string.AmbergramProxyWorking, String.valueOf(item.ping));
        }
        if (item.deadStreak > 0) {
            return source + "  •  " + LocaleController.getString(R.string.AmbergramProxyDead);
        }
        return source + "  •  " + LocaleController.getString(R.string.AmbergramProxyUntested);
    }

    private int itemStatusColor(AmbergramProxyManager.ProxyItem item) {
        if (item.checking) {
            return BRAND_ORANGE;
        }
        if (item.available && item.ping >= 0) {
            return item.ping < 800 ? STATE_GREEN : BRAND_ORANGE;
        }
        if (item.deadStreak > 0) {
            return STATE_RED;
        }
        return getThemedColor(Theme.key_windowBackgroundWhiteGrayText2);
    }

    private String relativeTime(long timestamp) {
        if (timestamp <= 0) {
            return LocaleController.getString(R.string.AmbergramProxyTimeNever);
        }
        long minutes = (System.currentTimeMillis() - timestamp) / 60000L;
        if (minutes < 1) {
            return LocaleController.getString(R.string.AmbergramProxyTimeNow);
        }
        if (minutes < 60) {
            return LocaleController.formatString(R.string.AmbergramProxyTimeMinutes, String.valueOf(minutes));
        }
        long hours = minutes / 60;
        if (hours < 24) {
            return LocaleController.formatString(R.string.AmbergramProxyTimeHours, String.valueOf(hours));
        }
        return LocaleController.formatString(R.string.AmbergramProxyTimeDays, String.valueOf(hours / 24));
    }

    private String buildStatusText() {
        AmbergramProxyManager manager = AmbergramProxyManager.getInstance();
        if (manager.isFetching()) {
            return LocaleController.getString(R.string.AmbergramProxyFetching);
        }
        if (manager.isTesting()) {
            return LocaleController.formatString(R.string.AmbergramProxyTesting,
                    String.valueOf(manager.getProcessedCount()), String.valueOf(manager.getTestTotal()));
        }
        int total = manager.getTotalCount();
        if (total == 0) {
            return LocaleController.getString(R.string.AmbergramProxyEmpty);
        }
        StringBuilder builder = new StringBuilder();
        builder.append(LocaleController.formatString(R.string.AmbergramProxyLastUpdate, relativeTime(manager.getLastFetchAt())));
        builder.append("  •  ");
        builder.append(LocaleController.formatString(R.string.AmbergramProxyStats,
                String.valueOf(manager.getWorkingCount()), String.valueOf(total)));
        if (manager.getLastRemovedCount() > 0) {
            builder.append("  •  ");
            builder.append(LocaleController.formatString(R.string.AmbergramProxyRemoved,
                    String.valueOf(manager.getLastRemovedCount())));
        }
        if (manager.getFailedSourceCount() > 0) {
            builder.append("  •  ");
            builder.append(LocaleController.formatString(R.string.AmbergramProxyFailedSources,
                    String.valueOf(manager.getFailedSourceCount())));
        }
        return builder.toString();
    }

    private void refreshList() {
        if (listContainer == null || listContainer.getContext() == null) {
            return;
        }
        Context context = listContainer.getContext();
        AmbergramProxyManager manager = AmbergramProxyManager.getInstance();
        ArrayList<AmbergramProxyManager.ProxyItem> items = manager.getProxiesSnapshot();

        listContainer.removeAllViews();
        boolean busy = manager.isFetching() || manager.isTesting();
        boolean empty = items.isEmpty();

        emptyTextView.setVisibility(empty ? View.VISIBLE : View.GONE);
        if (empty) {
            emptyTextView.setText(manager.isFetching()
                    ? LocaleController.getString(R.string.AmbergramProxyFetching)
                    : LocaleController.getString(R.string.AmbergramProxyEmpty));
        }

        int visible = Math.min(items.size(), MAX_VISIBLE_ROWS);
        for (int a = 0; a < visible; a++) {
            listContainer.addView(makeProxyRow(context, items.get(a), a != visible - 1));
        }

        if (visible > 0 && items.size() > visible) {
            TextView moreView = new TextView(context);
            moreView.setTypeface(AndroidUtilities.bold());
            moreView.setTextSize(13);
            ThemeBind.textColor(moreView, Theme.key_windowBackgroundWhiteGrayText2, null);
            moreView.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(6), AndroidUtilities.dp(21), AndroidUtilities.dp(10));
            moreView.setText(LocaleController.formatString(R.string.AmbergramProxyShowMore,
                    String.valueOf(visible), String.valueOf(items.size())));
            listContainer.addView(moreView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));
        }

        if (statusTextView != null) {
            statusTextView.setText(buildStatusText());
        }

        if (refreshButton != null) {
            refreshButton.setEnabled(!manager.isFetching());
            refreshButton.setAlpha(manager.isFetching() ? 0.45f : 1f);
        }
        if (testButton != null) {
            testButton.setEnabled(!busy && !empty);
            testButton.setAlpha(busy || empty ? 0.45f : 1f);
        }
    }

    @Override
    public void onProxyEvent(int event, int done, int total) {
        if (event == AmbergramProxyManager.EVENT_LIST_CLEANED && done > 0 && getParentActivity() != null) {
            Toast.makeText(getParentActivity(),
                    LocaleController.formatString(R.string.AmbergramProxyRemoved, String.valueOf(done)),
                    Toast.LENGTH_SHORT).show();
        }
        AndroidUtilities.runOnUIThread(() -> {
            if (!updateScheduled) {
                updateScheduled = true;
                AndroidUtilities.runOnUIThread(() -> {
                    updateScheduled = false;
                    refreshList();
                }, 300);
            }
        });
    }
}
```


## ۵-۴ دیباگ پروکسی

- لاگ‌ها با تگ رشته‌ای `AmbergramProxy` می‌روند (`FileLog.d(TAG + ": ...")`) — در logcat:
  ```bash
  adb logcat | grep AmbergramProxy
  ```
- رویدادها برای UI: `EVENT_FETCH_STARTED/FETCH_DONE/TEST_PROGRESS/TEST_DONE/LIST_CLEANED` (کدهای 0..4).
- اگر لیست خالی ماند: همه ۶ منبع خطا خورده‌اند (`failedSourceCount` روی status bar صفحه نمایش داده می‌شود) — معمولاً قطعی شبکه؛ دکمه «Update sources» دوباره تلاش می‌کند.
- اگر پروکسی فعال خودکار جابجا شد: `cleanupSharedConfig` — وقتی proxy فعال حذف شد، بهترین بازمانده وصل می‌شود؛ اگر هیچ‌کس نماند، پروکسی خاموش می‌شود. لاگ: `active proxy died, switching to ...`.
- تست‌های گیر‌افتاده: `testWatchdog` بعد از `testTotal*6s+60s` (سقف ۱۲ دقیقه) کل سیکل تست را می‌بندد.

---

# بخش ۶ — هاب تنظیمات AmberGram

## ۶-۱ AmbergramSettingsActivity.java — کد کامل

ساختار صفحه: ScrollView > card سفید > سه ردیف ناوبری (صف دانلود → `AmbergramQueueActivity`، پروکسی → `AmbergramProxyActivity`، حالت شبح = toggle) + ۱۲ ردیف toggle در `toggleSpecs` (آیکون، کلید رشته عنوان، کلید رشته توضیح). رنگ برند `0xFFF97316`. هر toggle یک `AmberToggle` lambda-مانند با get/set دارد که به getter/setter کلاس‌های `AmberAntiAds`/`AmberMorphe` وصل است (`getToggleValue`/`setToggleValue` بر اساس `R.string.*` سوییچ می‌کنند).

```java
package org.telegram.ui;

import android.content.Context;
import android.graphics.PorterDuff;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.telegram.messenger.AmberAntiAds;
import org.telegram.messenger.AmberGhost;
import org.telegram.messenger.AmberMorphe;
import org.telegram.messenger.AmbergramProxyManager;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.DownloadQueueController;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;
import org.telegram.ui.Cells.HeaderCell;
import org.telegram.ui.Cells.TextInfoPrivacyCell;
import org.telegram.ui.Components.LayoutHelper;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * AmberGram fork: settings hub for AmberGram features.
 * The sequential download queue lives on its own page (AmbergramQueueActivity)
 * so this hub stays clean and has room for upcoming features.
 */
public class AmbergramSettingsActivity extends BaseFragment implements DownloadQueueController.QueueListener, AmbergramProxyManager.Listener {

    private static final int BRAND_ORANGE = 0xFFF97316;

    private TextView queueValueView;
    private TextView proxyValueView;
    private TextView ghostValueView;
    private final HashMap<Integer, TextView> toggleValueViews = new HashMap<>();
    private final HashMap<Integer, AmberToggle> toggles = new HashMap<>();
    private boolean updateScheduled;
    private boolean proxyUpdateScheduled;

    private interface AmberToggle {
        boolean get();
        void set(boolean value);
    }

    @Override
    public boolean onFragmentCreate() {
        DownloadQueueController.getInstance(currentAccount).addQueueListener(this);
        AmbergramProxyManager.getInstance().addListener(this);
        return super.onFragmentCreate();
    }

    @Override
    public void onFragmentDestroy() {
        DownloadQueueController.getInstance(currentAccount).removeQueueListener(this);
        AmbergramProxyManager.getInstance().removeListener(this);
        super.onFragmentDestroy();
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(LocaleController.getString(R.string.AmbergramSettings));
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        fragmentView = new FrameLayout(context);
        ThemeBind.backgroundColor(fragmentView, Theme.key_windowBackgroundGray);

        ScrollView scrollView = new ScrollView(context);
        scrollView.setFillViewport(true);
        ((FrameLayout) fragmentView).addView(scrollView, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.MATCH_PARENT));

        LinearLayout contentWrapper = new LinearLayout(context);
        contentWrapper.setOrientation(LinearLayout.VERTICAL);
        scrollView.addView(contentWrapper, new ScrollView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        LinearLayout card = new LinearLayout(context);
        card.setOrientation(LinearLayout.VERTICAL);
        ThemeBind.backgroundColor(card, Theme.key_windowBackgroundWhite);
        contentWrapper.addView(card, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        LinearLayout queueRow = makeQueueRow(context);
        card.addView(queueRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        View queueDivider = new View(context);
        queueDivider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
        card.addView(queueDivider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1));

        LinearLayout proxyRow = makeProxyRow(context);
        card.addView(proxyRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        View proxyDivider = new View(context);
        proxyDivider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
        card.addView(proxyDivider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1));

        LinearLayout ghostRow = makeGhostRow(context);
        card.addView(ghostRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        int[][] toggleSpecs = {
                {R.drawable.msg_block, R.string.AmberNoSponsored, R.string.AmberNoSponsoredDesc},
                {R.drawable.msg_channel, R.string.AmberNoRecommendations, R.string.AmberNoRecommendationsDesc},
                {R.drawable.msg_speed, R.string.AmberTurboDownload, R.string.AmberTurboDownloadDesc},
                {R.drawable.msg_sticker, R.string.AmberNoGreetings, R.string.AmberNoGreetingsDesc},
                {R.drawable.msg_delete, R.string.AmberAntiDelete, R.string.AmberAntiDeleteDesc},
                {R.drawable.msg_photo_blur, R.string.AmberAntiDisappearing, R.string.AmberAntiDisappearingDesc},
                {R.drawable.msg_camera, R.string.AmberNoScreenshotNotify, R.string.AmberNoScreenshotNotifyDesc},
                {R.drawable.msg_copy, R.string.AmberBypassNoforwards, R.string.AmberBypassNoforwardsDesc},
                {R.drawable.msg_download, R.string.AmberNoAutoUpdate, R.string.AmberNoAutoUpdateDesc},
                {R.drawable.msg_block2, R.string.AmberNoChannelSwitch, R.string.AmberNoChannelSwitchDesc},
                {R.drawable.msg_mute, R.string.AmberHideStoriesRead, R.string.AmberHideStoriesReadDesc},
                {R.drawable.msg_secret, R.string.AmberBypassTranslation, R.string.AmberBypassTranslationDesc}
        };
        for (int[] spec : toggleSpecs) {
            View divider = new View(context);
            divider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
            card.addView(divider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1));
            LinearLayout toggleRow = makeToggleRow(context, spec[0], spec[1], spec[2]);
            card.addView(toggleRow, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        }

        TextInfoPrivacyCell footerCell = new TextInfoPrivacyCell(context, 24, null);
        footerCell.setText(LocaleController.getString(R.string.AmbergramQueueComingSoon));
        contentWrapper.addView(footerCell, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        refreshQueueValue();
        refreshProxyValue();
        refreshGhostValue();
        refreshAllToggles();
        return fragmentView;
    }

    private LinearLayout makeQueueRow(Context context) {
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> presentFragment(new AmbergramQueueActivity()));

        ImageView iconView = new ImageView(context);
        iconView.setImageResource(R.drawable.msg_download);
        iconView.setColorFilter(BRAND_ORANGE, PorterDuff.Mode.SRC_IN);
        row.addView(iconView, LayoutHelper.createLinear(AndroidUtilities.dp(26), AndroidUtilities.dp(26), 0, Gravity.CENTER_VERTICAL, 0, 0, AndroidUtilities.dp(14), 0));

        LinearLayout textCol = new LinearLayout(context);
        textCol.setOrientation(LinearLayout.VERTICAL);
        row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView titleView = new TextView(context);
        titleView.setTypeface(AndroidUtilities.bold());
        titleView.setTextSize(16);
        ThemeBind.textColor(titleView, Theme.key_windowBackgroundWhiteBlackText, null);
        titleView.setText(LocaleController.getString(R.string.AmbergramQueueSection));
        titleView.setSingleLine(true);
        textCol.addView(titleView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        queueValueView = new TextView(context);
        queueValueView.setTypeface(AndroidUtilities.bold());
        queueValueView.setTextSize(13);
        ThemeBind.textColor(queueValueView, Theme.key_windowBackgroundWhiteGrayText2, null);
        queueValueView.setSingleLine(true);
        textCol.addView(queueValueView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView chevronView = new TextView(context);
        chevronView.setTypeface(AndroidUtilities.bold());
        chevronView.setTextSize(20);
        ThemeBind.textColor(chevronView, Theme.key_windowBackgroundWhiteGrayText2, null);
        chevronView.setText(LocaleController.isRTL ? "‹" : "›");
        chevronView.setGravity(Gravity.CENTER);
        row.addView(chevronView, LayoutHelper.createLinear(AndroidUtilities.dp(28), ViewGroup.LayoutParams.WRAP_CONTENT, 0, Gravity.CENTER_VERTICAL, AndroidUtilities.dp(8), 0, 0, 0));

        return row;
    }

    private void refreshQueueValue() {
        if (queueValueView == null || getContext() == null) {
            return;
        }
        ArrayList<DownloadQueueController.QueueItem> items = DownloadQueueController.getInstance(currentAccount).getQueueSnapshot();
        int waiting = 0, downloading = 0;
        for (int a = 0; a < items.size(); a++) {
            DownloadQueueController.QueueItem item = items.get(a);
            if (item.state == DownloadQueueController.STATE_PENDING) {
                waiting++;
            } else if (item.state == DownloadQueueController.STATE_DOWNLOADING) {
                downloading++;
            }
        }
        if (waiting > 0 || downloading > 0) {
            queueValueView.setText(LocaleController.formatString(R.string.AmbergramQueueSummary, String.valueOf(waiting), String.valueOf(downloading)));
            queueValueView.setTextColor(BRAND_ORANGE);
        } else {
            queueValueView.setText(LocaleController.getString(R.string.AmbergramQueueRowIdle));
            queueValueView.setTextColor(getThemedColor(Theme.key_windowBackgroundWhiteGrayText2));
        }
    }

    private LinearLayout makeProxyRow(Context context) {
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> presentFragment(new AmbergramProxyActivity()));

        ImageView iconView = new ImageView(context);
        iconView.setImageResource(R.drawable.ic_ambergram_proxy);
        iconView.setColorFilter(BRAND_ORANGE, PorterDuff.Mode.SRC_IN);
        row.addView(iconView, LayoutHelper.createLinear(AndroidUtilities.dp(26), AndroidUtilities.dp(26), 0, Gravity.CENTER_VERTICAL, 0, 0, AndroidUtilities.dp(14), 0));

        LinearLayout textCol = new LinearLayout(context);
        textCol.setOrientation(LinearLayout.VERTICAL);
        row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView titleView = new TextView(context);
        titleView.setTypeface(AndroidUtilities.bold());
        titleView.setTextSize(16);
        ThemeBind.textColor(titleView, Theme.key_windowBackgroundWhiteBlackText, null);
        titleView.setText(LocaleController.getString(R.string.AmbergramProxySection));
        titleView.setSingleLine(true);
        textCol.addView(titleView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        proxyValueView = new TextView(context);
        proxyValueView.setTypeface(AndroidUtilities.bold());
        proxyValueView.setTextSize(13);
        ThemeBind.textColor(proxyValueView, Theme.key_windowBackgroundWhiteGrayText2, null);
        proxyValueView.setSingleLine(true);
        textCol.addView(proxyValueView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView chevronView = new TextView(context);
        chevronView.setTypeface(AndroidUtilities.bold());
        chevronView.setTextSize(20);
        ThemeBind.textColor(chevronView, Theme.key_windowBackgroundWhiteGrayText2, null);
        chevronView.setText(LocaleController.isRTL ? "‹" : "›");
        chevronView.setGravity(Gravity.CENTER);
        row.addView(chevronView, LayoutHelper.createLinear(AndroidUtilities.dp(28), ViewGroup.LayoutParams.WRAP_CONTENT, 0, Gravity.CENTER_VERTICAL, AndroidUtilities.dp(8), 0, 0, 0));

        return row;
    }

    private LinearLayout makeGhostRow(Context context) {
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> {
            boolean newValue = !AmberGhost.isEnabled();
            AmberGhost.setEnabled(newValue);
            refreshGhostValue();
            if (getParentActivity() != null) {
                Toast.makeText(getParentActivity(), LocaleController.getString(R.string.AmberGhostDesc), Toast.LENGTH_SHORT).show();
            }
        });

        ImageView iconView = new ImageView(context);
        iconView.setImageResource(R.drawable.ghost);
        iconView.setColorFilter(BRAND_ORANGE, PorterDuff.Mode.SRC_IN);
        row.addView(iconView, LayoutHelper.createLinear(AndroidUtilities.dp(26), AndroidUtilities.dp(26), 0, Gravity.CENTER_VERTICAL, 0, 0, AndroidUtilities.dp(14), 0));

        LinearLayout textCol = new LinearLayout(context);
        textCol.setOrientation(LinearLayout.VERTICAL);
        row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView titleView = new TextView(context);
        titleView.setTypeface(AndroidUtilities.bold());
        titleView.setTextSize(16);
        ThemeBind.textColor(titleView, Theme.key_windowBackgroundWhiteBlackText, null);
        titleView.setText(LocaleController.getString(R.string.AmberGhostSection));
        titleView.setSingleLine(true);
        textCol.addView(titleView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        ghostValueView = new TextView(context);
        ghostValueView.setTypeface(AndroidUtilities.bold());
        ghostValueView.setTextSize(13);
        ghostValueView.setSingleLine(true);
        textCol.addView(ghostValueView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        return row;
    }

    private LinearLayout makeToggleRow(Context context, int iconRes, int titleRes, int descRes) {
        toggles.put(titleRes, new AmberToggle() {
            @Override
            public boolean get() {
                return getToggleValue(titleRes);
            }

            @Override
            public void set(boolean value) {
                setToggleValue(titleRes, value);
            }
        });
        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> {
            AmberToggle toggle = toggles.get(titleRes);
            boolean newValue = !toggle.get();
            toggle.set(newValue);
            refreshToggle(titleRes);
            if (getParentActivity() != null) {
                Toast.makeText(getParentActivity(), LocaleController.getString(descRes), Toast.LENGTH_SHORT).show();
            }
        });

        ImageView iconView = new ImageView(context);
        iconView.setImageResource(iconRes);
        iconView.setColorFilter(BRAND_ORANGE, PorterDuff.Mode.SRC_IN);
        row.addView(iconView, LayoutHelper.createLinear(AndroidUtilities.dp(26), AndroidUtilities.dp(26), 0, Gravity.CENTER_VERTICAL, 0, 0, AndroidUtilities.dp(14), 0));

        LinearLayout textCol = new LinearLayout(context);
        textCol.setOrientation(LinearLayout.VERTICAL);
        row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView titleView = new TextView(context);
        titleView.setTypeface(AndroidUtilities.bold());
        titleView.setTextSize(16);
        ThemeBind.textColor(titleView, Theme.key_windowBackgroundWhiteBlackText, null);
        titleView.setText(LocaleController.getString(titleRes));
        titleView.setSingleLine(true);
        textCol.addView(titleView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView valueView = new TextView(context);
        valueView.setTypeface(AndroidUtilities.bold());
        valueView.setTextSize(13);
        valueView.setSingleLine(true);
        toggleValueViews.put(titleRes, valueView);
        textCol.addView(valueView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        return row;
    }

    private boolean getToggleValue(int titleRes) {
        if (titleRes == R.string.AmberNoSponsored) {
            return AmberAntiAds.noSponsored();
        } else if (titleRes == R.string.AmberNoRecommendations) {
            return AmberAntiAds.noRecommendations();
        } else if (titleRes == R.string.AmberTurboDownload) {
            return AmberAntiAds.turboDownload();
        } else if (titleRes == R.string.AmberNoGreetings) {
            return AmberAntiAds.noGreetings();
        } else if (titleRes == R.string.AmberAntiDelete) {
            return AmberMorphe.antiDelete();
        } else if (titleRes == R.string.AmberAntiDisappearing) {
            return AmberMorphe.antiDisappearing();
        } else if (titleRes == R.string.AmberNoScreenshotNotify) {
            return AmberMorphe.noScreenshotNotify();
        } else if (titleRes == R.string.AmberBypassNoforwards) {
            return AmberMorphe.bypassNoforwards();
        } else if (titleRes == R.string.AmberNoAutoUpdate) {
            return AmberMorphe.noAutoUpdate();
        } else if (titleRes == R.string.AmberNoChannelSwitch) {
            return AmberMorphe.noChannelSwitch();
        } else if (titleRes == R.string.AmberHideStoriesRead) {
            return AmberMorphe.hideStoriesRead();
        } else if (titleRes == R.string.AmberBypassTranslation) {
            return AmberMorphe.bypassTranslation();
        }
        return false;
    }

    private void setToggleValue(int titleRes, boolean value) {
        if (titleRes == R.string.AmberNoSponsored) {
            AmberAntiAds.setNoSponsored(value);
        } else if (titleRes == R.string.AmberNoRecommendations) {
            AmberAntiAds.setNoRecommendations(value);
        } else if (titleRes == R.string.AmberTurboDownload) {
            AmberAntiAds.setTurboDownload(value);
        } else if (titleRes == R.string.AmberNoGreetings) {
            AmberAntiAds.setNoGreetings(value);
        } else if (titleRes == R.string.AmberAntiDelete) {
            AmberMorphe.setAntiDelete(value);
        } else if (titleRes == R.string.AmberAntiDisappearing) {
            AmberMorphe.setAntiDisappearing(value);
        } else if (titleRes == R.string.AmberNoScreenshotNotify) {
            AmberMorphe.setNoScreenshotNotify(value);
        } else if (titleRes == R.string.AmberBypassNoforwards) {
            AmberMorphe.setBypassNoforwards(value);
        } else if (titleRes == R.string.AmberNoAutoUpdate) {
            AmberMorphe.setNoAutoUpdate(value);
        } else if (titleRes == R.string.AmberNoChannelSwitch) {
            AmberMorphe.setNoChannelSwitch(value);
        } else if (titleRes == R.string.AmberHideStoriesRead) {
            AmberMorphe.setHideStoriesRead(value);
        } else if (titleRes == R.string.AmberBypassTranslation) {
            AmberMorphe.setBypassTranslation(value);
        }
    }

    private void refreshAllToggles() {
        for (int titleRes : toggleValueViews.keySet()) {
            refreshToggle(titleRes);
        }
    }

    private void refreshToggle(int titleRes) {
        TextView valueView = toggleValueViews.get(titleRes);
        if (valueView == null || getContext() == null) {
            return;
        }
        if (toggles.get(titleRes).get()) {
            valueView.setText(LocaleController.getString(R.string.AmberGhostOn));
            valueView.setTextColor(BRAND_ORANGE);
        } else {
            valueView.setText(LocaleController.getString(R.string.AmberGhostOff));
            valueView.setTextColor(getThemedColor(Theme.key_windowBackgroundWhiteGrayText2));
        }
    }

    private void refreshGhostValue() {
        if (ghostValueView == null || getContext() == null) {
            return;
        }
        if (AmberGhost.isEnabled()) {
            ghostValueView.setText(LocaleController.getString(R.string.AmberGhostOn));
            ghostValueView.setTextColor(BRAND_ORANGE);
        } else {
            ghostValueView.setText(LocaleController.getString(R.string.AmberGhostOff));
            ghostValueView.setTextColor(getThemedColor(Theme.key_windowBackgroundWhiteGrayText2));
        }
    }

    private void refreshProxyValue() {
        if (proxyValueView == null || getContext() == null) {
            return;
        }
        AmbergramProxyManager manager = AmbergramProxyManager.getInstance();
        if (manager.isFetching()) {
            proxyValueView.setText(LocaleController.getString(R.string.AmbergramProxyFetching));
            proxyValueView.setTextColor(BRAND_ORANGE);
            return;
        }
        if (manager.isTesting()) {
            proxyValueView.setText(LocaleController.formatString(R.string.AmbergramProxyTesting, String.valueOf(manager.getProcessedCount()), String.valueOf(manager.getTestTotal())));
            proxyValueView.setTextColor(BRAND_ORANGE);
            return;
        }
        int working = manager.getWorkingCount();
        if (working > 0) {
            proxyValueView.setText(LocaleController.formatString(R.string.AmbergramProxySettingsValue, String.valueOf(working)));
            proxyValueView.setTextColor(BRAND_ORANGE);
        } else {
            proxyValueView.setText(LocaleController.getString(R.string.AmbergramProxySubtitle));
            proxyValueView.setTextColor(getThemedColor(Theme.key_windowBackgroundWhiteGrayText2));
        }
    }

    @Override
    public void onProxyEvent(int event, int done, int total) {
        AndroidUtilities.runOnUIThread(() -> {
            if (!proxyUpdateScheduled) {
                proxyUpdateScheduled = true;
                AndroidUtilities.runOnUIThread(() -> {
                    proxyUpdateScheduled = false;
                    refreshProxyValue();
                }, 300);
            }
        });
    }

    @Override
    public void onQueueUpdated() {
        AndroidUtilities.runOnUIThread(() -> {
            if (!updateScheduled) {
                updateScheduled = true;
                AndroidUtilities.runOnUIThread(() -> {
                    updateScheduled = false;
                    refreshQueueValue();
                }, 300);
            }
        });
    }
}
```


## ۶-۲ ردیف در تنظیمات اصلی (SettingsActivity)

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java
index e2b917be3..afd8a3c42 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java
@@ -804,6 +804,7 @@ public class SettingsActivity extends BaseFragment implements NotificationCenter
         items.add(SettingCell.Factory.of(8, IconBackgroundColors.CYAN.top, IconBackgroundColors.CYAN.bottom, R.drawable.settings_devices, getString(R.string.SettingsDevices), getString(R.string.SettingsDevicesInfo)));
         items.add(SettingCell.Factory.of(9, IconBackgroundColors.ORANGE_DEEP.top, IconBackgroundColors.ORANGE_DEEP.bottom, R.drawable.settings_power, getString(R.string.SettingsPowerSaving), getString(R.string.SettingsPowerSavingInfo)));
         items.add(SettingCell.Factory.of(10, IconBackgroundColors.PURPLE.top, IconBackgroundColors.PURPLE.bottom, R.drawable.settings_language, getString(R.string.SettingsLanguage), LocaleController.getCurrentLanguageName()));
+        items.add(SettingCell.Factory.of(30, 0xFFF97316, 0xFFEA580C, R.drawable.ic_ambergram_settings, getString(R.string.AmbergramSettings)));
 
         items.add(UItem.asShadow(null));
         if (!walletAbove && getMessagesController().config.walletAvailable.get()) {
@@ -944,6 +945,9 @@ public class SettingsActivity extends BaseFragment implements NotificationCenter
             case 10:
                 presentSettingFragment(new LanguageSelectActivity());
                 break;
+            case 30:
+                presentSettingFragment(new AmbergramSettingsActivity());
+                break;
 
             case 11:
                 presentSettingFragment(new PremiumPreviewFragment("settings"));
```


یعنی: ردیف با id=30 و آیکون `ic_ambergram_settings` (فقنوس نارنجی) بعد از ردیف زبان، و کلیکش `new AmbergramSettingsActivity()` را present می‌کند.

## ۶-۳ آیکون‌های وکتور جدید (کد کامل — کوچک هستند)

`res/drawable/ic_ambergram_proxy.xml`:

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
    <path
        android:fillColor="#FF000000"
        android:pathData="M12,2C6.48,2 2,6.48 2,12s4.48,10 10,10 10,-4.48 10,-10S17.52,2 12,2zM11,19.93c-3.95,-0.49 -7,-3.85 -7,-7.93 0,-0.62 0.08,-1.21 0.21,-1.79L9,15v1c0,1.1 0.9,2 2,2v1.93zM17.9,17.39c-0.26,-0.81 -1,-1.39 -1.9,-1.39h-1v-3c0,-0.55 -0.45,-1 -1,-1L8,12v-2h2c0.55,0 1,-0.45 1,-1L11,7h2c1.1,0 2,-0.9 2,-2v-0.41c2.93,1.19 5,4.06 5,7.41 0,2.08 -0.8,3.97 -2.1,5.39z" />
</vector>
```

`res/drawable/ic_ambergram_settings.xml`:

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
    <path
        android:fillColor="#F97316"
        android:pathData="M12,2C12,2 5,9.5 5,14.5C5,18.63 8.13,22 12,22C15.87,22 19,18.63 19,14.5C19,9.5 12,2 12,2ZM12,19.5C9.79,19.5 8,17.6 8,15.2C8,13.4 9.7,10.9 12,8.6C14.3,10.9 16,13.4 16,15.2C16,17.6 14.21,19.5 12,19.5Z" />
</vector>
```

## ۶-۴ دیباگ هاب

- toggle ها روی toast توضیح‌شان را نشان می‌دهند (`descRes`) — اگر toast درست ولی رفتار غلط بود، خود گیت را چک کنید نه این صفحه را.
- لیستنرهای زنده: کلاس `QueueListener` و `AmbergramProxyManager.Listener` را پیاده می‌کند؛ رفرش‌ها ۳۰۰ms debounce دارند (`updateScheduled`/`proxyUpdateScheduled`).
- اگر toggle «خاموش شد ولی برگشت روشن»: مقدار کش static با pref sync است — setter را ببینید؛ هر دو همزمان نوشته می‌شوند.

---

# بخش ۷ — تم آمبر، فونت UI، برندسازی، آیکون‌ها

## ۷-۱ تم Amber (OLED مشکی + نارنجی آمبر)

`Theme.java` — پنج هانک: (1) Amber در لیست تم‌های تیره، (2) تعریف ThemeInfo کامل با asset `amber.attheme` و ۳ accent مشکی‌نارنجی و پیش‌فرض روز/شب، (3) اعمال یک‌باره روی نصب‌های تازه/آپدیت‌شده با فلگ `amber_default_applied`، (4) جلوگیری از auto-night سوییچ وقتی تم روز خودش Amber است، (5) accent id=0 در `isDefaultAccent`:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/Theme.java b/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/Theme.java
index 7fc7292d1..8331be2a5 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/Theme.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/Theme.java
@@ -1676,7 +1676,7 @@ public class Theme {
             if (isDark != UNKNOWN) {
                 return isDark == DARK;
             }
-            if ("Dark Blue".equals(name) || "Night".equals(name)) {
+            if ("Dark Blue".equals(name) || "Night".equals(name) || "Amber".equals(name)) {
                 isDark = DARK;
             } else if ("Blue".equals(name) || "Arctic Blue".equals(name) || "Day".equals(name)) {
                 isDark = LIGHT;
@@ -3988,7 +3988,7 @@ public class Theme {
         themeInfo.setAccentColorOptions(
                 new int[]    { 0xFF5890C5,                     0xFF239853,                    0xFFCE5E82,                    0xFF7F63C3,                    0xFF2491AD,                    0xFF299C2F,                    0xFF8854B4,                    0xFF328ACF,                    0xFF43ACC7,                    0xFF52AC44,                    0xFFCD5F93,                    0xFFD28036,                    0xFF8366CC,                    0xFFCE4E57,                    0xFFD3AE40,                    0xFF7B88AB },
                 new int[]    { 0xFFB8E18D,                     0xFFFAFBCC,                    0xFFFFF9DC,                    0xFFC14F6E,                    0xFFD1BD1B,                    0xFFFFFAC9,                    0xFFFCF6D8,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000 },
-                new int[]    { 0x00000000,                     0xFFF2FBC9,                    0xFFFBF4DF, 	                         0,	                             0,                    0xFFFDEDB4,                    0xFFFCF7B6,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000 },
+                new int[]    { 0x00000000,                     0xFFF2FBC9,                    0xFFFBF4DF,                                0,                                  0,                    0xFFFDEDB4,                    0xFFFCF7B6,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000,                    0x00000000 },
                 new int[]    { 0x00000000,                     0xFFdfe2a0,                    0xFFf1b290,                    0xFFd7c1e9,                    0xFFd7b89e,                    0xFFec9e73,                    0xFFcbb0e4,                    0xff9bbce7,                    0xff91c5ec,                    0xff9bc982,                    0xffe4a1c1,                    0xffe3ae7d,                    0xffb8aaea,                    0xffeb9c79,                    0xffd3bc74,                    0xffa0aace },
                 new int[]    { 0x00000000,                     0xFFbad89d,                    0xFFeccf94,                    0xFFe8bdd6,                    0xFFe6dec2,                    0xFFe8d085,                    0xFFebc8e9,                    0xffc0d9f3,                    0xffbfdfec,                    0xffe0dd93,                    0xffe9bed6,                    0xffecd5a2,                    0xffc5c9ee,                    0xfff0bd99,                    0xffe9df9e,                    0xffcacedd },
                 new int[]    { 0x00000000,                     0xFFe2dea7,                    0xFFe7b384,                    0xFFd2aee9,                    0xFFdac5ae,                    0xFFeea677,                    0xFFdfa8d1,                    0xff95c3eb,                    0xffb5e1d9,                    0xffbed595,                    0xffcca8e1,                    0xffdfb076,                    0xffb3b1e2,                    0xffe79db4,                    0xffe0c88b,                    0xffa6add2 },
@@ -4026,6 +4026,38 @@ public class Theme {
         themes.add(themeInfo);
         themesDict.put("Dark Blue", currentNightTheme = themeInfo);
 
+        // Amber fork: built-in OLED black + amber orange theme, the default look
+        themeInfo = new ThemeInfo();
+        themeInfo.name = "Amber";
+        themeInfo.assetName = "amber.attheme";
+        themeInfo.previewBackgroundColor = 0xff0a0a0b;
+        themeInfo.previewInColor = 0xff17171a;
+        themeInfo.previewOutColor = 0xff33200e;
+        themeInfo.sortIndex = 0;
+        // accent id 0 == accentBaseColor, so the default state renders the
+        // amber.attheme colors exactly as authored (recolor engine skips it);
+        // firstAccentIsDefault stays false to avoid the 0x100000000L wallpaper
+        // marker which would drop key_chat_wallpaper back to the light default
+        themeInfo.firstAccentIsDefault = false;
+        themeInfo.currentAccentId = 0;
+        themeInfo.setAccentColorOptions(
+                new int[]    { 0xFFF97316, 0xFFFF8C00, 0xFFEA580C },
+                null,
+                null,
+                new int[]    { 0xFF000000, 0xFF171309, 0xFF161006 },
+                new int[]    { 0x00000000, 0x00000000, 0x00000000 },
+                new int[]    { 0x00000000, 0x00000000, 0x00000000 },
+                new int[]    { 0x00000000, 0x00000000, 0x00000000 },
+                new int[]    { 0, 1, 2 },
+                new String[] { "", "", "" },
+                new int[]    { 0, 0, 0 },
+                new int[]    { 0, 0, 0 }
+                );
+        sortAccents(themeInfo);
+        themes.add(themeInfo);
+        themesDict.put("Amber", themeInfo);
+        currentDayTheme = currentNightTheme = themeInfo;
+
         themeInfo = new ThemeInfo();
         themeInfo.name = "Arctic Blue";
         themeInfo.assetName = "arctic.attheme";
@@ -4143,6 +4175,13 @@ public class Theme {
 
         sortThemes();
 
+        // Amber fork: one-time default — apply the Amber theme on fresh installs
+        // and once on upgraded installs (user can still change it afterwards)
+        if (!themeConfig.contains("amber_default_applied")) {
+            themeConfig.edit().putBoolean("amber_default_applied", true).apply();
+            MessagesController.getGlobalMainSettings().edit().putString("theme", "Amber").commit();
+        }
+
         ThemeInfo applyingTheme = null;
         SharedPreferences preferences = MessagesController.getGlobalMainSettings();
         try {
@@ -6749,7 +6788,7 @@ public class Theme {
             }
         } else {
             ThemeInfo dayTheme = currentDayTheme;
-            if (dayTheme != null && dayTheme.isDark() && selectedAutoNightType != AUTO_NIGHT_TYPE_NONE && defaultTheme != null) {
+            if (dayTheme != null && !("Amber".equals(dayTheme.getKey())) && dayTheme.isDark() && selectedAutoNightType != AUTO_NIGHT_TYPE_NONE && defaultTheme != null) {
                 dayTheme = defaultTheme;
             }
             if (currentTheme != dayTheme && (currentTheme == null || dayTheme != null && currentTheme.isDark() != dayTheme.isDark())) {
@@ -10216,6 +10255,9 @@ public class Theme {
             if (accent.parentTheme.getKey().equals("Blue") && accent.id == 99) {
                 return true;
             }
+            if (accent.parentTheme.getKey().equals("Amber") && accent.id == 0) {
+                return true;
+            }
             if (accent.parentTheme.getKey().equals("Day") && accent.id == 9) {
                 return true;
             }
```


فایل پالت: `TMessagesProj/src/main/assets/amber.attheme` (پالت کامل کلیدها شامل Saved/Archived). `IntroActivity.java` هم تم شبیه پیش‌فرض را به `"Amber"` تغییر داده:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/IntroActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/IntroActivity.java
index 9f8f0977b..c44592202 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/IntroActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/IntroActivity.java
@@ -220,7 +220,7 @@ public class IntroActivity extends BaseFragment implements NotificationCenter.No
 
             // TODO: Generify this part, currently it's a clone of another theme switch toggle
             String dayThemeName = "Blue";
-            String nightThemeName = "Night";
+            String nightThemeName = "Amber";
 
             Theme.ThemeInfo themeInfo;
             boolean toDark;
```


## ۷-۲ فونت UI (Baloo Bhaijaan 2 Bold)

فونت: `assets/fonts/ambergramui.ttf`. مکانیزم: `AndroidUtilities.bold()` حالا فونت آمبر را برمی‌گرداند (با fallback به Roboto Medium)، و متد جدید `messageBold()` برای محتوای پیام‌ها (bold span داخل چت) با Roboto اصلی — تا متن پیام‌های کاربران تغییر ظاهری نکند:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/AndroidUtilities.java b/TMessagesProj/src/main/java/org/telegram/messenger/AndroidUtilities.java
index d59b29a66..0b7048bd9 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/AndroidUtilities.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/AndroidUtilities.java
@@ -255,22 +255,43 @@ public class AndroidUtilities {
     public final static String TYPEFACE_ROBOTO_MEDIUM_ITALIC = "fonts/rmediumitalic.ttf";
     public final static String TYPEFACE_ROBOTO_MONO = "fonts/rmono.ttf";
     public final static String TYPEFACE_MERRIWEATHER_BOLD = "fonts/mw_bold.ttf";
+    public final static String TYPEFACE_AMBERGRAM_UI = "fonts/ambergramui.ttf";
 
     public static Typeface mediumTypeface;
     public static ThreadLocal<byte[]> readBufferLocal = new ThreadLocal<>();
     public static ThreadLocal<byte[]> bufferLocal = new ThreadLocal<>();
 
+    /**
+     * AmberGram: the app-wide UI typeface. Bold and rounded, used for all
+     * Telegram-authored interface texts (headers, buttons, cells, menus).
+     * Message content keeps the original Roboto styling via messageBold().
+     */
     public static Typeface bold() {
         if (mediumTypeface == null) {
             if (SharedConfig.useSystemBoldFont && Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                 mediumTypeface = Typeface.create(null, 500, false);
             } else {
-                mediumTypeface = getTypeface(TYPEFACE_ROBOTO_MEDIUM);
+                mediumTypeface = getTypeface(TYPEFACE_AMBERGRAM_UI);
+                if (mediumTypeface == null) {
+                    mediumTypeface = getTypeface(TYPEFACE_ROBOTO_MEDIUM);
+                }
             }
         }
         return mediumTypeface;
     }
 
+    /**
+     * AmberGram: the original Roboto Medium typeface, used for user-generated
+     * content styling (bold spans inside messages, captions) so chats are not
+     * affected by the custom UI font.
+     */
+    public static Typeface messageBold() {
+        if (SharedConfig.useSystemBoldFont && Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
+            return Typeface.create(null, 500, false);
+        }
+        return getTypeface(TYPEFACE_ROBOTO_MEDIUM);
+    }
+
     private static final Hashtable<String, Typeface> typefaceCache = new Hashtable<>();
     public static float touchSlop;
     private static int prevOrientation = -10;
@@ -6461,7 +6482,7 @@ public class AndroidUtilities {
         return "";
     }
 
-	public static void quietSleep(long millis) {
+        public static void quietSleep(long millis) {
         try {
             Thread.sleep(millis);
         } catch (InterruptedException ignored) {
```


سپس در همه سل‌های اصلی، `setTypeface(AndroidUtilities.bold())` اضافه شده (اعمال سراسری): `TextStyleSpan` به `messageBold()` تغییر یافت و `AlertDialog/TextCell/TextCheckCell/TextInfoPrivacyCell/TextSettingsCell` به `bold()`:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Components/TextStyleSpan.java b/TMessagesProj/src/main/java/org/telegram/ui/Components/TextStyleSpan.java
index 475e7b465..23a5f55ca 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Components/TextStyleSpan.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Components/TextStyleSpan.java
@@ -94,7 +94,7 @@ public class TextStyleSpan extends MetricAffectingSpan {
             } else if ((flags & FLAG_STYLE_BOLD) != 0 && (flags & FLAG_STYLE_ITALIC) != 0) {
                 return AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM_ITALIC);
             } else if ((flags & FLAG_STYLE_BOLD) != 0) {
-                return AndroidUtilities.bold();
+                return AndroidUtilities.messageBold();
             } else if ((flags & FLAG_STYLE_ITALIC) != 0) {
                 return AndroidUtilities.getTypeface("fonts/ritalic.ttf");
             } else {
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/AlertDialog.java b/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/AlertDialog.java
index 14e8fbcd1..7443026e2 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/AlertDialog.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/AlertDialog.java
@@ -316,6 +316,7 @@ public class AlertDialog extends Dialog implements Drawable.Callback, Notificati
             textView.setSingleLine(true);
             textView.setGravity(Gravity.CENTER_HORIZONTAL);
             textView.setEllipsize(TextUtils.TruncateAt.END);
+            textView.setTypeface(AndroidUtilities.bold());
             ThemeBind.textColor(textView, Theme.key_dialogTextBlack, resourcesProvider);
             textView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16);
             addView(textView, LayoutHelper.createFrame(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, (LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT) | Gravity.CENTER_VERTICAL));
@@ -933,6 +934,7 @@ public class AlertDialog extends Dialog implements Drawable.Callback, Notificati
             secondTitleTextView = new TextView(getContext());
             secondTitleTextView.setText(secondTitle);
             ThemeBind.textColor(secondTitleTextView, Theme.key_dialogTextGray3, themedColors);
+            secondTitleTextView.setTypeface(AndroidUtilities.bold());
             secondTitleTextView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18);
             secondTitleTextView.setGravity((LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT) | Gravity.TOP);
             titleContainer.addView(secondTitleTextView, LayoutHelper.createFrame(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, (LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT) | Gravity.TOP, 0, 21, 0, 0));
@@ -942,6 +944,7 @@ public class AlertDialog extends Dialog implements Drawable.Callback, Notificati
             subtitleTextView = new TextView(getContext());
             subtitleTextView.setText(subtitle);
             ThemeBind.textColor(subtitleTextView, Theme.key_dialogIcon, themedColors);
+            subtitleTextView.setTypeface(AndroidUtilities.bold());
             subtitleTextView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14);
             subtitleTextView.setGravity((LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT) | Gravity.TOP);
             containerView.addView(subtitleTextView, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, (LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT) | Gravity.TOP, 24, 0, 24, items != null ? 14 : 10));
@@ -982,6 +985,7 @@ public class AlertDialog extends Dialog implements Drawable.Callback, Notificati
         messageTextView = new EffectsTextView(getContext());
         NotificationCenter.listenEmojiLoading(messageTextView);
         messageTextView.setTextColor(lastMessageTextColor = getThemedColor(topAnimationIsNew ? Theme.key_windowBackgroundWhiteGrayText : Theme.key_dialogTextBlack)); // re-applied in updateThemeColors unless customTextColor
+        messageTextView.setTypeface(AndroidUtilities.bold());
         messageTextView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16);
         messageTextView.setMovementMethod(new AndroidUtilities.LinkMovementMethodMy());
         ThemeBind.linkTextColor(messageTextView, Theme.key_dialogTextLink, themedColors);
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCell.java b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCell.java
index 94b04da83..d08da47f8 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCell.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCell.java
@@ -99,6 +99,7 @@ public class TextCell extends FrameLayout implements Theme.Colorable {
 
         textView = new SimpleTextView(context);
         ThemeBind.textColor(textView, dialog ? Theme.key_dialogTextBlack : Theme.key_windowBackgroundWhiteBlackText, resourcesProvider);
+        textView.setTypeface(AndroidUtilities.bold());
         textView.setTextSize(16);
         textView.setGravity(LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT);
         textView.setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
@@ -106,6 +107,7 @@ public class TextCell extends FrameLayout implements Theme.Colorable {
 
         subtitleView = new SimpleTextView(context);
         ThemeBind.textColor(subtitleView, dialog ? Theme.key_dialogTextGray : Theme.key_windowBackgroundWhiteGrayText, resourcesProvider);
+        subtitleView.setTypeface(AndroidUtilities.bold());
         subtitleView.setTextSize(13);
         subtitleView.setGravity(LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT);
         subtitleView.setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
@@ -114,6 +116,7 @@ public class TextCell extends FrameLayout implements Theme.Colorable {
         valueTextView = new AnimatedTextView(context, false, true, true);
         ThemeBind.textColor(valueTextView, dialog ? Theme.key_dialogTextBlue2 : Theme.key_windowBackgroundWhiteValueText, resourcesProvider);
         valueTextView.setPadding(0, dp(18), 0, dp(18));
+        valueTextView.setTypeface(AndroidUtilities.bold());
         valueTextView.setTextSize(dp(16));
         valueTextView.setGravity(LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT);
         valueTextView.setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
@@ -123,6 +126,7 @@ public class TextCell extends FrameLayout implements Theme.Colorable {
         valueSpoilersTextView = new SimpleTextView(context);
         valueSpoilersTextView.setEllipsizeByGradient(18, false);
         ThemeBind.textColor(valueSpoilersTextView, dialog ? Theme.key_dialogTextBlue2 : Theme.key_windowBackgroundWhiteValueText, resourcesProvider);
+        valueSpoilersTextView.setTypeface(AndroidUtilities.bold());
         valueSpoilersTextView.setGravity(LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT);
         valueSpoilersTextView.setTextSize(16);
         valueSpoilersTextView.setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCheckCell.java b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCheckCell.java
index 6d5d8e5d1..8becbd4d0 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCheckCell.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextCheckCell.java
@@ -103,6 +103,7 @@ public class TextCheckCell extends FrameLayout {
 
         textView = new TextView(context);
         ThemeBind.textColor(textView, dialog ? Theme.key_dialogTextBlack : Theme.key_windowBackgroundWhiteBlackText, resourcesProvider);
+        textView.setTypeface(AndroidUtilities.bold());
         textView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16);
         textView.setLines(1);
         textView.setMaxLines(1);
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextInfoPrivacyCell.java b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextInfoPrivacyCell.java
index 295745801..4a347c1bf 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextInfoPrivacyCell.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextInfoPrivacyCell.java
@@ -80,6 +80,7 @@ public class TextInfoPrivacyCell extends FrameLayout implements Theme.Colorable
             }
         };
         textView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14);
+        textView.setTypeface(AndroidUtilities.bold());
         textView.setGravity(LocaleController.isRTL ? Gravity.RIGHT : Gravity.LEFT);
         textView.setPadding(0, AndroidUtilities.dp(10), 0, AndroidUtilities.dp(17));
         textView.setMovementMethod(LinkMovementMethod.getInstance());
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextSettingsCell.java b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextSettingsCell.java
index 2f4003876..04f389895 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextSettingsCell.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/Cells/TextSettingsCell.java
@@ -80,6 +80,7 @@ public class TextSettingsCell extends FrameLayout {
         this.padding = padding;
 
         textView = new TextView(context);
+        textView.setTypeface(AndroidUtilities.bold());
         textView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16);
         textView.setLines(1);
         textView.setMaxLines(1);
@@ -91,6 +92,7 @@ public class TextSettingsCell extends FrameLayout {
 
         valueTextView = new AnimatedTextView(context, true, true, !LocaleController.isRTL);
         valueTextView.setAnimationProperties(.55f, 0, 320, CubicBezierInterpolator.EASE_OUT_QUINT);
+        valueTextView.setTypeface(AndroidUtilities.bold());
         valueTextView.setTextSize(AndroidUtilities.dp(16));
         valueTextView.setGravity((LocaleController.isRTL ? Gravity.LEFT : Gravity.RIGHT) | Gravity.CENTER_VERTICAL);
         ThemeBind.textColor(valueTextView, Theme.key_windowBackgroundWhiteValueText, resourcesProvider);
```


## ۷-۳ برندسازی: بازنویسی runtime پک‌های زبان

دو مکانیزم در `LocaleController.java`:
1. **کلیدهای برند محافظت‌شده** (`PROTECTED_BRAND_KEYS`): AppName، AppNameBeta، NoChats، NoChatsHelp، NoChatsContactsHelp، TelegramFeatures، Page1..6Title/Message — از پک ریموت حذف می‌شوند تا مقدار داخلی APK (فارسی در values-fa) پیروز شود.
2. **بازنویسی واژه‌ها** (`sanitizeBrandKeys`/`rebrandValue`): Telegram/TELEGRAM/«تلگرام» (۷ املا مختلف فارسی + سیریلیک) → AmberGram/«آمبرگرم»؛ کلیدها/مقدارهای URL (`://`) دست‌نخورده می‌مانند.

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java b/TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java
index 3a5413ce1..b561b7ffb 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java
@@ -64,6 +64,7 @@ import java.util.HashMap;
 import java.util.HashSet;
 import java.util.Iterator;
 import java.util.Locale;
+import java.util.Map;
 import java.util.Objects;
 import java.util.TimeZone;
 
@@ -1271,7 +1272,7 @@ public class LocaleController {
                 }
                 eventType = parser.next();
             }
-            return stringMap;
+            return sanitizeBrandKeys(stringMap);
         } catch (Exception e) {
             try {
                 File filesDir = ApplicationLoader.getFilesDirFixed();
@@ -1296,7 +1297,92 @@ public class LocaleController {
                 FileLog.e(e);
             }
         }
-        return stringMap != null ? stringMap : new HashMap<>();
+        return stringMap != null ? sanitizeBrandKeys(stringMap) : new HashMap<>();
+    }
+
+    /**
+     * AmberGram: brand keys that must never be overridden by remote (server) language
+     * packs. The official Persian pack, for example, ships AppName = "تلگرام", which
+     * made the main header show "Telegram" instead of "AmberGram". Removing these
+     * keys here makes getString() fall back to the baked-in APK values (with the
+     * localized values-fa variants picked up automatically for Persian).
+     */
+    private static final String[] PROTECTED_BRAND_KEYS = {
+        "AppName",
+        "AppNameBeta",
+        // empty main chat list — remote pack still says "به تلگرام خوش آمدید"
+        "NoChats",
+        "NoChatsHelp",
+        "NoChatsContactsHelp",
+        // settings row pointing at the tips channel
+        "TelegramFeatures",
+        // first-launch intro slides
+        "Page1Title",
+        "Page1Message",
+        "Page2Message",
+        "Page3Message",
+        "Page4Message",
+        "Page5Message",
+        "Page6Message",
+    };
+
+    /**
+     * AmberGram: rewrites the remaining Telegram wording inside remote (server)
+     * language packs to the fork brand while a pack is being loaded, so no screen
+     * ever falls back to "Telegram" / «تلگرام». Values that look like URLs (contain
+     * "://" or belong to *Url keys) are left untouched so links such as
+     * t.me/TelegramTips keep working; protected brand keys above are dropped
+     * entirely so the baked-in APK strings win.
+     */
+    private static final String AMBER_FA = "\u0622\u0645\u0628\u0631\u06AF\u0631\u0645";
+    private static final String TELEGRAM_CYRILLIC = "\u0422\u0435\u043B\u0435\u0433\u0440\u0430\u043C";
+    private static final String[] REMOTE_BRAND_WORDS = {
+        "\u062A\u0644\u06AF\u0631\u0627\u0645",
+        "\u062A\u064A\u0644\u064A\u062C\u0631\u0627\u0645",
+        "\u062A\u06CC\u0644\u06CC\u062C\u0631\u0627\u0645",
+        "\u062A\u0644\u064A\u062C\u0631\u0627\u0645",
+        "\u062A\u0644\u06CC\u062C\u0631\u0627\u0645",
+        "\u062A\u0644\u064A\u06AF\u0631\u0627\u0645",
+        "\u062A\u0644\u06CC\u06AF\u0631\u0627\u0645",
+    };
+
+    private static String rebrandValue(String v) {
+        v = v.replace("TELEGRAM", "AMBERGRAM").replace("Telegram", "AmberGram").replace(TELEGRAM_CYRILLIC, "AmberGram");
+        for (int a = 0; a < REMOTE_BRAND_WORDS.length; a++) {
+            v = v.replace(REMOTE_BRAND_WORDS[a], AMBER_FA);
+        }
+        return v;
+    }
+
+    private static boolean needsRebrand(String v) {
+        if (v.contains("Telegram") || v.contains(TELEGRAM_CYRILLIC)) {
+            return true;
+        }
+        for (int a = 0; a < REMOTE_BRAND_WORDS.length; a++) {
+            if (v.contains(REMOTE_BRAND_WORDS[a])) {
+                return true;
+            }
+        }
+        return false;
+    }
+
+    private static HashMap<String, String> sanitizeBrandKeys(HashMap<String, String> map) {
+        if (map != null) {
+            for (int a = 0; a < PROTECTED_BRAND_KEYS.length; a++) {
+                map.remove(PROTECTED_BRAND_KEYS[a]);
+            }
+            for (Map.Entry<String, String> entry : map.entrySet()) {
+                String k = entry.getKey();
+                String v = entry.getValue();
+                if (k == null || v == null || k.endsWith("Url") || v.contains("://")) {
+                    continue;
+                }
+                if (needsRebrand(v)) {
+                    entry.setValue(rebrandValue(v));
+                }
+            }
+        }
+        return map;
     }
 
     private static boolean hasMalformedCopy(File file) {
```


دو رشته ثابت دیگر: `SessionsActivity` (`session.app_name = "AmberGram Android"`) و `ThemePreviewActivity` (عنوان پیش‌نمایش):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/SessionsActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/SessionsActivity.java
index add1d6014..1672c27a4 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/SessionsActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/SessionsActivity.java
@@ -758,7 +758,7 @@ public class SessionsActivity extends BaseFragment implements NotificationCenter
         session.platform = "Android";
         session.device_model = Build.MANUFACTURER + " " + Build.MODEL;
         session.system_version = "SDK " + Build.VERSION.SDK_INT;
-        session.app_name = "Telegram Android";
+        session.app_name = "AmberGram Android";
         session.app_version = "";
         try {
             final PackageInfo pInfo = ApplicationLoader.applicationContext.getPackageManager().getPackageInfo(ApplicationLoader.applicationContext.getPackageName(), 0);
```


```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/ThemePreviewActivity.java b/TMessagesProj/src/main/java/org/telegram/ui/ThemePreviewActivity.java
index ae8c518ed..49b8e608f 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/ThemePreviewActivity.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/ThemePreviewActivity.java
@@ -1060,7 +1060,7 @@ public class ThemePreviewActivity extends BaseFragment implements DownloadContro
         }
 
         if (messagesAdapter.showSecretMessages) {
-            actionBar2.setTitle("Telegram Beta Chat");
+            actionBar2.setTitle("AmberGram Chat");
             actionBar2.setSubtitle(LocaleController.formatPluralString("Members", 505));
         } else {
             if (screenType == SCREEN_TYPE_CHANGE_BACKGROUND) {
```


## ۷-۴ آیکون‌های لانچر (مجموعه Leopard + Phoenix)

`LauncherIconController` — ۶ enum جدید (LEOPARD، LEOPARD_RING، LEOPARD_FULL، LEOPARD_PHOENIX، LEOPARD_PHOENIX_RING، LEOPARD_PHOENIX_FULL):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/ui/LauncherIconController.java b/TMessagesProj/src/main/java/org/telegram/ui/LauncherIconController.java
index 49bf82153..6421c2aa9 100644
--- a/TMessagesProj/src/main/java/org/telegram/ui/LauncherIconController.java
+++ b/TMessagesProj/src/main/java/org/telegram/ui/LauncherIconController.java
@@ -39,7 +39,13 @@ public class LauncherIconController {
         AQUA("AquaIcon", R.drawable.icon_4_background_sa, R.mipmap.icon_foreground_sa, R.string.AppIconAqua),
         PREMIUM("PremiumIcon", R.drawable.icon_3_background_sa, R.mipmap.icon_3_foreground_sa, R.string.AppIconPremium, true),
         TURBO("TurboIcon", R.drawable.icon_5_background_sa, R.mipmap.icon_5_foreground_sa, R.string.AppIconTurbo, true),
-        NOX("NoxIcon", R.mipmap.icon_2_background_sa, R.mipmap.icon_foreground_sa, R.string.AppIconNox, true);
+        NOX("NoxIcon", R.mipmap.icon_2_background_sa, R.mipmap.icon_foreground_sa, R.string.AppIconNox, true),
+        LEOPARD("LeopardIcon", R.drawable.icon_7_background_sa, R.drawable.icon_7_foreground_sa, R.string.AppIconLeopardFrame),
+        LEOPARD_RING("LeopardRingIcon", R.drawable.icon_8_background_sa, R.drawable.icon_8_foreground_sa, R.string.AppIconLeopardHalo),
+        LEOPARD_FULL("LeopardFullIcon", R.drawable.icon_9_background_sa, R.drawable.icon_9_foreground_sa, R.string.AppIconLeopard),
+        LEOPARD_PHOENIX("LeopardPhoenixIcon", R.drawable.icon_10_background_sa, R.drawable.icon_10_foreground_sa, R.string.AppIconAmberPhoenixFrame),
+        LEOPARD_PHOENIX_RING("LeopardPhoenixRingIcon", R.drawable.icon_11_background_sa, R.drawable.icon_11_foreground_sa, R.string.AppIconAmberPhoenixHalo),
+        LEOPARD_PHOENIX_FULL("LeopardPhoenixFullIcon", R.drawable.icon_12_background_sa, R.drawable.icon_12_foreground_sa, R.string.AppIconAmberPhoenix);
 
         public final String key;
         public final int background;
```


و ۶ activity-alias در AndroidManifest با intent-filter کامل لانچر (دیف کامل مانیفست شامل سرویس صف و receiver هم):

```diff
diff --git a/TMessagesProj/src/main/AndroidManifest.xml b/TMessagesProj/src/main/AndroidManifest.xml
index 303d463ea..6da826094 100644
--- a/TMessagesProj/src/main/AndroidManifest.xml
+++ b/TMessagesProj/src/main/AndroidManifest.xml
@@ -205,6 +205,102 @@
             <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
         </activity-alias>
 
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_7_launcher"
+            android:roundIcon="@mipmap/icon_7_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardRingIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_8_launcher"
+            android:roundIcon="@mipmap/icon_8_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardFullIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_9_launcher"
+            android:roundIcon="@mipmap/icon_9_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardPhoenixIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_10_launcher"
+            android:roundIcon="@mipmap/icon_10_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardPhoenixRingIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_11_launcher"
+            android:roundIcon="@mipmap/icon_11_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
+        <activity-alias
+            android:enabled="false"
+            android:name="org.telegram.messenger.LeopardPhoenixFullIcon"
+            android:targetActivity="org.telegram.ui.LaunchActivity"
+            android:icon="@mipmap/icon_12_launcher"
+            android:roundIcon="@mipmap/icon_12_launcher_round"
+            android:exported="true">
+
+            <intent-filter>
+                <action android:name="android.intent.action.MAIN" />
+                <category android:name="android.intent.category.LAUNCHER" />
+                <category android:name="android.intent.category.MULTIWINDOW_LAUNCHER" />
+            </intent-filter>
+            <meta-data android:name="android.app.shortcuts" android:resource="@xml/shortcuts" />
+        </activity-alias>
+
         <activity
             android:name="org.telegram.ui.LaunchActivity"
             android:theme="@style/Theme.TMessages.Start"
@@ -403,7 +499,7 @@
                 android:theme="@style/Theme.TMessages.Transparent"/>
         <activity android:name="org.telegram.ui.VoIPFeedbackActivity"
                   android:configChanges="keyboard|keyboardHidden|orientation|screenSize|uiMode"
-				  android:taskAffinity="${applicationId}.voip_feedback"
+                                  android:taskAffinity="${applicationId}.voip_feedback"
                   android:excludeFromRecents="true"
                 android:theme="@style/Theme.TMessages.TransparentWithAlerts"/>
 
@@ -489,6 +585,11 @@
             android:exported="true"
             android:foregroundServiceType="dataSync"
         />
+        <service
+            android:name=".AmberDownloadService"
+            android:exported="false"
+            android:foregroundServiceType="dataSync"
+        />
         <service
             android:name=".NotificationRepeat"
             android:exported="false"
@@ -550,7 +651,7 @@
             </intent-filter>
         </service>
 
-		<receiver android:name=".MusicPlayerReceiver" android:exported="false">
+                <receiver android:name=".MusicPlayerReceiver" android:exported="false">
             <intent-filter>
                 <action android:name="org.telegram.android.musicplayer.close" />
                 <action android:name="org.telegram.android.musicplayer.pause" />
@@ -574,6 +675,8 @@
             </intent-filter>
         </receiver>
 
+        <receiver android:name=".AmbergramProxyReceiver" android:enabled="true" android:exported="false"/>
+
         <receiver android:name=".RefererReceiver" android:exported="true" android:permission="android.permission.INSTALL_PACKAGES">
             <intent-filter>
                 <action android:name="com.android.vending.INSTALL_REFERRER" />
```


آیکون اصلی (ic_launcher) خودش طرح ققنوس×هواپیما است (فایل‌های webp/mipmap در دیف؛ دودویی‌اند و در سند متنی نمی‌گنجند — مسیرها: `res/drawable/icon_background_clip.webp`، `res/mipmap-*/ic_launcher*.png`، `res/drawable/icon_plane.xml`، `res/drawable/icon_background_sa.xml`، icon_7..12 در mipmap ها).

## ۷-۵ دیباگ تم/برند/فونت

- اگر هدر دوباره «تلگرام» شد: یعنی sanitize نشده — چک کنید `sanitizeBrandKeys` روی هر دو مسیر return در متد لود پک اعمال شده (دو هانک اول دیف).
- اگر تم روی نصب تازه اعمال نشد: فلگ `amber_default_applied` را از global main settings پاک کنید تا منطق «یک‌بار» دوباره اجرا شود.
- اگر فونت UI روی یک متن اعمال نشد: آن View در کد تلگرام typeface خودش را ست می‌کند (مثلاً `getTypeface(...)` مستقیم) — bold() را در آن نقطه اضافه کنید.
- آیکون‌ها: `LauncherIconController` + alias ها باید sync باشند (enabledComponentName)؛ تغییر آیکون روی بعضی لانچرها نیاز به ری‌استارت لانچر دارد.

---

# بخش ۸ — زیرساخت فورک

## ۸-۱ api_id / api_hash از BuildConfig

`BuildVars.java` — اعتبارنامه‌ها هاردکد نیستند؛ از `BuildConfig.TELEGRAM_APP_ID/HASH` می‌آیند که در بیلد از `local.properties` خوانده می‌شود (در CI از secrets؛ فال‌بک stub یعنی کامپایل می‌شود ولی لاگین نمی‌شود):

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java b/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java
index ca821813f..d13dc2096 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java
@@ -26,8 +26,9 @@ public class BuildVars {
     public static boolean NO_SCOPED_STORAGE = Build.VERSION.SDK_INT <= 29;
     public static String BUILD_VERSION_STRING = BuildConfig.BUILD_VERSION_STRING;
 
-    public static int APP_ID = 4;
-    public static String APP_HASH = "014b35b6184100b085b0d0572f9b5103";
+    // [FORK] api_id/api_hash injected from local.properties via BuildConfig. Never commit real credentials.
+    public static int APP_ID = BuildConfig.TELEGRAM_APP_ID;
+    public static String APP_HASH = BuildConfig.TELEGRAM_APP_HASH;
 
     // SafetyNet key for Google Identity SDK, set it to empty to disable
     public static String SAFETYNET_KEY = "AIzaSyDqt8P-7F7CPCseMkOiVRgb1LY8RN1bvH8";
```


تزریق در CI — بخش «Inject api credentials» در `release.yml` (کامل در ۸-۴).

## ۸-۲ نوع اکانت مخاطبین

`ContactsController.java` — نوع اکانت سیستم از `org.telegram.messenger` به `com.ambergram.app` (۵ هانک) تا با پکیج جدید بخواند/بنویسد:

```diff
diff --git a/TMessagesProj/src/main/java/org/telegram/messenger/ContactsController.java b/TMessagesProj/src/main/java/org/telegram/messenger/ContactsController.java
index 41ce86e17..2a9d3123c 100644
--- a/TMessagesProj/src/main/java/org/telegram/messenger/ContactsController.java
+++ b/TMessagesProj/src/main/java/org/telegram/messenger/ContactsController.java
@@ -391,7 +391,7 @@ public class ContactsController extends BaseController {
         Utilities.globalQueue.postRunnable(() -> {
             AccountManager am = AccountManager.get(ApplicationLoader.applicationContext);
             try {
-                Account[] accounts = am.getAccountsByType("org.telegram.messenger");
+                Account[] accounts = am.getAccountsByType("com.ambergram.app");
                 for (int a = 0; a < accounts.length; a++) {
                     Account acc = accounts[a];
                     boolean found = false;
@@ -423,7 +423,7 @@ public class ContactsController extends BaseController {
                 readContacts();
                 if (systemAccount == null) {
                     try {
-                        systemAccount = new Account("" + getUserConfig().getClientUserId(), "org.telegram.messenger");
+                        systemAccount = new Account("" + getUserConfig().getClientUserId(), "com.ambergram.app");
                         am.addAccountExplicitly(systemAccount, "", null);
                     } catch (Exception ignore) {
 
@@ -437,7 +437,7 @@ public class ContactsController extends BaseController {
         try {
             systemAccount = null;
             AccountManager am = AccountManager.get(ApplicationLoader.applicationContext);
-            Account[] accounts = am.getAccountsByType("org.telegram.messenger");
+            Account[] accounts = am.getAccountsByType("com.ambergram.app");
             for (int a = 0; a < accounts.length; a++) {
                 Account acc = accounts[a];
                 boolean found = false;
@@ -513,7 +513,7 @@ public class ContactsController extends BaseController {
                 AndroidUtilities.runOnUIThread(() -> {
                     AccountManager am = AccountManager.get(ApplicationLoader.applicationContext);
                     try {
-                        Account[] accounts = am.getAccountsByType("org.telegram.messenger");
+                        Account[] accounts = am.getAccountsByType("com.ambergram.app");
                         systemAccount = null;
                         for (int a = 0; a < accounts.length; a++) {
                             Account acc = accounts[a];
@@ -531,7 +531,7 @@ public class ContactsController extends BaseController {
 
                     }
                     try {
-                        systemAccount = new Account("" + getUserConfig().getClientUserId(), "org.telegram.messenger");
+                        systemAccount = new Account("" + getUserConfig().getClientUserId(), "com.ambergram.app");
                         am.addAccountExplicitly(systemAccount, "", null);
                     } catch (Exception ignore) {
```


## ۸-۳ gradle.properties (نسخه و پکیج)

```diff
diff --git a/gradle.properties b/gradle.properties
index 574e3b80b..2713b7346 100644
--- a/gradle.properties
+++ b/gradle.properties
@@ -13,9 +13,9 @@
 # http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
 # org.gradle.parallel=true
 #Sat Mar 12 05:53:50 MSK 2016
-APP_VERSION_CODE=7291
-APP_VERSION_NAME=13.2.1
-APP_PACKAGE=org.telegram.messenger
+APP_VERSION_CODE=7302
+APP_VERSION_NAME=0.6.0 (7302)
+APP_PACKAGE=com.ambergram.app
 IS_PRIVATE=false
 RELEASE_KEY_PASSWORD=android
 RELEASE_KEY_ALIAS=androidkey
```


فرمول versionCode: هر فلاور = `APP_VERSION_CODE × 10 + abiVersionCode` — afat=9 (universal)، arm64=2، armv7=3. پس 7302 → universal=73029، arm64=73022، armv7=73023.

## ۸-۴ workflows (کد کامل)

`.github/workflows/ci.yml` — کامپایل سریع روی push به master:

```yml
# Android CI for the Amber fork (Milestone 1)
# Copy this file to: .github/workflows/ci.yml
#
# - Builds :TMessagesProj_App:assembleDebug with STUB api keys (no secrets in CI).
# - Real-account login is a manual acceptance step (see docs/BUILD.md §6).
# - Upstream pins NDK 27.2.12479018; AGP auto-installs it on the runner.

name: android-ci

on:
  push:
    branches: [ main, master, fork-kit ]
  pull_request:
  workflow_dispatch:

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  assemble-debug:
    name: assembleDebug (stub api_id)
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - name: Checkout (recursive submodules)
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 1

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Set up Gradle (caching)
        uses: gradle/actions/setup-gradle@v4

      - name: Inject api credentials (real secrets, stub fallback)
        env:
          APP_ID: ${{ secrets.RAKHSH_TELEGRAM_APP_ID }}
          APP_HASH: ${{ secrets.RAKHSH_TELEGRAM_APP_HASH }}
        run: |
          {
            if [ -n "$APP_ID" ] && [ -n "$APP_HASH" ]; then
              echo "TELEGRAM_APP_ID=$APP_ID"
              echo "TELEGRAM_APP_HASH=$APP_HASH"
              echo "Using REAL api credentials from repo secrets"
            else
              echo "TELEGRAM_APP_ID=1"
              echo "TELEGRAM_APP_HASH="
              echo "Stub api_id (compile-only, cannot log in)"
            fi
          } >> local.properties

      - name: Build debug APK
        run: ./gradlew :TMessagesProj_App:assembleDebug --stacktrace

      - name: Upload debug APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: TMessagesProj_App/build/outputs/apk/afat/debug/*.apk
          if-no-files-found: error
```


`.github/workflows/release.yml` — بیلد سه APK امضاشده + ساخت GitHub Release با changelog و راهنمای نصب فارسی (تریگر: پوش تگ `v*` یا دستی):

```yml
# android-release.yml — signed release APK + GitHub Release for AmberGram
# Triggers on tag push (v*) or manual dispatch.
# Secrets required (set via repo Settings/Actions secrets):
#   RAKHSH_KEYSTORE_BASE64  – base64 of the release keystore (never committed to git)
#   RAKHSH_STORE_PASSWORD   – keystore store password
#   RAKHSH_KEY_ALIAS        – key alias
#   RAKHSH_KEY_PASSWORD     – key password
#   RAKHSH_TELEGRAM_APP_ID / RAKHSH_TELEGRAM_APP_HASH – packaged into the APK so
#   end-user login works out of the box.

name: android-release

on:
  push:
    tags: [ 'v*' ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  signed-release:
    name: assembleAfatRelease + GitHub Release
    runs-on: ubuntu-latest
    timeout-minutes: 150
    steps:
      - name: Checkout (recursive submodules)
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 1

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Set up Gradle (caching)
        uses: gradle/actions/setup-gradle@v4

      - name: Restore signing keystore from secret (not committed to git)
        run: |
          echo "${{ secrets.RAKHSH_KEYSTORE_BASE64 }}" | base64 -d > TMessagesProj/config/release.keystore

      - name: Inject api credentials (real secrets, stub fallback)
        env:
          APP_ID: ${{ secrets.RAKHSH_TELEGRAM_APP_ID }}
          APP_HASH: ${{ secrets.RAKHSH_TELEGRAM_APP_HASH }}
        run: |
          {
            if [ -n "$APP_ID" ] && [ -n "$APP_HASH" ]; then
              echo "TELEGRAM_APP_ID=$APP_ID"
              echo "TELEGRAM_APP_HASH=$APP_HASH"
              echo "Using REAL api credentials from repo secrets"
            else
              echo "TELEGRAM_APP_ID=1"
              echo "TELEGRAM_APP_HASH="
              echo "Stub api_id (compile-only, cannot log in)"
            fi
          } >> local.properties

      - name: Build signed release APKs (universal + arm64 + armv7)
        run: |
          ./gradlew :TMessagesProj_App:assembleAfatRelease :TMessagesProj_App:assembleArm64Release :TMessagesProj_App:assembleArmv7Release \
            -PRELEASE_STORE_PASSWORD="${{ secrets.RAKHSH_STORE_PASSWORD }}" \
            -PRELEASE_KEY_ALIAS="${{ secrets.RAKHSH_KEY_ALIAS }}" \
            -PRELEASE_KEY_PASSWORD="${{ secrets.RAKHSH_KEY_PASSWORD }}" \
            --stacktrace

      - name: Stage release files
        run: |
          mkdir -p dist
          cp TMessagesProj_App/build/outputs/apk/afat/release/app.apk "dist/AmberGram-${GITHUB_REF_NAME}-universal.apk"
          cp TMessagesProj_App/build/outputs/apk/arm64/release/app.apk "dist/AmberGram-${GITHUB_REF_NAME}-arm64-v8a.apk"
          cp TMessagesProj_App/build/outputs/apk/armv7/release/app.apk "dist/AmberGram-${GITHUB_REF_NAME}-armeabi-v7a.apk"
          sha256sum dist/*.apk > dist/SHA256SUMS.txt
          echo "--- dist contents ---"
          ls -l dist/

      - name: Create GitHub Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create "$GITHUB_REF_NAME" \
            --title "AmberGram $GITHUB_REF_NAME" \
            --prerelease \
            --notes "Unofficial GPLv2 client based on the Telegram open-source code (Android).
          - Signed APKs for every phone: universal (all 4 ABIs), arm64-v8a (most modern phones, nearly half the download size), armeabi-v7a (older 32-bit phones). SHA-256 checksums for every file are inside SHA256SUMS.txt.
          - Packaged with the project's own api_id/api_hash — login works out of the box.
          - NEW in 0.6.0 — hardened sequential download queue (full rework): 1) Auto-retry with exponential backoff — every item gets up to 8 attempts (2s to 120s delays) when the proxy or network hiccups, instead of being abandoned after one small attempt. 2) Network-aware — items only start when the connection is really established; while offline the queue waits and polls instead of failing the whole list in seconds. 3) Stall watchdog — if a download receives no bytes for 90 seconds (frozen proxy), it is cancelled and retried automatically. 4) Failed items are never silently erased — they stay visible in the queue page with a Retry button (also after app restart); only completed items are cleaned up. 5) The queue keeps flowing — while one item waits for its retry window, the next items continue downloading one by one. 6) Persistence fix — the active download is no longer saved twice, which previously re-queued the same file after restart. Queue logic verified by an 8-scenario / 20-assertion simulation (offline resilience, blip recovery, strict sequential order, watchdog, backoff, manual retry).
          - NEW in 0.5.0 — full Morphe patch bundle ported natively (the community Morphe patches applied to a source fork): 1) Anti-delete — messages deleted by the other side stay on this device, on by default. 2) Anti-disappearing — view-once voice notes and round videos stay playable and forwardable, on by default. 3) No screenshot alerts — the other side is never notified when you screenshot, on by default. 4) Allow saving everywhere — save, copy and forward in chats and channels that restrict content, on by default. 5) No in-app updates — AmberGram never suggests installing official Telegram updates, on by default. 6) Hide story views — stories are marked read locally without sending read receipts, on by default. 7) Always translatable — translation stays available even in chats that disabled it, on by default. 8) Disable channel swipe — optional toggle for the pull-down next-unread-channel gesture, off by default. Plus turbo download upgraded to the Morphe download-boost numbers: 1 MB chunks with 12 parallel requests. All 12 toggles live in AmberGram Settings.
          - NEW in 0.4.0 — anti-nag bundle inspired by the community Morphe patches: 1) No sponsored messages — channel and bot ads are never fetched or rendered (on by default). 2) No channel recommendations — the recommendations card at the end of channels is hidden (on by default). 3) Turbo download — big parallel chunks, the params official Telegram reserves for experimental builds (off by default). 4) Hide greeting stickers — greeting sticker suggestions and intro cards in empty chats are hidden (on by default). All toggles live in AmberGram Settings, under the ghost mode row.
          - Ghost mode (AmberGram Settings → Ghost mode): chats you open are NOT marked as read until you actually leave the chat, and your typing indicator is never sent — read quietly, reply later.
          - NEW packaging — smaller per-ABI APKs + this install guide, because the classic «there was a problem parsing the package» error is almost always caused by an incomplete download or by a device older than Android 6.0. Every published APK is verified healthy before release: SHA-256 recorded in SHA256SUMS.txt and the v1+v2 signatures are checked with the official apksigner tool.

          **راهنمای نصب فارسی:**

          - ۱. انتخاب فایل: اگر گوشی‌تان معمولی و از حدود ۲۰۱۷ به بعد است، فایل arm64-v8a را بگیرید (نصف حجم)؛ برای گوشی‌های قدیمی‌تر ۳۲ بیتی فایل armeabi-v7a؛ اگر مطمئن نیستید، فایل universal را بگیرید که روی همه گوشی‌ها نصب می‌شود.
          - ۲. دانلود فقط با مرورگر گوشی (کروم یا فایرفاکس) از همین صفحه و با زدن روی نام فایل انجام شود. دانلود از داخل پیام‌رسان‌ها یا مدیرهای دانلود غیراستاندارد ممکن است فایل را ناقص و خراب کند.
          - ۳. بعد از دانلود، حجم فایل را با حجمی که همین صفحه کنار فایل نوشته مقایسه کنید؛ اگر اختلاف داشت، دانلود ناقص است و باید دوباره دانلود کنید.
          - ۴. برای اطمینان کامل، SHA-256 را بسنجید: در ویندوز با دستور certutil -hashfile نام‌فایل SHA256 و در اندروید با یک اپ مقایسه هش، با عدد داخل فایل SHA256SUMS.txt.
          - ۵. حداقل اندروید ۶٫۰ لازم است (تنظیمات ← درباره گوشی ← نسخه اندروید) و حداقل ۲۰۰ مگابایت فضای خالی.
          - ۶. اگر باز هم خطای پارس آمد: با اینترنت دیگری (ترجیحاً بدون فیلترشکن) دوباره دانلود کنید و نصب را به نصب‌کننده خود سیستم بسپارید. اگر قبلاً بسته‌ای با همین نام (com.ambergram.app) از منبع دیگری نصب کرده‌اید، اول آن را حذف کنید.

          - AmberGram branding: OLED amber theme, fancy UI font, AmberGram Settings hub with a dedicated live sequential download queue page, polished phoenix × paper-plane launcher icon with embossed depth.
          - App header always shows AmberGram (brand keys are protected from remote language packs).
          - Download queue fully stops (service + notification) once everything is downloaded — idle behavior matches regular Telegram.
          - In-app free proxies (AmberGram Settings → Free proxies): six public GitHub proxy collectors fetched every 6 hours (automatic wakeup + catch-up on app start), merged and deduplicated, then every proxy is re-tested automatically with a real MTProto handshake through the native engine (no disruption to the active connection). Tap any proxy to connect instantly, long-press to copy its t.me link.
          - Automatic dead-proxy cleanup: proxies that fail their connection test are removed automatically from the list and from the system proxy screen; if the active proxy dies, AmberGram switches to the best surviving proxy instantly (or turns the proxy off when nothing is left), and removal is skipped during device network outages so a bad connection never wipes the whole list.
          - Six leopard-print app icons (Settings → Themes → App icons): three paper-plane designs (framed squircle, glowing halo ring, full circle) plus three matching Amber Phoenix versions — the white phoenix carrying the paper plane over the same golden spotted fur. Free for everyone, no premium needed.
          - Chat names and sender names in the chat list are pure white (they were orange, which caused eye strain), the channel verified badge check is white, and the drawer phone number and the search placeholder are calm gray instead of amber.
          - Full Telegram → AmberGram rebrand everywhere: empty chats screen, intro slides, settings rows, call menu items, permission dialogs and ~480 baked strings; leftover Telegram / «تلگرام» wording inside downloaded server language packs is rewritten automatically while loading (URLs stay untouched), so no screen ever falls back to the old name.
          - Source for this build: this repository at tag $GITHUB_REF_NAME (GPLv2). Not affiliated with Telegram Messenger Inc." \
            dist/*
```


Secrets موردنیاز: `RAKHSH_KEYSTORE_BASE64`، `RAKHSH_STORE_PASSWORD`، `RAKHSH_KEY_ALIAS`، `RAKHSH_KEY_PASSWORD`، `RAKHSH_TELEGRAM_APP_ID`، `RAKHSH_TELEGRAM_APP_HASH`.

## ۸-۵ دیباگ CI

- قبل از پوش تگ، همیشه صبر کنید `ci` روی master سبز شود (کامپایل validate).
- جستجوی خطا در لاگ ران: `error:` در هر دو workflow.
- خرابی کلاسیک changelog: `"` داخل متن یا خط بدون تورفتگی در بلوک `run: |` (همه خط‌ها باید هم‌تراز ۱۰ فاصله باشند)؛ با pyyaml قبل از پوش اعتبارسنجی کنید.
- راستی‌آزمایی artifact بعد از انتشار: دانلود از API با `Accept: application/octet-stream`، مقایسه sha256 با `SHA256SUMS.txt`، و `apksigner verify` (build-tools r34 از `dl.google.com/android/repository/build-tools_r34-linux.zip` — /tmp پایدار نیست، بعد از ریست سندباکس دوباره دانلود کنید).

---

# بخش ۹ — جدول کامل رشته‌های `Amber*` (فایل انگلیسی)

منبع: `TMessagesProj/src/main/res/values/strings.xml` — ۷۷ کلید با پیشوند `Amber`. فارسی معادل در `values-fa/strings.xml` (۷۶ کلید؛ همه جز دقیقاً همان‌ها با ترجمه فارسی — و `AppName` که در فایل فارسی وجود ندارد چون brand key محافظت‌شده است).

```xml
(77 کلید)
    <string name="AmberQueueMenu">Sequential download</string>
    <string name="AmberQueueNotificationTitle">AmberGram sequential downloads</string>
    <string name="AmberQueueAddedOne">1 file added to the sequential download queue</string>
    <string name="AmberQueueAddedMany">%1$d files added to the sequential download queue</string>
    <string name="AmberQueueNoneFound">No downloadable files in the selection</string>
    <string name="AmberQueueCancelAll">Cancel all</string>
    <string name="AmberQueueProgressLine">%1$d of %2$d</string>
    <string name="AmberQueueAlreadyQueued">Selected files are already in the download queue</string>
    <string name="AmbergramSettings" translatable="false">AmberGram Settings</string>
    <string name="AmbergramQueueSection">Sequential Downloads</string>
    <string name="AmbergramQueueEmpty">The queue is empty. Open a chat, long-press to select videos and files, then tap the three-dot menu and choose \"Sequential download\".</string>
    <string name="AmbergramQueueStatePending">Waiting</string>
    <string name="AmbergramQueueStateDownloading">Downloading</string>
    <string name="AmbergramQueueStateDone">Done</string>
    <string name="AmbergramQueueStateFailed">Failed</string>
    <string name="AmbergramQueueRetry">Retry</string>
    <string name="AmbergramQueueClearFinished">Clear finished</string>
    <string name="AmbergramQueueRemove">Remove</string>
    <string name="AmbergramQueueRemoved">Removed from the queue</string>
    <string name="AmbergramQueueSummary">%1$s waiting • %2$s downloading</string>
    <string name="AmbergramQueueRowIdle">No active downloads</string>
    <string name="AmbergramQueuePageHint">Files are downloaded one at a time and saved to Downloads/AmberGram.</string>
    <string name="AmbergramQueueComingSoon">More AmberGram features are on the way.</string>
    <string name="AmbergramProxySection">Free proxies</string>
    <string name="AmbergramProxySubtitle">Auto-fetch and test every 6 hours</string>
    <string name="AmbergramProxySettingsValue">%1$s working • refreshed every 6 hours</string>
    <string name="AmbergramProxyLastUpdate">Last update: %1$s</string>
    <string name="AmbergramProxyStats">%1$s of %2$s proxies working</string>
    <string name="AmbergramProxyFetching">Fetching sources…</string>
    <string name="AmbergramProxyTesting">Testing %1$s of %2$s…</string>
    <string name="AmbergramProxyRefresh">Update sources</string>
    <string name="AmbergramProxyTestAll">Test all</string>
    <string name="AmbergramProxyConnect">Connect</string>
    <string name="AmbergramProxyConnected">Connecting via %1$s</string>
    <string name="AmbergramProxyWorking">%1$s ms</string>
    <string name="AmbergramProxyDead">Unreachable</string>
    <string name="AmbergramProxyUntested">Not tested yet</string>
    <string name="AmbergramProxySource">Source: %1$s</string>
    <string name="AmbergramProxyEmpty">No proxies yet. Tap Update sources.</string>
    <string name="AmbergramProxyTimeNever">never</string>
    <string name="AmbergramProxyTimeNow">moments ago</string>
    <string name="AmbergramProxyTimeMinutes">%1$s minutes ago</string>
    <string name="AmbergramProxyTimeHours">%1$s hours ago</string>
    <string name="AmbergramProxyTimeDays">%1$s days ago</string>
    <string name="AmbergramProxyShowMore">Showing the best %1$s of %2$s proxies</string>
    <string name="AmbergramProxyFailedSources">%1$s source(s) unreachable</string>
    <string name="AmbergramProxyCopied">Proxy link copied</string>
    <string name="AmbergramProxyHint">Proxies are collected from public GitHub lists and automatically re-fetched and re-tested every 6 hours with a real MTProto handshake. Proxies that fail to connect are removed automatically. Tap a proxy to connect, long-press to copy its t.me link.</string>
    <string name="AmbergramProxyRemoved">Auto-clean: %1$s dead proxies removed</string>
    <string name="AmberGhostSection">Ghost mode</string>
    <string name="AmberGhostOn">On</string>
    <string name="AmberGhostOff">Off</string>
    <string name="AmberGhostDesc">Ghost mode: chats you open are not marked as read until you leave them, and your typing indicator is never sent.</string>
    <string name="AmberNoSponsored">No sponsored messages</string>
    <string name="AmberNoSponsoredDesc">Sponsored messages in channels and bots are never fetched or shown.</string>
    <string name="AmberNoRecommendations">No channel recommendations</string>
    <string name="AmberNoRecommendationsDesc">The recommended channels card at the end of channels is hidden.</string>
    <string name="AmberTurboDownload">Turbo download</string>
    <string name="AmberTurboDownloadDesc">Files download with big 1 MB chunks and 12 parallel requests (Morphe download boost numbers). New downloads pick this up automatically.</string>
    <string name="AmberNoGreetings">Hide greeting stickers</string>
    <string name="AmberNoGreetingsDesc">Greeting sticker suggestions and intro cards in empty chats are hidden.</string>
    <string name="AmberAntiDelete">Keep deleted messages</string>
    <string name="AmberAntiDeleteDesc">Messages deleted by the other side are kept on this device (anti-recall).</string>
    <string name="AmberAntiDisappearing">Keep view-once media</string>
    <string name="AmberAntiDisappearingDesc">View-once voice notes and round videos stay playable and forwardable.</string>
    <string name="AmberNoScreenshotNotify">No screenshot alerts</string>
    <string name="AmberNoScreenshotNotifyDesc">The other side is never notified when you take a screenshot.</string>
    <string name="AmberBypassNoforwards">Allow saving everywhere</string>
    <string name="AmberBypassNoforwardsDesc">Save, copy and forward in chats and channels that restrict content.</string>
    <string name="AmberNoAutoUpdate">No in-app updates</string>
    <string name="AmberNoAutoUpdateDesc">AmberGram never suggests installing the official Telegram update.</string>
    <string name="AmberNoChannelSwitch">Disable channel swipe</string>
    <string name="AmberNoChannelSwitchDesc">Turns off the pull-down gesture that jumps to the next unread channel.</string>
    <string name="AmberHideStoriesRead">Hide story views</string>
    <string name="AmberHideStoriesReadDesc">Stories are marked read locally without ever sending read receipts.</string>
    <string name="AmberBypassTranslation">Always translatable</string>
    <string name="AmberBypassTranslationDesc">Translation stays available even in chats that disabled it.</string>
```


---

# بخش ۱۰ — آشپزخانه دیباگ (مرجع سریع)

## ۱۰-۱ همه pref ها و فایل‌های persist

| فایل pref | کلیدها | مالک |
|-----------|--------|------|
| `getGlobalMainSettings()` (نام = پکیج، یعنی `com.ambergram.app_preferences`) | `amberNoSponsored`، `amberNoRecommendations`، `amberNoGreetings`، `amberTurboDownload`، `amberGhostMode`، `amberMorpheAntiDelete`، `amberMorpheAntiDisappearing`، `amberMorpheNoScreenshotNotify`، `amberMorpheBypassNoforwards`، `amberMorpheNoAutoUpdate`، `amberMorpheNoChannelSwitch`، `amberMorpheHideStoriesRead`، `amberMorpheBypassTranslation`، `theme`، `proxy_enabled` | کلاس‌های Amber* |
| `amber_queue_<accountNum>` | `queue` (JSON array) | DownloadQueueController |
| `ambergram_proxies` | `data` (JSON array)، `last_fetch`، `last_test`، `failed_sources`، `last_removed` | AmbergramProxyManager |

## ۱۰-۲ ثابت‌های شناسایی (برای logcat و dumpsys)

| چیز | مقدار |
|-----|-------|
| id نوتیف صف | 91231 |
| کانال نوتیف صف | `amber_queue` |
| requestCode آلارم پروکسی | 4213 |
| action آلارم پروکسی | `org.telegram.messenger.AMBERGRAM_PROXY_UPDATE` |
| id آیتم منوی صف در اکشن‌مود | 500 (ثابت `amber_queue`) |
| رنگ برند | `0xFFF97316` |
| تگ لاگ پروکسی | `AmbergramProxy` |
| رویدادهای پروکسی | 0=FETCH_STARTED 1=FETCH_DONE 2=TEST_PROGRESS 3=TEST_DONE 4=LIST_CLEANED |
| state های صف | 0=PENDING 1=DOWNLOADING 2=DONE 3=FAILED |

## ۱۰-۳ نقاط لاگ‌گذاری پیشنهادی (خلاصه)

- صف: `enqueue` / `startNextIfNeeded` / `failCurrent` / `checkCurrentStalled` / `finishCurrentWithFile` / هر سه رویداد NotificationCenter — با پیشوند `AmberQueue` (جدول کامل در بخش ۱-۸).
- پروکسی: از قبل لاگ دارد — `adb logcat | grep AmbergramProxy`.
- Morphe/شبح/ضدتبلیغ: گیت‌ها ساکت‌اند؛ برای trace، در اولِ هر گیت `FileLog.d("AmberMorphe: gateName=" + value)` بگذارید.

## ۱۰-۴ ترکیب‌های logcat مفید

```bash
adb logcat | grep -E "AmberQueue|AmbergramProxy"
adb logcat -s AmberQueue
adb logcat | grep -E "FileLoadOperation|FileLoader"          # موتور دانلود خود تلگرام
adb logcat | grep -iE "noforwards|sponsored|readStories"      # گیت‌ها (بعد از لاگ‌گذاری)
```

## ۱۰-۵ سناریوهای تست دستی سریع (خارج از صف)

1. شبح: چت را باز کنید، چند پیام بیاید، از چت خارج شوید → تیک دوسویه فقط بعد از خروج.
2. antiDelete: طرف مقابل پیام را حذف کند → پیام بماند (با نشانگر تغییر محتوا).
3. bypassNoforwards: کانال محافظت‌شده → گزینه فوروارد/کپی فعال.
4. turbo: toggle روشن، فایل بزرگ در شبکه خوب → سرعت بالا؛ در شبکه بد → صف با retry جبران می‌کند.
5. استوری: استوری ببینید → فرستنده آن را «دیده‌شده» نبیند.
6. اسکرین‌شات: در چت محرمانه اسکرین‌شات → اعلانی برای طرف نرود.

---

# بخش ۱۱ — تاریخچه نسخه‌ها و پروتکل مغز دوم

## تاریخچه تگ‌ها

v0.2.0 → v0.2.1 → v0.2.3 → v0.2.4 → v0.2.5 (صف دانلود اختصاصی + هدر برند-امن) → v0.2.6 → v0.2.7 (حذف خودکار پروکسی مرده) → v0.2.8 (پروکسی‌های رایگان درون‌برنامه‌ای) → v0.2.9 → v0.3.0 (حالت شبح) → v0.3.1 (APK هر ABI + راهنمای نصب فارسی) → v0.4.0 (ضدتبلیغ + توربو 512KB×8) → v0.5.0 (بسته کامل Morphe: ۸ پچ + توربو 1MB×12) → **v0.6.0 (صف دانلود مقاوم: retry/backoff/شبکه/watchdog/FAILED ماندگار)**

کامیت‌های شاخص (برای `git show`):

| کامیت | موضوع |
|-------|-------|
| `1b2c8ab` | پروکسی: ۶ کلکتور + رفرش ۶ ساعته |
| `d7c847d` | پروکسی: پاکسازی خودکار مرده‌ها + سوییچ به بهترین بازمانده |
| `7b0243d` | پروکسی: رفع خطای کامپایل lambda |
| `34fac1e` | آیکون‌های Leopard (۶ عدد) |
| `6e1a84d` | اسم چت‌ها سفید + تیک تأیید |
| `d52ca26` | بازنویسی runtime برند در پک‌های زبان |
| `a4748c3` | صف دانلود ترتیبی (نسخه اول) |
| `ade7788` | حالت شبح |
| `80f447e` | بسته ضدتبلیغ + توربو |
| `3cbbdb6` | بسته کامل Morphe |
| `8a2af2f` | صف دانلود مقاوم (بازنویسی v0.6.0) |

## پروتکل مغز دوم (پوشه `مغز دوم/` در ریشه ریپو)

هر نوبت کار: یادداشت LOG.md + به‌روزرسانی STATE.md + درس‌ها در LESSONS.md → commit → push master. فایل‌ها:
- `STATE.md` — وضعیت فعلی، نسخه‌ها، چک‌لیست انتشار بعدی (0.7.0 — کد 7303)
- `LOG.md` — گزارش کامل هر نوبت
- `LESSONS.md` — درس‌های فنی (مثل: `-r` در rg یعنی replace؛ YAML literal block؛ ...)
- `IDEAS.md` — ایده‌های نسخه‌های بعدی

## چک‌لیست انتشار نسخه بعد (0.7.0 — کد 7303)

1. `gradle.properties` در ریشه: bump به 7303 / 0.7.0
2. changelog واقعی در `release.yml` — بدون `"` داخلی، همه خط‌ها هم‌تراز ۱۰ فاصله، اعتبارسنجی pyyaml
3. commit + push master → صبر برای سبز شدن ci → تگ `v0.7.0-alpha` → پوش تگ
4. پایش لاگ با `error:` → بعد از انتشار artifact ها را با sha256+apksigner راستی‌آزمایی کن
5. گزارش نهایی به فارسی

---

*این سند به صورت خودکار از خود ریپو (دیف `7be672ead..HEAD` + محتوای فایل‌ها) تولید شده؛ اگر کد تغییر کرد، با همان اسکریپت بازتولید کنید.*

# گزارش نوبت‌ها

> قاعده: در پایان هر نوبت کاری، یک بخش جدید با خلاصه افکار، تصمیم‌ها، یادگیری‌ها و وضعیت اینجا ثبت می‌شود.

---

## نوبت ۱ — راه‌اندازی «مغز دوم»
- **درخواست کاربر:** پوشه‌ای به نام «مغز دوم» در ریپو بساز؛ در هر نوبت از هر چیزی که فکر کردی، یاد گرفتی یا تصمیم گرفتی نکته‌برداری کن.
- **کار انجام‌شده:**
  - سندباکس ریست شده بود → `/home/z/amber` دوباره shallow clone شد.
  - وضعیت واقعی با GitHub API بازسازی شد و کشف مهمی داشت: **v0.2.8 و v0.2.9 منتشر شده‌اند** و همه بدهی‌های قبلی بسته شده‌اند:
    - اسم سفید چت‌ها + تیک تأیید واضح‌تر + ریکارن کامل Telegram→AmberGram (`6e1a84dd`، `d52ca265`)
    - مجموعه آیکون‌های Leopard: 3 هواپیما + 3 ققنوس، انتخابگر در Settings > Themes (`34fac1e7`)
  - پوشه «مغز دوم» با 5 فایل (README / STATE / IDEAS / LESSONS / LOG) ساخته و به master پوش شد.
- **نکته مهم امروز:** قبل از نوشتن STATE، حافظه قدیمی می‌گفت نسخه فعلی v0.2.7 است؛ مقایسه با واقعیت ریپو نشان داد دو نسخه جلوتر هستیم. درس: همیشه STATE را با API ریپو کالیبره کن.
- **مصاحبه ایده‌پردازی این نوبت:** کاربر پرسید کدام قابلیت رقبا را پیشنهاد می‌کنم؛ لیست کامل در `IDEAS.md` ثبت شد. هنوز انتخابی انجام نشده.
- **قدم بعدی:** کاربر قابلیت بعدی را از `IDEAS.md` انتخاب می‌کند (پیشنهاد من: حالت شبح یا یادآور پیام).

---

## نوبت ۲ — پوش مغز دوم + جایگاه دائمی توکن GitHub
- **درخواست کاربر:** توکن GitHub فرستاده شد و پرسید کجا می‌توانم ابدی ذخیره‌اش کنم که پاک نشود.
- **پاسخ به «ذخیره ابدی»:**
  - در این محیط، `/home/z/my-project/` تنها مسیری است که بین پیام‌ها حفظ می‌شود → توکن آنجا ذخیره شد.
  - «ابد» واقعی فقط خارج از سندباکس معنا دارد؛ به کاربر توصیه شد خودش هم یک نسخه در جای امن نگه دارد و به‌دلخواه بعداً توکن را بچرخاند (rotate).
- **کار انجام‌شده:**
  - `/home/z/my-project/amber-git/git-credentials` (حالت 600) + اسکریپت بازیابی `/home/z/my-project/amber-git/restore-amber.sh` ساخته شد: بعد از هر ریست سندباکس، احراز هویت + هویت گیت + کلون `/home/z/amber` را یک‌جا برمی‌گرداند.
  - کامیت مغز دوم (`83af6d65`) با موفقیت به master پوش شد (`e3aca0f2..83af6d65`).
  - این گزارش + بخش احراز هویت در LESSONS اضافه شد و دوباره پوش شد.
- **درس امنیتی:** مقدار توکن هرگز داخل ریپو/فایل‌های مغز دوم نوشته نمی‌شود (ریپو عمومی است!)؛ فقط مسیر ذخیره ثبت می‌شود.
- **اصلاح نکته نوبت ۱:** فرض اشتباه «ممکن است my-project هم پاک شود» اصلاح شد — آزمایشی ثابت شد `/home/z/my-project` پایدار است؛ فقط `/home/z/amber` و پوشه home با ریست سندباکس می‌روند.

---

## نوبت ۳ — خطای پارس APK + پیاده‌سازی حالت شبح (نسخه 0.3.0)
- **گزارش کاربر:** موقع نصب نسخه قبلی، پیام «مشکل در پارس» (parse error) داد.
- **ریشه‌یابی:**
  - بررسی `TMessagesProj_App/build.gradle`: امضای استاندارد AGP، minSdk=23، `useLegacyPackaging=true` → ساختار APK سالم و سازگار است.
  - بررسی release.yml: امضا داخل خود gradle انجام می‌شود؛ ترتیب zipalign/sign تداخلی ندارد.
  - نتیجه: به‌احتمال زیاد دانلود ناقص/خراب (۸۰+ مگابایت از طریق اینترنت فیلترشده) یا باز کردن فایل اشتباه (مثلاً Source code zip). در changelog جدید راهنمای نصب + تأکید بر تطبیق SHA-256 اضافه شد؛ حداقل اندروید ۶.۰.
- **قابلیت جدید — حالت شبح (Ghost Mode):**
  - فایل جدید `AmberGhost.java`: وضعیت فعال/غیرفعال در `mainconfig` (`amberGhostMode`)، ردیابی چت باز، صف خوانده‌شده‌های معوق، پخش هنگام خروج.
  - `MessagesController.markDialogAsRead`: دروازه شبح — اگر چت باز و شبح روشن → ذخیره در صف و خروج؛ بدنه اصلی به `amberGhostMarkDialogAsRead` منتقل شد.
  - `MessagesController.sendTyping`: با شبح روشن، هرگز تایپ ارسال نمی‌شود (دروازه در نسخه ۵-آرگومان که نسخه ۴-آرگومان هم به آن delegate می‌کند).
  - `ChatActivity`: onResume → `chatOpened(dialog_id)`؛ onPause → `chatClosed` + `flushRead` (پخش واقعی خوانده‌شده‌ها).
  - `AmbergramSettingsActivity`: ردیف «حالت شبح» با آیکون `R.drawable.ghost` نارنجی و مقدار روشن/خاموش + Toast توضیح.
  - رشته‌ها: `AmberGhostSection/On/Off/Desc` در values و values-fa.
- **نسخه:** bump به 0.3.0 (7298)، تگ `v0.3.0-alpha`، changelog بازنویسی شد (قابلیت‌های قدیمی از حالت NEW خارج شدند — همان خطای کپی‌شدن changelog نوبت ۱ اصلاح شد).
- **کامیت:** `ade77889` + تگ → CI هر دو سبز: run 43610033486 (ci/master) SUCCESS — کامپایل سالم؛ run 43610035729 (release/v0.3.0-alpha) SUCCESS — انتشار با `AmberGram-v0.3.0-alpha-universal.apk` (۷۹.۳MB) + SHA256SUMS
- **نکته فنی:** grep با پرچم `-rn` اشتباه بود (r=replace)! درست: `rg -n`. 
- **درس معماری:** دروازه مرکزی در MessagesController بهتر از وصله در همه call-site ها است — یک نقطه حقیقت.

---

## نوبت ۴ — تشخیص قطعی خطای پارس + انتشار نسخه‌های سبک هر معماری (v0.3.1-alpha)
- **گزارش کاربر:** باز هم موقع نصب، خطای پارس می‌دهد؛ «درستش کن».
- **این بار فرض «دانلود خراب» را کنار گذاشتم و خود APK منتشرشده را باز کردم:**
  - v0.3.0-alpha را از GitHub API دانلود کردم: 83,130,812 بایت، SHA-256 **دقیقاً** مطابق SHA256SUMS منتشرشده (`4df96d5d...`) → فایل روی سرور سالم است.
  - بازرسی ساختاری با unzip: هر ۴ ABI موجود (arm64-v8a / armeabi-v7a / x86 / x86_64)، `resources.arsc` بدون فشرده‌سازی (STORED — شرط اندروید ۱۱+ رعایت شده)، ۴ classes.dex سالم.
  - با apksigner رسمی (build-tools r34 از dl.google.com): **v1 و v2 هر دو Verified** — نسخه اندرویدی پایین‌تر از ۷ هم می‌تواند نصب کند.
  - aapt2 badging: minSdk=23 (اندروید ۶.۰+)، targetSdk=36، versionCode=72989 که همان فرمول استاندارد است (7298×10 + abiVersionCode افلور afat=9) → مشکلی ندارد.
  - release.yml هیچ گام دستکاری بعد از امضا ندارد.
- **نتیجه:** خود فایل منتشرشده ۱۰۰٪ سالم است؛ خطای پارس سمت کاربر رخ می‌دهد: دانلود ناقص/خراب (۸۳ مگ از اینترنت فیلترشده، دو بار پشت هم کاملاً محتمل است) یا دستگاه قدیمی‌تر از اندروید ۶ یا نصب با مدیر فایل معیوب.
- **راه‌حل مهندسی (به‌جای تکرار توصیه):**
  - دو فلاور جدید `arm64` (abiVersionCode=2) و `armv7` (abiVersionCode=3) به `TMessagesProj_App/build.gradle` — با همان مانیفست‌های SDK23 و BUNDLE=false؛ versionCode ها زیر universal (9) می‌مانند تا ارتقا به universal همیشه ممکن باشد.
  - release.yml: حالا ۳ APK می‌سازد و منتشر می‌کند (universal + arm64-v8a + armeabi-v7a)؛ APK arm64 حدوداً نصف حجم می‌شود (~۴۰MB) → احتمال خرابی دانلود خیلی کمتر.
  - متن Release یک **راهنمای نصب فارسی ۶ مرحله‌ای** گرفت: انتخاب فایل، فقط دانلود با مرورگر، مقایسه حجم، سنجش SHA-256 (certutil/اپ هش)، حداقل اندروید ۶.۰ و ۲۰۰MB فضا، و نصب تمیز در صورت شکست.
  - یادداشت NEW در changelog هم صادقانه می‌گوید فایل‌ها قبل از انتشار با apksinger... (apksigner) و SHA-256 بررسی سالم می‌شوند.
- **تصادف نزدیک CI:** خط‌های فارسی راهنما را اول بدون تورفتگی نوشتم — از بلوک `run: |` خارج شدند و YAML را شکستند (pyyaml گرفتش قبل از پوش). همان خانواده خطای quoting نوبت‌های قبل؛ درس در LESSONS ثبت شد.
- **نسخه:** 0.3.1 (7299)، تگ `v0.3.1-alpha`.
- **نتیجه CI (پایش کامل شد):**
  - run ci/master (43619388353): SUCCESS — فلاورهای جدید کامپایل را نشکستند.
  - run release/v0.3.1-alpha (43619394041): SUCCESS — انتشار با ۴ asset.
  - راستی‌آزمایی artifact ها انجام شد: هر سه APK دانلود و sha256 آن‌ها با SHA256SUMS مطابقت کامل؛ apksigner: v1+v2 هر سه Verified؛ badging: universal=72999 (۴ ABI)، arm64=72992 (فقط arm64-v8a)، armv7=72993 (فقط armeabi-v7a)، همه versionName «0.3.1 (7299)»، minSdk 23.
  - حجم‌ها: universal=83.1MB، **arm64=44.9MB (۴۷٪ سبک‌تر)**، armv7=43.7MB.
  - متن Release شامل راهنمای نصب فارسی ۶ مرحله‌ای است.

---

## نوبت ۵ — بسته ضدتبلیغ الهام‌گرفته از پچ‌های Morphe (نسخه 0.4.0)
- **درخواست کاربر:** قابلیت‌های جدید اضافه کن؛ پیشنهاد داد از پچ‌های «telegram morphe» در گیت‌هاب استفاده کنم.
- **کشف:** Morphe اکوسیستم پچ ReVanced-مانند است که روی APK رسمی کار می‌کند (نه سورس) — `HushTelegram` با ۲۹۷ فایل پچ Kotlin. برای AmberGram که فورک سورس کامل است، راه درست «پورت بومی همان قابلیت‌ها» بود، نه استفاده مستقیم از فرمت پچ‌ها.
- **بررسی گیت‌هاب (API احرازشده):** repos مرتبط: HushTelegram (۱۵۲ ستاره — حذف اسپانسری/تبلیغات جستجو/استوری/upsell)، Hari-sys786/telegram-patches (پرمیوم آنلاک + بوست سرعت) و چند باندل دیگر. لیست کامل پچ‌ها را درآوردم و ۴ قابلیت کم‌ریسک و پرارزش انتخاب کردم.
- **قابلیت‌های پیاده‌شده (کلاس جدید `AmberAntiAds.java` + ۵ نقطه اتصال):**
  1. **بدون پیام اسپانسری** (پیش‌فرض روشن): `MessagesController.getSponsoredMessages` early-return + گارد در `ChatActivity.addSponsoredMessages` → هیچ درخواست شبکه‌ای برای تبلیغ هم نمی‌رود.
  2. **بدون کانال‌های پیشنهادی** (پیش‌فرض روشن): در `ChatMessageCell` فقط ساخت `ChannelRecommendationsCell` قفل می‌شود؛ حباب سرویس «به کانال پیوستید» سر جایش می‌ماند (دقت مهم: قفل کل branch حباب را هم می‌برد).
  3. **دانلود توربو** (پیش‌فرض خاموش): `FileLoadOperation.updateParams` → پارچه ۵۱۲KB + ۸ درخواست موازی (همان پارامترهای experimental رسمی)؛ عملیات‌های جدید خودکار می‌گیرند، عملیات جاری دست نمی‌خورد.
  4. **بدون استیکر خوش‌آمدگویی** (پیش‌فرض روشن): گارد ساخت `ChatGreetingsView` در ChatActivity.
  - UI: ۴ ردیف toggle عمومی در `AmbergramSettingsActivity` (الگوی ردیف شبح + helper عمومی `makeToggleRow` با interface داخلی)؛ آیکون‌های msg_block/msg_channel/msg_speed/msg_sticker نارنجی.
  - رشته‌های دوزبانه: `AmberNoSponsored/AmberNoRecommendations/AmberTurboDownload/AmberNoGreetings` + Desc برای هر کدام.
- **دو قابلیت کنار گذاشته شد و چرا:**
  - «پرمیوم آنلاک» — اخلاقاً و عملاً مناسب نیست (سرور-محور است و دروغ گفتن به کاربر).
  - «قفل کشیدن آرشیو به پایین» — با مسدود کردن `hasHiddenArchive()` دسترسی کاربر به آرشیو (که فقط با همان کشیدن باز می‌شود) قطع می‌شد؛ تله UX است. شماره تلفن هم در UI جدید ۱۳.x از کِشیر حذف شده.
- **راستی‌آزمایی محلی قبل از پوش:** توازن آکولاد همه فایل‌های ویرایشی نسبت به HEAD یکسان (تکنیک مقایسه نسبی — فایل‌های بزرگ آکولاد داخل رشته دارند!)؛ XML دو strings سالم؛ YAML release با pyyaml سالم و بدون `"` داخل متن.
- **استراتژی انتشار ایمن‌تر:** اول push به master + صبر برای ci/master سبز (کامپایل validate می‌شود)، بعد تگ — از این نوبت جزو چک‌لیست شد.
- **نسخه:** 0.4.0 (7300)، تگ `v0.4.0-alpha` — انتشار با ۳ APK مثل v0.3.1.
- **نتیجه CI (پایش کامل شد):**
  - ci/master (43625978149): SUCCESS — کد جدید کامپایل سالم (استراتژی «اول master سبز، بعد تگ» جواب داد).
  - release/v0.4.0-alpha (43631281316): SUCCESS — انتشار با ۴ asset.
  - راستی‌آزمایی: هر سه APK هش OK، امضا v1+v2 Verified، badging: universal=73009 (۴ ABI)، arm64=73002، armv7=73003، همه «0.4.0 (7300)»؛ متن Release شامل خط Morphe + راهنمای نصب فارسی.
  - حجم‌ها: universal=83.1MB، arm64=44.9MB، armv7=43.7MB.

---

## نوبت ۶ — بسته کامل پچ‌های Morphe (نسخه 0.5.0)
- **درخواست کاربر:** «تمامی پچ‌ها اعمال بشن، یک کلام ختم کلام» — بدون پرسش، همه پچ‌های قابل‌پیاده‌سازی.
- **کاتالوگ کامل از GitHub API:** دو مخزن با patches-list.json: rahul9999xda (۲۱ پچ) و newuser7171 (۲۰ پچ)؛ HushTelegram فقط مرجع توضیح.
- **نقشه ۲۰ پچ → اقدام:** ۸ پچ جدید پورت بومی شد + ۴ قبلاً انجام شده بود + توربو ارتقا یافت + ۷ مورد غیرقابل‌پورت (مستندشده):
  1. **antiDelete** — مصرف بلوک `deletedMessages` در MessagesController (بعد از جمع‌آوری از TL_updateDeleteMessages/کانال) گیت شد؛ حذف‌های ورودی دیگر از کش/دیتابیس پاک نمی‌شوند. حذف‌های خودمان از مسیر deleteMessages() مستقل‌اند و دست نمی‌خورند.
  2. **antiDisappearing** — گیت اول `isVoiceOnce()` و `isRoundOnce()` در MessageObject؛ چون ۳۰+ نقطه در ChatActivity/MediaController از همین دو متد استفاده می‌کنند، همه‌جا رسانه تک‌بار مثل رسانه معمولی رفتار می‌کند (پخش/فوروارد/ذخیره). عکس/ویدیوی once ساختار TL_messageExtendedMediaPreview دارد و برای جلوگیری از ریسک رندر دست نخورد (حذف آن‌ها بعد از بازدید سرور-محور است و toggle antiDelete هم پوشش می‌دهد).
  3. **noScreenshotNotify** — گیت بلوک ارسال در MediaController (هر دو مسیر secret و عادی).
  4. **bypassNoforwards** — گیت اول `isPeerNoForwards` در MessagesController (همه UI از همین می‌آید) + گیت `!messageOwner.noforwards` در `canForwardMessage`.
  5. **noAutoUpdate** — گیت اول `checkAppUpdate` در LaunchActivity.
  6. **noChannelSwitch** — `setNextChannels` در ChatActivity با toggle به null می‌رود (ژست کشیدن به پایین بی‌اثر می‌شود؛ پیش‌فرض خاموش).
  7. **hideStoriesRead** — فقط `sendRequest(TL_stories_readStories)` گیت شد؛ وضعیت خوانده‌شده محلی (max_read_id/storage/notification) سر جایش است.
  8. **bypassTranslation** — گیت `chatFull/userFull.translations_disabled` در `isTranslateDialogHidden`؛ انتخاب دستی خود کاربر (hideTranslateDialogs) محترم مانده.
  9. **توربو ارتقا** — پارامترهای پچ Morphe: پارچه ۱MB × ۱۲ درخواست موازی (قبلاً ۵۱۲KB × ۸).
- **غیرقابل‌پورت (مستند در کامنت AmberMorphe.java):** Unlock Premium (سرور-محور)، Bypass channel restrictions (گیت کلاینت در ۱۳.۲.۱ وجود ندارد — سرور محتوا را نمی‌فرستد)، Spoof signature/cert/install-source + Fix Firebase + Bypass integrity (زیرساخت Morphe برای APK ریمپ‌شده؛ فورک از سورس بیلد می‌شود و لاگین از قبل سالم است)، Rich clipboard paste (در این نسخه سورس وجود ندارد)، تلمتری (اصلاً Firebase Analytics/Crashlytics در سورس نیست)، Voice-to-music (خط لوله صوتی کل برنامه را می‌لرزاند — ریسک بالا).
- **UI:** ۸ ردیف toggle جدید در AmbergramSettingsActivity با همان الگوی spec array + get/set mapping؛ آیکون‌ها: msg_delete/msg_photo_blur/msg_camera/msg_copy/msg_download/msg_block2/msg_mute/msg_secret (همه موجود در res).
- **رشته‌ها:** ۱۶ کلید جدید دوزبانه (۸ نام + ۸ توضیح)؛ توضیح توربو هم برای اعداد جدید به‌روز شد.
- **نسخه:** 0.5.0 (7301)؛ چنج‌لاگ «NEW in 0.5.0 — full Morphe patch bundle» با ۸ آیتم + یادداشت ارتقای توربو.
- **اعتبارسنجی پیش از پوش:** توازن نسبی آکولاد هر ۱۰ فایل نسبت به HEAD = صفر؛ XML هر دو پک سالم؛ pyyaml سبز؛ ۰ دابل‌کوتیشن داخل notes.
- **نتیجه CI (پایش کامل شد):**
  - ci/master (43649039790): SUCCESS — هر ۱۰ فایل ویرایش‌شده و کلاس جدید کامپایل سالم.
  - release/v0.5.0-alpha (43653672487): SUCCESS — انتشار با ۴ asset.
  - راستی‌آزمایی: هر سه APK دانلود شد؛ sha256 با SHA256SUMS مطابقت کامل (۳×OK)؛ apksigner همه v1+v2 Verified؛ badging: universal=73019 (۴ ABI)، arm64=73012، armv7=73013، همه versionName «0.5.0 (7301)».
  - حجم‌ها: universal=83.1MB، arm64=44.9MB، armv7=43.7MB.
- **درس فنی این نوبت:** `rg -r` یعنی --replace و خروجی را خراب نمایش می‌دهد (دو بار متن گمراه‌کننده دیدم: «lnMessage» به‌جای sendScreenshotMessage و «lnListener» به‌جای AnalyticsListener)؛ پرچم -r را فقط عمدی بزن.

---

## نوبت ۷ — بازسازی کامل صف دانلود (نسخه 0.6.0)
- **گزارش کاربر:** صف دانلود خوب کار نمی‌کند: ۱) با چند فایل، یک تلاش کوچک می‌کند و با کوچک‌ترین اختلال پروکسی/نت بیخیال می‌شود و صف درست شکل نمی‌گیرد؛ ۲) بعد از اتمام فایل اول سراغ بقیه نمی‌رود و صف خودش را تمام‌شده می‌بیند. خواست: «خیلی بررسی و تست کن».
- **بررسی عمیق (۱۰ فایل مرتبط خوانده شد):** FileLoader → ImageLoader.FileLoaderDelegate → NotificationCenter.fileLoaded/fileLoadFailed(fileLoaded با (fileName, finalFile) و fileLoadFailed با (fileName, reason) پست می‌شود؛ reason=-1 کمبود فضا، reason=1 کنسل). ۶ نقص شناسایی شد:
  1. **بدون retry**: هر fileLoadFailed بلافاصله آیتم را FAILED می‌کرد — اختلال لحظه‌ای پروکسی = مرگ کل صف در چند ثانیه.
  2. **پاک‌سازی خودکار موارد شکست‌خورده**: وقتی همه آیتم‌ها سریع fail می‌شدند، شاخه drain در startNextIfNeeded همه DONE/FAILED را حذف می‌کرد → «صف اصلاً شکل نمی‌گیرد» (روایت ۱ کاربر).
  3. **تکرار current در persist()**: چون current هرگز از لیست صف حذف نمی‌شد، persist آن را دوبار می‌نوشت → بعد از ری‌استارت همان فایل دوبار دانلود می‌شد.
  4. **بدون آگاهی از شبکه**: با نت قطع، دانلودها پشت هم start و fail می‌شدند (cascade).
  5. **بدون watchdog**: عملیات فریزشده (پروکسی مرده) برای همیشه در حالت DOWNLOADING می‌ماند.
  6. **شکست بی‌صدا**: برای فایل‌های با نام نامعتبر (0_0/MIN_VALUE) هیچ event‌ای نمی‌آمد → صف همیشه گیر می‌کرد.
  - روایت ۲ کاربر («بعد از فایل اول، صف تمام‌شده می‌بیند») با ترکیب نقص ۱+۲ کامل توضیح داده می‌شود: فایل‌های بعدی با شبکه ناپایدار به‌سرعت fail و بلافاصله پاک می‌شدند؛ کاربر فقط فایل اول موفق را دید و صفحه خالی.
- **بازنویسی DownloadQueueController (همان API عمومی + ارتقا):**
  - **retry با backoff نمایی**: تا ۸ تلاش (۲s، ۴s، ۸s، ۱۵s، ۳۰s، ۶۰s، ۱۲۰s cap)؛ در فاصله backoff، صف جریان دارد و آیتم‌های بعدی دانلود می‌شوند (retry در نوبت بعدی خودش).
  - **آگاهی از شبکه**: شروع فقط با `getConnectionState()==ConnectionStateConnected`؛ در غیر این صورت poll هر ۵ ثانیه.
  - **watchdog رکود**: هر ۱۵s چک؛ ۹۰ ثانیه بدون بایت = کنسل + retry (تلاش جدید).
  - **FAILED ماندگار**: هرگز پاک‌سازی خودکار نمی‌شوند؛ در صفحه صف با دکمه «تلاش دوباره» (retryItem) می‌مانند و بعد از ری‌استارت هم دیده می‌شوند؛ فقط DONEها در drain حذف می‌شوند.
  - **current خارج از لیست صف** → persist دیگر تکراری نمی‌نویسد؛ snapshot با current در صدر.
  - **پیش‌اعتبارسنجی نام فایل** → شکست صریح به‌جای گیر بی‌صدا.
  - **persist بهبود**: attempts/retryAt هم ذخیره می‌شوند؛ loadQueue حالا FAILEDها را هم نگه می‌دارد.
- **UI**: ردیف FAILED در AmbergramQueueActivity دکمه Retry سبز گرفت (STATE_GREEN)؛ رشته دوزبانه AmbergramQueueRetry.
- **تست (خواسته صریح کاربر)**: شبیه‌ساز مستقل منطق (`/home/z/queuesim/queue_sim.py`) — آینه ۱:۱ ماشین حالت با ۸ سناریو / ۲۰ اظهار، همه سبز:
  A) اختلال لحظه‌ای با زمان‌بندی واقعی → retry خودکار + هیچ چیزی گم نمی‌شود؛ B) ادامه ترتیبی اکید؛ C) آفلاین ۶۰s → صفر load و صفر FAILED؛ D) فریز ۹۰s → watchdog retry؛ E) ۸ شکست متوالی → FAILED نمایان + صف ادامه + retry دستی؛ F) persist بدون تکرار؛ G) کمبود فضا = فوری FAILED؛ H) مرگ پروکسی وسط صف ۵تایی و ریکاوری → هر ۵ فایل کامل.
  - **شبیه‌ساز یک باگ واقعی هم لو داد**: در مسیر شکست کپی به Downloads، کد اول current را null می‌کرد و بعد failCurrent (با گارد current==item) رد می‌شد → آیتم برای همیشه گم می‌شد. اصلاح شد: منطق requeue/markFailed مستقیم در finishCurrentWithFile.
- **درس تست:** سناریونامه اول ۷ شکست داشت که همه خطای «تایم‌لاین غیرواقعی» بود (اتمام فایل در t=0 قبل از انقضای backoff) — نه خطای منطق؛ با زمان‌بندی واقع‌گرایانه همه سبز شدند. اول شکست تست → بعد تشخیص اینکه مقصر تست است یا کد.
- **نسخه:** 0.6.0 (7302).
- **نتیجه CI (پایش کامل شد):**
  - ci/master (43660354951): SUCCESS — کنترلر بازنویسی‌شده کامپایل سالم.
  - release/v0.6.0-alpha (43663717923): SUCCESS — انتشار با ۴ asset.
  - راستی‌آزمایی: هر سه APK دانلود شد؛ sha256 با SHA256SUMS مطابقت (۳×OK)؛ apksigner همه v1+v2 Verified؛ badging: universal=73029 (۴ ABI)، arm64=73022، armv7=73013، همه versionName «0.6.0 (7302)».
  - حجم‌ها: universal=83.1MB، arm64=44.9MB، armv7=43.7MB.

## نوبت ۸ — سند مرجع کامل کد (AMBERGRAM-CODE-REFERENCE.md)
- **درخواست کاربر:** همه بخش‌های کدنویسی‌شده با توضیحات در «یک فایل واحد» برای دیباگ.
- **روش:** بازسازی کامل از خود ریپو — ۱۰ فایل جدید Java + دیف کامل `git diff 7be672ead HEAD` برای همه فایل‌های اصلی تغییر‌یافته + رشته‌های Amber + workflows.
- **ساخت:** اسکلت فارسی ۱۱ بخش (نقشه، صف دانلود با راهنمای دیباگ اختصاصی، Morphe، ضدتبلیغ/توربو، شبح، پروکسی، هاب تنظیمات، تم/برند/فونت/آیکون، زیرساخت، جدول رشته‌ها، آشپزخانه دیباگ + تاریخچه) + تزریق خودکار کد/دیف با اسکریپت پایتون (`/home/z/docparts/assemble.py`).
- **حجم سند:** ~۵٬۵۵۰ خط / ۲۷۹KB؛ ۵۹ بلوک کد؛ بدون نشانگر جامانده.
- **کشف جانبی (برای دیباگ آینده):** ناهماهنگی رشته انگلیسی `AmbergramQueuePageHint` («Downloads/AmberGram») با کد کپی واقعی (`Downloads/Telegram`) — رشته فارسی درست است؛ در بخش ۱-۸ و ۱۰ سند ثبت شد.
- **نسخه:** بدون bump (فقط مستندات؛ versionCode همان 7302).

## نوبت ۹ — بسته اصلاحی عمیق v0.7.0-alpha (کد 7303)
- **ورودی کاربر:** «فیچرهای اضافه‌شده در عمل درست کار نمی‌کنند؛ باگ‌ها ریشه‌یابی شده‌اند؛ دقیقاً طبق مشخصات زیر اصلاح کن» + ۶ بسته مشخصات دقیق (صف دانلود، گیت‌های Morphe، حالت شبح، توربو، پروکسی، انتشار). خواسته سفت: بدون شکستن بیلد.
- **بسته ۱ — صف دانلود (۵ اصلاح):**
  1. **نام فایل خالی در UI**: `makeQueueRow` در AmbergramQueueActivity ویو nameView را می‌ساخت ولی هرگز `setText` نمی‌کرد → اکنون `nameView.setText(!TextUtils.isEmpty(item.displayName) ? item.displayName : item.fileName)` بلافاصله بعد از ساخت.
  2. **دسترسی به «دانلود ترتیبی»**: در این codebase اکشن‌مود هیچ `otherItem`/سه‌نقطه‌ای ندارد (API توصیف‌شده در مشخصات متعلق به نسخه‌های دیگر تلگرام است). معادل واقعی این نسخه: ActionBarMenuItem با addSubItem (الگوی TopicsFragment «other») — دکمه سه‌نقطه (`ic_ab_other`) جای دکمه مستقیم amber_queue در نوار اکشن‌مود نشست و amber_queue به‌عنوان زیرآیتم آن اضافه شد؛ کلیک زیرآیتم با همان مسیر `parentMenu.onItemClick(amber_queue)` به هندلر موجود در خط 3845 می‌رسد؛ زیرآیتم همیشه هنگام باز بودن اکشن‌مود نمایان است (معادل setSubItemVisible=true در این نسخه). جای مستقیم قبلی هم حذف شد تا دو دکمه مصرف فضا نکنند.
  3. **شکست فوری به‌خاطر parentObject==null**: QueueItem حالا `messageBase64` (کل messageOwner با SerializedData→Base64) + رفرنس موقت `transient MessageObject messageObject` را نگه می‌دارد؛ در `startNextIfNeeded` اگر messageObject null ولی messageBase64 هست، `TLRPC.Message.TLdeserialize` + `new MessageObject(account, msg, false, false)` و پاس دادن به‌عنوان parentObject به `FileLoader.loadFile` → FileRefController حالا file_reference منقضی را می‌تواند رفرش کند (بویژه فایل‌های کانال). persist/load با کلید «msg».
  4. **گیر صف در بررسی شبکه**: `isNetworkConnected` قبلا فقط `ConnectionStateConnected` می‌پذیرفت؛ حالا فقط `ConnectionStateWaitingForNetwork` را «قطع» می‌داند (Updating/Connecting = سالم).
  5. **هماهنگی مسیر ذخیره**: RELATIVE_PATH و مسیر legacy هر دو به `Downloads/AmberGram` رفتند + متن فارسی hint اصلاح شد (انگلیسی از قبل درست بود؛ در نوبت ۸ کشف شده بود).
- **بسته ۲ — گیت‌های Morphe (۴ اصلاح):**
  1. **ضدحذف واقعی**: `MessagesStorage.markMessagesAsDeleted` هر دو overload ابتدای متد `if (AmberMorphe.antiDelete()) return null;` (پوشش کانال‌ها + getDifference + همه صدا زنندگان؛ pts/pts_count لمس نشد). در MessagesController حلقه UI `deletedMessagesFinal` گیت شد (نه messagesDeleted پست می‌شود نه obj.deleted) + `deleteMessagesByPush` هم گیت شد (مسیر FCM).
  2. **ذخیره/کپی/اسکرین‌شات همه‌جا**: گیت `bypassNoforwards` به سر هر سه متد `isChatNoForwards(TLRPC.Chat)`، `isChatNoForwards(long)`، `isUserNoForwards(long)` — چون PhotoViewer/SharedMediaLayout/FLAG_SECURE در ChatActivity مستقیم صدا می‌زنند و از isPeerNoForwards رد نمی‌شوند.
  3. **ضدتک‌بار عکس/ویدیو**: گیت antiDisappearing در `isSecretPhotoOrVideo(Message)`، `isSecretMedia(Message)` استاتیک و `isSecretMedia()` نمونه‌ای — فقط برای چت‌های غیرمحرمانه (`!(instanceof TL_message_secret)`) false برمی‌گردانند؛ + در `markMessageContentAsRead` درخواست شبکه readMessageContents (هر دو شاخه channel/عادی) هنگام روشن بودن toggle ارسال نمی‌شود (علامت‌گذاری محلی حفظ شد تا UI باز بماند).
  4. **پرش کانال**: `allowPullingDownScroll` در ChatActivity حالا `&& !AmberMorphe.noChannelSwitch()` دارد — کل پنل کشیدن‌به‌پایین غیرفعال می‌شود (نال کردن setNextChannels کافی نبود).
- **بسته ۳ — حالت شبح (بازطراحی مالکیت flush):**
  - `AmberGhost.flushRead` از `ChatActivity.onPause` حذف شد (دلیل: فلاش تیک دوم موقع خروج/قفل صفحه).
  - `markDialogAsRead`: با ghost روشن → علامت‌گذاری محلی کامل (شمارنده UI صفر می‌شود) + `AmberGhost.stashRead`؛ هیچ ReadTask/شبکه‌ای ساخته نمی‌شود (پارامتر جدید `allowNetworkReadTask` در amberGhostMarkDialogAsRead؛ overload 9-آرگومانی با `!AmberGhost.isEnabled()` delegate می‌کند).
  - flush فقط در دو رویداد: (الف) ارسال پیام کاربر در همان چت — قیف `MessagesStorage.putMessages` (پیام out، غیر scheduled، mode!=1 → flushRead روی UI thread؛ idempotent)، (ب) `AmberGhost.setEnabled(false)` → flush همه stashها (حساب = UserConfig.selectedAccount).
  - آیکون آنلاین: `TL_account.updateStatus` مسیر keep-online حالا `req.offline = AmberGhost.isEnabled()` (پکت pause از قبل offline=true بود).
  - `shouldDeferRead/deferRead` → `stashRead` (hasStash هم اضافه شد)؛ chatOpened/chatClosed بدون تغییر برای سازگاری.
- **بسته ۴ — توربو دانلود**: بلوک turbo در `FileLoadOperation.updateParams` حالا `state == stateIdle` گارد دارد (updateParams در start() روی عملیات فعال هم صدا زده می‌شود → تغییر چانک وسط دانلود = OFFSET_INVALID) و اعداد به سقف پروتکل MTProto رفت: `downloadChunkSizeBig = 1024*512`، `maxDownloadRequests = 8`، `maxDownloadRequestsBig = 8` (1MB قبلی → LIMIT_INVALID سمت سرور/CDN)؛ محاسبه maxCdnParts بعد از بلوک می‌ماند.
- **بسته ۵ — پروکسی رایگان**: تابع `mirrorUrl(rawUrl)` — تبدیل خودکار `raw.githubusercontent.com/USER/REPO/BRANCH/PATH` به `cdn.jsdelivr.net/gh/USER/REPO@BRANCH/PATH`؛ در `runUpdateCycle` هر منبع اول raw و در شکست، خودکار jsDelivr (لاگ retry) — برای هر ۶ منبع. `REMOVE_AFTER_FAILS` از ۱ به ۳.
- **بسته ۶ — انتشار**: gradle.properties → 7303 / «0.7.0 (7303)»؛ changelog کامل 0.7.0 در release.yml (بدون `"`, هم‌تراز ۱۰ فاصله، طبق LESSONS 8)؛ strings فقط فا نیاز داشت.
- **سینتکس‌چک محلی**: javalang (پارسر جاوا در پایتون، چون JDK در سندباکس نصب نشد) — ۹ فایل Java تغییر یافته: ۸ تا OK کامل؛ MessagesController فقط در خط 1814 SYN-ERR دارد که با پارس نسخه HEAD همان فایل هم دقیقاً همان خطاست (محدودیت پارسر با `int[][]::new`) → false-positive؛ توازن برانس MessagesController/ChatActivity با HEAD یکسان. قبل از پوش، چک نهایی کامپایل را CI می‌کند.
- **نسخه:** 0.7.0-alpha (7303).
- **نتیجه CI (پایش کامل شد):**
  - ci/master push اول (43685122486): FAILURE — `MessagesStorage.java:13549 cannot find symbol scheduled`؛ TLRPC.Message فیلد scheduled ندارد؛ در putMessages معیار همان `mode == 1` است (صدا زنندگان `scheduled ? 1 : 0` می‌فرستند). فیکس → push دوم.
  - درس: شمارش regex برانس/پارانتر و پارسر javalang خطای symbol را نمی‌گیرند — تنها مرجع واقعی کامپایل CI است (LESSONS 15 تکمیل شد).
  - ci/master push دوم (43687727750): SUCCESS.
  - release/v0.7.0-alpha (43691834882): SUCCESS — انتشار با ۴ asset.
  - راستی‌آزمایی artifact: هر ۳ APK دانلود شد؛ sha256 با SHA256SUMS مطابق (۳×OK)؛ apksigner همه v1+v2 Verified؛ badging: universal=73039 (۴ ABI)، arm64=73032، armv7=73033، همه versionName «0.7.0 (7303)».
  - حجم‌ها: universal=83.1MB، arm64=44.9MB، armv7=43.7MB.
- **نتیجه:** نسخه 0.7.0-alpha (7303) منتشر شد؛ هر ۶ بسته مشخصات کاربر به‌طور کامل اعمال شد.

## نوبت ۱۰ — v0.8.0-alpha (کد 7304): پasse شفافیت، کنتراست و صادق‌سازی صف
- **ورودی کاربر:** «هیچ‌کدام از فیچرها درست کار نمی‌کنند: اسپانسری کانال‌ها نمایش داده می‌شود، فایل‌ها وارد صف دانلود نمی‌شوند و بعد از یک دانلود همه‌چیز تمام می‌شود، تم بشدت تیره است و مرزهای UI مشخص نیست، لوگو زشت است؛ تنها پروکسی و ذخیره در کانال خصوصی کار می‌کند.»
- **ریشه‌یابی‌ها (همه با خواندن کد واقعی):**
  1. **اسپانسری که هنوز دیده می‌شد**: مسیر «sponsored peers» در `DialogsSearchAdapter` (`TL_contacts_getSponsoredPeers`) هیچ گیت ضدتبلیغی نداشت — مستقل از مسیر گیت‌شده `MessagesController.getSponsoredMessages` است؛ + مسیر fetch «کانال‌های مشابه» (`getChannelRecommendations`) هم فقط در سلول رندر گیت شده بود نه در خود fetch (پروفایل/مدیا/سرچ).
  2. **«یک دانلود و تمام»**: `dialog_id` فیلد ران‌تایم `TLRPC.Message` است و در سریالایز نمی‌شود؛ پیام بازسازی‌شده از bytes (مسیر v0.7.0 برای parentObject) با dialog_id=0 ساخته می‌شد → `FileRefController.requestReferenceFromServer` با `getInputPeer(0)` هرگز نمی‌توانست file_reference را رفرش کند → همه تلاش‌ها به FAILED می‌رسید و در شاخه drain صف، اعلان بی‌صدا محو می‌شد. ترکیب دو نقطه = روایت دقیق کاربر.
  3. **«فایل‌ها وارد صف نمی‌شوند»**: ورودی تنهاِ صف در v0.7.0 زیر منوی سه‌نقطه اکشن‌مود بود (کشف‌ناپذیر در عمل) + پایان هر اجرا کاملاً بی‌صدا بود.
- **پچ‌ها:**
  - `DownloadQueueController`: مهر `dialogId` واقعی روی messageOwner بازسازی‌شده در هر attempt؛ اعلان پایان اجرا (`postCompletionNotification` — تعداد موفق/ناموفق + تاپ → صف) فقط وقتی ≥۱ آیتم در همین اجرا DONE شده؛ شمارش ناموفق در متن اعلان جاری؛ `messageFromString` حالا اکانت درست می‌گیرد.
  - `AmberDownloadService`: امضای update با failed + متن «X ناموفق».
  - `LaunchActivity`: extra `amber_open_queue` → presentFragment(AmbergramQueueActivity) (الگوی شاخه showDialogsList).
  - `ChatActivity`: دکمه مستقیم دانلود ترتیبی برگشت — **اولین** دکمه نوار انتخاب با آیکون `menu_download_round` (همان id=amber_queue=500)؛ جایگاه slot مخفی‌شده share فضا را حفظ می‌کند.
  - `DialogsSearchAdapter`: گیت `AmberAntiAds.noSponsored()` روی fetch sponsored peers؛ `MessagesController.getChannelRecommendations`: return null زودهنگام با toggle noRecommendations.
  - تم `amber.attheme` — ۱۴ کلید: windowBackgroundWhite 0xFF000000→0xFF141418، windowBackgroundGray→0xFF0B0B0D، divider 0x95000000→0x1FF0F0F0 (بالاخره مرئی!)، dialogBackground→0xFF18191D، actionBarDefault→0xF2141418، chat_wallpaper→0xFF0E0E11، inBubble→0xFF1E1F25، outBubble→0xFF3D2814، submenu bg/separator، switchTrack؛ + رنگ‌های preview در Theme.java.
  - **لوگوی جدید**: هواپیمای کاغذی تاخورده با گرادیان آمبر — تولید کامل با PIL (بدون AI-gen): foreground ۵ density، background clip (مربع/گرد، گرادیان زغالتی + glow گرم)، legacy ۴۸..۱۹۲ (مربع/گرد)، مونوکروم سفید؛ بال پایینی با گرادیان روشن‌تر تا افکت تاخوردگی روی پس‌زمینه تیره خوانا باشد.
  - رشته‌ها: `AmberQueueFailedCount`، `AmberQueueFinishedTitle`، `AmberQueueFinishedAll`، `AmberQueueFinishedFailed` (دوزبانه) + متن راهنمای صف به‌روز شد (سه‌نقطه → دکمه گرد)؛ `"` خام در XML با &quot;.
- **درس‌های جدید (→LESSONS 18، 19):** فیلدهای runtime MessageObject پس از هر دی‌سریالایز باید مهر مجدد شوند؛ پایان هر پردازش باید اعلان صریح داشته باشد — بی‌صدایی توسط کاربر «خرابی» تفسیر می‌شود.
- **سینتکس‌چک محلی:** javalang روی ۷ فایل ویرایش‌شده: ۶ OK + MessagesController false-positive معروف (خط 1814 `int[][]::new` — همان خطا روی HEAD).
- **نسخه:** 0.8.0-alpha (7304) — gradle.properties؛ changelog تک‌خط 0.8.0 در release.yml (بدون `"`، هم‌تراز ۱۰ فاصله، pyyaml VALID).
- **نتیجه CI (پایش کامل):**
  - ci/master push اول (43767167057): SUCCESS — ~۴۸ دقیقه.
  - release/v0.8.0-alpha (43770950080): SUCCESS — ~۴۸ دقیقه، ۴ asset.
  - راستی‌آزمایی: هر ۳ APK دانلود شد؛ sha256 با SHA256SUMS مطابق (۳×OK)؛ apksigner همه v1+v2 Verified؛ badging: universal=73049، arm64=73042، armv7=73043، همه versionName «0.8.0 (7304)».
  - حجم‌ها: universal=82.4MB، arm64=44.2MB، armv7=43.0MB.
- **نتیجه:** v0.8.0-alpha منتشر شد؛ چهار شکایت کاربر (اسپانسری، صف، تم، لوگو) هر کدام با پچ مشخص و ریشه مستند شده.

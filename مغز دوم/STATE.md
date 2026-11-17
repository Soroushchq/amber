# وضعیت فعلی پروژه

> آخرین به‌روزرسانی: نوبت ۲۶ — UI 2.0؛ **قدم ۲۰: حباب ورودی — رادیوس ۲۶ (SHAPE_BUBBLE) + زنجیرهٔ کم‌حجم + رفع خانوادهٔ ری‌اکشن** — هندسه: پیش‌فرض SharedConfig.bubbleRadius از ۱۷ آپستریم به توکن SHAPE_BUBBLE (۲۶dp؛ **اولین مصرف‌کنندهٔ این توکن**) بایند شد (۲ سایت: مقدار اولیه + خواندن SharedPreferences با حفظ انتخاب کاربر) + سقف اسلایدر «Message corners» در ThemeActivity از ۱۷ به توکن (مصرف‌کننده‌های شعاع بزرگ مثل getExtraTimeX=(r−۱۱)/۱٫۵ خودکار تنظیم می‌شوند)؛ **میراث قدم ۱۹**: ۵ کلید chat_compact_in* (inTimeText/inAudioDuration/inWaveform/inWaveformBackground/inTranscribeButton) پالت‌سازی شد — آپستریم سرد 0x80A1AAB3 و 1A1D21 بودند و اصلاً در پالت نبودند ← صدای منبع mapCompact هر کلید (زمان/مدت=dim/پر موج=اکسنت/بستره=جوهر×۳۰٪روز،×۳۵٪شب/دکمه=اکسنت جامد)؛ **رفع باگ واقعی ری‌اکشن**: chat_inReactionButtonBackground باید «جامد» می‌بود (آپستریم جامد؛ مصرف‌کننده‌ها خودشان ×۰٫۱۵۶/0x10 می‌سازند: چیپ ری‌اکشن ReactionsLayoutInBubble، transcribe، ReactionTabHolderView، TopicButton، TopicsSidePanel، SearchTagsList) — اکسنت×۱۰٪ قبلی چیپ غیرانتخاب‌شده را ۱٫۶٪ و آیکون transcribe را تقریباً نامرئی کرده بود ← اکسنت جامد؛ + متن چیپ انتخاب‌شده chat_inReactionButtonTextSelected از اکسنت (روی اکسنت = نامرئی!) ← onAccent (روز ۴٫۲۹ / شب ۷٫۲۳)؛ کلیدهای attheme: شب ۸۶۲ (۵ بازنویسی) / روز ۵۸۸ (۵ جدید + ۲ بازنویسی)؛ پیش‌نمایش Tools/preview_step20_bubble.py (حباب متن/صوتی r=۲۶ + چیپ‌ها + بوم کم‌حجم)؛ هیچ منطقی تغییر نکرد (۳ خط مقدار پیش‌فرض/سقف اسلایدر)؛ چک‌ها: javalang سبز روی ۳ فایل، رفت‌وبرگشت مولد OK | قدم بعدی: ۲۱ (حباب خروجی — primary-container FFDDB8، متن 331E00)

## هویت پروژه
- نام: **AmberGram** — فورک شخصی تلگرام اندروید (GPL-2.0)
- ریپازیتوری: `Soroushchq/amber` — شاخه `master`
- پایه: تلگرام رسمی 13.2.1 (کد 7291)
- ساخت/انتشار: GitHub Actions — `.github/workflows/release.yml` (فقط تگ `v*`)؛ **۳ APK امضاشده** (universal / arm64-v8a / armeabi-v7a) + SHA256SUMS برای هر سه
- پوش معمولی به master امن است (CI اجرا نمی‌شود؛ ولی ci/master کامپایل را چک می‌کند — قبل از تگ صبر برای سبز شدنش)

## نسخه‌ها
- نسخه فعلی منتشرشده: **0.8.0 (7304)** — تگ `v0.8.0-alpha` — پasse شفافیت: تم کنتراست‌دار + لوگوی هواپیمای کاغذی + گیت sponsored peers/recommendations + فیکس dialog_id صف + اعلان پایان اجرا
- قبل از آن: 0.7.0 (7303) — بسته اصلاحی عمیق | 0.6.0 (7302) — صف دانلود مقاوم
- قبل از آن: 0.5.0 (7301) — بسته کامل Morphe (۸ پچ + توربو ۱MB×۱۲) | 0.4.0 (7300) — بسته ضدتبلیغ | 0.3.1 (7299) — APKهای هر معماری | 0.3.0 (7298) — حالت شبح
- نسخه بعدی: **0.9.0 (7305)** — پایان UI 2.0 (versionCode فقط در قدم ۴۹ bump می‌شود)
- محل تعریف نسخه: `gradle.properties` در **ریشه ریپو** (خط 16-17: `APP_VERSION_CODE` / `APP_VERSION_NAME`)
- فلاورها: `afat`=9 (universal) | `arm64`=2 | `armv7`=3 | `bundleAfat`=1 (فقط AAB)؛ versionCode هر فلاور = APP_VERSION_CODE×10 + abiVersionCode

## تاریخچه تگ‌ها
v0.2.0 → v0.2.1 → v0.2.3 → v0.2.4 → v0.2.5 (صف دانلود اختصاصی + هدر برند-امن) → v0.2.6 → v0.2.7 (حذف خودکار پروکسی مرده) → v0.2.8 (پروکسی‌های رایگان درون‌برنامه‌ای + پاکسازی مرده‌ها) → v0.2.9 → v0.3.0 (حالت شبح) → v0.3.1 (APK سبک هر ABI + راهنمای نصب فارسی) → v0.4.0 (ضدتبلیغ + توربو) → v0.5.0 (بسته کامل Morphe: ۸ پچ) → v0.6.0 (صف دانلود مقاوم) → v0.7.0 (بسته اصلاحی عمیق) → **v0.8.0 (شفافیت/کنتراست — منتشر شد)**

> هشدار قدیمی (changelog کپی v0.2.9) برطرف شد — از v0.3.0 به بعد changelog واقعی است.

## قابلیت‌های انجام‌شده (همه منتشر شده‌اند)
1. تم مشکی OLED + نارنجی آمبر به‌صورت `amber.attheme` داخلی و پیش‌فرض (کلیدهای Saved/Archived هم در پالت)
2. فونت زیبای UI (Baloo Bhaijaan 2 Bold)
3. تغییر نام کامل به AmberGram و **حذف کامل واژه Telegram**: بازنویسی runtime در همه پکیج‌های زبان (`d52ca265`) + محافظت کلیدهای برند از پک‌های زبان ریموت؛ هدر برنامه همیشه AmberGram
4. **اسم چت‌ها/کانال‌ها سفید شد** + تیک تأیید واضح‌تر (`6e1a84dd`) — همان درخواست «سردرد» کاربر انجام شد
5. آیکون‌های جایگزین: مجموعه Leopard — 3 هواپیمای کاغذی + 3 ققنوس آمبر، قابل انتخاب از Settings > Themes (`34fac1e7`)
6. آیکون لانچر اصلی: ققنوس × هواپیمای کاغذی با افکت برجسته (embossed) — انتخاب نهایی کاربر: طرح «شبح آمبر»
7. بخش تنظیمات AmberGram (`AmbergramSettingsActivity`) با صف دانلود زنده (`AmbergramQueueActivity`)
8. صف دانلود پس‌زمینه ترتیبی (`AmberDownloadService`) — بعد از اتمام همه دانلودها سرویس و نوتیف کامل خاموش می‌شود
9. پروکسی‌های رایگان درون‌برنامه‌ای (`AmbergramProxyManager` + `AmbergramProxyActivity` + `AmbergramProxyReceiver`): 6 کلکتور GitHub، رفرش 6 ساعته + جبران موقع باز شدن برنامه، ادغام/حذف تکراری، تست واقعی MTProto handshake بدون قطع اتصال فعال، تپ=اتصال، لانگ‌پرس=کپی لینک t.me
10. پاکسازی خودکار پروکسی مرده: `REMOVE_AFTER_FAILS=3` (از v0.7.0؛ قبل از آن ۱)، نگهبان آفلاین `OFFLINE_GUARD_MIN_TESTED=10`، سوییچ خودکار به بهترین پروکسی زنده، رویداد `EVENT_LIST_CLEANED` → Toast با رشته `AmbergramProxyRemoved`
11. **حالت شبح (v0.3.0)**: کلاس `AmberGhost` — پیام‌ها تا خروج از چت خوانده‌شده ثبت نمی‌شوند، نشانگر تایپ هرگز ارسال نمی‌شود؛ کلید در تنظیمات AmberGram (آیکون ghost نارنجی)؛ رشته‌های دوزبانه `AmberGhost*`
15. **بسته اصلاحی عمیق (v0.7.0)**: صف دانلود — نام فایل در UI، سه‌نقطه اکشن‌مود (ActionBarMenuItem.addSubItem)، parentObject پیام کامل برای رفرش file_reference، گیت شبکه فقط WaitingForNetwork، ذخیره در Downloads/AmberGram؛ Morphe — ضدحذف واقعی (Storage دو overload + UI cache + push)، bypassNoforwards در سر ۳ متد isChatNoForwards/isUserNoForwards، ضدتک‌بار در isSecretMedia/isSecretPhotoOrVideo + عدم ارسال readMessageContents، قطع کامل ژست کشیدن‌به‌پایین؛ شبح — حذف flush از onPause، stashRead + flush فقط در ارسال پیام (قیف putMessages) یا خاموش‌کردن شبح، offline=true همیشگی در updateStatus؛ توربو — چانک 512KB×8 با گارد stateIdle (سقف پروتکل MTProto)؛ پروکسی — میرور خودکار jsDelivr برای هر ۶ منبع + REMOVE_AFTER_FAILS=3.
14. **صف دانلود مقاوم (v0.6.0)**: بازنویسی DownloadQueueController — retry خودکار با backoff نمایی (۸ تلاش)، آگاهی از شبکه (poll ۵s)، watchdog رکود ۹۰s، FAILED ماندگار با دکمه تلاش دوباره (باقی بعد از ری‌استارت)، صف حین backoff جریان دارد، رفع تکرار current در persist؛ تأیید با شبیه‌ساز ۸ سناریو/۲۰ اظهار (`/home/z/queuesim/queue_sim.py`)
12. **بسته ضدتبلیغ + توربو (v0.4.0)**: کلاس `AmberAntiAds` — بدون اسپانسری (no fetch!)، بدون کانال پیشنهادی، دانلود توربو (۱MB×۱۲ — اعداد Morphe)، بدون استیکر خوش‌آمدگویی؛ ۴ toggle در تنظیمات AmberGram؛ الهام از پچ‌های Morphe (HushTelegram)؛ **v0.8.0**: گیت واقعی sponsored peers جستجو + گیت fetch recommendations
16. **بسته شفافیت (v0.8.0)**: تم آمبر با پالت گرافیتی لایه‌دار (دیوایدرهای مرئی، bubbleهای روشن‌تر، پس‌زمینه غیر خالص‌مشکی) + لوگوی جدید هواپیمای کاغذی (PIL، همه densityها + مونوکروم) + دکمه مستقیم دانلود ترتیبی در ابتدای نوار انتخاب + مهر dialog_id روی MessageObject بازسازی‌شده (ریشه «یک دانلود و تمام») + اعلان پایان اجرا با شمار موفق/ناموق که تاپش صف را باز می‌کند
13. **بسته کامل Morphe (v0.5.0)**: کلاس `AmberMorphe.java` — ۸ پچ بومی: ضدحذف (anti-delete)، ماندگاری رسانه تک‌بار (صدا/دایره‌ای)، بدون اعلان اسکرین‌شات، ذخیره‌پذیری همه‌جا (bypass noforwards)، بدون به‌روزرسانی درون‌برنامه‌ای، بدون رسید بازدید استوری، ترجمه همیشه فعال، قطع اختیاری ژست سوییچ کانال؛ توربو ارتقا به ۱MB×۱۲؛ ۱۲ toggle در تنظیمات AmberGram

## کارهای صف‌شده فعلی
- **پروژه فعال: UI 2.0 — بازطراحی ۵۰ قدمی با کانسپت C (Expressive Material)** — نقشه کامل در `UI2-ROADMAP.md`؛ **فاز ۰ کامل (قدم‌های ۱-۶)؛ فاز ۱ کامل (قدم‌های ۷-۱۰)** — قدم ۱۱: کانتینر هدر Expressive؛ قدم ۱۲: پیل شناور تب‌ها؛ قدم ۱۳: کارت ردیف SHAPE_CARD ۲۰dp + ripple گرم؛ قدم ۱۴: شمارنده/بج‌ها — SHAPE_BADGE ۱۲dp + رفع بج بی‌صدای نامرئی (کلید MutedText)؛ قدم ۱۵: فاب Expressive — SHAPE_FAB ۲۰dp + رفع نشتی آبی فاب روز (کلید جدید addButtonIcon، سایه آمبر ELEV_FAB/tint توکنی)؛ قدم ۱۶: دراور/منوی اصلی — کارت ItemOptions با ۹-پیچ بازتولید SHAPE_MENU ۲۰dp (مولد generate_amber_menu_popup.py) + رفع سفید هاردکد روز ← DAY_SURFACE + ردیف‌ها SHAPE_MENU_ROW ۱۲dp (تو‌در‌تو M3). قدم ۱۷: حالت جستجو — بار جستجو SHAPE_FIELD ۱۶dp (اولین مصرف SHAPE_FIELD) + ۵ رفع رنگی + چیپ SHAPE_BADGE. قدم ۱۸: نوار اکشن‌مود/آرشیو — ۶ کلید نشتی پالت‌سازی شد (خانواده سوییچ «قرمز←آبی» آپستریم ← «خنثی←اکسنت» با رفع مسیر پیش‌فرض Switch، متن فرعی منو، چیپ فیلتر، متن روی اکسنت، دستگیره انتخاب متن) — **فاز ۲ (لیست چت) کامل ۸/۸**. قدم ۱۹: پس‌زمینه صفحه چت — وایپرپ ۴فاز توکنی (تأیید) + کلید rotation صریح + رفع مسیر کم‌حجم (بوم تخت وایپرپ + قرص سرویس شب که نامرئی بود). قدم ۲۰: حباب ورودی — bubbleRadius پیش‌فرض ۱۷←SHAPE_BUBBLE (۲۶dp؛ اولین مصرف؛ سقف اسلایدر هم توکن)؛ ۵ کلید compact_in* پالت‌سازی (میراث قدم ۱۹)؛ رفع باگ ری‌اکشن: inReactionButtonBackground جامد اکسنت (قبلاً ×۱۰٪ = چیپ ۱٫۶٪ و transcribe نامرئی) + متن چیپ انتخاب‌شده onAccent. قدم بعد: ۲۱ (حباب خروجی — primary-container FFDDB8، متن 331E00). با هر «پردازش کن» یک قدم جلو؛ نسخه نهایی 0.9.0 (7305).
- ⚠️ **درس نوبت ۱۲**: کامیت‌های محلی قدم‌های ۱-۵ در ریست سندباکس گم شدند؛ کل محتوا از اسناد مغز دوم + خلاصه نشست بازسازی شد. **از این به بعد: پوش بعد از هر قدم، بدون استثنا.**
- ایده‌های دیگر (یادآور پیام، تقویم شمسی، پیام‌شمار) در `IDEAS.md` ماند — بعد از UI 2.0.

## محیط کاری
- کلون محلی: `/home/z/amber` (با ریست سندباکس: `bash /home/z/my-project/amber-git/restore-amber.sh` + `git fetch --unshallow`)
- اعتبارسنجی جاوا: javac نیست؛ `python3 /home/z/my-project/amber-git/syntax_check.py FILE.java` (javalang)
- لیست ۸۶۲ کلید معتبر attheme: `rg -o 'colorKeysMap\.put\(key_[A-Za-z0-9_]+, "([^"]+)"\)' -r '$1' ThemeColors.java | sort -u > /tmp/valid_keys.txt` (بعد از هر ریست دوباره بساز)
- لاگ‌های CI قبلی: `/home/z/ci18`

## چک‌لیست انتشار (تگ v0.9.0-alpha — قدم ۴۹/۵۰)
1. `gradle.properties` (ریشه): bump کد به 7305 و نام به 0.9.0
2. changelog واقعی در `.github/workflows/release.yml` — بدون `"` داخلی؛ **همه خط‌ها هم‌تراز ۱۰ فاصله** (خط بدون تورفتگی YAML را می‌شکند!)؛ اعتبارسنجی pyyaml قبل از پوش
3. commit + push به master
4. **صبر برای سبز شدن ci/master (کامپایل validate)** — بعد تگ `v0.9.0-alpha` بزن و پوش کن
5. پایش لاگ CI با جستجوی `error:` (هر دو workflow: release تگ + ci master)
6. **بعد از انتشار: خود artifact را راستی‌آزمایی کن** — دانلود از API + sha256sum با SHA256SUMS + `apksigner verify` (build-tools از dl.google.com؛ با ریست سندباکس دوباره دانلودش کن)
7. گزارش نهایی به کاربر به فارسی

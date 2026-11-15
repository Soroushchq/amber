# نکته‌برداری فنی — خطاها، راه‌حل‌ها و درس‌ها

## خطاهای کامپایل / CI و راه‌حل‌ها
1. **lambda و effectively-final (دو بار رخ داده!)**
   - `15feeb3d`: lambda متغیر `ok` را می‌گرفت که effectively final نبود → خطای کامپایل
   - `7b0243dd`: در `AmbergramProxyManager` متغیر `best` داخل حلقه دوباره مقداردهی می‌شد → با `removedFinal`/`bestFinal` (final محلی) حل شد
   - درس: هر جا lambda داخل حلقه متغیری را می‌گیرد که عوض می‌شود، بلافاصله نسخه `final` محلی بساز.
2. **مسیر artifact در CI**: برای flavor `afat` مسیر `apk/afat/debug` بود (`7e427bbb`)
3. **پکیج DownloadManager**: `android.app.DownloadManager` (نه android.provider) + import گمشده `TextUtils` (`d632b98e`)
4. **ContactsController**: نوع اکانت در SQL/URI باید literal باشد، نه متغیر (`789bfc4c`)
5. **quoting یادداشت انتشار در release.yml**: کاراکتر `"` داخل متن changelog پارس shell را می‌شکند و قبل از اجرای `gh` خطای glob می‌دهد (`e3aca0f2`) → هرگز quote دوتایی داخل رشته‌های changelog نگذار.
6. **رشته‌های فارسی**: placeholder خام `%` باعث کرش می‌شود → همیشه شماره‌دار بنویس: `%1$s`.

## احراز هویت گیت (نکته حیاتی)
- توکن GitHub در `/home/z/my-project/amber-git/git-credentials` نگه داشته می‌شود — این مسیر بین پیام‌ها پاک نمی‌شود؛ **مقدار توکن هرگز داخل ریپو نوشته نمی‌شود** (ریپو عمومی است)، فقط این مسیر ثبت می‌شود.
- بعد از هر ریست سندباکس کافی است: `bash /home/z/my-project/amber-git/restore-amber.sh` → احراز هویت + هویت گیت + کلون `/home/z/amber` همه یک‌جا بازگردانی می‌شوند.
- اگر کاربر توکن را عوض کرد: فقط محتوای `git-credentials` را به‌روز کن (فرمت: `https://USER:TOKEN@github.com`).

## درس‌های محیطی
- سندباکس ریست می‌شود: `/home/z/amber` و پوشه home پاک می‌شوند ولی `/home/z/my-project` پایدار است → اول وجود مسیرها را چک کن؛ بعد `bash /home/z/my-project/amber-git/restore-amber.sh` را اجرا کن؛ وضعیت واقعی ریپو را با GitHub API (کامیت‌ها/تگ‌ها/ریلیزها) کالیبره کن، به حافظه قدیمی اعتماد نکن.
- شبیه‌ساز اندروید در سندباکس وجود ندارد → «اسکرین‌شات از تم برنامه» ممکن نیست؛ جایگزین: بازبینی سیستماتیک کد کلیدهای رنگ تم (`Theme.java`، `DialogCell`).
- پوش معمولی به master امن است؛ CI فقط با تگ `v*` اجرا می‌شود.

## نکات دامنه پروژه
- نسخه در `gradle.properties` **ریشه ریپو** تعریف می‌شود (نه TMessagesProj).
- رشته‌ها همیشه دوزبانه: `values/strings.xml` (انگلیسی) + `values-fa/strings.xml` (فارسی).
- برندینگ: پک‌های زبان ریموت می‌توانند رشته‌ها را بازنویسی کنند → کلیدهای برند باید محافظت/بازنویسی runtime شوند (`d52ca265`).
- آیکون‌های جایگزین اندروید: چند `<activity-alias>` در AndroidManifest + `PackageManager.setComponentEnabledSetting` + انتخابگر در تنظیمات + رشته‌های `AppIcon*`.
- کلیدهای مهم تم: `Theme.java` (مثل `key_windowBackgroundWhiteBlackText`)؛ رنگ نام چت‌ها در `DialogCell`.
7. **قبل از تشخیص «دانلود خراب»، خود artifact را باز کن**: دانلود APK منتشرشده + sha256sum + `apksigner verify --verbose` + `aapt2 dump badging` + چک STORED بودن resources.arsc با `unzip -v` — همه در سندباکس ممکن است (build-tools r34 از dl.google.com؛ apksigner با جاوا ۲۱ کار می‌کند). این‌بار نتیجه: artifact سالم، مشکل سمت دانلود/دستگاه بود؛ ولی بدون این بازرسی ادعا نمی‌شد.
8. **تورفتگی خط‌های غیرانگلیسی در بلوک `run: |`**: هر خطی که در اول ستون (بدون تورفتگی) بنویسی از literal block scalar بیرون می‌زند و YAML می‌شکند (مثلاً `**عنوان**` → alias error). همیشه همه خط‌های متن changelog را هم‌تراز بقیه (۱۰ فاصله) بنویس؛ اعتبارسنجی pyyaml قبل از push.
9. **جای خالی در versionCode فلاورها**: فلاورهای جدید باید abiVersionCode زیر فلاور universal (9) بگیرند تا ارتقا از APK سبک به universal همیشه مجاز باشد (قاعده تلگرام: universal=9).
10. **`rg -r` خروجی را خراب می‌کند**: `-r` یعنی `--replace` و اگر ناخواسته با دیگر پرچم‌ها ترکیب شود (`-rln`)، متن تطبیق را با رشته جایگزین نشان می‌دهد و خواننده را گمراه می‌کند (بوده‌ایم: sendScreenshotMessage را «lnMessage» دیدیم). برای جستجوی ساده فقط `-n`/`-l`/`-a` به‌کار ببر.
11. **نقشه پورت پچ‌های Morphe برای فورک سورس**: ۲۰ پچ Morphe → ۴ قابل پورت مستقیم (قبلی) + ۸ پورت شد در 0.5.0 + توربو ارتقا؛ غیرقابل‌پورت‌ها: پرمیوم/کانال محدود (سرور-محور)، اسپویف امضا/گواهی/منبع نصب + تعمیر Firebase (زیرساخت APK ریمپ)، Rich clipboard (سورس ندارد)، تلمتری (سورس ندارد). پیش از ادعای «همه پچ‌ها»، هر مورد یا پیاده یا با دلیل مستند می‌شود.

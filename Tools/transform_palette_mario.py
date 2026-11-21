#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مبدل یک‌بارمصرف — تزریق برند «دنیای ماریو» به AmberPalette.java (v0.9.10-ui2)
# الگوی عیناً transform_palette_premiere.py:
# ۱) پوشش مکانیکی هر ternary هم‌پسوندِ سه‌برند:
#    au ? (d ? AURORA_DAY_X : AURORA_NIGHT_X) : pr ? (d ? PREMIERE_DAY_X : PREMIERE_NIGHT_X) : (d ? DAY_X : NIGHT_X)
#    → … : pr ? (…) : ma ? (d ? MARIO_DAY_X : MARIO_NIGHT_X) : (d ? DAY_X : NIGHT_X)
# ۲) جدول صریح برای شاخه‌های اختصاصی (لوکال‌ها/وایپرپ/سوییچ/جدول/شیشه/سینما)
# ۳) بخش «اکسنت‌های مکمل» — بازنویسی با مپ کلید→رنگ سرزمین ماریو
# هر جایگزینی باید دقیقاً یک‌بار رخ دهد؛ وگرنه اسکریپت FATAL می‌دهد.
import re, sys

PATH = "TMessagesProj/src/main/java/org/telegram/messenger/AmberPalette.java"
src = open(PATH, encoding="utf-8").read()

EXPLICIT = []

# ── ۱) سرِ کلاس: کش‌ها + mode‌های دنیای ماریو + امضای build ────────────────────
EXPLICIT.append((
    """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;
    private static Map<String, Integer> premiereDayCache;
    private static Map<String, Integer> premiereNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا)، MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا)
     * و MODE_PREMIERE_NIGHT / MODE_PREMIERE_DAY (شب اکران).
     * برند سوم v0.9.9 — «عصر طلایی هالیوود». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false, false, false);
            }
            return nightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_NIGHT) {
            if (auroraNightCache == null) {
                auroraNightCache = build(false, true, false);
            }
            return auroraNightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_DAY) {
            if (auroraDayCache == null) {
                auroraDayCache = build(true, true, false);
            }
            return auroraDayCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_NIGHT) {
            if (premiereNightCache == null) {
                premiereNightCache = build(false, false, true);
            }
            return premiereNightCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_DAY) {
            if (premiereDayCache == null) {
                premiereDayCache = build(true, false, true);
            }
            return premiereDayCache;
        }
        if (dayCache == null) {
            dayCache = build(true, false, false);
        }
        return dayCache;
    }""",
    """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;
    private static Map<String, Integer> premiereDayCache;
    private static Map<String, Integer> premiereNightCache;
    private static Map<String, Integer> marioDayCache;
    private static Map<String, Integer> marioNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا)، MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا)،
     * MODE_PREMIERE_NIGHT / MODE_PREMIERE_DAY (شب اکران)
     * و MODE_MARIO_NIGHT / MODE_MARIO_DAY (دنیای ماریو).
     * برند چهارم v0.9.10 — «سرزمین پلتفرمر کلاسیک». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false, false, false, false);
            }
            return nightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_NIGHT) {
            if (auroraNightCache == null) {
                auroraNightCache = build(false, true, false, false);
            }
            return auroraNightCache;
        }
        if (mode == AmberTokens.MODE_AURORA_DAY) {
            if (auroraDayCache == null) {
                auroraDayCache = build(true, true, false, false);
            }
            return auroraDayCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_NIGHT) {
            if (premiereNightCache == null) {
                premiereNightCache = build(false, false, true, false);
            }
            return premiereNightCache;
        }
        if (mode == AmberTokens.MODE_PREMIERE_DAY) {
            if (premiereDayCache == null) {
                premiereDayCache = build(true, false, true, false);
            }
            return premiereDayCache;
        }
        if (mode == AmberTokens.MODE_MARIO_NIGHT) {
            if (marioNightCache == null) {
                marioNightCache = build(false, false, false, true);
            }
            return marioNightCache;
        }
        if (mode == AmberTokens.MODE_MARIO_DAY) {
            if (marioDayCache == null) {
                marioDayCache = build(true, false, false, true);
            }
            return marioDayCache;
        }
        if (dayCache == null) {
            dayCache = build(true, false, false, false);
        }
        return dayCache;
    }"""
))

EXPLICIT.append((
    "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) — pr = برند شب اکران (عصر طلایی هالیوود) در برابر برند کهربا */\n"
    "    private static Map<String, Integer> build(boolean d, boolean au, boolean pr) {",
    "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) — pr = برند شب اکران (عصر طلایی هالیوود) — ma = برند دنیای ماریو (سرزمین پلتفرمر کلاسیک) در برابر برند کهربا */\n"
    "    private static Map<String, Integer> build(boolean d, boolean au, boolean pr, boolean ma) {"
))

# ── ۲) پوشش مکانیکی هم‌پسوند ─────────────────────────────────────────────────
def wrap(m):
    sfx = m.group(1)
    return (f"au ? (d ? AmberTokens.AURORA_DAY_{sfx} : AmberTokens.AURORA_NIGHT_{sfx})"
            f" : pr ? (d ? AmberTokens.PREMIERE_DAY_{sfx} : AmberTokens.PREMIERE_NIGHT_{sfx})"
            f" : ma ? (d ? AmberTokens.MARIO_DAY_{sfx} : AmberTokens.MARIO_NIGHT_{sfx})"
            f" : (d ? AmberTokens.DAY_{sfx} : AmberTokens.NIGHT_{sfx})")

mech = re.compile(
    r"au \? \(d \? AmberTokens\.AURORA_DAY_([A-Za-z_]+) : AmberTokens\.AURORA_NIGHT_\1\)"
    r" : pr \? \(d \? AmberTokens\.PREMIERE_DAY_\1 : AmberTokens\.PREMIERE_NIGHT_\1\)"
    r" : \(d \? AmberTokens\.DAY_\1 : AmberTokens\.NIGHT_\1\)")
src, mech_count = mech.subn(wrap, src)
if mech_count < 20:
    sys.exit(f"FATAL: mechanical wraps suspiciously low: {mech_count}")

# ── ۳) موتور تزریق سطح‌بالا — همهٔ خطوط با زنجیرهٔ au/pr بیرون از پرانتز ──────
# مقدار هر خط باید ساختار «au ? X : pr ? Y : Z» داشته باشد؛ X/Y/Z ممکن است
# (d ? A : B)، توکن ثابت یا ترکیب توکن+alpha باشند. تزریق: … : pr ? Y : ma ? MA : Z
MARIO = {
    # لوکال‌های سطح‌بالا
    "white":                 "ma ? (d ? AmberTokens.MARIO_DAY_BG : AmberTokens.MARIO_NIGHT_BG)",
    "divider":               "ma ? (d ? AmberTokens.MARIO_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.MARIO_NIGHT_OUTLINE, 0.55f))",
    "deepFile":              "ma ? (d ? 0xFFE3EEFF : 0xFF1A2344)",
    "outTime":               "ma ? (d ? 0xFF6E5605 : 0xFF123A1A)",
    "sentCheckRead":         "ma ? (d ? 0xFF7A5E06 : 0xFF0F3A1E)",
    # جدول صریح — وایپرپ «زیرزمین سکه‌ها»
    "chat_wallpaper":                  "ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID)",
    "chat_wallpaper_gradient_to":      "ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_BOTTOM : AmberTokens.MARIO_NIGHT_WALLPAPER_TOP)",
    "key_chat_wallpaper_gradient_to2": "ma ? (d ? AmberTokens.MARIO_DAY_BG : AmberTokens.MARIO_NIGHT_WALLPAPER_BOTTOM)",
    "key_chat_wallpaper_gradient_to3": "ma ? (d ? AmberTokens.MARIO_DAY_HEADER : AmberTokens.MARIO_NIGHT_SURFACE)",
    "chat_compact_background":         "ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID)",
    "chat_compact_fadeEdge":           "ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID)",
    # سطوح و پنجره‌ها
    "windowBackgroundGray":            "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG)",
    "windowBackgroundGrayShadow":      "ma ? (d ? 0x1416243E : 0x28000000)",
    "dialogBackgroundGray":            "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG)",
    "actionBarDefaultArchived":        "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE)",
    "iv_backgroundGray":               "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_BG)",
    "profile_actionBackground":        "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE)",
    "avatar_backgroundInProfileBlue":  "ma ? (d ? AmberTokens.MARIO_DAY_SURFACE : AmberTokens.MARIO_NIGHT_SURFACE)",
    # سوییچ‌ها
    "switch2Track":          "ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE)",
    "switchTrack":           "ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE)",
    "switchTrackBlue":       "ma ? (d ? 0xFFD5E1F4 : AmberTokens.MARIO_NIGHT_OUTLINE)",
    "switchTrackBlueThumb":  "ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT_DIM)",
    # جدول/کد داخل حباب‌ها
    "chat_inTableBackground":          "ma ? (d ? 0xFFEFF5FF : 0xFF1A2344)",
    "chat_inCodeBackground":           "ma ? (d ? 0xFFE7F0FF : 0xFF161E3E)",
    "chat_inArticleCodeBackground":    "ma ? (d ? 0xFFE7F0FF : 0xFF161E3E)",
    "chat_outFileBackground":          "ma ? (d ? 0xFFF2C94C : 0xFF2E7D32)",
    "chat_outContactBackground":       "ma ? (d ? 0xFFF2C94C : 0xFF2E7D32)",
    "chat_outTableBackground":         "ma ? (d ? 0xFFF7D45E : 0xFF2E7D32)",
    "chat_outCodeBackground":          "ma ? (d ? 0xFFEFC63E : 0xFF29702C)",
    "chat_outArticleCodeBackground":   "ma ? (d ? 0xFFEFC63E : 0xFF29702C)",
    "chat_outPollCorrectAnswer":       "ma ? (d ? 0xFF27702F : 0xFF5FCE6A)",
    # سرویس/دکمهٔ بات/پنل‌ها
    "chat_serviceText":                "ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT)",
    "chat_serviceIcon":                "ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT)",
    "chat_fieldOverlayText":           "ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT)",
    "chat_botButtonText":              "ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT)",
    "chat_serviceLink":                "ma ? (d ? 0xFFFFE9A8 : 0xFFFFF3B8)",
    "chat_stickersHintPanel":          "ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE)",
    "chat_emojiPanelBackground":       "ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE)",
    "chat_emojiPanelStickerPackSelector": "ma ? (d ? 0xFFEFF5FF : AmberTokens.MARIO_NIGHT_SURFACE)",
    # دکمه‌های ضمیمه — سرزمین ماریو: صدا = قرمز قارچ، مخاطب = طلای سکه
    "chat_attachAudioBackground":      "ma ? (d ? 0xFFC6281C : 0xFFE85B50)",
    "chat_attachContactBackground":    "ma ? (d ? 0xFFB3651F : 0xFFE8B23A)",
    # شیشهٔ ناوبری اصلی — آسمان/بریکی
    "glass_targetMainTabs":            "ma ? (d ? 0xE6F2F7FF : 0xE6111731)",
    "glass_targetMainTopPanel":        "ma ? (d ? 0xE6E7F0FF : 0xE60D1226)",
    "chat_recordedVoiceBackground":    "ma ? (d ? AmberTokens.MARIO_DAY_HEADER : AmberTokens.MARIO_NIGHT_HEADER_BORDER)",
    "chat_messagePanelShadow":         "ma ? (d ? AmberTokens.MARIO_DAY_TEXT : 0xFF000000)",
}

# آواتارها — جفت‌های سرزمین ماریو (روز، شب)
AVATAR_MAP = {
    "avatar_backgroundBlue":         ("0xFF6FA8FF", "0xFF4066D8"),
    "avatar_background2Blue":        ("0xFF2E5BC4", "0xFF2547A0"),
    "avatar_backgroundCyan":         ("0xFF7FD9E8", "0xFF2FA0B8"),
    "avatar_background2Cyan":        ("0xFF1782A0", "0xFF126E88"),
    "avatar_backgroundGreen":        ("0xFF5FCE6A", "0xFF2E9E3E"),
    "avatar_background2Green":       ("0xFF27702F", "0xFF1D5A28"),
    "avatar_backgroundOrange":       ("0xFFFFA94D", "0xFFE86A1C"),
    "avatar_background2Orange":      ("0xFFC25414", "0xFFA04310"),
    "avatar_backgroundPink":         ("0xFFFFB4C4", "0xFFE87D94"),
    "avatar_background2Pink":        ("0xFFC25068", "0xFFA03C54"),
    "avatar_backgroundRed":          ("0xFFE85B50", "0xFFC63026"),
    "avatar_background2Red":         ("0xFF9E241C", "0xFF7E1C16"),
    "avatar_backgroundViolet":       ("0xFFA077E8", "0xFF6E48C2"),
    "avatar_background2Violet":      ("0xFF5C3494", "0xFF452473"),
    "avatar_backgroundSaved":        ("0xFFE8B23A", "0xFFC28C1E"),
    "avatar_background2Saved":       ("0xFF8C6414", "0xFF6E4E10"),
    "avatar_nameInMessageBlue":      ("0xFF2E5BC4", "0xFF7FB3FF"),
    "avatar_nameInMessageCyan":      ("0xFF1782A0", "0xFF7FD9E8"),
    "avatar_nameInMessageGreen":     ("0xFF27702F", "0xFF5FCE6A"),
    "avatar_nameInMessageOrange":    ("0xFFC25414", "0xFFFFA94D"),
    "avatar_nameInMessagePink":      ("0xFFC25068", "0xFFFFB4C4"),
    "avatar_nameInMessageRed":       ("0xFF9E241C", "0xFFE85B50"),
    "avatar_nameInMessageViolet":    ("0xFF5C3494", "0xFFA077E8"),
    "avatar_backgroundArchived":     ("0xFF8C9AB8", "0xFF4A5878"),
    "avatar_backgroundArchivedHidden": ("0xFFDCE4F2", "0xFF253260"),
    "avatar_text":                   None,  # ثابت — ma ? 0xFFFFFFFF
}

# اکسنت‌های مکمل — مپ کلید → جفت سرزمین ماریو
# اکسنت اصلی (قرمز ماریو روز / طلای سکه شب) / متن روی اکسنت / طلای عمیق /
# لولهٔ سبز / آسمان NES / قارچ / وارپ بنفش / گل آتش / کاغذ آسمان
M_ACCENT   = ("0xFFC6281C", "0xFFFBD000")
M_ACC_TXT  = ("0xFFA82014", "0xFFFFDF60")
M_ACC_SOFT = ("0xFFB3651F", "0xFFE8B23A")
M_GREEN    = ("0xFF27702F", "0xFF5FCE6A")
M_BLUE     = ("0xFF2E5BC4", "0xFF5C94FC")
M_RED      = ("0xFFA82014", "0xFFFF6B5E")
M_PURPLE   = ("0xFF5C3494", "0xFFA077E8")
M_FIRE     = ("0xFFC25414", "0xFFFF8A3C")
M_PAPER    = ("0xFFE7F0FF", "0xFF141B3C")
M_PAPER2   = ("0xFFEFF5FF", "0xFF1A2344")
M_PAPER3   = ("0xFFE3EEFF", "0xFF161E3E")
SUPPLEMENT = {
    "avatar_actionBarSelectorGreen": ("0xFFDCE4F2", "0xFF20305C"),
    "botKeyboard_button_primary": M_ACCENT,
    "buttonNeutralText": M_ACC_TXT,
    "changephoneinfo_image2": M_ACCENT,
    "chat_emojiPanelBadgeBackground": M_ACCENT,
    "chats_tabUnreadActiveBackground": M_ACCENT,
    "color_blue": M_BLUE,
    "color_lightblue": M_PURPLE,
    "color_orange": M_FIRE,
    "color_yellow": M_ACCENT,
    "contacts_inviteBackground": M_ACCENT,
    "contextProgressInner2": M_PAPER,
    "contextProgressInner3": M_ACC_SOFT,
    "contextProgressInner4": M_ACCENT,
    "contextProgressOuter1": M_ACCENT,
    "fastScrollActive": M_ACCENT,
    "featuredStickers_addButton2": M_ACC_SOFT,
    "featuredStickers_addedIcon": M_ACCENT,
    "featuredStickers_buttonProgress": M_ACC_TXT,
    "featuredStickers_unread": M_ACCENT,
    "files_folderIconBackground": M_GREEN,
    "fill_RedDark": ("0xFFB4271C", "0xFFCC4A3A"),
    "gift_ribbon": ("0xFFDCE4F2", "0xFF20305C"),
    "inappPlayerPlayPause": M_ACCENT,
    "key_player_progressCachedBackground": ("0xFFD5E1F4", "0xFF253260"),
    "location_actionBackground": M_ACCENT,
    "location_liveLocationProgress": M_ACC_SOFT,
    "location_placeLocationBackground": M_ACC_SOFT,
    "location_sendLiveLocationBackground": M_GREEN,
    "location_sendLiveLocationText": M_GREEN,
    "location_sendLocationBackground": M_ACCENT,
    "location_sendLocationIcon": M_ACCENT,
    "location_sendLocationText": M_ACCENT,
    "login_progressInner": M_ACCENT,
    "passport_authorizeBackground": M_ACCENT,
    "passport_authorizeBackgroundSelected": M_ACCENT,
    "passport_authorizeText": M_ACC_TXT,
    "picker_badge": M_ACCENT,
    "picker_enabledButton": M_ACCENT,
    "player_buttonActive": M_ACCENT,
    "player_progress": M_ACCENT,
    "pollCreateIcons": M_ACC_TXT,
    "premiumCoinGradient1": ("0xFFB3651F", "0xFF6E4A04"),
    "premiumCoinGradient2": M_ACCENT,
    "premiumGradient0": ("0xFF3A0E0A", "0xFF0A0F1E"),
    "premiumGradient1": ("0xFF4E1410", "0xFF0D1528"),
    "premiumGradient2": ("0xFF8C1A12", "0xFF14204A"),
    "premiumGradient3": ("0xFFB42018", "0xFF1A2A5E"),
    "premiumGradient4": ("0xFFE52521", "0xFFFBD000"),
    "premiumGradientBottomSheet1": ("0xFF4E1410", "0xFF0D1528"),
    "premiumGradientBottomSheet2": ("0xFF8C1A12", "0xFF14204A"),
    "premiumGradientBottomSheet3": ("0xFFE52521", "0xFFFBD000"),
    "premiumStarGradient1": ("0xFFE52521", "0xFFFBD000"),
    "premiumStartSmallStarsColor": ("0x71E52521", "0x71FBD000"),
    "progressCircle": M_ACCENT,
    "reactionStarSelector": M_ACCENT,
    "returnToCallBackground": M_ACC_SOFT,
    "sessions_devicesImage": M_PAPER,
    "sharedMedia_startStopLoadIcon": ("0xFFB3651F", "0xFFFBD000"),
    "statisticChartActivePickerChart": ("0xD8E3EEFF", "0xD820305C"),
    "statisticChartBackZoomColor": M_ACCENT,
    "statisticChartLine_blue": M_BLUE,
    "statisticChartLine_golden": M_ACCENT,
    "statisticChartLine_lightblue": M_PURPLE,
    "statisticChartLine_orange": M_FIRE,
    "statisticChartRipple": ("0x2CC6281C", "0x2CFBD000"),
    "stickers_menu": ("0xFFDCE4F2", "0xFF20305C"),
    "telegram_color": M_ACCENT,
    "telegram_color_text": M_ACC_TXT,
    "undo_cancelColor": M_ACC_TXT,
    "voipgroup_checkMenu": M_ACC_TXT,
    "voipgroup_connectingProgress": M_ACCENT,
    "voipgroup_listeningText": M_ACC_TXT,
    "voipgroup_muteButton": M_ACCENT,
    "voipgroup_muteButton2": M_ACC_SOFT,
    "voipgroup_muteButton3": M_ACC_SOFT,
    "voipgroup_overlayBlue1": M_PAPER,
    "voipgroup_overlayBlue2": M_PAPER2,
    "voipgroup_overlayGreen1": M_PAPER2,
    "voipgroup_overlayGreen2": M_PAPER,
    "voipgroup_rtmpButton": M_ACCENT,
    "voipgroup_soundButtonActive": M_ACCENT,
    "voipgroup_soundButtonActive2": M_ACC_SOFT,
    "voipgroup_soundButtonActive2Scrolled": M_ACC_SOFT,
    "voipgroup_soundButtonActiveScrolled": M_ACCENT,
    "voipgroup_speakingText": M_ACC_TXT,
    "voipgroup_topPanelBlue1": M_PAPER,
    "voipgroup_topPanelBlue2": M_PAPER2,
    "voipgroup_topPanelGray": ("0xFFDCE4F2", "0xFF253260"),
    "voipgroup_topPanelGreen1": M_PAPER2,
    "voipgroup_topPanelGreen2": M_PAPER,
    "voipgroup_unmuteButton": M_ACCENT,
    "voipgroup_unmuteButton2": M_ACC_SOFT,
    "voipgroup_windowBackgroundWhiteInputFieldActivated": M_ACCENT,
    "wallet_out_commentBorder": ("0xFFD5E1F4", "0xFF253260"),
}
FULL_MAP = {}
FULL_MAP.update({k: (f"ma ? (d ? {v[0]} : {v[1]})" if v else "ma ? 0xFFFFFFFF") for k, v in AVATAR_MAP.items()})
FULL_MAP.update({k: f"ma ? (d ? {v[0]} : {v[1]})" for k, v in SUPPLEMENT.items()})
FULL_MAP.update(MARIO)

def split_top(s):
    """شکستن در « : »های هم‌سطح (ردیابی عمق پرانتز) — مثل translate_ternaries مولد"""
    parts, depth, cur, i = [], 0, [], 0
    while i < len(s):
        c = s[i]
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        if depth == 0 and s[i:i+3] == " : ":
            parts.append("".join(cur))
            cur = []
            i += 3
            continue
        cur.append(c)
        i += 1
    parts.append("".join(cur))
    return parts

hits = {}
out_lines = []
for ln in src.split("\n"):
    s = ln
    mput = re.match(r'^(\s*)m\.put\("([a-zA-Z_0-9]+)", (.*)\);\s*$', ln)
    mloc = re.match(r'^(\s*)final int (\w+) = (.*);\s*$', ln)
    key = None
    expr = None
    prefix = None
    ending = None
    if mput and mput.group(2) in FULL_MAP and "au ?" in mput.group(3):
        key, expr, prefix, ending = mput.group(2), mput.group(3), mput.group(1) + f'm.put("{mput.group(2)}", ', ");"
    elif mloc and mloc.group(2) in FULL_MAP and "au ?" in mloc.group(3):
        key, expr, prefix, ending = mloc.group(2), mloc.group(3), mloc.group(1) + f"final int {mloc.group(2)} = ", ";"
    if key:
        segs = split_top(expr)
        if len(segs) == 3 and segs[0].startswith("au ?") and segs[1].startswith("pr ?") and "ma ?" not in expr:
            au_branch = segs[0][len("au ?"):].strip()
            pr_branch = segs[1][len("pr ?"):].strip()
            tail = segs[2].strip()
            s = f"{prefix}au ? {au_branch} : pr ? {pr_branch} : {FULL_MAP[key]} : {tail}{ending}"
            hits[key] = hits.get(key, 0) + 1
    out_lines.append(s)
src = "\n".join(out_lines)

missing = [k for k in FULL_MAP if k not in hits]
dupes = [k for k, v in hits.items() if v > 1]
if missing:
    sys.exit(f"FATAL: keys not found/transformed ({len(missing)}): {sorted(missing)[:12]}")
if dupes:
    sys.exit(f"FATAL: keys transformed more than once: {sorted(dupes)[:12]}")

# ── ۴) جدول صریح — لوکال‌ها و خطوط تو در تو (زنجیره داخل alpha/over) ──────────
EXPLICIT.append((
    "final int svcBg = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_SURFACE), d ? 0.65f : 0.70f);",
    "final int svcBg = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.MARIO_NIGHT_SURFACE) : (d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_SURFACE), d ? 0.65f : 0.70f);"
))
EXPLICIT.append((
    "final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.over(AmberTokens.PREMIERE_NIGHT_TEXT, AmberTokens.PREMIERE_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);",
    "final int svcBgSel = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : AmberTokens.over(AmberTokens.AURORA_NIGHT_TEXT, AmberTokens.AURORA_NIGHT_SURFACE, 0.12f)) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : AmberTokens.over(AmberTokens.PREMIERE_NIGHT_TEXT, AmberTokens.PREMIERE_NIGHT_SURFACE, 0.12f)) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : AmberTokens.over(AmberTokens.MARIO_NIGHT_TEXT, AmberTokens.MARIO_NIGHT_SURFACE, 0.12f)) : (d ? AmberTokens.DAY_TEXT : AmberTokens.over(AmberTokens.NIGHT_TEXT, AmberTokens.NIGHT_SURFACE, 0.12f)), d ? 0.78f : 0.72f);"
))
EXPLICIT.append((
    "final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);",
    "final int svcSel = AmberTokens.alpha(au ? (d ? 0xFFFFFFFF : AmberTokens.AURORA_NIGHT_TEXT) : pr ? (d ? 0xFFFFFFFF : AmberTokens.PREMIERE_NIGHT_TEXT) : ma ? (d ? 0xFFFFFFFF : AmberTokens.MARIO_NIGHT_TEXT) : (d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT), 0.14f);"
))
EXPLICIT.append((
    "final int goDown = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_SURFACE) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE), d ? 0.90f : 0.80f);",
    "final int goDown = AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_SURFACE) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_SURFACE) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_SURFACE) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE), d ? 0.90f : 0.80f);"
))
EXPLICIT.append((
    'm.put("chat_compact_backgroundGradient", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000), 0.03f));',
    'm.put("chat_compact_backgroundGradient", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_TEXT : 0xFF000000) : pr ? (d ? AmberTokens.PREMIERE_DAY_TEXT : 0xFF000000) : ma ? (d ? AmberTokens.MARIO_DAY_TEXT : 0xFF000000) : (d ? AmberTokens.DAY_TEXT : 0xFF000000), 0.03f));'
))
EXPLICIT.append((
    'm.put("chat_compact_outBackground", AmberTokens.over(outBubble, au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), d ? 0.85f : 0.55f));',
    'm.put("chat_compact_outBackground", AmberTokens.over(outBubble, au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), d ? 0.85f : 0.55f));'
))
EXPLICIT.append((
    'm.put("chat_compact_fadeMiddle", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), 0.64f));',
    'm.put("chat_compact_fadeMiddle", AmberTokens.alpha(au ? (d ? AmberTokens.AURORA_DAY_WALLPAPER_TOP : AmberTokens.AURORA_NIGHT_WALLPAPER_MID) : pr ? (d ? AmberTokens.PREMIERE_DAY_WALLPAPER_TOP : AmberTokens.PREMIERE_NIGHT_WALLPAPER_MID) : ma ? (d ? AmberTokens.MARIO_DAY_WALLPAPER_TOP : AmberTokens.MARIO_NIGHT_WALLPAPER_MID) : (d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID), 0.64f));'
))

# ── اجرا ────────────────────────────────────────────────────────────────────
for old, new in EXPLICIT:
    n = src.count(old)
    if n != 1:
        sys.exit(f"FATAL: expected 1 occurrence, found {n} for:\n---\n{old[:150]}\n---")
    src = src.replace(old, new)

# در نهایت: هیچ زنجیرهٔ au/pr نباید بدون شاخهٔ ma بماند
leftover = [ln for ln in src.split("\n") if "pr ?" in ln and "ma ?" not in ln]
if leftover:
    sys.exit(f"FATAL: {len(leftover)} leftover lines without ma branch:\n" + "\n".join(leftover[:6]))

open(PATH, "w", encoding="utf-8").write(src)
print(f"OK: mechanical wraps = {mech_count}, engine keys = {len(hits)}, explicit = {len(EXPLICIT)}")

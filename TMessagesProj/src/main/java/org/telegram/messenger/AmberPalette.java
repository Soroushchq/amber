package org.telegram.messenger;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * AmberGram UI 2.0 — موتور پالت (مصرف‌کننده AmberTokens).
 *
 * هر کلید به‌صورت ternary روز/شب از توکن‌ها + مشتق‌های alpha/over ساخته می‌شود.
 * نام کلیدها از ThemeColors.createColorKeysMap واقعی استخراج و اعتبارسنجی شده‌اند
 * (۸۶۲ نام معتبر؛ شامل قراردادهای عجیب مثل chat_wallpaper_gradient_to).
 *
 * مصرف: مولد Tools/generate_amber_theme2.py این فایل را واقعاً تفسیر و ارزیابی
 * می‌کند (بدون تکرار رنگ) و فایل‌های attheme را می‌سازد.
 */
public final class AmberPalette {

    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;

    private AmberPalette() {}

    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_NIGHT) {
            if (nightCache == null) {
                nightCache = build(false);
            }
            return nightCache;
        }
        if (dayCache == null) {
            dayCache = build(true);
        }
        return dayCache;
    }

    /** نام نامعتبر = 0 */
    public static int valueOf(String keyName, int mode) {
        Integer v = palette(mode).get(keyName);
        return v == null ? 0 : v;
    }

    /** خروجی فایل attheme مرتب الفبایی — برای مولد قدم ۳/۴ */
    public static String atthemeText(int mode) {
        Map<String, Integer> m = palette(mode);
        ArrayList<String> keys = new ArrayList<>(m.keySet());
        Collections.sort(keys);
        StringBuilder sb = new StringBuilder();
        for (String k : keys) {
            sb.append(k).append('=').append(m.get(k)).append('\n');
        }
        return sb.toString();
    }

    private static Map<String, Integer> build(boolean d) {
        HashMap<String, Integer> m = new HashMap<>();

        // ── اتم‌ها ───────────────────────────────────────────────────────────
        final int text = d ? AmberTokens.DAY_TEXT : AmberTokens.NIGHT_TEXT;
        final int dim = d ? AmberTokens.DAY_TEXT_DIM : AmberTokens.NIGHT_TEXT_DIM;
        final int time = d ? AmberTokens.DAY_TIME : AmberTokens.NIGHT_TIME;
        final int accent = d ? AmberTokens.DAY_ACCENT : AmberTokens.NIGHT_ACCENT;
        final int accentBright = d ? AmberTokens.DAY_ACCENT_BRIGHT : AmberTokens.NIGHT_ACCENT_BRIGHT;
        final int onAccent = d ? AmberTokens.DAY_ON_ACCENT : AmberTokens.NIGHT_ON_ACCENT;
        final int bg = d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_BG;
        final int white = d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_TOP;
        final int header = d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_HEADER;
        final int headerBorder = d ? AmberTokens.DAY_HEADER_BORDER : AmberTokens.NIGHT_HEADER_BORDER;
        final int surface = d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_SURFACE;
        final int outline = d ? AmberTokens.DAY_OUTLINE : AmberTokens.NIGHT_OUTLINE;
        final int inBubble = d ? AmberTokens.DAY_IN_BUBBLE : AmberTokens.NIGHT_IN_BUBBLE;
        final int inText = d ? AmberTokens.DAY_IN_TEXT : AmberTokens.NIGHT_IN_TEXT;
        final int outBubble = d ? AmberTokens.DAY_OUT_BUBBLE : AmberTokens.NIGHT_OUT_BUBBLE;
        final int outText = d ? AmberTokens.DAY_OUT_TEXT : AmberTokens.NIGHT_OUT_TEXT;
        final int badgeBg = d ? AmberTokens.DAY_BADGE_BG : AmberTokens.NIGHT_BADGE_BG;
        final int badgeText = d ? AmberTokens.DAY_BADGE_TEXT : AmberTokens.NIGHT_BADGE_TEXT;
        final int fieldBg = d ? AmberTokens.DAY_FIELD_BG : AmberTokens.NIGHT_FIELD_BG;
        final int fieldBorder = d ? AmberTokens.DAY_FIELD_BORDER : AmberTokens.NIGHT_FIELD_BORDER;

        // ── مشتق‌ها ──────────────────────────────────────────────────────────
        final int sel = AmberTokens.alpha(text, d ? 0.06f : 0.08f);
        final int selIn = AmberTokens.over(accent, inBubble, d ? 0.14f : 0.16f);
        final int selOut = AmberTokens.over(accent, outBubble, d ? 0.14f : 0.16f);
        final int divider = d ? AmberTokens.DAY_OUTLINE : AmberTokens.alpha(AmberTokens.NIGHT_OUTLINE, 0.55f);
        final int svcBg = AmberTokens.alpha(d ? AmberTokens.DAY_TEXT_DIM : AmberTokens.NIGHT_SURFACE, 0.70f);
        final int goDown = AmberTokens.alpha(d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_SURFACE, d ? 0.90f : 0.80f);
        final int deepFile = d ? 0xFFF7E3C8 : 0xFF2E2618;
        final int outDim = AmberTokens.alpha(outText, 0.65f);
        final int outTime = d ? 0xFFA8701E : 0xFFD9BC7A;
        final int red = d ? 0xFFB4382C : 0xFFFF6E54;
        final int green = d ? 0xFF3D7A2B : 0xFF7DBE72;

        // ── پنجره‌ها و سطوح عمومی ────────────────────────────────────────────
        m.put("windowBackgroundWhite", white);
        m.put("windowBackgroundWhiteBlackText", text);
        m.put("windowBackgroundWhiteGrayText", dim);
        m.put("windowBackgroundWhiteGrayIcon", dim);
        m.put("windowBackgroundWhiteHintText", time);
        m.put("windowBackgroundWhiteValueText", accent);
        m.put("windowBackgroundWhiteLinkText", accent);
        m.put("windowBackgroundWhiteLinkSelection", AmberTokens.alpha(accent, 0.25f));
        m.put("windowBackgroundWhiteBlueText", accent);
        m.put("windowBackgroundWhiteBlueText2", accent);
        m.put("windowBackgroundWhiteBlueText3", accent);
        m.put("windowBackgroundWhiteBlueText4", accent);
        m.put("windowBackgroundWhiteBlueText5", accent);
        m.put("windowBackgroundWhiteBlueText6", accent);
        m.put("windowBackgroundWhiteBlueText7", accent);
        m.put("windowBackgroundWhiteBlueButton", accent);
        m.put("windowBackgroundWhiteBlueHeader", accent);
        m.put("windowBackgroundWhiteBlueIcon", accent);
        m.put("windowBackgroundWhiteGreenText", green);
        m.put("windowBackgroundWhiteGreenText2", green);
        m.put("windowBackgroundWhiteInputField", fieldBorder);
        m.put("windowBackgroundWhiteInputFieldActivated", accent);
        m.put("windowBackgroundGray", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG);
        m.put("windowBackgroundGrayShadow", d ? 0x14211A12 : 0x28000000);
        m.put("windowBackgroundChecked", accent);
        m.put("windowBackgroundUnchecked", outline);
        m.put("windowBackgroundCheckText", text);
        m.put("divider", divider);

        // ── اکشن‌بار ─────────────────────────────────────────────────────────
        m.put("actionBarDefault", header);
        m.put("actionBarDefaultIcon", text);
        m.put("actionBarDefaultTitle", text);
        m.put("actionBarDefaultSubtitle", dim);
        m.put("actionBarDefaultSelector", AmberTokens.alpha(text, d ? 0.08f : 0.10f));
        m.put("actionBarDefaultSearch", fieldBg);
        m.put("actionBarDefaultSearchPlaceholder", dim);
        m.put("actionBarDefaultSearchArchivedPlaceholder", dim);
        m.put("actionBarDefaultArchived", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP);
        m.put("actionBarDefaultArchivedIcon", text);
        m.put("actionBarDefaultArchivedTitle", text);
        m.put("actionBarDefaultArchivedSelector", AmberTokens.alpha(text, 0.08f));
        m.put("actionBarDefaultSubmenuBackground", d ? 0xFFFFFFFF : AmberTokens.NIGHT_SURFACE);
        m.put("actionBarDefaultSubmenuItem", text);
        m.put("actionBarDefaultSubmenuItemIcon", dim);
        m.put("actionBarDefaultSubmenuSeparator", divider);
        m.put("actionBarTabActiveText", accent);
        m.put("actionBarTabUnactiveText", dim);
        m.put("actionBarTabLine", accent);
        m.put("actionBarTabSelector", AmberTokens.alpha(accent, 0.10f));
        m.put("actionBarWhiteSelector", AmberTokens.alpha(accent, 0.12f));
        m.put("actionBarBrowser", bg);
        m.put("actionBarActionModeDefault", outBubble);
        m.put("actionBarActionModeDefaultIcon", outText);
        m.put("actionBarActionModeDefaultTop", outBubble);
        m.put("actionBarActionModeDefaultSelector", AmberTokens.alpha(outText, 0.10f));
        m.put("actionBarActionModeReaction", AmberTokens.alpha(outText, 0.12f));
        m.put("actionBarActionModeReactionText", outText);
        m.put("actionBarActionModeReactionDot", accent);

        // ── لیست چت ──────────────────────────────────────────────────────────
        m.put("chats_name", text);
        m.put("chats_nameMessage", dim);
        m.put("chats_nameMessage_threeLines", dim);
        m.put("chats_message", dim);
        m.put("chats_message_threeLines", dim);
        m.put("chats_nameArchived", dim);
        m.put("chats_messageArchived", dim);
        m.put("chats_nameMessageArchived", dim);
        m.put("chats_nameMessageArchived_threeLines", dim);
        m.put("chats_date", time);
        m.put("chats_date_bold", time);
        m.put("chats_muteIcon", dim);
        m.put("chats_attachMessage", dim);
        m.put("chats_secretName", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chats_secretIcon", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chats_verifiedBackground", accent);
        m.put("chats_verifiedCheck", onAccent);
        m.put("chats_onlineCircle", d ? 0xFF3E9C4B : 0xFF63C26B);
        m.put("chats_actionBackground", deepFile);
        m.put("chats_actionIcon", accent);
        m.put("chats_actionMessage", dim);
        m.put("chats_actionPressedBackground", AmberTokens.alpha(text, 0.08f));
        m.put("chats_archiveBackground", surface);
        m.put("chats_archiveIcon", dim);
        m.put("chats_archiveText", dim);
        m.put("chats_archivePinBackground", headerBorder);
        m.put("chats_archivePullDownBackground", headerBorder);
        m.put("chats_archivePullDownBackgroundActive", accent);
        m.put("chats_unreadCounter", badgeBg);
        m.put("chats_unreadCounterText", badgeText);
        m.put("chats_unreadCounterMuted", surface);
        m.put("chats_pinnedIcon", dim);
        m.put("chats_pinnedOverlay", AmberTokens.alpha(accent, 0.08f));
        m.put("chats_sentCheck", accent);
        m.put("chats_sentReadCheck", accentBright);
        m.put("chats_sentClock", dim);
        m.put("chats_sentError", red);
        m.put("chats_sentErrorIcon", red);
        m.put("chats_draft", accent);
        m.put("chats_mentionIcon", accent);
        m.put("chats_menuBackground", bg);
        m.put("chats_menuTopBackground", header);
        m.put("chats_menuTopBackgroundCats", header);
        m.put("chats_menuName", text);
        m.put("chats_menuPhone", dim);
        m.put("chats_menuPhoneCats", dim);
        m.put("chats_menuItemIcon", dim);
        m.put("chats_menuItemText", text);
        m.put("chats_menuItemCheck", accent);
        m.put("chats_menuTopShadow", 0x00000000);
        m.put("chats_menuTopShadowCats", 0x00000000);
        m.put("chats_tabletSelectedOverlay", sel);

        // ── صفحه چت: بوم و حباب‌ها ──────────────────────────────────────────
        // وایپرپ گرادیانی متحرک (MotionBackgroundDrawable): پایه + سه توقف؛
        // نام‌های عجیب chat_wallpaper_gradient_to / key_..._to2/to3 عمداً
        // همان قرارداد ThemeColors.createColorKeysMap تلگرام است.
        m.put("chat_wallpaper", d ? AmberTokens.DAY_WALLPAPER_TOP : AmberTokens.NIGHT_WALLPAPER_MID);
        m.put("chat_wallpaper_gradient_to", d ? AmberTokens.DAY_WALLPAPER_BOTTOM : AmberTokens.NIGHT_WALLPAPER_TOP);
        m.put("key_chat_wallpaper_gradient_to2", d ? AmberTokens.DAY_BG : AmberTokens.NIGHT_WALLPAPER_BOTTOM);
        m.put("key_chat_wallpaper_gradient_to3", d ? AmberTokens.DAY_HEADER : AmberTokens.NIGHT_SURFACE);
        m.put("chat_inBubble", inBubble);
        m.put("chat_inBubbleSelected", selIn);
        m.put("chat_inBubbleSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_inBubbleShadow", 0x00000000);
        m.put("chat_inBubbleLocationPlaceholder", outline);
        m.put("chat_outBubble", outBubble);
        m.put("chat_outBubbleGradient", outBubble);
        m.put("chat_outBubbleGradient2", outBubble);
        m.put("chat_outBubbleGradient3", outBubble);
        m.put("chat_outBubbleGradientAnimated", 0);
        m.put("chat_outBubbleSelected", selOut);
        m.put("chat_outBubbleSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_outBubbleGradientSelectedOverlay", AmberTokens.alpha(0xFF000000, d ? 0.06f : 0.10f));
        m.put("chat_outBubbleShadow", 0x00000000);
        m.put("chat_outBubbleLocationPlaceholder", headerBorder);

        // ── متن حباب ورودی ──────────────────────────────────────────────────
        m.put("chat_messageTextIn", inText);
        m.put("chat_inTimeText", time);
        m.put("chat_inTimeSelectedText", dim);
        m.put("chat_inInstant", accent);
        m.put("chat_inInstantSelected", accent);
        m.put("chat_inReplyLine", accent);
        m.put("chat_inReplyNameText", accent);
        m.put("chat_inReplyMessageText", inText);
        m.put("chat_inReplyMediaMessageText", inText);
        m.put("chat_inReplyMediaMessageSelectedText", inText);
        m.put("chat_inForwardedNameText", accent);
        m.put("chat_inViaBotNameText", accent);
        m.put("chat_inSiteNameText", accent);
        m.put("chat_inPsaNameText", accent);
        m.put("chat_inPreviewLine", outline);
        m.put("chat_inPreviewInstantText", accent);
        m.put("chat_inLoader", accent);
        m.put("chat_inLoaderSelected", accent);
        m.put("chat_inLoaderPhoto", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_inMediaIcon", dim);
        m.put("chat_inMediaIconSelected", dim);
        m.put("chat_inMenu", dim);
        m.put("chat_inMenuSelected", dim);
        m.put("chat_inFileNameText", accent);
        m.put("chat_inFileInfoText", dim);
        m.put("chat_inFileInfoSelectedText", dim);
        m.put("chat_inFileProgress", accent);
        m.put("chat_inFileProgressSelected", accent);
        m.put("chat_inFileBackground", deepFile);
        m.put("chat_inFileBackgroundSelected", AmberTokens.over(accent, deepFile, d ? 0.10f : 0.12f));
        m.put("chat_inAudioTitleText", inText);
        m.put("chat_inAudioPerfomerText", accent);
        m.put("chat_inAudioPerfomerSelectedText", accent);
        m.put("chat_inAudioDurationText", dim);
        m.put("chat_inAudioDurationSelectedText", dim);
        m.put("chat_inAudioProgress", accent);
        m.put("chat_inAudioSelectedProgress", accent);
        m.put("chat_inAudioSeekbar", outline);
        m.put("chat_inAudioSeekbarFill", accent);
        m.put("chat_inAudioSeekbarSelected", accent);
        m.put("chat_inAudioCacheSeekbar", AmberTokens.alpha(inText, 0.12f));
        m.put("chat_inVoiceSeekbar", outline);
        m.put("chat_inVoiceSeekbarFill", accent);
        m.put("chat_inVoiceSeekbarSelected", accent);
        m.put("chat_inVenueInfoText", inText);
        m.put("chat_inVenueInfoSelectedText", inText);
        m.put("chat_inContactBackground", deepFile);
        m.put("chat_inContactNameText", inText);
        m.put("chat_inContactPhoneText", dim);
        m.put("chat_inContactPhoneSelectedText", dim);
        m.put("chat_inContactIcon", accent);
        m.put("chat_inLocationBackground", deepFile);
        m.put("chat_inLocationIcon", accent);
        m.put("chat_inTableBackground", d ? 0xFFFFFDF8 : 0xFF2E2618);
        m.put("chat_inTableBorder", outline);
        m.put("chat_inCodeBackground", d ? 0xFFF7EFE4 : 0xFF211B12);
        m.put("chat_inArticleCodeBackground", d ? 0xFFF7EFE4 : 0xFF211B12);
        m.put("chat_inArticleCodeScrollbar", AmberTokens.alpha(text, 0.25f));
        m.put("chat_inArticleCodeScrollbarBackground", outline);
        m.put("chat_inArticleDetailsArrow", dim);
        m.put("chat_inArticleDetailsLine", outline);
        m.put("chat_inPollCorrectAnswer", green);
        m.put("chat_inPollWrongAnswer", red);
        m.put("chat_inReactionButtonBackground", AmberTokens.alpha(accent, d ? 0.10f : 0.12f));
        m.put("chat_inReactionButtonText", accent);
        m.put("chat_inReactionButtonTextSelected", accent);
        m.put("chat_inQuote", AmberTokens.alpha(inText, d ? 0.10f : 0.12f));
        m.put("chat_inViews", dim);
        m.put("chat_inViewsSelected", dim);
        m.put("chat_inSentClock", dim);
        m.put("chat_inSentClockSelected", dim);
        m.put("chat_inTextSelectionHighlight", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_inDownCall", accent);
        m.put("chat_inDivider", outline);

        // ── متن حباب خروجی ──────────────────────────────────────────────────
        m.put("chat_messageTextOut", outText);
        m.put("chat_outTimeText", outTime);
        m.put("chat_outTimeSelectedText", outText);
        m.put("chat_outInstant", accent);
        m.put("chat_outInstantSelected", accent);
        m.put("chat_outReplyLine", accent);
        m.put("chat_outReplyLine2", accent);
        m.put("chat_outReplyNameText", accent);
        m.put("chat_outReplyMessageText", outText);
        m.put("chat_outReplyMediaMessageText", outText);
        m.put("chat_outReplyMediaMessageSelectedText", outText);
        m.put("chat_outForwardedNameText", accent);
        m.put("chat_outViaBotNameText", accent);
        m.put("chat_outSiteNameText", accent);
        m.put("chat_outPsaNameText", accent);
        m.put("chat_outPreviewLine", AmberTokens.alpha(outText, 0.40f));
        m.put("chat_outPreviewInstantText", accent);
        m.put("chat_outLoader", accent);
        m.put("chat_outLoaderSelected", accent);
        m.put("chat_outMediaIcon", outTime);
        m.put("chat_outMediaIconSelected", outTime);
        m.put("chat_outMenu", outTime);
        m.put("chat_outMenuSelected", outTime);
        m.put("chat_outFileNameText", accent);
        m.put("chat_outFileInfoText", outDim);
        m.put("chat_outFileInfoSelectedText", outDim);
        m.put("chat_outFileProgress", accent);
        m.put("chat_outFileProgressSelected", accent);
        m.put("chat_outFileBackground", d ? 0xFFFBCE8F : 0xFF6E5200);
        m.put("chat_outFileBackgroundSelected", AmberTokens.over(accent, outBubble, d ? 0.08f : 0.10f));
        m.put("chat_outAudioTitleText", outText);
        m.put("chat_outAudioPerfomerText", accent);
        m.put("chat_outAudioPerfomerSelectedText", accent);
        m.put("chat_outAudioDurationText", outDim);
        m.put("chat_outAudioDurationSelectedText", outDim);
        m.put("chat_outAudioProgress", accent);
        m.put("chat_outAudioSelectedProgress", accent);
        m.put("chat_outAudioSeekbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outAudioSeekbarFill", accent);
        m.put("chat_outAudioSeekbarSelected", accent);
        m.put("chat_outAudioCacheSeekbar", AmberTokens.alpha(outText, 0.15f));
        m.put("chat_outVoiceSeekbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outVoiceSeekbarFill", accent);
        m.put("chat_outVoiceSeekbarSelected", accent);
        m.put("chat_outVenueInfoText", outText);
        m.put("chat_outVenueInfoSelectedText", outText);
        m.put("chat_outContactBackground", d ? 0xFFFBCE8F : 0xFF6E5200);
        m.put("chat_outContactNameText", outText);
        m.put("chat_outContactPhoneText", outDim);
        m.put("chat_outContactPhoneSelectedText", outDim);
        m.put("chat_outContactIcon", accent);
        m.put("chat_outLocationIcon", accent);
        m.put("chat_outTableBackground", d ? 0xFFFBF1DD : 0xFF6E5200);
        m.put("chat_outTableBorder", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outCodeBackground", d ? 0xFFF6E3C2 : 0xFF524000);
        m.put("chat_outArticleCodeBackground", d ? 0xFFF6E3C2 : 0xFF524000);
        m.put("chat_outArticleCodeScrollbar", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outArticleCodeScrollbarBackground", AmberTokens.alpha(outText, 0.25f));
        m.put("chat_outArticleDetailsArrow", outDim);
        m.put("chat_outArticleDetailsLine", AmberTokens.alpha(outText, 0.30f));
        m.put("chat_outPollCorrectAnswer", d ? 0xFF3D7A2B : 0xFF9BC77E);
        m.put("chat_outPollWrongAnswer", d ? 0xFFB4382C : 0xFFFF8A75);
        m.put("chat_outReactionButtonBackground", AmberTokens.alpha(outText, d ? 0.10f : 0.14f));
        m.put("chat_outReactionButtonText", accent);
        m.put("chat_outReactionButtonTextSelected", accent);
        m.put("chat_outQuote", AmberTokens.alpha(outText, 0.12f));
        m.put("chat_outViews", outDim);
        m.put("chat_outViewsSelected", outDim);
        m.put("chat_outSentCheck", accent);
        m.put("chat_outSentCheckRead", accentBright);
        m.put("chat_outSentCheckSelected", accent);
        m.put("chat_outSentCheckReadSelected", accentBright);
        m.put("chat_outSentClock", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outSentClockSelected", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outAdminText", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outAdminSelectedText", AmberTokens.alpha(outText, 0.60f));
        m.put("chat_outLinkSelectBackground", AmberTokens.alpha(accent, 0.25f));
        m.put("chat_outTextSelectionCursor", accent);
        m.put("chat_outTextSelectionHighlight", AmberTokens.alpha(accent, 0.30f));
        m.put("chat_outUpCall", accent);
        m.put("chat_outDivider", outline);

        // ── اشتراکی صفحه چت ─────────────────────────────────────────────────
        m.put("chat_linkSelectBackground", AmberTokens.alpha(accent, 0.25f));
        m.put("chat_textSelectBackground", AmberTokens.alpha(accent, 0.35f));
        m.put("chat_serviceText", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);
        m.put("chat_serviceBackground", svcBg);
        m.put("chat_serviceBackgroundSelected", svcBg);
        m.put("chat_serviceBackgroundSelector", svcBg);
        m.put("chat_serviceIcon", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);
        m.put("chat_serviceLink", d ? 0xFFFFEFC9 : 0xFFFFDDB8);
        m.put("chat_goDownButton", goDown);
        m.put("chat_goDownButtonCounter", badgeText);
        m.put("chat_goDownButtonCounterBackground", accent);
        m.put("chat_status", dim);
        m.put("chat_topPanelBackground", header);
        m.put("chat_topPanelTitle", text);
        m.put("chat_topPanelMessage", dim);
        m.put("chat_topPanelLine", divider);
        m.put("chat_topPanelClose", dim);
        m.put("chat_fieldOverlayText", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);
        m.put("chat_muteIcon", dim);
        m.put("chat_unreadMessagesStartBackground", header);
        m.put("chat_unreadMessagesStartText", accent);
        m.put("chat_unreadMessagesStartArrowIcon", accent);
        m.put("chat_searchPanelText", dim);
        m.put("chat_searchPanelIcons", dim);
        m.put("chat_stickersHintPanel", d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE);
        m.put("chat_botButtonText", accent);
        m.put("chat_botKeyboardButtonBackground", accent);
        m.put("chat_botKeyboardButtonBackgroundPressed", accentBright);
        m.put("chat_botKeyboardButtonText", onAccent);
        m.put("chat_botSwitchToInlineText", accent);
        m.put("chat_replyPanelClose", dim);
        m.put("chat_replyPanelIcons", dim);
        m.put("chat_replyPanelLine", divider);
        m.put("chat_replyPanelName", accent);
        m.put("chat_recordTime", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);
        m.put("chat_recordVoiceCancel", dim);
        m.put("chat_recordedVoiceBackground", d ? 0xFFFFEFC9 : 0xFF332717);
        m.put("chat_recordedVoiceDarkerBackground", headerBorder);
        m.put("chat_recordedVoiceDot", accent);
        m.put("chat_recordedVoicePlayPause", accent);
        m.put("chat_recordedVoiceProgress", accent);
        m.put("chat_recordedVoiceProgressInner", d ? 0xFFFFFFFF : AmberTokens.NIGHT_TEXT);
        m.put("chat_secretTimeText", dim);
        m.put("chat_secretChatStatusText", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chat_stickerNameText", accent);
        m.put("chat_stickerReplyLine", accent);
        m.put("chat_stickerReplyMessageText", text);
        m.put("chat_stickerReplyNameText", accent);
        m.put("chat_stickerViaBotNameText", accent);
        m.put("chat_inlineResultIcon", dim);

        // ── پنل پیام ────────────────────────────────────────────────────────
        m.put("chat_messagePanelBackground", d ? 0xFFFFEFC9 : AmberTokens.NIGHT_HEADER);
        m.put("chat_messagePanelShadow", 0x00000000);
        m.put("chat_messagePanelText", text);
        m.put("chat_messagePanelHint", dim);
        m.put("chat_messagePanelCursor", accent);
        m.put("chat_messagePanelIcons", accent);
        m.put("chat_messagePanelSend", accent);
        m.put("chat_messagePanelCancelInlineBot", dim);
        m.put("chat_messagePanelVoiceBackground", header);
        m.put("chat_messagePanelVoiceDelete", dim);
        m.put("chat_messagePanelVoiceDuration", text);
        m.put("chat_messagePanelVoicePressed", AmberTokens.alpha(text, 0.08f));
        m.put("key_chat_messagePanelVoiceLock", header);
        m.put("key_chat_messagePanelVoiceLockBackground", accent);
        m.put("key_chat_messagePanelVoiceLockShadow", 0x00000000);

        // ── پنل پیوست ───────────────────────────────────────────────────────
        m.put("chat_attachAudioBackground", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("chat_attachContactBackground", d ? 0xFF8C6A1D : 0xFFC79A3E);
        m.put("chat_attachGalleryBackground", accent);
        m.put("chat_attachPhotoBackground", accentBright);
        m.put("chat_attachLocationBackground", green);
        m.put("chat_attachPollBackground", dim);
        m.put("chat_attachIcon", dim);
        m.put("chat_attachActiveTab", accent);
        m.put("chat_attachUnactiveTab", dim);
        m.put("chat_attachCheckBoxBackground", accent);
        m.put("chat_attachCheckBoxCheck", onAccent);
        m.put("chat_attachEmptyImage", dim);
        m.put("chat_attachPermissionImage", dim);
        m.put("chat_attachPermissionMark", dim);
        m.put("chat_attachPermissionText", dim);

        // ── پنل ایموجی ──────────────────────────────────────────────────────
        m.put("chat_emojiPanelBackground", d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE);
        m.put("chat_emojiPanelIcon", dim);
        m.put("chat_emojiPanelIconSelected", accent);
        m.put("chat_emojiPanelBackspace", dim);
        m.put("chat_emojiPanelShadowLine", d ? 0x1E000000 : 0x33000000);
        m.put("chat_emojiPanelStickerPackSelector", d ? 0xFFF7EFE4 : AmberTokens.NIGHT_SURFACE);
        m.put("chat_emojiPanelStickerPackSelectorLine", accent);
        m.put("chat_emojiSearchBackground", fieldBg);
        m.put("chat_emojiSearchIcon", dim);

        // ── دیالوگ‌ها ────────────────────────────────────────────────────────
        m.put("dialogBackground", fieldBg);
        m.put("dialogBackgroundGray", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG);
        m.put("dialogTextBlack", text);
        m.put("dialogTextGray", dim);
        m.put("dialogTextGray2", dim);
        m.put("dialogTextGray3", time);
        m.put("dialogTextGray4", time);
        m.put("dialogTextHint", time);
        m.put("dialogTextBlue", accent);
        m.put("dialogTextBlue2", accent);
        m.put("dialogTextBlue4", accent);
        m.put("dialogTextLink", accent);
        m.put("dialogLinkSelection", AmberTokens.alpha(accent, 0.25f));
        m.put("dialogInputField", fieldBorder);
        m.put("dialogInputFieldActivated", accent);
        m.put("dialogButton", accent);
        m.put("dialogButtonSelector", AmberTokens.alpha(accent, 0.10f));
        m.put("dialogIcon", dim);
        m.put("dialogGrayLine", divider);
        m.put("dialogTopBackground", surface);
        m.put("dialogScrollGlow", AmberTokens.alpha(accent, 0.30f));
        m.put("dialogRoundCheckBox", accent);
        m.put("dialogRoundCheckBoxCheck", onAccent);
        m.put("dialogRadioBackground", outline);
        m.put("dialogRadioBackgroundChecked", accent);
        m.put("dialogCheckboxSquareBackground", accent);
        m.put("dialogCheckboxSquareCheck", onAccent);
        m.put("dialogCheckboxSquareUnchecked", dim);
        m.put("dialogCheckboxSquareDisabled", outline);
        m.put("dialogLineProgress", accent);
        m.put("dialogLineProgressBackground", outline);
        m.put("dialogSearchBackground", fieldBg);
        m.put("dialogSearchHint", time);
        m.put("dialogSearchIcon", dim);
        m.put("dialogSearchText", text);
        m.put("dialogFloatingButton", accent);
        m.put("dialogFloatingButtonPressed", accentBright);
        m.put("dialogFloatingIcon", onAccent);
        m.put("dialogEmptyText", dim);
        m.put("dialogEmptyImage", dim);
        m.put("dialogShadowLine", 0x00000000);
        m.put("dialogCardShadow", 0x00000000);
        m.put("dialogSwipeRemove", surface);
        m.put("dialogReactionMentionBackground", AmberTokens.alpha(accent, 0.12f));
        m.put("dialog_inlineProgress", accent);
        m.put("dialog_inlineProgressBackground", outline);
        m.put("dialog_liveLocationProgress", accent);

        // ── کنترل‌ها: سوییچ/چک‌باکس/رادیو ───────────────────────────────────
        m.put("switchTrack", d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE);
        m.put("switchTrackChecked", accent);
        m.put("switchTrackBlue", d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE);
        m.put("switchTrackBlueChecked", accent);
        m.put("switchTrackBlueSelector", AmberTokens.alpha(accent, 0.12f));
        m.put("switchTrackBlueSelectorChecked", AmberTokens.alpha(accent, 0.12f));
        m.put("switchTrackBlueThumb", onAccent);
        m.put("switchTrackBlueThumbChecked", onAccent);
        m.put("checkbox", accent);
        m.put("checkboxCheck", onAccent);
        m.put("checkboxDisabled", d ? 0xFFDCCFB8 : AmberTokens.NIGHT_OUTLINE);
        m.put("checkboxSquareBackground", accent);
        m.put("checkboxSquareCheck", onAccent);
        m.put("checkboxSquareUnchecked", dim);
        m.put("checkboxSquareDisabled", outline);
        m.put("radioBackground", outline);
        m.put("radioBackgroundChecked", accent);

        // ── پروفایل ─────────────────────────────────────────────────────────
        m.put("profile_title", text);
        m.put("profile_status", accent);
        m.put("profile_tabText", dim);
        m.put("profile_tabSelectedText", accent);
        m.put("profile_tabSelectedLine", accent);
        m.put("profile_tabSelector", AmberTokens.alpha(accent, 0.10f));
        m.put("profile_actionBackground", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP);
        m.put("profile_actionIcon", accent);
        m.put("profile_actionPressedBackground", AmberTokens.alpha(text, 0.08f));
        m.put("profile_creatorIcon", accent);
        m.put("profile_verifiedBackground", accent);
        m.put("profile_verifiedCheck", onAccent);

        // ── آواتارها: ۸ رنگ + توقف دوم گرادیان (هویت گرم) ───────────────────
        m.put("avatar_backgroundBlue", d ? 0xFFFFB25E : 0xFFB45309);
        m.put("avatar_background2Blue", d ? 0xFFE8871E : 0xFF8A3E06);
        m.put("avatar_backgroundCyan", d ? 0xFFDD8A5B : 0xFF9E4632);
        m.put("avatar_background2Cyan", d ? 0xFFB4382C : 0xFF6E2A1E);
        m.put("avatar_backgroundGreen", d ? 0xFFC2A25E : 0xFF8C6A1D);
        m.put("avatar_background2Green", d ? 0xFF8C6A1D : 0xFF5E470F);
        m.put("avatar_backgroundOrange", d ? 0xFFF0C08A : 0xFFB06428);
        m.put("avatar_background2Orange", d ? 0xFFC25E00 : 0xFF74400E);
        m.put("avatar_backgroundPink", d ? 0xFFE8871E : 0xFF8A3E06);
        m.put("avatar_background2Pink", d ? 0xFFFFB25E : 0xFFB45309);
        m.put("avatar_backgroundRed", d ? 0xFFB4382C : 0xFF6E2A1E);
        m.put("avatar_background2Red", d ? 0xFFDD8A5B : 0xFF9E4632);
        m.put("avatar_backgroundViolet", d ? 0xFF8C6A1D : 0xFF5E470F);
        m.put("avatar_background2Violet", d ? 0xFFC2A25E : 0xFF8C6A1D);
        m.put("avatar_backgroundSaved", d ? 0xFFC25E00 : 0xFF74400E);
        m.put("avatar_background2Saved", d ? 0xFFF0C08A : 0xFFB06428);
        m.put("avatar_nameInMessageBlue", d ? 0xFFB4561A : 0xFFE8A45C);
        m.put("avatar_nameInMessageCyan", d ? 0xFF9C7A1E : 0xFFD6B25C);
        m.put("avatar_nameInMessageGreen", d ? 0xFF6E8C2A : 0xFFB6C25E);
        m.put("avatar_nameInMessageOrange", d ? 0xFFC25E00 : 0xFFF5A623);
        m.put("avatar_nameInMessagePink", d ? 0xFFB4382C : 0xFFE06A5B);
        m.put("avatar_nameInMessageRed", d ? 0xFFA03A2A : 0xFFE08573);
        m.put("avatar_nameInMessageViolet", d ? 0xFF8C5A3C : 0xFFD69A78);
        m.put("avatar_backgroundArchived", d ? 0xFFA8A094 : 0xFF6B6257);
        m.put("avatar_backgroundArchivedHidden", d ? 0xFFD8D0C4 : 0xFF3A332A);
        m.put("avatar_text", d ? 0xFFFFFFFF : 0xFFFFF1DC);
        m.put("avatar_actionBarIconBlue", text);
        m.put("avatar_actionBarSelectorBlue", AmberTokens.alpha(text, 0.10f));
        m.put("avatar_backgroundActionBarBlue", header);
        m.put("avatar_backgroundInProfileBlue", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_WALLPAPER_TOP);
        m.put("avatar_subtitleInProfileBlue", dim);

        // ── استوری/تاپیک/شیشه/متن قرمز ──────────────────────────────────────
        m.put("stories_circle1", accent);
        m.put("stories_circle2", accentBright);
        m.put("stories_circle_closeFriends1", d ? 0xFF4E9C4B : 0xFF7DBE72);
        m.put("stories_circle_closeFriends2", d ? 0xFF3D7A2B : 0xFF5E9C52);
        m.put("stories_circle_dialog1", accent);
        m.put("stories_circle_dialog2", accentBright);
        m.put("stories_circle_live1", d ? 0xFFB4382C : 0xFFE2695B);
        m.put("stories_circle_live2", d ? 0xFF8C2E2E : 0xFFB44A3E);
        m.put("topics_unreadCounter", accent);
        m.put("topics_unreadCounterMuted", surface);
        m.put("glass_defaultIcon", text);
        m.put("glass_defaultText", text);
        m.put("glass_tabSelected", AmberTokens.alpha(accent, 0.30f));
        m.put("glass_tabSelectedText", accent);
        m.put("glass_tabUnselected", dim);
        m.put("glass_targetMainTabs", d ? 0xE6FFF6EA : 0xE6241D14);
        m.put("glass_targetMainTopPanel", d ? 0xE6FFE9CF : 0xE61F1912);
        m.put("text_RedRegular", red);
        m.put("text_RedBold", red);

        // ── Instant View ────────────────────────────────────────────────────
        m.put("iv_background", white);
        m.put("iv_backgroundGray", d ? AmberTokens.DAY_SURFACE : AmberTokens.NIGHT_BG);
        m.put("iv_navigationBackground", header);
        m.put("iv_ab_progress", accent);

        return m;
    }
}

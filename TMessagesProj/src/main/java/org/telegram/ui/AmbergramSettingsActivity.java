package org.telegram.ui;

import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;

import org.telegram.messenger.AmberAntiAds;
import org.telegram.messenger.AmberBackup;
import org.telegram.messenger.AmberChatTweaks;
import org.telegram.messenger.AmberExtras;
import org.telegram.messenger.AmberGhost;
import org.telegram.messenger.AmberMorphe;
import org.telegram.messenger.AmberPrivacy;
import org.telegram.messenger.AmberThemeFX;
import org.telegram.messenger.AmbergramProxyManager;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.browser.Browser;
import org.telegram.messenger.DownloadQueueController;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;
import org.telegram.ui.Cells.AppIconsSelectorCell;
import org.telegram.ui.Components.AmberSettingsUI;
import org.telegram.ui.Components.AmberSettingsUI.SettingRow;
import org.telegram.ui.Components.AmberSettingsUI.StatusChip;
import org.telegram.ui.Components.LayoutHelper;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * AmberGram UI 3.0 "Solstice" — هاب تنظیمات.
 *
 * معماری جدید: هدر قهرمان (گم کهربایی + هالهٔ گرم)، چیپ‌های وضعیت زنده
 * (صف/شبح/پروکسی)، کارت‌های بخش‌بندی‌شده با گوشه گرد و ردیف‌های سوییچ‌دار واقعی.
 * همهٔ اجزا از تم جاری رنگ می‌گیرند (ThemeBind)؛ منطق شبکه/صف/پروکسی دست‌نخورده.
 */
public class AmbergramSettingsActivity extends BaseFragment implements DownloadQueueController.QueueListener, AmbergramProxyManager.Listener {

    private AmberSettingsUI.StatusChip queueChip;
    private AmberSettingsUI.StatusChip ghostChip;
    private AmberSettingsUI.StatusChip proxyChip;

    private SettingRow queueRow;
    private SettingRow proxyRow;
    private SettingRow ghostRow;
    private SettingRow doubleTapRow;
    private SettingRow lockedRow;
    private final HashMap<Integer, SettingRow> toggleRows = new HashMap<>();
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

        LinearLayout content = new LinearLayout(context);
        content.setOrientation(LinearLayout.VERTICAL);
        scrollView.addView(content, new ScrollView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        // ── هدر قهرمان: گم کهربایی + هالهٔ گرم + چیپ نسخهٔ Solstice ──
        content.addView(new AmberSettingsUI.HeroView(context, getResourceProvider()),
                LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        // ── چیپ‌های وضعیت زنده ──
        HorizontalScrollView chipsScroll = new HorizontalScrollView(context);
        chipsScroll.setHorizontalScrollBarEnabled(false);
        chipsScroll.setVerticalScrollBarEnabled(false);
        content.addView(chipsScroll, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, 0, 12, 0, 0));

        LinearLayout chipsRow = new LinearLayout(context);
        chipsRow.setOrientation(LinearLayout.HORIZONTAL);
        chipsRow.setPadding(AndroidUtilities.dp(14), 0, AndroidUtilities.dp(14), 0);
        chipsScroll.addView(chipsRow, new HorizontalScrollView.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        queueChip = new StatusChip(context, R.drawable.msg_download, LocaleController.getString(R.string.AmberChipQueue), getResourceProvider());
        chipsRow.addView(queueChip, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, 0, 0, 8, 0));
        ghostChip = new StatusChip(context, R.drawable.ghost, LocaleController.getString(R.string.AmberChipGhost), getResourceProvider());
        chipsRow.addView(ghostChip, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, 0, 0, 8, 0));
        proxyChip = new StatusChip(context, R.drawable.ic_ambergram_proxy, LocaleController.getString(R.string.AmberChipProxy), getResourceProvider());
        chipsRow.addView(proxyChip, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT));

        // ── ابزارها ──
        AmberSettingsUI.SectionCard toolsCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionTools, getResourceProvider());
        queueRow = toolsCard.addActionRow(context, R.drawable.msg_download, R.string.AmbergramQueueSection, 0,
                v -> presentFragment(new AmbergramQueueActivity()), getResourceProvider());
        proxyRow = toolsCard.addActionRow(context, R.drawable.ic_ambergram_proxy, R.string.AmbergramProxySection, 0,
                v -> presentFragment(new AmbergramProxyActivity()), getResourceProvider());
        registerGhostToggle();
        ghostRow = toolsCard.addToggleRow(context, R.drawable.ghost, R.string.AmberGhostSection, R.string.AmberGhostDesc,
                AmberGhost.isEnabled(), value -> AmberGhost.setEnabled(value), getResourceProvider());

        // ── گفت‌وگوها ──
        AmberSettingsUI.SectionCard chatsCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionChats, getResourceProvider());
        addToggleSection(context, chatsCard, new int[][]{
                {R.drawable.msg_block, R.string.AmberNoSponsored, R.string.AmberNoSponsoredDesc},
                {R.drawable.msg_channel, R.string.AmberNoRecommendations, R.string.AmberNoRecommendationsDesc},
                {R.drawable.msg_sticker, R.string.AmberNoGreetings, R.string.AmberNoGreetingsDesc},
                {R.drawable.msg_mute, R.string.AmberHideStoriesRead, R.string.AmberHideStoriesReadDesc},
                {R.drawable.msg_sticker, R.string.AmberHideStickerTime, R.string.AmberHideStickerTimeDesc}
        });
        doubleTapRow = chatsCard.addActionRow(context, R.drawable.msg_copy, R.string.AmberDoubleTap, 0,
                v -> {
                    int next = (AmberChatTweaks.doubleTapIncoming() + 1) % 4;
                    AmberChatTweaks.setDoubleTapIncoming(next);
                    AmberChatTweaks.setDoubleTapOutgoing(next);
                    refreshDoubleTapValue();
                }, getResourceProvider());
        lockedRow = chatsCard.addActionRow(context, R.drawable.ic_lock_header, R.string.AmberLockedChats, 0,
                v -> {
                    if (getParentActivity() != null) {
                        presentFragment(new AmberLockedChatsActivity());
                    }
                }, getResourceProvider());

        // ── حریم خصوصی ──
        AmberSettingsUI.SectionCard privacyCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionPrivacy, getResourceProvider());
        addToggleSection(context, privacyCard, new int[][]{
                {R.drawable.msg_delete, R.string.AmberAntiDelete, R.string.AmberAntiDeleteDesc},
                {R.drawable.msg_photo_blur, R.string.AmberAntiDisappearing, R.string.AmberAntiDisappearingDesc},
                {R.drawable.msg_camera, R.string.AmberNoScreenshotNotify, R.string.AmberNoScreenshotNotifyDesc},
                {R.drawable.msg_copy, R.string.AmberBypassNoforwards, R.string.AmberBypassNoforwardsDesc},
                {R.drawable.msg_block2, R.string.AmberNoChannelSwitch, R.string.AmberNoChannelSwitchDesc},
                {R.drawable.msg_secret, R.string.AmberBypassTranslation, R.string.AmberBypassTranslationDesc},
                {R.drawable.msg_link2, R.string.AmberNoLinkPreviews, R.string.AmberNoLinkPreviewsDesc},
                {R.drawable.msg_search, R.string.AmberNoGlobalSearch, R.string.AmberNoGlobalSearchDesc},
                {R.drawable.input_ai, R.string.AmberNoAiFeatures, R.string.AmberNoAiFeaturesDesc},
                {R.drawable.msg_link, R.string.AmberStripLinkTracking, R.string.AmberStripLinkTrackingDesc}
        });

        // ── سرعت و شبکه ──
        AmberSettingsUI.SectionCard speedCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionSpeed, getResourceProvider());
        addToggleSection(context, speedCard, new int[][]{
                {R.drawable.msg_speed, R.string.AmberTurboDownload, R.string.AmberTurboDownloadDesc},
                {R.drawable.msg_speed_fast, R.string.AmberTurboUpload, R.string.AmberTurboUploadDesc},
                {R.drawable.msg_download, R.string.AmberNoAutoUpdate, R.string.AmberNoAutoUpdateDesc},
                {R.drawable.msg_secret, R.string.AmberProxyAutoOffVpn, R.string.AmberProxyAutoOffVpnDesc}
        });

        // ── ظاهر و برندینگ ──
        AmberSettingsUI.SectionCard appearanceCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionAppearance, getResourceProvider());
        addToggleSection(context, appearanceCard, new int[][]{
                {R.drawable.msg_palette, R.string.AmberThemeFX, R.string.AmberThemeFXDesc}
        });
        appearanceCard.addActionRow(context, R.drawable.msg_palette, R.string.AmberDynamicThemes, R.string.AmberDynamicThemesDesc,
                v -> presentFragment(new ThemeActivity(ThemeActivity.THEME_TYPE_BASIC)), getResourceProvider());
        AppIconsSelectorCell appIconsCell = new AppIconsSelectorCell(context, this, currentAccount);
        appIconsCell.setNestedScrollingEnabled(false);
        ThemeBind.backgroundColor(appIconsCell, Theme.key_windowBackgroundWhite);
        appearanceCard.addCustomRow(appIconsCell);

        // ── پشتیبان‌گیری ──
        AmberSettingsUI.SectionCard backupCard = new AmberSettingsUI.SectionCard(context, content, R.string.AmberSectionBackup, getResourceProvider());
        backupCard.addActionRow(context, R.drawable.msg_copy, R.string.AmberBackupExport, 0,
                v -> {
                    if (getParentActivity() != null) {
                        AmberBackup.exportSettings(this);
                    }
                }, getResourceProvider());
        backupCard.addActionRow(context, R.drawable.msg_download, R.string.AmberBackupImport, 0,
                v -> {
                    if (getParentActivity() != null) {
                        AmberBackup.importSettings(this);
                    }
                }, getResourceProvider());

        // ── فوتر ──
        content.addView(AmberSettingsUI.createFooter(context, getResourceProvider(),
                v -> Browser.openUrl(getParentActivity(), "https://github.com/Soroushchq/amber")),
                LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        refreshQueueValue();
        refreshProxyValue();
        refreshGhostValue();
        refreshDoubleTapValue();
        refreshLockedValue();
        refreshAllToggles();
        return fragmentView;
    }

    private void registerGhostToggle() {
        toggles.put(R.string.AmberGhostSection, new AmberToggle() {
            @Override
            public boolean get() {
                return AmberGhost.isEnabled();
            }

            @Override
            public void set(boolean value) {
                AmberGhost.setEnabled(value);
            }
        });
    }

    private void addToggleSection(Context context, AmberSettingsUI.SectionCard card, int[][] specs) {
        for (int[] spec : specs) {
            final int titleRes = spec[1];
            AmberToggle toggle = new AmberToggle() {
                @Override
                public boolean get() {
                    return getToggleValue(titleRes);
                }

                @Override
                public void set(boolean value) {
                    setToggleValue(titleRes, value);
                }
            };
            toggles.put(titleRes, toggle);
            SettingRow row = card.addToggleRow(context, spec[0], titleRes, spec[2], toggle.get(),
                    value -> setToggleValue(titleRes, value), getResourceProvider());
            toggleRows.put(titleRes, row);
        }
    }

    // ─────────────────────────── به‌روزرسانی زنده ───────────────────────────

    private void refreshQueueValue() {
        if (queueChip == null || queueRow == null || getContext() == null) {
            return;
        }
        ArrayList<DownloadQueueController.QueueItem> items = DownloadQueueController.getInstance(currentAccount).getQueueSnapshot();
        int waiting = 0, downloading = 0;
        for (DownloadQueueController.QueueItem item : items) {
            if (item.state == DownloadQueueController.STATE_PENDING) {
                waiting++;
            } else if (item.state == DownloadQueueController.STATE_DOWNLOADING) {
                downloading++;
            }
        }
        if (waiting > 0 || downloading > 0) {
            CharSequence summary = LocaleController.formatString(R.string.AmbergramQueueSummary, String.valueOf(waiting), String.valueOf(downloading));
            queueChip.update(summary, true);
            queueRow.setValueText(summary, true);
        } else {
            CharSequence idle = LocaleController.getString(R.string.AmbergramQueueRowIdle);
            queueChip.update(idle, false);
            queueRow.setValueText(idle, false);
        }
    }

    private void refreshGhostValue() {
        if (ghostChip == null || ghostRow == null || getContext() == null) {
            return;
        }
        boolean enabled = AmberGhost.isEnabled();
        ghostChip.update(LocaleController.getString(enabled ? R.string.AmberGhostOn : R.string.AmberGhostOff), enabled);
        ghostRow.setChecked(enabled);
    }

    private void refreshProxyValue() {
        if (proxyChip == null || proxyRow == null || getContext() == null) {
            return;
        }
        AmbergramProxyManager manager = AmbergramProxyManager.getInstance();
        if (manager.isFetching()) {
            CharSequence fetching = LocaleController.getString(R.string.AmbergramProxyFetching);
            proxyChip.update(fetching, true);
            proxyRow.setValueText(fetching, true);
            return;
        }
        if (manager.isTesting()) {
            CharSequence testing = LocaleController.formatString(R.string.AmbergramProxyTesting, String.valueOf(manager.getProcessedCount()), String.valueOf(manager.getTestTotal()));
            proxyChip.update(testing, true);
            proxyRow.setValueText(testing, true);
            return;
        }
        int working = manager.getWorkingCount();
        if (working > 0) {
            CharSequence value = LocaleController.formatString(R.string.AmbergramProxySettingsValue, String.valueOf(working));
            proxyChip.update(value, true);
            proxyRow.setValueText(value, true);
        } else {
            CharSequence value = LocaleController.getString(R.string.AmbergramProxySubtitle);
            proxyChip.update(value, false);
            proxyRow.setValueText(value, false);
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        refreshDoubleTapValue();
        refreshLockedValue();
        refreshQueueValue();
        refreshGhostValue();
        refreshProxyValue();
    }

    @Override
    public void onActivityResultFragment(int requestCode, int resultCode, Intent data) {
        if (AmberBackup.handleActivityResult(requestCode, resultCode, data)) {
            return;
        }
        super.onActivityResultFragment(requestCode, resultCode, data);
    }

    private void refreshAllToggles() {
        for (HashMap.Entry<Integer, SettingRow> entry : toggleRows.entrySet()) {
            AmberToggle toggle = toggles.get(entry.getKey());
            if (toggle != null) {
                entry.getValue().setChecked(toggle.get());
            }
        }
        if (ghostRow != null) {
            ghostRow.setChecked(AmberGhost.isEnabled());
        }
    }

    private void refreshDoubleTapValue() {
        if (doubleTapRow == null || getContext() == null) {
            return;
        }
        int action = AmberChatTweaks.doubleTapIncoming();
        int res;
        if (action == AmberChatTweaks.DOUBLE_TAP_REPEAT) {
            res = R.string.AmberDoubleTapOptionRepeat;
        } else if (action == AmberChatTweaks.DOUBLE_TAP_FORWARD_NO_QUOTE) {
            res = R.string.AmberDoubleTapOptionForward;
        } else if (action == AmberChatTweaks.DOUBLE_TAP_COPY) {
            res = R.string.AmberDoubleTapOptionCopy;
        } else {
            res = R.string.AmberDoubleTapOptionReaction;
        }
        doubleTapRow.setValueText(LocaleController.getString(res), true);
    }

    private void refreshLockedValue() {
        if (lockedRow == null || getContext() == null) {
            return;
        }
        int count = AmberExtras.lockedDialogsCount();
        if (count > 0) {
            lockedRow.setValueText(LocaleController.formatString(R.string.AmberLockedChatsCount, String.valueOf(count)), true);
        } else {
            lockedRow.setValueText(LocaleController.getString(R.string.AmberGhostOff), false);
        }
    }

    // ─────────────────────────── نگاشت toggle ها ───────────────────────────

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
        } else if (titleRes == R.string.AmberHideStickerTime) {
            return AmberChatTweaks.hideStickerTime();
        } else if (titleRes == R.string.AmberBypassTranslation) {
            return AmberMorphe.bypassTranslation();
        } else if (titleRes == R.string.AmberNoLinkPreviews) {
            return AmberPrivacy.disableLinkPreviews();
        } else if (titleRes == R.string.AmberNoGlobalSearch) {
            return AmberPrivacy.disableGlobalSearch();
        } else if (titleRes == R.string.AmberNoAiFeatures) {
            return AmberPrivacy.disableAiFeatures();
        } else if (titleRes == R.string.AmberStripLinkTracking) {
            return AmberPrivacy.stripLinkTracking();
        } else if (titleRes == R.string.AmberTurboUpload) {
            return AmberExtras.turboUpload();
        } else if (titleRes == R.string.AmberProxyAutoOffVpn) {
            return AmbergramProxyManager.proxyAutoOffVpn();
        } else if (titleRes == R.string.AmberThemeFX) {
            return AmberThemeFX.enabled();
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
        } else if (titleRes == R.string.AmberHideStickerTime) {
            AmberChatTweaks.setHideStickerTime(value);
        } else if (titleRes == R.string.AmberBypassTranslation) {
            AmberMorphe.setBypassTranslation(value);
        } else if (titleRes == R.string.AmberNoLinkPreviews) {
            AmberPrivacy.setDisableLinkPreviews(value);
        } else if (titleRes == R.string.AmberNoGlobalSearch) {
            AmberPrivacy.setDisableGlobalSearch(value);
        } else if (titleRes == R.string.AmberNoAiFeatures) {
            AmberPrivacy.setDisableAiFeatures(value);
        } else if (titleRes == R.string.AmberStripLinkTracking) {
            AmberPrivacy.setStripLinkTracking(value);
        } else if (titleRes == R.string.AmberTurboUpload) {
            AmberExtras.setTurboUpload(value);
        } else if (titleRes == R.string.AmberProxyAutoOffVpn) {
            AmbergramProxyManager.setProxyAutoOffVpn(value);
        } else if (titleRes == R.string.AmberThemeFX) {
            AmberThemeFX.setEnabled(value);
        }
    }

    // ─────────────────────────── شنونده‌های صف/پروکسی ───────────────────────────

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

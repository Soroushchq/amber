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
                {R.drawable.msg_sticker, R.string.AmberNoGreetings, R.string.AmberNoGreetingsDesc}
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

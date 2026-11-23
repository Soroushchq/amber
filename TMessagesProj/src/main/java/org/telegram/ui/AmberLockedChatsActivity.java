package org.telegram.ui;

import android.content.Context;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.telegram.messenger.AmberExtras;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.DialogObject;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;
import org.telegram.ui.Cells.TextInfoPrivacyCell;
import org.telegram.ui.Components.LayoutHelper;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Set;

/**
 * AmberGram fork (round 19 — extras): management page for hidden/locked chats.
 * Locked dialogs are hidden from the chat list and never raise notifications
 * (the gates live in DialogsActivity.getDialogsArray and
 * NotificationsController.processNewMessages); this page is the reveal and
 * unlock surface — one row per locked dialog with an «Unlock» button.
 * Structural style mirrors AmbergramSettingsActivity (house style): gray
 * window, ScrollView + vertical LinearLayout, themed colors, TextInfoPrivacyCell.
 */
public class AmberLockedChatsActivity extends BaseFragment {

    private LinearLayout rowsCard;
    private TextInfoPrivacyCell hintCell;

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(LocaleController.getString(R.string.AmberLockedChats));
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

        // explainer — locked chats are hidden from the list and never notify
        hintCell = new TextInfoPrivacyCell(context, 24, null);
        contentWrapper.addView(hintCell, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        rowsCard = new LinearLayout(context);
        rowsCard.setOrientation(LinearLayout.VERTICAL);
        ThemeBind.backgroundColor(rowsCard, Theme.key_windowBackgroundWhite);
        contentWrapper.addView(rowsCard, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        // tail gray cell keeps the same rhythm as the other Amber pages
        TextInfoPrivacyCell tailCell = new TextInfoPrivacyCell(context, 24, null);
        tailCell.setText(LocaleController.getString(R.string.AmberLockedChatsDesc));
        contentWrapper.addView(tailCell, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        rebuildRows();
        return fragmentView;
    }

    @Override
    public void onResume() {
        super.onResume();
        // locks can change from the chat list while this page sits in the back stack
        rebuildRows();
    }

    private void rebuildRows() {
        if (rowsCard == null || hintCell == null || getContext() == null) {
            return;
        }
        rowsCard.removeAllViews();
        Set<String> locked = AmberExtras.getLockedDialogs();
        ArrayList<Long> dialogIds = new ArrayList<>();
        for (String raw : locked) {
            try {
                dialogIds.add(Long.parseLong(raw));
            } catch (Exception ignore) {
            }
        }
        Collections.sort(dialogIds);
        if (dialogIds.isEmpty()) {
            rowsCard.setVisibility(View.GONE);
            hintCell.setText(LocaleController.getString(R.string.AmberLockedChatsEmpty));
            return;
        }
        rowsCard.setVisibility(View.VISIBLE);
        hintCell.setText(LocaleController.getString(R.string.AmberLockedChatsDesc));
        for (int a = 0; a < dialogIds.size(); a++) {
            if (a > 0) {
                View divider = new View(getContext());
                divider.setBackgroundColor(getThemedColor(Theme.key_windowBackgroundGray));
                rowsCard.addView(divider, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, 1));
            }
            rowsCard.addView(makeRow(getContext(), dialogIds.get(a)), LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        }
    }

    private View makeRow(Context context, long dialogId) {
        // resolve the title: getDialog may return null for unknown peers — fall back
        // to the raw dialog id so the row is still actionable
        boolean known = MessagesController.getInstance(currentAccount).getDialog(dialogId) != null;
        String title = known ? DialogObject.getName(currentAccount, dialogId) : "";
        if (TextUtils.isEmpty(title)) {
            title = "#" + dialogId;
        }

        LinearLayout row = new LinearLayout(context);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(12), AndroidUtilities.dp(16), AndroidUtilities.dp(12));
        row.setBackground(Theme.createSelectorDrawable(getThemedColor(Theme.key_listSelector)));
        row.setOnClickListener(v -> {
            AmberExtras.setDialogLocked(dialogId, false);
            rebuildRows();
        });

        LinearLayout textCol = new LinearLayout(context);
        textCol.setOrientation(LinearLayout.VERTICAL);
        row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

        TextView titleView = new TextView(context);
        titleView.setTypeface(AndroidUtilities.bold());
        titleView.setTextSize(16);
        ThemeBind.textColor(titleView, Theme.key_windowBackgroundWhiteBlackText, null);
        titleView.setText(title);
        titleView.setSingleLine(true);
        titleView.setEllipsize(TextUtils.TruncateAt.END);
        textCol.addView(titleView, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

        TextView unlockView = new TextView(context);
        unlockView.setTypeface(AndroidUtilities.bold());
        unlockView.setTextSize(14);
        unlockView.setText(LocaleController.getString(R.string.AmberUnlockChat));
        unlockView.setGravity(Gravity.CENTER);
        unlockView.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(8), AndroidUtilities.dp(14), AndroidUtilities.dp(8));
        ThemeBind.textColor(unlockView, Theme.key_windowBackgroundWhiteBlueText, null);
        unlockView.setOnClickListener(v -> {
            AmberExtras.setDialogLocked(dialogId, false);
            rebuildRows();
        });
        row.addView(unlockView, LayoutHelper.createLinear(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, 0, Gravity.CENTER_VERTICAL, 8, 0, 0, 0));

        return row;
    }
}

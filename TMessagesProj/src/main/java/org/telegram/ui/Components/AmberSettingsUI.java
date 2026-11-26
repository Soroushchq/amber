package org.telegram.ui.Components;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.graphics.RadialGradient;
import android.graphics.Shader;
import android.graphics.drawable.GradientDrawable;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeBind;

/**
 * AmberGram UI 3.0 "Solstice" — کیت اجزای تنظیمات.
 *
 * اجزای حرفه‌ای برای هاب تنظیمات: هدر قهرمان با درخشش گم، چیپ‌های وضعیت زنده،
 * کارت‌های بخش‌بندی‌شده با گوشه‌های گرد، و ردیف‌های تنظیم با سوییچ واقعی.
 * همهٔ رنگ‌ها از تم جاری می‌آیند (ThemeBind) تا با هر تمی هماهنگ بمانند.
 */
public class AmberSettingsUI {

    /** رنگ برند آمبر — فقط برای درخشش/تینت‌های تزئینی ثابت */
    public static final int BRAND_AMBER = 0xFFF5A623;
    public static final int BRAND_AMBER_DEEP = 0xFFC25E00;

    private AmberSettingsUI() {}

    // ═══════════════════════════════════════════════════════════════════════
    // هدر قهرمان — پس‌زمینهٔ سطح تم + هالهٔ گرم شعاعی پشت نشان گم
    // ═══════════════════════════════════════════════════════════════════════
    public static class HeroView extends FrameLayout {

        private final Paint basePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint glowPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint linePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Theme.ResourcesProvider resourcesProvider;

        public HeroView(Context context, Theme.ResourcesProvider provider) {
            super(context);
            this.resourcesProvider = provider;
            setWillNotDraw(false);

            LinearLayout content = new LinearLayout(context);
            content.setOrientation(LinearLayout.VERTICAL);
            content.setGravity(Gravity.CENTER_HORIZONTAL);
            addView(content, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 22, 0, 20));

            ImageView gem = new ImageView(context);
            gem.setImageResource(R.drawable.amber_gem);
            content.addView(gem, LayoutHelper.createLinear(84, 84, Gravity.CENTER_HORIZONTAL));

            TextView title = new TextView(context);
            title.setTypeface(AndroidUtilities.bold());
            title.setTextSize(25);
            title.setGravity(Gravity.CENTER);
            ThemeBind.textColor(title, Theme.key_windowBackgroundWhiteBlackText, provider);
            title.setText("AmberGram");
            content.addView(title, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_HORIZONTAL, 0, 10, 0, 0));

            TextView tagline = new TextView(context);
            tagline.setTextSize(13.5f);
            tagline.setGravity(Gravity.CENTER);
            ThemeBind.textColor(tagline, Theme.key_windowBackgroundWhiteGrayText2, provider);
            tagline.setText(LocaleController.getString(R.string.AmberSettingsTagline));
            content.addView(tagline, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_HORIZONTAL, 0, 3, 0, 0));

            TextView versionChip = new TextView(context);
            versionChip.setTypeface(AndroidUtilities.bold());
            versionChip.setTextSize(12.5f);
            versionChip.setGravity(Gravity.CENTER);
            ThemeBind.textColor(versionChip, Theme.key_windowBackgroundWhiteBlueText, provider);
            versionChip.setText(LocaleController.formatString(R.string.AmberVersionFormat, org.telegram.messenger.BuildVars.BUILD_VERSION_STRING));
            GradientDrawable chipBg = new GradientDrawable();
            chipBg.setColor((BRAND_AMBER & 0x00FFFFFF) | 0x22000000);
            chipBg.setCornerRadius(AndroidUtilities.dp(13));
            versionChip.setBackground(chipBg);
            versionChip.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(5), AndroidUtilities.dp(14), AndroidUtilities.dp(5));
            content.addView(versionChip, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_HORIZONTAL, 0, 10, 0, 2));
        }

        @Override
        protected void onDraw(Canvas canvas) {
            int w = getMeasuredWidth();
            int h = getMeasuredHeight();
            if (w <= 0 || h <= 0) {
                return;
            }
            basePaint.setColor(Theme.getColor(Theme.key_windowBackgroundWhite, resourcesProvider));
            canvas.drawRect(0, 0, w, h, basePaint);

            // هالهٔ گرم پشت گم — مرکز بالای هدر
            float cx = w / 2f;
            float cy = AndroidUtilities.dp(62);
            float radius = Math.max(w, h) * 0.62f;
            glowPaint.setShader(new RadialGradient(cx, cy, radius,
                    new int[]{Color.argb(52, 245, 166, 35), Color.argb(0, 245, 166, 35)},
                    new float[]{0f, 1f}, Shader.TileMode.CLAMP));
            canvas.drawCircle(cx, cy, radius, glowPaint);

            // خط جداکنندهٔ پایین هدر
            linePaint.setStrokeWidth(AndroidUtilities.dp(1));
            linePaint.setColor(Theme.getColor(Theme.key_divider, resourcesProvider));
            canvas.drawLine(0, h - AndroidUtilities.dp(1), w, h - AndroidUtilities.dp(1), linePaint);
        }
    }

    // ═══════════════════════════════════════════════════════════════════════
    // چیپ وضعیت — پیل زنده با آیکون
    // ═══════════════════════════════════════════════════════════════════════
    public static class StatusChip extends LinearLayout {

        private final ImageView icon;
        private final TextView label;
        private final TextView value;
        private final Theme.ResourcesProvider resourcesProvider;
        private boolean active;

        public StatusChip(Context context, int iconRes, CharSequence labelText, Theme.ResourcesProvider provider) {
            super(context);
            this.resourcesProvider = provider;
            setOrientation(LinearLayout.HORIZONTAL);
            setGravity(Gravity.CENTER_VERTICAL);
            setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(7), AndroidUtilities.dp(12), AndroidUtilities.dp(7));
            refreshBackground();

            icon = new ImageView(context);
            icon.setImageResource(iconRes);
            icon.setScaleType(ImageView.ScaleType.FIT_CENTER);
            icon.setColorFilter(BRAND_AMBER, PorterDuff.Mode.SRC_IN);
            addView(icon, LayoutHelper.createLinear(15, 15, Gravity.CENTER_VERTICAL, 0, 0, 7, 0));

            label = new TextView(context);
            label.setTypeface(AndroidUtilities.bold());
            label.setTextSize(12.5f);
            label.setMaxLines(1);
            label.setEllipsize(TextUtils.TruncateAt.END);
            ThemeBind.textColor(label, Theme.key_windowBackgroundWhiteBlackText, provider);
            label.setText(labelText);
            addView(label, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL, 0, 0, 5, 0));

            value = new TextView(context);
            value.setTypeface(AndroidUtilities.bold());
            value.setTextSize(12.5f);
            value.setMaxLines(1);
            value.setEllipsize(TextUtils.TruncateAt.END);
            addView(value, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL));
        }

        private void refreshBackground() {
            GradientDrawable bg = new GradientDrawable();
            bg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite, resourcesProvider));
            bg.setCornerRadius(AndroidUtilities.dp(15));
            bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_divider, resourcesProvider));
            setBackground(bg);
        }

        /** به‌روزرسانی زنده: active=true متن را اکسنت می‌کند */
        public void update(CharSequence valueText, boolean activeState) {
            active = activeState;
            value.setText(valueText);
            int color = activeState
                    ? Theme.getColor(Theme.key_windowBackgroundWhiteBlueText, resourcesProvider)
                    : Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2, resourcesProvider);
            value.setTextColor(color);
            icon.setColorFilter(activeState ? BRAND_AMBER : 0xFF8A8074, PorterDuff.Mode.SRC_IN);
        }

        public boolean isActive() {
            return active;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════
    // ردیف تنظیم — دو حالت: سوییچ‌دار و اکشن (مقدار + فلش)
    // ═══════════════════════════════════════════════════════════════════════
    public static class SettingRow extends FrameLayout {

        public interface ToggleListener {
            void onToggle(boolean newValue);
        }

        private final ImageView icon;
        private final TextView title;
        private final TextView subtitle;
        private final TextView value;
        private final TextView chevron;
        private final Switch switchView;
        private final View divider;
        private final LinearLayout rowLayout;
        private final Theme.ResourcesProvider resourcesProvider;
        private final boolean toggleMode;

        public SettingRow(Context context, boolean toggle, Theme.ResourcesProvider provider) {
            super(context);
            this.resourcesProvider = provider;
            this.toggleMode = toggle;

            LinearLayout row = new LinearLayout(context);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(11), AndroidUtilities.dp(16), AndroidUtilities.dp(11));
            row.setBackground(Theme.createSelectorDrawable(Theme.getColor(Theme.key_listSelector, provider)));
            addView(row, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));
            rowLayout = row;

            FrameLayout tile = new FrameLayout(context);
            GradientDrawable tileBg = new GradientDrawable();
            tileBg.setColor((BRAND_AMBER & 0x00FFFFFF) | 0x24000000);
            tileBg.setCornerRadius(AndroidUtilities.dp(13));
            tile.setBackground(tileBg);
            icon = new ImageView(context);
            icon.setScaleType(ImageView.ScaleType.FIT_CENTER);
            icon.setColorFilter(BRAND_AMBER, PorterDuff.Mode.SRC_IN);
            tile.addView(icon, LayoutHelper.createFrame(21, 21, Gravity.CENTER));
            row.addView(tile, LayoutHelper.createLinear(42, 42, Gravity.CENTER_VERTICAL, 0, 0, 13, 0));

            LinearLayout textCol = new LinearLayout(context);
            textCol.setOrientation(LinearLayout.VERTICAL);
            textCol.setGravity(Gravity.CENTER_VERTICAL);
            row.addView(textCol, LayoutHelper.createLinear(0, LayoutHelper.WRAP_CONTENT, 1f));

            title = new TextView(context);
            title.setTypeface(AndroidUtilities.bold());
            title.setTextSize(15.5f);
            title.setMaxLines(1);
            title.setEllipsize(TextUtils.TruncateAt.END);
            ThemeBind.textColor(title, Theme.key_windowBackgroundWhiteBlackText, provider);
            textCol.addView(title, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));

            subtitle = new TextView(context);
            subtitle.setTextSize(12.5f);
            subtitle.setMaxLines(2);
            subtitle.setEllipsize(TextUtils.TruncateAt.END);
            subtitle.setLineSpacing(AndroidUtilities.dp(1.5f), 1f);
            ThemeBind.textColor(subtitle, Theme.key_windowBackgroundWhiteGrayText2, provider);
            textCol.addView(subtitle, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, 0, 1, 0, 0));

            value = new TextView(context);
            value.setTypeface(AndroidUtilities.bold());
            value.setTextSize(12.5f);
            value.setMaxLines(1);
            value.setEllipsize(TextUtils.TruncateAt.END);
            value.setVisibility(GONE);
            row.addView(value, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL, 10, 0, 4, 0));

            chevron = new TextView(context);
            chevron.setTypeface(AndroidUtilities.bold());
            chevron.setTextSize(19);
            ThemeBind.textColor(chevron, Theme.key_windowBackgroundWhiteGrayText2, provider);
            chevron.setText(LocaleController.isRTL ? "‹" : "›");
            chevron.setVisibility(GONE);
            row.addView(chevron, LayoutHelper.createLinear(20, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL));

            if (toggle) {
                switchView = new Switch(context, provider);
                switchView.setColors(Theme.key_switchTrack, Theme.key_switchTrackChecked, Theme.key_switchTrackBlueThumb, Theme.key_switchTrackBlueThumbChecked);
                row.addView(switchView, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, Gravity.CENTER_VERTICAL, 8, 0, 0, 0));
            } else {
                switchView = null;
            }

            divider = new View(context);
            divider.setBackgroundColor(Theme.getColor(Theme.key_divider, provider));
            divider.setVisibility(GONE);
            addView(divider, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, AndroidUtilities.dp(1), Gravity.BOTTOM, LocaleController.isRTL ? 0 : AndroidUtilities.dp(71), 0, LocaleController.isRTL ? AndroidUtilities.dp(71) : 0, 0));
        }

        public SettingRow bindAction(int iconRes, int titleRes, int subtitleRes, View.OnClickListener click) {
            icon.setImageResource(iconRes);
            title.setText(LocaleController.getString(titleRes));
            if (subtitleRes != 0) {
                subtitle.setText(LocaleController.getString(subtitleRes));
            } else {
                subtitle.setVisibility(GONE);
            }
            value.setVisibility(VISIBLE);
            chevron.setVisibility(VISIBLE);
            rowLayout.setOnClickListener(click);
            return this;
        }

        public SettingRow bindToggle(int iconRes, int titleRes, int subtitleRes, boolean checked, ToggleListener listener) {
            icon.setImageResource(iconRes);
            title.setText(LocaleController.getString(titleRes));
            if (subtitleRes != 0) {
                subtitle.setText(LocaleController.getString(subtitleRes));
            } else {
                subtitle.setVisibility(GONE);
            }
            setChecked(checked);
            rowLayout.setOnClickListener(v -> {
                boolean newValue = !switchView.isChecked();
                setChecked(newValue);
                if (listener != null) {
                    listener.onToggle(newValue);
                }
            });
            return this;
        }

        public void setChecked(boolean checked) {
            if (switchView != null) {
                switchView.setChecked(checked, true);
            }
        }

        public boolean isChecked() {
            return switchView != null && switchView.isChecked();
        }

        /** مقدار ردیف اکشن — accent=true رنگ برند می‌گیرد */
        public void setValueText(CharSequence text, boolean accent) {
            value.setText(text);
            value.setTextColor(accent
                    ? Theme.getColor(Theme.key_windowBackgroundWhiteBlueText, resourcesProvider)
                    : Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2, resourcesProvider));
        }

        public void setDividerVisible(boolean visible) {
            divider.setVisibility(visible ? VISIBLE : GONE);
        }

        /** فاصلهٔ داخلی عمودی ردیف */
        public void setRowPadding(int verticalDp) {
            rowLayout.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(verticalDp), AndroidUtilities.dp(16), AndroidUtilities.dp(verticalDp));
        }
    }

    // ═══════════════════════════════════════════════════════════════════════
    // کارت بخش — گوشه‌های گرد + عنوان بالای کارت
    // ═══════════════════════════════════════════════════════════════════════
    public static class SectionCard extends LinearLayout {

        private final LinearLayout card;

        public SectionCard(Context context, LinearLayout wrapper, int titleRes, Theme.ResourcesProvider provider) {
            super(context);
            setOrientation(LinearLayout.VERTICAL);

            TextView header = new TextView(context);
            header.setTypeface(AndroidUtilities.bold());
            header.setTextSize(13f);
            header.setPadding(AndroidUtilities.dp(16), 0, AndroidUtilities.dp(16), 0);
            ThemeBind.textColor(header, Theme.key_windowBackgroundWhiteGrayText2, provider);
            header.setText(LocaleController.getString(titleRes));
            wrapper.addView(header, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, 0, 20, 16, 7, 0));

            card = new LinearLayout(context);
            card.setOrientation(LinearLayout.VERTICAL);
            GradientDrawable cardBg = new GradientDrawable();
            cardBg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite, provider));
            cardBg.setCornerRadius(AndroidUtilities.dp(18));
            card.setBackground(cardBg);
            card.setClipToOutline(true);
            ThemeBind.backgroundColor(card, Theme.key_windowBackgroundWhite, provider);
            wrapper.addView(card, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT, 0, 0, 14, 0));
        }

        public LinearLayout card() {
            return card;
        }

        public SettingRow addToggleRow(Context context, int iconRes, int titleRes, int subtitleRes, boolean checked, SettingRow.ToggleListener listener, Theme.ResourcesProvider provider) {
            SettingRow row = new SettingRow(context, true, provider);
            row.bindToggle(iconRes, titleRes, subtitleRes, checked, listener);
            card.addView(row, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));
            refreshDividers();
            return row;
        }

        public SettingRow addActionRow(Context context, int iconRes, int titleRes, int subtitleRes, View.OnClickListener click, Theme.ResourcesProvider provider) {
            SettingRow row = new SettingRow(context, false, provider);
            row.bindAction(iconRes, titleRes, subtitleRes, click);
            card.addView(row, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));
            refreshDividers();
            return row;
        }

        public void addCustomRow(View view) {
            card.addView(view, LayoutHelper.createLinear(LayoutHelper.MATCH_PARENT, LayoutHelper.WRAP_CONTENT));
            refreshDividers();
        }

        private void refreshDividers() {
            int count = card.getChildCount();
            for (int i = 0; i < count; i++) {
                View child = card.getChildAt(i);
                if (child instanceof SettingRow) {
                    ((SettingRow) child).setDividerVisible(i < count - 1);
                }
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════════════
    // فوتر — امضای برند
    // ═══════════════════════════════════════════════════════════════════════
    public static View createFooter(Context context, Theme.ResourcesProvider provider, View.OnClickListener onGitHub) {
        LinearLayout footer = new LinearLayout(context);
        footer.setOrientation(LinearLayout.VERTICAL);
        footer.setGravity(Gravity.CENTER_HORIZONTAL);
        footer.setPadding(0, AndroidUtilities.dp(22), 0, AndroidUtilities.dp(18));

        ImageView gem = new ImageView(context);
        gem.setImageResource(R.drawable.amber_gem);
        footer.addView(gem, LayoutHelper.createLinear(30, 30, Gravity.CENTER_HORIZONTAL));

        TextView crafted = new TextView(context);
        crafted.setTypeface(AndroidUtilities.bold());
        crafted.setTextSize(13);
        crafted.setGravity(Gravity.CENTER);
        ThemeBind.textColor(crafted, Theme.key_windowBackgroundWhiteGrayText2, provider);
        crafted.setText(LocaleController.getString(R.string.AmberFooterCrafted));
        footer.addView(crafted, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, 0, 8, 0, 1, 0));

        TextView version = new TextView(context);
        version.setTextSize(12);
        version.setGravity(Gravity.CENTER);
        ThemeBind.textColor(version, Theme.key_windowBackgroundWhiteGrayText3, provider);
        version.setText(LocaleController.formatString(R.string.AmberVersionFormat, org.telegram.messenger.BuildVars.BUILD_VERSION_STRING));
        footer.addView(version, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT));

        TextView github = new TextView(context);
        github.setTypeface(AndroidUtilities.bold());
        github.setTextSize(12.5f);
        github.setGravity(Gravity.CENTER);
        ThemeBind.textColor(github, Theme.key_windowBackgroundWhiteBlueText, provider);
        github.setText("GitHub · Soroushchq/amber");
        github.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(8), AndroidUtilities.dp(14), AndroidUtilities.dp(8));
        github.setBackground(Theme.createSelectorDrawable(Theme.getColor(Theme.key_listSelector, provider)));
        github.setOnClickListener(onGitHub);
        footer.addView(github, LayoutHelper.createLinear(LayoutHelper.WRAP_CONTENT, LayoutHelper.WRAP_CONTENT, 0, 6, 0, 0));

        return footer;
    }
}

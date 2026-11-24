package org.telegram.ui.Components;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RadialGradient;
import android.graphics.RectF;
import android.graphics.Shader;
import android.view.HapticFeedbackConstants;
import android.view.MotionEvent;
import android.view.View;

import org.telegram.messenger.AmberThemeFX;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.AmberTokens;
import org.telegram.ui.ActionBar.Theme;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

/**
 * AmberGram round 21 — «انیمیشن امضای هر تم».
 *
 * یک نوار شفاف در پایین صفحهٔ اصلی که هر خانوادهٔ برند، صحنهٔ زندهٔ اختصاصی خودش را
 * روی آن اجرا می‌کند. همهٔ اجزا با Canvas خام رسم می‌شوند — بدون هیچ asset تازه:
 *
 *   FX_MARIO    — کاراکتر پیکسل‌آرتی ماریو: ایست → راه‌رفتن عرض صفحه (سه فریم) →
 *                 پرش اسکواش-استرچ + سکهٔ چرخان؛ شبا زمین آجری، روز چمن
 *   FX_AURORA   — دو روبان شفق قطبی موج‌دار + ستاره‌های چشمک‌زن + شهاب‌سنگ دوره‌ای
 *   FX_PREMIERE — نورافکن سینما جارو می‌کند + قرص فیلم غلتان + نوار فیلم متحرک
 *   FX_SLING    — تیرکمان: کشش کشبان و پرتاب کرهٔ پرنده (نایت‌رید: نئون + پینگ رادار)
 *   FX_SW       — میدان ستاره‌ای پارالاکس + شمشیر نور قرمز (تاریک) / آبی (روشن)
 *   FX_HARMONY  — حلقه‌های موج نفس‌گیر + حباب‌های شناور ملایم
 *   FX_AMBER    — هالهٔ کهربایی تنفس‌کننده + اخگرهای بالارونده + جرقهٔ مداری
 *
 * پس‌زمینه کاملاً شفاف می‌ماند تا ردیف‌های لیست زیرش دیده شوند؛ فقط اجزای امضا
 * با آلفای ملایم رسم می‌شوند. لمس فقط وقتی روی ناحیهٔ امضای فعال است مصرف می‌شود
 * و بقیهٔ لمس‌ها به لیست/دکمهٔ شناور زیرین عبور داده می‌شوند.
 */
public class AmberMascotView extends View {

    public static final int FX_AMBER = 0;
    public static final int FX_AURORA = 1;
    public static final int FX_PREMIERE = 2;
    public static final int FX_MARIO = 3;
    public static final int FX_SLING = 4;
    public static final int FX_SW = 5;
    public static final int FX_HARMONY = 6;

    private static final String[] DARK_NAMES = {
        "Night", "Dark Blue", "Amber", "Monet Dark", "Monet AMOLED"
    };

    private final boolean rtl;
    private final float dp;
    private final Random random = new Random();

    private long tStart;
    private long lastFrame;
    private boolean watching;
    private boolean wasEnabled = true;
    private boolean touchActive;

    private int family = -1;
    private boolean night;

    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint paintNoAA = new Paint();
    private final Path path = new Path();
    private final Path path2 = new Path();
    private final RectF hitRect = new RectF();
    private final RectF rect = new RectF();

    // ── شیدرهای کش‌شده (با تغییر خانواده/شب‌روز/اندازه بازسازی می‌شوند) ──
    private Paint washPaint;
    private Paint glowPaint;
    private boolean shadersDirty = true;

    // ── وضعیت ماریو ──
    private static final int M_IDLE = 0, M_WALK = 1, M_JUMP = 2;
    private int marioState = M_IDLE;
    private long marioStateUntil;
    private long nextWalkAt;
    private float marioX;
    private int marioDir = 1;
    private float walkFromX, walkToX, walkProgress, walkDuration;
    private float jumpT;
    private float jumpStartX, jumpEndX;
    private boolean coinSpawned;
    private float groundY;

    // ── وضعیت شهاب آورورا ──
    private float shootingT = -1f;
    private float shootingX, shootingY;
    private long nextShootingAt;

    // ── وضعیت سینگ‌شات ──
    private static final int S_IDLE = 0, S_PULL = 1, S_FLY = 2;
    private int slingState = S_IDLE;
    private long slingStateAt;
    private long nextShotAt;
    private float birdX, birdY, birdVx, birdVy;

    // ── وضعیت شمشیر نور ──
    private float saberBoost;

    // ── وضعیت پالس هارمونی ──
    private float harmonyPulse = -1f;
    private float harmonyPulseX, harmonyPulseY;

    // ── زمان‌سنج‌های تولید ذره ──
    private long nextEmberAt;
    private long nextBubbleAt;
    private long nextReelSparkAt;
    private float reelAngle;

    // ── ذرات عمومی ──
    private static final int P_EMBER = 0, P_SPARK = 1, P_COIN = 2, P_BUBBLE = 3, P_TRAIL = 4, P_STAR_DUST = 5;

    private static class Particle {
        float x, y, vx, vy, life, max, size;
        int color;
        int kind;
        float seed;
    }

    private final ArrayList<Particle> particles = new ArrayList<>();

    private final Runnable ticker = new Runnable() {
        @Override
        public void run() {
            if (!watching) {
                return;
            }
            boolean enabledNow = AmberThemeFX.enabled();
            if (enabledNow) {
                invalidate();
            } else if (wasEnabled) {
                // خاموش‌شدن تازهٔ سوییچ — یک فریم برای پاک‌کردن صحنه
                invalidate();
            }
            wasEnabled = enabledNow;
            postDelayed(this, 32);
        }
    };

    public AmberMascotView(Context context) {
        super(context);
        rtl = LocaleController.isRTL;
        dp = context.getResources().getDisplayMetrics().density;
        setWillNotDraw(false);
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
        tStart = System.currentTimeMillis();
        nextWalkAt = tStart + 3500L;
        nextShootingAt = tStart + 2500L;
        nextShotAt = tStart + 2200L;
        nextEmberAt = tStart + 400L;
        nextBubbleAt = tStart + 900L;
        nextReelSparkAt = tStart + 1200L;
    }

    public void startWatching() {
        if (watching) {
            return;
        }
        watching = true;
        lastFrame = 0;
        removeCallbacks(ticker);
        post(ticker);
    }

    public void stopWatching() {
        watching = false;
        removeCallbacks(ticker);
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        shadersDirty = true;
        placeMarioAtCorner();
    }

    @Override
    protected void onDetachedFromWindow() {
        stopWatching();
        super.onDetachedFromWindow();
    }

    @Override
    protected void onAttachedToWindow() {
        super.onAttachedToWindow();
        if (isShown()) {
            startWatching();
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // خانوادهٔ فعال و واریانت شب/روز
    // ─────────────────────────────────────────────────────────────────────────

    private int resolveFamily() {
        if (Theme.currentThemeIsMario()) {
            return FX_MARIO;
        } else if (Theme.currentThemeIsAurora()) {
            return FX_AURORA;
        } else if (Theme.currentThemeIsPremiere()) {
            return FX_PREMIERE;
        } else if (Theme.currentThemeIsSling()) {
            return FX_SLING;
        } else if (Theme.currentThemeIsStarWars()) {
            return FX_SW;
        } else if (Theme.currentThemeIsHarmony()) {
            return FX_HARMONY;
        }
        return FX_AMBER;
    }

    private boolean resolveNight(int familyValue) {
        String name = Theme.getCurrentTheme() != null ? Theme.getCurrentTheme().name : null;
        if (name == null) {
            return false;
        }
        switch (familyValue) {
            case FX_MARIO:
                // «Mario» در فهرست تیره‌های Theme است؛ «Mario Day» روز
                return "Mario".equals(name);
            case FX_SW:
                return "Dark Side".equals(name);
            case FX_SLING:
                return "Night Raid".equals(name);
            case FX_AURORA:
                return "Aurora".equals(name);
            case FX_PREMIERE:
                return "Premiere".equals(name);
            case FX_HARMONY:
                return "Harmony".equals(name);
            default:
                for (String dark : DARK_NAMES) {
                    if (dark.equals(name)) {
                        return true;
                    }
                }
                return false;
        }
    }

    private void onFamilySwitched() {
        particles.clear();
        placeMarioAtCorner();
        marioState = M_IDLE;
        marioStateUntil = 0;
        nextWalkAt = System.currentTimeMillis() + 3000L;
        slingState = S_IDLE;
        nextShotAt = System.currentTimeMillis() + 2500L;
        shootingT = -1f;
        nextShootingAt = System.currentTimeMillis() + 2500L;
        saberBoost = 0f;
        harmonyPulse = -1f;
        reelAngle = 0f;
    }

    private void placeMarioAtCorner() {
        final int w = getWidth();
        if (w <= 0) {
            return;
        }
        marioX = rtl ? w - 40f * dp : 40f * dp;
        marioDir = rtl ? -1 : 1;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // شیدرها
    // ─────────────────────────────────────────────────────────────────────────

    private void ensureShaders() {
        if (!shadersDirty && washPaint != null) {
            return;
        }
        final int w = getWidth();
        final int h = getHeight();
        if (w <= 0 || h <= 0) {
            return;
        }
        shadersDirty = false;

        int top, bottom, glowColor;
        switch (family) {
            case FX_AURORA:
                top = night ? 0x55070A10 : 0x33E9F6EF;
                bottom = 0x00070A10;
                glowColor = night ? AmberTokens.AURORA_NIGHT_ACCENT : AmberTokens.AURORA_DAY_ACCENT_BRIGHT;
                break;
            case FX_PREMIERE:
                top = 0x441A1016;
                bottom = 0x001A1016;
                glowColor = night ? AmberTokens.PREMIERE_NIGHT_ACCENT : AmberTokens.PREMIERE_DAY_ACCENT_BRIGHT;
                break;
            case FX_SLING:
                top = night ? 0x440E2430 : 0x22F4FAFF;
                bottom = 0x000E2430;
                glowColor = night ? AmberTokens.SLING_NIGHT_ACCENT : AmberTokens.SLING_DAY_ACCENT_BRIGHT;
                break;
            case FX_SW:
                top = night ? 0x5505070D : 0x22F6F3E7;
                bottom = 0x0005070D;
                glowColor = night ? AmberTokens.SW_NIGHT_ACCENT_BRIGHT : AmberTokens.SW_DAY_ACCENT_BRIGHT;
                break;
            case FX_HARMONY:
                top = night ? 0x330D0E1A : 0x22F4F5FB;
                bottom = 0x000D0E1A;
                glowColor = night ? AmberTokens.HARMONY_NIGHT_ACCENT_BRIGHT : AmberTokens.HARMONY_DAY_ACCENT_BRIGHT;
                break;
            case FX_MARIO:
                top = 0x00000000;
                bottom = 0x00000000;
                glowColor = night ? AmberTokens.MARIO_NIGHT_ACCENT : AmberTokens.MARIO_DAY_ACCENT;
                break;
            default:
                top = night ? 0x3317130E : 0x22FFF3E4;
                bottom = 0x0017130E;
                glowColor = night ? AmberTokens.NIGHT_ACCENT_BRIGHT : AmberTokens.DAY_ACCENT_BRIGHT;
                break;
        }
        washPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        washPaint.setShader(new LinearGradient(0, 0, 0, h, top, bottom, Shader.TileMode.CLAMP));
        glowPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        float radius = 56f * dp;
        int glowInner = (glowColor & 0x00FFFFFF) | (night ? 0x5A000000 : 0x4A000000);
        glowPaint.setShader(new RadialGradient(
            glowX(w), h - 18f * dp, radius,
            new int[]{glowInner, (glowInner & 0x00FFFFFF), 0x00000000},
            new float[]{0f, 0.55f, 1f}, Shader.TileMode.CLAMP));
    }

    private float glowX(int w) {
        return rtl ? w - 64f * dp : 64f * dp;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // حلقهٔ رسم
    // ─────────────────────────────────────────────────────────────────────────

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (getWidth() <= 0 || getHeight() <= 0) {
            return;
        }
        long now = System.currentTimeMillis();
        float dt = lastFrame == 0 ? 32f : Math.min(100f, now - lastFrame);
        lastFrame = now;
        float t = (now - tStart) / 1000f;

        int newFamily = resolveFamily();
        boolean newNight = resolveNight(newFamily);
        if (newFamily != family || newNight != night) {
            family = newFamily;
            night = newNight;
            shadersDirty = true;
            onFamilySwitched();
        }

        if (!AmberThemeFX.enabled()) {
            return;
        }

        ensureShaders();
        if (washPaint != null) {
            canvas.drawRect(0, 0, getWidth(), getHeight(), washPaint);
        }

        hitRect.setEmpty();
        switch (family) {
            case FX_MARIO:
                drawMario(canvas, t, dt);
                break;
            case FX_AURORA:
                drawAurora(canvas, t, dt);
                break;
            case FX_PREMIERE:
                drawPremiere(canvas, t, dt);
                break;
            case FX_SLING:
                drawSling(canvas, t, dt);
                break;
            case FX_SW:
                drawStarWars(canvas, t, dt);
                break;
            case FX_HARMONY:
                drawHarmony(canvas, t, dt);
                break;
            default:
                drawAmber(canvas, t, dt);
                break;
        }
        drawParticles(canvas, dt);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // ماریو — اسپرایت پیکسل‌آرتی
    // ─────────────────────────────────────────────────────────────────────────

    private static final int PIXEL_MARIO_R = 0xFFE43B30; // کلاهک و پیراهن
    private static final int PIXEL_MARIO_B = 0xFF2E63D4; // سرهمی
    private static final int PIXEL_MARIO_S = 0xFFFFC7A0; // پوست
    private static final int PIXEL_MARIO_N = 0xFF6B3E12; // مو و کفش
    private static final int PIXEL_MARIO_Y = 0xFFFBD000; // دکمه‌ها
    private static final int COIN_BODY = 0xFFFBD000;
    private static final int COIN_RING = 0xFFC89B00;

    private static final String[] SPRITE_STAND = {
        "....RRRRR...",
        "...RRRRRRRR.",
        "...NNNSSKS..",
        "..NSNSSSKSS.",
        "..NSNNSSSSS.",
        "..NNSSSSKKK.",
        "....SSSSS...",
        "...RRBRRR...",
        "..RRRBRRBRR.",
        ".RRRRBBBBRR.",
        ".SSRBYBBYBRS",
        ".SSSBBBBBBSS",
        ".SSBBBBBBBB.",
        "...BBB..BBB.",
        "..NNNN..NNN.",
        ".NNNN....NNN"
    };

    private static final String[] SPRITE_WALK1 = {
        "....RRRRR...",
        "...RRRRRRRR.",
        "...NNNSSKS..",
        "..NSNSSSKSS.",
        "..NSNNSSSSS.",
        "..NNSSSSKKK.",
        "....SSSSS...",
        "..SRRBRRRS..",
        ".SRRRBRRBRS.",
        "..RRRBBBBRR.",
        "..SRBYBBYBRS",
        "..SSBBBBBBSS",
        "..SBBBBBBBB.",
        "..BBBBBBBN..",
        ".NNNNN..NN..",
        ".NNN.....NNN"
    };

    private static final String[] SPRITE_WALK2 = {
        "....RRRRR...",
        "...RRRRRRRR.",
        "...NNNSSKS..",
        "..NSNSSSKSS.",
        "..NSNNSSSSS.",
        "..NNSSSSKKK.",
        "....SSSSS...",
        "..RRBRRRS...",
        ".RRRBRRBRRS.",
        "RRRRBBBBRR..",
        "SSRBYBBYBRS.",
        "SSSBBBBBBSS.",
        ".SBBBBBBBB..",
        ".BBB...BBB..",
        "NNNN.....NNN",
        "NNN.......NN"
    };

    private static final String[] SPRITE_JUMP = {
        "....RRRRR..S",
        "...RRRRRRRRS",
        "...NNNSSKS.S",
        "..NSNSSSKSS.",
        "..NSNNSSSSS.",
        "..NNSSSSKKK.",
        "....SSSSS...",
        "...RRBRRRS..",
        "..RRRBRRBRR.",
        ".RRRRBBBBRR.",
        ".SSRBYBBYBRS",
        ".SSSBBBBBBSS",
        "..SBBBBBBBB.",
        "..BBBBBBBB..",
        "..NNNN.BNN..",
        "..NNN......."
    };

    private static int marioPixelColor(char c) {
        switch (c) {
            case 'R': return PIXEL_MARIO_R;
            case 'B': return PIXEL_MARIO_B;
            case 'S': return PIXEL_MARIO_S;
            case 'N': return PIXEL_MARIO_N;
            case 'Y': return PIXEL_MARIO_Y;
            default: return 0;
        }
    }

    private void drawMarioSprite(Canvas canvas, String[] sprite, float centerX, float baselineY, float sx, float sy, int dir) {
        final float p = 3f * dp;
        final int cols = sprite[0].length();
        final int rows = sprite.length;
        final float totalW = cols * p * sx;
        final float totalH = rows * p * sy;
        final float left = centerX - totalW / 2f;
        final float top = baselineY - totalH;
        for (int r = 0; r < rows; r++) {
            String row = sprite[r];
            for (int c = 0; c < cols; c++) {
                char cell = dir < 0 ? row.charAt(cols - 1 - c) : row.charAt(c);
                int color = marioPixelColor(cell);
                if (color == 0) {
                    continue;
                }
                paint.setColor(color);
                canvas.drawRect(left + c * p * sx, top + r * p * sy, left + (c + 1) * p * sx, top + (r + 1) * p * sy, paint);
            }
        }
        // ناحیهٔ لمس — همیشه با فریم استاندارد محاسبه می‌شود
        hitRect.set(left - 8f * dp, top - 8f * dp, left + totalW + 8f * dp, baselineY + 6f * dp);
    }

    private void drawMarioGround(Canvas canvas, float t) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        if (night) {
            // زیرزمینی — آجر آبی بریکی
            paintNoAA.setColor(0xFF1B2A55);
            canvas.drawRect(0, groundY, w, h, paintNoAA);
            paintNoAA.setColor(0xFF0D1226);
            float bw = 14f * dp;
            float offset = (t * 6f * dp) % (bw * 2f);
            for (float x = -bw * 2f + offset; x < w + bw; x += bw) {
                canvas.drawRect(x, groundY, x + 1.5f * dp, h, paintNoAA);
                canvas.drawRect(x - bw / 2f, groundY + groundH / 2f, x - bw / 2f + 1.5f * dp, h, paintNoAA);
            }
            canvas.drawRect(0, groundY, w, groundY + 1f * dp, paintNoAA);
        } else {
            // دنیای روز — چمن + خاک
            paintNoAA.setColor(0xFF7CCB4C);
            canvas.drawRect(0, groundY, w, groundY + 3f * dp, paintNoAA);
            paintNoAA.setColor(0xFFA05A2C);
            canvas.drawRect(0, groundY + 3f * dp, w, h, paintNoAA);
            paintNoAA.setColor(0xFF8A4820);
            float offset = (t * 6f * dp) % (12f * dp);
            for (float x = -12f * dp + offset; x < w + 12f * dp; x += 12f * dp) {
                canvas.drawRect(x, groundY + 4.5f * dp, x + 3f * dp, groundY + 6f * dp, paintNoAA);
            }
        }
    }

    private void drawMario(Canvas canvas, float t, float dt) {
        final long now = System.currentTimeMillis();
        final int w = getWidth();
        drawMarioGround(canvas, t);

        float sx = 1f, sy = 1f, bobY = 0f;
        String[] sprite = SPRITE_STAND;

        switch (marioState) {
            case M_IDLE: {
                bobY = (float) Math.sin(t * 2.4) * 1.4f * dp;
                if (now >= nextWalkAt) {
                    // شروع یک پیاده‌روی عرض صفحه به سمت گوشهٔ مقابل
                    float target = rtl ? 40f * dp : w - 40f * dp;
                    if (Math.abs(target - marioX) < 8f * dp) {
                        target = rtl ? w - 40f * dp : 40f * dp;
                    }
                    walkFromX = marioX;
                    walkToX = target;
                    marioDir = walkToX > walkFromX ? 1 : -1;
                    walkDuration = Math.max(900f, Math.abs(walkToX - walkFromX) / (70f * dp) * 1000f);
                    walkProgress = 0f;
                    marioState = M_WALK;
                    marioStateUntil = now + (long) walkDuration;
                }
                break;
            }
            case M_WALK: {
                walkProgress = Math.min(1f, walkProgress + dt / walkDuration);
                marioX = walkFromX + (walkToX - walkFromX) * easeInOut(walkProgress);
                long frameMs = 140L;
                int frame = (int) ((now / frameMs) % 3);
                sprite = frame == 1 ? SPRITE_WALK1 : frame == 2 ? SPRITE_WALK2 : SPRITE_STAND;
                bobY = -Math.abs((float) Math.sin(walkProgress * Math.PI * 7f)) * 2.2f * dp;
                if (now >= marioStateUntil || walkProgress >= 1f) {
                    marioX = walkToX;
                    marioState = M_IDLE;
                    nextWalkAt = now + 6500L + random.nextInt(5000L);
                }
                break;
            }
            case M_JUMP: {
                jumpT = Math.min(1f, jumpT + dt / 620f);
                marioX = jumpStartX + (jumpEndX - jumpStartX) * Math.min(1f, jumpT * 1.3f);
                if (jumpT < 0.18f) {
                    float k = jumpT / 0.18f;
                    sy = 1f - 0.22f * k;
                    sx = 1f + 0.18f * k;
                } else if (jumpT < 0.85f) {
                    float k = (jumpT - 0.18f) / 0.67f;
                    float arc = (float) Math.sin(Math.PI * k);
                    bobY = -44f * dp * arc;
                    sy = 1f + 0.14f * arc;
                    sx = 1f - 0.10f * arc;
                    if (!coinSpawned && k >= 0.45f) {
                        coinSpawned = true;
                        spawnCoin(marioX, getHeight() - 8f * dp - 16 * 3f * dp - bobY);
                    }
                } else {
                    float k = (jumpT - 0.85f) / 0.15f;
                    sy = 1f - 0.16f * (1f - k);
                    sx = 1f + 0.14f * (1f - k);
                }
                sprite = SPRITE_JUMP;
                if (jumpT >= 1f) {
                    marioState = M_IDLE;
                    nextWalkAt = now + 5000L + random.nextInt(5000L);
                }
                break;
            }
        }

        drawMarioSprite(canvas, sprite, marioX, groundY + bobY, sx, sy, marioDir);
    }

    private void spawnCoin(float x, float y) {
        Particle p = new Particle();
        p.x = x;
        p.y = y;
        p.vx = 0f;
        p.vy = -42f * dp;
        p.life = 0f;
        p.max = 900f;
        p.size = 4.5f * dp;
        p.color = COIN_BODY;
        p.kind = P_COIN;
        p.seed = random.nextFloat();
        particles.add(p);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // آورورا — شفق قطبی
    // ─────────────────────────────────────────────────────────────────────────

    private static final int AURORA_STAR_COUNT = 46;
    private final float[] starFx = new float[AURORA_STAR_COUNT];
    private final float[] starFy = new float[AURORA_STAR_COUNT];
    private final float[] starPhase = new float[AURORA_STAR_COUNT];
    private boolean starsInit;

    private void initStars() {
        for (int i = 0; i < AURORA_STAR_COUNT; i++) {
            starFx[i] = random.nextFloat();
            starFy[i] = random.nextFloat() * 0.7f;
            starPhase[i] = random.nextFloat() * 6.28f;
        }
        starsInit = true;
    }

    private void drawAurora(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        if (!starsInit) {
            initStars();
        }
        int accent = night ? AmberTokens.AURORA_NIGHT_ACCENT : AmberTokens.AURORA_DAY_ACCENT_BRIGHT;
        int accentBright = night ? AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT : AmberTokens.AURORA_DAY_ACCENT;

        // ستاره‌ها
        paint.setStrokeWidth(2f * dp);
        paint.setStrokeCap(Paint.Cap.ROUND);
        for (int i = 0; i < AURORA_STAR_COUNT; i++) {
            float tw = 0.35f + 0.65f * (0.5f + 0.5f * (float) Math.sin(t * 2.1f + starPhase[i]));
            paint.setColor((accentBright & 0x00FFFFFF) | ((int) (255 * tw) << 24));
            canvas.drawPoint(starFx[i] * w, starFy[i] * h, paint);
        }

        // دو روبان شفق
        drawAuroraRibbon(canvas, t, w, h, 0.42f, 0.06f, 1.1f, accent, 0.55f);
        drawAuroraRibbon(canvas, t, w, h, 0.52f, -0.04f, 0.8f, 0xFF9D5CF0, 0.38f);

        // شهاب‌سنگ دوره‌ای
        long now = System.currentTimeMillis();
        if (shootingT < 0f && now >= nextShootingAt) {
            shootingT = 0f;
            shootingX = w * (0.25f + random.nextFloat() * 0.5f);
            shootingY = h * 0.12f;
        }
        if (shootingT >= 0f) {
            shootingT += dt / 800f;
            float px = shootingX + shootingT * 150f * dp;
            float py = shootingY + shootingT * 90f * dp;
            paint.setColor((accentBright & 0x00FFFFFF) | 0xB3000000);
            paint.setStrokeWidth(1.6f * dp);
            canvas.drawLine(px, py, px - 26f * dp, py - 15f * dp, paint);
            paint.setColor((accentBright & 0x00FFFFFF) | 0x33000000);
            canvas.drawLine(px - 26f * dp, py - 15f * dp, px - 52f * dp, py - 30f * dp, paint);
            if (shootingT >= 1f) {
                shootingT = -1f;
                nextShootingAt = now + 5500L + random.nextInt(5000L);
            }
        }

        // خط نور زمین
        paint.setColor((accent & 0x00FFFFFF) | 0x77000000);
        canvas.drawRect(0, groundY, w, groundY + 1.5f * dp, paint);
        paint.setColor((accentBright & 0x00FFFFFF) | 0x22000000);
        canvas.drawRect(0, groundY + 1.5f * dp, w, groundY + 4f * dp, paint);
        hitRect.set(glowX(w) - 24f * dp, groundY - 40f * dp, glowX(w) + 24f * dp, groundY + 4f * dp);
    }

    private void drawAuroraRibbon(Canvas canvas, float t, int w, int h, float baseY, float amp, float speed, int color, float alphaScale) {
        final float step = 14f * dp;
        path.reset();
        boolean first = true;
        for (float x = -step; x <= w + step; x += step) {
            float y = h * baseY
                + (float) Math.sin((x / w) * 3.4f + t * speed) * 9f * dp
                + (float) Math.sin((x / w) * 8.1f + t * speed * 1.7f) * 4f * dp;
            if (first) {
                path.moveTo(x, y);
                first = false;
            } else {
                path.lineTo(x, y);
            }
        }
        float ribbonH = 30f * dp;
        for (float x = w + step; x >= -step; x -= step) {
            float y = h * baseY
                + (float) Math.sin((x / w) * 3.4f + t * speed) * 9f * dp
                + (float) Math.sin((x / w) * 8.1f + t * speed * 1.7f) * 4f * dp;
            path.lineTo(x, y + ribbonH);
        }
        path.close();
        int a = (int) (90f * alphaScale * (0.7f + 0.3f * (float) Math.sin(t * 1.4f + baseY * 9f)));
        paint.setColor((color & 0x00FFFFFF) | (a << 24));
        canvas.drawPath(path, paint);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // پریمیر — سینما
    // ─────────────────────────────────────────────────────────────────────────

    private void drawPremiere(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        int accent = night ? AmberTokens.PREMIERE_NIGHT_ACCENT : AmberTokens.PREMIERE_DAY_ACCENT_BRIGHT;

        // نورافکن جاروکننده
        float cx = w * (0.5f + 0.42f * (float) Math.sin(t * 0.5f));
        path.reset();
        path.moveTo(cx, h * 0.18f);
        path.lineTo(cx - 64f * dp, groundY);
        path.lineTo(cx + 64f * dp, groundY);
        path.close();
        paint.setColor(0x14FFF6DC);
        canvas.drawPath(path, paint);
        paint.setColor(0x0AFFEEC0);
        canvas.drawCircle(cx, groundY, 40f * dp, paint);

        // نوار فیلم روی زمین
        paintNoAA.setColor(0xFF171020);
        canvas.drawRect(0, groundY, w, groundY + 3f * dp, paintNoAA);
        paintNoAA.setColor((accent & 0x00FFFFFF) | 0x66000000);
        float period = 16f * dp;
        float offset = (t * 22f * dp) % period;
        for (float x = -period + offset; x < w + period; x += period) {
            canvas.drawRect(x, groundY, x + 5f * dp, groundY + 3f * dp, paintNoAA);
        }

        // قرص فیلم غلتان
        float reelX = rtl ? w - 34f * dp : 34f * dp;
        float reelY = groundY - 14f * dp;
        reelAngle += dt / 1000f * 2.6f;
        paint.setColor(0xFF26222E);
        canvas.drawCircle(reelX, reelY, 13f * dp, paint);
        paint.setColor((accent & 0x00FFFFFF) | 0xCC000000);
        canvas.drawCircle(reelX, reelY, 13f * dp, paint);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(1.2f * dp);
        paint.setColor((accent & 0x00FFFFFF) | 0x88000000);
        canvas.drawCircle(reelX, reelY, 13f * dp, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(0xFF15121B);
        for (int i = 0; i < 4; i++) {
            double ang = reelAngle + i * Math.PI / 2f;
            float hx = reelX + (float) Math.cos(ang) * 6.5f * dp;
            float hy = reelY + (float) Math.sin(ang) * 6.5f * dp;
            canvas.drawCircle(hx, hy, 2.6f * dp, paint);
        }
        paint.setColor(0xFF3A3444);
        canvas.drawCircle(reelX, reelY, 1.8f * dp, paint);

        // جرقه‌های نورافکن
        long now = System.currentTimeMillis();
        if (now >= nextReelSparkAt) {
            nextReelSparkAt = now + 500L + random.nextInt(900L);
            spawnSpark(cx + (random.nextFloat() - 0.5f) * 90f * dp, h * 0.3f + random.nextFloat() * 20f * dp, accent, 0.5f);
        }

        hitRect.set(reelX - 22f * dp, reelY - 22f * dp, reelX + 22f * dp, reelY + 22f * dp);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // سینگ‌شات / نایت‌رید — تیرکمان
    // ─────────────────────────────────────────────────────────────────────────

    private void drawSling(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        int accent = night ? AmberTokens.SLING_NIGHT_ACCENT : AmberTokens.SLING_DAY_ACCENT;
        int accentBright = night ? AmberTokens.SLING_NIGHT_ACCENT_BRIGHT : AmberTokens.SLING_DAY_ACCENT_BRIGHT;
        long now = System.currentTimeMillis();

        // خط زمین
        if (night) {
            paintNoAA.setColor(0xFF0B1D27);
        } else {
            paintNoAA.setColor(0xFF9BCB62);
        }
        canvas.drawRect(0, groundY, w, h, paintNoAA);

        // پینگ رادار نایت‌رید
        if (night) {
            for (int i = 0; i < 2; i++) {
                float phase = ((t * 0.5f) + i * 0.5f) % 1f;
                paint.setColor((accent & 0x00FFFFFF) | ((int) (90f * (1f - phase)) << 24));
                paint.setStyle(Paint.Style.STROKE);
                paint.setStrokeWidth(1.2f * dp);
                canvas.drawCircle(slingBaseX(w), groundY - 4f * dp, 10f * dp + phase * 26f * dp, paint);
                paint.setStyle(Paint.Style.FILL);
            }
        }

        // تیرکمان
        float bx = slingBaseX(w);
        float topY = groundY - 26f * dp;
        paint.setColor(night ? 0xFF3C5A68 : 0xFF7A4A22);
        paint.setStrokeWidth(3.4f * dp);
        canvas.drawLine(bx, groundY, bx, topY, paint);
        canvas.drawLine(bx, topY, bx - 9f * dp, topY - 7f * dp, paint);
        canvas.drawLine(bx, topY, bx + 9f * dp, topY - 7f * dp, paint);

        // چرخهٔ شلیک
        if (slingState == S_IDLE && now >= nextShotAt) {
            slingState = S_PULL;
            slingStateAt = now;
        }
        float ballX = bx - marioSign() * 4f * dp, ballY = topY - 8f * dp;
        boolean bandToBall = false;
        if (slingState == S_PULL) {
            float p = Math.min(1f, (now - slingStateAt) / 900f);
            float ease = easeInOut(p);
            ballX = bx - marioSign() * (6f + 16f * ease) * dp;
            ballY = topY - 8f * dp + 5f * ease * dp;
            bandToBall = true;
            if (p >= 1f) {
                slingState = S_FLY;
                slingStateAt = now;
                birdX = ballX;
                birdY = ballY;
                birdVx = marioSign() * 260f * dp;
                birdVy = -170f * dp;
            }
        } else if (slingState == S_FLY) {
            float seconds = dt / 1000f;
            birdVy += 420f * dp * seconds;
            birdX += birdVx * seconds;
            birdY += birdVy * seconds;
            spawnTrail(birdX, birdY, accentBright);
            paint.setColor(night ? (accentBright & 0x00FFFFFF) | 0x55000000 : 0x22000000);
            canvas.drawCircle(birdX, birdY, 9f * dp, paint);
            if (birdY > h + 10f * dp || birdX < -20f * dp || birdX > w + 20f * dp) {
                slingState = S_IDLE;
                nextShotAt = now + 2600L + random.nextInt(3400L);
            }
            ballX = birdX;
            ballY = birdY;
        } else {
            // کرهٔ بیکار روی آستانهٔ تیرکمان
            ballX = bx - marioSign() * 6f * dp;
            ballY = topY - 8f * dp;
            bandToBall = true;
        }

        // کشبان
        paint.setColor(night ? 0xFFB7E2E2 : 0xFF5A3818);
        paint.setStrokeWidth(1.6f * dp);
        if (bandToBall) {
            canvas.drawLine(bx - 9f * dp, topY - 7f * dp, ballX, ballY, paint);
            canvas.drawLine(bx + 9f * dp, topY - 7f * dp, ballX, ballY, paint);
        } else {
            canvas.drawLine(bx - 9f * dp, topY - 7f * dp, bx - 4f * dp, topY - 7f * dp, paint);
            canvas.drawLine(bx + 9f * dp, topY - 7f * dp, bx + 4f * dp, topY - 7f * dp, paint);
        }

        // کرهٔ پرنده
        if (slingState != S_FLY || (birdX > -20f * dp && birdX < w + 20f * dp)) {
            paint.setColor(accent);
            canvas.drawCircle(ballX, ballY, 6.5f * dp, paint);
            paint.setColor(accentBright);
            canvas.drawCircle(ballX - 2f * dp, ballY - 2f * dp, 2.2f * dp, paint);
        }

        hitRect.set(bx - 26f * dp, groundY - 42f * dp, bx + 26f * dp, groundY + 4f * dp);
    }

    private float slingBaseX(int w) {
        return rtl ? w - 44f * dp : 44f * dp;
    }

    private int marioSign() {
        return rtl ? -1 : 1;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // سوی تاریک/روشن — میدان ستاره‌ای + شمشیر نور
    // ─────────────────────────────────────────────────────────────────────────

    private static final int SW_STAR_COUNT = 64;
    private final float[] swStarX = new float[SW_STAR_COUNT];
    private final float[] swStarY = new float[SW_STAR_COUNT];
    private final float[] swStarLayer = new float[SW_STAR_COUNT];
    private boolean swStarsInit;

    private void initSwStars() {
        for (int i = 0; i < SW_STAR_COUNT; i++) {
            swStarX[i] = random.nextFloat();
            swStarY[i] = random.nextFloat() * 0.85f;
            swStarLayer[i] = random.nextFloat();
        }
        swStarsInit = true;
    }

    private void drawStarWars(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        if (!swStarsInit) {
            initSwStars();
        }
        boolean darkSide = night;
        int saberColor = darkSide ? 0xFFFF2E3E : 0xFF57A8FF;
        int saberGlow = darkSide ? AmberTokens.SW_NIGHT_ACCENT_BRIGHT : AmberTokens.SW_DAY_ACCENT_BRIGHT;
        float seconds = dt / 1000f;

        // میدان ستاره‌ای با پارالاکس
        for (int i = 0; i < SW_STAR_COUNT; i++) {
            float speed = 0.006f + swStarLayer[i] * 0.02f;
            float x = (swStarX[i] - t * speed) % 1f;
            if (x < 0f) {
                x += 1f;
            }
            float size = 1.2f + swStarLayer[i] * 1.6f;
            paint.setColor(0xE6FFFFFF);
            canvas.drawCircle(x * w, swStarY[i] * h, size * dp * 0.6f, paint);
        }

        // شمشیر نور
        saberBoost = Math.max(0f, saberBoost - seconds);
        float bx = rtl ? w * 0.24f : w * 0.76f;
        float by = groundY - 2f * dp;
        float dirSign = rtl ? -1f : 1f;
        float wave = (float) Math.abs(Math.sin(t * 0.75f));
        float eased = wave * wave;
        float maxLen = w * 0.42f;
        float len = maxLen * (0.30f + 0.62f * eased) + saberBoost * maxLen * 0.2f;
        float angle = -22f * dirSign;

        canvas.save();
        canvas.translate(bx, by);
        canvas.rotate(angle);
        // هالهٔ گسترده
        paint.setColor((saberColor & 0x00FFFFFF) | 0x2E000000);
        rect.set(0, -11f * dp, len, 11f * dp);
        canvas.drawRoundRect(rect, 11f * dp, 11f * dp, paint);
        // هالهٔ میانی
        paint.setColor((saberColor & 0x00FFFFFF) | 0x77000000);
        rect.set(0, -6f * dp, len, 6f * dp);
        canvas.drawRoundRect(rect, 6f * dp, 6f * dp, paint);
        // هستهٔ نور
        paint.setColor((saberGlow & 0x00FFFFFF) | 0xE6000000);
        rect.set(0, -2.4f * dp, len, 2.4f * dp);
        canvas.drawRoundRect(rect, 2.4f * dp, 2.4f * dp, paint);
        // دسته
        paint.setColor(0xFF2E3238);
        rect.set(-15f * dp, -3f * dp, -2f * dp, 3f * dp);
        canvas.drawRoundRect(rect, 1.5f * dp, 1.5f * dp, paint);
        paint.setColor(0xFF565E66);
        canvas.drawRect(-12f * dp, -3f * dp, -10f * dp, 3f * dp, paint);
        canvas.restore();

        // جرقهٔ نوک شمشیر
        double ang = Math.toRadians(angle);
        float tipX = bx + (float) Math.cos(ang) * len;
        float tipY = by + (float) Math.sin(ang) * len;
        if (eased > 0.86f && random.nextFloat() < 0.35f) {
            spawnSpark(tipX, tipY, saberColor, 0.8f);
        }
        paint.setColor((saberColor & 0x00FFFFFF) | 0x33000000);
        canvas.drawCircle(tipX, tipY, 5f * dp, paint);

        // خط زمین ایستگاه
        paint.setColor((saberGlow & 0x00FFFFFF) | 0x55000000);
        canvas.drawRect(0, groundY, w, groundY + 1.5f * dp, paint);

        hitRect.set(bx - 24f * dp, by - 30f * dp, bx + 24f * dp, by + 8f * dp);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // هارمونی — موج‌های نفس‌گیر
    // ─────────────────────────────────────────────────────────────────────────

    private void drawHarmony(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        int accent = night ? AmberTokens.HARMONY_NIGHT_ACCENT : AmberTokens.HARMONY_DAY_ACCENT;
        int accentBright = night ? AmberTokens.HARMONY_NIGHT_ACCENT_BRIGHT : AmberTokens.HARMONY_DAY_ACCENT_BRIGHT;
        long now = System.currentTimeMillis();

        float cx = w / 2f;
        float cy = h * 0.62f;

        // هالهٔ نفس‌گیر (شیدر خودش نوسان آلفا دارد از طریق مرکز شعاعی)
        if (glowPaint != null) {
            paint.setShader(glowPaint.getShader());
            paint.setAlpha((int) (200f + 55f * (float) Math.sin(t * 1.6f)));
            canvas.drawRect(0, 0, w, h, paint);
            paint.setShader(null);
            paint.setAlpha(255);
        }

        // سه حلقهٔ موج
        for (int i = 0; i < 3; i++) {
            float phase = ((t * 0.35f) + i * 0.33f) % 1f;
            float r = phase * 46f * dp + 6f * dp;
            paint.setColor((accent & 0x00FFFFFF) | ((int) (110f * (1f - phase)) << 24));
            paint.setStyle(Paint.Style.STROKE);
            paint.setStrokeWidth(1.6f * dp);
            canvas.drawCircle(cx, cy, r, paint);
            paint.setStyle(Paint.Style.FILL);
        }

        // پالس لمس
        if (harmonyPulse >= 0f) {
            harmonyPulse += dt / 700f;
            float pr = harmonyPulse * 60f * dp;
            paint.setColor((accentBright & 0x00FFFFFF) | ((int) (140f * (1f - harmonyPulse)) << 24));
            paint.setStyle(Paint.Style.STROKE);
            paint.setStrokeWidth(2.4f * dp);
            canvas.drawCircle(harmonyPulseX, harmonyPulseY, pr, paint);
            paint.setStyle(Paint.Style.FILL);
            if (harmonyPulse >= 1f) {
                harmonyPulse = -1f;
            }
        }

        // حباب‌های شناور
        if (now >= nextBubbleAt) {
            nextBubbleAt = now + 700L + random.nextInt(700L);
            Particle p = new Particle();
            p.x = random.nextFloat() * w;
            p.y = h - groundH;
            p.vx = 0f;
            p.vy = -(14f + random.nextFloat() * 12f) * dp;
            p.life = 0f;
            p.max = 3800f;
            p.size = (2.2f + random.nextFloat() * 2.6f) * dp;
            p.color = random.nextBoolean() ? accentBright : accent;
            p.kind = P_BUBBLE;
            p.seed = random.nextFloat() * 6.28f;
            particles.add(p);
        }

        // خط زمین ملایم
        paint.setColor((accent & 0x00FFFFFF) | 0x44000000);
        canvas.drawRect(0, groundY, w, groundY + 1.5f * dp, paint);
        hitRect.set(cx - 30f * dp, cy - 30f * dp, cx + 30f * dp, cy + 30f * dp);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // آمبر (پیش‌فرض) — هالهٔ گرم + اخگر
    // ─────────────────────────────────────────────────────────────────────────

    private void drawAmber(Canvas canvas, float t, float dt) {
        final int w = getWidth();
        final int h = getHeight();
        final float groundH = 8f * dp;
        groundY = h - groundH;
        int accent = night ? AmberTokens.NIGHT_ACCENT : AmberTokens.DAY_ACCENT_BRIGHT;
        int accentBright = night ? AmberTokens.NIGHT_ACCENT_BRIGHT : AmberTokens.DAY_ACCENT_BRIGHT;
        long now = System.currentTimeMillis();
        float gx = glowX(w);
        float gy = groundY - 18f * dp;

        // هالهٔ تنفس‌کننده
        if (glowPaint != null) {
            paint.setShader(glowPaint.getShader());
            paint.setAlpha((int) (200f + 55f * (float) Math.sin(t * 1.8f)));
            canvas.drawRect(0, 0, w, h, paint);
            paint.setShader(null);
            paint.setAlpha(255);
        }

        // جرقه‌های مداری
        for (int i = 0; i < 3; i++) {
            float ang = t * 1.6f + i * 2.09f;
            float ox = gx + (float) Math.cos(ang) * 17f * dp;
            float oy = gy + (float) Math.sin(ang) * 11f * dp;
            paint.setColor((accentBright & 0x00FFFFFF) | 0xB3000000);
            canvas.drawCircle(ox, oy, 1.7f * dp, paint);
        }

        // اخگرهای بالارونده
        if (now >= nextEmberAt) {
            nextEmberAt = now + 300L + random.nextInt(260L);
            Particle p = new Particle();
            p.x = gx + (random.nextFloat() - 0.5f) * 44f * dp;
            p.y = groundY - 2f * dp;
            p.vx = (random.nextFloat() - 0.5f) * 6f * dp;
            p.vy = -(16f + random.nextFloat() * 18f) * dp;
            p.life = 0f;
            p.max = 2600f + random.nextFloat() * 1200f;
            p.size = (1.6f + random.nextFloat() * 2f) * dp;
            p.color = random.nextBoolean() ? accent : accentBright;
            p.kind = P_EMBER;
            p.seed = random.nextFloat() * 6.28f;
            particles.add(p);
        }

        paint.setColor((accent & 0x00FFFFFF) | 0x55000000);
        canvas.drawRect(0, groundY, w, groundY + 1.5f * dp, paint);
        hitRect.set(gx - 26f * dp, gy - 26f * dp, gx + 26f * dp, gy + 26f * dp);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // ذرات
    // ─────────────────────────────────────────────────────────────────────────

    private void spawnSpark(float x, float y, int color, float speed) {
        Particle p = new Particle();
        p.x = x;
        p.y = y;
        double ang = random.nextDouble() * Math.PI * 2f;
        float v = (30f + random.nextFloat() * 50f) * dp * speed;
        p.vx = (float) Math.cos(ang) * v;
        p.vy = (float) Math.sin(ang) * v;
        p.life = 0f;
        p.max = 500f + random.nextFloat() * 400f;
        p.size = (1.4f + random.nextFloat() * 1.6f) * dp;
        p.color = color;
        p.kind = P_SPARK;
        p.seed = 0f;
        particles.add(p);
    }

    private void spawnTrail(float x, float y, int color) {
        if (particles.size() > 80) {
            return;
        }
        Particle p = new Particle();
        p.x = x;
        p.y = y;
        p.vx = 0f;
        p.vy = 0f;
        p.life = 0f;
        p.max = 420f;
        p.size = 2.4f * dp;
        p.color = color;
        p.kind = P_TRAIL;
        p.seed = 0f;
        particles.add(p);
    }

    private void spawnBurst(float x, float y, int color, int count) {
        for (int i = 0; i < count; i++) {
            spawnSpark(x, y, random.nextBoolean() ? color : lighten(color), 1.1f);
        }
    }

    private static int lighten(int color) {
        int r = Math.min(255, ((color >> 16) & 0xFF) + 60);
        int g = Math.min(255, ((color >> 8) & 0xFF) + 60);
        int b = Math.min(255, (color & 0xFF) + 60);
        return 0xFF000000 | (r << 16) | (g << 8) | b;
    }

    private void drawParticles(Canvas canvas, float dt) {
        float seconds = dt / 1000f;
        Iterator<Particle> it = particles.iterator();
        while (it.hasNext()) {
            Particle p = it.next();
            p.life += dt;
            if (p.life >= p.max) {
                it.remove();
                continue;
            }
            float k = p.life / p.max;
            switch (p.kind) {
                case P_EMBER:
                case P_STAR_DUST:
                    p.x += p.vx * seconds + (float) Math.sin(p.life / 260f + p.seed) * 0.4f * dp;
                    p.y += p.vy * seconds;
                    break;
                case P_SPARK:
                case P_TRAIL:
                    p.x += p.vx * seconds;
                    p.y += p.vy * seconds;
                    if (p.kind == P_SPARK) {
                        p.vy += 120f * dp * seconds;
                    }
                    break;
                case P_BUBBLE:
                    p.x += (float) Math.sin(p.life / 420f + p.seed) * 0.5f * dp;
                    p.y += p.vy * seconds;
                    break;
                case P_COIN:
                    p.y += p.vy * seconds;
                    p.vy += 40f * dp * seconds;
                    break;
            }
            int alpha;
            if (p.kind == P_COIN) {
                alpha = 255;
            } else if (k < 0.15f) {
                alpha = (int) (255 * (k / 0.15f));
            } else {
                alpha = (int) (255 * (1f - (k - 0.15f) / 0.85f));
            }
            if (p.kind == P_EMBER) {
                alpha = (int) (alpha * (0.6f + 0.4f * (float) Math.sin(p.life / 90f + p.seed)));
            }
            if (p.kind == P_COIN) {
                // سکهٔ چرخان — بیضی با پهنای نوسانی
                float spin = (float) Math.cos(p.life / 90f);
                paint.setColor(COIN_RING);
                rect.set(p.x - p.size * Math.abs(spin), p.y - p.size, p.x + p.size * Math.abs(spin), p.y + p.size);
                canvas.drawOval(rect, paint);
                paint.setColor(COIN_BODY);
                rect.set(p.x - p.size * Math.abs(spin) * 0.62f, p.y - p.size * 0.62f, p.x + p.size * Math.abs(spin) * 0.62f, p.y + p.size * 0.62f);
                canvas.drawOval(rect, paint);
            } else {
                paint.setColor((p.color & 0x00FFFFFF) | (Math.min(255, alpha) << 24));
                canvas.drawCircle(p.x, p.y, p.size, paint);
            }
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // لمس — فقط ناحیهٔ امضای فعال مصرف می‌شود
    // ─────────────────────────────────────────────────────────────────────────

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (!AmberThemeFX.enabled()) {
            return false;
        }
        switch (event.getActionMasked()) {
            case MotionEvent.ACTION_DOWN: {
                if (hitRect.isEmpty() || !hitRect.contains(event.getX(), event.getY())) {
                    return false;
                }
                touchActive = true;
                return true;
            }
            case MotionEvent.ACTION_UP: {
                if (!touchActive) {
                    return false;
                }
                touchActive = false;
                performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP);
                triggerSignature(event.getX(), event.getY());
                return true;
            }
            case MotionEvent.ACTION_CANCEL: {
                touchActive = false;
                return false;
            }
            default:
                return touchActive;
        }
    }

    private void triggerSignature(float x, float y) {
        long now = System.currentTimeMillis();
        switch (family) {
            case FX_MARIO: {
                if (marioState == M_JUMP) {
                    return;
                }
                jumpStartX = marioX;
                float target = marioX + (x >= marioX ? 1 : -1) * 26f * dp;
                jumpEndX = Math.max(20f * dp, Math.min(getWidth() - 20f * dp, target));
                marioDir = jumpEndX > jumpStartX ? 1 : -1;
                jumpT = 0f;
                coinSpawned = false;
                marioState = M_JUMP;
                break;
            }
            case FX_AURORA: {
                shootingT = 0f;
                shootingX = Math.max(30f * dp, Math.min(getWidth() - 30f * dp, x));
                shootingY = Math.max(10f * dp, y - 14f * dp);
                spawnBurst(x, Math.max(12f * dp, y), AmberTokens.AURORA_NIGHT_ACCENT_BRIGHT, 8);
                break;
            }
            case FX_PREMIERE: {
                spawnBurst(x, Math.max(12f * dp, y), AmberTokens.PREMIERE_NIGHT_ACCENT, 10);
                nextReelSparkAt = now + 600L;
                break;
            }
            case FX_SLING: {
                if (slingState != S_FLY) {
                    slingState = S_FLY;
                    slingStateAt = now;
                    birdX = slingBaseX(getWidth()) - marioSign() * 22f * dp;
                    birdY = groundY - 34f * dp;
                    birdVx = marioSign() * 300f * dp;
                    birdVy = -180f * dp;
                }
                break;
            }
            case FX_SW: {
                saberBoost = 1.2f;
                double ang = Math.toRadians(-22f * (rtl ? -1f : 1f));
                float bx = rtl ? getWidth() * 0.24f : getWidth() * 0.76f;
                float tipX = bx + (float) Math.cos(ang) * getWidth() * 0.42f;
                float tipY = groundY - 2f * dp + (float) Math.sin(ang) * getWidth() * 0.42f;
                spawnBurst(tipX, tipY, night ? 0xFFFF2E3E : 0xFF57A8FF, 12);
                break;
            }
            case FX_HARMONY: {
                harmonyPulse = 0f;
                harmonyPulseX = x;
                harmonyPulseY = Math.max(20f * dp, Math.min(getHeight() - 12f * dp, y));
                break;
            }
            default: {
                spawnBurst(x, Math.max(12f * dp, Math.min(getHeight() - 10f * dp, y)),
                    night ? AmberTokens.NIGHT_ACCENT_BRIGHT : AmberTokens.DAY_ACCENT_BRIGHT, 14);
                break;
            }
        }
    }

    private static float easeInOut(float k) {
        return k < 0.5f ? 2f * k * k : 1f - 2f * (1f - k) * (1f - k);
    }
}

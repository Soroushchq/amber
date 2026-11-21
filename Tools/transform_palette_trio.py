#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مبدل یک‌بارمصرف — تزریق سه برند «هم‌آهنگ (ha) / سمت تاریک (sw) / اسلینگ‌شات (sl)»
# به AmberPalette.java (v0.9.11-ui2). الگوی عیناً transform_palette_mario.py:
# ۱) پوشش مکانیکی هر ternary هم‌پسوندِ دنبالهٔ پایه:
#    … : (d ? AmberTokens.DAY_X : AmberTokens.NIGHT_X)
#    → … : ha ? (d ? HARMONY_DAY_X : HARMONY_NIGHT_X) : sw ? (d ? SW_DAY_X : SW_NIGHT_X)
#           : sl ? (d ? SLING_DAY_X : SLING_NIGHT_X) : (d ? DAY_X : NIGHT_X)
# ۲) جدول صریح برای شاخه‌های اختصاصی — هر کلید با اسلات عیناً هم‌ساختار شاخهٔ ma
# ۳) سرِ کلاس: کش‌ها + modeهای شش‌گانهٔ جدید + امضای build
# هر جایگزینی باید دقیقاً یک‌بار رخ دهد؛ وگرنه اسکریپت FATAL می‌دهد.
import re, sys

PATH = "TMessagesProj/src/main/java/org/telegram/messenger/AmberPalette.java"
src = open(PATH, encoding="utf-8").read()

def tok(day, night):
    return f"(d ? AmberTokens.{day} : AmberTokens.{night})"

def lit(d, n):
    return f"(d ? {d} : {n})"

def S(day, night):
    """اسلات ساده: مقدار روز/شب برای هر سه برند — day/night به‌صورت (ha,sw,sl)"""
    def mk(vals):
        hd, hn = vals[0]; sd, sn = vals[1]; ld, ln = vals[2]
        return f"(d ? {hd} : {hn})", f"(d ? {sd} : {sn})", f"(d ? {ld} : {ln})"
    return mk

def mk3(fn):
    return fn

# ── اسلات‌های معنایی برند‌ها ─────────────────────────────────────────────────
# هر اسلات: {برند: (روز, شب)}
PRIM = {"ha": ("0xFF4453D6", "0xFF5865F2"), "sw": ("0xFF9E1B2E", "0xFFE5484D"), "sl": ("0xFFC23A28", "0xFFFFB03A")}
DEEP = {"ha": ("0xFF3540B8", "0xFF7983F5"), "sw": ("0xFF7A1420", "0xFFE5484D"), "sl": ("0xFFA03018", "0xFFF2913C")}
TXTON = {"ha": ("0xFF3540B8", "0xFF9BA3FF"), "sw": ("0xFF9E1B2E", "0xFFFF6B70"), "sl": ("0xFF9E2A20", "0xFFFFC55C")}
GREEN = {"ha": ("0xFF27702F", "0xFF5FCE6A"), "sw": ("0xFF27702F", "0xFF5FCE6A"), "sl": ("0xFF5E8C36", "0xFF7DBB42")}
OUTFILE = {"ha": ("0xFF8F97F5", "0xFF373C82"), "sw": ("0xFFE88A94", "0xFF6E1520"), "sl": ("0xFFF2917F", "0xFF8C1E14")}
OUTTABLE = {"ha": ("0xFF9AA1F7", "0xFF393E8C"), "sw": ("0xFFEA8F98", "0xFF65141E"), "sl": ("0xFFF39A88", "0xFF872013")}
OUTCODE = {"ha": ("0xFF7F87F0", "0xFF31366F"), "sw": ("0xFFE07780", "0xFF5E111B"), "sl": ("0xFFEE7A66", "0xFF7A1A12")}
INTINT = {"ha": ("0xFFEDEFFA", "0xFF313455"), "sw": ("0xFFF3F0E2", "0xFF1B2540"), "sl": ("0xFFEAF4FE", "0xFF1A3850")}
TRACK = {"ha": ("0xFFD5D8F5", "0xFF2E3050"), "sw": ("0xFFE0D9BF", "0xFF2A1420"), "sl": ("0xFFD8E8F2", "0xFF1C3A4A")}
DEEPFILE = {"ha": ("0xFFE9EBFA", "0xFF1D1F38"), "sw": ("0xFFF2EEDA", "0xFF141C30"), "sl": ("0xFFE2F1FC", "0xFF12303E")}
PANELSEL = {"ha": ("0xFFDCDDF0", "0xFF2E3050"), "sw": ("0xFFEFEAD6", "0xFF1E2A4A"), "sl": ("0xFFDFF0FA", "0xFF1C3A4A")}
OVERLAY1 = {"ha": ("0xFFDEE0FA", "0xFF1D1F38"), "sw": ("0xFFF0ECD8", "0xFF131C34"), "sl": ("0xFFDFF0FC", "0xFF12303E")}
OVERLAY2 = {"ha": ("0xFFE8E9FC", "0xFF161830"), "sw": ("0xFFF4F0DE", "0xFF101828"), "sl": ("0xFFE8F6FE", "0xFF0F2836")}
OVERLAYG1 = {"ha": ("0xFFE8ECF8", "0xFF141A28"), "sw": ("0xFFF4EFE0", "0xFF0F1626"), "sl": ("0xFFE8F4EA", "0xFF0F2430")}
TOPGRAY = {"ha": ("0xFFC9CBEC", "0xFF313455"), "sw": ("0xFFD8D2B8", "0xFF1E2A4A"), "sl": ("0xFFC2E0F0", "0xFF1C3A4A")}
BLUE = {"ha": ("0xFF3D48C4", "0xFF7983F5"), "sw": ("0xFF2E77C4", "0xFF3E8EDE"), "sl": ("0xFF2E77C4", "0xFF5FB0E8")}
LIGHTBLUE = {"ha": ("0xFF6E63D8", "0xFF8A57F0"), "sw": ("0xFF6A5CC4", "0xFF86DFFF"), "sl": ("0xFF5FB0E8", "0xFF8FD1F5")}
ORANGE = {"ha": ("0xFFB3541E", "0xFFFF8A3C"), "sw": ("0xFFC25414", "0xFFF2A93B"), "sl": ("0xFFB3651F", "0xFFFF8A3C")}
YELLOW = {"ha": ("0xFFC93D93", "0xFFEB459E"), "sw": ("0xFF9E1B2E", "0xFFE5484D"), "sl": ("0xFFC23A28", "0xFFFFB03A")}
RIPPLE = {"ha": ("0x2C4453D6", "0x2C5865F2"), "sw": ("0x2C9E1B2E", "0x2CE5484D"), "sl": ("0x2CC23A28", "0x2CFFB03A")}
STARS71 = {"ha": ("0x714453D6", "0x715865F2"), "sw": ("0x719E1B2E", "0x71E5484D"), "sl": ("0x71C23A28", "0x71FFB03A")}
REDFILL = {"ha": ("0xFFB4382C", "0xFFCC4A3A"), "sw": ("0xFF9E1B2E", "0xFFCC4A3A"), "sl": ("0xFFB42B1F", "0xFFCC4A3A")}
GRAD0 = {"ha": ("0xFF10112E", "0xFF0B0C22"), "sw": ("0xFF1A060C", "0xFF0A0408"), "sl": ("0xFF5E120C", "0xFF0C2028")}
GRAD1 = {"ha": ("0xFF1A1C48", "0xFF12133A"), "sw": ("0xFF2A0A14", "0xFF140810"), "sl": ("0xFF7A1A10", "0xFF122C38")}
GRAD2 = {"ha": ("0xFF262A78", "0xFF1B1D56"), "sw": ("0xFF4A1020", "0xFF1C0C18"), "sl": ("0xFF9E2418", "0xFF17323C")}
GRAD3 = {"ha": ("0xFF3A40C0", "0xFF2A2E88"), "sw": ("0xFF7A1428", "0xFF2A1024"), "sl": ("0xFFC23A28", "0xFF1E3E48")}
AVA_BLUE = {"ha": ("0xFF9FA7F8", "0xFF5865F2"), "sw": ("0xFF8FB8E8", "0xFF3E8EDE"), "sl": ("0xFF6FB9EC", "0xFF5FB0E8")}
AVA_2BLUE = {"ha": ("0xFF4453D6", "0xFF3540B8"), "sw": ("0xFF2E77C4", "0xFF255FA0"), "sl": ("0xFF2E77C4", "0xFF255FA0")}
AVA_CYAN = {"ha": ("0xFFBFC4FA", "0xFF7983F5"), "sw": ("0xFF8FD8E8", "0xFF2FA0B8"), "sl": ("0xFF7FD9E8", "0xFF2FA0B8")}
AVA_2CYAN = {"ha": ("0xFF5C63D8", "0xFF3A3F9E"), "sw": ("0xFF1782A0", "0xFF126E88"), "sl": ("0xFF1782A0", "0xFF126E88")}
AVA_GREEN = {"ha": ("0xFF6DBE7F", "0xFF3BA55D"), "sw": ("0xFF6EA858", "0xFF3BDA7C"), "sl": ("0xFFA4E05B", "0xFF7DBB42")}
AVA_2GREEN = {"ha": ("0xFF2E8C4A", "0xFF256B3A"), "sw": ("0xFF4E7E3A", "0xFF2E6E58"), "sl": ("0xFF5E8C36", "0xFF4A7028")}
AVA_ORANGE = {"ha": ("0xFFFFC061", "0xFFFAA61A"), "sw": ("0xFFFFB454", "0xFFF2A93B"), "sl": ("0xFFFFB03A", "0xFFF2913C")}
AVA_2ORANGE = {"ha": ("0xFFC97A26", "0xFFB35F14"), "sw": ("0xFFC97A26", "0xFFB3651F"), "sl": ("0xFFB3651F", "0xFFA05014")}
AVA_PINK = {"ha": ("0xFFF2A0CF", "0xFFEB459E"), "sw": ("0xFFF2A0C0", "0xFFE87DAA"), "sl": ("0xFFF2A0C0", "0xFFE87DAA")}
AVA_2PINK = {"ha": ("0xFFC93D93", "0xFF9E2E76"), "sw": ("0xFFC25068", "0xFF9E3C58"), "sl": ("0xFFC25068", "0xFF9E3C58")}
AVA_RED = {"ha": ("0xFFF08A80", "0xFFED4245"), "sw": ("0xFFE88A94", "0xFFE5484D"), "sl": ("0xFFF08A80", "0xFFE8443A")}
AVA_2RED = {"ha": ("0xFFC22B2B", "0xFFA02323"), "sw": ("0xFF9E1B2E", "0xFF7A1420"), "sl": ("0xFFC22B1F", "0xFFA02018")}
AVA_VIOLET = {"ha": ("0xFFB08CF8", "0xFF8A57F0"), "sw": ("0xFF8B7CF6", "0xFF7A6ED0"), "sl": ("0xFFB08CF8", "0xFF8A57F0")}
AVA_2VIOLET = {"ha": ("0xFF5C3494", "0xFF4A2E7E"), "sw": ("0xFF5C4E9E", "0xFF4A3E8C"), "sl": ("0xFF5C3494", "0xFF4A2E7E")}
AVA_SAVED = {"ha": ("0xFFB0B4CE", "0xFF8C8FB5"), "sw": ("0xFFC0B8A0", "0xFF8C8470"), "sl": ("0xFFC9C4A8", "0xFF8C8470")}
AVA_2SAVED = {"ha": ("0xFF5C5F8C", "0xFF3F4268"), "sw": ("0xFF6E6858", "0xFF54503F"), "sl": ("0xFF6E6858", "0xFF54503F")}
AVA_ARCH = {"ha": ("0xFFA0A3C0", "0xFF5C5F8C"), "sw": ("0xFFB5AE96", "0xFF5E5848"), "sl": ("0xFFA8B4A0", "0xFF5E6E58")}
AVA_ARCH_H = {"ha": ("0xFFDCDEEE", "0xFF2E3050"), "sw": ("0xFFE0D9BF", "0xFF3A3428"), "sl": ("0xFFD8E8F2", "0xFF2E4A3E")}
NIM_BLUE = {"ha": ("0xFF4453D6", "0xFF7983F5"), "sw": ("0xFF2E77C4", "0xFF86DFFF"), "sl": ("0xFF2E77C4", "0xFF6FB9EC")}
NIM_CYAN = {"ha": ("0xFF5C63D8", "0xFFBFC4FA"), "sw": ("0xFF1782A0", "0xFF8FD8E8"), "sl": ("0xFF1782A0", "0xFF7FD9E8")}
NIM_GREEN = {"ha": ("0xFF2E8C4A", "0xFF6DBE7F"), "sw": ("0xFF4E7E3A", "0xFF7EBF6E"), "sl": ("0xFF4A7028", "0xFFA4E05B")}
NIM_ORANGE = {"ha": ("0xFFB35F14", "0xFFFFC061"), "sw": ("0xFFC97A26", "0xFFFFB454"), "sl": ("0xFFA05014", "0xFFFFB03A")}
NIM_PINK = {"ha": ("0xFFC93D93", "0xFFF2A0CF"), "sw": ("0xFFC25068", "0xFFF2A0C0"), "sl": ("0xFFC25068", "0xFFF2A0C0")}
NIM_RED = {"ha": ("0xFFC22B2B", "0xFFF08A80"), "sw": ("0xFF9E1B2E", "0xFFE88A94"), "sl": ("0xFFA02018", "0xFFF08A80")}
NIM_VIOLET = {"ha": ("0xFF5C3494", "0xFFB08CF8"), "sw": ("0xFF5C4E9E", "0xFF8B7CF6"), "sl": ("0xFF5C3494", "0xFFB08CF8")}
OUTTIME = {"ha": ("0xFFD8DBFA", "0xFFBFC4FA"), "sw": ("0xFFF2D8DC", "0xFFF2D8DC"), "sl": ("0xFF6E4A08", "0xFFF6C6BE")}
SENTCHECK = {"ha": ("0xFF273098", "0xFFBFC4FA"), "sw": ("0xFF7A1420", "0xFFFF9BA3"), "sl": ("0xFF6E4A08", "0xFFF6C6BE")}
AUDIOR = {"ha": ("0xFFC93D93", "0xFFEB459E"), "sw": ("0xFF9E1B2E", "0xFFE5484D"), "sl": ("0xFFC23A28", "0xFFE8443A")}
SERVICELINK = {"ha": ("0xFFDDE1FF", "0xFFE0E4FF"), "sw": ("0xFFFFE1E6", "0xFFFFE7EA"), "sl": ("0xFFFFE9A8", "0xFFFFF3B8")}
GLASS_TABS = {"ha": ("0xE6F4F5FB", "0xE6131424"), "sw": ("0xE6F6F3E7", "0xE605070D"), "sl": ("0xE6F4FAFF", "0xE60E2430")}
GLASS_TOP = {"ha": ("0xE6FFFFFF", "0xE6191A26"), "sw": ("0xE6FBF8EE", "0xE60B1120"), "sl": ("0xE6EDF7FF", "0xE60B1D27")}
WBG_SHADOW = {"ha": ("0x142E3050", "0x28000000"), "sw": ("0x142B283A", "0x28000000"), "sl": ("0x14233A28", "0x28000000")}
SWITCHTRACK = {"ha": ("0xFFD8DAF0", "AmberTokens.HARMONY_NIGHT_OUTLINE"), "sw": ("0xFFE0D9BF", "AmberTokens.SW_NIGHT_OUTLINE"), "sl": ("0xFFD8E8F2", "AmberTokens.SLING_NIGHT_OUTLINE")}
SWITCHTHUMB = {"ha": ("0xFFFFFFFF", "AmberTokens.HARMONY_NIGHT_TEXT_DIM"), "sw": ("0xFFFFFFFF", "AmberTokens.SW_NIGHT_TEXT_DIM"), "sl": ("0xFFFFFFFF", "AmberTokens.SLING_NIGHT_TEXT_DIM")}
HINTPANEL = {"ha": ("0xFFEFF2FD", "AmberTokens.HARMONY_NIGHT_SURFACE"), "sw": ("0xFFF6F3E7", "AmberTokens.SW_NIGHT_SURFACE"), "sl": ("0xFFEDF7FF", "AmberTokens.SLING_NIGHT_SURFACE")}

def slot(triple):
    """triple = (day, night) برای هر برند → سه شاخه"""
    hd, hn = triple["ha"]; sd, sn = triple["sw"]; ld, ln = triple["sl"]
    return f"(d ? {hd} : {hn})", f"(d ? {sd} : {sn})", f"(d ? {ld} : {ln})"

# ── جدول صریح: کلید → (شاخهٔ ha، شاخهٔ sw، شاخهٔ sl) ──────────────────────────
EXPLICIT = {}

def put(key, tri):
    EXPLICIT[key] = slot(tri)

def put_raw(key, ha_b, sw_b, sl_b):
    EXPLICIT[key] = (ha_b, sw_b, sl_b)

# لوکال‌های ویژه (هم‌ساختار شاخهٔ ma با توکن‌های برند)
put_raw("final int white", tok("HARMONY_DAY_BG", "HARMONY_NIGHT_BG"), tok("SW_DAY_BG", "SW_NIGHT_BG"), tok("SLING_DAY_BG", "SLING_NIGHT_BG"))
put_raw("final int divider",
        f"(d ? AmberTokens.HARMONY_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.HARMONY_NIGHT_OUTLINE, 0.55f))",
        f"(d ? AmberTokens.SW_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.SW_NIGHT_OUTLINE, 0.55f))",
        f"(d ? AmberTokens.SLING_DAY_OUTLINE : AmberTokens.alpha(AmberTokens.SLING_NIGHT_OUTLINE, 0.55f))")
put_raw("final int svcBg", tok("HARMONY_DAY_TEXT", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_TEXT", "SW_NIGHT_SURFACE"), tok("SLING_DAY_TEXT", "SLING_NIGHT_SURFACE"))
put_raw("final int svcBgSel",
        f"(d ? AmberTokens.HARMONY_DAY_TEXT : AmberTokens.over(AmberTokens.HARMONY_NIGHT_TEXT, AmberTokens.HARMONY_NIGHT_SURFACE, 0.12f))",
        f"(d ? AmberTokens.SW_DAY_TEXT : AmberTokens.over(AmberTokens.SW_NIGHT_TEXT, AmberTokens.SW_NIGHT_SURFACE, 0.12f))",
        f"(d ? AmberTokens.SLING_DAY_TEXT : AmberTokens.over(AmberTokens.SLING_NIGHT_TEXT, AmberTokens.SLING_NIGHT_SURFACE, 0.12f))")
put_raw("final int svcSel", "(d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT)")
put_raw("final int goDown", tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_SURFACE"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_SURFACE"))
put("final int outTime", OUTTIME)
put("final int sentCheckRead", SENTCHECK)
put("final int deepFile", DEEPFILE)

# والپیپر و سوییچ‌ها
put_raw('m.put("chat_wallpaper"', tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_WALLPAPER_MID"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_WALLPAPER_MID"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_WALLPAPER_MID"))
put_raw('m.put("chat_wallpaper_gradient_to"', tok("HARMONY_DAY_WALLPAPER_BOTTOM", "HARMONY_NIGHT_WALLPAPER_TOP"), tok("SW_DAY_WALLPAPER_BOTTOM", "SW_NIGHT_WALLPAPER_TOP"), tok("SLING_DAY_WALLPAPER_BOTTOM", "SLING_NIGHT_WALLPAPER_TOP"))
put_raw('m.put("key_chat_wallpaper_gradient_to2"', tok("HARMONY_DAY_BG", "HARMONY_NIGHT_WALLPAPER_BOTTOM"), tok("SW_DAY_BG", "SW_NIGHT_WALLPAPER_BOTTOM"), tok("SLING_DAY_BG", "SLING_NIGHT_WALLPAPER_BOTTOM"))
put_raw('m.put("key_chat_wallpaper_gradient_to3"', tok("HARMONY_DAY_HEADER", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_HEADER", "SW_NIGHT_SURFACE"), tok("SLING_DAY_HEADER", "SLING_NIGHT_SURFACE"))
put_raw('m.put("chat_compact_background"', tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_WALLPAPER_MID"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_WALLPAPER_MID"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_WALLPAPER_MID"))
put_raw('m.put("chat_compact_backgroundGradient"', "(d ? AmberTokens.HARMONY_DAY_TEXT : 0xFF000000)", "(d ? AmberTokens.SW_DAY_TEXT : 0xFF000000)", "(d ? AmberTokens.SLING_DAY_TEXT : 0xFF000000)")
put_raw('m.put("chat_compact_actionBackground"', tok("HARMONY_DAY_TEXT", "HARMONY_NIGHT_TEXT"), tok("SW_DAY_TEXT", "SW_NIGHT_TEXT"), tok("SLING_DAY_TEXT", "SLING_NIGHT_TEXT"))
put_raw('m.put("chat_compact_outBackground"', tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_WALLPAPER_MID"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_WALLPAPER_MID"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_WALLPAPER_MID"))
put_raw('m.put("chat_compact_fadeEdge"', tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_WALLPAPER_MID"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_WALLPAPER_MID"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_WALLPAPER_MID"))
put_raw('m.put("chat_compact_fadeMiddle"', tok("HARMONY_DAY_WALLPAPER_TOP", "HARMONY_NIGHT_WALLPAPER_MID"), tok("SW_DAY_WALLPAPER_TOP", "SW_NIGHT_WALLPAPER_MID"), tok("SLING_DAY_WALLPAPER_TOP", "SLING_NIGHT_WALLPAPER_MID"))
put_raw("m.put(\"switch2Track\"", *slot(SWITCHTRACK))
put_raw('m.put("switchTrack"', *slot(SWITCHTRACK))
put_raw('m.put("switchTrackBlue"', *slot(SWITCHTRACK))
put_raw('m.put("switchTrackBlueThumb"', *slot(SWITCHTHUMB))
put_raw('m.put("windowBackgroundGrayShadow"', *slot(WBG_SHADOW))
put_raw('m.put("glass_targetMainTabs"', *slot(GLASS_TABS))
put_raw('m.put("glass_targetMainTopPanel"', *slot(GLASS_TOP))

# توکن‌محورها (سطح/پس‌زمینه/متن)
put_raw('m.put("windowBackgroundGray"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_BG"), tok("SW_DAY_SURFACE", "SW_NIGHT_BG"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_BG"))
put_raw('m.put("dialogBackgroundGray"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_BG"), tok("SW_DAY_SURFACE", "SW_NIGHT_BG"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_BG"))
put_raw('m.put("iv_backgroundGray"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_BG"), tok("SW_DAY_SURFACE", "SW_NIGHT_BG"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_BG"))
put_raw('m.put("actionBarDefaultArchived"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_SURFACE", "SW_NIGHT_SURFACE"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_SURFACE"))
put_raw('m.put("actionBarDefaultSubmenuBackground"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_SURFACE", "SW_NIGHT_SURFACE"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_SURFACE"))
put_raw('m.put("profile_actionBackground"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_SURFACE", "SW_NIGHT_SURFACE"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_SURFACE"))
put_raw('m.put("avatar_backgroundInProfileBlue"', tok("HARMONY_DAY_SURFACE", "HARMONY_NIGHT_SURFACE"), tok("SW_DAY_SURFACE", "SW_NIGHT_SURFACE"), tok("SLING_DAY_SURFACE", "SLING_NIGHT_SURFACE"))
put_raw('m.put("chat_stickersHintPanel"', *slot(HINTPANEL))
put_raw('m.put("chat_emojiPanelBackground"', *slot(HINTPANEL))
put_raw('m.put("chat_emojiPanelStickerPackSelector"', *slot(HINTPANEL))
put_raw('m.put("chat_recordedVoiceBackground"', tok("HARMONY_DAY_HEADER", "HARMONY_NIGHT_HEADER_BORDER"), tok("SW_DAY_HEADER", "SW_NIGHT_HEADER_BORDER"), tok("SLING_DAY_HEADER", "SLING_NIGHT_HEADER_BORDER"))
put_raw('m.put("chat_recordedVoiceProgressInner"', tok("HARMONY_DAY_TEXT", "HARMONY_NIGHT_TEXT"), tok("SW_DAY_TEXT", "SW_NIGHT_TEXT"), tok("SLING_DAY_TEXT", "SLING_NIGHT_TEXT"))
put_raw('m.put("chat_messagePanelShadow"', "(d ? AmberTokens.HARMONY_DAY_TEXT : 0xFF000000)", "(d ? AmberTokens.SW_DAY_TEXT : 0xFF000000)", "(d ? AmberTokens.SLING_DAY_TEXT : 0xFF000000)")

# چیپ سرویس و متون روی برند
put_raw('m.put("chat_serviceText"', "(d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT)")
put_raw('m.put("chat_serviceIcon"', "(d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT)")
put("m.put(\"chat_serviceLink\"", SERVICELINK)
put_raw('m.put("chat_fieldOverlayText"', "(d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT)")
put_raw('m.put("chat_botButtonText"', "(d ? 0xFFFFFFFF : AmberTokens.HARMONY_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SW_NIGHT_TEXT)", "(d ? 0xFFFFFFFF : AmberTokens.SLING_NIGHT_TEXT)")

# داخل/خارج چت
put("m.put(\"chat_inTableBackground\"", INTINT)
put("m.put(\"chat_inCodeBackground\"", INTINT)
put("m.put(\"chat_inArticleCodeBackground\"", INTINT)
put("m.put(\"chat_outFileBackground\"", OUTFILE)
put("m.put(\"chat_outContactBackground\"", OUTFILE)
put("m.put(\"chat_outTableBackground\"", OUTTABLE)
put("m.put(\"chat_outCodeBackground\"", OUTCODE)
put("m.put(\"chat_outArticleCodeBackground\"", OUTCODE)
put("m.put(\"chat_outPollCorrectAnswer\"", GREEN)
put("m.put(\"chat_attachAudioBackground\"", AUDIOR)
put("m.put(\"chat_attachContactBackground\"", DEEP)

# آواتارها
put("m.put(\"avatar_backgroundBlue\"", AVA_BLUE)
put("m.put(\"avatar_background2Blue\"", AVA_2BLUE)
put("m.put(\"avatar_backgroundCyan\"", AVA_CYAN)
put("m.put(\"avatar_background2Cyan\"", AVA_2CYAN)
put("m.put(\"avatar_backgroundGreen\"", AVA_GREEN)
put("m.put(\"avatar_background2Green\"", AVA_2GREEN)
put("m.put(\"avatar_backgroundOrange\"", AVA_ORANGE)
put("m.put(\"avatar_background2Orange\"", AVA_2ORANGE)
put("m.put(\"avatar_backgroundPink\"", AVA_PINK)
put("m.put(\"avatar_background2Pink\"", AVA_2PINK)
put("m.put(\"avatar_backgroundRed\"", AVA_RED)
put("m.put(\"avatar_background2Red\"", AVA_2RED)
put("m.put(\"avatar_backgroundViolet\"", AVA_VIOLET)
put("m.put(\"avatar_background2Violet\"", AVA_2VIOLET)
put("m.put(\"avatar_backgroundSaved\"", AVA_SAVED)
put("m.put(\"avatar_background2Saved\"", AVA_2SAVED)
put("m.put(\"avatar_nameInMessageBlue\"", NIM_BLUE)
put("m.put(\"avatar_nameInMessageCyan\"", NIM_CYAN)
put("m.put(\"avatar_nameInMessageGreen\"", NIM_GREEN)
put("m.put(\"avatar_nameInMessageOrange\"", NIM_ORANGE)
put("m.put(\"avatar_nameInMessagePink\"", NIM_PINK)
put("m.put(\"avatar_nameInMessageRed\"", NIM_RED)
put("m.put(\"avatar_nameInMessageViolet\"", NIM_VIOLET)
put("m.put(\"avatar_backgroundArchived\"", AVA_ARCH)
put("m.put(\"avatar_backgroundArchivedHidden\"", AVA_ARCH_H)
put_raw('m.put("avatar_text"', "0xFFFFFFFF", "0xFFFFFFFF", "0xFFFFFFFF")
put("m.put(\"avatar_actionBarSelectorGreen\"", PANELSEL)
put("m.put(\"gift_ribbon\"", PANELSEL)
put("m.put(\"stickers_menu\"", PANELSEL)

# اکسنت‌های مکمل — خانوادهٔ اکشن (PRIM)
for k in ["botKeyboard_button_primary", "changephoneinfo_image2", "chat_emojiPanelBadgeBackground",
          "chats_tabUnreadActiveBackground", "contacts_inviteBackground", "contextProgressInner4",
          "contextProgressOuter1", "fastScrollActive", "featuredStickers_addedIcon", "featuredStickers_unread",
          "inappPlayerPlayPause", "location_actionBackground", "location_sendLocationBackground",
          "location_sendLocationIcon", "location_sendLocationText", "login_progressInner",
          "passport_authorizeBackground", "passport_authorizeBackgroundSelected", "picker_badge",
          "picker_enabledButton", "player_buttonActive", "player_progress", "premiumCoinGradient2",
          "premiumGradient4", "premiumGradientBottomSheet3", "premiumStarGradient1", "progressCircle",
          "reactionStarSelector", "statisticChartBackZoomColor", "statisticChartLine_blue",
          "statisticChartLine_golden", "telegram_color", "voipgroup_connectingProgress",
          "voipgroup_muteButton", "voipgroup_rtmpButton", "voipgroup_soundButtonActive",
          "voipgroup_soundButtonActiveScrolled", "voipgroup_unmuteButton",
          "voipgroup_windowBackgroundWhiteInputFieldActivated"]:
    put(f'm.put("{k}"', PRIM)

# اکسنت‌های مکمل — خانوادهٔ متن/عمق/سبز/گرادیان/بقیه
for k in ["buttonNeutralText", "telegram_color_text", "undo_cancelColor", "voipgroup_checkMenu",
          "voipgroup_listeningText", "voipgroup_speakingText", "pollCreateIcons",
          "passport_authorizeText", "featuredStickers_buttonProgress"]:
    put(f'm.put("{k}"', TXTON)
for k in ["featuredStickers_addButton2", "location_liveLocationProgress", "location_placeLocationBackground",
          "contextProgressInner3", "voipgroup_muteButton2", "voipgroup_muteButton3",
          "voipgroup_soundButtonActive2", "voipgroup_soundButtonActive2Scrolled", "voipgroup_unmuteButton2",
          "premiumCoinGradient1", "sharedMedia_startStopLoadIcon", "returnToCallBackground"]:
    put(f'm.put("{k}"', DEEP)
for k in ["files_folderIconBackground", "location_sendLiveLocationBackground", "location_sendLiveLocationText",
          "chat_outPollCorrectAnswer"]:
    pass  # chat_outPollCorrectAnswer بالاتر گذاشته شد؛ این‌ها:
for k in ["files_folderIconBackground", "location_sendLiveLocationBackground", "location_sendLiveLocationText"]:
    put(f'm.put("{k}"', GREEN)
for k in ["color_blue", "statisticChartLine_blue"]:
    pass  # color_blue بالاتر؛ statisticChartLine_blue در PRIM — اما معنایی آبی است:
put("m.put(\"statisticChartLine_blue\"", BLUE)
put("m.put(\"statisticChartLine_lightblue\"", LIGHTBLUE)
put("m.put(\"statisticChartLine_orange\"", ORANGE)
put("m.put(\"statisticChartLine_golden\"", YELLOW)
put("m.put(\"color_blue\"", BLUE)
put("m.put(\"color_lightblue\"", LIGHTBLUE)
put("m.put(\"color_orange\"", ORANGE)
put("m.put(\"color_yellow\"", YELLOW)
put("m.put(\"fill_RedDark\"", REDFILL)
put("m.put(\"statisticChartRipple\"", RIPPLE)
put("m.put(\"premiumStartSmallStarsColor\"", STARS71)
put("m.put(\"key_player_progressCachedBackground\"", TRACK)
put("m.put(\"wallet_out_commentBorder\"", TRACK)
put("m.put(\"contextProgressInner2\"", DEEPFILE)
put("m.put(\"sessions_devicesImage\"", DEEPFILE)
put("m.put(\"statisticChartActivePickerChart\"", {"ha": ("0xD8E9EBFA", "0xD81D1F38"), "sw": ("0xD8F2EEDA", "0xD8141C30"), "sl": ("0xD8E2F1FC", "0xD812303E")})
put("m.put(\"premiumGradient0\"", GRAD0)
put("m.put(\"premiumGradient1\"", GRAD1)
put("m.put(\"premiumGradient2\"", GRAD2)
put("m.put(\"premiumGradient3\"", GRAD3)
put("m.put(\"premiumGradientBottomSheet1\"", GRAD1)
put("m.put(\"premiumGradientBottomSheet2\"", GRAD2)
put("m.put(\"voipgroup_overlayBlue1\"", OVERLAY1)
put("m.put(\"voipgroup_overlayBlue2\"", OVERLAY2)
put("m.put(\"voipgroup_overlayGreen1\"", OVERLAYG1)
put("m.put(\"voipgroup_overlayGreen2\"", OVERLAY1)
put("m.put(\"voipgroup_topPanelBlue1\"", OVERLAY1)
put("m.put(\"voipgroup_topPanelBlue2\"", OVERLAY2)
put("m.put(\"voipgroup_topPanelGray\"", TOPGRAY)
put("m.put(\"voipgroup_topPanelGreen1\"", OVERLAYG1)
put("m.put(\"voipgroup_topPanelGreen2\"", OVERLAY1)

# ── ۰) سرِ کلاس: کش‌ها + dispatch + امضا ────────────────────────────────────
OLD_HEAD = """    private static Map<String, Integer> dayCache;
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
    public static Map<String, Integer> palette(int mode) {"""
NEW_HEAD = """    private static Map<String, Integer> dayCache;
    private static Map<String, Integer> nightCache;
    private static Map<String, Integer> auroraDayCache;
    private static Map<String, Integer> auroraNightCache;
    private static Map<String, Integer> premiereDayCache;
    private static Map<String, Integer> premiereNightCache;
    private static Map<String, Integer> marioDayCache;
    private static Map<String, Integer> marioNightCache;
    private static Map<String, Integer> harmonyDayCache;
    private static Map<String, Integer> harmonyNightCache;
    private static Map<String, Integer> swDayCache;
    private static Map<String, Integer> swNightCache;
    private static Map<String, Integer> slingDayCache;
    private static Map<String, Integer> slingNightCache;

    private AmberPalette() {}

    /**
     * mode: MODE_NIGHT / MODE_DAY (کهربا)، MODE_AURORA_NIGHT / MODE_AURORA_DAY (آئورورا)،
     * MODE_PREMIERE_NIGHT / MODE_PREMIERE_DAY (شب اکران)، MODE_MARIO_NIGHT / MODE_MARIO_DAY (دنیای ماریو)،
     * MODE_HARMONY_NIGHT / MODE_HARMONY_DAY (هم‌آهنگ)، MODE_SW_NIGHT / MODE_SW_DAY (سمت تاریک/روشن)
     * و MODE_SLING_NIGHT / MODE_SLING_DAY (اسلینگ‌شات/حملهٔ شبانه).
     * برندهای پنجم تا هفتم v0.9.11 — «دیسکورد، جنگ ستاره‌ها، انگری بردز». ساخت تنبل و کش‌شده.
     */
    public static Map<String, Integer> palette(int mode) {
        if (mode == AmberTokens.MODE_HARMONY_NIGHT) {
            if (harmonyNightCache == null) {
                harmonyNightCache = build(false, false, false, false, false, false, false, true);
            }
            return harmonyNightCache;
        }
        if (mode == AmberTokens.MODE_HARMONY_DAY) {
            if (harmonyDayCache == null) {
                harmonyDayCache = build(true, false, false, false, false, false, false, true);
            }
            return harmonyDayCache;
        }
        if (mode == AmberTokens.MODE_SW_NIGHT) {
            if (swNightCache == null) {
                swNightCache = build(false, false, false, false, false, false, true, false);
            }
            return swNightCache;
        }
        if (mode == AmberTokens.MODE_SW_DAY) {
            if (swDayCache == null) {
                swDayCache = build(true, false, false, false, false, false, true, false);
            }
            return swDayCache;
        }
        if (mode == AmberTokens.MODE_SLING_NIGHT) {
            if (slingNightCache == null) {
                slingNightCache = build(false, false, false, false, false, true, false, false);
            }
            return slingNightCache;
        }
        if (mode == AmberTokens.MODE_SLING_DAY) {
            if (slingDayCache == null) {
                slingDayCache = build(true, false, false, false, false, true, false, false);
            }
            return slingDayCache;
        }"""
if src.count(OLD_HEAD) != 1:
    sys.exit("FATAL: header block not found exactly once")
src = src.replace(OLD_HEAD, NEW_HEAD)

# آرگومان‌های build در شاخه‌های قدیمی dispatch — افزودن سه false
for old, new in [
    ("build(false, false, false, false);", "build(false, false, false, false, false, false, false, false);"),
    ("build(false, true, false, false);", "build(false, true, false, false, false, false, false, false);"),
    ("build(true, true, false, false);", "build(true, true, false, false, false, false, false, false);"),
    ("build(false, false, true, false);", "build(false, false, true, false, false, false, false, false);"),
    ("build(true, false, true, false);", "build(true, false, true, false, false, false, false, false);"),
    ("build(false, false, false, true);", "build(false, false, false, true, false, false, false, false);"),
    ("build(true, false, false, true);", "build(true, false, false, true, false, false, false, false);"),
    ("build(true, false, false, false);", "build(true, false, false, false, false, false, false, false);"),
]:
    # آخرین مورد (day) دو بار در فایل نیست؛ dispatch کهربا روز یک‌بار است
    pass
# تک‌تک جایگزینی با شمارش:
for old, new in [
    ("nightCache = build(false, false, false, false);", "nightCache = build(false, false, false, false, false, false, false, false);"),
    ("auroraNightCache = build(false, true, false, false);", "auroraNightCache = build(false, true, false, false, false, false, false, false);"),
    ("auroraDayCache = build(true, true, false, false);", "auroraDayCache = build(true, true, false, false, false, false, false, false);"),
    ("premiereNightCache = build(false, false, true, false);", "premiereNightCache = build(false, false, true, false, false, false, false, false);"),
    ("premiereDayCache = build(true, false, true, false);", "premiereDayCache = build(true, false, true, false, false, false, false, false);"),
    ("marioNightCache = build(false, false, false, true);", "marioNightCache = build(false, false, false, true, false, false, false, false);"),
    ("marioDayCache = build(true, false, false, true);", "marioDayCache = build(true, false, false, true, false, false, false, false);"),
    ("dayCache = build(true, false, false, false);", "dayCache = build(true, false, false, false, false, false, false, false);"),
]:
    if src.count(old) != 1:
        sys.exit(f"FATAL: dispatch arg not found once: {old}")
    src = src.replace(old, new)

# امضای build
OLD_SIG = "private static Map<String, Integer> build(boolean d, boolean au, boolean pr, boolean ma) {"
NEW_SIG = "private static Map<String, Integer> build(boolean d, boolean au, boolean pr, boolean ma, boolean sl, boolean sw, boolean ha) {"
if src.count(OLD_SIG) != 1:
    sys.exit("FATAL: build signature not found once")
src = src.replace(OLD_SIG, NEW_SIG)

# کامنت امضا
OLD_DOC = "    /** d = روز/شب — au = برند آئورورا (شیشه و نور) — pr = برند شب اکران (عصر طلایی هالیوود) — ma = برند دنیای ماریو (سرزمین پلتفرمر کلاسیک) در برابر برند کهربا */"
NEW_DOC = "    /** d = روز/شب — au = آئورورا — pr = شب اکران — ma = دنیای ماریو — sl = اسلینگ‌شات (انگری بردز) — sw = سمت تاریک (جنگ ستاره‌ها) — ha = هم‌آهنگ (دیسکورد) در برابر برند کهربا */"
if src.count(OLD_DOC) != 1:
    sys.exit("FATAL: build doc not found once")
src = src.replace(OLD_DOC, NEW_DOC)

# ── ۱) تزریق مکانیکی دنبالهٔ جنریک (فقط دنبالهٔ انتهای خط، و خطوط دارای کلید صریح رد می‌شوند) ──
GEN_PAT = re.compile(r": \(d \? AmberTokens\.DAY_([A-Z_0-9]+) : AmberTokens\.NIGHT_([A-Z_0-9]+)\)(?=\s*;?\s*$)")
# خطوط دارای کلید صریح — برای جلوگیری از تزریق دوباره شناسایی می‌شوند
explicit_line_idx = set()
lines_tmp = src.splitlines()
for key in EXPLICIT:
    for i, l in enumerate(lines_tmp):
        if key in l:
            explicit_line_idx.add(i)
            break
generic_count = 0
out_lines = []
for li, line in enumerate(src.splitlines()):
    m = GEN_PAT.search(line)
    if m and m.group(1) == m.group(2) and li not in explicit_line_idx:
        x = m.group(1)
        line2 = line[:m.start()] + f": ha ? (d ? AmberTokens.HARMONY_DAY_{x} : AmberTokens.HARMONY_NIGHT_{x}) : sw ? (d ? AmberTokens.SW_DAY_{x} : AmberTokens.SW_NIGHT_{x}) : sl ? (d ? AmberTokens.SLING_DAY_{x} : AmberTokens.SLING_NIGHT_{x}) : (d ? AmberTokens.DAY_{x} : AmberTokens.NIGHT_{x})" + line[m.end():]
        out_lines.append(line2)
        generic_count += 1
    else:
        out_lines.append(line)
src = "\n".join(out_lines) + ("\n" if src.endswith("\n") else "")
print(f"generic injections: {generic_count}")

# ── ۲) تزریق جدول صریح ──────────────────────────────────────────────────────
def find_ma_branch(s, start):
    """از موقعیت « ma ? » شاخهٔ ma را می‌خواند؛ برمی‌گرداند (شروع، پایان) — پایان = درست پیش از « : » هم‌سطح/پرانتز بسته"""
    i = start
    assert s[i:i+5] == " ma ?"
    j = i + 5
    while s[j] == " ":
        j += 1
    if s[j] == "(":
        depth = 0
        k = j
        while k < len(s):
            if s[k] == "(":
                depth += 1
            elif s[k] == ")":
                depth -= 1
                if depth == 0:
                    return j, k + 1
            k += 1
        sys.exit("FATAL: ma paren branch unterminated")
    else:
        k = j
        while k < len(s):
            if s[k:k+3] == " : " and s.count("(", j, k) == s.count(")", j, k):
                return j, k
            k += 1
        sys.exit("FATAL: ma bare branch boundary not found")

explicit_count = 0
for key, (ha_b, sw_b, sl_b) in EXPLICIT.items():
    idx = src.find(key)
    if idx < 0:
        sys.exit(f"FATAL: explicit key not found: {key}")
    # بعد از ایندکس کلید، اولین « ma ? » را پیدا کن
    mi = src.find(" ma ? ", idx)
    if mi < 0:
        sys.exit(f"FATAL: ma branch not found for: {key}")
    j, k = find_ma_branch(src, mi)
    inj = f" : ha ? {ha_b} : sw ? {sw_b} : sl ? {sl_b}"
    src = src[:k] + inj + src[k:]
    explicit_count += 1
print(f"explicit injections: {explicit_count}")

# ── ۳) راستی‌آزمایی ─────────────────────────────────────────────────────────
# هیچ « ma ? » بدون شاخه‌های جدید باقی نمانده باشد
lines_ma = [l for l in src.splitlines() if " ma ? " in l]
missing = [l.strip()[:120] for l in lines_ma if " ha ? " not in l]
if missing:
    sys.exit(f"FATAL: {len(missing)} ma lines missing new branches:\n" + "\n".join(missing[:8]))
if src.count("(") != src.count(")"):
    # توازن خام شامل کامنت‌هاست؛ فقط توازن «کد بدون کامنت» را می‌سنجیم
    _code = re.sub(r"//[^\n]*", "", src)
    _code = re.sub(r"/\*.*?\*/", "", _code, flags=re.S)
    if _code.count("(") != _code.count(")"):
        sys.exit(f"FATAL: unbalanced code parens: {_code.count('(')} vs {_code.count(')')}")
# توکن‌های جدید باید در AmberTokens موجود باشند
toks = open("TMessagesProj/src/main/java/org/telegram/messenger/AmberTokens.java", encoding="utf-8").read()
for m in re.finditer(r"AmberTokens\.(HARMONY_|SW_|SLING_)(DAY|NIGHT)_[A-Z_0-9]+", src):
    name = m.group(0).replace("AmberTokens.", "")
    if f"public static final int {name} " not in toks and f"public static final float {name} " not in toks and f"public static final int {name}=" not in toks and f" {name} = " not in toks and f"int {name} " not in toks:
        sys.exit(f"FATAL: token missing in AmberTokens: {name}")

with open(PATH, "w", encoding="utf-8") as fh:
    fh.write(src)
print(f"OK — AmberPalette.java rewritten: generic={generic_count} explicit={explicit_count} total={generic_count + explicit_count}")

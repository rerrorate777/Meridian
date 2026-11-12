#!/usr/bin/env python3
"""Restyle the top-of-screen match bar (frame, timer notch, player portraits).

Usage: patch_topbar.py <stock resource/ui dir> <meridian resource/ui dir>

  * hudmatchstatus.res         flat frame instead of the cream-bordered box; Meridian timer text;
                               portrait colours / health-bar colours / fonts for the player list
  * hudobjectivetimepanel.res  Meridian font + colour for the "Waiting for players", "Overtime",
                               "Setup" ... labels under the notch
  * hudroundcounter.res        the notch art (hud/comp_round_timer) -> meridian/mer_timer

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import os
import re
import sys

PANEL = "12 14 18 205"
TEXT = "236 240 244 255"

# portrait backgrounds: muted team colours, darker when dead
PORTRAIT = {
    "color_portrait_bg_red": "108 48 44 255",
    "color_portrait_bg_blue": "44 78 112 255",
    "color_portrait_bg_red_dead": "46 30 30 255",
    "color_portrait_bg_blue_dead": "30 38 48 255",
    "color_bar_health_high": "126 224 150 255",
    "color_bar_health_med": "240 207 78 255",
    "color_bar_health_low": "255 70 56 255",
}


def read(path):
    return open(path, encoding="utf-8", errors="surrogateescape", newline="").read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(text)


def sub1(pattern, repl, text, what, flags=re.S):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        raise SystemExit("%s: expected 1 match, got %d" % (what, n))
    return new


def block(text, name, indent="\t"):
    m = re.search(r'\n%s"%s"\s*\n%s\{.*?\n%s\}' % (indent, re.escape(name), indent, indent), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn, indent="\t"):
    s, e = block(text, name, indent)
    return text[:s] + fn(text[s:e]) + text[e:]


def key(blk, k, value, what):
    pat = r'(\n\s*"%s"\s*)"[^"]*"' % re.escape(k)
    return sub1(pat, lambda m: m.group(1) + '"' + value + '"', blk, what + "." + k)


def patch_matchstatus(src, dst):
    t = read(src)

    def frame(b):
        b = key(b, "ControlName", "ImagePanel", "BGFrame")
        b = sub1(r'\n\t\t"border"\s*"TFFatLineBorder"', '\n\t\t"fillcolor"\t\t"%s"' % PANEL, b, "BGFrame.border")
        return b

    t = edit_block(t, "BGFrame", frame)

    # timer text inside the notch (match layout only: the "if_match" block)
    def timer(b):
        b = key(b, "fgcolor", "MerText", "TimePanelValue")
        i = b.index("if_match")
        head, tail = b[:i], b[i:]
        tail = sub1(r'("ypos"\s*)"12"', r'\1"10"', tail, "TimePanelValue.if_match.ypos")
        tail = sub1(r'("tall"\s*)"10"', r'\1"22"', tail, "TimePanelValue.if_match.tall")
        for k in ("font", "font_minmode", "font_lodef"):
            tail = key(tail, k, "MerNumberSmall", "TimePanelValue.if_match")
        return head + tail

    t = edit_block(t, "ObjectiveStatusTimePanel", lambda b: edit_block(b, "TimePanelValue", timer, "\t\t"))

    # player portraits
    def portraits(b):
        for k, v in PORTRAIT.items():
            b = key(b, k, v, "playerpanels_kv")
        b = edit_block(b, "playername", lambda x: key(x, "font", "MerLabel", "playername"), "\t\t\t")
        b = edit_block(b, "respawntime", lambda x: key(x, "font", "MerLabel", "respawntime"), "\t\t\t")
        b = sub1(r'("bgcolor_override"\s*)"80 80 80 255"', r'\1"40 44 52 255"', b, "healthbar.bgcolor")
        # (the tab under a dead player's portrait is left stock: the game swaps its art per team)
        return b

    t = edit_block(t, "TeamStatus", lambda b: sub1(
        r'"playerpanels_kv"\s*\{.*?\n\t\t\}', lambda m: portraits(m.group(0)), b, "playerpanels_kv"))
    write(dst, t)


def patch_timepanel(src, dst):
    t = read(src)
    labels = ["WaitingForPlayersLabel", "OvertimeLabel", "SuddenDeathLabel", "SetupLabel", "ServerTimeLimitLabel"]

    def label(b):
        i = b.index("if_match")
        head, tail = b[:i], b[i:]
        tail = sub1(r'("font"\s*)"HudFontSmallestBold"',
                    r'\1"MerLabel"\n\t\t\t"fgcolor"\t\t\t\t\t"MerText"', tail, "label.font")
        for k in ("font_hidef", "font_lodef"):
            tail = key(tail, k, "MerLabel", "label")
        return head + tail

    for name in labels:
        t = edit_block(t, name, label)
    write(dst, t)


# The stock notch art has transparent margins, so its visible part is ~91 units wide although the
# panel is 3.833 x 35 = 134. mer_timer has no margins, so size the panel to the visible width
# (2.5 x 35 = 87.5, a little inside the portraits) or it runs into the first player portraits (team bases are c-45 / c+47).
NOTCH_ASPECT = "o2.5"


def patch_roundcounter(src, dst):
    t = read(src)
    t = sub1(r'"\.\./hud/comp_round_timer"', '"meridian/mer_timer"', t, "roundcounter.Background.image")
    t = sub1(r'("wide"\s*)"o3\.833"', r'\1"%s"' % NOTCH_ASPECT, t, "roundcounter.Background.wide")
    write(dst, t)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    for name, fn in (("hudmatchstatus.res", patch_matchstatus),
                     ("hudobjectivetimepanel.res", patch_timepanel),
                     ("hudroundcounter.res", patch_roundcounter)):
        fn(os.path.join(stock, name), os.path.join(mer, name))
        print("patched", name)


if __name__ == "__main__":
    main()

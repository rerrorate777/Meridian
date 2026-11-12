#!/usr/bin/env python3
"""Restyle the Tab scoreboard from the stock files.

Usage: patch_scoreboard.py <stock resource/ui dir> <meridian dir>

  * resource/ui/scoreboard.res    flat dark frames, team-tinted banners (no logos), Meridian fonts
                                  and colours
  * resource/clientscheme.res     the Scoreboard* fonts used by the player rows / stats (built in
                                  code, so they can only be changed in the scheme) -> Barlow.
                                  Edited in place; re-running is harmless.

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import os
import re
import sys

PANEL = "12 14 18 205"
INSET = "28 32 40 235"  # solid: a translucent white came out far greyer than its alpha suggests
LINE = "255 255 255 30"
BLUE_TEXT = "130 185 240 255"
RED_TEXT = "240 120 108 255"

# explicit controls in scoreboard.res: stock font -> Meridian font
FONTS = {
    "ScoreboardVerySmall": "MerLabel",
    "ScoreboardSmall": "MerLabel",
    "ScoreboardMediumSmall": "MerBody",
    "ScoreboardMedium": "MerTitle",
    "ScoreboardTeamNameNew": "MerTitle",
    "ScoreboardTeamCountNew": "MerBody",
    "ScoreboardTeamScoreNew": "MerHealth",
    "HudFontSmallest": "MerLabel",
}

# scheme fonts: name swapped for Barlow, bold; the smallest one gets a bump.
# NOTE: the player-list rows use a different, unlisted stock font (changing these has no effect on
# them). That is fine: Barlow only covers Latin scripts, so rows keep the stock font and non-Latin
# player names stay readable. Applied on the first run only (marked with "// meridian").
SCHEME_FONTS = {
    "ScoreboardVerySmall": ("Barlow", 4),
    "ScoreboardSmall": ("Barlow", 1),
    "ScoreboardMediumSmall": ("Barlow", 1),
    "ScoreboardMedium": ("Barlow", 0),
    "ScoreboardTeamNameNew": ("Barlow", 0),
    "ScoreboardTeamCountNew": ("Barlow", 0),
    "ScoreboardTeamScoreNew": ("Barlow Condensed", 0),
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


def block(text, name):
    m = re.search(r'\n\t"?%s"?\s*\n\t\{.*?\n\t\}' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn):
    s, e = block(text, name)
    return text[:s] + fn(text[s:e]) + text[e:]


def key(blk, k, value, what):
    return sub1(r'(\n\t\t"%s"\s*)"[^"]*"' % re.escape(k), lambda m: m.group(1) + '"' + value + '"', blk, what + "." + k)


def flat(fill):
    """EditablePanel with a border -> ImagePanel with a flat fill."""
    def fn(b, name=None):
        b = key(b, "ControlName", "ImagePanel", "flat")
        return sub1(r'\n\t\t"border"\s*"[^"]*"', '\n\t\t"fillcolor"\t\t"%s"' % fill, b, "flat.border")
    return fn


def add_color(b, color):
    """Give a label an fgcolor (replace an existing one)."""
    if re.search(r'\n\t\t"fgcolor"', b):
        return key(b, "fgcolor", color, "label")
    return sub1(r'(\n\t\t"font"\s*"[^"]*")', r'\1\n\t\t"fgcolor"\t\t"%s"' % color, b, "label.font")


def patch_scoreboard(src, dst):
    t = read(src)

    # frames
    t = edit_block(t, "MainBG", flat(PANEL))
    t = edit_block(t, "TimerBG", flat("12 14 18 235"))
    t = edit_block(t, "ServerTimeLeftInsetBG", flat(INSET))
    t = edit_block(t, "PlayerNameBG", flat(INSET))
    t = edit_block(t, "ShadedBar", lambda b: key(b, "fillcolor", "0 0 0 60", "ShadedBar"))
    t = edit_block(t, "VerticalLine", lambda b: key(b, "fillcolor", LINE, "VerticalLine"))
    t = edit_block(t, "HorizontalLine", lambda b: key(b, "fillcolor", LINE, "HorizontalLine"))

    # team banners: flat tinted panels, the team logos are hidden and the text moves to the edge
    t = edit_block(t, "BlueScoreBG", lambda b: key(b, "image", "meridian/mer_panel_blue", "BlueScoreBG"))
    t = edit_block(t, "RedScoreBG", lambda b: key(b, "image", "meridian/mer_panel_red", "RedScoreBG"))
    # (the game ignores visible=0 on the logos, so also park them outside the scoreboard panel,
    # where the parent clips them)
    for n in ("BlueTeamImage", "RedTeamImage"):
        t = edit_block(t, n, lambda b: key(key(b, "visible", "0", "logo"), "xpos", "-400", "logo"))

    def label(xpos, ypos, tall, visible=None):
        def fn(b):
            b = key(b, "xpos", xpos, "label")
            b = key(b, "ypos", ypos, "label")
            b = key(b, "tall", tall, "label")
            if visible is not None:
                b = sub1(r'(\n\t\t"visible"\s*)"0"(\s*\n\t\t"enabled")', r'\1"%s"\2' % visible, b, "label.visible")
            return add_color(b, "MerText")
        return fn

    t = edit_block(t, "BlueTeamPlayerCount", label("16", "38", "18"))
    t = edit_block(t, "RedTeamPlayerCount", label("468", "38", "18"))
    for n in ("BlueTeamScore", "RedTeamScore"):
        t = edit_block(t, n, lambda b: add_color(b, "MerText"))
    for n in ("BlueTeamScoreDropshadow", "RedTeamScoreDropshadow"):
        t = edit_block(t, n, lambda b: key(b, "visible", "0", "dropshadow"))
    t = edit_block(t, "ServerTimeLeftValue", lambda b: key(b, "fgcolor", "MerText", "ServerTimeLeftValue"))

    # player lists
    t = edit_block(t, "BluePlayerList", lambda b: key(b, "fgcolor", BLUE_TEXT, "BluePlayerList"))
    t = edit_block(t, "RedPlayerList", lambda b: key(b, "fgcolor", RED_TEXT, "RedPlayerList"))

    # fonts of the explicit controls
    def font(m):
        return m.group(1) + '"' + FONTS[m.group(2)] + '"'
    t = re.sub(r'(\n\s*"font"\s*)"(%s)"' % "|".join(FONTS), font, t)
    write(dst, t)


def patch_scheme(path):
    t = read(path)
    for name, (face, bump) in SCHEME_FONTS.items():
        m = re.search(r'\n\t\t"%s"\s*\n\s*\{.*?\n\t\t\}' % name, t, re.S)
        if not m:
            raise SystemExit("scheme font not found: " + name)
        b = m.group(0)
        if "// meridian" not in b:  # first run
            b = sub1(r'("name"\s*)"[^"]*"', r'\1"%s"' % face, b, name + ".name")
            b = sub1(r'("weight"\s*)"\d+"', r'\1"700"', b, name + ".weight")
            if bump:
                b = re.sub(r'("tall(?:_hidef|_lodef)?"\s*)"(\d+)"', lambda x: x.group(1) + '"%d"' % (int(x.group(2)) + bump), b)
            b = b.replace("{", "{ // meridian", 1)
        t = t[:m.start()] + b + t[m.end():]
    # highlight of the local player's row (and any selected list row): subtler than stock
    t = sub1(r'(SectionedListPanel\.OutOfFocusSelectedBgColor\s*)"[^"]*"', r'\1"255 255 255 14"', t, "highlight")
    write(path, t)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock_ui, mer = sys.argv[1], sys.argv[2]
    patch_scoreboard(os.path.join(stock_ui, "scoreboard.res"), os.path.join(mer, "resource", "ui", "scoreboard.res"))
    patch_scheme(os.path.join(mer, "resource", "clientscheme.res"))
    print("patched scoreboard.res and the Scoreboard* fonts in clientscheme.res")


if __name__ == "__main__":
    main()

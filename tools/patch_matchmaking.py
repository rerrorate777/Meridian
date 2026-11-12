#!/usr/bin/env python3
"""Restyle the top bar and the Find a Game screens (mode selection, casual / competitive / MvM
dashboards and lobbies, playlist entries) from the stock files.

Usage: patch_matchmaking.py <stock resource/ui dir> <meridian resource/ui dir>

  * every matchmaking / lobby / playlist file: Meridian fonts, and the tan-era hard-coded colours
    (dark brown text for tan buttons, brown panel fills) -> the Meridian greys.
    The panel/button borders and the green button colours come from clientscheme.res
    (tools/patch_menus.py), so they are not touched here.
  * matchmakingdashboard.res (the top bar): flat bar instead of the bordered panel with a gradient
    and shadow; Quit / Disconnect / Find a Game buttons in Meridian colours.

Files that do not change are not written. Every top-bar edit must match exactly once, otherwise the
script aborts (see patch_layout.py).
"""
import glob
import os
import re
import sys

TEXT = "236 240 244 255"
WHITE = "255 255 255 255"
DIM = "150 160 172 255"

FILE_RE = re.compile(r"(matchmaking|lobby|mainmenuplaylist|mainmenueventplaylist|casualrank|casualwelcome|"
                     r"competitive|compstats|comprank|mvmcriteria|mvmeconrequirement|training|playlist|dashboard)")

FONTS = {
    "HudFontSmallBold": "MerBody", "HudFontSmallestBold": "MerLabel", "HudFontSmall": "MerBody",
    "HudFontSmallest": "MerLabel", "HudFontMediumBold": "MerTitle", "HudFontMediumSmallBold": "MerBody",
    "HudFontMediumBigBold": "MerTitle", "HudFontMediumSmall": "MerBody", "HudFontGiantBold": "MerHealth",
    "HudFontBiggerBold": "MerHealth", "MenuSmallFont": "MerBody", "MMenuPlayListDesc": "MerLabel",
}

# hard-coded colours by key: stock value -> Meridian
COLORS = {
    "bgcolor_override": {"60 53 46 255": "28 32 40 255", "77 72 68 255": "34 38 46 255",
                         "76 70 66 255": "34 38 46 255", "46 43 42 255": "16 18 24 255",
                         "42 39 37 255": "14 16 22 255"},
    "fgcolor": {"117 107 94 255": DIM, "235 226 202 255": TEXT, "Orange": TEXT},
    "defaultFgColor_override": {"46 43 42 255": TEXT},
    "armedFgColor_override": {"200 80 60 255": WHITE, "235 226 202 255": WHITE, "Orange": WHITE},
    # translucent cream / orange fills (the "View Maps" strips, list rows): dark, with a lighter hover
    "defaultBgColor_override": {"235 226 202 20": "20 24 32 200", "235 226 202 2": "20 24 32 20"},
    "armedBgColor_override": {"LightOrange": "46 52 64 220"},
    "selectedBGColor_override": {"Orange": "60 68 82 255"},
}


def read(path):
    return open(path, encoding="utf-8", errors="surrogateescape", newline="").read()


def write(path, text):
    with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(text)


def sub1(pattern, repl, text, what, flags=re.S):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        raise SystemExit("%s: expected 1 match, got %d" % (what, n))
    return new


def generic(t):
    t = re.sub(r'(\n\s*"font"\s*)"(%s)"' % "|".join(FONTS), lambda m: m.group(1) + '"' + FONTS[m.group(2)] + '"', t)
    for key, table in COLORS.items():
        def fix(m, table=table):
            return m.group(1) + '"' + table.get(m.group(2), m.group(2)) + '"'
        t = re.sub(r'("%s"\s*)"([^"]*)"' % key, fix, t)
    return t


# Buttons that get the footer-button style (square, flat, 2px accent line on the left, from the
# MerButtonBorder / MerButtonBorderArmed borders in clientscheme.res). Image-only buttons (close,
# next/prev arrows, checkboxes) are left alone.
STYLED_BUTTONS = {
    "QueueButton", "MannUpQueueButton", "BootCampQueueButton", "PlayNowButton", "PracticeButton", "LearnMoreButton",
    "StartPartyButton", "OptionsButton", "SearchButton", "StopSearchButton", "RematchButton", "RequeueButton",
    "LeavePartyButton", "LeaveQueueButton", "AbandonButton", "JoinNowButton", "SmallJoinButton", "WideJoinButton",
    "SelectButton", "ShowLeaderboardsButton", "ShowMatchHistoryButton", "RestoreCasualSearchCriteria",
    "SaveCasualSearchCriteria", "ShowExplanationsButton", "TakeTourButton", "ConfirmButton", "ModeButton",
    "MannUpNowButton", "BackButton",
}
BUTTON_KEYS = {"border_default": "MerButtonBorder", "border_armed": "MerButtonBorderArmed",
               "paintborder": "1", "PaintBackgroundType": "0"}
_BUTTON_KEY_RE = re.compile(r'\n[ \t]*"(?:border_default|border_armed|border_depressed|paintborder|PaintBackgroundType)"[^\n]*')


def match_brace(t, i):
    """Index just past the } matching the { at t[i]."""
    depth = 0
    k = i
    while k < len(t):
        c = t[k]
        if c == '"':
            k = t.index('"', k + 1)
        elif c == "/" and t.startswith("//", k):
            k = t.index("\n", k)
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return k + 1
        k += 1
    raise SystemExit("unbalanced braces")


def style_buttons(t):
    """Apply BUTTON_KEYS to every button block named in STYLED_BUTTONS (any nesting depth)."""
    out, pos, count = [], 0, 0
    pat = re.compile(r'"ControlName"\s*"(?:CExButton|CExImageButton|CTFButton|Button)"\s*\n\s*"fieldName"\s*"([^"]*)"[^\n]*', re.I)
    for m in pat.finditer(t):
        if m.group(1) not in STYLED_BUTTONS or m.start() < pos:
            continue
        open_i = t.rindex("{", 0, m.start())
        close_i = match_brace(t, open_i)
        blk = t[open_i:close_i]
        child = blk.find("{", 1)
        head, tail = (blk[:child], blk[child:]) if child != -1 else (blk, "")
        head = _BUTTON_KEY_RE.sub("", head)
        ind = re.search(r'\n([ \t]*)"ControlName"', head)
        ind = ind.group(1) if ind else "\t\t"  # ControlName on the same line as the brace
        add = "".join('\n%s"%s"\t\t"%s"' % (ind, k, v) for k, v in BUTTON_KEYS.items())
        fm = re.search(r'"fieldName"[^\n]*', head)
        head = head[:fm.end()] + add + head[fm.end():]
        out.append(t[pos:open_i] + head + tail)
        pos = close_i
        count += 1
    out.append(t[pos:])
    return "".join(out), count


def block(text, name, indent="\t"):
    m = re.search(r'\n%s"?%s"?\s*(?:\[[^\]]*\])?\s*\n%s\{.*?\n%s\}' % (indent, re.escape(name), indent, indent), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn, indent="\t"):
    s, e = block(text, name, indent)
    return text[:s] + fn(text[s:e]) + text[e:]


def key(b, k, v, what, indent="\t\t\t"):
    return sub1(r'(\n%s"%s"\s*)"[^"]*"' % (indent, re.escape(k)), lambda m: m.group(1) + '"' + v + '"', b, what + "." + k)


def topbar(t):
    """The dashboard top bar: TopBar > Gradient / BGPanel / OuterShadow / buttons (2 tabs deep)."""
    # inside TopBar the children sit at two tabs, their keys at three
    t = edit_block(t, "Gradient", lambda b: key(b, "visible", "0", "Gradient"), "\t\t")
    t = edit_block(t, "OuterShadow", lambda b: key(b, "visible", "0", "OuterShadow"), "\t\t")

    def bar(b):
        b = key(b, "ControlName", "ImagePanel", "BGPanel")
        return sub1(r'\n\t\t\t"border"\s*"ReplayDefaultBorder"', '\n\t\t\t"fillcolor"\t\t"10 12 16 245"', b, "BGPanel.border")
    t = edit_block(t, "BGPanel", bar, "\t\t")

    def keys(kv, what):
        def fn(b):
            for k, v in kv.items():
                b = key(b, k, v, what)
            return b
        return fn

    red = {"defaultBgColor_override": "28 32 40 235", "armedBgColor_override": "224 84 72 200"}
    for n in ("QuitButton", "DisconnectButton"):
        t = edit_block(t, n, keys(red, n), "\t\t")
    green = {"defaultBgColor_override": "46 110 70 255", "armedBgColor_override": "62 138 88 255"}
    t = edit_block(t, "FindAGameButton", keys(green, "FindAGameButton"), "\t\t")
    return t


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    n = styled = 0
    for path in sorted(glob.glob(os.path.join(stock, "*.res"))):
        name = os.path.basename(path)
        if not FILE_RE.match(name):
            continue
        t = read(path)
        out = generic(t)
        if name == "matchmakingdashboard.res":
            out = topbar(out)
        out, nb = style_buttons(out)
        styled += nb
        if out != t:
            write(os.path.join(mer, name), out)
            n += 1
    print("patched %d files, %d buttons styled" % (n, styled))


if __name__ == "__main__":
    main()

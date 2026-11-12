#!/usr/bin/env python3
"""Restyle the team select and class select menus from the stock files.

Usage: patch_classteam.py <stock resource/ui dir> <meridian resource/ui dir>

Both menus are built on 3D model scenes (a hallway with doors; a classroom). Those models cannot be
restyled, so they are shrunk to an off-screen 1x1 panel (the game still finds them by name) and a
dark scrim replaces them.

  * teammenu.res / teammenu_sc.res        three flat cards (Random, BLU, RED) plus a Spectate button
  * classselection.res / _sc.res          scrim instead of the classroom, flat bottom bar
  * classtipsitem.res                     the class tips drop the chalkboard font
  * all                                   Meridian fonts and text colours

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import os
import re
import sys

TEXT = "MerText"
DIM = "150 160 172 255"
SCRIM = "8 10 14 225"
BAR = "12 14 18 235"
CARD = "12 14 18 225"
CARD_RANDOM = "34 38 48 235"
HOVER = "255 255 255 7"  # translucent white renders ~3x stronger than its alpha suggests
PRESS = "255 255 255 16"
CARD_BLUE = "28 58 92 225"
CARD_RED = "86 34 30 225"
EDGE_BLUE = "76 156 232 255"
EDGE_RED = "224 84 72 255"
EDGE_NEUTRAL = "150 160 172 255"

FONTS = {
    "MenuMainTitle": "MerTitle",
    "MenuSmallFont": "MerBody",
    "MenuSmallestFont": "MerLabel",
    "TeamMenuBold": "MerNumberMed",
    "MenuKeys": "MerLabel",
    "MenuClassBuckets": "MerBody",
    "HudFontSmallBold": "MerBody",
    "HudFontMediumSmallSecondary": "MerBody",
    "CapPlayerFont": "MerTitle",
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
    m = re.search(r'\n\t"?%s"?\s*(?:\[[^\]]*\])?\s*\n\t\{.*?\n\t\}' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn):
    s, e = block(text, name)
    return text[:s] + fn(text[s:e]) + text[e:]


def strip_variants(b):
    """Drop the per-resolution overrides so the positions below apply at every resolution."""
    return re.sub(r'\n\t\t"(?:xpos|ypos|wide|tall|visible)_(?:lodef|hidef)"[^\n]*', "", b)


def setk(b, k, v):
    """Set a key in a top-level block, adding it when missing. Conditional variants are dropped."""
    b = re.sub(r'\n\t\t"%s"[^\n]*\[\$[^\n]*' % re.escape(k), "", b)  # [$WIN32]/[$X360] copies
    if re.search(r'\n\t\t"%s"\s*"' % re.escape(k), b):
        return sub1(r'(\n\t\t"%s"\s*)"[^"]*"' % re.escape(k), lambda m: m.group(1) + '"' + v + '"', b, k)
    return b[:b.rindex("\n\t}")] + '\n\t\t"%s"\t\t"%s"' % (k, v) + b[b.rindex("\n\t}"):]


def place(**kw):
    def fn(b):
        b = strip_variants(b)
        for k, v in kw.items():
            b = setk(b, k, v)
        return b
    return fn


def label(x, y, w, h, font, color=TEXT, align="center", **extra):
    def fn(b):
        b = strip_variants(b)
        for k, v in dict(xpos=x, ypos=y, wide=w, tall=h, font=font, fgcolor=color, textAlignment=align, **extra).items():
            b = setk(b, k, v)
        return b
    return fn


def hide_model(b):
    """A CModelPanel scene piece -> a 1x1 panel off screen (still found by name, draws nothing)."""
    b = strip_variants(b)
    for k, v in (("xpos", "-10"), ("ypos", "-10"), ("wide", "1"), ("tall", "1")):
        b = setk(b, k, v)
    return b


def flat_bar(b):
    b = strip_variants(b)
    b = re.sub(r'\n\t\t"(?:image|tileImage)"[^\n]*', "", b)
    return setk(b, "fillcolor", BAR)


def new_panel(name, x, y, w, h, fill, z="1"):
    return ('\n\t"%s"\n\t{\n\t\t"ControlName"\t"ImagePanel"\n\t\t"fieldName"\t\t"%s"\n\t\t"xpos"\t\t\t"%s"\n'
            '\t\t"ypos"\t\t\t"%s"\n\t\t"zpos"\t\t\t"%s"\n\t\t"wide"\t\t\t"%s"\n\t\t"tall"\t\t\t"%s"\n'
            '\t\t"visible"\t\t"1"\n\t\t"enabled"\t\t"1"\n\t\t"fillcolor"\t\t"%s"\n\t}\n' % (name, name, x, y, z, w, h, fill))


def new_label(name, x, y, w, h, text, font, color=TEXT, align="center", z="4"):
    return ('\n\t"%s"\n\t{\n\t\t"ControlName"\t"CExLabel"\n\t\t"fieldName"\t\t"%s"\n\t\t"xpos"\t\t\t"%s"\n'
            '\t\t"ypos"\t\t\t"%s"\n\t\t"zpos"\t\t\t"%s"\n\t\t"wide"\t\t\t"%s"\n\t\t"tall"\t\t\t"%s"\n'
            '\t\t"visible"\t\t"1"\n\t\t"enabled"\t\t"1"\n\t\t"labelText"\t\t"%s"\n\t\t"textAlignment"\t"%s"\n'
            '\t\t"font"\t\t\t"%s"\n\t\t"fgcolor"\t\t"%s"\n\t}\n' % (name, name, x, y, z, w, h, text, align, font, color))


def append(text, extra):
    i = text.rindex("}")
    return text[:i] + extra + text[i:]


def apply_fonts(t):
    return re.sub(r'(\n\s*"font"\s*)"(%s)"' % "|".join(FONTS), lambda m: m.group(1) + '"' + FONTS[m.group(2)] + '"', t)


# --- team menu layout (HUD units; c = centre of the screen) ---------------------------------------
CARD_W, CARD_H, CARD_Y, GAP = 160, 220, 110, 20
X_RANDOM, X_BLUE, X_RED = -(CARD_W * 3 + GAP * 2) // 2, -CARD_W // 2, CARD_W // 2 + GAP


def c(x):
    return "c%d" % x


def patch_teammenu(src, dst):
    t = read(src)

    # the 3D scene
    for n in ("MenuBG", "bluedoor", "reddoor", "autodoor", "spectate"):
        t = edit_block(t, n, hide_model)
    t = edit_block(t, "ShadedBar", flat_bar)

    # invisible click areas over the cards; "&N" (the key hint) stays at the bottom-left
    cards = {"teambutton2": (X_RANDOM, CARD_Y, CARD_W, CARD_H), "teambutton0": (X_BLUE, CARD_Y, CARD_W, CARD_H),
             "teambutton1": (X_RED, CARD_Y, CARD_W, CARD_H), "teambutton3": (X_BLUE, CARD_Y + CARD_H + 20, CARD_W, 32)}
    for n, (x, y, w, h) in cards.items():
        t = edit_block(t, n, lambda b, x=x, y=y, w=w, h=h: place(
            xpos=c(x), ypos=str(y), wide=str(w), tall=str(h), font="MerLabel", fgcolor=DIM, zpos="6",
            paintbackground="1", defaultBgColor_override="0 0 0 0", armedBgColor_override=HOVER,
            depressedBgColor_override=PRESS)(b))

    # text on the cards
    t = edit_block(t, "TeamMenuAuto", label(c(X_RANDOM), "238", str(CARD_W), "40", "MerTitle", zpos="5"))
    t = edit_block(t, "TeamMenuSpectate", label(c(X_BLUE), str(CARD_Y + CARD_H + 20), str(CARD_W), "32", "MerBody", zpos="5"))
    t = edit_block(t, "BlueCount", label(c(X_BLUE), "238", str(CARD_W), "40", "MerNumberMed", zpos="5"))
    t = edit_block(t, "RedCount", label(c(X_RED), "238", str(CARD_W), "40", "MerNumberMed", zpos="5"))
    t = edit_block(t, "TeamMenuSelect", label("30", "r40", "450", "30", "MerTitle", align="west"))
    for n, x in (("HighlanderLabel", -150), ("HighlanderLabelShadow", -149)):
        t = edit_block(t, n, label(c(x + 40), "62", "220", "24", "MerBody", "0 0 0 0" if "Shadow" in n else TEXT))
    for n, x in (("TeamsFullLabel", -150), ("TeamsFullLabelShadow", -149)):
        t = edit_block(t, n, label(c(x + 40), "84", "220", "24", "MerBody", "0 0 0 0" if "Shadow" in n else TEXT))

    extra = new_panel("MerScrim", "0", "0", "f0", "480", SCRIM, z="0")
    for name, x, fill, edge, title in (("Random", X_RANDOM, CARD_RANDOM, EDGE_NEUTRAL, "?"),
                                       ("Blue", X_BLUE, CARD_BLUE, EDGE_BLUE, "BLU"),
                                       ("Red", X_RED, CARD_RED, EDGE_RED, "RED")):
        extra += new_panel("MerCard" + name, c(x), str(CARD_Y), str(CARD_W), str(CARD_H), fill, z="1")
        extra += new_panel("MerCard%sEdge" % name, c(x), str(CARD_Y), str(CARD_W), "4", edge, z="2")
        if title:
            extra += new_label("MerCard%sTitle" % name, c(x), "150", str(CARD_W), "50", title, "MerHealth")
            if name != "Random":
                extra += new_label("MerCard%sPlayers" % name, c(x), "278", str(CARD_W), "20", "players", "MerLabel", DIM)
    extra += new_panel("MerCardSpectate", c(X_BLUE), str(CARD_Y + CARD_H + 20), str(CARD_W), "32", CARD, z="1")
    t = append(t, extra)
    write(dst, apply_fonts(t))


def patch_classselection(src, dst):
    t = read(src)
    t = edit_block(t, "MenuBG", hide_model)
    t = edit_block(t, "ShadedBar", flat_bar)
    t = append(t, new_panel("MerScrim", "0", "0", "f0", "480", SCRIM, z="0"))
    write(dst, apply_fonts(t))


def patch_tips(src, dst):
    t = read(src)
    t = sub1(r'(\n\t\t\t"font"\s*)"ChalkboardText"', r'\1"MerBody"\n\t\t\t"fgcolor"\t\t\t"%s"' % TEXT, t, "classtips.font")
    write(dst, t)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    for name, fn in (("teammenu.res", patch_teammenu), ("teammenu_sc.res", patch_teammenu),
                     ("classselection.res", patch_classselection), ("classselection_sc.res", patch_classselection),
                     ("classtipsitem.res", patch_tips)):
        fn(os.path.join(stock, name), os.path.join(mer, name))
        print("patched", name)


if __name__ == "__main__":
    main()

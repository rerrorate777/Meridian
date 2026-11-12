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
BTN = "28 32 40 235"
BTN_ARMED = "46 52 64 235"
BTN_PRESSED = "60 68 82 235"
CANCEL_TEXT = "224 84 72 255"
CANCEL_TEXT_ARMED = "255 130 118 255"
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


def flat_button(cancel=False):
    """Footer button: flat dark fill (lighter on hover/press) in the Meridian font, no stock border."""
    def fn(b):
        kw = dict(paintbackground="1", paintborder="0", font="MerBody",
                  border_default="NoBorder", border_armed="NoBorder", border_depressed="NoBorder",
                  defaultBgColor_override=BTN, armedBgColor_override=BTN_ARMED,
                  depressedBgColor_override=BTN_PRESSED,
                  defaultFgColor_override=CANCEL_TEXT if cancel else TEXT,
                  armedFgColor_override=CANCEL_TEXT_ARMED if cancel else "255 255 255 255",
                  depressedFgColor_override=CANCEL_TEXT_ARMED if cancel else "255 255 255 255")
        for k, v in kw.items():
            b = setk(b, k, v)
        return re.sub(r'\n\t\t"fgcolor_override"[^\n]*', "", b)  # stock red text colour -> the override above
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
CARD_W, CARD_H, CARD_Y, GAP = 160, 250, 110, 20
DOOR_W, DOOR_H, DOOR_Y = 140, 112, 156
DOOR_SHIFT = {"autodoor": 51, "bluedoor": -9, "reddoor": -51}  # the door models are authored off-centre
COUNT_Y, PLAYERS_Y = 270, 302
SPECTATE_Y = CARD_Y + CARD_H + 18
HINT_Y = SPECTATE_Y + 38
X_RANDOM, X_BLUE, X_RED = -(CARD_W * 3 + GAP * 2) // 2, -CARD_W // 2, CARD_W // 2 + GAP


def c(x):
    return "c%d" % x


def patch_teammenu(src, dst):
    t = read(src)

    # the 3D scene
    for n in ("MenuBG", "spectate"):
        t = edit_block(t, n, hide_model)
    # The doors are kept, small, as status pictograms: they are the only thing that shows a locked team
    # (the game plays their "disabled" animation, a no-entry sign, when mp_teams_unbalance_limit
    # blocks joining; the buttons themselves look and hover the same either way).
    for n, x in (("autodoor", X_RANDOM), ("bluedoor", X_BLUE), ("reddoor", X_RED)):
        t = edit_block(t, n, lambda b, x=x, n=n: place(xpos=c(x + (CARD_W - DOOR_W) // 2 + DOOR_SHIFT[n]), ypos=str(DOOR_Y),
                                                   wide=str(DOOR_W), tall=str(DOOR_H), zpos="3")(b))
    t = edit_block(t, "ShadedBar", flat_bar)

    # invisible click areas over the cards; "&N" (the key hint) stays at the bottom-left
    cards = {"teambutton2": (X_RANDOM, CARD_Y, CARD_W, CARD_H), "teambutton0": (X_BLUE, CARD_Y, CARD_W, CARD_H),
             "teambutton1": (X_RED, CARD_Y, CARD_W, CARD_H), "teambutton3": (X_BLUE, SPECTATE_Y, CARD_W, 32)}
    for n, (x, y, w, h) in cards.items():
        t = edit_block(t, n, lambda b, x=x, y=y, w=w, h=h: place(
            xpos=c(x), ypos=str(y), wide=str(w), tall=str(h), font="MerLabel", fgcolor=DIM, zpos="6",
            paintbackground="1", defaultBgColor_override="0 0 0 0", armedBgColor_override=HOVER,
            depressedBgColor_override=PRESS)(b))

    # text on the cards
    # the title is the button's own text. The key hints ("&3") that the buttons used to show are
    # static labels below. (A team that is locked by mp_teams_unbalance_limit is NOT disabled in the
    # UI: the stock menu showed that only through the 3D door, so the cards carry a static hint.)
    titles = {"teambutton2": "?", "teambutton0": "BLU", "teambutton1": "RED"}
    for n, text in titles.items():
        t = edit_block(t, n, lambda b, text=text: place(
            labelText=text, font="MerHealth", textAlignment="north", textinsety="30", fgcolor=TEXT,
            defaultFgColor_override=TEXT, armedFgColor_override="255 255 255 255",
            depressedFgColor_override="255 255 255 255")(b))
    t = edit_block(t, "teambutton3", lambda b: place(
        labelText="SPECTATE", font="MerBody", textAlignment="center", fgcolor=TEXT, defaultFgColor_override=TEXT,
        armedFgColor_override="255 255 255 255", depressedFgColor_override="255 255 255 255")(b))
    t = edit_block(t, "TeamMenuSpectate", lambda b: place(visible="0")(b))
    t = edit_block(t, "TeamMenuAuto", lambda b: place(visible="0")(b))
    t = edit_block(t, "BlueCount", label(c(X_BLUE), str(COUNT_Y), str(CARD_W), "34", "MerNumberMed", zpos="5"))
    t = edit_block(t, "RedCount", label(c(X_RED), str(COUNT_Y), str(CARD_W), "34", "MerNumberMed", zpos="5"))
    t = edit_block(t, "CancelButton", flat_button(cancel=True))
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
        if name != "Random":
            extra += new_label("MerCard%sPlayers" % name, c(x), str(PLAYERS_Y), str(CARD_W), "20", "players", "MerLabel", DIM)
    extra += new_label("MerCardRandomLabel", c(X_RANDOM), str(COUNT_Y), str(CARD_W), "34", "RANDOM", "MerTitle")
    extra += new_panel("MerCardSpectate", c(X_BLUE), str(SPECTATE_Y), str(CARD_W), "32", CARD, z="1")
    # key hints (the buttons' own "&N" text was replaced by the card titles)
    for name, x, y, key_ in (("Random", X_RANDOM, CARD_Y + CARD_H - 22, "1"), ("Blue", X_BLUE, CARD_Y + CARD_H - 22, "3"),
                             ("Red", X_RED, CARD_Y + CARD_H - 22, "4"), ("Spectate", X_BLUE, SPECTATE_Y + 14, "2")):
        extra += new_label("MerKey" + name, c(x + 8), str(y), "20", "16", key_, "MerLabel", DIM, align="west", z="7")
    # why a card can be locked (the stock menu showed a no-entry sign, which was part of the 3D scene)
    extra += new_label("MerBalanceHint", c(X_RANDOM), str(HINT_Y), str(CARD_W * 3 + GAP * 2), "16",
                       "Point at a team: a no-entry sign means joining it would unbalance the teams.", "MerLabel", DIM)
    t = append(t, extra)
    write(dst, apply_fonts(t))


# class select: groups of class buttons, left x of the first button (HUD units from the centre)
CLASS_GROUPS = (("Offense", -300, 3), ("Defense", -110, 3), ("Support", 78, 3), ("Random", 250, 1))
CLASS_BUTTONS = ("random", "scout", "soldier", "pyro", "demoman", "heavyweapons", "engineer", "medic", "sniper", "spy")
BUTTON_W = 50


def patch_classselection(src, dst):
    t = read(src)
    t = edit_block(t, "MenuBG", hide_model)
    t = edit_block(t, "ShadedBar", flat_bar)

    # click targets: hover/press highlight and Meridian key-hint colours
    for n in CLASS_BUTTONS:
        t = edit_block(t, n, lambda b: place(
            paintbackground="1", defaultBgColor_override="0 0 0 0", armedBgColor_override=HOVER,
            depressedBgColor_override=PRESS, fgcolor=DIM, defaultFgColor_override=DIM,
            armedFgColor_override=TEXT, depressedFgColor_override=TEXT)(b))
    for n in ("Offense", "Defense", "Support"):
        t = edit_block(t, n, lambda b: place(fgcolor=DIM, textAlignment="center", wide=str(BUTTON_W * 3), zpos="2")(b))
    t = edit_block(t, "CancelButton", flat_button(cancel=True))
    t = edit_block(t, "EditLoadoutButton", flat_button())
    t = edit_block(t, "ResetButton", flat_button())
    t = edit_block(t, "ClassMenuSelect", label("30", "r40", "450", "30", "MerTitle", align="west", zpos="6"))

    extra = new_panel("MerScrim", "0", "0", "f0", "480", SCRIM, z="0")
    for name, x, n in CLASS_GROUPS:
        w = n * BUTTON_W + 12
        extra += new_panel("MerClassCard" + name, c(x - 6), "0", str(w), "114", CARD, z="1")
        extra += new_panel("MerClassCard%sEdge" % name, c(x - 6), "0", str(w), "4", EDGE_NEUTRAL, z="2")
    # the tips box next to the model
    extra += new_panel("MerTipsCard", "c20", "c-92", "251", "181", CARD, z="1")
    extra += new_panel("MerTipsCardEdge", "c20", "c-92", "251", "4", EDGE_NEUTRAL, z="2")
    write(dst, apply_fonts(append(t, extra)))


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

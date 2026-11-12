#!/usr/bin/env python3
"""Restyle the main menu and the panels/dialogs that share its borders and colours.

Usage: patch_menus.py <stock resource/ui dir> <meridian dir>

  * resource/clientscheme.res   (edited in place; re-running is harmless)
      - Borders: the stock art-based panel, button and dialog borders are pointed at flat Meridian
        textures (mer_btn / mer_btn_hover / mer_btn_press / mer_panel / mer_panel_solid ...), so
        every panel that uses them changes at once: main menu, loadout, store, popups...
      - Colors: the tan text/background palette -> Meridian greys
  * resource/ui/mainmenuoverride.res   (from the stock file)
      - Meridian fonts; the dark-brown text that sat on tan buttons -> light text for dark buttons

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import os
import re
import sys

TEXT = "236 240 244 255"
WHITE = "255 255 255 255"
DIM = "150 160 172 255"

# scheme border name -> Meridian texture (under materials/vgui/meridian/)
BORDERS = {
    "TFThinLineBorder": "mer_panel", "TFFatLineBorder": "mer_panel", "TFFatLineBorderOpaque": "mer_panel_solid",
    "TFFatLineBorderRedBGOpaque": "mer_panel_red", "TFFatLineBorderRedBGOpaque_Store": "mer_panel_red",
    "TFFatLineBorderRedBG": "mer_panel_red", "TFFatLineBorderRedBGMoreOpaque": "mer_panel_red",
    "TFFatLineBorderBlueBG": "mer_panel_blue", "TFFatLineBorderBlueBGMoreOpaque": "mer_panel_blue",
    "TFFatLineBorderBlueBGOpaque": "mer_panel_blue", "TFFatLineBorderClearBG": "mer_inset",
    "GrayDialogBorder": "mer_panel_solid", "EconItemBorder": "mer_btn", "LoadoutItemMouseOverBorder": "mer_btn_hover",
    "LoadoutItemPopupBorder": "mer_panel_solid", "OutlinedGreyBox": "mer_btn_hover", "OutlinedDullGreyBox": "mer_btn",
    "MainMenuButtonGlow": "mer_btn_hover", "MainMenuButtonGlow2": "mer_btn_hover",
    "NotificationDefault": "mer_panel", "NotificationHighPriority": "mer_panel_red",
    "MainMenuButtonDepressed": "mer_btn_press", "MainMenuButtonDepressedArmed": "mer_btn_press",
    "MainMenuButtonDefault": "mer_btn", "MainMenuButtonArmed": "mer_btn_hover", "MainMenuButtonDisabled": "mer_panel",
    "MainMenuMiniButtonDefault": "mer_btn", "MainMenuMiniButtonArmed": "mer_btn_hover",
    "MainMenuBGBorder": "mer_panel_solid", "MainMenuBGBorderAlpha": "mer_panel_solid", "MainMenuBlogTabBG": "mer_panel",
    "MainMenuHighlightBorder": "mer_panel_solid", "TrainingResultsBG": "mer_panel_solid",
    "ArmoryScrollbarBox": "mer_btn", "ArmoryScrollbarWell": "mer_inset",
    "RedWithThinBorder": "mer_panel_red", "BlueWithThinBorder": "mer_panel_blue",
    "ReplayDefaultBorder": "mer_panel_solid", "ReplayHighlightBorder": "mer_btn_hover",
}

# 1px outline borders (not images): TanDark became a light grey, which is too bright for an outline
OUTLINE_BORDERS = ("QuickplayBorder", "SortCategoryBorder")
OUTLINE = "60 68 82 255"

# the tan palette
COLORS = {
    "TanLight": TEXT, "TanDark": DIM, "TanDarker": "12 14 18 255", "HudOffWhite": "200 208 218 255",
    "GreenSolid": "46 110 70 255", "SaleGreen": "46 110 70 255", "CreditsGreen": "72 160 100 255",
    "Black": "16 18 24 255",  # was a brown-black, used for the tan-era text and bars
    "ProgressOffWhite": TEXT, "LighterDarkBrown": "34 38 46 255", "DarkBrown": "22 25 32 255",
}

# BaseSettings: control colours. Buttons are drawn from these colours (the "border" images above are
# only used where a panel names one explicitly), so this is what turns the tan buttons dark.
BTN, BTN_ARMED, BTN_PRESSED = "28 32 40 235", "46 52 64 235", "60 68 82 235"
BASE = {
    "Button.BgColor": BTN, "Button.ArmedBgColor": BTN_ARMED, "Button.SelectedBgColor": BTN_ARMED,
    "Button.DepressedBgColor": BTN_PRESSED, "Button.DepressedTextColor": WHITE,
    "Econ.Button.BgColor": BTN, "Econ.Button.ArmedBgColor": BTN_ARMED, "Econ.Button.DepressedBgColor": BTN_PRESSED,
    "Econ.Button.DepressedFgColor": WHITE,
    "Frame.BgColor": "12 14 18 235", "Frame.OutOfFocusBgColor": "12 14 18 235",
    "FrameTitleBar.TextColor": TEXT, "FrameTitleBar.DisabledTextColor": TEXT,
    "PropertySheet.TextColor": DIM, "PropertySheet.SelectedTextColor": TEXT,
    "RadioButton.TextColor": TEXT, "RadioButton.SelectedTextColor": TEXT, "ToggleButton.SelectedTextColor": TEXT,
    "ListPanel.TextColor": TEXT, "ListPanel.EmptyListInfoTextColor": DIM,
    "ListPanel.SelectedTextColor": WHITE, "ListPanel.SelectedBgColor": BTN_PRESSED,
    "ListPanel.SelectedOutOfFocusBgColor": BTN_ARMED,
    "CheckButton.TextColor": TEXT, "CheckButton.SelectedTextColor": TEXT, "CheckButton.Border1": DIM,
    "CheckButton.Border2": DIM, "CheckButton.Check": TEXT, "CheckButton.HighlightFgColor": WHITE,
    "TextEntry.TextColor": TEXT, "TextEntry.BgColor": "28 32 40 255", "TextEntry.CursorColor": TEXT,
    "TextEntry.SelectedBgColor": BTN_PRESSED,
    "Tooltip.TextColor": TEXT, "Tooltip.BgColor": "12 14 18 235",
}

FONTS = {
    "HudFontSmallBold": "MerBody", "HudFontSmallestBold": "MerLabel",
    "HudFontSmall": "MerBody", "HudFontSmallest": "MerLabel",
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


def patch_scheme(path):
    t = read(path)
    # borders (inside the Borders section only; the names are not unique across sections)
    i = t.index("\n\tBorders")
    j = t.index("\n\tCustomFontFiles")
    b = t[i:j]
    for name, tex in BORDERS.items():
        m = re.search(r'\n\t\t%s\s*\n\t\t\{.*?\n\t\t\}' % re.escape(name), b, re.S)
        if not m:
            raise SystemExit("scheme border not found: " + name)
        blk = m.group(0)
        blk = sub1(r'(\n\t\t\t"image"\s*)"[^"]*"', r'\1"meridian/%s"' % tex, blk, name + ".image")  # not the //"image" ones
        # flat texture: 1px corners, drawn 1 unit
        blk = re.sub(r'("src_corner_(?:height|width)"\s*)"\d+"', r'\1"1"', blk)
        blk = re.sub(r'("draw_corner_(?:height|width)"\s*)"\d+"', r'\1"1"', blk)
        b = b[:m.start()] + blk + b[m.end():]
    for name in OUTLINE_BORDERS:
        m = re.search(r'\n\t\t%s\s*\n\t\t\{.*?\n\t\t\}' % re.escape(name), b, re.S)
        if not m:
            raise SystemExit("scheme border not found: " + name)
        b = b[:m.start()] + m.group(0).replace('"TanDark"', '"%s"' % OUTLINE) + b[m.end():]
    t = t[:i] + b + t[j:]
    # BaseSettings colours
    for name, value in BASE.items():
        t = sub1(r'(\n\t\t%s\s+)"[^"]*"' % re.escape(name), lambda m: m.group(1) + '"' + value + '"', t, "base " + name)
    # colors
    for name, value in COLORS.items():
        t = sub1(r'(\n\t\t"%s"\s*)"[^"]*"' % re.escape(name), lambda m: m.group(1) + '"' + value + '"', t, "color " + name)
    write(path, t)


def block(text, name):
    m = re.search(r'\n\t"?%s"?\s*(?:\[[^\]]*\])?\s*\n\t\{.*?\n\t\}' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn):
    s, e = block(text, name)
    return text[:s] + fn(text[s:e]) + text[e:]


def setk(b, k, v):
    """Set a key in a top-level block (added when missing; [$...] copies dropped)."""
    b = re.sub(r'\n\t\t"%s"[^\n]*\[\$[^\n]*' % re.escape(k), "", b)
    if re.search(r'\n\t\t"%s"\s*"' % re.escape(k), b):
        return sub1(r'(\n\t\t"%s"\s*)"[^"]*"' % re.escape(k), lambda m: m.group(1) + '"' + v + '"', b, k)
    return b[:b.rindex("\n\t}")] + '\n\t\t"%s"\t\t"%s"' % (k, v) + b[b.rindex("\n\t}"):]


def hide_panel(b):
    """Park a panel as a 1x1 off screen (the game may still show it, but nothing is drawn)."""
    for k, v in (("xpos", "-10"), ("ypos", "-10"), ("wide", "1"), ("tall", "1")):
        b = setk(b, k, v)
    return b


def flat_fill(color):
    """An image panel drawn from art -> a flat fill."""
    def fn(b):
        b = re.sub(r'\n\t\t"(?:image|tileImage|scaleImage)"[^\n]*', "", b)
        return b[:b.rindex("\n\t}")] + '\n\t\t"fillcolor"\t\t"%s"' % color + b[b.rindex("\n\t}"):]
    return fn


def patch_mainmenu(src, dst):
    t = read(src)
    t = edit_block(t, "BackgroundFooter", flat_fill("10 12 16 245"))
    t = edit_block(t, "FooterLine", flat_fill("46 52 64 255"))
    # The "Featured" store item panel is gone; the friends list moves up into its place
    t = edit_block(t, "EventPromo", hide_panel)
    t = edit_block(t, "FriendsContainer", lambda b: setk(setk(b, "ypos", "160"), "tall", "250"))

    # inside the friends panel the list is anchored to the bottom ("rs1-10"); anchor it under the title
    def friends_inner(b):
        for name in ("SteamFriendsList", "InnerShadow", "BelowDarken"):
            m = re.search(r'\n\t\t"%s"\s*\n\t\t\{.*?\n\t\t\}' % name, b, re.S)
            if not m:
                raise SystemExit("FriendsContainer child not found: " + name)
            blk = m.group(0)
            blk = sub1(r'(\n\t\t\t"ypos"\s*)"rs1-10"', r'\1"30"', blk, name + ".ypos")
            blk = sub1(r'(\n\t\t\t"tall"\s*)"110"', r'\1"210"', blk, name + ".tall")
            b = b[:m.start()] + blk + b[m.end():]
        return b
    t = edit_block(t, "FriendsContainer", friends_inner)
    # Solid backdrop. The sepia photo behind the character is the 3D background map; vgui panels draw
    # over it, and the character panel (TFCharacterImage, zpos -99, hidden by the game while in a
    # match) sits above this one, so the character stays and the map goes. (It also covers the game
    # view behind the in-game pause menu; there is no way to tell the two apart in this file.)
    i = t.rindex("}")
    t = t[:i] + ('\t"MerBackdrop"\n\t{\n\t\t"ControlName"\t"ImagePanel"\n\t\t"fieldName"\t\t"MerBackdrop"\n'
                 '\t\t"xpos"\t\t\t"0"\n\t\t"ypos"\t\t\t"0"\n\t\t"zpos"\t\t\t"-150"\n\t\t"wide"\t\t\t"f0"\n'
                 '\t\t"tall"\t\t\t"480"\n\t\t"visible"\t\t"1"\n\t\t"enabled"\t\t"1"\n'
                 '\t\t"mouseinputenabled"\t"0"\n\t\t"fillcolor"\t\t"10 12 16 255"\n\t}\n') + t[i:]
    t = re.sub(r'(\n\s*"font"\s*)"(%s)"' % "|".join(FONTS), lambda m: m.group(1) + '"' + FONTS[m.group(2)] + '"', t)
    # dark text that sat on tan buttons -> light text; the light hover text -> white
    t = re.sub(r'("(?:default|armed|depressed)FgColor_override"\s*)"(?:46 43 42 255|235 226 202 255)"',
               lambda m: m.group(1) + '"' + (TEXT if "default" in m.group(1) else WHITE) + '"', t)
    t = re.sub(r'("fgcolor"\s*)"LabelDark"', r'\1"%s"' % DIM, t)
    # the top-right image buttons are tinted cream; their textures are recoloured (gen_menu_icons.py), so no tint
    t = re.sub(r'("image_drawcolor"\s*)"235 226 202 255"', r'\1"%s"' % WHITE, t)
    t = re.sub(r'("fgcolor(?:_override)?"\s*)"23[45] 22[67] 20[23] 255"', r'\1"%s"' % TEXT, t)  # cream text
    write(dst, t)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock_ui, mer = sys.argv[1], sys.argv[2]
    patch_scheme(os.path.join(mer, "resource", "clientscheme.res"))
    patch_mainmenu(os.path.join(stock_ui, "mainmenuoverride.res"), os.path.join(mer, "resource", "ui", "mainmenuoverride.res"))
    print("patched clientscheme.res (%d borders, %d colours) and mainmenuoverride.res" % (len(BORDERS), len(COLORS)))


if __name__ == "__main__":
    main()

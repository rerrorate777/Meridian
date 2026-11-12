#!/usr/bin/env python3
"""HUD pieces that were still stock: the control point icons' text and the stalemate / sudden death box.

Usage: patch_hudmisc.py <stock resource/ui dir> <meridian resource/ui dir>

  * controlpointicon.res / controlpointcountdown.res   Meridian fonts and colours for the capture count
    and countdown (the icons themselves are recoloured textures: tools/gen_cp_icons.py)
  * votehud.res   the Call Vote dialog (Vote Setup): Meridian fonts, flat combo box and buttons, an accent line,
    the title centred over the dialog. (The list colours - stock orange headings, red selection - are
    scheme colours: tools/patch_menus.py.) The vote popups are left as they are.
  * hudstalemate.res   the box shown on "Sudden death" / "teams balanced": flat dark panel with an accent
    edge instead of the cream-bordered art, and the text centred inside it (stock left-aligns it)

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_matchmaking as mm  # noqa: E402
import patch_menus as pm  # noqa: E402

TEXT = "236 240 244 255"
DIM = "150 160 172 255"
FONTS = {"CapPlayerFont": "MerNumberSmall", "CapPlayerFontSmall": "MerLabel", "ControlPointTimer": "MerNumberSmall",
         "ControlPointTimerSmaller": "MerLabel", "HudFontMedium": "MerNumberSmall", "HudFontMediumSmall": "MerLabel"}


def fonts(t):
    return re.sub(r'(\n\s*"font(?:_minmode)?"\s*)"(%s)"' % "|".join(FONTS), lambda m: m.group(1) + '"' + FONTS[m.group(2)] + '"', t)


def patch_stalemate(t):
    t = mm.edit_block(t, "HudStalemateBG", lambda b: pm.setk(pm.setk(b, "image", "meridian/mer_panel"), "tall", "100"))
    t = mm.edit_block(t, "StalemateLabel", lambda b: pm.setk(pm.setk(pm.setk(pm.setk(pm.setk(
        b, "xpos", "20"), "font", "MerTitle"), "textAlignment", "north"), "fgcolor", TEXT), "ypos", "12"))
    t = mm.edit_block(t, "ReasonLabel", lambda b: pm.setk(pm.setk(pm.setk(pm.setk(pm.setk(
        b, "xpos", "20"), "font", "MerBody"), "textAlignment", "north"), "fgcolor", DIM), "ypos", "42"))
    accent = ('\t"HudStalemateAccent"\n\t{\n\t\t"ControlName"\t"ImagePanel"\n\t\t"fieldName"\t\t"HudStalemateAccent"\n'
              '\t\t"xpos"\t\t\t"0"\n\t\t"ypos"\t\t\t"0"\n\t\t"zpos"\t\t\t"2"\n\t\t"wide"\t\t\t"320"\n\t\t"tall"\t\t\t"3"\n'
              '\t\t"visible"\t\t"1"\n\t\t"enabled"\t\t"1"\n\t\t"fillcolor"\t\t"150 160 172 255"\n\t}\n')
    i = t.rindex("}")
    return t[:i] + accent + t[i:]


def patch_votehud(t):
    def dialog(b):
        for k, old, new in (("header_font", "ItemFontNameLarge", "MerBody"), ("header_fgcolor", "Orange", DIM),
                            ("issue_font", "ItemFontNameSmall", "MerBody"), ("issue_fgcolor", "TanLight", TEXT)):
            b = mm.sub1(r'(\n\t\t"%s"\s*)"%s"' % (k, old), r'\g<1>"%s"' % new, b, k)

        def title(m):  # the stock label is 550 wide in a 600 wide dialog, so the title sat off centre
            blk = mm.sub1(r'(\n\t\t\t"font"\s*)"[^"]*"', r'\1"MerTitle"', m.group(0), "TitleLabel.font")
            return mm.sub1(r'(\n\t\t\t"wide"\s*)"[^"]*"', r'\1"600"', blk, "TitleLabel.wide")
        b = re.sub(r'\n\t\t"TitleLabel"\s*\n\t\t\{.*?\n\t\t\}', title, b, count=1, flags=re.S)

        def combo(m):  # the cream drop-down box
            blk = m.group(0)
            for k, v in (("fgcolor_override", TEXT), ("bgcolor_override", "28 32 40 255"),
                         ("disabledFgColor_override", DIM), ("disabledBgColor_override", "28 32 40 255"),
                         ("selectionColor_override", "60 68 82 255"), ("selectionTextColor_override", TEXT),
                         ("defaultSelectionBG2Color_override", "60 68 82 255")):
                blk = mm.sub1(r'(\n\t\t\t"%s"\s*)"[^"]*"' % k, r'\g<1>"%s"' % v, blk, "ComboBox." + k)
            return blk
        b = re.sub(r'\n\t\t"ComboBox"\s*\n\t\t\{.*?\n\t\t\}', combo, b, count=1, flags=re.S)
        # a plain vgui "Button" ignores border_default and draws the scheme's rounded ButtonBorder
        for n in ("CallVoteButton", "Button1"):
            b = mm.sub1(r'(\n\t\t"%s"\s*\n\t\t\{\s*\n\t\t\t"ControlName"\s*)"Button"' % n, r'\1"CExButton"', b, n + ".ControlName")
        accent = ('\n\t\t"VoteAccent"\n\t\t{\n\t\t\t"ControlName"\t"ImagePanel"\n\t\t\t"fieldName"\t\t"VoteAccent"\n'
                  '\t\t\t"xpos"\t\t"0"\n\t\t\t"ypos"\t\t"0"\n\t\t\t"zpos"\t\t"3"\n\t\t\t"wide"\t\t"600"\n'
                  '\t\t\t"tall"\t\t"3"\n\t\t\t"visible"\t"1"\n\t\t\t"enabled"\t"1"\n'
                  '\t\t\t"fillcolor"\t"150 160 172 255"\n\t\t}')
        k = b.rindex("\n\t}")
        return b[:k] + accent + b[k:]
    t = mm.edit_block(t, "VoteSetupDialog", dialog)
    t, _ = mm.style_buttons(t, {"CallVoteButton", "Button1"})
    return t


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    for name in ("controlpointicon.res", "controlpointcountdown.res", "hudstalemate.res", "votehud.res"):
        t = mm.read(os.path.join(stock, name))
        t = fonts(mm.generic(t))
        t = re.sub(r'("fgcolor"\s*)"235 226 202 255"', r'\1"%s"' % TEXT, t)
        if name == "hudstalemate.res":
            t = patch_stalemate(t)
        if name == "votehud.res":
            t = patch_votehud(t)
        mm.write(os.path.join(mer, name), t)
        print("patched", name)


if __name__ == "__main__":
    main()

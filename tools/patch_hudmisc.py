#!/usr/bin/env python3
"""HUD pieces that were still stock: the control point icons' text and the stalemate / sudden death box.

Usage: patch_hudmisc.py <stock resource/ui dir> <meridian resource/ui dir>

  * controlpointicon.res / controlpointcountdown.res   Meridian fonts and colours for the capture count
    and countdown (the icons themselves are recoloured textures: tools/gen_cp_icons.py)
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


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    for name in ("controlpointicon.res", "controlpointcountdown.res", "hudstalemate.res"):
        t = mm.read(os.path.join(stock, name))
        t = fonts(mm.generic(t))
        t = re.sub(r'("fgcolor"\s*)"235 226 202 255"', r'\1"%s"' % TEXT, t)
        if name == "hudstalemate.res":
            t = patch_stalemate(t)
        mm.write(os.path.join(mer, name), t)
        print("patched", name)


if __name__ == "__main__":
    main()

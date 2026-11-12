#!/usr/bin/env python3
"""Restyle the Loadout screens (class picker, class page, item picker, backpack, crafting, inspection,
item dialogs) from the stock files.

Usage: patch_loadout.py <stock resource/ui dir> <meridian resource/ui dir>

  * every loadout / econ file: the same font and colour pass as the Find a Game screens
    (patch_matchmaking.generic) plus the footer-button style on the "BackButton"
  * charinfopanel.res (the frame): flat header, footer and divider lines instead of the striped
    brown art; Meridian tab colours

The panel borders and button colours come from clientscheme.res (tools/patch_menus.py). Item art, class
portraits and the large icons (backpack, anvil, catalogue...) are stock images and stay.

Files that do not change are not written. Every charinfopanel edit must match exactly once, otherwise
the script aborts (see patch_layout.py).
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_matchmaking as mm  # noqa: E402

FILE_RE = re.compile(r"(charinfo|classloadout|loadoutpreset|itemselection|itemslot|crafting|giveaway|importpreview|"
                     r"itemoptions|itemrename|itemdiscard|itempickup|inspection|paintkit|collection|manncotrade|"
                     r"backpack|store|quest|armory|mvmecon)")
PANEL = "12 14 18 255"
LINE = "46 52 64 255"
TEXT = "236 240 244 255"
DIM = "150 160 172 255"


def flat(color, tall=None):
    """An image panel drawn from art -> a flat fill (key indent: the block's own keys)."""
    def fn(b):
        ind = re.search(r'\n([ \t]*)"ControlName"', b).group(1)
        b = re.sub(r'\n[ \t]*"(?:image|tileImage|scaleImage)"[^\n]*', "", b)
        if tall is not None:
            b = mm.sub1(r'(\n%s"tall"\s*)"[^"]*"' % ind, r'\g<1>"%s"' % tall, b, "tall")
        k = b.rindex("}")
        return b[:k].rstrip("\t") + '%s"fillcolor"\t\t"%s"\n%s' % (ind, color, ind[:-1] if ind else "") + b[k:]
    return fn


def patch_charinfo(t):
    t = mm.edit_block(t, "BackgroundHeader", flat(PANEL))
    t = mm.edit_block(t, "BackgroundFooter", flat("10 12 16 255"))  # opaque: the main menu's buttons are behind
    t = mm.edit_block(t, "FooterLine", flat(LINE, tall="2"))
    t = mm.edit_block(t, "HeaderLine", flat(LINE, tall="2"), "\t\t")
    # tab text colours (selected / unselected)
    t = mm.sub1(r'("selectedcolor"\s*)"[^"]*"', r'\1"%s"' % TEXT, t, "selectedcolor")
    t = mm.sub1(r'("unselectedcolor"\s*)"[^"]*"', r'\1"%s"' % DIM, t, "unselectedcolor")
    t = mm.sub1(r'("titlebarfgcolor_override"\s*)"[^"]*"', r'\1"%s"' % TEXT, t, "titlebarfgcolor")
    t = mm.sub1(r'("titlebardisabledfgcolor_override"\s*)"[^"]*"', r'\1"%s"' % TEXT, t, "titlebardisabledfgcolor")
    return t


def flat_lines(t):
    """Image panels that draw the tan dotted / solid divider art -> a thin flat line."""
    pat = re.compile(r'"image"\s*"(?:loadout_dotted_line|loadout_solid_line)"')
    out, pos = [], 0
    for m in pat.finditer(t):
        if m.start() < pos:
            continue
        open_i = t.rindex("{", 0, m.start())
        close_i = mm.match_brace(t, open_i)
        blk = t[open_i:close_i]
        if '"ControlName"' not in blk or "ImagePanel" not in blk.split('"ControlName"')[1][:40]:
            continue
        # indent of the block's own keys, then reuse flat() on "\n<indent-1>{...}"-shaped text
        out.append(t[pos:open_i] + flat(LINE, tall="2")(blk))
        pos = close_i
    out.append(t[pos:])
    return "".join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    paths = sorted(p for p in glob.glob(os.path.join(stock, "*.res")) if FILE_RE.match(os.path.basename(p)))
    paths += sorted(glob.glob(os.path.join(stock, "econ", "**", "*.res"), recursive=True))
    n = styled = 0
    for path in paths:
        rel = os.path.relpath(path, stock)
        t = mm.read(path)
        out = mm.generic(t)
        out = flat_lines(out) if rel != "charinfopanel.res" else out
        if rel == "charinfopanel.res":
            out = patch_charinfo(out)
        out, nb = mm.style_buttons(out)
        styled += nb
        if out != t:
            dst = os.path.join(mer, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            mm.write(dst, out)
            n += 1
    print("patched %d files, %d buttons styled" % (n, styled))


if __name__ == "__main__":
    main()

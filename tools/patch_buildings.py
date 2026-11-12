#!/usr/bin/env python3
"""Restyle the Engineer/Spy building status list (top-left) from the stock files.

Usage: patch_buildings.py <stock dir> <meridian dir>

<stock dir> holds scripts/mod_textures.txt and resource/ui/hud_obj_*.res, e.g. extracted with
  tools/vpk_extract.py ".../tf/tf2_misc_dir.vpk" STOCK 'scripts/mod_textures.txt' 'resource/ui/hud_obj_*.res'

  * scripts/mod_textures.txt   the building panel backgrounds (CIconPanel icons that the game
                               swaps by team / state) are pointed at flat Meridian panels
  * resource/ui/hud_obj_*.res  labels use the Meridian font and colour; backgrounds are trimmed
                               so stacked panels have a gap

Every edit must match, otherwise the script aborts (see patch_layout.py).
"""
import glob
import os
import re
import sys

# icon name -> (Meridian material under materials/vgui/meridian/, width, height in pixels)
BACKGROUNDS = {
    "obj_status_background_blue": ("mer_panel_blue", 4, 4),
    "obj_status_background_red": ("mer_panel_red", 4, 4),
    "obj_status_background_disabled": ("mer_panel", 4, 4),
    "obj_status_background_tall_blue": ("mer_panel_blue", 4, 4),
    "obj_status_background_tall_red": ("mer_panel_red", 4, 4),
    "obj_status_background_tall_disabled": ("mer_panel", 4, 4),
    # NOT replaced: obj_status_alert_background and obj_status_alert_background_tall, the tray
    # that appears beside a row when a building is damaged or sapped. The game hides the stock
    # art at rest by tinting it transparent; a replacement texture ignored that and showed the
    # tray permanently (it even showed for "can be upgraded").
    "obj_status_alert_background_tall_nocolor": ("mer_panel", 4, 4),
}
LABEL_FONTS = ("DefaultVerySmall", "DefaultSmall")
BG_TRIM = 3  # shave the backgrounds so stacked panels show a gap instead of one dark slab
TEXT = "236 240 244 255"


def read(path):
    return open(path, encoding="utf-8", errors="surrogateescape", newline="").read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(text)


def patch_textures(src, dst):
    t = read(src)
    for name, (mat, tw, th) in BACKGROUNDS.items():
        pat = r'("%s"\s*\{)([^{}]*?)(\})' % re.escape(name)
        m = re.search(pat, t)
        if not m or len(re.findall(pat, t)) != 1:
            raise SystemExit("mod_textures: expected exactly one entry for " + name)
        body = m.group(2)
        for key, val in (("file", "vgui/meridian/" + mat), ("x", "0"), ("y", "0"),
                         ("width", str(tw)), ("height", str(th))):
            body, n = re.subn(r'("%s"\s*)"[^"]*"' % key, lambda k: k.group(1) + '"' + val + '"', body)
            if n != 1:
                raise SystemExit("mod_textures: %s has no single %s" % (name, key))
        t = t[:m.start(2)] + body + t[m.end(2):]
    write(dst, t)


def patch_res(src, dst):
    t = read(src)
    out, n = re.subn(
        r'("font"\s*)"(%s)"([^\n]*)' % "|".join(LABEL_FONTS),
        lambda m: '%s"MerLabel"%s\n\t\t\t"fgcolor"\t\t"%s"' % (m.group(1), m.group(3), TEXT),
        t,
    )
    if n == 0:
        raise SystemExit("%s: no label fonts found" % src)
    # Background panel: 3 units shorter, nudged down 1 so the contents stay centred.
    pat = r'(\n\t"Background"\s*\{[^{}]*?"ypos"\s*)"0"([^{}]*?"tall"\s*)"(\d+)"'
    m = re.search(pat, out)
    if not m:
        raise SystemExit("%s: Background block not found" % src)
    out = out[:m.start()] + m.group(1) + '"1"' + m.group(2) + '"%d"' % (int(m.group(3)) - BG_TRIM) + out[m.end():]
    write(dst, out)
    return n


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    stock, mer = sys.argv[1], sys.argv[2]
    patch_textures(os.path.join(stock, "scripts", "mod_textures.txt"),
                   os.path.join(mer, "scripts", "mod_textures.txt"))
    print("scripts/mod_textures.txt: %d backgrounds" % len(BACKGROUNDS))
    for path in sorted(glob.glob(os.path.join(stock, "resource", "ui", "hud_obj_*.res"))):
        name = os.path.basename(path)
        n = patch_res(path, os.path.join(mer, "resource", "ui", name))
        print("resource/ui/%s: %d labels" % (name, n))


if __name__ == "__main__":
    main()

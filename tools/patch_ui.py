#!/usr/bin/env python3
"""Derive the lightly-modified UI files in meridian/resource/ui from the stock ones.

Usage: patch_ui.py <stock resource/ui dir> <output resource/ui dir>

Covers:
  * targetid.res                    flat team-tinted background, Meridian fonts
  * huditemeffectmeter_*.res        roots moved into the bottom row left of the ammo dock
Every edit must match, otherwise the script aborts (see patch_layout.py).
"""
import glob
import os
import re
import sys

ITEM_METER_X = "r260"
ITEM_METER_Y_SHIFT = 18  # stock y (r57 for most meters) -> r75, keeps stacked meters stacked
ITEM_METER_Y_SHIFT_STACKED = 28  # meters stock-placed above the pipes/metal row (r92 -> r120)
ITEM_METER_SKIP = {
    "huditemeffectmeter.res",  # fully restyled, hand written
    "huditemeffectmeter_kartcharge.res",
    "huditemeffectmeter_halloweensouls.res",
    "huditemeffectmeter_powerupbottle.res",
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


def block(text, name):
    m = re.search(r'\n\t"%s"\s*\n\t\{.*?\n\t\}' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.span()


def edit_block(text, name, fn):
    s, e = block(text, name)
    return text[:s] + fn(text[s:e]) + text[e:]


def set_key(blk, key, value, what):
    pat = r'(\n\t\t"%s"\s*)"[^"]*"' % re.escape(key)
    return sub1(pat, lambda m: m.group(1) + '"' + value + '"', blk, what + "." + key)


def drop_keys(blk, keys):
    for key in keys:
        blk = re.sub(r'\n\t\t"%s"[^\n]*' % re.escape(key), "", blk)
    return blk


def patch_targetid(src, dst):
    t = read(src)
    corner = ["src_corner_height", "src_corner_width", "draw_corner_width", "draw_corner_height"]

    def bg(b):
        b = drop_keys(b, corner)
        b = set_key(b, "tall", "40", "TargetIDBG")
        b = set_key(b, "image", "../hud/mer_panel", "TargetIDBG")
        b = set_key(b, "teambg_1", "../hud/mer_panel", "TargetIDBG")
        b = set_key(b, "teambg_2", "../hud/mer_panel_red", "TargetIDBG")
        b = set_key(b, "teambg_2_lodef", "../hud/mer_panel_red", "TargetIDBG")
        b = set_key(b, "teambg_3", "../hud/mer_panel_blue", "TargetIDBG")
        b = set_key(b, "teambg_3_lodef", "../hud/mer_panel_blue", "TargetIDBG")
        return b

    def spec(img):
        def f(b):
            b = set_key(b, "image", "../hud/" + img, "spec bg")
            b = set_key(b, "image_lodef", "../hud/" + img, "spec bg")
            b = set_key(b, "tall", "30", "spec bg")
            b = drop_keys(b, corner)
            return b
        return f

    def name_label(b):
        b = set_key(b, "font", "MerTitle", "TargetNameLabel")
        b = set_key(b, "ypos", "3", "TargetNameLabel")
        b = set_key(b, "tall", "18", "TargetNameLabel")
        return b.replace('\n\t\t"visible"', '\n\t\t"fgcolor"\t\t"236 240 244 255"\n\t\t"visible"', 1)

    def data_label(b):
        b = set_key(b, "font", "MerBody", "TargetDataLabel")
        b = re.sub(r'\n\t\t"ypos"\s*"17"\s*\[\$WIN32\]', '\n\t\t"ypos"\t\t\t"21"\t[$WIN32]', b)
        b = set_key(b, "tall", "14", "TargetDataLabel")
        return b.replace('\n\t\t"visible"', '\n\t\t"fgcolor"\t\t"150 160 172 255"\n\t\t"visible"', 1)

    t = edit_block(t, "TargetIDBG", bg)
    t = edit_block(t, "TargetIDBG_Spec_Blue", spec("mer_panel_blue"))
    t = edit_block(t, "TargetIDBG_Spec_Red", spec("mer_panel_red"))
    t = edit_block(t, "TargetNameLabel", name_label)
    t = edit_block(t, "TargetDataLabel", data_label)
    write(dst, t)


def patch_item_meter(src, dst):
    t = read(src)
    m = re.search(r'\n\tHudItemEffectMeter\s*\n\t\{.*?\n\t\}', t, re.S)
    if not m:
        raise SystemExit("root not found in " + src)
    blk = m.group(0)

    def ypos(mm):
        old = int(mm.group(2))
        shift = ITEM_METER_Y_SHIFT_STACKED if old >= 80 else ITEM_METER_Y_SHIFT
        return mm.group(1) + '"r%d"' % (old + shift)

    new = re.sub(r'(\n\t\t"xpos"\s*)"r?\d+"(?=\s*(\[\$WIN32\])?\s*\n)', lambda mm: mm.group(1) + '"%s"' % ITEM_METER_X, blk)
    new = re.sub(r'(\n\t\t"ypos"\s*)"r(\d+)"(?=\s*(\[\$WIN32\])?\s*\n)', ypos, new)
    if new == blk:
        raise SystemExit("no position change in " + src)
    write(dst, t[:m.start()] + new + t[m.end():])


def main(stock, out):
    os.makedirs(out, exist_ok=True)
    patch_targetid(os.path.join(stock, "targetid.res"), os.path.join(out, "targetid.res"))
    n = 0
    for path in sorted(glob.glob(os.path.join(stock, "huditemeffectmeter_*.res"))):
        name = os.path.basename(path)
        if name in ITEM_METER_SKIP:
            continue
        patch_item_meter(path, os.path.join(out, name))
        n += 1
    print("patched targetid.res and %d item meters -> %s" % (n, out))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])

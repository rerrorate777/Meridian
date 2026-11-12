#!/usr/bin/env python3
"""Recolour the four image buttons at the top right of the main menu (alert, streaming, quests, MOTD).

Usage: gen_menu_icons.py <tf2_textures_dir.vpk> <meridian dir>

Each stock icon is one 128x128 image: a brown rounded square with a cream glyph. They cannot be
restyled from a .res file, so the textures are recoloured and shipped under the same names
(materials/vgui/button_*.vtf): pixel luminance is remapped from the stock brown..cream range to
Meridian dark..light, and the alpha (the rounded square) is kept.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_textures  # noqa: E402  (vtf() writer)
import vpk_extract  # noqa: E402

ICONS = ("button_alert", "button_streaming", "button_quests_pda", "button_motd")
DARK = (28, 32, 40)
LIGHT = (236, 240, 244)
SIZE = 128


def top_mip_bgra(vtf):
    w, h = struct.unpack("<HH", vtf[16:20])
    fmt = struct.unpack("<i", vtf[52:56])[0]
    if (w, h, fmt) != (SIZE, SIZE, 12):  # 12 = BGRA8888
        raise SystemExit("unexpected icon format: %dx%d fmt %d" % (w, h, fmt))
    return vtf[-w * h * 4:]  # mips are stored smallest first, so the largest is last


def recolor(bgra):
    px = [(bgra[i + 2], bgra[i + 1], bgra[i], bgra[i + 3]) for i in range(0, len(bgra), 4)]
    lum = sorted(0.299 * r + 0.587 * g + 0.114 * b for r, g, b, a in px if a > 200)
    lo, hi = lum[int(len(lum) * 0.05)], lum[int(len(lum) * 0.95)]
    out = []
    for r, g, b, a in px:
        t = (0.299 * r + 0.587 * g + 0.114 * b - lo) / max(hi - lo, 1)
        t = min(max(t, 0.0), 1.0)
        out.append(tuple(round(DARK[k] + (LIGHT[k] - DARK[k]) * t) for k in range(3)) + (a,))
    return [out[y * SIZE:(y + 1) * SIZE] for y in range(SIZE)]


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    vpk, mer = sys.argv[1], sys.argv[2]
    outdir = os.path.join(mer, "materials", "vgui")
    os.makedirs(outdir, exist_ok=True)
    for name in ICONS:
        data = vpk_extract.extract_bytes(vpk, "materials/vgui/%s.vtf" % name)
        if data is None:
            raise SystemExit("not found in the VPK: " + name)
        rows = recolor(top_mip_bgra(data))
        with open(os.path.join(outdir, name + ".vtf"), "wb") as f:
            f.write(gen_textures.vtf(SIZE, SIZE, rows))
        with open(os.path.join(outdir, name + ".vmt"), "w") as f:
            f.write('"UnlitGeneric"\n{\n\t"$basetexture"\t"vgui/%s"\n\t"$translucent"\t"1"\n\t"$ignorez"\t"1"\n'
                    '\t"$vertexcolor"\t"1"\n\t"$vertexalpha"\t"1"\n}\n' % name)
        print("wrote", name)


if __name__ == "__main__":
    main()

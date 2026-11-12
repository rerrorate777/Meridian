#!/usr/bin/env python3
"""Recolour the control point icons (sprites/obj_icons/icon_obj_*) in the Meridian palette.

Usage: gen_cp_icons.py <tf2_textures_dir.vpk> <meridian dir>

The stock icons are a team-coloured rounded square with a cream border and a cream lock / letter /
number. Each pixel's luminance is remapped: the body becomes the Meridian dark tint of its team (blue,
red or neutral, taken from the file name) and the cream border/glyph becomes the Meridian light, with a
smoothstep so the body stays flat and the glyph crisp. The alpha (the rounded shape) is kept. Written as
128x128 RGBA textures under the same names, so they override the stock ones (the .vmt files are the
game's own).

Handles BGRA8888 and DXT5 sources (the only formats these icons use).
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_textures  # noqa: E402  (vtf() writer)
import vpk_extract  # noqa: E402

LIGHT = (236, 240, 244)
BODY = {"blu": (28, 58, 92), "red": (86, 34, 30), "neutral": (28, 32, 40)}
SIZE = 128
# icon_obj_*, icon_obj_N_*, the lettered ones, and the base icons. Not: cap_* / timer (progress art).
PREFIXES = ("icon_obj_", "icon_base_")
SKIP = ("icon_obj_cap_", "icon_obj_timer")


def team(name):
    if "_red" in name:
        return "red"
    if "_blu" in name:
        return "blu"
    return "neutral"


def rgb565(c):
    return (((c >> 11) & 31) * 255 // 31, ((c >> 5) & 63) * 255 // 63, (c & 31) * 255 // 31)


def decode_dxt5(data, w, h):
    px = [None] * (w * h)
    pos = 0
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            a0, a1 = data[pos], data[pos + 1]
            bits = int.from_bytes(data[pos + 2:pos + 8], "little")
            c0, c1 = struct.unpack("<HH", data[pos + 8:pos + 12])
            ci = struct.unpack("<I", data[pos + 12:pos + 16])[0]
            pos += 16
            if a0 > a1:
                al = [a0, a1] + [((7 - i) * a0 + i * a1) // 7 for i in range(1, 7)]
            else:
                al = [a0, a1] + [((5 - i) * a0 + i * a1) // 5 for i in range(1, 5)] + [0, 255]
            r0, r1 = rgb565(c0), rgb565(c1)
            cols = [r0, r1,
                    tuple((2 * r0[k] + r1[k]) // 3 for k in range(3)),
                    tuple((r0[k] + 2 * r1[k]) // 3 for k in range(3))]
            for i in range(16):
                x, y = bx + (i & 3), by + (i >> 2)
                r, g, b = cols[(ci >> (2 * i)) & 3]
                px[y * w + x] = (r, g, b, al[(bits >> (3 * i)) & 7])
    return px


def decode(vtf):
    w, h = struct.unpack("<HH", vtf[16:20])
    fmt = struct.unpack("<i", vtf[52:56])[0]
    if (w, h) != (SIZE, SIZE):
        return None
    if fmt == 15:  # DXT5, largest mip last: sizes of all mips below it are summed
        size = w * h
        return decode_dxt5(vtf[-size:], w, h)
    if fmt == 12:  # BGRA8888
        d = vtf[-w * h * 4:]
        return [(d[i + 2], d[i + 1], d[i], d[i + 3]) for i in range(0, len(d), 4)]
    return None


def smoothstep(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)


def recolor(px, body):
    lum = sorted(0.299 * r + 0.587 * g + 0.114 * b for r, g, b, a in px if a > 200)
    lo, hi = lum[int(len(lum) * 0.05)], lum[int(len(lum) * 0.95)]
    out = []
    for r, g, b, a in px:
        t = (0.299 * r + 0.587 * g + 0.114 * b - lo) / max(hi - lo, 1)
        t = smoothstep(0.5, 0.75, t)
        out.append(tuple(round(body[k] + (LIGHT[k] - body[k]) * t) for k in range(3)) + (a,))
    return [out[y * SIZE:(y + 1) * SIZE] for y in range(SIZE)]


def tail_size(vtf):
    return None


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    vpk, mer = sys.argv[1], sys.argv[2]
    outdir = os.path.join(mer, "materials", "sprites", "obj_icons")
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for full, *_ in vpk_extract.entries(vpk):
        low = full.lower()
        base = os.path.basename(low)
        if not (low.startswith("materials/sprites/obj_icons/") and low.endswith(".vtf")):
            continue
        if not base.startswith(PREFIXES) or base.startswith(SKIP):
            continue
        px = decode(vpk_extract.extract_bytes(vpk, full))
        if px is None:
            continue
        rows = recolor(px, BODY[team(base)])
        with open(os.path.join(outdir, base), "wb") as f:
            f.write(gen_textures.vtf(SIZE, SIZE, rows))
        n += 1
    print("wrote %d icons to %s" % (n, outdir))


if __name__ == "__main__":
    main()

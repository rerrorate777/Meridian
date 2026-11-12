#!/usr/bin/env python3
"""Generate the small set of HUD textures used by Meridian (VTF 7.2 + VMT).

Output goes to meridian/materials/hud/. No third-party dependencies.
Re-run after changing the palette below.
"""
import os
import struct

OUT = os.path.join(os.path.dirname(__file__), "..", "meridian", "materials", "vgui", "meridian")

# name -> RGBA, translucent panel fills (neutral / team tinted)
PANELS = {
    "mer_panel": (12, 14, 18, 205),
    "mer_panel_red": (86, 34, 30, 215),
    "mer_panel_blue": (28, 58, 92, 215),
}

# name -> RGB. Keep in sync with the colours referenced in the .res files.
SOLIDS = {
    "mer_solid": (255, 255, 255),
    "mer_red": (224, 84, 72),
    "mer_blue": (76, 156, 232),
    "mer_alert": (255, 70, 56),
    "mer_uber": (126, 224, 150),
}

# VTF flags: CLAMPS | CLAMPT | NOMIP | NOLOD | EIGHTBITALPHA
FLAGS = 0x4 | 0x8 | 0x100 | 0x200 | 0x2000
FMT_RGBA8888 = 0


def vtf(width, height, rgba_rows):
    header = struct.pack(
        "<4s2I I 2H I 2H 4x 3f 4x f i B i 2B H",
        b"VTF\0",
        7, 2,
        80,
        width, height,
        FLAGS,
        1, 0,
        1.0, 1.0, 1.0,
        1.0,
        FMT_RGBA8888,
        1,
        -1, 0, 0,
        1,
    )
    header = header.ljust(80, b"\0")
    data = b"".join(bytes(px) for row in rgba_rows for px in row)
    return header + data


def vmt(texture):
    return (
        '"UnlitGeneric"\n{\n'
        f'\t"$basetexture"\t"vgui/meridian/{texture}"\n'
        '\t"$vertexcolor"\t"1"\n'
        '\t"$vertexalpha"\t"1"\n'
        '\t"$translucent"\t"1"\n'
        '\t"$ignorez"\t"1"\n'
        '\t"$nolod"\t"1"\n'
        '\t"$nocull"\t"1"\n'
        "}\n"
    )


def write(name, w, h, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".vtf"), "wb") as f:
        f.write(vtf(w, h, rows))
    with open(os.path.join(OUT, name + ".vmt"), "w") as f:
        f.write(vmt(name))


# Top-centre match timer notch (replaces hud/comp_round_timer). The panel is drawn with
# aspect 3.833:1 ("o3.833" in hudroundcounter.res).
TIMER = "mer_timer"
TIMER_W, TIMER_H = 256, 64  # power of two; stretched very slightly to the 3.833:1 panel
TIMER_BAR = 8  # px: blue | red team bar along the top edge
TIMER_INSET = 0.07  # bottom edge is this fraction of the width narrower on each side
TIMER_BODY = (20, 23, 30, 235)
TIMER_BLUE = (76, 156, 232, 255)  # = mer_blue
TIMER_RED = (224, 84, 72, 255)  # = mer_red
SS = 4  # supersampling per axis for the slanted edges


def timer_rows():
    rows = []
    for y in range(TIMER_H):
        row = []
        for x in range(TIMER_W):
            cov = 0
            for sy in range(SS):
                for sx in range(SS):
                    fy = (y + (sy + 0.5) / SS) / TIMER_H
                    fx = (x + (sx + 0.5) / SS) / TIMER_W
                    edge = TIMER_INSET * fy
                    cov += edge <= fx <= 1 - edge
            a = cov / (SS * SS)
            if y < TIMER_BAR:
                r, g, b, _ = TIMER_BLUE if x < TIMER_W // 2 else TIMER_RED
                base_a = 255
            else:
                r, g, b, base_a = TIMER_BODY
            row.append((r, g, b, round(base_a * a)))
        rows.append(row)
    return rows


def main():
    for name, (r, g, b) in SOLIDS.items():
        write(name, 4, 4, [[(r, g, b, 255)] * 4 for _ in range(4)])
    for name, rgba in PANELS.items():
        write(name, 4, 4, [[rgba] * 4 for _ in range(4)])
    write(TIMER, TIMER_W, TIMER_H, timer_rows())
    print("wrote", len(SOLIDS) + len(PANELS) + 1, "textures to", os.path.normpath(OUT))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Print the Meridian font definitions for resource/clientscheme.res.

Sizes are authored in HUD units (the 480-unit-tall virtual screen) and expanded
into one entry per common 16:10 vertical resolution band, so the text scales
with the layout instead of staying a fixed pixel size.

16:10 heights: 800 (1280x800), 900 (1440x900), 1050 (1680x1050),
1200 (1920x1200), 1600 (2560x1600), 2400 (3840x2400).
"""

# (yres_low, yres_high, representative_height)
BANDS = [
    (1, 849, 800),
    (850, 999, 900),
    (1000, 1124, 1050),
    (1125, 1349, 1200),
    (1350, 1799, 1600),
    (1800, 99999, 2400),
]

# font id -> (family, weight, size in HUD units)
FONTS = {
    "MerHealth": ("Barlow Condensed", 700, 30),
    "MerAmmo": ("Barlow Condensed", 700, 30),
    "MerAmmoReserve": ("Barlow", 700, 15),
    "MerNumberMed": ("Barlow Condensed", 700, 18),
    "MerNumberSmall": ("Barlow Condensed", 700, 13),
    "MerTitle": ("Barlow", 700, 13),
    "MerBody": ("Barlow", 400, 11),
    "MerLabel": ("Barlow", 700, 8),
}


def block():
    out = ["\t\t// ---- Meridian ----"]
    for name, (family, weight, size) in FONTS.items():
        out.append(f'\t\t"{name}"\n\t\t{{')
        for i, (lo, hi, rep) in enumerate(BANDS, 1):
            tall = round(size * rep / 480)
            out.append(
                f'\t\t\t"{i}"\n\t\t\t{{\n'
                f'\t\t\t\t"name"\t\t"{family}"\n'
                f'\t\t\t\t"tall"\t\t"{tall}"\n'
                f'\t\t\t\t"weight"\t"{weight}"\n'
                f'\t\t\t\t"additive"\t"0"\n'
                f'\t\t\t\t"antialias"\t"1"\n'
                f'\t\t\t\t"yres"\t\t"{lo} {hi}"\n'
                "\t\t\t}"
            )
        out.append("\t\t}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(block(), end="")

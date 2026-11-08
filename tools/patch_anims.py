#!/usr/bin/env python3
"""Derive meridian/scripts/hudanimations_tf.txt from the stock file.

Usage: patch_anims.py <stock hudanimations_tf.txt> <output>

Only two things need to change for this HUD:
  * the "Ubercharge ready" flash, which stock animates between tan colours
  * the Spy disguise outline, which stock animates back to a hardcoded screen position
"""
import sys

DIM = "150 160 172 255"
TEXT = "236 240 244 255"
GREEN = "126 224 150 255"

# (old, new) - each old string must occur exactly once
EDITS = [
    ('Animate\tChargeLabel \tFgColor\t\t"TanLight"\t\tLinear 0.0 0.1',
     'Animate\tChargeLabel \tFgColor\t\t"%s"\t\tLinear 0.0 0.1' % GREEN),
    ('Animate\tChargeLabel \tFgColor\t\t"TanDarker"\t\tLinear 0.3 0.4',
     'Animate\tChargeLabel \tFgColor\t\t"%s"\t\tLinear 0.3 0.4' % DIM),
    ('Animate\tChargeMeter \tFgColor\t\t"TanLight"\t\tLinear 0.0 0.1',
     'Animate\tChargeMeter \tFgColor\t\t"%s"\t\tLinear 0.0 0.1' % GREEN),
    ('Animate\tChargeMeter \tFgColor\t\t"TanDarker"\t\tLinear 0.3 0.4',
     'Animate\tChargeMeter \tFgColor\t\t"%s"\t\tLinear 0.3 0.4' % TEXT),
    ('Animate\tChargeLabel \tFgColor\t\t"TanLight"\t\tLinear 0.0 0.0001',
     'Animate\tChargeLabel \tFgColor\t\t"%s"\t\tLinear 0.0 0.0001' % DIM),
    ('Animate\tChargeMeter \tFgColor\t\t"TanLight"\t\tLinear 0.0 0.0001',
     'Animate\tChargeMeter \tFgColor\t\t"%s"\t\tLinear 0.0 0.0001' % TEXT),
    # class icon cell of the health dock (see hudplayerclass.res)
    ('Animate PlayerStatusSpyOutlineImage\t\tPosition\t"3 413"\t\t\tLinear 0.0 0.2',
     'Animate PlayerStatusSpyOutlineImage\t\tPosition\t"28 420"\t\t\tLinear 0.0 0.2'),
    ('Animate PlayerStatusSpyOutlineImage\t\tSize\t\t"55 55"\t\t\tLinear 0.0 0.2',
     'Animate PlayerStatusSpyOutlineImage\t\tSize\t\t"32 32"\t\t\tLinear 0.0 0.2'),
]


def main(src, dst):
    text = open(src, encoding="utf-8", errors="surrogateescape", newline="").read()
    for old, new in EDITS:
        n = text.count(old)
        if n != 1:
            raise SystemExit("expected 1 match, got %d for: %r" % (n, old))
        text = text.replace(old, new)
    open(dst, "w", encoding="utf-8", errors="surrogateescape", newline="").write(text)
    print("patched", len(EDITS), "lines ->", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])

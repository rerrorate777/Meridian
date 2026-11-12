#!/usr/bin/env python3
"""Derive meridian/scripts/hudlayout.res from the stock TF2 hudlayout.res.

Usage: patch_layout.py <stock hudlayout.res> <output>

Every edit must match exactly once; if Valve changes the stock file such that
an edit no longer applies, the script aborts instead of producing a half-patched
layout. Coordinates are in HUD units (480 tall; 768x480 at 16:10).
"""
import re
import sys

WHITE = "236 240 244 255"
TRACK = "255 255 255 40"
PANEL = "12 14 18 205"

EDITS = {
    # bottom-right: ammo dock, with item/medic/metal stacked around it
    "HudWeaponAmmo": {"xpos": "r140", "ypos": "r68", "wide": "120", "tall": "48"},
    # generic meter (Sandman/Wrap Assassin ball, Sandvich, Jarate...): directly above the ammo
    # dock; the class meters (gen_meters.py) stack to the left of the dock instead
    "HudItemEffectMeter": {"xpos": "r140", "ypos": "r120", "wide": "120", "tall": "48",
                           "MeterFG": WHITE, "MeterBG": TRACK},
    "HudMedicCharge": {"xpos": "r140", "ypos": "r120", "wide": "120", "tall": "44"},
    "HudDemomanCharge": {"xpos": "r140", "ypos": "r80", "wide": "120", "tall": "6",
                         "MeterFG": WHITE, "MeterBG": TRACK},
    "HudBowCharge": {"xpos": "r140", "ypos": "r80", "wide": "120", "tall": "6",
                     "MeterFG": WHITE, "MeterBG": TRACK},
    "HudFlameRocketCharge": {"xpos": "r140", "ypos": "r80", "wide": "120", "tall": "6",
                             "MeterFG": WHITE, "MeterBG": TRACK},
    "HudDemomanPipes": {"xpos": "r260", "ypos": "r69"},
    "CHudAccountPanel": {"xpos": "r140", "ypos": "r200", "wide": "120", "tall": "200"},
    # bottom-left: health dock, floating +health, spy disguise, chat above
    "CHealthAccountPanel": {"xpos": "20", "ypos": "r200", "wide": "148", "tall": "200"},
    "DisguiseStatus": {"xpos": "10", "ypos": "322"},
    "HudChat": {"xpos": "20", "ypos": "224", "wide": "250"},
    # nudged right so chat and the target ID never overlap at 16:10
    "CMainTargetID": {"xpos": "c-116"},
    "CSpectatorTargetID": {"xpos": "c-116"},
    "CSecondaryTargetID": {"xpos": "c-116"},
    # top-right
    "HudDeathNotice": {"xpos": "r648", "ypos": "20",
                       "BaseBackgroundColor": PANEL, "CornerRadius": "2"},
    "HudWeaponSelection": {"RightMargin": "20", "BoxColor": PANEL,
                           "SelectedBoxClor": "40 46 56 235",
                           "SelectionNumberFg": WHITE},
}


def block_span(text, name):
    m = re.search(r'\n\t"?%s"?[ \t]*\r?\n\t\{.*?\r?\n\t\}' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit("block not found: " + name)
    return m.start(), m.end()


def set_key(block, name, key, value):
    pat = re.compile(r'(\n\t\t"%s"\s*)"[^"]*"((?:[ \t]*\[\$WIN32\])?[ \t]*(?=\r?\n))' % re.escape(key))
    new, n = pat.subn(lambda m: m.group(1) + '"' + value + '"' + m.group(2), block)
    if n != 1:
        raise SystemExit("%s.%s: expected 1 match, got %d" % (name, key, n))
    return new


def main(src, dst):
    text = open(src, encoding="utf-8", errors="surrogateescape", newline="").read()
    for name, keys in EDITS.items():
        s, e = block_span(text, name)
        block = text[s:e]
        for key, value in keys.items():
            block = set_key(block, name, key, value)
        text = text[:s] + block + text[e:]
    open(dst, "w", encoding="utf-8", errors="surrogateescape", newline="").write(text)
    print("patched", len(EDITS), "elements ->", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])

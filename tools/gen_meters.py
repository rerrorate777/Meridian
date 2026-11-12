#!/usr/bin/env python3
"""Rewrite the class-specific item meters in meridian/resource/ui in the Meridian style.

The stock per-class meters (Scout drink, cleaver, Demoman/Engineer counters, ...) draw
slanted stock art, and several of them are stacked with an x_offset that makes them overlap
the flat Meridian docks. This regenerates them from one template, keeping from each file:

  * the label token (labelText of ItemEffectMeterLabel)
  * whether it has a %progresscount% label (ItemEffectMeterCount)
  * whether it stacks with other meters (stock x_offset)
  * which row it sits in (bottom row, or the row above it)
  * Heavy's kill-combo widgets

so it can be run repeatedly (it reads its own output). Usage: gen_meters.py [ui dir]
"""
import glob
import os
import re
import sys

UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meridian", "resource", "ui")

SKIP = {"huditemeffectmeter.res", "huditemeffectmeter_pyro.res"}  # hand written / #base
PANEL_W = 100
PANEL_H = 48
GAP = 6
STACK_STEP = PANEL_W + GAP  # positive x_offset moves a later meter LEFT, away from the ammo dock
X = "r248"
ROW_BOTTOM = "r68"
ROW_ABOVE = "r120"


def parse(path):
    t = open(path, encoding="utf-8", errors="surrogateescape").read()
    live = re.sub(r"//[^\n]*", "", t)
    m = re.search(r'"ItemEffectMeterLabel"\s*\{([^}]*)\}', live)  # this block only
    lm = re.search(r'"labelText"\s*"([^"]*)"', m.group(1)) if m else None
    label = lm.group(1) if lm else ""
    if "%" in label:  # a variable, not a caption (e.g. a file that was already mangled)
        label = ""
    ym = re.search(r'HudItemEffectMeter\s*\{.*?"ypos"\s*"r(\d+)"', live, re.S)
    y = int(ym.group(1)) if ym else 68
    return {
        "label": label,
        "count": '"ItemEffectMeterCount"' in live,
        "stack": re.search(r'"x_offset"\s*"-?\d+"', live) is not None,
        "row": ROW_ABOVE if y >= 100 else ROW_BOTTOM,
        "combo": '"KillComboClassIcon1"' in live,
        "name": re.search(r'"Resource/UI/([^"]+)"', t).group(1),
    }


def render(s):
    out = []
    w = out.append
    w('"Resource/UI/%s"' % s["name"])
    w("{")
    w("\tHudItemEffectMeter")
    w("\t{")
    w('\t\t"fieldName"\t\t"HudItemEffectMeter"')
    w('\t\t"visible"\t\t"1"')
    w('\t\t"enabled"\t\t"1"')
    if s["stack"]:
        w('\t\t"x_offset"\t\t"%d"' % STACK_STEP)
    w('\t\t"xpos"\t\t\t"%s"' % X)
    w('\t\t"ypos"\t\t\t"%s"' % s["row"])
    w('\t\t"wide"\t\t\t"%d"' % PANEL_W)
    w('\t\t"tall"\t\t\t"%d"' % PANEL_H)
    w('\t\t"MeterFG"\t\t"236 240 244 255"')
    w('\t\t"MeterBG"\t\t"255 255 255 40"')
    w("\t}")
    w("")
    w('\t"ItemEffectMeterBG"')
    w("\t{")
    w('\t\t"ControlName"\t"CTFImagePanel"')
    w('\t\t"fieldName"\t\t"ItemEffectMeterBG"')
    w('\t\t"xpos"\t\t\t"0"')
    w('\t\t"ypos"\t\t\t"0"')
    w('\t\t"zpos"\t\t\t"0"')
    w('\t\t"wide"\t\t\t"%d"' % PANEL_W)
    w('\t\t"tall"\t\t\t"%d"' % PANEL_H)
    w('\t\t"visible"\t\t"1"')
    w('\t\t"enabled"\t\t"1"')
    w('\t\t"scaleImage"\t"1"')
    w('\t\t"image"\t\t\t"meridian/mer_panel"')
    w("\t}")
    w("")
    w('\t"ItemEffectMeterAccent"')
    w("\t{")
    w('\t\t"ControlName"\t"CTFImagePanel"')
    w('\t\t"fieldName"\t\t"ItemEffectMeterAccent"')
    w('\t\t"xpos"\t\t\t"0"')
    w('\t\t"ypos"\t\t\t"0"')
    w('\t\t"zpos"\t\t\t"1"')
    w('\t\t"wide"\t\t\t"3"')
    w('\t\t"tall"\t\t\t"%d"' % PANEL_H)
    w('\t\t"visible"\t\t"1"')
    w('\t\t"enabled"\t\t"1"')
    w('\t\t"scaleImage"\t"1"')
    w('\t\t"image"\t\t\t"meridian/mer_blue"')
    w('\t\t"teambg_2"\t\t"meridian/mer_red"')
    w('\t\t"teambg_3"\t\t"meridian/mer_blue"')
    w("\t}")
    w("")
    label_w = 44 if s["count"] else 82
    w('\t"ItemEffectMeterLabel"')
    w("\t{")
    w('\t\t"ControlName"\t\t"CExLabel"')
    w('\t\t"fieldName"\t\t\t"ItemEffectMeterLabel"')
    w('\t\t"xpos"\t\t\t\t"12"')
    w('\t\t"ypos"\t\t\t\t"9"')
    w('\t\t"zpos"\t\t\t\t"2"')
    w('\t\t"wide"\t\t\t\t"%d"' % label_w)
    w('\t\t"tall"\t\t\t\t"14"')
    w('\t\t"autoResize"\t\t\t"0"')
    w('\t\t"pinCorner"\t\t\t"0"')
    w('\t\t"visible"\t\t\t"1"')
    w('\t\t"enabled"\t\t\t"1"')
    w('\t\t"labelText"\t\t\t"%s"' % s["label"])
    w('\t\t"textAlignment"\t\t"west"')
    w('\t\t"font"\t\t\t\t"MerLabel"')
    w('\t\t"fgcolor"\t\t\t"150 160 172 255"')
    w("\t}")
    w("")
    if s["count"]:
        w('\t"ItemEffectMeterCount"')
        w("\t{")
        w('\t\t"ControlName"\t\t"CExLabel"')
        w('\t\t"fieldName"\t\t\t"ItemEffectMeterCount"')
        w('\t\t"xpos"\t\t\t\t"56"')
        w('\t\t"ypos"\t\t\t\t"4"')
        w('\t\t"zpos"\t\t\t\t"2"')
        w('\t\t"wide"\t\t\t\t"38"')
        w('\t\t"tall"\t\t\t\t"22"')
        w('\t\t"visible"\t\t\t"1"')
        w('\t\t"enabled"\t\t\t"1"')
        w('\t\t"labelText"\t\t\t"%progresscount%"')
        w('\t\t"textAlignment"\t\t"east"')
        w('\t\t"font"\t\t\t\t"MerNumberSmall"')
        w('\t\t"fgcolor"\t\t\t"236 240 244 255"')
        w("\t}")
        w("")
    w('\t"ItemEffectMeter"')
    w("\t{")
    w('\t\t"ControlName"\t\t\t"ContinuousProgressBar"')
    w('\t\t"fieldName"\t\t\t\t"ItemEffectMeter"')
    w('\t\t"font"\t\t\t\t\t"Default"')
    w('\t\t"xpos"\t\t\t\t\t"12"')
    w('\t\t"ypos"\t\t\t\t\t"28"')
    w('\t\t"zpos"\t\t\t\t\t"2"')
    w('\t\t"wide"\t\t\t\t\t"82"')
    w('\t\t"tall"\t\t\t\t\t"8"')
    w('\t\t"autoResize"\t\t\t"0"')
    w('\t\t"pinCorner"\t\t\t\t"0"')
    w('\t\t"visible"\t\t\t\t"1"')
    w('\t\t"enabled"\t\t\t\t"1"')
    w('\t\t"textAlignment"\t\t\t"Left"')
    w('\t\t"dulltext"\t\t\t\t"0"')
    w('\t\t"brighttext"\t\t\t"0"')
    w("\t}")
    if s["combo"]:
        # Heavy kill-combo: a second label and up to three class icons drawn over the bar.
        w("")
        w('\t"ItemEffectMeterLabel2"')
        w("\t{")
        w('\t\t"ControlName"\t\t"CExLabel"')
        w('\t\t"fieldName"\t\t\t"ItemEffectMeterLabel2"')
        w('\t\t"xpos"\t\t\t\t"12"')
        w('\t\t"ypos"\t\t\t\t"9"')
        w('\t\t"zpos"\t\t\t\t"2"')
        w('\t\t"wide"\t\t\t\t"82"')
        w('\t\t"tall"\t\t\t\t"14"')
        w('\t\t"visible"\t\t\t"0"')
        w('\t\t"enabled"\t\t\t"1"')
        w('\t\t"labelText"\t\t\t"#TF_KILLCOMBO"')
        w('\t\t"textAlignment"\t\t"west"')
        w('\t\t"font"\t\t\t\t"MerLabel"')
        w('\t\t"fgcolor"\t\t\t"150 160 172 255"')
        w("\t}")
        for i, x in enumerate((12, 28, 44), 1):
            w("")
            w('\t"KillComboClassIcon%d"' % i)
            w("\t{")
            w('\t\t"ControlName"\t"ImagePanel"')
            w('\t\t"fieldName"\t\t"KillComboClassIcon%d"' % i)
            w('\t\t"xpos"\t\t\t"%d"' % x)
            w('\t\t"ypos"\t\t\t"26"')
            w('\t\t"zpos"\t\t\t"2"')
            w('\t\t"wide"\t\t\t"14"')
            w('\t\t"tall"\t\t\t"14"')
            w('\t\t"visible"\t\t"0"')
            w('\t\t"enabled"\t\t"1"')
            w('\t\t"image"\t\t\t"../HUD/leaderboard_class_scout"')
            w('\t\t"scaleImage"\t"1"')
            w("\t}")
    w("}")
    return "\n".join(out) + "\n"


def main():
    ui = sys.argv[1] if len(sys.argv) > 1 else UI
    n = 0
    for path in sorted(glob.glob(os.path.join(ui, "huditemeffectmeter_*.res"))):
        if os.path.basename(path) in SKIP:
            continue
        spec = parse(path)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(render(spec))
        n += 1
        print("%-40s label=%-18s count=%-5s stack=%-5s row=%s" % (
            os.path.basename(path), spec["label"], spec["count"], spec["stack"], spec["row"]))
    print("rewrote", n, "meters")


if __name__ == "__main__":
    main()

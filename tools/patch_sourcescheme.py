#!/usr/bin/env python3
"""Restyle the GameUI dialogs (Options, server browser, popups) via SourceScheme.res.

Usage: patch_sourcescheme.py <stock sourcescheme.res> <output sourcescheme.res>

SourceScheme.res themes the platform dialogs, which do not use ClientScheme.res. Only the colours are
changed: the tan / olive-green palette becomes the Meridian greys, and the Button / ScrollBar / List /
Menu colours are set so buttons are dark with light text (the stock buttons are tan with dark text).
Fonts stay stock: these dialogs show many user-supplied strings (key names, server names) and Barlow
only covers Latin scripts.

Every edit must match exactly once, otherwise the script aborts (see patch_layout.py).
"""
import re
import sys

TEXT = "236 240 244 255"
WHITE = "255 255 255 255"
DIM = "150 160 172 255"
BTN, BTN_ARMED, BTN_PRESSED = "28 32 40 235", "46 52 64 235", "60 68 82 235"

COLORS = {
    "TFDarkBrown": "12 14 18 255", "TFDarkBrownTransparent": "12 14 18 215",
    "TFTanBright": "236 240 244 150", "TFTanLight": "150 160 172 150", "TFTanMedium": "100 108 120 150",
    "TFTanLightBright": "229 232 238 90", "TFTanLightDark": "60 68 82 120",
    "TFOrangeBright": "60 68 82 255",
    "TFTextBright": TEXT, "TFTextLight": "200 208 218 255", "TFTextMedium": DIM, "TFTextMediumDark": "104 112 124 255",
    "TFTextBlack": "12 14 18 255", "TFTextDull": DIM,
    "TFMediumBrown": "28 32 40 255", "QuickListBGDeselected": "28 32 40 255", "QuickListBGSelected": "60 68 82 200",
    "ControlBG": "28 32 40 255", "ControlDarkBG": "22 25 32 255", "WindowBG": "18 20 26 255",
    "SelectionBG": "60 68 82 255", "SelectionBG2": "40 46 58 255", "ListBG": "16 18 24 255",
}

# BaseSettings keys: the stock values reference the TF* colours above, which are now dark, so the
# button text (dark on tan before) has to be set explicitly.
SETTINGS = {
    "Button.TextColor": TEXT, "Button.BgColor": BTN, "Button.ArmedTextColor": WHITE, "Button.ArmedBgColor": BTN_ARMED,
    "Button.DepressedTextColor": WHITE, "Button.DepressedBgColor": BTN_PRESSED,
    "ScrollBarButton.FgColor": TEXT, "ScrollBarButton.BgColor": BTN, "ScrollBarButton.ArmedFgColor": WHITE,
    "ScrollBarButton.ArmedBgColor": BTN_ARMED, "ScrollBarButton.DepressedFgColor": WHITE,
    "ScrollBarButton.DepressedBgColor": BTN_PRESSED,
    "ScrollBarSlider.FgColor": DIM, "Slider.NobColor": DIM,
    "Menu.ArmedFgColor": WHITE, "Menu.ArmedBgColor": BTN_PRESSED,
    "TextEntry.SelectedBgColor": BTN_PRESSED,
}


# Keys that SourceSchemeBase.res defines (selection colour "Orange" 255 155 0, black selected text, an
# orange tooltip) and the stock SourceScheme.res does not touch: added to BaseSettings, where they
# override the base.
EXTRA = {
    "ListPanel.SelectedTextColor": WHITE, "ListPanel.SelectedBgColor": BTN_PRESSED,
    "ListPanel.SelectedOutOfFocusBgColor": "46 52 64 255",
    "SectionedListPanel.SelectedTextColor": WHITE, "SectionedListPanel.SelectedBgColor": BTN_PRESSED,
    "SectionedListPanel.OutOfFocusSelectedTextColor": WHITE, "SectionedListPanel.OutOfFocusSelectedBgColor": "46 52 64 255",
    "RichText.SelectedTextColor": WHITE, "RichText.SelectedBgColor": BTN_PRESSED,
    "TextEntry.SelectedTextColor": WHITE, "TextEntry.OutOfFocusSelectedBgColor": "46 52 64 255",
    "Tooltip.BgColor": "12 14 18 235", "Tooltip.TextColor": TEXT,
}


def sub1(pattern, repl, text, what, flags=re.S):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        raise SystemExit("%s: expected 1 match, got %d" % (what, n))
    return new


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    t = open(sys.argv[1], encoding="utf-8", errors="surrogateescape", newline="").read()
    for name, value in COLORS.items():
        t = sub1(r'(\n\s*"%s"\s*)"[^"]*"' % re.escape(name), lambda m: m.group(1) + '"' + value + '"', t, "color " + name)
    for name, value in SETTINGS.items():
        t = sub1(r'(\n\s*%s\s+)"[^"]*"' % re.escape(name), lambda m: m.group(1) + '"' + value + '"', t, "setting " + name)
    extra = "".join('\n\t\t%s\t\t"%s"' % (k, v) for k, v in EXTRA.items())
    t = sub1(r'(BaseSettings\s*\{)', lambda m: m.group(1) + extra, t, "BaseSettings")
    with open(sys.argv[2], "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(t)
    print("patched %d colours, %d settings, %d added" % (len(COLORS), len(SETTINGS), len(EXTRA)))


if __name__ == "__main__":
    main()

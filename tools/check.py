#!/usr/bin/env python3
"""Static checks for the Meridian HUD (no game needed).

  * every .res/.txt parses as balanced Valve KeyValues
  * all file names are lowercase (the Linux client lower-cases lookups)
  * every font used by a .res exists in clientscheme.res or the stock scheme
  * every Meridian material / font file referenced actually ships
  * VTF headers are well formed
Exit status is non-zero on any problem.
"""
import os
import re
import struct
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meridian")
problems = []


def err(msg):
    problems.append(msg)


def tokens(text):
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
        elif text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
        elif c == '"':
            j = text.find('"', i + 1)
            if j < 0:
                raise ValueError("unterminated string")
            yield ("s", text[i + 1:j])
            i = j + 1
        elif c in "{}":
            yield (c, c)
            i += 1
        elif c == "[":
            j = text.find("]", i)
            if j < 0:
                raise ValueError("unterminated condition")
            i = j + 1
        else:
            j = i
            while j < n and text[j] not in ' \t\r\n{}"[':
                j += 1
            yield ("s", text[i:j])
            i = j


def check_kv(path, text):
    depth = 0
    try:
        for kind, _ in tokens(text):
            if kind == "{":
                depth += 1
            elif kind == "}":
                depth -= 1
                if depth < 0:
                    return err("%s: unmatched }" % path)
    except ValueError as e:
        return err("%s: %s" % (path, e))
    if depth:
        err("%s: %d unclosed {" % (path, depth))


def main():
    files = []
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            files.append(os.path.join(d, f))
    for p in files:
        rel = os.path.relpath(p, ROOT)
        if rel != rel.lower():
            err("not lowercase: " + rel)

    scheme = open(os.path.join(ROOT, "resource", "clientscheme.res"), encoding="utf-8", errors="replace").read()
    fonts_section = scheme[scheme.index("Fonts"):scheme.index("CustomFontFiles")]
    defined = set(re.findall(r'^\t\t"([^"]+)"\s*$', fonts_section, re.M))
    mer_fonts = {f for f in defined if f.startswith("Mer")}
    if not mer_fonts:
        err("no Mer* fonts in clientscheme.res")

    for p in files:
        if p.endswith((".res", ".txt")):
            text = open(p, encoding="utf-8", errors="replace").read()
            check_kv(os.path.relpath(p, ROOT), text)
            for m in re.finditer(r'"font"\s*"(Mer[^"]+)"', text):
                if m.group(1) not in defined:
                    err("%s: undefined font %s" % (os.path.relpath(p, ROOT), m.group(1)))
            for m in re.finditer(r'"(?:image|image_lodef|teambg_\d(?:_lodef)?)"\s*"\.\./hud/(mer_[^"]+)"', text):
                if not os.path.exists(os.path.join(ROOT, "materials", "hud", m.group(1) + ".vmt")):
                    err("%s: missing material %s" % (os.path.relpath(p, ROOT), m.group(1)))
        elif p.endswith(".vtf"):
            d = open(p, "rb").read()
            sig, major, minor, hsize, w, h = struct.unpack_from("<4sIIIHH", d, 0)
            if sig != b"VTF\0" or hsize < 80 or len(d) != hsize + w * h * 4:
                err("bad VTF: " + os.path.relpath(p, ROOT))

    for m in re.finditer(r'"resource/fonts/([^"]+)"', scheme):
        if not os.path.exists(os.path.join(ROOT, "resource", "fonts", m.group(1))):
            err("clientscheme references missing font file " + m.group(1))

    for name in ("hudlayout.res", "hudanimations_tf.txt"):
        if not os.path.exists(os.path.join(ROOT, "scripts", name)):
            err("missing scripts/" + name)
    if not os.path.exists(os.path.join(ROOT, "info.vdf")):
        err("missing info.vdf")

    print("checked %d files, %d problem(s)" % (len(files), len(problems)))
    for pr in problems:
        print(" -", pr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

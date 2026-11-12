#!/usr/bin/env python3
"""Extract files from a Source VPK (v1/v2 *_dir.vpk) without third-party packages.

Usage: vpk_extract.py <tf2_misc_dir.vpk> <out dir> <pattern> [<pattern> ...]

Patterns are fnmatch globs against the in-VPK path, e.g. 'scripts/mod_textures.txt' or
'resource/ui/hud_obj_*.res'. Files keep their in-VPK directory structure under <out dir>.
"""
import fnmatch
import os
import struct
import sys


def read_cstr(f):
    out = bytearray()
    while True:
        c = f.read(1)
        if not c or c == b"\0":
            return out.decode("utf-8", "surrogateescape")
        out += c


def entries(path):
    with open(path, "rb") as f:
        sig, ver = struct.unpack("<II", f.read(8))
        if sig != 0x55AA1234 or ver not in (1, 2):
            raise SystemExit("not a VPK v1/v2 file: " + path)
        tree_size = struct.unpack("<I", f.read(4))[0]
        header = 12 if ver == 1 else 28
        if ver == 2:
            f.read(16)
        data_start = header + tree_size
        while True:
            ext = read_cstr(f)
            if not ext:
                break
            while True:
                d = read_cstr(f)
                if not d:
                    break
                while True:
                    name = read_cstr(f)
                    if not name:
                        break
                    _crc, preload, idx, off, length, term = struct.unpack("<IHHIIH", f.read(18))
                    assert term == 0xFFFF
                    pre = f.read(preload)
                    full = ("" if d == " " else d + "/") + ("" if name == " " else name)
                    full += "" if ext == " " else "." + ext
                    yield full, pre, idx, off, length, data_start


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    vpk, out = sys.argv[1], sys.argv[2]
    pats = sys.argv[3:]
    base = vpk[: -len("_dir.vpk")] if vpk.endswith("_dir.vpk") else vpk
    n = 0
    for full, pre, idx, off, length, data_start in entries(vpk):
        if not any(fnmatch.fnmatch(full, p) for p in pats):
            continue
        if idx == 0x7FFF:
            with open(vpk, "rb") as f:
                f.seek(data_start + off)
                body = f.read(length)
        else:
            with open("%s_%03d.vpk" % (base, idx), "rb") as f:
                f.seek(off)
                body = f.read(length)
        dst = os.path.join(out, full)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(pre + body)
        n += 1
        print(full)
    if n == 0:
        raise SystemExit("no files matched")


if __name__ == "__main__":
    main()

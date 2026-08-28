#!/usr/bin/env python3
"""Printable-string extractor with file offsets.

`strings(1)` is not available everywhere and this pipeline needs the byte
offset of every hit, so the tool is carried in the repository.

Usage:  python3 tools/strings.py FILE [-n MIN] [-e latin1|amiga] [--grep RE]
"""
import sys, re, argparse

PRINT = set(range(0x20, 0x7f))


def scan(data, minlen):
    out = []
    start = None
    for i, b in enumerate(data):
        if b in PRINT or b == 9:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= minlen:
                out.append((start, data[start:i].decode('latin-1')))
            start = None
    if start is not None and len(data) - start >= minlen:
        out.append((start, data[start:].decode('latin-1')))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-n", type=int, default=4)
    ap.add_argument("--grep", default=None)
    ap.add_argument("--quiet-name", action="store_true")
    a = ap.parse_args()
    rx = re.compile(a.grep, re.I) if a.grep else None
    for path in a.files:
        data = open(path, 'rb').read()
        for off, s in scan(data, a.n):
            if rx and not rx.search(s):
                continue
            if a.quiet_name:
                print("%08x  %s" % (off, s))
            else:
                print("%-24s %08x  %s" % (path.split('/')[-1], off, s))


main()

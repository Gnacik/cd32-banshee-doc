#!/usr/bin/env python3
"""Extract the four-language string table out of `bans.exe`.

The table is a flat run of strings in the data area of hunk 0.  Two control
bytes carry the structure:

    0xFF   separates the language variants of one string
    0xFE   ends a group and starts the next

and the variants are always in the order **English, German, French, Danish**.
German and French accented letters are **code page 437** bytes; the three
Danish letters are *not* -- although CP437 has them -- and are written with
ASCII punctuation instead:

    0x22 "  ->  AE      0x2B +  ->  ae
    0x3D =  ->  aa      0x7E ~  ->  oe

which is why a naive CP437 decode of this disc produces readable German and
French and nonsense Danish.

    python3 tools/text.py <bans.exe> [start] [end] [--raw]
"""
import sys

DANISH = {0x22: 'Æ', 0x2B: 'æ', 0x3D: 'å', 0x7E: 'ø'}
LANGS = ['en', 'de', 'fr', 'da']


def decode(b, danish):
    out = []
    for c in b:
        if danish and c in DANISH:
            out.append(DANISH[c])
        else:
            out.append(bytes([c]).decode('cp437'))
    return ''.join(out)


def main():
    path = sys.argv[1]
    start = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x1c840
    end = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x1e600
    d = open(path, 'rb').read()[start:end]
    groups = d.split(b'\xfe')
    n = 0
    counts = {c: d.count(bytes([c])) for c in (0xfc, 0xfd, 0xfe, 0xff)}
    print("control bytes in 0x%x..0x%x: " % (start, end) +
          "  ".join("0x%02X x%d" % (k, v) for k, v in sorted(counts.items())))
    print()
    for g in groups:
        if not g.strip(b'\x00'):
            continue
        parts = g.split(b'\xff')
        n += 1
        print("--- group %d  (%d variants) ---" % (n, len(parts)))
        for i, p in enumerate(parts):
            lang = LANGS[i] if i < 4 else '??'
            print("  %-3s %s" % (lang, decode(p, lang == 'da')))


main()

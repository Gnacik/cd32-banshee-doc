#!/usr/bin/env python3
"""Write `notes/file-inventory.md` -- every directory record on the disc with
its LBA, size on disc, unpacked size, bytes actually used, timestamp and
SHA-1.

    python3 tools/inventory.py <track1.iso> > notes/file-inventory.md
"""
import sys, os, hashlib, importlib.util

_here = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(_here, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


rnc = load("rnc")
SEC = 2048


def u32le(b, o):
    return int.from_bytes(b[o:o + 4], 'little')


def dirdate(b, o):
    if b[o] == 0 and b[o + 1] == 0:
        return "-"
    return "%04d-%02d-%02d %02d:%02d:%02d" % (1900 + b[o], b[o + 1], b[o + 2],
                                              b[o + 3], b[o + 4], b[o + 5])


def walk(f, lba, ln, path, out):
    f.seek(lba * SEC)
    data = f.read(ln)
    o = 0
    while o < len(data):
        rl = data[o]
        if rl == 0:
            o = (o // SEC + 1) * SEC
            continue
        rec = data[o:o + rl]
        nlen = rec[32]
        raw = rec[33:33 + nlen]
        if not (nlen == 1 and rec[33] in (0, 1)):
            nm = raw.split(b';')[0].decode('latin-1')
            ext, sz, dt, fl = u32le(rec, 2), u32le(rec, 10), dirdate(rec, 18), rec[25]
            if fl & 2:
                out.append((path + "/" + nm, ext, sz, dt, True))
                walk(f, ext, sz, path + "/" + nm, out)
            else:
                out.append((path + "/" + nm, ext, sz, dt, False))
        o += rl


def main():
    iso = sys.argv[1]
    f = open(iso, 'rb')
    f.seek(16 * SEC)
    pvd = f.read(SEC)
    root_lba, root_len = u32le(pvd, 158), u32le(pvd, 166)
    out = [("/", root_lba, root_len, dirdate(pvd, 174), True)]
    walk(f, root_lba, root_len, "", out)
    print("# File inventory")
    print()
    print("Every directory record in the volume, in LBA order.  `on disc` is the")
    print("size in the directory record; `unpacked` and `used` are present only")
    print("for the RNC ProPack streams and come from `tools/census.py` -- `used`")
    print("is the offset of the last non-zero byte of the unpacked buffer.")
    print()
    print("Reproduce with `python3 tools/inventory.py <track1.iso>`.")
    print()
    print("| LBA | on disc | unpacked | used | use % | timestamp | path | SHA-1 |")
    print("|---:|---:|---:|---:|---:|---|---|---|")
    tot_disc = tot_unp = tot_used = 0
    for path, lba, sz, dt, isdir in sorted(out, key=lambda x: (x[1], x[0])):
        if isdir:
            print("| %d | %d | | | | %s | `%s/` (directory) | |" % (lba, sz, dt, path))
            continue
        f.seek(lba * SEC)
        blob = f.read(sz)
        sha = hashlib.sha1(blob).hexdigest() if sz else "-"
        unp = used = pct = ""
        tot_disc += sz
        if blob[:3] == b'RNC' and blob[3] == 1:
            o = rnc.unpack(blob)
            i = len(o)
            while i > 0 and o[i - 1] == 0:
                i -= 1
            unp, used, pct = len(o), i, "%.1f" % (100.0 * i / len(o))
            tot_unp += len(o)
            tot_used += i
        print("| %d | %d | %s | %s | %s | %s | `%s` | `%s` |" %
              (lba, sz, unp, used, pct, dt, path, sha))
    print()
    print("Totals: **%d bytes on disc**, **%d bytes unpacked** (RNC files only), "
          "**%d bytes used** (%.1f %% of unpacked)."
          % (tot_disc, tot_unp, tot_used, 100.0 * tot_used / tot_unp))


main()

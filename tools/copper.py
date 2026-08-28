#!/usr/bin/env python3
"""Disassemble an Amiga copper list.

Prints MOVE / WAIT / SKIP with the custom-chip register names, so a display
can be read out of a data hunk without guessing.

    python3 tools/copper.py <file> [start] [length]
"""
import sys

REG = {
    0x02: 'DMACONR', 0x04: 'VPOSR', 0x06: 'VHPOSR', 0x08: 'DSKDATR',
    0x00A: 'JOY0DAT', 0x00C: 'JOY1DAT', 0x01C: 'INTENAR', 0x01E: 'INTREQR',
    0x020: 'DSKPTH', 0x022: 'DSKPTL', 0x024: 'DSKLEN',
    0x02A: 'VPOSW', 0x02C: 'VHPOSW',
    0x040: 'BLTCON0', 0x042: 'BLTCON1', 0x044: 'BLTAFWM', 0x046: 'BLTALWM',
    0x048: 'BLTCPTH', 0x04A: 'BLTCPTL', 0x04C: 'BLTBPTH', 0x04E: 'BLTBPTL',
    0x050: 'BLTAPTH', 0x052: 'BLTAPTL', 0x054: 'BLTDPTH', 0x056: 'BLTDPTL',
    0x058: 'BLTSIZE', 0x05A: 'BLTCON0L', 0x05C: 'BLTSIZV', 0x05E: 'BLTSIZH',
    0x060: 'BLTCMOD', 0x062: 'BLTBMOD', 0x064: 'BLTAMOD', 0x066: 'BLTDMOD',
    0x070: 'BLTCDAT', 0x072: 'BLTBDAT', 0x074: 'BLTADAT',
    0x07C: 'DENISEID', 0x07E: 'DSKSYNC',
    0x080: 'COP1LCH', 0x082: 'COP1LCL', 0x084: 'COP2LCH', 0x086: 'COP2LCL',
    0x088: 'COPJMP1', 0x08A: 'COPJMP2', 0x08E: 'DIWSTRT', 0x090: 'DIWSTOP',
    0x092: 'DDFSTRT', 0x094: 'DDFSTOP', 0x096: 'DMACON', 0x098: 'CLXCON',
    0x09A: 'INTENA', 0x09C: 'INTREQ', 0x09E: 'ADKCON',
    0x0A0: 'AUD0LCH', 0x0A2: 'AUD0LCL', 0x0A4: 'AUD0LEN', 0x0A6: 'AUD0PER',
    0x0A8: 'AUD0VOL', 0x0AA: 'AUD0DAT',
    0x100: 'BPLCON0', 0x102: 'BPLCON1', 0x104: 'BPLCON2', 0x106: 'BPLCON3',
    0x108: 'BPL1MOD', 0x10A: 'BPL2MOD', 0x10C: 'BPLCON4',
    0x110: 'BPL1DAT', 0x112: 'BPL2DAT',
    0x1FC: 'FMODE', 0x1DC: 'BEAMCON0', 0x1E4: 'DIWHIGH',
}
for i in range(8):
    REG[0x0E0 + 4 * i] = 'BPL%dPTH' % (i + 1)
    REG[0x0E2 + 4 * i] = 'BPL%dPTL' % (i + 1)
    REG[0x120 + 4 * i] = 'SPR%dPTH' % i
    REG[0x122 + 4 * i] = 'SPR%dPTL' % i
for i in range(32):
    REG[0x180 + 2 * i] = 'COLOR%02d' % i


def name(r):
    return REG.get(r, '$%03X' % r)


def main():
    d = open(sys.argv[1], 'rb').read()
    start = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
    length = int(sys.argv[3], 0) if len(sys.argv) > 3 else len(d) - start
    o = start
    end = start + length
    while o + 4 <= end:
        w1 = int.from_bytes(d[o:o + 2], 'big')
        w2 = int.from_bytes(d[o + 2:o + 4], 'big')
        if w1 & 1:
            vp, hp = w1 >> 8, w1 & 0xfe
            if w2 & 1:
                print("%06x  %04x %04x  SKIP  v=%d h=%d  mask=%04x" % (o, w1, w2, vp, hp, w2))
            else:
                print("%06x  %04x %04x  WAIT  v=%d h=%d  mask=%04x" % (o, w1, w2, vp, hp, w2))
            if w1 == 0xffff and w2 == 0xfffe:
                print("%06x  -- end of copper list --" % o)
                break
        else:
            print("%06x  %04x %04x  MOVE  %-9s $%04x" % (o, w1, w2, name(w1 & 0x1fe), w2))
        o += 4


main()

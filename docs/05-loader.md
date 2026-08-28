# `bans.exe` — the game

149,524 bytes. An AmigaDOS hunk executable, six hunks, **1,948 relocations**,
and — unlike the other Core Design disc in this series — a program that keeps
AmigaDOS alive underneath it and loads its files with `dos.library`.

## Hunks

```
hunk  kind  memory   length      file offset of body
  0   CODE  any        97,500    0x000034
  1   DATA  any        26,932    0x019894
  2   BSS   any       342,356    -- (bss)
  3   CODE  chip          288    0x020490
  4   DATA  chip       16,752    0x020678
  5   BSS   chip    1,285,052    -- (bss)
```

Chip RAM claimed before the program allocates anything: 288 + 16,752 +
1,285,052 = **1,302,092 bytes**, or 62 % of a CD32's 2 MB. Hunk 5 alone is
1.28 MB and is where the screen buffers and the decrunched level data live;
hunk 3 is 288 bytes of code that has to be in chip RAM, which on an Amiga
means it is copied into the copper's or the blitter's way and is almost
certainly the interrupt handler; hunk 4 is the copper-list templates
([07-graphics.md](07-graphics.md)).

## Relocations, and the address convention

```
1,948 relocations
  hunk 0 -> hunk 0 : 1108      hunk 1 -> hunk 1 : 161
  hunk 0 -> hunk 1 :  240      hunk 1 -> hunk 4 :   1
  hunk 0 -> hunk 2 :    6      hunk 1 -> hunk 5 :   2
  hunk 0 -> hunk 3 :    3      hunk 3 -> hunk 0 :  19
  hunk 0 -> hunk 4 :  299      hunk 3 -> hunk 3 :   2
  hunk 0 -> hunk 5 :   88      hunk 3 -> hunk 4 :  13
                               hunk 3 -> hunk 5 :   3
                               hunk 4 -> hunk 5 :   3
```

Every absolute longword in this file that names an address is in that list,
and every absolute longword that is **not** in that list is a literal. This
distinction is the whole reason the convention is stated in
[00-overview.md](00-overview.md): `lea $27c.l,a0` in a hunk file is not a
reference to address 0x27C, it is `hunk_base + 0x27C` where the hunk is
whichever one the relocation names — and the same encoding with no relocation
covering it is a constant that happens to look like an address.

`tools/relocs.py <file> --at <file offset>` answers the question directly and
says "NOT covered by a relocation (the constant is literal)" when it is one.

The three relocations from hunk 4 into hunk 5 are the interesting ones: they
are the bitplane pointers inside the copper templates, patched by `LoadSeg`
before the program has run a single instruction.

## How it reaches its files

Both scans, because either one alone gives the wrong answer:

```
lea $dff000,aN          15  (all into a6 except one into a1)
movea.l #$dff000,aN      0
absolute $00DFF0xx     257 references in 29 registers
jsr d16(a6)             71 call sites, 33 distinct LVOs
lea/movea $B80000,aN     0
$00B80038 / $00B8003C    0
$C0DE0000                0
```

So this is the platform checklist's **fifth position**: AmigaDOS stays alive,
the files come through `dos.library`, and the hardware is driven directly by a
mixture of absolute writes and `d16(a6)` after a `lea`. Running only the
absolute scan finds 29 registers and misses the entire Blitter; running only
the based scan finds 21 and misses `COP1LCH`, `DMACON` and all four Paula
channels. Run both.

Five libraries and two devices are named, in this order in the data:

```
0x00075c  lowlevel.library
0x000b26  freeanim.library
0x000b37  graphics.library
0x000b48  dos.library
0x000b54  intuition.library
0x000b66  input.device
0x000b73  cd.device
0x005efc  audio.device       -- The Player 6.0A's own (09-audio.md)
0x005f09  ciax.resource      -- The Player 6.0A's own
```

Five `OpenLibrary` (LVO −552, not `OldOpenLibrary`) and five `CloseLibrary`
call sites; three `OpenDevice` (−444) and two `CloseDevice` (−450). The
lowest-numbered LVOs in the histogram are `dos.library`'s file calls — `Open`
(−30) four times, `Close` (−36), `Read` (−42), `Write` (−48), `Seek` (−66) —
which is how the 37 data files get in.

**`freeanim.library` is opened and the disc does not carry it.** It is one of
the five modules Commodore added to the CD32 ROM, so on the console the open
succeeds; on an A1200 it would fail, and with no `libs/` on the disc there is
no fallback. Note that Dragonstone ships `c/FreeAnim` — the installer for that
same library — and Banshee does not, which is the difference between a disc
that expects to run on a 1200 and one that does not.

Four `SetFunction` (−420) call sites: the program patches library vectors,
which on an Amiga game usually means intercepting `graphics.library`'s or
`intuition.library`'s idea of who owns the display.

## The file table

37 records in the data area of hunk 0, at hunk0+0x27DA … hunk0+0x2B96 (file
0x280E … 0x2BCA). Dump it with `python3 tools/loadertable.py _work/ext/bans.exe`;
full output in [notes/loader-file-table.txt](../notes/loader-file-table.txt).

Each record is variable length:

```
+0  buffer size, 4 bytes big-endian
+4  floppy disk number, 1 byte
+5  flag byte, 0x01 on all 37
+6  the path, NUL-terminated, padded to an even offset
```

```
#    offset   size       disk flag  path
1    0x00280e 81920      2    0x01  banshee2:core
2    0x002822 147912     2    0x01  banshee2:plyrmisc
3    0x00283a 153946     2    0x01  banshee2:soundfx
4    0x002852 487944     2    0x01  banshee2:level1c
...
36   0x002b92 8000       1    0x01  banshee1:introseq.006
37   0x002bae 11500      1    0x01  banshee1:introseq.007
```

The **disk byte** is the digit in the volume name, and the two agree on all 37
records, which is what makes the table a genuine four-floppy layout rather
than a decoration ([03-boot-chain.md](03-boot-chain.md)).

The **size field** is a buffer size and it is hand-maintained, which the
intro-sequence entries prove on their own:

| File | Packed on disc | Table says |
|---|---:|---:|
| `introseq.001` | 4,342 | 4,400 |
| `introseq.002` | 8,254 | 8,300 |
| `introseq.003` | 5,314 | 5,400 |
| `introseq.004` | 6,908 | 7,000 |
| `introseq.005` | 3,954 | 4,000 |
| `introseq.006` | 7,927 | 8,000 |
| `introseq.007` | 11,429 | 11,500 |

Every one is the packed size **rounded up to the next hundred bytes** — by
hand, in decimal, by somebody who looked at a directory listing and typed a
number. The ten ending frames all get 10,960, one buffer big enough for the
largest of them; `soundfx4` gets 153,946, which is `soundfx`'s size and 25,362
bytes more than it needs, because the two share a buffer. Eleven of the
thirty-seven entries are the unpacked size instead, exactly for the files that
are decrunched into a buffer of their own.

## The thirty-eighth name

Immediately after the last record, with **no record header at all** — no size,
no disk byte, no flag — sits one more NUL-terminated string:

```
0x002bca  62 61 6e 73 31 3a 66 6c 65 76 00     'bans1:flev'
```

`bans1:` is not one of the four volume names the boot script assigns, and
`flev` is not a file on the disc. See [11-leftovers.md](11-leftovers.md).

## The 68000 disassembly caveat

Capstone's M68K backend prints wrong-but-plausible branch displacements,
immediates and absolute addresses on this code. `tools/dis68k.py` keeps
Capstone's decode, prints the raw bytes beside every instruction, and
recomputes the one thing that matters most — where each `Bcc`/`BRA`/`BSR`/
`DBcc` actually goes — straight from the encoding. **Every constant quoted in
this repository was re-read from the byte column**, and where a listing is
reproduced here the bytes are reproduced with it so a reader can check.

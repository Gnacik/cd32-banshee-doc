# Compression

Reproduce with `python3 tools/census.py _work/ext`; raw output in
[notes/compression-census.txt](../notes/compression-census.txt).

## The census over files

| Container | Files | Bytes on disc |
|---|---:|---:|
| RNC ProPack **method 1** | 37 | 2,434,293 |
| AmigaDOS hunk executable | 5 | 445,140 |
| plain text | 1 | 230 |
| **zero bytes** | 2 | 0 |
| **45** | | **2,879,663** |

Every packed file decodes and every CRC-16/ARC in every header checks.

**And the decoder that did it is Dragonstone's.** `tools/rnc.py` in this
repository is
[cd32-dragonstone-doc](https://github.com/vs-sr-dev/cd32-dragonstone-doc)'s
file, copied without a line changed, and it unpacked all 37 streams on the
first run. Same cruncher, same method, same version, same header layout, two
discs, two development teams — see
[10-core-design-control.md](10-core-design-control.md).

Header fields, as they appear here:

| Field | Range on this disc |
|---|---|
| method | 1, on all 37 |
| leeway | 0 on 34 files, 1 on `bossf`, 2 on `introscreen` and `soundfx` |
| chunks | 3 to 41, tracking the unpacked size at roughly one chunk per 12 KB |

## The rule about floppy origins holds, and this is the seventh test

The platform checklist's rule is that compression on this format tracks a
title's **floppy origin**, not the disc. Banshee packs 37 of 45 files, so the
rule predicts a floppy release — and the disc supplies the evidence for one
without leaving the boot script: four `assign bansheeN: CD0:` lines and a
loader table that says which of four disks each file was on, level 3 split
across two of them ([03-boot-chain.md](03-boot-chain.md)). That is **[7 of 7]**
on the positive side.

## And the census over files is wrong about one file

`picture.exe` shows in the table above as "AmigaDOS hunk executable, not
compressed". It is 274,764 bytes and **three of its four hunks are RNC
ProPack method 2 streams**, 329,184 bytes of them, decrunched at load time by
a 484-byte stub in hunk 0. A magic scan over files finds nothing because the
magic is 44 bytes into the file, behind a hunk header.

The cheap thing that catches it is the **entropy column**, which the file
census prints anyway:

```
bans.exe      149,524 B   entropy 6.172     <- a normal 68k executable
picture.exe   274,764 B   entropy 7.840     <- not a normal 68k executable
C/SetPatch     13,200 B   entropy 6.175
```

A hunk file at 7.84 is packed, whatever its magic says. This is the second
disc in this series where the file-level census is right and misses the
compression *inside* an executable — Guardian hides nine ByteRun1 images
behind a 12-byte header — and the two cases share nothing except the lesson:
**look inside the executables anyway.**

Method 2 appears **nowhere else on the disc**. Every file is method 1; the
only method 2 stream is inside the one program that is packed. That is two
different tools in one build chain, and [08-picture-exe.md](08-picture-exe.md)
disassembles the decoder for the second one.

`tools/rnc2.py` implements method 2 from that stub's own 484 bytes rather than
from an outside description, and all three hunks check against their CRCs.

## Fixed-size buffers, and how much of them is used

The unpacked sizes are not the sizes of the data. They are the sizes of the
buffers the data was assembled in, and the same round numbers repeat:

| Unpacked size | Files | What it is |
|---:|---:|---|
| 40,960 | 17 | every cut-scene frame — a 320×256 four-bitplane screen |
| 164,864 | 3 | every full picture — 1,024 bytes of palette + 640×256 at 8 planes |
| 81,920 | 1 | `core` |

and the used fraction — the offset of the last non-zero byte — ranges from
**60.6 %** (`core`, 49,657 of 81,920) to **100 %**:

```
core            81,920 ->  49,657   60.6 %
banspic2       164,864 -> 119,760   72.6 %
introseq.004    40,960 ->  31,466   76.8 %
endseq1/2.*     40,960 ->  31,950   78.0 %   (all ten of them, to the byte)
banspic1       164,864 -> 148,002   89.8 %
introscreen    164,864 -> 164,864  100.0 %
level1c        487,644 -> 487,644  100.0 %
```

The ten ending frames all stop at exactly 31,950 of 40,960, which is 320×200
at four bitplanes (32,000 bytes) less the last 50 bytes of the final plane
row: the frames are 320×200 pictures in 320×256 buffers, and the sequence was
exported by one tool in one pass. `banspic2` at 72.6 % is the same 640×256
buffer as `introscreen` with a smaller picture in it.

This is the same habit Dragonstone has, on the same publisher's other disc,
and the numbers are directly comparable — see below.

## Three ways to measure a disc, and which one the size band means

The platform checklist carries a band of "2.7 – 13.3 MB of game" that several
discs fall into, and it has an inconsistency in it: Dragonstone's 2.7 MB is
the figure **on disc**, while Gloom's and HeroQuest II's are the figures
**after unpacking**. Two Core Design discs with the same fixed-buffer habit
can settle what the band is actually measuring, so here are all three figures
for both, computed by the same tool over the same kind of tree:

| | Files | On disc | Resident after unpacking | Actually used |
|---|---:|---:|---:|---:|
| **Banshee** | 45 (37 packed) | **2,879,663** (2.88 MB) | **5,768,936** (5.77 MB) | **5,542,774** (96.1 %) |
| **Dragonstone** | 89 (84 packed) | **2,709,626** (2.71 MB) | **10,354,949** (10.35 MB) | **9,410,064** (90.9 %) |

("Resident" counts the unpacked size of every packed file plus the size of
every unpacked one, which is what has to exist in memory if everything is
loaded at once. "Used" is the last non-zero byte of each.)

Read as **on disc**, the two discs are 6 % apart and both sit at the bottom of
the band. Read as **unpacked**, they are 80 % apart and one is near the middle
of the band while the other is below it.

So the band is only coherent if it is read as *on disc*, and every entry in it
should be restated that way. The unpacked figure is a different measurement
and a more interesting one — it is the size of the game rather than the size
of the file set — but it is not the number the band was built from, and mixing
the two makes two discs from one publisher look like different classes of
title when the thing that differs is which column somebody quoted.

The third figure, **used**, is worth keeping for a separate reason: the gap
between resident and used is the buffer slack, and it is 226 KB on Banshee
(3.9 %) against 945 KB on Dragonstone (9.1 %). Both studios rounded their
buffers up; the one with four levels rounded less.

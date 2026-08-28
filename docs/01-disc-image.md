# The disc image

Reproduce everything here with `python3 tools/isodump.py <track1.iso>`; the
raw output is in [notes/pvd-and-sector-map.txt](../notes/pvd-and-sector-map.txt).

## Cue sheet

```
CATALOG 5020717200444
FILE "Banshee (1994)(Core)(M4)(Track 1 of 3)[!].iso" BINARY
  TRACK 01 MODE1/2048
    INDEX 01 00:00:00
FILE "Banshee (1994)(Core)(M4)(Track 2 of 3)[!].wav" WAVE
  TRACK 02 AUDIO
    PREGAP 00:02:00
    INDEX 01 00:00:00
FILE "Banshee (1994)(Core)(M4)(Track 3 of 3)[!].wav" WAVE
  TRACK 03 AUDIO
    INDEX 01 00:00:00
```

Three tracks: one `MODE1/2048` data track and two Red Book audio tracks.

`CATALOG 5020717200444` is a real UK EAN-13 with a valid check digit, unlike
the thirteen zeros four other discs in this series carry. The `502071` prefix
is Core Design's own — it is the barcode of the retail box, and on a disc
whose label is not in front of you it is the only field that identifies the
release commercially.

## The tracks

| Track | Type | Length | Sectors | Bytes |
|---:|---|---|---:|---:|
| 1 | `MODE1/2048` | — | 1,773 in the image, 1,687 declared | 3,631,104 |
| 2 | audio, 44.1 kHz 16-bit stereo | 2:05.33 | 9,400 | 22,108,844 |
| 3 | audio, 44.1 kHz 16-bit stereo | 3:00.37 | 13,528 | 31,817,900 |

**Five minutes six seconds of Red Book on a disc that can hold seventy-four.**
The game plays them out of the drive while it runs — see
[09-audio.md](09-audio.md), which also explains why there is a watchdog around
that.

## Sector map

The volume declares 1,687 sectors and the image is 1,773, so the map is built
against the declared size. Nothing in the volume is unclaimed except one run
at the end.

| LBA | Sectors | Contents |
|---:|---:|---|
| 0–15 | 16 | system area, all zero |
| 16 | 1 | primary volume descriptor |
| 17 | 1 | **the same descriptor again**, byte for byte |
| 18 | 1 | descriptor set terminator |
| 19 | 1 | M path table |
| 20 | 1 | L path table |
| 21 | 1 | the CDTV trademark block ([02](02-filesystem.md)) |
| 22 | 1 | root directory |
| 23 | 1 | `/s` directory |
| 24 | 1 | `/s/startup-sequence` |
| 25 | 1 | `/C` directory |
| 26–1453 | 1,428 | `/C` commands and the 41 game files |
| 1454 | 1 | `/icons` directory — **and it is empty** |
| 1455–1686 | **232** | unclaimed, all zero |
| 1687–1772 | 86 | beyond the declared volume, all zero |

**There is no gap in front of the files.** The volume starts at 19, the
trademark block is at 21, the root directory at 22, and the first file at 24
with no space wasted. Three discs in this series leave a large zero run ahead
of their files and one candidate explanation was that it optimises the seek
for Red-Book-during-play; Guardian was the first negative for that and
**Banshee is the second**: it plays Red Book while the game runs, with the one
head the console has, and it has no front gap at all.

### The 232-sector run, and who else has one

Eight discs in this series leave **32** zero sectors at the end of the volume,
across volumes from 772 to 255,552 sectors. One leaves **232**: Liberation.

Banshee leaves **232**, at LBA 1455–1686, in a 1,687-sector volume.

That is now two discs at 232 and eight at 32 — and the two discs at 232 have
the same value in the one PVD field that names a person:

```
Liberation  (Byte Engineers / Mindscape, April 1994)   D J Pocock - ISOCD 1.04 ...
Banshee     (Core Design, July 1994)                   D J Pocock - ISOCD 1.04 ...
```

Two unrelated studios, two unrelated publishers, three months apart, the same
tool version, the same anomalous trailing run, and the same named operator.
Liberation's volume is 82,502 sectors and Banshee's is 1,687 — a factor of
49 — so the number is not a function of volume size, which was the last
surviving explanation for it. Whatever produces 232 rather than 32 travels
with the person running the tool, not with the disc.

This does not say *what* produces it. It says where to look next: an ISOCD
option, a pad setting, or a habit of the operator's own workflow. It is the
first time any layout anomaly in this series has correlated with a named
individual, and it cost one field comparison.

### The overrun

The image is 86 sectors longer than the declared volume, all zero. Nine of
the ten ISOCD discs here overrun by something; three of them by exactly 152
sectors. 86 is a new value and joins 103, 106, 150, 180, 225 and 227 in a list
with no pattern in it. **Build the sector map against the declared size** or
this run merges with the 232 and reports as 318.

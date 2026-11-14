# Level formats, palettes, and the floppy release

Findings added after the original pipeline: the level file formats read from
the code that consumes them, the palettes the picture files do not carry, and
a comparison against the A1200 floppy release that settles three of the open
questions. Addresses are Ghidra addresses with hunk 0 loaded at `0x21f000`
(file offset = address − `0x21f000` + `0x34`).

## Palettes that are not in the files

| Data | Palette | Format |
|---|---|---|
| `introseq.*`, `endseq*.*` (320×256, 4 planes, interleaved) | `bans.exe` @ `0x2229dc`, 16 entries | one word per channel, R,G,B, 8 bits in the low byte |
| `core` (640×256, 4 planes, interleaved) | `bans.exe` @ `0x22297c`, 16 entries | same |
| level graphics | `levelNf` + field `+0x16`, **128** entries | same |

The intro player fades from the 16-entry table at `0x222ac6` (every entry
`0,4,0x19`, a dark blue) to the sepia table at `0x2229dc` (`FUN_0022318e`).

## `levelNc` (chip RAM)

Five longwords, offsets from the start of the file. The level initialiser
(`0x22e676`) converts them to pointers and stores them in the `levelNf`
structure:

| `levelNc` header | → `levelNf` field | Contents |
|---|---|---|
| `[0]` | `+0x2c` | sample table: 16-byte records `{offset.l, length-in-words.w, loop.w, …}` followed by 8-bit signed PCM |
| `[1]` | `+0x40` | status-panel graphics (copied, `0x810` longwords) |
| `[2]` | `+0x20` | **bob bank** |
| `[3]` | `+0x48` | realigned to 8 bytes at init |
| `[4]` | `+0x4c` | optional, realigned to 8 bytes |

`soundfx` and `soundfx4` use the same 16-byte sample records, offsets
relative to the start of the file. No sample rate is stored; callers pass the
Paula period (`0x2bc`, `0x258` and others, i.e. roughly 5–6 kHz).

### Bob bank (`FUN_00227b2e`)

```
+0           long   offset of the graphics area, from the bank start
+4 + 20*i    desc   { long gfx offset, word width-in-words, word height,
                      word hot-x, word hot-y, 8 bytes hit box }
gfx          per line: mask row, then planes 0..5, each width-in-words words
```

Drawn as a cookie-cut blit (minterm `$CA`, A = mask, B = plane data) into a
six-plane buffer with planes `0x6000` apart. Bank sizes: level 1 = 561
descriptors, level 2 = 697, level 3 = 654, level 4 = 513, boss = 530.

## `levelNf`

Header fields (offsets relative to the file, relocated at init):

| Field | Contents |
|---|---|
| `+0x00` w | level number |
| `+0x06` | ground tile directory |
| `+0x0a` | ground tile stream (compressed) |
| `+0x0e` | enemy type table |
| `+0x12` | enemy scripts and paths |
| `+0x16` | palette, 128 × R,G,B words |
| `+0x1c` | spawn list |
| `+0x24` / `+0x28` | cloud-layer map / tiles (levels 1 and 3 only) |
| `+0x3c` | attract-mode joystick recording, 4 words per step |

### Ground layer

Tiles are 16×16 in **seven** bitplanes (hence the 128-colour palette). Each
directory entry is a longword: bits 0–17 are a word offset from the directory
to the tile data; bits 31–18 hold 2 bits per plane — `00` sixteen data words,
`01` all ones, `10` all zeros, `11` one word repeated sixteen times.

The tile stream is decoded by a coroutine at `0x22d61e` (called through
`FUN_0022d614`, one tile number per call). Control byte `b`:

| `b` | Meaning |
|---|---|
| `1xxx nnnn` | literal: `n+1` bytes follow, each the low 8 bits of a tile number; the high 3 bits are `(b<<4) & 0x700` |
| `0000 nnnn` | repeat the current tile `n+1` times |
| `0001 nnnn` | `n+1` tiles, each one less than the previous |
| `0010 nnnn` | as `0001`, then one tile `+7` |
| `0011 nnnn` | `n+1` tiles, each one more than the previous |
| `0100 xxxx` | end of stream |
| `0101`–`0111` | back-reference: the word `w = b<<8 \| next`; re-read the literal at `position_of_b + 0x5000 − w` |

Tiles fill rows of 24 (384 pixels) from right to left, rows from the bottom of
the level upwards (`FUN_0022cc28`, `FUN_0022ce72`). Stream lengths: level 1
23,232 tiles (968 rows), level 2 22,320, level 3 26,256, level 4 24,048, boss
1,584. The scroller can rewind the decoder state (`0x22d860`) to repeat a
stretch, so the linear decode is the level's material, not its exact
on-screen length.

### Spawns, types, scripts

Spawn records (`FUN_0022ec94`) are 12 bytes, `{trigger, x, y, type×4, flags,
param}`, terminated by a negative trigger. A record fires when the scroll
position minus the segment base equals `trigger`.

`+0x0e` is a table of longwords indexed by `type×4`, each an offset (from the
start of `levelNf`) to a type definition: script offset, flags, an x/y offset
pair, a word, and a path offset (both offsets relative to `+0x12`).

Scripts are word opcodes, each a byte offset into a 45-entry jump table at
`0x22f8d2`. Opcode `0` sets the animation frame: `[0][delay][N][bob…]`. Opcode
`0x20` dispatches again through its own sub-table. The full instruction set is
not decoded here.

## The floppy release (A1200, four disks)

* Volume names are `bans1`…`bans4`; the floppy `startup-sequence` assigns
  `banshee1:` … `banshee4:` to them. `bans1:flev` is present in the floppy
  `bans.exe` too, so it predates both builds (open question 5).
* `scrpt2` on disk 1 is two lines, `banshee1:picture.exe` and
  `banshee1:bans.exe`. The installer appends it to the hard-disk start script,
  so **`picture.exe` was the title screen of the hard-disk installation**. The
  same file is present in all ten Disk 1 variants examined, from unrelated
  sources. On the CD `scrpt2` is zero bytes, so nothing runs the picture
  (open question 8).
* `/icons` on the floppy holds `banshee.info`, which the installer copies; on
  the CD the directory is empty (open question 9). `Installer` is 63,436 bytes
  on the floppy and zero on the CD.
* The floppy file dates are also **1992-12-21**, 15:19–15:31 (open question 2):
  the wrong clock belongs to the machine the game files came from, not to the
  CD mastering session.
* Floppy `picture.exe` is not crunched; its 327,744-byte bitmap hunk is
  byte-identical to the CD's decrunched hunk 3. Its copper list starts with
  every colour at zero (fade-in), the CD's has the colours pre-filled; the
  palette table at `0x2c8` is identical.
* Floppy `bans.exe` carries the same link stamp, `8/7-94 12:59`, with
  `RNC Beta` where the CD has `CD32 slut`. Its code hunk is RNC method 1,
  106,824 bytes unpacked against the CD's 97,500. Strings only in the floppy
  build: the in-game music module `p60.calm bottom4` (one copy on each of
  disks 2–4) and a one-/two-button option in five languages, including Danish
  `Een knap` / `To knapper`. Only in the CD build: `cd.device`,
  `lowlevel.library`, `Joypad` / `Joystick`. The CD replaces the in-game
  module with the two Red Book tracks.

## Tools

In [`tools/`](../tools/): `ground.py` (tile stream and directory), `bobs.py` (bob bank),
`map.py` (cloud layer), `spawns.py` (spawn overlay), `samples.py` (sample
tables to WAV), `adf.py` (FFS reader).

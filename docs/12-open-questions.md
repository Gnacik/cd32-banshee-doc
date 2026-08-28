# Open questions

Everything this repository could not settle, with the measurement beside it.
A question with a number attached is worth more than an answer without one.

## 1. What produces a 232-sector trailing run instead of 32?

```
disc         preparer      declared volume   trailing zero run
Liberation   D J Pocock            82,502    232
Banshee      D J Pocock             1,687    232
the other 8  various          772..255,552    32
```

Eight ISOCD discs leave 32, across a 331 : 1 span of volume sizes and two tool
versions. Two leave 232, and they are the two discs whose preparer field names
the same person — across two unrelated studios and two unrelated publishers,
three months apart. The size explanation is dead (1,687 against 82,502).

Two observations are not a correlation. **The test is one field comparison on
the next disc**: if a third `D J Pocock` disc turns up, check the trailing run
before anything else; if a 232 turns up under a different name, this is
coincidence. What it would mean if it holds is that an ISOCD option or a
padding setting travelled with an operator rather than with a tool version.

## 2. Why is `1992-12-21` on two unrelated discs, in the same quarter hour?

```
Banshee   41 file records          1992-12-21 15:11:46 .. 15:27:34
Marvin    PVD                      1992-12-21 15:15:40
Marvin    all 9 directory records  1992-12-21 15:24:31 .. 15:26:43
```

Two discs from unrelated studios and publishers, on the same wrong date, with
overlapping times of day inside the same sixteen-minute window — and on
different halves of the disc, Banshee's from the *source* file system and
Marvin's from the *mastering* machine.

A dead battery on an Amiga gives 1978, not this. The shape that would explain
it is a machine with **no battery-backed clock**, where AmigaDOS restores the
date from the boot volume at every boot and the time runs forward from there:
every session then starts at the same stored date and the time-of-day is a
function of uptime only.

This repository cannot test that. **The next disc carrying 1992-12-21 decides
it**, and the thing to record when one does is the *time of day*, not just the
date.

## 3. Where do the copper modulos come from?

The two copper templates in `bans.exe` set

```
game screen     BPLCON0 $0211 (lores, 8 planes)   BPL1MOD = BPL2MOD = $0070 = 112
picture screen  BPLCON0 $8211 (hires, 8 planes)   BPL1MOD = BPL2MOD = $0228 = 552
```

with `FMODE $0007` (64-bit bitplane fetch) and `DDFSTRT $0038` / `DDFSTOP
$00D0` on both.

The picture files' geometry is settled independently and unambiguously —
`introscreen` renders correctly as 640 × 256, eight bitplanes, interleaved, 80
bytes per plane row, and the screen-clear blit's own numbers (width 80 bytes,
`BLTDMOD` 560, eight passes at 80-byte intervals) reproduce 640 bytes per
display row and 163,840 bytes total. A row advance of 640 with 80 bytes
fetched would want a modulo of 560, not 552.

So either the fetch is 88 bytes per plane per line under `FMODE 3` with this
`DDF` window, or the pointers are advanced somewhere else as well. The
repository has no emulator in the loop, and this is exactly the kind of number
that is easy to rationalise and hard to be sure of. **Recorded as measured,
not reconciled.**

The lores template's 112 is further from anything derivable and its screen's
geometry is not independently pinned down at all — the game's playfield buffer
is in chip BSS and the pointers are written at run time.

## 4. What is the playfield buffer's geometry?

The object blit ([07-graphics.md](07-graphics.md)) steps the destination by
`$6000` = 24,576 bytes six times, so the playfield is **six bitplanes,
non-interleaved, 24,576 bytes per plane**. 24,576 factors as 96 × 256 and as
64 × 384 and as 48 × 512, and the blits that touch it use destination modulos
of 62, 66 and 14 with widths of 34 and 30 bytes, giving row advances of 96, 96
and 48.

96 bytes per row is 768 pixels for a display window of 320. Whether that is a
scroll margin, a double buffer laid out side by side, or something else is not
established. The game screen's copper template asks for **eight** planes and
this buffer has six, so they are not the same buffer.

## 5. What was `flev`, and what is `bans1:`?

`bans1:flev` sits after the loader's 37 records with no record header
([11-leftovers.md](11-leftovers.md)). `bans1:` is assigned by nothing;
`banshee1:` is. `flev` is not on the disc.

An A1200 floppy release, or an ADF of one, would settle both in a single
string search. This repository has neither.

## 6. Why did `soundfx4` take seven and a half minutes?

The copy session's other 40 gaps track file size at roughly 150–200 KB/s.
`plyrmisc4` is written at wrong-clock 15:20:06 and `soundfx4`, 108,871 bytes,
at 15:27:34 — **7 minutes 28 seconds** where its size predicts about nine.
It is the last file written before ISOCD started, and the whole session only
had seventeen minutes in it.

## 7. What triggers the message about killing animals?

Eight lines at file offset 0x1F1C4, English only, outside the four-language
table ([11-leftovers.md](11-leftovers.md)). Nothing in the surrounding data
identifies a condition, and the repository does not run the game.

## 8. What ran `picture.exe`?

274,764 bytes, 9.5 % of the data track, holding a 640 × 512 HAM8 image, and
nothing on the disc names it ([08-picture-exe.md](08-picture-exe.md)). It is
the first file in the copy session, 36 seconds before `bans.exe`.

Candidates the disc cannot distinguish: a title screen from an earlier build
that was replaced by `introscreen`; a viewer used to show the picture to
somebody during development; or the A1200 floppy release's title program,
carried across with everything else. A floppy release would settle it.

## 9. What was `/icons` for?

An empty directory at LBA 1454, written 27 seconds before `/C`, on a disc with
no `.info` file anywhere ([11-leftovers.md](11-leftovers.md)).

## 10. What does the loader's flag byte mean?

Every one of the 37 file-table records carries `0x01` at offset +5
([05-loader.md](05-loader.md)). A field that never varies cannot be decoded
from one disc. Worth checking on any other title by the same team.

## 11. Is `0x9C` really Ø, or is the font not CP437 at all?

The Danish letters are `"` = Æ, `$` = Å, `+` = æ, `=` = å, `~` = ø and `0x9C`
= Ø, established from the hall-of-fame alphabet's ordering
([06-text.md](06-text.md)). CP437's `0x9C` is `£`, and the German and French
letters in the same table *are* CP437 (`0x81` ü, `0x82` é, `0x84` ä, `0x85` à,
`0x8A` è, `0x8B` ï, `0x94` ö, `0xE1` ß).

So either the font is CP437 with one glyph replaced, or it is a private font
that happens to agree with CP437 on eight positions. Rendering the font would
settle it; the font is inside a packed data file and has not been located.

## 12. Two things the platform checklist asks that this disc answers "nothing"

Recorded as results rather than as failed checks:

* **No `.bak` beside the boot script.** Two discs in eleven have one and both
  times it named the ancestor. This one has none.
* **No `.info` files at all**, so the hash comparison that identified Blitz
  Basic 2 on Guardian has nothing to compare.

# Banshee against Dragonstone — the first same-label control

This series has eleven discs before this one. Two of them are the *same title
on two consoles* (Prey, CD32 and CDTV) and two are the *same publisher*
(Legends and Gloom, both Guildhall, which agree on nothing). What it has never
had is **two discs from the same name on the box**, close enough in date to
share a build kit, documented to the same depth.

Dragonstone is Core Design, 1994/1995. Banshee is Core Design, 1994. This
document compares them point by point. **The predictions below were written
before any of the measurements were made**, and where a prediction was wrong
it is marked wrong and left in.

## First, a correction to the premise

The comparison is weaker than "same studio" and the disc says so itself. The
credits screen reads:

```
Programming and Design   Søren Hannibal
Graphics and Design      Jacob "Jade" Andersen
Music and soundfx        Martin Iveson
Lots of ideas and gameplay tweaking   Adrian Smith
Storyboard etc.          Guy "The Dictionary" Miller
Thanks to  Ged  Mark W  Mark P  Mac  Jon  Jim
           Barry  Roberto and the rest at Core
                                     © 1994 Jeremy Heath Smith
```

Three independent things say the two people who wrote it worked in Danish:
a **fourth language, Danish**, in the four-language table
([06-text.md](06-text.md)); the build banner inside `bans.exe` written
`8/7-94 12:59 CD32 slutp`, in day/month-year order with a dash and the Danish
word *slut*; and the hero being renamed `Svend` in the Danish text alone. And
the credit list thanks "**the rest at Core**" as a group the writers are not
part of.

So this is a **same-label** control rather than a same-studio one: one Core
Design title made in Derby and one made for Core by a two-person Danish team.
That does not weaken the result — it sharpens the question. If a shared build
kit travels with a publishing deal, it should show up here.

## The comparison

| | Dragonstone | Banshee | |
|---|---|---|---|
| Preparer field | `Sajjad Majid` | **`D J Pocock`** | ✗ |
| `c/SetPatch` | 40.14, 13,200 B | **byte-identical** | ✓ |
| `.TM` block | the common 2,048 bytes | **byte-identical** | ✓ |
| Timestamp epoch | AmigaDOS 1978, uptime | 1992-12-21, a wrong clock | ✗ |
| Timestamp *shape* | a 26-minute copy log | a 15m48s copy log | ✓ |
| Cruncher | RNC ProPack method 1 | **RNC ProPack method 1** | ✓ |
| Dragonstone's `rnc.py` on this disc | — | **37/37, first run, all CRCs** | ✓ |
| Fixed-size buffers | 73.9–95.2 % used | 60.6–100 % used | ✓ |
| Library calls in the loader | **zero** | **71, across 33 LVOs** | ✗ |
| ISO 9660 parsing | by hand, no OS | `dos.library` `Open`/`Read` | ✗ |
| Overlay header | `DNLD`, 16 bytes | **no `DNLD` anywhere** | ✗ |
| File-table format | fixed-width names + 16-bit index table | variable-length records | ✗ |
| Text encoding | CP437 | **CP437** (German/French) | ✓ |
| Languages | 3 | 4, the fourth with a private charset | ✗ |
| Text control codes | `FF FE FC FD` | `FF FE` only | ✗ |
| Akiko `$00B80000` pointer load | **yes** — drives the drive | **zero** | ✗ |
| Akiko `$B80038` / `$B8003C` | zero | zero | ✓ |
| `$C0DE0000` | zero | zero | ✓ |

Nine mismatches, eight matches. What decides the question is not the count but
**which** things matched.

## The three things that matched are the three things nobody wrote

**The `.TM` block** is Commodore's `CD32.TM`, a file every CD32 developer was
sent. It is byte-identical on ten of the eleven CD32-era discs in this series,
from ten studios and ten publishers across thirty-eight months. Matching it
carries no information about anything.

**`c/SetPatch`** looked like the strongest possible evidence and the control
set kills it. Ten discs carry SetPatch and there are six distinct binaries; a
matching hash always means a matching `$VER:` and never means anything else:

| SHA-1 | Bytes | `$VER:` | Discs |
|---|---:|---|---|
| `00d74a35…` | 13,200 | `setpatch 40.14 (7.10.93)` | **Dragonstone, Banshee** — both Core |
| `5fa6e230…` | 12,968 | `setpatch 40.12 (16.9.93)` | Prey CD32, Liberation, HeroQuest II |
| `8b6cf001…` | 10,964 | `setpatch 40.3 (10.5.93)` | Guardian, Gloom |
| `4d4aae98…` | 7,364 | `setpatch 39.6 (8.9.92)` | Marvin, Legends |
| `568db17c…` | 13,484 | `setpatch 40.16 (14.2.94)` | Speris |
| `7b42c0b6…` | 5,088 | `SetPatch 1.34 (12-May-89)` | Prey CDTV |

Four of the six binaries are shared by two or more discs. **Exactly one of
those four groups is a same-publisher group and three are not** — Prey with
Liberation with HeroQuest II is three studios and three publishers; Guardian
with Gloom is two; Marvin with Legends is two. So the prior probability that a
SetPatch match means "same label" is about one in four, which is to say the
match is real and tells you nothing. What it identifies is **which Kickstart
3.1 release was on the build machine**, and in 1993–94 there were only five in
circulation.

The prediction — *a byte-identical match would be the first studio-level proof*
— is therefore **wrong**, and it is wrong in an instructive way: it was a good
prediction until there was a control set to test it against, and the control
set was already in the repository.

**RNC ProPack method 1** is the strongest of the three and still not a studio
signal. It is a commercial cruncher (Rob Northen Computing) that was on a
large fraction of Amiga developers' shelves; the useful measurement is not
that both discs use it but that **Dragonstone's decoder, copied without a line
changed, unpacked all 37 of Banshee's streams on the first run with every
CRC-16 checking**. Same method, same version, same header layout, same
fixed-size-buffer habit. That is a shared toolshelf — but it is the Amiga
scene's shelf, not Core Design's.

## The nine things that differ are the nine things somebody wrote

The loader is the clearest. Dragonstone's `Lx_DataL.exe` makes **no library
calls at all**, sets `move #$2700,sr`, parses ISO 9660 by hand, drives the CD
through Akiko at `$B80000`, and wraps its overlays in a 16-byte `DNLD` header.
`bans.exe` opens five libraries and two devices, makes **71 `jsr d16(a6)`
calls across 33 distinct LVOs**, loads every file with `dos.library`'s
`Open`/`Read`/`Seek`/`Close`, and never touches Akiko. The string `DNLD` does
not occur in Banshee's volume; neither does `CDIOEND`, Dragonstone's
module-end marker.

The file tables are the same idea implemented twice with nothing in common.
Dragonstone: fixed-width filenames followed by a 12 × 7 table of 16-bit
indices. Banshee: variable-length records of `[size:4][disk:1][flag:1][path]`
with the path carrying its own floppy volume name.

The text tables are the same idea implemented twice with nothing in common.
Both are CP437, which is the one shared thing and is an artefact of both teams
using a PC to type foreign text; the structures are unrelated, the control
codes are different, and Banshee has a private six-character Danish extension
that Dragonstone has no equivalent of.

And Akiko — the one place a shared low-level library would be visible — is
**zero on both halves**. The prediction here was split in two and half of it
was wrong:

* *`$00B80000` pointer load: predicted **positive*** (same studio, same
  first-generation loader) — **wrong, zero**;
* *`$00B80038` / `$00B8003C`, the chunky-to-planar port: predicted negative* —
  correct, zero;
* *`$C0DE0000`: predicted negative* — correct, zero.

## What this answers

The checklist's open item 14 asks whether the unit of shared practice is the
studio or something else. On the evidence of two discs from one label, **it is
not the studio and it is not the label.** Everything that matched is
attributable to something wider than either:

| Unit | What it explains |
|---|---|
| Commodore's developer distribution | the `.TM` block, `c/Assign` 37.4 on six discs |
| The AmigaOS release on the build machine | which of six `SetPatch` binaries |
| The Amiga commercial tool market | RNC ProPack, the Imploder, CrunchMania, Blitz Basic 2 |
| **The person who cut the master** | see below — this is new |
| The individual programmer | the loader, the file table, the text format, the display code |

and "the studio" does not appear in it.

## A unit that does show up, and it is not one anybody proposed

The preparer field on this disc reads

```
D J Pocock - ISOCD 1.04 by Pantaray, Inc. USA -
```

which is character for character
[Liberation](https://github.com/vs-sr-dev/cd32-liberation-doc)'s — a Byte
Engineers title published by Mindscape, mastered three months earlier. Two
unrelated studios, two unrelated publishers.

And those two discs share something else that no other disc in the series
does. Eight discs leave a run of **32** zero sectors at the end of the volume,
across volumes from 772 to 255,552 sectors. Liberation leaves **232**. Banshee
leaves **232** — in a volume of 1,687 sectors, one forty-ninth of
Liberation's, which kills the last surviving explanation that the number was a
function of size.

```
disc         preparer      volume     trailing run
Liberation   D J Pocock    82,502     232
Banshee      D J Pocock     1,687     232
the other 8  various       772..255,552   32
```

Two variables, two discs, perfect correlation, and no third disc yet to break
it. It is not proof — two observations never are — but it is the first time
any layout anomaly in this series has lined up with a named individual, and it
costs one field comparison to check on the next disc. **When a mastering
anomaly appears, read the preparer field before looking for a technical
cause.**

## The short version

Two discs, one publisher, three months apart. They share a Commodore file,
an operating-system file, and a commercial cruncher — and nothing else. Every
component either team actually wrote is different, down to the number of
control bytes in the string table. The only cross-disc regularity this
comparison turned up runs the *other* way: it links Banshee to a disc from a
completely different studio, through the person who ran the mastering tool.

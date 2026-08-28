# The boot chain

`/s/startup-sequence`, 230 bytes, twelve lines. It is the only boot script in
this series with a **conditional developer branch still in it**.

```
c:Setpatch quiet
c:assign >NIL: DebugDisk: exists
if not warn
   c:assign t: ram:
   c:execute DebugDisk:debugscript
endif
;
C:assign banshee1: CD0:
C:assign banshee2: CD0:
C:assign banshee3: CD0:
C:assign banshee4: CD0:
bans.exe
```

## The debug hook

Lines 2 to 6 are a shipped, pressed, retail hook for a development machine.

`assign >NIL: DebugDisk: exists` is the AmigaDOS idiom for "does the assign
`DebugDisk:` exist" — it prints nothing and sets the condition flag. `if not
warn` is true when the assign *does* exist, and in that case the script
assigns `T:` to the RAM disk and **executes a script called `debugscript` off
a volume named `DebugDisk:`**.

On a CD32 there is no `DebugDisk:` and the branch is skipped, so the hook is
inert on the shipped hardware. On the developers' machines it was the way in:
plug in a drive or a partition assigned `DebugDisk:`, put a `debugscript` on
it, and the retail boot script runs it before the game starts, with a writable
`T:` already set up.

Nothing else on the disc mentions `DebugDisk` or `debugscript` — the string
`DebugDisk` occurs once in the whole volume, in this file, and `bans.exe`
contains neither word. It is a boot-script-level facility and it survived into
the master.

This is a different kind of leftover from the ones this series has collected
so far. Gloom and Guardian ship the *previous* boot script as a `.bak`;
Marvin ships an unused development command in `c/`. Banshee ships the live
boot script with the developer's own escape hatch still wired into it.

There is **no `.bak`** beside it, so the check that has paid twice does not
pay here.

## Four floppy volumes assigned to one CD

```
C:assign banshee1: CD0:
C:assign banshee2: CD0:
C:assign banshee3: CD0:
C:assign banshee4: CD0:
```

`bans.exe` addresses all 37 of its data files through these four names —
`banshee2:level1c`, `banshee4:soundfx4`, `banshee1:introseq.001` and so on
([05-loader.md](05-loader.md)). This is the fifth shape of boot script the
platform checklist describes and the third sighting of the idiom: Speris uses
`speris-1:`…`speris-4:`, HeroQuest II uses `"Legacy of Sorasil DISK 1:"`…`3:`,
and Banshee uses `banshee1:`…`banshee4:`.

The four names reconstruct the **A1200 floppy release's disk layout** from the
CD alone, and the loader's table says which file was on which disk
([05-loader.md](05-loader.md)):

| Disk | Files |
|---|---|
| `banshee1:` | 21 — `bossc`, `bossf`, both music modules, all 17 cut-scene frames |
| `banshee2:` | 6 — `core`, `plyrmisc`, `soundfx`, `level1c`, `level1f`, `introscreen` |
| `banshee3:` | 4 — `level2c`, `level2f`, `level3c`, `banspic2` |
| `banshee4:` | 6 — `level3f`, `level4c`, `level4f`, `plyrmisc4`, `soundfx4`, `banspic1` |

The detail that makes this a real floppy layout rather than a decoration:
**level 3 is split across two disks.** `level3c` is on disk 3 and `level3f` is
on disk 4, which is what happens when a level's two halves will not fit on one
880 KB floppy together, and is not something anybody would invent for a CD.

There is no disk-swap prompt in the executable — no `Insert`, no `Disk`, no
`Please insert` — so unlike Dragonstone and HeroQuest II, the floppy prompt
was taken out and only the volume names were left. Which is the honest way
round to read it: **the assigns are the evidence, and their absence would not
have been.**

## `C:` — three commands, none of them the studio's

```
LBA 26   13,200 B  1993-11-11 09:50:58  C/SetPatch   $VER: setpatch 40.14 (7.10.93)
LBA 33    3,220 B  1993-06-17 14:40:04  C/Assign     $VER: assign 37.4 (25.4.91)
LBA 35    4,432 B  1993-06-17 14:40:04  C/Execute
LBA  0        0 B  1978-01-01 00:00:00  C/Installer  -- zero bytes
```

Hashes, against the other repositories in this series:

```
SHA-1  00d74a35300f7009ed02bc47db88427e9e0fc0a5  13,200 B  C/SetPatch 40.14
       == Dragonstone (Core Design) -- and nothing else in the set

SHA-1  b5b7edb67f578019d46af425a16458ec0cdb1c2e   3,220 B  C/Assign 37.4
       == Prey CD32, Speris, Legends, Liberation, HeroQuest II -- SIX discs now

SHA-1  ef1e6f6db0f3a513e0dc98add537e1db87b1856a   4,432 B  C/Execute
       -- first sighting in this series
```

`C/Assign` 37.4 is dated April 1991 and is now on **six** CD32 discs across
six studios, six publishers and three years, byte for byte. It is the most
widely copied file this series has found after the trademark block itself.

The SetPatch match with Dragonstone is the interesting one and it does **not**
mean what it looks like; [10-core-design-control.md](10-core-design-control.md)
takes it apart with the whole set as a control.

`C/Execute` is here because the debug branch calls it. `C/Assign` is here
because the four floppy assigns need it. `C/SetPatch` is line one. Every
command in `C:` is used by the boot script — which is unusual: most discs in
this series carry at least one command nothing runs.

Except the fourth, which is used by nothing and is zero bytes long. See
[11-leftovers.md](11-leftovers.md).

## What the boot script does not do

* **no `noopenwb`** — the game takes the machine over itself
* **no reboot at the end** — `bans.exe` restores what it took
* **no `libs/` and no `devs/`** — `lowlevel.library`, `freeanim.library` and
  `cd.device` are all in the CD32's ROM, and the disc carries no fallback copy
  of any of them, so this executable cannot boot an A1200 from this disc
* **no `<Game>.info` and no `IconX`** — there is no desktop entry point; the
  `/icons` directory that would have held one is empty

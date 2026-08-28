# String inventory

Every string of five or more printable characters in `bans.exe` that reads
as language rather than as code (three consecutive lower-case letters, or
six or more upper-case letters and spaces), with its file offset. The
four-language dialogue table occupies 0x1C400..0x1F300 and is listed
separately in [text-table.txt](text-table.txt); it is excluded here.

`picture.exe` has no strings at all: hunk 0 is 484 bytes of depacker and
hunks 1-3 are RNC ProPack method 2 streams.

Reproduce with `python3 tools/strings.py _work/ext/bans.exe -n 5`.

| Offset | String |
|---|---|
| `0x000050` | `Nu8/7-94 12:59 CD32 slutp` |
| `0x00075c` | `lowlevel.library` |
| `0x000b24` | `Nufreeanim.library` |
| `0x000b37` | `graphics.library` |
| `0x000b48` | `dos.library` |
| `0x000b54` | `intuition.library` |
| `0x000b66` | `input.device` |
| `0x000b73` | `cd.device` |
| `0x001af3` | `$}swu` |
| `0x002814` | `banshee2:core` |
| `0x002828` | `banshee2:plyrmisc` |
| `0x002840` | `banshee2:soundfx` |
| `0x002858` | `banshee2:level1c` |
| `0x002870` | `banshee2:level1f` |
| `0x002888` | `banshee3:level2c` |
| `0x0028a0` | `banshee3:level2f` |
| `0x0028b8` | `banshee3:level3c` |
| `0x0028d0` | `banshee4:level3f` |
| `0x0028e8` | `banshee4:level4c` |
| `0x002900` | `banshee4:level4f` |
| `0x002918` | `banshee4:plyrmisc4` |
| `0x002932` | `banshee4:soundfx4` |
| `0x00294a` | `banshee1:bossc` |
| `0x002960` | `banshee1:bossf` |
| `0x002976` | `banshee2:introscreen` |
| `0x002992` | `banshee3:banspic2` |
| `0x0029aa` | `banshee4:banspic1` |
| `0x0029c2` | `banshee1:p60.end` |
| `0x0029da` | `banshee1:endseq1.001` |
| `0x0029f6` | `banshee1:endseq1.002` |
| `0x002a12` | `banshee1:endseq1.003` |
| `0x002a2e` | `banshee1:endseq1.004` |
| `0x002a4a` | `banshee1:endseq1.005` |
| `0x002a66` | `banshee1:endseq2.001` |
| `0x002a82` | `banshee1:endseq2.002` |
| `0x002a9e` | `banshee1:endseq2.003` |
| `0x002aba` | `banshee1:endseq2.004` |
| `0x002ad6` | `banshee1:endseq2.005` |
| `0x002af2` | `banshee1:p60.intro` |
| `0x002b0c` | `banshee1:introseq.001` |
| `0x002b28` | `banshee1:introseq.002` |
| `0x002b44` | `banshee1:introseq.003` |
| `0x002b60` | `banshee1:introseq.004` |
| `0x002b7c` | `banshee1:introseq.005` |
| `0x002b98` | `banshee1:introseq.006` |
| `0x002bb4` | `banshee1:introseq.007` |
| `0x002bca` | `bans1:flev` |
| `0x004a24` | `XHXIRL` |
| `0x004aae` | `XHXIRL` |
| `0x005efc` | `audio.device` |
| `0x005f09` | `ciax.resource` |
| `0x005f18` | `P60TimerInterrupt` |
| `0x006688` | `HBHCHDBBBCBD` |
| `0x00b506` | `XHXIRL` |
| `0x00b5d7` | `XXHXIRL` |
| `0x00bb5a` | `XHXIRL` |
| `0x00bc50` | `XHXIRL` |
| `0x00db3f` | `dnr0*` |
| `0x00db45` | `dgl2-` |
| `0x01038f` | `vdz`2` |
| `0x014fcb` | `-mhgJ` |
| `0x01a1e6` | `B^4hrj` |
| `0x01b05c` | `OC?zjv` |
| `0x01b113` | `rzlUA` |
| `0x01c323` | `0qpp0` |

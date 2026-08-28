# Text

All of the game's text is in `bans.exe`, in the data area of hunk 0, roughly
file offset 0x1C560 to 0x1F300. There is no language file, no `.lng`, and
nothing to select at build time: **all four languages ship in every copy** and
the menu switches between them at run time (`English` / `Deutsch` /
`Francais` / `Dansk`).

Extract it with `python3 tools/text.py _work/ext/bans.exe`; full output in
[notes/text-table.txt](../notes/text-table.txt).

## Structure

Two control bytes, and only two:

```
0xFF   ends one language variant
0xFE   ends a group of four
```

so a group is `english FF german FF french FF danish FF` followed by `FE`.
There is no length prefix, no index table and no padding: 68 groups, 276
`0xFF`s, laid down end to end. Dragonstone uses four control codes
(`0xFF`/`0xFE`/`0xFC`/`0xFD`); on this disc `0xFC` and `0xFD` do not occur in
the text region at all.

The language order is fixed and never varies:

```
group 4    English   Deutsch   Francais   Dansk
group 9    Easy      Leicht    Facile     Nem
group 5    View Highscores
                     Höchstpunktzahlen ansehen
                               Meilleurs scores
                                          Se Højskoren
```

Where a language has no translation the English is repeated verbatim
(`Options` / `Options` / `Options` / `Valg`, `On` / `Ein` / `On` / `På`), so
the table is complete but the French menu is partly English.

## The character set: code page 437, plus three letters on punctuation keys

The German and French accented letters are ordinary **code page 437** bytes,
the same encoding Dragonstone uses:

```
0x81 ü    0x82 é    0x84 ä    0x85 à    0x8A è    0x8B ï    0x94 ö    0xE1 ß
```

`Zurück zum Hauptmenü` is `5A 75 72 81 63 6B 20 7A 75 6D 20 48 61 75 70 74 6D
65 6E 81`, and 0x81 is `ü` in CP437 and a C1 control in Latin-1, so the
identification is unambiguous.

The three Danish letters are **not** CP437 bytes, although CP437 has room for
them. They are ASCII punctuation:

| Byte | Character | Letter |
|---|---|---|
| `0x22` | `"` | Æ |
| `0x24` | `$` | Å |
| `0x2B` | `+` | æ |
| `0x3D` | `=` | å |
| `0x7E` | `~` | ø |
| `0x9C` | (CP437 `£`) | **Ø** |

which is why a straight CP437 decode of this disc produces clean German and
French and nonsense Danish:

```
raw     Hold spillere p= sk+rmen
means   Hold spillere på skærmen

raw     S~ren Hannibal
means   Søren Hannibal

raw     $h, Svend - s= t~t p= og alligevel s= langt fra!
means   Åh, Svend - så tæt på og alligevel så langt fra!
```

Five of the six are punctuation and the sixth, uppercase Ø, is a high byte —
which looks arbitrary until you find the alphabet.

### The alphabet settles it

The hall-of-fame name entry stores its character set as a `0xFF`-separated
list at file offset 0x1F274:

```
A FF B FF C FF ... X FF Y FF Z FF " FF 9C FF $ FF space FF FF
a FF b FF c FF ... w FF ...
```

The three characters after `Z` are `"`, `0x9C` and `$` — and **Æ, Ø, Å is the
Danish alphabet's order after Z**. The mapping is not arbitrary at all: it is
a Danish alphabet, appended to a Latin one, with whatever font slots were
free. Five ASCII punctuation positions were free and one was not, so Ø went to
0x9C.

This is a fifth kind of answer to the platform checklist's encoding question,
and it is worth stating in the general form: **a disc can use a standard code
page for one language group and a private substitution for another, in the
same string table, with no marker of any kind.** The give-away is a language
whose text is full of `~`, `=` and `+` where letters should be.

## Four languages, and the Danish one is not a translation

The Danish text is longer and funnier than the other three, and in places it
is a different text:

```
en   You really are a hero of epic proportions!
de   Du bist in der Tat ein Held von epischer Größe!
fr   Tu es un véritable héros épique!
da   Du er virkelig en helt af episke proportioner,
     og det selvom dit navn er lidt nedtur!
```

— "and that even though your name is a bit of a let-down", which no other
language says. The hero is `Sven Svardensvart` everywhere except in Danish,
where he is **`Svend`**. And the ending line

```
en   Ah, Sven. So near and yet so far!
da   Åh, Svend - så tæt på og alligevel så langt fra!
```

is the only one of the four that is idiomatic.

Taken with the credits, the build banner and the fourth language existing at
all, this is the disc telling you which language it was written in. See
[10-core-design-control.md](10-core-design-control.md).

## The plot, in full

The four-language table carries the whole intro and both endings. In English:

```
Earth, 1999.  But the Earth of a different timeline.
There are no microwave ovens and tv is still in black and white.
Humanity lives peacefully, until...
Blardax Maldrear, The evil ruler of the Styx Empire,
has an exquisitely evil idea...
Wouldn't it be great if he could take over good old planet Earth?
The invasion begins...
...And only one man stands in the way of Blardax's
relentless lust for world domination.
His name: Sven Svardensvart!
Sven has good reason to hate the Styx invaders.
His father was murdered by them for refusing to
invent the microwave oven.
Sven escapes to the last free place on Earth
and swiftly builds an incredible flying machine
with big guns and rockets...
```

and the four level briefings, which is the only place on the disc that names
the levels:

```
1  Fly across the Atlantikan Ocean and destroy the Styx held
   Harbour town of Mova Scosha...
2  Enter Styx City and destroy the gigantic guardians...
3  Obliterate the Styxian High Command in their defence bunker and steal the
   technology required to equip your Banshee with spaceflight capability...
4  Earth is free! Blardax is fleeing to his command base on Veenix!
   Give chase in your redesigned Banshee and put an end to him once and
   for all..!
```

There are two endings — `endseq1.*` and `endseq2.*`, five frames each — and
the text says why: finishing on the easiest difficulty gets

```
Congratulations. You have completed Banshee on the easiest difficulty
level. Now join the tough guys on Hard to see the real ending.
```

## One block that is not in the table

At file offset 0x1F1C4, eight lines of nineteen columns, each terminated by
`0xFF` and right-padded with spaces, **with no German, French or Danish
variant and no `0xFE` group terminator**:

```
    YOU REALLY NEED
    A MENTAL
    EXAMINATION.

    HOW CAN ANYONE
    SERIOUSLY WANT
    TO KILL ANIMALS
    AND CIVILIANS.
```

See [11-leftovers.md](11-leftovers.md).

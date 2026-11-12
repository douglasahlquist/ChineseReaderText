# Bible passages

`bible_pages.py` builds a Chinese Reader page for a Bible passage. In the app each verse shows
the Hanzi (pinyin on tap, words spoken whole), then one row per version underneath: first the
original language (Greek for the New Testament, Hebrew for the Old Testament, right to left),
then the English, then any other versions. `--en web,kjv` gives two English rows.

```
pip3 install pypinyin jieba opencc-python-reimplemented

python3 tools/bible/bible_pages.py "Romans 12" --add-to-index
python3 tools/bible/bible_pages.py "罗马书 12:1-8"                 # Chinese book names work too
python3 tools/bible/bible_pages.py "Psalm 23" --en web,kjv        # two English rows, Hebrew from the WLC
python3 tools/bible/bible_pages.py "John 3:16" --greek tr --stdout # print instead of writing
python3 tools/bible/bible_pages.py --versions
```

Run it from the ChineseReaderText folder. Pages go to `bible/passages/` (e.g.
`bible/passages/romans-12.md`); `--add-to-index` lists them under **经文 Passages** in
`bible/README.md`. The texts download once from GitHub into `~/.cache/chinesereader-bible`
(`BIBLE_CACHE` changes the folder).

| Option | Versions |
|---|---|
| `--zh` | `cuv` 和合本 simplified (default), `cuv-trad` traditional, `none` |
| `--en` | `web` World English Bible (default), `kjv`, `asv`, `none`; several with commas |
| `--greek` | `sblgnt` SBL Greek New Testament (default), `tr` Textus Receptus, `byz` Byzantine Textform, `none`; several with commas |
| `--hebrew` | `wlc` Westminster Leningrad Codex, without cantillation marks (default), `none` |

**Your own text.** `--hanzi-file` and `--english-file` take a text file with one verse per
line (`16 text` or `3:16 text`). Those verses replace the downloaded ones, so a translation that
can't be downloaded can still be used. Pinyin always comes from the Hanzi.

**Groups.** With the WEB, a passage is split into the WEB's paragraphs; otherwise into groups
of 5 verses (`--group N` sets the size).

**Pinyin.** pypinyin with jieba word splitting, a list of Bible readings (耶和华 Yē hé huá,
弟兄 dì xiong, 得着 dé zháo, …) and the tone changes of 不 and 一. Check each page: a word with
two readings can still come out wrong. Add fixes to `PHRASES`, `SINGLE`, `DE_GET` or the word
lists near the top of the script.

**Sources.** Chinese Union Version, KJV, ASV, Textus Receptus, Byzantine Textform and WLC from
scrollmapper/bible_databases; the World English Bible from TehShrike/world-english-bible; the
SBLGNT from morphgnt/sblgnt (its page carries the attribution the SBLGNT license asks for).
All are public domain except the SBLGNT, which is free to use with that attribution.

**The page.** Each group is a table marked `<!-- reader: table=verses -->`:
`| Hanzi | Pinyin | SBLGNT | WEB | KJV |`, one row per verse. The header names the versions;
the app shows each as a labeled row under the Hanzi, and Settings can hide the English rows or
the Greek and Hebrew rows. Only these pages look this way. Older app builds show the Hanzi,
pinyin and the first version (the Greek or Hebrew) as an ordinary line.

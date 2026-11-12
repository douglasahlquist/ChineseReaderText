#!/usr/bin/env python3
"""Builds Chinese Reader pages for Bible passages: Hanzi, pinyin, English, and the original
language (Greek for the New Testament, Hebrew for the Old Testament).

    python3 tools/bible/bible_pages.py "Romans 12"
    python3 tools/bible/bible_pages.py "罗马书 12"                 # the book's Chinese name works too
    python3 tools/bible/bible_pages.py "Romans 12:1-8" "Psalm 23" --en web,kjv --greek sblgnt,tr
    python3 tools/bible/bible_pages.py "John 3:16" --hanzi-file my-zh.txt --english-file my-en.txt
    python3 tools/bible/bible_pages.py "Romans 12" --add-to-index   # also list it in bible/README.md
    python3 tools/bible/bible_pages.py --versions                    # what each option means

Run it from the ChineseReaderText folder; pages go to bible/passages/. The texts are downloaded
once from GitHub and kept in ~/.cache/chinesereader-bible.

Each verse shows the Hanzi with its pinyin, then the Greek (or Hebrew), then the English, then
any other versions, one row each. --en, --greek
and --hebrew take one version or several, comma-separated (--en web,kjv gives two English rows).

Versions (all public domain, or free to use with the attribution the page carries):
  --zh      cuv (和合本, simplified; default) · cuv-trad (和合本, traditional) · none
  --en      web (World English Bible; default) · kjv · asv · none
  --greek   sblgnt (SBL Greek New Testament; default) · tr (Textus Receptus) · byz (Byzantine) · none
  --hebrew  wlc (Westminster Leningrad Codex; default) · none

Your own text: --hanzi-file and --english-file take a text file with one verse per line,
"16 text" or "3:16 text". Those verses replace the downloaded ones, so a version that can't be
downloaded (or a translation of your own) can still be used: give the Hanzi, the English, or both.
Pinyin is always generated from the Hanzi.

Needs: pip3 install pypinyin jieba opencc-python-reimplemented
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request

try:
    from pypinyin import Style, lazy_pinyin, load_phrases_dict
    import jieba
except ImportError:
    sys.exit("Needs pypinyin and jieba:  pip3 install pypinyin jieba opencc-python-reimplemented")

jieba.setLogLevel(60)
# Bible words the segmenter should keep whole, and splits it gets wrong in the CUV.
for _w in ["服事", "恒切", "圣徒", "帮补", "同心", "俯就", "牧者", "安歇", "以恶报恶", "神", "主", "得着",
           "弟兄们", "慈悲", "察验", "纯全", "旨意", "肢体", "恩赐", "预言", "执事", "教导", "劝化", "施舍"]:
    jieba.add_word(_w)
for _w in ["事主", "中要", "要恒切", "我必", "我以", "爱人", "神爱世人", "当照", "美的", "事要", "倒要", "神爱", "神所"]:
    jieba.del_word(_w)

try:
    from opencc import OpenCC
    _t2s = OpenCC("t2s")
    _s2t = OpenCC("s2t")
    def to_simplified(text): return _t2s.convert(text)
    def to_traditional(text): return _s2t.convert(text)
except Exception:  # pragma: no cover - only without opencc
    to_simplified = to_traditional = None

CACHE = os.path.expanduser(os.environ.get("BIBLE_CACHE", "~/.cache/chinesereader-bible"))
SCROLLMAPPER = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/{}.json"
WEB = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/{}.json"
SBLGNT = "https://raw.githubusercontent.com/morphgnt/sblgnt/master/{}-morphgnt.txt"

# ------------------------------------------------------------------------------------- books
# (English name, Chinese name, its pinyin, other English names and abbreviations)
BOOKS = [
    ("Genesis", "创世记", "Chuàng shì jì", "gen ge gn"),
    ("Exodus", "出埃及记", "Chū āi jí jì", "exod exo ex"),
    ("Leviticus", "利未记", "Lì wèi jì", "lev le lv"),
    ("Numbers", "民数记", "Mín shù jì", "num nu nm nb"),
    ("Deuteronomy", "申命记", "Shēn mìng jì", "deut de dt"),
    ("Joshua", "约书亚记", "Yuē shū yà jì", "josh jos"),
    ("Judges", "士师记", "Shì shī jì", "judg jdg jg"),
    ("Ruth", "路得记", "Lù dé jì", "ru rth"),
    ("1 Samuel", "撒母耳记上", "Sā mǔ ěr jì shàng", "1sam 1sa 1sm"),
    ("2 Samuel", "撒母耳记下", "Sā mǔ ěr jì xià", "2sam 2sa 2sm"),
    ("1 Kings", "列王纪上", "Liè wáng jì shàng", "1kgs 1ki 1kg"),
    ("2 Kings", "列王纪下", "Liè wáng jì xià", "2kgs 2ki 2kg"),
    ("1 Chronicles", "历代志上", "Lì dài zhì shàng", "1chr 1ch"),
    ("2 Chronicles", "历代志下", "Lì dài zhì xià", "2chr 2ch"),
    ("Ezra", "以斯拉记", "Yǐ sī lā jì", "ezr"),
    ("Nehemiah", "尼希米记", "Ní xī mǐ jì", "neh ne"),
    ("Esther", "以斯帖记", "Yǐ sī tiē jì", "esth est es"),
    ("Job", "约伯记", "Yuē bó jì", "jb"),
    ("Psalms", "诗篇", "Shī piān", "psalm ps psa pss"),
    ("Proverbs", "箴言", "Zhēn yán", "prov pro pr prv"),
    ("Ecclesiastes", "传道书", "Chuán dào shū", "eccl ecc ec qoh"),
    ("Song of Songs", "雅歌", "Yǎ gē", "song of solomon song sos ss canticles"),
    ("Isaiah", "以赛亚书", "Yǐ sài yà shū", "isa is"),
    ("Jeremiah", "耶利米书", "Yē lì mǐ shū", "jer je jr"),
    ("Lamentations", "耶利米哀歌", "Yē lì mǐ āi gē", "lam la"),
    ("Ezekiel", "以西结书", "Yǐ xī jié shū", "ezek eze ezk"),
    ("Daniel", "但以理书", "Dàn yǐ lǐ shū", "dan da dn"),
    ("Hosea", "何西阿书", "Hé xī ā shū", "hos ho"),
    ("Joel", "约珥书", "Yuē ěr shū", "jl"),
    ("Amos", "阿摩司书", "Ā mó sī shū", "am"),
    ("Obadiah", "俄巴底亚书", "É bā dǐ yà shū", "obad ob"),
    ("Jonah", "约拿书", "Yuē ná shū", "jon jnh"),
    ("Micah", "弥迦书", "Mí jiā shū", "mic mc"),
    ("Nahum", "那鸿书", "Nà hóng shū", "nah na"),
    ("Habakkuk", "哈巴谷书", "Hā bā gǔ shū", "hab hb"),
    ("Zephaniah", "西番雅书", "Xī fān yǎ shū", "zeph zep zp"),
    ("Haggai", "哈该书", "Hā gāi shū", "hag hg"),
    ("Zechariah", "撒迦利亚书", "Sā jiā lì yà shū", "zech zec zc"),
    ("Malachi", "玛拉基书", "Mǎ lā jī shū", "mal ml"),
    ("Matthew", "马太福音", "Mǎ tài fú yīn", "matt mat mt"),
    ("Mark", "马可福音", "Mǎ kě fú yīn", "mrk mk mr"),
    ("Luke", "路加福音", "Lù jiā fú yīn", "luk lk"),
    ("John", "约翰福音", "Yuē hàn fú yīn", "jhn jn"),
    ("Acts", "使徒行传", "Shǐ tú xíng zhuàn", "act ac"),
    ("Romans", "罗马书", "Luó mǎ shū", "rom ro rm"),
    ("1 Corinthians", "哥林多前书", "Gē lín duō qián shū", "1cor 1co"),
    ("2 Corinthians", "哥林多后书", "Gē lín duō hòu shū", "2cor 2co"),
    ("Galatians", "加拉太书", "Jiā lā tài shū", "gal ga"),
    ("Ephesians", "以弗所书", "Yǐ fú suǒ shū", "eph ephes"),
    ("Philippians", "腓立比书", "Féi lì bǐ shū", "phil php pp"),
    ("Colossians", "歌罗西书", "Gē luó xī shū", "col"),
    ("1 Thessalonians", "帖撒罗尼迦前书", "Tiē sā luó ní jiā qián shū", "1thess 1th"),
    ("2 Thessalonians", "帖撒罗尼迦后书", "Tiē sā luó ní jiā hòu shū", "2thess 2th"),
    ("1 Timothy", "提摩太前书", "Tí mó tài qián shū", "1tim 1ti"),
    ("2 Timothy", "提摩太后书", "Tí mó tài hòu shū", "2tim 2ti"),
    ("Titus", "提多书", "Tí duō shū", "tit ti"),
    ("Philemon", "腓利门书", "Féi lì mén shū", "philem phm pm"),
    ("Hebrews", "希伯来书", "Xī bó lái shū", "heb"),
    ("James", "雅各书", "Yǎ gè shū", "jas jm"),
    ("1 Peter", "彼得前书", "Bǐ dé qián shū", "1pet 1pe 1pt"),
    ("2 Peter", "彼得后书", "Bǐ dé hòu shū", "2pet 2pe 2pt"),
    ("1 John", "约翰一书", "Yuē hàn yī shū", "1jn 1jo 1jhn"),
    ("2 John", "约翰二书", "Yuē hàn èr shū", "2jn 2jo 2jhn"),
    ("3 John", "约翰三书", "Yuē hàn sān shū", "3jn 3jo 3jhn"),
    ("Jude", "犹大书", "Yóu dà shū", "jud jd"),
    ("Revelation", "启示录", "Qǐ shì lù", "rev re revelations apocalypse"),
]
NT_START = 40  # book number of Matthew (Genesis is 1)
SBLGNT_CODES = ["Mt", "Mk", "Lk", "Jn", "Ac", "Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th",
                "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud", "Re"]


def _key(name):
    return re.sub(r"[\s.]", "", name.lower())


BOOK_KEYS = {}
for number, (en, zh, _py, others) in enumerate(BOOKS, start=1):
    for name in [en, zh] + others.split():
        BOOK_KEYS[_key(name)] = number
    if to_traditional:
        BOOK_KEYS[_key(to_traditional(zh))] = number
    BOOK_KEYS[_key(zh.rstrip("书记"))] = BOOK_KEYS.get(_key(zh.rstrip("书记")), number)  # 罗马 → 罗马书
for alias, en in [("psalm", "Psalms"), ("诗", "Psalms"), ("songofsolomon", "Song of Songs")]:
    BOOK_KEYS[_key(alias)] = [b[0] for b in BOOKS].index(en) + 1


def find_book(name):
    key = _key(name)
    if key in BOOK_KEYS:
        return BOOK_KEYS[key]
    if to_simplified and _key(to_simplified(name)) in BOOK_KEYS:
        return BOOK_KEYS[_key(to_simplified(name))]
    # "1 Cor" → "1cor": a unique prefix of an English name.
    hits = {n for k, n in BOOK_KEYS.items() if k.startswith(key) and key[:1].isalnum() and len(key) >= 3}
    if len(hits) == 1:
        return hits.pop()
    raise SystemExit(f"Don't know the book “{name}”.")


REF = re.compile(r"""^\s*(?P<book>.+?)\s*第?\s*(?P<ch>\d+)\s*[章篇]?
                     (?:\s*[:：]\s*(?P<v1>\d+)(?:\s*[-–—~至到]\s*(?P<v2>\d+))?\s*节?)?\s*$""", re.X)


def parse_reference(text):
    """'Romans 12', 'Rom 12:1-8', '罗马书 12', '罗马书第12章', '罗马书12:1-8' → (book, chapter, v1, v2)."""
    m = REF.match(text)
    if not m:
        raise SystemExit(f"Can't read the reference “{text}”. Try e.g. “Romans 12” or “罗马书 12:1-8”.")
    book = find_book(m["book"])
    v1 = int(m["v1"]) if m["v1"] else None
    v2 = int(m["v2"]) if m["v2"] else v1
    return book, int(m["ch"]), v1, v2


# ----------------------------------------------------------------------------------- sources
def fetch(url, name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        print(f"  downloading {name} …", file=sys.stderr)
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
    return path


_json_cache = {}


def scrollmapper(code, book, chapter):
    """{verse: text} from one of the scrollmapper translations (whole-Bible JSON files)."""
    if code not in _json_cache:
        with open(fetch(SCROLLMAPPER.format(code), f"{code}.json"), encoding="utf-8") as f:
            _json_cache[code] = json.load(f)
    books = _json_cache[code]["books"]
    # Match by name: the Hebrew Bible (WLC) has its own book order and names like "I Samuel".
    entry = next((b for b in books if _book_number(b["name"]) == book), None)
    if entry is None:
        return {}
    for ch in entry["chapters"]:
        if ch["chapter"] == chapter:
            return {v["verse"]: v["text"].strip() for v in ch["verses"]}
    return {}


def web_english(book, chapter):
    """({verse: text}, [verses that start a paragraph]) from the World English Bible."""
    name = re.sub(r"[^a-z0-9]", "", BOOKS[book - 1][0].lower()).replace("songofsongs", "songofsolomon")
    with open(fetch(WEB.format(name), f"web-{name}.json"), encoding="utf-8") as f:
        items = json.load(f)
    verses, starts, new_paragraph = {}, [], True
    for item in items:
        kind = item.get("type", "")
        if kind in ("paragraph start", "stanza start"):
            new_paragraph = True
        if item.get("chapterNumber") != chapter or "verseNumber" not in item:
            continue
        v = item["verseNumber"]
        if new_paragraph and v not in starts:
            starts.append(v)
        new_paragraph = False
        verses[v] = (verses.get(v, "") + " " + item.get("value", "")).strip()
    return {v: re.sub(r"\s+", " ", t) for v, t in verses.items()}, starts


def sblgnt(book, chapter):
    code = SBLGNT_CODES[book - NT_START]
    number = book - NT_START + 61
    path = fetch(SBLGNT.format(f"{number}-{code}"), f"sblgnt-{number}-{code}.txt")
    verses = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            bcv = parts[0]
            if int(bcv[2:4]) != chapter:
                continue
            word = re.sub(r"[⸀⸁⸂⸃⸄⸅()\[\]]", "", parts[3])
            verses.setdefault(int(bcv[4:6]), []).append(word)
    return {v: " ".join(w) for v, w in verses.items()}


def _book_number(name):
    name = re.sub(r"^(III|II|I)\s", lambda m: f"{len(m[1])} ", name.strip())
    try:
        return find_book(name)
    except SystemExit:
        return None


def strip_cantillation(text):
    """Keeps Hebrew letters and vowel points; drops the cantillation (accent) marks."""
    return "".join(c for c in text if not 0x0591 <= ord(c) <= 0x05AF)


ZH = {"cuv": ("ChiUn", "和合本 (Chinese Union Version, 1919)"),
      "cuv-trad": ("ChiUn", "和合本 (Chinese Union Version, 1919, traditional)")}
EN = {"web": "World English Bible (WEB)", "kjv": "King James Version (KJV, 1769)", "asv": "American Standard Version (ASV, 1901)"}
GREEK = {"sblgnt": "SBL Greek New Testament (SBLGNT)", "tr": "Textus Receptus (1550/1894)",
         "byz": "Byzantine Textform (2013)"}
HEBREW = {"wlc": "Westminster Leningrad Codex (WLC)"}
ATTRIBUTION = {"sblgnt": "Greek: SBL Greek New Testament, © 2010 Society of Biblical Literature and Logos "
                         "Bible Software (sblgnt.com)."}


def chinese_text(version, book, chapter):
    raw = scrollmapper(ZH[version][0], book, chapter)
    out = {}
    for v, text in raw.items():
        # The CUV leaves a space before 神 (a mark of respect) and between some words. The spaces
        # are kept as word boundaries for the segmenter and removed from what is shown.
        # Only the space before 神 is kept as a boundary; the other spaces are uneven.
        text = re.sub(r"\s+(?=神)", "\u0001", text)
        text = re.sub(r"\s+", "", text).replace("\u0001", " ")
        if version == "cuv":
            if not to_simplified:
                raise SystemExit("cuv needs OpenCC:  pip3 install opencc-python-reimplemented")
            text = to_simplified(text).replace("著", "着")   # the CUV's 著 is the particle 着
        out[v] = text
    return out


def english_text(version, book, chapter):
    if version == "web":
        return web_english(book, chapter)
    return scrollmapper(version.upper(), book, chapter), []


def read_own_text(path, chapter):
    """'16 text' or '3:16 text' lines → {verse: text} (lines for other chapters are skipped)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\s*(?:(\d+)\s*[:：])?\s*(\d+)\s+(.+)", line)
            if m and (m[1] is None or int(m[1]) == chapter):
                out[int(m[2])] = m[3].strip()
    return out


# ------------------------------------------------------------------------------------ pinyin
# Readings that pypinyin gets wrong in the Bible, and names it doesn't know.
PHRASES = {
    "耶稣": [["yē"], ["sū"]], "耶和华": [["yē"], ["hé"], ["huá"]], "弟兄": [["dì"], ["xiong"]],
    "弟兄们": [["dì"], ["xiong"], ["men"]], "祭": [["jì"]], "献祭": [["xiàn"], ["jì"]],
    "圣灵": [["shèng"], ["líng"]], "以色列": [["yǐ"], ["sè"], ["liè"]], "基督": [["jī"], ["dū"]],
    "行善": [["xíng"], ["shàn"]], "行恶": [["xíng"], ["è"]], "恶": [["è"]], "为善": [["wéi"], ["shàn"]],
    "喜乐": [["xǐ"], ["lè"]], "乐意": [["lè"], ["yì"]], "长久": [["cháng"], ["jiǔ"]],
    "得着": [["dé"], ["zháo"]], "着": [["zhe"]], "仇敌": [["chóu"], ["dí"]], "报应": [["bào"], ["yìng"]],
    "伸冤": [["shēn"], ["yuān"]], "炭火": [["tàn"], ["huǒ"]], "供给": [["gōng"], ["jǐ"]],
    "看守": [["kān"], ["shǒu"]], "长老": [["zhǎng"], ["lǎo"]], "传道": [["chuán"], ["dào"]],
    "所得": [["suǒ"], ["dé"]], "用处": [["yòng"], ["chu"]], "照着": [["zhào"], ["zhe"]],
    "凭着": [["píng"], ["zhe"]], "服事": [["fú"], ["shi"]], "事奉": [["shì"], ["fèng"]],
}
# One-character words read differently on their own than pypinyin's default.
SINGLE = {"得": "de", "着": "zhe", "了": "le", "地": "dì"}
# 得 is dé (“to get”) after these words, de (linking a verb to how it's done) otherwise.
DE_GET = {"反", "必", "可", "就", "才", "能", "要", "已", "不", "未", "所", "便", "要", "得以", "也", "都", "又"}
OPENING = set("「『“‘（(《")
load_phrases_dict(PHRASES)

PUNCT = {"，": ",", "。": ".", "；": ";", "：": ":", "？": "?", "！": "!", "、": ",",
         "「": "“", "」": "”", "『": "‘", "』": "’", "（": "(", "）": ")"}
SENTENCE_END = set("。？！")


def is_han(ch):
    return "一" <= ch <= "鿿" or "㐀" <= ch <= "䶿"


def sandhi(syllables, chars):
    """不 bù → bú and 一 yī → yí / yì before the next syllable's tone, as spoken."""
    def tone(s):
        for c in unicodedata.normalize("NFD", s):
            if c in "̄́̌̀":
                return {"̄": 1, "́": 2, "̌": 3, "̀": 4}[c]
        return 5
    out = list(syllables)
    for i, ch in enumerate(chars[:-1]):
        nxt = tone(syllables[i + 1]) if i + 1 < len(syllables) else 5
        if ch == "不" and out[i] == "bù" and nxt == 4:
            out[i] = "bú"
        elif ch == "一" and out[i] == "yī" and not is_han_number(chars, i):
            out[i] = "yí" if nxt == 4 else "yì" if nxt in (1, 2, 3) else "yī"
    return out


def is_han_number(chars, i):
    numerals = set("〇一二三四五六七八九十百千万")
    return (i > 0 and chars[i - 1] in numerals | {"第"}) or (i + 1 < len(chars) and chars[i + 1] in numerals)


def hanzi_and_pinyin(text):
    """Hanzi with words separated by spaces (for word-by-word speech) and pinyin with one
    syllable per character, punctuation as ASCII and the first syllable of a sentence capitalized."""
    # Spaces in the source are word boundaries (the CUV's space before 神, for one).
    words = [w for chunk in text.split() for w in jieba.cut(chunk) if w.strip()]
    hanzi_out, pinyin_out = [], []
    capital = True
    pending = ""                                           # opening quotes wait for the next word
    for i, word in enumerate(words):
        if all(c in OPENING for c in word):
            pending += word
            pinyin_out.append("".join(PUNCT.get(c, c) for c in word))
            continue
        if all(not is_han(c) for c in word):
            mark = "".join(PUNCT.get(c, c) for c in word)
            if hanzi_out and all(c in PUNCT or not c.isalnum() for c in word):
                hanzi_out[-1] += word                      # punctuation sticks to the word before it
            else:
                hanzi_out.append(word)
            pinyin_out.append(mark)
            if any(c in SENTENCE_END for c in word):
                capital = True
            continue
        chars = [c for c in word if is_han(c)]
        if word == "得" and i > 0 and words[i - 1] in DE_GET:
            syllables = ["dé"]
        elif word == "为" and any("所" in w for w in words[i + 1:i + 3]):
            syllables = ["wéi"]                            # 为…所: the passive, “be … by”
        elif word in SINGLE:
            syllables = [SINGLE[word]]
        else:
            syllables = lazy_pinyin(word, style=Style.TONE, errors=lambda x: [c for c in x])
        syllables = sandhi(syllables, chars) if len(syllables) == len(chars) else syllables
        if capital and syllables:
            syllables[0] = syllables[0][:1].upper() + syllables[0][1:]
            capital = False
        hanzi_out.append(pending + word)
        pending = ""
        pinyin_out.extend(syllables)
    if pending:
        hanzi_out.append(pending)
    return " ".join(hanzi_out), " ".join(pinyin_out)


# ------------------------------------------------------------------------------------- pages
def cell(text):
    return (text or "").replace("|", "\\|").strip()


def number_pinyin(n):
    return str(n)


LABELS = {"web": "WEB", "kjv": "KJV", "asv": "ASV", "sblgnt": "SBLGNT", "tr": "TR", "byz": "Byz", "wlc": "WLC"}


def versions(value, table):
    """'web,kjv' → ['web', 'kjv']; 'none' → []."""
    names = [v.strip().lower() for v in value.split(",") if v.strip()]
    if names == ["none"]:
        return []
    for name in names:
        if name not in table:
            raise SystemExit(f"Unknown version “{name}”. Choose from: {', '.join(table)} (or none).")
    return names


def build_page(ref, args):
    """The page for one passage. Each verse is one row of a `table=verses` table:
    Hanzi | Pinyin | one column per version, named in the header (SBLGNT, WEB, KJV …).
    The app shows the Hanzi with its pinyin, then each version as a row of its own underneath,
    in column order: the Greek or Hebrew, then the English, then any other versions."""
    book, chapter, v1, v2 = ref
    en_name, zh_name, zh_py, _ = BOOKS[book - 1]
    is_nt = book >= NT_START
    zh = chinese_text(args.zh, book, chapter) if args.zh != "none" else {}
    if args.hanzi_file:
        zh.update(read_own_text(args.hanzi_file, chapter))

    columns = []          # (label, {verse: text}, source description)
    paragraphs = []
    for name in versions(args.en, EN):
        text, starts = english_text(name, book, chapter)
        if name == "web":
            paragraphs = starts
        columns.append((LABELS[name], text, EN[name]))
    if args.english_file:
        columns.insert(0, ("English", read_own_text(args.english_file, chapter),
                           f"English from {os.path.basename(args.english_file)}"))
    for name in (versions(args.greek, GREEK) if is_nt else versions(args.hebrew, HEBREW)):
        if name == "sblgnt":
            text = sblgnt(book, chapter)
        elif name == "wlc":
            text = {v: strip_cantillation(t) for v, t in scrollmapper("WLC", book, chapter).items()}
        else:
            text = scrollmapper({"tr": "TR", "byz": "Byz"}[name], book, chapter)
        source = GREEK[name] if is_nt else HEBREW[name] + ", without cantillation marks"
        columns.append((LABELS[name], text, source))

    # Order under the Hanzi: the original (Greek or Hebrew), then English, then any other versions.
    originals = [c for c in columns if c[0] in ("SBLGNT", "TR", "Byz", "WLC")]
    translations = [c for c in columns if c not in originals]
    columns = originals[:1] + translations[:1] + translations[1:] + originals[1:]

    verses = sorted(set(zh).union(*[set(c[1]) for c in columns]))
    if v1:
        verses = [v for v in verses if v1 <= v <= (v2 or v1)]
    if not verses:
        raise SystemExit(f"No verses found for {en_name} {chapter}.")

    span = "" if not v1 else f":{v1}" + (f"–{v2}" if v2 and v2 != v1 else "")
    span_zh = "" if not v1 else f"：{v1}" + (f"–{v2}" if v2 and v2 != v1 else "")
    title_zh = f"{zh_name} {chapter}{span_zh}"
    title_py = f"{zh_py} {chapter}" + (f" : {v1}" + (f"–{v2}" if v2 and v2 != v1 else "") if v1 else "")
    title_en = f"{en_name} {chapter}{span}"

    # Groups: the WEB's paragraphs, else runs of --group verses.
    starts = [v for v in paragraphs if v in verses] if args.group == 0 else []
    if not starts:
        starts = verses[::args.group or 5]
    if verses[0] not in starts:
        starts.insert(0, verses[0])
    groups, current = [], []
    for v in verses:
        if v in starts and current:
            groups.append(current)
            current = []
        current.append(v)
    groups.append(current)

    sources = []
    if args.zh != "none" and not args.hanzi_file:
        sources.append(ZH[args.zh][1])
    if args.hanzi_file:
        sources.append(f"Hanzi from {os.path.basename(args.hanzi_file)}")
    sources += [c[2] for c in columns]

    lines = ["<!-- reader: speak=word -->", "", f"# {title_zh} | {title_py} | {title_en}", "",
             "> " + " · ".join(sources), ""]
    header = "| " + " | ".join(["Hanzi", "Pinyin"] + [c[0] for c in columns]) + " |"
    rule = "|" + "---|" * (2 + len(columns))
    for group in groups:
        a, b = group[0], group[-1]
        nums = f"{a}" if a == b else f"{a}–{b}"
        lines += [f"## 第{nums}节 | Dì {nums} jié | {'Verse' if a == b else 'Verses'} {nums}", "",
                  "<!-- reader: table=verses -->", header, rule]
        for v in group:
            hz, py = hanzi_and_pinyin(zh[v]) if v in zh else ("", "")
            row = [f"{v} {hz}".strip(), f"{v} {py}".strip()] + [c[1].get(v, "") for c in columns]
            lines.append("| " + " | ".join(cell(c) for c in row) + " |")
        lines.append("")
    if any(c[0] == "SBLGNT" for c in columns):
        lines += ["> " + ATTRIBUTION["sblgnt"], ""]

    slug = re.sub(r"[^a-z0-9]+", "-", en_name.lower()).strip("-") + f"-{chapter}"
    if v1:
        slug += f"-{v1}" + (f"-{v2}" if v2 and v2 != v1 else "")
    return slug, title_zh, title_en, "\n".join(lines).rstrip() + "\n"


def add_to_index(index_path, page_path, title_zh, title_en):
    """Adds the page under “### 经文 Passages” in bible/README.md (made if missing)."""
    with open(index_path, encoding="utf-8") as f:
        text = f.read()
    rel = os.path.relpath(page_path, os.path.dirname(index_path))
    entry = f"- [{title_zh} · {title_en}]({rel})"
    if f"]({rel})" in text:
        return False
    heading = "### 经文 Passages"
    if heading not in text:
        text = text.rstrip() + f"\n\n{heading}\n\n{entry}\n"
    else:
        head, rest = text.split(heading, 1)
        block, sep, tail = rest.partition("\n### ")
        text = head + heading + block.rstrip() + "\n" + entry + "\n" + (("\n### " + tail) if sep else "")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("references", nargs="*", help='e.g. "Romans 12", "罗马书 12:1-8", "Psalm 23"')
    p.add_argument("--zh", default="cuv", choices=list(ZH) + ["none"])
    p.add_argument("--en", default="web", help="English versions, comma-separated: web,kjv,asv (or none)")
    p.add_argument("--greek", default="sblgnt", help="Greek versions for the New Testament: sblgnt,tr,byz (or none)")
    p.add_argument("--hebrew", default="wlc", help="Hebrew versions for the Old Testament: wlc (or none)")
    p.add_argument("--hanzi-file", help="your own Hanzi, one verse per line (“16 text”)")
    p.add_argument("--english-file", help="your own English, one verse per line")
    p.add_argument("--group", type=int, default=0,
                   help="verses per group (default: the WEB's paragraphs, else 5)")
    p.add_argument("--out", default="bible/passages", help="folder for the pages (default bible/passages)")
    p.add_argument("--add-to-index", action="store_true", help="list the pages in bible/README.md")
    p.add_argument("--stdout", action="store_true", help="print the page instead of writing it")
    p.add_argument("--versions", action="store_true", help="list the versions and stop")
    args = p.parse_args()

    if args.versions:
        for label, table in [("--zh", {k: v[1] for k, v in ZH.items()}), ("--en", EN), ("--greek", GREEK), ("--hebrew", HEBREW)]:
            print(label)
            for k, v in table.items():
                print(f"  {k:8} {v}")
        return
    if not args.references:
        p.error("give at least one reference, e.g. \"Romans 12\"")

    for text in args.references:
        ref = parse_reference(text)
        slug, title_zh, title_en, page = build_page(ref, args)
        if args.stdout:
            print(page)
            continue
        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, slug + ".md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"wrote {path}")
        if args.add_to_index:
            index = os.path.join(os.path.dirname(args.out.rstrip("/")) or ".", "README.md")
            if os.path.exists(index) and add_to_index(index, path, title_zh, title_en):
                print(f"  listed in {index}")


if __name__ == "__main__":
    main()

"""Builds the HSK 1 lesson pages from the lesson data, checking the vocabulary rules.

    python3 tools/hsk/build_course.py beginner/hsk1            write the pages
    python3 tools/hsk/build_course.py beginner/hsk1 --review x.csv  also write a review sheet

Rules checked for every sentence (word sections, grammar examples and dialogs):
  * every word is an HSK 1 word already taught (earlier lessons, or this lesson up to the word
    being taught), an extra word declared by this or an earlier lesson, or a cast name;
  * a word section's sentences all contain that word.
"""
import csv, importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hsk1_plan import PLAN, NOT_HSK1_OK, GOALS
from pypinyin import pinyin as _pinyin, Style

WORDS = json.load(open(os.path.join(HERE, "hsk1_words.json"), encoding="utf-8"))
NAMES = {"大明": "Dà míng", "小月": "Xiǎo yuè", "小明": "Xiǎo míng", "安娜": "Ān nà"}
NUMERALS = set("零一二三四五六七八九十百两")
# Readings that the word list gets wrong or that need the neutral tone / tone change.
OVERRIDE = {"都": "dōu", "那": "nà", "号": "hào", "哪里": "nǎ li", "这里": "zhè li", "那里": "nà li",
            "不客气": "bú kè qi", "星期天": "xīng qī tiān", "星期日": "xīng qī rì", "教会": "jiào huì",
            "喂": "wéi", "一下儿": "yí xià r", "一会儿": "yí huì r", "一点儿": "yì diǎn r", "一些": "yì xiē",
            "一起": "yì qǐ", "一样": "yí yàng", "一半": "yí bàn", "一边": "yì biān", "一块儿": "yí kuài r",
            "有一些": "yǒu yì xiē", "一百": "yì bǎi", "一百零五": "yì bǎi líng wǔ", "吗": "ma", "吧": "ba", "打": "dǎ", "地": "dì", "个": "gè", "过": "guo",
            "还": "hái", "几": "jǐ", "教": "jiāo", "看": "kàn", "累": "lèi", "跑": "pǎo", "上": "shàng",
            "说": "shuō", "听": "tīng", "页": "yè", "要": "yào", "着": "zhe", "正": "zhèng", "重": "zhòng",
            "行": "xíng", "差": "chà", "读": "dú", "干": "gàn", "东西": "dōng xi", "告诉": "gào su",
            "是不是": "shì bu shì", "子": "zi", "小朋友": "xiǎo péng you", "地方": "dì fang", "这边": "zhè bian",
            "西边": "xī bian", "不大": "bú dà", "不对": "bú duì", "不用": "bú yòng", "中国": "Zhōng guó",
            "北京": "Běi jīng", "汉语": "Hàn yǔ", "中文": "Zhōng wén", "汉字": "Hàn zì", "礼拜": "lǐ bài", "北边": "běi bian", "进来": "jìn lai", "进去": "jìn qu", "出来": "chū lai", "出去": "chū qu", "记住": "jì zhù", "关上": "guān shang"}
PUNCT = {"，": ",", "。": ".", "？": "?", "！": "!", "、": ",", "：": ":", "——": ""}
TONE4 = set("àèìòùǜ")
TONE_OF = {c: t for t, cs in enumerate(["āēīōūǖ", "áéíóúǘ", "ǎěǐǒǔǚ", "àèìòùǜ"], 1) for c in cs}
NUM_PY = {"零": "líng", "一": "yī", "二": "èr", "三": "sān", "四": "sì", "五": "wǔ", "六": "liù", "七": "qī",
          "八": "bā", "九": "jiǔ", "十": "shí", "百": "bǎi", "两": "liǎng"}


def _plain(p):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", p.lower()) if not unicodedata.combining(c)).replace(" ", "")


from glosses import GLOSS


def gloss(w):
    """English for an HSK word: our short learner gloss, else the meanings of the reading these
    lessons use, without surname senses."""
    if w in GLOSS: return GLOSS[w]
    entry = WORDS.get(w)
    if not entry: return ""
    want = OVERRIDE.get(w, entry["py"]).lower().replace(" ", "")
    forms = entry["forms"]
    best = next((f for f in forms if f["py"].lower().replace(" ", "") == want and f["en"]
                 and not all(m.lower().startswith("surname") for m in f["en"])), None)
    if best is None:
        best = next((f for f in forms if f["en"] and not all(m.lower().startswith("surname") for m in f["en"])), forms[0])
    means = [re.sub(r";? *also pr\. \[[^]]*\]", "", m).strip() for m in best["en"]
             if not m.lower().startswith("surname") and not m.lower().startswith("variant of")]
    return "; ".join(m for m in means[:3] if m)


def tone(syl):
    return next((TONE_OF[c] for c in syl if c in TONE_OF), 5)


class Course:
    def __init__(self):
        self.extras = {}            # word -> (pinyin, english, lesson)

    def word_py(self, w):
        if w in NAMES: return NAMES[w]
        if w in OVERRIDE: return OVERRIDE[w]
        if w in self.extras: return self.extras[w][0]
        if w in WORDS: return WORDS[w]["py"].lower()
        if w.endswith("们") and len(w) > 1: return self.word_py(w[:-1]) + " men"
        if w and all(c in NUMERALS for c in w): return " ".join(NUM_PY[c] for c in w)
        m = re.fullmatch(r"([零一二三四五六七八九十百两]+)([月号日点])", w)
        if m: return " ".join(NUM_PY[c] for c in m.group(1)) + " " + self.word_py(m.group(2))
        m = re.fullmatch(r"星期([一二三四五六])", w)
        if m: return "xīng qī " + NUM_PY[m.group(1)]
        return " ".join(x[0] for x in _pinyin(w, style=Style.TONE))

    def segment(self, text):
        """Greedy longest-match split of unspaced Chinese into known words (for titles)."""
        vocab = set(WORDS) | set(NAMES) | set(OVERRIDE) | set(self.extras)
        out, i = [], 0
        while i < len(text):
            for j in range(min(len(text), i + 4), i, -1):
                if text[i:j] in vocab or j == i + 1:
                    out.append(text[i:j]); i = j; break
        return " ".join(out)

    @staticmethod
    def tokens(sentence):
        out = []
        for tok in sentence.split():
            m = re.match(r"^(.*?)([，。？！、：—]*)$", tok)
            if m.group(1): out.append(("w", m.group(1)))
            for p in re.findall(r"——|[，。？！、：]", m.group(2)): out.append(("p", p))
        return out

    def sentence_py(self, sentence):
        toks = self.tokens(sentence)
        parts = []
        for k, (kind, t) in enumerate(toks):
            if kind == "p":
                parts.append(PUNCT[t]); continue
            p = self.word_py(t)
            nxt = toks[k + 1] if k + 1 < len(toks) else None
            prev = toks[k - 1] if k > 0 else None
            nxt_py = self.word_py(nxt[1]).split()[0] if nxt and nxt[0] == "w" else ""
            if t == "不" and nxt_py and tone(nxt_py) == 4:
                p = "bú"
            # 一 changes tone before another word, but stays yī in numbers, dates (一月, 一号,
            # 一日), days of the week (星期一) and ordinals (第一).
            if t == "一" and nxt and nxt[0] == "w" and nxt[1][0] not in NUMERALS \
                    and nxt[1] not in ("月", "号", "日", "楼") \
                    and not (prev and prev[0] == "w" and (prev[1][-1] in NUMERALS or prev[1] in ("星期", "第"))):
                p = "yí" if tone(nxt_py) == 4 else "yì"
            parts.append(p)
        out, cap = [], True
        for s in parts:
            if not s: continue
            if cap and s[0].isalpha():
                s = s[0].upper() + s[1:]; cap = False
            if s in (".", "?", "!"): cap = True
            out.append(s)
        return " ".join(out)

    def allowed(self, t, known):
        if t in known or t in NAMES or t in self.extras: return True
        if t.endswith("们") and "们" in known and self.allowed(t[:-1], known): return True
        if all(c in NUMERALS for c in t) and all(c in known for c in t): return True
        # dates and times written as one word: 十二月, 二十五号, 十月一日, 三点
        m = re.fullmatch(r"([零一二三四五六七八九十百两]+)([月号日点])", t)
        if m and all(c in known for c in m.group(1)) and m.group(2) in known: return True
        # 星期一 … 星期六
        m = re.fullmatch(r"星期([一二三四五六])", t)
        if m and "星期" in known and m.group(1) in known: return True
        return False

    def check(self, sentence, known, where, target=None):
        words = [t for kind, t in self.tokens(sentence) if kind == "w"]
        bad = [t for t in words if not self.allowed(t, known)]
        if bad:
            raise SystemExit(f"{where}: not taught yet: {bad}\n    “{sentence}”")
        def has(t):
            if t == target: return True
            if target not in t: return False
            return t.endswith("们") or all(c in NUMERALS for c in t) or bool(re.fullmatch(r"[零一二三四五六七八九十百两]+[月号日点]|星期[一二三四五六]", t))
        if target and not any(has(t) for t in words):
            raise SystemExit(f"{where}: sentence doesn't use “{target}”\n    “{sentence}”")


NUMBERS_ZH = "一二三四五六七八九十"


def lesson_number_zh(n):
    if n <= 10: return NUMBERS_ZH[n - 1]
    tens, ones = divmod(n, 10)
    return ("" if tens == 1 else NUMBERS_ZH[tens - 1]) + "十" + (NUMBERS_ZH[ones - 1] if ones else "")


def cell(s): return s.replace("|", "\\|")


def intro(out_dir, course, built):
    """00.md: what HSK 1 is, what the section sets out to do, how a lesson works, and the lessons."""
    total = sum(len(p[4].split()) for p in PLAN)
    L = ["<!-- reader: speak=word -->",
         "# HSK 1 介绍 | HSK yī jiè shào | About HSK 1", "",
         "> **Draft** — the lessons are not yet reviewed by a native speaker.", "",
         "## 目标 | Mù biāo | The goal", "",
         f"> HSK 1 is the first level of the HSK 3.0 standard (2021). This course teaches all **{total - len(NOT_HSK1_OK)} HSK 1 words** in "
         f"**{len(PLAN)} lessons** of about ten new words each, in an order that lets every sentence use only what you have already learned.",
         "",
         "> By the end you can talk simply about yourself, your family and friends; count, give your age and phone number; "
         "say dates and the time; say where people are and where they are going; eat, drink and shop; get around town; "
         "talk about the weather, health, work and school; and follow short everyday conversations at home, at church and in town.",
         "",
         "## 每课 | Měi kè | How each lesson works", "",
         "> **Goal and new words.** Each lesson starts with what it sets out to teach and its word list, with Hanzi, pinyin and English all shown.",
         "",
         "> **Sentences that build up.** Each new word then gets about ten sentences, from the word on its own to full sentences, using only words already taught. "
         "Only the Hanzi show: **tap** a word to see its pinyin and hear it, **double-tap** a line for its English.",
         "",
         "> **Grammar notes** explain the lesson's new patterns, with examples you can tap.",
         "",
         "> **Dialogs** close each lesson: short conversations that use everything learned so far.",
         "",
         "> **补充 Extra** words are not on the HSK 1 list but are needed for the settings, such as 教会 (church). They are marked wherever they appear.",
         "",
         "## 人物 | Rén wù | The people in the lessons", "",
         "<!-- reader: table=glossary -->", "| Hanzi | Pinyin | English |", "|---|---|---|",
         "| 大明 | Dà míng | Daming, the oldest child of the Wang family |",
         "| 小月 | Xiǎo yuè | Xiaoyue, his younger sister |",
         "| 小明 | Xiǎo míng | Xiaoming, their younger brother (seven years old) |",
         "| 爸爸 妈妈 | bà ba mā ma | their dad and mom |",
         "| 爷爷 奶奶 | yé ye nǎi nai | their grandpa and grandma |",
         "| 安娜 | Ān nà | Anna, a friend from church |",
         "",
         "## 课文 | Kè wén | The lessons", "",
         "<!-- reader: table=glossary -->", "| Hanzi | Pinyin | English |", "|---|---|---|"]
    for n, zh, en, setting, words in PLAN:
        num = lesson_number_zh(n)
        py = f"Dì {course.word_py(num)} kè : {course.sentence_py(course.segment(zh)).lower()}"
        status = "" if n <= built else " (coming)"
        L.append(f"| 第{num}课：{zh} | {py} | {en}{status} |")
    L.append("")
    open(os.path.join(out_dir, "00.md"), "w", encoding="utf-8").write("\n".join(L))


def build(out_dir, review_csv=None, upto=None):
    course = Course()
    known = set()
    os.makedirs(out_dir, exist_ok=True)
    pages, review = [], []
    for n, zh_title, en_title, setting, words in PLAN:
        if upto and n > upto: break
        try:
            mod = importlib.import_module(f"hsk1_l{((n - 1) // 5) * 5 + 1:02d}_{((n - 1) // 5) * 5 + 5:02d}")
        except ModuleNotFoundError:
            break
        data = getattr(mod, f"L{n:02d}", None)
        if data is None: break
        plan_words = words.split()
        if list(data["words"]) != plan_words:
            raise SystemExit(f"lesson {n}: words differ from the plan\n  plan: {plan_words}\n  data: {list(data['words'])}")
        for w, py, en in data["extra"]:
            course.extras.setdefault(w, (py, en, n))
        num = lesson_number_zh(n)
        title_zh = f"第{num}课：{zh_title}"
        title_py = f"Dì {course.word_py(num)} kè : {course.sentence_py(course.segment(zh_title)).lower()}"
        L = ["<!-- reader: speak=word -->",
             f"# {title_zh} | {title_py} | HSK 1 · Lesson {n}: {en_title}", "",
             "> **Draft** — not yet reviewed by a native speaker.", ""]
        if n in GOALS:
            L += [f"> **Goal:** {GOALS[n]}", ""]
        # vocabulary: an always-visible glossary (Hanzi, pinyin, English)
        L += [f"## 生词 | Shēng cí | New words ({len(plan_words)})", "",
              "<!-- reader: table=glossary -->", "| Hanzi | Pinyin | English |", "|---|---|---|"]
        for w in plan_words:
            g = gloss(w) if w in WORDS else dict((e[0], e[2]) for e in data["extra"]).get(w, "")
            mark = " · 补充 extra (not HSK 1)" if w in NOT_HSK1_OK else ""
            L.append(f"| {w} | {course.word_py(w)} | {cell(g)}{mark} |")
        L.append("")
        if data["extra"]:
            L += ["## 补充 | Bǔ chōng | Extra words (not in HSK 1)", "",
                  "> These words aren't on the HSK 1 list; they're here for the church and family settings.", "",
                  "<!-- reader: table=glossary -->", "| Hanzi | Pinyin | English |", "|---|---|---|"]
            for w, py, en in data["extra"]:
                L.append(f"| {w} | {py} | {cell(en)} |")
            L.append("")
        # words with their sentences
        for i, w in enumerate(plan_words, 1):
            known.add(w)
            wpy = course.word_py(w)
            L += [f"## 生词{i}：{w} | Shēng cí {i} : {wpy} | Word {i}: {wpy} — {cell(gloss(w))}", "",
                  "| Hanzi | Pinyin | English |", "|---|---|---|"]
            for zh, en in data["words"][w]:
                course.check(zh, known, f"lesson {n}, word {w}", target=w)
                py = course.sentence_py(zh)
                L.append(f"| {cell(zh)} | {py} | {cell(en)} |")
                review.append([n, f"Word {i}: {w}", zh.replace(" ", ""), py, en])
            L.append("")
        # grammar
        for key, title, notes, examples in data["grammar"]:
            kpy = course.sentence_py(course.segment(key))
            L += [f"## 语法：{key} | Yǔ fǎ : {kpy.lower()} | Grammar: {cell(title)}", ""]
            for note in notes:
                L += [f"> {note}", ""]
            L += ["| Hanzi | Pinyin | English |", "|---|---|---|"]
            for zh, en in examples:
                course.check(zh, known, f"lesson {n}, grammar {key}")
                py = course.sentence_py(zh)
                L.append(f"| {cell(zh)} | {py} | {cell(en)} |")
                review.append([n, f"Grammar: {title}", zh.replace(" ", ""), py, en])
            L.append("")
        # dialogs
        for d, (dtitle, lines) in enumerate(data["dialogs"], 1):
            dnum = NUMBERS_ZH[d - 1]
            L += [f"## 对话{dnum} | Duì huà {course.word_py(dnum)} | Dialog {d} · {cell(dtitle)}", "",
                  "| Hanzi | Pinyin | English |", "|---|---|---|"]
            for spk, zh, en in lines:
                course.check(zh, known, f"lesson {n}, dialog {d}")
                if not en: raise SystemExit(f"lesson {n}, dialog {d}: missing English for “{zh}”")
                py = course.sentence_py(zh)
                L.append(f"| {spk}：{cell(zh)} | {py} | {cell(en)} |")
                review.append([n, f"Dialog {d}: {dtitle}", f"{spk}：" + zh.replace(" ", ""), py, en])
            L.append("")
        fname = f"{n:02d}.md"
        open(os.path.join(out_dir, fname), "w", encoding="utf-8").write("\n".join(L))
        pages.append((n, title_zh, en_title, fname))
    intro(out_dir, course, built=len(pages))
    if review_csv:
        with open(review_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Lesson", "Part", "Hanzi", "Pinyin", "English", "Status", "Reviewer notes"])
            for r in review: w.writerow(r + ["To review", ""])
    return pages, len(review)


if __name__ == "__main__":
    out = sys.argv[1]
    review = sys.argv[sys.argv.index("--review") + 1] if "--review" in sys.argv else None
    pages, count = build(out, review)
    for p in pages: print(p)
    print(f"{len(pages)} lessons, {count} sentences checked")

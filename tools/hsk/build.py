import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from lessons import LESSONS, NAMES
from pypinyin import pinyin, Style

OUT = sys.argv[1] if __name__ == "__main__" else None
PY = {"不客气": "bú kè qi", "谢谢": "xiè xie", "朋友": "péng you", "名字": "míng zi", "什么": "shén me",
      "我们": "wǒ men", "你们": "nǐ men", "他们": "tā men", "没有": "méi yǒu", "再见": "zài jiàn",
      "的": "de", "吗": "ma", "呢": "ne", "个": "gè", "这": "zhè", "那": "nà", "一": "yī", "不": "bù"}
PY.update(NAMES)
PUNCT = {"，": ",", "。": ".", "？": "?", "！": "!", "——": "", "：": ":"}
TONE4 = set("àèìòùǜ")

def word_py(w):
    if w in PY: return PY[w]
    return " ".join(x[0] for x in pinyin(w, style=Style.TONE))

def split(sentence):
    """Words and punctuation, in order."""
    out = []
    for tok in sentence.split():
        m = re.match(r"^(.*?)([，。？！：—]*)$", tok)
        if m.group(1): out.append(("w", m.group(1)))
        for p in re.findall(r"——|[，。？！：]", m.group(2)): out.append(("p", p))
    return out

def sentence_py(sentence):
    toks = split(sentence)
    syls = []   # per word list of syllables
    for k, (kind, t) in enumerate(toks):
        if kind == "p":
            syls.append(PUNCT[t]); continue
        p = word_py(t)
        nxt = next((x for x in toks[k+1:]), None)
        nxt_py = word_py(nxt[1]).split()[0] if nxt and nxt[0] == "w" else ""
        if t == "不" and nxt_py and any(c in TONE4 for c in nxt_py): p = "bú"
        if t == "一" and nxt and nxt[0] == "w" and nxt[1] == "个": p = "yí"
        syls.append(p)
    out, cap = [], True
    for s in syls:
        if not s: continue
        if cap and s[0].isalpha(): s = s[0].upper() + s[1:]; cap = False
        if s in (".", "?", "!"): cap = True
        out.append(s)
    return " ".join(out)

def check(sentence, known, where):
    bad = [t for kind, t in split(sentence) if kind == "w" and t not in known and t not in NAMES]
    if bad: raise SystemExit(f"{where}: not yet learned: {bad} in “{sentence}”")

def cell(s): return s.replace("|", "\\|")

def main():
    known = set()
    os.makedirs(OUT, exist_ok=True)
    index = []
    for n, L in enumerate(LESSONS, 1):
        zh, en = L["title"]
        lines = ["<!-- reader: speak=word -->",
                 f"# {zh} | {sentence_py(' '.join(zh.replace('：', ' ： ').split()))} | HSK 1 · {en}", ""]
        for i, (w, gloss, sents) in enumerate(L["words"], 1):
            known.add(w)
            wpy = word_py(w)
            lines += [f"## 生词{i}：{w} | Shēng cí {i} : {wpy} | New word {i}: {wpy} — {gloss}", "",
                      "| Hanzi | Pinyin | English |", "|---|---|---|"]
            for zh_s, en_s in sents:
                check(zh_s, known, f"lesson {n} word {w}")
                lines.append(f"| {cell(zh_s)} | {sentence_py(zh_s)} | {cell(en_s)} |")
            lines.append("")
        numerals = "一二三四五六七八九十"
        for d, dialog in enumerate(L["dialogs"], 1):
            lines += [f"## 对话{numerals[d-1]} | Duì huà {['yī','èr','sān','sì','wǔ'][d-1]} | Dialog {d}", "",
                      "| Hanzi | Pinyin | English |", "|---|---|---|"]
            for spk, zh_s, en_s in dialog:
                check(zh_s, known, f"lesson {n} dialog {d}")
                lines.append(f"| {spk}：{cell(zh_s)} | {sentence_py(zh_s)} | {cell(en_s)} |")
            lines.append("")
        open(os.path.join(OUT, L["file"]), "w", encoding="utf-8").write("\n".join(lines))
        index.append((zh, L["file"], len(L["words"]), len(L["dialogs"])))
    print("ok", index, "words learned:", len(known))


if __name__ == "__main__":
    main()

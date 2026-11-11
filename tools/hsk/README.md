# HSK lessons: source and build

The HSK 1 lesson pages (`beginner/hsk1/01.md` …) are generated from the files here.

| File | What it holds |
|---|---|
| `hsk1_plan.py` | The course plan: all 506 HSK 1 words (2021 standard) in 51 lessons, in teaching order, with each lesson's title and setting (home, church, town) |
| `hsk1_l01_05.py`, `hsk1_l06_10.py`, … | The lessons: for each new word about ten sentences that build on each other, grammar notes with examples, and three dialogs; extra (non-HSK) words are declared per lesson |
| `glosses.py` | Short English glosses for the taught words |
| `hsk1_words.json` | The HSK 1 word list with every reading and meaning (from the HSK 3.0 data) |
| `build_course.py` | Checks the rules and writes the pages |

## Rules the build checks

Every sentence (in word sections, grammar examples and dialogs) may use only:
- HSK 1 words already taught — in an earlier lesson, or in this lesson up to the word being taught;
- extra words declared by this or an earlier lesson (shown on the page as **补充 Extra**);
- the cast's names (大明, 小月, 小明, 安娜).

Each word's sentences must contain that word, and every line needs an English translation. If a rule
is broken the build stops and prints the sentence. It also writes the pinyin, with the tone changes
of 不 and 一 (yí / yì; yī in numbers, dates and 星期一), and the neutral tones of the word list.

```bash
pip3 install pypinyin
python3 tools/hsk/build_course.py beginner/hsk1 --review hsk1-review.csv
```

`--review` also writes every sentence to a CSV for the native-speaker review sheet.

## Review

Every page starts with a **Draft** note until a native speaker has reviewed it. To mark a lesson
reviewed, remove that note (or ask Claude to) after fixing what the reviewer found.

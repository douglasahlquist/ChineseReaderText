# HSK lessons: source and build

The HSK lesson pages in `beginner/hsk1/` are generated from `lessons.py`.

- `lessons.py`: each lesson's new words, with three sentences per word, and its dialogs. Words inside a
  sentence are separated by spaces, so tapping speaks the whole word (`speak=word`). The cast's names
  (大明, 小月, 小明) are listed in `NAMES`.
- `build.py`: checks that every sentence uses only words already taught (in this lesson or an earlier
  one) plus the names, stops with the offending sentence if not, writes the pinyin (with the tone
  changes of 不 and 一), and writes the lesson pages.

```bash
pip3 install pypinyin
python3 tools/hsk/build.py beginner/hsk1
```

Then add any new page to README.md under `### HSK 1 · 第一级`.

# Format

## The list (README.md)

- Each `## Beginner`, `## Intermediate`, `## Advanced` or `## Music` heading starts a section in the app.
  Keep the space after `##` so GitHub shows it as a heading.
- Each `- [Title](folder/file.md)` line under a heading is one entry, shown in the order written.
  The path is relative to this repository's root and must end in `.md`.
- Lines inside `<!-- … -->` are ignored, which is handy for entries that aren't ready yet.
- Folder names: `beginner/`, `intermediate/`, `advanced/`, `music/`. A music piece may use its
  own subfolder, e.g. `music/001-short-name/README.md`.

## A lesson page

```markdown
# 第3课：我喜欢吃什么 | Dì 3 kè : wǒ xǐ huan chī shén me | Lesson 3: What I like to eat

## 第一组：日常聊天 | Dì yī zǔ : rì cháng liáo tiān | Group 1: Everyday chat

| Hanzi | Pinyin | English |
|---|---|---|
| A：你饿了吗？ | Nǐ è le ma ? | Are you hungry? |
```

- `#` is the page title; `##` starts a group (or a verse). Both take `Hanzi | Pinyin | English`;
  the pinyin and English parts are optional.
- Each table row is one line of text. A leading `A：` or `B：` is shown as the speaker.
- Pinyin: **one space-separated syllable per Hanzi character**. Punctuation in the pinyin is
  optional; each syllable is matched to the next non-punctuation character.
- A Latin word in the Hanzi, such as a name (`我爸爸叫David。`), counts as one unit: write it
  as-is in the pinyin (`Wǒ bà ba jiào David .`).
- Leave the English cell empty if there's no translation yet.
- An empty row, `| | | |`, ends an exchange (a question and its answer). The app spaces the
  lines inside an exchange closely and leaves a larger gap between exchanges; both gaps are
  set in Settings. Without empty rows, a new exchange starts each time the group's first
  speaker speaks again (A B | A B), so add them whenever an exchange has three or more lines.

## Page settings

Put this line at the top of a page to change how tapping sounds:

```markdown
<!-- reader: speak=word -->
```

- `speak=character` (the default): tapping speaks just that character.
- `speak=word`: tapping speaks the whole word the character belongs to. Words are separated
  by spaces in the Hanzi; a line with no spaces counts as one word (e.g. a book name).

GitHub hides the line, since it's an HTML comment.

## Sheet music (music pages)

A Markdown image on its own line shows a score (PNG, JPEG, HEIC, or every page of a PDF).
The path is relative to the page, as on GitHub:

```markdown
![Score](score.png)
```

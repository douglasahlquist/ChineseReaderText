# Format

## The list (README.md)

- Each `## Beginner`, `## Intermediate`, `## Advanced`, `## Characters` or `## Music` heading starts a section in the app.
  Keep the space after `##` so GitHub shows it as a heading.
- Each `- [Title](folder/file.md)` line under a heading is one entry, shown in the order written.
  The path is relative to this repository's root and must end in `.md`, except under
  `## Characters`, where entries point to character or word lists ending in `.json`.
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

## Character and word lists (characters/data)

Entries under `## Characters` open a list of characters or words instead of a lesson. Each list is
a JSON file; the app downloads it once and keeps a copy, like a lesson.

```json
{
  "kind": "characters",            // "characters" (single Hanzi), "words" or "radicals"
  "title": "Top 2000 Characters",
  "strokes": "characters/data/strokes.json",
  "items": [
    { "rank": 5, "simplified": "了", "traditional": ["了", "瞭"],
      "pinyin": ["le", "liǎo", "liào"], "english": "(completed action marker)",
      "meanings": [ { "pinyin": "le", "definitions": ["(completed action marker)"] } ] }
  ]
}
```

- `traditional` lists every traditional form, the usual one first (Taiwan standard).
- `pinyin` lists every reading, the most common first. A word has one, written as one word (`wǒmen`).
- Word lists may add `"hsk": "1"` … `"7–9"` (HSK 3.0 level) per item.
- The radicals list (`radicals.json`) uses the same fields: `rank` is the Kangxi number (1–214),
  `traditional` the Kangxi form and `simplified` its simplified form (the same when there is none).
  Each item adds `"radical"`: `strokes`, `forms` (shapes inside characters, such as 亻),
  `simplifiedForms`, `name` (such as 单人旁), `position` (`left`/`right` for 阝), `characters`
  (the top-2000 characters with this radical, most common first), `totalCharacters` (of about
  9,500 common characters) and `unicode`.
- `strokes.json` holds the stroke shapes for every character used in either list, simplified and
  traditional, keyed by character: `strokes` (SVG outlines, in writing order) and `medians`
  (the centre line of each stroke, used to animate it). Coordinates are 1024 × 1024 with y
  pointing up and the baseline at 900, from Make Me a Hanzi (Arphic Public License).
- The app links the lists: a word shows each of its characters with that character's rank,
  a character shows its radical and the common words that contain it, and a radical shows
  the characters that use it.

The other files in `characters/` (spreadsheets, the PDF and the web page) are for reading and
printing; the app uses only `characters/data/`.

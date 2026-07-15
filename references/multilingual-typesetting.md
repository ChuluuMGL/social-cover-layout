# Multilingual typesetting

This Skill currently validates a focused P0 language set: Simplified Chinese, Traditional Chinese, English, Japanese, and Korean. The goal is reliable social-cover typography without turning the Skill into a heavy internationalization engine.

## Input contract

Every multilingual brief should resolve these fields before generation:

```yaml
language: "zh-Hans"
locale: "zh-CN"
script: "Hans"
direction: "ltr"
text_mode: "controlled-typeset | model-rendered | hybrid"
font_preferences: []
break_policy: "locale-default"
```

If the language or script is unknown, return `manual-review` rather than guessing a font or line-break policy. Spanish, Russian, Arabic, and other non-P0 languages are currently out of the validated scope; they may be generated only with an explicit manual-review label.

## P0 regression profiles

| Language | Script | Break rule | Cover requirements |
| --- | --- | --- | --- |
| Simplified Chinese (`zh-Hans`) | Hans | Character-group breaks with CJK kinsoku punctuation rules | Do not start a line with closing punctuation or end a line with opening punctuation; keep short semantic groups intact. |
| Traditional Chinese (`zh-Hant`) | Hant | Same CJK kinsoku rules, checked with the selected font | Keep product names and key phrases together; do not let a single glyph drop below the shared baseline. |
| English (`en`) | Latn | Word boundaries and language-aware hyphenation | Do not split URLs, product names, abbreviations, emoji sequences, or numbers without an explicit rule. |
| Japanese (`ja`) | Jpan | Japanese kinsoku shori; preserve kana/kanji phrase groups | Avoid orphaned punctuation, small kana, prolonged sound marks, and closing brackets at line starts. |
| Korean (`ko`) | Kore | Prefer word-group breaks; keep syllable blocks intact | Increase line height and avoid forcing long compound nouns into narrow headline columns. |

All five current P0 profiles use `ltr`. The schema keeps `direction` for forward compatibility, but RTL or mixed-direction text is a manual-review case until a dedicated regression set is added.

## Text modes

- `controlled-typeset`: generate the visual layers, then place the exact title with a licensed font. Use this for spelling-critical titles, product names, and final production artwork.
- `hybrid`: use the image model for the scene and decorative labels, but typeset the primary title separately. This is the default for P0 social covers.
- `model-rendered`: allow the model to render only short, low-risk decorative text when the user accepts possible glyph errors; it is not evidence of exact-title support.

The final image must be checked after compositing. A prompt that asks for correct text is not evidence that the model rendered correct text.

## Font and fallback rules

- Select a font with complete glyph coverage for the requested P0 script before composing the title.
- Keep one primary display font and one fallback family; do not silently fall back to a symbol font or mixed-style glyphs.
- Check weight, outline, shadow, line-height, and baseline at the final thumbnail size. Technical glyph coverage alone is not enough.
- Record the font name, source, and license in the asset handoff. Font substitution is a manual-review trigger.

## P0 quality gate

Before delivery, render the title at full size and at a 25% phone-thumbnail preview. Confirm:

1. no wrong glyph, missing glyph, tofu box, reversed punctuation, or accidental transliteration;
2. no illegal line-start or line-end punctuation for the selected P0 script;
3. no broken word, phrase group, emoji sequence, URL, or product name;
4. sufficient line height, contrast, stable baseline, and safe-area clearance after outlines and shadows;
5. the selected `text_mode` and any manual review item are recorded.

Passing Chinese and English does not imply support for non-P0 scripts. Non-P0 output must remain explicitly marked `manual-review`.

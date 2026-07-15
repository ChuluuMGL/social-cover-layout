# Multilingual typesetting

The cover system is locale-aware, not just language-label-aware. A language input must change line breaking, direction, font coverage, title density, and safe-area behavior.

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

If `language` is not known, detect the script and return `manual-review` rather than guessing a font or direction.

## Text modes

- `controlled-typeset`: generate the background and visual layers, then place the exact title with a licensed, script-complete font. Default for Arabic, Hebrew, Indic, Thai, Lao, Khmer, and any title where spelling is critical.
- `model-rendered`: allow the image model to render short, low-risk text only when the user accepts possible glyph errors.
- `hybrid`: use the model for a small label or environmental text, but typeset the primary title separately. This is the default for Chinese, Japanese, Korean, and multilingual product names.

The final image must be checked after compositing. A prompt that asks for correct text is not evidence that the model rendered correct text.

## Script profiles

| Script family | Break rule | Direction | Layout requirements |
| --- | --- | --- | --- |
| Simplified/Traditional Chinese | Character-group breaks with CJK kinsoku punctuation rules | LTR | Do not start a line with closing punctuation or end a line with opening punctuation; keep 4–12 Han characters as a visual group when possible. |
| Japanese | Japanese kinsoku shori; preserve kana/kanji phrase groups | LTR | Avoid orphaned punctuation, small kana, prolonged sound marks, and closing brackets at line starts. |
| Korean | Prefer word-group breaks; keep syllable blocks intact | LTR | Increase line height and avoid forcing long compound nouns into narrow headline columns. |
| English and Latin-script languages | Word boundaries, language-aware hyphenation | LTR | Do not split URLs, product names, abbreviations, emoji sequences, or numbers without an explicit rule. |
| Arabic and Hebrew | Word/cluster-safe breaks with bidi isolation for embedded Latin | RTL | Mirror the reading hierarchy when appropriate, keep the primary title on the RTL-safe side, and never reverse an English product name accidentally. |
| Hindi, Bengali, and other Indic scripts | Grapheme-cluster and conjunct-safe breaks | LTR | Never split a consonant conjunct or detached mark; reserve more line height for stacked glyphs. |
| Thai, Lao, Khmer | Dictionary or grapheme-aware breaks | LTR | Never cut blindly after an arbitrary character; validate word boundaries and tone/diacritic marks. |
| Vietnamese and other diacritic-heavy Latin languages | Word boundaries with accent-safe rendering | LTR | Check that accents are not clipped by tight line boxes, outlines, or image-model artifacts. |

## Font and fallback rules

- Select a font with complete glyph coverage for the requested script before composing the title.
- Keep one primary display font and one fallback family; do not silently fall back to a symbol font or mixed-style glyphs.
- Check weight, outline, shadow, and line-height at the final thumbnail size. A font can technically contain a glyph and still be visually unusable in a bold cover.
- Record the font name, source, and license in the asset handoff. Font substitution is a manual-review trigger.

## Direction and safe area

- `direction: ltr` and `direction: rtl` affect title alignment, reading order, layer entry, and the side reserved for the person/product proof.
- Mixed-direction titles must isolate embedded English names, numbers, URLs, and punctuation before line breaking.
- For RTL covers, do not simply flip the finished LTR image. Recompose the title, evidence, and foreground overlap so the reading path remains intentional.
- For narrow wide cards, calculate safe areas after shaping the actual text; character count is not a reliable proxy for rendered width.

## Multilingual quality gate

Before delivery, render the title in the target locale at full size and at the platform thumbnail size. Confirm:

1. no wrong glyph, missing glyph, tofu box, reversed punctuation, or accidental transliteration;
2. no illegal line-start or line-end punctuation for the script;
3. no broken grapheme cluster, conjunct, diacritic, emoji sequence, URL, or product name;
4. correct text direction and mixed-script ordering;
5. sufficient line height, contrast, and safe-area clearance after outlines and shadows;
6. the chosen text mode is recorded in the output brief.

The minimum regression set for this Skill is: `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `ar`, `hi`, and `th`. Passing English and Chinese does not imply support for the other script families.

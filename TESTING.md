# Testing Matrix

## Deterministic package checks

```bash
npm run validate
```

The validator checks:

- `SKILL.md` frontmatter and required routing markers;
- the standalone metadata and MIT declaration;
- the three visual reference files;
- English and Simplified Chinese README sections;
- required release and publishing documents.
- `references/platform-specs.md` and its explicit source-status labels.
- `references/multilingual-typesetting.md` and the locale-aware metadata markers.

## Visual acceptance matrix

Each generated cover should be reviewed at full size and at a lightweight 25% phone-thumbnail preview.

| Dimension | Pass condition |
|---|---|
| Platform | The surface and ratio match the requested platform. |
| Title | The title is correct, readable, and limited to two visual groups. |
| Line breaks | Breaks follow meaning; no single character drops or floats. |
| Subject | Person, product, laptop, or type is the intended visual anchor. |
| Evidence | Product or workflow proof is visible without tiny UI copy. |
| Layering | Foreground, middle, and background roles are explainable. |
| Occlusion | Overlap creates depth while preserving the main title. |
| Color | Accent roles are deliberate and do not overpower the subject. |
| Rights | References, fonts, logos, screenshots, and people are authorized. |
| Extra text | No accidental slogans, watermarks, platform UI, or model artifacts. |

## Control-case protocol

When comparing routes or palettes, keep the following fixed:

1. the same content brief;
2. the same person or visual anchor;
3. the same title and ratio;
4. the same generation model and output size.

Change one visual variable at a time. A template-composited preview is not evidence of image-model performance and must be labeled separately from an independently generated cover.

## Cross-platform test case

See [`PLATFORM_TEST_REPORT.md`](./PLATFORM_TEST_REPORT.md) for the `Website Skill / 快速建站` test across Xiaohongshu, X, YouTube, WeChat, Instagram, LinkedIn, and TikTok. The rendered demo assets are published under [`demo/technical-platform-tests/`](./demo/technical-platform-tests/); the deterministic browser harness remains under `output/platform-tests/` and is intentionally ignored from the package.

## Multilingual regression matrix

This is a focused P0 text and layout acceptance matrix, not a claim that every language has already been image-model generated:

| Fixture | Required check |
|---|---|
| `zh-Hans` / `zh-Hant` | CJK kinsoku punctuation, semantic grouping, no single-glyph drop |
| `en` | word-boundary wrapping, product-name integrity, URL and number integrity |
| `ja` / `ko` | phrase grouping, punctuation, line height, dense headline safety |
| Non-P0 (`es`, `ru`, `ar`, and others) | no current regression claim; route to explicit `manual-review` |

All five P0 languages use `controlled-typeset` or `hybrid` for production titles. Passing one P0 language does not imply support for the other four, and non-P0 output must not be described as validated support.

## Canvas-family smoke check

Run one representative composition per family rather than every platform × template combination:

| Family | Representative ratios | Check |
|---|---|---|
| `vertical` | 3:4 or 9:16 | title remains dominant and central-safe |
| `wide` | 16:9 | title stays short and evidence remains visible at a glance |
| `square` | 1:1 | title and evidence form two stable blocks without corner clutter |

These are composition checks, not additional visual templates.

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

## Visual acceptance matrix

Each generated cover should be reviewed at full size and at phone-thumbnail size.

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

See [`PLATFORM_TEST_REPORT.md`](./PLATFORM_TEST_REPORT.md) for the `Website Skill / 快速建站` test across Xiaohongshu, X, YouTube, WeChat, Instagram, LinkedIn, and TikTok. The local PNGs and deterministic browser harness are kept under `output/platform-tests/` and are intentionally ignored from the package.

# Changelog

## Unreleased

- Renamed the public Skill and repository identity from `content-cover-router` to `social-cover-layout`.
- Kept `content-cover-router` as a legacy/internal compatibility name in the documentation and metadata.

## 0.2.1 — 2026-07-15

- Narrowed the validated language regression set to the five P0 languages: Simplified Chinese, Traditional Chinese, English, Japanese, and Korean.
- Marked Spanish, Russian, Arabic, and other non-P0 languages as explicit `manual-review` cases instead of implying tested support.
- Added the lightweight `vertical`, `wide`, and `square` canvas families as composition constraints shared by all platform routes.
- Kept thumbnail QA as a 25% manual readability check; no OCR, CTR prediction, or heavy rendering dependency was added.

## 0.2.0 — 2026-07-15

- Added locale-aware multilingual typesetting profiles for CJK, Latin, RTL, Indic, Thai/Lao/Khmer, and diacritic-heavy scripts.
- Added `controlled-typeset`, `model-rendered`, and `hybrid` text modes.
- Added script direction, font coverage, grapheme safety, and multilingual thumbnail checks to the quality gate.
- Split platform surfaces for YouTube Shorts, WeChat article/share cards, and LinkedIn image ads.
- Added explicit Bilibili video-cover and multilingual handoff metadata.

## 0.1.0 — 2026-07-15

- Initial standalone release of `social-cover-layout`.
- Added the unified `adaptive-composite` route system.
- Added platform routing for Xiaohongshu, X/Twitter, YouTube, WeChat, and other surfaces.
- Added semantic title grouping, keyword color roles, layer-depth rules, and quality gates.
- Added English and Simplified Chinese repository documentation.
- Added originality, asset-rights, and publishing boundaries.

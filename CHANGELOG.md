# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions track the
`version` field in `skill.json`.

## [Unreleased]

### Added

- `.github/workflows/validate.yml`: CI runs `scripts/validate_skill.py` and the version consistency check.
- `.github/workflows/tag-on-bump.yml`: creates the `v<x.y.z>` tag and GitHub release automatically when `skill.json` is bumped on `main`.
- `scripts/check_release_consistency.py`: stdlib-only check that `skill.json`, `package.json`, README badges, and this changelog agree on the version.

## [0.2.4] - 2026-07-15

- Promoted the five independent multilingual cover images to the repository homepage and Demo Gallery first view.
- Removed the old palette sheet from the primary Demo position; it remains archived as a historical comparison.
- Added direct visual links so the updated Demo is visible without opening a nested folder.

## [0.2.3] - 2026-07-15

- Replaced the multilingual card-sheet specimen with five independent cover images.
- Kept the proven Chinese cover composition while using distinct blue, yellow, purple, and green language variants.
- Clarified that multilingual demos are cover outputs, not typography charts or palette sheets.

## [0.2.2] - 2026-07-15

- Added a platform demo gallery for X, WeChat Official Account, YouTube, and Bilibili outputs.
- Added a P0 multilingual typography gallery for Simplified Chinese, Traditional Chinese, English, Japanese, and Korean.
- Separated generated platform demos from controlled-typeset language QA specimens so the evidence type is clear.
- Used varied accent colors across the cases without turning the gallery into a palette-only showcase.

## [0.2.1] - 2026-07-15

- Narrowed the validated language regression set to the five P0 languages: Simplified Chinese, Traditional Chinese, English, Japanese, and Korean.
- Marked Spanish, Russian, Arabic, and other non-P0 languages as explicit `manual-review` cases instead of implying tested support.
- Added the lightweight `vertical`, `wide`, and `square` canvas families as composition constraints shared by all platform routes.
- Kept thumbnail QA as a 25% manual readability check; no OCR, CTR prediction, or heavy rendering dependency was added.

## [0.2.0] - 2026-07-15

- Added locale-aware multilingual typesetting profiles for CJK, Latin, RTL, Indic, Thai/Lao/Khmer, and diacritic-heavy scripts.
- Added `controlled-typeset`, `model-rendered`, and `hybrid` text modes.
- Added script direction, font coverage, grapheme safety, and multilingual thumbnail checks to the quality gate.
- Split platform surfaces for YouTube Shorts, WeChat article/share cards, and LinkedIn image ads.
- Added explicit Bilibili video-cover and multilingual handoff metadata.

Also includes changes made on top of 0.1.0 before this version bump:

- Renamed the public Skill and repository identity from `content-cover-router` to `social-cover-layout`.
- Kept `content-cover-router` as a legacy/internal compatibility name in the documentation and metadata.
- Added cross-platform cover specifications (`references/platform-specs.md`) and `PLATFORM_TEST_REPORT.md`.
- Published the generated cover demo gallery and platform demos for X, WeChat Official Account, YouTube, and Bilibili.

## [0.1.0] - 2026-07-15

- Initial standalone release of `social-cover-layout`.
- Added the unified `adaptive-composite` route system.
- Added platform routing for Xiaohongshu, X/Twitter, YouTube, WeChat, and other surfaces.
- Added semantic title grouping, keyword color roles, layer-depth rules, and quality gates.
- Added English and Simplified Chinese repository documentation.
- Added originality, asset-rights, and publishing boundaries.

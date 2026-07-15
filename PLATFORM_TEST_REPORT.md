# Cross-platform cover test report

Test case: `Website Skill / 快速建站`

The same synthetic person, scene, title, color system, and proof label were held constant. Only the platform canvas, crop, title scale, and safe-area route changed. This is a deterministic layout/safe-area test; it is not being presented as seven independent image-model generations.

## Results

| Platform surface | Output | Route | Result | Finding |
| --- | --- | --- | --- | --- |
| Xiaohongshu note cover | `demo/platform-tests/xiaohongshu-3x4-1080x1440.png` | `bridge-hybrid` + `person-over-type` | pass | The vertical title block remains the strongest first-screen hook; face and laptop stay visible. |
| X organic post image | `demo/platform-tests/x-organic-16x9-1200x675.png` | `proof-first` + `type-over-object` | pass | Horizontal crop needs a shorter text block; the proof label can sit in the lower-right without becoming UI-like. |
| YouTube thumbnail | `demo/platform-tests/youtube-16x9-1280x720.png` | `headline-first` + `person-over-type` | pass | The title is readable at thumbnail scale; the subject is larger and the subtitle is kept small. |
| WeChat share card | `demo/platform-tests/wechat-share-21x9-900x383.png` | `proof-first` + `split-layer` | pass with manual review | The narrow band works only after recomposition. This ratio is a working default, not a universal official rule. |
| Instagram feed post | `demo/platform-tests/instagram-feed-4x5-1080x1350.png` | `bridge-hybrid` + `person-over-type` | pass | Similar to XHS in shape, but the title is kept more centered for feed cropping. |
| LinkedIn website share card | `demo/platform-tests/linkedin-share-191x1-1200x627.png` | `proof-first` + `type-over-object` | pass | A restrained horizontal proof card is more appropriate than a dense XHS title stack. |
| TikTok video cover | `demo/platform-tests/tiktok-video-9x16-1080x1920.png` | `headline-first` + `person-over-type` | pass with manual review | Central safe area is usable; the bottom 18% must remain clear for video UI and caption overlays. |

## What this changes in the Skill

- Platform is no longer enough input; `surface` is required for reliable routing.
- A 3:4 XHS cover is not treated as a universal source image. Wide cards and video-like vertical surfaces are recomposed.
- X organic images and X ads use different supported ratios and must not share an automatic default.
- Instagram 4:5 and TikTok 9:16 are now explicit routes instead of falling into `other`.
- WeChat and Xiaohongshu defaults carry a `working-default` label until a stable first-party note/share-card spec is available for the exact surface.

## Visual review conclusion

The platform routes are usable, but the next image-model test should be done separately from this deterministic layout test. The current result proves that the new platform matrix can preserve title hierarchy and safe areas; it does not prove that an image model will render Chinese type correctly. For production, generate the image background and typeset the final Chinese title as a controlled overlay when exact text is required.

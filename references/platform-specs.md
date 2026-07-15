# Platform specifications

This matrix separates published technical constraints, the platform surface being designed for, and the practical layout default used by this Skill.

The `source_status` values are explicit:

- `verified-official`: checked against a current first-party help or business page;
- `surface-dependent`: the platform publishes different rules for different surfaces;
- `working-default`: a practical default where a stable public note-cover rule was not found.

## Matrix

| Platform | Surface | Ratio | Recommended canvas | Source status | Layout profile |
| --- | --- | --- | --- | --- | --- |
| Xiaohongshu | note cover | 3:4 | 1080×1440 | working-default | `headline-first`, short Chinese title, strong first-screen subject |
| X/Twitter | organic post image | 16:9 or 1:1 | 1200×675 or 1200×1200 | verified-official | one-second comprehension, no X UI |
| X/Twitter | image ad | 1.91:1, 1:1, 4:5, 2:3, 16:9, 9:16 | 1200×628, 1200×1200, 1440×1800, 1080×1620, 1920×1080, 1080×1920 | verified-official | choose one ad placement before composing |
| YouTube | video thumbnail | 16:9 | 3840×2160; 1280×720 fallback | verified-official | very short title, largest subject, high contrast |
| WeChat | article/share card | about 21:9 or 1:1 | 900×383 or 900×900 | working-default | recompose into a narrow band or square; never stretch XHS |
| Instagram | feed post | 1.91:1–3:4 | 1080×1350 default | verified-official | keep text inside feed-safe center; 4:5 is the practical default |
| Instagram | Reel cover | 9:16 | 1080×1920 | verified-official | center-safe title because profile/grid crops can differ |
| LinkedIn | website share card | 1.91:1 | 1200×627 | verified-official | proof-first, restrained title, product/screenshot evidence |
| LinkedIn | article cover | 10:3 | 2000×600 | verified-official | editorial header, very wide safe band |
| TikTok | video cover / vertical image creative | 9:16 | 1080×1920; 720×1280 fallback | surface-dependent | title in the central safe area; avoid bottom UI zone |

## Source notes

- **X/Twitter organic post:** X Help says a single photo with a standard aspect ratio between 2:1 and 3:4 displays in full. X ad specifications are a separate surface and support more placements, so the Skill must not reuse ad dimensions for an organic post automatically.
- **YouTube:** the current YouTube Help page recommends 3840×2160 and 16:9, with a minimum width of 640. The 1280×720 version remains a useful lower-cost fallback when an image model or export pipeline cannot produce 4K.
- **Instagram:** Meta documents a width up to 1080 and a supported range from 1.91:1 to 3:4 for feed images. Reels promotion is a separate full-screen 9:16 surface.
- **LinkedIn:** LinkedIn documents 1200×627 for website sharing previews and 2000×600 as the optimal article-cover size. Ads have additional square and 4:5 variants.
- **TikTok:** TikTok's current image-ad documentation includes 720×1280 vertical creatives; the organic product is primarily video-first, so this Skill treats 9:16 as a video-cover default rather than claiming a universal static-post rule.
- **Xiaohongshu and WeChat:** no stable public first-party note-cover/share-card specification was verified for this test. The defaults above are intentionally labeled `working-default`; re-check the current uploader or campaign surface before publishing. Xiaohongshu's public open-platform product-image documentation does show 1:1 and 3:4 image variants, but that is not the same as a universal note-cover guarantee.

## Safe-area rules used in tests

- Keep the primary title inside the central 80% of width unless a platform-specific profile says otherwise.
- For 9:16 video-like surfaces, keep title and face/product proof away from the bottom 18% and top 10%.
- For wide cards, use one horizontal reading band and do not stack an XHS-style vertical title block into the crop.
- For every platform, test the image at a small preview size before delivery. Technical compliance does not guarantee thumbnail readability.

## First-party references

- X Help: https://help.x.com/en/using-x/posting-gifs-and-pictures
- X Business creative specifications: https://business.x.com/en/help/campaign-setup/creative-ad-specifications
- YouTube custom thumbnails: https://support.google.com/youtube/answer/72431?hl=en
- Instagram image resolution: https://www.facebook.com/help/1631821640426723
- LinkedIn website sharing: https://www.linkedin.com/help/linkedin/answer/a521928/making-your-website-shareable-on-linkedin?lang=en
- LinkedIn single-image ads: https://www.linkedin.com/help/lms/answer/a426534
- Xiaohongshu open-platform product images: https://school.xiaohongshu.com/en/open/product/create-spl.html
- TikTok image and carousel ad playbook: https://ads.tiktok.com/business/library/Image_Ads_Carousel_Ads_Playbook.pdf

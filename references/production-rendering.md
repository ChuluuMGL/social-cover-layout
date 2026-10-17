# Accurate title workflow: 16:9 and 3:4

This is an executable local path for hybrid covers. Image generation still uses the host's existing tool; this repository contains no model keys or image API client. The optional helper typesets approved LTR title lines onto a text-free image. Other ratios, RTL shaping, and full editorial automation are outside this helper's tested scope.

## 1. Choose the available path

| Host capability | Delivery |
| --- | --- |
| Image tool + local Python/font access | Generate text-free art, typeset locally, inspect final image and thumbnail |
| Image tool only | Use model-rendered text or hand the exact title to an external typesetter; mark unresolved checks explicitly |
| No image tool | Return the complete image prompt, references and layout brief, clearly marked not generated |

Source code is MIT. Image generation may consume the user's plan or API credits. Local rendering does not call a model or upload files. Keep reference images and output outside public commits unless separately authorized.

## 2. Set up the local renderer

Run from this Skill's root using Python 3.10+:

~~~bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-render.txt
~~~

Windows uses .venv\Scripts\python.exe instead. Use the same interpreter for installation and rendering. Fonts are not bundled or downloaded automatically. Pick a locally licensed .ttf/.otf/.ttc with complete glyph coverage; record the source and license in the command.

On macOS, one working Simplified Chinese system-font example is /System/Library/Fonts/STHeiti Medium.ttc (face index 1, Heiti SC). Check that it exists on the user's Mac. On Ubuntu with fonts-noto-cjk installed, a candidate is /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc (SC face index 2). A different font/collection face must pass the glyph check; inspect the family/style recorded in the QA JSON and do not silently substitute an English-only default font.

## 3. Generate a text-free background

Keep the same authorized visual subject and brand brief. Request each ratio independently, saving the art and prompt:

- 16:9: keep the left 60% quiet silver/white, reserve x=10–58% and y=16–58% for dark title and badge. Place the person/product in the right side, keeping important facial and product details within safe margins. A small batch of video/product frames can sit below the title area.
- 3:4: keep the top 42% quiet silver/white for the title and badge; place the person/product in the lower portion with clear breathing room. Recompose instead of cropping the wide image.
- In both: no letters, numbers, labels, logos, fake UI, watermarks or tiny packaging text. Explain that this is a background layer and the exact title will be typeset afterward.

Inspect the actual generated art. If text or an obstructed subject remains, correct that specific problem using the available image-editing tool within the user's call/fee limit. A local typesetter cannot clean hallucinated background text.

The helper contains the entire background without cropping it, then exports the exact target canvas. A slightly wrong source ratio can introduce a thin neutral band. A substantially wrong composition needs another background, not a claim that resizing fixed it.

## 4. Typeset the approved title

Example macOS command after saving the wide background to output/wide-bg.png:

~~~bash
.venv/bin/python scripts/render_cover.py \
  --background output/wide-bg.png \
  --ratio 16:9 \
  --line "批量做电商视频" \
  --line "审核到结果回传" \
  --badge "免费开源" \
  --accent-word "批量" \
  --font "/System/Library/Fonts/STHeiti Medium.ttc" \
  --font-index 1 \
  --font-source "local macOS system font" \
  --font-license "macOS system font; not redistributed" \
  --output output/wide-v1.png
~~~

For the vertical image, repeat with a separately generated output/vertical-bg.png, ratio 3:4 and a new output/vertical-v1.png. Keep the same approved title, font and color roles. The title is never shortened, translated or ellipsized. Supply one or two explicit semantic lines; include a badge only if the brief provides that secondary text, otherwise omit the badge argument. If the text cannot fit legibly, the helper stops so the title can be revised by the author.

Outputs:

| File | Meaning |
| --- | --- |
| wide-v1.png | Exact 1536×864 wide canvas; vertical is 1152×1536 |
| wide-v1.thumb.png | 25% preview of the final exported image |
| wide-v1.qa.json | Actual size, hashes, font face/source/license, exact text, layer bounds, and outstanding visual review |

The helper refuses existing output names and sidecars. Use v2 for a revision. It verifies saved image and thumbnail dimensions, required glyphs and text bounds inside the central 80% width. It does not copy a font into the result.

For an offline installation/typography smoke test, replace the background argument with:

~~~text
--solid-background "#edf1f2"
~~~

This is a controlled-typeset test fixture, not image-model output or a finished creative demo.

## 5. Read back and finish QA

1. Open the final PNG and its thumbnail. Read the title literally; inspect the face/hands/product, contrast, composition and absence of stray background text.
2. Read the JSON's actual size and bounds. The helper's checks cover its own text layers; the image model's subject placement is still a visual check.
3. Fix identified problems with a new version and record the count. Font glyph errors, overflowing text or unsafe bounds stop rendering; background errors require an art correction.
4. Leave the result manual-review until it has been viewed. Mark a known unresolved issue revise. Record pass separately only after all applicable visual checks succeed.

Runtime limits remain visible: exact typography does not guarantee attractiveness, an exact ratio does not guarantee every platform crop, and one working example does not establish CTR or time savings.

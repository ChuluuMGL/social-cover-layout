# Social Cover Layout Quality Gate

## P0 必须通过

- 平台比例和交付 surface 正确。
- `layout_family` 与比例匹配（`vertical`、`wide` 或 `square`）。
- 在约 25% 手机缩略图预览中，主标题和视觉主体仍可识别，无错字、乱码或未要求的额外文字。
- 标题、人物脸、产品主体和关键证据都在安全区内。
- 无人物时，产品/截图/字体确实承担了视觉主体，不出现无意义的默认人物。
- 不包含未经授权的真人、Logo、截图、字体、水印或第三方品牌。
- 标题字形共享稳定基线；没有因为模型生成而出现单字下坠、漂浮或无意断行。
- 目标语言的字形、方向、断句和字体覆盖正确；没有缺字框、反向标点、被拆开的组合字或错误的混合方向。

## P1 优先修复

- 主标题、主体、证据的阅读顺序明确。
- 主视觉文字组不超过两组；小字不超过必要的辅助信息。
- 颜色角色不超过四种，装饰不抢主体。
- 同一案例的不同路线保持标题语义和视觉主体一致，只改变版式语言。
- 层叠关系可解释：能看出谁在前景、谁在中景、谁在背景；遮挡不超过主标题字形的 12%。
- 关键词的换行和变色服务于阅读顺序，而不是装饰性随机变化。
- 复杂文字、RTL 文字或必须零错字的标题已经记录 `text_mode`，并经过最终合成图复核。
- 缩略图检查保留为轻量人工门槛，不把 OCR、CTR 预测或重型渲染引擎作为当前版本依赖。

## 输出记录

每个成品记录：

```yaml
case: ""
platform: ""
surface: ""
ratio: ""
layout_family: "vertical | wide | square"
route: ""
title: ""
language: ""
locale: ""
script: ""
direction: "ltr | rtl"
text_mode: "controlled-typeset | model-rendered | hybrid"
break_policy: ""
references: []
prompt_path: ""
image_path: ""
qa_status: "pass | revise | manual-review"
thumbnail_check: "pass | manual-review"
preview_scale: "25%"
manual_review: []
```

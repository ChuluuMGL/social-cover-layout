---
name: social-cover-layout
description: "把完成的内容 brief 变成适配小红书、X/Twitter、YouTube、微信及其他媒体表面的原创社交封面方案或生成封面。根据内容目的、平台比例、视觉主体和素材授权选择可质检的排版、配色和层叠路线。"
---

# Social Cover Layout

这是 content-creation-workflow 的可选封面模块。它接收已经完成的内容 brief，负责平台路由、视觉系统选择、提示词组织和图片质检；不负责写正文，也不负责登录、上传或发布。

## 设计边界

- 只借鉴通用设计方法：短标题、单一视觉主体、强对比、人物或产品证据、平台比例和安全区。
- 不复制任何第三方 Skill 的原文、文件结构、品牌名称、示例图片、人物头像或单张封面构图。
- 人像不是必需素材。没有人像时，网站截图、产品界面、电脑、手部操作、数字或字体可以成为视觉主体。
- 参考创作者时提炼视觉语言，不复制头像、水印、Logo、文案或具体构图。
- 生成图片和已发布是两件事；默认只返回生成结果和人工发布清单。

## 调用方式

可以直接调用：

```text
使用 $social-cover-layout，把这篇小红书笔记做成封面
```

也可以由 `$content-creation-workflow` 在用户明确要求配图时传入 handoff brief。

必须接收或推断：

```yaml
topic: ""
purpose: "click | save | tutorial | proof | series-recognition"
selected_title: ""
hook: ""
visual_anchor: "person | screenshot | product | laptop | hand | typography | scene"
language: ""
locale: ""
script: ""
direction: "ltr | rtl | auto"
text_mode: "controlled-typeset | model-rendered | hybrid"
font_preferences: []
break_policy: "locale-default"
platform: "xiaohongshu | x | youtube | wechat | bilibili | instagram | linkedin | tiktok | other"
surface: "note-cover | post-image | thumbnail | shorts-frame | video-cover | reel-cover | article-cover | share-card | profile-cover | image-ad"
ratio: ""
person_reference: []
asset_references: []
brand_rules: ""
generation_mode: "prompt-only | generate"
```

## 路由顺序

### 1. 先判断内容，而不是先选颜色

- 工具发布、教程、效率方法：结果承诺 + 产品/界面证据。
- 测评、对比、案例：前后或证据对照。
- 观点、品牌故事、生活方式：照片或场景主导。
- 排版、字体、设计教程：文字或数字成为主视觉。

### 2. 再判断平台表面和规格

- 先读取 `references/platform-specs.md`，同时确认 `platform` 和 `surface`；同一平台的 organic、广告、缩略图和文章封面不能混用规格。
- 小红书首图：默认 3:4，优先首屏停留和收藏；默认一个主标题、一个主体，不塞正文小字。该比例在本 Skill 中标为工作默认值，发布前以当前上传器为准。
- X/Twitter organic 帖子图：优先 16:9 或 1:1，一秒理解和转发；不画入 X 的界面按钮。X 广告另走广告比例，不自动复用帖子图。
- YouTube thumbnail：16:9，标题更短、主体更大、对比更强；不画播放条或平台 UI。
- YouTube Shorts：只输出 9:16 可选视频帧，不承诺可以上传自定义 Shorts 缩略图。
- Bilibili 视频封面：默认 16:9；保留底部元数据安全带，并避开右上角重要信息；不能把 YouTube 封面直接换 Logo。
- 微信公众号文章封面：按约 21:9 重新构图；微信公众号分享卡：按 1:1 重新构图；两者都不能把小红书图拉伸过去，比例在本 Skill 中标为工作默认值。
- Instagram feed：默认 4:5；Reel cover 走 9:16，并把标题和主体放在中间安全区以应对个人主页裁切。
- LinkedIn 分享卡：默认 1.91:1；文章封面走超宽版，标题减少、证据优先。
- LinkedIn 广告：先确认 1.91:1、1:1 或 4:5 placement，再选择画布；不能把分享卡默认当广告图。
- TikTok：视频封面/竖版素材默认 9:16；它是视频优先平台，不能把静态图广告规格当成统一的普通帖子规则。

### 3. 进入统一的 adaptive-composite 系统

本 Skill 只有一个统一的 `adaptive-composite` 系统，不要求用户在两个 Skill 之间选择。它把“标题优先”和“证据优先”合并成同一张有前后层级的封面：

- `headline-first`：标题是第一阅读对象，适合人物教程、经验和强钩子；根据语义拆行，并用关键词变色建立阅读入口。
- `proof-first`：产品、网站截图或电脑是主要证据，适合工具发布；标题与产品形成前后关系，而不是把产品缩成背景。
- `bridge-hybrid`：人物承担情绪和点击，产品承担可信度，标题拆成语义组；这是 Website Skill、内容创作 Skill 等工具主题的默认策略。

三者不是三个 Skill，而是同一 Skill 的内部决策。根据标题长度、内容目的、视觉主体和平台自动决定。

统一系统还会选择一个层叠动作：`person-over-type`、`type-over-object` 或 `split-layer`。具体规则见 `references/visual-routes.md`。

`adaptive-composite` 可以从 `references/color-system.md` 选择亮色、柔和色或双色组合。颜色由内容情绪、背景明度和品牌规则决定，不固定使用黄色。

## 多语言排版

`language` 不是装饰性字段。必须同时解析 `locale`、`script`、`direction`、`text_mode` 和 `break_policy`，再决定标题分组、行高、对齐、字体和层叠方向。中文、日文、韩文、阿拉伯文、希伯来文、印地语、泰文等不能共用英文的简单按空格断行规则。

- 默认读取 `references/multilingual-typesetting.md` 的脚本规则。
- 复杂文字、RTL 文字、品牌名或必须零错字的主标题，默认使用 `controlled-typeset` 或 `hybrid`，不要把最终文字完全交给图片模型。
- RTL 和混合方向标题必须重新构图，不能把 LTR 成品水平翻转。
- 没有脚本完整的字体、断句策略或实际缩略图复核时，输出 `manual-review`，不声称“支持该语言”。

## 人像规则

- 有用户本人照片：保留性别呈现、脸型、发型、五官和气质；不能把参考创作者的脸放进新图。
- 只有普通人像：默认自然半身或胸像，不自动变成大头 Q 版。
- 没有人像：在 `adaptive-composite` 内把产品、界面、电脑、手部、数字或字体设为视觉主体，不因为缺人像而停止生成。
- 需要手部/局部出镜时，明确写清素材只作为局部动作参考，不生成额外人物脸。
- 使用真实人物、Logo、产品截图或字体前，保留授权和来源记录。

## 标题规则

- 先从正文提炼一个结果承诺，不把工具类别和结果混成含义不清的一句话。
- 小红书主标题通常 4–12 个汉字，最多两组主视觉文字；英文产品名可以作为第二层关键词。
- 多字标题必须保持同一行或明确的整行分组：所有汉字共享同一基线，不允许单个字下坠、漂浮、错位或被模型拆成无意的断行。
- 可以使用“主体压字”：人物、电脑、网页卡片或道具有意识地遮盖标题约 5%–12%，形成前后层叠；遮盖必须来自主体与文字的前后关系，不能通过让某个字自身下移来制造错位。
- 例如 Website Skill 应写成 `Website Skill / 快速建站`，而不是 `Website / 快速出图`。
- 图片模型生成中文可能出现错字；生成前写入 `prompts/`，生成后按 `references/quality-gate.md` 检查。
- 不添加用户没有提供的数字、用户量、速度、平台背书或“爆款保证”。

## 生成流程

1. 接收 content brief，不重复询问已经提供的信息。
2. 提炼主标题、视觉主体、证明元素和目标动作。
3. 根据平台、surface、locale 和内容选择 `adaptive-composite` 的内部优先级、语义换行、关键词变色、层叠动作、颜色 Token 和安全区。
4. 写入任务目录的 `prompts/{case}-{route}-{ratio}.md`。
5. 用户明确要求出图时，调用当前运行时图片生成能力；没有人像时使用产品/界面/字体主体。
6. 检查比例、标题可读性、语言断句、字形方向、字体覆盖、主体安全区、人物/产品完整性和额外文字。
7. 返回路线、提示词路径、图片路径、质检结果和仍需人工确认的授权事项。

## 商用与原创实现

本 Skill 的代码、规则和示例由本项目原创维护，遵循本仓库 LICENSE。第三方仓库只作为研究来源，不把其文本、资源或未授权代码打包进本 Skill。生成图片的商用权利还取决于所用图片模型的服务条款，以及人物、Logo、截图、字体和素材授权。

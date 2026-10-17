# Social Cover Layout

> **面向 AI Agent 的社交媒体封面 Skill**  
> 把已经完成的内容 brief 路由成适配小红书、X/Twitter、YouTube、微信公众号、Instagram、LinkedIn、TikTok 及其他媒体表面的原创封面方案或生成封面。
>
> 由 **Chuluu** 创建和维护。

[English](README.md) | 中文说明

[![AI Skill](https://img.shields.io/badge/AI%20Skill-social--cover--layout-0E5E43)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.2.5-green)](./skill.json)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](./LICENSE)
[![by Chuluu](https://img.shields.io/badge/by-Chuluu-0E5E43)](https://github.com/ChuluuMGL)
[![Workflow](https://img.shields.io/badge/workflow-adaptive--composite-purple)](./references/visual-routes.md)
[![QA](https://img.shields.io/badge/QA-quality--gate-blue)](./references/quality-gate.md)

[GitHub 仓库](https://github.com/ChuluuMGL/social-cover-layout) | [Demo 图库](./demo/README.md) | [Skill 定义](./SKILL.md) | [平台规格](./references/platform-specs.md) | [多语言排版](./references/multilingual-typesetting.md) | [视觉路线](./references/visual-routes.md) | [配色系统](./references/color-system.md) | [质量门](./references/quality-gate.md) | [测试矩阵](./TESTING.md) | [发布边界](./PUBLISHING.md)

## 3 分钟开始使用

Codex在macOS/Linux的默认个人安装目录示例：

~~~bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/ChuluuMGL/social-cover-layout.git \
  "$HOME/.codex/skills/social-cover-layout"
~~~

已有同名目录时先保留并检查来源，再决定如何更新。配置了自定义CODEX_HOME时，改用其skills目录。安装后在新会话里让Agent读取该目录的SKILL.md并确认名称；这只能确认已识别Skill，生图能力还要单独确认。

也可以只克隆工作目录，并明确让Agent读取其中的SKILL.md：

```bash
git clone https://github.com/ChuluuMGL/social-cover-layout.git
cd social-cover-layout
```

其他兼容宿主按各自的安装目录操作，或直接读取仓库根目录；不能据此声称所有宿主的生图能力都已实测。安装后调用：

```text
使用 $social-cover-layout，把这篇已经完成的小红书笔记做成 3:4 封面。
平台：小红书。
主题：内容创作 Skill。
标题：内容创作 Skill / 写笔记还能做封面。
视觉主体：人物、电脑、笔记卡片和封面卡片。
生成模式：generate。
```

它也可以由内容创作流程在正文完成后，通过结构化 brief 调用。

### 生图能力与费用

- 宿主有图像工具：使用现有工具和用户给定的调用范围。本Skill不提供模型账户或调用额度。
- 宿主没有图像工具：用prompt-only模式，交付可复制提示词和版式说明，明确标注尚未出图。
- 中文标题需要准确时：按[可执行的生成与排字流程](references/production-rendering.md)，先做预留标题区的无字画面，再用本地真实字体排字。可选Python工具支持16:9与3:4，输出精确尺寸、25%缩略图和检查JSON，已有文件不会覆盖。
- 直接由模型生成整张含字图片的方式仍保留，需逐字检查标题和背景小字。

免费开源的是Skill源码，模型用量可能由宿主计费。本地排字需Python 3.10+、Pillow、fonttools和用户自己的可用字体，不调用模型或上传文件。

## Demo 样张

下面是之前 Website Skill 和 Content Creation Skill 测试中实际生成的封面；新的[跨平台生成 Demo](./demo/generated-platform-demos/)包含 X、微信公众号、YouTube 和 B 站版本，[P0 多语言 Demo](./demo/multilingual-p0-demos/)包含简体中文、繁体中文、英文、日文和韩文。平台尺寸和安全区测试单独放在[技术测试包](./demo/technical-platform-tests/)中，不作为主视觉 Demo。

![跨平台生成封面 Demo](./demo/generated-platform-demos/generated-platform-contact-sheet.jpg)

### P0 多语言独立封面

下面是五张真正的独立封面，不是语言说明图，也不是配色卡：

<table>
  <tr>
    <td><img src="./demo/multilingual-p0-demos/zh-hans-content-creation-skill.png" alt="简体中文封面" width="180"></td>
    <td><img src="./demo/multilingual-p0-demos/zh-hant-content-creation-skill.png" alt="繁体中文封面" width="180"></td>
    <td><img src="./demo/multilingual-p0-demos/en-content-creation-skill.png" alt="英文封面" width="180"></td>
    <td><img src="./demo/multilingual-p0-demos/ja-content-creation-skill.png" alt="日文封面" width="180"></td>
    <td><img src="./demo/multilingual-p0-demos/ko-content-creation-skill.png" alt="韩文封面" width="180"></td>
  </tr>
</table>

查看[五张独立的 P0 多语言封面 Demo](./demo/multilingual-p0-demos/)。之前的配色长图仍保留在 [`demo/previous-cases/`](./demo/previous-cases/) 作为历史测试，不再作为首页主 Demo。

完整内容见[Demo 图库](./demo/README.md)。

## 这个 Skill 做什么

`social-cover-layout` 把“内容创作”和“封面制作”连接起来，但不负责写正文。它接收完成的内容 brief，再根据媒体平台、内容目的、标题和视觉主体选择封面路线。`content-cover-router` 是此前的内部名称和兼容别名。

| 输出 | 内容 |
|---|---|
| 平台路线 | 小红书、X/Twitter、YouTube、微信或其他媒体的比例、安全区和缩略图重点。 |
| 视觉路线 | 一个统一 `adaptive-composite` 系统中的 `headline-first`、`proof-first` 或 `bridge-hybrid`。 |
| 标题系统 | 语义换行、最多两组主视觉文字、关键词变色、稳定基线，避免单字下坠。 |
| 层叠系统 | 背景、文字/证据、前景三层，以及可解释的人物/文字/道具关系。 |
| 画布家族 | `vertical`、`wide`、`square` 三类构图约束，复用同一套视觉系统，不增加模板数量。 |
| 配色系统 | 根据内容气质和品牌规则选择亮色、柔和色或双色组合。 |
| 生成 brief | 可直接交给图片生成能力的提示词、参考素材、平台、比例和标题规则。 |
| 质检交接 | 可读性、安全区、素材授权、额外文字和层叠关系检查。 |
| 多语言排版 | 当前 P0 支持简体中文、繁体中文、英文、日文和韩文；其他语言进入人工复核。 |

## 典型场景

- 小红书笔记首图：突出首屏停留、收藏价值和结果承诺。
- X/Twitter 配图：突出一秒理解和转发，不画平台按钮。
- YouTube 缩略图：16:9，更短标题、更大主体和更强冲突。
- Instagram：信息流默认 4:5，Reel 封面走 9:16，并预留主页裁切安全区。
- LinkedIn：网站分享卡默认 1.91:1，文章封面使用超宽编辑版。
- TikTok：视频封面默认 9:16；它是视频优先平台，不能把普通静态图广告规格当成统一帖子规格。
- Skill、工具或产品发布：用人物、电脑、网页卡片或界面作为可信证据。
- 内容创作流程交接：正文完成后，询问是否将 brief 交给封面 Skill。
- 没有人像时：使用产品界面、电脑、手部、字体或场景承担主视觉。

## 工作流

1. 接收 topic、purpose、标题、平台、surface、比例和参考素材。
2. 选择平台表面、安全区和缩略图阅读优先级。
3. 选择 `adaptive-composite` 内部路线、语义换行、关键词颜色和层叠动作。
4. 用户要求出图时生成；否则只返回封面方案和 prompt。
5. 按质量门检查标题、人物、产品证据、比例、额外文字和素材授权。

## 原创与素材边界

本仓库的 Skill 规则、路由和文档为原创维护，只提炼通用设计方法，不打包第三方 Skill 的原文、文件结构、品牌名称、人物头像、Logo、水印、截图或单张封面构图。

公开示例应使用原创提示词、已授权素材或合成人物。生成图片是否可以商用，还取决于所使用的图片模型条款，以及人物、Logo、截图、字体和其他参考素材的授权。

## 与内容创作 Skill 集成

`content-creation-workflow` 可以在完成标题、正文、评分和平台适配后，把结构化 brief 交给本 Skill。本仓库也可以完全独立调用。

```yaml
cover_skill: "social-cover-layout"
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
layout_family: "vertical | wide | square | auto"
generation_mode: "prompt-only | generate"
```

## 质量门

- 平台比例和交付 surface 正确。
- 在轻量 25% 手机缩略图预览中，主标题和视觉主体仍可识别，没有错字、乱码或未要求的额外文字。
- 标题、人物脸、手势、产品和证据都在安全区内。
- 没有未经授权的真人、Logo、截图、字体、水印或第三方品牌。
- 没有单字下坠、漂浮、随机断行或用文字自身错位制造层叠。
- 主标题、视觉主体和证据的阅读顺序清晰。

完整规则见 [`references/quality-gate.md`](./references/quality-gate.md)。

## 校验

```bash
npm run validate
```

校验会检查 frontmatter、必要参考文件、JSON 元数据、README 必要章节、版本一致性和独立仓库结构。最终视觉仍需要人工在手机缩略图尺寸下复核。

离线排字测试：先按[排字指南](references/production-rendering.md)安装requirements-render.txt，再运行：

~~~bash
.venv/bin/python -m unittest discover -s tests -v
~~~

测试需要真实的中文/拉丁字体；默认macOS/Ubuntu候选不可用时，用COVER_TEST_FONT指定路径。覆盖尺寸、文字边界、缺字、超长标题、源图保留、输出冲突和独立安装目录调用。纯色测试图只是排字夹具，不是AI生图案例。

## 许可证

MIT，见 [`LICENSE`](./LICENSE)。MIT 只覆盖本仓库源代码和文档，不自动授予外部图片、字体、Logo、截图、模型输出或第三方参考素材的权利。

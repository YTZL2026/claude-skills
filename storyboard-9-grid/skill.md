---
name: storyboard-9-grid
description: 生成 NanoBananaPro 专用 3x3 横版16:9宫格分镜JSON。当用户需要把剧本拆成9个分镜、做横版故事板、用NanoBananaPro出图时使用。
---

# 横版9宫格分镜提示词 Skill

根据剧本和参考图，生成 NanoBananaPro 专用的 3x3 宫格分镜 JSON，追求极致精简且空间逻辑严密的关键词描述。

## 使用方式

用户通过以下方式调用：
- `/storyboard-9-grid <剧本文本>`
- "帮我把这个剧本拆成9个分镜"
- "生成3x3横版分镜"
- "用NanoBananaPro出9宫格图"

## 核心角色

以 **"Creative Visualization Script Assistant - Spatial Mode"** 角色工作，具备5项核心技能：

1. **极简提炼**：将复杂场景压缩为 3-5 个核心关键词
2. **视觉转化**：提取参考图风格标签
3. **宫格规划**：设计 9 个独立分镜
4. **空间调度**：明确人物相对位置 (如 'beside bed', 'background')
5. **格式控制**：严格遵循 JSON 与字数限制

## 执行流程

### 步骤 1：接收输入

接收用户的：
- **中文剧本文本**：需要拆解的故事内容
- **视觉参考图片**（可选）：用于提取风格的参考图

### 步骤 2：提取风格标签

如果用户提供了参考图，分析并提取 3-4 个最具代表性的风格单词，追加在每个 Prompt 后部。例如：`Anime style, 3D render, 8k, Volumetric lighting`

如果没有参考图，使用用户指定的风格或默认高质量风格标签。

### 步骤 3：拆解剧本为 9 个关键戏剧瞬间

将剧本切分为 9 个关键动作，确保叙事完整：
- 定义空间地图 (如：床在中央，门在背景)
- 组合公式：`[动态景别] + [主体与位置] + [环境光影] + [风格标签] + [排除词]`

### 步骤 4：编写动态 Prompt

为每个分镜编写 prompt_text，遵循以下规则：
- 加入位置关系词、运动模糊、角度变化
- 必须体现紧张感和戏剧性
- 必须包含镜头感描述

### 步骤 5：检查与封装

1. 检查每个 prompt_text 字数在 **20-30 个英文单词**之间
2. 确认分镜间人物位置逻辑连贯 (如医生始终在床边)
3. 封装为标准 JSON 输出

## 输出规范

### 强制要求

| 规则 | 说明 |
|------|------|
| 格式 | 纯净 JSON 字符串，无 Markdown 代码块包裹 |
| 模型 | `image_generation_model`: "NanoBananaPro" |
| 布局 | `grid_layout`: "3x3" |
| 画幅 | `grid_aspect_ratio`: "16:9" |
| 数量 | `shots` 数组精确 **9** 个对象 |
| 字数 | 每个 prompt_text 严格 **20-30** 个英文单词 |
| 语法 | 使用 '关键词 + 逗号' (Tags) 形式，禁用长难句 |
| 禁用句式 | 严禁 `A scene showing...`、`There is a...` 等废话开头 |
| 排除词 | 每个 prompt 必须包含 `no watermark, no timecode, no subtitles` |
| 去水印 | 绝对不允许分镜内容出现水印，严禁添加任何 watermark 配置及文字指令 |

### 戏剧性与镜头感词库

**情绪词（体现紧张感）：**
Agony, Frantic, Desperate, Intense, Suffering, Screaming, Gasping, Trembling

**镜头词（增强电影感）：**
Motion Blur, Low Angle, Extreme Close-up, Dutch Angle, Wide Shot, Tracking Shot, Deep Focus

### JSON 输出结构

```json
{
  "image_generation_model": "NanoBananaPro",
  "grid_layout": "3x3",
  "grid_aspect_ratio": "16:9",
  "shots": [
    {
      "shot_number": "分镜 1",
      "prompt_text": "Extreme Close-up, [主体] on central [位置], [动作], [情绪], [环境], [光影], [风格标签], 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 2",
      "prompt_text": "..."
    }
    // ... 共 9 个
  ]
}
```

## 约束清单

1. **C1 - 格式**：标准 JSON，无 Markdown 废话
2. **C2 - 数量**：Shots 数组必须为 9 个
3. **C3 - 字数锁**：每个 prompt_text 限制在 20-30 词之间
4. **C4 - 句式**：严禁使用长难句，严禁使用 'A scene showing...', 'There is a...' 等废话
5. **C5 - 排除指令**：必须包含 'no watermark, no timecode, no subtitles'
6. **C6 - 去水印**：绝对不允许分镜内容出现水印，严禁在 JSON 结构或 Prompt 中添加任何 watermark 配置及文字指令
7. **C7 - 戏剧性**：必须体现紧张感，使用 Agony, Frantic, Desperate 等词
8. **C8 - 镜头感**：必须包含 Motion Blur, Low Angle, Extreme Close-up 等
9. **C9 - 空间逻辑**：分镜间人物位置需符合逻辑连贯性

## 完整示例

输入剧本：「皇后在寝宫中痛苦分娩，侍女羽衣外出寻药」

```json
{
  "image_generation_model": "NanoBananaPro",
  "grid_layout": "3x3",
  "grid_aspect_ratio": "16:9",
  "shots": [
    {
      "shot_number": "分镜 1",
      "prompt_text": "Extreme Close-up, Queen on central bed, head thrown back, neck veins popping, screaming in agony, dark palace bedroom, flickering candlelight, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 2",
      "prompt_text": "Close-up, Queen's face covered in cold sweat, eyes closed tightly, expression of pure suffering, red candlelight flickering, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 3",
      "prompt_text": "Medium Shot, Maid Yuyi standing beside bed, anxiously wringing cloth, worried expression, sweat on brow, warm interior light, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 4",
      "prompt_text": "Low Angle, Queen's hand gripping silk sheets, knuckles white, rings digging into fingers, extreme tension, shallow depth of field, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 5",
      "prompt_text": "Close-up, Maid Yuyi's determined face, turning from bed, grabbing cloak, urgent movement, motion blur on edges, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 6",
      "prompt_text": "Wide Shot, Maid Yuyi running through dark corridor, cloak billowing behind, torchlight casting long shadows, frantic pace, motion blur, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 7",
      "prompt_text": "Extreme Wide Shot, palace exterior at night, single lantern moving rapidly through courtyard, storm clouds gathering, lightning in distance, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 8",
      "prompt_text": "Medium Shot, Queen alone on bed, reaching toward door, desperate expression, tears streaming, body arching in pain, volumetric candlelight, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜 9",
      "prompt_text": "Medium Shot, Maid Yuyi returning holding precious medicine box, hopeful expression, sweat on forehead, bright light from door, Ancient Palace, Cinematic Lighting, 8k, no watermark, no timecode, no subtitles."
    }
  ]
}
```

## 版本信息

- 作者：海皮哥，改编自原作者：黄鑫波
- 版本：0.3.6 (16:9 无水印版)
- 修订：用户定制版 - 16:9横屏 无水印 空间调度增强

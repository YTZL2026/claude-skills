---
name: storyboard-25-grid
description: 生成 NanoBananaPro 专用 5x5 横版16:9宫格分镜JSON（25个分镜）。当用户需要更精细的故事板、把剧本拆成25个镜头、做详细分镜规划时使用。
---

# 智能体提示词 - 25宫格分镜 Skill

根据剧本和参考图，生成 NanoBananaPro 专用的 5x5 宫格分镜 JSON，追求极致精简的关键词描述。适用于需要更精细镜头拆解的场景。

## 使用方式

用户通过以下方式调用：
- `/storyboard-25-grid <剧本文本>`
- "帮我把剧本拆成25个分镜"
- "生成5x5分镜"
- "用智能体拆解分镜"

## 核心角色

以 **"Creative Visualization Script Assistant - Concise Mode"** 角色工作，具备4项核心技能：

1. **极简提炼**：将复杂场景压缩为 3-5 个核心关键词
2. **视觉转化**：提取参考图风格标签
3. **宫格规划**：设计 25 个独立分镜
4. **格式控制**：严格遵循 JSON 与字数限制

## 执行流程

### 步骤 1：接收输入

接收用户的：
- **中文剧本文本**：需要拆解的故事内容
- **视觉参考图片**（可选）：用于提取风格的参考图

### 步骤 2：提取风格标签

分析参考图，提取 3-4 个最具代表性的风格单词（如 `Cyberpunk, Neon, Oil Painting`），追加在每个 Prompt 后部。

### 步骤 3：拆解剧本为 25 个瞬间

将剧本切分为 25 个关键动作。组合公式：
`[景别] + [主体与动作] + [环境] + [风格标签] + [排除词]`

### 步骤 4：编写精简 Prompt

仅保留：景别、主语、动词、核心环境词。每个 Prompt 控制在 **25 词左右 (±5词)**。

### 步骤 5：封装 JSON

检查字数后封装为标准 JSON 输出。

## 输出规范

### 强制要求

| 规则 | 说明 |
|------|------|
| 格式 | 纯净 JSON 字符串，无 Markdown 代码块包裹 |
| 模型 | `image_generation_model`: "NanoBananaPro" |
| 布局 | `grid_layout`: "5x5" |
| 画幅 | `grid_aspect_ratio`: "16:9" |
| 水印 | `global_watermark`: { "position": "bottom_center", "size": "extremely small" } |
| 数量 | `shots` 数组精确 **25** 个对象 |
| 字数 | 每个 prompt_text **25 词左右 (±5词)** |
| 语法 | 使用 '关键词 + 逗号' (Tags) 形式，禁用长难句 |
| 禁用句式 | 严禁 `A scene showing...`、`There is a...` 等废话开头 |
| 排除词 | 必须包含 `no timecode, no subtitles` |
| 去水印 | 严禁添加 '分镜X in corner' 等文字指令 |

### JSON 输出结构

```json
{
  "image_generation_model": "NanoBananaPro",
  "grid_layout": "5x5",
  "grid_aspect_ratio": "16:9",
  "global_watermark": {
    "position": "bottom_center",
    "size": "extremely small"
  },
  "shots": [
    {
      "shot_number": "分镜1",
      "prompt_text": "Short keywords prompt... no timecode, no subtitles."
    },
    {
      "shot_number": "分镜2",
      "prompt_text": "..."
    }
    // ... 共 25 个
  ]
}
```

## 约束清单

1. **C1 - 格式**：标准 JSON，无 Markdown 废话
2. **C2 - 数量**：Shots 数组必须为 25 个
3. **C3 - 字数锁**：每个 prompt_text 限制在 25 词左右 (±5词)
4. **C4 - 句式**：严禁使用长难句，严禁使用 'A scene showing...', 'There is a...' 等废话
5. **C5 - 排除指令**：必须包含 'no timecode, no subtitles'
6. **C6 - 去水印**：严禁添加 '分镜X in corner' 等文字指令

## 景别参考词库

| 景别 | 英文关键词 |
|------|-----------|
| 大远景 | Extreme Wide Shot, Establishing Shot |
| 全景 | Wide Shot, Full Shot |
| 中景 | Medium Shot, Cowboy Shot |
| 近景 | Close-up, Medium Close-up |
| 特写 | Extreme Close-up, Detail Shot |
| 过肩 | Over-the-Shoulder Shot |
| 低角度 | Low Angle Shot |
| 高角度 | High Angle, Bird's Eye View |
| 荷兰角 | Dutch Angle, Canted Angle |
| 跟拍 | Tracking Shot, Dolly Shot |

## 风格标签参考

```
Anime style, 3D render, 8k, Volumetric lighting
Cyberpunk, Neon, Oil Painting, High Contrast
Cinematic Lighting, Photorealistic, Octane Render
Artstation trend, Unreal Engine 5, Ray Tracing
Dark Fantasy, Gothic, Chiaroscuro, Muted Colors
```

## 完整示例

输入剧本：「科幻山村，村民在发光峡谷中生活」

```json
{
  "image_generation_model": "NanoBananaPro",
  "grid_layout": "5x5",
  "grid_aspect_ratio": "16:9",
  "global_watermark": {
    "position": "bottom_center",
    "size": "extremely small"
  },
  "shots": [
    {
      "shot_number": "分镜1",
      "prompt_text": "Extreme Wide Shot, mountain village in glowing canyon, waterfalls, futuristic flora, anime style, 3D render, 8k, cinematic lighting, no timecode, no subtitles."
    },
    {
      "shot_number": "分镜2",
      "prompt_text": "Medium Shot, villagers walking on glowing path, joyful expressions, vibrant colors, high contrast, anime aesthetic, detailed textures, no timecode, no subtitles."
    }
  ]
}
```

> **注意**：示例仅展示前2个分镜，实际需生成完整 25 个。

## 版本信息

- 作者：白灵，改编自原作者：黄鑫波
- 版本：0.3.3 (精简关键词版)
- 修订：用户定制版

<div align="center">

# Claude Code Skills 合集

<p>
  <strong>我的 AI 编程助手 Skills 仓库 — 一键复用的能力模块</strong>
</p>

<p>
  <a href="#"><img src="https://img.shields.io/badge/Skills-12个-blue?style=flat-square" alt="Skills Count"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-CC0-green?style=flat-square" alt="CC0"></a>
</p>

</div>

---

## 这是什么？

[Claude Code](https://claude.ai/code) 的 Skills 是一种可复用的提示词+脚本组合。每个 skill 封装了一个完整的工作流，一句话触发。

这个仓库包含我在日常开发中沉淀的 12 个 skills，覆盖：

| 分类 | Skills | 说明 |
|------|--------|------|
| 🏥 医疗 | `batch-import` | 病历样本全格式（docx/pdf/图片）自动提取→CSV→导入不良事件系统 |
| 🔧 工具 | `github-fix` | 单位网络 GitHub 访问修复（hosts + IP轮换） |
| 🔧 工具 | `migrate-package` | 一键打包整个项目为可移植迁移包 |
| 🎨 设计 | `character-design-sheet` | AI 生成游戏/动漫角色三视图+表情+动作人设图 |
| 🎨 设计 | `storyboard-9-grid` | 3x3 16:9 分镜 JSON（NanoBananaPro） |
| 🎨 设计 | `storyboard-25-grid` | 5x5 精细化分镜 JSON |
| 🎨 设计 | `image-consistency-supplement` | 分镜画面空间一致性与连贯性提示词 |
| 📖 阅读 | `read-image` | 图片文字识别（数学题专用） |
| 🏗️ 开发 | `flask-to-exe` | Flask 应用打包为 Windows EXE |
| 🏗️ 开发 | `html-embed-flask` | HTML 页面嵌入 Flask 服务端 |
| 🏗️ 开发 | `global-file-search-api` | 全局文件搜索 API 端点 |
| 🏗️ 开发 | `ai-structured-inspection` | AI 结构化巡检/质控检查 |
| 🏗️ 开发 | `exceljs-export-template` | ExcelJS 绿色主题导出模板 |

## 使用方式

把这些文件放到你的 `~/.claude/skills/` 目录下，然后在 Claude Code 中输入 `/skill-name` 即可调用。

例如：
```
/github-fix        # 修复 GitHub 访问
/batch-import      # 批量导入病历
/migrate-package   # 打包项目
```

## 自定义

每个 skill 都是独立的 Markdown 文件，你可以自由修改里面的提示词、参数和流程来适配自己的项目。

## 开源协议

[CC0 1.0 Universal](LICENSE) — 完全开源，无需署名，自由使用、修改、分发。

> 这些 skills 本身就是提示词模板，希望它们能帮你提高效率 ✨

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/86132">86132</a> · Powered by Claude Code</sub>
</p>

---
name: migrate-package
description: 完美项目迁移打包 — 一键打包全部项目、Skills、文稿、产品、日志为可移植文件夹。本地文件完整保留。当用户说"备份项目""迁移包""打包带走""换电脑"时使用。
---

# Perfect Migration Package Skill

一键生成 CC Switch 完整项目迁移包，包含所有项目、Skills、文稿、产品、日志。本地不做任何删除。

## 触发条件

当用户说以下内容时使用：
- "做迁移包" "打包项目" "备份所有" "完美迁移"
- "换电脑了怎么迁移" "帮我把项目带走"
- "/migrate-package"

## 执行流程

### 步骤 1：确认脚本存在

检查 `_migrate_package.py` 是否在项目根目录 `C:\Users\86132\AppData\Local\Programs\CC Switch\`。

如果不存在，按下方模板重建。

**在重建或修改脚本时，必须注意以下常被遗漏的内容：**

| 类别 | 内容 | 常见遗漏原因 |
|------|------|-------------|
| 项目级 Skills | `.claude/skills/` | 被 `.claude` 排除规则误杀 |
| 项目日志 | `.claude/project-log/` | 同上 |
| 根目录脚本 | `serve.bat` / `serve.ps1` / `*。bat` | 只加了子目录，忘了根 |
| 单文件产品 | `PROJECT_MIGRATION_GUIDE.html` 等 | `os.walk()` 不处理单文件 |
| 迁移工具自身 | `_migrate_package.py` / `migrate.py` | 忘了自举 |
| API Key 文件 | `settings.local.json` | 应排除，不能打包 |

### 步骤 2：运行脚本

```bash
cd "C:\Users\86132\AppData\Local\Programs\CC Switch"
python _migrate_package.py
```

### 步骤 3：验证完整性

脚本运行后，检查输出统计。手动确认以下目录非空：

| 检查项 | 路径 | 预期内容 |
|--------|------|---------|
| 医院系统 | `医院系统/` | index.html + training-map/ + adverse-events/ |
| 灵枢AI | `灵枢AI/` | 4个版本目录 |
| 项目日志 | `项目日志/` | 迁移指南HTML + 开发日志 |
| Skills | `Claude配置/skills/` | 至少10个skill目录 |
| 项目Skills | `Claude配置/项目级skills/` | 4个skill文件 |
| 迁移工具 | `迁移工具/` | _migrate_package.py 等 |

### 步骤 4：报告给用户

告知用户：
- 包的位置（桌面 `CC_Switch_迁移包_YYYY-MM-DD\`）
- 文件总数、模块数、Skills 数
- 包内 README.md 含完整还原指南
- 本地文件完整保留

## 迁移包标准结构

```
CC_Switch_迁移包_YYYY-MM-DD/
├── 医院系统/                         ← 主力项目
│   ├── index.html
│   ├── training-map/
│   ├── adverse-events/
│   ├── 病历质控台账生成器.html
│   └── serve.bat
├── 灵枢AI/                           ← 全版本
│   ├── palm-ai/
│   ├── palm-ai-app/
│   ├── palm-ai-app-v1-backup/
│   └── palm-ai-mobile/
├── 宝箱怪挂机/                        ← 游戏脚本
├── 项目日志/                          ← 文档 + 开发日志
│   ├── PROJECT_MIGRATION_GUIDE.html
│   └── 开发日志/
├── Claude配置/                        ← Skills + 记忆
│   ├── skills/
│   ├── 项目级skills/
│   └── project-memory/
├── 迁移工具/                          ← 迁移脚本
├── 杂项/
└── README.md                         ← 清单 + 还原指南
```

## 迁移脚本核心逻辑

脚本 `_migrate_package.py` 的关键设计决策：

1. **单文件 vs 目录**：`os.walk()` 不能遍历单文件，用 `os.path.isfile()` 预先判断
2. **排除规则**：排除 `__pycache__`/`.git`/`node_modules`/`dist`/`build`/`models`/`.EasyOCR`
3. **API Key 保护**：`settings.local.json` 不打包
4. **`.claude` 特殊处理**：不在全局排除中，通过独立 spec 精确复制 skills 和 project-log
5. **本地保留**：只做 `shutil.copy2()`，不做任何 `shutil.move()` 或 `os.remove()`
6. **manifest 生成**：自动生成 README.md 含目录结构和还原指南

## 注意事项

- `.claude` 目录中 `settings.local.json` 含 API Key，切勿打包
- EasyOCR 缓存目录 (`~/.EasyOCR`) 约 2GB，切勿打包
- `palm-ai/models/` AI 模型文件大，不打包（需要时重新下载）
- `cc-switch.exe` 和 `Uninstall CC Switch.lnk` 是安装产物，不打包
- 打包脚本自身 (`_migrate_package.py`) 应自举到 `迁移工具/` 目录

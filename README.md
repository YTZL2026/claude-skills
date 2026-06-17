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

  <strong>鎴戠殑 AI 缂栫▼鍔╂墜 Skills 浠撳簱 鈥?涓€閿鐢ㄧ殑鑳藉姏妯″潡</strong>
  <a href="#"><img src="https://img.shields.io/badge/Skills-16涓?blue?style=flat-square" alt="Skills Count"></a>
[Claude Code](https://claude.ai/code) 鐨?Skills 鏄竴绉嶅彲澶嶇敤鐨勬彁绀鸿瘝+鑴氭湰缁勫悎銆傛瘡涓?skill 灏佽浜嗕竴涓畬鏁寸殑宸ヤ綔娴侊紝涓€鍙ヨ瘽瑙﹀彂銆?
杩欎釜浠撳簱鍖呭惈鎴戝湪鏃ュ父寮€鍙戜腑娌夋穩鐨?12 涓?skills锛岃鐩栵細
| 馃彞 鍖荤枟 | `batch-import` | 鐥呭巻鏍锋湰鍏ㄦ牸寮忥紙docx/pdf/鍥剧墖锛夎嚜鍔ㄦ彁鍙栤啋CSV鈫掑鍏ヤ笉鑹簨浠剁郴缁?|
| 🛡 工具 | `recycle-fix` | 外置硬盘/U盘回收站损坏修复 |
| 🛡 工具 | `disk-fix` | 移动硬盘/U盘盘符丢失修复（SAN策略+USB省电） |
| 🛡 工具 | `desktop-organize` | 桌面文件智能归类整理（扫描→分析→合并→重命名） |
| 🛡 工具 | `bookmark-fix` | 浏览器书签膨胀去重修复（电脑Chromium系） |
| 馃敡 宸ュ叿 | `github-fix` | 鍗曚綅缃戠粶 GitHub 璁块棶淇锛坔osts + IP杞崲锛?|
| 馃帹 璁捐 | `character-design-sheet` | AI 鐢熸垚娓告垙/鍔ㄦ极瑙掕壊涓夎鍥?琛ㄦ儏+鍔ㄤ綔浜鸿鍥?|
| 馃帹 璁捐 | `storyboard-9-grid` | 3x3 16:9 鍒嗛暅 JSON锛圢anoBananaPro锛?|
| 馃帹 璁捐 | `storyboard-25-grid` | 5x5 绮剧粏鍖栧垎闀?JSON |
| 馃摉 闃呰 | `read-image` | 鍥剧墖鏂囧瓧璇嗗埆锛堟暟瀛﹂涓撶敤锛?|
| 馃彈锔?寮€鍙?| `flask-to-exe` | Flask 搴旂敤鎵撳寘涓?Windows EXE |
| 馃彈锔?寮€鍙?| `html-embed-flask` | HTML 椤甸潰宓屽叆 Flask 鏈嶅姟绔?|
| 馃彈锔?寮€鍙?| `global-file-search-api` | 鍏ㄥ眬鏂囦欢鎼滅储 API 绔偣 |
| 馃彈锔?寮€鍙?| `ai-structured-inspection` | AI 缁撴瀯鍖栧贰妫€/璐ㄦ帶妫€鏌?|
| 馃彈锔?寮€鍙?| `exceljs-export-template` | ExcelJS 缁胯壊涓婚瀵煎嚭妯℃澘 |
鎶婅繖浜涙枃浠舵斁鍒颁綘鐨?`~/.claude/skills/` 鐩綍涓嬶紝鐒跺悗鍦?Claude Code 涓緭鍏?`/skill-name` 鍗冲彲璋冪敤銆?
渚嬪锛?```
## 鑷畾涔?
姣忎釜 skill 閮芥槸鐙珛鐨?Markdown 鏂囦欢锛屼綘鍙互鑷敱淇敼閲岄潰鐨勬彁绀鸿瘝銆佸弬鏁板拰娴佺▼鏉ラ€傞厤鑷繁鐨勯」鐩€?
## 寮€婧愬崗璁?
[CC0 1.0 Universal](LICENSE) 鈥?瀹屽叏寮€婧愶紝鏃犻渶缃插悕锛岃嚜鐢变娇鐢ㄣ€佷慨鏀广€佸垎鍙戙€?
> 杩欎簺 skills 鏈韩灏辨槸鎻愮ず璇嶆ā鏉匡紝甯屾湜瀹冧滑鑳藉府浣犳彁楂樻晥鐜?鉁?
  <sub>Built with 鉂わ笍 by <a href="https://github.com/YTZL2026">YTZL2026</a> 路 Powered by Claude Code</sub>
---
name: batch-import
description: 批量文件识别导入 — 全格式（docx/json/csv/xps/pdf/png/jpg等）→ 字段提取 → CSV → 导入不良事件系统。当用户需要将患者样本文件批量导入不良事件报告系统时使用。
---

# Batch Import Skill

批量文件识别导入工具，将多种格式的患者样本文件自动提取字段并导入不良事件报告系统。

## 使用方式

用户通过以下方式调用：
- `/batch-import <文件夹路径>`
- "批量导入这些样本"
- "把这些患者文件导入系统"

## 支持格式

| 格式 | 提取方式 | 准确率 | 需要安装 |
|------|---------|--------|---------|
| `.docx` (Word) | ZIP+XML 直接解析 | 100% | 无 |
| `.json` | JSON 直接解析 | 100% | 无 |
| `.txt` / `.md` | 直接读取 | 100% | 无 |
| `.csv` | CSV 模块解析 | 100% | 无 |
| `.xps` | ZIP+XML 直接解析 | 100% | 无 |
| `.pdf` (文本型) | PyMuPDF 提取文字 | ~95% | PyMuPDF |
| `.pdf` (扫描型) | PyMuPDF → EasyOCR | ~90% | PyMuPDF + easyocr |
| `.png` / `.jpg` / `.bmp` / `.tiff` / `.webp` | EasyOCR | ~90% | easyocr |

## 执行流程

### 步骤 1：确认环境

1. 检查 `_batch_import.py` 是否存在于项目目录 `C:\Users\86132\AppData\Local\Programs\CC Switch\adverse-events\`
2. 如果不存在，按下方模板创建
3. 检查 easyocr 是否已安装。如果用户未安装，提示：
   ```
   pip install easyocr
   ```
   注意：文本型文件（docx/json/txt/csv/xps）不需要 easyocr，只有图片和扫描PDF才需要。

### 步骤 2：运行批量导入脚本

告知用户运行：
```
python adverse-events/_batch_import.py <文件夹路径>
```

或指定输出文件：
```
python adverse-events/_batch_import.py <文件夹路径> --output <输出CSV路径>
```

### 步骤 3：读取结果并整理

1. 脚本运行完成后，读取输出的 CSV 文件
2. 汇总提取到的字段：患者姓名、病历号、性别、年龄、诊断、科室等
3. 呈现给用户核对，标注哪些字段可能需要人工修正

### 步骤 4：引导用户导入系统

告知用户：
1. 用 Excel 打开 CSV 核对修正
2. 打开 `adverse-events/index.html`
3. 点击「📥 批量导入」→ 上传 CSV 文件
4. 在预览中确认列映射 → 点击导入

## _batch_import.py 脚本位置

项目目录：`C:\Users\86132\AppData\Local\Programs\CC Switch\adverse-events\_batch_import.py`

如果脚本不存在或被删除，按项目中的最新版本重建。脚本应包含：
- 全格式文件检测与分发
- 文本型直接提取（docx/json/txt/csv/xps）
- OCR 图像识别（pdf/png/jpg/bmp/tiff）
- 正则字段提取（姓名、病历号、性别、年龄、诊断、科室、日期、事件描述等）
- CSV 输出

## 提取的字段

脚本自动从文件中提取以下字段（基于正则匹配）：

| 字段名 | 说明 | 匹配模式 |
|--------|------|---------|
| `a_name` | 患者姓名 | 姓名/患者/病人 + 2-4个中文字符 |
| `a_record_id` | 病历号/住院号 | 病历号/住院号/登记号/ID + 编号 |
| `a_gender` | 性别 | 性别 + 男/女 |
| `a_age` | 年龄 | 年龄 + 数字 |
| `a_diagnosis` | 临床诊断 | 诊断/临床诊断/入院诊断 + 描述 |
| `h_dept` | 科室 | 科室/病区/所在科室 + 名称 |
| `b_location` | 事件场所 | 急诊/门诊/住院部/医技部门等 |
| `a_treatment_time` | 诊疗时间 | YYYY-MM-DD 格式日期 |
| `h_name` | 报告人 | 报告人/上报人/医师 + 姓名 |
| `h_phone` | 联系电话 | 电话/Tel/Phone + 号码 |
| `b_description` | 事件经过 | 事件经过/不良事件/事件描述 + 文本 |

## 注意事项

- 图片识别率取决于清晰度，打印体效果好于手写体
- 识别结果建议在 Excel 中人工核对后再导入系统
- EasyOCR 首次运行会自动下载中文识别模型（约200MB），需要联网
- XPS 格式是微软的 XML Paper Specification，类似 PDF，可用 ZIP+XML 直接解析

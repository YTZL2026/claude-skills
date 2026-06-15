---
name: read-image
description: 读取图片中的文字内容，专为数学题图片设计。当用户需要查看图片里的题目文字时使用。
---

# Read Image Skill

读取图片文件中的文字内容，将图片中的数学题目提取为可读文本。

## 使用方式

用户通过以下方式调用：
- `/read-image <图片路径>`
- "帮我读一下这张图"
- "看看这张图片里写了什么"

## 执行流程

### 步骤 1：检查图片是否存在

使用 Read 工具尝试读取指定的图片文件。如果文件不存在，告知用户。

### 步骤 2：尝试直接读取

当前模型如果不支持图片，则跳转到步骤 3。

### 步骤 3：使用 Python OCR 脚本

在项目目录 `C:\Users\86132\Desktop\宁宁的数学课堂\` 下，有一份 OCR 脚本 `read_image.py`。

**操作方式：**

1. 先检查 `read_image.py` 是否存在
2. 如果不存在，按以下模板创建它
3. 如果存在，请用户手动运行：
   ```
   python "C:\Users\86132\Desktop\宁宁的数学课堂\read_image.py" "<图片路径>"
   ```
4. 读取脚本输出的文本结果

### 步骤 4：整理输出

将 OCR 提取的文字按题目格式整理，呈现给用户。对于数学题，特别注意：
- 数字和符号是否正确
- 题目编号是否清晰
- 有图表的题目提醒用户图表需要人工查看

## OCR 脚本模板

当 `read_image.py` 不存在时，使用以下代码创建它：

```python
"""
数学题图片 OCR 读取工具
用法: python read_image.py <图片路径>
"""
import sys
import os

def read_image_with_ocr(image_path):
    """使用可用库读取图片中的文字"""
    if not os.path.exists(image_path):
        return f"错误：文件不存在 - {image_path}"
    
    results = []
    results.append(f"图片路径: {image_path}")
    
    # 方案1: 使用 Pillow 获取基本信息
    try:
        from PIL import Image
        img = Image.open(image_path)
        results.append(f"尺寸: {img.size[0]} x {img.size[1]}")
        results.append(f"格式: {img.format}")
        results.append(f"模式: {img.mode}")
    except ImportError:
        results.append("[提示] Pillow 未安装，无法读取图片基本信息。")
        results.append("[安装] pip install Pillow")
    except Exception as e:
        results.append(f"Pillow 读取失败: {e}")
    
    # 方案2: 使用 pytesseract 进行 OCR
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        if text.strip():
            results.append("\n--- OCR 识别结果 ---")
            results.append(text)
        else:
            results.append("\n[提示] OCR 未识别到文字。")
    except ImportError:
        results.append("\n[提示] pytesseract 未安装。")
        results.append("[安装步骤]")
        results.append("  1. 下载安装 Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki")
        results.append("  2. pip install pytesseract")
        results.append("  3. 安装中文语言包（安装时勾选 Chinese Simplified）")
    except Exception as e:
        results.append(f"\n[提示] OCR 失败: {e}")
    
    # 方案3: 使用 easyocr 作为备选
    try:
        import easyocr
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        result = reader.readtext(image_path)
        if result:
            results.append("\n--- EasyOCR 识别结果 ---")
            for detection in result:
                text = detection[1]
                confidence = detection[2]
                results.append(f"  [{confidence:.0%}] {text}")
    except ImportError:
        results.append("\n[提示] easyocr 未安装。")
        results.append("[安装] pip install easyocr")
    except Exception as e:
        results.append(f"\n[提示] EasyOCR 失败: {e}")
    
    return "\n".join(results)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python read_image.py <图片路径>")
        print("示例: python read_image.py 数学题.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output = read_image_with_ocr(image_path)
    print(output)
```

## 首次使用的安装引导

如果用户首次使用本 Skill，先检查环境：

1. 检查 Python 是否可用（询问用户能否运行 `python --version`）
2. 建议用户安装所需库：

**最小安装（只能看图片基本信息）：**
```
pip install Pillow
```

**完整安装（能 OCR 识别中英文）：**
```
pip install Pillow pytesseract
```
并下载 Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki

**备选方案（纯 Python，无需额外软件）：**
```
pip install Pillow easyocr
```
EasyOCR 首次运行会自动下载模型，需要联网。

## 注意事项

- 手写文字的识别率较低，打印体效果好
- 图片清晰度直接影响 OCR 结果
- 数学符号（÷、×、分数等）可能识别不准，需要人工核对
- 如果图片包含图表/图形，OCR 无法处理，只能提取文字部分

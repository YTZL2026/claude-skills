# HTML 嵌入路由 — 前端源码保护

## 适用场景
Flask 打包为桌面 EXE 时，需要保护 HTML/JS/CSS 前端源码不被用户通过 F12 或直接访问静态文件获取。

## 原理

Flask 默认 `static/` 目录是公开的，任何人访问 `/static/xxx.html` 就能拿到源码。
**改为路由返回内存/文件内容，不暴露静态目录**。

## 模板

```python
from flask import Flask, Response

app = Flask(__name__)  # 注意：不传 static_folder 参数，或传 None

_HTML_PATH = os.path.join(BUNDLE, 'static', 'app.html')

@app.route('/')
@app.route('/app.html')
def index():
    """每次请求实时读取文件，绝不缓存（调试时改完即生效）"""
    try:
        with open(_HTML_PATH, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/html; charset=utf-8')
    except:
        return Response('<h1>加载失败</h1>', mimetype='text/html; charset=utf-8')
```

## 三种策略对比

| 策略 | 写法 | 适用 |
|------|------|------|
| 启动时读入内存 | `HTML = open(f).read()` 模块变量 | 生产环境，性能最优 |
| 每次请求读文件 | `open(f).read()` 在路由里 | 开发调试，改完刷新即生效 |
| 硬编码字符串 | `HTML = "<html>..."` | 极简单页，但难维护 |

**推荐：开发时用实时读取，打包前改成内存变量（减少 IO）。**

## 打包时的路径处理

```python
if getattr(sys, 'frozen', False):
    BUNDLE = sys._MEIPASS  # EXE 内部
else:
    BUNDLE = os.path.dirname(os.path.abspath(__file__))  # 源码目录

_HTML_PATH = os.path.join(BUNDLE, 'static', 'app.html')
```

静态文件（HTML/CSS/JS/图片）通过 `--add-data "static;static"` 打包进 EXE。
PyInstaller 运行时自动解压到 `sys._MEIPASS`。

## 注意事项

- CDN 引用的外部资源（如 `cdn.jsdelivr.net` 的 ExcelJS）不受影响
- 页面内引用的本地 JS/CSS 也要通过路由返回或用 `--add-data` 打包
- API 路由照常工作，只是静态文件不公开

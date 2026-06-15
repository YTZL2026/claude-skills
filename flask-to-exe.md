# Flask 单页应用 → 独立 EXE 打包

## 适用场景
任何 Flask 内部工具（台账/报表/管理后台），需要打包成双击即用的 Windows EXE，无需用户安装 Python。

## 极简服务器模板

```python
# server.py
import sys, os, webbrowser, threading, time

# === 路径自适应：EXE 和源码都能正确找到文件 ===
if getattr(sys, 'frozen', False):
    ROOT = os.path.dirname(sys.executable)    # EXE 所在目录
    BUNDLE = sys._MEIPASS                     # PyInstaller 临时解压目录
else:
    ROOT = os.path.dirname(os.path.abspath(__file__))
    BUNDLE = ROOT

from flask import Flask, Response
app = Flask(__name__)

# === HTML：每次请求实时读取，绝不缓存 ===
_HTML_PATH = os.path.join(BUNDLE, 'static', 'index.html')

@app.route('/')
def index():
    with open(_HTML_PATH, 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='text/html; charset=utf-8')

# === 你的 API 路由放这里 ===

# === 启动：自动打开浏览器 ===
def _open_browser():
    time.sleep(1)
    webbrowser.open('http://localhost:8081')

if __name__ == '__main__':
    threading.Thread(target=_open_browser, daemon=True).start()
    # 优先 waitress 生产服务器，失败降级 Flask dev
    try:
        from waitress import serve
        import logging
        logging.getLogger('waitress').setLevel(logging.WARNING)
        serve(app, host='0.0.0.0', port=8081, _quiet=True)
    except:
        app.run(host='0.0.0.0', port=8081, debug=False)
```

## PyInstaller 打包脚本模板

```python
# build_exe.py
import os, sys, shutil, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
ICO = 'app_icon.ico'

# 1. 安装依赖
subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', 'flask', 'waitress', '--quiet'])

# 2. Logo 转换（PNG → 多尺寸 ICO）
try:
    from PIL import Image
    img = Image.open('logo.png')
    img.save(ICO, format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
except: pass

# 3. 打包
icon = f'--icon="{ICO}"' if os.path.exists(ICO) else ''
cmd = (
    f'"{sys.executable}" -m PyInstaller '
    f'--onefile --noconsole --name="MyApp" {icon} '
    f'--add-data "static{os.pathsep}static" '
    f'--add-data "config.json{os.pathsep}." '
    f'--hidden-import=flask --hidden-import=waitress --hidden-import=webbrowser '
    f'--collect-all=flask '
    f'server.py'
)
subprocess.run(cmd, shell=True, cwd=BASE)

# 4. 复制数据文件到 dist/
for d in ['dist/data/subdir1', 'dist/data/subdir2']:
    os.makedirs(d, exist_ok=True)
# ... 复制业务数据 ...
```

## 关键配置

| 参数 | 作用 |
|------|------|
| `--onefile` | 打包为单个 EXE |
| `--noconsole` | 无黑窗（后台运行） |
| `--icon=app.ico` | 自定义图标 |
| `--add-data "src;dst"` | 把文件/目录嵌入 EXE |
| `--collect-all=flask` | 确保 Flask 所有模块被打包 |
| `sys._MEIPASS` | EXE 运行时，PyInstaller 解压文件的临时目录 |

## 迁移部署

1. 复制整个 `dist/` 到目标电脑
2. 目标电脑可能需要 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
3. 数据放 EXE 同级的 `data/` 目录
4. `config.json` 放 EXE 同级（用户可编辑）

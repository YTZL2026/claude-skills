# 全局文件搜索 API

## 适用场景
桌面工具需要让用户找到散落在项目目录各处的文件（XPS/JSON/图片/文档），不用手动指定路径，一键搜索自动发现。

## 服务端

```python
import os, json
from flask import jsonify

SEARCH_ROOT = 'C:/your-project-root'  # 搜索起点

@app.route('/api/search')
def global_search():
    result = {
        'xps': [],      # 按类型分组
        'txt': [],
        'json': [],
        'search_root': SEARCH_ROOT
    }
    for dirpath, dirnames, filenames in os.walk(SEARCH_ROOT):
        # 跳过无关目录
        dirnames[:] = [d for d in dirnames
                       if d not in ['__pycache__','.git','node_modules','build','.claude']]
        # 限制深度防止过慢
        depth = dirpath.replace(SEARCH_ROOT, '').count(os.sep)
        if depth > 6:
            dirnames[:] = []

        for f in filenames:
            fp = os.path.join(dirpath, f)
            rel = os.path.relpath(fp, SEARCH_ROOT)
            size_kb = os.stat(fp).st_size // 1024

            if f.lower().endswith('.xps'):
                result['xps'].append({'name':f, 'path':rel, 'dir':dirpath, 'size_kb':size_kb})
            elif f.endswith('.txt') and '_extracted' in dirpath:
                result['txt'].append({'name':f, 'path':rel, 'dir':dirpath, 'size_kb':size_kb})
            elif f.endswith('.json') and '_analysis' in dirpath:
                # 可读取摘要信息
                try:
                    with open(fp, 'r', encoding='utf-8') as jf:
                        d = json.load(jf)
                    result['json'].append({
                        'name':f, 'path':rel, 'dir':dirpath,
                        'summary': d.get('summary','')[:80]
                    })
                except:
                    result['json'].append({'name':f, 'path':rel, 'dir':dirpath})

    return jsonify(result)
```

## 前端调用

```javascript
async function doSearch() {
  const resp = await fetch('/api/search');
  const data = await resp.json();

  // 按类型渲染：data.xps / data.txt / data.json
  // 每个文件附带 path 字段，后续操作通过 path 定位
  data.json.forEach(f => {
    // 渲染带勾选框的列表，选中后可批量操作
  });
}

// 通过路径读取文件内容
async function readFile(path) {
  const resp = await fetch('/api/file-action', {
    method: 'POST',
    body: new URLSearchParams({ action: 'read', path: path })
  });
  return await resp.json();
}
```

## 关键设计

| 要点 | 说明 |
|------|------|
| 按文件类型分组返回 | 前端按 XPS/文本/JSON 分区展示 |
| 返回相对路径 | 前端不感知绝对路径，后续操作传回 path 参数 |
| 限制深度 | `depth > 6` 防止在大型项目中超时 |
| 跳过目录 | `__pycache__` 等开发目录必须跳过 |
| **不要跳过 `dist`** | EXE 运行后数据就在 dist 下，跳过会导致搜不到文件 |
| JSON 可带摘要 | 让用户无需点开就知道内容 |

## 配套 API：通过路径操作文件

```python
@app.route('/api/file-action', methods=['POST'])
def file_action():
    action = request.form.get('action')  # extract / analyze / read
    fpath = request.form.get('path')
    if not os.path.isabs(fpath):
        fpath = os.path.join(SEARCH_ROOT, fpath)
    # 根据 action 执行对应操作...
```

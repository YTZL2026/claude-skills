---
name: bookmark-fix
description: 浏览器书签修复 — 诊断书签文件膨胀 → 去重清理 → 恢复浏览器正常使用。当用户说"收藏夹打不开""书签无限重复""收藏夹卡死""浏览器收藏夹崩了"时使用。
---

# Bookmark Fix Skill

一键诊断和修复 Chromium 系浏览器（Chrome/Edge/Tabbit）书签文件膨胀导致的收藏夹卡死/崩溃问题。

## 触发条件

用户说以下任意一句时调用此技能：
- "收藏夹打不开了"
- "书签无限重复"
- "/bookmark-fix"
- "收藏夹卡死"
- "浏览器收藏夹崩了"
- "书签栏一直加载"

## 问题原理

Chromium 系浏览器的书签存储在本地 JSON 文件中（`User Data/Default/Bookmarks`）。当账号跨设备同步时，sync 引擎在某些情况下会产生死循环——同一个书签被反复复制，导致文件膨胀到几十 MB、包含数万乃至数十万条重复条目。浏览器打开收藏夹时需要解析整个 JSON，IO 和内存双双爆炸，表现为点击收藏夹后长时间卡死甚至浏览器崩溃。

## 执行流程

### Phase 1：定位书签文件

根据用户使用的浏览器确定 `Bookmarks` 文件路径：

| 浏览器 | 路径 |
|--------|------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks` |
| Edge | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks` |
| Tabbit | `%LOCALAPPDATA%\Tabbit Browser\User Data\Default\Bookmarks` |
| Brave | `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks` |

先让用户确认浏览器类型，然后检查文件大小：

```bash
ls -lh "<书签文件路径>"
```

正常书签文件应该 < 1 MB，行数 < 10000。如果超过 10 MB 或 10 万行，判定为膨胀。

### Phase 2：分析重复情况

```bash
grep -c '"name"' <书签文件路径>           # 总书签条数
grep '"name"' <书签文件路径> | sort | uniq -c | sort -rn | head -20  # Top 20 重复标题
```

找出重复最多的书签标题和数量，向用户确认问题。

### Phase 3：告知用户关闭浏览器

**必须**先让用户完全关闭浏览器（任务栏右键退出，确认任务管理器中没有残留进程）。浏览器运行时会持有 Bookmarks 文件锁并可能覆盖修改。

### Phase 4：运行修复脚本

使用 `fix_bookmarks.py`（位于本 skill 目录下）：

```bash
python fix_bookmarks.py
```

脚本自动完成：
1. 备份原文件（`.backup_YYYYMMDD_HHMMSS`）
2. 解析 JSON 书签树
3. 递归查找重复条目（默认去重最多的那一条，可通过参数指定）
4. 保留 1 条，删除其余重复
5. 写回清理后的文件
6. 输出前后对比统计

### Phase 5：验证

- 新文件大小应恢复正常（几十 KB）
- 提示用户重新打开浏览器
- 让用户确认收藏夹是否恢复正常

## 脚本参数

```bash
python fix_bookmarks.py                          # 默认：去重"百度一下，你就知道"
python fix_bookmarks.py --name "其他重复标题"    # 去重指定标题
python fix_bookmarks.py --keep 3                 # 保留 3 条而非默认 1 条
```

## 支持的浏览器

- **Chromium 内核浏览器**全系通用（Chrome / Edge / Tabbit / Brave / Opera / Vivaldi / 360 / QQ 等）
- 本质上就是操作 Chromium 的 Bookmarks JSON 文件

## 安全措施

- **自动备份**：修复前创建带时间戳的 `.backup` 文件
- **只删除重复**：不会动其他正常书签
- **可回滚**：如果出问题，把备份文件重命名为 `Bookmarks` 即可恢复

## 注意事项

- **必须关闭浏览器再运行脚本**，否则修改会被覆盖
- 如果用户的重复书签名称不是"百度一下，你就知道"，用 `--name` 参数指定
- 备份文件保留在原目录，确认无误后可手动删除以释放空间
- 此问题根源在 Chromium Sync 引擎的 bug，建议定期检查书签文件大小
- 长期建议：不要同时在 3 台以上设备登录同一浏览器账号并开同步

## 关联技能

- `/github-fix` — 同样是一键修复类工具，解决网络层问题

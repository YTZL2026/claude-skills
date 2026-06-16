---
name: disk-fix
description: 移动硬盘盘符修复 — 诊断离线原因 → 上线磁盘 → 分配盘符 → 修改SAN策略 → 禁用USB省电。根治移动硬盘/U盘反复掉盘符问题。当用户说"移动硬盘不显示""盘符丢了""U盘读不出来""硬盘连上没反应"时使用。
---

# Disk Fix Skill

一键诊断和修复 Windows 下移动硬盘/U盘盘符丢失问题，三步根治反复掉盘。

## 触发条件

用户说以下任意一句时调用此技能：
- "移动硬盘不显示了"
- "盘符又找不到了"
- "/disk-fix"
- "U盘读不出来"
- "硬盘连上没反应"
- "外置硬盘盘符丢了"
- "昨天还能用今天又不行了"

## 问题原理

Windows 对 USB 外置磁盘默认执行 **SAN Policy**（Storage Area Network 策略），该策略会将外置磁盘标记为"离线（Offline）"以保护数据。但对于普通移动硬盘/U盘，这个策略适得其反——每次插拔或重启后，磁盘被踢下线，盘符消失。

三个根因叠加：
1. **SAN Policy = OfflineShared**（默认）→ Windows 主动踢下线
2. **USB 选择性暂停** → 省电策略让 USB 控制器休眠，磁盘随之离线
3. **磁盘未自动上线** → 即便物理连接正常，逻辑层仍是 Offline

## 执行流程

### Phase 1：诊断（3 秒）

确认物理磁盘状态：

```powershell
# 列出所有物理磁盘
Get-PhysicalDisk | Select FriendlyName, MediaType, OperationalStatus, BusType, Size

# 列出所有磁盘（含逻辑状态）
Get-Disk | Select Number, FriendlyName, OperationalStatus, OfflineReason, BusType

# 检查分区和盘符
Get-Disk -Number <N> | Get-Partition | Select DriveLetter, Size, OperationalStatus
```

诊断关键指标：
- `OperationalStatus: Offline` + `OfflineReason: Policy` → SAN 策略导致，需要修复
- `OperationalStatus: OK` 但 `DriveLetter` 为空 → 纯盘符丢失，只需分配盘符
- `HealthStatus: Warning` → 硬盘硬件问题，非本 skill 范畴

### Phase 2：生成修复脚本

根据诊断结果，生成对应的 `fix_disk.bat`（位于本 skill 目录下），包含三板斧：

**第一板：立刻上线 + 分配盘符**
```bat
diskpart /s script.txt
  select disk <N>
  online disk
  attributes disk clear readonly
  select partition 1
  assign letter=<X>
```

**第二板：改 SAN 策略（根治）**
```bat
diskpart /s script.txt
  SAN POLICY=OnlineAll
```

**第三板：禁用 USB 省电**
```bat
powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53c8e1a2a1a2 0
powercfg /SETDCVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53c8e1a2a1a2 0
powercfg /S SCHEME_CURRENT
```

### Phase 3：告知用户执行

**必须右键 → 以管理员身份运行** `fix_disk.bat`。

diskpart 操作需要管理员权限，无法绕过。

### Phase 4：验证

```powershell
Get-PSDrive -PSProvider FileSystem | Select Name, Used, Free
```

确认盘符已出现。打开资源管理器验证可正常访问。

## 支持的设备

- USB 移动硬盘（HDD/SSD）
- U盘 / 闪存盘
- 所有 Windows 10/11 系统

## 常见盘符分配

| 盘符 | 说明 |
|------|------|
| A: B: | 传统软驱，一般不分配 |
| C: | 系统盘 |
| D: E: | 常见内置分区 |
| F: G: H: | 推荐外置磁盘使用 |

选择当前未被占用的盘符。若不确定，脚本会自动选择首个可用盘符。

## 安全措施

- 只 online 磁盘和分配盘符，不格式化、不删除数据
- SAN Policy 改为 OnlineAll 是 Windows 官方支持的操作
- USB 省电禁用仅影响 USB 控制器不休眠，不影响其他电源策略
- 可通过 `SAN POLICY=OfflineShared` 恢复默认策略

## 注意事项

- **必须管理员权限**（diskpart 硬性要求，提示 UAC 弹窗点"是"）
- 如果移动硬盘之前被弹出过（安全移除硬件），需要重新插拔后再运行脚本
- SAN Policy 修改后永久生效，重装系统后需重新设置
- 极少数企业 IT 策略可能锁定 SAN Policy，此情况下需联系 IT 部门

## 关联技能

- `/bookmark-fix` — 同样是一键修复类工具，解决浏览器层膨胀问题
- `/github-fix` — 一键修复 GitHub 访问问题，解决网络层连通

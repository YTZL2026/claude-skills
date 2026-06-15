---
name: github-fix
description: GitHub 访问修复 — 诊断 + 切换可用 IP + 更新 hosts。当用户说"GitHub 上不去""github 登录失败""github 又不行了""VS Code 登录 GitHub 报错"时使用。
---

# GitHub Access Fix Skill

一键诊断和修复公司网络下 GitHub 访问问题（DNS 污染 + TCP 封锁 + TLS SNI 检测）。

## 触发条件

用户说以下任意一句时调用此技能：
- "GitHub 又上不去了"
- "/github-fix"
- "修复 GitHub"
- "github 登录失败"
- "VS Code 登录 GitHub 报错"
- "github.com 打不开"

## 执行流程

### Phase 1：诊断（3 秒）

```powershell
# 检查 hosts 文件完整性
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String -Pattern "github"

# 检查 DNS 解析
Resolve-DnsName github.com | Select-Object Name, IPAddress

# 检查 TCP 连通性
Test-NetConnection github.com -Port 443 -WarningAction SilentlyContinue | Select-Object RemoteAddress, TcpTestSucceeded
```

如 hosts 条目格式正常、DNS 指向 hosts IP、TCP 通 → 跳到 Phase 4。否则继续。

### Phase 2：扫描可用 IP（5 秒）

从 IP 池中找当前可用的：

```powershell
$pool = @(
    "140.82.114.4", "140.82.113.4", "140.82.112.4",
    "140.82.114.3", "140.82.112.3",
    "20.27.177.113", "20.205.243.166",
    "185.199.108.153", "185.199.109.153", "185.199.110.153"
)

$working = @()
foreach ($ip in $pool) {
    $tcp = Test-NetConnection $ip -Port 443 -WarningAction SilentlyContinue -InformationLevel Quiet
    if (-not $tcp) { continue }
    # TCP 通还要验证 HTTPS
    try {
        $r = Invoke-WebRequest -Uri "https://$ip" -TimeoutSec 5 -UseBasicParsing -Headers @{"Host"="github.com"}
        Write-Host "WORKING: $ip (HTTP $($r.StatusCode))"
        $working += $ip
    } catch {
        Write-Host "TCP_ONLY: $ip (HTTPS blocked by SNI filter)"
    }
}

if ($working.Count -eq 0) {
    Write-Host "ERROR: 所有 IP 都不可用，可能防火墙升级了策略，需用代理/VPN"
    exit 1
}

$chosenIP = $working[0]
Write-Host "CHOSEN: $chosenIP"
```

### Phase 3：更新 hosts（需管理员权限）

```powershell
$chosenIP = "<上一步选出的 IP>"
$tempPath = "$env:TEMP\hosts_github_fix"
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

$content = Get-Content $hostsPath
$clean = $content | Where-Object { $_ -notmatch "github" }

# vscode-auth/github.io 如果 IP 在 185.199 段就用 Pages IP，否则也指给主站 IP
if ($chosenIP -like "185.199.*") {
    # Pages IP 段，vscode-auth 用这个，github.com 也试试
    $clean += "$chosenIP github.com"
    $clean += "$chosenIP vscode-auth.github.com"
    $clean += "$chosenIP github.github.io"
    # API 和 codeload 需要主站 IP
    $clean += "140.82.114.4 api.github.com"
    $clean += "140.82.114.4 codeload.github.com"
} else {
    # 主站 IP 段，所有域名统一指向
    $clean += "$chosenIP github.com"
    $clean += "$chosenIP api.github.com"
    $clean += "$chosenIP codeload.github.com"
    $clean += "$chosenIP vscode-auth.github.com"
    $clean += "$chosenIP github.github.io"
}

$clean | Set-Content $tempPath -Encoding ASCII
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -Command Copy-Item '$tempPath' '$hostsPath' -Force; ipconfig /flushdns" -Wait

Write-Host "Hosts updated with $chosenIP"
```

### Phase 4：验证（2 秒）

```powershell
ipconfig /flushdns

$tests = @(
    @{Url="https://github.com"; Name="github.com 主站"},
    @{Url="https://api.github.com"; Name="api.github.com API"},
    @{Url="https://vscode-auth.github.com"; Name="vscode-auth 回调"}
)

foreach ($t in $tests) {
    try {
        $r = Invoke-WebRequest -Uri $t.Url -TimeoutSec 8 -UseBasicParsing -MaximumRedirection 0
        Write-Host "[OK] $($t.Name)"
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        if ($code -ge 200 -and $code -lt 400) {
            Write-Host "[OK] $($t.Name) (redirect $code)"
        } else {
            Write-Host "[FAIL] $($t.Name)"
        }
    }
}
```

### Phase 5：报告

向用户报告：
- 使用哪个 IP
- 当前 hosts 文件内容
- 建议：浏览器打开 `https://github.com` 验证，VS Code 重新登录

## 核心 IP 池

<!-- 每次修复成功后更新此表 -->

| IP | 上次验证 | 备注 |
|----|---------|------|
| 140.82.114.4 | 2026-06-15 | 当前主力 |
| 140.82.113.4 | 2026-06-15 | 备选 |
| 20.27.177.113 | 2026-06-15 | 备选 |
| 185.199.108.153 | 2026-06-15 | GitHub Pages，vscode-auth 用 |

## 注意事项

- **不要用 `Add-Content -Value`**：会把 `-Value` 写进文件，改用数组追加 + `Set-Content`
- **`Test-NetConnection` 不够**：TCP True 不代表 HTTPS 能通，必须做 HTTP 层验证
- **管理员权限**：告诉用户看到 UAC 弹窗要点"是"
- **IP 轮换**：如果修复后很快又封，直接换另一个 IP 再跑一遍
- **长期方案**：建议装 Clash/Clash Verge/V2RayN，单位网络迟早封完所有 GitHub IP

## 关联技能

- `/batch-import` — 批量导入（OCR 模型下载依赖 GitHub 连通）

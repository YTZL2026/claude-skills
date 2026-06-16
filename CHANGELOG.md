## 2026-06-16 (later) — v1.3

### Added: `disk-fix` skill

**Problem:**
WD Elements 1TB USB HDD kept losing its drive letter after reconnection. Windows SAN Policy default ("OfflineShared") forcibly takes external disks offline. Combined with USB selective suspend, the drive letter disappears every time the disk is re-plugged or the system wakes from sleep.

**Solution:**
A 3-in-1 batch script that permanently fixes the issue:
1. Online the disk + assign drive letter (immediate fix)
2. Set SAN POLICY=OnlineAll (permanent — disk auto-mounts on reconnect)
3. Disable USB selective suspend (prevent power-saving from dropping the connection)

**Results:**
- Immediate: Drive F: accessible again
- Permanent: No more drive letter loss after unplug/replug/reboot

**Files:**
- `disk-fix/skill.md` — Skill definition with full diagnostic + fix workflow
- `disk-fix/fix_disk.bat` — One-click batch script (requires admin)

---

# Changelog

## 2026-06-16 — v1.2

### Added: `bookmark-fix` skill

**Problem:**
Tabbit browser bookmarks file ballooned to 56.9 MB (106,547 entries) due to a Chromium sync engine bug that duplicated a single "Baidu" bookmark 106,516 times. Opening the bookmarks manager caused the browser to freeze and crash.

**Solution:**
A Python script that directly operates on the Chromium `Bookmarks` JSON file:
- Auto-detects browser type (Chrome/Edge/Tabbit/Brave)
- Creates a timestamped backup before any modification
- Recursively walks the bookmark tree, removing duplicate entries by name
- Supports `--name`, `--keep`, `--path`, `--dry-run` CLI arguments

**Results:**
- Before: 106,547 bookmarks, 56.9 MB
- After: 32 bookmarks, 23.8 KB
- Reduction: 99.97% of entries removed, file size reduced 2400x

**Files:**
- `bookmark-fix/skill.md` — Skill definition with full workflow
- `bookmark-fix/fix_bookmarks.py` — Portable cleanup script (Chromium-universal)

---

## 2026-06-15 — v1.1

### Added
- `batch-import` skill (multi-format medical record import)
- `character-design-sheet` skill
- `storyboard-9-grid` / `storyboard-25-grid` skills
- `image-consistency-supplement` skill
- `read-image` skill
- `migrate-package` skill

### Infrastructure
- Repo initialized: `github.com/YTZL2026/claude-skills`
- CC0-1.0 license

---

## 2026-06-11 — v1.0

### Added
- `github-fix` skill (GitHub access repair via hosts + IP rotation)
- `flask-to-exe` skill
- `html-embed-flask` skill
- `global-file-search-api` skill
- `ai-structured-inspection` skill
- `exceljs-export-template` skill

"""
Bookmark Fix - Clean duplicated bookmarks in Chromium-based browsers
Usage: python fix_bookmarks.py [--name NAME] [--keep N] [--path PATH]
"""
import json
import shutil
import os
import sys
import argparse
from datetime import datetime


def get_bookmarks_path(browser=None):
    """Detect or return specified bookmarks path."""
    if browser:
        return browser

    localappdata = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        # Tabbit
        os.path.join(localappdata, "Tabbit Browser", "User Data", "Default", "Bookmarks"),
        # Chrome
        os.path.join(localappdata, "Google", "Chrome", "User Data", "Default", "Bookmarks"),
        # Edge
        os.path.join(localappdata, "Microsoft", "Edge", "User Data", "Default", "Bookmarks"),
        # Brave
        os.path.join(localappdata, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Bookmarks"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def count_bookmarks(data):
    """Recursively count all URL-type bookmarks."""
    total = 0
    if isinstance(data, dict):
        if data.get("type") == "url":
            total += 1
        for v in data.values():
            total += count_bookmarks(v)
    elif isinstance(data, list):
        for item in data:
            total += count_bookmarks(item)
    return total


def dedup_bookmarks(data, target_name, keep_count, stats):
    """Recursively find and deduplicate bookmarks with target_name.
    Keeps the first `keep_count` occurrences, removes the rest.
    `stats` is a dict with 'seen' and 'removed' counters.
    """
    if isinstance(data, dict):
        if "children" in data and isinstance(data["children"], list):
            new_children = []
            for child in data["children"]:
                if isinstance(child, dict) and child.get("type") == "url":
                    if child.get("name") == target_name:
                        if stats["seen"] < keep_count:
                            stats["seen"] += 1
                            new_children.append(child)  # keep this one
                        else:
                            stats["removed"] += 1  # discard
                        continue
                # Recursively process child (including folders)
                dedup_bookmarks(child, target_name, keep_count, stats)
                new_children.append(child)
            data["children"] = new_children
        else:
            for v in data.values():
                dedup_bookmarks(v, target_name, keep_count, stats)
    elif isinstance(data, list):
        for item in data:
            dedup_bookmarks(item, target_name, keep_count, stats)


def main():
    parser = argparse.ArgumentParser(
        description="Fix bloated Chromium bookmarks by removing duplicates"
    )
    parser.add_argument(
        "--name", type=str, default="百度一下，你就知道",
        help="Target bookmark name to deduplicate (default: %(default)s)"
    )
    parser.add_argument(
        "--keep", type=int, default=1,
        help="Number of copies to keep (default: %(default)s)"
    )
    parser.add_argument(
        "--path", type=str, default=None,
        help="Path to Bookmarks file (auto-detect if not specified)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Only show what would be done, don't modify the file"
    )
    args = parser.parse_args()

    bookmarks_path = get_bookmarks_path(args.path)
    if not bookmarks_path:
        print("ERROR: Could not find Bookmarks file. Use --path to specify.")
        sys.exit(1)

    if not os.path.exists(bookmarks_path):
        print(f"ERROR: File not found: {bookmarks_path}")
        sys.exit(1)

    # 1. Show info
    size_mb = os.path.getsize(bookmarks_path) / 1024 / 1024
    print(f"Browser bookmarks file: {bookmarks_path}")
    print(f"File size: {size_mb:.1f} MB")

    if args.dry_run:
        # Just count without modifying
        with open(bookmarks_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        total = count_bookmarks(data)

        # Count occurrences of target name
        def count_name(d, name):
            c = 0
            if isinstance(d, dict):
                if d.get("type") == "url" and d.get("name") == name:
                    c += 1
                for v in d.values():
                    c += count_name(v, name)
            elif isinstance(d, list):
                for item in d:
                    c += count_name(item, name)
            return c

        dup_count = count_name(data, args.name)
        print(f"Total bookmarks: {total}")
        print(f"Occurrences of '{args.name}': {dup_count}")
        if dup_count > args.keep:
            print(f"[DRY RUN] Would remove {dup_count - args.keep} duplicates, keep {args.keep}")
        else:
            print("No action needed.")
        return

    # 2. Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = bookmarks_path + f".backup_{timestamp}"
    print(f"Backing up to: {backup_path}")
    shutil.copy2(bookmarks_path, backup_path)

    # 3. Read
    print("Reading bookmarks file...")
    with open(bookmarks_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    before = count_bookmarks(data)
    print(f"Total bookmarks before cleanup: {before}")

    # 4. Dedup
    stats = {"seen": 0, "removed": 0}
    dedup_bookmarks(data, args.name, args.keep, stats)

    after = count_bookmarks(data)
    print(f"Deleted {stats['removed']} duplicate '{args.name}' bookmarks")
    print(f"Kept {stats['seen']} copy/copies")
    print(f"Total bookmarks after cleanup: {after}")

    if stats["removed"] == 0:
        print("No duplicates found. File unchanged.")
        return

    # 5. Write back
    print("Writing cleaned file...")
    with open(bookmarks_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

    new_size_kb = os.path.getsize(bookmarks_path) / 1024
    print(f"Done! New file size: {new_size_kb:.1f} KB (was {size_mb:.1f} MB)")
    print(f"Backup kept at: {backup_path}")
    print("\nYou can now reopen your browser. Bookmarks should load instantly!")


if __name__ == "__main__":
    main()

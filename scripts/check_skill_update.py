#!/usr/bin/env python3
"""Check whether skill directories have pending git updates or local changes.

Usage: check_skill_update.py [DIR ...] [--fetch]

Inspects git status and branch tracking for skill directories.
When no directory is specified, checks default skill locations:
- current directory
- ~/.copilot/skills
- ~/.gemini/antigravity-cli/skills
- ~/.gemini/config/skills
- ~/.claude/skills
- ~/.agents/skills
"""

import argparse
import os
import subprocess
import sys

DEFAULT_HOMES = [
    ".",
    os.path.expanduser("~/.copilot/skills"),
    os.path.expanduser("~/.gemini/antigravity-cli/skills"),
    os.path.expanduser("~/.gemini/config/skills"),
    os.path.expanduser("~/.claude/skills"),
    os.path.expanduser("~/.agents/skills"),
]


def run_git(cmd, cwd, timeout=10):
    try:
        res = subprocess.run(
            ["git", "-C", cwd] + cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as exc:
        return 1, "", str(exc)


def inspect_skill_repo(target_dir, fetch=True):
    path = os.path.abspath(target_dir)
    if not os.path.isdir(path):
        return {"path": path, "status": "missing", "detail": "directory not found"}

    code, toplevel, _ = run_git(["rev-parse", "--show-toplevel"], path)
    if code != 0 or not toplevel:
        return {"path": path, "status": "not_git", "detail": "not a git repository"}

    repo_dir = toplevel
    if fetch:
        # Dry-run fetch to see if upstream has newer commits without altering local branches
        run_git(["fetch", "--dry-run"], repo_dir, timeout=8)

    code, status_out, _ = run_git(["status", "--short", "--branch"], repo_dir)
    if code != 0:
        return {"path": repo_dir, "status": "error", "detail": "git status failed"}

    lines = status_out.splitlines()
    branch_line = lines[0] if lines else "## unknown"
    dirty_files = [line for line in lines[1:] if line.strip()]

    is_behind = "behind" in branch_line
    is_ahead = "ahead" in branch_line
    is_diverged = is_behind and is_ahead
    is_dirty = len(dirty_files) > 0

    if is_diverged:
        status = "diverged"
        detail = branch_line.lstrip("# ").strip()
    elif is_behind:
        status = "behind"
        detail = branch_line.lstrip("# ").strip()
    elif is_ahead:
        status = "ahead"
        detail = branch_line.lstrip("# ").strip()
    elif is_dirty:
        status = "dirty"
        detail = f"{len(dirty_files)} uncommitted file(s)"
    else:
        status = "clean"
        detail = branch_line.lstrip("# ").strip()

    return {
        "path": repo_dir,
        "status": status,
        "detail": detail,
        "branch_line": branch_line,
        "dirty_count": len(dirty_files),
        "is_behind": is_behind,
    }


def main():
    parser = argparse.ArgumentParser(description="Check git status for skill directories.")
    parser.add_argument("dirs", nargs="*", help="Skill directories to inspect")
    parser.add_argument("--fetch", action="store_true", default=True, help="Fetch from remote (default: True)")
    parser.add_argument("--no-fetch", action="store_false", dest="fetch", help="Skip remote fetch")
    args = parser.parse_args()

    targets = args.dirs if args.dirs else DEFAULT_HOMES
    seen = set()
    results = []

    for item in targets:
        real = os.path.realpath(os.path.abspath(item))
        if real in seen or not os.path.isdir(real):
            continue
        seen.add(real)
        results.append(inspect_skill_repo(real, fetch=args.fetch))

    if not results:
        print("No existing skill directories found to check.")
        return 0

    print("Skill folder update check:")
    has_behind = False
    for r in results:
        path = r["path"]
        status = r["status"]
        detail = r.get("detail", "")
        if status == "behind" or status == "diverged":
            has_behind = True
            print(f"  [STALE] {path}: {detail} (run 'git -C {path} pull' to update)")
        elif status == "clean":
            print(f"  [OK]    {path}: up to date ({detail})")
        elif status == "dirty":
            print(f"  [INFO]  {path}: local changes present ({detail})")
        elif status == "ahead":
            print(f"  [INFO]  {path}: ahead of upstream ({detail})")
        elif status == "not_git":
            print(f"  [INFO]  {path}: not a git repository (standalone files)")
        else:
            print(f"  [INFO]  {path}: {status} ({detail})")

    if has_behind:
        print("\nOne or more skill folders have updates available upstream.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

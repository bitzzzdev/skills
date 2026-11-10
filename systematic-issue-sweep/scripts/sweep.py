#!/usr/bin/env python3
"""Sweep workspace for recurring issues, typos, anti-patterns, or logic flaws.

Usage:
    python sweep.py PATTERN [PATH ...]
    python sweep.py --regex REGEX [PATH ...]
    python sweep.py --count-only PATTERN [PATH ...]

Scans files across the workspace, ignoring binary files, build artifacts,
and version control directories. Reports every occurrence with file path,
line number, and matching context.
"""

import argparse
import os
import re
import sys

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", ".venv", "venv",
    "__pycache__", "coverage", ".cache", "vendor", ".turbo", ".vercel", "out",
    ".idea", ".vscode", "target", "bin", "obj",
}
SKIP_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "Cargo.lock",
}
SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg", ".pdf", ".zip",
    ".gz", ".tar", ".woff", ".woff2", ".ttf", ".otf", ".mp3", ".mp4", ".mov",
    ".webm", ".map", ".class", ".jar", ".exe", ".dll", ".so", ".pyc", ".bin",
}
MAX_BYTES = 1_000_000


def is_text(data):
    return b"\x00" not in data[:4096]


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in files:
                    if name in SKIP_FILES or name.endswith(".min.js") or name.endswith(".min.css"):
                        continue
                    if os.path.splitext(name)[1].lower() in SKIP_EXT:
                        continue
                    yield os.path.join(root, name)
        else:
            yield p


def snippet(line, start, end, width=40):
    a = max(0, start - width)
    b = min(len(line), end + width)
    return line[a:b].strip()


def sweep_path(path, regex):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return []
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return []

    if not is_text(data):
        return []

    text = data.decode("utf-8", errors="ignore")
    matches = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in regex.finditer(line):
            matches.append((lineno, m.start() + 1, snippet(line, m.start(), m.end())))
    return matches


def main():
    ap = argparse.ArgumentParser(
        description="Sweep workspace for recurring issue patterns or logic flaws."
    )
    ap.add_argument("pattern", help="text pattern or regular expression to sweep for")
    ap.add_argument("paths", nargs="*", default=["."], help="files or directories to sweep (default: current dir)")
    ap.add_argument("--regex", "-r", action="store_true", help="treat pattern as regular expression")
    ap.add_argument("--case-sensitive", "-c", action="store_true", help="case-sensitive match")
    ap.add_argument("--count-only", action="store_true", help="only print total match count")
    ap.add_argument("--quiet", "-q", action="store_true", help="suppress line snippets")
    args = ap.parse_args()

    flags = 0 if args.case_sensitive else re.IGNORECASE
    try:
        if args.regex:
            rx = re.compile(args.pattern, flags)
        else:
            rx = re.compile(re.escape(args.pattern), flags)
    except re.error as exc:
        print("Invalid pattern regex: %s" % exc, file=sys.stderr)
        return 2

    files_with_matches = 0
    total_matches = 0

    for path in iter_files(args.paths):
        matches = sweep_path(path, rx)
        if not matches:
            continue
        files_with_matches += 1
        total_matches += len(matches)

        if args.count_only:
            continue

        for lineno, col, ctx in matches:
            if args.quiet:
                print("%s:%d:%d" % (path, lineno, col))
            else:
                print("%s:%d:%d: %s" % (path, lineno, col, ctx))

    if args.count_only:
        print(total_matches)
    else:
        print(
            "\nSweep complete: %d occurrence(s) across %d file(s)."
            % (total_matches, files_with_matches),
            file=sys.stderr,
        )

    return 1 if total_matches > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

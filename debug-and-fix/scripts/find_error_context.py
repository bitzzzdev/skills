#!/usr/bin/env python3
"""Pull file locations and identifiers out of an error log or stack trace,
then show the matching source lines with context.

usage: find_error_context.py LOGFILE_OR_- [--root DIR] [--context N]
Use - to read the log from stdin.
"""
import argparse
import os
import re
import sys

LOC_PATTERNS = [
    re.compile(r'File "([^"]+)", line (\d+)'),                    # Python
    re.compile(r'at (?:[^\s(]+ )?\(?([^\s():]+\.\w+):(\d+)(?::\d+)?\)?'),  # JS/Node
    re.compile(r'([\w./\\-]+\.\w{1,5}):(\d+)(?::\d+)?'),          # generic path:line
    re.compile(r'([\w./\\-]+\.go):(\d+)'),                        # Go
    re.compile(r'--> ([^\s:]+):(\d+):\d+'),                       # Rust
]
ERR_NAME = re.compile(r'\b([A-Z][A-Za-z]*(?:Error|Exception|Warning)|panic|FATAL|ERROR)\b[:\s]?(.*)')
QUOTED = re.compile(r"[`'\"]([A-Za-z_][\w.]{2,})[`'\"]")
SKIP_DIRS = ("node_modules", "site-packages", "/usr/lib", "dist-packages", ".git/")


def find_locations(text):
    seen, out = set(), []
    for rx in LOC_PATTERNS:
        for m in rx.finditer(text):
            path, line = m.group(1), int(m.group(2))
            if any(s in path for s in SKIP_DIRS):
                continue
            if (path, line) not in seen:
                seen.add((path, line))
                out.append((path, line))
    return out


def resolve(path, root):
    if os.path.isfile(path):
        return path
    base = os.path.basename(path)
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "venv", ".venv", "__pycache__")]
        if base in files:
            return os.path.join(dirpath, base)
    return None


def show(path, line, ctx):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        print("  cannot read %s: %s" % (path, e))
        return
    lo, hi = max(0, line - 1 - ctx), min(len(lines), line + ctx)
    for i in range(lo, hi):
        mark = ">>" if i == line - 1 else "  "
        print("%s %5d  %s" % (mark, i + 1, lines[i].rstrip()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--root", default=".")
    ap.add_argument("--context", type=int, default=4)
    a = ap.parse_args()

    text = sys.stdin.read() if a.log == "-" else open(a.log, encoding="utf-8", errors="replace").read()

    print("== Error lines ==")
    errs = [m for m in (ERR_NAME.search(l) for l in text.splitlines()) if m]
    for m in errs[:10]:
        print("  " + m.group(0).strip()[:200])
    if not errs:
        print("  none matched, read the log by hand")

    idents = sorted({m.group(1) for m in QUOTED.finditer(text)})[:15]
    if idents:
        print("\n== Identifiers worth grepping ==")
        print("  " + ", ".join(idents))

    print("\n== Source locations ==")
    locs = find_locations(text)
    if not locs:
        print("  no file:line references found")
    for path, line in locs[:12]:
        real = resolve(path, a.root)
        print("\n%s:%d%s" % (path, line, "" if real else "  (not found under %s)" % a.root))
        if real:
            show(real, line, a.context)


if __name__ == "__main__":
    main()

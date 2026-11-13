#!/usr/bin/env python3
"""Reject emoji and emoji-like symbols in files changed by the current commit."""

import subprocess
import sys
from pathlib import Path

EMOJI = __import__("re").compile(
    "[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\u2B50\\u2B55\\u2B1B\\u2B1C"
    "\\u231A\\u231B\\u23E9-\\u23FA\\u2934\\u2935\\u3030\\u303D\\u3297\\u3299"
    "\\uFE0F\\u200D]"
)
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".woff", ".woff2", ".ttf", ".otf", ".mp3", ".mp4", ".jar", ".class", ".bin"}
SKIP_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "Cargo.lock", "bun.lockb"}

def changed_paths():
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        check=True, capture_output=True, text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line]

def main():
    errors = []
    for path in changed_paths():
        if not path.is_file() or path.name in SKIP_NAMES or path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(content.splitlines(), 1):
            if EMOJI.search(line):
                errors.append(f"{path}:{number}: emoji or emoji-like symbol is prohibited")
    if errors:
        print("\\n".join(errors))
        return 1
    print("Changed-file emoji policy passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

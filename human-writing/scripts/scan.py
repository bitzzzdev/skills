#!/usr/bin/env python3
"""Scan text or code for common AI writing tells and owner-voice issues."""

import argparse
import os
import re
import sys

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", ".venv", "venv",
    "__pycache__", "coverage", ".cache", "vendor", ".turbo", ".vercel", "out",
}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "Cargo.lock"}
SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg", ".pdf", ".zip",
    ".gz", ".tar", ".woff", ".woff2", ".ttf", ".otf", ".mp3", ".mp4", ".mov",
    ".webm", ".map", ".class", ".jar", ".exe", ".dll", ".so", ".pyc", ".bin",
}
MAX_BYTES = 1_000_000

HARD = [
    ("em dash", re.compile("\u2014")),
    ("horizontal bar", re.compile("\u2015")),
    ("en dash", re.compile("\u2013")),
    (
        "emoji or decorative symbol",
        re.compile(
            "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u2B1B\u2B1C"
            "\u231A\u231B\u23E9-\u23FA\u2934\u2935\u3030\u303D\u3297\u3299"
            "\uFE0F\u200D]"
        ),
    ),
]

WORDS = [
    "delve", "leverage", "utilize", "harness", "unlock", "unleash", "elevate",
    "empower", "foster", "streamline", "supercharge", "embark", "showcase",
    "underscore", "resonate", "revolutionize", "enhance", "facilitate",
    "bolster", "spearhead", "cultivate", "seamless", "robust", "comprehensive",
    "crucial", "pivotal", "paramount", "cutting-edge", "state-of-the-art",
    "innovative", "dynamic", "meticulous", "intricate", "nuanced",
    "multifaceted", "holistic", "transformative", "groundbreaking",
    "game-changing", "tailored", "bespoke", "effortless", "intuitive",
    "user-centric", "feature-rich", "best-in-class", "tapestry", "testament",
    "realm", "journey", "synergy", "beacon", "cornerstone", "plethora",
    "myriad", "paradigm", "game-changer", "takeaway", "pain points",
]

PHRASES = [
    r"it's (important|worth) (to )?(note|noting|mention|mentioning)",
    r"in today's (fast-paced|digital|modern|ever)",
    r"ever-evolving",
    r"plays? an? (crucial|pivotal|vital|key|important) role",
    r"a testament to",
    r"at the end of the day",
    r"when it comes to",
    r"dive into",
    r"deep dive",
    r"let's (explore|unpack|break (this|it) down|dive)",
    r"whether you're an? .{1,40} or an? ",
    r"look no further",
    r"the key takeaway",
    r"in order to",
    r"due to the fact that",
    r"great question",
    r"i'd be (happy|glad) to",
    r"i hope this (email )?(helps|finds you)",
    r"feel free to (reach out|ask|contact)",
    r"not (just|only|merely) .{1,60}\bbut( also)?\b",
    r"\b(in conclusion|in summary|to summarize|to sum up)\b",
    r"engineering and writing standards",
    r"every paper documents (observed behavior|verified endpoints)",
    r"all prose follows (strict )?(human writing|writing) standards",
    r"configurations must include exact file locations",
    r"every (paper|document|configuration) must (document|include|contain)\b",
]

WORD_RE = re.compile(r"\b(" + "|".join(re.escape(word) for word in WORDS) + r")\b", re.I)
PHRASE_RE = re.compile("|".join("(?:%s)" % phrase for phrase in PHRASES), re.I)
FILLER_RE = re.compile(
    r"^\s*(?:[-*>#/]+\s*)?(Moreover|Furthermore|Additionally|Overall|Ultimately|Certainly|Absolutely)\b[,!]"
)

SOFT_PATTERNS = [
    (
        "third-person maintainer narration",
        re.compile(
            r"\bthe (developer|maintainer|author|project owner) "
            r"(created|built|chose|decided|implemented|added|changed|updated|maintains|recommends)\b",
            re.I,
        ),
    ),
    (
        "AI or assistant self-reference",
        re.compile(r"\b(as an ai|as a language model|the assistant|the ai agent)\b", re.I),
    ),
    (
        "generic standards language that should be replaced with project facts",
        re.compile(
            r"\b(engineering and writing standards|every paper documents|"
            r"all prose follows (strict )?(human writing|writing) standards|"
            r"configurations must include exact file locations)\b",
            re.I,
        ),
    ),
]


def is_text(data):
    return b"\x00" not in data[:4096]


def iter_files(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
                for name in files:
                    if name in SKIP_FILES or name.endswith((".min.js", ".min.css")):
                        continue
                    if os.path.splitext(name)[1].lower() not in SKIP_EXT:
                        yield os.path.join(root, name)
        else:
            yield path


def scan_text(label, text, hard_only=False):
    hard, soft = [], []
    for line_number, line in enumerate(text.splitlines(), 1):
        for name, pattern in HARD:
            for match in pattern.finditer(line):
                hard.append((line_number, match.start() + 1, name, line.strip()))
        if hard_only:
            continue
        for match in WORD_RE.finditer(line):
            soft.append((line_number, match.start() + 1, "stock word '%s'" % match.group(), line.strip()))
        for match in PHRASE_RE.finditer(line):
            soft.append((line_number, match.start() + 1, "stock phrase '%s'" % match.group(), line.strip()))
        filler = FILLER_RE.match(line)
        if filler:
            soft.append((line_number, filler.start(1) + 1, "filler transition", line.strip()))
        for name, pattern in SOFT_PATTERNS:
            match = pattern.search(line)
            if match:
                soft.append((line_number, match.start() + 1, name, line.strip()))
    return hard, soft


def main():
    parser = argparse.ArgumentParser(description="Scan text or code for common writing tells.")
    parser.add_argument("paths", nargs="+", help="files, folders, or - for stdin")
    parser.add_argument("--hard-only", action="store_true")
    args = parser.parse_args()

    hard_total = soft_total = files_scanned = 0

    def report(label, content):
        nonlocal hard_total, soft_total, files_scanned
        files_scanned += 1
        hard, soft = scan_text(label, content, args.hard_only)
        for line, column, name, snippet in hard:
            print("%s:%d:%d: HARD %s: %s" % (label, line, column, name, snippet))
        for line, column, name, snippet in soft:
            print("%s:%d:%d: soft %s: %s" % (label, line, column, name, snippet))
        hard_total += len(hard)
        soft_total += len(soft)

    for path in args.paths:
        if path == "-":
            report("<stdin>", sys.stdin.read())
            continue
        if not os.path.exists(path):
            print("%s: not found" % path, file=sys.stderr)
            sys.exit(2)
        for filename in iter_files([path]):
            try:
                if os.path.getsize(filename) > MAX_BYTES:
                    continue
                with open(filename, "rb") as handle:
                    data = handle.read()
            except OSError:
                continue
            if is_text(data):
                report(filename, data.decode("utf-8", errors="ignore"))

    print(
        "\nScanned %d file(s): %d hard, %d soft." % (files_scanned, hard_total, soft_total),
        file=sys.stderr,
    )
    sys.exit(1 if hard_total else 0)


if __name__ == "__main__":
    main()

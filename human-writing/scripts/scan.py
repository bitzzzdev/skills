#!/usr/bin/env python3
"""Scan text or code for AI writing tells.

Usage:
    python scan.py FILE_OR_DIR [FILE_OR_DIR ...]
    echo "some text" | python scan.py -
    python scan.py --hard-only src/

Hard findings (em dash, en dash, horizontal bar, emoji and emoji-like symbols)
make the script exit with status 1. Soft findings (stock phrases, structural
tells) are printed as warnings and never change the exit status: reread the
line and decide.
"""

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

# Characters are written as escapes so this file never contains the banned
# characters itself.
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
    "delve", "delves", "delving", "tapestry", "testament", "realm", "leverage",
    "leverages", "leveraging", "leveraged", "utilize", "utilizes", "utilizing",
    "utilization", "seamless", "seamlessly", "robust", "comprehensive",
    "crucial", "crucially", "pivotal", "paramount", "foster", "fosters",
    "fostering", "harness", "harnessing", "unlock", "unlocking", "unleash",
    "elevate", "elevating", "streamline", "streamlined", "streamlining",
    "empower", "empowering", "cutting-edge", "state-of-the-art", "game-changer",
    "game-changing", "groundbreaking", "revolutionize", "revolutionary",
    "transformative", "holistic", "meticulous", "meticulously", "intricate",
    "nuanced", "multifaceted", "underscore", "underscores", "showcase",
    "showcases", "showcasing", "embark", "embarking", "vibrant", "bustling",
    "beacon", "cornerstone", "plethora", "myriad", "bespoke", "supercharge",
    "effortless", "effortlessly", "resonate", "resonates", "commendable",
    "synergy", "paradigm", "blazing-fast", "feature-rich", "best-in-class",
    "user-centric", "facilitate", "facilitates", "facilitating", "bolster",
    "spearhead", "cultivate",
]

PHRASES = [
    r"it'?s (important|worth) (to )?(note|noting|mention|mentioning)",
    r"it is (important|worth) (to )?(note|noting|mention|mentioning)",
    r"in today'?s (fast-paced|digital|modern|ever)",
    r"ever-evolving",
    r"in the (realm|world|landscape) of",
    r"plays? an? (crucial|pivotal|vital|key|important) role",
    r"a testament to",
    r"at the end of the day",
    r"when it comes to",
    r"dive into",
    r"deep dive",
    r"let'?s (explore|unpack|break (this|it) down|dive)",
    r"whether you'?re an? .{1,40} or an? ",
    r"look no further",
    r"take (it|this|your \w+) to the next level",
    r"the key takeaway",
    r"navigate the complexit",
    r"in order to",
    r"due to the fact that",
    r"a (wide )?(range|variety) of",
    r"great question",
    r"i'?d be (happy|glad) to",
    r"i hope this (email )?(helps|finds you)",
    r"feel free to (reach out|ask|contact)",
    r"let me know if you('d| would) like",
    r"here'?s the thing",
    r"not (just|only|merely) .{1,60}\bbut( also)?\b",
    r"(it'?s|this is|that'?s) not (just |only |merely )?(about )?.{1,40}[,.;] (it'?s|this is|that'?s) ",
    r"more than just",
    r"\b(in conclusion|in summary|to summarize|to sum up)\b",
]

LINE_START_FILLER = re.compile(
    r"^\s*(?:[-*>#/]+\s*)?(Moreover|Furthermore|Additionally|Overall|Ultimately|Certainly|Absolutely)\b[,!]"
)

WORD_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in WORDS) + r")\b", re.I)
PHRASE_RE = re.compile("|".join("(?:%s)" % p for p in PHRASES), re.I)

SOFT_PATTERNS = [
    ("curly quote (use straight quotes)", re.compile("[\u2018\u2019\u201C\u201D]")),
    ("arrow symbol used as connector", re.compile("[\u2192\u21D2\u279C\u2794]")),
    (
        "double hyphen used like a dash (ignore if this is a CLI flag separator)",
        re.compile(r"\w\s--\s\w"),
    ),
    (
        "enthusiastic exclamation mark",
        re.compile(r"[A-Za-z)\]]!(?:\s|$)"),
    ),
    (
        "banner or divider comment",
        re.compile(r"^\s*(?://|#|/\*|<!--)\s*[=\-*#~_]{4,}"),
    ),
    (
        "bold lead-in bullet",
        re.compile(r"^\s*[-*]\s+\*\*[^*\n]{1,40}?:?\*\*\s*[:\-]?\s*\S"),
    ),
    (
        "comment may just restate the code",
        re.compile(
            r"^\s*(?://|#)\s*(Initialize|Initialise|Loop through|Iterate (over|through)|"
            r"Define|Import|Create a|Set the|Return the|Get the|Increment|Check if|"
            r"Helper function)\b",
            re.I,
        ),
    ),
]


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


def scan_text(label, text, hard_only):
    hard, soft = [], []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, rx in HARD:
            for m in rx.finditer(line):
                hard.append((lineno, m.start() + 1, name, snippet(line, m.start(), m.end())))
        if hard_only:
            continue
        for m in WORD_RE.finditer(line):
            soft.append((lineno, m.start() + 1, "stock word '%s'" % m.group(0), snippet(line, m.start(), m.end())))
        for m in PHRASE_RE.finditer(line):
            soft.append((lineno, m.start() + 1, "stock phrase '%s'" % m.group(0), snippet(line, m.start(), m.end())))
        m = LINE_START_FILLER.match(line)
        if m:
            soft.append((lineno, m.start(1) + 1, "filler transition '%s'" % m.group(1), snippet(line, m.start(1), m.end(1))))
        for name, rx in SOFT_PATTERNS:
            m = rx.search(line)
            if m:
                soft.append((lineno, m.start() + 1, name, snippet(line, m.start(), m.end())))
    return hard, soft


def main():
    ap = argparse.ArgumentParser(description="Scan text or code for AI writing tells.")
    ap.add_argument("paths", nargs="+", help="files, folders, or - for stdin")
    ap.add_argument("--hard-only", action="store_true", help="only report em dashes, en dashes and emoji")
    args = ap.parse_args()

    total_hard = total_soft = files_scanned = 0

    def report(label, text):
        nonlocal total_hard, total_soft, files_scanned
        files_scanned += 1
        hard, soft = scan_text(label, text, args.hard_only)
        for lineno, col, name, ctx in hard:
            print("%s:%d:%d: HARD %s: %s" % (label, lineno, col, name, ctx))
        for lineno, col, name, ctx in soft:
            print("%s:%d:%d: soft %s: %s" % (label, lineno, col, name, ctx))
        total_hard += len(hard)
        total_soft += len(soft)

    for p in args.paths:
        if p == "-":
            report("<stdin>", sys.stdin.read())
            continue
        if not os.path.exists(p):
            print("%s: not found" % p, file=sys.stderr)
            sys.exit(2)
        for f in iter_files([p]):
            try:
                if os.path.getsize(f) > MAX_BYTES:
                    continue
                with open(f, "rb") as fh:
                    data = fh.read()
            except OSError:
                continue
            if not is_text(data):
                continue
            report(f, data.decode("utf-8", errors="ignore"))

    print(
        "\nScanned %d file(s): %d hard, %d soft." % (files_scanned, total_hard, total_soft),
        file=sys.stderr,
    )
    sys.exit(1 if total_hard else 0)


if __name__ == "__main__":
    main()

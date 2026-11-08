#!/usr/bin/env python3
"""Lint a commit message file. Works standalone or as a commit-msg hook.

Usage:
    python lint_commit.py MESSAGE_FILE

Exit status is 1 when the message is rejected, with every problem printed.
Warnings are printed but do not reject the message.
"""

import re
import subprocess
import sys

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u2B1B\u2B1C"
    "\u231A\u231B\u23E9-\u23FA\u2934\u2935\u3030\u303D\u3297\u3299"
    "\uFE0F\u200D]"
)
DASHES = re.compile("[\u2014\u2013\u2015]")
SECRETS = [
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub token"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[=:]\s*\S{6,}"), "credential assignment"),
]
VAGUE = re.compile(
    r"^(update|updates|updated|fix|fixes|fixed|change|changes|changed|wip|misc|"
    r"stuff|tweak|tweaks|cleanup|minor( changes| fixes)?|updated? (files?|code)|"
    r"fix (stuff|bug|bugs|issue|issues)|commit|save|test|testing)\.?$",
    re.I,
)
SKIP_SUBJECT = re.compile(r"^(Merge|Revert|fixup!|squash!|amend!)\b")

CHECKPOINT_REQUIRED = [
    "Project", "Run", "Structure", "Architecture",
    "Recent changes", "Current state", "Next steps", "Previous checkpoint",
]

SUBSTANTIAL_FILES = 3
SUBSTANTIAL_LINES = 40


def clean(text):
    """Drop git comment lines and everything after the scissors line."""
    out = []
    for line in text.splitlines():
        if line.startswith("# ------------------------ >8"):
            break
        if line.startswith("#"):
            continue
        out.append(line.rstrip())
    while out and not out[-1]:
        out.pop()
    return out


def staged_size():
    """Return (files, changed_lines) for the staged diff, or (0, 0)."""
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--numstat"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return 0, 0
    files = lines = 0
    for row in res.stdout.splitlines():
        parts = row.split("\t")
        if len(parts) < 3:
            continue
        files += 1
        for n in parts[:2]:
            if n.isdigit():
                lines += int(n)
    return files, lines


def has_label(lines, label):
    rx = re.compile(r"^\s*(?:[-*]\s*)?%s\s*(?:\([^)]*\))?\s*:" % re.escape(label), re.I)
    return any(rx.match(l) for l in lines)


def lint(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = clean(fh.read())

    errors, warnings = [], []

    if not lines or not lines[0].strip():
        return ["The commit message is empty."], []

    subject = lines[0]
    body = lines[1:]

    if SKIP_SUBJECT.match(subject):
        return [], []

    full = "\n".join(lines)

    if EMOJI.search(full):
        errors.append("Contains an emoji or decorative symbol. Remove it.")
    if DASHES.search(full):
        errors.append("Contains an em dash, en dash or horizontal bar. Use a comma, colon, period or parentheses.")
    for rx, label in SECRETS:
        if rx.search(full):
            errors.append("Looks like it contains a secret (%s). Commit messages are permanent. Remove it." % label)
            break

    if len(subject) > 72:
        errors.append("Subject is %d characters. Keep it to 72 or fewer." % len(subject))
    if subject.endswith("."):
        errors.append("Subject ends with a period. Remove it.")
    if VAGUE.match(subject.strip()):
        errors.append("Subject is too vague (%r). Say what changed." % subject)
    if body and body[0].strip():
        errors.append("Leave a blank line between the subject and the body.")

    body_text = [l for l in body if l.strip()]

    if subject.lower().startswith("checkpoint:"):
        for section in CHECKPOINT_REQUIRED:
            if not has_label(body, section):
                errors.append("Checkpoint is missing the '%s:' section." % section)
        return errors, warnings

    files, changed = staged_size()
    substantial = files >= SUBSTANTIAL_FILES or changed >= SUBSTANTIAL_LINES

    if substantial:
        if len(body_text) < 2:
            errors.append(
                "This commit touches %d files and %d lines but has no real body. "
                "Add at least Why: and Changes:." % (files, changed)
            )
        elif not has_label(body, "Why"):
            errors.append("Add a 'Why:' section. A substantial change needs its reason recorded.")
        if body_text and not has_label(body, "Verified"):
            warnings.append("No 'Verified:' line. Say what you ran, or write 'Verified: not run'.")
        if body_text and not has_label(body, "Changes"):
            warnings.append("No 'Changes:' section listing the files and what changed in each.")

    long_lines = [l for l in body if len(l) > 100 and not l.lstrip().startswith(("http", "-", "*"))]
    if long_lines:
        warnings.append("%d body line(s) are over 100 characters. Wrap prose at about 72." % len(long_lines))

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("usage: lint_commit.py MESSAGE_FILE", file=sys.stderr)
        return 2
    errors, warnings = lint(sys.argv[1])
    for w in warnings:
        print("warning: %s" % w, file=sys.stderr)
    if errors:
        print("Commit message rejected:", file=sys.stderr)
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

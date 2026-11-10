#!/usr/bin/env python3
"""Check that every skill folder has a valid SKILL.md.

A skill folder is any top-level directory that contains SKILL.md. Each one
needs YAML frontmatter with a name that matches the folder and a description.
Also verifies frontmatter formatting and checks for disallowed em dashes and emoji.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors = []
count = 0

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u2B1B\u2B1C"
    "\u231A\u231B\u23E9-\u23FA\u2934\u2935\u3030\u303D\u3297\u3299"
    "\uFE0F\u200D]"
)
DASHES = re.compile("[\u2014\u2013\u2015]")

for skill_md in sorted(ROOT.glob("*/SKILL.md")):
    folder = skill_md.parent.name
    count += 1
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append(f"{folder}: SKILL.md has no frontmatter")
        continue
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{folder}: frontmatter is not closed")
        continue
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{folder}: invalid YAML frontmatter ({exc})")
        continue
    if meta.get("name") != folder:
        errors.append(f"{folder}: name is {meta.get('name')!r}, expected {folder!r}")
    if not str(meta.get("description", "")).strip():
        errors.append(f"{folder}: missing description")

    # Check for em dashes or emoji in SKILL.md
    if DASHES.search(text):
        errors.append(f"{folder}: SKILL.md contains em or en dashes (violates human-writing rules)")
    if EMOJI.search(text):
        errors.append(f"{folder}: SKILL.md contains emoji (violates human-writing rules)")

    # Check for skill folder update check
    lower = text.lower()
    if "skill folder update" not in lower or "git status" not in lower:
        errors.append(f"{folder}: SKILL.md missing check for skill folder update and git status")

if count == 0:
    errors.append("no skills found")

for line in errors:
    print(f"error: {line}")
print(f"Checked {count} skill(s), {len(errors)} problem(s).")
sys.exit(1 if errors else 0)

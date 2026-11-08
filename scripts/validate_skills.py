#!/usr/bin/env python3
"""Check that every skill folder has a valid SKILL.md.

A skill folder is any top-level directory that contains SKILL.md. Each one
needs YAML frontmatter with a name that matches the folder and a description.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors = []
count = 0

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

if count == 0:
    errors.append("no skills found")

for line in errors:
    print(f"error: {line}")
print(f"Checked {count} skill(s), {len(errors)} problem(s).")
sys.exit(1 if errors else 0)

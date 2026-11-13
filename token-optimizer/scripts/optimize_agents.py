#!/usr/bin/env python3
"""Apply conservative, backed-up reasoning settings to detected coding agents."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

HOME = Path.home()
XDG = Path(os.environ.get("XDG_CONFIG_HOME", str(HOME / ".config")))
JSON_CONFIGS = {
    "OpenCode": [XDG / "opencode/opencode.json", Path.cwd() / "opencode.json"],
    "Claude Code": [HOME / ".claude/settings.json", Path.cwd() / ".claude/settings.local.json"],
    "Copilot CLI": [HOME / ".copilot/settings.json"],
    "Muse Code": [XDG / "muse/settings.json"],
    "Antigravity": [HOME / ".antigravity/settings.json"],
    "Gemini CLI": [HOME / ".gemini/settings.json", Path.cwd() / ".gemini/settings.json"],
}


def set_existing(data: Any, keys: set[str], value: Any) -> int:
    changed = 0
    if isinstance(data, dict):
        for key, child in list(data.items()):
            if key in keys and child != value:
                data[key] = value
                changed += 1
            else:
                changed += set_existing(child, keys, value)
    elif isinstance(data, list):
        for child in data:
            changed += set_existing(child, keys, value)
    return changed


def set_reasoning_options(data: Any) -> int:
    changed = 0
    if isinstance(data, dict):
        for key, child in data.items():
            if key == "reasoning" and isinstance(child, dict) and child.get("enabled") is True:
                child["enabled"] = False
                changed += 1
            else:
                changed += set_reasoning_options(child)
    elif isinstance(data, list):
        for child in data:
            changed += set_reasoning_options(child)
    return changed


def backup(path: Path) -> Path:
    target = path.with_name(path.name + ".BAK")
    if not target.exists():
        shutil.copy2(path, target)
    return target


def write_atomic(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    temporary.replace(path)


def edit_json(path: Path, agent: str, dry_run: bool) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return f"SKIP {path}: unsafe to parse ({exc})"

    changed = 0
    if agent == "Claude Code" and isinstance(data, dict):
        if data.get("alwaysThinkingEnabled") is not False:
            data["alwaysThinkingEnabled"] = False
            changed += 1
        env = data.setdefault("env", {})
        if isinstance(env, dict):
            for key, value in {
                "MAX_THINKING_TOKENS": "0",
                "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
                "DISABLE_INTERLEAVED_THINKING": "1",
            }.items():
                if env.get(key) != value:
                    env[key] = value
                    changed += 1
    elif agent == "OpenCode":
        changed += set_existing(data, {"enable_thinking"}, False)
        changed += set_reasoning_options(data)
    elif agent == "Gemini CLI":
        # Change only model-specific API controls already present.
        # Hiding inline thinking is a UI preference, not a token-saving setting.
        changed += set_existing(data, {"thinkingBudget"}, 0)
        changed += set_existing(data, {"thinkingLevel"}, "MINIMAL")
    elif agent == "Muse Code" and isinstance(data, dict):
        if data.get("reasoning_effort") != "none" and "reasoning_effort" in data:
            data["reasoning_effort"] = "none"
            changed += 1
    elif agent == "Antigravity":
        changed += set_existing(data, {"thinkingLevel", "thinking_level"}, "MINIMAL")
        changed += set_existing(data, {"thinkingBudget", "thinking_budget"}, 0)
    else:
        return f"MANUAL {agent}: no verified automatic edit; left unchanged"

    if not changed:
        return f"UNCHANGED {agent}: no supported existing setting needed modification"
    if dry_run:
        return f"DRY-RUN {agent}: {changed} setting(s) would change in {path}"
    saved = backup(path)
    write_atomic(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return f"UPDATED {agent}: {path} (backup: {saved})"


def edit_codex(path: Path, dry_run: bool) -> str:
    original = path.read_text(encoding="utf-8")
    model = re.search(r'(?m)^model\s*=\s*["\'](.*?)["\']\s*$', original)
    model_name = model.group(1).lower() if model else ""
    effort = "low" if re.search(r"(^|[/_-])o[0-9]([-_/]|$)", model_name) else "none"
    pattern = r'(?m)^model_reasoning_effort[ \t]*=[ \t]*(["\'])(.*?)\1[ \t]*$'
    match = re.search(pattern, original)
    if match and match.group(2) == effort:
        return f"UNCHANGED Codex CLI: already uses {effort}"
    updated = (
        original[:match.start(2)] + effort + original[match.end(2):]
        if match else original.rstrip() + f'\nmodel_reasoning_effort = "{effort}"\n'
    )
    if dry_run:
        return f"DRY-RUN Codex CLI: would set reasoning effort to {effort}"
    saved = backup(path)
    write_atomic(path, updated)
    return f"UPDATED Codex CLI: {path} (backup: {saved})"


def edit_aider(path: Path, dry_run: bool) -> str:
    original = path.read_text(encoding="utf-8")
    updated = original
    for key, value in (("thinking-tokens", "0"), ("reasoning-effort", "none")):
        pattern = rf"(?m)^{re.escape(key)}[ \t]*:.*$"
        replacement = f"{key}: {value}"
        if re.search(pattern, updated):
            updated = re.sub(pattern, replacement, updated)
        else:
            updated = updated.rstrip() + f"\n{replacement}\n"
    if updated == original:
        return f"UNCHANGED Aider: {path}"
    if dry_run:
        return f"DRY-RUN Aider: would update {path}"
    saved = backup(path)
    write_atomic(path, updated)
    return f"UPDATED Aider: {path} (backup: {saved})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="preview without writing files")
    args = parser.parse_args()
    found = 0

    for agent, paths in JSON_CONFIGS.items():
        for path in dict.fromkeys(paths):
            if path.is_file():
                found += 1
                print(edit_json(path, agent, args.dry_run))

    codex = HOME / ".codex/config.toml"
    if codex.is_file():
        found += 1
        try:
            print(edit_codex(codex, args.dry_run))
        except (OSError, UnicodeError) as exc:
            print(f"SKIP {codex}: {exc}")

    for path in dict.fromkeys([HOME / ".aider.conf.yml", Path.cwd() / ".aider.conf.yml"]):
        if path.is_file():
            found += 1
            try:
                print(edit_aider(path, args.dry_run))
            except (OSError, UnicodeError) as exc:
                print(f"SKIP {path}: {exc}")

    if not found:
        print("No supported agent configuration files were found.")
    print(f"Detected configuration files: {found}")
    print("Unsupported settings remain unchanged. Consult references/agents.md for manual controls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

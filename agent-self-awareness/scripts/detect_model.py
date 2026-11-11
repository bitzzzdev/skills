#!/usr/bin/env python3
"""Detect the active coding agent and model, then print the quality gate.

The result decides whether the agent may implement from memory or must run a
research-first protocol. Unknown models are treated as non-frontier.

Usage:
    python detect_model.py
    python detect_model.py --json
    python detect_model.py --require-frontier   # exit 1 when not frontier
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

HOME = Path.home()

HARNESS_SIGNALS = [
    ("opencode", ["OPENCODE", "OPENCODE_SESSION_ID", "OPENCODE_TERMINAL"]),
    ("claude", ["CLAUDECODE", "CLAUDE_CODE", "CLAUDE_CODE_ENTRYPOINT"]),
    ("codex", ["CODEX", "CODEX_HOME", "CODEX_SANDBOX"]),
    ("gemini", ["GEMINI_CLI", "GEMINI_SESSION_ID"]),
    ("antigravity", ["ANTIGRAVITY", "AGY_SESSION"]),
    ("muse", ["MUSE_SESSION", "MUSE_CLI"]),
    ("cursor", ["CURSOR_TRACE_ID", "CURSOR_AGENT"]),
    ("windsurf", ["WINDSURF", "CODEIUM"]),
    ("copilot", ["COPILOT_AGENT", "GITHUB_COPILOT"]),
    ("aider", ["AIDER_MODEL", "AIDER"]),
]

MODEL_ENV_KEYS = [
    "OPENCODE_MODEL",
    "OPENCODE_MODEL_ID",
    "ANTHROPIC_MODEL",
    "CLAUDE_MODEL",
    "OPENAI_MODEL",
    "CODEX_MODEL",
    "GEMINI_MODEL",
    "AGENT_MODEL",
    "AIDER_MODEL",
    "LLM_MODEL",
    "MODEL",
]

CONFIG_HINTS = [
    (HOME / ".config/opencode/opencode.json", "opencode"),
    (HOME / ".codex/config.toml", "codex"),
    (HOME / ".claude/settings.json", "claude"),
    (HOME / ".gemini/settings.json", "gemini"),
    (HOME / ".gemini/antigravity-cli/settings.json", "antigravity"),
    (HOME / ".copilot/config.json", "copilot"),
]

FRONTIER_MARKERS = [
    r"\bopus\b",
    r"gpt[-_. ]?5(?![-_. ]?(mini|nano))",
    r"\bo3[-_. ]?pro\b",
    r"gemini[-_. ]?3(?:[.-]?\d+)?[-_. ]?(pro|ultra|thinking)",
    r"grok[-_. ]?4",
    r"deepseek[-_. ]?v4(?![-_. ]?(flash|lite))",
    r"qwen[-_. ]?3[-_. ]?max",
    r"kimi[-_. ]?k2",
    r"sonnet[-_. ]?4\.[5-9]",
    r"glm[-_. ]?5",
]

EFFICIENT_MARKERS = [
    r"\bflash\b",
    r"\bmini\b",
    r"\bnano\b",
    r"\bhaiku\b",
    r"\blite\b",
    r"\bsmall\b",
    r"\bfree\b",
    r"\bturbo\b",
    r"\bcheap\b",
    r"\bfast\b",
    r"3\.5[-_. ]?sonnet",
    r"sonnet[-_. ]?3\.5",
    r"gpt[-_. ]?4\.1",
]

CAPABLE_MARKERS = [
    r"\bsonnet\b",
    r"\bpro\b",
    r"gpt[-_. ]?4",
    r"deepseek[-_. ]?v3",
    r"qwen[-_. ]?3",
    r"codestral",
    r"command[-_. ]?r",
]


def detect_harness():
    found = []
    for name, variables in HARNESS_SIGNALS:
        if any(os.environ.get(var) for var in variables):
            found.append(name)
    return found


def first_env_model():
    for key in MODEL_ENV_KEYS:
        value = os.environ.get(key)
        if value and len(value) < 200:
            return key, value
    return None, None


def regex_model(path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:200000]
    except OSError:
        return None
    if path.suffix == ".toml":
        match = re.search(r"(?m)^\s*model\s*=\s*[\"']([^\"']+)[\"']", text)
    else:
        match = re.search(r"[\"']model[\"']\s*:\s*[\"']([^\"']+)[\"']", text)
        if not match:
            match = re.search(r"(?m)^\s*model\s*=\s*[\"']([^\"']+)[\"']", text)
    return match.group(1) if match else None


def opencode_session_model():
    session_id = os.environ.get("OPENCODE_SESSION_ID")
    db = HOME / ".local/share/opencode/opencode.db"
    if not session_id or not db.is_file():
        return None
    try:
        uri = db.resolve().as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=1)
        rows = conn.execute(
            "select data from session_message where session_id=? and type='assistant' "
            "order by seq desc limit 5",
            (session_id,),
        )
        for (data,) in rows:
            try:
                payload = json.loads(data)
            except (TypeError, json.JSONDecodeError):
                continue
            model = payload.get("model") or {}
            model_id = model.get("id") or model.get("modelID")
            provider = model.get("providerID") or model.get("provider")
            if model_id:
                conn.close()
                return (
                    "%s/%s" % (provider, model_id) if provider else model_id,
                    "opencode session %s" % session_id,
                )
        conn.close()
    except sqlite3.Error:
        pass
    return None


def codex_thread_model():
    databases = sorted(
        (HOME / ".codex").glob("state_*.sqlite"),
        key=lambda path: path.stat().st_mtime,
    )
    for db in reversed(databases):
        try:
            uri = db.resolve().as_uri() + "?mode=ro"
            conn = sqlite3.connect(uri, uri=True, timeout=1)
            columns = {row[1] for row in conn.execute("pragma table_info(threads)")}
            if "model" not in columns:
                conn.close()
                continue
            row = conn.execute(
                "select model from threads where model is not null and model != '' "
                "order by updated_at desc limit 1"
            ).fetchone()
            conn.close()
            if row and row[0]:
                return row[0], "codex state %s" % db.name
        except sqlite3.Error:
            continue
    return None


def detect_model():
    evidence = []

    key, value = first_env_model()
    if value:
        evidence.append((value, "environment %s" % key))

    session = opencode_session_model()
    if session:
        evidence.append(session)

    thread = codex_thread_model()
    if thread:
        evidence.append(thread)

    for path, label in CONFIG_HINTS:
        if path.is_file():
            value = regex_model(path)
            if value:
                evidence.append((value, "%s config %s" % (label, path)))

    if not evidence:
        return None, None
    return evidence[0]


def classify(model):
    text = (model or "").lower()
    if not text:
        return "unknown", False
    if any(re.search(pattern, text) for pattern in EFFICIENT_MARKERS):
        return "efficient", False
    if any(re.search(pattern, text) for pattern in FRONTIER_MARKERS):
        return "frontier", True
    if any(re.search(pattern, text) for pattern in CAPABLE_MARKERS):
        return "capable", False
    return "unknown", False


def mode_for(frontier):
    if frontier:
        return "standard quality gates, research still required for version-sensitive work"
    return "research-first mandatory before implementation"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-frontier",
        action="store_true",
        help="exit 1 when the detected model is not frontier class",
    )
    args = parser.parse_args()

    harnesses = detect_harness()
    model, source = detect_model()
    tier, frontier = classify(model)
    result = {
        "harness": harnesses[0] if harnesses else "unknown",
        "harnesses": harnesses,
        "model": model or "unknown",
        "source": source or "no evidence found",
        "tier": tier,
        "frontier": frontier,
        "mode": mode_for(frontier),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Agent self-awareness")
        print("Harness: %s" % result["harness"])
        print("Model: %s" % result["model"])
        print("Evidence: %s" % result["source"])
        print("Tier: %s" % tier)
        print("Frontier coding class: %s" % ("yes" if frontier else "no"))
        print("Execution mode: %s" % result["mode"])
        if not frontier:
            print()
            print("Required before implementation:")
            print("  1. Restate the task and acceptance criteria.")
            print("  2. Read the relevant code and repository docs.")
            print("  3. Read current official docs for every library and version.")
            print("  4. Check upstream issues or examples for the exact problem.")
            print("  5. Write a short plan with risks and verification steps.")
            print("  6. Implement in small verified increments.")
            print("  7. Run the build, tests, and linters.")
            print("  8. Review the full diff and report remaining uncertainty.")

    if args.require_frontier and not frontier:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

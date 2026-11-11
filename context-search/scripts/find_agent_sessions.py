#!/usr/bin/env python3
"""Find prior coding-agent sessions for a project and extract a short brief.

Supports OpenCode, Codex CLI, Claude Code, Antigravity CLI, Gemini CLI, Muse,
Aider, and editor workspace storage, with a generic JSONL fallback. Read-only.
Credentials found in transcripts are redacted before printing.

Usage:
    python find_agent_sessions.py --project /path/to/repo
    python find_agent_sessions.py --project . --brief
    python find_agent_sessions.py --project . --json --limit 5
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
MAX_FILE_BYTES = 5 * 1024 * 1024

REDACTIONS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "[REDACTED]"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "[REDACTED]"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "[REDACTED]"),
    (re.compile(r"AIza[0-9A-Za-z_-]{20,}"), "[REDACTED]"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "[REDACTED]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED]"),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.S,
        ),
        "[REDACTED PRIVATE KEY]",
    ),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"), "Bearer [REDACTED]"),
    (
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?[^\s'\"]{6,}"
        ),
        r"\1=[REDACTED]",
    ),
]


def redact(text):
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def clean(text, limit):
    if not text:
        return ""
    text = re.sub(r"\r\n?", "\n", str(text))
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > limit:
        text = text[:limit].rstrip() + "..."
    return redact(text)


def norm(path):
    if not path:
        return None
    try:
        return str(Path(path).expanduser().resolve(strict=False))
    except (OSError, RuntimeError):
        return os.path.normpath(os.path.expanduser(str(path)))


def iso_from_epoch(value):
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if number > 1e14:
        number /= 1000.0
    elif number > 1e11:
        number /= 1000.0
    try:
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def iso_from_mtime(path):
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        return None


def git_toplevel(path):
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return norm(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else None


def git_common_dir(path):
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--git-common-dir"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    common = out.stdout.strip()
    if not os.path.isabs(common):
        common = os.path.join(str(path), common)
    return norm(common)


def match_project(candidate, project):
    """Return exact, worktree, subdir, parent, or None."""
    cand = norm(candidate)
    if not cand:
        return None
    if cand == project:
        return "exact"
    if cand.startswith(project + os.sep):
        return "subdir"
    if project.startswith(cand + os.sep):
        return "parent"
    cand_common = git_common_dir(cand)
    if cand_common and cand_common == git_common_dir(project):
        return "worktree"
    return None


def ro_connect(path):
    uri = Path(path).resolve().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True, timeout=1)


def table_columns(conn, table):
    try:
        return {row[1] for row in conn.execute('pragma table_info("%s")' % table)}
    except sqlite3.Error:
        return set()


def table_exists(conn, table):
    row = conn.execute(
        "select 1 from sqlite_master where type='table' and name=?", (table,)
    ).fetchone()
    return bool(row)


def add_session(sessions, provider, session_id, title, when, path, match, detail=""):
    sessions.append(
        {
            "provider": provider,
            "id": str(session_id or ""),
            "title": clean(title, 200) if title else "",
            "time": when,
            "path": str(path) if path else "",
            "match": match,
            "detail": clean(detail, 400) if detail else "",
        }
    )


def scan_opencode(project, sessions, all_projects):
    roots = [
        HOME / ".local/share/opencode",
        HOME / ".opencode",
    ]
    for root in roots:
        db = root / "opencode.db"
        if db.is_file():
            try:
                conn = ro_connect(db)
                if table_exists(conn, "session_v2"):
                    cols = table_columns(conn, "session_v2")
                    project_cols = table_columns(conn, "project")
                    directory_expr = "s.directory" if "directory" in cols else "null"
                    if "project_id" in cols and "worktree" in project_cols:
                        query = (
                            "select s.id, s.title, s.time_created, s.time_updated, "
                            + directory_expr
                            + ", p.worktree, s.path from session_v2 s "
                            "left join project p on p.id = s.project_id"
                            if "path" in cols
                            else "select s.id, s.title, s.time_created, s.time_updated, "
                            + directory_expr
                            + ", p.worktree, null from session_v2 s "
                            "left join project p on p.id = s.project_id"
                        )
                    else:
                        query = (
                            "select id, title, time_created, time_updated, "
                            + ("directory" if "directory" in cols else "null")
                            + ", null, "
                            + ("path" if "path" in cols else "null")
                            + " from session_v2"
                        )
                    for row in conn.execute(query):
                        sid, title, created, updated, directory, worktree, spath = row
                        candidate = directory or worktree or spath
                        match = "all" if all_projects else match_project(candidate, project)
                        if not match:
                            continue
                        add_session(
                            sessions,
                            "opencode",
                            sid,
                            title,
                            iso_from_epoch(updated or created),
                            db,
                            match,
                            directory or worktree or "",
                        )
                conn.close()
            except sqlite3.Error as exc:
                print("warning: opencode database unreadable: %s" % exc, file=sys.stderr)
        legacy = root / "storage" / "session"
        if legacy.is_dir():
            for path in legacy.glob("**/*.json"):
                try:
                    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
                except (OSError, json.JSONDecodeError):
                    continue
                candidate = data.get("directory") or data.get("path")
                match = "all" if all_projects else match_project(candidate, project)
                if not match:
                    continue
                created = (data.get("time") or {}).get("created")
                add_session(
                    sessions,
                    "opencode",
                    data.get("id", path.stem),
                    data.get("title"),
                    iso_from_epoch(created) or iso_from_mtime(path),
                    path,
                    match,
                    candidate or "",
                )


def scan_codex(project, sessions, all_projects):
    root = HOME / ".codex"
    databases = sorted(root.glob("state_*.sqlite"), key=lambda p: p.stat().st_mtime)
    for db in reversed(databases):
        try:
            conn = ro_connect(db)
            if not table_exists(conn, "threads"):
                conn.close()
                continue
            cols = table_columns(conn, "threads")
            wanted = [
                "id",
                "title",
                "name",
                "first_user_message",
                "preview",
                "updated_at_ms",
                "updated_at",
                "created_at_ms",
                "created_at",
                "cwd",
                "rollout_path",
                "git_branch",
            ]
            selected = [c for c in wanted if c in cols]
            query = "select %s from threads" % ", ".join(selected)
            for row in conn.execute(query):
                record = dict(zip(selected, row))
                match = "all" if all_projects else match_project(record.get("cwd"), project)
                if not match:
                    continue
                when = iso_from_epoch(record.get("updated_at_ms") or record.get("updated_at"))
                add_session(
                    sessions,
                    "codex",
                    record.get("id"),
                    record.get("title") or record.get("name") or record.get("first_user_message"),
                    when,
                    record.get("rollout_path") or db,
                    match,
                    record.get("preview") or record.get("git_branch") or "",
                )
            conn.close()
        except sqlite3.Error:
            continue
    for path in root.glob("sessions/**/rollout-*.jsonl"):
        meta = read_jsonl_head(path, 12)
        candidate = None
        for item in meta:
            payload = item.get("payload") if isinstance(item, dict) else None
            if isinstance(payload, dict) and payload.get("cwd"):
                candidate = payload.get("cwd")
                break
            if isinstance(item, dict) and item.get("cwd"):
                candidate = item.get("cwd")
                break
        match = "all" if all_projects else match_project(candidate, project)
        if not match:
            continue
        add_session(
            sessions,
            "codex",
            path.stem,
            "",
            iso_from_mtime(path),
            path,
            match,
            candidate or "",
        )


def scan_antigravity(project, sessions, all_projects):
    roots = [
        HOME / ".gemini/antigravity-cli",
        HOME / ".gemini/antigravity",
    ]
    for root in roots:
        db = root / "conversation_summaries.db"
        if not db.is_file():
            continue
        try:
            conn = ro_connect(db)
            if not table_exists(conn, "conversation_summaries"):
                conn.close()
                continue
            cols = table_columns(conn, "conversation_summaries")
            wanted = [
                "conversation_id",
                "title",
                "preview",
                "raw_summary",
                "workspace_uris",
                "last_modified_time",
                "agent_name",
                "source",
            ]
            selected = [c for c in wanted if c in cols]
            for row in conn.execute("select %s from conversation_summaries" % ", ".join(selected)):
                record = dict(zip(selected, row))
                uris = record.get("workspace_uris") or "[]"
                try:
                    parsed = json.loads(uris) if isinstance(uris, str) else uris
                except json.JSONDecodeError:
                    parsed = [uris]
                candidates = [
                    str(item).replace("file://", "") for item in (parsed or [])
                ]
                match = None
                for candidate in candidates:
                    match = "all" if all_projects else match_project(candidate, project)
                    if match:
                        break
                if not match:
                    continue
                add_session(
                    sessions,
                    "antigravity",
                    record.get("conversation_id"),
                    record.get("title"),
                    record.get("last_modified_time"),
                    root / "brain" / str(record.get("conversation_id", "")),
                    match,
                    record.get("preview") or record.get("raw_summary") or "",
                )
            conn.close()
        except sqlite3.Error:
            continue


def scan_claude(project, sessions, all_projects):
    root = HOME / ".claude"
    for directory in (root / "projects").glob("*") if (root / "projects").is_dir() else []:
        expected = norm(project).replace("/", "-")
        if expected.startswith("-"):
            expected = "-" + expected[1:]
        for path in directory.glob("*.jsonl"):
            head = read_jsonl_head(path, 25)
            candidate = None
            title = None
            for item in head:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "summary" and item.get("summary"):
                    title = item.get("summary")
                if item.get("cwd"):
                    candidate = item.get("cwd")
                message = item.get("message")
                if isinstance(message, dict) and message.get("cwd"):
                    candidate = message.get("cwd")
            if candidate is None and directory.name.lower() == expected.lower():
                candidate = project
            match = "all" if all_projects else match_project(candidate, project)
            if not match:
                continue
            add_session(
                sessions,
                "claude",
                path.stem,
                title,
                iso_from_mtime(path),
                path,
                match,
                candidate or directory.name,
            )


def scan_gemini(project, sessions, all_projects):
    root = HOME / ".gemini"
    for path in (root / "tmp").glob("*/chats/*.json"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:200000]
        except OSError:
            continue
        match = None
        if all_projects:
            match = "all"
        elif norm(project) in text:
            match = "exact"
        elif path.parent.parent.name and path.parent.parent.name in norm(project):
            match = "name"
        if not match:
            continue
        title = ""
        try:
            data = json.loads(text)
            title = str(data.get("title") or data.get("summary") or "")[:200]
        except json.JSONDecodeError:
            pass
        add_session(
            sessions,
            "gemini",
            path.stem,
            title,
            iso_from_mtime(path),
            path,
            match,
            str(path.parent.parent),
        )


def scan_aider(project, sessions, all_projects):
    for name in (".aider.chat.history.md", ".aider.input.history"):
        path = Path(project) / name
        if path.is_file():
            add_session(
                sessions,
                "aider",
                name,
                "Aider history",
                iso_from_mtime(path),
                path,
                "exact",
                str(path),
            )


def scan_editor_workspaces(project, sessions, all_projects):
    roots = [
        (HOME / ".config/Cursor", "cursor"),
        (HOME / "Library/Application Support/Cursor", "cursor"),
        (HOME / ".config/Windsurf", "windsurf"),
        (HOME / "Library/Application Support/Windsurf", "windsurf"),
        (HOME / ".config/Code", "vscode"),
    ]
    for root, provider in roots:
        storage = root / "User" / "workspaceStorage"
        if not storage.is_dir():
            continue
        for workspace in storage.glob("*/workspace.json"):
            try:
                data = json.loads(workspace.read_text(encoding="utf-8", errors="ignore"))
            except (OSError, json.JSONDecodeError):
                continue
            candidate = data.get("folder") or data.get("workspace") or ""
            candidate = str(candidate).replace("file://", "")
            match = "all" if all_projects else match_project(candidate, project)
            if not match:
                continue
            db = workspace.parent / "state.vscdb"
            add_session(
                sessions,
                provider,
                workspace.parent.name,
                "Workspace history",
                iso_from_mtime(db if db.exists() else workspace),
                db if db.exists() else workspace,
                match,
                candidate,
            )


def scan_generic(project, sessions, all_projects):
    roots = [
        HOME / ".muse",
        HOME / ".config/muse",
        HOME / ".local/share/muse",
        HOME / ".copilot",
        HOME / ".local/share/goose",
        HOME / ".config/goose",
        HOME / ".local/share/crush",
        HOME / ".config/crush",
        HOME / ".amp",
        HOME / ".local/share/amp",
        HOME / ".factory",
        HOME / ".openhands",
    ]
    needle = norm(project)
    for root in roots:
        if not root.is_dir():
            continue
        provider = root.name.replace(".", "") or "agent"
        for path in root.glob("**/*.jsonl"):
            if len(sessions) > 200:
                return
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                head = path.read_text(encoding="utf-8", errors="ignore")[:12000]
            except OSError:
                continue
            if needle in head:
                add_session(
                    sessions,
                    provider,
                    path.stem,
                    "",
                    iso_from_mtime(path),
                    path,
                    "all" if all_projects else "exact",
                    str(root),
                )


def read_jsonl_head(path, lines):
    items = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for index, line in enumerate(handle):
                if index >= lines:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return items


def text_from_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") in {"thinking", "reasoning", "tool_use", "tool_result"}:
                    continue
                value = block.get("text") or block.get("content")
                if isinstance(value, str):
                    parts.append(value)
        return "\n".join(parts)
    if isinstance(content, dict):
        return text_from_content(content.get("text") or content.get("content"))
    return ""


def messages_from_jsonl(path):
    messages = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(item, dict):
                    continue
                payload = item.get("payload") if isinstance(item.get("payload"), dict) else None
                if payload:
                    kind = payload.get("type")
                    if kind in {"user_message", "agent_message"}:
                        messages.append((kind.split("_")[0], str(payload.get("message") or "")))
                        continue
                    if payload.get("role") in {"user", "assistant"}:
                        text = text_from_content(payload.get("content"))
                        if text:
                            messages.append((payload["role"], text))
                        continue
                message = item.get("message")
                if isinstance(message, dict) and message.get("role") in {"user", "assistant"}:
                    text = text_from_content(message.get("content"))
                    if text:
                        messages.append((message["role"], text))
                    continue
                if item.get("type") in {"user", "assistant"}:
                    text = text_from_content(item.get("content") or item.get("text"))
                    if text:
                        messages.append((item["type"], text))
    except OSError:
        pass
    return messages


def extract_brief(session, max_chars):
    provider = session["provider"]
    path = session["path"]
    messages = []
    if provider == "opencode":
        db = Path(path)
        if db.is_file():
            try:
                conn = ro_connect(db)
                rows = conn.execute(
                    "select type, data from session_message where session_id=? "
                    "order by seq asc",
                    (session["id"],),
                )
                for kind, data in rows:
                    try:
                        payload = json.loads(data)
                    except (TypeError, json.JSONDecodeError):
                        continue
                    text = payload.get("text") or text_from_content(payload.get("content"))
                    if text:
                        messages.append((kind, text))
                conn.close()
            except sqlite3.Error:
                pass
    elif provider == "antigravity":
        root = HOME / ".gemini/antigravity-cli"
        db = root / "conversation_summaries.db"
        if db.is_file():
            try:
                conn = ro_connect(db)
                row = conn.execute(
                    "select user_body, agent_body from conversations_fts "
                    "where conversation_id=? limit 1",
                    (session["id"],),
                ).fetchone()
                if row:
                    if row[0]:
                        messages.append(("user", row[0]))
                    if row[1]:
                        messages.append(("assistant", row[1]))
                conn.close()
            except sqlite3.Error:
                pass
    elif path and Path(path).is_file():
        if path.endswith(".jsonl"):
            messages = messages_from_jsonl(Path(path))
        elif path.endswith(".md"):
            try:
                messages = [("history", Path(path).read_text(encoding="utf-8", errors="ignore"))]
            except OSError:
                pass
        elif path.endswith(".json"):
            try:
                data = json.loads(Path(path).read_text(encoding="utf-8", errors="ignore")[:200000])
                messages = generic_json_messages(data)
            except (OSError, json.JSONDecodeError):
                pass

    if not messages:
        return session.get("detail", "")

    users = [text for role, text in messages if role in {"user", "history"}]
    assistants = [text for role, text in messages if role in {"agent", "assistant"}]
    selected = []
    for text in users[:2] + users[-2:] + assistants[-2:]:
        if text and text not in selected:
            selected.append(text)
    joined = "\n\n".join(clean(text, max_chars) for text in selected)
    return clean(joined, max_chars * 2)


def generic_json_messages(data, depth=0):
    """Best-effort extraction from an unknown JSON session shape."""
    found = []
    if depth > 6:
        return found
    if isinstance(data, dict):
        if isinstance(data.get("messages"), list):
            for item in data["messages"]:
                role = item.get("role") or item.get("type") or item.get("author")
                content = item.get("content") or item.get("text") or item.get("message")
                text = text_from_content(content)
                if text and role in {"user", "assistant", "model", "agent"}:
                    found.append((str(role), text))
            return found
        for key in ("history", "conversation", "turns", "contents", "items"):
            if key in data:
                found.extend(generic_json_messages(data[key], depth + 1))
                if found:
                    return found
        for value in data.values():
            if isinstance(value, (dict, list)):
                found.extend(generic_json_messages(value, depth + 1))
    elif isinstance(data, list):
        for item in data:
            found.extend(generic_json_messages(item, depth + 1))
    return found


def discover_agents():
    tools = {
        "opencode": ["opencode"],
        "codex": ["codex"],
        "claude": ["claude"],
        "gemini": ["gemini"],
        "antigravity": ["agy", "antigravity"],
        "muse": ["muse"],
        "aider": ["aider"],
        "cursor": ["cursor"],
        "windsurf": ["windsurf"],
        "copilot": ["copilot"],
        "goose": ["goose"],
        "crush": ["crush"],
        "amp": ["amp"],
        "droid": ["droid"],
    }
    stores = {
        "opencode": [HOME / ".local/share/opencode", HOME / ".opencode"],
        "codex": [HOME / ".codex"],
        "claude": [HOME / ".claude"],
        "gemini": [HOME / ".gemini"],
        "antigravity": [HOME / ".gemini/antigravity-cli", HOME / ".gemini/antigravity"],
        "muse": [HOME / ".muse", HOME / ".config/muse", HOME / ".local/share/muse"],
        "aider": [HOME / ".aider"],
        "cursor": [HOME / ".config/Cursor", HOME / "Library/Application Support/Cursor"],
        "windsurf": [HOME / ".codeium/windsurf", HOME / ".config/Windsurf"],
        "copilot": [HOME / ".copilot"],
        "goose": [HOME / ".local/share/goose", HOME / ".config/goose"],
        "crush": [HOME / ".local/share/crush", HOME / ".config/crush"],
        "amp": [HOME / ".amp", HOME / ".local/share/amp"],
        "droid": [HOME / ".factory"],
    }
    report = []
    for name in sorted(set(tools) | set(stores)):
        executables = [shutil.which(item) for item in tools.get(name, [])]
        executables = [item for item in executables if item]
        present = [str(path) for path in stores.get(name, []) if path.is_dir()]
        if executables or present:
            report.append(
                {
                    "agent": name,
                    "executables": executables,
                    "stores": present,
                }
            )
    return report


def since_filter(days):
    if not days:
        return None
    return time.time() - days * 86400


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="project directory (default: .)")
    parser.add_argument("--json", action="store_true", help="print JSON")
    parser.add_argument("--brief", action="store_true", help="extract bounded excerpts")
    parser.add_argument("--limit", type=int, default=10, help="sessions to report")
    parser.add_argument("--max-chars", type=int, default=1200, help="characters per excerpt")
    parser.add_argument("--since", type=float, help="only sessions newer than N days")
    parser.add_argument("--all", action="store_true", help="ignore the project filter")
    parser.add_argument("--extra-store", action="append", default=[], help="extra JSONL store root")
    args = parser.parse_args()

    project_path = Path(args.project).expanduser()
    if not project_path.is_dir():
        print("error: project directory not found: %s" % project_path, file=sys.stderr)
        return 2
    project = norm(git_toplevel(project_path) or project_path)

    sessions = []
    scanners = [
        scan_opencode,
        scan_codex,
        scan_antigravity,
        scan_claude,
        scan_gemini,
        scan_aider,
        scan_editor_workspaces,
        scan_generic,
    ]
    for scanner in scanners:
        try:
            scanner(project, sessions, args.all)
        except Exception as exc:  # noqa: BLE001 - a broken store must not stop the scan
            print("warning: %s failed: %s" % (scanner.__name__, exc), file=sys.stderr)
    for extra in args.extra_store:
        root = Path(extra).expanduser()
        if root.is_dir():
            needle = project
            for path in root.glob("**/*.jsonl"):
                try:
                    head = path.read_text(encoding="utf-8", errors="ignore")[:12000]
                except OSError:
                    continue
                if needle in head:
                    add_session(
                        sessions,
                        "extra",
                        path.stem,
                        "",
                        iso_from_mtime(path),
                        path,
                        "all" if args.all else "exact",
                        str(root),
                    )

    cutoff = since_filter(args.since)
    if cutoff:
        filtered = []
        for session in sessions:
            try:
                stamp = datetime.fromisoformat(session["time"]).timestamp()
            except (TypeError, ValueError):
                stamp = None
            if stamp is None or stamp >= cutoff:
                filtered.append(session)
        sessions = filtered

    seen = set()
    unique = []
    for session in sessions:
        key = (session["provider"], session["id"])
        if session["id"] and key in seen:
            continue
        seen.add(key)
        unique.append(session)
    sessions = unique

    sessions.sort(key=lambda item: item.get("time") or "", reverse=True)
    sessions = sessions[: args.limit]

    if args.brief:
        for session in sessions:
            session["brief"] = extract_brief(session, args.max_chars)

    agents = discover_agents()
    result = {
        "project": project,
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "agents": agents,
        "sessions": sessions,
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("Context search")
    print("Project: %s" % project)
    print()
    print("Installed agents and stores:")
    if not agents:
        print("  none detected in known locations")
    for agent in agents:
        executable = ", ".join(agent["executables"]) or "not on PATH"
        stores = ", ".join(agent["stores"]) or "no data directory"
        print("  %-12s %s | %s" % (agent["agent"], executable, stores))
    print()
    if not sessions:
        print("No project-matched sessions found.")
        print("Checked known stores and fallbacks. Absence of history is not proof")
        print("that the repository is untouched.")
        return 0
    print("Sessions for this project (newest first):")
    for index, session in enumerate(sessions, 1):
        print()
        print("%d. [%s] %s" % (index, session["provider"], session["time"] or "unknown time"))
        if session["title"]:
            print("   title: %s" % session["title"])
        if session["id"]:
            print("   id: %s" % session["id"])
        print("   match: %s" % session["match"])
        print("   store: %s" % session["path"])
        if session.get("detail"):
            print("   detail: %s" % session["detail"])
        if session.get("brief"):
            print("   brief:")
            for line in session["brief"].splitlines():
                print("     %s" % line)
    print()
    print("Verify before acting: check git status, git log, and the named files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Agent session stores

Where coding agents keep history on disk, and how to match a session to a
project. Paths change between releases and differ across Linux, macOS, and
Windows. Treat this file as a starting map, verify on the machine, and update
it when a store moves.

## Quick reference

| Agent | Executable | Common data root | Typical format | Project match |
|---|---|---|---|---|
| OpenCode | `opencode` | `~/.local/share/opencode/` | SQLite `opencode.db`, older JSON storage | `project.worktree`, `session_v2.directory` |
| Codex CLI | `codex` | `~/.codex/` | SQLite `state_5.sqlite`, legacy `sessions/**/rollout-*.jsonl` | `threads.cwd`, rollout `cwd` |
| Claude Code | `claude` | `~/.claude/` | `projects/<slug>/*.jsonl` | path-encoded project directory |
| Antigravity CLI | `agy`, `antigravity` | `~/.gemini/antigravity-cli/` | SQLite summaries plus `brain/<id>/` | workspace URI in `conversation_summaries` |
| Gemini CLI | `gemini` | `~/.gemini/` | `tmp/<project>/chats/*.json` | recorded project path or directory name |
| Muse | `muse` | `~/.muse/`, `~/.config/muse/`, `~/.local/share/muse/` | varies, JSONL or SQLite | inspect metadata for cwd |
| Aider | `aider` | project root plus `~/.aider/` | `.aider.chat.history.md`, `.aider.input.history` | file lives in the project |
| Cursor | `cursor` | `~/.config/Cursor/` or `~/Library/Application Support/Cursor/` | `workspaceStorage/<hash>/state.vscdb` | `workspace.json` in the same folder |
| Windsurf | `windsurf` | `~/.codeium/windsurf/`, `~/.config/Windsurf/` | SQLite and workspace storage | workspace metadata |
| Cline | VS Code extension | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/` | `tasks/<id>/api_conversation_history.json` | task workspace metadata |
| Roo Code | VS Code extension | `~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/` | task folders with JSON | task workspace metadata |
| Copilot CLI | `copilot` | `~/.copilot/` | JSON and JSONL history | session metadata |
| Goose | `goose` | `~/.local/share/goose/`, `~/.config/goose/` | `sessions/*.jsonl` | message metadata |
| Crush | `crush` | `~/.local/share/crush/`, `~/.config/crush/` | JSON or SQLite | project path |
| Amp | `amp` | `~/.amp/`, `~/.local/share/amp/` | JSONL threads | workspace metadata |
| Factory Droid | `droid` | `~/.factory/` | session JSON | workspace metadata |
| OpenHands | `openhands` | `~/.openhands/` | conversation folders | workspace path |

On macOS, many GUI tools use `~/Library/Application Support/<Vendor>/` instead
of `~/.config`. On Windows, use `%APPDATA%` and `%LOCALAPPDATA%`. The script
checks the common Linux and macOS paths; add `--extra-store` for anything else.

## OpenCode

Current versions keep one SQLite database:

- `~/.local/share/opencode/opencode.db`
- Tables: `project`, `session_v2`, `session_message`, `session_part`
- `project.worktree` holds the repository path.
- `session_v2.directory` holds the session working directory.
- `session_v2.title` is the human session title.
- `session_message.data` is JSON with `text` for user turns and a `content`
  array for assistant turns. Reasoning entries are not context.

Older versions use `~/.local/share/opencode/project/<id>/storage/session/` and
`storage/message/` with one JSON file per object. Search for `session` folders if
the database is absent. `~/.opencode/` may hold the binary or older state.

Read-only query:

```sql
select s.id, s.title, s.time_created, s.time_updated, s.directory
from session_v2 s
join project p on p.id = s.project_id
where p.worktree = '/absolute/project/path';
```

## Codex CLI

Newer builds keep state in `~/.codex/state_5.sqlite`, table `threads`:

- `cwd` is the project path.
- `rollout_path` points at the transcript JSONL.
- `title`, `first_user_message`, and `preview` are useful for a quick brief.
- Timestamps appear as seconds or milliseconds depending on the column.
- `git_branch`, `git_sha`, and `git_origin_url` help confirm the repository.

Older builds store transcripts at:

```text
~/.codex/sessions/YYYY/MM/DD/rollout-YYYY-MM-DDThh-mm-ss-<id>.jsonl
```

`~/.codex/history.jsonl` holds prompt history. `~/.codex/logs_*.sqlite` holds
operational logs, not conversation context.

Rollout JSONL usually contains `response_item` entries with `payload.role` and
`payload.content`, and `event_msg` entries with `payload.type` such as
`user_message` and `agent_message`.

## Claude Code

Transcripts live under a dash-encoded project directory:

```text
~/.claude/projects/-home-dev-projects-skills/<session-id>.jsonl
```

The encoding replaces `/` and `.` with `-`. A session file is JSONL with
`type` values such as `user`, `assistant`, `summary`, and `system`. Message text
sits under `message.content`, which can be a string or an array of blocks.
`~/.claude/history.jsonl` holds command history. Project-local overrides may
appear in `.claude/` inside the repository.

## Antigravity CLI (`agy`)

Data root: `~/.gemini/antigravity-cli/`.

- `conversation_summaries.db` has a `conversation_summaries` table and a
  `conversations_fts` full-text table with `user_body` and `agent_body`.
- `workspace_uris` is a JSON array such as `["file:///home/dev/projects/skills"]`.
- `cache/last_conversations.json` maps workspace paths to conversation IDs.
- `brain/<conversation-id>/` holds per-conversation scratch and uploads.
- `history.jsonl` holds prompt history.
- Older installs may use `~/.gemini/antigravity/` or a GUI directory with a
  similar database.

This store is searchable without reading full transcripts:

```sql
select title, workspace, substr(user_body, 1, 800)
from conversations_fts
where workspace like '%/projects/skills%';
```

## Gemini CLI

Session data commonly lives under:

```text
~/.gemini/tmp/<project-name-or-hash>/chats/session-*.json
~/.gemini/tmp/<project-name-or-hash>/logs.json
```

Project selection is in `~/.gemini/projects.json` or
`~/.gemini/config/projects/*.json` depending on version. Checkpoints may be in
`~/.gemini/tmp/<project>/checkpoints/`. Match on the recorded `cwd`, `project`,
or workspace field, and fall back to the folder name.

## Muse

Muse layouts are not stable across releases. Check these in order:

```text
~/.muse/
~/.config/muse/
~/.local/share/muse/
~/.cache/muse/
```

Look for `*.jsonl`, `*.json`, and `*.sqlite` or `*.db` files. Open databases
read-only and inspect table names for `session`, `conversation`, `thread`, or
`message`. Match on a recorded `cwd`, `workspace`, `project`, or `path` field.
If the layout is unclear, report the store path and that it could not be parsed
instead of guessing.

## Aider

Aider writes into the project itself:

- `.aider.chat.history.md` (full conversation markdown)
- `.aider.input.history` (user prompts)
- `.aider.tags.cache.v*/` (repository map cache, not context)

Global configuration lives in `~/.aider.conf.yml` and `~/.aider/`. Because the
history file is project-local, path matching is automatic. These files are
often gitignored; check for them even when `git status` is clean.

## Cursor, Windsurf, and VS Code agents

GUI editors store per-workspace state in SQLite:

```text
~/.config/Cursor/User/workspaceStorage/<hash>/state.vscdb
~/.config/Cursor/User/workspaceStorage/<hash>/workspace.json
~/.config/Windsurf/User/workspaceStorage/<hash>/state.vscdb
~/.config/Code/User/workspaceStorage/<hash>/state.vscdb
```

`workspace.json` contains the folder URI, which is the reliable match key.
Conversation payloads sit in `state.vscdb` tables such as `ItemTable` and
`cursorDiskKV`. Extension-specific data lives under `globalStorage`.

Cline and Roo Code keep one folder per task:

```text
~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<task-id>/
~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<task-id>/
```

Read `api_conversation_history.json` and task metadata. The Cursor equivalents
sit under `~/.config/Cursor/User/globalStorage/`.

## Copilot CLI and other terminals

Check `~/.copilot/` for JSON or JSONL session history, `~/.copilot/logs/`, and
any project-local `.copilot/` directory. Newer builds may use a single state
file. Search for files modified around the session time when the exact layout
is unknown.

## Generic fallback

When no known layout matches, search targeted data roots rather than the whole
home directory:

```bash
find ~/.config ~/.local/share ~/.codex ~/.claude ~/.gemini ~/.muse \
  -maxdepth 5 -type f \( -name '*.jsonl' -o -name '*.json' -o -name '*.db' \) \
  -mtime -30 2>/dev/null | head -200
```

Then narrow by filename or by grepping a bounded prefix for the project path:

```bash
grep -l --include='*.jsonl' -F '/home/dev/projects/skills' <store-root> 2>/dev/null
```

Do not dump matches. List the stores and inspect only the newest relevant ones.

## Adding a new store

When you find an undocumented layout:

1. Record the agent name, data root, format, and match key here.
2. Add a parser to `scripts/find_agent_sessions.py` if the format is stable.
3. Test against a real project and confirm the path match is exact.
4. Note the version or date you verified, because these paths drift.

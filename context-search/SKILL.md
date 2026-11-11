---
name: context-search
description: Recovers prior work context when a new agent session starts in an existing codebase. Discovers installed coding agents (OpenCode, Codex, Claude Code, Antigravity CLI, Gemini CLI, Muse, Aider, Cursor, Windsurf, Cline, Copilot, Goose, and similar), finds session transcripts or databases tied to the current project, extracts a bounded working brief, and verifies it against the live worktree and git history. Use when joining an unfamiliar repository, resuming interrupted work, or checking whether another agent already investigated or changed the project.
---

# Context Search

A new session in an old repository starts blind. Earlier agents may have made
decisions, hit dead ends, left unfinished edits, or discovered constraints that
are not written in the README. This skill finds that prior context, turns it
into a short working brief, and checks every claim against the current
worktree, git history, and project docs before acting on it.

Prior transcripts are clues, not authority. The live repository is authority.

## Check for skill folder updates

Before applying this skill, check whether the skill folder has updates:

1. Identify the directory where this skill is installed (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, `~/.agents/skills/`, or the active repository).
2. If the folder is inside a git repository, check git status:
   ```bash
   git -C <skill-folder> status --short --branch
   ```
3. When network access is available, check for upstream changes:
   ```bash
   git -C <skill-folder> fetch --dry-run
   ```
4. If updates are available, pull them before proceeding so you use the latest instructions. If the folder is not a git repository, proceed with the installed files.

## When to run

Run this skill at the start of a session when any of these is true:

- The repository has files, branches, or uncommitted changes you did not create.
- The user says "continue", "resume", "where were we", or refers to earlier work.
- You are asked to fix, extend, or review an existing project.
- The git log contains checkpoint commits from another agent or tool.
- The project is unfamiliar and the README does not explain recent changes.

Skip it when the project is brand new, when the user explicitly wants a clean
start, or when the only installed agent is the current one and the current
session already holds the context.

## Workflow

### 1. Establish the real project root

Resolve the path instead of trusting the shell prompt:

```bash
pwd -P
git rev-parse --show-toplevel 2>/dev/null || true
git status --short --branch
git log --oneline -10
```

Use the git top level as the project key. Record the current branch, head
commit, and uncommitted files. These are the facts that later checks compare
against.

### 2. Discover installed agents

Check executables and data directories, not just the tool you are running in:

```bash
for tool in opencode codex claude gemini agy muse aider cursor windsurf \
  code codium copilot goose crush amp droid; do
  command -v "$tool" 2>/dev/null && echo "found: $tool"
done
```

Then inspect the known data roots in `references/agent-stores.md`. Presence of
a directory is enough evidence of prior use. Presence of an executable without a
data directory means the agent is installed but has no history to recover.

The bundled script does both steps and reports what it finds:

```bash
python scripts/find_agent_sessions.py --project "$(git rev-parse --show-toplevel)"
```

Useful options:

```bash
python scripts/find_agent_sessions.py --project . --json        # machine readable
python scripts/find_agent_sessions.py --project . --brief       # bounded excerpts
python scripts/find_agent_sessions.py --project . --brief --max-chars 1500
python scripts/find_agent_sessions.py --project . --all         # ignore path filter
python scripts/find_agent_sessions.py --project . --extra-store ~/.someagent
```

If the script misses a store, read `references/agent-stores.md` and inspect the
location manually. Store layouts change between versions. Never conclude that
no prior work exists from one missing directory.

### 3. Locate sessions for this project

Match on the canonical project path, then on repository identity. Useful keys:

- Exact `cwd` or `worktree` recorded in session metadata.
- Project hash or slug derived from the path (Claude Code uses a dash-encoded
  path; Gemini CLI uses a temporary project directory).
- Workspace URI recorded by GUI agents such as Antigravity.
- The repository remote URL, when the session records it.
- A git worktree that shares the same `.git` directory as the main checkout.

Do not count a session merely because its transcript mentions the project name.
Require a path, workspace, or repository match. Treat a mention-only hit as a
weak lead and label it that way.

### 4. Extract a bounded brief

Read only what answers these questions:

- What was the user trying to accomplish?
- What changed, and which files were touched?
- Which decisions and constraints were established?
- What failed, and why?
- What was left unfinished or explicitly deferred?
- Which commands, tests, or checks were run and what did they return?

Cap the extraction. Read the newest sessions first, take the first few user
requests and the final assistant messages, and stop when the brief is complete.
Do not paste whole transcripts into the conversation. The script defaults to
1200 characters per session and redacts likely credentials.

Write the brief as a short section in your own words:

```markdown
## Recovered context
- Prior agents: <names and session dates>
- Goal: <one or two lines>
- Decisions: <decisions that still apply>
- Changed files or areas: <paths, verified against git>
- Open work: <unfinished items and known failures>
- Conflicts with current state: <claims that no longer hold>
- Evidence checked: <git status, git log, tests, files read>
- Confidence: high, medium, or low, with the reason
```

Store the brief in the conversation or in a gitignored scratch file. Do not
commit raw transcripts or extracted excerpts into the repository unless the
user explicitly asks for a context note.

### 5. Verify every important claim

For each claim worth acting on, check the current source:

```bash
git status --short
git log --oneline --all --decorate -20
git diff --stat
git branch --all
```

Then open the named files and run the named tests if they still exist. A
transcript that says "tests pass" proves only that they passed at that time.
A transcript that says "fixed in auth.ts" proves nothing if `auth.ts` was later
rewritten.

Classify recovered statements:

- **Confirmed**: current files, git, or command output agrees.
- **Stale**: the code moved on, or the claim no longer applies.
- **Unverified**: plausible but no current evidence.
- **Contradicted**: current evidence shows the opposite.

Act only on confirmed facts. Mention stale or unverified items as open
questions, not as established truth.

### 6. Reconcile with git history and project memory

Read the checkpoint commits and recent messages. Skills such as
`context-rich-commits` may already have recorded decisions, verification, and
next steps in commit bodies. Prefer that record over chat transcripts because it
was written against the repository state.

Also read, when present:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`
- `README.md`, `CHANGELOG.md`, `docs/`
- `.agent-context/`, `.serena/`, `.claude/`, `.opencode/` planning notes

Project-local notes are usually more current than global session stores.

### 7. Continue the work

State the recovered context briefly to the user, then proceed with the requested
task. Do not restart work that is already done and verified. Do not silently
trust unfinished edits either: review them before building on them.

If no prior session is found, say so plainly and continue from the repository.
Absence of transcripts is not proof that the code is untouched; someone may
have edited files without an agent.

## What to look for in a transcript

Prioritize signal over volume:

- User requests and corrections, especially repeated corrections.
- File paths in tool calls and patches.
- Exact error messages and the fixes that followed.
- Commands that failed and the workaround chosen.
- Explicit decisions, constraints, and rejected approaches.
- The last few turns, which usually show the live state and next step.
- References to secrets, environment variables, or external services, recorded
  as names only, never values.

Ignore model reasoning, token counts, retries, UI noise, and duplicated tool
output unless it explains a failure.

## Privacy and credential safety

Session stores can contain API keys, tokens, private keys, personal data, and
confidential source. Treat every transcript as sensitive.

- Never print full transcripts, full tool outputs, or environment dumps.
- Run the script with its default redaction. Do not disable redaction for a
  report to the user.
- Do not copy secrets into the brief, commits, issues, or docs.
- If you find a live credential, stop, do not echo it, and follow
  `credential-safety`: rotate it and remove it from history if it was committed.
- Respect the user's privacy. Do not read unrelated projects just because their
  sessions are on disk.
- Do not upload transcripts or session databases to external services.

## Reading stores safely

- Open SQLite databases read-only. The script uses `mode=ro` URIs.
- Never modify, vacuum, or migrate another agent's database.
- Do not hold long transactions; copy nothing unless the user asks.
- Cap file reads by size. Transcripts can be hundreds of megabytes.
- Use `--since` or `--limit` to keep the scan bounded.

## Failure modes

- **Store location changed**: search the data root for `*.jsonl`, `*.db`, and
  `*.json`, then update `references/agent-stores.md` in the skill repository.
- **Encrypted or binary state**: skip it and say it could not be read. Do not
  guess at contents.
- **Database locked**: retry read-only once, then fall back to transcript files.
- **No matches**: report which agents and stores were checked, then continue
  from git. Do not invent prior context.
- **Conflicting sessions**: prefer the newest session, the one whose path
  matches exactly, and the one whose claims survive current verification.
- **Huge transcript**: read the tail first, then targeted searches for error
  strings or file names.

## Report

Include one short line in the final response:

```text
Context search: checked <agents and stores>; found <n> prior session(s) from <dates>;
recovered <goal and open work>; verified against <git status, tests, files>.
```

If nothing was found:

```text
Context search: checked <agents and stores>; no project-matched sessions found;
continued from git state at <commit>.
```

## Rules that keep this honest

- The current worktree, git history, and test output outrank every transcript.
- Never claim another agent's work as your own, and never claim it was verified
  before you checked it.
- Do not resume stale work just because a transcript says it was next. Confirm
  it still matters.
- Do not expose sensitive transcript content in summaries, commits, or reports.
- Keep the brief short. A context dump that nobody reads is not context.
- Match the repository's existing conventions before applying this skill's
  templates.

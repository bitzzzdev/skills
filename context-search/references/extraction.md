# Turning transcripts into usable context

A transcript is raw material. The deliverable is a short brief that lets a new
agent continue correctly without reading a hundred thousand tokens of history.

## Principles

1. Read the newest sessions first. Old context is usually superseded.
2. Prefer metadata and summaries over full transcripts. Titles, first user
   messages, and final assistant messages carry most of the signal.
3. Cap everything. Define a character budget per session and a total budget
   before reading.
4. Redact before display. Tokens, keys, passwords, and private keys must never
   reach the conversation, a commit, or a report.
5. Verify before trusting. A transcript records intent at a point in time, not
   the current state of the repository.
6. Separate fact from inference. Mark what the transcript said, what git shows,
   and what you concluded.

## Budgets

Suggested defaults, adjustable for large or complex projects:

| Item | Default |
|---|---|
| Sessions considered | 5 newest per agent, 10 total |
| User turns read | first 3 and last 3 |
| Assistant turns read | last 2 |
| Characters per session | 1200 |
| Characters in the final brief | 3000 |
| Transcript file size | stop above 50 MB unless targeted search is required |

The script uses `--max-chars` and `--limit` for the first two. Keep the final
brief shorter than the raw excerpts.

## What to extract

### Goal

The user's stated objective, including corrections. Corrections are more
valuable than the first request because they show what was rejected.

### Decisions and constraints

Examples: "stay on Python 3.11", "do not add a database", "the client wants no
analytics", "use the existing design tokens". A decision without a reason is
weaker than one with a reason. Capture the reason when it exists.

### Changes

File paths, modules, migrations, config keys, dependency changes, and tests.
Cross-check each path against `git status` and `git log --stat`.

### Failures

Exact error text is useful. Verbatim stack traces are not, unless the same error
is still present. Record what failed, what was tried, and what worked.

### Open work

Unchecked plan items, TODO comments, failing tests, draft branches, and explicit
"next steps". Treat all of these as leads, not commitments.

### Commands and results

Only commands whose result affects the current task. Record command, outcome,
and when it ran. Old green tests say nothing about the current tree.

## Verification matrix

| Transcript claim | Check |
|---|---|
| "I added feature X" | `git log --all --grep`, `git show`, search the symbol |
| "Tests pass" | run the test command now |
| "Fixed in file Y" | open Y, inspect current content |
| "The bug is in Z" | reproduce or read Z before editing |
| "Do not touch W" | look for the reason in docs, issues, or commit bodies |
| "Branch B has the work" | `git log B`, `git diff main...B` |
| "Dependency D is required" | read the manifest and lockfile |
| "The user wants approach A" | prefer the most recent user statement |

Status labels:

- **Confirmed**: current evidence agrees.
- **Stale**: true earlier, no longer applies.
- **Unverified**: no current evidence either way.
- **Contradicted**: current evidence disagrees.

Only confirmed claims go into the working plan. Stale and unverified claims go
into a short "Open questions" list. Contradicted claims are noted once so nobody
repeats the same assumption.

## Brief template

```markdown
## Recovered context

**Sessions found**
- <agent>, <date>, <session id or file>, <match key>

**Goal**
<one or two sentences>

**Decisions that still apply**
- <decision>, reason, source

**Current state**
- Branch and commit: <value>
- Uncommitted files: <list or none>
- Recent commits: <summary>

**Work already done**
- <change>, verified by <evidence>

**Open work**
- <item>, status: confirmed, stale, or unverified

**Known failures**
- <error summary>, still present: yes or no

**Conflicts**
- <transcript claim that current state contradicts>

**Not read**
- <stores skipped and why>

**Confidence**
<high, medium, or low, with a one-line reason>
```

Drop empty sections. The template is a checklist, not a required shape.

## Redaction

Apply these patterns before showing any excerpt. The script does this by
default. Do not add a bypass for convenience.

```text
sk-[A-Za-z0-9_-]{16,}
gh[pousr]_[A-Za-z0-9]{20,}
github_pat_[A-Za-z0-9_]{20,}
AIza[0-9A-Za-z_-]{20,}
xox[baprs]-[A-Za-z0-9-]{10,}
AKIA[0-9A-Z]{16}
-----BEGIN [A-Z ]*PRIVATE KEY----- ... -----END [A-Z ]*PRIVATE KEY-----
(?i)bearer\s+[A-Za-z0-9._-]{20,}
(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*\S+
```

Names of environment variables are safe to mention. Values are not. If a
transcript contains a live credential, do not repeat it even in redacted form
beyond `[REDACTED]`, and follow the `credential-safety` skill to rotate it.

## Handling large stores

- Query the database instead of loading it. Select only columns you need.
- Use `LIMIT` and `ORDER BY time DESC`.
- For JSONL, read the tail first with a bounded line count.
- For targeted searches, grep for a file name or exact error string, then read
  the surrounding lines.
- If a file is compressed, decompress to a temporary location outside the
  repository and delete it after use.

## Handling multiple agents

When several agents worked on the same project, build a timeline:

```text
date        agent        session             summary
2026-11-02  codex        thread 8f2a         schema draft
2026-11-05  opencode     ses_19ab            API wiring
2026-11-09  claude       a41c9e              tests and cleanup
```

Newer sessions usually override older plans. If two sessions disagree, check
git and the current files; do not average the claims or assume the newest is
right.

## Ending the search

Stop when you can answer these without guessing:

- Why does this repository look the way it does?
- What was the last agent doing?
- What is safe to continue, and what must be rechecked?
- Which files are likely to matter next?

If the answer is still unclear after the newest sessions and git history, report
the gap and proceed carefully. More transcript reading has diminishing returns.

---
name: debug-and-fix
description: Finds the cause of a bug or error and fixes it. Use whenever the user asks Claude or an agent to fix, debug, troubleshoot or investigate something broken, including pasted stack traces, failing tests, build or CI errors, crashes, "it doesn't work", "why is this failing", or "fix this". The agent searches the relevant files, reads the error, checks the official docs online, fixes the root cause and verifies the fix. Also use it when the user tags this skill by name, even if they only describe a symptom. Pairs with error-docs-lookup for the online docs step and with human-writing and context-rich-commits for the commit.
---

# Debug and Fix

Find out why something is broken, fix that cause, and prove the fix works. Don't guess, and don't patch symptoms.

## Check for skill folder updates

Before applying this skill, check whether the skill folder has updates:

1. Identify the directory where this skill is installed (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, or the active repository).
2. If the folder is inside a git repository, check git status:
   ```bash
   git -C <skill-folder> status --short --branch
   ```
3. When network access is available, check for upstream changes:
   ```bash
   git -C <skill-folder> fetch --dry-run
   ```
4. If updates are available, pull them before proceeding so you use the latest instructions. If the folder is not a git repository, proceed with the installed files.

## Rules

1. **Reproduce first.** Run the failing command, test or request and capture the exact error. If you can't reproduce it, say so and ask for the missing piece (input, env, version) before changing code.
2. **Read before editing.** Open the files the error points at and the code around them. Never edit a file you haven't read.
3. **Fix the root cause.** No swallowing exceptions, no `try/except: pass`, no disabling tests, no `@ts-ignore` or `# noqa` to silence a real problem.
4. **Smallest change that works.** Don't refactor or reformat unrelated code while fixing a bug.
5. **Verify.** Rerun the original failing command and the nearby tests. Report what you ran and what happened. If you couldn't run anything, say "not verified".
6. **Don't invent.** Only claim a cause you saw in the code, logs or docs.

## Workflow

### 1. Capture the problem
Get the exact error text, the command that triggers it, and what the user expected. If they only said "it's broken", run the project's test, build or start command to find out.

### 2. Search the codebase
Work from the error outward:

```bash
python scripts/find_error_context.py <error-log-or-file>
```

The script pulls file paths, line numbers, error names and quoted identifiers out of a stack trace or log and prints the matching lines with context. Without it, do the same by hand:

- Open every file and line named in the stack trace, top to bottom.
- `grep -rn` for the error message, function name and variable names.
- Check recent changes with `git log -p -5 -- <file>` and `git diff`. A bug that just appeared usually sits in the latest change.
- Read config and dependency files: `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `.env.example`, lockfiles.
- Note the installed versions of the libraries involved (`pip show`, `npm ls <pkg>`, and so on).

### 3. Check for other errors
Look past the first message. Scan the full log for earlier warnings, deprecation notices, a second traceback, or a failure in a different test. The first error in the log is often the real one, and the last is often fallout.

### 4. Read the online docs
Do this when the error involves a library, framework, API, CLI tool or platform, or when the cause isn't obvious from the code.

- If the `error-docs-lookup` skill is installed, use it.
- Otherwise search the web with the exact error text plus the library name and version, then open the official docs, changelog or migration guide. Prefer official docs and the project's issue tracker over blog posts and forum answers.
- Check that the doc matches the version installed. Many bugs are an API that changed between versions.
- If the web isn't available, say so and work from the code and installed package sources (`node_modules`, `site-packages`).

### 5. Form a cause, then fix
Write the cause in one or two sentences before editing: what is wrong, where, and why it produces this error. If you have two plausible causes, test the cheaper one first (a print, a minimal repro, a single test).

Then make the fix. Match the project's existing style.

### 6. Verify
- Rerun the exact command that failed.
- Run the tests for the files you touched, then the wider suite if it's quick.
- If no test covers the bug, add a small one that fails without the fix and passes with it.
- Remove any debug prints or temporary files you added.

### 7. Report
Keep it short and plain:

- What was wrong and where (file and line).
- What you changed.
- What you ran to verify, and the result.
- Anything you noticed but did not change.

If the project uses commits, write the message with `context-rich-commits` and keep the prose clean with `human-writing`.

## If you get stuck

After two failed fixes, stop and rethink. Reread the error from scratch, question your assumption about where the bug is, and look for a simpler explanation (wrong version, stale cache, missing env var, wrong working directory, file not saved). If it's still unclear, tell the user what you tried, what you ruled out and what you need.

## Common causes worth checking early

- Version mismatch between a library and its docs or plugins.
- Stale build output, cache or lockfile. Clear and rebuild before assuming a code bug.
- Missing or misnamed environment variable.
- Off-by-one, null or undefined, or a type that changed shape.
- Async code not awaited, or a race between two steps.
- Path problems: relative paths, case sensitivity, Windows versus Linux separators.
- A test that depends on order, time or network.

## Safety

Don't run destructive commands (`rm -rf`, `git reset --hard`, dropping tables, force push) to make an error go away. Don't print or commit secrets you find in logs or env files. Ask before changing anything outside the project folder.

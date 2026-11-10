---
name: credential-safety
description: Prevents agents from committing or pushing API keys, passwords, tokens, private keys, certificates, or other credentials to remote repositories. Use before commits, pushes, releases, and whenever configuration or authentication code changes.
---

# Credential Safety

Keep secrets out of commits and remote repositories. Treat the current
worktree, index, commit history, and remote branch state as separate surfaces
that must be checked before pushing.

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

## Inspect before committing or pushing

- Read repository instructions and identify the intended secret-management
  method, such as environment variables, ignored local files, or a secret
  manager.
- Inspect staged, unstaged, and untracked files. Check filenames and content
  for API keys, access tokens, passwords, connection strings, session cookies,
  private keys, certificates, signing files, cloud credential files, and
  production configuration.
- Check the commits being pushed, not only the current working tree. A secret
  in an earlier commit is still exposed when that commit is reachable from the
  remote branch.
- Use available repository-approved secret scanners and review their full
  results. If no scanner is available, use targeted searches and inspect
  suspicious files without printing complete credential values.
- Check ignore rules for local secret files. Do not treat `.gitignore` as
  proof that a file is safe if it is already tracked.

## What to do when a secret is found

- Stop the commit or push. Do not work around a scanner finding by weakening
  patterns, hiding output, or adding the file to an allowlist without review.
- Remove the secret from the change and replace it with a documented
  placeholder or environment-based configuration.
- Revoke or rotate any exposed credential before continuing. Removing a value
  from the latest file does not invalidate a credential already present in
  history or logs.
- If the secret exists in reachable history, explain the exposure and use the
  repository's approved history-rewrite process only with explicit
  authorization. Coordinate force-pushes and verify every affected remote
  branch afterward.
- Never paste full secrets into chat, commit messages, issue comments, logs, or
  reports. Identify the file, type, and remediation state without exposing the
  value.

## Push gate

Before any remote push, verify that:

1. The staged diff contains no credentials.
2. The commits being pushed contain no credentials.
3. Secret files are ignored and not tracked unless the repository explicitly
   requires a safe, non-secret template.
4. The scanner result and manual review cover the complete push range.
5. Any finding is resolved, rotated, and documented before proceeding.

Do not claim a push is safe because tests pass, the scanner was not installed,
or no obvious secret was noticed. Report missing tooling or incomplete coverage
as an unresolved blocker.

## Required response

Report the files and commit range checked, the scanner or searches used, the
result, any finding and rotation status without revealing secret values, and
whether the push is safe, blocked, or not yet checked.

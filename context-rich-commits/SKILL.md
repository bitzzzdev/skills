---
name: context-rich-commits
description: Turns git history into the project's long-term memory. Use this skill every time you commit, write or suggest a commit message, push, finish a work session, hand work off, or start work on an existing repo (to read the history first). Commit messages explain why, what changed, decisions, gotchas, verification and next steps, and periodic checkpoint commits record the full state of the codebase so any person or agent who joins later can get up to speed from git log alone. Also trigger on requests like commit this, save my changes, checkpoint, handoff, document what changed, or get me up to speed on this repo.
---

# Context-Rich Commits

A repo's history is the one record that every person and every agent can read, and it never goes stale in the way a separate notes file does. This skill makes commits carry that knowledge. Someone who starts on the project tomorrow, with no memory of today's session, should be able to read the log and know what the project is, how it is laid out, what changed recently, why, and what is left to do.

It works in three layers:

1. **Every commit** explains itself: the reason, the change, the decisions, the gotchas, how it was checked.
2. **Checkpoint commits** record the complete state of the project at a point in time.
3. **A reading routine** that anyone starting work runs first, so the knowledge actually gets used.

## Rules that always apply

1. **Only record what you verified.** Facts come from the diff, command output, the files themselves, or the conversation. Never invent a reason, a test result, a decision or a file's purpose. If you didn't run the tests, write `Verified: not run`. If the reason is unknown, say so in the message instead of guessing.
2. **No secrets or personal data.** Commit messages are permanent and public in most repos. Never include tokens, keys, passwords, private URLs or personal details, even if they appeared in the conversation.
3. **No emoji, no em dashes, no AI filler.** Plain words, same as the `human-writing` skill. No "robust", "seamless", "comprehensive", no "This commit...".
4. **One logical change per commit.** If the diff mixes a refactor, a fix and a feature, split it with `git add -p` or by path and commit each separately.
5. **Don't stop to ask whether the message is good.** Write it and commit. Pushing follows the project's or user's standing instruction, not a prompt from this skill.
6. **Don't rewrite pushed history to fix a message.** Add a follow-up commit or a checkpoint that corrects the record.
7. **Follow the repo's existing subject style** if it has one (for example Conventional Commits). Keep the body format from this skill either way.

## The commit message

```
<Subject: imperative, specific, 72 characters or fewer, no trailing period>

Why: the problem or trigger. What was wrong or missing, and who or what
it affected. One to three sentences.

Changes:
- `path/to/file.ext`: what changed and what it does now
- `other/file.ext`: ...

Decisions:
- Chose X over Y because Z. Rejected options and why, so nobody retries them.

Gotchas:
- Anything that looks wrong but is intentional, hidden coupling, ordering
  requirements, things that will break if changed.

Verified: the exact commands run and the result, or "not run".
Status: complete, or partial with what remains.
Next: the follow-up work, if any.
Refs: issue, PR or doc links.
```

Include only the sections that apply. Never write empty sections or "N/A". Wrap prose at about 72 columns.

### How much to write

| Change | Message |
|---|---|
| Typo, comment, formatting, version bump | Subject only |
| One file, one behavior | Subject plus `Why:` and `Verified:` |
| Normal feature or fix | Full format above |
| Migration, dependency change, architecture change, anything risky | Full format, with `Decisions:` and a note on rollback or impact |

### What makes it useful

- **Describe the result, not just the diff.** The reader can see the diff. They cannot see why it exists or how the pieces now fit. Say how the feature works after the change and where its entry point is.
- **Name things, not lines.** Use file paths, function names, config keys and commands. Line numbers go stale immediately.
- **Record the why behind choices.** "Used a queue because the API rate-limits to 10 requests per second" saves the next person an afternoon.
- **Record dead ends.** If an approach failed, say what you tried and what broke.
- **Say what is unfinished.** A partial commit that says it is partial is useful. One that implies completeness is a trap.
- **Note changes that affect others:** new env vars, new dependencies, changed commands, schema changes, anything that needs action after pulling.

## Checkpoint commits

A checkpoint is an empty commit whose message is a full snapshot of the project. It adds no files, so it never clutters the tree, and anyone can find it with `git log --grep='^checkpoint:'`.

Make one:
- on the first commit of a new project,
- at the end of every work session and before any handoff,
- after a major feature, refactor or dependency upgrade,
- when the last checkpoint is more than about 25 commits old,
- whenever the user asks.

Create it from the real repo state. Open the files, run `ls`, read `package.json` or the equivalent, check the test command. Don't copy the previous checkpoint forward blindly: keep what is still true, drop what is stale, and add what changed.

```bash
git commit --allow-empty -F - <<'MSG'
checkpoint: <one line on the current state of the project>

Project: ...
Run: ...
...
MSG
```

The full template, with every required section and an example, is in `references/checkpoint-template.md`. Read it before writing the first checkpoint in a repo.

## When you start work on a repo

Before changing anything, read what the history already knows:

```bash
sh /path/to/context-rich-commits/scripts/project_context.sh
```

It prints the latest checkpoint, every commit since it, and the current working tree status. The equivalent by hand:

```bash
git log --grep='^checkpoint:' -n 1 --format='%h %ad%n%n%B' --date=short
git log <checkpoint-hash>..HEAD --format='--- %h %ad%n%B' --date=short
git status --short
```

To learn about one file or symbol:

```bash
git log --follow -p -- path/to/file     # history of a file
git log -S'functionName' --oneline      # when a symbol was added or removed
git blame -w path/to/file               # who changed each line and which commit
```

If there is no checkpoint yet, read the last 30 commits, orient yourself in the files, then make a checkpoint so the next reader doesn't repeat the work.

If the clone is shallow, run `git fetch --unshallow` first, or the history will be incomplete.

## Workflow when committing

1. Run `git status` and `git diff --staged`. If the diff mixes concerns, split it.
2. Collect facts: the diff, test output, and what the conversation says about why.
3. Write the message with the format above.
4. Check it: `python /path/to/context-rich-commits/scripts/lint_commit.py <message-file>`. Fix every reported problem.
5. Commit with `git commit -F -` and a heredoc, so multi-line bodies survive intact.
6. At the end of the session, add a checkpoint.

Enforce it for everyone by installing the linter as a hook in the repo:

```bash
cp /path/to/context-rich-commits/scripts/lint_commit.py .git/hooks/commit-msg.py
printf '#!/bin/sh\npython3 "$(dirname "$0")/commit-msg.py" "$1"\n' > .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

Hooks live in `.git` and are not cloned, so each clone installs its own.

The linter rejects emoji, em and en dashes, likely secrets, vague subjects such as `update` or `fix stuff`, over-long subjects, and substantial changes with no body. It also checks that a checkpoint has all its required sections. It prints each problem and exits non-zero, so a bad message fails loudly instead of slipping through.

More worked examples are in `references/examples.md`.

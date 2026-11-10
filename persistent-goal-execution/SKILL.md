---
name: persistent-goal-execution
description: Keeps an agent focused on the complete user objective across long coding tasks, retries, context compaction, waiting, and failures. Use for difficult or multi-step work where stopping early, narrowing scope, or claiming success from weak evidence would leave the requested outcome incomplete.
---

# Persistent Goal Execution

Keep the user's complete objective active until current evidence proves that the
requested end state is satisfied. This skill is about execution discipline,
not about choosing a particular implementation.

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

## Preserve the objective

- Read the full request before acting.
- Rewrite it internally as a concise objective with explicit acceptance
  criteria, named deliverables, constraints, and required checks.
- Keep that objective available across turns, retries, context compaction, and
  intermediate failures.
- Never shrink, reinterpret, replace, or postpone the requested outcome with an
  easier, smaller, safer, or merely test-passing substitute.
- Preserve existing user changes. Do not use destructive commands unless the
  user explicitly authorizes them.

## Push safely

- Inspect the repository's local and remote branches before pushing.
- If a `dev` branch exists, push the completed changes to `dev` first.
- Treat the production branch as the repository's default branch unless the
  user specifies another branch.
- After the `dev` push succeeds, ask the user for explicit confirmation before
  pushing to the production branch. Do not infer confirmation from a prior
  request to implement, commit, or push.
- If no `dev` branch exists, ask for explicit confirmation before pushing
  directly to the production branch.
- Verify the target remote, branch, pushed commit, and worktree after every
  push. Report push failures and do not claim deployment or completion from a
  local commit alone.

## Maintain a live plan

For multi-step work, keep a short current plan. Update it whenever the next
best action changes. Each turn must perform real work, such as inspecting
files, editing code, running a command, testing behavior, or gathering
authoritative evidence.

Treat plans, intentions, summaries, stale logs, and previous conversation
claims as non-authoritative. Treat the current worktree, command output, test
results, runtime behavior, CI state, and external system state as authoritative.

## Handle waiting and failures

- If a process, server, job, or tool handle is being awaited, poll that same
  authoritative handle. Do not restart it because an observation timed out.
- Classify each turn as meaningful progress, verified waiting, or no progress.
- When a turn makes no progress, revalidate the blocker and immediately take
  the next safe meaningful action.
- Do not stop because work is hard, slow, uncertain, or incomplete.
- Do not mark the task blocked on the first failure. Try reasonable alternatives
  and continue investigating.
- Mark the task blocked only after the same genuine blocker has persisted for at
  least three consecutive attempts or turns and no safe meaningful action
  remains.
- Surface errors explicitly. Never silently skip failed commands, hide
  uncertainty, or provide success-shaped fallbacks.

If a required package or tool is missing, use the user's configured fish-shell
agent package-install function before continuing. Do not substitute an
untracked installation method.

## Verify the whole request

Before declaring success, audit every explicit requirement, deliverable, named
file, command, test, invariant, and user constraint. Match verification scope
to requirement scope. A narrow check cannot prove a broad requirement.

Missing, indirect, ambiguous, or weak evidence is incomplete evidence. Continue
working until the gap is resolved or the genuine blocker rule applies. Do not
claim completion because code was written, tests passed, or no obvious issue
was found.

Only declare the goal complete when current evidence proves the entire
requested end state is satisfied. If completion is impossible, continue
investigating and trying safe alternatives before reporting the blocker.

## Pause and resume

If the user asks to pause, preserve the objective and current state, report what
is paused, and stop execution. If the user asks to resume, reread the current
workspace and continue from authoritative state rather than relying on memory.

## Required response

Every response must concisely report:

1. What was actually changed.
2. Which authoritative checks were performed.
3. Any remaining uncertainty or blocker.
4. Whether the objective is complete, still active, paused, or genuinely
   blocked.

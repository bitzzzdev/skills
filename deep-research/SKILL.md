---
name: deep-research
description: Reconstructs a feature's behavior and integration context from a user-provided repository before implementing an equivalent change in the current repository. Use when a user asks to copy, port, reproduce, or adapt a feature from another codebase.
---

# Deep Research

When a user asks to copy a feature from another repository, understand the
source behavior and the target architecture before writing code. Reproduce the
required capability, not a shallow file copy or an unverified approximation.

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

## Define the transfer

- Identify the source repository, target repository, feature name, requested
  behavior, constraints, and expected validation.
- Separate behavior that must match from source-specific names, paths,
  frameworks, dependencies, and deployment assumptions.
- Confirm the source repository and revision are accessible. If the source,
  feature scope, or license is unclear, surface the uncertainty before
  implementing.
- Respect the source repository's license and attribution requirements. Do not
  copy code or assets when the license does not permit the intended use.

## Explore the source repository

- Inspect repository instructions, `AGENTS.md` files, README files, manifests,
  build files, CI configuration, tests, and relevant git history.
- Locate the feature entry point, public API, configuration, data models,
  state transitions, side effects, error handling, and user-facing behavior.
- Trace callers and dependencies in both directions. Read the surrounding
  code, not only the first matching function or file.
- Follow the runtime path from input to output and record important invariants,
  defaults, validation rules, persistence, concurrency, retries, and cleanup.
- Read focused tests and fixtures to identify edge cases and compatibility
  expectations. Treat tests as evidence, not as the complete specification.
- Record the source revision, relevant files, symbols, and commands used so
  another agent can reproduce the research without guessing.

## Map the target repository

- Reinspect the current target worktree and read its local instructions before
  changing anything.
- Find the target subsystem's entry points, extension points, conventions,
  dependency policy, configuration approach, and validation commands.
- Compare source and target assumptions. Identify what can be reused as a
  concept, what must be translated, and what cannot be carried over safely.
- Prefer existing target helpers and patterns over introducing source-specific
  abstractions or unnecessary dependencies.
- Define acceptance criteria that cover behavior, integration, errors,
  compatibility, documentation, and tests.

## Implement and verify

- Implement the feature in the target repository using its conventions and
  existing abstractions. Keep the change scoped to the requested behavior.
- Add focused tests for the transferred behavior and important edge cases.
  Update configuration, documentation, and CI only when the feature requires
  them.
- Run the narrowest relevant checks first, then broaden validation when the
  feature crosses package, runtime, or integration boundaries.
- Compare observed target behavior with the source behavior and acceptance
  criteria. Do not claim parity because the code compiles or one test passes.
- If the source cannot be fully reproduced, report the exact gap, its cause,
  attempted alternatives, and the safest useful partial result.

## Required response

Report the source repository and revision researched, the behavior and
integration points understood, the target files changed, the authoritative
checks performed, any intentional differences or license constraints, and
whether the requested feature is complete, still active, paused, or blocked.

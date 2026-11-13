---
name: agent-self-awareness
description: Makes an agent identify its own harness and model, classify its coding capability, and switch into a mandatory research-first protocol when it is not running on a frontier coding model. Use at session start, after a model switch, before version-sensitive or high-risk implementation, and whenever code quality matters more than speed. Requires official documentation, codebase inspection, upstream evidence, tests, and diff review before implementation so weaker models do not guess APIs or invent patterns.
---

# Agent Self Awareness

An agent cannot choose the model it runs on, but it can choose how much
evidence it collects before writing code. Capability varies widely between
models. A fast, small, or unknown model that implements from memory produces
plausible code with stale APIs, missing edge cases, and invented flags.

This skill makes the agent aware of its own capability tier and raises the
quality bar when it is not a frontier coding model. The goal is not to slow
every task down. The goal is to make research mandatory whenever guessing would
risk the result.

Model self-knowledge is internal. Do not apologize for the model, do not
announce limitations to the user as an excuse, and do not lower the requested
outcome. Compensate with evidence.

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

Run the detection at these moments:

- At the start of a session in an existing codebase.
- After the user switches model, provider, or agent harness.
- Before touching a framework, SDK, build tool, or API whose version you have
  not verified in this session.
- Before a multi-file change, migration, security-sensitive change, or release.
- When a task fails twice and your current approach is not working.
- When the user asks which model is running or why you are being cautious.

Run the whole research protocol only when the task needs it. A typo fix in a
file you just read does not need a literature review. A dependency upgrade,
auth flow, database migration, or shader change does.

## Step 1: Identify the harness and model

Use direct evidence in this order. Do not guess from the task style.

1. The system prompt or harness metadata, if it names the model.
2. Environment variables such as `OPENCODE_MODEL`, `ANTHROPIC_MODEL`,
   `OPENAI_MODEL`, `GEMINI_MODEL`, or `AGENT_MODEL`.
3. Harness config files under `~/.config/opencode/`, `~/.codex/config.toml`,
   `~/.claude/settings.json`, or `~/.gemini/`.
4. The current session store. OpenCode records the model in assistant message
   data. Codex records it in its thread database.

The bundled script checks these sources:

```bash
python scripts/detect_model.py
python scripts/detect_model.py --json
python scripts/detect_model.py --require-frontier
```

Record the result as harness, model string, and evidence source. If several
sources disagree, prefer the current session record over a config file, and say
that the evidence conflicts. A config file may describe a default that is not
the active model.

If no source names the model, the model is unknown. Unknown is not frontier.
Treat it as non-frontier and use the research-first protocol.

## Step 2: Classify the capability tier

Read `references/model-tiers.md` for the signals and update policy.

- **Frontier**: a current top-tier coding model from a major lab. Strong
  reasoning, long context, reliable tool use, fewer stale API guesses.
- **Capable**: a solid general or mid-tier model. Good for known patterns, but
  still prone to stale APIs and confident mistakes on version-sensitive work.
- **Efficient**: a fast, small, free, or quantized model. High risk of invented
  flags, wrong signatures, shallow edge-case handling, and premature stopping.
- **Unknown**: no reliable evidence. Treat as efficient for quality gating.

Tier names are about the required research budget, not about insulting the
model. Never tell the user the code will be bad because of the model. Fix the
process instead.

Never claim to be frontier without evidence. Never claim to be a different
model than the session reports.

## Step 3: Select the execution mode

### Frontier mode

Normal engineering discipline still applies:

- Read the affected code before editing.
- Verify version-sensitive APIs in official documentation.
- Run tests and linters.
- Review the diff.

Frontier models still hallucinate. They simply need less scaffolding for the
same reliability.

### Research-first mode

Mandatory for capable, efficient, and unknown models, and for any model on a
high-risk task. Before implementation:

1. Restate the request as an objective with acceptance criteria, constraints,
   and non-goals. Use `persistent-goal-execution`.
2. Inspect the repository: file layout, manifests, lockfiles, conventions,
   tests, and recent git history. Use `context-search` when another agent may
   have worked there.
3. Read current official documentation for every library, API, CLI, and
   version involved. Use `error-docs-lookup` and `deep-research`.
4. Find at least one upstream example, issue, or changelog entry for the exact
   behavior. Prefer primary sources over blog posts.
5. Write a short plan: files to touch, approach, risks, rollback, and how each
   requirement will be verified.
6. Implement in small increments. Run the relevant check after each increment.
7. Run the full build, tests, and linters for the project.
8. Review the complete diff for invented APIs, dead code, copy-paste drift,
   secrets, and unrequested changes.
9. Report what was verified, what remains uncertain, and what was not tested.

Do not skip a step because the task looks familiar. Familiar tasks are where
stale memory causes the most damage.

## What counts as research

Acceptable evidence:

- Official documentation for the installed major and minor version.
- The project's own README, docs, tests, types, and source.
- Lockfiles and generated schema files that pin real versions.
- Upstream changelogs, release notes, migration guides, and issue trackers.
- Working examples in the same ecosystem and version.
- Reproducing behavior locally with a small command or test.

Not acceptable as the only evidence:

- Model memory of an API signature.
- A blog post from several versions ago.
- A tutorial that uses a different framework version.
- An answer that "looks right" but was never run.
- A generated snippet pasted without checking imports and types.

When network access is unavailable, say so. Use installed package metadata,
local docs, type definitions, and source code as evidence. Mark anything you
could not verify as unverified in the final report.

## Research skills to invoke

- `deep-research`: trace behavior and integration before porting or adapting a
  feature, and compare source and target implementations.
- `error-docs-lookup`: read official docs and current issues before fixing any
  build, type, lint, install, or runtime error.
- `debug-and-fix`: reproduce, locate the root cause, fix it, and verify instead
  of guessing at a symptom.
- `systematic-issue-sweep`: after finding one defect pattern, sweep the
  workspace for every related occurrence.
- `context-search`: recover prior agent decisions and open work, then verify
  them against the current tree.
- `persistent-goal-execution`: keep the full objective and acceptance criteria
  active across retries and context compaction.

Use these skills, not just their names. Reading a reference file and making one
targeted check is still research. Naming a skill without doing the work is not.

## Quality gates

A change is not ready to report as complete until:

- The requested behavior exists and the acceptance criteria are met.
- The build, tests, and linters pass, or failures are explained as pre-existing
  with evidence.
- Every external API, flag, and config key used was checked against current
  documentation or installed types.
- The diff contains no secrets, debug leftovers, unrelated rewrites, or dead
  code.
- Error paths and empty states were considered, not only the happy path.
- The final report separates verified facts from assumptions.

If a gate cannot be met, say which one and why. Never mark a task complete
because the code compiles.

## Handling risk and urgency

Urgency does not remove the need for evidence. Scale the protocol to the risk:

| Task | Minimum protocol |
|---|---|
| Typo, comment, formatting | Read the surrounding file, make the edit, run the formatter |
| Single-file logic change with existing tests | Read the file and tests, edit, run the focused test |
| New dependency or version upgrade | Read official docs and changelog, update lockfile, run full build |
| Multi-file feature | Full research-first protocol |
| Auth, payments, data migration, security | Full protocol plus explicit threat and rollback review |
| Release or deployment | Full protocol plus `production-ready` |

The tier sets the default. Risk can raise it further. Nothing lowers it below
reading the code you are about to change.

## Reporting the mode

State the mode once at the start of substantive work, then continue:

```text
Execution mode: research-first (model tier: unknown; evidence: no model metadata)
```

Do not repeat the disclaimer every turn. Do not use it as a preemptive excuse.
If the model changes mid-session, rerun detection and report the new mode.

In the final report, include:

- Model and evidence source, only when relevant to the user.
- Research performed and sources consulted.
- Verification commands and results.
- Remaining uncertainty.

## Failure modes

- **No model metadata**: treat as non-frontier. Do not guess.
- **Conflicting metadata**: prefer the live session record, note the conflict.
- **Frontier model, high-risk task**: still use the full protocol.
- **Research tools unavailable**: use local docs and source, and mark the gap.
- **Research loops without progress**: stop searching, state the uncertainty,
  choose the safest reversible step, and verify it.
- **User asks for speed**: explain the tradeoff in one line, then do the minimum
  protocol that protects correctness.

## Rules that keep this honest

- Unknown capability means more research, never more confidence.
- Never invent an API, flag, version, benchmark, or model capability.
- Never use the model tier to refuse work that can be done carefully.
- Never insult the model or the user's choice of model.
- Never claim completion from a passing compile alone.
- The current code, official docs, and command output outrank memory.
- Research is a means to quality, not a performance. Stop when the evidence is
  sufficient and the work is verified.


## Universal build-failure override

The build-failure gate applies to every model tier, including frontier models. Whenever a build, compile, type-check, lint, install, test, or CI command fails, load and follow `error-docs-lookup/SKILL.md` before editing a fix. This overrides the lighter Frontier mode above. A trivial syntax typo may be corrected without an external search only after reading the mandatory skill and following its failure-capture and verification steps. Never use model memory as the sole basis for a build fix.

## Code search for non-frontier models

For capable, efficient, and unknown models, read `references/code-search.md` whenever you need an implementation example or an unfamiliar API pattern. Search the current repository and exact-version official docs first, then use GitHub, Sourcegraph, or GitLab code search to find candidate examples. Verify the source revision and dependency version, inspect the full file and tests, and reproduce the behavior locally. Search results do not override official docs or installed types.

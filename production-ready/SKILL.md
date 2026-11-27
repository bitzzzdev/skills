---
name: production-ready
description: Orchestrates a complete production-level finish by directing the agent to use all other relevant skills in its toolkit (agent-self-awareness, token-optimizer, context-search, parallel-agent-orchestration, persistent-goal-execution, credential-safety, deep-research, debug-and-fix, error-docs-lookup, human-writing, context-rich-commits, Ponytail review and audit skills, google-seo-skill, and domain-specific skills), auditing the repository, updating changelogs, READMEs, documentation, legal files, and community standards. Use whenever the user asks to get a project production-ready, ship it, prepare a release, finish up, or review what is missing before launch. Always begins with a mandatory skill relevance check, so no relevant skill in the toolkit is skipped, and always runs with thinking turned off and a live todo list (token-optimizer).
---

# Production Ready

A project is not finished when the code works. It is finished when someone else can install it, understand it, trust it, and see what changed. This skill directs the agent to orchestrate all other relevant skills in its toolkit to bring the codebase to a production-level release: recover prior agent context, changelog, documentation, terms and rules, followed by a multi-skill refresh pass that reruns tests, looks up errors in official documentation, evaluates search indexing, verifies writing style, and commits with full context.

Work on what the project actually has. Read the code and git history first, write second. Never invent features, versions, dates, company names, addresses, or legal facts. If a fact is unknown, leave a clearly marked placeholder like `[COMPANY NAME]` and list it in the final report.

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

## Mandatory skill relevance check

Self-awareness is not optional, and neither is this check. Before any substantive work, and again whenever the task changes scope, the agent decides for itself which skills in its toolkit apply. It does not wait for the user to name them, and it does not rely on the lists in this file, which go stale as skills are added.

1. **Inventory.** List every skill available: the harness skill listing, installed skill folders (`~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, `~/.agents/skills/`), and the skills repository. Read each skill's name and frontmatter description. The `dev` branch of the skills repository holds the current set.
2. **Always on.** `agent-self-awareness` and `token-optimizer` run every time, and so does this check. `credential-safety` and `context-rich-commits` apply whenever anything is committed or pushed. `human-writing` is mandatory for every task and every user-facing or project-facing sentence, including chat replies, plans, code, comments, logs, documentation, legal text, commit messages, and handoffs. Load its full SKILL.md before work. Apply its no-emoji and human-writing rules throughout the session, not only when editing prose. `context-search` applies on a new session in an existing codebase.
3. **Match.** Compare each remaining skill's description against the task, the project type, and the files being touched. Mark it USE or SKIP and write a one-line reason. When unsure, read the skill's `SKILL.md` before deciding. Do not skip a skill only because it is missing from the lists in this file.
4. **Load.** Read the full `SKILL.md` of every USE skill, plus any reference file or script it tells you to read, before acting. Naming a skill without reading it does not count as using it.
5. **Repeat.** Run the check again when the work shifts: a new file type or framework, a failure, a deployment step, a second repeated error, or a model or harness switch.
6. **Overlap and conflict.** Apply compatible instructions from several skills together. If two skills conflict, the user's current instruction wins, then the more specific skill. Say which won in the report.
7. **Not installed.** If a needed skill is missing, do its checks from the matching reference file, note the gap, and never claim to have run it.

Record the outcome as a short table of skill, USE or SKIP, and reason. It goes in the final report.

## Mandatory token-optimizer mode

`token-optimizer` is always on, like `agent-self-awareness`. Every agent working under this skill runs with thinking off and works from a live todo list instead of reasoning its way through the task.

1. **Turn thinking off first.** Before the first substantive step, follow `token-optimizer/SKILL.md` and `token-optimizer/references/agents.md`: detect the active agent, read its config, back it up, and disable reasoning and thinking (extended thinking, reasoning effort, thinking budget). Record the agent, the config path, and the before and after values in `.progress.md`. If a harness or model cannot go fully off, clamp it to the lowest setting and record that. Never claim thinking is off without reading the setting back. Change only the config files `token-optimizer` lists, and keep the backup.
2. **Do not think, follow the list.** Do not spend tokens on extended deliberation, long plans, or narrated reasoning. Pick the next action by reading the next open item in `.progress.md`, do it, and update the file. Keep any text between tool calls to a line.
3. **One interactive todo list.** `.progress.md` in the project root is the single source of truth for what is done, in progress, and pending. If the project already has a tracking file or handoff note, use that instead and do not start a second list.
   - Break the objective and its acceptance criteria into items before starting. One item is one verifiable action.
   - Re-read the file before each item, after each context compaction, and when resuming a session.
   - Mark an item in progress before starting it. Mark it done only after its check passed.
   - Add items the moment work turns them up: a failing test, a bug, a skill from the relevance check, a doc gap, a blocker. Do not hold them in memory.
   - The user can edit the file at any time to add, reorder, or remove items. Re-read before acting and treat their edits as instructions.
   - Other agents read and update the same file. Preserve their entries and never rewrite the whole list.
4. **Plain markers.** Use `[ ]` pending, `[~]` in progress, `[x]` done, `[!]` blocked. No emoji, since `human-writing` forbids them in project files. Keep secrets out of the file.
5. **Evidence still required.** Thinking off does not lower the bar. The research-first mode from `agent-self-awareness`, official documentation lookup, tests, and diff review still happen, but as tool calls and todo items, not as reasoning. Each research step is an item with its result noted beside it. When the two skills seem to conflict, the evidence requirements stay and only the form changes.
6. **Cannot disable.** If the config cannot be edited or the model has a reasoning floor, say so in the file and the report, keep the list discipline, and continue.
7. **Final state.** Leave `.progress.md` current: nothing marked done without evidence, and open items with the next action at the top of pending. It is the handoff for the next agent.

## Multi-Skill Orchestration

When finishing a project, you act as the orchestrator across your entire skill ecosystem. Do not treat production readiness as simply editing markdown files. Proactively invoke and apply the other skills available in your environment when their criteria are met:

0. **Skill folder update check**: Inspect git status in active skill folders (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, or the project skills directory) with `git -C <skill-folder> status --short --branch` or `python scripts/check_skill_update.py`. Pull pending updates before running release audits.

0a. **token-optimizer**: Disable thinking and reasoning in the active agent, then plan and track every step in `.progress.md` instead of reasoning. Always on.

1. **agent-self-awareness**: Detect the active harness and model, classify its capability tier, and switch to a research-first protocol when it is not a frontier coding model. Unknown models are treated as non-frontier. The tier raises the evidence bar; it never lowers the requested outcome.
2. **context-search**: On a new session in an existing codebase, discover installed agents, find project-matched session transcripts or databases, extract a bounded brief, and verify it against git and the live worktree. Prior transcripts are clues, never authority.
2b. **parallel-agent-orchestration**: When two or more work streams are independent, delegate bounded tasks to available subagents and run safe long commands in the background. Track process handles and worker results, avoid shared-file write conflicts, and verify the integrated result.
3. **persistent-goal-execution**: Keep the complete release objective, acceptance criteria, current plan, authoritative evidence, and completion state active across context compaction, retries, waits, and failures. Do not declare the release complete until every requirement is verified.
4. **credential-safety**: Check worktree files, staged changes, pushed commit ranges, ignore rules, and available secret-scanner results before committing or pushing. Stop, rotate, and remediate any exposed credential without printing its value.
5. **deep-research and third-party attribution**: When a release includes a feature copied, ported, or adapted from another repository, inspect the source and target context, verify licensing, trace behavior, and document intentional differences before implementation. Audit third-party packages, bundled code, fonts, and assets to provide licensing attribution in `CREDITS.md` or `NOTICE`.
6. **debug-and-fix**: Run the project build, tests, and linters. Fix any failures at their root cause. A release with a red build is not production ready.
7. **systematic-issue-sweep**: Whenever an issue, bug, typo, anti-pattern, or user-pointed inconvenience is identified during testing, audit, or review, sweep the entire codespace to locate and resolve all related occurrences. Abstract the underlying mistake pattern and eradicate it across code, tests, docs, and configs so the defect is never repeated elsewhere in the project.
8. **error-docs-lookup**: When encountering library deprecations, build tool warnings, or version migrations, search and read current official documentation before applying fixes.
9. **google-seo-skill**:
   - **Pull updates first**: If any update to `google-seo-skill` is available in git (upstream `https://github.com/mikezupper/google-seo-skill`), pull it first using `python scripts/update_seo_skill.py`. Verify clean frontmatter and human writing, then push updates to the skills repo.
   - **Use when**: Working on a public web project where search ranking and public search engine visibility are needed. Use it to audit crawlability, metadata, structured data, canonical URLs, and Core Web Vitals.
   - **Avoid when**: Working on a personal project, private repository, internal dashboard, staging site, or any project where search indexing is not desired. In those cases, skip SEO ranking checks entirely and verify that `noindex` meta tags, `X-Robots-Tag: noindex` headers, or robots disallow rules are present to prevent indexing.
10. **human-writing**: Mandatory on every task, including tasks that do not modify project files. Load the complete skill before responding or writing. Apply it to all assistant communication and every project artifact. Scan every changed text file with `human-writing/scripts/scan.py`. Enforce zero hard hits: no emoji or emoji-like symbols, no em dashes, no en dashes used as punctuation, and no horizontal bars. Rewrite stock AI phrasing into specific, natural language.
11. **context-rich-commits**: Record the release work using structured git commits (separating doc updates from legal text and code changes), followed by a project checkpoint commit. Push committed releases to the repo when instructed.
12. **Domain-specific skills**:
   - `android-app-dev`: Use for Android apps to verify the CI workflow, Gradle version catalog, and Compose configuration.
   - `minecraft-fabric-mod`: Use for Minecraft Fabric mods to verify Loom, Fabric API, and CI build workflows.
   - `iris-shaderpack-dev`: Use for shaderpacks to verify program names and shaders.properties.
   - `threejs-awwwards-site`: Use for WebGL and 3D websites to verify performance budgets and mobile fallbacks.
   - Google Cloud skills (such as `gcloud`, `google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`): Use when configuring or deploying services to Google Cloud Platform.

## Workflow

### Step 0. Skill relevance check (mandatory, always first)
Before the audit, run the check from "Mandatory skill relevance check" above: inventory the available skills, mark each USE or SKIP with a reason, and read the full `SKILL.md` of every USE skill. This step never gets skipped, including for small tasks and for sessions that resume earlier work. Repeat it when the task shifts.

### Step 0b. Token optimizer mode (mandatory, always)
Right after the relevance check, apply "Mandatory token-optimizer mode" above: turn thinking off, read the setting back, create or open the todo list in `.progress.md`, and load every later step as an item. From here on, work the list: re-read it before each item and update it after each one.

### 0. Recover context and set the execution mode
Run self-awareness and context recovery before the audit. They are independent and can run in parallel:

```bash
python agent-self-awareness/scripts/detect_model.py
python context-search/scripts/find_agent_sessions.py --project <project-root> --brief
```

`agent-self-awareness` decides whether a research-first protocol is mandatory. If the model is capable, efficient, or unknown, read current official documentation and inspect the code before implementing. `context-search` recovers prior agent decisions and open work. Read `context-search/references/agent-stores.md` for session locations and `references/extraction.md` for the brief format.

Check git status, git log, and the named files before trusting any transcript. Record the execution mode, recovered brief, and what you verified in the final report.

### 0c. Parallelize independent work

Apply `parallel-agent-orchestration` after context recovery and before the audit when the task has two or more independent work streams. Build a dependency graph, delegate bounded research or implementation tasks with exclusive file ownership, and start safe long-running checks in the background. Continue coordinator work while those tasks run. Track every worker and process to completion, integrate changes under coordinator control, then run the required checks against the integrated repository. Keep dependent work sequential and do not create extra workers when coordination costs more than it saves. Read the full skill and its `references/parallel-workflows.md` before delegating or backgrounding work.

### 1. Audit
Run the audit script from the project root. It inspects the codebase, checks for missing, stale, or excluded files, verifies skill folder git status, and lists which skills to USE and which to SKIP:

```bash
python scripts/audit.py <project-root>
```

For personal, internal, or private repositories where consumer legal documents and public search indexing should be avoided:

```bash
python scripts/audit.py <project-root> --personal
```

When an explicit user override requests full corporate release documentation for an internal or private project:

```bash
python scripts/audit.py <project-root> --force-release
```

When the user explicitly opts out of legal documents:

```bash
python scripts/audit.py <project-root> --skip-legal
```

The script reports items organized into clear categories:
- **REQUIRED**: Essential documents and configurations missing for release.
- **RECOMMENDED**: Advisory best-practice files missing for release.
- **OPTIONAL**: Documents omitted because they do not apply to this project type or mode.
- **USER-EXCLUDED**: Documents omitted by explicit user decision.
- **STALE**: Existing files that are outdated or contain broken references.
- **OK**: Verified files that are present and up to date.
- **INFO**: Project scope, branch tracking, and git metadata.

### 2. Changelog
Create or update `CHANGELOG.md` following `references/changelog.md`. Source entries from `git log` since the last release tag and from the git diff, not from memory. Write for users: what they can now do or what behaves differently, not an internal list of moved files. Group under Added, Changed, Fixed, Removed, Security. Keep an `Unreleased` section at the top until a version release is cut.

### 3. Docs and README
Create or update the README and anything under `docs/`. Follow the checklist in `references/docs.md`. The standard: a newcomer can go from cloning to running in a few minutes using only the README. Always write as the project owner, never as an external assistant. Never leave assistant coaching, multiple-choice options, or reminders in README or docs (such as "The license is not selected yet. Choose one before publishing: ...").

Run every install and execution command you document. A command you did not run is an unverified guess, so either run it or mark it unverified. Update docs for every behavior mentioned in the changelog, and remove docs for removed features.

### 4. Terms, privacy, and community rules
Review `references/legal-and-rules.md` for complete outlines, codebase audit checklists, and decision trees covering the full corporate release suite:

1. **Terms of Service (`TERMS.md` or `TERMS_OF_SERVICE.md`)**: Covers eligibility, user accounts, acceptable use, user-generated content, intellectual property, third-party integrations, disclaimer of warranties, liability limits, termination, governing law, and dispute resolution.
2. **Privacy Policy (`PRIVACY.md`)**: Audits the real codebase for data collection (cookies, localStorage, session tokens, analytics, crash reporters, third-party APIs, authentication providers). Details data retention, user rights (GDPR/CCPA access and deletion), international transfers, and privacy contact information.
3. **License (`LICENSE`)**: Verifies an explicit license exists (MIT, Apache-2.0, GPL-3.0, BSD, or proprietary Commercial All Rights Reserved). Never guesses or changes an existing license without explicit authorization. If no license exists, ask the user in chat or write clean owner terms (`Copyright (c) [YEAR] [OWNER]. All rights reserved.`). Never commit assistant options lists or coaching instructions into the repository.
4. **Third-Party Credits and Attribution (`CREDITS.md` or `NOTICE`)**: Details third-party dependencies, open-source packages, fonts, media assets, and external APIs used by the project, including required copyright and license notices.
5. **Security Policy (`SECURITY.md`)**: Defines supported versions, private vulnerability reporting process, response timelines (SLA), security contact address, and safe harbor / responsible disclosure expectations.
6. **Contributing Guidelines (`CONTRIBUTING.md`)**: Explains local setup, branching rules, testing expectations, pull request workflows, and code review standards.
7. **Code of Conduct (`CODE_OF_CONDUCT.md`)**: Community and contributor standards based on established industry templates (such as Contributor Covenant 2.1).
8. **Changelog (`CHANGELOG.md`)**: Chronological release notes adhering strictly to Keep a Changelog and Semantic Versioning.
9. **Environment Template (`.env.example`)**: Documents all required environment variables without committing actual secrets.

Smart conditional rules for private projects and user preferences:
- **Private and internal projects**: The audit script automatically detects private projects from `package.json` (`"private": true`), `pyproject.toml`, or internal markers. By default, skip public-facing consumer terms, public privacy policies, and public community files. Focus on code quality, build verification, tests, credential safety, changelog, `.env.example`, internal README, and proprietary license notices.
- **Explicit user override (`--force-release`)**: If the user explicitly asks to make a private project production-ready, or requests release documents, generate the full corporate suite tailored for commercial/internal software (commercial terms, internal security policy, third-party attribution notices, proprietary license).
- **User opt-out / denial**: If the user denies or opts out of any legal file (such as "skip terms", "no license needed", "don't add privacy policy", or passes `--skip-legal`), immediately honor the decision, skip generation, and document the omission in the audit report as user-excluded rather than missing.

State plainly in the report that generated terms and privacy text are starting drafts that need legal review before launch. Do not claim legal compliance.

### 5. Skill selection and routing
Read `references/skill-selection.md` and confirm the project type from the audit output:
- **Web project needing search ranking**: USE `google-seo-skill` (or `references/seo.md`).
- **Personal web project, internal tool, staging site, or no indexing desired**: SKIP `google-seo-skill`. Verify that `noindex` tags or robots disallow rules protect the site from search crawlers.
- **Native mobile, desktop, mod, shaderpack, bot, or library**: SKIP SEO skills. Prepare store listing copy, mod registry text, or package metadata instead.
- **Domain skills**: If `android-app-dev`, `minecraft-fabric-mod`, `iris-shaderpack-dev`, or `threejs-awwwards-site` apply and are installed, invoke them for domain-specific checks and verification.
- **Ponytail skills**: Follow `references/skill-selection.md`. Use `ponytail` to keep implementation to the smallest complete change, `ponytail-review` to review the resulting diff, and `ponytail-audit` for a whole-repository code audit. Use `ponytail-debt` when the repository contains `shortcut:` or legacy `ponytail:` comments. Use `ponytail-gain` only when upstream benchmark results are relevant, and `ponytail-help` only when Ponytail commands or levels need explanation.

### 6. Multi-skill refresh pass
Run the applicable skills in this sequence:

0. **Skill folder update check**: Inspect git status in the skills folder (`python scripts/check_skill_update.py` or `git -C <skill-folder> status --short --branch`) to verify installed skills are up to date before running the refresh pass.
0b. **token-optimizer**: Confirm thinking is still off and `.progress.md` matches the real state before each stage. Update it after each stage.
1. **agent-self-awareness**: Detect the active model and tier. If it is not frontier class, enforce research-first mode for the refresh pass: official docs, code inspection, tests, and diff review before any fix. Report the execution mode.
2. **context-search**: Recover prior agent context on a new session in an existing codebase. Run `context-search/scripts/find_agent_sessions.py --brief`, build the short brief, and verify it against the current worktree, git history, and tests before relying on it.
3. **persistent-goal-execution**: Preserve the full production objective through the refresh pass and verify every requirement before reporting completion.
4. **credential-safety**: Check for credentials before committing or pushing. Stop and remediate findings, rotate exposed values, and do not expose secret contents in reports.
5. **deep-research and attribution**: If the release includes copied or ported functionality, verify source behavior, licensing, target integration, and intentional differences before accepting the implementation. Verify that `CREDITS.md` or `NOTICE` documents all third-party dependencies and asset licenses.
6. **debug-and-fix and systematic-issue-sweep**: Run the project's build, test, and lint commands. Fix any failures at their root cause. When fixing any error, bug, typo, or user-pointed issue, invoke `systematic-issue-sweep` to abstract the pattern and eradicate all identical or related occurrences across the entire workspace.
7. **error-docs-lookup**: For any warning, deprecation, or error involving a library or toolchain, look up official documentation for the installed version.
8. **Domain skill checks**: Run specific checks (for example, verifying CI workflows in `android-app-dev` or `minecraft-fabric-mod`).
8a. **Ponytail implementation and review**: Apply `ponytail` when making code changes, then run `ponytail-review` against the completed diff. Use `ponytail-audit` when the release task includes a repository-wide code-quality audit. Run `ponytail-debt` only when shortcut markers exist or the user requests the debt ledger. These reports complement the production documentation audit; they do not replace builds, tests, security checks, or `scripts/audit.py`.
9. **Search indexing and SEO check**:
   - If using `google-seo-skill`, first check if any update is available in git (`python scripts/update_seo_skill.py`) and pull it.
   - For public websites where ranking is needed: run `google-seo-skill` (or `references/seo.md`).
   - For personal or internal projects: verify that `noindex` headers or meta tags and robots rules are correctly in place.
10. **human-writing**: Run `human-writing/scripts/scan.py` on every touched file (README, changelog, docs, terms, comments). Eliminate all hard hits (no em dashes, no emoji).
11. **Audit rerun**: Rerun `scripts/audit.py`. Confirm zero remaining MISSING or STALE items.
12. **context-rich-commits and push**: Commit the changes using structured commit messages:
   - One commit for docs and changelog.
   - One commit for legal and community files.
   - A final checkpoint commit capturing the current state of the repository.
   - Always create or use a `dev` branch and push the current work there
     without waiting for user confirmation, whether the implementation is
     incomplete or complete. Verify the remote state and report what remains
     unfinished when applicable.
   - After the `dev` push succeeds, wait for the CI/CD workflow for that exact
     commit. If the workflow passes, push that same verified commit to the
     production branch without asking for confirmation. If CI/CD fails, is
     unavailable, or does not cover the full change, do not push to production.
     Report the failure or missing evidence and continue remediation.
   - If no `dev` branch exists, create it before waiting for CI/CD. A
     production push is never allowed without a successful `dev` check for
     the exact commit.
   - A final checkpoint commit capturing the current state of the repository.

### 7. Report
Provide a concise, factual summary:
- Files created or updated.
- User-excluded documents if legal files were omitted by user decision.
- Placeholders the user must fill in ([COMPANY NAME], [CONTACT EMAIL], [JURISDICTION], [SECURITY EMAIL], [EFFECTIVE DATE]).
- Skill relevance check: the inventory source, each skill marked USE or SKIP with a reason, and confirmation that every USE skill's `SKILL.md` was read.
- Token optimizer: agents and config files changed, thinking state read back after the change, backups made, any agent where thinking could not be turned off, and the final state of `.progress.md`.
- Skills used and skills skipped, each with a brief reason.
- Execution mode: model tier and evidence source, plus the research protocol applied when the model was not frontier class.
- Recovered prior context: agents and stores checked, sessions found, and what was verified against git and tests.
- Search indexing status: confirmed public indexing checklist or verified personal/internal `noindex` protections.
- Commands run and verification results (mark anything unverified as "not verified").
- Open observations (such as missing test suites or upstream dependencies).
- Legal review reminder if terms or privacy policies were drafted.

## Rules that keep this honest

- Check which skills are relevant every time, the same way `agent-self-awareness` runs every time. Do not rely on memory of the skill list, and do not stop at the skills named in this file. Read the full `SKILL.md` of each relevant skill before using it, and report the USE and SKIP decisions.
- Run `token-optimizer` every time, the same way `agent-self-awareness` runs every time. Thinking stays off, no extended deliberation, and every step comes from the todo list in `.progress.md`, which is re-read before each item and updated after it. Verification and research still happen as tool calls and list items.
- The current worktree, git history, and test output outrank every recovered transcript. Use `context-search` to find prior work, then verify each claim against the repository before acting on it.
- When the model is capable, efficient, or unknown, research comes before implementation. Use `agent-self-awareness` to set the mode, then read official docs and inspect the code instead of guessing. A lower tier raises the evidence bar; it never lowers the deliverable.
- Eradicate issues workspace-wide: When any bug, typo, anti-pattern, or inconvenience is pointed out by the user or identified during tests, sweep the entire codespace using `systematic-issue-sweep` to ensure the issue pattern is not repeated anywhere else.
- Write as the project owner: All documentation, README entries, comments, and licenses must speak with the direct voice and authority of the repository creator or maintainer. Never include assistant meta-instructions, advice to the developer, or multiple-choice checklists in committed deliverables.
- Version numbers and dates come from the manifest, tags, and git, never from guesses. Use today's system date for release headings.
- Do not bump the version or tag a release unless the user asked. Put changes under `Unreleased` otherwise.
- Do not delete existing legal text. Extend or flag it.
- Never put secrets, tokens, or personal emails found in the repository into public docs.
- Match existing project voice, formatting, and file layout before applying templates.

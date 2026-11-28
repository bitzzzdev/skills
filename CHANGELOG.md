# Changelog

All notable changes to this project are listed here.
The format follows Keep a Changelog and the project uses Semantic Versioning.

## [Unreleased]

### Added

- Added `bento-terminal-orchestration` with tmux bento layouts, per-worker TTY panes, Bash and Fish background job tracking, VPS resource guidance, and plain-TTY fallback rules.

- Added `parallel-agent-orchestration` with delegation contracts, task dependency planning, isolated concurrent writes, and tracked background command workflows.

- Added root `install.sh` to symlink every top-level skill into the shared `~/.agents/skills` directory for OpenCode, Codex, Cursor, Gemini CLI, and GitHub Copilot CLI, plus the Claude Code and Kiro skill directories. Added isolated installer tests and CI coverage.

- Added the six MIT-licensed Ponytail skills: `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, and `ponytail-help`. Recorded the upstream revision and retained its license in `ponytail/`.
- Added `agent-self-awareness` skill with guide (`SKILL.md`), model tier
  reference (`references/model-tiers.md`), quality gate reference
  (`references/quality-gates.md`), and a detection script
  (`scripts/detect_model.py`) that identifies the harness and model from live
  session data, environment, and config, then sets a research-first protocol
  when the model is not frontier class or cannot be identified.
- Added `context-search` skill with guide (`SKILL.md`), agent store reference
  (`references/agent-stores.md`), extraction guide
  (`references/extraction.md`), and a read-only discovery script
  (`scripts/find_agent_sessions.py`) that finds prior sessions from OpenCode,
  Codex, Claude Code, Antigravity, Gemini CLI, Muse, Aider, editor agents, and
  generic JSONL stores, then extracts a redacted brief.
- Added `systematic-issue-sweep` skill with guide (`SKILL.md`), reference
  (`references/sweep-patterns.md`), and CLI scanner (`scripts/sweep.py`) to
  sweep the entire workspace and eradicate defect classes across code, tests,
  docs, and configuration.
- Added project owner authority rules and assistant meta-instruction bans
  across `human-writing` and `production-ready`, eliminating assistant coaching
  leaks, placeholder advice, and unselected license prompts.
- Added assistant coaching and meta-instruction detection patterns to
  `human-writing/scripts/scan.py` and `scripts/audit.py`.
- Added technical social media post writing reference
  (`human-writing/references/social-posts.md`) covering post themes, archetypes,
  platform rules for X and Reddit, hook engineering, and editing checklists.
- Added soft pattern detection in `human-writing/scripts/scan.py` for social media
  engagement bait and thread cliches.
- Added corporate release documentation suite and audit checks to
  `production-ready`, covering terms of service, privacy policy, third-party
  credits, security policy, contributing guidelines, and code of conduct.
- Added support for `--force-release`, `--personal`, `--skip-legal`, and
  `--skip-files` flags in `audit.py`.
- Added skill folder update checks to every skill so agents inspect git status in
  the skill directory before running.
- Added `scripts/check_skill_update.py` to inspect git status and branch tracking
  across known skill locations.
- Added `persistent-goal-execution` for preserving complete objectives,
  acceptance criteria, plans, authoritative evidence, and completion state
  across long coding tasks.
- Added `credential-safety` for checking credentials before commits, pushes,
  and production releases.
- Added `deep-research` for understanding source and target repositories before
  copying or porting a feature.
- Added `scripts/sync_skills.py`, a smart sync engine that fetches GitHub and
  GitLab, checks CI evidence for the `dev` branch, and updates each skills clone
  from the newest verified source. When GitHub Actions is unavailable and the
  GitLab `dev` pipeline passed, it switches a clean `main` clone to the tested
  `dev` branch.
- Added fish functions (`skill`, `pull_agent_skills`, `clone_agent_skills`,
  `update_agent_skill_repo`) plus bash and zsh functions and aliases in `shell/`,
  so the sync helpers can be installed from this repository.
- Added `shell/install.sh` to install the sync script and shell helpers into
  `${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/`, copy fish functions to
  `~/.config/fish/functions/`, and update `~/.bashrc` and `~/.zshrc`.
- Added `.gitlab-ci.yml` so GitLab validates the skills, scripts, and shell
  helpers on `dev` and `main`.

### Changed

- Added a mandatory post-push CI/CD watch loop to `context-rich-commits` and `production-ready`. Agents must monitor required checks for the exact pushed SHA, diagnose failures, push root-cause fixes, and rewatch each new commit until checks pass or an external blocker is documented.


- Integrated the six Ponytail skills into `production-ready` skill routing, with explicit triggers and boundaries for implementation, diff review, repository audits, shortcut debt, benchmark data, and help.

- Integrated `agent-self-awareness` into `production-ready` orchestration, the
  pre-audit workflow, the refresh pass, the skill selection matrix, and the
  audit recommendations. Non-frontier and unknown models must research before
  implementing, and the report records the execution mode.
- Integrated `context-search` into `production-ready` orchestration, the
  workflow as a pre-audit recovery step, the refresh pass, and the skill
  selection matrix. Prior transcripts are treated as leads that must be
  verified against git and the live worktree.
- Updated `audit.py` to recommend `context-search` when the skill is installed.
- Integrated `systematic-issue-sweep` into `production-ready` multi-skill
  orchestration and refresh pass, requiring workspace sweeps for any reported
  bug, typo, or user inconvenience before release.
- Integrated `systematic-issue-sweep` into `debug-and-fix` workflow to search
  and fix recurrences across all files after root cause resolution.
- Updated `audit.py` to recommend `systematic-issue-sweep` in production audits.
- Updated `human-writing` `SKILL.md` and `references/ai-tells.md` to require
  writing from the owner's perspective, ban assistant-to-developer coaching,
  and provide before/after examples for license sections and code comments.
- Updated `production-ready` `SKILL.md`, `references/docs.md`, and
  `references/legal-and-rules.md` to mandate owner perspective for license
  notices and READMEs, forbidding unselected option prompts.
- Updated `audit.py` to flag assistant meta-instructions in README and candidate
  release documents as stale.
- Updated `human-writing` `SKILL.md` with guidelines for technical social posts
  on X, Reddit, and developer forums, including the inverted rule of excitement,
  zero throat-clearing, platform rules, and before/after comparisons.
- Updated `production-ready` `SKILL.md` and `references/legal-and-rules.md` with
  enterprise document outlines, codebase audit steps, and architecture decision
  trees.
- Enhanced `audit.py` with clear output categorization across REQUIRED,
  RECOMMENDED, OPTIONAL, and USER-EXCLUDED document tiers.
- Added automatic private project detection and explicit user override handling
  in production readiness checks.
- Updated `validate_skills.py` to verify skill folder update checks in all skills.
- Updated `audit.py` and `production-ready` flow to inspect skill folder status
  and include `~/.copilot/skills`.
- Documented GitHub Copilot skill installation and update checks in README.
- Updated `production-ready` and the skills catalog to include the new goal
  execution skill.
- Added branch-aware push guidance: use `dev` first when available and require
  explicit confirmation before pushing to production.
- Clarified that all production work must be pushed to `dev` without
  confirmation first, while production pushes still require human approval.
- Added credential checks to the `production-ready` orchestration flow.
- Added deep research checks to the `production-ready` orchestration flow for
  copied or ported functionality.
- Updated release promotion to require a passing CI/CD check on the exact
  `dev` commit before automatically pushing it to production.


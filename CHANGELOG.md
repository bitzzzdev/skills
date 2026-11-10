# Changelog

All notable changes to this project are listed here.
The format follows Keep a Changelog and the project uses Semantic Versioning.

## [Unreleased]

### Added

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

### Changed

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


# Changelog

All notable changes to this project are listed here.
The format follows Keep a Changelog and the project uses Semantic Versioning.

## [Unreleased]

### Added

- Added `persistent-goal-execution` for preserving complete objectives,
  acceptance criteria, plans, authoritative evidence, and completion state
  across long coding tasks.
- Added `credential-safety` for checking credentials before commits, pushes,
  and production releases.
- Added `deep-research` for understanding source and target repositories before
  copying or porting a feature.

### Changed

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


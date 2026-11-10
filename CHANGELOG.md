# Changelog

All notable changes to this project are listed here.
The format follows Keep a Changelog and the project uses Semantic Versioning.

## [Unreleased]

### Added

- Added `persistent-goal-execution` for preserving complete objectives,
  acceptance criteria, plans, authoritative evidence, and completion state
  across long coding tasks.

### Changed

- Updated `production-ready` and the skills catalog to include the new goal
  execution skill.
- Added branch-aware push guidance: use `dev` first when available and require
  explicit confirmation before pushing to production.
- Clarified that incomplete production work must be pushed to `dev` without
  confirmation, while production pushes still require human approval.


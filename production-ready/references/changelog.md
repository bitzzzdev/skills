# Changelog guide

Use the Keep a Changelog layout with Semantic Versioning unless the project already uses another format. If it does, follow that format.

```markdown
# Changelog

All notable changes to this project are listed here.
The format follows Keep a Changelog and the project uses Semantic Versioning.

## [Unreleased]

### Added
- Export to CSV from the reports page.

## [1.4.0] - 2026-10-02

### Added
- Dark mode, saved per user.

### Changed
- Login now locks the account for 15 minutes after 5 failed attempts.

### Fixed
- Uploads over 10 MB no longer time out on slow connections.

[Unreleased]: https://github.com/owner/repo/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/owner/repo/compare/v1.3.0...v1.4.0
```

## Building entries from git

```bash
git describe --tags --abbrev=0            # last release tag
git log <tag>..HEAD --pretty='%h %s'      # what changed since
git diff <tag>..HEAD --stat               # where it changed
```

Read the diffs for anything vague. Merge related commits into one entry. Skip commits users never see (formatting, CI tweaks, refactors) unless they change behavior.

## Writing entries

- One line, starts with what changed for the user. "Fixed crash when the cart is empty", not "Fix null check in cart.js".
- Name breaking changes under Changed or Removed and start the line with "Breaking:". Say what to do instead.
- Security fixes go under Security. Don't publish exploit details before a fix is available.
- Link issues or PRs when they exist, not otherwise.

## Choosing the next version

- Breaking change to public behavior: major.
- New feature, backward compatible: minor.
- Bug fix only: patch.
- Before 1.0.0, minor bumps may carry breaking changes. Say so in the entry.

Only cut a version when the user asks. Otherwise leave entries under Unreleased.

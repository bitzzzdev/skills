# Base Package Tracker - Usage Guide

This guide explains how to use the base-package-tracker skill effectively for tracking upstream base changes and UI impact.

## Quick Start

### 1. Configuration

Before first use, configure the paths:

```bash
# Simple configuration via prompt (the skill will ask you)
base-package-tracker config

# Or set manually in base-progress.md
BASE_DIR=/path/to/base/package
UI_DIR=/path/to/ui/presentation
```

### 2. First Detection

Run discovery of base changes (determines current state):

```bash
base-package-tracker detect \
  --base-dir ./vendor/chromium \
  --ui-dir ./browser-overlay \
  --label "Initial discovery"
```

This creates `base-progress.md` with:
- Current base version
- A list of upstream changes since last detection
- Initial UI guidance

### 3. Ongoing Monitoring

After initial setup, use this pattern for each base update:

```bash
# After getting an upstream update notification
base-package-tracker detect --base-dir ./vendor/chromium --ui-dir ./browser-overlay

# If CI already detected the update
base-package-tracker detect --label "Auto-detected Chromium update"
```

## Basic Patterns

### Pattern 1: Chromium Browser Layer

Project: Custom browser on top of upstream Chromium (similar to Boyutar/Brave/etc.)

```markdown
# Base: Chromium
# Plan: CSS Overlay + JS Bridge for features
```

**Detection output:**
```markdown
### Base Update - 2026-11-11
- **Merged:** Minor CSS changes to user profile icons
- **URL Changes:** New user profile page structure
- **Breaking:** Session endpoint moved

**UI Impact:**
- [x] User profile page styling integrated
- [ ] Session bridge endpoints documented in repo
- [ ] Test all custom Popup menus
```

**Fix guidance shows:**
```markdown
### Session Bridge Update

**Component:** `/src/bridge/session.js`

**Issue:** Base moved `chromium.session.login()` to new async patterns

**Fix:**
```javascript
// Old
chromium.session.login(username, password);

// New
const session = await chromium.session.login({ username, password });
```

**Test command:**
```bash
npm run test:bridge-session
```
```

### Pattern 2: Dependency Upgrade

Project: React app with multiple dependencies upgraded

```bash
base-package-tracker detect \
  --base-dir ./node_modules/react \
  --ui-dir ./src/components \
  --label "React 19 upgrade"
```

**Detection output:**
```markdown
### React 19 Upgrade - 2026-11-10
- **Files Changed:** 45 files (mostly in react-dom)
- **Breaking:** ref forwarding in useEffect

**UI Impact:**
- [ ] Update all ref usage in HomeLayout
- [ ] Ref test suite needs parameter changes
- [ ] New Suspense loader for loading screens
```

### Pattern 3: Framework Release

Project: Flutter mobile app with framework updates

```bash
base-package-tracker detect \
  --base-dir ./vendor/flutter \
  --ui-dir ./lib/app \
  --label "Flutter 3.24 Beta"
```

## Advanced Usage

### Auto-Updates with CI

Integrate with CI/CD pipeline:

```yaml
# .github/workflows/check-base-updates.yml
name: Base Package Updates

on:
  schedule:
    - cron: '0 2 * * 0' # Weekly at 2 AM
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for Chromium updates
        run: |
          npm run check-chromium-updates
          if [ $? -ne 0 ]; then
            base-package-tracker detect --label "CI-detected Chromium update"
            base-package-tracker commit
          fi
```

### Multi-Repo Sync

Keep base tracking synced across GitHub and GitLab:

```bash
# After commit, push to both
git push origin main
git push git@gitlab.com:your-org/browser.git main

# Sync progress file
base-package-tracker push --repo github --branch main
base-package-tracker push --repo gitlab --branch main
```

### Prioritization System

The skill provides three priorities for UI impact items:

**🔴 Blocking (Priority 1):**
- UI doesn't work at all
- Data pipelines break
- Authentication fails

These items should be addressed immediately and have test commands ready.

**🟡 Warning (Priority 2):**
- UI looks off but works
- Minor UX regressions
- Deprecated warnings

Add to your backlog to be fixed in the next sprint.

**🟢 Info (Priority 3):**
- Documentation changes needed
- Cosmetic layout changes
- Optional enhancements

Can be addressed at team's discretion.

## Progress File Best Practices

### Naming Conventions

Use consistent labels for base changes:
- `v133_release` for stable releases (e.g., Chrome 133)
- `v133_dev_20261111` for development builds
- `CVE-2026-XXXX` for security fixes
- `api-update_session` for API changes

### Truncation Policy

For large projects with many updates month-over-month, the skill creates a `CHANGELOG` subfile to keep `base-progress.md` readable:

```
base-progress.md
├── base-progress.md          # Summary (1-2KB)
└── changes/
    ├── 2026-11-11_v133.md   # Full change details
    ├── 2026-10-28_v132.md
    └── CHANGES_LOG.md       # Historical archive
```

### Cleanest Writing

Follow this minimal format for updates:

```markdown
### v133 - 2026-11-11
- **Merged:** Styling change for dashboard
- **Breaking:** Widget API removed

**UI Impact:**
- [ ] Dashboard widgets migrated (Priority 2)
- [ ] Test migration with heatmaps (test:widgets)

**Pending Manual Review:**
- [ ] Review API docs for widget replacement
```

Complete details are in `changes/2026-11-11_v133.md`.

## Command Reference

### `base-package-tracker`

**Check current status:**
```bash
base-package-tracker status
# Outputs:
# Base: Chromium v132.0.6758.0
# Last Updated: 2 days ago
# Pending Blockers: 1 (session API change)
```

**Generate a change log entry manually:**
```bash
base-package-tracker --change=brave_v132 --label="Brave v132 migration"
```

**Configure paths:**
```bash
base-package-tracker config
# Interactive CLI to set BASE_DIR and UI_DIR
```

**Commit current changes:**
```bash
base-package-tracker commit
# Commits base-progress.md + any pending patches
```

**Push to repository:**
```bash
base-package-tracker push --repo github
# Pushes commits to configured remote
```

**Skip Git operations (for CI):**
```bash
base-package-tracker push --no-commit --no-push
```

## Common Workflows

### Workflow 1: Market Updates

You release a new feature every week and the base has updates:

```bash
# Friday release process
base-package-tracker detect --label "Weekly Release"
base-package-tracker commit

# If blockers are present
base-package-tracker open --issue=1 --title="Fix session API after Chrome update"
base-package-tracker push --repo github
```

### Workflow 2: Security Patches

Security issues require fast triage:

```bash
base-package-tracker detect --label="Security Update: CVE-2026-4721"
# Output shows the vulnerability and UI impact

if [[ "$(cat ./base-progress.md | grep -c '🔴 Blocking')" -gt 0 ]]; then
  base-package-tracker open --issue=Bad --title="Critical: Disable insecure polyfill"
  base-package-tracker push --repo github
fi
```

### Workflow 3: Major Version Upgrade

Upgrading from React 18 to 19:

```bash
# Step 1: Document expectations
base-package-tracker detect --label "React 19 major upgrade plan"

# Step 2: Work through blockers with your team
base-package-tracker open --list 12 --title="React 19 refactoring"
base-package-tracker

# Step 3: Commit as you make progress
base-package-tracker --change=react19_dc --label="React 19 coding"

# Step 4: Merge into main
base-package-tracker push --repo github --branch main
```

## Integration with Other Skills

### With Token Optimizer

For token efficiency, run both in sequence:

```bash
token-optimizer                           # Disable thinking globally
base-package-tracker detect --label="Base update"  # Track base changes
debug-and-fix                             # Fix any UI issues discovered
```

### With Production-Ready

For project releases:

```bash
base-package-tracker detect --label="Release 1.2.0"
context-rich-commits                       # Commit base changes with message
production-ready                           # Full release checklist
```

## Troubleshooting

### Issue: Baseline Comparison Fails

If detection can't find previous baseline state:

**Fix:** Manually set a baseline by specifying a previous hash:

```bash
base-package-tracker detect --last-checkout=abc123def --label="Manual baseline"
```

### Issue: Progress File Too Large

If `base-progress.md` grows beyond 1MB:

**Action:** The skill automatically relocates old updates to `changes/CHANGES_LOG.md`.

To manually control this:
```bash
base-package-tracker --max-keeps=12   # Keep only last 12 major updates
```

### Issue: UI Impact Flood

If too many items are marked "Blocking":

**Analysis:** Look at base changes that are overly sensitive to UI (rarely base changes alone cause 50+ blockers).

**Fix:** Mark realistically:
```python
# Don't write 50 individual line checks—group them
- [ ] All app navigation icons migrated (8 items)
- [ ] All state management hooks updated (12 items)
```

### Issue: Git Push Fails

If committing pushes fails:

**Debug:**
```bash
base-package-tracker status
git remote -v  # Verify remote isn't missing
```

**Fix:** Add missing remote:
```bash
git remote add gitlab git@gitlab.com:your-org/browser.git
base-package-tracker push --repo gitlab
```

## Language Support

The tool uses English for all system outputs, but supports localized labels in `base-progress.md`:

```markdown
# Base: Chromium (中文追踪)
# Plan: CSS Overlay + JS Bridge for features (计划: CSS 覆盖 + JS 桥接)
```

This helps international teams while keeping the internal tracking tool in English.

## Getting Help

If you encounter issues:

1. Check skill logs: `.base-package-tracker.log`
2. Verify paths exist and are readable
3. Confirm git repository is initialized
4. See agent instructions here if the skill fails to run

## Demo

A complete minimal project example:

```bash
mkdir demo-chromium-browser
cd demo-chromium-browser
git init

# Create base and UI directory structure
mkdir vendor/base browser-ui

# Run initial configuration (assuming skill files are in your path)
base-package-tracker config
# Answer prompts to set BASE_DIR and UI_DIR

# Detect initial state
base-package-tracker detect --label "Initial setup"

# The skill creates base-progress.md
cat base-progress.md  # Shows you the summary

# On a real browser, Chrome updates:
base-package-tracker detect --label="Chrome 133 update"
# Shows new files, broken links, etc.

# When you fix issues:
base-package-tracker --fix-ui HomeLayout --issue session-api-broke
# Creates a pending patch

# Finalizing:
base-package-tracker commit
base-package-tracker push --repo github
```

The entire process takes seconds and saves you from manually reconciling upstream changes with your UI layer.
# AI Coding Agent Skills

This repository contains reusable skills for AI coding agents (OpenCode, Claude Code, Copilot CLI, and other agents). Skills are standalone, modular instructions that can be loaded by an agent to handle specific coding workflows.

## Available Skills

### 1. Production-Ready
**ID:** `production-ready`
**Level:** Orchestrator for releases and code audits

Manages complete production-level workflows including audits, documentation, changelogs, legal text, CI testing, and git commits. Ideal for finalizing projects and preparing for public releases.

### 2. Token Optimizer
**ID:** `token-optimizer`
**Level:** Configuration & Optimization

Minimizes AI agent token usage by:
- Detecting and disabling thinking/reasoning features across agents (OpenCode, Claude Code, Copilot CLI, Muse, Antigravity, Aider, etc.)
- Creating automatic progress tracking files (.progress.md) instead of using reasoning tokens
- Adding new todos dynamically for bugs, syntax issues, or blocking problems
- Preserving code quality while maximizing throughput

**Best for:** Long coding sessions, frequent project restarts, and projects where thinking overhead adds up significantly.

### 3. Base Package Tracker
**ID:** `base-package-tracker`
**Level:** Quality Assurance & Maintenance

Tracks updates to base packages (Chromium, frameworks, libraries) and guides UI adaptation:
- Automatically detects base package version changes
- Records UI impact and migration needs
- Generates minimal-progress updates instead of long reasoning chains
- Tracks changes and commits them to GitLab/GitHub
- Provides specific, actionable UI guidance for breaking changes

**Best for:** Projects that build on top of frameworks (e.g., custom browsers on Chromium), long-term dependency management, and multi-repo UI tracking.

### 4. Debug and Fix
**ID:** `debug-and-fix`
**Level:** Error Resolution

Finds and fixes bugs, crashes, and runtime errors by:
- Running tests and linters
- Analyzing error messages and stack traces
- Searching codebases for patterns
- Implementing fixes at the root cause

### 5. Systematic Issue Sweep
**ID:** `systematic-issue-sweep`
**Level:** Quality Assurance

When any issue or anti-pattern is found, sweeps the entire workspace to:
- Find all related occurrences
- Abstract the underlying mistake pattern
- Fix every instance
- Add regression guards

### 6. Agent Self-Awareness
**ID:** `agent-self-awareness`
**Level:** Model Detection

Detects the active harness and model, classifies capability tier, and switches to a research-first protocol when appropriate.

### 7. Context Search
**ID:** `context-search`
**Level:** Knowledge Recovery

Discovers prior agent work across codebases, locating session transcripts, databases, and prior decisions. Links to git history and current worktree.

### 8. Persistent Goal Execution
**ID:** `persistent-goal-execution`
**Level:** Orchestration

Keeps the complete user objective active across retry contexts, waits, and failures. Ensures work is completed before declaring success.

### 9. Credential Safety
**ID:** `credential-safety`
**Level:** Security

Stops agents from committing or pushing API keys, passwords, or tokens to remote repositories.

### 10. Deep Research
**ID:** `deep-research`
**Level:** Research

Reconstructs feature behavior and integration context from repositories when porting features or adapting codebases.

### 11. Error Docs Lookup
**ID:** `error-docs-lookup`
**Level:** Documentation

Searches and reads current official documentation before fixing build, compile, syntax, type, or runtime errors.

### 12. Google SEO Skill
**ID:** `google-seo-skill`
**Level:** Optimization

Audits crawlability, metadata, structured data, and Core Web Vitals for public web projects.

### 13. Human Writing
**ID:** `human-writing`
**Level:** Quality

Ensures all written text reads like a person typed it (no AI tells, no emoji, no em dashes).

### 14. Context Rich Commits
**ID:** `context-rich-commits`
**Level:** Git

Records git history as long-term memory, maintaining context across sessions with detailed commit messages.

## Installation

### For openagents/skills (OpenCode)

This repository is the primary install location. Skills are accessed via:

```json
{
  "skills": [
    "token-optimizer",
    "base-package-tracker",
    "debug-and-fix",
    "context-rich-commits",
    ...
  ]
}
```

### For Claude Code

1. Make a copy of the skills folder:
   ```bash
   cp -r /home/dev/projects/skills ~/.claude/skills/
   ```

2. Load a skill in Claude Code:
   ```bash
   /skill token-optimizer
   ```

### For Copilot CLI

1. Copy skills to:
   ```bash
   cp -r /home/dev/projects/skills ~/.copilot/skills/
   ```

2. Skills are loaded automatically by Copilot CLI via its configuration.

### For GitHub Copilot Workspace

The skills in `.agents/skills/` are picked up by Copilot Workspace in GitHub.

## Loading a Skill

Every skill has a frontmatter format:

```yaml
---
name: skill-id
description: One-line description of what the skill does
---

# Skill Documentation

Extended documentation here explaining:
- When to use the skill
- How it works
- Workflow steps
- Important notes
```

To load a skill, run:

```bash
.skill token-optimizer
```

Or in most agent interfaces, type:

```
/load token-optimizer
```

## Skill Structure

Each skill follows this structure:

```
skill-id/
├── SKILL.md                # Main documentation
├── scripts/                # Python scripts for automation
└── references/            # Additional documentation
    ├── design.md          # Design decisions
    ├── patterns.md        # Usage patterns
    └── examples.md        # Examples
```

## Skill Guidelines

### Creating a New Skill

When adding a skill, follow these principles:

1. **Keep it focused:** One skill = one clear problem domain
2. **Be Prescriptive:** Give clear, step-by-step instructions
3. **Use Frontmatter:** Include `name` and `description` for agent discovery
4. **Add Examples:** Provide concrete examples in scripts/references
5. **Document Dependencies:** Note other skills or requirements

### Naming Conventions

Use kebab-case IDs:
- ✅ `token-optimizer`
- ✅ `base-package-tracker`
- ✅ `android-app-dev`
- ❌ `TokenOptimizer`
- ❌ `BasePackageTracker`

### Documentation Style

- Write in imperative mood (e.g., "Run `npm test` instead of "You should run...")
- Use bold for tool names and file paths
- Provide code examples with syntax highlighting
- Keep descriptions within 5-10 words in frontmatter

## Contributing

1. Fork this repository
2. Create a feature branch
3. Add your skill in `skills/` directory
4. Render examples/test to ensure it's working
5. Submit a pull request with tested skills

## License

See LICENSE file for details.

## Support

For bug reports or feature requests, open an issue in this repository.

---

**Created:** 2026-11-11
**Maintained:** OpenCode Tools Team
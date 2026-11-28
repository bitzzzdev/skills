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

Mandatory for every task. Enforces natural, factual writing and prohibits emojis, emoji-like symbols, em dashes, and AI-generated filler in all communication and project files.

### 14. Context Rich Commits
**ID:** `context-rich-commits`
**Level:** Git

Records git history as long-term memory, maintains context across sessions, and requires monitoring every pushed commit's CI/CD runs through pass or a documented blocker.


### 15. Ponytail
**ID:** `ponytail`
**Level:** Coding approach

Applies a minimal-change approach: understand the affected code first, reuse existing behavior, and implement the smallest complete solution without removing validation, error handling, security, or accessibility.

### 16. Ponytail Review
**ID:** `ponytail-review`
**Level:** Change review

Reviews a diff for correctness, security, load behavior, missing tests, performance, and unnecessary code. Reports findings without changing files.

### 17. Ponytail Audit
**ID:** `ponytail-audit`
**Level:** Repository audit

Audits a repository for bugs, security risks, scaling problems, missing tests, slow paths, and code that can be removed or simplified.

### 18. Ponytail Debt
**ID:** `ponytail-debt`
**Level:** Deferred work tracking

Collects `shortcut:` comments into a ledger with the stated limit and the condition for revisiting each shortcut.

### 19. Ponytail Gain
**ID:** `ponytail-gain`
**Level:** Benchmark reference

Displays the benchmark figures published by the upstream Ponytail project. It does not estimate savings for the current repository.

### 20. Ponytail Help
**ID:** `ponytail-help`
**Level:** Quick reference

Lists Ponytail levels, companion skills, commands, and configuration options.

### 21. Parallel Agent Orchestration
**ID:** `parallel-agent-orchestration`
**Level:** Execution orchestration

Splits independent work across subagents and background processes. Defines task ownership, safe concurrency, process tracking, integration, and final verification.

### 22. Bento Terminal Orchestration
**ID:** `bento-terminal-orchestration`
**Level:** Remote terminal execution

Creates a persistent multi-agent workspace inside an SSH TTY using tmux, Zellij, or GNU Screen. Covers Bash and Fish background jobs, pane ownership, VPS resource limits, and plain-TTY fallbacks.

The six skills are imported from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) under MIT. See `ponytail/UPSTREAM.md` and `ponytail/LICENSE` for the source revision and license.

## Repository standards

All agents must load `human-writing/SKILL.md` at the start of every task. Emoji and emoji-like symbols are prohibited throughout project files and communication. Public and production releases must follow `production-ready/SKILL.md`, including user documentation, help, FAQs, troubleshooting, known issues, terms of use, privacy, and third-party credits where applicable.

## Installation

Clone the repository or update an existing checkout on `dev`, then run the
installer from the repository root:

```bash
git clone --branch dev https://gitlab.com/bitzzdev/skills.git
cd skills
./install.sh --dry-run
./install.sh
```

The installer finds every top-level directory containing `SKILL.md` and
creates a symlink to that directory. It does not copy skill files, so a later
`git pull` updates the linked content without reinstalling existing links.

| Agents | User skill directory |
|---|---|
| OpenCode, Codex, Cursor, Gemini CLI, GitHub Copilot CLI | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Kiro | `~/.kiro/skills/` |

OpenCode, Codex, Cursor, Gemini CLI, and Copilot share the Agent Skills
directory at `~/.agents/skills/`. Claude Code and Kiro use their own global
skill directories.

Options:

```bash
./install.sh --dry-run
./install.sh --list-agents
./install.sh --agent shared
./install.sh --agent claude
./install.sh --agent kiro
```

Repeat `--agent` to select more than one target. The default installs all
supported targets. Existing skill paths are never overwritten. A conflict is
reported and makes the installer exit with a non-zero status, so inspect the
existing path before deciding what to do. The installer does not remove stale
links for skills that have since been deleted from the repository.

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
- `token-optimizer`
- `base-package-tracker`
- `android-app-dev`
- `TokenOptimizer`
- `BasePackageTracker`

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
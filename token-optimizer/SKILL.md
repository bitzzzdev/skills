---
name: token-optimizer
description: Reduces AI agent token usage by disabling reasoning/thinking features across OpenCode, Claude Code, Copilot CLI, Muse, Antigravity, Aider, and other tools. Creates and updates task progress files, automatically tracks completed and pending work items, and uses minimal token introspection while preserving code quality. Ideal for long-running coding sessions or projects with frequent restarts where you want maximum throughput without wasting tokens on thinking overhead.
---

# Token Optimizer

This skill minimizes AI agent token usage while maintaining code quality by:

1. Detecting and disabling thinking/reasoning features in supported coding agents (OpenCode, Claude Code, Copilot CLI, Muse, Antigravity, Aider, Cline, Continue.dev, Roo Code, Cursor, Windsurf, etc.)
2. Automatically generating and updating a progress/todo file that tracks completion status
3. Adding new todos automatically when bugs, syntax issues, or blocking problems appear
4. Keeping quality intact by using simple progress tracking instead of full reasoning chains

## When to Use This Skill

- Running long coding sessions where thinking/reasoning costs add up
- Many project restarts where you need to pick up from where you left off
- Working on complex projects with multiple agents that keep thinking overhead enabled
- Projects where you want to maximize throughput while maintaining code standards

## What the Skill Does

### 1. Agent Configuration Detection

The skill scans your environment for common AI coding agents and checks if they have thinking/reasoning features enabled. It then disables them to stop API token generation for Chain-of-Thought reasoning.

Supported agents and their configuration paths:

| Agent | Config File | Detection Method | Disable Method |
|-------|-------------|------------------|----------------|
| **OpenCode** | `~/.config/opencode/opencode.json` | Checks for `enable_thinking: true` or `thinking: "high"` | Sets `enable_thinking: false` or `thinking: "hide"` |
| **Claude Code** | `~/.claude/settings.json` | Checks `alwaysThinkingEnabled` or `MAX_THINKING_TOKENS` | Sets both to `false`/`0` and sets `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` |
| **GitHub Copilot CLI** | `~/.copilot/settings.json` | Checks for reasoning-related flags | Clamps to lowest effort or switches to non-reasoning model |
| **Muse Code** | `~/.config/muse/settings.json` | Checks `reasoning_effort` | Sets to `none` |
| **Antigravity (agy)** | `~/.antigravity/settings.json` | Checks `thinking_level` | Sets to `MINIMAL` or removes `thinking_config` |
| **Codex CLI** | `~/.codex/config.toml` | Checks `model_reasoning_effort` | Sets to `none` or `minimal` |
| **Gemini CLI** | `~/.gemini/settings.json` | Checks `inlineThinkingMode` and `thinkingBudget` | Sets to `off` and `0` |
| **Aider** | `~/.aider.conf.yml` | Checks `thinking-tokens` or `reasoning-effort` | Sets both to `0` and `none` |
| **Cline** | `~/.cline/` or VS Code settings | Checks reasoning flags | Sets to `--thinking none` or UI to `OFF` |
| **Continue.dev** | `~/.continue/config.yaml` | Checks `reasoning` config | Sets to `false` |

### 2. Progress Tracking

Instead of using thinking tokens to plan and track work, the skill creates a simple **progress file** at `.progress.md` (in the current working directory) with this format:

```markdown
# Project Progress

## Active Agent
- Name: [agent name detected]
- Config Location: [path to config]
- Thinking Disabled: [yes/no]

## Tasks

### Completed
- [x] Task 1: Initial setup
- [x] Task 2: Create base structure
- [x] Task 3: Implement core feature

### In Progress
- [ ] Task 4: Add error handling
- [ ] Task 5: Write unit tests

### Pending
- [ ] Task 6: Deploy to staging
- [ ] Task 7: Run integration tests

## Bugs & Issues
- [ ] Bug 1: Syntax error in line 42
- [ ] Issue 1: Memory leak detected in module X

## Last Updated
- Timestamp: 2026-11-11T10:30:00Z
- Work session: [agent session ID if available]
```

### 3. Dynamic Task Management

When working:

1. **Start a task:** Mark it as in-progress `[~]` when you begin
2. **Finish a task:** Move to `[x]` when completed and optionally add details
3. **Encounter an issue:** Add to the Bugs & Issues section with:
   - A clear description
   - Affected file(s) and line(s)
   - Expected vs actual behavior
4. **Create a subtask:** Add a new bullet under `[ ]` to break complex tasks into smaller pieces

The progress file is written to disk, truncated, or appended to as needed with minimal tokens used for JSON/parsing operations.

### 4. Quality Preservation

Even though thinking is disabled, you still maintain:
- Access to existing context via git history, session transcripts, and documentation
- Code review and testing during normal development workflow
- Ability to use git branches, commits, and labels to organize work
- Manual quality checks before committing

The skill focuses on stopping unnecessary *internal* thinking overhead, not your *visible* quality checks or debugging.

## Workflow

### Initial Optimization Check

When you invoke this skill during a coding session:

1. **Detect active agents:** The skill scans all known agent config locations
2. **Check current state:** Reads existing config files to see what's enabled
3. **Apply improvements:**
   - Disables reasoning/thinking APIs where supported
   - Records current values as baseline for verification
   - Creates a backup of the modified file (`filename.bak`)
4. **Create progress file:** Sets up `.progress.md` in the current directory
5. **Report findings:** Informs you which agents were found and what was changed

### Task Planning

The skill doesn't force specific tasks, but it encourages a simple workflow:

1. **Prompt:** You describe what you want to build or fix
2. **Response:** Agent provides code with full quality (no thinking overhead)
3. **Generate todos:** The agent can mark completed tasks and create new ones dynamically
4. **Update progress:** Files are written as efficiently as possible

### Progress Update Command

After working on tasks, you can refresh the progress by:

```bash
# Sheep skill will check .progress.md and confirm current state
```

The skill reads the file and summarizes:
- How many tasks are completed vs pending
- Any open bugs or issues
- Recent changes in configuration

## Notes & Fallback

- Reasoning-enabled models that cannot be fully disabled (e.g., some DeepSeek/O1 series with minimum floors) are clamped to lowest possible level
- If an agent config file doesn't exist, no modification is attempted
- Config backups are created before any changes so you can restore if needed
- The skill is safe for day-to-day development; it enables max speed without sacrificing correctness
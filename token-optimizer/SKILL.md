---
name: token-optimizer
description: Applies conservative token-saving settings to detected coding agents, runs the settings editor at every task start, and maintains concise progress tracking without weakening verification.
---

# Token Optimizer

This skill reduces avoidable reasoning-token use while preserving code quality. It changes local agent configuration only where a supported setting is known. It cannot change the model or reasoning policy of a hosted ChatGPT session unless that host exposes a writable setting.

## Mandatory execution

At the beginning of every coding task, and again after changing the active agent, model, provider, or harness, run this command from the skills repository root:

```bash
python token-optimizer/scripts/optimize_agents.py
```

This is an apply operation. Do not replace it with a dry run, skip it because the model is frontier, or merely describe the settings that should change. The script is idempotent, creates a `.BAK` backup before each modified file, and reports every detected configuration. If you need to preview changes, run `--dry-run` first, then run the normal command.

The script must be run before substantive implementation, not after the task is finished. If the repository is installed as a standalone skill folder, run `python scripts/optimize_agents.py` from that folder.

### Honesty and safety

- Never claim the active model's reasoning was disabled because a local config file changed. Report the exact agent configuration that was modified.
- A UI option that hides reasoning output is not a token-saving setting. Do not count it as one.
- The script changes only known settings in detected files. It does not create speculative provider/model options.
- Configurations without a verified safe edit are reported as manual-only and left unchanged.
- Never edit a config file that cannot be parsed safely. Keep the original backup and report parse errors.
- If no supported configuration is found, report that fact. Do not invent a configuration path or claim success.
- Keep the `.BAK` file until the user has confirmed the new configuration works.

## Supported settings editor

The required script is `scripts/optimize_agents.py`.

It checks these locations:

| Agent | Configuration | Automatic behavior |
|---|---|---|
| OpenCode | `~/.config/opencode/opencode.json`, project `opencode.json` | Turns off existing `enable_thinking` and existing `reasoning.enabled` provider options only |
| Claude Code | `~/.claude/settings.json`, project `.claude/settings.local.json` | Sets `alwaysThinkingEnabled=false` and the documented thinking environment values |
| Codex CLI | `~/.codex/config.toml` | Sets `model_reasoning_effort=none`, or `low` for o-series models that require a floor |
| Gemini CLI | `~/.gemini/settings.json`, project `.gemini/settings.json` | Lowers existing model-specific `thinkingBudget` and `thinkingLevel` controls; does not mistake UI hiding for token savings |
| Muse Code | `~/.config/muse/settings.json` | Sets an existing `reasoning_effort` key to `none` |
| Antigravity | `~/.antigravity/settings.json` | Lowers existing `thinkingLevel` and `thinkingBudget` keys |
| Aider | `~/.aider.conf.yml`, project `.aider.conf.yml` | Sets `thinking-tokens: 0` and `reasoning-effort: none` |
| Copilot CLI | `~/.copilot/settings.json` | Detects the file but leaves it unchanged pending a verified stable settings schema; use the manual guidance in `references/agents.md` |

Cline, Continue.dev, Roo Code, Cursor, and Windsurf may expose controls through version-specific UI or extension state. Do not write guessed settings into those stores. Use the manual guidance in `references/agents.md` and verify the installed version's documentation.

## Workflow

1. Run the settings editor before implementation.
2. Read its output. Investigate parse failures and manual-only results instead of ignoring them.
3. Detect the active model and harness with `agent-self-awareness/scripts/detect_model.py` when available. Unknown models use the non-frontier research protocol.
4. Maintain a concise `.progress.md` for substantial tasks.
5. Mark work as active, completed, or blocked using plain text. Add new tasks when failures reveal more work.
6. Preserve backups and never overwrite another agent's unrelated work.
7. Run the relevant tests, review the diff, and report exact verification results.

## Progress file

Use this format in the active project:

```markdown
# Project Progress

## Active Agent
- Name: [detected agent]
- Configurations changed: [exact files, or none]
- Model reasoning changed: [yes/no/unknown, with evidence]

## Tasks
### Completed
- [x] Task description

### In Progress
- [ ] Task description

### Pending
- [ ] Task description

## Bugs and Issues
- [ ] Confirmed issue and affected file

## Last Updated
- Timestamp: [ISO 8601]
- Session: [session ID, if available]
```

Do not use progress tracking as a substitute for tests, source inspection, or documentation lookup.

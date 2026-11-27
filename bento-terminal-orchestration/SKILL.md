---
name: bento-terminal-orchestration
description: Runs multiple coding agents in one remote terminal.
---

# Bento Terminal Orchestration

Build a compact, persistent multi-agent workspace inside one terminal. Use terminal panes as a bento layout: one coordinator pane and separate worker panes, with optional background jobs for non-interactive commands. The workflow must work over SSH on a VPS with a plain TTY and either Bash or Fish.

This skill complements `parallel-agent-orchestration`. That skill decides what can run concurrently and how to integrate the work. This skill provides the terminal layout and process-control mechanics.

## When to use

Use this skill when:

- The user is connected to a VPS over SSH.
- The environment is a terminal-only TTY with no desktop or GUI.
- Multiple interactive coding agents need their own terminal sessions.
- A coordinator needs to watch workers, logs, and tests in one terminal.
- The user uses Bash or Fish and wants a repeatable pane layout.

Do not use it for a single short task, or when the active agent harness already provides reliable native subagents and a terminal layout would add overhead.

## Operating model

Use one terminal multiplexer session as the workspace:

- **Coordinator pane:** owns the task, plan, shared state, integration, and final verification.
- **Worker panes:** each runs one interactive agent or one bounded command.
- **Observer pane:** tails logs, watches tests, or inspects process state.
- **Background jobs:** run only non-interactive commands that do not need a TTY.

Every worker needs an explicit task, file ownership, acceptance criteria, and return format. Keep Git writes and final integration under coordinator control.

## Capability detection

Start by detecting the current shell, TTY, and available multiplexer. Do not assume a package is installed.

```sh
printf 'shell=%s\\n' "${SHELL:-unknown}"
printf 'tty='
tty 2>/dev/null || true
printf 'tmux='
command -v tmux || true
printf 'zellij='
command -v zellij || true
printf 'screen='
command -v screen || true
printf 'agents: '
for agent in opencode codex claude gemini copilot aider goose; do
  command -v "$agent" 2>/dev/null || true
done
```

Choose the first supported option:

1. **tmux:** preferred for SSH and minimal VPS environments. It supports persistent sessions, pane targeting, and layouts.
2. **Zellij:** use when installed and the user prefers its terminal UI.
3. **GNU Screen:** use for persistent terminal windows when tmux and Zellij are unavailable.
4. **Plain TTY fallback:** run one interactive coordinator and use tracked background jobs for non-interactive work. A plain TTY cannot provide several independent interactive agent terminals without a multiplexer or another PTY manager.

Do not install packages automatically. If a multiplexer is missing, explain the option and use the available fallback. Follow the user's package manager and approval requirements.

## Build a tmux bento

Create a named session from the project root. Start with two or three workers, not one pane per possible agent.

```sh
session="agent-bento"
project_dir="$(pwd -P)"

if tmux has-session -t "$session" 2>/dev/null; then
  printf 'Reusing tmux session: %s\\n' "$session"
else
  tmux new-session -d -s "$session" -n work -c "$project_dir"
  tmux split-window -h -t "$session:work" -c "$project_dir"
  tmux split-window -v -t "$session:work.1" -c "$project_dir"
  tmux select-layout -t "$session:work" tiled
fi

tmux list-panes -t "$session:work" \\
  -F 'pane=#{pane_index} id=#{pane_id} pid=#{pane_pid} size=#{pane_width}x#{pane_height} path=#{pane_current_path}'
tmux attach-session -t "$session"
```

The initial layout is a three-pane bento. Adapt the pane count to available memory and terminal dimensions. On a narrow terminal, use separate windows instead of tiny panes.

### Pane roles

Assign roles before launching agents:

| Pane | Role | Typical command |
|---|---|---|
| 0 | Coordinator | Current agent session or shell |
| 1 | Research worker | Agent CLI with a read-only research task |
| 2 | Implementation worker | Agent CLI with exclusive file ownership |
| 3 | Observer | Test command, log tail, or process monitor |

Do not assume pane indexes remain stable after panes are closed. Record pane IDs with `tmux list-panes` and target those IDs when sending commands.

### Launch interactive workers

Launch a worker only after its task contract is ready. Use a separate pane for each interactive agent so each process receives its own TTY.

Example with OpenCode:

```sh
tmux split-window -h -t agent-bento:work -c "$project_dir"
tmux send-keys -t agent-bento:work.2 'opencode' C-m
```

Example with Claude Code:

```sh
tmux split-window -v -t agent-bento:work -c "$project_dir"
tmux send-keys -t agent-bento:work.3 'claude' C-m
```

These are examples, not guaranteed CLI flags. Start the CLI without invented arguments, then provide the bounded task through its supported prompt interface. Confirm the executable exists first.

If a CLI supports a documented non-interactive prompt mode, it may be used as a background job instead. Do not send passwords, API keys, or authentication codes through pane command strings or logs.

### Inspect and control the workspace

```sh
tmux list-sessions
tmux list-windows -t agent-bento
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_id} #{pane_current_command}'
tmux capture-pane -p -t agent-bento:work.1 -S -80
tmux select-pane -t agent-bento:work.1
tmux attach-session -t agent-bento
```

Detach with `Ctrl-b` then `d`. The session continues on the VPS. Reconnect over SSH and run `tmux attach-session -t agent-bento`.

Do not kill a pane or session until its worker's result and any unsaved work are checked. Use `tmux kill-pane` only for a confirmed finished or cancelled worker. Keep the session after SSH disconnects; do not use `exit` in the coordinator pane unless the session is intentionally finished.

## Bash and Fish background jobs

Use background jobs for non-interactive tests, builds, scans, and read-only commands. Keep logs and exit status. These commands do not create interactive agent terminals.

See `references/tty-bento-patterns.md` for Bash and Fish process patterns, TTY limitations, and a full session checklist.

## Resource limits on VPS hosts

- Inspect available CPU and memory before launching more model clients.
- Start with one coordinator and one or two workers. Add a worker only when the task graph has another independent task and the VPS has headroom.
- Prefer lightweight read-only research workers over multiple full coding runtimes.
- Avoid running multiple builds, package managers, language servers, or indexers against the same checkout.
- If memory pressure, swapping, terminal lag, or provider rate limits rise, stop adding workers and reduce concurrency.
- Keep model/API usage and provider limits in view. More panes do not create more compute capacity.

## Shared worktree and Git safety

- Prefer read-only research workers.
- Give each writing worker exclusive paths.
- For concurrent edits, use separate Git worktrees or separate branches. Do not have workers switch branches in one shared worktree.
- Do not let workers independently commit, push, rebase, merge, or change remote refs.
- Keep one coordinator responsible for integration and final tests.
- Do not run two formatters, package managers, generators, or builds against the same mutable paths.
- Preserve user changes and follow repository instructions, credential-safety, and approval gates.

## Plain TTY fallback

If no multiplexer exists, keep the current shell as coordinator. Start only non-interactive jobs in the background, capture each log and status, and poll the same PID. Use native subagents if the harness actually exposes them.

A plain SSH TTY cannot host multiple independent full-screen interactive CLIs in the same terminal safely. Do not fake this with several commands writing to one terminal. Either use an available multiplexer, use the harness's native subagent mechanism, or keep interactive work sequential.

## Completion gate

Before reporting completion:

1. Collect every worker's final response and changed paths.
2. Inspect all worker diffs and check for overlapping edits.
3. Read every background log and exit status.
4. Integrate changes in dependency order.
5. Run focused and final tests against the integrated tree.
6. Check Git status, branch, and diff.
7. Record the session name, worker roles, pane or process IDs, logs, exit codes, and unresolved items in the project handoff.
8. Leave the tmux session running if the user may want to resume it. Otherwise close it only after confirming all work is saved.

A pane being visible, an agent appearing active, or a command returning no output is not evidence of success.

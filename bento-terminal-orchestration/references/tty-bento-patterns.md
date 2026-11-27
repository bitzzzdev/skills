# TTY Bento Patterns

These examples target Bash and Fish in an SSH session on a Linux VPS. They use ordinary terminal tools and do not require a desktop environment.

## Bash background job with a durable status file

Use this for a non-interactive command. Keep the shell session alive so `wait` can collect the job.

```bash
log_file=$(mktemp)
status_file=$(mktemp)
(
  set +e
  your_noninteractive_command
  command_status=$?
  printf '%s\n' "$command_status" > "$status_file"
  exit "$command_status"
) >"$log_file" 2>&1 &
process_id=$!
printf 'pid=%s log=%s status=%s\n' "$process_id" "$log_file" "$status_file"

# Continue independent work here.

wait "$process_id"
wait_status=$?
cat "$log_file"
if test -f "$status_file"; then
  printf 'command exit status: %s\n' "$(cat "$status_file")"
else
  printf 'No status file was written. Inspect the process and log.\n'
fi
printf 'wait status: %s\n' "$wait_status"
```

Do not start a duplicate command because a poll is slow. Check the original PID and log.

## Fish background job with a durable status file

Fish has different list and status syntax. Use `$last_pid` immediately after starting the background block.

```fish
set log_file (mktemp)
set status_file (mktemp)
begin
    your_noninteractive_command
    set command_status $status
    printf '%s\n' $command_status > $status_file
end > $log_file 2>&1 &
set process_id $last_pid
printf 'pid=%s log=%s status=%s\n' $process_id $log_file $status_file

# Continue independent work here.

wait $process_id
set wait_status $status
cat $log_file
if test -f $status_file
    printf 'command exit status: %s\n' (cat $status_file)
else
    printf 'No status file was written. Inspect the process and log.\n'
end
printf 'wait status: %s\n' $wait_status
```

Run `help wait` if the installed Fish version has different wait behavior. The status file records the wrapped command's exit status.

## Detached jobs and SSH disconnects

A shell's `&` only backgrounds a process. It does not guarantee survival after SSH disconnects. Prefer a detached tmux session for interactive agents and long-running work that must survive disconnects.

For a non-interactive command that must outlive the shell, use a documented service manager or `nohup` only when appropriate. Redirect both output streams and write an exit-status file. Do not assume `disown`, `nohup`, or shell job control behaves identically across shells and SSH server configurations.

## tmux bento quick start

Run from the project directory:

```sh
session="agent-bento"
project_dir="$(pwd -P)"
if ! tmux has-session -t "$session" 2>/dev/null; then
  tmux new-session -d -s "$session" -n work -c "$project_dir"
  tmux split-window -h -t "$session:work" -c "$project_dir"
  tmux split-window -v -t "$session:work.1" -c "$project_dir"
  tmux select-layout -t "$session:work" tiled
fi
tmux list-panes -t "$session:work" -F '#{pane_id} #{pane_current_command} #{pane_current_path}'
tmux attach -t "$session"
```

Attach after reconnecting:

```sh
tmux attach -t agent-bento
```

Detach without stopping workers: press `Ctrl-b`, then `d`.

## When only a plain TTY is available

A plain TTY provides one foreground terminal. It cannot safely host several full-screen interactive agents at once. Use native subagents exposed by the current harness, or run independent non-interactive commands with captured logs and PIDs. Do not redirect several interactive programs into one terminal.

## VPS sizing and concurrency

Check resources before opening more workers:

```sh
nproc
free -h
uptime
df -h .
```

These commands are Linux-oriented. On constrained VPS instances, start with one coordinator and one worker. Add workers only when memory, CPU, disk, and provider limits allow. Avoid multiple language servers, dependency installs, and builds sharing the same worktree.

## Pane and worker checklist

- One coordinator owns the task graph and final integration.
- Each interactive worker has a dedicated pane and TTY.
- Each worker has a bounded task and exclusive write paths.
- The pane ID, worker role, and current command are recorded.
- Non-interactive background jobs have logs, PIDs, and exit-status files.
- Every process is collected or explicitly cancelled.
- Worker changes are reviewed before integration.
- Final tests run after integration.
- The handoff records unfinished work and whether the tmux session remains available.

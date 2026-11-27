# Parallel Workflows

Use these patterns only when supported by the active harness and shell.

## Delegation contract

    Objective:
      Return one specific deliverable.

    Context:
      Relevant architecture, decisions, conventions, and constraints.

    Owned paths:
      Exact files or directories this worker may edit.

    Do not touch:
      Shared files, unrelated modules, Git refs, and deployment settings.

    Dependencies:
      Required inputs and upstream decisions.

    Acceptance:
      Observable conditions for completion.

    Verification:
      Safe commands and actual results.

    Return:
      Findings, changed paths, decisions, tests, and blockers.

For research-only workers, prohibit file edits. For implementation workers, assign exclusive file ownership. Agree on interfaces before starting components that depend on each other.

## Background process: Bash

Run a non-interactive command in the background, preserve its log and exit code, then continue unrelated work in the same shell session.

    log_file=$(mktemp)
    status_file=$(mktemp)
    (
      set +e
      long_running_command
      command_status=$?
      printf '%s\n' "$command_status" > "$status_file"
      exit "$command_status"
    ) >"$log_file" 2>&1 &
    process_id=$!
    printf 'pid=%s\nlog=%s\nstatus=%s\n' "$process_id" "$log_file" "$status_file"

Later, in the same shell session:

    wait "$process_id"
    wait_status=$?
    cat "$log_file"
    if test -f "$status_file"; then
      command_status=$(cat "$status_file")
      printf 'command exit status: %s\n' "$command_status"
    else
      printf 'No status file was written; inspect the process and log.\n'
    fi
    printf 'wait status: %s\n' "$wait_status"

The status file records the command exit code. If the shell or terminal session closes, the process may be terminated or become un-waitable. Do not assume it survived. Inspect the PID and log before considering a rerun.

## Background process: Fish

Fish uses its own process ID and status variables.

    set log_file (mktemp)
    set status_file (mktemp)
    begin
        long_running_command
        set command_status $status
        printf '%s\n' $command_status > $status_file
    end > $log_file 2>&1 &
    set process_id $last_pid
    printf 'pid=%s\nlog=%s\nstatus=%s\n' $process_id $log_file $status_file

Later, in the same fish session:

    wait $process_id
    set wait_status $status
    cat $log_file
    if test -f $status_file
        set command_status (cat $status_file)
        printf 'command exit status: %s\n' $command_status
    else
        printf 'No status file was written; inspect the process and log.\n'
    end
    printf 'wait status: %s\n' $wait_status

Confirm shell behavior if the host embeds an older or restricted Fish version. The status file is the command's exit code; the wait result is the shell's process-wait result.

## Polling without duplicate work

- Keep the original PID, task ID, or job handle.
- Check whether it is still running using supported process inspection.
- Read the latest log tail while it runs.
- If active, continue independent work and poll the same handle later.
- If exited, read the relevant log and recorded status.
- If failed, capture the failure and retry only after identifying the cause.
- Never start a second copy because the first poll was slow or timed out.

## Safe and unsafe background jobs

Usually safe when isolated:

- Unit tests for a module no longer being edited.
- Type checks on an immutable snapshot or separate worktree.
- Dependency metadata inspection and read-only repository scans.
- Builds with separate output directories.
- Benchmarks on a stable build.

Usually unsafe without isolation:

- Two package managers changing one lockfile or dependency directory.
- Two formatters writing the same source tree.
- Multiple builds sharing one output directory.
- Database migrations or destructive maintenance.
- Git operations changing the same worktree or branch.
- Interactive authentication or deployment approvals.
- Tests mutating shared fixtures, snapshots, ports, or external services.

## Integration checklist

- Every delegated task returned a result.
- Every background process has a known final state.
- Worker changes were reviewed and integrated.
- No workers silently overwrote the same file.
- Focused and integration tests ran against the integrated state.
- Final diff and Git status are clean or explained.
- The handoff records failed, cancelled, and unverified work.

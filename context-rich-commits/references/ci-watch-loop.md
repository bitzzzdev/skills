# CI/CD Watch Loop

Use this after every push that can trigger CI/CD. A successful push is not a successful change. Keep watching the pipeline for the exact pushed commit until it reaches a verified terminal state. If it fails, diagnose and fix the cause, push the fix, and watch the new commit's pipeline from the beginning.

## Required behavior

1. Record the pushed branch and full commit SHA immediately after the push.
2. Identify every CI provider and workflow that should run for that branch and commit. Inspect repository workflow files and branch/path filters rather than assuming a pipeline exists.
3. Find the pipeline or workflow run associated with that exact SHA. Do not watch only a moving "latest pipeline" pointer when newer commits may arrive.
4. If no run appears immediately, poll for creation with a reasonable interval. Check whether the push is excluded by rules, workflows are disabled, permissions are missing, or the provider has not scheduled the run yet.
5. While the run is queued, pending, running, or waiting for a runner, keep monitoring it. Use provider APIs, CLI watch commands, or the connected CI integration. Avoid tight polling loops.
6. Inspect all jobs and stages. A green top-level status is not enough if required checks were skipped, omitted, or never created.
7. Treat only a completed successful run for the exact SHA, with all required jobs passed, as verified CI success.
8. If any required job fails, inspect its logs and artifacts, identify the root cause, fix it in the repository, run the relevant checks locally, commit the fix, and push it to the same intended branch.
9. After the fix push, record the new SHA and return to step 2. Watch the new run to completion. Repeat until the required checks pass or a genuine external blocker prevents progress.
10. After the final passing run, verify that the passing pipeline SHA equals the branch head being promoted or reported as complete.

## Status handling

| Provider state | Required action |
|---|---|
| queued, pending, created, running, waiting for resource | Continue watching |
| success, passed, completed successfully | Inspect required jobs and verify exact SHA |
| failed, failure, action_required | Inspect failed jobs and logs, then fix |
| canceled, cancelled, skipped, manual, blocked | Not a pass. Determine why and whether a permitted action can resolve it |
| no pipeline found | Check trigger rules, branch filters, provider configuration, permissions, and scheduling delay |
| pipeline failed before any job starts | Treat as a CI orchestration, account, runner, or configuration blocker until evidence identifies the cause. No tests ran |
| optional job skipped | Confirm it is genuinely optional under repository policy; never silently treat a missing required check as passed |

## Failure diagnosis and repair

- Retrieve the failed job's full log or trace, not just the summary badge.
- Identify the first causal error. Later failures may be consequences.
- Classify the failure: source defect, test regression, dependency or lockfile issue, workflow syntax/configuration, unavailable runner, provider outage, permission/identity restriction, secret or variable problem, or external service failure.
- For source and test defects, reproduce the failing command locally, fix the root cause, add or update regression coverage, and run focused tests plus the relevant full suite.
- For workflow/configuration defects, validate the workflow syntax and confirm branch/path rules and required jobs.
- Retry a failed job or pipeline without a code change only when logs show a transient infrastructure failure and retrying is safe. Do not use retries to hide deterministic failures.
- Do not repeatedly retry the same deterministic failure. If the repair needs a secret, permission, identity verification, runner, external service, or human approval that is unavailable, record the blocker and the exact action needed.
- Preserve user changes and branch policy. Do not force-push, rewrite pushed history, bypass required checks, disable failing tests, or push to a protected production branch to evade CI.

## Provider and command guidance

- **GitLab:** identify the pipeline by project, ref, and commit SHA. Inspect pipeline status, jobs, and each failed job trace. Continue polling while the status is non-terminal. If a pipeline has no jobs or never starts, investigate trigger rules, account restrictions, and runner availability; do not claim tests ran.
- **GitHub Actions:** identify workflow runs for the pushed commit SHA, inspect run status and conclusion, then inspect jobs and failed job logs. A run triggered by a pull request is not proof that the push-triggered workflow ran unless repository policy explicitly treats it as the required check.
- **Other providers:** use the provider's documented CLI/API to query the exact commit, status, required checks, jobs, and logs.
- If a CLI offers a documented watch command, use it. Otherwise poll the provider API at a reasonable interval and keep the watch active while doing independent safe work.
- Do not claim that a watcher is active if the tool call or process has ended. If the environment cannot keep a process running between turns, continue polling through available tools or clearly report the monitoring limitation.

## Completion report

Report:

- Branch and exact final commit SHA.
- CI provider and pipeline/run URL or ID.
- Final pipeline conclusion and required job results.
- Any failures found, root causes, repair commits, and subsequent passing run.
- Any jobs that were skipped or not required, with the evidence for that decision.
- Any external blocker. A blocked, missing, canceled, skipped, or never-started pipeline is not a pass.

Never report "CI passed" based on a successful push, a queued run, a green badge for a different SHA, a partial job set, or a pipeline that never started.

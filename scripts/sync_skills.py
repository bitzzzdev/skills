#!/usr/bin/env python3
"""Smart sync for bitzzdev/skills clones across GitHub and GitLab.

Fetches both remotes, checks CI evidence for the dev branch, and updates each
clone from the newest source that is actually verified. When GitHub Actions is
unavailable and the GitLab dev pipeline passed, it switches the clone to the
tested dev branch instead of leaving it on a stale main.

Usage:
    python sync_skills.py --all
    python sync_skills.py --folder ~/.agents/skills
    python sync_skills.py --clone
    python sync_skills.py --all --dry-run
    python sync_skills.py --all --assume-gitlab-dev-passed
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HOME = Path.home()

GITHUB_REPO = os.environ.get("SKILLS_GITHUB_REPO", "bitzzdev/skills")
GITLAB_PROJECT = os.environ.get("SKILLS_GITLAB_PROJECT", "bitzzdev/skills")
GITLAB_URL = os.environ.get("SKILLS_GITLAB_URL", "git@gitlab.com:bitzzdev/skills.git")
GITLAB_API = os.environ.get("SKILLS_GITLAB_API", "https://gitlab.com/api/v4")
GITHUB_CLONE_URL = os.environ.get(
    "SKILLS_GITHUB_URL", "https://github.com/bitzzdev/skills"
)

DEFAULT_FOLDERS = [
    HOME / ".agents/skills",
    HOME / ".claude/skills",
    HOME / ".cursor/skills",
    HOME / ".github/skills",
    HOME / ".gemini/skills",
    HOME / ".gemini/antigravity-cli/skills",
    HOME / ".gemini/config/skills",
    HOME / ".copilot/skills",
    HOME / ".kiro/skills",
    HOME / ".windsurf/skills",
]

TRUST_FILE = Path(
    os.environ.get(
        "SKILLS_TRUST_FILE", str(HOME / ".config/agent-skills/trust-gitlab-dev")
    )
)


def run(command, cwd=None, timeout=60):
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, "", str(exc)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git(folder, *args, timeout=60):
    return run(["git", "-C", str(folder), *args], timeout=timeout)


def current_branch(folder):
    code, out, _ = git(folder, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0 or not out or out == "HEAD":
        return None
    return out


def is_dirty(folder):
    code, out, _ = git(folder, "status", "--porcelain")
    return code != 0 or bool(out)


def ensure_remote(folder, dry_run):
    code, out, _ = git(folder, "remote", "get-url", "gitlab")
    if code != 0:
        if dry_run:
            return True, "would add gitlab remote"
        code, _, err = git(folder, "remote", "add", "gitlab", GITLAB_URL)
        return code == 0, err or "added gitlab remote"
    if out != GITLAB_URL:
        if dry_run:
            return True, "would update gitlab remote URL"
        code, _, err = git(folder, "remote", "set-url", "gitlab", GITLAB_URL)
        return code == 0, err or "updated gitlab remote URL"
    return True, ""


def fetch_remote(folder, remote, dry_run):
    if dry_run:
        return True, ""
    code, _, err = git(folder, "fetch", "--prune", remote)
    return code == 0, err


def resolve_ref(folder, ref):
    code, out, _ = git(folder, "rev-parse", "--verify", "--quiet", ref)
    if code != 0 or not out:
        return None
    return out


def commit_time(folder, sha):
    code, out, _ = git(folder, "log", "-1", "--format=%ct", sha)
    if code != 0 or not out.isdigit():
        return 0
    return int(out)


def is_ancestor(folder, older, newer):
    code, _, _ = git(folder, "merge-base", "--is-ancestor", older, newer)
    return code == 0


def local_branch_exists(folder, branch):
    code, _, _ = git(folder, "rev-parse", "--verify", "--quiet", "refs/heads/" + branch)
    return code == 0


def github_ci(sha):
    if not sha:
        return "unavailable", "no GitHub dev commit"
    if not shutil.which("gh"):
        return "unavailable", "gh CLI not installed"
    query = "repos/%s/actions/runs?head_sha=%s" % (GITHUB_REPO, sha)
    code, out, err = run(["gh", "api", query, "--jq", ".workflow_runs"])
    if code != 0:
        return "unavailable", err or "gh api failed"
    try:
        runs = json.loads(out or "[]")
    except json.JSONDecodeError:
        return "unavailable", "invalid gh output"
    if not runs:
        return "unavailable", "no workflow run for this commit"
    if any(item.get("conclusion") == "success" for item in runs):
        return "passed", "GitHub Actions success"
    if any(item.get("status") in {"queued", "in_progress", "waiting", "requested"} for item in runs):
        return "pending", "GitHub Actions still running"
    conclusions = {item.get("conclusion") for item in runs if item.get("conclusion")}
    if conclusions and conclusions <= {"failure", "cancelled", "timed_out", "action_required"}:
        return "failed", "GitHub Actions failed"
    return "unavailable", "no conclusive GitHub run"


def gitlab_ci(sha, ref, assume_passed):
    if not sha:
        return "unavailable", "no GitLab dev commit"
    if assume_passed:
        return "passed", "trusted by --assume-gitlab-dev-passed"
    if TRUST_FILE.exists():
        return "passed", "trusted by " + str(TRUST_FILE)
    token = (
        os.environ.get("GITLAB_TOKEN")
        or os.environ.get("GLAB_TOKEN")
        or os.environ.get("CI_JOB_TOKEN")
    )
    if not token:
        return "unavailable", "set GITLAB_TOKEN to verify GitLab pipelines"
    project = urllib.parse.quote(GITLAB_PROJECT, safe="")
    query = urllib.parse.urlencode({"ref": ref, "sha": sha, "per_page": 5})
    url = "%s/projects/%s/pipelines?%s" % (GITLAB_API.rstrip("/"), project, query)
    request = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        return "unavailable", "GitLab API error: %s" % exc
    if not payload:
        return "unavailable", "no GitLab pipeline for this commit"
    latest = max(payload, key=lambda item: item.get("id", 0))
    status = latest.get("status", "")
    if status == "success":
        return "passed", "GitLab pipeline %s success" % latest.get("id")
    if status in {"failed", "canceled", "cancelled"}:
        return "failed", "GitLab pipeline %s %s" % (latest.get("id"), status)
    if status in {"created", "waiting_for_resource", "preparing", "pending", "running"}:
        return "pending", "GitLab pipeline %s %s" % (latest.get("id"), status)
    return "unavailable", "GitLab pipeline %s %s" % (latest.get("id"), status)


def collect_refs(folder, branch):
    refs = {}
    for remote_name, remote in (("github", "origin"), ("gitlab", "gitlab")):
        sha = resolve_ref(folder, "%s/%s" % (remote, branch))
        if sha:
            refs[remote_name] = {
                "remote": remote,
                "branch": branch,
                "ref": "%s/%s" % (remote, branch),
                "sha": sha,
                "time": commit_time(folder, sha),
            }
    return refs


def newest(refs):
    if not refs:
        return None
    return max(refs.values(), key=lambda item: item["time"])


def choose_target(folder, branch, assume_gitlab, dry_run, log):
    dev_refs = collect_refs(folder, "dev")
    github_dev = dev_refs.get("github")
    gitlab_dev = dev_refs.get("gitlab")

    github_state, github_detail = github_ci(github_dev["sha"] if github_dev else "")
    gitlab_state, gitlab_detail = gitlab_ci(
        gitlab_dev["sha"] if gitlab_dev else "",
        "dev",
        assume_gitlab,
    )

    log["github_dev_ci"] = github_state
    log["github_dev_detail"] = github_detail
    log["gitlab_dev_ci"] = gitlab_state
    log["gitlab_dev_detail"] = gitlab_detail

    target = None
    reason = ""

    if github_state == "unavailable" and gitlab_state == "passed" and gitlab_dev:
        target = gitlab_dev
        reason = "GitHub CI unavailable and GitLab dev pipeline passed"
    elif github_state == "passed" and gitlab_state == "passed":
        target = max([github_dev, gitlab_dev], key=lambda item: item["time"])
        reason = "both dev remotes passed CI; using the newer one"
    elif github_state == "passed" and github_dev:
        target = github_dev
        reason = "GitHub dev pipeline passed"
    elif gitlab_state == "passed" and gitlab_dev:
        target = gitlab_dev
        reason = "GitLab dev pipeline passed"

    if target:
        return target, reason

    current_refs = collect_refs(folder, branch)
    fallback = newest(current_refs)
    if fallback:
        return fallback, "no passing dev CI evidence; using newest %s" % branch
    return None, "no usable branch on either remote"


def apply_target(folder, current, target, dry_run, allow_branch_switch, log):
    target_branch = target["branch"]
    target_sha = target["sha"]
    target_ref = target["ref"]

    if target_branch != current:
        if not allow_branch_switch:
            return False, "selected %s but branch switching is disabled" % target_branch
        if current not in {"main", "dev"} or target_branch not in {"main", "dev"}:
            return False, "refusing to switch from %s to %s" % (current, target_branch)
        if is_dirty(folder):
            return False, "local changes present; not switching to %s" % target_branch
        if dry_run:
            log["would_switch"] = target_branch
            return True, "would switch to %s" % target_branch
        if local_branch_exists(folder, target_branch):
            code, _, err = git(folder, "checkout", target_branch)
        else:
            code, _, err = git(
                folder, "checkout", "-b", target_branch, "--track", target_ref
            )
        if code != 0:
            return False, "could not switch to %s: %s" % (target_branch, err)
        log["switched"] = target_branch
        current = target_branch

    local_sha = resolve_ref(folder, "HEAD")
    if local_sha == target_sha:
        return True, "already up to date on %s" % current
    if not is_ancestor(folder, local_sha, target_sha):
        if is_ancestor(folder, target_sha, local_sha):
            return False, "local %s is ahead of selected source" % current
        return False, "local %s has diverged from selected source" % current
    if dry_run:
        log["would_ff"] = target_sha
        return True, "would fast-forward to %s" % target_sha[:12]
    code, _, err = git(folder, "merge", "--ff-only", target_ref)
    if code != 0:
        return False, "fast-forward failed: %s" % err
    log["updated_to"] = target_sha
    return True, "updated to %s" % target_sha[:12]


def sync_folder(folder, args, log):
    folder = Path(folder).expanduser()
    log["folder"] = str(folder)
    if not (folder / ".git").is_dir():
        log["status"] = "skipped"
        log["detail"] = "not a git repository"
        return False

    if is_dirty(folder):
        log["status"] = "skipped"
        log["detail"] = "local changes present"
        return False

    branch = current_branch(folder)
    if not branch:
        log["status"] = "skipped"
        log["detail"] = "detached HEAD"
        return False
    log["branch"] = branch

    ok, detail = ensure_remote(folder, args.dry_run)
    if not ok:
        log["status"] = "failed"
        log["detail"] = detail
        return False

    github_ok, github_err = fetch_remote(folder, "origin", args.dry_run)
    gitlab_ok, gitlab_err = fetch_remote(folder, "gitlab", args.dry_run)
    log["github_fetch"] = "ok" if github_ok else (github_err or "failed")
    log["gitlab_fetch"] = "ok" if gitlab_ok else (gitlab_err or "failed")
    if not github_ok and not gitlab_ok:
        log["status"] = "failed"
        log["detail"] = "no remote could be fetched"
        return False

    target, reason = choose_target(
        folder, branch, args.assume_gitlab_dev_passed, args.dry_run, log
    )
    log["reason"] = reason
    if not target:
        log["status"] = "failed"
        log["detail"] = reason
        return False
    log["source"] = target["ref"]
    log["source_sha"] = target["sha"]

    ok, detail = apply_target(
        folder,
        branch,
        target,
        args.dry_run,
        allow_branch_switch=not args.no_branch_switch,
        log=log,
    )
    log["status"] = "ok" if ok else "failed"
    log["detail"] = detail
    return ok


def clone_all(args):
    failures = 0
    for folder in DEFAULT_FOLDERS:
        folder = Path(folder).expanduser()
        if folder.exists():
            print("%s already exists. Skipping clone." % folder)
            continue
        print("Cloning skills to %s..." % folder)
        if args.dry_run:
            continue
        folder.parent.mkdir(parents=True, exist_ok=True)
        code, _, err = run(["git", "clone", GITHUB_CLONE_URL, str(folder)], timeout=300)
        if code != 0:
            print("Clone failed for %s: %s" % (folder, err))
            failures += 1
            continue
        git(folder, "remote", "add", "gitlab", GITLAB_URL)
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", action="append", default=[], help="skills clone to sync")
    parser.add_argument("--all", action="store_true", help="sync every known skills folder")
    parser.add_argument("--clone", action="store_true", help="clone missing skills folders")
    parser.add_argument("--dry-run", action="store_true", help="show actions without changing files")
    parser.add_argument("--json", action="store_true", help="print machine-readable results")
    parser.add_argument("--no-branch-switch", action="store_true", help="never switch branches")
    parser.add_argument(
        "--assume-gitlab-dev-passed",
        action="store_true",
        help="treat GitLab dev as CI verified (use only after checking the pipeline)",
    )
    args = parser.parse_args()

    if args.clone:
        return clone_all(args)

    folders = [Path(item).expanduser() for item in args.folder]
    if args.all or not folders:
        folders = DEFAULT_FOLDERS

    results = []
    failures = 0
    for folder in folders:
        log = {}
        ok = sync_folder(folder, args, log)
        results.append(log)
        if not ok:
            failures += 1
        if not args.json:
            print("%s: %s" % (log.get("folder", folder), log.get("status", "unknown")))
            if log.get("reason"):
                print("  reason: %s" % log["reason"])
            print(
                "  CI: GitHub dev %s (%s); GitLab dev %s (%s)"
                % (
                    log.get("github_dev_ci", "unknown"),
                    log.get("github_dev_detail", ""),
                    log.get("gitlab_dev_ci", "unknown"),
                    log.get("gitlab_dev_detail", ""),
                )
            )
            if log.get("source"):
                print("  source: %s at %s" % (log["source"], log["source_sha"][:12]))
            if log.get("detail"):
                print("  result: %s" % log["detail"])

    if args.json:
        print(json.dumps(results, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Exercise the smart sync engine against twin local remotes.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYNC="$REPO_ROOT/scripts/sync_skills.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

GITHUB="$TMP/github.git"
GITLAB="$TMP/gitlab.git"
WORK="$TMP/work"
CLONE="$TMP/clone"

export SKILLS_GITLAB_URL="$GITLAB"
export SKILLS_TRUST_FILE="$TMP/no-trust"

git init -q --bare "$GITHUB"
git init -q --bare "$GITLAB"
git clone -q "$GITHUB" "$WORK"
git -C "$WORK" config user.email test@example.com
git -C "$WORK" config user.name Test
printf 'one\n' > "$WORK/skills.txt"
git -C "$WORK" add skills.txt
git -C "$WORK" commit -qm initial
git -C "$WORK" branch -M main
git -C "$WORK" remote add gitlab "$GITLAB"
git -C "$WORK" push -q origin main
git -C "$WORK" push -q gitlab main

git clone -q "$GITHUB" "$CLONE"
git -C "$CLONE" checkout -q -B main origin/main

fail() {
    echo "FAIL: $1" >&2
    exit 1
}

head_sha() {
    git -C "$CLONE" rev-parse HEAD
}

echo "case: GitLab ahead"
printf 'two\n' >> "$WORK/skills.txt"
git -C "$WORK" commit -qam "gitlab ahead"
git -C "$WORK" push -q gitlab main
python3 "$SYNC" --folder "$CLONE" >/dev/null
[ "$(head_sha)" = "$(git -C "$WORK" rev-parse HEAD)" ] || fail "GitLab tip was not used"
grep -q two "$CLONE/skills.txt" || fail "GitLab content missing"

echo "case: GitHub ahead"
printf 'three\n' >> "$WORK/skills.txt"
git -C "$WORK" commit -qam "github ahead"
git -C "$WORK" push -q origin main
python3 "$SYNC" --folder "$CLONE" >/dev/null
[ "$(head_sha)" = "$(git -C "$WORK" rev-parse HEAD)" ] || fail "GitHub tip was not used"
grep -q three "$CLONE/skills.txt" || fail "GitHub content missing"

echo "case: identical tips"
python3 "$SYNC" --folder "$CLONE" >/dev/null
[ "$(head_sha)" = "$(git -C "$WORK" rev-parse HEAD)" ] || fail "clone moved unexpectedly"

echo "case: dirty worktree is skipped"
printf 'local\n' >> "$CLONE/skills.txt"
if python3 "$SYNC" --folder "$CLONE" >/dev/null 2>&1; then
    fail "dirty worktree was not rejected"
fi
grep -q local "$CLONE/skills.txt" || fail "local changes were overwritten"
git -C "$CLONE" checkout -q -- skills.txt

echo "case: switch to tested dev"
git -C "$WORK" checkout -q -b dev
printf 'dev\n' >> "$WORK/skills.txt"
git -C "$WORK" commit -qam "dev work"
git -C "$WORK" push -q gitlab dev
git -C "$WORK" checkout -q main
python3 "$SYNC" --folder "$CLONE" --assume-gitlab-dev-passed >/dev/null
[ "$(git -C "$CLONE" rev-parse --abbrev-ref HEAD)" = "dev" ] || fail "clone did not switch to dev"
[ "$(head_sha)" = "$(git -C "$WORK" rev-parse dev)" ] || fail "clone did not reach the dev tip"
grep -q dev "$CLONE/skills.txt" || fail "dev content missing"

echo "all sync tests passed"

#!/bin/sh
# Print the project knowledge stored in git history:
# the latest checkpoint, the commits since it, and the working tree status.
set -eu

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not inside a git repository" >&2
  exit 1
fi

echo "Repository: $(git rev-parse --show-toplevel)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo detached)"

if [ "$(git rev-parse --is-shallow-repository 2>/dev/null || echo false)" = "true" ]; then
  echo "warning: shallow clone, history is incomplete. Run: git fetch --unshallow" >&2
fi

if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "No commits yet. Make the first commit a checkpoint."
  exit 0
fi

cp=$(git log --grep='^checkpoint:' -n 1 --format=%H || true)

if [ -n "$cp" ]; then
  echo
  echo "=== Latest checkpoint ==="
  git log -n 1 --date=short --format='%h  %ad%n%n%B' "$cp"
  echo "=== Commits since checkpoint ($(git rev-list --count "$cp..HEAD")) ==="
  git log --date=short --format='--- %h  %ad  %an%n%B' "$cp..HEAD"
else
  echo
  echo "No checkpoint found. Showing the last 30 commits."
  echo "After you get oriented, add a checkpoint (see references/checkpoint-template.md)."
  echo
  git log -n 30 --date=short --format='--- %h  %ad  %an%n%B'
fi

echo "=== Working tree ==="
git status --short

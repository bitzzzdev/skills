#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$ROOT_DIR/install.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() {
    echo "FAIL: $1" >&2
    exit 1
}

shopt -s nullglob
SKILL_FILES=("$ROOT_DIR"/*/SKILL.md)
EXPECTED="${#SKILL_FILES[@]}"
((EXPECTED > 0)) || fail "no skills found"

HOME="$TMP/dry" "$INSTALL" --dry-run > "$TMP/dry.log"
[[ ! -e "$TMP/dry/.agents/skills" ]] || fail "dry run created a directory"
grep -q 'would link' "$TMP/dry.log" || fail "dry run did not list links"

first_skill="$(basename "$(dirname "${SKILL_FILES[0]}")")"
mkdir -p "$TMP/all/.agents/skills/$first_skill"
printf 'keep me\n' > "$TMP/all/.agents/skills/$first_skill/marker"
mkdir -p "$TMP/all/.claude/skills"
ln -s "$TMP/all/wrong-target" "$TMP/all/.claude/skills/$first_skill"

HOME="$TMP/all" "$INSTALL" > "$TMP/install.log"
for target in "$TMP/all/.agents/skills" "$TMP/all/.claude/skills" "$TMP/all/.kiro/skills"; do
    for skill_file in "${SKILL_FILES[@]}"; do
        skill_dir="$(dirname "$skill_file")"
        skill_name="$(basename "$skill_dir")"
        link="$target/$skill_name"
        [[ -L "$link" && "$link" -ef "$skill_dir" ]] || fail "incorrect link: $link"
    done
done

backup_dir=("$TMP/all/.agents/skills/$first_skill".backup.*)
((${#backup_dir[@]} > 0)) || fail "existing directory was not backed up"
[[ -d "${backup_dir[0]}" ]] || fail "directory backup is missing"
[[ "$(cat "${backup_dir[0]}/marker")" == "keep me" ]] || fail "backup content was not preserved"

backup_link=("$TMP/all/.claude/skills/$first_skill".backup.*)
((${#backup_link[@]} > 0)) || fail "old symlink was not backed up"
[[ -L "${backup_link[0]}" ]] || fail "old symlink backup is missing"

HOME="$TMP/all" "$INSTALL" > "$TMP/repeat.log"
grep -q 'Links created: 0' "$TMP/repeat.log" || fail "repeat install created links"
grep -q 'Existing paths backed up: 0' "$TMP/repeat.log" || fail "repeat install made unnecessary backups"

mkdir -p "$TMP/dry-conflict/.agents/skills/$first_skill"
printf 'preserve\n' > "$TMP/dry-conflict/.agents/skills/$first_skill/marker"
HOME="$TMP/dry-conflict" "$INSTALL" --dry-run > "$TMP/dry-conflict.log"
[[ -d "$TMP/dry-conflict/.agents/skills/$first_skill" ]] || fail "dry-run changed existing directory"
[[ "$(cat "$TMP/dry-conflict/.agents/skills/$first_skill/marker")" == "preserve" ]] || fail "dry-run changed existing content"
grep -q 'would back up' "$TMP/dry-conflict.log" || fail "dry-run did not describe backup"

HOME="$TMP/shared" "$INSTALL" --agent opencode --agent codex > /dev/null
[[ -L "$TMP/shared/.agents/skills/$first_skill" ]] || fail "shared agent path missing"
[[ ! -e "$TMP/shared/.claude/skills" ]] || fail "unselected Claude path created"
[[ ! -e "$TMP/shared/.kiro/skills" ]] || fail "unselected Kiro path created"

if HOME="$TMP/invalid" "$INSTALL" --agent unknown > /dev/null 2>&1; then
    fail "unknown agent was accepted"
fi

HOME="$TMP/list" "$INSTALL" --list-agents > "$TMP/agents.log"
grep -q 'opencode, codex, cursor, gemini, copilot' "$TMP/agents.log" || fail "shared agent list missing"

bash -n "$INSTALL" "$ROOT_DIR/shell/test_install.sh"
echo "all installer tests passed ($EXPECTED skills)"

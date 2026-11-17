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

HOME="$TMP/all" "$INSTALL" > "$TMP/install.log"
for target in "$TMP/all/.agents/skills" "$TMP/all/.claude/skills" "$TMP/all/.kiro/skills"; do
    for skill_file in "${SKILL_FILES[@]}"; do
        skill_dir="$(dirname "$skill_file")"
        skill_name="$(basename "$skill_dir")"
        link="$target/$skill_name"
        [[ -L "$link" && "$link" -ef "$skill_dir" ]] || fail "incorrect link: $link"
    done
done

HOME="$TMP/all" "$INSTALL" > "$TMP/repeat.log"
grep -q 'Links created: 0' "$TMP/repeat.log" || fail "repeat install created links"
expected_links=$((EXPECTED * 3))
grep -q "Links already correct: $expected_links" "$TMP/repeat.log" || fail "repeat install was not idempotent"

HOME="$TMP/shared" "$INSTALL" --agent opencode --agent codex > /dev/null
[[ -d "$TMP/shared/.agents/skills" ]] || fail "shared agent path missing"
[[ ! -e "$TMP/shared/.claude/skills" ]] || fail "unselected Claude path created"
[[ ! -e "$TMP/shared/.kiro/skills" ]] || fail "unselected Kiro path created"

first_skill="$(basename "$(dirname "${SKILL_FILES[0]}")")"
mkdir -p "$TMP/conflict/.agents/skills/$first_skill"
printf 'keep\n' > "$TMP/conflict/.agents/skills/$first_skill/marker"
if HOME="$TMP/conflict" "$INSTALL" > /dev/null 2>&1; then
    fail "existing path conflict did not return failure"
fi
[[ "$(cat "$TMP/conflict/.agents/skills/$first_skill/marker")" == "keep" ]] || fail "existing content was changed"

if HOME="$TMP/invalid" "$INSTALL" --agent unknown > /dev/null 2>&1; then
    fail "unknown agent was accepted"
fi

HOME="$TMP/list" "$INSTALL" --list-agents > "$TMP/agents.log"
grep -q 'opencode, codex, cursor, gemini, copilot' "$TMP/agents.log" || fail "shared agent list missing"

bash -n "$INSTALL" "$ROOT_DIR/shell/test_install.sh"
echo "all installer tests passed ($EXPECTED skills)"

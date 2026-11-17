#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME:?HOME must be set}"
DRY_RUN=0
LIST_AGENTS=0
EXPLICIT_AGENTS=0
AGENTS=()
TARGETS=()
WARNINGS=0
INSTALLED=0
UNCHANGED=0

usage() {
    cat <<'USAGE'
Usage: ./install.sh [options]

Link every skill directory in this repository into supported agent skill roots.

Options:
  --agent NAME  Select an agent (repeatable). Default: all
  --dry-run     Show planned links without changing files
  --list-agents Show supported agents and their skill directories
  -h, --help    Show this help

Agents:
  opencode, codex, cursor, gemini, copilot, claude, kiro
USAGE
}

list_agents() {
    printf '%s\n' \
        'opencode, codex, cursor, gemini, copilot: ~/.agents/skills' \
        'claude: ~/.claude/skills' \
        'kiro: ~/.kiro/skills'
}

while (($#)); do
    case "$1" in
        --dry-run) DRY_RUN=1; shift ;;
        --list-agents) LIST_AGENTS=1; shift ;;
        --agent)
            if (($# < 2)); then
                echo "--agent requires a name" >&2
                exit 2
            fi
            EXPLICIT_AGENTS=1
            AGENTS+=("$2")
            shift 2
            ;;
        --agent=*)
            EXPLICIT_AGENTS=1
            AGENTS+=("${1#*=}")
            shift
            ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
    esac
done

if ((LIST_AGENTS)); then
    list_agents
    exit 0
fi

if ((!EXPLICIT_AGENTS)); then
    AGENTS=(opencode codex cursor gemini copilot claude kiro)
fi

add_target() {
    local candidate="$1"
    local existing
    for existing in "${TARGETS[@]}"; do
        if [[ "$existing" == "$candidate" ]]; then
            return 0
        fi
    done
    TARGETS+=("$candidate")
}

for agent in "${AGENTS[@]}"; do
    case "$agent" in
        all)
            add_target "$HOME_DIR/.agents/skills"
            add_target "$HOME_DIR/.claude/skills"
            add_target "$HOME_DIR/.kiro/skills"
            ;;
        shared|opencode|codex|cursor|gemini|gemini-cli|copilot|copilot-cli|github-copilot)
            add_target "$HOME_DIR/.agents/skills"
            ;;
        claude|claude-code)
            add_target "$HOME_DIR/.claude/skills"
            ;;
        kiro)
            add_target "$HOME_DIR/.kiro/skills"
            ;;
        *)
            echo "Unsupported agent: $agent" >&2
            echo "Run ./install.sh --list-agents to see supported agents." >&2
            exit 2
            ;;
    esac
done

shopt -s nullglob
SKILL_FILES=("$ROOT_DIR"/*/SKILL.md)
if (("${#SKILL_FILES[@]}" == 0)); then
    echo "No top-level skill folders containing SKILL.md were found in $ROOT_DIR" >&2
    exit 1
fi

for target in "${TARGETS[@]}"; do
    for skill_file in "${SKILL_FILES[@]}"; do
        skill_dir="$(dirname "$skill_file")"
        skill_name="$(basename "$skill_dir")"
        link="$target/$skill_name"

        if [[ -L "$link" ]] && [[ "$link" -ef "$skill_dir" ]]; then
            printf 'unchanged %s -> %s\n' "$link" "$skill_dir"
            ((UNCHANGED += 1))
            continue
        fi

        if [[ -e "$link" || -L "$link" ]]; then
            printf 'conflict: keeping existing path %s\n' "$link" >&2
            ((WARNINGS += 1))
            continue
        fi

        if ((DRY_RUN)); then
            printf 'would link %s -> %s\n' "$link" "$skill_dir"
            continue
        fi

        mkdir -p "$target"
        if ln -s "$skill_dir" "$link"; then
            printf 'linked %s -> %s\n' "$link" "$skill_dir"
            ((INSTALLED += 1))
        else
            printf 'conflict: could not create %s\n' "$link" >&2
            ((WARNINGS += 1))
        fi
    done
done

printf '\nSkills found: %d\n' "${#SKILL_FILES[@]}"
printf 'Links created: %d\n' "$INSTALLED"
printf 'Links already correct: %d\n' "$UNCHANGED"
printf 'Conflicts: %d\n' "$WARNINGS"

if ((WARNINGS)); then
    echo "Some skills were not linked. Existing paths were left untouched." >&2
    exit 1
fi

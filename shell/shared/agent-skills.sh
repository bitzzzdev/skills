# Shared shell integration for bitzzdev/skills.
# Source this file from bash or zsh. It defines functions and aliases that call
# the smart sync script installed by shell/install.sh.

_agent_skills_sync_script() {
    if [ -n "${AGENT_SKILLS_SYNC:-}" ] && [ -f "$AGENT_SKILLS_SYNC" ]; then
        printf '%s\n' "$AGENT_SKILLS_SYNC"
        return 0
    fi

    for candidate in \
        "$HOME/.agents/skills/scripts/sync_skills.py" \
        "$HOME/.claude/skills/scripts/sync_skills.py" \
        "${AGENT_SKILLS_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills}/sync_skills.py"
    do
        if [ -f "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

pull_agent_skills() {
    script="$(_agent_skills_sync_script)" || {
        echo "Skills sync script not found. Run shell/install.sh from the skills repository." >&2
        return 1
    }
    python3 "$script" --all "$@"
}

clone_agent_skills() {
    script="$(_agent_skills_sync_script)" || {
        echo "Skills sync script not found. Run shell/install.sh from the skills repository." >&2
        return 1
    }
    python3 "$script" --clone "$@"
}

skill() {
    case "${1:-}" in
        -p|--pull)
            shift
            pull_agent_skills "$@"
            ;;
        -c|--clone)
            shift
            clone_agent_skills "$@"
            ;;
        *)
            echo "Usage: skill -c  (clone repositories)"
            echo "       skill -p  (pull the newest tested source from GitHub or GitLab)"
            return 1
            ;;
    esac
}

alias skill-pull='pull_agent_skills'
alias skill-clone='clone_agent_skills'

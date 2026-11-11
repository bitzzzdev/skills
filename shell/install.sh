#!/usr/bin/env bash
# Install the smart skills sync helpers for fish, bash, and zsh.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="${AGENT_SKILLS_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills}"
FISH_DIR="$HOME/.config/fish/functions"
DRY_RUN=0
INSTALL_FISH=1
INSTALL_RC=1

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --no-fish) INSTALL_FISH=0 ;;
        --no-rc) INSTALL_RC=0 ;;
        -h|--help)
            cat <<'EOF'
Usage: shell/install.sh [options]

Options:
  --dry-run   Show what would be installed without changing files
  --no-fish   Skip fish function installation
  --no-rc     Skip ~/.bashrc and ~/.zshrc updates
  -h, --help  Show this help
EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $arg" >&2
            exit 1
            ;;
    esac
done

copy_file() {
    src="$1"
    dst="$2"
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "would install $src -> $dst"
        return
    fi
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "installed $dst"
}

append_rc_block() {
    rc_file="$1"
    source_line="$2"
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "would source $source_line in $rc_file"
        return
    fi
    mkdir -p "$(dirname "$rc_file")"
    touch "$rc_file"
    tmp="$(mktemp)"
    awk '
        /^# >>> agent-skills >>>$/ { skip = 1; next }
        /^# <<< agent-skills <<<$/ { skip = 0; next }
        !skip { print }
    ' "$rc_file" > "$tmp"
    cat "$tmp" > "$rc_file"
    rm -f "$tmp"
    {
        printf '\n# >>> agent-skills >>>\n'
        printf '%s\n' "$source_line"
        printf '# <<< agent-skills <<<\n'
    } >> "$rc_file"
    echo "updated $rc_file"
}

copy_file "$REPO_ROOT/scripts/sync_skills.py" "$DATA_DIR/sync_skills.py"
copy_file "$REPO_ROOT/shell/shared/agent-skills.sh" "$DATA_DIR/agent-skills.sh"
copy_file "$REPO_ROOT/shell/bash/agent-skills.sh" "$DATA_DIR/bash/agent-skills.sh"
copy_file "$REPO_ROOT/shell/zsh/agent-skills.zsh" "$DATA_DIR/zsh/agent-skills.zsh"

if [ "$INSTALL_FISH" -eq 1 ] && { command -v fish >/dev/null 2>&1 || [ -d "$HOME/.config/fish" ]; }; then
    for file in "$REPO_ROOT"/shell/fish/functions/*.fish; do
        copy_file "$file" "$FISH_DIR/$(basename "$file")"
    done
fi

if [ "$INSTALL_RC" -eq 1 ]; then
    if command -v bash >/dev/null 2>&1; then
        append_rc_block "$HOME/.bashrc" ". \"$DATA_DIR/bash/agent-skills.sh\""
    fi
    if command -v zsh >/dev/null 2>&1; then
        append_rc_block "$HOME/.zshrc" ". \"$DATA_DIR/zsh/agent-skills.zsh\""
    fi
fi

if [ "$DRY_RUN" -eq 0 ]; then
    echo
    echo "Open a new shell or run:"
    echo "  source \"$DATA_DIR/bash/agent-skills.sh\"   # bash"
    echo "  source \"$DATA_DIR/zsh/agent-skills.zsh\"    # zsh"
    echo "  fish -c 'pull_agent_skills'                # fish"
fi

# Zsh integration for bitzzdev/skills.
# Source this file from ~/.zshrc after running shell/install.sh.

AGENT_SKILLS_HOME="${AGENT_SKILLS_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills}"

if [ -f "$AGENT_SKILLS_HOME/agent-skills.sh" ]; then
    . "$AGENT_SKILLS_HOME/agent-skills.sh"
fi

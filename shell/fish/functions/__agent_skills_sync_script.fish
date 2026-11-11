function __agent_skills_sync_script --description 'Locate the smart skills sync script'
    if set -q AGENT_SKILLS_SYNC; and test -f "$AGENT_SKILLS_SYNC"
        echo $AGENT_SKILLS_SYNC
        return 0
    end

    for candidate in \
        "$HOME/.agents/skills/scripts/sync_skills.py" \
        "$HOME/.claude/skills/scripts/sync_skills.py" \
        "$HOME/.local/share/agent-skills/sync_skills.py"
        if test -f "$candidate"
            echo $candidate
            return 0
        end
    end

    return 1
end

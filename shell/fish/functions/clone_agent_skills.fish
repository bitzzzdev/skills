function clone_agent_skills --description 'Clone bitzzdev/skills into every known agent skills folder'
    set -l script (__agent_skills_sync_script)
    if test -z "$script"
        echo "Skills sync script not found. Run shell/install.sh from the skills repository."
        return 1
    end

    python3 $script --clone
end

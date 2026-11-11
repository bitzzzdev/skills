function pull_agent_skills --description 'Sync all agent skills folders from the newest verified GitHub or GitLab source'
    set -l script (__agent_skills_sync_script)
    if test -z "$script"
        echo "Skills sync script not found. Run shell/install.sh from the skills repository."
        return 1
    end

    python3 $script --all
end

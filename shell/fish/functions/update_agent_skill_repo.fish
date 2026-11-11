function update_agent_skill_repo --description 'Sync one skills clone from the newest verified GitHub or GitLab source'
    set -l script (__agent_skills_sync_script)
    if test -z "$script"
        echo "Skills sync script not found. Run shell/install.sh from the skills repository."
        return 1
    end

    python3 $script --folder $argv[1]
end

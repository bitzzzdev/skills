function skill --description 'Manage agent skills sync (use -c to clone, -p to pull tested updates)'
    set -l options 'c/clone' 'p/pull'
    argparse $options -- $argv
    or return 1

    set -l script (__agent_skills_sync_script)
    if test -z "$script"
        echo "Skills sync script not found. Run shell/install.sh from the skills repository."
        return 1
    end

    if set -q _flag_clone
        python3 $script --clone
        return $status
    end

    if set -q _flag_pull
        python3 $script --all
        return $status
    end

    echo "Error: supply a valid operation flag."
    echo "Usage: skill -c  (clone repositories)"
    echo "       skill -p  (pull the newest tested source from GitHub or GitLab)"
    return 1
end

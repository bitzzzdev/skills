# Smart skills sync for every shell

These helpers keep every installed copy of `bitzzdev/skills` current. The sync
script fetches GitHub and GitLab, checks CI evidence for the dev branch, and
updates from the newest source that is verified. When GitHub Actions is
unavailable and the GitLab dev pipeline passed, it switches the clone to the
tested dev branch instead of leaving it on a stale main.

## Install

From the skills repository:

```bash
shell/install.sh
```

The installer copies the sync script and shell helpers into
`${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/`, installs the fish
functions into `~/.config/fish/functions/`, and adds a managed source block to
`~/.bashrc` and `~/.zshrc`.

Options:

```bash
shell/install.sh --dry-run
shell/install.sh --no-fish
shell/install.sh --no-rc
```

## Commands

Fish:

```fish
skill -p
pull_agent_skills
update_agent_skill_repo ~/.agents/skills
skill -c
```

Bash and zsh:

```bash
skill -p
pull_agent_skills
skill-pull
skill -c
```

`skill -p` and `pull_agent_skills` sync every known skills folder. `skill -c`
and `clone_agent_skills` clone missing folders from GitHub and add the GitLab
remote.

## CI verification

GitHub CI is checked with the `gh` CLI. GitLab CI is checked with the GitLab
API when a token is available:

```bash
export GITLAB_TOKEN=your_read_api_token
```

Without a token, the sync still updates from the newest dev commit, but reports
GitLab CI as unverified. After you confirm a GitLab dev pipeline passed in the
web UI, you can trust it locally:

```bash
mkdir -p ~/.config/agent-skills
touch ~/.config/agent-skills/trust-gitlab-dev
```

Remove that marker when you want the script to require a token again.

## Branch switching

The sync will switch a clone between `main` and `dev` only when:

- The working tree is clean.
- The selected branch has passing CI evidence.
- The clone is behind the selected commit.

It never resets or discards local commits. A dirty clone or a diverged branch is
reported and skipped.

## Paths

- Sync script: `scripts/sync_skills.py`
- Fish functions: `shell/fish/functions/`
- Shared shell helpers: `shell/shared/agent-skills.sh`
- Bash entry point: `shell/bash/agent-skills.sh`
- Zsh entry point: `shell/zsh/agent-skills.zsh`
- Installed data: `${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/`

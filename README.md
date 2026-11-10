# skills

A collection of agent skills for Antigravity, Gemini CLI, Claude Code, OpenCode, and Claude.ai. Each skill is a self-contained folder with a `SKILL.md` and reference files that load only when the agent needs them.

## Skills

| Skill | What it does |
|---|---|
| [`android-app-dev`](android-app-dev) | Builds, edits, and debugs native Android apps in Kotlin or Java, with Jetpack Compose or XML views, Gradle setup, and GitHub Actions CI builds. |
| [`context-rich-commits`](context-rich-commits) | Turns git history into project memory. Commit messages record why, what changed, decisions, and gotchas; checkpoint commits snapshot the repository state. Includes a commit linter and history reader. |
| [`credential-safety`](credential-safety) | Checks worktree files, commit ranges, ignore rules, and scanner results so credentials do not reach remote repositories. |
| [`deep-research`](deep-research) | Investigates source and target repositories before copying or porting a feature, tracing behavior, integration points, licensing, and validation. |
| [`debug-and-fix`](debug-and-fix) | Finds and fixes bugs end-to-end. Reproduces the error, searches affected files, checks full logs, reads official documentation, fixes root causes, and verifies. Includes error context extraction scripts. |
| [`error-docs-lookup`](error-docs-lookup) | Directs the agent to read current official documentation, changelogs, and GitHub issues before fixing build, type, lint, install, or runtime errors instead of guessing from memory. |
| [`google-seo-skill`](google-seo-skill) | Applies official Google SEO and generative AI search (AEO/GEO) guidance when writing, reviewing, or auditing web pages. Used for public web projects needing search ranking; avoided for personal or internal projects where indexing is not needed. |
| [`human-writing`](human-writing) | Keeps written output sounding human. Enforces project owner authority, bans assistant meta-instructions, bans em dashes and emoji, eliminates stock AI phrasing, and covers code comments, commit messages, READMEs, UI copy, and technical social posts on X and Reddit. Includes a scanner script. |
| [`iris-shaderpack-dev`](iris-shaderpack-dev) | Creates and debugs Minecraft shaderpacks for Iris and OptiFine, including `shaders.properties`, program files, and common shader effects. |
| [`minecraft-fabric-mod`](minecraft-fabric-mod) | Scaffolds and updates Fabric mods for Minecraft Java Edition, with version-sensitive Gradle, Loom, mapping guidance, and CI workflows. |
| [`persistent-goal-execution`](persistent-goal-execution) | Keeps agents focused on the complete requested outcome across long tasks, retries, waiting, context compaction, and failures. |
| [`production-ready`](production-ready) | Takes a project to a production release. Directs the agent to orchestrate all other relevant skills in its toolkit, audits the repository, generates changelogs and docs, drafts legal files, and conducts a multi-skill refresh pass. Includes an audit script. |
| [`systematic-issue-sweep`](systematic-issue-sweep) | Sweeps the entire workspace to locate, fix, and prevent recurrences of any reported issue, typo, style flaw, or logic error. Eradicates whole defect classes across code, tests, docs, and configs. Includes a sweep script. |
| [`threejs-awwwards-site`](threejs-awwwards-site) | Builds Three.js and WebGL websites with scroll-driven motion, smooth scrolling, and cinematic transitions. |

## Skill Orchestration

The skills work together as an interconnected toolkit:
- When preparing a release, invoke `production-ready`. It acts as the orchestrator, detecting the project type and running `persistent-goal-execution`, `debug-and-fix`, `error-docs-lookup`, `google-seo-skill` (if a public website needing search ranking), `human-writing`, and `context-rich-commits`.
- Before committing or pushing a release, `production-ready` runs
  `credential-safety` to check for exposed credentials and stop unsafe pushes.
- When a release includes a feature copied or ported from another repository,
  `production-ready` runs `deep-research` before accepting the implementation.
- `production-ready` pushes every release to `dev` first and promotes the
  exact commit to production only after its `dev` CI/CD check passes.
- For personal or internal projects where search indexing is not desired, `production-ready` automatically avoids SEO ranking checks and ensures `noindex` or authentication guards are in place.
- `production-ready` verifies the corporate release document suite (terms, privacy, licenses, third-party attribution, security policies, and community standards) while properly handling private projects, user exclusions, and release overrides.
- When an error occurs during any build or test, `debug-and-fix` automatically pairs with `error-docs-lookup` to consult official live documentation before making changes.
- For difficult or multi-step work, `persistent-goal-execution` keeps the full objective, acceptance criteria, current plan, authoritative evidence, and completion state active until the requested end state is proven.
- Every skill includes an update check directing agents to inspect git status in the skill directory (such as `~/.copilot/skills/` or `~/.gemini/antigravity-cli/skills/`) before running, so instructions stay current.
- All documentation, license entries, and comments are authored strictly from the perspective and authority of the project owner, banning assistant coaching leaks, meta-instructions, and unselected license checklists.
- When any defect, typo, or user-pointed inconvenience is identified, `production-ready` and `debug-and-fix` invoke `systematic-issue-sweep` to search the entire workspace and eradicate all related occurrences across code, docs, tests, and configuration before release.

## Installation

**GitHub Copilot**

Copy the skill folder into your personal Copilot skills directory:

```bash
git clone https://github.com/bitzzdev/skills.git
cp -r skills/google-seo-skill ~/.copilot/skills/
```

Or clone the entire repository directly into `~/.copilot/skills/`.

**Antigravity and Gemini CLI**

Copy the skill folder into your personal skills directory:

```bash
git clone https://github.com/bitzzdev/skills.git
cp -r skills/google-seo-skill ~/.gemini/antigravity-cli/skills/
```

For project-specific skills, place them in `.gemini/skills/` within your project root.

**Claude Code**

Copy the skill folder into your personal skills directory, or into a project:

```bash
cp -r skills/google-seo-skill ~/.claude/skills/
```

For a single project, use `.claude/skills/` inside that project instead.

**OpenCode**

Copy the skill folder into your OpenCode skills directory (such as `~/.config/opencode/skills/`).

**Claude.ai**

Zip the skill folder so `SKILL.md` sits inside a top-level folder named after the skill, rename the archive to `<skill-name>.skill`, and upload it from the skills section of your Claude.ai settings.

## Layout

```
skill-name/
  SKILL.md          required, YAML frontmatter plus instructions
  references/       optional, loaded when the skill points to them
  scripts/          optional, helpers the skill can run
```

The `name` in the frontmatter must match the folder name. A GitHub Action checks this on every push and pull request. You can run the same check locally:

```bash
pip install pyyaml
python scripts/validate_skills.py
```

## Contributing

Fixes and new skills are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

## Support

If these are useful to you, you can support the work on [Ko-fi](https://ko-fi.com/bitzdev).

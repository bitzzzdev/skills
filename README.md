# skills

A collection of agent skills for Claude Code, OpenCode and Claude.ai. Each skill is a folder with a `SKILL.md` and optional reference files that load only when the agent needs them.

## Skills

| Skill | What it does |
|---|---|
| [`android-app-dev`](android-app-dev) | Builds, edits and debugs native Android apps in Kotlin or Java, with Jetpack Compose or XML views, Gradle setup and GitHub Actions builds. |
| [`context-rich-commits`](context-rich-commits) | Turns git history into project memory. Commit messages record why, what changed, decisions and gotchas, and checkpoint commits snapshot the whole codebase so anyone joining later can read the log and get up to speed. Includes a linter and a history reader. |
| [`debug-and-fix`](debug-and-fix) | Finds and fixes bugs end to end. Reproduces the error, searches the files the trace points at, checks the full log for other errors, reads the official docs for the installed version, fixes the root cause and verifies. Includes a script that pulls file locations out of a stack trace. |
| [`error-docs-lookup`](error-docs-lookup) | Makes the agent read current official docs, changelogs and GitHub issues before fixing a build, type, lint, install or runtime error, instead of guessing from memory. |
| [`human-writing`](human-writing) | Keeps written output sounding like a person. Bans em dashes and emoji, cuts common AI phrasing, and covers code comments, commit messages, READMEs and UI copy. Includes a scanner script. |
| [`iris-shaderpack-dev`](iris-shaderpack-dev) | Creates and debugs Minecraft shaderpacks for Iris and OptiFine, including `shaders.properties`, program files and common effects. |
| [`minecraft-fabric-mod`](minecraft-fabric-mod) | Scaffolds and updates Fabric mods for Minecraft Java Edition, with version-sensitive Gradle, Loom and mapping guidance. |
| [`production-ready`](production-ready) | Takes a project to a production finish. Creates or updates the changelog, README and docs, and drafts terms, privacy and project rules from what the code really does. Ends with a refresh pass through the other skills. Includes an audit script. |
| [`threejs-awwwards-site`](threejs-awwwards-site) | Builds Three.js and WebGL sites with scroll-driven motion, smooth scrolling and cinematic transitions. |

## Installation

**Claude Code**

Copy the skill folder into your personal skills directory, or into a project:

```bash
git clone https://github.com/bitzzdev/skills.git
cp -r skills/human-writing ~/.claude/skills/
```

For a single project, use `.claude/skills/` inside that project instead.

**OpenCode**

Copy the skill folder into your OpenCode skills directory. See the OpenCode docs for the current location.

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

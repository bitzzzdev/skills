# Choosing which skills to run

Run a skill only when it fits the project. A skill that does not apply wastes time, adds noise to docs, and can do harm (SEO tags in a native app are clutter; SEO ranking optimization on a private internal tool leaks private routes). Decide from the project type and privacy requirements, then report which skills were used and which were skipped and why.

## Always run the relevance check first

The matrix below is a starting point, not the full list. Before using it, run the mandatory skill relevance check from `SKILL.md`: inventory every available skill, compare each description against the task and project, and read the full `SKILL.md` of every skill that applies. `agent-self-awareness`, `token-optimizer`, and this check run every time. Skills added to the repository after this file was written count as candidates too.

Record the result like this and put it in the final report:

| Skill | Decision | Reason |
|---|---|---|
| agent-self-awareness | USE | Always on, sets the execution mode |
| token-optimizer | USE | Always on, thinking off and steps tracked in `.progress.md` |
| google-seo-skill | SKIP | Internal dashboard, verified noindex instead |
| systematic-issue-sweep | USE | Lint failure found, sweeping for the same pattern |

Repeat the check when the task shifts, a failure repeats, or the model or harness changes.

## Detect the project type and visibility

`scripts/audit.py` guesses the project type and checks whether the repository is private or personal, then prints USE and SKIP recommendations. Confirm by inspecting project files. If it guesses incorrectly, pass `--type`, `--personal`, or `--no-indexing`.

| Type | Signs |
|---|---|
| website | Next, Nuxt, Astro, Gatsby, SvelteKit, Remix, WordPress, static `index.html`, server-rendered templates with public pages |
| mobile-native | `AndroidManifest.xml`, Gradle Android plugin, `.xcodeproj`, `Info.plist`, Flutter `pubspec.yaml`, React Native, Expo |
| desktop | Electron, Tauri, Qt, WPF, a packaged installer |
| game-mod | `fabric.mod.json`, `mods.toml`, plugin manifests for Minecraft, Roblox or similar |
| shaderpack | `shaders/` with `.fsh`, `.vsh` or `.glsl` |
| library-cli | package with no UI, a `bin` entry, `console_scripts`, a Cargo or Go library |
| bot | discord.js, discord.py, Telegraf, Slack Bolt |
| api | Express, Fastify, FastAPI, Flask, Rails or Go server without public pages |

A project can be multiple types: a Tauri app with a marketing site is desktop plus website. Apply website rules only to the marketing site.

## Privacy and indexing status

Before evaluating SEO or ranking skills, determine if the site should be public or private:
- **Public website needing search ranking**: Apply `google-seo-skill` (or `references/seo.md`) to maximize search visibility and meet Google Search Central standards.
- **Personal project, private repo, internal dashboard, staging site, or no indexing needed**: Explicitly avoid `google-seo-skill`. Do not optimize for search ranking. Instead, verify that search engines cannot index the site: ensure `<meta name="robots" content="noindex, nofollow">` or `X-Robots-Tag: noindex, nofollow` headers and robots disallow rules are present.

## Skill orchestration matrix

| Skill or task | website (public) | website (personal/internal) | mobile-native | desktop | game-mod | shaderpack | library-cli | bot | api |
|---|---|---|---|---|---|---|---|---|---|
| changelog | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| context-search | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| parallel-agent-orchestration | when independent work exists | when independent work exists | when independent work exists | when independent work exists | when independent work exists | when independent work exists | when independent work exists | when independent work exists | when independent work exists |
| agent-self-awareness | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| token-optimizer | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| README and docs | yes | yes | yes | yes | yes | yes | yes | yes | yes, plus API reference |
| terms and privacy | yes if users | no | yes, stores require privacy URL | yes if data collected | rarely | no | no | yes | yes if public |
| license, contributing, security | yes | yes if open source | yes if open source | yes if open source | yes | yes | yes | yes | yes |
| google-seo-skill | yes | no, enforce noindex | no, store listing copy | landing page only | no, mod page copy | no | docs site only | no | docs site only |
| accessibility pass | yes | yes | yes | yes | no | no | no | no | no |
| performance budget | yes | optional | startup time and memory | startup time | no | framerate budget | no | latency | latency / throughput |
| debug-and-fix | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| error-docs-lookup | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| human-writing | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| context-rich-commits | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| project-specific skill | threejs-awwwards-site if 3D | threejs-awwwards-site if 3D | android-app-dev for Android | none | minecraft-fabric-mod | iris-shaderpack-dev | none | none | cloud skills if deployed |

## Ponytail skills

The Ponytail skills cover code scope and code quality. They do not replace the
release, security, documentation, or legal checks above.

| Skill | Use it when | Do not use it as |
|---|---|---|
| `ponytail` | Implementing or changing code; keep the solution minimal without dropping required behavior or checks. | A reason to skip tests, validation, security, accessibility, or requested scope. |
| `ponytail-review` | Reviewing the completed code diff before release. | A substitute for running the project's test and build commands. |
| `ponytail-audit` | The task calls for a repository-wide code-quality audit. | A replacement for `production-ready/scripts/audit.py`, which checks release documentation and repository readiness. |
| `ponytail-debt` | The repository has `shortcut:` or legacy `ponytail:` comments, or the user requests a debt ledger. | A general TODO or issue tracker. |
| `ponytail-gain` | The user asks about Ponytail's published benchmark results. | A source of per-project savings estimates or release evidence. |
| `ponytail-help` | The user needs the Ponytail command, level, or companion-skill reference. | A mandatory release check. |

For a code-bearing release, use `ponytail` during implementation and
`ponytail-review` after the final code change. Add the audit and debt skills
only when their stated scope applies. Never report upstream benchmark figures
as measurements from the current project.

## Skill orchestration guidelines

When productionizing a project, orchestrate all relevant skills in sequence:
- **token-optimizer**: Always on. Turn thinking off, read the setting back, and work from the todo list in `.progress.md`: re-read it before each item, update it after each one, and add items as bugs and blockers appear. Research and verification still run, as tool calls and list items.
- **agent-self-awareness**: Detect the active model tier. Non-frontier and unknown models must gather official documentation, code evidence, and tests before implementing. Report the execution mode.
- **context-search**: On a new session in an existing codebase, discover installed agents, locate project sessions, extract a bounded brief, and verify it against git and the current files before resuming work.
- **debug-and-fix**: Verify tests, build, and linters. Fix any breakages at their root cause.
- **error-docs-lookup**: When encountering deprecations, toolchain issues, or version upgrades, look up official documentation before making changes.
- **google-seo-skill**: Invoke for public web projects needing search ranking and AI Overviews visibility. Avoid for personal/internal tools or projects with no indexing needed.
- **human-writing**: Run `human-writing/scripts/scan.py` on all changed files and prose. Ensure zero hard hits and natural tone.
- **context-rich-commits**: Record all updates with structured commits and a final project checkpoint commit.
- **Domain skills (`android-app-dev`, `minecraft-fabric-mod`, `iris-shaderpack-dev`, `threejs-awwwards-site`)**: Use for domain-specific checks and CI verification.

## What replaces SEO outside public web projects

- Mobile and desktop apps: store listing title, short and long description, keywords, screenshots with captions, release notes in the docs folder.
- Personal or internal web projects: verification of `noindex` directives and authenticated access controls.
- Mods and shaderpacks: Modrinth or CurseForge page text, tags, supported versions, install steps.
- Libraries: package registry description, keywords, and repository links.

## Missing skills

If a skill the project calls for is not installed in the environment, perform its checks from the matching reference file (`references/seo.md`, `references/docs.md`, `references/legal-and-rules.md`, `context-search/references/agent-stores.md`, or `agent-self-awareness/references/quality-gates.md`) and note this in the final report. Never claim to have run a skill that was not executed.

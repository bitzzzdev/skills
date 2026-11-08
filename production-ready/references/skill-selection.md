# Choosing which skills to run

Run a skill only when it fits the project. A skill that does not apply wastes time, adds noise to the docs and can do harm (SEO tags in a native app are clutter). Decide from the project type, then say in the report which skills you used and which you skipped and why.

## Detect the project type
`scripts/audit.py` guesses it and prints USE and SKIP lines. Confirm by looking at the files. If it guesses wrong, pass `--type`.

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

A project can be two types. A Tauri app with a marketing site is desktop plus website. Apply the website rules to the site only.

## Matrix

| Skill or task | website | mobile-native | desktop | game-mod | shaderpack | library-cli | bot | api |
|---|---|---|---|---|---|---|---|---|
| changelog | yes | yes | yes | yes | yes | yes | yes | yes |
| README and docs | yes | yes | yes | yes | yes | yes | yes | yes, plus API reference |
| terms and privacy | yes if users | yes, stores require a privacy URL | yes if it collects data | rarely | no | no | yes | yes if public |
| license, contributing, security | yes | yes if open source | yes if open source | yes | yes | yes | yes | yes |
| SEO (`references/seo.md`) | yes | no, use store listing text instead | landing page only | no, use the mod page text | no | docs site only | no | docs site only |
| accessibility pass | yes | yes | yes | no | no | no | no | no |
| performance budget (Core Web Vitals) | yes | no, use startup time and size | no | no | no | no | no | no |
| debug-and-fix | yes | yes | yes | yes | yes | yes | yes | yes |
| error-docs-lookup | yes | yes | yes | yes | yes | yes | yes | yes |
| human-writing | yes | yes | yes | yes | yes | yes | yes | yes |
| context-rich-commits | yes | yes | yes | yes | yes | yes | yes | yes |
| project-specific skill (see below) | threejs-awwwards-site if 3D | android-app-dev for Android | none | minecraft-fabric-mod | iris-shaderpack-dev | none | none | none |

## Project-specific skills
Use the one skill built for the project when the type matches and it is installed: `android-app-dev`, `minecraft-fabric-mod`, `iris-shaderpack-dev`, `threejs-awwwards-site`. Use them for fixes and checks during the release, not to add features.

## What replaces SEO outside the web
- Mobile and desktop apps: store listing title, short and long description, keywords field, screenshots with captions, release notes. Write them in the docs folder so they are versioned.
- Mods and shaderpacks: the Modrinth or CurseForge page text, tags, supported versions, install steps.
- Libraries: package registry description, keywords and links.

## Missing skills
If a skill the type calls for is not installed, do its job from the matching reference file and note it in the report. If no reference exists, skip it and say so. Never pretend to have run a skill you did not run.

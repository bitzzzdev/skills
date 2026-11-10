---
name: production-ready
description: Orchestrates a complete production-level finish by directing the agent to use all other relevant skills in its toolkit (persistent-goal-execution, credential-safety, deep-research, debug-and-fix, error-docs-lookup, human-writing, context-rich-commits, google-seo-skill, and domain-specific skills), auditing the repository, updating changelogs, READMEs, documentation, legal files, and community standards. Use whenever the user asks to get a project production-ready, ship it, prepare a release, finish up, or review what is missing before launch.
---

# Production Ready

A project is not finished when the code works. It is finished when someone else can install it, understand it, trust it, and see what changed. This skill directs the agent to orchestrate all other relevant skills in its toolkit to bring the codebase to a production-level release: changelog, documentation, terms and rules, followed by a multi-skill refresh pass that reruns tests, looks up errors in official documentation, evaluates search indexing, verifies writing style, and commits with full context.

Work on what the project actually has. Read the code and git history first, write second. Never invent features, versions, dates, company names, addresses, or legal facts. If a fact is unknown, leave a clearly marked placeholder like `[COMPANY NAME]` and list it in the final report.

## Check for skill folder updates

Before applying this skill, check whether the skill folder has updates:

1. Identify the directory where this skill is installed (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, or the active repository).
2. If the folder is inside a git repository, check git status:
   ```bash
   git -C <skill-folder> status --short --branch
   ```
3. When network access is available, check for upstream changes:
   ```bash
   git -C <skill-folder> fetch --dry-run
   ```
4. If updates are available, pull them before proceeding so you use the latest instructions. If the folder is not a git repository, proceed with the installed files.

## Multi-Skill Orchestration

When finishing a project, you act as the orchestrator across your entire skill ecosystem. Do not treat production readiness as simply editing markdown files. Proactively invoke and apply the other skills available in your environment when their criteria are met:

0. **Skill folder update check**: Inspect git status in active skill folders (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, or the project skills directory) with `git -C <skill-folder> status --short --branch` or `python scripts/check_skill_update.py`. Pull pending updates before running release audits.

1. **persistent-goal-execution**: Keep the complete release objective, acceptance criteria, current plan, authoritative evidence, and completion state active across context compaction, retries, waits, and failures. Do not declare the release complete until every requirement is verified.
2. **credential-safety**: Check worktree files, staged changes, pushed commit ranges, ignore rules, and available secret-scanner results before committing or pushing. Stop, rotate, and remediate any exposed credential without printing its value.
3. **deep-research and third-party attribution**: When a release includes a feature copied, ported, or adapted from another repository, inspect the source and target context, verify licensing, trace behavior, and document intentional differences before implementation. Audit third-party packages, bundled code, fonts, and assets to provide licensing attribution in `CREDITS.md` or `NOTICE`.
4. **debug-and-fix**: Run the project build, tests, and linters. Fix any failures at their root cause. A release with a red build is not production ready.
5. **error-docs-lookup**: When encountering library deprecations, build tool warnings, or version migrations, search and read current official documentation before applying fixes.
6. **google-seo-skill**:
   - **Pull updates first**: If any update to `google-seo-skill` is available in git (upstream `https://github.com/mikezupper/google-seo-skill`), pull it first using `python scripts/update_seo_skill.py`. Verify clean frontmatter and human writing, then push updates to the skills repo.
   - **Use when**: Working on a public web project where search ranking and public search engine visibility are needed. Use it to audit crawlability, metadata, structured data, canonical URLs, and Core Web Vitals.
   - **Avoid when**: Working on a personal project, private repository, internal dashboard, staging site, or any project where search indexing is not desired. In those cases, skip SEO ranking checks entirely and verify that `noindex` meta tags, `X-Robots-Tag: noindex` headers, or robots disallow rules are present to prevent indexing.
7. **human-writing**: Scan all written or edited text (README, changelog, documentation, legal text, commit messages, and code comments) with `human-writing/scripts/scan.py`. Enforce zero hard hits (no em dashes, no emoji) and clear, human tone.
8. **context-rich-commits**: Record the release work using structured git commits (separating doc updates from legal text and code changes), followed by a project checkpoint commit. Push committed releases to the repo when instructed.
9. **Domain-specific skills**:
   - `android-app-dev`: Use for Android apps to verify the CI workflow, Gradle version catalog, and Compose configuration.
   - `minecraft-fabric-mod`: Use for Minecraft Fabric mods to verify Loom, Fabric API, and CI build workflows.
   - `iris-shaderpack-dev`: Use for shaderpacks to verify program names and shaders.properties.
   - `threejs-awwwards-site`: Use for WebGL and 3D websites to verify performance budgets and mobile fallbacks.
   - Google Cloud skills (such as `gcloud`, `google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`): Use when configuring or deploying services to Google Cloud Platform.

## Workflow

### 1. Audit
Run the audit script from the project root. It inspects the codebase, checks for missing, stale, or excluded files, verifies skill folder git status, and lists which skills to USE and which to SKIP:

```bash
python scripts/audit.py <project-root>
```

For personal, internal, or private repositories where consumer legal documents and public search indexing should be avoided:

```bash
python scripts/audit.py <project-root> --personal
```

When an explicit user override requests full corporate release documentation for an internal or private project:

```bash
python scripts/audit.py <project-root> --force-release
```

When the user explicitly opts out of legal documents:

```bash
python scripts/audit.py <project-root> --skip-legal
```

The script reports items organized into clear categories:
- **REQUIRED**: Essential documents and configurations missing for release.
- **RECOMMENDED**: Advisory best-practice files missing for release.
- **OPTIONAL**: Documents omitted because they do not apply to this project type or mode.
- **USER-EXCLUDED**: Documents omitted by explicit user decision.
- **STALE**: Existing files that are outdated or contain broken references.
- **OK**: Verified files that are present and up to date.
- **INFO**: Project scope, branch tracking, and git metadata.

### 2. Changelog
Create or update `CHANGELOG.md` following `references/changelog.md`. Source entries from `git log` since the last release tag and from the git diff, not from memory. Write for users: what they can now do or what behaves differently, not an internal list of moved files. Group under Added, Changed, Fixed, Removed, Security. Keep an `Unreleased` section at the top until a version release is cut.

### 3. Docs and README
Create or update the README and anything under `docs/`. Follow the checklist in `references/docs.md`. The standard: a newcomer can go from cloning to running in a few minutes using only the README. Always write as the project owner, never as an external assistant. Never leave assistant coaching, multiple-choice options, or reminders in README or docs (such as "The license is not selected yet. Choose one before publishing: ...").

Run every install and execution command you document. A command you did not run is an unverified guess, so either run it or mark it unverified. Update docs for every behavior mentioned in the changelog, and remove docs for removed features.

### 4. Terms, privacy, and community rules
Review `references/legal-and-rules.md` for complete outlines, codebase audit checklists, and decision trees covering the full corporate release suite:

1. **Terms of Service (`TERMS.md` or `TERMS_OF_SERVICE.md`)**: Covers eligibility, user accounts, acceptable use, user-generated content, intellectual property, third-party integrations, disclaimer of warranties, liability limits, termination, governing law, and dispute resolution.
2. **Privacy Policy (`PRIVACY.md`)**: Audits the real codebase for data collection (cookies, localStorage, session tokens, analytics, crash reporters, third-party APIs, authentication providers). Details data retention, user rights (GDPR/CCPA access and deletion), international transfers, and privacy contact information.
3. **License (`LICENSE`)**: Verifies an explicit license exists (MIT, Apache-2.0, GPL-3.0, BSD, or proprietary Commercial All Rights Reserved). Never guesses or changes an existing license without explicit authorization. If no license exists, ask the user in chat or write clean owner terms (`Copyright (c) [YEAR] [OWNER]. All rights reserved.`). Never commit assistant options lists or coaching instructions into the repository.
4. **Third-Party Credits and Attribution (`CREDITS.md` or `NOTICE`)**: Details third-party dependencies, open-source packages, fonts, media assets, and external APIs used by the project, including required copyright and license notices.
5. **Security Policy (`SECURITY.md`)**: Defines supported versions, private vulnerability reporting process, response timelines (SLA), security contact address, and safe harbor / responsible disclosure expectations.
6. **Contributing Guidelines (`CONTRIBUTING.md`)**: Explains local setup, branching rules, testing expectations, pull request workflows, and code review standards.
7. **Code of Conduct (`CODE_OF_CONDUCT.md`)**: Community and contributor standards based on established industry templates (such as Contributor Covenant 2.1).
8. **Changelog (`CHANGELOG.md`)**: Chronological release notes adhering strictly to Keep a Changelog and Semantic Versioning.
9. **Environment Template (`.env.example`)**: Documents all required environment variables without committing actual secrets.

Smart conditional rules for private projects and user preferences:
- **Private and internal projects**: The audit script automatically detects private projects from `package.json` (`"private": true`), `pyproject.toml`, or internal markers. By default, skip public-facing consumer terms, public privacy policies, and public community files. Focus on code quality, build verification, tests, credential safety, changelog, `.env.example`, internal README, and proprietary license notices.
- **Explicit user override (`--force-release`)**: If the user explicitly asks to make a private project production-ready, or requests release documents, generate the full corporate suite tailored for commercial/internal software (commercial terms, internal security policy, third-party attribution notices, proprietary license).
- **User opt-out / denial**: If the user denies or opts out of any legal file (such as "skip terms", "no license needed", "don't add privacy policy", or passes `--skip-legal`), immediately honor the decision, skip generation, and document the omission in the audit report as user-excluded rather than missing.

State plainly in the report that generated terms and privacy text are starting drafts that need legal review before launch. Do not claim legal compliance.

### 5. Skill selection and routing
Read `references/skill-selection.md` and confirm the project type from the audit output:
- **Web project needing search ranking**: USE `google-seo-skill` (or `references/seo.md`).
- **Personal web project, internal tool, staging site, or no indexing desired**: SKIP `google-seo-skill`. Verify that `noindex` tags or robots disallow rules protect the site from search crawlers.
- **Native mobile, desktop, mod, shaderpack, bot, or library**: SKIP SEO skills. Prepare store listing copy, mod registry text, or package metadata instead.
- **Domain skills**: If `android-app-dev`, `minecraft-fabric-mod`, `iris-shaderpack-dev`, or `threejs-awwwards-site` apply and are installed, invoke them for domain-specific checks and verification.

### 6. Multi-skill refresh pass
Run the applicable skills in this sequence:

0. **Skill folder update check**: Inspect git status in the skills folder (`python scripts/check_skill_update.py` or `git -C <skill-folder> status --short --branch`) to verify installed skills are up to date before running the refresh pass.
1. **persistent-goal-execution**: Preserve the full production objective through the refresh pass and verify every requirement before reporting completion.
2. **credential-safety**: Check for credentials before committing or pushing. Stop and remediate findings, rotate exposed values, and do not expose secret contents in reports.
3. **deep-research and attribution**: If the release includes copied or ported functionality, verify source behavior, licensing, target integration, and intentional differences before accepting the implementation. Verify that `CREDITS.md` or `NOTICE` documents all third-party dependencies and asset licenses.
4. **debug-and-fix**: Run the project's build, test, and lint commands. Fix any failures at their root cause.
5. **error-docs-lookup**: For any warning, deprecation, or error involving a library or toolchain, look up official documentation for the installed version.
6. **Domain skill checks**: Run specific checks (for example, verifying CI workflows in `android-app-dev` or `minecraft-fabric-mod`).
7. **Search indexing and SEO check**:
   - If using `google-seo-skill`, first check if any update is available in git (`python scripts/update_seo_skill.py`) and pull it.
   - For public websites where ranking is needed: run `google-seo-skill` (or `references/seo.md`).
   - For personal or internal projects: verify that `noindex` headers or meta tags and robots rules are correctly in place.
8. **human-writing**: Run `human-writing/scripts/scan.py` on every touched file (README, changelog, docs, terms, comments). Eliminate all hard hits (no em dashes, no emoji).
9. **Audit rerun**: Rerun `scripts/audit.py`. Confirm zero remaining MISSING or STALE items.
10. **context-rich-commits and push**: Commit the changes using structured commit messages:
   - One commit for docs and changelog.
   - One commit for legal and community files.
   - A final checkpoint commit capturing the current state of the repository.
   - Always create or use a `dev` branch and push the current work there
     without waiting for user confirmation, whether the implementation is
     incomplete or complete. Verify the remote state and report what remains
     unfinished when applicable.
   - After the `dev` push succeeds, wait for the CI/CD workflow for that exact
     commit. If the workflow passes, push that same verified commit to the
     production branch without asking for confirmation. If CI/CD fails, is
     unavailable, or does not cover the full change, do not push to production.
     Report the failure or missing evidence and continue remediation.
   - If no `dev` branch exists, create it before waiting for CI/CD. A
     production push is never allowed without a successful `dev` check for
     the exact commit.
   - A final checkpoint commit capturing the current state of the repository.

### 7. Report
Provide a concise, factual summary:
- Files created or updated.
- User-excluded documents if legal files were omitted by user decision.
- Placeholders the user must fill in ([COMPANY NAME], [CONTACT EMAIL], [JURISDICTION], [SECURITY EMAIL], [EFFECTIVE DATE]).
- Skills used and skills skipped, each with a brief reason.
- Search indexing status: confirmed public indexing checklist or verified personal/internal `noindex` protections.
- Commands run and verification results (mark anything unverified as "not verified").
- Open observations (such as missing test suites or upstream dependencies).
- Legal review reminder if terms or privacy policies were drafted.

## Rules that keep this honest

- Write as the project owner: All documentation, README entries, comments, and licenses must speak with the direct voice and authority of the repository creator or maintainer. Never include assistant meta-instructions, advice to the developer, or multiple-choice checklists in committed deliverables.
- Version numbers and dates come from the manifest, tags, and git, never from guesses. Use today's system date for release headings.
- Do not bump the version or tag a release unless the user asked. Put changes under `Unreleased` otherwise.
- Do not delete existing legal text. Extend or flag it.
- Never put secrets, tokens, or personal emails found in the repository into public docs.
- Match existing project voice, formatting, and file layout before applying templates.

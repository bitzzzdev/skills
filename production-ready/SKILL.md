---
name: production-ready
description: Orchestrates a complete production-level finish by directing the agent to use all other relevant skills in its toolkit (persistent-goal-execution, credential-safety, debug-and-fix, error-docs-lookup, human-writing, context-rich-commits, google-seo-skill, and domain-specific skills), auditing the repository, updating changelogs, READMEs, documentation, legal files, and community standards. Use whenever the user asks to get a project production-ready, ship it, prepare a release, finish up, or review what is missing before launch.
---

# Production Ready

A project is not finished when the code works. It is finished when someone else can install it, understand it, trust it, and see what changed. This skill directs the agent to orchestrate all other relevant skills in its toolkit to bring the codebase to a production-level release: changelog, documentation, terms and rules, followed by a multi-skill refresh pass that reruns tests, looks up errors in official documentation, evaluates search indexing, verifies writing style, and commits with full context.

Work on what the project actually has. Read the code and git history first, write second. Never invent features, versions, dates, company names, addresses, or legal facts. If a fact is unknown, leave a clearly marked placeholder like `[COMPANY NAME]` and list it in the final report.

## Multi-Skill Orchestration

When finishing a project, you act as the orchestrator across your entire skill ecosystem. Do not treat production readiness as simply editing markdown files. Proactively invoke and apply the other skills available in your environment when their criteria are met:

1. **persistent-goal-execution**: Keep the complete release objective, acceptance criteria, current plan, authoritative evidence, and completion state active across context compaction, retries, waits, and failures. Do not declare the release complete until every requirement is verified.
2. **credential-safety**: Check worktree files, staged changes, pushed commit ranges, ignore rules, and available secret-scanner results before committing or pushing. Stop, rotate, and remediate any exposed credential without printing its value.
3. **debug-and-fix**: Run the project build, tests, and linters. Fix any failures at their root cause. A release with a red build is not production ready.
4. **error-docs-lookup**: When encountering library deprecations, build tool warnings, or version migrations, search and read current official documentation before applying fixes.
5. **google-seo-skill**:
   - **Pull updates first**: If any update to `google-seo-skill` is available in git (upstream `https://github.com/mikezupper/google-seo-skill`), pull it first using `python scripts/update_seo_skill.py`. Verify clean frontmatter and human writing, then push updates to the skills repo.
   - **Use when**: Working on a public web project where search ranking and public search engine visibility are needed. Use it to audit crawlability, metadata, structured data, canonical URLs, and Core Web Vitals.
   - **Avoid when**: Working on a personal project, private repository, internal dashboard, staging site, or any project where search indexing is not desired. In those cases, skip SEO ranking checks entirely and verify that `noindex` meta tags, `X-Robots-Tag: noindex` headers, or robots disallow rules are present to prevent indexing.
6. **human-writing**: Scan all written or edited text (README, changelog, documentation, legal text, commit messages, and code comments) with `human-writing/scripts/scan.py`. Enforce zero hard hits (no em dashes, no emoji) and clear, human tone.
7. **context-rich-commits**: Record the release work using structured git commits (separating doc updates from legal text and code changes), followed by a project checkpoint commit. Push committed releases to the repo when instructed.
8. **Domain-specific skills**:
   - `android-app-dev`: Use for Android apps to verify the CI workflow, Gradle version catalog, and Compose configuration.
   - `minecraft-fabric-mod`: Use for Minecraft Fabric mods to verify Loom, Fabric API, and CI build workflows.
   - `iris-shaderpack-dev`: Use for shaderpacks to verify program names and shaders.properties.
   - `threejs-awwwards-site`: Use for WebGL and 3D websites to verify performance budgets and mobile fallbacks.
   - Google Cloud skills (such as `gcloud`, `google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`): Use when configuring or deploying services to Google Cloud Platform.

## Workflow

### 1. Audit
Run the audit script from the project root. It inspects the codebase, checks for missing or stale files, and lists which skills to USE and which to SKIP:

```bash
python scripts/audit.py <project-root>
```

For personal or internal projects where search indexing should be avoided, pass `--personal` or `--no-indexing`:

```bash
python scripts/audit.py <project-root> --personal
```

The script checks for changelog, README, docs, license, terms, privacy, security, contributing, and conduct files; compares the manifest version with the changelog; lists commits since the last tag; detects undocumented environment variables; flags broken README file references and npm scripts; and runs the human-writing scanner.

### 2. Changelog
Create or update `CHANGELOG.md` following `references/changelog.md`. Source entries from `git log` since the last release tag and from the git diff, not from memory. Write for users: what they can now do or what behaves differently, not an internal list of moved files. Group under Added, Changed, Fixed, Removed, Security. Keep an `Unreleased` section at the top until a version release is cut.

### 3. Docs and README
Create or update the README and anything under `docs/`. Follow the checklist in `references/docs.md`. The standard: a newcomer can go from cloning to running in a few minutes using only the README.

Run every install and execution command you document. A command you did not run is an unverified guess, so either run it or mark it unverified. Update docs for every behavior mentioned in the changelog, and remove docs for removed features.

### 4. Terms, privacy, and community rules
Review `references/legal-and-rules.md` for templates and the decision table:
- **Software installed or forked**: license, contributing guide, code of conduct, security policy.
- **Hosted app, public site, bot, or API with users**: add terms and conditions and privacy policy based on actual data collected (accounts, analytics, cookies, payments, uploads, third-party SDKs). Read the code to verify.
- **Personal project or internal tool**: standard open-source license or proprietary notice; omit consumer terms of service unless external users are onboarded.
- **Project rules**: write guidelines based on the actual policies enforced (contribution rules, API rate limits, community standards).

State plainly in the report that generated terms and privacy text are starting drafts that need legal review before launch. Do not claim legal compliance.

### 5. Skill selection and routing
Read `references/skill-selection.md` and confirm the project type from the audit output:
- **Web project needing search ranking**: USE `google-seo-skill` (or `references/seo.md`).
- **Personal web project, internal tool, staging site, or no indexing desired**: SKIP `google-seo-skill`. Verify that `noindex` tags or robots disallow rules protect the site from search crawlers.
- **Native mobile, desktop, mod, shaderpack, bot, or library**: SKIP SEO skills. Prepare store listing copy, mod registry text, or package metadata instead.
- **Domain skills**: If `android-app-dev`, `minecraft-fabric-mod`, `iris-shaderpack-dev`, or `threejs-awwwards-site` apply and are installed, invoke them for domain-specific checks and verification.

### 6. Multi-skill refresh pass
Run the applicable skills in this sequence:

1. **persistent-goal-execution**: Preserve the full production objective through the refresh pass and verify every requirement before reporting completion.
2. **credential-safety**: Check for credentials before committing or pushing. Stop and remediate findings, rotate exposed values, and do not expose secret contents in reports.
3. **debug-and-fix**: Run the project's build, test, and lint commands. Fix any failures at their root cause.
4. **error-docs-lookup**: For any warning, deprecation, or error involving a library or toolchain, look up official documentation for the installed version.
5. **Domain skill checks**: Run specific checks (for example, verifying CI workflows in `android-app-dev` or `minecraft-fabric-mod`).
6. **Search indexing and SEO check**:
   - If using `google-seo-skill`, first check if any update is available in git (`python scripts/update_seo_skill.py`) and pull it.
   - For public websites where ranking is needed: run `google-seo-skill` (or `references/seo.md`).
   - For personal or internal projects: verify that `noindex` headers or meta tags and robots rules are correctly in place.
7. **human-writing**: Run `human-writing/scripts/scan.py` on every touched file (README, changelog, docs, terms, comments). Eliminate all hard hits (no em dashes, no emoji).
8. **Audit rerun**: Rerun `scripts/audit.py`. Confirm zero remaining MISSING or STALE items.
9. **context-rich-commits and push**: Commit the changes using structured commit messages:
   - One commit for docs and changelog.
   - One commit for legal and community files.
   - A final checkpoint commit capturing the current state of the repository.
   - Always create or use a `dev` branch and push the current work there
     without waiting for user confirmation, whether the implementation is
     incomplete or complete. Verify the remote state and report what remains
     unfinished when applicable.
   - After the `dev` push succeeds, a production push always requires explicit
     human confirmation. If no `dev` branch exists, create it before asking
     for confirmation to push to production.
   - A final checkpoint commit capturing the current state of the repository.

### 7. Report
Provide a concise, factual summary:
- Files created or updated.
- Placeholders the user must fill in (company name, contact email, jurisdiction, dates).
- Skills used and skills skipped, each with a brief reason.
- Search indexing status: confirmed public indexing checklist or verified personal/internal `noindex` protections.
- Commands run and verification results (mark anything unverified as "not verified").
- Open observations (such as missing test suites or upstream dependencies).
- Legal review reminder if terms or privacy policies were drafted.

## Rules that keep this honest

- Version numbers and dates come from the manifest, tags, and git, never from guesses. Use today's system date for release headings.
- Do not bump the version or tag a release unless the user asked. Put changes under `Unreleased` otherwise.
- Do not delete existing legal text. Extend or flag it.
- Never put secrets, tokens, or personal emails found in the repository into public docs.
- Match existing project voice, formatting, and file layout before applying templates.

---
name: production-ready
description: Gets a project to a production-level finish by creating or updating the changelog, README and docs, and the legal and community files (terms of service, privacy policy, license, code of conduct, security policy, contributing rules), then refreshing the result with the related skills. Use whenever the user says production ready, ship it, release, prepare a release, final polish, wrap up the project, write or update a changelog, update the docs, write terms and conditions, write project rules, or asks what is missing before launch. Also use at the end of any large build or feature, even if the user only says done or finish up. Pairs with human-writing, debug-and-fix, error-docs-lookup and context-rich-commits.
---

# Production Ready

A project is not finished when the code works. It is finished when someone else can install it, understand it, trust it, and see what changed. This skill closes that gap: changelog, docs, terms and rules, then a refresh pass that reruns the other skills so nothing ships stale or broken.

Work on what the project actually has. Read the code and git history first, write second. Never invent features, versions, dates, company names, addresses or legal facts. If a fact is unknown, leave a clearly marked placeholder like `[COMPANY NAME]` and list it in the final report.

## Workflow

### 1. Audit
Run the audit script from the project root. It is the quick way to see what is missing or stale before touching anything.

```bash
python scripts/audit.py <project-root>
```

It checks for the changelog, README, docs, license, terms, privacy, security, contributing and conduct files, compares the version in the manifest with the latest changelog entry, lists commits since the last tag, flags README references to files and npm scripts that don't exist, and runs the human-writing scanner on the docs if that skill is installed. Without the script, do the same by hand with `ls`, `git log`, and a read of the manifest and README.

### 2. Changelog
Create or update `CHANGELOG.md`. Format and rules are in `references/changelog.md`. Source the entries from `git log` since the last release and from the diff, not from memory. Write for users: what they can now do or what behaves differently, not which files moved. Group under Added, Changed, Fixed, Removed, Security. Keep an `Unreleased` section at the top until a version is cut.

### 3. Docs
Create or update the README and anything under `docs/`. The checklist is in `references/docs.md`. The test: a stranger can go from clone to running in a few minutes using only the README. Run the install and run commands you document. A command you did not run is a guess, so either run it or mark it unverified.

Update docs for every behavior the changelog mentions. Remove docs for features that no longer exist. Stale docs are worse than missing docs.

### 4. Terms, privacy and project rules
Decide what the project needs, then read `references/legal-and-rules.md` for templates and the decision table.

- **Software people only install or fork:** license, contributing guide, code of conduct, security policy.
- **A hosted app, site, bot or API with users:** add terms and conditions and a privacy policy, based on what the code really collects (accounts, analytics, cookies, payments, uploads, third-party SDKs). Read the code to find out.
- **Rules for the project itself** (contribution rules, community rules, usage rules for a Discord bot, API rate limits, acceptable use): write them from the behavior the project enforces.

State plainly in the report that generated terms and privacy text is a starting draft and a lawyer should review it before launch, especially for payments, children's data, health data, or users in the EU, UK or California. Do not claim legal compliance.

### 5. Refresh pass
Run these in order. Skip any that are not installed and say so.

1. **debug-and-fix.** Run the project's build, test and lint commands. Fix what fails at the root cause. A release with a red build is not production level.
2. **error-docs-lookup.** For any warning, deprecation or error that involves a library, read the current official docs for the installed version. Update dependency notes and the docs if behavior changed.
3. **human-writing.** Run its scanner on every file you wrote or changed, README, changelog, docs, terms and comments. Fix every hard hit (em dashes, emoji) and reread soft warnings.
4. **Audit again.** Rerun `scripts/audit.py`. Nothing should be MISSING or STALE that you meant to fix.
5. **context-rich-commits.** Commit the work in that skill's format, one commit for the changelog and docs and a separate one for legal files. Add a checkpoint commit if the project uses them.

### 6. Report
Short and plain:
- Files created or updated.
- Placeholders the user must fill in (company name, contact email, jurisdiction, dates).
- What you ran and what happened. Say "not verified" for anything you could not run.
- Anything you noticed and left alone, such as a missing test suite or a vulnerable dependency.
- The legal review reminder, if you wrote terms or a privacy policy.

## Rules that keep this honest

- Version numbers and dates come from the manifest, tags and git, never from guesses. Use today's date from the system for new release headings.
- Don't bump the version or tag a release unless the user asked. Put changes under `Unreleased` otherwise.
- Don't delete existing legal text. Extend or flag it. Changing terms that live users already accepted is a decision for the owner.
- Never put secrets, tokens or personal emails you found in the repo into docs.
- Keep the project's existing voice and file layout. Match what is already there before applying a template.

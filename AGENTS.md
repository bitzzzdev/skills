# Repository-wide agent rules

These instructions apply to every agent and every task in this repository.

## Mandatory human writing

Load and follow `human-writing/SKILL.md` before starting any task. This is a mandatory skill, not an optional writing preference. Apply it to assistant communication, planning, code, comments, logs, tests, commit messages, documentation, legal files, and handoffs.

No emoji or emoji-like symbols are allowed anywhere in new or edited text. This includes status icons, checkmarks, crosses, decorative bullets, pictograms, and emoji presentation selectors. Do not add them to examples or test output. Also follow the skill's punctuation rules and write in a natural, factual voice from the project owner's perspective.

Run `python human-writing/scripts/scan.py <changed-files>` before committing. The CI job also checks changed files for emoji and emoji-like symbols. Do not weaken or bypass these checks to make a build pass.

## Public and production projects

Before calling a project production-ready, apply `production-ready/SKILL.md` and its references. A public release must have user-facing documentation for setup, usage, support, FAQs, troubleshooting, and verified known issues. Include terms of use, a privacy policy, a license, security guidance, and third-party credits or notices whenever required by the project's architecture and dependencies.

Document real behavior only. Verify commands, links, integrations, data collection, dependencies, licenses, and known issues against the repository. Never invent legal facts, support channels, bug reports, or integration details. Link the documentation from the README.

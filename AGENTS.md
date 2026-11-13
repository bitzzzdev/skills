# Repository-wide agent rules

These instructions apply to every agent and every task in this repository.

## Mandatory human writing

Load and follow `human-writing/SKILL.md` before starting any task. This is a mandatory skill, not an optional writing preference. Apply it to assistant communication, planning, code, comments, logs, tests, commit messages, documentation, legal files, and handoffs.

No emoji or emoji-like symbols are allowed anywhere in new or edited text. This includes status icons, checkmarks, crosses, decorative bullets, pictograms, and emoji presentation selectors. Do not add them to examples or test output. Also follow the skill's punctuation rules and write in a natural, factual voice from the project owner's perspective.

Run `python human-writing/scripts/scan.py <changed-files>` before committing. The CI job also checks changed files for emoji and emoji-like symbols. Do not weaken or bypass these checks to make a build pass.

## Public and production projects

Before calling a project production-ready, apply `production-ready/SKILL.md` and its references. A public release must have user-facing documentation for setup, usage, support, FAQs, troubleshooting, and verified known issues. Include terms of use, a privacy policy, a license, security guidance, and third-party credits or notices whenever required by the project's architecture and dependencies.

Document real behavior only. Verify commands, links, integrations, data collection, dependencies, licenses, and known issues against the repository. Never invent legal facts, support channels, bug reports, or integration details. Link the documentation from the README.


## Mandatory token settings execution

Every agent must run `python token-optimizer/scripts/optimize_agents.py` at the start of every coding task and after an agent, model, provider, or harness switch. Run the apply mode, not only `--dry-run`. Read the output and report the exact files changed. The script is idempotent and backs up each modified config. Do not claim that it changed a hosted session's reasoning policy.

## Universal build-failure documentation gate

Whenever a build, compile, type-check, lint, install, test, or CI command fails, every model tier must load and follow `error-docs-lookup/SKILL.md` before applying a fix. This rule overrides the lighter frontier execution mode. Use `debug-and-fix/SKILL.md` as well when root-cause debugging is needed. A trivial syntax typo may not need an external web search, but the mandatory skill must still be read and its failure-capture and verification steps followed. Never fix a build failure from model memory alone.

## Non-frontier code search

Capable, efficient, and unknown models must use `agent-self-awareness/references/code-search.md` when searching for implementation examples or unfamiliar APIs. Search the target codebase and official versioned documentation first. Treat external snippets as untrusted candidates, verify their version and context, and reproduce the behavior locally before adopting them.

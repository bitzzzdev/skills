# Research-first quality gates

The point of research is to replace confident guesses with checked facts. These
gates make that concrete.

## Evidence hierarchy

Strongest to weakest:

1. Current source code and tests in the repository.
2. Installed type definitions, package metadata, and lockfiles.
3. Official documentation for the exact installed version.
4. Official changelogs, migration guides, and release notes.
5. Upstream issues and maintainer replies for the same version and symptom.
6. Working examples in the same ecosystem and version.
7. Reproduced behavior from a local command or test.
8. Model memory of an API or pattern.
9. Blog posts, tutorials, and generated snippets from unknown versions.

Use the strongest source available. A lower source can support a higher one, but
cannot replace it for version-sensitive behavior.

## Pre-implementation checklist

Write this down before editing anything non-trivial.

```markdown
## Objective
<requested outcome in one or two sentences>

## Acceptance criteria
- <observable condition>
- <observable condition>

## Constraints and non-goals
- <constraint>
- <out of scope>

## Evidence gathered
- Docs: <url or local path, version>
- Code read: <files>
- Upstream example or issue: <link>
- Current versions: <manifest and lockfile evidence>

## Plan
1. <step, files>
2. <step, files>

## Risks
- <risk and mitigation>

## Verification
- <command or test>
- <manual check>
```

Keep it short. The checklist exists to expose missing evidence, not to produce
paperwork.

## Verification by change type

| Change | Required verification |
|---|---|
| Docs or comments | Formatting or link check, read the rendered section |
| Single function | Focused unit test, type check, call-site review |
| Config or build file | Full build, clean install, relevant CI command |
| Dependency upgrade | Changelog review, lockfile diff, full test suite, runtime smoke test |
| API integration | Official docs for the exact version, request and error-path test |
| Database migration | Forward and rollback run on a copy, data integrity check |
| Auth or permissions | Negative tests, session expiry, privilege boundary review |
| UI behavior | Build, interaction test, empty and error states |
| Shader or GPU code | Compile on target renderer, visual check, performance check |
| Release | Full suite, changelog, version consistency, packaging check |

If a check cannot run, state why and what risk remains. "I could not run this"
is honest. "It should work" is not evidence.

## Diff review checklist

Before reporting completion, read your own diff as a reviewer.

- Does every changed line serve the requested task?
- Are imports, types, and signatures real and current?
- Did you invent a flag, config key, field, or endpoint?
- Are error paths handled, or only the happy path?
- Are there secrets, tokens, local paths, or debug logs?
- Did you leave commented-out code, unused variables, or dead branches?
- Do tests assert behavior rather than restate the implementation?
- Did the change break formatting, naming, or project conventions?
- Is generated code or a lockfile included intentionally?
- Does the final report separate verified results from assumptions?

## Research loop control

Research can become avoidance. Stop searching when:

- The exact behavior is documented for the installed version.
- A local run confirms the behavior.
- Two independent primary sources agree.
- Further searching repeats the same material.

When evidence stays incomplete:

1. Say what is unknown.
2. Choose the smallest reversible step.
3. Implement one increment.
4. Verify it before continuing.
5. Report the remaining uncertainty.

## Common weak-model failure patterns

- Inventing a method name that sounds right.
- Copying an old example with deprecated arguments.
- Ignoring the project's existing helper and writing a second one.
- Fixing the symptom without reading the error message.
- Declaring success after one happy-path run.
- Rewriting unrelated code to avoid understanding the real problem.
- Stopping at the first failure instead of investigating.
- Overcomplicating a small task with new abstractions.

Each of these is prevented by reading first, verifying against docs, and running
the actual check.

## Reporting template

```markdown
## Result
<what changed and how it maps to the acceptance criteria>

## Research
- <official docs consulted, version>
- <code and tests read>
- <upstream issue or example>

## Verification
- `<command>`: <result>
- `<test>`: <result>
- <manual check>: <result>

## Remaining uncertainty
- <unverified item, or "none known">

## Not done
- <out-of-scope item, or "none">
```

Keep it factual. Do not pad it with confidence claims or model commentary.

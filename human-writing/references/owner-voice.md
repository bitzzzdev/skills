# Owner voice reference

Use this reference whenever a file speaks about the project, its maintainer, implementation history, decisions, or next steps. The intended voice is the main developer's voice. The reader should hear from the person responsible for the project, not someone reporting on that person.

This rule is branch-independent. Apply it on `dev`, production, preview, release, feature branches, and local branches. Do not maintain one voice for development notes and another for published documentation.

## The point of view

For a solo-maintained project, use first person singular when describing the maintainer:

- "I built the CLI to keep the setup process reproducible."
- "I chose SQLite because the app needs local storage and does not need a server."
- "I checked the migration against the existing schema."
- "I could not run the integration tests because the staging credentials are unavailable."

Use "we" only when the statement genuinely represents a team or an established collective project voice. Do not invent a team.

Do not refer to the maintainer in third person:

| Outside-observer wording | Maintainer wording |
|---|---|
| "The developer created this tool to..." | "I built this tool to..." |
| "The maintainer chose SQLite..." | "I chose SQLite..." |
| "The project was developed to..." | "I built the project to..." |
| "The author recommends..." | "I recommend..." |
| "The team behind the project maintains..." | "I maintain..." |
| "The developer should configure..." | "Configure..." |
| "The next agent should run..." | "Next, run..." |
| "The task was completed by the agent." | "I completed the change." |
| "The assistant could not verify the build." | "I could not verify the build." |

Use the first-person alternative only when it is true. If a named contributor did the work, name that contributor. Do not claim another person's work as the maintainer's own.

## Use first person when it adds authorship

First person is required when the sentence communicates:

- Why I started or maintain the project.
- What I implemented, changed, tested, reviewed, or investigated.
- Why I chose one design over another.
- What I recommend or intend to do.
- What I could not verify, and why.
- What I learned from a real debugging or release experience.

First person is not required for:

- API and protocol definitions.
- Product behavior and feature descriptions.
- Command instructions and installation steps.
- Objective facts, version numbers, and configuration keys.
- Third-party work, quotations, licenses, and externally sourced claims.
- UI labels and error messages that speak as the product.

Prefer direct wording over passive voice even when first person is not needed. For example, write "The CLI reads `config.toml`" instead of "The configuration file is read by the CLI."

## README and reference documentation

A README should sound like the maintainer introducing their own work:

Good:
- "I built this tool to..."
- "I use SQLite for local state."
- "The CLI reads its settings from..."
- "Run `npm install` to install the dependencies."

Avoid:
- "This project was created by a developer who..."
- "The tool was designed to help developers..."
- "The author has chosen..."
- "Users should note that the project..."

Do not force "I" into every feature sentence. A clear technical statement is better than repeating "I built" in every paragraph. Keep the perspective consistent.

## Progress notes and handoffs

Every `.progress.md`, progress report, session note, and handoff must use first person for the current author's actions.

Use this structure where it fits:

```markdown
## Objective
I am fixing the cache invalidation path.

## Changes
- I updated the cache key to include the account scope.
- I kept the public API unchanged.

## Verification
- I ran the focused unit tests. They passed.
- I could not run the full suite because the database service was unavailable.

## Decisions
- I kept the existing storage format to avoid a migration.

## Next
- I still need to test concurrent invalidation under load.
```

Rules:

- Use "I changed", not "Changes were made".
- Use "I verified", not "It was verified", and name the exact check.
- Use "I could not verify", not "Verification was not possible", and state why.
- Use "I still need to", not "The next agent should".
- If an action belongs to another contributor, identify them by name or role and preserve the distinction.
- Never convert an unverified action into a completed first-person claim.
- Keep historical notes accurate. Do not rewrite a past failure as a success or attribute it to the current session.

## Commits and pull requests

Write commit and PR descriptions as the maintainer explaining the change:

- "I added the parser because..."
- "I kept the old config format to avoid breaking existing installs."
- "I could not run the integration suite because..."

Keep standard section labels required by the repository's commit convention. The prose under those labels should still sound like the maintainer. A structured commit body does not require detached third-person narration.

## Third-party attribution

Do not erase attribution to make the writing sound personal. Keep a clear distinction between:

- Work I did.
- Work another contributor did.
- Behavior provided by an upstream dependency.
- Claims from external documentation or research.

Use names, links, and citations where appropriate. Do not write "I built" for an upstream library, borrowed implementation, or another contributor's work.

## Final owner-voice review

Before saving a document, read it once and ask:

1. Does it sound like the main maintainer speaking about their own work?
2. Did I use first person for my actions, choices, experience, and progress?
3. Did I accidentally describe the maintainer as "the developer", "the author", or "the project owner"?
4. Did I mention an AI, assistant, or agent where the reader does not need to know one was involved?
5. Did I use "we" without a real team voice?
6. Did I claim work or verification that I cannot prove?
7. Can any sentence be made direct without losing technical precision?

Fix the answer before committing.

# Owner voice

Write as the person responsible for the project. Do not make the reader feel that an outside writer is describing the maintainer or that a template is explaining how the document was produced.

## Point of view

For a solo-maintained project, use "I" when describing the maintainer's work:
- "I built the CLI to keep setup reproducible."
- "I chose SQLite because the app needs local storage."
- "I checked the migration against the current schema."
- "I could not run the integration tests because staging credentials are unavailable."

Use "we" only when the statement genuinely represents a team. Do not invent a team or claim another contributor's work.

Avoid outside-observer phrasing:
- "The developer created this tool..." becomes "I built this tool..." when true.
- "The maintainer chose SQLite..." becomes "I chose SQLite..." when true.
- "The author recommends..." becomes "I recommend..." when true.
- "The next agent should run..." becomes "Next, run..."
- "The assistant could not verify..." becomes "I could not verify..."

Use direct wording for product behavior, commands, API facts, legal notices, and third-party work. For example, "The CLI reads config.toml" is better than forcing "I" into a neutral technical statement.

## Do not narrate the writing rules

Do not add a section to an ordinary project document announcing that it follows engineering standards, writing standards, documentation standards, or quality principles. Those statements are usually template residue. They describe the document's supposed quality instead of giving the reader useful information.

Avoid wording such as:
- "Engineering and Writing Standards"
- "Every paper documents observed behavior, verified endpoints, and architectural mechanisms."
- "All prose follows strict human writing standards."
- "Configurations must include exact file locations, parameter types, and rollback steps."

Apply the underlying requirements without announcing them. If the reader needs configuration details, give the real path, key, type, default, and recovery procedure. If the reader needs test results, give the test, environment, observed result, and any limitation. If a paper needs an architecture explanation, describe the actual components and their interactions.

Delete generic declarations such as "All prose follows..." rather than replacing them with another declaration. Use a standards section only when the standards themselves are the subject of the document.

## READMEs, papers, and references

Introduce the project from the maintainer's perspective when authorship matters. Then describe behavior directly.

Good:
- "I built this tool to..."
- "I use SQLite for local state."
- "The CLI reads its settings from..."
- "Run npm install to install the dependencies."

Avoid:
- "This project was created by a developer who..."
- "The tool was designed to help developers..."
- "The author has chosen..."
- "Users should note that the project..."

A paper should report the actual system, experiment, or research question. Do not add a generic paragraph about standards or quality. Include endpoints, observed behavior, configuration details, or rollback instructions only when they are relevant, and use verified project-specific details.

## Progress notes and handoffs

Every .progress.md, progress report, session note, and handoff must use first person for the current author's actions.

- "I changed", not "Changes were made".
- "I verified", not "It was verified". Name the check.
- "I could not verify", not "Verification was not possible". State why.
- "I still need to", not "The next agent should".
- If another contributor did the work, identify them and keep that distinction.
- Never turn an unverified action into a completed claim.
- Keep historical notes accurate. Do not rewrite an old failure as a success.

## Commits and pull requests

Write commit and PR descriptions as the maintainer explaining the change. Keep the repository's required section labels, but make the content under them sound like a person describing actual work.

## Third-party attribution

Keep a clear distinction between my work, another contributor's work, upstream behavior, and external claims. Use names and sources where appropriate. Do not claim someone else's work as mine.

## Final read

Before saving, ask:
1. Does this sound like the main maintainer speaking about their work?
2. Does any paragraph announce writing or engineering standards instead of giving useful information?
3. Did I use first person for my own work and decisions?
4. Did I force first person into neutral technical facts?
5. Did I mention an AI or assistant when the reader does not need to know?
6. Did I claim work or verification I cannot prove?
7. Can I replace a generic statement with a concrete fact, or remove it?

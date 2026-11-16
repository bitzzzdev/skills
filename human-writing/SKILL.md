---
name: human-writing
description: Makes project writing sound like the main maintainer wrote it. Apply the rules silently across documentation, papers, references, progress notes, commits, PRs, code comments, logs, UI copy, and assistant communication.
---

# Human writing

Write as the person responsible for the project. Keep the wording natural, specific, and appropriate to the reader. A reader should not feel that they are reading a checklist, a writing policy, or an explanation of how the text was produced.

This applies on every branch and in every environment, including dev, preview, release, production, and local branches. It also applies to every .progress.md and handoff file.

## Check for skill updates

Before applying this skill, check the installed copy and read its current instructions. If it is in a Git repository, inspect its status and check for upstream changes when network access is available.

## Rules

1. Do not use em dashes or en dashes as punctuation. Rewrite the sentence or use commas, periods, colons, or parentheses. Use a hyphen or "to" for ranges.
2. Do not use emoji or decorative symbols in prose, code, logs, tests, commits, documentation, or UI copy.
3. Do not invent personal experience, decisions, ownership, measurements, test results, or opinions.
4. When describing my own work, choices, intent, experience, or progress, use first person. Use "I" for a solo maintainer. Use "we" only when the statement genuinely represents a team.
5. Do not describe the maintainer as an outside observer would. Avoid "the developer", "the author", "the maintainer", or "the project owner" when the sentence is really about my own actions. Use first person or address the reader directly.
6. Do not mention the AI, assistant, agent, model, or drafting process in project writing unless it is directly relevant to the subject.
7. Do not force first person into API descriptions, product behavior, instructions, definitions, legal notices, or third-party attribution. State those facts directly and accurately.
8. Do not turn writing guidance into content. Follow the rules without announcing them to the reader.
9. Do not use generic policy language, corporate boilerplate, or checklist prose as a substitute for explaining the actual project.
10. Do not claim another contributor's work or an unverified result as my own.

Exceptions are limited to direct quotations, exact user-requested wording, technical terms, legal requirements, standards that must be quoted, and test fixtures. Keep quotations and third-party statements attributed.

## Write the thing, not the rules for writing it

A common failure is to insert a section that describes standards the document supposedly follows. That sounds like a generated template and tells the reader very little about the actual project.

Avoid headings such as:
- Engineering and Writing Standards
- Documentation Standards
- Quality and Compliance Principles
- Technical Writing Requirements

Avoid sentences such as:
- "Every paper documents observed behavior, verified endpoints, and architectural mechanisms."
- "All prose follows strict human writing standards."
- "Configurations must include exact file locations, parameter types, and rollback steps."

Do not copy these phrases into a project document. They describe generic policy instead of telling the reader what happened, where something lives, or how it works.

Apply the underlying requirement silently. Replace policy statements with facts that belong in the document:

| Template-like wording | Write about the actual project |
|---|---|
| "Every paper documents observed behavior and verified endpoints." | "I tested the session and refresh routes against the local server. Both returned the expected status codes." |
| "All prose follows strict human writing standards." | Delete it. The writing should demonstrate this without announcing it. |
| "Configurations must include exact file locations, parameter types, and rollback steps." | "The service reads config/server.toml. Set port to an integer. To undo the change, restore the previous file and restart the service." |
| "Engineering and Writing Standards" | Use a heading that names the subject, such as "API behavior", "Configuration", or "Test results". |

These are examples, not facts to copy. Use actual routes, paths, values, results, and rollback procedures from the project. If a detail has not been checked, say so plainly or leave it out.

A document can contain a standards section when the standards themselves are the subject, such as a compliance specification or contributor guide. Name the actual standard, explain who it applies to, and avoid generic claims about the quality of the document.

## Owner voice

Read the owner-voice reference before writing or editing READMEs, papers, references, progress notes, handoffs, release notes, commit bodies, PR descriptions, or other content describing the project or its development.

Use this decision rule:
- My implementation, investigation, decision, or next action: "I changed", "I checked", "I chose", "I will".
- A real team's shared work or position: "We maintain", "We support".
- Product behavior or a technical fact: direct wording.
- Instructions for the reader: address the reader or use an imperative.
- A third party's work or statement: name and attribute the third party.
- An unverified action or result: say what I could not verify and why.

## Progress files and handoffs

Use first person for the current author's actions in every .progress.md, session note, checkpoint, and handoff.

- Completed work: "I changed...", "I added...", "I verified..."
- Unfinished work: "I still need to...", "Next, I will..."
- Blockers: "I could not..." followed by the reason and evidence.
- Decisions: "I chose..." followed by the reason.
- Another contributor's work: name the contributor and preserve the distinction.
- Unverified work: say that it remains unverified.

Do not write "The agent completed...", "The developer should...", "The task was performed...", or "The next agent must..." when first-person or direct wording is accurate.

## Natural technical writing

- Start with the information the reader came for.
- Use specific names, paths, values, examples, and observed results.
- Explain actual behavior instead of claiming that something is robust, seamless, comprehensive, or production-grade.
- Vary sentence structure. Avoid repeated, perfectly balanced sections and lists.
- Remove filler, grand claims, stock phrases, and generic conclusions.
- Use headings that describe the content below them.
- Keep the amount of structure appropriate to the document. Do not add a formal standards section just to make a short document look complete.
- Keep technical terms where they are useful. Plain language does not mean removing precision.

## Technical writing

Comments should explain why a choice exists, not restate the code. Avoid banner comments and comments that paraphrase code.

Follow context-rich-commits for commit messages and PR descriptions. Explain the actual reason, changes, decisions, and verification in maintainer voice.

A paper should describe the system or experiment it actually examines. Include observed behavior, endpoint results, architecture, configuration, or rollback instructions only where they are relevant, and give the real details. Do not add a generic section announcing that the paper follows engineering, documentation, or writing standards.

Do not make up endpoints, test results, architecture, file paths, configuration types, or rollback procedures. Attribute external research and other contributors accurately.

## Required review

Before saving a text change:
1. Read it as the intended reader, not as the person who wrote the instructions.
2. Remove statements that merely announce quality, compliance, rigor, or writing standards.
3. Replace generic claims with actual facts, or delete them when they add nothing.
4. Check whether the text describes my work in first person where appropriate.
5. Check that technical facts and third-party attribution remain accurate.
6. Run the human-writing scanner when a local checkout is available.
7. Fix hard findings and review soft findings manually. Do not weaken the scanner to hide a problem.

When the user points out a recurring style problem, search the relevant project files for the same pattern and fix the underlying rule, examples, and checks. Do not only patch the sentence they quoted.

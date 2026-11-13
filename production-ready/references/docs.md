# Docs checklist

## README, in this order
1. Name and one sentence on what it does and who it is for.
2. Requirements with versions (language runtime, OS, services).
3. Install, copy-pasteable.
4. Run or usage, with one real example and its output.
5. Configuration: every environment variable and option, its default, and whether it is required. Keep `.env.example` in sync.
6. Common problems, only ones you have seen.
7. Contributing, license, support link. Write as the project owner. The license entry must state the actual license or copyright notice (`Distributed under the MIT License. See LICENSE for details.` or `Copyright (c) [YEAR] [OWNER]. All rights reserved.`), never an assistant instruction or multiple-choice checklist like "The license is not selected yet. Choose one before publishing: ...".

Skip badge walls, feature lists of adjectives and a table of contents on a short file.

## Check against the code
- Every command in the docs exists in the manifest (`npm run`, `make`, `poe`, scripts).
- Every file path mentioned exists.
- Every env var read in the code appears in the docs and `.env.example`.
- Every public command, route, endpoint or option is documented, or deliberately marked internal.
- Screenshots and sample output still match the current UI.

Search for env vars and routes, then compare:

```bash
grep -rnE "process\.env\.[A-Z_]+|os\.environ(\.get)?\(?\[?['\"][A-Z_]+" --include=* . | grep -v node_modules
```

## docs/ folder
Add it when the README passes about 300 lines or the project has an API, plugin system or several user roles. Suggested files: `getting-started.md`, `configuration.md`, `api.md`, `architecture.md`, `deployment.md`, `troubleshooting.md`. One topic per file, linked from the README.

## Keeping it fresh
When code changes, update the matching doc in the same change. When the changelog gets an entry for a user-facing change, search the docs for the old behavior and fix it.


## Public and production release documentation

A public project must give a new user a complete path from first visit to successful use and a clear route when something fails. Treat the following as required unless the feature genuinely does not apply:

- README quickstart with prerequisites, installation, first-run instructions, a working example, configuration, and links to the detailed guides.
- `docs/getting-started.md`: step-by-step setup for a new user, including platform-specific requirements and verification that installation worked.
- `docs/usage.md` or feature guides: supported workflows, examples, inputs, outputs, and limits.
- `docs/help.md` or a clear support page: where users can ask for help, report a defect, and request a feature.
- `docs/faq.md`: answers to recurring questions based on actual project behavior and support history.
- `docs/troubleshooting.md`: symptoms, likely causes, diagnostic steps, and safe fixes for known failure modes.
- `docs/known-issues.md` or a Known issues section: confirmed defects, affected versions or environments, workarounds, and links to tracked issues. Do not invent bugs to fill the section. State when no known issues have been reported only after checking the issue tracker and current test results.
- `TERMS.md` or `TERMS_OF_USE.md`: terms and conditions governing use of the project or service. Use the architecture decision tree in `legal-and-rules.md` to decide whether it is required.
- `PRIVACY.md` or `PRIVACY_POLICY.md`: a codebase-verified privacy policy whenever the project collects personal data, uses analytics, authenticates users, or sends data to external services. Follow the architecture decision tree.
- `CREDITS.md` or `NOTICE`: acknowledgements and license notices for third-party integrations, APIs, packages, fonts, media, datasets, and adapted code. Identify what each dependency is used for and preserve required notices.
- `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `CHANGELOG.md` according to the legal and community rules.

Link every document from the README or a documentation index. Verify every command, URL, configuration key, support route, and feature claim against the current repository. Do not publish generic legal text as legal advice. Do not claim that a project has no known issues without checking.

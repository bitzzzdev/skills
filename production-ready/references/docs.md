# Docs checklist

## README, in this order
1. Name and one sentence on what it does and who it is for.
2. Requirements with versions (language runtime, OS, services).
3. Install, copy-pasteable.
4. Run or usage, with one real example and its output.
5. Configuration: every environment variable and option, its default, and whether it is required. Keep `.env.example` in sync.
6. Common problems, only ones you have seen.
7. Contributing, license, support link.

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

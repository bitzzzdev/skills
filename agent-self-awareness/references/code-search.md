# Code search sources for implementation research

Use this reference when the active model is capable, efficient, or unknown, and whenever an implementation pattern or unfamiliar API needs corroboration. Code search is a way to find candidate implementations. It is not proof that an example is current, secure, or compatible with the target project.

## Search order

1. Read the target repository first: manifests, lockfiles, source, tests, generated types, and existing patterns.
2. Read the official documentation for the exact installed version.
3. Search upstream source repositories and release history for the same version.
4. Compare at least one real implementation with the official API contract.
5. Reproduce the behavior locally and add a focused test before relying on the pattern.

## Useful code search services

| Source | Best use | Limits and cautions |
|---|---|---|
| [GitHub Code Search](https://docs.github.com/en/search-github/github-code-search/using-github-code-search) | Search public repositories for exact symbols, APIs, qualifiers, and regular expressions | Search syntax differs from issue search. Results are candidate examples, not version guarantees. |
| [Sourcegraph public search](https://sourcegraph.com/docs/getting-started) | Search open-source repositories across hosts, filter by repository, language, file, or revision | Sourcegraph.com is for public open-source code. Some advanced features require paid plans or a configured instance. |
| [GitLab code search](https://docs.gitlab.com/user/search/) | Search code in a specific project and, where enabled, group or instance scopes | Global and exact-code search availability depends on subscription, indexing, and configuration. Basic search may be limited to one project. |
| [GitLab Search API](https://docs.gitlab.com/api/search/) | Scripted searches where the user has an authenticated GitLab connection | API search requires authentication; blob search depends on advanced or exact code search being enabled. |
| [GitLab CLI search](https://docs.gitlab.com/cli/search/) | Search a GitLab project from the terminal | The documented search command is beta. Check the installed glab version and help output before depending on it. |

## Query construction

Use specific, version-aware searches. Examples:

- Exact symbol: `"createBrowserRouter" repo:remix-run/react-router`
- API plus runtime: `"use server" language:TypeScript`
- Error plus package version: `"ERR_PACKAGE_PATH_NOT_EXPORTED" vite 6`
- Config key: `"model_reasoning_effort" repo:openai/codex`
- Narrow a GitLab search by project, path, extension, or language using the syntax supported by that GitLab instance.

Search for the exact symbol or error first. Then search for the official repository, tagged release, migration guide, tests, and changelog. Prefer a release tag or commit that matches the dependency version in the lockfile.

## How to evaluate a result

For every candidate snippet:

- Open the complete file and inspect imports, surrounding code, error handling, and call sites.
- Check the commit date, release tag, dependency versions, and whether the example is maintained.
- Compare names, parameters, return types, and behavior against official documentation or installed type definitions.
- Check whether the example relies on an undocumented internal API, unsafe workaround, deprecated option, or unrelated framework version.
- Search for the same pattern in tests and changelogs.
- Reproduce it in the target project before adapting it.

Do not copy a snippet merely because it compiles in a search result. Never paste private source code, credentials, tokens, or customer data into public code search.

## When results disagree

The target project's source and tests, installed types, and official versioned documentation outrank search snippets. If evidence conflicts, record the conflict and test the smallest safe hypothesis. Do not ask a non-frontier model to choose between snippets by intuition.

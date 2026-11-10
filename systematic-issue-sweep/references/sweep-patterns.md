# Systematic Issue Sweep: Reference Patterns

This guide covers query formulation, classification strategies, and remediation patterns for sweeping workspaces when a defect, typo, or flawed assumption is discovered.

## 1. The Single-Occurrence Fallacy

When a defect is spotted at line 42 of a file, developers often fix line 42 and move on. In real codebases, isolated bugs are rare:
- Typos in variable names or copy are copied to tests, documentation, and sister modules.
- Missing null checks or unhandled edge cases represent a shared blind spot across all endpoints written in that sprint.
- Flawed error handling or un-awaited promises reflect misunderstanding of a third-party library API.
- Bypassed permission checks or missing tenant filters usually affect multiple routes sharing similar controllers.

Every identified issue is an opportunity to clean the entire codebase of that failure pattern.

## 2. Query Formulation Tactics

When a problem is reported, formulate search queries at three levels:

### Level A: Literal Pattern
Search for the exact token or phrase.
- Target: Typos, misspelled identifiers, outdated brand names, exact bad constants.
- Tools:
  ```bash
  python systematic-issue-sweep/scripts/sweep.py "old_function_name"
  git grep -n "exact_typo"
  ```

### Level B: Structural and Regex Pattern
Search for variations of the pattern (casing, spacing, naming variants).
- Target: camelCase vs snake_case variants, optional parameters, syntax shapes.
- Examples:
  - Misspelled word in camelCase or snake_case: `\b(recieved|isRecieved|recieve_count)\b`
  - Un-awaited async call: `(?:await\s+)?db\.users\.find\(` where `await` is missing.
  - Insecure query concatenation: `(?:SELECT|INSERT|UPDATE).*\$\{` or `f"(?:SELECT|INSERT|UPDATE)`

### Level C: Conceptual / Semantic Cousins
Search for related operations that share the same underlying logic.
- Target: All functions in the same family, all route handlers using the same auth decorator, all event listeners that fail to clean up.
- Example: If `onUserDeleted` fails to invalidate the Redis cache, search every other `onUser*` handler (`onUserUpdated`, `onUserRoleChanged`, `onUserBanned`) to verify cache invalidation.

## 3. The Issue Spectrum

### Tier 1: Lexical, Copy, and Naming
- Symptoms: Misspellings, outdated terminology, inconsistent casing, assistant meta-instructions, leaked placeholder text.
- Sweep strategy:
  1. Identify all lexical variants: singular, plural, uppercase, lowercase, camelCase, kebab-case.
  2. Search code, tests, documentation, comments, and configuration.
  3. Verify whether external APIs or public interfaces rely on the old name before changing.

### Tier 2: Interface and API Usage
- Symptoms: Wrong argument order, unhandled promise rejections, deprecated library calls, missing error callbacks.
- Sweep strategy:
  1. Search for every import and call site of the affected function or library.
  2. Inspect each call site against the authoritative documentation.
  3. Where appropriate, create a single validated wrapper function rather than patching dozens of raw call sites.

### Tier 3: Defensive and Boundary Checks
- Symptoms: Missing null/undefined checks, unvalidated user input, unhandled empty arrays, un-sanitized file paths.
- Sweep strategy:
  1. Identify the input schema or data boundary.
  2. Locate every consumer of that data shape across the application.
  3. Apply schema validation at the perimeter (e.g. Zod, Pydantic, or explicit guard clauses) so internal components do not need defensive duplication.

### Tier 4: Business Logic and State Invariants
- Symptoms: Off-by-one errors in pagination, missing tenant isolation, race conditions in status transitions, incorrect fee calculations.
- Sweep strategy:
  1. Extract the invariant into a single authoritative rule or helper.
  2. Search for all locations where that calculation or transition is computed manually.
  3. Replace manual logic with the unified helper.
  4. Write parameterized unit tests covering boundary values across all consumers.

### Tier 5: Architectural and Configuration Flaws
- Symptoms: Hardcoded timeouts, missing environment fallbacks, unencrypted cookies, inconsistent logging formats.
- Sweep strategy:
  1. Centralize the configuration in the project's config module.
  2. Search for ad-hoc references across the tree.
  3. Verify against deployment manifests and `.env.example`.

## 4. Remediation Checklist

1. **Quantify the scope first:** Run `sweep.py` to count total occurrences across all files before editing.
2. **Cluster by file type:** Review occurrences in core source, tests, documentation, and configs separately.
3. **Harmonize root causes:** Prefer fixing the root abstraction over editing 20 downstream files when a single central helper solves all 20.
4. **Preserve intentional exceptions:** Some test fixtures intentionally test invalid inputs or misspelled strings. Do not alter test fixtures designed to assert error handling.
5. **Run test suite after sweeping:** Prove that all fixes pass clean builds, type checks, and tests.
6. **Add recurrence guards:** Add a linter rule, unit test, or scanner pattern so the issue cannot re-enter the repository.

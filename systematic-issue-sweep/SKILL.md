---
name: systematic-issue-sweep
description: Sweeps the entire workspace to find, fix, and prevent recurrences of any reported issue, bug, typo, style flaw, or logic error. Use whenever a user, test, or reviewer points out an issue or inconvenience in one place, or during a production-ready refresh pass. The skill abstracts the underlying mistake pattern, conducts a workspace-wide search across code, docs, tests, and config, systematically fixes every occurrence, and adds regression guards so the issue cannot recur. Pairs with debug-and-fix and production-ready.
---

# Systematic Issue Sweep

When a bug, typo, bad copy, or logic flaw is found in one location, fixing only that single spot leaves identical or related problems scattered across the rest of the workspace. This skill eradicates the entire class of problem across the whole codespace.

It treats every reported issue or user inconvenience not as an isolated accident, but as a symptom of a repeatable pattern.

## Check for skill folder updates

Before applying this skill, check whether the skill folder has updates:

1. Identify the directory where this skill is installed (such as `~/.copilot/skills/`, `~/.gemini/antigravity-cli/skills/`, `~/.claude/skills/`, or the active repository).
2. If the folder is inside a git repository, check git status:
   ```bash
   git -C <skill-folder> status --short --branch
   ```
3. When network access is available, check for upstream changes:
   ```bash
   git -C <skill-folder> fetch --dry-run
   ```
4. If updates are available, pull them before proceeding so you use the latest instructions. If the folder is not a git repository, proceed with the installed files.

## Hard rules

1. **Never stop at the reported site.** Fixing only the exact line reported by the user or test is incomplete. Every fix requires checking for recurrences across the entire workspace.
2. **Abstract before sweeping.** Do not search only for the literal variable or line. Formulate the general pattern: what category of mistake is this, and where else could the same assumption have been made?
3. **Inspect each match in context.** Never perform blind global regex replacements without verifying syntax, imports, and intent at each site.
4. **Preserve deliberate test fixtures.** Test suites frequently contain deliberate errors or malformed inputs to verify error handling. Do not alter test inputs designed to assert rejection.
5. **Install recurrence prevention.** Where possible, add a test case, linter rule, type check, or automated audit check so the pattern cannot re-enter the repository.

## The 5-Step Sweep Workflow

### 1. Abstract the problem
Convert the concrete report into a searchable pattern:
- **Typo or copy tell:** Extract all lexical forms (singular, plural, camelCase, snake_case, uppercase).
- **API misuse:** Identify the library, function, or endpoint being called incorrectly.
- **Defensive flaw:** Identify the unvalidated data shape or boundary condition.
- **Logic or state error:** Identify the invariant that was broken (such as unhandled status transitions or missing cache invalidations).

### 2. Search the entire codespace
Run the sweep script or workspace grep across all source files, tests, documentation, markdown files, and configurations:

```bash
python /path/to/systematic-issue-sweep/scripts/sweep.py "pattern" .
```

For structural or regex patterns:

```bash
python /path/to/systematic-issue-sweep/scripts/sweep.py --regex "regex_pattern" .
```

Inspect the total count and distribution across files.

### 3. Classify occurrences
Group the findings:
- **Direct recurrences:** Identical code or copy duplicated in other modules or files.
- **Conceptual cousins:** Sister functions, sibling routes, or parallel handlers built with the same flawed mental model.
- **Downstream fallout:** Documentation, tests, mock data, or type declarations referencing the flawed pattern.
- **Intentional exceptions:** Error assertions or negative test fixtures that must remain.

### 4. Apply systematic remediation
Fix every valid occurrence:
- If many files duplicate the same manual logic, extract a single robust helper function and route all call sites through it.
- If an identifier or term was misspelled, update all declarations, usages, docs, and tests together.
- If a security check or tenant filter was bypassed, centralize the check in middleware or shared query builders.

### 5. Verify and guard against recurrence
- Run the project build, type checker, and full test suite.
- If the issue was a logic bug, write a regression test covering the edge case across all affected components.
- Run `sweep.py` one final time to confirm zero remaining unwanted occurrences across the workspace.

## Issue Spectrum

### Level 1: Lexical, Copy, and Documentation
- Typos, misspelled variables, outdated product names, assistant coaching leaks ("Choose one before publishing"), and banned stock phrases.
- Action: Sweep code, comments, READMEs, changelogs, and legal files.

### Level 2: Signatures and API Usage
- Inverted argument order, missing `await` on asynchronous operations, deprecated API endpoints, unhandled error callbacks.
- Action: Search for all imports and call sites of the affected library.

### Level 3: Defensive Bounds and Null Safety
- Unchecked property access, missing null/undefined guards, unvalidated request payloads, unhandled empty collections.
- Action: Enforce perimeter validation with schema guards or shared validation utilities.

### Level 4: Core Logic and State Invariants
- Race conditions, off-by-one errors in pagination or ranges, broken state machines, missing cache eviction on mutations.
- Action: Extract logic to a single state manager or service class, sweep and replace all inline reimplementations.

### Level 5: Architecture and Security
- Missing authentication middleware, bypassed authorization checks, SQL or command injection risks, hardcoded credentials.
- Action: Audit all public routes and controllers for compliance with the security invariant.

## Before and after

**User report: "Typo in user controller: `recieveData` should be `receiveData`"**

Before (shallow fix):
Renames `recieveData` to `receiveData` in `user_controller.py` only. The typo remains in `auth_controller.py`, `webhook_handler.py`, API documentation, and three test files.

After (systematic sweep):
Runs `python sweep.py "recieve" .`. Finds 9 occurrences across controllers, tests, and markdown docs. Renames all occurrences, updates documentation, runs the test suite, and confirms zero remaining instances.

**User report: "Missing tenant isolation in `get_invoices` allows cross-tenant leaks"**

Before (shallow fix):
Adds `where tenant_id = current_tenant` inside `get_invoices` only. Five other billing queries (`get_receipts`, `get_subscriptions`, `get_payment_methods`) still lack tenant filtering.

After (systematic sweep):
Identifies the core invariant: every database query in the billing service must enforce tenant boundaries. Sweeps all repository methods in the billing module, finds 4 other queries missing tenant constraints, updates all of them to use a scoped query helper, and adds integration tests asserting tenant isolation across all endpoints.

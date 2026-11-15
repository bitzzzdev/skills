# Change impact analysis

Use this procedure before and after implementation. It applies to every model tier and every change. The amount of investigation depends on the risk, but the agent must always check for effects beyond the edited line or file.

## 1. Define the change

Write down:

- The requested end state.
- Observable acceptance criteria.
- Explicit constraints and non-goals.
- Existing behavior that must remain unchanged.

Inspect the current implementation before deciding which files need edits. Read the parent and child components, related routes, callers, tests, configuration, and project conventions.

## 2. Build the dependency map

Start with the direct target, then trace outward:

- Imports, exports, callers, consumers, and shared components.
- Data producers, transformations, storage, caches, and consumers.
- Routes, navigation, links, anchors, selectors, CSS variables, and layout containers.
- Public APIs, types, schemas, configuration keys, environment variables, and command interfaces.
- Tests, fixtures, mocks, snapshots, generated files, build scripts, and CI.
- README sections, guides, API docs, changelogs, and external integration contracts.

Use repository-wide searches for identifiers and references. Static imports alone are not a complete dependency map. Include runtime references, string-based lookups, generated outputs, and shared styles when they exist.

Follow transitive dependencies until the next layer no longer introduces a new consumer or behavior. Record the files and relationships that matter to the requested change.

## 3. Enumerate foreseeable outcomes

For each affected surface, consider:

| Outcome | Questions |
|---|---|
| Intended result | Does the requested behavior work in every supported context? |
| Partial result | Can only some routes, states, devices, or records receive the change? |
| No-op | Can a selector, condition, event, migration, or update fail to match anything? |
| Failure | What happens when data, a dependency, a request, or an external service is missing or invalid? |
| Regression | What existing behavior, layout, interface, or consumer could change unintentionally? |
| Boundary state | What happens with empty, null, long, large, small, invalid, repeated, or concurrent inputs? |
| Timing and state | Can caches, asynchronous work, hydration, retries, history restoration, or stale state change the result? |
| Compatibility | Could existing links, APIs, data, configs, clients, or persisted state stop working? |
| Recovery | Can the change be rolled back safely, and what state would remain? |

Do not manufacture implausible scenarios. Derive cases from actual architecture, code references, supported inputs, and known failure modes. Prioritize by likelihood and impact.

For every identified outcome, choose one action:

- Update the affected implementation.
- Add or update a test.
- Update documentation or generated output.
- Preserve compatibility or add a migration.
- Record why no change is needed.
- Record an unresolved risk when it cannot be addressed safely.

## 4. Treat placement changes as structural changes

Moving a component, header, navigation region, or document section can affect consumers that were not edited directly.

### UI header and navigation placement

Inspect:

- Parent layout flow, container dimensions, flex and grid relationships, and sibling positioning.
- Sticky and fixed offsets, scroll containers, stacking contexts, overlays, and z-index.
- Anchor targets, scroll margins, browser history restoration, and initial scroll behavior.
- Desktop, tablet, and mobile breakpoints, wrapping, overflow, and viewport clipping.
- Focus order, keyboard behavior, accessible names, landmarks, and heading structure.
- Every route and shared shell that renders the component.
- Route-specific styles, visual snapshots, interaction tests, and screenshot expectations.

Test at representative viewport sizes and with keyboard navigation. Check that content is not hidden behind fixed elements and that focus remains visible after navigation.

### Document heading and section placement

Inspect:

- Heading levels and the resulting document outline.
- Table of contents generation, navigation trees, and section numbering.
- Generated slugs, fragment identifiers, bookmarks, inbound links, and cross-references.
- Search metadata, rendered pages, generated documentation, and index output.
- References in other docs, examples, tests, and release notes.

Preserve existing public fragment identifiers where possible. If an identifier must change, add a compatibility anchor or redirect when the documentation platform supports it. Update every stale reference.

## 5. Implement in small increments

For each increment:

1. State which impact-map entries it addresses.
2. Make the smallest change that satisfies those entries.
3. Run focused tests or checks immediately.
4. Inspect the result in its actual context.
5. Add newly discovered effects to the impact map before continuing.

Do not batch several unrelated adjustments and then test only the final happy path.

## 6. Rebuild the impact map from the final diff

The original plan is only a hypothesis. The actual implementation is the evidence.

After editing:

1. Read the complete diff.
2. Search for every changed symbol, heading, identifier, route, selector, config key, and public interface.
3. Inspect all references and transitive consumers.
4. Compare actual changed files with the original impact map.
5. Add missing surfaces and outcomes.
6. Update dependent implementation, tests, docs, generated files, links, and compatibility measures.
7. Run the relevant focused checks, regression suite, type checks, lint, build, and integration tests.
8. Repeat the review after every follow-up adjustment.

If a correction changes placement or structure again, restart the relevant placement analysis. Do not assume the first impact review still applies.

## 7. Stop when the analysis converges

A change is ready only when:

- Every acceptance criterion has direct evidence.
- Every affected surface in the final impact map has been updated, tested, or deliberately left unchanged with a reason.
- The important failure and boundary outcomes have been checked.
- Existing public interfaces and references remain valid or have compatibility handling.
- The complete diff contains no unexplained changes.
- A full reference and dependency pass discovers no new affected surface.

If a check cannot run, state the exact limitation and residual risk. Do not replace missing evidence with confidence.

## 8. Keep a traceable record

For non-trivial work, record:

```markdown
## Change impact

- Intended change:
- Directly affected files and components:
- Transitive dependents:
- User-visible and runtime effects:
- Failure and boundary outcomes:
- Compatibility and migration effects:
- Documentation and generated outputs:
- Tests and verification:
- Rollback or recovery:
- Unchanged surfaces and why:
```

The record can live in the task plan or existing progress file. Do not create a new tracking file for a trivial edit.

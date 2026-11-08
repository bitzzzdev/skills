# Commit Message Examples

## Typo or tiny change

```
Fix typo in contact page heading
```

## Small fix

```
Stop nav overflowing at 360px width

Why: On narrow phones the five nav links wrapped under the logo and
pushed the page 40px wider than the viewport, causing sideways scroll.

Changes:
- `components/Nav.tsx`: links now collapse into the menu button below
  the `sm` breakpoint instead of wrapping

Verified: Checked at 360px, 390px and 768px in Chrome devtools. No
horizontal scroll at any of them.
```

## Normal feature

```
Add JWT login and refresh endpoints

Why: The dashboard needs authenticated API calls. Until now every route
was open, which was fine for the prototype but blocks the client demo.

Changes:
- `src/auth/login.ts`: POST /auth/login checks the password hash and
  returns a 15 minute access token and a 7 day refresh token
- `src/auth/refresh.ts`: POST /auth/refresh swaps a valid refresh token
  for a new access token and rotates the refresh token
- `src/middleware/requireAuth.ts`: verifies the access token and sets
  `req.user`. Applied to every route under `/api` except `/api/health`
- `.env.example`: added `JWT_SECRET` and `JWT_REFRESH_SECRET`

Decisions:
- Refresh tokens are stored hashed in the `sessions` table, not just
  signed. This lets us revoke one session without rotating the secret.
- Chose short-lived access tokens over server sessions because the
  frontend is hosted on a different domain and cookies were unreliable.

Gotchas:
- Both secrets must be set or the server exits at startup with a clear
  error. This is intentional.
- `requireAuth` must be registered before the route handlers. Order in
  `src/server.ts` matters.

Verified: `npm test` passes (42 tests, 9 new in `auth.test.ts`). Logged
in and refreshed manually with curl against a local server.
Status: complete
Next: password reset flow, tracked in issue 14.
```

## Refactor

```
Move image handling out of ProjectCard into lib/images

Why: `ProjectCard.tsx` had grown to 240 lines and three other components
needed the same srcset logic, so it was being copied.

Changes:
- `lib/images.ts`: new `buildSrcSet(path, widths)` helper
- `components/ProjectCard.tsx`, `Hero.tsx`, `Gallery.tsx`: use the helper
  instead of their own copies

No behavior change. Rendered HTML is identical for all three
components (compared before and after with a diff of the built output).

Verified: `npm run build` and `npm run lint` clean.
```

## Partial work

```
Start migrating storage from localStorage to IndexedDB

Why: localStorage hit the 5 MB limit for users with long histories.

Changes:
- `src/storage/idb.ts`: new IndexedDB wrapper with `get`, `set`, `list`
- `src/storage/index.ts`: reads try IndexedDB first, then fall back to
  localStorage

Status: partial. Reads are migrated. Writes still go to localStorage
only, so new data is not in IndexedDB yet.
Next: switch writes in `src/storage/index.ts`, add a one-time copy of
existing localStorage data, then remove the fallback.
Verified: not run. No tests cover the storage layer yet.
```

## Bad message and a better one

Bad:

```
update files
```

```
feat: implement robust authentication system leveraging JWT to ensure
seamless and secure user access
```

Better:

```
Add JWT login and refresh endpoints
```

with a body like the feature example above. The bad versions say nothing a reader can use. The better one names the change and, through its body, records the reason, the decisions and the traps.

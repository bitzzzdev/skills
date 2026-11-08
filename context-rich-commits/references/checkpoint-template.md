# Checkpoint Template

A checkpoint is an empty commit (`git commit --allow-empty`) whose message is a snapshot of the whole project. Write it from the actual repo state, not from memory. Open the files and run the commands before you claim anything.

The subject must start with `checkpoint:` so it can be found with `git log --grep='^checkpoint:'`.

## Required sections

Each section is a label at the start of a line, followed by a colon. The linter checks that these exist.

| Section | What goes in it |
|---|---|
| `Project:` | What the project is, who it is for, the stack and main dependency versions |
| `Run:` | Exact commands to install, run in development, build, test and lint. Env vars and services needed |
| `Structure:` | Top-level directories and the key files in each, one line each, saying what they are for |
| `Architecture:` | How the pieces fit: entry points, data flow, where state lives, external services |
| `Recent changes:` | What changed since the previous checkpoint, grouped by area, with commit hashes |
| `Current state:` | What works, what is broken, what is half done |
| `Next steps:` | Prioritized list of what to do next |
| `Previous checkpoint:` | Hash of the last checkpoint, or `none` for the first one |

## Optional sections

| Section | What goes in it |
|---|---|
| `Conventions:` | Naming, code style, patterns to follow, commit style |
| `Known issues:` | Bugs, limits, tech debt, with where to look |
| `Gotchas:` | Traps, hidden coupling, things that look wrong but are intentional |
| `Decisions:` | Standing decisions and why, including options that were rejected |
| `Deploy:` | Where and how it ships, and anything manual in the process |

## Rules

- Verify each claim against the repo. If you did not check it, leave it out or mark it unverified.
- Carry forward only what is still true. Remove anything that has gone stale.
- Use paths, commands and names. Avoid line numbers.
- No secrets, tokens or personal data.
- Keep it as short as the project allows. A small project gets a short checkpoint. Do not pad.
- Plain words, no emoji, no em dashes.

## Example

```
checkpoint: portfolio site redesign is live, contact form still stubbed

Project: Personal portfolio for a freelance web developer. Next.js 14
(App Router), TypeScript, Tailwind CSS 3, deployed on Vercel.

Run:
- Install: `npm install`
- Dev: `npm run dev` (http://localhost:3000)
- Build: `npm run build`, lint: `npm run lint`
- Needs `RESEND_API_KEY` in `.env.local` once the contact form is wired

Structure:
- `app/`: routes. `page.tsx` is the home page, `work/[slug]/page.tsx`
  renders one case study
- `components/`: UI pieces. `Hero.tsx`, `ProjectCard.tsx`, `Nav.tsx`
- `content/projects/*.mdx`: case study content, loaded in `lib/projects.ts`
- `public/assets/`: images, all pre-optimized to webp
- `lib/`: `projects.ts` (MDX loading), `seo.ts` (metadata helpers)

Architecture: Static generation for every route. Case studies are MDX
files read at build time by `lib/projects.ts`. No database, no API
routes yet. Theme is a CSS variable set on `<html>` by `Nav.tsx`.

Conventions: Components are PascalCase files with a default export.
Tailwind only, no CSS modules. Commit messages follow context-rich-commits.

Recent changes (since 3f2a9c1):
- Redesign: new hero, project grid and nav (a41be07, 77d0c3e)
- Case study pages from MDX (c92d5f1)
- Fixed mobile nav overflow at 360px (5be8812)

Current state: All pages render and deploy. The contact form in
`components/ContactForm.tsx` validates input but does not send anything.

Known issues:
- Lighthouse performance is 82 on mobile because of the hero video

Gotchas:
- `next.config.js` sets `images.unoptimized = true` on purpose, because
  images are already webp and the Vercel image quota is limited

Next steps:
1. Wire `ContactForm` to Resend through `app/api/contact/route.ts`
2. Replace the hero video with a poster image on mobile
3. Add case study for the second client project

Previous checkpoint: 3f2a9c1
```

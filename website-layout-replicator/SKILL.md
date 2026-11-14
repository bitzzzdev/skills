---
name: website-layout-replicator
description: Rebuild the layout, structure, and styling of a reference website URL while keeping our own text, data, and descriptions. Use when the user wants a page or site to look and be laid out like a reference, but with their own content.
---

# Website Layout Replicator

This skill rebuilds how a page looks and is organized from a reference URL. The content stays ours. The reference contributes structure and styling only.

## What is replicated and what is not

Replicated:
- Section order, grid, column counts, spacing, and alignment
- Typography scale, weights, line heights, and font families (use the same family only if it is licensed for our use, otherwise pick a close free alternative and say so)
- Colors, borders, radii, shadows, and hover or focus states
- Navigation pattern, header, footer, and component shapes (cards, tabs, accordions, forms)
- Responsive breakpoints and how the layout reflows

Not replicated:
- Text, headlines, product names, prices, testimonials, and any copy from the reference
- Logos, brand marks, photos, illustrations, icons, and fonts that we do not have rights to
- Source code copied verbatim from the reference
- Anything behind a login, paywall, or access block

Our content fills every text, data, and media slot. If a slot has no content from us, leave a clearly marked placeholder and list it in the report. Never fill it with reference copy.

## Inputs

Before starting, confirm:
1. The reference URL (or URLs) and which pages to match.
2. Where our content lives: a URL, a file, a CMS export, or pasted text.
3. The target stack (plain HTML and CSS, or the project's framework).
4. Whether the reference is ours, a competitor, or third-party. This decides how far the design can go, and it is stated in the report.

If an input is missing and the answer changes the result, ask. Otherwise state the assumption and continue.

## Workflow

### 1. Fetch the reference
- Fetch the page with WebFetch or the shell, whichever the network allowlist permits. If a request is refused, say so and ask the user for the HTML or a screenshot. Do not work around the refusal.
- Save the HTML, linked stylesheets, and the computed layout to a scratch directory. Keep the scratch directory outside the project.
- Take screenshots at mobile (375 px), tablet (768 px), and desktop (1280 px) widths when a browser is available.

### 2. Map the structure
Record the page as a tree of sections. For each section note:
- Its role (header, hero, feature grid, pricing table, footer, and so on)
- The layout method (flex, grid, absolute, float) and the column or row count
- Its spacing rhythm (padding, gap, max width)
- Its repeated components and how many times they repeat

Keep the tree short. One line per section is enough.

### 3. Extract the style system
- Collect the font stacks, sizes, weights, and line heights used for each text role (headline, body, label, caption).
- Collect the color palette and map it to roles (background, surface, text, accent, border).
- Collect the spacing and radius scale. Prefer a small set of tokens over one-off values.
- Note breakpoints from the media queries and how each section reflows at each one.

Write the tokens into CSS custom properties. Do not hard-code values in each rule.

### 4. Inventory our content
List every text node, data field, image, and link that our page needs, grouped by section. Keep our wording exactly as given. Do not rewrite it to match the reference's tone, length, or structure. If our text is longer or shorter, adjust the layout, not the text.

### 5. Build the page
- Use semantic elements (header, nav, main, section, article, footer) and real headings in order.
- Reproduce the layout with the same grid and spacing, using our tokens.
- Build components once and reuse them.
- Keep every interactive element reachable by keyboard and give it a visible focus state.
- Give images alt text from our content. Decorative images get an empty alt.
- Add no tracking, third-party scripts, or fonts unless our project already uses them.

### 6. Verify
- Compare screenshots side by side at the three widths. Note every visible difference that is not a deliberate change.
- Check that every item in the content inventory appears on the page, once, with our wording.
- Check that no reference text, logo, or image slipped into the output. Search the output for strings from the reference HTML.
- Check the page without CSS, with a keyboard, and with a screen reader if one is available.
- Run the project's build, lint, and tests. Report what actually ran.
- Scan new text with `human-writing` before committing.

### 7. Report
State:
- The reference URL and the date it was fetched.
- The sections matched and any that were simplified, with the reason.
- The fonts and assets used, and their license status.
- Placeholders left for missing content.
- Checks that ran, and checks that did not.

## Rules
- Our content is the only content on the page.
- Do not copy copyrighted text, images, or code from the reference.
- Do not bypass robots rules, logins, paywalls, or rate limits.
- Do not push to production. Work on `dev` or a feature branch and leave promotion to the user.
- Keep all written text free of emoji and em dashes.

# SEO checklist (public websites only)

Use for website projects and for the public landing page of other project types. Skip for native apps, mods, shaderpacks, bots and private tools.

## Per page
- One `<title>`, unique, under about 60 characters, main topic first.
- One meta description, unique, under about 160 characters, written for a person.
- One `<h1>`, then ordered headings.
- A canonical URL.
- Open Graph and Twitter card tags: title, description, image (1200 by 630), url.
- Descriptive link text and image `alt` text.
- Valid HTML with a `lang` attribute.

## Site level
- `robots.txt` that does not block pages or assets you want indexed, and points to the sitemap.
- `sitemap.xml` with only canonical, indexable URLs. Generate it from the routes, don't hand write it.
- HTTPS everywhere, one canonical host, redirects for old URLs.
- Real 404 status for missing pages, not a 200 with an error message.
- Structured data (JSON-LD) only for content that is really on the page: Organization, Article, Product, FAQ, Breadcrumb. Validate it.
- Pages that need JavaScript to show content must be server rendered or prerendered so crawlers see them.
- `noindex` on staging, admin and account pages.

## Speed and usability
Check Core Web Vitals with Lighthouse or PageSpeed Insights: largest content paint, layout shift, interaction delay. Compress images, size them, lazy load below the fold, preload the main font, ship less JavaScript. Check mobile layout and tap targets.

## Verify
Run Lighthouse (`npx lighthouse <url> --only-categories=seo,performance --quiet`) or read the page source. Look up the current Google Search Central guidance with error-docs-lookup rather than relying on memory, since the advice changes. Don't promise rankings in the report. Say what was checked and what passed.

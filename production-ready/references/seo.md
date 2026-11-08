# SEO checklist

Use this checklist for public website projects and public landing pages where search ranking and discoverability are desired.

If the `google-seo-skill` is installed, invoke it for a complete audit based on Google Search Central guidelines (covering crawlability, structured data, canonical URLs, and generative AI search / AI Overviews). Before running the audit, check if any update to `google-seo-skill` is available from git (`python scripts/update_seo_skill.py`) and pull it first. After pulling updates, commit and push them to the skills repo.

## When to avoid SEO ranking optimization

If the project is a personal project, private repository, internal tool, staging environment, or any site where search indexing is not desired:
- **Do NOT optimize for search ranking.**
- **Enforce indexing prevention**:
  - Add `<meta name="robots" content="noindex, nofollow">` in the `<head>` of all pages.
  - Set `X-Robots-Tag: noindex, nofollow` HTTP headers on all served responses.
  - Set `User-agent: *\nDisallow: /` in `robots.txt` if crawlers should not visit the site.
  - Do not publish public `sitemap.xml` files containing private internal routes.
  - Restrict access with authentication or IP allowlists where applicable.

## Per page (public sites needing ranking)

- One `<title>`, unique, under 60 characters, main topic first.
- One meta description, unique, 1 to 2 sentences, under 160 characters, written for a person.
- One `<h1>`, followed by logical heading order.
- A canonical URL (`rel="canonical"`).
- Open Graph and Twitter card tags: title, description, image (1200 by 630), url.
- Descriptive link text (avoid "click here") and image `alt` text.
- Valid HTML with a `lang` attribute.

## Site level (public sites needing ranking)

- `robots.txt` that allows indexing of public assets and routes, pointing to `sitemap.xml`.
- `sitemap.xml` with only canonical, indexable URLs generated from routes.
- HTTPS everywhere, one canonical domain host, and 301 redirects for legacy URLs.
- Real 404 status codes for missing pages, not a 200 with an error template.
- Structured data (JSON-LD) only for real page content (Organization, Article, Product, FAQ, Breadcrumb).
- Server-rendered or prerendered content for JavaScript-heavy frameworks (Next, Nuxt, Astro).
- `noindex` on staging, admin, and authenticated account pages.

## Speed and usability

- Check Core Web Vitals (Largest Contentful Paint, Cumulative Layout Shift, Interaction to Next Paint).
- Compress images, specify dimensions, and lazy-load below the fold.
- Preload critical fonts and bundle less JavaScript.
- Verify mobile responsiveness and tap target spacing.

## Verification

When `google-seo-skill` is installed, run through its self-review checklist. Otherwise, run Lighthouse (`npx lighthouse <url> --only-categories=seo,performance --quiet`) or inspect page source. Report what was verified and what passed. Do not promise specific search rankings in the final report.

# Legal, Privacy, Attribution, and Community Rules

These guidelines help agents draft enterprise-grade documentation and legal files for software releases. They are drafting aids based on project architecture and actual codebase behavior, not formal legal advice. Use clear placeholders like `[COMPANY NAME]`, `[CONTACT EMAIL]`, `[JURISDICTION]`, `[EFFECTIVE DATE]`, `[SECURITY EMAIL]`, and `[DPO CONTACT]` for any unknown fact. Never invent company details, dates, or legal jurisdictions. List every placeholder in the release report. Remind the user that generated legal texts are starting drafts requiring qualified legal counsel before official publication.

## Corporate Release Level Document Suite

A complete commercial or high-profile open-source launch requires nine core documentation assets:

1. **Terms of Service or Terms of Use (`TERMS.md` or `TERMS_OF_SERVICE.md`)**: Defines legal terms between operator and user.
2. **Privacy Policy (`PRIVACY.md`)**: Documents actual data collected, storage, user rights, and retention.
3. **License (`LICENSE`)**: Explicit license governing usage, modification, and distribution.
4. **Third-Party Credits and Attribution (`CREDITS.md` or `NOTICE`)**: Details all open-source packages, bundled assets, fonts, and external APIs with copyright and license notices.
5. **Security Policy (`SECURITY.md`)**: Defines supported versions, vulnerability disclosure channels, response timelines, and safe harbor protections.
6. **Contributing Guidelines (`CONTRIBUTING.md`)**: Details setup, branching rules, testing expectations, pull request workflows, and review criteria.
7. **Code of Conduct (`CODE_OF_CONDUCT.md`)**: Community standards based on established industry templates such as Contributor Covenant 2.1.
8. **Changelog (`CHANGELOG.md`)**: Chronological release history adhering to Keep a Changelog and Semantic Versioning.
9. **Environment Configuration Template (`.env.example`)**: Documents all environment variables with non-secret dummy defaults.

## Decision Trees by Project Architecture

### 1. Public SaaS, Consumer Web App, or Hosted Platform

When users create accounts, store data, or access a hosted service:

- `TERMS.md`: Required. Must cover accounts, acceptable use, subscriptions, service availability, user content, liability caps, and dispute resolution.
- `PRIVACY.md`: Required. Must audit actual cookies, session tokens, analytics, database models, payment gateways, and third-party APIs.
- `LICENSE`: Required. Proprietary All Rights Reserved for closed platforms, or commercial open-source license.
- `CREDITS.md` or `NOTICE`: Required. Covers all frontend and backend dependencies, bundled assets, and web fonts.
- `SECURITY.md`: Required. Provides a dedicated security contact and vulnerability disclosure SLA.
- `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`: Recommended if public contributors are accepted; optional for private teams.

### 2. Public API or Developer Platform

When providing programmatic endpoints, SDKs, or developer webhooks:

- `TERMS.md`: Required. Focus on API keys, rate limits, acceptable query volume, uptime disclaimers, data caching limits, and revocation rights.
- `PRIVACY.md`: Required. Detail API payload logging, IP capture, telemetry, and developer account handling.
- `SECURITY.md`: Required. High priority due to exposed network endpoints; include API vulnerability scope.
- `CREDITS.md`: Required for SDKs or public client libraries.
- `LICENSE`: Required.

### 3. Native Mobile Application (iOS or Android)

When distributing binaries via app stores:

- `TERMS.md`: Required. Mobile End User License Agreement (EULA) complying with Apple App Store and Google Play distribution terms.
- `PRIVACY.md`: Required. Mandatory app store requirement. Must account for device permissions (camera, location, contacts, notifications, storage) and embedded analytics SDKs.
- `CREDITS.md`: Required. Compiles third-party notices for all compiled dependencies (frequently displayed in app "About" or "Legal" screens).
- `SECURITY.md`: Required.

### 4. Open-Source Library, Tool, or Framework

When publishing packages to npm, PyPI, crates.io, Go modules, or GitHub:

- `LICENSE`: Required. Permissive (MIT, Apache-2.0, BSD) or copyleft (GPL-3.0, AGPL-3.0). Never change without explicit instruction.
- `README.md`: Required. Clear quickstart and usage examples.
- `CHANGELOG.md`: Required. SemVer and Keep a Changelog.
- `CREDITS.md` or `NOTICE`: Recommended. Required if using Apache-2.0 dependencies with NOTICE files, or when bundling vendor code.
- `CONTRIBUTING.md`: Recommended. Local setup, testing, and pull request rules.
- `CODE_OF_CONDUCT.md`: Recommended. Contributor Covenant 2.1.
- `SECURITY.md`: Recommended. Defines which library versions receive security patches.
- `TERMS.md` and `PRIVACY.md`: Optional. Omit unless the library collects telemetry or connects to a hosted service.

### 5. Private Commercial Software, Internal Tools, or Personal Projects

When the repository is private, marked `"private": true` in `package.json`, or intended for internal company use:

- Default posture: Skip consumer terms of service, public privacy policies, and public community files.
- Focus on code quality, build verification, test suites, credential safety, changelog, `.env.example`, internal README, and proprietary license notices.
- Explicit user override (`--force-release`): When the user requests enterprise production readiness for an internal or commercial project, generate the full commercial suite:
  - Commercial Terms of Use (for internal or business customers).
  - Internal Security Vulnerability Policy (internal reporting channels and escalation paths).
  - Third-Party Credits (`CREDITS.md` / `NOTICE`) to ensure corporate open-source license compliance.
  - Proprietary License statement.

### 6. User Opt-Outs and Preferences

When the user specifies "skip terms", "no license needed", "don't generate privacy policy", or passes `--skip-legal`:

- Immediately honor the user's decision without argument.
- Do not generate the excluded files.
- Record the omitted files as USER-EXCLUDED in the audit output and final report rather than reporting them as missing.

## Terms of Service Architecture

When drafting `TERMS.md` or `TERMS_OF_SERVICE.md`, cover these eleven standard sections:

1. **Eligibility and Agreement**: Minimum age requirement (typically 13 or 16 depending on jurisdiction), legal capacity to enter into contracts, authority to represent an organization if using on behalf of a company, and condition that use constitutes acceptance.
2. **User Accounts and Security**: Account creation rules, accurate information requirement, responsibility for credential security, prompt notification of unauthorized access, and right to suspend unverified accounts.
3. **Acceptable Use and Prohibitions**: Clear prohibitions against reverse engineering, security probing without authorization, rate limit circumvention, automated scraping without permission, transmitting malware, harassing others, or infringing third-party rights.
4. **User-Generated Content**: Ownership remains with user, license granted to operator to host, display, and process content solely to deliver the service, user representation of necessary rights, and DMCA / copyright takedown process.
5. **Intellectual Property**: Operator ownership of application code, interface design, logos, trademarks, and documentation. Explicit feedback license granting operator right to implement suggested improvements without obligation.
6. **Third-Party Services and Integrations**: Disclaim responsibility for external services, APIs, identity providers, and payment processors connected by the user.
7. **Fees, Billing, and Subscriptions (if applicable)**: Pricing terms, billing cycles, renewal policies, cancellation mechanics, refund policy (or all sales final statement), and responsibility for applicable taxes.
8. **Termination and Suspension**: Operator right to suspend or terminate accounts for breach of terms, user right to cancel at any time, and post-termination provisions (data retrieval window, survival of clauses).
9. **Disclaimer of Warranties**: Provided "as is" and "as available". Disclaimer of implied warranties including merchantability, fitness for a particular purpose, and non-infringement.
10. **Limitation of Liability**: Exclusion of consequential, indirect, special, and punitive damages. Aggregate liability cap (typically limited to fees paid in previous 12 months or a nominal sum like $100).
11. **Governing Law and Dispute Resolution**: Choice of law `[JURISDICTION]`, venue for legal proceedings, mandatory informal dispute resolution period, binding arbitration provision, and class action waiver.

## Privacy Policy Architecture and Codebase Audit

Do not write a generic privacy policy. Audit the actual codebase before drafting:

### Codebase Audit Checklist

- Authentication: Inspect login flows, session handlers, JWT signatures, OAuth providers (Google, GitHub, Apple), password hashing libraries (bcrypt, argon2).
- Client storage: Inspect `localStorage`, `sessionStorage`, `IndexedDB`, and cookie setters. Identify whether cookies are strictly necessary, functional, or tracking.
- Analytics and monitoring: Look for Google Analytics, Mixpanel, PostHog, Segment, Datadog, Sentry, Bugsnag, or custom telemetry endpoints.
- Payment processing: Check for Stripe, PayPal, Braintree, Lemon Squeezy SDKs. Note that raw card details should never hit the application database.
- Third-party APIs: Identify external APIs that receive user data (OpenAI, AWS S3, Resend, Sendgrid, Twilio).
- Database models: Inspect schemas (Prisma, TypeORM, SQLAlchemy, Mongoose, migrations) for PII fields (email, phone, address, IP, device identifiers).

### Privacy Policy Core Sections

1. **Information We Collect**: Divided into data provided directly by user (registration details, profile, communications), data collected automatically (IP address, browser type, device info, usage telemetry, cookies), and data from third parties (OAuth profiles).
2. **How We Use Information**: Specific purposes (authenticating users, processing transactions, preventing fraud, providing customer support, sending service notices).
3. **Legal Bases for Processing (GDPR Article 6)**: Contractual necessity (delivering the service), legitimate business interests (security, product stability), legal obligations (tax and compliance), and user consent (optional marketing or cookies).
4. **Data Sharing and Third-Party Subprocessors**: Categories of recipients (cloud hosting providers, payment processors, customer support tools). State that personal data is never sold.
5. **International Transfers**: Safeguards used when transferring data across borders (EU Standard Contractual Clauses, UK International Data Transfer Agreements, adequacy decisions).
6. **Data Retention and Deletion**: Retention periods tied to account lifetime plus legal requirement windows. Automated or manual deletion workflows upon account closure.
7. **User Rights (GDPR, CCPA/CPRA, and Global Laws)**: Right to access, rectify, delete, restrict processing, and port personal data. CCPA/CPRA rights: right to know, delete, correct, opt-out of sale/sharing, and non-discrimination. Dedicated instructions for exercising rights via `[CONTACT EMAIL]`.
8. **Security Practices**: Technical and organizational safeguards: encryption in transit (TLS 1.3), encryption at rest (AES-256), strict role-based access control, periodic vulnerability scans.
9. **Children's Privacy**: Clear declaration that the service is not directed to children under 13 (or 16 in the EU/UK) and commitment to delete data if inadvertent collection occurs.
10. **Changes to This Policy**: Mechanics of policy updates and notification methods for material changes.
11. **Contact Information**: Clear privacy contact address `[CONTACT EMAIL]` and physical mailing placeholder `[PHYSICAL ADDRESS]`.

## Security Vulnerability Policy (`SECURITY.md`)

A professional security policy must include:

1. **Supported Versions**: A markdown table showing which major or minor versions currently receive security fixes and which are end-of-life.
2. **Reporting Process**: Step-by-step instructions for submitting vulnerability reports privately. Direct reports to `[SECURITY EMAIL]` or a private GitHub Security Advisory / disclosure platform. Request detailed reproduction steps, proof-of-concept, and environment details.
3. **Response Timelines and SLA**: Commitment to acknowledge reports within 48 to 72 hours, provide a triage and severity assessment within 5 business days, and provide regular progress updates until a patch is released.
4. **Safe Harbor / Responsible Disclosure**: Explicit commitment that security researchers acting in good faith, avoiding privacy violations, data destruction, and service interruption will not face legal action or account termination.
5. **Out of Scope**: Clear listing of non-qualifying issues (denial of service attacks, social engineering, physical attacks, issues in unmaintained third-party dependencies without proof of exploitability).

## Third-Party Credits and Attribution (`CREDITS.md` or `NOTICE`)

Failing to provide open-source notices can violate licenses (including MIT and Apache 2.0). A complete `CREDITS.md` or `NOTICE` contains:

1. **Package Inventory**: Direct dependencies categorized by runtime and build tools.
2. **Per-Package Information**:
   - Package name and version
   - Upstream repository or project URL
   - Copyright holders
   - License type (MIT, Apache-2.0, BSD-3-Clause, ISC)
   - Required notice text or license reproduction where mandated by upstream terms.
3. **Non-Code Assets**: Attribution for bundled web fonts (such as Inter, Roboto under OFL or Apache), icon packages (Lucide, Feather), audio, video, or image assets.
4. **Dependency Audit Commands**:
   - Node: `npm list --depth=0` and `npx license-checker --summary`
   - Python: `pip list` and `pip-licenses`
   - Rust: `cargo license`
   - Go: `go list -m all`

## Contributing Guidelines (`CONTRIBUTING.md`)

Cover operational workflow for team members and external contributors:

1. **Prerequisites and Setup**: Required runtimes, package managers, and setup commands.
2. **Branching Strategy**: Branch naming conventions (`dev`, `feat/*`, `fix/*`). Emphasize that all work integrates through `dev` first.
3. **Testing and Verification**: Commands to run test suites, linters, and type checkers. Require tests for bug fixes and new features.
4. **Commit Message Format**: Follow `context-rich-commits` (why, changes, decisions, verified result).
5. **Pull Request Protocol**: PR title conventions, linked issues, checklist of completed checks, and review process.

## Code of Conduct (`CODE_OF_CONDUCT.md`)

Adopt the standard Contributor Covenant 2.1:

- Our Pledge: Positive, inclusive, harassment-free experience for everyone.
- Standards: Welcoming language, respecting differing viewpoints, accepting constructive feedback, focusing on community benefit.
- Unacceptable Behavior: Harassment, trolling, derogatory comments, personal attacks, publishing private information without consent.
- Enforcement and Reporting: Contact details `[CONTACT EMAIL]`, investigation procedure, confidentiality commitment, and enforcement actions (correction, warning, temporary ban, permanent ban).

## License Selection and Rules (`LICENSE`)

- Permissive licenses like MIT (minimal restrictions), Apache-2.0 (permissive with explicit patent grant and NOTICE requirement), or BSD-2/3-Clause.
- Copyleft licenses like GPL-3.0 (strong copyleft, modifications must be GPL), or AGPL-3.0 (network copyleft for hosted services).
- Proprietary licenses like Commercial All Rights Reserved (closed-source, internal tools, proprietary SaaS).
- Rule of integrity: Never guess or change an existing license without explicit user authorization. If no license exists, present the options and ask.

## Integrity and Human Writing Rules

- Never invent facts: Do not invent names, dates, addresses, or phone numbers.
- Always use explicit placeholders: `[COMPANY NAME]`, `[CONTACT EMAIL]`, `[JURISDICTION]`, `[SECURITY EMAIL]`, `[EFFECTIVE DATE]`.
- Clearly state in reports that legal documents are initial drafts that need professional legal review prior to production launch.
- Zero em dashes, zero emoji, and natural human tone throughout all documentation.

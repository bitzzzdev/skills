# Terms, privacy and project rules

These are drafting aids, not legal advice. Fill from the project's real behavior. Use `[PLACEHOLDER]` for anything unknown and list every placeholder in the report.

## Which files does this project need?

| Project type | Add |
|---|---|
| Open source library or tool | LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md |
| Hosted app, site or SaaS with accounts | Terms of Service, Privacy Policy, plus the above that apply |
| Bot (Discord, Slack, Telegram) | Terms, privacy, and a rules page for users |
| API offered to others | Terms of use, acceptable use and rate limits, privacy |
| Mobile app | Terms, privacy (stores require a privacy URL), data safety answers |
| Game server or community | Rules page, ban and appeal process, privacy if data is stored |

Check what exists first. Extend it, don't replace it.

## Find out what the project collects
Read the code, config and dependencies before writing the privacy policy.

- Accounts: email, username, password hashes, OAuth providers.
- Analytics, error tracking, ads SDKs (Google Analytics, Sentry, Firebase, Meta).
- Cookies and local storage, and what they hold.
- Payments and which processor handles them.
- Uploads, messages, logs, IP addresses.
- Where data is stored and which third parties receive it.
- Retention and how a user deletes their account or data.

## Terms of Service outline
1. Who we are and what the service is.
2. Acceptance and who may use it (minimum age).
3. Accounts and security.
4. Acceptable use and prohibited behavior.
5. User content and the license the user grants.
6. Payments, refunds and cancellation, if any.
7. Intellectual property.
8. Third-party services.
9. Termination and suspension.
10. Disclaimers and limits of liability. Mark for lawyer review.
11. Changes to the terms and how users are told.
12. Governing law and contact. `[JURISDICTION]`, `[CONTACT EMAIL]`.

## Privacy Policy outline
What is collected, why, the legal basis if GDPR applies, who it is shared with, how long it is kept, user rights (access, deletion, export, opt out), cookies, children, security, international transfers, changes, contact.

## Project rules (contribution, community or usage)
Write rules the project can enforce or that maintainers will actually apply. Each rule: what is expected, what happens when broken. Examples: how to open an issue, branch and commit rules, review expectations, code of conduct contact, bot command limits, rate limits, report and appeal steps.

## Always flag for review
Payments, children under 13 or 16, health or financial data, biometric data, users in the EU, UK or California, marketplace or user-generated content with liability exposure, and any claim of compliance. Say these need a lawyer. Don't write "GDPR compliant" or "COPPA compliant".

## License choice
Don't pick for the user. Show the common options briefly (MIT permissive, Apache-2.0 permissive with a patent grant, GPL-3.0 copyleft, proprietary all rights reserved) and ask. If a LICENSE file exists, keep it.

## Style
Plain sentences, short, with defined terms. No legalese for its own sake, no emoji, no em dashes. Run human-writing's scanner on the result.

# AI Writing Tells: Full Reference

Read this when drafting anything longer than a few lines, or when cleaning up existing text. Nothing here is banned by itself except punctuation and emoji (see the hard rules in SKILL.md). The vocabulary and structure items are tells because of how often and how densely AI text uses them. One "robust" in a long document is fine. Three in a page is a signal. When in doubt, use the plain word.

Contents:
1. Punctuation and symbols
2. Vocabulary
3. Phrases
4. Sentence and paragraph structure
5. Formatting
6. Openers and closers
7. Code and technical text
8. Replacement guide

## 1. Punctuation and symbols

Hard bans:
- Em dash. Replace with a comma, period, colon, parentheses, or restructure.
- En dash used as punctuation. For ranges use a hyphen or "to".
- Horizontal bar, and a spaced double hyphen used as a dash.
- Emoji and emoji-like symbols: checkmark and cross marks, sparkles, rocket, stars, warning sign, light bulb, target, fire, party popper, pointing hands, colored circles used as status dots.

Soft signals:
- Curly quotes in code or config (they're also a bug risk). Use straight quotes.
- Arrow symbols used as connectors in prose. Write "then" or restructure.
- Exclamation marks used for enthusiasm. One in a friendly message is fine, several is a tell.
- Semicolons used to join clauses in casual text. Most people use a period.
- Colon reveals: "The result? Faster builds." Rhetorical question followed by an answer.

## 2. Vocabulary

Verbs: delve, leverage, utilize, harness, unlock, unleash, elevate, empower, foster, streamline, supercharge, navigate (figurative), embark, showcase, underscore, highlight (as a lazy verb), resonate, revolutionize, transform (figurative), enhance, facilitate, bolster, spearhead, cultivate.

Adjectives: seamless, robust, comprehensive, crucial, pivotal, vital, paramount, cutting-edge, state-of-the-art, innovative, dynamic, vibrant, bustling, meticulous, intricate, nuanced, multifaceted, holistic, transformative, groundbreaking, game-changing, tailored, bespoke, effortless, intuitive, user-centric, scalable (when meaningless), blazing-fast, feature-rich, best-in-class, next-generation.

Nouns: tapestry, testament, landscape (figurative), realm, journey, ecosystem (figurative), synergy, beacon, cornerstone, plethora, myriad, paradigm, game-changer, deep dive, takeaway, pain points, stakeholders (in casual text), solutions (as a vague noun).

Adverbs: seamlessly, effortlessly, meticulously, ultimately, essentially, fundamentally, significantly (without a number), notably, importantly, crucially.

## 3. Phrases

- it's important to note that / it's worth noting that / it's worth mentioning
- in today's fast-paced world / in the ever-evolving landscape of / in the digital age
- plays a crucial (or pivotal, vital) role
- a testament to
- at the end of the day
- when it comes to
- in the realm of
- dive into / deep dive / let's explore / let's unpack / let's break this down
- whether you're a beginner or an expert
- look no further
- take it to the next level
- the key takeaway is
- by leveraging
- ensuring that
- in order to (just write "to")
- due to the fact that (write "because")
- a wide range of / a variety of / a plethora of
- not only ... but also
- navigate the complexities of
- choose one before publishing / choose a license before releasing
- the license is not selected yet / the license has not been chosen
- replace this with your / insert your details here
- note to developer / note to the user / note to author

## 4. Sentence and paragraph structure

- **Contrast framing.** "It's not just X, it's Y." "This isn't about A. It's about B." "More than just a tool." One use is fine, a document full of them is a tell.
- **Rule of three.** Three adjectives, three bullets, three examples, always three. Real lists vary: two items, four items, one.
- **Uniform rhythm.** Every sentence 15 to 22 words, every paragraph 3 to 4 sentences. Mix it up.
- **Tidy paragraph endings.** Each paragraph closing on a neat one-line moral.
- **Mirror structure.** Section openers and closers that restate each other.
- **Throat-clearing.** A sentence that announces what the next sentence will say.
- **Hedge stacks.** "May potentially help to somewhat improve."
- **False balance.** "There are pros and cons to both" with no recommendation.
- **Vague attribution.** "Experts say", "studies show", "many developers find" with no source.
- **Abstract nouns where a person or action belongs.** "The implementation of authentication facilitates secure access" instead of "Login uses JWT."
- **Inflated significance.** Treating a small utility or a routine change as a milestone.
- **Present-participle tails.** "..., ensuring a smooth experience", "..., highlighting the importance of..."

## 5. Formatting

- Headings on short content. If it fits in a few paragraphs, skip headings.
- A bullet list where a sentence would do.
- Bold lead-in on every bullet: "**Performance:** ...", "**Security:** ...".
- Bold sprinkled on random phrases for emphasis.
- Title Case On Every Heading. Use sentence case.
- Numbered steps for things that aren't sequential.
- A table for two or three data points.
- Horizontal rules between every section.
- A "Summary", "Conclusion", "TL;DR" or "Key Takeaways" section that repeats the content above it.
- Perfectly parallel bullets, all starting with the same verb form and ending the same way.

## 6. Openers and closers

Openers to cut:
- "Great question!" / "That's a great point!" / "Excellent choice!"
- "Certainly!" / "Absolutely!" / "Of course!" / "Sure thing!"
- "I'd be happy to help with that."
- "I hope this email finds you well."
- Restating the question back before answering.
- "In this article/guide, we will explore..."

Closers to cut:
- "I hope this helps!"
- "Feel free to reach out if you have any questions."
- "Let me know if you'd like me to elaborate."
- "In conclusion," / "In summary," / "Overall," / "Ultimately,"
- A final paragraph that restates the whole answer.
- Offering a menu of follow-ups at the end of every reply.

A natural ending is the last useful thing. If a next step genuinely exists, name it once, specifically ("Send me the staging URL and I'll check it").

## 7. Code and technical text

Comments:
- Comments that restate the line below them ("Initialize variable", "Loop through array", "Return the result").
- Banner comments and ASCII section dividers.
- "Helper function to..." and "This function..." openers.
- Full JSDoc or docstring blocks on trivial functions, with every param described by its own name.
- Comments in perfect grammar on every block while the code around them has none.
- TODOs and placeholder comments ("add error handling here") left in finished code.

Names and structure:
- Very long descriptive names (`handleUserAuthenticationDataSubmission`).
- A try/catch around everything that just logs the error generically.
- Defensive checks for cases that can't happen.
- Wrapper functions and abstraction layers for a single use.

Output text:
- Emoji in console.log, logger calls, CLI output, test names, commit messages and README headings.
- "Successfully" in every success message.
- "Oops!" and "Something went wrong" error text with no detail.
- Over-friendly CLI banners.

Commits, PRs, docs:
- Emoji or gitmoji prefixes.
- "feat: implement robust ... leveraging ... to ensure ..."
- PR bodies with Summary / Changes / Testing sections when the change is three lines.
- READMEs with emoji section titles, badge walls, a "Features" list of adjectives, and a table of contents on a short file.
- Assistant coaching and meta-instructions left in deliverables ("The license is not selected yet. Choose one before publishing: MIT, Apache-2.0, GPL-3.0, or a proprietary notice.", "Replace this with your API key", "Remember to configure this", "Note to developer:").
- Writing as an outside observer or assistant instead of as the project owner. Every file must be written with the direct authority of the creator or maintainer.

## 8. Replacement guide

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| facilitate | help, let |
| in order to | to |
| due to the fact that | because |
| a plethora of, a myriad of | many, a lot of, or a number |
| showcase | show |
| embark on | start |
| delve into | look at |
| seamless | (say what actually works: "no manual steps") |
| robust | (say what it handles: "retries on timeout") |
| comprehensive | (say what's covered) |
| it's worth noting that X | X |
| plays a crucial role in | (say what it does) |
| not just X but Y | Y |
| ensuring a smooth experience | (cut, or state the concrete effect) |
| Successfully saved! | Saved |
| Oops! Something went wrong | (say what failed) |
| The license is not selected yet. Choose one before publishing: ... | Distributed under the MIT License. See LICENSE for details. (or: Copyright 2026 [OWNER]. All rights reserved.) |
| Note to developer: remember to replace this with your key | Read API_KEY from environment |

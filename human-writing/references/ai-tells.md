# AI Writing Tells: Full Reference

Read this when drafting anything longer than a few lines, or when cleaning up existing text. Nothing here is banned by itself except punctuation and emoji (see the hard rules in `SKILL.md`). The vocabulary and structure items are tells because of how often and how densely AI text uses them. Use the plain word when it carries the same meaning.

Contents:
1. Punctuation and symbols
2. Vocabulary
3. Phrases
4. Sentence and paragraph structure
5. Owner voice and point of view
6. Formatting
7. Openers and closers
8. Code and technical text
9. Replacement guide

## 1. Punctuation and symbols

Hard bans:
- Em dash. Replace it with a comma, period, colon, parentheses, or restructure.
- En dash used as punctuation. For ranges use a hyphen or "to".
- Horizontal bar, and a spaced double hyphen used as a dash.
- Emoji and emoji-like symbols: checkmarks, crosses, sparkles, rockets, stars, warning signs, light bulbs, targets, fire, party poppers, pointing hands, and colored status dots.

Soft signals:
- Curly quotes in code or config. Use straight quotes.
- Arrow symbols used as connectors in prose. Write "then" or restructure.
- Exclamation marks used for enthusiasm.
- Semicolons joining clauses in casual text.
- Rhetorical colon reveals such as "The result? Faster builds."

## 2. Vocabulary

Verbs: delve, leverage, utilize, harness, unlock, unleash, elevate, empower, foster, streamline, supercharge, navigate (figurative), embark, showcase, underscore, highlight (as a lazy verb), resonate, revolutionize, transform (figurative), enhance, facilitate, bolster, spearhead, cultivate.

Adjectives: seamless, robust, comprehensive, crucial, pivotal, vital, paramount, cutting-edge, state-of-the-art, innovative, dynamic, vibrant, bustling, meticulous, intricate, nuanced, multifaceted, holistic, transformative, groundbreaking, game-changing, tailored, bespoke, effortless, intuitive, user-centric, scalable (when meaningless), blazing-fast, feature-rich, best-in-class, next-generation.

Nouns: tapestry, testament, landscape (figurative), realm, journey, ecosystem (figurative), synergy, beacon, cornerstone, plethora, myriad, paradigm, game-changer, deep dive, takeaway, pain points, stakeholders (in casual text), solutions (as a vague noun).

Adverbs: seamlessly, effortlessly, meticulously, ultimately, essentially, fundamentally, significantly (without a number), notably, importantly, crucially.

## 3. Phrases

- "It's important to note that" and "it's worth noting".
- "In today's fast-paced world" and "in the ever-evolving landscape".
- "Plays a crucial role" and "a testament to".
- "At the end of the day" and "when it comes to".
- "Dive into", "deep dive", "let's explore", and "let's unpack".
- "Whether you're a beginner or an expert".
- "Look no further" and "take it to the next level".
- "The key takeaway is".
- "By leveraging" and "ensuring that".
- "In order to" when "to" works.
- "Due to the fact that" when "because" works.
- "A wide range of", "a variety of", and "a plethora of".
- Artificial contrast framing: "not only X but also Y", "not just X but Y".
- "Choose one before publishing", "the license is not selected yet".
- "Replace this with your", "insert your details here", and "note to developer".

## 4. Sentence and paragraph structure

- Repeated "It's not just X, it's Y" framing.
- Exactly three adjectives, bullets, or examples in every section.
- Uniform sentence length and paragraph size.
- Tidy one-line morals at the end of every paragraph.
- Section openers and closers that repeat each other.
- Throat-clearing that announces the next sentence.
- Stacked hedges such as "may potentially help to somewhat improve".
- False balance with no recommendation.
- Vague attribution such as "experts say" or "studies show" without a source.
- Abstract nouns where a person or action belongs.
- Inflated significance for routine changes.
- Present-participle tails that add no concrete information.

## 5. Owner voice and point of view

The main maintainer's voice is the default for project content on every branch. Do not switch to an outside-observer voice for development branches, production branches, references, or handoffs.

Use first person when writing about the maintainer's own work, choices, intent, experience, recommendations, and progress. For a solo-maintained project, use "I". Use "we" only for a real team voice.

Avoid:
- "The developer created this project..."
- "The maintainer decided..."
- "The author recommends..."
- "The project was built by..."
- "The next agent should..."
- "The assistant could not verify..."
- "As an AI language model..."

Prefer:
- "I built this project..."
- "I chose this approach..."
- "I recommend..."
- "I could not verify..."
- "Next, run..."
- Direct technical statements such as "The CLI reads the config file."

Do not force first person into product behavior, API definitions, commands, UI labels, legal notices, or third-party attribution. Keep facts accurate. Never claim another contributor's work or an unrun test as your own. Read `references/owner-voice.md` for the full rule and examples.

## 6. Formatting

- Headings on short content.
- Bullets where a sentence would do.
- Bold lead-ins on every bullet.
- Random bold emphasis.
- Title Case On Every Heading. Use sentence case.
- Numbered steps for non-sequential content.
- Tables for two or three data points.
- Horizontal rules between every section.
- A summary or conclusion that repeats the content above it.
- Perfectly parallel bullets with identical grammar.

## 7. Openers and closers

Cut openers such as "Great question", "Certainly", "I'd be happy to help", and question restatements.

Cut closers such as "I hope this helps", "Feel free to reach out", "Let me know if you'd like me to elaborate", and repeated summaries. End with the last useful point.

## 8. Code and technical text

Comments:
- Comments that restate the next line.
- Banner comments and ASCII dividers.
- "Helper function to..." and "This function..." openers.
- Trivial docstrings that repeat parameter names.
- TODO placeholders left in finished code.

Names and structure:
- Overly long names.
- Generic try/catch blocks that hide the actual error.
- Defensive checks for impossible states.
- Abstractions used only once without a reason.

Output text:
- Emoji in logs, CLI output, test names, commit messages, and README headings.
- "Successfully" in every success message.
- "Oops" and "Something went wrong" without a useful error.
- Over-friendly CLI banners.

Commits, PRs, and docs:
- Emoji or gitmoji prefixes.
- Inflated commit subjects.
- PR templates that add no useful information.
- Assistant coaching or maintainer instructions left in deliverables.
- Writing as an outside observer or AI instead of as the main maintainer.

## 9. Replacement guide

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| facilitate | help, let |
| in order to | to |
| due to the fact that | because |
| a plethora of, a myriad of | many, a number of |
| showcase | show |
| embark on | start |
| delve into | look at |
| seamless | state what works without manual steps |
| robust | state the cases handled |
| comprehensive | state what is covered |
| it's worth noting that X | X |
| plays a crucial role in | state what it does |
| not just X but Y | Y |
| ensuring a smooth experience | state the concrete effect or cut it |
| Successfully saved! | Saved |
| Oops! Something went wrong | state what failed |
| The license is not selected yet. Choose one before publishing | state the actual license and link to its file |
| Note to developer: remember to replace this with your key | Read the key from the environment |

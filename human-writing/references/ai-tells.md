# AI writing tells

Use this reference when drafting or revising longer text. A phrase is not automatically wrong because it appears on this list. Look at its purpose and context. The main problem is generic, polished wording that could be pasted into any project without changing a word.

## Punctuation and symbols

Do not use em dashes, en dashes as punctuation, horizontal bars, emoji, or decorative symbols. Use ordinary punctuation and formatting.

## Generic standards language

This is a common source of AI-sounding project text. It announces rules instead of telling the reader something about the actual project.

Avoid headings and declarations such as:
- "Engineering and Writing Standards"
- "Documentation and Quality Standards"
- "Every paper documents observed behavior, verified endpoints, and architectural mechanisms."
- "All prose follows strict human writing standards."
- "Configurations must include exact file locations, parameter types, and rollback steps."
- "All implementations follow best practices and production standards."
- "The documentation provides a comprehensive overview of the system."

Do not replace these with slightly different policy slogans. Apply the requirement and write the relevant facts:
- Instead of saying every paper documents endpoints, name the endpoints you tested and report their actual responses.
- Instead of announcing that prose follows writing rules, remove the sentence.
- Instead of saying configurations must include exact details, give the actual configuration path, parameter name, type, default, and recovery steps when the reader needs them.
- Instead of claiming the documentation is comprehensive, tell the reader what is covered or link to the specific guide.

Use a standards section only when the document is actually about a named standard, specification, or contributor policy. Explain the real scope and source. Do not add one as decorative structure.

## Vocabulary that often sounds generic

Use a simpler word when it says the same thing.

Verbs: delve, leverage, utilize, harness, unlock, unleash, elevate, empower, foster, streamline, supercharge, embark, showcase, underscore, resonate, revolutionize, enhance, facilitate, bolster, spearhead, cultivate.

Adjectives: seamless, robust, comprehensive, crucial, pivotal, vital, paramount, cutting-edge, state-of-the-art, innovative, dynamic, meticulous, intricate, nuanced, multifaceted, holistic, transformative, groundbreaking, game-changing, tailored, bespoke, effortless, intuitive, user-centric, feature-rich, best-in-class.

Nouns: tapestry, testament, realm, journey, synergy, beacon, cornerstone, plethora, myriad, paradigm, game-changer, deep dive, takeaway, pain points.

Adverbs: seamlessly, effortlessly, meticulously, ultimately, essentially, fundamentally, notably, importantly, crucially.

These words are fine when they have a precise meaning. Avoid stacking them or using them to inflate a routine feature.

## Stock phrases

Avoid:
- "It's important to note that" and "it's worth noting".
- "In today's fast-paced world" and "in the ever-evolving landscape".
- "Plays a crucial role" and "a testament to".
- "At the end of the day" and "when it comes to".
- "Dive into", "deep dive", and "let's unpack".
- "Whether you're a beginner or an expert".
- "Look no further" and "take it to the next level".
- "The key takeaway is".
- "By leveraging" and "ensuring that".
- "In order to" when "to" works.
- "Due to the fact that" when "because" works.
- "A wide range of" and "a plethora of".
- Artificial contrast framing such as "not only X but also Y".
- "Choose one before publishing", "replace this with your", and "note to developer".

## Sentence and paragraph patterns

Watch for repeated structures that make text feel generated:
- Every section starts with a summary sentence.
- Every list has exactly three items.
- Every paragraph ends with a neat conclusion.
- The introduction and conclusion repeat each other.
- Every heading uses a broad abstract noun followed by "and" or "standards".
- Several sections repeat the same point with slightly different wording.
- A document has a formal standards section that says nothing about the subject itself.
- Perfectly parallel bullets where natural variation would be clearer.
- A conclusion that restates the whole document.

## Owner voice

Use first person for the maintainer's own work, choices, intent, experience, recommendations, and progress. Use "I" for a solo maintainer and "we" only for a real team.

Avoid:
- "The developer created this project..."
- "The maintainer decided..."
- "The author recommends..."
- "The next agent should..."
- "The assistant could not verify..."
- "As an AI language model..."

Prefer:
- "I built this project..."
- "I chose this approach..."
- "I recommend..."
- "I could not verify..."
- "Next, run..."
- Direct facts such as "The CLI reads the config file."

Do not force first person into API definitions, product behavior, commands, legal text, or third-party attribution. Never claim another contributor's work or an unrun test as your own.

## Formatting and technical text

Use headings only when they help readers find information. Prefer sentence case. Avoid bold lead-ins on every bullet, badge walls, decorative separators, unnecessary tables, and formal structure on short content.

Comments should explain why a choice exists, not restate the code. Error messages should say what failed and what the user can do next. Documentation should describe actual behavior, not claim to be comprehensive or production-ready.

# Model capability tiers

The tier is a research budget, not a personality. Classify the model you are
actually running on, using the best available evidence, and apply the matching
protocol from `SKILL.md`.

## Tiers

| Tier | Meaning | Default protocol |
|---|---|---|
| Frontier | Current top-tier coding model from a major lab | Standard gates, official docs for version-sensitive work |
| Capable | Solid general model, or a previous-generation frontier model | Research-first for unfamiliar or version-sensitive work |
| Efficient | Fast, small, free, quantized, or otherwise reduced model | Full research-first protocol |
| Unknown | No reliable model metadata, or an unrecognized name | Full research-first protocol, same as efficient |

`--require-frontier` exits nonzero for every tier except frontier. Use it when a
script or workflow needs a hard gate.

## Frontier signals

These are family keywords, not a guarantee. A model can share a name with a
frontier release and still be a smaller variant.

- Claude Opus class, and recent Claude Sonnet releases.
- GPT-5 class, including Codex variants, excluding mini and nano variants.
- Gemini 3 Pro, Ultra, or thinking variants.
- Grok 4 class.
- DeepSeek V4 class, excluding flash and lite variants.
- Qwen 3 Max class.
- Kimi K2 class.
- GLM 5 class.
- Comparable current top-tier coding models from other labs.

## Efficient signals

- Names containing flash, mini, nano, haiku, lite, small, free, turbo, cheap, or
  fast.
- Quantized or distilled variants when the name says so.
- Older small models such as Sonnet 3.5 class.
- Local models with a small parameter count.

## Capable signals

- Sonnet, Pro, or previous-generation flagship families.
- GPT-4 class.
- DeepSeek V3 class.
- Qwen 3 class below Max.
- Codestral, Command R, and similar mid-tier coding models.

If a name contains both a frontier and an efficient marker, prefer the efficient
tier. A "mini" or "flash" suffix matters more than the family name.

## Classification order

1. Empty or missing model string: unknown.
2. Efficient marker present: efficient.
3. Frontier marker present: frontier.
4. Capable marker present: capable.
5. Otherwise: unknown.

Run `scripts/detect_model.py` for the current implementation. It prints the
model string, evidence source, tier, and required mode.

## Evidence sources

Prefer, in order:

1. The live session record written by the harness. OpenCode stores provider and
   model in assistant message data. Codex stores the model in its thread table.
2. An explicit environment variable for the active model.
3. Harness configuration files.
4. The system prompt or model metadata provided by the harness.

A configuration file may hold a default that is not active. If the session
record and config disagree, trust the session and state the conflict.

## Why tiers go stale

New models ship constantly. Names are reused across generations, providers
change suffixes, and benchmark leadership moves. Any hardcoded list is a
snapshot, not the truth.

Update this file when:

- The detection script misses a model family you are using.
- A provider renames variants or adds a new tier suffix.
- A model you classified as capable clearly matches frontier behavior on
  official benchmarks and real coding tasks.
- A model you classified as frontier is now a smaller or deprecated variant.

Keep changes conservative. It is safer to research more than to overestimate a
model's reliability.

## Using the tier correctly

- The tier decides how much evidence to gather, not whether the user's request
  is valid.
- A frontier model on an auth migration still needs the full protocol.
- An efficient model on a typo still only needs to read the file.
- Unknown never means "assume capable". Unknown means "gather evidence first".
- Never mention the tier to excuse a failure. Fix the process and report the
  actual blocker.

## Anti-patterns

- Guessing a model name from the writing style of the conversation.
- Treating a provider's marketing name as proof of coding quality.
- Assuming a large context window means the model reads it correctly.
- Assuming a benchmark score removes the need to run the project's tests.
- Downgrading the requested deliverable because the model is not frontier.
- Claiming frontier status to avoid research.

# Contributing

Thanks for your interest in contributing.

## How to contribute

1. Fork the repository.
2. Create a branch (`git checkout -b add-my-skill`).
3. Make your changes and commit them.
4. Push the branch and open a pull request.

## Adding a skill

- Create a top-level folder named in lowercase with hyphens, for example `my-skill`.
- Add a `SKILL.md` with frontmatter containing `name` (same as the folder) and `description`.
- Write the description so it says what the skill does and when it should trigger. This is what the agent reads to decide whether to load it.
- Avoid a colon followed by a space inside the description. Strict YAML parsers reject it. Use a comma or wrap the value in quotes.
- Keep `SKILL.md` focused. Move long lists and templates into `references/` and say when to read them.
- Add the skill to the table in `README.md`.

Run `python scripts/validate_skills.py` before opening a pull request.

## Style

- Keep changes small and focused.
- Write plainly. No emoji, no em dashes, no marketing language. The `human-writing` skill has a scanner you can run: `python human-writing/scripts/scan.py <path>`.
- Commit messages are short and in the imperative, for example `Add retry notes to android-app-dev`.

## Reporting issues

Open an issue with a clear description, steps to reproduce, and which agent and version you used.

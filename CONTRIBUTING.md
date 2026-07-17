# Contributing

Read `AGENTS.md`, `GLOBAL_GOAL.md`, `REPOSITORY_ROLE.md`, and `docs/message-format.md` before changing localization data.

## Change process

1. Inspect `git status --short` and preserve unrelated work.
2. Explain affected keys, locales, placeholder types, plural/select branches, and compatibility impact.
3. Keep English definitions and locale changes reviewable; never use display text as a key.
4. Mark machine-generated translations `draft` and `unreviewed`.
5. Run every command in `docs/testing.md` and inspect the generated diff.
6. Update `IMPLEMENTATION_STATUS.md` only with commands that actually ran.

Use short imperative commit subjects, for example `locales: add document progress messages`. Pull requests must identify reviewer language competence, generated drafts, source-revision changes, affected clients, and exact validation results.

Locale packs are data-only. Never include credentials, private translation content, executable hooks, provider branding copied from another project, or unlicensed translations.

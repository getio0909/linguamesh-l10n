# Contributing

Read `GLOBAL_GOAL.md`, `REPOSITORY_ROLE.md`, and `AGENTS.md` before proposing changes.

## Change process

1. Inspect `git status --short` and preserve unrelated work.
2. Explain the affected message keys, locales, placeholders, generators, and compatibility range.
3. Keep source-message and translation changes reviewable and avoid unrelated reformatting.
4. Run `./tools/check-foundation.sh` at the current checkpoint.
5. Once product tooling exists, run every format, lint, test, and build command in `docs/testing.md`.
6. Record actual evidence in `IMPLEMENTATION_STATUS.md` when changing implementation state.

Use short imperative commit subjects with an optional scope, for example `locales: define English fallback metadata`.

Pull requests must identify machine-generated drafts, reviewer language competence where relevant, placeholder changes, compatibility impact, and exact validation results. Never include credentials or private translation content.

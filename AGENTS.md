# LinguaMesh Localization Instructions

## Required reading

Before changing this repository, read `REPOSITORY_ROLE.md`, `GLOBAL_GOAL.md`, `IMPLEMENTATION_STATUS.md`, and the relevant files under `docs/`.

## Scope

This repository owns canonical UI messages, locale metadata, official translations, validation, pseudo-localization, and generators for platform-native resources. Do not add client UI code, provider adapters, translation prompts, or document codecs here.

## Workflow

1. Inspect `git status --short` and preserve user changes.
2. Confirm the pinned global-goal revision remains compatible.
3. Record uncertain decisions with `Assumption:`.
4. Make the smallest complete localization change, including schema validation and fixtures.
5. Run every current command documented in `docs/testing.md`.
6. Update `IMPLEMENTATION_STATUS.md` with commands and actual results.

## Data and code rules

- Use stable, descriptive message keys; never use English display text as an identifier.
- Preserve placeholder identity, types, plural/select branches, platform applicability, accessibility context, status, and source revision.
- Use BCP 47 locale identifiers and English fallback.
- Mark machine-generated translations as drafts; never imply human review.
- Keep locale packs data-only and reject unknown keys or incompatible placeholders.
- All code comments must be Simplified Chinese on separate lines above the code they describe.
- All console, log, diagnostic, and command-line output strings must be English.

## Safety

Never commit credentials, private translation content, or executable community locale packs. Do not publish a localization release until generated native resources, compatibility metadata, and placeholder validation have reproducible evidence.

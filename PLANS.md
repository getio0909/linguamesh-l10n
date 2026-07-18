# Localization Vertical Slice Plan

Status: Complete for the `0.1.0` development vertical slice

## Goal

Deliver a reproducible `0.1.0` localization bundle from typed canonical data, with all required official locales, pseudo-locales, validation, native platform generators, tests, and CI.

## Assumptions

Assumption: English is the reviewed canonical source. The other eleven required locale packs are machine-generated drafts and remain explicitly unreviewed until qualified human reviewers approve them.

Assumption: This development bundle may define a small representative UI catalog that exercises plain text, typed placeholders, plurals, selects, platform filtering, and accessibility context. It does not claim complete product copy or a stable release.

## Work

- [x] Confirm repository scope and pinned global-goal revision.
- [x] Define versioned catalog and locale-pack schemas with canonical English messages.
- [x] Add twelve official locale packs and generated pseudo-locales.
- [x] Implement strict validation and deterministic native resource generators.
- [x] Add fixtures, tests, CI, contributor documentation, and status evidence.
- [x] Run setup, format, lint, test, generation, deterministic regeneration, and build checks with Python 3.13.

## Completion evidence

Record exact commands and outcomes in `IMPLEMENTATION_STATUS.md`. Generated resources must be checked into `generated/` and byte-for-byte reproducible from canonical data.

## Linux runtime-error coverage checkpoint

Assumption: Core/provider transport details remain English diagnostic detail; stable Linux error
sentences emitted by the worker are catalog-backed and can be localized without exposing secrets.

- [x] Add Linux-only catalog keys for Core startup, loopback-provider startup, compatibility reads,
  and profile-database path/permission failures.
- [x] Add Simplified Chinese and Traditional Chinese draft translations and English fallback values
  to every official locale pack.
- [x] Generate and validate all 59 native resource artifacts at catalog source revision 7.
- [x] Verify deterministic development bundle checksum
  `a8c5535b23eb27f02ff5fd3bb4c4c1c6948718f1233321305c173b1741b27e6f`.

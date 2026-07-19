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

## Linux request-level glossary copy

Assumption: Linux initially exposes a bounded, semicolon-separated request-level glossary in the
text workspace. Entries remain in memory for the request and are not persisted in locale data or
provider profiles; richer CSV/TBX import and cross-platform glossary UX remain later work.

- [x] Add localized Linux label, syntax placeholder, and privacy tooltip keys.
- [x] Regenerate all 59 deterministic native resource artifacts and pseudo-locales.
- [x] Validate the 211-message catalog and deterministic bundle checksum
  `116a9cdedd8b0a3d31171b365969b745681e50257e183b40aa2c37c77f1e6d91`.

## Linux glossary rule-validation copy

Assumption: request-level glossary syntax, credential-like data rejection, and conflicting-rule
errors are stable user-facing Linux messages and should use dedicated catalog keys rather than
falling back to the generic English diagnostic.

- [x] Add three Linux-only canonical validation messages and draft values to all official packs.
- [x] Regenerate all 59 deterministic native resources and both pseudo-locales.
- [x] Run `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check`; schema lint,
  26 tests, regeneration, bundle build, and foundation validation passed.
- [x] Bundle checksum: `c8bd6b0464ebbfa015988a4fc0cfd30b1f9e28d9e1aad19b8c50d36976128e8f`.

## Linux document-job metadata localization

Assumption: persisted document-job rows must not expose Rust enum debug names as user-facing copy;
the source filename and technical format names remain data, while lifecycle state labels and the
row summary use the canonical Linux catalog.

- [x] Add one row-summary template and six document-job state labels at source revision 20.
- [x] Regenerate all 59 deterministic resources and both pseudo-locales.
- [x] Run `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check`; 296 messages,
  26 tests, generation, bundle build, and foundation validation passed.
- [x] Bundle checksum: `d2f4fd439b5fbc8fc6d48f1be0a91ee92f558c70b851271d643829cfe8590e9b`.

## Linux optional OCR copy

Assumption: OCR is an explicit opt-in Linux capability. Its messages describe bounded external
plugin work and page-marked text output; they do not promise high-fidelity PDF reconstruction.

- [x] Add OCR toggle, progress, and fixed-error messages at source revision 21.
- [x] Regenerate all 59 deterministic native resources and both pseudo-locales.
- [x] Run the full deterministic bundle check; 306 messages, 26 tests, generation, bundle build,
  and foundation validation passed.
- [x] Bundle checksum: `6fc6839fce3a449eaf37d2efb9a52fa0ede1eab3a39fecdaff68682a79d8a4f8`.
- [ ] Publish the pinned revision and record GitHub Actions evidence after Linux sync.

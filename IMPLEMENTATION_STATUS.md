# Implementation Status

Status date: 2026-07-19

## Implemented

- Versioned JSON Schema contracts for the canonical catalog and data-only locale packs.
- A `0.1.0` English source catalog with 306 messages, including Linux-only status announcements, document-job row metadata and state labels, opt-in image-only PDF OCR controls and errors, text-file import, glossary CSV import/export and rule-validation errors, and translation-export labels, provider-profile controls, onboarding-stage copy, active-provider summaries, completion notifications, draft-locale notes, locale selector language names, fixed user-facing error messages, fixed state-error/category copy, fixed worker/file/storage/provider errors, production runtime/storage error coverage, the localized default provider name, request-level glossary controls, and the Android vertical-slice UI, covering typed string and integer placeholders, plurals, selects, platform applicability, accessibility context, and per-message source revisions.
- All 12 required official BCP 47 locale packs. English is source; the other 11 packs are explicitly machine-generated, draft, and unreviewed.
- Generated `en-XA` accented and `ar-XB` RTL pseudo-locales that preserve placeholders.
- Strict rejection of missing or unknown keys, malformed placeholders, incompatible plural/select branches, native resource-identifier collisions, stale revisions, invalid fallback/direction metadata, unsafe paths or text, and dishonest review status.
- Deterministic generators for Android strings/plurals XML, Windows RESW, macOS XCStrings, and paired Linux PO/MO catalogs. `generated/manifest.json` records status, compatibility, size, and SHA-256 for 59 artifacts.
- A versioned development compatibility record with no unverified minimum client versions.
- Python 3.13 setup, format, lint, test, generate, regeneration-check, and deterministic build commands; 26 unit and fixture tests; and GitHub Actions CI.

Assumption: the 201 Linux-only status, document-job row, text-import, image-only PDF OCR, glossary CSV and rule-validation, translation-export, provider-profile, onboarding, active-provider, notification, draft-note, locale-name, fixed-error, state-error/category, worker/file/storage/provider-error, runtime/storage-error, default-provider-name, and request-level glossary messages use machine-generated draft
translations; they are included in every official pack for schema completeness but are not
human-reviewed.

## Not yet implemented or verified

- Qualified human review of any non-English official locale.
- Complete production UI copy or community pack installation.
- Native-client ingestion, runtime locale switching, RTL layout behavior, accessibility behavior, or platform builds through Android, Windows, and Xcode toolchains.
- A stable localization release or central known-good release-train entry.

## Evidence

Validated locally on Debian Linux with `/home/wangtinghu/miniconda3/envs/py313/bin/python` 3.13.13 on 2026-07-18:

- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup, canonical JSON format checking for 20 files, schema/catalog lint, all 26 tests, byte-for-byte regeneration, deterministic bundle build, and foundation validation.
- `msgfmt --check --check-format -o /dev/null generated/linux/*/LC_MESSAGES/linguamesh.po` was run for each of the 14 official/pseudo PO catalogs; all passed without warnings. GNU `msgunfmt` read the generated Simplified Chinese MO and confirmed the fixed state-error context and translation.
- Android AAPT2 `2.20-15703166` compiled all 14 generated Android resource files; parsing all 28 generated Android and Windows XML files with Python `xml.etree.ElementTree` also succeeded.
- `jq` confirmed 83 native message keys in the macOS String Catalog, 59 files in the generated manifest, and 306 canonical entries in every official locale pack; the Linux PO/MO catalogs contain the new status, document-job row/state, text-import, image-only PDF OCR, glossary CSV and rule-validation, translation-export, provider-profile, onboarding, active-provider, notification, draft-note, locale-name, fixed-error, state-error/category, worker/file/storage/provider-error, runtime/storage-error, default-provider-name, and request-level glossary keys.
- Two consecutive unchanged builds produced SHA-256 `6fc6839fce3a449eaf37d2efb9a52fa0ede1eab3a39fecdaff68682a79d8a4f8` for `dist/linguamesh-l10n-0.1.0.zip` after adding deterministic Linux OCR controls and error resources.
- `git diff --check` exited successfully.
- The first `make check` run correctly detected stale generated resources after the catalog edit; `make generate` refreshed them and the subsequent full `make check` passed.
- GitHub Actions foundation run `29552975874` and localization run `29552975875` passed
  revision `d0e44b158e87481875862a3ce24f0432a0e0416b`. The localization workflow
  rebuilt the bundle, verified its internal checksum, and uploaded development artifact
  `linguamesh-l10n-0.1.0` (artifact ID `8396408392`).
- Local `tools/l10n lint`, `tools/l10n test`, `tools/l10n generate`, and `tools/l10n build` passed
  for the 306-message catalog; the first deterministic test correctly rejected stale generated
  resources, and the regenerated tree passed all 26 tests.

This checkpoint remains a development bundle rather than a stable release. Native-consumer
evidence remains pending until each client revision passes its own ingestion checks.

## 2026-07-19 — Linux optional OCR localization checkpoint

Assumption: OCR is an explicit, opt-in Linux capability. OCR failures remain localized errors,
the original PDF is never rewritten, and the generated text task is page-marked rather than a
claim of pixel-identical PDF reconstruction.

- Added ten Linux-only catalog messages for the OCR toggle, progress state, and bounded plugin
  errors; the catalog now contains 306 messages and 201 Linux-only source messages.
- Regenerated all 59 deterministic resources and both pseudo-locales.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, lint, 26 tests, byte-for-byte generation, deterministic bundle build, and
  foundation validation.
- Bundle SHA-256: `6fc6839fce3a449eaf37d2efb9a52fa0ede1eab3a39fecdaff68682a79d8a4f8`.
- GitHub Actions Foundation run `29668388992` and Localization run `29668388983` passed for this
  revision; Linux consumes the pinned revision after its own synchronization gate.

## 2026-07-19 — Linux document-job metadata localization checkpoint

Assumption: persisted document-job rows must not expose Rust enum debug names as user-facing copy;
the source filename and technical format names remain data, while lifecycle state labels and the
row summary use the canonical Linux catalog.

- Added `status.document_job_row` plus six document-job state labels, raising the catalog to 296
  messages and the Linux-only source count to 191.
- Regenerated all 59 deterministic resources and pseudo-locales.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, lint, 26 tests, generation, deterministic bundle build, and foundation validation.
- Bundle SHA-256: `d2f4fd439b5fbc8fc6d48f1be0a91ee92f558c70b851271d643829cfe8590e9b`.

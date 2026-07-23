# Implementation Status

## 2026-07-23 — Linux TBX glossary import messages

Assumption: the existing Linux glossary message keys remain stable while their copy expands from
CSV-only to the bounded CSV/TBX import contract; no other client consumes these Linux-only keys.

- Catalog source revision 62 now labels the native chooser as **CSV and TBX glossary files** and
  reports a format-neutral import error. Official locale packs, pseudo-locales, Linux PO/MO files,
  and the manifest were regenerated deterministically; no credentials or translation content were
  added.
- `make check` passed: Python doctor, format check, schema/lint (494 messages, 12 official packs),
  all 26 tests, byte-for-byte generation check, bundle build, and foundation validation. Release
  remains `unreleased`.

## 2026-07-23 — Linux regional and script preference messages

Assumption: the Linux translation-preset selector is the bounded client surface for Core's
regional-locale and script fields; cross-client parity and qualified human translation review
remain open.

- Added two source-revision-61 Linux messages for United States English and Mainland China
  Simplified Chinese preset labels. All twelve official locale packs, pseudo-locales, and
  deterministic native resources now carry the catalog's 494 messages.
- `make check` is the required final gate for this revision; non-English values remain
  machine-generated drafts pending qualified human translation and native visual/Orca review.

## 2026-07-23 — Linux glossary-library selector messages

Assumption: the Linux GTK glossary-library selector is a bounded client surface; TBX import and
cross-client library parity remain outside this localization checkpoint.

- Added twelve source-revision-60 Linux messages for listing, saving, loading, deleting, naming,
  and describing reusable glossary libraries. All twelve official locale packs, pseudo-locales,
  and deterministic native resources now carry the catalog's 492 messages.
- `make check` passed setup, formatting, schema/catalog lint, all 26 tests, byte-for-byte resource
  generation, deterministic bundle build, and foundation validation. Non-English values remain
  machine-generated drafts pending qualified human translation and native visual/Orca review.

## 2026-07-23 — Linux client-certificate identity messages

Assumption: the Linux provider form accepts a combined PEM client certificate and private key
identity; the value is session-only unless the user explicitly remembers it in Secret Service.

- Added three source-revision-59 Linux messages for the masked client-certificate identity field.
  All twelve official locale packs, pseudo-locales, and deterministic native resources now carry
  the catalog's 480 messages.
- `make check` passed formatting, schema/catalog lint, all 26 tests, byte-for-byte generation,
  deterministic bundle build, and foundation validation.
- Non-English values remain machine-generated drafts pending qualified human translation review;
  native visual/RTL/Orca review and stable-release qualification remain open.

## 2026-07-23 — Linux proxy credential messages

Assumption: Linux consumes proxy credentials through a separate SecretRef field; localized copy
must describe the username:password format and the Secret Service boundary without exposing values.

- Commit `f0b1c507d73f540f298a534303d0e6e63d44e87b` adds three source-revision-58 Linux messages
  for proxy credentials and updates all twelve official locale packs plus pseudo-locales and
  deterministic native resources. The catalog now contains 477 messages.
- `make check` passed formatting, schema/catalog lint, all 26 tests, byte-for-byte generation,
  deterministic bundle build, and foundation validation. Localization/Foundation runs
  `29975220462` and `29975220469` passed for the exact commit.
- Non-English values remain machine-generated drafts pending qualified human translation review;
  native visual/RTL/Orca review and stable-release qualification remain open.

## 2026-07-22 — Linux provider custom-header copy

Assumption: custom request headers are optional, bounded, non-secret metadata for Linux provider
profiles; authorization, credential-shaped values, and built-in request metadata remain rejected.

- Added three source-revision-51 messages for the custom-header label, placeholder, and safety
  tooltip. All twelve official locale packs and generated native resources include the keys;
  non-English values remain machine-generated drafts pending qualified human review.
- Regenerated 59 deterministic native resources and both pseudo-locales. The catalog now contains
  459 messages.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passes formatting,
  schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle build, and
  foundation validation.

Native Linux consumers must pin localization revision 51 before claiming the custom-header UI
evidence. Human translation review, native visual/RTL/Orca review, and stable-release qualification
remain open.

## 2026-07-22 — Linux provider profile notes copy

Assumption: profile notes are optional, non-secret, and Linux-only for this checkpoint; they are
stored as draft English fallback text in non-English packs until human translation review.

- Added three source-revision-47 messages for the Linux provider-profile notes label, placeholder,
  and safety tooltip. All twelve official locale packs and generated native resources include the
  keys without claiming translation approval.
- Regenerated the deterministic bundle; the catalog now contains 444 messages.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passes formatting,
  schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle build, and
  foundation validation.

Native Linux consumers must pin localization revision 47 before claiming the notes UI evidence.
Human translation review, native visual/RTL/Orca review, and stable-release qualification remain
open.

## 2026-07-22 — Linux document translation report copy

Assumption: the first report surface is Linux-only and emits a redacted TSV snapshot; provider
usage and retry counts remain explicitly unknown until document-job persistence records them.

- Added three Linux-only source messages at source revision 44 for the document report action,
  tooltip, and success status. All twelve official locale packs carry the keys; Simplified and
  Traditional Chinese include localized draft copy and the other non-English values remain
  machine-generated drafts.
- Regenerated all 59 deterministic native resources and both pseudo-locales. The catalog now
  contains 434 messages.
- ./tools/l10n lint, ./tools/l10n test (26 tests), ./tools/l10n generate --check, and
  ./tools/l10n build all pass after generation.

Native consumers must pin this localization revision before claiming report-export evidence.
Human translation review, native visual/RTL/Orca review, and stable-release qualification remain
open.

## 2026-07-21 — Linux usage-source metadata

Assumption: Linux displays normalized token counts as non-sensitive metadata; local estimates are
clearly labeled, provider-reported counts remain distinct, and missing counts remain unknown.

- Added five Linux-only source messages at source revision 43 for usage totals, unavailable usage,
  and provider/local/unknown source labels. All twelve official locale packs carry the keys;
  non-English values remain machine-generated drafts.
- Regenerated all 59 deterministic native resources and both pseudo-locales. The catalog now
  contains 431 messages.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passes setup,
  formatting, schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle
  build, and foundation validation.

Native consumers must pin this localization revision before claiming runtime usage-label evidence.
Human translation review, native visual/RTL/Orca review, and stable-release qualification remain
open.

## 2026-07-20 — Linux translation quality-mode copy

Assumption: the three quality modes are Linux-only UI controls for this checkpoint; non-English
strings remain explicitly unreviewed drafts and English remains the source fallback.

- Added five Linux-only source messages at source revision 40 for the quality-mode label, Fast,
  Balanced, Best, and the trade-off tooltip. All twelve official locale packs carry the keys with
  draft provenance outside English, and pseudo-locales plus Linux PO/MO resources were regenerated.
- The catalog now contains 410 messages. `make check` passes formatting, schema/catalog lint, all
  26 tests, deterministic regeneration, bundle construction, and foundation validation.

## 2026-07-20 — Azure OpenAI Linux provider copy

Assumption: Azure OpenAI deployment names are user-entered model identifiers; no live credentials
or account behavior are exercised by the deterministic localization checkpoint.

- Added five Linux-only source messages for the Azure OpenAI preset, resource endpoint guidance,
  manual deployment field, default profile name, and missing-deployment validation. The catalog
  now contains 401 messages at source revision 38, and all twelve official packs plus generated
  native resources carry the new keys as unreviewed drafts outside English.

Status date: 2026-07-19

## Implemented

- Added ten Linux-only routing constraint messages at source revision 36 for provider/model
  allowlists and denylists, minimum quality, maximum request bytes, list/limit tooltips, and invalid
  input errors. All twelve official packs carry the keys, and the catalog now contains 387 messages.
- `make check` passes setup, formatting, schema/catalog lint, all 26 tests, byte-for-byte
  regeneration, deterministic bundle build, and foundation validation after the routing constraint
  update. The first test run correctly detected stale generated resources; `make generate` refreshed
  all 59 artifacts before the passing run.

- Added seventeen Linux-only routing preference and privacy/capability constraint messages at source
  revision 35. All twelve official packs carry the keys, and the catalog now contains 377 messages.
- `make check` passes setup, formatting, schema/catalog lint, all 26 tests, byte-for-byte
  regeneration, deterministic bundle build, and foundation validation after the routing update.
- Added the Linux-only `status.text_metrics` message at source revision 34. The Linux editor
  can expose character counts and clearly approximate token counts without logging text content;
  all 12 official packs carry the key and the catalog now contains 360 messages.
- `make check` passes setup, formatting, schema/catalog lint, all 26 tests, byte-for-byte
  regeneration, deterministic bundle build, and foundation validation after the metrics update.
- Added the Linux-only duplicate routing-profile ID error at source revision 33. All 12 official
  packs carry the key, and the 359-message catalog regenerates all 59 deterministic resources.
- `make check` passes setup, formatting, schema/catalog lint, all 26 tests, byte-for-byte
  regeneration, deterministic bundle build, and foundation validation.
- A Linux-only routing-profile ID field with Core-compatible 1–128 byte ASCII validation;
  source revision 32 adds the label and invalid-ID error to all 12 official locale packs.
- Regenerated 59 deterministic native resources and both pseudo-locales for the 359-message
  catalog; `make check` passes all 26 tests and foundation validation.
- Versioned JSON Schema contracts for the canonical catalog and data-only locale packs.
- A `0.1.0` English source catalog with 359 messages, including Linux-only status announcements, document-job row metadata and state labels, stored-entry metadata, active-provider mode summaries, opt-in image-only PDF OCR controls and errors, text-file import, glossary CSV import/export and rule-validation errors, translation-export labels, provider-profile controls, onboarding-stage copy, active-provider summaries, completion notifications, draft-locale notes, locale selector language names, fixed user-facing error messages, fixed state-error/category copy, fixed worker/file/storage/provider errors, production runtime/storage error coverage, localized default provider names, request-level glossary controls, Secret Service prompt dismissal errors, Linux GTK drag-fixture and text-retry actions, routing-profile editing, IDs, and duplicate-ID protection, and the Android vertical-slice UI, covering typed string and integer placeholders, plurals, selects, platform applicability, accessibility context, and per-message source revisions.
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
- `jq` confirmed 83 native message keys in the macOS String Catalog, 59 files in the generated manifest, and 327 canonical entries in every official locale pack; the Linux PO/MO catalogs contain the new status, document-job row/state, text-import, image-only PDF OCR, glossary CSV and rule-validation, translation-export, provider-profile, onboarding, active-provider, notification, draft-note, locale-name, fixed-error, state-error/category, worker/file/storage/provider-error, runtime/storage-error, default-provider-name, request-level glossary, and Secret Service prompt-dismissal keys.
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

## 2026-07-19 — Linux visible-string coverage checkpoint

Assumption: user-visible compound summaries must localize their full template, not only a
prefix, so punctuation, fallback labels, and persistence-mode wording remain grammatically
replaceable in every supported Linux locale.

- Added three Linux-only messages for stored translation-entry metadata, persisted document-job
  IDs, and active-provider persistence-mode summaries at source revision 27. All official packs
  contain the keys; non-English values remain explicit machine-generated drafts.
- Routed history and translation-memory metadata, document-job IDs, active-provider summaries,
  and unavailable provider/model labels through the canonical catalog. Technical model IDs,
  filenames, and translation content remain data rather than localized copy.
- Regenerated all 59 deterministic native resources and both pseudo-locales. `make lint`,
  `make test` (26 tests), and `make generate-check` passed after refreshing generated output.

## 2026-07-19 — Linux text retry action checkpoint

Assumption: a failed or cancelled ordinary text request must be explicitly retryable without
creating a document job or changing the confirmed provider/model selection.

- Added Linux-only `action.retry_translation` and `tooltip.retry_translation` messages to all
  official packs and both pseudo-locales; non-English values remain machine-generated drafts.
- Regenerated the 59 deterministic native resources. `make lint`, `make test` (26 tests), and
  `make generate-check` passed after refreshing the generated tree.
- Linux consumes this catalog through its immutable revision and exposes the action only for
  failed/cancelled text requests; human copy review, other clients, and stable release remain open.

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

## 2026-07-19 — Linux diagnostics-label localization checkpoint

Assumption: the non-sensitive diagnostics panel is Linux-visible UI, so its fixed field labels,
boolean values, onboarding/status/theme/locale values, and profile-storage states must resolve
through the canonical catalog while provider identifiers, paths, endpoints, and output content
remain excluded.

- Added 20 Linux-only diagnostics messages, raising the catalog to 326 messages and the Linux-only
  source count to 221. Simplified Chinese, Traditional Chinese, and Arabic draft values cover the
  new labels; all other non-English packs retain explicit English fallback drafts.
- Regenerated all 59 deterministic native resources and both pseudo-locales. Bundle SHA-256 is
  `054d6749397cbbf652e099784f2c7d0e3650779a3c17c98e68d25560d286b2d3`.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle
  build, and foundation validation.

Native consumers must pin the resulting revision before claiming runtime evidence. Human review,
complete production copy coverage, and stable release qualification remain open.

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

## 2026-07-19 — Linux Secret Service prompt localization checkpoint

Assumption: Secret Service approval and dismissal are user-visible Linux security
interactions, so the prompt-dismissed failure must resolve through the canonical catalog
while the credential and prompt result remain outside logs and localization payloads.

- Added the Linux-only `error.storage.prompt_dismissed` message at source revision 23,
  raising the catalog to 327 messages and the Linux-only source count to 222. All official
  non-English values remain machine-generated draft translations.
- Regenerated all 59 deterministic native resources and both pseudo-locales.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic
  bundle build, and foundation validation.
- Bundle SHA-256: `53821e2397e6697b7551693c6f5787cc1f88e24d96b3077ac590645a848f1977`.

Native consumers must pin this revision before claiming runtime evidence. Human review,
complete production copy coverage, and stable release qualification remain open.

## 2026-07-19 — Linux built-in Ollama profile-name localization checkpoint

Assumption: built-in provider display names are user-visible Linux form values, so both the
OpenAI-compatible and native Ollama defaults must resolve through the canonical catalog while
user-edited names remain untouched.

- Added the Linux-only `profile.default_ollama_name` message at source revision 26 and routed
  built-in profile initialization/switching through the localized default-name helper.
- Regenerated all 59 deterministic native resources and both pseudo-locales. Bundle SHA-256 is
  `028d25b3637fbc19d41d497a860b414353615b9576db6f852a9f236bcbe770ce`.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle
  build, and foundation validation.

Native Linux must pin this revision before claiming the updated provider-name evidence. Human
translated-copy review, visual/RTL review, Orca speech review, and stable-release qualification
remain open.

## 2026-07-19 — Linux GTK fixture localization checkpoint

Assumption: the automated GTK drag-and-drop fixture button is still user-visible UI and must
resolve through the canonical catalog, even though it is only enabled for interaction-test runs.

- Added the Linux-only `fixture.drag_file` source message at catalog revision 25; all 12 official
  locale packs carry the key, with non-English values remaining machine-generated drafts.
- Regenerated all 59 deterministic native resources and both pseudo-locales. Bundle SHA-256 is
  `61a054d99935b256e79d5be7feb4d929fc8cf61af663a02b8fd10475745d70bd`.
- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup,
  formatting, schema/catalog lint, all 26 tests, byte-for-byte generation, deterministic bundle
  build, and foundation validation.

Linux must pin this revision before claiming the updated visible-string audit. Human translated
copy review, visual/RTL review, Orca speech review, and stable-release qualification remain open.

# Implementation Status

Status date: 2026-07-18

## Implemented

- Versioned JSON Schema contracts for the canonical catalog and data-only locale packs.
- A `0.1.0` English source catalog with 148 messages, including Linux-only status announcements, text-file import labels, provider-profile controls, onboarding-stage copy, active-provider summaries, completion notifications, draft-locale notes, fixed user-facing error messages, fixed state-error/category copy, and the Android vertical-slice UI, covering typed string and integer placeholders, plurals, selects, platform applicability, accessibility context, and per-message source revisions.
- All 12 required official BCP 47 locale packs. English is source; the other 11 packs are explicitly machine-generated, draft, and unreviewed.
- Generated `en-XA` accented and `ar-XB` RTL pseudo-locales that preserve placeholders.
- Strict rejection of missing or unknown keys, malformed placeholders, incompatible plural/select branches, native resource-identifier collisions, stale revisions, invalid fallback/direction metadata, unsafe paths or text, and dishonest review status.
- Deterministic generators for Android strings/plurals XML, Windows RESW, macOS XCStrings, and paired Linux PO/MO catalogs. `generated/manifest.json` records status, compatibility, size, and SHA-256 for 59 artifacts.
- A versioned development compatibility record with no unverified minimum client versions.
- Python 3.13 setup, format, lint, test, generate, regeneration-check, and deterministic build commands; 25 unit and fixture tests; and GitHub Actions CI.

Assumption: the 107 Linux-only status, text-import, provider-profile, onboarding, active-provider, notification, draft-note, fixed-error, and state-error/category messages use machine-generated draft
translations; they are included in every official pack for schema completeness but are not
human-reviewed.

## Not yet implemented or verified

- Qualified human review of any non-English official locale.
- Complete production UI copy or community pack installation.
- Native-client ingestion, runtime locale switching, RTL layout behavior, accessibility behavior, or platform builds through Android, Windows, and Xcode toolchains.
- A stable localization release or central known-good release-train entry.

## Evidence

Validated locally on Debian Linux with `/home/wangtinghu/miniconda3/envs/py313/bin/python` 3.13.13 on 2026-07-18:

- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup, canonical JSON format checking for 20 files, schema/catalog lint, all 25 tests, byte-for-byte regeneration, deterministic bundle build, and foundation validation.
- `msgfmt --check --check-format -o /dev/null generated/linux/*/LC_MESSAGES/linguamesh.po` was run for each of the 14 official/pseudo PO catalogs; all passed without warnings. GNU `msgunfmt` read the generated Simplified Chinese MO and confirmed the fixed state-error context and translation.
- Android AAPT2 `2.20-15703166` compiled all 14 generated Android resource files; parsing all 28 generated Android and Windows XML files with Python `xml.etree.ElementTree` also succeeded.
- `jq` confirmed 83 native message keys in the macOS String Catalog, 59 files in the generated manifest, and 148 canonical entries in every official locale pack; the Linux PO/MO catalogs contain the new status, text-import, provider-profile, onboarding, active-provider, notification, draft-note, fixed-error, and state-error/category keys.
- Two consecutive unchanged builds produced SHA-256 `d82a152aff0212b7dde55d9b9a67ceac7ed16245d6a0ca6de49564f7d1dafcc5` for `dist/linguamesh-l10n-0.1.0.zip` after adding deterministic Linux MO resources.
- `git diff --check` exited successfully.
- The first `make check` run correctly detected stale generated resources after the catalog edit; `make generate` refreshed them and the subsequent full `make check` passed.
- GitHub Actions foundation run `29552975874` and localization run `29552975875` passed
  revision `d0e44b158e87481875862a3ce24f0432a0e0416b`. The localization workflow
  rebuilt the bundle, verified its internal checksum, and uploaded development artifact
  `linguamesh-l10n-0.1.0` (artifact ID `8396408392`).

This checkpoint remains a development bundle rather than a stable release. Native-consumer
evidence remains pending until each client revision passes its own ingestion checks.

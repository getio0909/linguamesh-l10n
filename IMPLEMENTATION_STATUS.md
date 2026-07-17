# Implementation Status

Status date: 2026-07-17

## Implemented

- Versioned JSON Schema contracts for the canonical catalog and data-only locale packs.
- A `0.1.0` English source catalog with 41 messages, including the Android vertical-slice UI, covering typed string and integer placeholders, plurals, selects, platform applicability, accessibility context, and per-message source revisions.
- All 12 required official BCP 47 locale packs. English is source; the other 11 packs are explicitly machine-generated, draft, and unreviewed.
- Generated `en-XA` accented and `ar-XB` RTL pseudo-locales that preserve placeholders.
- Strict rejection of missing or unknown keys, malformed placeholders, incompatible plural/select branches, native resource-identifier collisions, stale revisions, invalid fallback/direction metadata, unsafe paths or text, and dishonest review status.
- Deterministic generators for Android strings/plurals XML, Windows RESW, macOS XCStrings, and Linux PO. `generated/manifest.json` records status, compatibility, size, and SHA-256 for 45 artifacts.
- A versioned development compatibility record with no unverified minimum client versions.
- Python 3.13 setup, format, lint, test, generate, regeneration-check, and deterministic build commands; 25 unit and fixture tests; and GitHub Actions CI.

## Not yet implemented or verified

- Qualified human review of any non-English official locale.
- Complete production UI copy, community pack installation, or Linux MO compilation.
- Native-client ingestion, runtime locale switching, RTL layout behavior, accessibility behavior, or platform builds through Android, Windows, and Xcode toolchains.
- A stable localization release or central known-good release-train entry.

## Evidence

Validated locally on Debian Linux with `/home/wangtinghu/miniconda3/envs/py313/bin/python` 3.13.13 on 2026-07-17:

- `PYTHON_BIN=/home/wangtinghu/miniconda3/envs/py313/bin/python make check` passed setup, canonical JSON format checking for 20 files, schema/catalog lint, all 25 tests, byte-for-byte regeneration, deterministic bundle build, and foundation validation.
- `msgfmt --check --check-format -o /dev/null generated/linux/*/LC_MESSAGES/linguamesh.po` was run for each of the 14 official/pseudo PO catalogs; all passed without warnings.
- Android AAPT2 `2.20-15703166` compiled all 14 generated Android resource files; parsing all 28 generated Android and Windows XML files with Python `xml.etree.ElementTree` also succeeded.
- `jq` confirmed 43 native message keys in the macOS String Catalog, 45 files in the generated manifest, and 41 canonical entries in every official locale pack.
- Two consecutive unchanged builds produced SHA-256 `0f7ac7b6086032ca29e7a27376e32e88d7387029f6d87b868e72c12fc2b19391` for `dist/linguamesh-l10n-0.1.0.zip` after pinning the current Node 24 action runtimes.
- `git diff --check` exited successfully.
- GitHub Actions foundation run `29552975874` and localization run `29552975875` passed
  revision `d0e44b158e87481875862a3ce24f0432a0e0416b`. The localization workflow
  rebuilt the bundle, verified its internal checksum, and uploaded development artifact
  `linguamesh-l10n-0.1.0` (artifact ID `8396408392`).

This checkpoint remains a development bundle rather than a stable release. Native-consumer
evidence remains pending until each client revision passes its own ingestion checks.

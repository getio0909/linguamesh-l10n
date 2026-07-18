# LinguaMesh Localization

Canonical, typed localization data and deterministic native resource generators for LinguaMesh clients.

## Current development bundle

Catalog `0.1.0` contains 107 messages, including the Android vertical-slice UI, Linux status
announcements, text-file import labels, provider-profile controls, onboarding-stage copy, active-provider summaries, completion notifications, and draft-locale notes, and exercises typed placeholders, plurals,
selects, accessibility context, and RTL metadata. English is the canonical source. Simplified Chinese, Traditional Chinese, Spanish,
French, German, Japanese, Korean, Brazilian Portuguese, Russian, Arabic, and Hindi are complete
machine-generated drafts marked unreviewed. They are not claimed as human-approved translations.

The generator also derives accented `en-XA` and RTL `ar-XB` pseudo-locales. Outputs are committed under `generated/` for Android XML, Windows RESW, macOS XCStrings, and Linux PO.

## Repository layout

- `catalog/messages.json`: canonical English messages and typed parameters.
- `schema/`: versioned JSON Schema contracts.
- `locales/`: twelve official, data-only locale packs.
- `compatibility.json`: explicit development compatibility and limitations.
- `src/linguamesh_l10n/`: validation, pseudo-localization, and generators.
- `generated/`: reproducible platform resources and SHA-256 manifest.
- `tests/fixtures/`: intentionally invalid compatibility cases.

## Quick start

Python 3.13 and the standard library are the only requirements.

```sh
make setup
make check
```

Use `PYTHON_BIN=/path/to/python3.13 make check` when Python is installed elsewhere. `make build` creates a deterministic development ZIP and checksum under ignored `dist/`.

Read [GLOBAL_GOAL.md](GLOBAL_GOAL.md), [REPOSITORY_ROLE.md](REPOSITORY_ROLE.md), and [docs/message-format.md](docs/message-format.md) before changing the catalog.

## License

MIT. See [LICENSE](LICENSE).

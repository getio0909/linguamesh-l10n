# Repository Role

`linguamesh-l10n` is the canonical localization-data repository for LinguaMesh.

It is responsible for:

- typed and versioned UI message definitions;
- canonical English source messages;
- official locale translations and metadata;
- placeholder, plural, select, fallback, and RTL validation;
- pseudo-localization;
- generators for Android, Windows, macOS, and Linux native resources;
- localization bundle compatibility and release records.

It is not responsible for translating user content, rendering native UI, storing application credentials, or implementing shared core behavior. Those responsibilities belong to `linguamesh-core` and the native client repositories.

The current `0.1.0` development slice implements canonical data, required official draft packs, pseudo-locales, validation, and four native resource generators. It does not claim qualified translation review, native-client integration, runtime locale behavior, or a stable release.

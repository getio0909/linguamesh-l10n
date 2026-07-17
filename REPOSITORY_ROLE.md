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

The current foundation does not claim any implemented locales or generators.

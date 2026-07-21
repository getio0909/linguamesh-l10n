# Architecture

## Data flow

`catalog/messages.json` is the sole definition of message identity, canonical English, parameter types, plural/select semantics, platform applicability, accessibility context, status, and source revision. Versioned schemas in `schema/` make the persisted contracts inspectable; the standard-library validator enforces their cross-file invariants without a network dependency.

Each `locales/<bcp47>.json` pack is data-only. It declares direction, English fallback, CLDR-style plural categories, gettext form mapping, review provenance, and translations for exactly the known message keys. The validator rejects missing or unknown keys, stale source revisions, incompatible branches, malformed placeholders, native resource-identifier collisions, unsafe metadata, and unreviewed machine text presented as reviewed.

The pipeline is:

```text
catalog + official packs -> validation -> pseudo-locales -> native generators -> manifest
```

Generators produce Android `strings.xml`/`plurals`, Windows RESW entries, one macOS XCStrings catalog, and paired Linux PO/MO catalogs. The PO files remain reviewable source resources; the deterministic GNU MO files are the runtime lookup resources. Platforms without an arbitrary select primitive receive stable branch-suffixed identifiers such as `history.mode.incognito`; the client chooses the branch through its typed localization layer.

Linux usage labels identify whether a normalized count was provider-reported, locally estimated, or
unknown. Localization carries only the category and bounded numeric count; it never carries source
or translated text, credentials, or pricing data.

## Determinism and trust

Generation starts in an empty staging directory, uses stable ordering and UTF-8/LF output, then records every artifact size and SHA-256 in `generated/manifest.json`. `./tools/l10n generate --check` regenerates independently and compares every byte.

Official draft packs and pseudo-locales remain distinct. Neither can replace canonical English definitions. Generated strings are untrusted display data and are escaped for each target format. JSON and bundle inputs have explicit size limits; symbolic-link inputs and outputs are rejected. This repository does not execute locale-pack content or accept credentials.

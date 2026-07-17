# Architecture

## Intended data flow

The future localization pipeline will treat a typed, versioned message schema and canonical English values as the source of truth. Validated locale data will feed deterministic generators for Android resources, Windows resources, macOS String Catalogs, and Linux gettext artifacts.

Each message must preserve a stable key, description, placeholder definitions, plural/select variants, platform applicability, accessibility context, translation status, and source revision. Locale metadata must use BCP 47 identifiers, declare text direction, and define English fallback behavior.

Generated resources may be committed only with deterministic regeneration checks. Community bundles must be data-only, removable, schema compatible, and unable to overwrite canonical English source data.

## Current boundary

No schema, generator, or generated artifact exists at this checkpoint. This document describes the required direction and does not claim runtime behavior.

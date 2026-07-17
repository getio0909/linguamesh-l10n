# Message and Locale Format

## Canonical messages

Each entry in `catalog/messages.json` has a stable dotted key, English value, description, typed placeholders, value kind, platform set, optional accessibility context, source status, and source revision. Supported value kinds are:

- `text`: one template;
- `plural`: an integer selector with English `one` and `other` branches;
- `select`: a declared select parameter whose choices exactly match its branches.

Templates use named placeholders such as `{provider}` or `{count}`. A translation must preserve every placeholder exactly. Do not construct sentences by concatenating message fragments.

Select choices must be stable lowercase identifiers such as `enabled` or `incognito`. Catalog validation rejects identifiers that would collide after conversion to Android, Windows, or macOS resource names.

## Locale packs

Official packs are named with BCP 47 tags, for example `zh-Hans.json` and `pt-BR.json`. Every non-English pack falls back to `en`, declares direction and plural rules, and contains exactly the canonical message keys. Arabic demonstrates RTL and six plural categories; Russian records its three gettext forms separately from its four CLDR categories.

Machine-generated content must use:

```json
{
  "machineGenerated": true,
  "reviewStatus": "unreviewed",
  "status": "draft"
}
```

Do not change those claims until a qualified reviewer has reviewed every affected entry. Update a translation's `sourceRevision` whenever the canonical message revision changes.

## Contributor sequence

1. Change the canonical message and increment its source revision when meaning or parameters change.
2. Update all locale packs; keep unreviewed entries marked draft.
3. Run `make format lint generate test`.
4. Run `make generate-check` and inspect `git diff -- generated/`.

Pseudo-locales are always generated; never edit `generated/pseudo/*.json` directly.

# Releasing

Catalog `0.1.0` is a development bundle, not a stable localization release. The eleven non-English official packs are machine-generated and unreviewed.

## Development bundle

Run:

```sh
make check
```

This regenerates native resources, verifies committed output, creates `dist/linguamesh-l10n-0.1.0.zip`, and writes its SHA-256 file. The archive uses fixed timestamps, stable path ordering, and fixed permissions. Repeating `make build` with unchanged inputs must produce the same checksum.

## Stable release gate

Before tagging a stable bundle:

1. obtain and record qualified human review for every locale claimed reviewed;
2. run all commands in `docs/testing.md` in CI;
3. verify client consumption of Android XML, Windows RESW, macOS XCStrings, and Linux PO;
4. record compatibility, artifact checksums, limitations, and rollback guidance;
5. update the central `linguamesh-project/release-manifest.toml` with the tested localization version and compatible clients.

Do not publish drafts as reviewed, omit `generated/manifest.json`, or claim runtime locale switching and RTL client behavior from generator tests alone.

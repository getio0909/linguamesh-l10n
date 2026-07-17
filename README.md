# LinguaMesh Localization

Canonical localization source for LinguaMesh native clients. This repository will own typed message definitions, English source text, official locale data, placeholder validation, pseudo-locales, and generators for Android, Windows, macOS, and Linux resources.

## Current status

This checkpoint contains repository policy, architecture, and foundation validation only. No message schema, locale pack, generator, or distributable localization bundle exists yet.

## Repository boundaries

- Keep UI message data and localization generators here.
- Keep platform UI code in the corresponding client repository.
- Keep translation-engine prompts and provider behavior in `linguamesh-core`.
- Treat generated platform resources as reproducible outputs of the canonical schema.

Read [GLOBAL_GOAL.md](GLOBAL_GOAL.md), [REPOSITORY_ROLE.md](REPOSITORY_ROLE.md), and [docs/architecture.md](docs/architecture.md) before contributing.

## Current validation

No external dependencies are required for the foundation checkpoint.

```sh
./tools/check-foundation.sh
```

Product format, lint, test, and build commands are unavailable until the localization schema and generator toolchain are implemented. See [docs/testing.md](docs/testing.md) for the intended command contract.

## License

MIT. See [LICENSE](LICENSE).

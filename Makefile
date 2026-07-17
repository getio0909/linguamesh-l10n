.PHONY: setup format format-check lint test generate generate-check build check

setup:
	./tools/l10n doctor

format:
	./tools/l10n format

format-check:
	./tools/l10n format --check

lint:
	./tools/l10n lint

test:
	./tools/l10n test

generate:
	./tools/l10n generate

generate-check:
	./tools/l10n generate --check

build:
	./tools/l10n build

check: setup format-check lint test generate-check build
	./tools/check-foundation.sh

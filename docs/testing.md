# Testing

Python 3.13 is required; the product toolchain has no external package dependencies. On this workstation the verified interpreter is `/home/wangtinghu/miniconda3/envs/py313/bin/python`. Override `PYTHON_BIN` on other hosts.

Run each command from the repository root:

```sh
make setup
make format-check
make lint
make test
make generate-check
make build
```

In order, these commands verify Python and imports; check JSON formatting; validate schemas, catalogs, placeholders, branches, and syntax; run unit and fixture tests; compare independently generated output byte for byte; and build the ZIP plus SHA-256.

`make check` runs all commands above and the repository foundation check. Formatting changes can be applied with `make format`; native resources can be refreshed with `make generate`.

The tests parse every generated Android and Windows XML document, load the macOS String Catalog as JSON, inspect Linux PO escaping/review metadata and GNU MO tables, validate pseudo-locales and Arabic quantities, verify all manifest hashes, and compare generated output against a fresh tree. Safety tests reject resource-identifier collisions, unsafe select branches, invalid XML characters, overstated review metadata, symbolic-link inputs and outputs, oversized JSON, and unsafe bundle versions. Fixtures under `tests/fixtures/` prove that unknown keys, placeholder drift, missing plural categories, and incompatible select branches fail validation.

Default tests use no provider, network access, paid credential, or private translation content.

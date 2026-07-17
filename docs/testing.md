# Testing

## Available now

Setup requires only Bash, Git, and standard POSIX utilities. From the repository root run:

```sh
./tools/check-foundation.sh
```

This verifies required foundation files, the global-goal revision pin, repository identity, line endings, and trailing whitespace. It is the only implemented format/lint/test check. There is no product build.

## Unavailable until implementation

The product toolchain and its exact executable interface have not been selected, so product setup, formatting, linting, tests, generators, and builds are unavailable. Do not invent commands or report those checks as passing.

When the schema toolchain is implemented, this document must name exact reproducible commands for dependency setup, formatting, schema linting, unit and fixture tests, all four platform generators, deterministic-output comparison, and bundle packaging. Default CI must require no paid provider credentials.

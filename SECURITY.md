# Security Policy

## Reporting a vulnerability

Do not open a public issue for an unpatched vulnerability. Use the private security-reporting channel configured on the canonical GitHub repository. If that channel is unavailable, contact the maintainers privately before disclosing details.

Include affected revision, reproduction conditions, impact, and a minimal non-sensitive proof. Do not include credentials, private source text, or personal data.

## Localization security

- Locale packs must remain data-only and must never execute code.
- Parsers must bound input size and reject malformed schemas, unknown keys, invalid locale identifiers, incompatible placeholders, and unsafe paths.
- Generated resources must escape content for their target platform.
- Community and machine-generated text must not overwrite canonical English source messages.
- Diagnostics must not contain credentials or private translation content.

No release is currently supported. Security support windows will be documented with the first versioned bundle.

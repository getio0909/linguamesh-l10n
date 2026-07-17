#!/usr/bin/env bash
set -euo pipefail

expected_goal_sha="11f9a65927aac7e57e2af119e9d21cc98e8d5a08b8a112a19ee1c47903e36198"
required_files=(
  README.md
  LICENSE
  AGENTS.md
  REPOSITORY_ROLE.md
  GLOBAL_GOAL.md
  SECURITY.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  THIRD_PARTY_NOTICES.md
  IMPLEMENTATION_STATUS.md
  compatibility.json
  docs/architecture.md
  docs/testing.md
  docs/releasing.md
  .gitignore
  .github/workflows/foundation.yml
)

for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "Missing required file: $path" >&2
    exit 1
  fi
done

grep -Fqx 'Central repository: `linguamesh-project`' GLOBAL_GOAL.md
grep -Fqx "Authoritative SHA-256: \`$expected_goal_sha\`" GLOBAL_GOAL.md
grep -Fq '`linguamesh-l10n`' REPOSITORY_ROLE.md

mapfile -t text_files < <(
  find . \
    \( -path ./.git -o -path ./dist -o -path ./.cache -o -name __pycache__ \) -prune \
    -o -type f ! -name '*.pyc' ! -name '*.pyo' ! -name '*.zip' -print \
    | sort
)
if grep -nE '[[:blank:]]+$' "${text_files[@]}"; then
  echo "Trailing whitespace detected." >&2
  exit 1
fi

if grep -Il $'\r' "${text_files[@]}" | grep -q .; then
  echo "Carriage-return line endings detected." >&2
  exit 1
fi

credential_pattern='(-----BEGIN (RSA |EC |OPENSSH )?PRIVATE'
credential_pattern+=' KEY-----|sk-[A-Za-z0-9_-]{20,}|gh'
credential_pattern+='[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})'
if grep -Eq "$credential_pattern" "${text_files[@]}"; then
  echo "Credential signature detected." >&2
  exit 1
fi

echo "Foundation validation passed."

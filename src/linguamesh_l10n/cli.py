from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import tokenize
import unittest
from pathlib import Path

from .generators import generate_tree
from .package import build_bundle
from .validation import ValidationError, canonical_json, load_json, source_json_paths, validate_repository

ROOT = Path(__file__).resolve().parents[2]


def _tree_bytes(path: Path) -> dict[str, bytes]:
    if not path.exists():
        return {}
    return {
        item.relative_to(path).as_posix(): item.read_bytes()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def _replace_generated() -> dict[str, object]:
    destination = ROOT / "generated"
    if destination.parent != ROOT or destination.name != "generated":
        raise RuntimeError("Generated output path is unsafe")
    temporary_root = Path(tempfile.mkdtemp(prefix=".l10n-generated-", dir=ROOT))
    staging = temporary_root / "generated"
    try:
        manifest = generate_tree(ROOT, staging)
        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)
        return manifest
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)


def _check_generated() -> None:
    with tempfile.TemporaryDirectory(prefix="linguamesh-l10n-") as directory:
        actual = Path(directory) / "generated"
        generate_tree(ROOT, actual)
        expected_files = _tree_bytes(ROOT / "generated")
        actual_files = _tree_bytes(actual)
    if expected_files != actual_files:
        missing = sorted(actual_files.keys() - expected_files.keys())
        stale = sorted(expected_files.keys() - actual_files.keys())
        changed = sorted(
            path for path in actual_files.keys() & expected_files.keys() if actual_files[path] != expected_files[path]
        )
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if stale:
            details.append(f"stale: {', '.join(stale)}")
        if changed:
            details.append(f"changed: {', '.join(changed)}")
        raise ValidationError("generated resources are not current (" + "; ".join(details) + ")")


def _format_sources(check: bool) -> None:
    changed: list[str] = []
    for path in source_json_paths(ROOT):
        expected = canonical_json(load_json(path))
        current = path.read_text(encoding="utf-8")
        if current != expected:
            changed.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_text(expected, encoding="utf-8", newline="\n")
    if changed and check:
        raise ValidationError("JSON formatting differs: " + ", ".join(changed))
    action = "checked" if check else "formatted"
    print(f"JSON sources {action}: {len(source_json_paths(ROOT))} files.")


def _lint_python() -> None:
    for path in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        with path.open("rb") as stream:
            for token in tokenize.tokenize(stream.readline):
                if token.type == tokenize.COMMENT and not token.string.startswith("#!"):
                    if not any("\u4e00" <= character <= "\u9fff" for character in token.string):
                        raise ValidationError(
                            f"{path.relative_to(ROOT)}:{token.start[0]}: code comments must be Simplified Chinese"
                        )


def _run_tests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="l10n", description="Validate and generate LinguaMesh localization resources.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="Check the local Python setup.")
    format_parser = subparsers.add_parser("format", help="Format canonical JSON sources.")
    format_parser.add_argument("--check", action="store_true", help="Fail instead of writing changes.")
    subparsers.add_parser("lint", help="Validate schemas, catalogs, and source syntax.")
    subparsers.add_parser("test", help="Run unit and generated-resource tests.")
    generate_parser = subparsers.add_parser("generate", help="Generate all native resources.")
    generate_parser.add_argument("--check", action="store_true", help="Verify committed output byte for byte.")
    subparsers.add_parser("build", help="Generate and package a deterministic development bundle.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "doctor":
            if sys.version_info < (3, 13):
                raise ValidationError("Python 3.13 or newer is required")
            print(f"Python setup passed: {sys.version.split()[0]}; no external dependencies required.")
        elif args.command == "format":
            _format_sources(args.check)
        elif args.command == "lint":
            catalog, messages, packs = validate_repository(ROOT)
            _lint_python()
            print(
                f"Localization validation passed: schema {catalog['schemaVersion']}, "
                f"{len(messages)} messages, {len(packs)} official locale packs."
            )
        elif args.command == "test":
            return 0 if _run_tests() else 1
        elif args.command == "generate":
            if args.check:
                _check_generated()
                print("Generated resources are byte-for-byte current.")
            else:
                manifest = _replace_generated()
                print(f"Generated {len(manifest['artifacts'])} deterministic resource files.")
        elif args.command == "build":
            manifest = _replace_generated()
            archive, checksum = build_bundle(ROOT, str(manifest["catalogVersion"]))
            print(f"Built {archive.relative_to(ROOT)} and {checksum.relative_to(ROOT)}.")
        return 0
    except (ValidationError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

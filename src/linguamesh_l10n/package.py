from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

MAX_BUNDLE_FILE_BYTES = 32 * 1024 * 1024
MAX_BUNDLE_BYTES = 256 * 1024 * 1024
VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
BUNDLE_DIRECTORIES = (
    "catalog",
    "schema",
    "locales",
    "generated",
    "src",
    "tools",
    "tests",
    "docs",
    ".github",
)
BUNDLE_FILES = (
    "LICENSE",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "REPOSITORY_ROLE.md",
    "GLOBAL_GOAL.md",
    ".gitignore",
    "compatibility.json",
    "pyproject.toml",
    "Makefile",
)


def _bundle_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in BUNDLE_DIRECTORIES:
        directory = root / relative
        if directory.is_symlink():
            raise ValueError(f"Bundle input must not be a symbolic link: {relative}")
        if not directory.is_dir():
            raise ValueError(f"Bundle input directory is missing: {relative}")
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Bundle input must not be a symbolic link: {path.relative_to(root)}")
            if path.is_file() and "__pycache__" not in path.parts:
                files.append(path)
    for relative in BUNDLE_FILES:
        files.append(root / relative)
    ordered = sorted(set(files), key=lambda path: path.relative_to(root).as_posix())
    total_size = 0
    for path in ordered:
        relative = path.relative_to(root)
        if path.is_symlink():
            raise ValueError(f"Bundle input must not be a symbolic link: {relative}")
        if not path.is_file():
            raise ValueError(f"Bundle input is missing or not a regular file: {relative}")
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Bundle input escapes the repository root: {relative}")
        size = path.stat().st_size
        if size > MAX_BUNDLE_FILE_BYTES:
            raise ValueError(f"Bundle input exceeds {MAX_BUNDLE_FILE_BYTES} bytes: {relative}")
        total_size += size
        if total_size > MAX_BUNDLE_BYTES:
            raise ValueError(f"Bundle inputs exceed {MAX_BUNDLE_BYTES} bytes")
    return ordered


def build_bundle(root: Path, version: str, output: Path | None = None) -> tuple[Path, Path]:
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Bundle version must be a semantic version: {version}")
    output = output or root / "dist"
    if output.is_symlink():
        raise ValueError(f"Bundle output must not be a symbolic link: {output}")
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"linguamesh-l10n-{version}.zip"
    checksum_path = archive.with_suffix(".zip.sha256")
    for path in (archive, checksum_path):
        if path.is_symlink():
            raise ValueError(f"Bundle output must not be a symbolic link: {path}")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in _bundle_files(root):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if relative == "tools/l10n" else 0o100644) << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum_path.write_text(f"{checksum}  {archive.name}\n", encoding="utf-8", newline="\n")
    return archive, checksum_path

from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from linguamesh_l10n.package import BUNDLE_DIRECTORIES, BUNDLE_FILES, _bundle_files, build_bundle

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_bundle_is_deterministic_and_contains_reproducibility_inputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="linguamesh-package-tests-") as directory:
            temporary = Path(directory)
            first, first_checksum = build_bundle(ROOT, "0.1.0", temporary / "first")
            second, second_checksum = build_bundle(ROOT, "0.1.0", temporary / "second")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                first_checksum.read_text(encoding="utf-8").split()[0],
                second_checksum.read_text(encoding="utf-8").split()[0],
            )
            with zipfile.ZipFile(first) as bundle:
                names = set(bundle.namelist())
                self.assertIn("catalog/messages.json", names)
                self.assertIn("generated/manifest.json", names)
                self.assertIn("tests/test_validation.py", names)
                self.assertIn("tools/l10n", names)
                self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in bundle.infolist()))

    def test_bundle_rejects_unsafe_version_and_output_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="linguamesh-package-tests-") as directory:
            temporary = Path(directory)
            with self.assertRaisesRegex(ValueError, "semantic version"):
                build_bundle(ROOT, "../escape", temporary / "output")

            destination = temporary / "destination"
            destination.mkdir()
            output_link = temporary / "output-link"
            output_link.symlink_to(destination, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "must not be a symbolic link"):
                build_bundle(ROOT, "0.1.0", output_link)

    def test_bundle_rejects_symbolic_link_inputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="linguamesh-package-tests-") as directory:
            temporary = Path(directory)
            root = temporary / "repository"
            for relative in BUNDLE_DIRECTORIES:
                (root / relative).mkdir(parents=True)
            for relative in BUNDLE_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            target = temporary / "outside.txt"
            target.write_text("private fixture", encoding="utf-8")
            (root / "docs" / "linked.txt").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "must not be a symbolic link"):
                _bundle_files(root)


if __name__ == "__main__":
    unittest.main()

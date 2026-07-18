from __future__ import annotations

import copy
import hashlib
import json
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from linguamesh_l10n.generators import generate_android, generate_linux, generate_tree
from linguamesh_l10n.validation import validate_repository

ROOT = Path(__file__).resolve().parents[1]


def tree_bytes(path: Path) -> dict[str, bytes]:
    return {
        item.relative_to(path).as_posix(): item.read_bytes()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="linguamesh-generator-tests-")
        cls.output = Path(cls.temporary.name) / "generated"
        cls.manifest = generate_tree(ROOT, cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_committed_resources_are_deterministic(self) -> None:
        self.assertEqual(tree_bytes(ROOT / "generated"), tree_bytes(self.output))

    def test_manifest_hashes_every_generated_artifact(self) -> None:
        self.assertEqual("development", self.manifest["compatibility"]["status"])
        self.assertEqual(1, self.manifest["compatibility"]["platformResourceContractVersion"])
        for artifact in self.manifest["artifacts"]:
            path = self.output / artifact["path"]
            self.assertEqual(artifact["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(artifact["size"], path.stat().st_size)

    def test_android_and_windows_resources_are_well_formed_xml(self) -> None:
        android = list((self.output / "android").glob("*/strings.xml"))
        windows = list((self.output / "windows").glob("*/Resources.resw"))
        self.assertEqual(14, len(android))
        self.assertEqual(14, len(windows))
        for path in android + windows:
            ET.parse(path)
        arabic_pseudo = ET.parse(
            self.output / "android" / "values-b+ar+XB" / "strings.xml"
        )
        quantities = {
            item.attrib["quantity"]
            for item in arabic_pseudo.findall("./plurals[@name='document_file_count']/item")
        }
        self.assertEqual({"zero", "one", "two", "few", "many", "other"}, quantities)

    def test_macos_catalog_contains_all_locales_and_plural_variations(self) -> None:
        catalog = json.loads((self.output / "macos" / "Localizable.xcstrings").read_text(encoding="utf-8"))
        localizations = catalog["strings"]["document.file_count"]["localizations"]
        self.assertEqual(14, len(localizations))
        self.assertEqual(
            {"zero", "one", "two", "few", "many", "other"},
            set(localizations["ar"]["variations"]["plural"]),
        )

    def test_linux_catalogs_preserve_review_provenance(self) -> None:
        catalogs = list((self.output / "linux").glob("*/LC_MESSAGES/linguamesh.po"))
        self.assertEqual(14, len(catalogs))
        spanish = (self.output / "linux" / "es" / "LC_MESSAGES" / "linguamesh.po").read_text(encoding="utf-8")
        english = (self.output / "linux" / "en" / "LC_MESSAGES" / "linguamesh.po").read_text(encoding="utf-8")
        self.assertIn("X-LinguaMesh-Review-Status: unreviewed", spanish)
        self.assertIn("#, fuzzy", spanish)
        self.assertIn("X-LinguaMesh-Review-Status: source", english)

    def test_linux_mo_catalogs_are_valid_and_deterministic(self) -> None:
        catalogs = list((self.output / "linux").glob("*/LC_MESSAGES/linguamesh.mo"))
        self.assertEqual(14, len(catalogs))
        for path in catalogs:
            source = path.read_bytes()
            magic, version, count, original_offset, translation_offset, _, _ = struct.unpack(
                "<7I", source[:28]
            )
            self.assertEqual(0x950412DE, magic)
            self.assertEqual(0, version)
            self.assertGreaterEqual(count, 100)
            self.assertEqual(28, original_offset)
            self.assertEqual(original_offset + count * 8, translation_offset)
        english = (self.output / "linux" / "en" / "LC_MESSAGES" / "linguamesh.mo").read_bytes()
        self.assertIn(b"error.state.missing_source\x04", english)
        self.assertIn(b"Enter source text before translating.", english)

    def test_android_escapes_resource_syntax_without_changing_placeholders(self) -> None:
        catalog, _, packs = validate_repository(ROOT)
        english = copy.deepcopy(packs["en"])
        english["messages"]["provider.active"]["template"] = (
            'Don\'t say "stop" at C:\\tmp\n100% {provider}'
        )
        with tempfile.TemporaryDirectory(prefix="linguamesh-android-escaping-") as directory:
            output = Path(directory)
            generate_android(output, catalog, {"en": english})
            resources = ET.parse(output / "android" / "values" / "strings.xml")
            value = resources.find("./string[@name='provider_active']")
            self.assertIsNotNone(value)
            self.assertEqual(
                'Don\\\'t say \\"stop\\" at C:\\\\tmp\\n100%% %1$s',
                value.text,
            )

    def test_linux_escapes_headers_and_multiline_extracted_comments(self) -> None:
        catalog, _, packs = validate_repository(ROOT)
        catalog = copy.deepcopy(catalog)
        english = copy.deepcopy(packs["en"])
        english["locale"]["englishName"] = 'English "source" \\ team'
        catalog["messages"][0]["description"] = 'First line\nmsgid "not a directive"'
        with tempfile.TemporaryDirectory(prefix="linguamesh-po-escaping-") as directory:
            output = Path(directory)
            generate_linux(output, catalog, {"en": english})
            po_text = (output / "linux" / "en" / "LC_MESSAGES" / "linguamesh.po").read_text(encoding="utf-8")
            header_line = next(line for line in po_text.splitlines() if "Language-Team" in line)
            self.assertEqual('Language-Team: English "source" \\ team (source)\n', json.loads(header_line))
            self.assertIn('#. msgid "not a directive"', po_text)


if __name__ == "__main__":
    unittest.main()

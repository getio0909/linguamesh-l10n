from __future__ import annotations

import unittest
from pathlib import Path

from linguamesh_l10n.pseudo import create_pseudo_pack
from linguamesh_l10n.validation import template_placeholders, validate_locale_pack, validate_repository

ROOT = Path(__file__).resolve().parents[1]


class PseudoLocaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, cls.messages, _ = validate_repository(ROOT)

    def test_accented_pseudo_locale_expands_without_changing_placeholders(self) -> None:
        pack = create_pseudo_pack(self.catalog, "en-XA")
        validate_locale_pack(pack, self.catalog, self.messages, "en-XA")
        translated = pack["messages"]["provider.active"]["template"]
        self.assertIn("［", translated)
        self.assertEqual({"provider"}, template_placeholders(translated, "pseudo"))

    def test_rtl_pseudo_locale_uses_isolation_and_rtl_metadata(self) -> None:
        pack = create_pseudo_pack(self.catalog, "ar-XB")
        validate_locale_pack(pack, self.catalog, self.messages, "ar-XB")
        translated = pack["messages"]["translation.progress"]["template"]
        self.assertEqual("rtl", pack["locale"]["direction"])
        self.assertEqual(
            ["zero", "one", "two", "few", "many", "other"],
            pack["locale"]["pluralCategories"],
        )
        self.assertEqual(
            {"zero", "one", "two", "few", "many", "other"},
            set(pack["messages"]["document.file_count"]["variants"]),
        )
        self.assertTrue(translated.startswith("\u2067"))
        self.assertTrue(translated.endswith("\u2069"))
        self.assertEqual({"completed", "total"}, template_placeholders(translated, "pseudo"))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from linguamesh_l10n.validation import (
    PLURAL_CATEGORIES_BY_LOCALE,
    REQUIRED_LOCALES,
    ValidationError,
    load_json,
    validate_catalog,
    validate_locale_pack,
    validate_repository,
)

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, cls.messages, cls.packs = validate_repository(ROOT)

    def fixture(self, name: str) -> dict[str, object]:
        return load_json(ROOT / "tests" / "fixtures" / name)

    def test_required_locales_are_complete_and_honestly_marked(self) -> None:
        self.assertEqual(set(REQUIRED_LOCALES), set(self.packs))
        self.assertEqual("source", self.packs["en"]["translation"]["reviewStatus"])
        for tag in set(REQUIRED_LOCALES) - {"en"}:
            metadata = self.packs[tag]["translation"]
            self.assertEqual("draft", metadata["status"])
            self.assertEqual("unreviewed", metadata["reviewStatus"])
            self.assertTrue(metadata["machineGenerated"])

    def test_invalid_placeholder_fixture_is_rejected(self) -> None:
        fixture = self.fixture("invalid-placeholder.json")
        pack = copy.deepcopy(self.packs[fixture["locale"]])
        pack["messages"][fixture["message"]]["template"] = fixture["template"]
        with self.assertRaisesRegex(ValidationError, "placeholder identities"):
            validate_locale_pack(pack, self.catalog, self.messages, fixture["locale"])

    def test_missing_plural_branch_fixture_is_rejected(self) -> None:
        fixture = self.fixture("invalid-plural.json")
        pack = copy.deepcopy(self.packs[fixture["locale"]])
        pack["messages"][fixture["message"]]["variants"] = fixture["variants"]
        with self.assertRaisesRegex(ValidationError, "branches do not match"):
            validate_locale_pack(pack, self.catalog, self.messages, fixture["locale"])

    def test_invalid_select_branch_fixture_is_rejected(self) -> None:
        fixture = self.fixture("invalid-select.json")
        pack = copy.deepcopy(self.packs[fixture["locale"]])
        pack["messages"][fixture["message"]]["variants"] = fixture["variants"]
        with self.assertRaisesRegex(ValidationError, "branches do not match"):
            validate_locale_pack(pack, self.catalog, self.messages, fixture["locale"])

    def test_unknown_message_fixture_is_rejected(self) -> None:
        fixture = self.fixture("unknown-key.json")
        pack = copy.deepcopy(self.packs[fixture["locale"]])
        pack["messages"][fixture["key"]] = fixture["message"]
        with self.assertRaisesRegex(ValidationError, "unknown message keys"):
            validate_locale_pack(pack, self.catalog, self.messages, fixture["locale"])

    def test_rtl_and_plural_metadata_are_explicit(self) -> None:
        self.assertEqual("rtl", self.packs["ar"]["locale"]["direction"])
        self.assertEqual(
            ["zero", "one", "two", "few", "many", "other"],
            self.packs["ar"]["locale"]["pluralCategories"],
        )
        self.assertEqual(["one", "few", "many"], self.packs["ru"]["locale"]["gettextCategories"])
        for tag in REQUIRED_LOCALES:
            self.assertEqual(
                PLURAL_CATEGORIES_BY_LOCALE[tag],
                tuple(self.packs[tag]["locale"]["pluralCategories"]),
            )

    def test_android_required_plural_categories_cannot_be_removed(self) -> None:
        pack = copy.deepcopy(self.packs["es"])
        pack["locale"]["pluralCategories"] = ["one", "other"]
        for message in ("document.file_count", "error.rate_limited"):
            del pack["messages"][message]["variants"]["many"]
        with self.assertRaisesRegex(ValidationError, "must match required categories"):
            validate_locale_pack(pack, self.catalog, self.messages, "es")

    def test_json_input_size_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory(prefix="linguamesh-validation-tests-") as directory:
            path = Path(directory) / "oversized.json"
            path.write_bytes(b" " * (2 * 1024 * 1024 + 1))
            with self.assertRaisesRegex(ValidationError, "JSON input exceeds"):
                load_json(path)

    def test_platform_resource_identifier_collisions_are_rejected(self) -> None:
        android_catalog = copy.deepcopy(self.catalog)
        android_message = copy.deepcopy(self.messages["error.authentication_failed"])
        android_message["key"] = "error.authentication.failed"
        android_catalog["messages"].append(android_message)
        with self.assertRaisesRegex(ValidationError, "android resource identifier"):
            validate_catalog(android_catalog)

        windows_catalog = copy.deepcopy(self.catalog)
        windows_message = copy.deepcopy(self.messages["app.title"])
        windows_message["key"] = "history.mode.enabled"
        windows_catalog["messages"].append(windows_message)
        with self.assertRaisesRegex(ValidationError, "windows resource identifier"):
            validate_catalog(windows_catalog)

    def test_select_branches_must_be_safe_identifiers(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        message = next(item for item in catalog["messages"] if item["key"] == "history.mode")
        message["placeholders"]["mode"]["choices"] = ["../enabled"]
        message["placeholders"]["mode"]["example"] = "../enabled"
        message["value"]["variants"] = {"../enabled": "History is enabled"}
        with self.assertRaisesRegex(ValidationError, "must be a stable identifier"):
            validate_catalog(catalog)

    def test_review_metadata_cannot_overstate_message_review(self) -> None:
        pack = copy.deepcopy(self.packs["es"])
        pack["translation"].update(
            {
                "machineGenerated": False,
                "reviewStatus": "reviewed",
                "status": "reviewed",
            }
        )
        with self.assertRaisesRegex(ValidationError, "must be one of reviewed"):
            validate_locale_pack(pack, self.catalog, self.messages, "es")

    def test_generated_format_metadata_and_text_are_safe(self) -> None:
        metadata_pack = copy.deepcopy(self.packs["es"])
        metadata_pack["locale"]["englishName"] = "Spanish\nInjected-Header"
        with self.assertRaisesRegex(ValidationError, "single-line string"):
            validate_locale_pack(metadata_pack, self.catalog, self.messages, "es")

        text_pack = copy.deepcopy(self.packs["es"])
        text_pack["messages"]["app.title"]["template"] = "LinguaMesh\u0000"
        with self.assertRaisesRegex(ValidationError, "unsupported by XML 1.0"):
            validate_locale_pack(text_pack, self.catalog, self.messages, "es")

    def test_symbolic_link_json_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="linguamesh-validation-tests-") as directory:
            root = Path(directory)
            target = root / "target.json"
            target.write_text("{}", encoding="utf-8")
            link = root / "link.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(ValidationError, "must not be a symbolic link"):
                load_json(link)


if __name__ == "__main__":
    unittest.main()

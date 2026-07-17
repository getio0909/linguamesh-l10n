from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REQUIRED_LOCALES = (
    "en",
    "zh-Hans",
    "zh-Hant",
    "es",
    "fr",
    "de",
    "ja",
    "ko",
    "pt-BR",
    "ru",
    "ar",
    "hi",
)
PLATFORMS = ("android", "windows", "macos", "linux")
PLURAL_CATEGORIES = ("zero", "one", "two", "few", "many", "other")
PLURAL_CATEGORIES_BY_LOCALE = {
    "ar": ("zero", "one", "two", "few", "many", "other"),
    "ar-XB": ("zero", "one", "two", "few", "many", "other"),
    "de": ("one", "other"),
    "en": ("one", "other"),
    "en-XA": ("one", "other"),
    "es": ("one", "many", "other"),
    "fr": ("one", "many", "other"),
    "hi": ("one", "other"),
    "ja": ("other",),
    "ko": ("other",),
    "pt-BR": ("one", "many", "other"),
    "ru": ("one", "few", "many", "other"),
    "zh-Hans": ("other",),
    "zh-Hant": ("other",),
}
KEY_PATTERN = re.compile(r"^[a-z][a-z0-9]*(\.[a-z][a-z0-9_]*)+$")
PLACEHOLDER_PATTERN = re.compile(r"\{([a-z][a-z0-9_]*)\}")
SELECT_BRANCH_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
LOCALE_PATTERN = re.compile(r"^[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[0-9]{3}))?$")
GETTEXT_RULE_PATTERN = re.compile(
    r"^nplurals=([1-9][0-9]*); plural=[n0-9 ()+\-*/%<>=!&|?:]+;$"
)
MAX_JSON_BYTES = 2 * 1024 * 1024


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        if path.is_symlink():
            raise ValidationError(f"{path}: JSON input must not be a symbolic link")
        if path.stat().st_size > MAX_JSON_BYTES:
            raise ValidationError(f"{path}: JSON input exceeds {MAX_JSON_BYTES} bytes")
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValidationError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValidationError(f"{path}: cannot load JSON: {error}") from error
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: root must be an object")
    return data


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _fail(path: str, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def _object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    return value


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(path, "must be an array")
    return value


def _string(value: Any, path: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        _fail(path, "must be a non-empty string")
    for character in value:
        codepoint = ord(character)
        if not (
            codepoint in {0x09, 0x0A, 0x0D}
            or 0x20 <= codepoint <= 0xD7FF
            or 0xE000 <= codepoint <= 0xFFFD
            or 0x10000 <= codepoint <= 0x10FFFF
        ):
            _fail(path, "contains a character unsupported by XML 1.0")
    return value


def _single_line_string(value: Any, path: str) -> str:
    text = _string(value, path)
    if "\n" in text or "\r" in text:
        _fail(path, "must be a single-line string")
    return text


def _integer(value: Any, path: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        _fail(path, "must be an integer")
    return value


def _exact_keys(value: dict[str, Any], required: set[str], optional: set[str], path: str) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required - optional)
    if missing:
        _fail(path, f"missing keys: {', '.join(missing)}")
    if unknown:
        _fail(path, f"unknown keys: {', '.join(unknown)}")


def template_placeholders(template: str, path: str) -> set[str]:
    names = set(PLACEHOLDER_PATTERN.findall(template))
    remainder = PLACEHOLDER_PATTERN.sub("", template)
    if "{" in remainder or "}" in remainder:
        _fail(path, "contains malformed placeholder braces")
    return names


def _validate_schema_files(root: Path) -> None:
    schemas = {
        "catalog.schema.v1.json": "https://linguamesh.dev/schema/l10n/catalog.v1.json",
        "locale-pack.schema.v1.json": "https://linguamesh.dev/schema/l10n/locale-pack.v1.json",
    }
    for filename, schema_id in schemas.items():
        path = root / "schema" / filename
        schema = load_json(path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            _fail(str(path), "must declare JSON Schema draft 2020-12")
        if schema.get("$id") != schema_id:
            _fail(str(path), f"must declare schema identifier {schema_id}")


def _validate_placeholder(definition: Any, path: str) -> None:
    item = _object(definition, path)
    _exact_keys(item, {"type", "example"}, {"choices"}, path)
    kind = item["type"]
    if kind not in {"string", "integer", "number", "select"}:
        _fail(f"{path}.type", "must be string, integer, number, or select")
    example = item["example"]
    if kind == "string":
        _string(example, f"{path}.example", allow_empty=True)
    if kind == "integer" and (not isinstance(example, int) or isinstance(example, bool)):
        _fail(f"{path}.example", "must be an integer")
    if kind == "number" and (not isinstance(example, (int, float)) or isinstance(example, bool)):
        _fail(f"{path}.example", "must be a number")
    if kind == "select":
        choices = _array(item.get("choices"), f"{path}.choices")
        if not choices:
            _fail(f"{path}.choices", "must contain non-empty strings")
        for index, choice in enumerate(choices):
            choice_path = f"{path}.choices[{index}]"
            identifier = _string(choice, choice_path)
            if not SELECT_BRANCH_PATTERN.fullmatch(identifier):
                _fail(choice_path, "must be a stable identifier")
        if len(choices) != len(set(choices)):
            _fail(f"{path}.choices", "must not contain duplicates")
        if example not in choices:
            _fail(f"{path}.example", "must be one of the select choices")
    elif "choices" in item:
        _fail(f"{path}.choices", "is only valid for select placeholders")


def _android_name(key: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", key.lower())


def _validate_platform_resource_ids(messages: dict[str, dict[str, Any]], path: str) -> None:
    for platform in PLATFORMS:
        identifiers: dict[str, str] = {}
        for key, message in messages.items():
            if platform not in message["platforms"]:
                continue
            kind = message["value"]["type"]
            branches = message["value"]["variants"] if kind == "select" else {None: None}
            for branch in branches:
                logical_id = key if branch is None else f"{key}[{branch}]"
                if platform == "android":
                    native_id = _android_name(key) if branch is None else f"{_android_name(key)}__{branch}"
                elif branch is not None and platform in {"windows", "macos"}:
                    native_id = f"{key}.{branch}"
                elif branch is not None:
                    native_id = logical_id
                else:
                    native_id = key
                previous = identifiers.get(native_id)
                if previous is not None:
                    _fail(
                        f"{path}.messages",
                        f"{platform} resource identifier {native_id} collides between {previous} and {logical_id}",
                    )
                identifiers[native_id] = logical_id


def validate_catalog(catalog: dict[str, Any], path: str = "catalog/messages.json") -> dict[str, dict[str, Any]]:
    _exact_keys(
        catalog,
        {"schemaVersion", "catalogVersion", "sourceRevision", "sourceLocale", "messages"},
        set(),
        path,
    )
    if catalog["schemaVersion"] != 1:
        _fail(f"{path}.schemaVersion", "must equal 1")
    if not isinstance(catalog["catalogVersion"], str) or not SEMVER_PATTERN.fullmatch(catalog["catalogVersion"]):
        _fail(f"{path}.catalogVersion", "must be a semantic version")
    source_revision = _integer(catalog["sourceRevision"], f"{path}.sourceRevision")
    if source_revision < 1:
        _fail(f"{path}.sourceRevision", "must be positive")
    if catalog["sourceLocale"] != "en":
        _fail(f"{path}.sourceLocale", "must equal en")
    messages = _array(catalog["messages"], f"{path}.messages")
    if not messages:
        _fail(f"{path}.messages", "must not be empty")
    by_key: dict[str, dict[str, Any]] = {}
    for index, raw_message in enumerate(messages):
        message_path = f"{path}.messages[{index}]"
        message = _object(raw_message, message_path)
        _exact_keys(
            message,
            {
                "key",
                "description",
                "placeholders",
                "value",
                "platforms",
                "accessibilityContext",
                "status",
                "sourceRevision",
            },
            set(),
            message_path,
        )
        key = _string(message["key"], f"{message_path}.key")
        if not KEY_PATTERN.fullmatch(key):
            _fail(f"{message_path}.key", "must be a stable dotted identifier")
        if key in by_key:
            _fail(f"{message_path}.key", f"duplicates {key}")
        _string(message["description"], f"{message_path}.description")
        accessibility = message["accessibilityContext"]
        if accessibility is not None:
            _string(accessibility, f"{message_path}.accessibilityContext")
        platforms = _array(message["platforms"], f"{message_path}.platforms")
        if not platforms or len(platforms) != len(set(platforms)) or any(item not in PLATFORMS for item in platforms):
            _fail(f"{message_path}.platforms", "must contain unique supported platform identifiers")
        if message["status"] != "source":
            _fail(f"{message_path}.status", "must equal source")
        revision = _integer(message["sourceRevision"], f"{message_path}.sourceRevision")
        if revision < 1 or revision > source_revision:
            _fail(f"{message_path}.sourceRevision", "must be within the catalog source revision")
        placeholders = _object(message["placeholders"], f"{message_path}.placeholders")
        for name, definition in placeholders.items():
            if not re.fullmatch(r"^[a-z][a-z0-9_]*$", name):
                _fail(f"{message_path}.placeholders", f"invalid placeholder name {name}")
            _validate_placeholder(definition, f"{message_path}.placeholders.{name}")
        value = _object(message["value"], f"{message_path}.value")
        kind = value.get("type")
        if kind == "text":
            _exact_keys(value, {"type", "template"}, set(), f"{message_path}.value")
            template = _string(value["template"], f"{message_path}.value.template", allow_empty=True)
            expected = set(placeholders)
            if any(definition["type"] == "select" for definition in placeholders.values()):
                _fail(f"{message_path}.placeholders", "text messages cannot declare select placeholders")
            if template_placeholders(template, f"{message_path}.value.template") != expected:
                _fail(f"{message_path}.value.template", "placeholder identities do not match definitions")
        elif kind in {"plural", "select"}:
            _exact_keys(value, {"type", "selector", "variants"}, set(), f"{message_path}.value")
            selector = _string(value["selector"], f"{message_path}.value.selector")
            if selector not in placeholders:
                _fail(f"{message_path}.value.selector", "must name a declared placeholder")
            variants = _object(value["variants"], f"{message_path}.value.variants")
            if kind == "plural":
                if placeholders[selector]["type"] != "integer":
                    _fail(f"{message_path}.value.selector", "plural selectors must be integer placeholders")
                if set(variants) != {"one", "other"}:
                    _fail(f"{message_path}.value.variants", "English plurals must define one and other")
                expected = set(placeholders)
            else:
                if placeholders[selector]["type"] != "select":
                    _fail(f"{message_path}.value.selector", "select selectors must be select placeholders")
                choices = placeholders[selector]["choices"]
                if set(variants) != set(choices):
                    _fail(f"{message_path}.value.variants", "select branches must match declared choices")
                expected = set(placeholders) - {selector}
            for variant, template_value in variants.items():
                template = _string(template_value, f"{message_path}.value.variants.{variant}", allow_empty=True)
                if template_placeholders(template, f"{message_path}.value.variants.{variant}") != expected:
                    _fail(
                        f"{message_path}.value.variants.{variant}",
                        "placeholder identities do not match definitions",
                    )
        else:
            _fail(f"{message_path}.value.type", "must be text, plural, or select")
        by_key[key] = message
    _validate_platform_resource_ids(by_key, path)
    return by_key


def validate_locale_pack(
    pack: dict[str, Any],
    catalog: dict[str, Any],
    messages: dict[str, dict[str, Any]],
    filename_tag: str,
    path: str | None = None,
) -> None:
    pack_path = path or f"locales/{filename_tag}.json"
    _exact_keys(pack, {"schemaVersion", "catalogVersion", "sourceLocale", "locale", "translation", "messages"}, set(), pack_path)
    if pack["schemaVersion"] != 1:
        _fail(f"{pack_path}.schemaVersion", "must equal 1")
    if pack["catalogVersion"] != catalog["catalogVersion"]:
        _fail(f"{pack_path}.catalogVersion", "must match the canonical catalog")
    if pack["sourceLocale"] != "en":
        _fail(f"{pack_path}.sourceLocale", "must equal en")
    locale = _object(pack["locale"], f"{pack_path}.locale")
    _exact_keys(
        locale,
        {"tag", "englishName", "direction", "fallback", "pluralCategories", "gettextCategories", "gettextPluralRule"},
        set(),
        f"{pack_path}.locale",
    )
    tag = _string(locale["tag"], f"{pack_path}.locale.tag")
    if tag != filename_tag:
        _fail(f"{pack_path}.locale.tag", "must match the file name")
    if not LOCALE_PATTERN.fullmatch(tag):
        _fail(f"{pack_path}.locale.tag", "must be a supported BCP 47 identifier")
    _single_line_string(locale["englishName"], f"{pack_path}.locale.englishName")
    if locale["direction"] not in {"ltr", "rtl"}:
        _fail(f"{pack_path}.locale.direction", "must be ltr or rtl")
    expected_fallback = None if tag == "en" else "en"
    if locale["fallback"] != expected_fallback:
        _fail(f"{pack_path}.locale.fallback", f"must equal {expected_fallback}")
    plural_categories = _array(locale["pluralCategories"], f"{pack_path}.locale.pluralCategories")
    if not plural_categories or "other" not in plural_categories or len(plural_categories) != len(set(plural_categories)):
        _fail(f"{pack_path}.locale.pluralCategories", "must be unique and include other")
    if any(category not in PLURAL_CATEGORIES for category in plural_categories):
        _fail(f"{pack_path}.locale.pluralCategories", "contains an unknown CLDR plural category")
    required_plural_categories = PLURAL_CATEGORIES_BY_LOCALE.get(tag)
    if required_plural_categories is not None and tuple(plural_categories) != required_plural_categories:
        _fail(
            f"{pack_path}.locale.pluralCategories",
            f"must match required categories: {', '.join(required_plural_categories)}",
        )
    gettext_categories = _array(locale["gettextCategories"], f"{pack_path}.locale.gettextCategories")
    if not gettext_categories or len(gettext_categories) != len(set(gettext_categories)):
        _fail(f"{pack_path}.locale.gettextCategories", "must contain unique categories")
    if any(category not in plural_categories for category in gettext_categories):
        _fail(f"{pack_path}.locale.gettextCategories", "must be a subset of plural categories")
    rule = _single_line_string(locale["gettextPluralRule"], f"{pack_path}.locale.gettextPluralRule")
    rule_match = GETTEXT_RULE_PATTERN.fullmatch(rule)
    if not rule_match or int(rule_match.group(1)) != len(gettext_categories):
        _fail(f"{pack_path}.locale.gettextPluralRule", "nplurals must match gettextCategories")
    translation = _object(pack["translation"], f"{pack_path}.translation")
    _exact_keys(
        translation,
        {"status", "reviewStatus", "machineGenerated", "sourceRevision"},
        set(),
        f"{pack_path}.translation",
    )
    if not isinstance(translation["machineGenerated"], bool):
        _fail(f"{pack_path}.translation.machineGenerated", "must be a boolean")
    if translation["sourceRevision"] != catalog["sourceRevision"]:
        _fail(f"{pack_path}.translation.sourceRevision", "must match the catalog source revision")
    if tag == "en":
        if translation != {
            "status": "source",
            "reviewStatus": "source",
            "machineGenerated": False,
            "sourceRevision": catalog["sourceRevision"],
        }:
            _fail(f"{pack_path}.translation", "English must be the non-generated source pack")
    else:
        if translation["status"] not in {"draft", "reviewed"}:
            _fail(f"{pack_path}.translation.status", "must be draft or reviewed")
        if translation["reviewStatus"] not in {"unreviewed", "reviewed"}:
            _fail(f"{pack_path}.translation.reviewStatus", "must be unreviewed or reviewed")
        expected_review_status = "reviewed" if translation["status"] == "reviewed" else "unreviewed"
        if translation["reviewStatus"] != expected_review_status:
            _fail(f"{pack_path}.translation", "status and reviewStatus must describe the same review state")
        if translation["machineGenerated"] and (
            translation["status"] != "draft" or translation["reviewStatus"] != "unreviewed"
        ):
            _fail(f"{pack_path}.translation", "machine-generated packs must remain draft and unreviewed")
    translations = _object(pack["messages"], f"{pack_path}.messages")
    missing = sorted(messages.keys() - translations.keys())
    unknown = sorted(translations.keys() - messages.keys())
    if missing:
        _fail(f"{pack_path}.messages", f"missing message keys: {', '.join(missing)}")
    if unknown:
        _fail(f"{pack_path}.messages", f"unknown message keys: {', '.join(unknown)}")
    for key, source in messages.items():
        item_path = f"{pack_path}.messages.{key}"
        item = _object(translations[key], item_path)
        kind = source["value"]["type"]
        value_key = "template" if kind == "text" else "variants"
        _exact_keys(item, {"status", "sourceRevision", value_key}, set(), item_path)
        if item["sourceRevision"] != source["sourceRevision"]:
            _fail(f"{item_path}.sourceRevision", "must match the canonical message revision")
        allowed_statuses = {"source"} if tag == "en" else {translation["status"]}
        if item["status"] not in allowed_statuses:
            _fail(f"{item_path}.status", f"must be one of {', '.join(sorted(allowed_statuses))}")
        if translation["reviewStatus"] == "unreviewed" and item["status"] != "draft":
            _fail(f"{item_path}.status", "must remain draft while the pack is unreviewed")
        placeholders = source["placeholders"]
        if kind == "text":
            template = _string(item["template"], f"{item_path}.template", allow_empty=True)
            if template_placeholders(template, f"{item_path}.template") != set(placeholders):
                _fail(f"{item_path}.template", "placeholder identities do not match the canonical message")
            if tag == "en" and template != source["value"]["template"]:
                _fail(f"{item_path}.template", "English must match the canonical source")
        else:
            variants = _object(item["variants"], f"{item_path}.variants")
            selector = source["value"]["selector"]
            if kind == "plural":
                expected_branches = set(plural_categories)
                expected_placeholders = set(placeholders)
            else:
                expected_branches = set(source["value"]["variants"])
                expected_placeholders = set(placeholders) - {selector}
            if set(variants) != expected_branches:
                _fail(f"{item_path}.variants", "branches do not match the locale or canonical select definition")
            for branch, template_value in variants.items():
                template = _string(template_value, f"{item_path}.variants.{branch}", allow_empty=True)
                if template_placeholders(template, f"{item_path}.variants.{branch}") != expected_placeholders:
                    _fail(f"{item_path}.variants.{branch}", "placeholder identities do not match the canonical message")
            if tag == "en" and variants != source["value"]["variants"]:
                _fail(f"{item_path}.variants", "English must match the canonical source")


def load_repository(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    catalog_path = root / "catalog" / "messages.json"
    catalog = load_json(catalog_path)
    messages = validate_catalog(catalog, str(catalog_path.relative_to(root)))
    packs: dict[str, dict[str, Any]] = {}
    locales_path = root / "locales"
    for path in sorted(locales_path.glob("*.json")):
        tag = path.stem
        pack = load_json(path)
        validate_locale_pack(pack, catalog, messages, tag, str(path.relative_to(root)))
        packs[tag] = pack
    missing_locales = sorted(set(REQUIRED_LOCALES) - packs.keys())
    if missing_locales:
        _fail("locales", f"missing required official locale packs: {', '.join(missing_locales)}")
    unexpected_locales = sorted(packs.keys() - set(REQUIRED_LOCALES))
    if unexpected_locales:
        _fail("locales", f"unexpected official locale packs: {', '.join(unexpected_locales)}")
    compatibility = load_json(root / "compatibility.json")
    _exact_keys(
        compatibility,
        {
            "schemaVersion",
            "localizationVersion",
            "catalogSchemaVersion",
            "platformResourceContractVersion",
            "globalGoalSha256",
            "status",
            "minimumClientVersions",
            "limitations",
        },
        set(),
        "compatibility.json",
    )
    if compatibility["schemaVersion"] != 1 or compatibility["catalogSchemaVersion"] != catalog["schemaVersion"]:
        _fail("compatibility.json", "schema versions must match the canonical catalog contract")
    if compatibility["localizationVersion"] != catalog["catalogVersion"]:
        _fail("compatibility.json.localizationVersion", "must match the catalog version")
    if compatibility["platformResourceContractVersion"] != 1:
        _fail("compatibility.json.platformResourceContractVersion", "must equal 1")
    if compatibility["globalGoalSha256"] != "11f9a65927aac7e57e2af119e9d21cc98e8d5a08b8a112a19ee1c47903e36198":
        _fail("compatibility.json.globalGoalSha256", "must match the reviewed global-goal revision")
    if compatibility["status"] != "development":
        _fail("compatibility.json.status", "must remain development until client compatibility is verified")
    minimum_clients = _object(compatibility["minimumClientVersions"], "compatibility.json.minimumClientVersions")
    _exact_keys(minimum_clients, set(PLATFORMS), set(), "compatibility.json.minimumClientVersions")
    for platform, version in minimum_clients.items():
        if version is not None and (not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version)):
            _fail(f"compatibility.json.minimumClientVersions.{platform}", "must be null or a semantic version")
    limitations = _array(compatibility["limitations"], "compatibility.json.limitations")
    if not limitations or any(not isinstance(item, str) or not item for item in limitations):
        _fail("compatibility.json.limitations", "must contain explicit non-empty limitations")
    return catalog, messages, packs


def validate_repository(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    _validate_schema_files(root)
    return load_repository(root)


def source_json_paths(root: Path) -> list[Path]:
    paths = [root / "catalog" / "messages.json", root / "compatibility.json"]
    paths.extend(sorted((root / "schema").glob("*.json")))
    paths.extend(sorted((root / "locales").glob("*.json")))
    paths.extend(sorted((root / "tests" / "fixtures").glob("*.json")))
    return paths

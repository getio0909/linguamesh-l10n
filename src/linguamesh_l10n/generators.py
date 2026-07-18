from __future__ import annotations

import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .pseudo import create_pseudo_pack
from .validation import PLACEHOLDER_PATTERN, canonical_json, load_json, validate_locale_pack, validate_repository

PSEUDO_LOCALES = ("en-XA", "ar-XB")


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def _xml_text(root: ET.Element) -> str:
    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True, short_empty_elements=True) + "\n"


def _placeholder_order(message: dict[str, Any]) -> dict[str, int]:
    return {name: index for index, name in enumerate(message["placeholders"], start=1)}


def _format_template(template: str, message: dict[str, Any], platform: str) -> str:
    order = _placeholder_order(message)
    if platform == "android":
        escaped = (
            template.replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace("\r", "\\r")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace("%", "%%")
        )
    elif platform == "macos":
        escaped = template.replace("%", "%%")
    else:
        escaped = template

    def replacement(match: re.Match[str]) -> str:
        name = match.group(1)
        index = order[name]
        kind = message["placeholders"][name]["type"]
        if platform == "android":
            specifier = {"string": "s", "integer": "d", "number": ".2f"}[kind]
            return f"%{index}${specifier}"
        if platform == "macos":
            specifier = {"string": "@", "integer": "lld", "number": ".2f"}[kind]
            return f"%{index}${specifier}"
        if platform == "windows":
            return f"{{{index - 1}}}"
        return match.group(0)

    return PLACEHOLDER_PATTERN.sub(replacement, escaped)


def _android_name(key: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", key.lower())


def _android_directory(tag: str) -> str:
    if tag == "en":
        return "values"
    return "values-b+" + tag.replace("-", "+")


def _platform_messages(catalog: dict[str, Any], platform: str) -> list[dict[str, Any]]:
    return [message for message in catalog["messages"] if platform in message["platforms"]]


def generate_android(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
) -> None:
    for tag, pack in packs.items():
        resources = ET.Element("resources")
        for message in _platform_messages(catalog, "android"):
            key = message["key"]
            kind = message["value"]["type"]
            translated = pack["messages"][key]
            name = _android_name(key)
            if kind == "text":
                element = ET.SubElement(resources, "string", {"name": name})
                element.text = _format_template(translated["template"], message, "android")
            elif kind == "plural":
                plurals = ET.SubElement(resources, "plurals", {"name": name})
                for category in pack["locale"]["pluralCategories"]:
                    item = ET.SubElement(plurals, "item", {"quantity": category})
                    item.text = _format_template(translated["variants"][category], message, "android")
            else:
                for branch in message["value"]["variants"]:
                    element = ET.SubElement(resources, "string", {"name": f"{name}__{branch}"})
                    element.text = _format_template(translated["variants"][branch], message, "android")
        path = output / "android" / _android_directory(tag) / "strings.xml"
        _write_text(path, _xml_text(resources))


def _resw_data(root: ET.Element, name: str, value: str, description: str, status: str) -> None:
    element = ET.SubElement(root, "data", {"name": name})
    element.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    ET.SubElement(element, "value").text = value
    ET.SubElement(element, "comment").text = f"{description} Translation status: {status}."


def generate_windows(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
) -> None:
    for tag, pack in packs.items():
        root = ET.Element("root")
        headers = (
            ("resmimetype", "text/microsoft-resx"),
            ("version", "2.0"),
            ("reader", "System.Resources.ResXResourceReader, System.Windows.Forms"),
            ("writer", "System.Resources.ResXResourceWriter, System.Windows.Forms"),
        )
        for name, value in headers:
            header = ET.SubElement(root, "resheader", {"name": name})
            ET.SubElement(header, "value").text = value
        for message in _platform_messages(catalog, "windows"):
            key = message["key"]
            kind = message["value"]["type"]
            translated = pack["messages"][key]
            if kind == "text":
                _resw_data(
                    root,
                    key,
                    _format_template(translated["template"], message, "windows"),
                    message["description"],
                    translated["status"],
                )
            else:
                branch_order = (
                    pack["locale"]["pluralCategories"]
                    if kind == "plural"
                    else list(message["value"]["variants"])
                )
                for branch in branch_order:
                    _resw_data(
                        root,
                        f"{key}.{branch}",
                        _format_template(translated["variants"][branch], message, "windows"),
                        message["description"],
                        translated["status"],
                    )
        path = output / "windows" / tag / "Resources.resw"
        _write_text(path, _xml_text(root))


def _xcstrings_unit(template: str, message: dict[str, Any], status: str) -> dict[str, Any]:
    state = "translated" if status in {"source", "reviewed"} else "new"
    return {
        "stringUnit": {
            "state": state,
            "value": _format_template(template, message, "macos"),
        }
    }


def generate_macos(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
) -> None:
    strings: dict[str, Any] = {}
    for message in _platform_messages(catalog, "macos"):
        key = message["key"]
        kind = message["value"]["type"]
        if kind == "select":
            for branch in message["value"]["variants"]:
                localizations = {
                    tag: _xcstrings_unit(
                        pack["messages"][key]["variants"][branch],
                        message,
                        pack["messages"][key]["status"],
                    )
                    for tag, pack in packs.items()
                }
                strings[f"{key}.{branch}"] = {
                    "comment": message["description"],
                    "extractionState": "manual",
                    "localizations": localizations,
                }
        elif kind == "plural":
            localizations: dict[str, Any] = {}
            for tag, pack in packs.items():
                translated = pack["messages"][key]
                plural = {
                    category: _xcstrings_unit(
                        translated["variants"][category],
                        message,
                        translated["status"],
                    )
                    for category in pack["locale"]["pluralCategories"]
                }
                localizations[tag] = {"variations": {"plural": plural}}
            strings[key] = {
                "comment": message["description"],
                "extractionState": "manual",
                "localizations": localizations,
            }
        else:
            localizations = {
                tag: _xcstrings_unit(
                    pack["messages"][key]["template"],
                    message,
                    pack["messages"][key]["status"],
                )
                for tag, pack in packs.items()
            }
            strings[key] = {
                "comment": message["description"],
                "extractionState": "manual",
                "localizations": localizations,
            }
    document = {
        "sourceLanguage": "en",
        "strings": strings,
        "version": "1.0",
    }
    _write_text(output / "macos" / "Localizable.xcstrings", canonical_json(document))


def _po_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _po_header(name: str, value: str) -> str:
    return _po_escape(f"{name}: {value}\n")


def _po_entry_prefix(message: dict[str, Any], status: str) -> list[str]:
    lines = [f"#. {line}" for line in message["description"].splitlines()]
    if message["placeholders"]:
        lines.append("#, python-brace-format" if status != "draft" else "#, fuzzy, python-brace-format")
    elif status == "draft":
        lines.append("#, fuzzy")
    return lines


def generate_linux(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
) -> None:
    source_by_key = {message["key"]: message for message in catalog["messages"]}
    for tag, pack in packs.items():
        translation = pack["translation"]
        review_label = translation["reviewStatus"]
        translator = (
            "LinguaMesh source maintainers <noreply@linguamesh.invalid>"
            if tag == "en"
            else "LinguaMesh machine draft <noreply@linguamesh.invalid>"
        )
        lines = [
            'msgid ""',
            'msgstr ""',
            _po_header("Project-Id-Version", f"LinguaMesh {catalog['catalogVersion']}"),
            _po_header("Language", tag),
            _po_header("Language-Team", f"{pack['locale']['englishName']} ({review_label})"),
            _po_header("PO-Revision-Date", "2026-07-17 00:00+0000"),
            _po_header("Last-Translator", translator),
            _po_header("MIME-Version", "1.0"),
            _po_header("Content-Type", "text/plain; charset=UTF-8"),
            _po_header("Content-Transfer-Encoding", "8bit"),
            _po_header("Plural-Forms", pack["locale"]["gettextPluralRule"]),
            _po_header("X-LinguaMesh-Review-Status", review_label),
            _po_header("X-LinguaMesh-Machine-Generated", str(translation["machineGenerated"]).lower()),
            "",
        ]
        for key, message in source_by_key.items():
            if "linux" not in message["platforms"]:
                continue
            translated = pack["messages"][key]
            kind = message["value"]["type"]
            if kind == "text":
                lines.extend(_po_entry_prefix(message, translated["status"]))
                lines.extend(
                    [
                        f"msgctxt {_po_escape(key)}",
                        f"msgid {_po_escape(message['value']['template'])}",
                        f"msgstr {_po_escape(translated['template'])}",
                        "",
                    ]
                )
            elif kind == "plural":
                lines.extend(_po_entry_prefix(message, translated["status"]))
                lines.extend(
                    [
                        f"msgctxt {_po_escape(key)}",
                        f"msgid {_po_escape(message['value']['variants']['one'])}",
                        f"msgid_plural {_po_escape(message['value']['variants']['other'])}",
                    ]
                )
                for index, category in enumerate(pack["locale"]["gettextCategories"]):
                    lines.append(f"msgstr[{index}] {_po_escape(translated['variants'][category])}")
                lines.append("")
            else:
                for branch, source_template in message["value"]["variants"].items():
                    lines.extend(_po_entry_prefix(message, translated["status"]))
                    lines.extend(
                        [
                            f"msgctxt {_po_escape(f'{key}[{branch}]')}",
                            f"msgid {_po_escape(source_template)}",
                            f"msgstr {_po_escape(translated['variants'][branch])}",
                            "",
                        ]
                    )
        path = output / "linux" / tag / "LC_MESSAGES" / "linguamesh.po"
        _write_text(path, "\n".join(lines).rstrip() + "\n")


def _linux_mo_entries(
    catalog: dict[str, Any],
    pack: dict[str, Any],
) -> list[tuple[bytes, bytes]]:
    translation = pack["translation"]
    review_label = translation["reviewStatus"]
    header = "\n".join(
        [
            f"Project-Id-Version: LinguaMesh {catalog['catalogVersion']}",
            f"Language: {pack['locale']['tag']}",
            f"Language-Team: {pack['locale']['englishName']} ({review_label})",
            "PO-Revision-Date: 2026-07-17 00:00+0000",
            "Last-Translator: LinguaMesh source maintainers <noreply@linguamesh.invalid>"
            if pack["locale"]["tag"] == "en"
            else "Last-Translator: LinguaMesh machine draft <noreply@linguamesh.invalid>",
            "MIME-Version: 1.0",
            "Content-Type: text/plain; charset=UTF-8",
            "Content-Transfer-Encoding: 8bit",
            f"Plural-Forms: {pack['locale']['gettextPluralRule']}",
            f"X-LinguaMesh-Review-Status: {review_label}",
            f"X-LinguaMesh-Machine-Generated: {str(translation['machineGenerated']).lower()}",
            "",
        ]
    )
    entries: list[tuple[bytes, bytes]] = [(b"", header.encode("utf-8"))]
    for message in catalog["messages"]:
        if "linux" not in message["platforms"]:
            continue
        key = message["key"]
        translated = pack["messages"][key]
        kind = message["value"]["type"]
        if kind == "text":
            entries.append(
                (
                    f"{key}\x04{message['value']['template']}".encode("utf-8"),
                    translated["template"].encode("utf-8"),
                )
            )
        elif kind == "plural":
            msgid = (
                f"{key}\x04{message['value']['variants']['one']}"
                f"\x00{message['value']['variants']['other']}"
            )
            values = [translated["variants"][category] for category in pack["locale"]["gettextCategories"]]
            entries.append((msgid.encode("utf-8"), "\x00".join(values).encode("utf-8")))
        else:
            for branch, source_template in message["value"]["variants"].items():
                entries.append(
                    (
                        f"{key}[{branch}]\x04{source_template}".encode("utf-8"),
                        translated["variants"][branch].encode("utf-8"),
                    )
                )
    return sorted(entries, key=lambda entry: entry[0])


def _mo_bytes(entries: list[tuple[bytes, bytes]]) -> bytes:
    count = len(entries)
    original_table_offset = 28
    translation_table_offset = original_table_offset + count * 8
    string_offset = translation_table_offset + count * 8
    original_table: list[tuple[int, int]] = []
    translation_table: list[tuple[int, int]] = []
    string_data = bytearray()
    for original, translation in entries:
        original_table.append((len(original), string_offset + len(string_data)))
        string_data.extend(original)
        string_data.append(0)
        translation_table.append((len(translation), string_offset + len(string_data)))
        string_data.extend(translation)
        string_data.append(0)
    header = struct.pack(
        "<7I",
        0x950412DE,
        0,
        count,
        original_table_offset,
        translation_table_offset,
        0,
        0,
    )
    tables = b"".join(struct.pack("<2I", *item) for item in original_table + translation_table)
    return header + tables + bytes(string_data)


def generate_linux_mo(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
) -> None:
    for tag, pack in packs.items():
        path = output / "linux" / tag / "LC_MESSAGES" / "linguamesh.mo"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_mo_bytes(_linux_mo_entries(catalog, pack)))


def _manifest(
    output: Path,
    catalog: dict[str, Any],
    packs: dict[str, dict[str, Any]],
    compatibility: dict[str, Any],
) -> dict[str, Any]:
    artifacts = []
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item.name != "manifest.json"):
        content = path.read_bytes()
        artifacts.append(
            {
                "path": path.relative_to(output).as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
                "size": len(content),
            }
        )
    locales = []
    for tag, pack in packs.items():
        locales.append(
            {
                "direction": pack["locale"]["direction"],
                "machineGenerated": pack["translation"]["machineGenerated"],
                "reviewStatus": pack["translation"]["reviewStatus"],
                "status": pack["translation"]["status"],
                "tag": tag,
            }
        )
    return {
        "artifacts": artifacts,
        "catalogVersion": catalog["catalogVersion"],
        "compatibility": {
            "platformResourceContractVersion": compatibility["platformResourceContractVersion"],
            "status": compatibility["status"],
        },
        "locales": locales,
        "schemaVersion": 1,
        "sourceRevision": catalog["sourceRevision"],
    }


def generate_tree(root: Path, output: Path) -> dict[str, Any]:
    if output.is_symlink():
        raise ValueError(f"Generation destination must not be a symbolic link: {output}")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Generation destination must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    catalog, messages, official_packs = validate_repository(root)
    compatibility = load_json(root / "compatibility.json")
    packs = dict(official_packs)
    for tag in PSEUDO_LOCALES:
        pack = create_pseudo_pack(catalog, tag)
        validate_locale_pack(pack, catalog, messages, tag, f"generated/pseudo/{tag}.json")
        packs[tag] = pack
        _write_text(output / "pseudo" / f"{tag}.json", canonical_json(pack))
    generate_android(output, catalog, packs)
    generate_windows(output, catalog, packs)
    generate_macos(output, catalog, packs)
    generate_linux(output, catalog, packs)
    generate_linux_mo(output, catalog, packs)
    manifest = _manifest(output, catalog, packs, compatibility)
    _write_text(output / "manifest.json", canonical_json(manifest))
    return manifest

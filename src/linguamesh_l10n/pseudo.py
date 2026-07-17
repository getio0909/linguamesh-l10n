from __future__ import annotations

from typing import Any

from .validation import PLACEHOLDER_PATTERN, PLURAL_CATEGORIES_BY_LOCALE

ACCENTS = str.maketrans(
    {
        "A": "Å",
        "B": "Ɓ",
        "C": "Ç",
        "D": "Ð",
        "E": "Ë",
        "F": "Ƒ",
        "G": "Ĝ",
        "H": "Ħ",
        "I": "Ï",
        "J": "Ĵ",
        "K": "Ķ",
        "L": "Ŀ",
        "M": "Ṁ",
        "N": "Ñ",
        "O": "Ø",
        "P": "Þ",
        "Q": "Ǫ",
        "R": "Ŕ",
        "S": "Š",
        "T": "Ŧ",
        "U": "Û",
        "V": "Ṽ",
        "W": "Ŵ",
        "X": "Ẋ",
        "Y": "Ÿ",
        "Z": "Ž",
        "a": "å",
        "b": "ƀ",
        "c": "ç",
        "d": "ð",
        "e": "ë",
        "f": "ƒ",
        "g": "ĝ",
        "h": "ħ",
        "i": "ï",
        "j": "ĵ",
        "k": "ķ",
        "l": "ŀ",
        "m": "ṁ",
        "n": "ñ",
        "o": "ø",
        "p": "þ",
        "q": "ǫ",
        "r": "ŕ",
        "s": "š",
        "t": "ŧ",
        "u": "û",
        "v": "ṽ",
        "w": "ŵ",
        "x": "ẋ",
        "y": "ÿ",
        "z": "ž",
    }
)


def pseudo_template(template: str, tag: str) -> str:
    tokens: list[str] = []
    cursor = 0
    for match in PLACEHOLDER_PATTERN.finditer(template):
        literal = template[cursor : match.start()]
        if tag == "en-XA":
            tokens.append(literal.translate(ACCENTS))
        else:
            tokens.append(literal)
        tokens.append(match.group(0))
        cursor = match.end()
    tail = template[cursor:]
    tokens.append(tail.translate(ACCENTS) if tag == "en-XA" else tail)
    body = "".join(tokens)
    if tag == "en-XA":
        padding = "~" * max(2, len(template) // 3)
        return f"［{body}{padding}］"
    if tag == "ar-XB":
        return f"\u2067⟦{body}⟧\u2069"
    raise ValueError(f"Unsupported pseudo-locale: {tag}")


def create_pseudo_pack(catalog: dict[str, Any], tag: str) -> dict[str, Any]:
    if tag not in {"en-XA", "ar-XB"}:
        raise ValueError(f"Unsupported pseudo-locale: {tag}")
    direction = "rtl" if tag == "ar-XB" else "ltr"
    name = "Pseudo (Accented)" if tag == "en-XA" else "Pseudo (RTL)"
    plural_categories = list(PLURAL_CATEGORIES_BY_LOCALE[tag])
    messages: dict[str, Any] = {}
    for source in catalog["messages"]:
        value = source["value"]
        item: dict[str, Any] = {
            "sourceRevision": source["sourceRevision"],
            "status": "draft",
        }
        if value["type"] == "text":
            item["template"] = pseudo_template(value["template"], tag)
        elif value["type"] == "plural":
            item["variants"] = {
                branch: pseudo_template(value["variants"].get(branch, value["variants"]["other"]), tag)
                for branch in plural_categories
            }
        else:
            item["variants"] = {
                branch: pseudo_template(template, tag)
                for branch, template in value["variants"].items()
            }
        messages[source["key"]] = item
    return {
        "catalogVersion": catalog["catalogVersion"],
        "locale": {
            "direction": direction,
            "englishName": name,
            "fallback": "en",
            "gettextCategories": plural_categories,
            "gettextPluralRule": (
                "nplurals=6; plural=(n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : "
                "n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5);"
                if tag == "ar-XB"
                else "nplurals=2; plural=(n != 1);"
            ),
            "pluralCategories": plural_categories,
            "tag": tag,
        },
        "messages": messages,
        "schemaVersion": 1,
        "sourceLocale": "en",
        "translation": {
            "machineGenerated": True,
            "reviewStatus": "unreviewed",
            "sourceRevision": catalog["sourceRevision"],
            "status": "draft",
        },
    }

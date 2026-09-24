"""Loads content/*.yaml into a single normalized content dict."""

import re
from pathlib import Path

import yaml

CONTENT_DIR = Path(__file__).parent / "content"


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "item"


def _normalize_bullets(bullets):
    normalized = []
    for b in bullets or []:
        if isinstance(b, str):
            normalized.append({"text": b, "tier": "standard"})
        else:
            normalized.append({"text": b["text"], "tier": b.get("tier", "standard")})
    return normalized


def _normalize_experiences(entries):
    normalized = []
    for e in entries or []:
        e = dict(e)
        e["tier"] = e.get("tier", "standard")
        e["tags"] = e.get("tags", [])
        e["id"] = e.get("id") or slugify(f"{e.get('company', '')}-{e.get('role', '')}")
        e["description_bullets"] = _normalize_bullets(e.get("description_bullets"))
        normalized.append(e)
    return normalized


_META_FILES = {"sections", "theme"}


def load_all(content_dir=CONTENT_DIR):
    content = {}
    for path in sorted(content_dir.glob("*.yaml")):
        if path.stem in _META_FILES:
            continue
        with open(path, encoding="utf-8") as f:
            content[path.stem] = yaml.safe_load(f) or ([] if path.stem != "personal_info" else {})

    if "experiences" in content:
        content["experiences"] = _normalize_experiences(content["experiences"])
    for tagged_section in ("projects", "certificates"):
        if content.get(tagged_section):
            for item in content[tagged_section]:
                item.setdefault("tags", [])
                item.setdefault("id", slugify(item.get("name") or item.get("title") or ""))

    return content


def load_sections(content_dir=CONTENT_DIR):
    path = content_dir / "sections.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_theme(content_dir=CONTENT_DIR):
    path = content_dir / "theme.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

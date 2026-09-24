"""Tier filtering (feature B: summary vs. full) and target filtering (feature C: tailoring)."""

import copy

# Sections whose items carry an entry-level `tier` (highlight/standard) that
# summary mode filters on. Everything else is small enough to always show in
# full once its section is included at all.
TIERED_SECTIONS = {"experiences"}


def apply_tier_mode(content, sections_meta, mode):
    """Returns a deep copy of `content` filtered for the given --mode.

    mode == "full": nothing is dropped.
    mode == "summary": sections marked summary:false in sections.yaml are
    dropped entirely. Within a TIERED_SECTIONS section, every entry is kept
    (so the full career timeline still reads top to bottom) but a standard-
    tier entry's bullets are dropped -- it condenses to a one-line role/
    company/date mention -- while a highlight-tier entry keeps only its
    highlight-tier bullets.
    """
    content = copy.deepcopy(content)
    if mode == "full":
        return content

    summary_sections = {s["section"] for s in sections_meta if s.get("summary")}
    summary_sections.add("personal_info")  # always keep the header, it isn't a listed section
    for key in list(content.keys()):
        if key not in summary_sections:
            del content[key]

    for key in TIERED_SECTIONS & content.keys():
        for e in content[key]:
            if e.get("tier") == "highlight":
                e["description_bullets"] = [b for b in e["description_bullets"] if b["tier"] == "highlight"]
            else:
                e["description_bullets"] = []

    return content


def apply_target(content, target):
    """Returns a deep copy of `content` filtered/reordered per a targets/*.yaml config."""
    content = copy.deepcopy(content)

    overrides = target.get("personal_info_overrides") or {}
    if overrides and "personal_info" in content:
        content["personal_info"].update(overrides)

    for section, rules in (target.get("sections") or {}).items():
        if section not in content:
            continue
        if rules.get("exclude_all"):
            content[section] = []
            continue

        items = content[section]

        include_tags = rules.get("include_tags")
        if include_tags:
            items = [i for i in items if set(i.get("tags", [])) & set(include_tags)]

        exclude_ids = set(rules.get("exclude_ids") or [])
        if exclude_ids:
            items = [i for i in items if i.get("id") not in exclude_ids]

        bullet_tags = rules.get("bullet_include_tags")
        if bullet_tags and section == "experiences":
            for i in items:
                i["description_bullets"] = [
                    b for b in i["description_bullets"]
                    if not bullet_tags or b.get("tier") == "highlight"
                ]

        order = rules.get("order")
        if order:
            by_id = {i["id"]: i for i in items}
            ordered = [by_id.pop(oid) for oid in order if oid in by_id]
            items = ordered + list(by_id.values())

        content[section] = items

    return content

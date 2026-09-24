"""Loads and lists targets/*.yaml tailoring configs."""

from pathlib import Path

import yaml

TARGETS_DIR = Path(__file__).parent / "targets"


def list_target_names():
    return sorted(
        p.stem for p in TARGETS_DIR.glob("*.yaml")
        if not p.stem.startswith("_")
    )


def load_target(name):
    path = TARGETS_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No such target: {name} (expected {path})")
    with open(path, encoding="utf-8") as f:
        target = yaml.safe_load(f)
    target.setdefault("output_slug", name)
    return target

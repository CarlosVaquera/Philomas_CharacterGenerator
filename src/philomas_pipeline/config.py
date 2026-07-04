from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .paths import animations_path, character_path, project_style_path


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return data


def load_character(character_id: str, root: Path | None = None) -> dict[str, Any]:
    return load_yaml(character_path(character_id, root))


def load_project_style(root: Path | None = None) -> dict[str, Any]:
    return load_yaml(project_style_path(root))


def load_animations(root: Path | None = None) -> dict[str, int]:
    data = load_yaml(animations_path(root))
    return {str(name): int(count) for name, count in data.items()}


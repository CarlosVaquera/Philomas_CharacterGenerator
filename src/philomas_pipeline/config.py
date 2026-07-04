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


def normalize_animation(name: str, value: Any) -> dict[str, Any]:
    if isinstance(value, int):
        return {
            "frames": value,
            "loop": True,
            "frame_duration_ms": 100,
        }
    if not isinstance(value, dict):
        raise ValueError(f"Animation '{name}' must be an integer or mapping")

    frames = int(value.get("frames", 0))
    if frames <= 0:
        raise ValueError(f"Animation '{name}' must define a positive frame count")

    return {
        "frames": frames,
        "loop": bool(value.get("loop", True)),
        "frame_duration_ms": int(value.get("frame_duration_ms", 100)),
    }


def load_animations(root: Path | None = None) -> dict[str, dict[str, Any]]:
    data = load_yaml(animations_path(root))
    return {str(name): normalize_animation(str(name), value) for name, value in data.items()}

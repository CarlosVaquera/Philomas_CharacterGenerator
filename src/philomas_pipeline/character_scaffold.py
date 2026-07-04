from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .paths import (
    character_path,
    clean_asset_dir,
    export_asset_dir,
    find_project_root,
    generated_prompt_dir,
    raw_asset_dir,
)

CHARACTER_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def validate_character_id(character_id: str) -> str:
    normalized = character_id.strip().lower()
    if not CHARACTER_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Character id must use lowercase letters, numbers, hyphens, or underscores, "
            "and must start with a letter or number"
        )
    return normalized


def default_character_data(character_id: str, name: str | None = None) -> dict[str, Any]:
    display_name = name.strip() if name and name.strip() else character_id.replace("_", " ").replace("-", " ").title()
    return {
        "name": display_name,
        "role": "TODO: Character role",
        "theme": "TODO: Character theme",
        "personality": [
            "TODO: personality trait",
            "TODO: personality trait",
        ],
        "physical_appearance": {
            "build": "TODO",
            "hair": "TODO",
            "face": "TODO",
            "silhouette": "TODO",
        },
        "clothing": {
            "top": "TODO",
            "bottom": "TODO",
            "shoes": "TODO",
        },
        "equipment": {
            "primary": "TODO",
        },
        "supernatural_theme": [
            "TODO: supernatural motif",
        ],
        "palette": {
            "primary": [
                "#D72638",
                "#101820",
                "#F2E8CF",
            ],
            "accents": [
                "#15E6CD",
                "#F7C531",
                "#7A1CAC",
            ],
        },
        "frame_size": [
            112,
            192,
        ],
        "sheet_layout": [
            12,
            12,
        ],
        "hitbox": [
            30,
            24,
            52,
            168,
        ],
    }


def ensure_gitkeep(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    gitkeep_path = directory / ".gitkeep"
    gitkeep_path.touch(exist_ok=True)
    return gitkeep_path


def create_character(
    character_id: str,
    name: str | None = None,
    root: Path | None = None,
    force: bool = False,
) -> dict[str, Path]:
    project_root = root or find_project_root()
    normalized_id = validate_character_id(character_id)
    path = character_path(normalized_id, project_root)

    if path.exists() and not force:
        raise FileExistsError(f"Character already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    data = default_character_data(normalized_id, name)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    generated_dir = generated_prompt_dir(normalized_id, project_root)
    raw_dir = raw_asset_dir(normalized_id, project_root)
    clean_dir = clean_asset_dir(normalized_id, project_root)
    export_dir = export_asset_dir(normalized_id, project_root)

    for directory in (generated_dir, raw_dir, clean_dir, export_dir):
        ensure_gitkeep(directory)

    return {
        "character": path,
        "prompts": generated_dir,
        "raw_assets": raw_dir,
        "clean_assets": clean_dir,
        "export_assets": export_dir,
    }

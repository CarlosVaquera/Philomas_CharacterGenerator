from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__
from .config import load_animations, load_character
from .frame_exporter import build_animation_frame_manifest
from .paths import (
    animation_manifest_path,
    clean_spritesheet_path,
    exported_frames_dir,
    find_project_root,
)

def project_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def build_engine_animation_manifest(
    character_id: str,
    root: Path | None = None,
) -> dict[str, Any]:
    project_root = root or find_project_root()
    character = load_character(character_id, project_root)
    animations = load_animations(project_root)
    frame_manifest = build_animation_frame_manifest(
        animations,
        exported_frames_dir(character_id, project_root),
    )

    engine_animations: dict[str, Any] = {}
    for animation_name, animation_data in frame_manifest.items():
        engine_animations[animation_name] = {
            "loop": animation_data["loop"],
            "frame_duration_ms": animation_data["frame_duration_ms"],
            "start_frame": animation_data["start_frame"],
            "frame_count": animation_data["frame_count"],
            "frames": [
                project_relative(path, project_root)
                for path in animation_data["paths"]
            ],
        }

    return {
        "version": __version__,
        "schema": "philomas.animation_manifest.v1",
        "character": {
            "id": character_id,
            "name": character["name"],
        },
        "frame_size": character["frame_size"],
        "sheet_layout": character["sheet_layout"],
        "hitbox": character["hitbox"],
        "source": {
            "clean_spritesheet": project_relative(
                clean_spritesheet_path(character_id, project_root),
                project_root,
            ),
        },
        "animations": engine_animations,
    }


def export_animation_manifest(
    character_id: str,
    root: Path | None = None,
) -> Path:
    project_root = root or find_project_root()
    output_path = animation_manifest_path(character_id, project_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = build_engine_animation_manifest(
        character_id,
        project_root,
    )
    output_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return output_path

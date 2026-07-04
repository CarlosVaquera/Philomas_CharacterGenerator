from __future__ import annotations

import json
from pathlib import Path

from . import __version__
from .config import load_animations, load_character
from .frame_exporter import build_animation_frame_manifest
from .paths import (
    animation_manifest_path,
    character_path,
    clean_spritesheet_path,
    export_asset_dir,
    exported_frames_dir,
    find_project_root,
    generated_prompt_dir,
    placeholder_spritesheet_path,
    project_style_path,
    qa_report_path,
)


def project_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def export_metadata(character_id: str, root: Path | None = None) -> Path:
    project_root = root or find_project_root()
    character = load_character(character_id, project_root)
    animations = load_animations(project_root)
    prompt_dir = generated_prompt_dir(character_id, project_root)
    output_dir = export_asset_dir(character_id, project_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt_paths = sorted(path for path in prompt_dir.glob("*.txt") if path.is_file())
    frame_manifest = build_animation_frame_manifest(
        animations,
        exported_frames_dir(character_id, project_root),
    )
    metadata_frame_exports = {
        animation_name: {
            "start_frame": animation_data["start_frame"],
            "frame_count": animation_data["frame_count"],
            "loop": animation_data["loop"],
            "frame_duration_ms": animation_data["frame_duration_ms"],
            "paths": [
                project_relative(path, project_root)
                for path in animation_data["paths"]
            ],
        }
        for animation_name, animation_data in frame_manifest.items()
    }
    metadata = {
        "version": __version__,
        "character": {
            "id": character_id,
            "name": character["name"],
            "role": character["role"],
            "theme": character["theme"],
        },
        "frame_size": character["frame_size"],
        "sheet_layout": character["sheet_layout"],
        "animations": animations,
        "hitbox": character["hitbox"],
        "source_paths": {
            "character": project_relative(character_path(character_id, project_root), project_root),
            "project_style": project_relative(project_style_path(project_root), project_root),
            "raw_spritesheet": project_relative(
                placeholder_spritesheet_path(character_id, project_root),
                project_root,
            ),
            "clean_spritesheet": project_relative(
                clean_spritesheet_path(character_id, project_root),
                project_root,
            ),
            "animation_manifest": project_relative(
                animation_manifest_path(character_id, project_root),
                project_root,
            ),
            "qa_report": project_relative(
                qa_report_path(character_id, project_root),
                project_root,
            ),
        },
        "generated_prompt_paths": [project_relative(path, project_root) for path in prompt_paths],
        "frame_exports": metadata_frame_exports,
    }

    output_path = output_dir / "metadata.json"
    output_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return output_path

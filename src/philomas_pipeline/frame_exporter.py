from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image

from .config import load_animations, load_character
from .paths import exported_frames_dir, find_project_root, placeholder_spritesheet_path
from .sprite_sheet import crop_frame, validate_sheet_size


def build_animation_frame_manifest(
    animations: dict[str, int],
    output_root: Path,
) -> dict[str, dict[str, Any]]:
    manifest: dict[str, dict[str, Any]] = {}
    global_frame = 0
    for animation_name, frame_count in animations.items():
        paths = [
            output_root / animation_name / f"{animation_name}_{frame_index:03d}.png"
            for frame_index in range(frame_count)
        ]
        manifest[animation_name] = {
            "start_frame": global_frame,
            "frame_count": frame_count,
            "paths": paths,
        }
        global_frame += frame_count
    return manifest


def export_animation_frames(
    character_id: str,
    root: Path | None = None,
    image_path: Path | None = None,
) -> dict[str, dict[str, Any]]:
    project_root = root or find_project_root()
    character = load_character(character_id, project_root)
    animations = load_animations(project_root)

    frame_width, frame_height = character["frame_size"]
    columns, rows = character["sheet_layout"]
    capacity = int(columns) * int(rows)
    requested_frames = sum(int(count) for count in animations.values())
    if requested_frames > capacity:
        raise ValueError(
            f"Animation frame count {requested_frames} exceeds sheet capacity {capacity}"
        )

    source_path = image_path or placeholder_spritesheet_path(character_id, project_root)
    output_root = exported_frames_dir(character_id, project_root)
    manifest = build_animation_frame_manifest(animations, output_root)

    with Image.open(source_path) as image:
        image.load()
        validate_sheet_size(image, int(columns), int(rows), int(frame_width), int(frame_height))

        for animation_name, animation_data in manifest.items():
            animation_dir = output_root / animation_name
            animation_dir.mkdir(parents=True, exist_ok=True)
            for old_frame in animation_dir.glob("*.png"):
                old_frame.unlink()

            start_frame = int(animation_data["start_frame"])
            for local_frame_index, output_path in enumerate(animation_data["paths"]):
                global_frame = start_frame + local_frame_index
                col = global_frame % int(columns)
                row = global_frame // int(columns)
                frame = crop_frame(image, col, row, int(frame_width), int(frame_height))
                frame.save(output_path)

    return manifest

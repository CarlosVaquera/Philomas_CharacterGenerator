from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from .config import load_animations, load_character
from .frame_exporter import build_animation_frame_manifest
from .paths import (
    animation_manifest_path,
    clean_spritesheet_path,
    exported_frames_dir,
    find_project_root,
    placeholder_spritesheet_path,
    qa_report_path,
)
from .validator import validate_character


def project_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def alpha_bbox(path: Path) -> tuple[int, int, int, int] | None:
    with Image.open(path) as image:
        frame = image.convert("RGBA")
        return frame.getchannel("A").getbbox()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def summarize_bounding_boxes(
    boxes: list[tuple[int, int, int, int]],
) -> dict[str, int]:
    if not boxes:
        return {
            "max_width_delta": 0,
            "max_height_delta": 0,
            "max_center_x_delta": 0,
            "max_center_y_delta": 0,
        }

    widths = [right - left for left, _top, right, _bottom in boxes]
    heights = [bottom - top for _left, top, _right, bottom in boxes]
    centers_x = [(left + right) // 2 for left, _top, right, _bottom in boxes]
    centers_y = [(top + bottom) // 2 for _left, top, _right, bottom in boxes]
    return {
        "max_width_delta": max(widths) - min(widths),
        "max_height_delta": max(heights) - min(heights),
        "max_center_x_delta": max(centers_x) - min(centers_x),
        "max_center_y_delta": max(centers_y) - min(centers_y),
    }


def build_qa_report(character_id: str, root: Path | None = None) -> dict[str, Any]:
    project_root = root or find_project_root()
    character = load_character(character_id, project_root)
    animations = load_animations(project_root)
    frame_width, frame_height = character["frame_size"]
    columns, rows = character["sheet_layout"]
    expected_sheet_size = [int(frame_width) * int(columns), int(frame_height) * int(rows)]

    validation = validate_character(character_id, project_root)
    frame_manifest = build_animation_frame_manifest(
        animations,
        exported_frames_dir(character_id, project_root),
    )

    expected_frame_paths = [
        path
        for animation_data in frame_manifest.values()
        for path in animation_data["paths"]
    ]
    exported_frame_paths = sorted(exported_frames_dir(character_id, project_root).glob("*/*.png"))
    missing_exported_frames = [
        project_relative(path, project_root)
        for path in expected_frame_paths
        if not path.exists()
    ]
    unexpected_exported_frames = [
        project_relative(path, project_root)
        for path in exported_frame_paths
        if path not in expected_frame_paths
    ]

    empty_frames: list[str] = []
    frame_size_mismatches: list[dict[str, Any]] = []
    boxes: list[tuple[int, int, int, int]] = []
    for path in expected_frame_paths:
        if not path.exists():
            continue
        size = image_size(path)
        if size != (int(frame_width), int(frame_height)):
            frame_size_mismatches.append(
                {
                    "path": project_relative(path, project_root),
                    "size": list(size),
                    "expected_size": [int(frame_width), int(frame_height)],
                }
            )
        bbox = alpha_bbox(path)
        if bbox is None:
            empty_frames.append(project_relative(path, project_root))
        else:
            boxes.append(bbox)

    clean_path = clean_spritesheet_path(character_id, project_root)
    raw_path = placeholder_spritesheet_path(character_id, project_root)
    manifest_path = animation_manifest_path(character_id, project_root)
    requested_animation_frames = sum(int(spec["frames"]) for spec in animations.values())
    total_sheet_frames = int(columns) * int(rows)

    errors = list(validation.errors)
    if missing_exported_frames:
        errors.append(f"Missing exported frames: {len(missing_exported_frames)}")
    if empty_frames:
        errors.append(f"Empty exported frames: {len(empty_frames)}")
    if frame_size_mismatches:
        errors.append(f"Frame size mismatches: {len(frame_size_mismatches)}")

    warnings = list(validation.warnings)
    if unexpected_exported_frames:
        warnings.append(f"Unexpected exported frames: {len(unexpected_exported_frames)}")

    return {
        "character_id": character_id,
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "sheet": {
            "frame_size": character["frame_size"],
            "sheet_layout": character["sheet_layout"],
            "expected_sheet_size": expected_sheet_size,
            "total_sheet_frames": total_sheet_frames,
            "requested_animation_frames": requested_animation_frames,
            "unused_sheet_frames": total_sheet_frames - requested_animation_frames,
        },
        "paths": {
            "raw_spritesheet": project_relative(raw_path, project_root),
            "clean_spritesheet": project_relative(clean_path, project_root),
            "animation_manifest": project_relative(manifest_path, project_root),
        },
        "exports": {
            "expected_frame_count": requested_animation_frames,
            "exported_frame_count": len(exported_frame_paths),
            "missing_exported_frames": missing_exported_frames,
            "unexpected_exported_frames": unexpected_exported_frames,
            "empty_frames": empty_frames,
            "frame_size_mismatches": frame_size_mismatches,
            "bounding_box_consistency": summarize_bounding_boxes(boxes),
        },
    }


def export_qa_report(character_id: str, root: Path | None = None) -> Path:
    project_root = root or find_project_root()
    output_path = qa_report_path(character_id, project_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = build_qa_report(character_id, project_root)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return output_path

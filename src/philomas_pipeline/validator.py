from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image

from .config import load_animations, load_character
from .models import ValidationReport
from .paths import clean_spritesheet_path

REQUIRED_CHARACTER_FIELDS = {
    "name",
    "role",
    "theme",
    "personality",
    "physical_appearance",
    "clothing",
    "equipment",
    "supernatural_theme",
    "palette",
    "frame_size",
    "sheet_layout",
    "hitbox",
}


def validate_character_metadata(character: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CHARACTER_FIELDS - set(character))
    if missing:
        errors.append(f"Character metadata is missing required fields: {', '.join(missing)}")

    for field, expected_length in (("frame_size", 2), ("sheet_layout", 2), ("hitbox", 4)):
        value = character.get(field)
        if not isinstance(value, list) or len(value) != expected_length:
            errors.append(f"Character field '{field}' must be a list of {expected_length} numbers")
            continue
        if not all(isinstance(item, int) and item > 0 for item in value):
            errors.append(f"Character field '{field}' must contain positive integers")

    return errors


def image_has_transparency(image: Image.Image) -> bool:
    if image.mode != "RGBA":
        return False
    alpha = image.getchannel("A")
    min_alpha, max_alpha = alpha.getextrema()
    return min_alpha < 255 and max_alpha > 0


def validate_character(
    character_id: str,
    root: Path | None = None,
    image_path: Path | None = None,
) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        character = load_character(character_id, root)
    except Exception as exc:
        return ValidationReport(character_id, [str(exc)], warnings)

    errors.extend(validate_character_metadata(character))

    try:
        animations = load_animations(root)
    except Exception as exc:
        errors.append(str(exc))
        animations = {}

    path = image_path or clean_spritesheet_path(character_id, root)
    if not path.exists():
        errors.append(f"PNG does not exist: {path}")
        return ValidationReport(character_id, errors, warnings)

    try:
        with Image.open(path) as image:
            image.load()
            frame_width, frame_height = character.get("frame_size", [0, 0])
            columns, rows = character.get("sheet_layout", [0, 0])
            expected_size = (int(frame_width) * int(columns), int(frame_height) * int(rows))

            if image.format != "PNG":
                errors.append(f"Asset must be a PNG file: {path}")
            if image.mode != "RGBA":
                errors.append(f"PNG must be RGBA; found {image.mode}")
            if image.size != expected_size:
                errors.append(f"PNG size {image.size} does not match expected {expected_size}")
            if not image_has_transparency(image):
                errors.append("PNG must contain transparent and non-transparent pixels")

            expected_frames = int(columns) * int(rows)
            animation_frames = sum(int(spec["frames"]) for spec in animations.values())
            if expected_frames != 144:
                warnings.append(f"Sheet contains {expected_frames} frames; Pepe placeholder target is 144")
            if animation_frames > expected_frames:
                errors.append(
                    f"Animation frame count {animation_frames} exceeds sheet capacity {expected_frames}"
                )
    except Exception as exc:
        errors.append(f"Could not inspect PNG '{path}': {exc}")

    return ValidationReport(character_id, errors, warnings)

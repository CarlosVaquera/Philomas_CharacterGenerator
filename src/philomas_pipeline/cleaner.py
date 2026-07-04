from __future__ import annotations

from pathlib import Path

from PIL import Image

from .config import load_character
from .paths import clean_spritesheet_path, find_project_root, placeholder_spritesheet_path
from .sprite_sheet import validate_sheet_size


def clean_spritesheet(
    character_id: str,
    root: Path | None = None,
    source_path: Path | None = None,
) -> Path:
    project_root = root or find_project_root()
    character = load_character(character_id, project_root)
    frame_width, frame_height = character["frame_size"]
    columns, rows = character["sheet_layout"]

    input_path = source_path or placeholder_spritesheet_path(character_id, project_root)
    if not input_path.exists():
        raise FileNotFoundError(f"Raw spritesheet does not exist: {input_path}")

    output_path = clean_spritesheet_path(character_id, project_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as image:
        image.load()
        cleaned = image.convert("RGBA")
        validate_sheet_size(
            cleaned,
            int(columns),
            int(rows),
            int(frame_width),
            int(frame_height),
        )
        cleaned.save(output_path)

    return output_path

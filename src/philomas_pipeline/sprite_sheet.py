from __future__ import annotations

from collections.abc import Iterator

from PIL import Image


def get_frame_box(
    col: int,
    row: int,
    frame_width: int,
    frame_height: int,
) -> tuple[int, int, int, int]:
    if col < 0 or row < 0:
        raise ValueError("Frame column and row must be non-negative")
    left = col * frame_width
    top = row * frame_height
    return left, top, left + frame_width, top + frame_height


def validate_sheet_size(
    image: Image.Image,
    columns: int,
    rows: int,
    frame_width: int,
    frame_height: int,
) -> None:
    expected = (columns * frame_width, rows * frame_height)
    if image.size != expected:
        raise ValueError(f"Invalid spritesheet size {image.size}; expected {expected}")


def crop_frame(
    image: Image.Image,
    col: int,
    row: int,
    frame_width: int,
    frame_height: int,
) -> Image.Image:
    if (col + 1) * frame_width > image.width or (row + 1) * frame_height > image.height:
        raise ValueError(f"Frame ({col}, {row}) is outside image bounds {image.size}")
    return image.crop(get_frame_box(col, row, frame_width, frame_height))


def iter_frames(
    image: Image.Image,
    columns: int,
    rows: int,
    frame_width: int,
    frame_height: int,
) -> Iterator[tuple[int, int, Image.Image]]:
    validate_sheet_size(image, columns, rows, frame_width, frame_height)
    for row in range(rows):
        for col in range(columns):
            yield col, row, crop_frame(image, col, row, frame_width, frame_height)


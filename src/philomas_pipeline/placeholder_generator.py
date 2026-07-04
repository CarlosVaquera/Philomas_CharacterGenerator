from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from .config import load_character
from .paths import placeholder_spritesheet_path


def generate_placeholder_spritesheet(
    character_id: str,
    root: Path | None = None,
) -> Path:
    character = load_character(character_id, root)
    frame_width, frame_height = character["frame_size"]
    columns, rows = character["sheet_layout"]
    width = int(frame_width) * int(columns)
    height = int(frame_height) * int(rows)

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")

    total_frames = int(columns) * int(rows)
    for index in range(total_frames):
        col = index % int(columns)
        row = index // int(columns)
        x0 = col * int(frame_width)
        y0 = row * int(frame_height)
        draw_pose(draw, x0, y0, int(frame_width), int(frame_height), index)

    output_path = placeholder_spritesheet_path(character_id, root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


def draw_pose(
    draw: ImageDraw.ImageDraw,
    frame_x: int,
    frame_y: int,
    frame_width: int,
    frame_height: int,
    frame_index: int,
) -> None:
    phase = frame_index % 12
    lean = (phase - 5) // 2
    bob = 2 if phase in {1, 2, 7, 8} else 0
    arm_swing = (phase % 4) - 1

    cx = frame_x + frame_width // 2 + lean
    ground = frame_y + frame_height - 14 - bob
    head_color = (242, 232, 207, 255)
    jacket_color = (215, 38, 56, 255)
    pants_color = (16, 24, 32, 255)
    accent_color = (21, 230, 205, 210)
    guitar_color = (247, 197, 49, 255)
    shadow_color = (0, 0, 0, 80)

    draw.ellipse((cx - 20, ground - 4, cx + 22, ground + 4), fill=shadow_color)
    draw.rectangle((cx - 10, ground - 86, cx + 10, ground - 36), fill=jacket_color)
    draw.rectangle((cx - 6, ground - 78, cx + 6, ground - 40), fill=(30, 30, 36, 255))

    draw.ellipse((cx - 13, ground - 120, cx + 13, ground - 94), fill=head_color)
    draw.rectangle((cx - 15, ground - 126, cx + 9, ground - 116), fill=pants_color)
    draw.rectangle((cx + 4, ground - 112, cx + 12, ground - 108), fill=pants_color)

    left_leg_shift = -4 if phase in {3, 4, 5} else 2
    right_leg_shift = 4 if phase in {9, 10, 11} else -2
    draw.rectangle((cx - 10, ground - 38, cx - 2, ground - 4), fill=pants_color)
    draw.rectangle((cx + 2, ground - 38, cx + 10, ground - 4), fill=pants_color)
    draw.rectangle((cx - 14 + left_leg_shift, ground - 6, cx - 1 + left_leg_shift, ground), fill=pants_color)
    draw.rectangle((cx + 1 + right_leg_shift, ground - 6, cx + 14 + right_leg_shift, ground), fill=pants_color)

    left_arm_y = ground - 76 + arm_swing * 3
    right_arm_y = ground - 74 - arm_swing * 3
    draw.line((cx - 10, ground - 78, cx - 28, left_arm_y, cx - 20, left_arm_y + 20), fill=jacket_color, width=5)
    draw.line((cx + 10, ground - 76, cx + 28, right_arm_y, cx + 20, right_arm_y + 18), fill=jacket_color, width=5)

    guitar_y = ground - 62 + (phase % 3)
    draw.line((cx - 26, guitar_y + 8, cx + 34, guitar_y - 34), fill=guitar_color, width=4)
    draw.ellipse((cx - 30, guitar_y - 2, cx + 4, guitar_y + 28), fill=(122, 28, 172, 255))
    draw.rectangle((cx - 2, guitar_y + 6, cx + 22, guitar_y + 14), fill=guitar_color)

    aura_offset = phase % 6
    draw.arc(
        (cx - 34 - aura_offset, ground - 128, cx + 34 + aura_offset, ground - 42),
        start=200,
        end=330,
        fill=accent_color,
        width=2,
    )


from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .config import load_animations, load_character, load_project_style
from .paths import generated_prompt_dir, prompt_template_dir

PLACEHOLDER_PATTERN = re.compile(r"{{\s*([a-zA-Z0-9_.]+)\s*}}")


def format_value(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {format_value(item)}" for item in value)
    if isinstance(value, dict):
        return yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()
    return str(value)


def build_context(
    character: dict[str, Any],
    project: dict[str, Any],
    animations: dict[str, int],
) -> dict[str, Any]:
    frame_width, frame_height = character["frame_size"]
    sheet_columns, sheet_rows = character["sheet_layout"]
    return {
        "character": character,
        "project": project,
        "animations": animations,
        "frame_width": frame_width,
        "frame_height": frame_height,
        "sheet_columns": sheet_columns,
        "sheet_rows": sheet_rows,
    }


def resolve_placeholder(context: dict[str, Any], key: str) -> str:
    value: Any = context
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"Unknown template placeholder: {key}")
        value = value[part]
    return format_value(value)


def render_template(template_text: str, context: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        return resolve_placeholder(context, match.group(1))

    return PLACEHOLDER_PATTERN.sub(replace, template_text)


def render_templates_for_character(
    character_id: str,
    root: Path | None = None,
) -> list[Path]:
    character = load_character(character_id, root)
    project = load_project_style(root)
    animations = load_animations(root)
    context = build_context(character, project, animations)

    template_dir = prompt_template_dir(root)
    output_dir = generated_prompt_dir(character_id, root)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_paths: list[Path] = []
    for template_path in sorted(template_dir.glob("*.txt")):
        rendered = render_template(template_path.read_text(encoding="utf-8"), context)
        output_path = output_dir / template_path.name
        output_path.write_text(rendered, encoding="utf-8")
        generated_paths.append(output_path)

    return generated_paths


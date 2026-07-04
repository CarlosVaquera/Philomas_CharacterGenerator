from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find the pipeline project root from cwd or package location."""
    candidates: list[Path] = []
    if start is not None:
        candidates.append(start.resolve())
    candidates.append(Path.cwd().resolve())
    candidates.append(Path(__file__).resolve().parents[2])

    for base in candidates:
        for path in (base, *base.parents):
            if (path / "pyproject.toml").exists() and (path / "data").exists():
                return path

    return Path(__file__).resolve().parents[2]


def data_dir(root: Path | None = None) -> Path:
    return (root or find_project_root()) / "data"


def character_path(character_id: str, root: Path | None = None) -> Path:
    return data_dir(root) / "characters" / f"{character_id}.yaml"


def project_style_path(root: Path | None = None) -> Path:
    return data_dir(root) / "project_style.yaml"


def animations_path(root: Path | None = None) -> Path:
    return data_dir(root) / "animations.yaml"


def prompt_template_dir(root: Path | None = None) -> Path:
    return (root or find_project_root()) / "prompts" / "templates"


def generated_prompt_dir(character_id: str, root: Path | None = None) -> Path:
    return (root or find_project_root()) / "prompts" / "generated" / character_id


def raw_asset_dir(character_id: str, root: Path | None = None) -> Path:
    return (root or find_project_root()) / "assets" / "raw" / character_id


def clean_asset_dir(character_id: str, root: Path | None = None) -> Path:
    return (root or find_project_root()) / "assets" / "clean" / character_id


def export_asset_dir(character_id: str, root: Path | None = None) -> Path:
    return (root or find_project_root()) / "assets" / "export" / character_id


def exported_frames_dir(character_id: str, root: Path | None = None) -> Path:
    return export_asset_dir(character_id, root) / "frames"


def placeholder_spritesheet_path(character_id: str, root: Path | None = None) -> Path:
    return raw_asset_dir(character_id, root) / f"{character_id}_placeholder_spritesheet.png"

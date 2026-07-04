from __future__ import annotations

import argparse
from pathlib import Path

from .character_scaffold import create_character
from .frame_exporter import export_animation_frames
from .metadata import export_metadata
from .placeholder_generator import generate_placeholder_spritesheet
from .prompt_builder import render_templates_for_character
from .validator import validate_character


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="philomas-pipeline",
        description="Local placeholder pipeline for Philomas character assets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    character_commands = (
        "build-prompts",
        "generate-placeholder",
        "validate",
        "export-frames",
        "export-metadata",
        "run",
    )
    for command in character_commands:
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("character_id")
        command_parser.add_argument(
            "--root",
            type=Path,
            default=None,
            help="Optional project root override.",
        )

    create_parser = subparsers.add_parser(
        "create-character",
        help="Create a new character data file and asset folders.",
    )
    create_parser.add_argument("character_id")
    create_parser.add_argument(
        "--name",
        default=None,
        help="Display name to write into the character YAML file.",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing character YAML file.",
    )
    create_parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Optional project root override.",
    )

    return parser


def command_create_character(
    character_id: str,
    name: str | None = None,
    root: Path | None = None,
    force: bool = False,
) -> int:
    paths = create_character(character_id, name=name, root=root, force=force)
    print(f"created character: {paths['character']}")
    print(f"created prompt folder: {paths['prompts']}")
    print(f"created raw assets folder: {paths['raw_assets']}")
    print(f"created clean assets folder: {paths['clean_assets']}")
    print(f"created export assets folder: {paths['export_assets']}")
    return 0


def command_build_prompts(character_id: str, root: Path | None = None) -> int:
    paths = render_templates_for_character(character_id, root)
    for path in paths:
        print(f"generated prompt: {path}")
    return 0


def command_generate_placeholder(character_id: str, root: Path | None = None) -> int:
    path = generate_placeholder_spritesheet(character_id, root)
    print(f"generated placeholder spritesheet: {path}")
    return 0


def command_validate(character_id: str, root: Path | None = None) -> int:
    report = validate_character(character_id, root)
    for warning in report.warnings:
        print(f"warning: {warning}")
    if report.errors:
        for error in report.errors:
            print(f"error: {error}")
        return 1
    print(f"validation passed: {character_id}")
    return 0


def command_export_metadata(character_id: str, root: Path | None = None) -> int:
    path = export_metadata(character_id, root)
    print(f"exported metadata: {path}")
    return 0


def command_export_frames(character_id: str, root: Path | None = None) -> int:
    report = validate_character(character_id, root)
    if report.errors:
        for error in report.errors:
            print(f"error: {error}")
        return 1

    manifest = export_animation_frames(character_id, root)
    exported_count = sum(int(data["frame_count"]) for data in manifest.values())
    print(f"exported animation frames: {exported_count}")
    return 0


def command_run(character_id: str, root: Path | None = None) -> int:
    command_build_prompts(character_id, root)
    command_generate_placeholder(character_id, root)
    status = command_validate(character_id, root)
    if status != 0:
        return status
    status = command_export_frames(character_id, root)
    if status != 0:
        return status
    command_export_metadata(character_id, root)
    print(f"pipeline complete: {character_id}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "create-character":
        return command_create_character(args.character_id, args.name, args.root, args.force)

    handlers = {
        "build-prompts": command_build_prompts,
        "generate-placeholder": command_generate_placeholder,
        "validate": command_validate,
        "export-frames": command_export_frames,
        "export-metadata": command_export_metadata,
        "run": command_run,
    }
    return handlers[args.command](args.character_id, args.root)


if __name__ == "__main__":
    raise SystemExit(main())

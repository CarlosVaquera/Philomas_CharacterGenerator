import shutil
from uuid import uuid4
from pathlib import Path

import pytest
import yaml

from philomas_pipeline.character_scaffold import create_character


def make_workspace_scratch() -> Path:
    root = Path(".pytest_workspace") / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_create_character_writes_data_and_folders():
    root = make_workspace_scratch()
    try:
        paths = create_character("lola", name="Lola", root=root)

        character_data = yaml.safe_load(paths["character"].read_text(encoding="utf-8"))

        assert character_data["name"] == "Lola"
        assert character_data["frame_size"] == [112, 192]
        assert character_data["sheet_layout"] == [12, 12]
        assert paths["prompts"].joinpath(".gitkeep").exists()
        assert paths["raw_assets"].joinpath(".gitkeep").exists()
        assert paths["clean_assets"].joinpath(".gitkeep").exists()
        assert paths["export_assets"].joinpath(".gitkeep").exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_create_character_refuses_duplicate_without_force():
    root = make_workspace_scratch()
    try:
        create_character("lola", name="Lola", root=root)

        with pytest.raises(FileExistsError):
            create_character("lola", name="Lola Again", root=root)
    finally:
        shutil.rmtree(root, ignore_errors=True)

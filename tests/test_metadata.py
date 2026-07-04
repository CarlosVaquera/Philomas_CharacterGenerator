import json

from philomas_pipeline.metadata import export_metadata
from philomas_pipeline.prompt_builder import render_templates_for_character


def test_export_metadata_includes_core_character_fields():
    render_templates_for_character("pepe")
    path = export_metadata("pepe")

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "0.1.0"
    assert data["character"]["name"] == "Pepe"
    assert data["frame_size"] == [112, 192]
    assert data["sheet_layout"] == [12, 12]
    assert data["hitbox"] == [30, 24, 52, 168]
    assert "idle" in data["animations"]
    assert len(data["generated_prompt_paths"]) == 3
    assert data["source_paths"]["character"].replace("\\", "/") == "data/characters/pepe.yaml"
    assert all(not path.startswith("C:") for path in data["generated_prompt_paths"])

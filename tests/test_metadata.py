import json

from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.frame_exporter import export_animation_frames
from philomas_pipeline.metadata import export_metadata
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet
from philomas_pipeline.prompt_builder import render_templates_for_character


def test_export_metadata_includes_core_character_fields():
    render_templates_for_character("pepe")
    generate_placeholder_spritesheet("pepe")
    clean_spritesheet("pepe")
    export_animation_frames("pepe")
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
    assert data["source_paths"]["clean_spritesheet"].replace("\\", "/") == "assets/clean/pepe/pepe_clean_spritesheet.png"
    assert data["source_paths"]["animation_manifest"].replace("\\", "/") == "assets/export/pepe/animation_manifest.json"
    assert data["source_paths"]["qa_report"].replace("\\", "/") == "assets/export/pepe/qa_report.json"
    assert all(not path.startswith("C:") for path in data["generated_prompt_paths"])
    assert data["frame_exports"]["idle"]["frame_count"] == 6
    assert data["frame_exports"]["idle"]["frame_duration_ms"] == 120
    assert data["frame_exports"]["death"]["loop"] is False
    assert data["frame_exports"]["run"]["start_frame"] == 6

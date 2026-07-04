import json

from philomas_pipeline.animation_manifest import export_animation_manifest
from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.frame_exporter import export_animation_frames
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet


def test_export_animation_manifest_writes_engine_contract():
    generate_placeholder_spritesheet("pepe")
    clean_spritesheet("pepe")
    export_animation_frames("pepe")

    path = export_animation_manifest("pepe")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["schema"] == "philomas.animation_manifest.v1"
    assert data["character"]["id"] == "pepe"
    assert data["character"]["name"] == "Pepe"
    assert data["frame_size"] == [112, 192]
    assert data["sheet_layout"] == [12, 12]
    assert data["hitbox"] == [30, 24, 52, 168]
    assert data["source"]["clean_spritesheet"].replace("\\", "/") == "assets/clean/pepe/pepe_clean_spritesheet.png"
    assert data["animations"]["idle"]["loop"] is True
    assert data["animations"]["idle"]["frame_duration_ms"] == 120
    assert data["animations"]["idle"]["frame_count"] == 6
    assert len(data["animations"]["idle"]["frames"]) == 6
    assert data["animations"]["death"]["loop"] is False

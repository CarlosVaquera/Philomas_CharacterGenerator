import json

from philomas_pipeline.animation_manifest import export_animation_manifest
from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.frame_exporter import export_animation_frames
from philomas_pipeline.metadata import export_metadata
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet
from philomas_pipeline.qa_report import export_qa_report


def test_export_qa_report_summarizes_exported_assets():
    generate_placeholder_spritesheet("pepe")
    clean_spritesheet("pepe")
    export_animation_frames("pepe")
    export_animation_manifest("pepe")
    export_metadata("pepe")

    path = export_qa_report("pepe")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["character_id"] == "pepe"
    assert data["is_valid"] is True
    assert data["sheet"]["requested_animation_frames"] == 75
    assert data["sheet"]["unused_sheet_frames"] == 69
    assert data["exports"]["expected_frame_count"] == 75
    assert data["exports"]["exported_frame_count"] == 75
    assert data["exports"]["missing_exported_frames"] == []
    assert data["exports"]["empty_frames"] == []
    assert data["paths"]["animation_manifest"].replace("\\", "/") == "assets/export/pepe/animation_manifest.json"

from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.frame_exporter import export_animation_frames
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet


def test_export_animation_frames_writes_expected_animation_frames():
    generate_placeholder_spritesheet("pepe")
    clean_spritesheet("pepe")
    manifest = export_animation_frames("pepe")

    idle = manifest["idle"]
    run = manifest["run"]

    assert idle["start_frame"] == 0
    assert idle["frame_count"] == 6
    assert len(idle["paths"]) == 6
    assert idle["paths"][0].exists()
    assert run["start_frame"] == 6
    assert run["frame_count"] == 12
    assert run["paths"][-1].exists()

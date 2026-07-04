from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet
from philomas_pipeline.validator import validate_character


def test_validate_generated_placeholder_passes():
    generate_placeholder_spritesheet("pepe")
    clean_spritesheet("pepe")
    report = validate_character("pepe")

    assert report.is_valid
    assert report.errors == []

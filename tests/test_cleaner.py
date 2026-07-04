from PIL import Image

from philomas_pipeline.cleaner import clean_spritesheet
from philomas_pipeline.placeholder_generator import generate_placeholder_spritesheet


def test_clean_spritesheet_writes_rgba_clean_asset():
    generate_placeholder_spritesheet("pepe")
    path = clean_spritesheet("pepe")

    assert path.exists()
    assert path.name == "pepe_clean_spritesheet.png"

    with Image.open(path) as image:
        assert image.mode == "RGBA"
        assert image.size == (1344, 2304)

from philomas_pipeline.config import load_animations, load_character, load_project_style
from philomas_pipeline.prompt_builder import build_context, render_template, render_templates_for_character


def test_render_template_replaces_nested_placeholders():
    character = load_character("pepe")
    project = load_project_style()
    animations = load_animations()
    context = build_context(character, project, animations)

    rendered = render_template(
        "{{character.name}} {{project.pixel_style}} {{frame_width}} {{sheet_rows}}",
        context,
    )

    assert "Pepe" in rendered
    assert "crisp chunky pixel art" in rendered
    assert "112" in rendered
    assert "12" in rendered


def test_render_templates_for_character_writes_outputs():
    output_paths = render_templates_for_character("pepe")

    assert len(output_paths) == 3
    assert all(path.exists() for path in output_paths)
    assert any("spritesheet_generation_prompt" in path.name for path in output_paths)

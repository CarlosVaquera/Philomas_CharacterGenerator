# philomas-character-pipeline

Local, modular framework for generating, organizing, validating, and exporting
character assets for Philomas Engine.

This first version does not connect to real AI services. Prompt rendering,
image generation, and exports are functional placeholders designed so the
pipeline can later connect to GPT Image, FLUX, ComfyUI, or any other provider
behind small interfaces.

## Requirements

- Python 3.11+
- Pillow
- PyYAML
- pytest

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## CLI

```bash
philomas-pipeline create-character <character_id> --name "Character Name"
philomas-pipeline build-prompts pepe
philomas-pipeline generate-placeholder pepe
philomas-pipeline clean-spritesheet pepe
philomas-pipeline validate pepe
philomas-pipeline export-frames pepe
philomas-pipeline export-animation-manifest pepe
philomas-pipeline export-metadata pepe
philomas-pipeline qa-report pepe
philomas-pipeline run pepe
```

## VS Code Tasks

Open the folder `philomas-character-pipeline` in VS Code, select a Python
interpreter, then open `Terminal > Run Task...`.

For the user-facing workflow and exact manual inputs, read
[`docs/USER_GUIDE.md`](docs/USER_GUIDE.md).

### First Time Manual Steps

1. Select a Python 3.11+ interpreter in VS Code.
2. Run `Philomas: 00 First Time Setup + Run`.
3. Run `Philomas: 03 Run Tests`.

Task `00` runs tasks `01` and `02` in sequence. After dependencies are installed
once, daily work usually starts at task `02`.

### Regular Workflow

1. Run `Philomas: 02 Run Pipeline`.
2. Run `Philomas: 03 Run Tests`.
3. Inspect generated outputs if needed:
   - `prompts/generated/<character_id>/`
   - `assets/raw/<character_id>/<character_id>_placeholder_spritesheet.png`
   - `assets/clean/<character_id>/<character_id>_clean_spritesheet.png`
   - `assets/export/<character_id>/frames/`
   - `assets/export/<character_id>/animation_manifest.json`
   - `assets/export/<character_id>/metadata.json`
   - `assets/export/<character_id>/qa_report.json`

### Manual Step-by-step Pipeline

Use these only when you want to inspect or debug each stage:

1. `Philomas: Step A - Build Prompts`
2. `Philomas: Step B - Generate Placeholder`
3. `Philomas: Step C - Clean Spritesheet`
4. `Philomas: Step D - Validate`
5. `Philomas: Step E - Export Frames`
6. `Philomas: Step F - Export Animation Manifest`
7. `Philomas: Step G - Export Metadata`
8. `Philomas: Step H - QA Report`

The tasks use the Python interpreter selected in VS Code and set
`PYTHONPATH` to `src` for local module execution.

The `run` command executes the full placeholder pipeline:

1. Render prompt files into `prompts/generated/<character>/`.
2. Generate a placeholder RGBA spritesheet in `assets/raw/<character>/`.
3. Normalize the raw spritesheet into `assets/clean/<character>/`.
4. Validate the clean spritesheet and character metadata.
5. Export individual animation frames into `assets/export/<character>/frames/`.
6. Export `animation_manifest.json` into `assets/export/<character>/`.
7. Export `metadata.json` into `assets/export/<character>/`.
8. Export `qa_report.json` into `assets/export/<character>/`.

## Project Layout

```text
data/                 Character, project style, and animation data.
prompts/templates/    Plain text prompt templates with {{placeholders}}.
prompts/generated/    Rendered prompts per character.
assets/raw/           Unprocessed generated spritesheets.
assets/clean/         Future cleaned/intermediate assets.
assets/export/        Engine-ready metadata and future exports.
src/                  Python package source.
scripts/              Small convenience scripts.
tests/                Unit tests.
```

## Current Example Character

The repository starts with `pepe`, a lead vocalist/guitarist, and `lola`, a
bassist/occult mechanic, for an arcade rock horror direction. Each placeholder
spritesheet uses:

- Frame size: `112 x 192`
- Sheet layout: `12 x 12`
- Total image size: `1344 x 2304`
- Total frames: `144`

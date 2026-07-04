from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from philomas_pipeline.cli import main


if __name__ == "__main__":
    character_id = sys.argv[1] if len(sys.argv) > 1 else "pepe"
    raise SystemExit(main(["run", character_id]))

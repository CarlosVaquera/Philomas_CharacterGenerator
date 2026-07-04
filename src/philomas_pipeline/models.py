from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CharacterSpec:
    character_id: str
    data: dict[str, Any]

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def frame_size(self) -> tuple[int, int]:
        width, height = self.data["frame_size"]
        return int(width), int(height)

    @property
    def sheet_layout(self) -> tuple[int, int]:
        columns, rows = self.data["sheet_layout"]
        return int(columns), int(rows)

    @property
    def hitbox(self) -> tuple[int, int, int, int]:
        x, y, width, height = self.data["hitbox"]
        return int(x), int(y), int(width), int(height)


@dataclass(frozen=True)
class ValidationReport:
    character_id: str
    errors: list[str]
    warnings: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def raise_for_errors(self) -> None:
        if self.errors:
            formatted = "\n".join(f"- {error}" for error in self.errors)
            raise ValueError(f"Validation failed for {self.character_id}:\n{formatted}")


"""UA-DETRAC dataset adapter."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class UADETRACDataset:
    root: str
    split: str = "train"

    def sequences(self) -> Iterator[str]:
        yield f"detrac-{self.split}-seq"

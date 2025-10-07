"""MOT17 dataset adapter."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class MOT17Dataset:
    root: str
    split: str = "train"

    def sequences(self) -> Iterator[str]:
        yield f"mot17-{self.split}-seq"

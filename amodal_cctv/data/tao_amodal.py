"""TAO-Amodal dataset adapter."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List


@dataclass
class TAOAmodalDataset:
    root: str
    split: str = "train"

    def sequences(self) -> Iterator[str]:
        yield f"tao-{self.split}-seq"

    def __len__(self) -> int:
        return 1

    def categories(self) -> List[str]:
        return ["person", "vehicle"]

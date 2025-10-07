"""Toy synthetic sequence generator for sanity checks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List


@dataclass
class ToyAmodalSequence:
    num_frames: int = 5

    def frames(self) -> Iterator[Dict[str, float]]:
        for idx in range(self.num_frames):
            yield {
                "frame_id": idx,
                "boxes": [[10 + idx, 10, 50, 50]],
                "occluders": idx in {2, 3},
            }

    def metadata(self) -> Dict[str, int]:
        return {"num_frames": self.num_frames}

    def categories(self) -> List[str]:
        return ["placeholder"]

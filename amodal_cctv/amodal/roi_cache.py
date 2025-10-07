"""Region-of-interest caching utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import torch


@dataclass
class ROICache:
    max_items: int = 128
    storage: Dict[int, torch.Tensor] = field(default_factory=dict)

    def put(self, track_id: int, tensor: torch.Tensor) -> None:
        if len(self.storage) >= self.max_items:
            self.storage.pop(next(iter(self.storage)))
        self.storage[track_id] = tensor.detach().cpu()

    def get(self, track_id: int) -> torch.Tensor | None:
        return self.storage.get(track_id)

    def keys(self) -> List[int]:
        return list(self.storage.keys())

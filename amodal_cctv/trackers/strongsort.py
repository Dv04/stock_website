"""StrongSORT placeholder with optional Re-ID support."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StrongSortConfig:
    appearance_weight: float = 0.5
    motion_weight: float = 0.5
    reid_enabled: bool = False


class StrongSortTracker:
    """Mock StrongSORT tracker that merges detection metadata."""

    def __init__(self, config: StrongSortConfig, reid_model: Optional[Any] = None) -> None:
        self.config = config
        self.reid_model = reid_model

    def track(self, detections: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "track_id": idx,
                "box": box,
                "score": score,
                "appearance": self.reid_model.describe(box) if self.reid_model else None,
            }
            for idx, (box, score) in enumerate(
                zip(detections.get("boxes", []), detections.get("scores", [])),
                start=1,
            )
        ]


def build_strongsort_tracker(
    config_dict: Dict[str, Any] | None = None,
    reid_model: Optional[Any] = None,
) -> StrongSortTracker:
    config = StrongSortConfig(**(config_dict or {}))
    return StrongSortTracker(config, reid_model=reid_model)

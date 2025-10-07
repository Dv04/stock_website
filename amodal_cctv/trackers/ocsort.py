"""OC-SORT placeholder implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class OCSortConfig:
    track_thresh: float = 0.5
    match_thresh: float = 0.7
    delta_t: int = 3


class OCSortTracker:
    """Simplified OC-SORT tracker returning empty track list."""

    def __init__(self, config: OCSortConfig) -> None:
        self.config = config

    def track(self, detections: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []


def build_ocsort_tracker(config_dict: Dict[str, Any] | None = None) -> OCSortTracker:
    config = OCSortConfig(**(config_dict or {}))
    return OCSortTracker(config)

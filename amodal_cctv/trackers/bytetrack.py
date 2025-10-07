"""ByteTrack wrapper for association with amodal support hooks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ByteTrackConfig:
    track_thresh: float = 0.5
    match_thresh: float = 0.8
    buffer_size: int = 30


class ByteTrackTracker:
    """Simplified ByteTrack interface emitting placeholder tracks."""

    def __init__(self, config: ByteTrackConfig) -> None:
        self.config = config

    def track(self, detections: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "track_id": 1,
                "box": det_box,
                "score": 1.0,
                "status": "tracked",
            }
            for det_box in detections.get("boxes", [])
        ]


def build_bytetrack_tracker(config_dict: Dict[str, Any] | None = None) -> ByteTrackTracker:
    config = ByteTrackConfig(**(config_dict or {}))
    return ByteTrackTracker(config)

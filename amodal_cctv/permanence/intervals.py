"""Occlusion interval logging utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class OcclusionInterval:
    track_id: int
    start_frame: int
    end_frame: int | None = None
    cause: str | None = None


@dataclass
class IntervalLogger:
    intervals: List[OcclusionInterval] = field(default_factory=list)

    def start(self, track_id: int, frame: int, cause: str | None = None) -> None:
        self.intervals.append(OcclusionInterval(track_id=track_id, start_frame=frame, cause=cause))

    def end(self, track_id: int, frame: int) -> None:
        for interval in reversed(self.intervals):
            if interval.track_id == track_id and interval.end_frame is None:
                interval.end_frame = frame
                break

    def to_serializable(self) -> List[dict]:
        return [interval.__dict__ for interval in self.intervals]

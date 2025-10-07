"""Narrative generation utilities for reappearance events."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class NarrativeEvidence:
    gate_sigma: float
    appearance_cosine: float
    occlusion_frames: int
    reentry_camera: str


TEMPLATE = (
    "Track {track_id} reappeared after {occlusion_frames} frames via {reentry_camera}; "
    "gate σ={gate_sigma:.2f}, cosine={appearance_cosine:.2f}."
)


def build_narrative(track_id: int, evidence: NarrativeEvidence) -> str:
    return TEMPLATE.format(track_id=track_id, **evidence.__dict__)


def narrative_record(track_id: int, evidence: NarrativeEvidence) -> Dict[str, object]:
    return {
        "track_id": track_id,
        "message": build_narrative(track_id, evidence),
        "evidence": evidence.__dict__,
    }

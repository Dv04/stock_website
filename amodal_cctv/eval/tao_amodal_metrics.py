"""TAO-Amodal specific evaluation helpers."""
from __future__ import annotations

from typing import Dict


def compute_visibility_binned_ap(predictions: Dict[str, object], ground_truth: Dict[str, object]) -> Dict[str, float]:
    """Return placeholder AP metrics bucketed by visibility."""
    return {
        "visible": 0.0,
        "partially_occluded": 0.0,
        "heavily_occluded": 0.0,
    }

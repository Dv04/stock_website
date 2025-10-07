"""Grad-CAM helper stubs."""
from __future__ import annotations

from typing import Any, Dict


def compute_gradcam(roi_tensor: Any, target_layer: str | None = None) -> Dict[str, Any]:
    """Return placeholder Grad-CAM heatmap."""
    return {
        "heatmap": None,
        "target_layer": target_layer or "default",
    }

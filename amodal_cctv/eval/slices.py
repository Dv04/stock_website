"""Occlusion-aware evaluation slice helpers."""
from __future__ import annotations

from typing import Dict, List


def available_slices() -> List[str]:
    return ["full", "occlusion_only", "out_of_fov"]


def filter_by_slice(data: Dict[str, object], slice_name: str) -> Dict[str, object]:
    if slice_name not in available_slices():
        raise ValueError(f"Unknown slice: {slice_name}")
    return data

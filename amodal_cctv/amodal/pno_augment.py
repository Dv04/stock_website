"""Paste-N-Occlude augmentation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class PnOConfig:
    min_occluders: int = 2
    max_occluders: int = 5
    copy_paste_prob: float = 0.5


def apply_pno(image: Any, boxes: List[Tuple[float, float, float, float]], config: PnOConfig) -> Dict[str, Any]:
    """Return placeholder augmentation metadata."""
    return {
        "image": image,
        "boxes": boxes,
        "metadata": {
            "occluder_count": config.min_occluders,
            "copy_paste_prob": config.copy_paste_prob,
        },
    }


def build_pno_config(config_dict: Dict[str, Any] | None = None) -> PnOConfig:
    return PnOConfig(**(config_dict or {}))

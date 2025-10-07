"""Transformer relevance visualization placeholders."""
from __future__ import annotations

from typing import Any, Dict


def compute_relevance(attention_maps: Any) -> Dict[str, Any]:
    """Return mock relevance information for transformer-based detectors."""
    return {
        "relevance": None,
        "num_heads": getattr(attention_maps, "shape", (0, 0)),
    }

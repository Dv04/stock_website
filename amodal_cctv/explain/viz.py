"""Visualization helpers for narrative cards."""
from __future__ import annotations

from typing import Dict


def render_narrative_card(entry: Dict[str, object]) -> Dict[str, object]:
    """Return metadata for visualization; actual rendering implemented later."""
    return {
        "message": entry.get("message"),
        "evidence": entry.get("evidence"),
        "rendered": False,
    }

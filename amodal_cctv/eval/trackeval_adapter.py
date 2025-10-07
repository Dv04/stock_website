"""Adapter into TrackEval metrics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TrackEvalConfig:
    eval_dir: str = "outputs/trackeval"


def format_for_trackeval(seqs: Dict[str, object], config: TrackEvalConfig | None = None) -> Dict[str, object]:
    cfg = config or TrackEvalConfig()
    return {
        "eval_dir": cfg.eval_dir,
        "sequences": list(seqs.keys()),
    }

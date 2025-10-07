"""Training loop placeholder for the amodal expander head."""
from __future__ import annotations

from typing import Any, Dict


def configure_optimizer(model: Any, lr: float = 1e-3, weight_decay: float = 1e-4) -> Dict[str, Any]:
    """Return optimizer hyperparameters without instantiating training state."""
    return {
        "optimizer": "AdamW",
        "lr": lr,
        "weight_decay": weight_decay,
    }


def schedule_config(total_steps: int = 20000) -> Dict[str, Any]:
    return {
        "type": "cosine",
        "total_steps": total_steps,
        "warmup_steps": int(0.1 * total_steps),
    }

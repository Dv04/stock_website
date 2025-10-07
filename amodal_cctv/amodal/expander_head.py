"""Amodal expander head definitions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

try:
    import torch
    import torch.nn as nn
except ImportError:  # pragma: no cover - optional dependency in scaffolding stage
    torch = None
    nn = None


@dataclass
class ExpanderHeadConfig:
    input_dim: int = 256
    hidden_dim: int = 256
    dropout: float = 0.2


class AmodalExpanderHead(nn.Module if nn is not None else object):
    """Lightweight MLP that regresses amodal deltas."""

    def __init__(self, config: ExpanderHeadConfig) -> None:
        if nn is None:
            raise ImportError("PyTorch is required to instantiate AmodalExpanderHead.")
        super().__init__()  # type: ignore[misc]
        self.config = config
        self.mlp = nn.Sequential(
            nn.Linear(config.input_dim, config.hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(config.hidden_dim, 4),
        )

    def forward(self, roi_features: torch.Tensor) -> torch.Tensor:  # type: ignore[name-defined]
        return self.mlp(roi_features)

    def loss(
        self,
        predictions: torch.Tensor,  # type: ignore[name-defined]
        targets: torch.Tensor,  # type: ignore[name-defined]
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:  # type: ignore[name-defined]
        criterion = nn.SmoothL1Loss()
        value = criterion(predictions, targets)
        return value, {"smooth_l1": value.detach()}


def build_amodal_head(config_dict: Dict[str, Any] | None = None) -> AmodalExpanderHead:
    config = ExpanderHeadConfig(**(config_dict or {}))
    return AmodalExpanderHead(config)

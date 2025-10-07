"""Mahalanobis gating helpers with time-widened gates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass
class GatingConfig:
    base_sigma: float = 3.0
    time_widen_coeff: float = 0.2


def mahalanobis_gate(residual: np.ndarray, covariance: np.ndarray, dt: int, config: GatingConfig) -> Dict[str, float]:
    inv_cov = np.linalg.pinv(covariance)
    distance = float(residual.T @ inv_cov @ residual)
    threshold = (config.base_sigma + config.time_widen_coeff * dt) ** 2
    return {
        "distance": distance,
        "threshold": threshold,
        "accepted": distance <= threshold,
    }

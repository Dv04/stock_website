"""Constant-velocity Kalman filter with covariance inflation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass
class KalmanConfig:
    position_dim: int = 4
    velocity_dim: int = 4
    process_noise: float = 1.0
    measurement_noise: float = 1.0
    covariance_inflation: float = 1.05


class KalmanPermanenceFilter:
    """Simple constant-velocity Kalman filter stub."""

    def __init__(self, config: KalmanConfig) -> None:
        self.config = config
        dim = config.position_dim + config.velocity_dim
        self.state = np.zeros((dim, 1))
        self.covariance = np.eye(dim)

    def predict(self) -> Tuple[np.ndarray, np.ndarray]:
        self.covariance *= self.config.covariance_inflation
        return self.state, self.covariance

    def update(self, measurement: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        self.state[: self.config.position_dim] = measurement.reshape(-1, 1)
        self.covariance[: self.config.position_dim, : self.config.position_dim] = (
            np.eye(self.config.position_dim) * self.config.measurement_noise
        )
        return self.state, self.covariance

    def to_dict(self) -> Dict[str, float]:
        return {
            "process_noise": self.config.process_noise,
            "measurement_noise": self.config.measurement_noise,
            "covariance_inflation": self.config.covariance_inflation,
        }


def build_kalman_filter(config_dict: Dict[str, float] | None = None) -> KalmanPermanenceFilter:
    config = KalmanConfig(**(config_dict or {}))
    return KalmanPermanenceFilter(config)

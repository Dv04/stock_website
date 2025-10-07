"""Existence probability filter with exponential decay."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExistenceConfig:
    alpha_decay: float = 0.94
    boost_on_detection: float = 0.2
    min_probability: float = 0.01


class ExistenceFilter:
    """Maintain per-track existence probability."""

    def __init__(self, config: ExistenceConfig | None = None) -> None:
        self.config = config or ExistenceConfig()
        self.probability = 1.0

    def decay(self) -> float:
        self.probability = max(self.config.min_probability, self.probability * self.config.alpha_decay)
        return self.probability

    def boost(self) -> float:
        self.probability = min(1.0, self.probability + self.config.boost_on_detection)
        return self.probability

"""Lightweight Re-ID backbone placeholders."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ReIDConfig:
    model_name: str = "osnet_x0_25"
    device: str = "cuda"


class BaseReIDModel:
    """Base interface for Re-ID models."""

    def __init__(self, config: ReIDConfig) -> None:
        self.config = config

    def describe(self, box: Any) -> str:
        return f"embedding@{self.config.model_name}"


def build_reid_model(config_dict: dict | None = None) -> BaseReIDModel:
    config = ReIDConfig(**(config_dict or {}))
    return BaseReIDModel(config)

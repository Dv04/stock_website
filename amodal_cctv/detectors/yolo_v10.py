"""YOLOv10 detector wrapper for fast amodal CCTV tracking experiments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class YOLOv10Config:
    weights_path: str | None = None
    device: str = "cuda"
    input_size: int = 640
    confidence: float = 0.3


class YOLOv10Detector:
    """Minimal placeholder for the frozen YOLOv10 detector."""

    def __init__(self, config: YOLOv10Config) -> None:
        self.config = config
        self._model = None  # Lazy-loaded model placeholder

    def load(self) -> None:
        """Mock load routine; replace with actual model init when weights are available."""
        if self._model is None:
            self._model = f"yolov10::{self.config.weights_path or 'pretrained'}"

    def infer(self, inputs: Any) -> Dict[str, Any]:
        """Return dummy detections; to be replaced with real inference logic."""
        self.load()
        return {
            "boxes": [],
            "scores": [],
            "classes": [],
            "metadata": {
                "model": self._model,
                "input_size": self.config.input_size,
            },
        }


def build_yolov10_detector(config_dict: Dict[str, Any] | None = None) -> YOLOv10Detector:
    """Factory that builds the default YOLOv10 detector."""
    config = YOLOv10Config(**(config_dict or {}))
    return YOLOv10Detector(config)

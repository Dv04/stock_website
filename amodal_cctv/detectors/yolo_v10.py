"""YOLOv10 detector wrapper for amodal CCTV tracking."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np


def _is_placeholder(value: Optional[str]) -> bool:
    return value is not None and "{{PLACEHOLDER" in value


@dataclass
class YOLOv10Config:
    """Runtime configuration for the YOLOv10 detector."""

    weights_path: Optional[str] = None
    device: str = "cuda"
    confidence: float = 0.25
    iou_threshold: float = 0.45
    image_size: int = 640
    max_detections: int = 300
    half_precision: bool = False
    fuse: bool = True


class YOLOv10Detector:
    """Ultralytics YOLOv10 detector with numpy-friendly outputs."""

    def __init__(self, config: YOLOv10Config) -> None:
        self.config = config
        self._model = None

    def _resolve_weights(self) -> str:
        if _is_placeholder(self.config.weights_path):
            raise ValueError(
                "YOLOv10 weights path unresolved ({{PLACEHOLDER:YOLOV10_WEIGHTS_PATH}}). "
                "Update placeholders.md with a valid checkpoint path."
            )
        if self.config.weights_path:
            resolved = Path(self.config.weights_path).expanduser()
            if not resolved.exists():
                raise FileNotFoundError(
                    f"YOLOv10 weights not found at {resolved}. See placeholders.md to set the correct path."
                )
            return str(resolved)
        # Fall back to Ultralytics default lightweight model.
        return "yolov10n.pt"

    def _ensure_model(self):
        if self._model is not None:
            return self._model
        try:
            from ultralytics import YOLO  # type: ignore
        except ImportError as exc:  # pragma: no cover - dependency enforcement
            raise ImportError(
                "Ultralytics package is required for YOLOv10 inference. "
                "Install via `pip install ultralytics==8.3.0`."
            ) from exc

        weights = self._resolve_weights()
        model = YOLO(weights)
        if self.config.fuse and hasattr(model, "fuse"):
            model.fuse()
        self._model = model
        return self._model

    def infer(self, inputs: Any, frame_id: Optional[int] = None) -> Dict[str, Any]:
        """Run inference on an image tensor, numpy array, or file path."""
        model = self._ensure_model()
        results = model.predict(  # type: ignore[attr-defined]
            source=inputs,
            device=self.config.device,
            conf=self.config.confidence,
            iou=self.config.iou_threshold,
            imgsz=self.config.image_size,
            half=self.config.half_precision,
            max_det=self.config.max_detections,
            verbose=False,
            stream=False,
        )

        result = results[0]
        if result.boxes is None:
            boxes_xyxy = np.empty((0, 4), dtype=float)
            scores = np.empty((0,), dtype=float)
            classes = np.empty((0,), dtype=int)
        else:
            boxes_xyxy = result.boxes.xyxy.detach().cpu().numpy()
            scores = result.boxes.conf.detach().cpu().numpy()
            classes = result.boxes.cls.detach().cpu().numpy().astype(int)

        # Ultralytics YOLO does not expose ROI embeddings by default; keep placeholder for downstream hooks.
        roi_features: Optional[np.ndarray] = None

        return {
            "frame_id": frame_id,
            "boxes": boxes_xyxy,
            "scores": scores,
            "classes": classes,
            "features": roi_features,
            "metadata": {
                "model": "yolov10",
                "weights": self._resolve_weights(),
                "device": self.config.device,
                "image_size": self.config.image_size,
            },
        }


def build_yolov10_detector(config_dict: Dict[str, Any] | None = None) -> YOLOv10Detector:
    """Factory that builds the default YOLOv10 detector."""
    config = YOLOv10Config(**(config_dict or {}))
    return YOLOv10Detector(config)

"""CLI entry point for running inference with amodal CCTV pipeline."""
from __future__ import annotations

import argparse
from typing import Dict

from ..detectors.yolo_v10 import build_yolov10_detector
from ..trackers.bytetrack import build_bytetrack_tracker
from ..data.toy_examples import ToyAmodalSequence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run amodal CCTV inference")
    parser.add_argument("--config", type=str, required=False, default="configs/speed_yolov10.yaml")
    return parser.parse_args()


def run(config_path: str) -> Dict[str, object]:
    detector = build_yolov10_detector()
    tracker = build_bytetrack_tracker()
    dataset = ToyAmodalSequence()

    predictions = []
    for frame in dataset.frames():
        dets = detector.infer(frame)
        tracks = tracker.track(dets)
        predictions.append({"frame": frame["frame_id"], "tracks": tracks})
    return {
        "config": config_path,
        "predictions": predictions,
    }


def main() -> None:
    args = parse_args()
    _ = run(args.config)


if __name__ == "__main__":
    main()

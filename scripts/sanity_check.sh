#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"
OUT_DIR="$ROOT_DIR/outputs/sanity_demo"
mkdir -p "$OUT_DIR"

python <<'PY'
import json
from pathlib import Path

from amodal_cctv.detectors.yolo_v10 import build_yolov10_detector
from amodal_cctv.trackers.bytetrack import build_bytetrack_tracker
from amodal_cctv.explain.narratives import NarrativeEvidence, narrative_record
from amodal_cctv.data.toy_examples import ToyAmodalSequence

out_dir = Path("$OUT_DIR")
out_dir.mkdir(parents=True, exist_ok=True)

detector = build_yolov10_detector()
tracker = build_bytetrack_tracker()
dataset = ToyAmodalSequence(num_frames=5)

records = []
for frame in dataset.frames():
    detections = detector.infer(frame)
    tracks = tracker.track(detections)
    evidence = NarrativeEvidence(
        gate_sigma=2.5,
        appearance_cosine=0.92,
        occlusion_frames=frame["frame_id"],
        reentry_camera="cam0",
    )
    records.append(narrative_record(track_id=1, evidence=evidence))

json_path = out_dir / "narratives.json"
json_path.write_text(json.dumps(records, indent=2))

try:
    from amodal_cctv.amodal.expander_head import AmodalExpanderHead, ExpanderHeadConfig
except ImportError:
    head_status = "Amodal head skipped (PyTorch unavailable)"
else:
    _ = AmodalExpanderHead(ExpanderHeadConfig(input_dim=4, hidden_dim=8))
    head_status = "Amodal head instantiated"

print("Sanity check complete; narratives saved to", json_path)
print(head_status)
PY

"""Ensure core modules are importable."""
from amodal_cctv import (
    AmodalExpanderHead,
    KalmanPermanenceFilter,
    build_bytetrack_tracker,
    build_yolov10_detector,
)
from amodal_cctv.data.datasets import build_dataset
from amodal_cctv.explain.narratives import NarrativeEvidence, build_narrative


def test_factories():
    detector = build_yolov10_detector()
    tracker = build_bytetrack_tracker()
    assert detector is not None
    assert tracker is not None


def test_dataset_registry():
    dataset = build_dataset("toy")
    assert len(list(dataset.frames())) > 0


def test_narratives_template():
    evidence = NarrativeEvidence(gate_sigma=2.5, appearance_cosine=0.9, occlusion_frames=3, reentry_camera="cam0")
    message = build_narrative(track_id=42, evidence=evidence)
    assert "Track 42" in message

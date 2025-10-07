<!-- BEGIN AUTO-HANDOFF -->
- 2025-10-07T19:12:06-05:00 | Initialized engineering handoff with goals, decisions, and environment notes.
- 2025-10-07T19:12:06-05:00 | Captured run commands, risks, TODOs, and next-agent bootstrap guidance.
- 2025-10-07T19:12:06-05:00 | Logged change history and provided prompt seed for future automation.

_Tip: Refresh this handoff after altering configs, datasets, or metrics so successors stay aligned._

## Context & Goals
Amodal CCTV Tracking Pipeline aims to deliver amodal detections, permanence-aware tracking, and narrative
explanations for reappearance events. Current scope focuses on scaffolding detectors (YOLOv10, RT-DETRv2),
ByteTrack association, amodal expander head, permanence filters, and evaluation stubs for occlusion-aware
metrics across TAO-Amodal, MOT17, and UA-DETRAC adapters.

## Current State & Decisions Log
- **D1**: Default experiment stack couples YOLOv10 detector and ByteTrack tracker for fast iteration.
- **D2**: Config files are placeholders; values live in Python factories until YAML authoring lands.
- **D3**: Sanity check relies on synthetic toy data to avoid distributing large assets.
- **D4**: Metrics modules are stubbed; integration with TrackEval deferred until ground truth wiring exists.

## Environment
| Component | Notes |
| --- | --- |
| OS | Developed on macOS (zsh shell); Linux expected to work with same commands. |
| Python | Target 3.10+. Use `python3 -m venv .venv` and activate before running tooling. |
| Key libs | Torch, Torchvision, NumPy, SciPy, PyYAML, OpenCV, Pillow, PyCOCOTools, Lap, FilterPy, Einops, Timm, Matplotlib, Seaborn, TQDM, Hydra-Core, TrackEval. |
| CLI entry | Run modules via `python -m ...`; export `PYTHONPATH=$PWD:${PYTHONPATH:-}`. |
| Tests | `pytest` (see `tests/test_imports.py`). No CI wiring yet. |

## Data Paths & Assumptions
- TAO-Amodal: `TAO_AMODAL_ROOT/{annotations,images}` with per-sequence folders.
- MOT17: `MOT17_ROOT/train/<sequence>/{img1,gt}`.
- UA-DETRAC: `UA_DETRAC_ROOT/Insight-MVT_Annotation_*`.
- Dataset factories accept `root` and `split`. Real loaders are stubs; create JSON/GT readers before scaling.
- Synthetic `ToyAmodalSequence` drives current smoke tests; no external data needed.

## How to Run
- **Sanity smoke**:
  ```bash
  source .venv/bin/activate
  export PYTHONPATH=$PWD:${PYTHONPATH:-}
  bash scripts/sanity_check.sh
  ```
- **Inference scaffold**:
  ```bash
  python -m amodal_cctv.scripts.run_infer --config configs/speed_yolov10.yaml
  ```
  Edit the script to switch from toy data to real adapters once configs expose dataset roots.
- **Evaluation skeleton**:
  ```bash
  python -m amodal_cctv.scripts.run_eval --slices occlusion_only
  ```
- **Ablation grid enumeration**:
  ```bash
  python -m amodal_cctv.scripts.run_ablation --detectors yolov10 rtdetrv2 --pno on off --reid off on
  ```

## Design Notes
- **Detector**: YOLOv10 wrapper lazily loads weights; RT-DETRv2 and ViTDet placeholders ready for swap-ins.
- **Tracker**: ByteTrack stub exposes `track_thresh`, `match_thresh`, `buffer_size`; Re-ID hooks still TODO.
- **Amodal head**: `AmodalExpanderHead` uses a 3-layer MLP; requires PyTorch import at instantiation time.
- **Permanence filter**: Existence decay (`alpha=0.94`) plus Kalman covariance inflation (`1.05`) and gate
  widening (`time_widen_coeff=0.2`) balance recall vs. false permanence.
- **Narratives**: Templates live in `amodal_cctv/explain/narratives.py`; evidence schema includes gate sigma,
  appearance cosine, occlusion duration, and reentry camera metadata.
- **Evaluation**: Slices enumerated in `amodal_cctv/eval/slices.py`; TrackEval adapter awaits real predictions.

## Metrics Status
| Metric | Status | Blocking Items |
| --- | --- | --- |
| Visibility-binned AP | Stub | Implement TAO loaders and precision-recall hooks. |
| Track-AP | Stub | Needs track association + evaluation harness. |
| APOoF | Planned | Requires out-of-fov GT and tracking telemetry. |
| HOTA / IDF1 | Stub | Wire to TrackEval adapter once predictions persist. |
| Time-to-reacquire | Planned | Depends on occlusion interval logger integration. |
| IDSW (occlusion-only) | Planned | Requires stable track IDs from tracker output. |

## Risks & Mitigations
- **R1**: Real dataset loaders absent -> Mitigate by prototyping TAO reader with small clip before scale-up.
- **R2**: Dependency drift -> Capture `pip freeze` per experiment; plan pinned `requirements.txt`.
- **R3**: Re-ID scope creep -> Keep ByteTrack baseline until Re-ID embeddings validated on MOT17.
- **R4**: Metric correctness -> Build unit tests around synthetic sequences per slice to validate math.
- **R5**: Long occlusion handling -> Implement `T_max_gap` guard and stress-test gating thresholds.

## Open Questions & TODOs
- [P0] Implement dataset-backed inference/eval pipeline with persisted predictions.
- [P0] Author YAML configs under `configs/` with detector/tracker/permanence toggles.
- [P1] Integrate TrackEval metrics and persist results for occlusion slices.
- [P1] Add lightweight Re-ID option (OSNet or FastReID) and expose toggles.
- [P2] Build narrative overlay renderer for qualitative demos.
- [P2] Automate dependency export into maintained lockfile.

## Next-Agent Bootstrap
1. Create or update a `configs/*.yaml` pointing to your dataset roots and toggles.
2. Flesh out dataset loaders (`amodal_cctv/data/*.py`) to return real frames and annotations.
3. Extend `run_infer` and `run_eval` to read configs, persist outputs, and emit metrics.
4. Add focused unit tests mirroring new functionality under `tests/`.

## Paste-ready System Prompt Seed
```text
You are the next Amodal CCTV Tracking engineer. Improve dataset adapters, config loading, and metrics so the pipeline evaluates TAO-Amodal, MOT17, and UA-DETRAC slices end-to-end while keeping narratives consistent.
```

## Minimal File Tree to Scaffold
```text
amodal_cctv/
  amodal/
  data/
  detectors/
  eval/
  explain/
  permanence/
  scripts/
  trackers/
configs/
docs/
scripts/
tests/
```

## Smoke Tests
- `bash scripts/sanity_check.sh`
- `pytest -q`
- `python -m amodal_cctv.scripts.run_eval --slices occlusion_only`

## Change Log
- 2025-10-07T19:12:06-05:00 | Created initial HANDOFF with environment, decisions, and TODOs.

**Last updated:** 2025-10-07T19:12:06-05:00
<!-- END AUTO-HANDOFF -->

# Amodal CCTV Tracking Pipeline

## Overview
This repository hosts a modular, speed-first pipeline for amodal CCTV tracking with object permanence and narrative explanations. The default configuration couples a frozen YOLOv10 detector with ByteTrack for association, extends tracks with an amodal expander head, and maintains existence probabilities through a Kalman-based permanence filter. Narrative one-liners and relevance visualizations are emitted whenever objects reappear after occlusion.

## Key Capabilities
- **Amodal detection**: Lightweight MLP expander predicts amodal deltas for occluded or out-of-view objects without updating the base detector.
- **Object permanence**: Constant-velocity Kalman filter with time-widened Mahalanobis gates and per-track existence probability decay/inflation.
- **Narrative explanations**: Template-based summaries enriched with evidence statistics (gate sigma, cosine similarity, occlusion duration, re-entry camera) and hooks for Grad-CAM/transformer relevance.
- **Evaluation ready**: TAO-Amodal primary dataset with adapters for MOT17 and UA-DETRAC, occlusion-aware metrics (visibility-binned AP/Track-AP, APOoF, HOTA/IDF1, time-to-reacquire), and TrackEval integration.
- **Speed-first defaults**: YOLOv10 + ByteTrack + no Re-ID for rapid experiments; OC-SORT, StrongSORT, and lightweight Re-ID (OSNet/FastReID) available as switches.

## Repository Layout
- `amodal_cctv/`: Core Python package with detectors, trackers, amodal head, permanence logic, explainability helpers, evaluation tools, and dataset adapters.
- `configs/`: YAML configuration files controlling detector/tracker toggles, permanence parameters, and ablations.
- `scripts/`: Entry points for sanity checks, inference, evaluation, and ablations.
- `docs/`: Project documentation including install instructions, method card, metrics protocol, and ablation notes.
- `tests/`: Unit tests targeting critical math components and import coverage.

## Quickstart
1. Follow `docs/install.md` to set up the environment.
2. Run the sanity script to validate the installation:
   ```bash
   bash scripts/sanity_check.sh
   ```
3. Launch a fast inference pass with the speed-focused config:
   ```bash
   python -m amodal_cctv.scripts.run_infer --config configs/speed_yolov10.yaml
   ```
4. Evaluate occlusion-focused slices:
   ```bash
   python -m amodal_cctv.scripts.run_eval --slices occlusion_only
   ```

## Status
- Training of the amodal head is deferred until explicit instruction (`BEGIN TRAINING`).
- Re-ID is wired but disabled by default; enable via `configs/reid_on.yaml` when long-term re-entries are critical.
- Grad-CAM and transformer relevance visualizers provide qualitative support for reappearance decisions.

## Citation
A `CITATION.cff` file is included for ease of referencing this work in academic material.

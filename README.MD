<!-- BEGIN AUTO-README -->
- 2025-10-07T19:12:06-05:00 | README skeleton with setup, run, and eval sections captured.
- 2025-10-07T19:12:06-05:00 | Repo map, dataset adapters, and metrics status linked.
- 2025-10-07T19:12:06-05:00 | Troubleshooting guidance and maintenance tip added.

_Tip: Re-run this updater after modifying configs, metrics, or scripts to keep guidance fresh._

## Project Title & One-Liner
**Amodal CCTV Tracking Pipeline** - Modular amodal detection, permanence filtering, and narrative CCTV tracking.

## Quickstart (macOS & Linux)
1. Ensure Python 3.10+ is available: `python3 --version`.
2. Create and activate an isolated env:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Upgrade pip and install core deps (CUDA wheels recommended when available):
   ```bash
   pip install --upgrade pip
   pip install torch torchvision numpy scipy pyyaml opencv-python pillow pycocotools lap filterpy \
einops timm matplotlib seaborn tqdm hydra-core trackeval
   ```
4. Expose the repo on `PYTHONPATH` for local modules:
   ```bash
   export PYTHONPATH=$PWD:${PYTHONPATH:-}
   ```

## Prereqs
- Python 3.10 or newer.
- Optional: NVIDIA GPU with CUDA 12.1+ for detector acceleration.
- Git for version tracking.
- Recommended: `ffmpeg` for video export when qualitative demos expand.

## Install
The project is not yet packaged. Use editable source layout via `PYTHONPATH` as above. To capture your
dependency snapshot, run:
```bash
pip freeze > requirements.lock.txt
```
Keep this file out of version control until dependency governance is finalized.

## Sanity Check
Run the bundled smoke script:
```bash
bash scripts/sanity_check.sh
```
Expected output: `outputs/sanity_demo/narratives.json` plus console log indicating success.

## Run Guide
- Always activate `.venv` and export `PYTHONPATH`.
- To run inference with default speed config:
  ```bash
  python -m amodal_cctv.scripts.run_infer --config configs/speed_yolov10.yaml
  ```
  Create or edit the referenced config before first use (see Config toggles).
- Evaluation entry point:
  ```bash
  python -m amodal_cctv.scripts.run_eval --slices full
  ```

## Inference
- **Toy sequence (bundled)**: The CLI currently loads `ToyAmodalSequence` by default; run:
  ```bash
  python -m amodal_cctv.scripts.run_infer --config configs/speed_yolov10.yaml
  ```
  Inspect the returned predictions dict for placeholder track outputs.
- **Real sequence (TAO-Amodal example)**: Extend `amodal_cctv.scripts.run_infer` to build a dataset via
  `build_dataset("tao_amodal", root=...)`, then launch with a config that names the dataset root. Add the
  config under `configs/` and version it with your experiment.

## Evaluation
- Occlusion-only slice:
  ```bash
  python -m amodal_cctv.scripts.run_eval --slices occlusion_only
  ```
- Out-of-fov slice:
  ```bash
  python -m amodal_cctv.scripts.run_eval --slices out_of_fov
  ```
- APOoF, HOTA, IDF1, time-to-reacquire, and ID switch metrics are scaffolded in `amodal_cctv/eval` and
  require dataset-specific ground truth before producing values.

## Config Toggles
| Toggle | Location | Default | Notes |
| --- | --- | --- | --- |
| Detector | `amodal_cctv/detectors/yolo_v10.py` | YOLOv10 frozen | Swap via factory or future YAML configs. |
| Detector (RT-DETRv2) | `amodal_cctv/detectors/rtdetrv2.py` | Variant `r18` | Add weights path for accuracy-focused runs. |
| Tracker | `amodal_cctv/trackers/bytetrack.py` | ByteTrack | Adjust `track_thresh`, `match_thresh`, `buffer_size`. |
| Re-ID | TODO (tracker extensions) | Off | Implement lightweight Re-ID before flipping on. |
| Amodal head | `amodal_cctv/amodal/expander_head.py` | MLP 256 hidden | Requires PyTorch; dropout tunable. |
| Alpha (existence decay) | `amodal_cctv/permanence/existence_filter.py` | 0.94 | Increase for slower decay; boost is 0.2. |
| Gate growth | `amodal_cctv/permanence/gating.py` | `time_widen_coeff=0.2` | Controls Mahalanobis gate widening per frame gap. |
| T_max_gap | Not yet implemented | N/A | Track this in configs once long-gap handling lands. |
| Kalman inflation | `amodal_cctv/permanence/kalman.py` | 1.05 | Inflates covariance before predict step. |

## Repo Map
| Path | Purpose |
| --- | --- |
| `amodal_cctv/` | Core package exports for detectors, trackers, amodal head, permanence, eval. |
| `amodal_cctv/amodal/` | Amodal expander head and related configs. |
| `amodal_cctv/data/` | Dataset adapters (TAO-Amodal, MOT17, UA-DETRAC, toy). |
| `amodal_cctv/detectors/` | Detector wrappers (YOLOv10, RT-DETRv2, ViTDet placeholder). |
| `amodal_cctv/eval/` | Metric slices and adapters to TrackEval. |
| `amodal_cctv/explain/` | Narrative templates and evidence schemas. |
| `amodal_cctv/permanence/` | Kalman filter, gating, existence probability utilities. |
| `amodal_cctv/trackers/` | Association logic (ByteTrack stub, future variants). |
| `amodal_cctv/scripts/` | CLI entry points for inference, eval, ablations. |
| `scripts/` | Shell helpers (sanity_check). |
| `tests/` | Pytest smoke tests for imports and narrative templates. |
| `docs/` | Supplemental documentation (install notes, method guide). |
| `configs/` | Placeholder for YAML configs (create per experiment). |

## Datasets
- **TAO-Amodal**: Expect `TAO_AMODAL_ROOT/annotations/*.json` and `TAO_AMODAL_ROOT/images/<sequence>/<frame>.jpg`.
- **MOT17**: Expect `MOT17_ROOT/train/<sequence>/img1/*.jpg` with matching `gt/gt.txt`.
- **UA-DETRAC**: Expect `UA_DETRAC_ROOT/Insight-MVT_Annotation_*` folders.
- Point adapters via config fields (once configs land) or direct kwargs:
  ```python
  from amodal_cctv.data.datasets import build_dataset
  tao = build_dataset("tao_amodal", root="/data/tao-amodal", split="val")
  ```
- For quick tests, the toy dataset requires no assets.

## Metrics
| Metric | Slice | Status | Notes |
| --- | --- | --- | --- |
| AP by visibility bins | full or occlusion | Stub | Implement in `tao_amodal_metrics.py`. |
| Track-AP | occlusion_only | Stub | Requires detection-track matching logic. |
| APOoF | out_of_fov | Planned | Add once occlusion ground truth ingested. |
| HOTA / IDF1 | full | Stub | Integrate via `trackeval_adapter.py`. |
| Time-to-reacquire | occlusion_only | Planned | Needs interval logger wiring. |
| IDSW (occ-only) | occlusion_only | Planned | Depends on tracker outputs with IDs. |

## Ablations
Enumerate detector, permanence, and Re-ID combinations (currently prints grid for orchestration tooling):
```bash
python -m amodal_cctv.scripts.run_ablation --detectors yolov10 rtdetrv2 --pno on off --reid off on
```
Pipe future JSON outputs into your sweep manager once the CLI emits metrics.

## Narratives Demo
- Run `bash scripts/sanity_check.sh`.
- Inspect `outputs/sanity_demo/narratives.json` for narrative one-liners plus evidence.
- Extend by adding overlay rendering under `amodal_cctv/explain/` when visualization hooks are ready.

## Troubleshooting & FAQs
- **ImportError: No module named amodal_cctv**  
  Ensure `.venv` is active and `export PYTHONPATH=$PWD:${PYTHONPATH:-}`.
- **CUDA mismatch**  
  Install Torch wheel matching your driver (`pip install torch==<version>+cu121 -f https://download.pytorch.org/whl/torch_stable.html`).
- **Missing pycocotools on macOS**  
  `pip install cython` before installing, or use `pip install "pycocotools>=2.0.7"`.
- **Need CPU fallback**  
  Override detector device: `build_yolov10_detector({"device": "cpu"})`.
- **Version drift**  
  Capture `pip freeze` snapshots and pin in per-experiment lockfiles.

## License & Citation
- License: MIT (see `LICENSE`).
- Citation metadata: `CITATION.cff`.

**Last updated:** 2025-10-07T19:12:06-05:00 | Initial auto-managed README created.
<!-- END AUTO-README -->

# Installation Guide

The pipeline targets Python 3.10+ and CUDA-enabled GPUs but can operate in CPU-only mode for lightweight debugging. These instructions assume a Unix-like environment.

## 1. Create Environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## 2. Install Core Dependencies
```bash
pip install -r requirements.txt
```
The initial requirements file will include:
- `torch`, `torchvision` (CUDA wheels recommended when available)
- `numpy`, `scipy`, `pyyaml`
- `opencv-python`, `Pillow`
- `pycocotools`, `lap`, `filterpy`
- `einops`, `timm` (for transformer-based detectors)
- `matplotlib`, `seaborn`, `tqdm`
- `hydra-core` (if using Hydra style configs)
- `trackeval`

Detector-specific extras (YOLOv10, RT-DETRv2, ViTDet) are vendored via lightweight wrappers; optional dependencies will be listed in `extras/` sections inside the config files.

## 3. Install Pretrained Weights (Optional)
Download detector/tracker checkpoints into `weights/` (create if absent). The sanity script falls back to automatically generated synthetic frames if no weights are found.

## 4. Run Diagnostics
```bash
bash scripts/sanity_check.sh
```
This script verifies Python package imports, instantiates the default YOLOv10+ByteTrack configuration, runs a synthetic occlusion toy scenario, and emits a short narrative JSON + PNG pair under `outputs/sanity_demo/`.

## 5. Development Tips
- Use `npm run dev`? No Node stack here—stick to Python entry points described in `docs/README.md`.
- Before modifying configs, duplicate them into a separate file and document your changes in `docs/ablations.md`.
- Run `pytest` (or `npm test` equivalent) via `pytest tests -q` before committing code changes.

## Troubleshooting
- **Import errors**: Double-check that `.venv` is activated and the project root is on `PYTHONPATH` (`export PYTHONPATH=$PWD:$PYTHONPATH`).
- **CUDA mismatch**: Ensure the installed PyTorch build matches your driver/runtime. Use `pip install torch==<version>+cu121 -f https://download.pytorch.org/whl/torch_stable.html` as needed.
- **Missing weights**: Update the corresponding config to point to your local checkpoint or switch to CPU-friendly mock outputs for quick debugging.

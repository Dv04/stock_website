"""Dataset registry for amodal CCTV experiments."""
from __future__ import annotations

from typing import Dict, Type

from .tao_amodal import TAOAmodalDataset
from .mot17 import MOT17Dataset
from .detrac import UADETRACDataset
from .toy_examples import ToyAmodalSequence


DATASET_REGISTRY: Dict[str, Type] = {
    "tao_amodal": TAOAmodalDataset,
    "mot17": MOT17Dataset,
    "ua_detrac": UADETRACDataset,
    "toy": ToyAmodalSequence,
}


def build_dataset(name: str, **kwargs):
    if name not in DATASET_REGISTRY:
        raise KeyError(f"Dataset {name} not registered")
    return DATASET_REGISTRY[name](**kwargs)

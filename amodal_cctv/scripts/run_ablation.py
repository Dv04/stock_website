"""CLI entry point for running ablation sweeps (declaration only)."""
from __future__ import annotations

import argparse
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Declare ablation sweep parameters")
    parser.add_argument("--detectors", nargs="*", default=["yolov10", "rtdetrv2"])
    parser.add_argument("--pno", nargs="*", default=["on", "off"])
    parser.add_argument("--reid", nargs="*", default=["off", "on"])
    return parser.parse_args()


def enumerate_grid(detectors: List[str], pno: List[str], reid: List[str]) -> List[dict]:
    grid = []
    for det in detectors:
        for p in pno:
            for r in reid:
                grid.append({"detector": det, "pno": p, "reid": r})
    return grid


def main() -> None:
    args = parse_args()
    _ = enumerate_grid(args.detectors, args.pno, args.reid)


if __name__ == "__main__":
    main()

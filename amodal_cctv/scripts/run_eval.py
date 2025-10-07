"""CLI entry point for evaluating occlusion-aware metrics."""
from __future__ import annotations

import argparse

from ..eval import slices


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate amodal CCTV metrics")
    parser.add_argument("--slices", type=str, default="full")
    return parser.parse_args()


def run(slice_name: str) -> None:
    data = {"dummy": []}
    _ = slices.filter_by_slice(data, slice_name)


def main() -> None:
    args = parse_args()
    run(args.slices)


if __name__ == "__main__":
    main()

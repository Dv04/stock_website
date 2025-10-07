"""ByteTrack tracker implementation with linear assignment matching."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from scipy.optimize import linear_sum_assignment
except ImportError:  # pragma: no cover - fallback when SciPy unavailable
    linear_sum_assignment = None


@dataclass
class ByteTrackConfig:
    """Configurables for the simplified ByteTrack tracker."""

    track_thresh: float = 0.5
    match_thresh: float = 0.8
    buffer_size: int = 30
    max_age: int = 60


@dataclass
class TrackState:
    """Internal representation of a track hypothesis."""

    track_id: int
    box: np.ndarray
    score: float
    class_id: int
    feature: Optional[np.ndarray]
    hits: int = 1
    age: int = 1
    time_since_update: int = 0
    is_confirmed: bool = False

    def update(self, box: np.ndarray, score: float, feature: Optional[np.ndarray]) -> None:
        self.box = box
        self.score = score
        self.feature = feature
        self.hits += 1
        self.time_since_update = 0
        if self.hits >= 3:
            self.is_confirmed = True

    def mark_missed(self) -> None:
        self.age += 1
        self.time_since_update += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "box": self.box.copy(),
            "score": float(self.score),
            "class_id": int(self.class_id),
            "age": self.age,
            "hits": self.hits,
            "time_since_update": self.time_since_update,
            "is_confirmed": self.is_confirmed,
            "feature": None if self.feature is None else self.feature.copy(),
        }


class ByteTrackTracker:
    """Simplified but functional ByteTrack association pipeline."""

    def __init__(self, config: ByteTrackConfig) -> None:
        self.config = config
        self._tracks: List[TrackState] = []
        self._next_track_id = 1

    @staticmethod
    def _compute_iou_matrix(track_boxes: np.ndarray, det_boxes: np.ndarray) -> np.ndarray:
        if track_boxes.size == 0 or det_boxes.size == 0:
            return np.zeros((track_boxes.shape[0], det_boxes.shape[0]), dtype=float)
        iou = np.zeros((track_boxes.shape[0], det_boxes.shape[0]), dtype=float)
        for i, t_box in enumerate(track_boxes):
            tx1, ty1, tx2, ty2 = t_box
            t_area = max(tx2 - tx1, 0) * max(ty2 - ty1, 0)
            for j, d_box in enumerate(det_boxes):
                dx1, dy1, dx2, dy2 = d_box
                d_area = max(dx2 - dx1, 0) * max(dy2 - dy1, 0)
                ix1, iy1 = max(tx1, dx1), max(ty1, dy1)
                ix2, iy2 = min(tx2, dx2), min(ty2, dy2)
                iw, ih = max(ix2 - ix1, 0), max(iy2 - iy1, 0)
                inter = iw * ih
                union = t_area + d_area - inter
                if union <= 0:
                    iou[i, j] = 0.0
                else:
                    iou[i, j] = inter / union
        return iou

    @staticmethod
    def _extract_feature(features: Any, index: int) -> Optional[np.ndarray]:
        if features is None:
            return None
        if isinstance(features, np.ndarray):
            if features.ndim == 1:
                return features.copy()
            if features.shape[0] > index:
                return features[index].copy()
            return None
        if isinstance(features, Sequence):
            if len(features) > index:
                value = features[index]
                if isinstance(value, np.ndarray):
                    return value.copy()
                return np.array(value)
        return None

    def _match_tracks(
        self, det_boxes: np.ndarray, track_boxes: np.ndarray
    ) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
        if len(self._tracks) == 0 or det_boxes.shape[0] == 0:
            return [], list(range(len(self._tracks))), list(range(det_boxes.shape[0]))

        iou_matrix = self._compute_iou_matrix(track_boxes, det_boxes)
        matched, unmatched_tracks, unmatched_dets = [], list(range(len(self._tracks))), list(range(det_boxes.shape[0]))

        if linear_sum_assignment is not None:
            cost = 1.0 - iou_matrix
            row_ind, col_ind = linear_sum_assignment(cost)
            for r, c in zip(row_ind, col_ind):
                if iou_matrix[r, c] >= self.config.match_thresh:
                    matched.append((r, c))
                    unmatched_tracks.remove(r)
                    unmatched_dets.remove(c)
        else:  # pragma: no cover - fallback for environments without SciPy
            taken_tracks, taken_dets = set(), set()
            flat_indices = np.dstack(np.unravel_index(np.argsort(-iou_matrix, axis=None), iou_matrix.shape))[0]
            for r, c in flat_indices:
                if r in taken_tracks or c in taken_dets:
                    continue
                if iou_matrix[r, c] >= self.config.match_thresh:
                    matched.append((r, c))
                    taken_tracks.add(r)
                    taken_dets.add(c)
            unmatched_tracks = [idx for idx in unmatched_tracks if idx not in taken_tracks]
            unmatched_dets = [idx for idx in unmatched_dets if idx not in taken_dets]
        return matched, unmatched_tracks, unmatched_dets

    def update(self, detections: Dict[str, Any], timestamp: Optional[float] = None) -> List[Dict[str, Any]]:
        boxes = np.asarray(detections.get("boxes", []), dtype=float)
        scores = np.asarray(detections.get("scores", []), dtype=float)
        classes = np.asarray(detections.get("classes", []), dtype=int)
        features = detections.get("features")

        if boxes.ndim == 1:
            boxes = boxes.reshape(-1, 4)
        if boxes.size == 0:
            boxes = np.empty((0, 4), dtype=float)
        if scores.size == 0:
            scores = np.zeros((boxes.shape[0],), dtype=float)
        if classes.size == 0:
            classes = np.zeros((boxes.shape[0],), dtype=int)

        # Update bookkeeping for existing tracks.
        for track in self._tracks:
            track.mark_missed()

        track_boxes = np.vstack([track.box for track in self._tracks]) if self._tracks else np.empty((0, 4))
        matched, unmatched_tracks, unmatched_dets = self._match_tracks(boxes, track_boxes)

        for track_idx, det_idx in matched:
            track = self._tracks[track_idx]
            feature_vec = self._extract_feature(features, det_idx)
            track.update(boxes[det_idx], float(scores[det_idx]), feature_vec)
            track.class_id = int(classes[det_idx])

        # Retire tracks that exceeded buffer / age.
        surviving_tracks: List[TrackState] = []
        for idx, track in enumerate(self._tracks):
            if idx in unmatched_tracks and track.time_since_update > self.config.buffer_size:
                continue
            if track.age > self.config.max_age:
                continue
            surviving_tracks.append(track)
        self._tracks = surviving_tracks

        # Spawn tracks for unmatched detections above threshold.
        for det_idx in unmatched_dets:
            if float(scores[det_idx]) < self.config.track_thresh:
                continue
            feature_vec = self._extract_feature(features, det_idx)
            new_track = TrackState(
                track_id=self._next_track_id,
                box=boxes[det_idx],
                score=float(scores[det_idx]),
                class_id=int(classes[det_idx]),
                feature=feature_vec,
                hits=1,
                age=1,
                time_since_update=0,
                is_confirmed=False,
            )
            self._next_track_id += 1
            self._tracks.append(new_track)

        # Sort tracks by track_id for deterministic output.
        self._tracks.sort(key=lambda t: t.track_id)
        outputs = [track.to_dict() for track in self._tracks if track.is_confirmed or track.hits >= 1]

        for item in outputs:
            item["timestamp"] = timestamp
            item["status"] = "tracked" if item["time_since_update"] == 0 else "tentative"
        return outputs

    def track(self, detections: Dict[str, Any], timestamp: Optional[float] = None) -> List[Dict[str, Any]]:
        """Compatibility alias for previous API."""
        return self.update(detections, timestamp=timestamp)


def build_bytetrack_tracker(config_dict: Dict[str, Any] | None = None) -> ByteTrackTracker:
    config = ByteTrackConfig(**(config_dict or {}))
    return ByteTrackTracker(config)

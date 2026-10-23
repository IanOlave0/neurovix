"""Full-inverse frontalization (no camera needed).

Pins three properties with synthetic similarity transforms
(M = translation @ Y-rotation @ uniform scale):
1. Round trip: frontalize(M @ face) recovers the mouth points, for +20 AND
   -20 degrees (the old yaw-angle path was only tested one way — that is
   how the directional bias shipped).
2. Asymmetry survives: a deformed (drooped) face keeps its half-width gap
   after frontalization. Frontalization removes pose, never the signal.
"""

import numpy as np

from src.index import mouth_half_widths
from src.landmarks import MOUTH_LEFT, MOUTH_RIGHT
from src.normalize import frontalize_full
from tests.test_index import fake_face


def similarity_matrix(yaw_deg: float, scale: float = 2.0) -> np.ndarray:
    theta = np.radians(yaw_deg)
    c, s = np.cos(theta), np.sin(theta)
    m = np.eye(4)
    m[:3, :3] = [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]
    m[:3, :3] *= scale
    m[:3, 3] = [0.5, 0.25, 0.1]
    return m


def apply(pts: np.ndarray, m: np.ndarray) -> np.ndarray:
    homo = np.ones((len(pts), 4))
    homo[:, :3] = pts[:, :3]
    out = homo @ m.T
    return (out[:, :3] / out[:, 3:4]).astype(np.float32)


def test_round_trip_positive_yaw():
    pts = fake_face()
    back = frontalize_full(apply(pts, similarity_matrix(20.0)),
                           similarity_matrix(20.0))
    assert np.allclose(back[MOUTH_LEFT, :2], pts[MOUTH_LEFT, :2], atol=1e-4)
    assert np.allclose(back[MOUTH_RIGHT, :2], pts[MOUTH_RIGHT, :2], atol=1e-4)


def test_round_trip_negative_yaw():
    pts = fake_face()
    back = frontalize_full(apply(pts, similarity_matrix(-20.0)),
                           similarity_matrix(-20.0))
    assert np.allclose(back[MOUTH_LEFT, :2], pts[MOUTH_LEFT, :2], atol=1e-4)
    assert np.allclose(back[MOUTH_RIGHT, :2], pts[MOUTH_RIGHT, :2], atol=1e-4)


def test_frontalization_preserves_asymmetry():
    pts = fake_face()
    pts[MOUTH_RIGHT, 0] -= 0.10
    before = abs(mouth_half_widths(pts)[0] - mouth_half_widths(pts)[1])
    back = frontalize_full(apply(pts, similarity_matrix(-20.0)),
                           similarity_matrix(-20.0))
    after = abs(mouth_half_widths(back)[0] - mouth_half_widths(back)[1])
    assert abs(before - after) < 1e-4  # pose removed, signal intact

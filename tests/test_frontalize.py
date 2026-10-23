"""3D yaw frontalization math (no camera needed).

frontalize_yaw must invert a pure Y-rotation: rotate the fake face by +20
degrees about the nose vertical axis, frontalize by the same angle read the
way yaw_from_matrix reads it, and the mouth must land back where it was.
yaw_from_matrix is checked against a synthetic Y-rotation matrix first, so
the convention is pinned before touching real detector output.
"""

import numpy as np
import pytest

from src.landmarks import MOUTH_LEFT, MOUTH_RIGHT, NOSE_TIP
from src.normalize import frontalize_yaw, yaw_from_matrix
from tests.test_index import fake_face


def y_rotation_matrix(degrees: float) -> np.ndarray:
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    m = np.eye(4)
    m[:3, :3] = [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]
    return m


def apply_yaw(points: np.ndarray, degrees: float) -> np.ndarray:
    """Simulate a yaw turn: rotate about the nose vertical axis."""
    out = points.copy().astype(float)
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    v = out - out[NOSE_TIP]
    out[:, 0] = c * v[:, 0] + s * v[:, 2] + out[NOSE_TIP, 0]
    out[:, 2] = -s * v[:, 0] + c * v[:, 2] + out[NOSE_TIP, 2]
    return out.astype(np.float32)


def test_yaw_from_matrix_reads_y_rotation():
    assert yaw_from_matrix(y_rotation_matrix(20.0)) == pytest.approx(np.radians(20.0))


def test_frontalize_inverts_yaw_turn():
    pts = fake_face()
    turned = apply_yaw(pts, 20.0)
    back = frontalize_yaw(turned, np.radians(20.0))
    assert np.allclose(back[MOUTH_LEFT, :2], pts[MOUTH_LEFT, :2], atol=1e-5)
    assert np.allclose(back[MOUTH_RIGHT, :2], pts[MOUTH_RIGHT, :2], atol=1e-5)

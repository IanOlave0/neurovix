"""Pose-gate behavior on synthetic faces.

A 5-degree tilt must pass (correctable); a 20-degree ear-to-shoulder tilt
must be rejected with reason "roll", never silently corrected. These
thresholds pin the CURRENT values — recalibration with real logged data
must update both the constant and these tests together.
"""

import numpy as np

from src.normalize import ROLL_EXCLUDE_DEG, normalize_frame
from tests.test_index import fake_face


def tilt(points: np.ndarray, degrees: float) -> np.ndarray:
    out = points.copy()
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    xy = out[:, :2] - np.array([0.5, 0.5])
    out[:, 0] = c * xy[:, 0] - s * xy[:, 1] + 0.5
    out[:, 1] = s * xy[:, 0] + c * xy[:, 1] + 0.5
    return out


def test_small_tilt_accepted():
    _, info = normalize_frame(tilt(fake_face(), 5.0))
    assert info["accepted"] is True
    assert info["rejected"] is None


def test_strong_tilt_rejected_with_reason():
    _, info = normalize_frame(tilt(fake_face(), 20.0))
    assert abs(info["roll_deg"]) > ROLL_EXCLUDE_DEG
    assert info["accepted"] is False
    assert info["rejected"] == "roll"


def test_frontal_face_accepted():
    _, info = normalize_frame(fake_face())
    assert info["accepted"] is True

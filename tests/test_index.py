"""Index behavior on synthetic faces (no camera needed).

Trick: build a fake 478x3 mesh with known geometry. A symmetric fake must
score ~0; a fake with one shifted corner must score high on that side.
This rig is ALSO the seed of the R7 robustness validation: the same
"deform one side, measure" machinery will later stress-test the real
landmarker (protocol section 7, risks.md R7).
"""

import numpy as np

from src.index import build_rest_index, gesture_score, smile_index
from src.landmarks import (
    CHIN,
    LEFT_EYE_INNER,
    LEFT_EYE_OUTER,
    MOUTH_LEFT,
    MOUTH_RIGHT,
    NOSE_TIP,
    RIGHT_EYE_INNER,
    RIGHT_EYE_OUTER,
)


def fake_face() -> np.ndarray:
    """Frontal, symmetric, already in eye-width units (interocular = 1)."""
    pts = np.zeros((478, 3), dtype=np.float32)
    pts[NOSE_TIP] = (0.5, 0.40, 0.0)
    pts[CHIN] = (0.5, 0.70, 0.0)
    pts[LEFT_EYE_OUTER] = (0.0, 0.35, 0.0)
    pts[LEFT_EYE_INNER] = (0.4, 0.35, 0.0)
    pts[RIGHT_EYE_INNER] = (0.6, 0.35, 0.0)
    pts[RIGHT_EYE_OUTER] = (1.0, 0.35, 0.0)
    pts[MOUTH_LEFT] = (0.30, 0.60, 0.0)
    pts[MOUTH_RIGHT] = (0.70, 0.60, 0.0)
    return pts


def test_symmetric_face_scores_zero():
    idx = smile_index(fake_face())
    assert idx["asymmetry"] == 0.0
    assert idx["weaker_side"] == "symmetric"
    assert idx["angle_diff_deg"] == 0.0


def test_drooped_corner_detected_on_correct_side():
    pts = fake_face()
    pts[MOUTH_RIGHT, 0] -= 0.10  # right corner pulled toward midline
    idx = smile_index(pts)
    assert idx["asymmetry"] == 0.10
    assert idx["weaker_side"] == "right"


def test_gesture_is_delta_against_rest():
    rest = smile_index(fake_face())
    smile = smile_index(fake_face())
    assert gesture_score(smile, rest) == 0.0
    droop = fake_face()
    droop[MOUTH_LEFT, 0] += 0.08
    assert gesture_score(smile_index(droop), rest) == 0.08


def test_rolled_face_still_symmetric_after_deroll():
    from src.normalize import deroll

    pts = fake_face()
    theta = np.radians(10.0)
    c, s = np.cos(theta), np.sin(theta)
    xy = pts[:, :2] - np.array([0.5, 0.5])
    pts[:, 0] = c * xy[:, 0] - s * xy[:, 1] + 0.5
    pts[:, 1] = s * xy[:, 0] + c * xy[:, 1] + 0.5
    assert smile_index(deroll(pts))["weaker_side"] == "symmetric"


def test_rest_baseline_is_scale_invariant():
    # Regression test: rest built on raw pixels must equal rest built at
    # any camera distance (the old bug subtracted pixel-rest from
    # normalized-live). A face twice as close = identical rest index.
    rest_near = build_rest_index([fake_face()])
    rest_far = build_rest_index([fake_face() * 2.0])
    assert rest_near == rest_far

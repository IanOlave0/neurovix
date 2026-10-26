"""Rest-referenced alignment behavior (no camera needed).

These tests pin the redesign contract: rigid motion is removed, gestures
are preserved, mouth points never steer the alignment, and bad fits report
a large residual instead of a false measurement.
"""

import numpy as np

from src.index import dynamic_asymmetry
from src.landmarks import MOUTH_RIGHT
from src.normalize import interocular
from src.pose import ALIGN_RESID_TOL, STABLE_POINTS, align_to_rest, estimate_similarity
from tests.test_index import fake_face


def rigid(points: np.ndarray, degrees: float, scale: float, shift):
    out = points.copy().astype(float)
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    rot = np.array([[c, -s], [s, c]])
    out[:, :2] = scale * (out[:, :2] @ rot) + np.asarray(shift, dtype=float)
    return out.astype(np.float32)


def test_identity_alignment_is_exact():
    pts = fake_face()
    aligned, rmse, _ = align_to_rest(pts, pts)
    assert rmse < 1e-6
    assert np.allclose(aligned, pts, atol=1e-6)


def test_rigid_motion_positive_and_negative_is_removed():
    rest = fake_face()
    for deg in (20.0, -20.0):
        current = rigid(rest, deg, 1.2, [30.0, -12.0])
        aligned, rmse, _ = align_to_rest(current, rest)
        assert rmse < 1e-4
        assert np.allclose(aligned[:, :2], rest[:, :2], atol=1e-4)


def test_gesture_survives_alignment_and_scores():
    rest = fake_face()
    current = rigid(rest, -10.0, 1.1, [5.0, 3.0])
    current[MOUTH_RIGHT, 0] -= 0.10  # right corner droop in current space
    aligned, _, _ = align_to_rest(current, rest)
    unit = interocular(rest)
    dyn = dynamic_asymmetry(aligned / unit, rest / unit)
    assert dyn["move_right"] > dyn["move_left"]
    assert dyn["status"] == "CHECK"


def test_mouth_never_steers_alignment():
    rest = fake_face()
    moved = rigid(rest, 10.0, 1.1, [5.0, 3.0])
    moved[MOUTH_RIGHT, 0] -= 0.25  # large gesture must not move the fit
    _, _, t1 = align_to_rest(moved, rest)
    _, _, t2 = align_to_rest(rigid(rest, 10.0, 1.1, [5.0, 3.0]), rest)
    assert t1["scale"] == t2["scale"]
    assert np.allclose(t1["rotation"], t2["rotation"])
    assert np.allclose(t1["translation"], t2["translation"])


def test_corrupt_stable_fit_reports_large_residual():
    pts = fake_face()
    bad = pts.copy()
    bad[STABLE_POINTS[4], 0] += 0.40  # nose jumped: not a rigid motion
    _, rmse, _ = align_to_rest(bad, pts)
    assert rmse > ALIGN_RESID_TOL

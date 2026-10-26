"""Warp-field math tests (no camera, no detector).

These pin the deformation itself: the experiment in scripts/r7_validate.py
compares DETECTOR output against this math, so the math must be beyond
doubt first.
"""

import numpy as np

from src.warp import apply_warp, displacement_at


def test_center_moves_by_full_amplitude():
    d = displacement_at(np.array([[10.0, 10.0]]), np.array([10.0, 10.0]),
                        20.0, np.array([-1.0, 0.0]), 12.0)
    assert np.allclose(d, [[-12.0, 0.0]])


def test_far_field_is_negligible():
    d = displacement_at(np.array([[500.0, 500.0]]), np.array([10.0, 10.0]),
                        20.0, np.array([-1.0, 0.0]), 12.0)
    assert float(np.linalg.norm(d)) < 1e-3


def test_zero_amplitude_is_identity():
    rng = np.random.default_rng(0)
    frame = (rng.random((60, 80, 3)) * 255).astype(np.uint8)
    out = apply_warp(frame, np.array([40.0, 30.0]), 20.0,
                     np.array([-1.0, 0.0]), 0.0)
    assert np.array_equal(out, frame)


def test_direction_is_respected():
    d = displacement_at(np.array([[0.0, 0.0]]), np.array([0.0, 0.0]),
                        50.0, np.array([0.0, 1.0]), 5.0)
    assert np.allclose(d, [[0.0, 5.0]])


def test_output_shape_preserved():
    frame = np.zeros((48, 64, 3), dtype=np.uint8)
    out = apply_warp(frame, np.array([32.0, 24.0]), 10.0,
                     np.array([1.0, 0.0]), 8.0)
    assert out.shape == frame.shape


def test_known_dot_moves_as_predicted():
    # End-to-end warp check on synthetic content: a bright dot's centroid
    # must travel (approximately) the field displacement at its location.
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[48:53, 48:53] = (255, 255, 255)
    center = np.array([50.0, 50.0])
    out = apply_warp(frame, center, 30.0, np.array([1.0, 0.0]), 10.0)
    ys, xs = np.nonzero(out[..., 0] > 50)
    assert len(xs) > 0
    cx, cy = xs.mean(), ys.mean()
    assert abs(cx - 60.0) < 1.5
    assert abs(cy - 50.0) < 1.5

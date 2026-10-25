"""Pose gates: matrix yaw in degrees, roll relative to rest (no camera).

Pins the gate-only design (protocol 3.3): no geometric correction, only
exclusion — with the exclusion measured from the subject's own rest.
"""

import numpy as np
import pytest

from src.normalize import (
    ROLL_EXCLUDE_DEG,
    ROLL_REL_DEG,
    YAW_EXCLUDE_DEG,
    normalize_frame,
    yaw_from_matrix,
)
from tests.test_gates import tilt
from tests.test_index import fake_face


def y_rotation_matrix_4x4(degrees: float) -> np.ndarray:
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    m = np.eye(4)
    m[:3, :3] = [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]
    return m


def test_yaw_from_matrix_reads_both_directions():
    assert yaw_from_matrix(y_rotation_matrix_4x4(20.0)) == pytest.approx(np.radians(20.0))
    assert yaw_from_matrix(y_rotation_matrix_4x4(-20.0)) == pytest.approx(np.radians(-20.0))


def test_matrix_yaw_gate_rejects_extreme_turn():
    _, info = normalize_frame(fake_face(), matrix=y_rotation_matrix_4x4(25.0))
    assert info["accepted"] is False
    assert info["rejected"] == "yaw"


def test_matrix_yaw_gate_accepts_mild_turn():
    _, info = normalize_frame(fake_face(), matrix=y_rotation_matrix_4x4(5.0))
    assert info["accepted"] is True


def test_yaw_gate_measures_from_rest():
    # Rest posture turned -8 deg: +4 deg of further turn must pass
    # (12 excursion budget), -8 more must trip yaw-rel, not the horizon.
    _, info = normalize_frame(fake_face(), matrix=y_rotation_matrix_4x4(4.0),
                              rest_yaw=-8.0)
    assert info["accepted"] is True
    _, info = normalize_frame(fake_face(), matrix=y_rotation_matrix_4x4(5.0),
                              rest_yaw=-8.0)
    assert info["accepted"] is False
    assert info["rejected"] == "yaw-rel"


def test_roll_gate_measures_from_rest_not_horizon():
    rest_roll = 0.0  # frontal rest
    _, info = normalize_frame(tilt(fake_face(), ROLL_REL_DEG + 2.0),
                              rest_roll=rest_roll)
    assert info["accepted"] is False
    assert info["rejected"] == "roll-rel"


def test_absolute_roll_guard_still_fires():
    _, info = normalize_frame(tilt(fake_face(), ROLL_EXCLUDE_DEG + 5.0),
                              rest_roll=ROLL_EXCLUDE_DEG + 5.0)
    assert info["rejected"] == "roll"


def test_thresholds_are_placeholders_documented():
    assert YAW_EXCLUDE_DEG == 20.0
    assert ROLL_REL_DEG == 10.0

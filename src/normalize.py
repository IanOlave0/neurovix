"""Scale + pose normalization (protocol section 3.2, risk R4).

Why: raw landmarks carry three things tangled together — the face's
identity geometry, its distance/angle to the camera, and the gesture.
Only the gesture is signal. This module strips the camera out:

- Scale: divide every coordinate by the interocular distance, so a face
  30 cm away and one 60 cm away yield the same numbers (unit: "eye widths").
- Pose: measure in-plane roll from the eye line and rotate x, y back to
  level; estimate a yaw proxy from nose-to-eye distances and REJECT frames
  past the threshold (protocol 3.3) instead of correcting what we cannot
  trust. A turned head fakes asymmetry — exclusion beats correction.
"""

import numpy as np

from src.landmarks import (
    CHIN,
    LEFT_EYE_OUTER,
    MOUTH_LEFT,
    MOUTH_RIGHT,
    NOSE_TIP,
    RIGHT_EYE_OUTER,
)

YAW_EXCLUDE = 0.25  # |yaw proxy| above this -> frame rejected (tune in Phase 1)
ROLL_EXCLUDE_DEG = 15.0  # |roll| above this -> frame rejected, not corrected.
# 2D derotation cannot undo real 3D tilt (perspective + occlusion), and the
# eye line it measures from degrades under tilt too. Initial value is a
# placeholder: calibrate against logged roll-vs-asymmetry data (see demo).


def interocular(points: np.ndarray) -> float:
    """Eye-width unit, computed on raw (un-normalized) points."""
    return float(np.linalg.norm(points[LEFT_EYE_OUTER, :2] - points[RIGHT_EYE_OUTER, :2]))


def normalize_scale(points: np.ndarray) -> np.ndarray:
    """Divide x, y, z by the interocular distance (z shares x's scale)."""
    d = interocular(points)
    assert d > 1e-6, "degenerate face: eyes coincide"
    return points / d


def roll_deg(points: np.ndarray) -> float:
    """In-plane head tilt from the eye-outer-corner line, in degrees."""
    dx = points[RIGHT_EYE_OUTER, 0] - points[LEFT_EYE_OUTER, 0]
    dy = points[RIGHT_EYE_OUTER, 1] - points[LEFT_EYE_OUTER, 1]
    return float(np.degrees(np.arctan2(dy, dx)))


def deroll(points: np.ndarray) -> np.ndarray:
    """Rotate x, y by -roll around the eye midpoint (2D leveling)."""
    out = points.copy()
    center = (points[LEFT_EYE_OUTER, :2] + points[RIGHT_EYE_OUTER, :2]) / 2
    theta = np.radians(roll_deg(points))
    c, s = np.cos(theta), np.sin(theta)
    xy = out[:, :2] - center
    out[:, 0] = c * xy[:, 0] + s * xy[:, 1] + center[0]
    out[:, 1] = -s * xy[:, 0] + c * xy[:, 1] + center[1]
    return out


def yaw_proxy(points: np.ndarray) -> float:
    """Scale-free yaw estimate: how much closer one eye's outer corner is
    to the nose than the other's, in eye-width units. Zero = frontal."""
    nose = points[NOSE_TIP, :2]
    dl = float(np.linalg.norm(points[LEFT_EYE_OUTER, :2] - nose))
    dr = float(np.linalg.norm(points[RIGHT_EYE_OUTER, :2] - nose))
    return (dl - dr) / interocular(points)


def normalize_frame(points: np.ndarray) -> tuple[np.ndarray, dict]:
    """Full pipeline for one mesh: scale -> deroll -> yaw gate.

    Returns (normalized points, info dict with roll_deg, yaw_proxy,
    accepted). Rejected frames must be dropped by the caller, never
    silently corrected (protocol 3.3)."""
    yaw = yaw_proxy(points)
    roll = roll_deg(points)
    reason = None
    if abs(yaw) > YAW_EXCLUDE:
        reason = "yaw"
    elif abs(roll) > ROLL_EXCLUDE_DEG:
        reason = "roll"
    info = {"roll_deg": roll, "yaw_proxy": yaw,
            "accepted": reason is None, "rejected": reason}
    return normalize_scale(deroll(points)), info

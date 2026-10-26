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

YAW_EXCLUDE = 0.25  # proxy fallback (no matrix) -> frame rejected
YAW_EXCLUDE_DEG = 20.0  # absolute outer guard: beyond this the projection
# is too distorted no matter the rest posture.
YAW_REL_DEG = 12.0  # excursion from the SUBJECT'S OWN rest yaw. Same lesson
# as roll: a subject resting at -8 deg has 28 deg of room one way and 12
# the other under an absolute gate. PLACEHOLDER: calibrate with labeled logs.
ROLL_EXCLUDE_DEG = 15.0  # absolute outer guard: beyond this, no correction
# is even attempted (pure 2D leveling cannot undo real 3D tilt).
ROLL_REL_DEG = 10.0  # tilt RELATIVE to the subject's own rest posture.
# Rationale: a subject resting at roll -9 has ~2 degrees of room under an
# absolute gate — the gate must measure excursion from THEIR rest, not from
# the camera horizon. PLACEHOLDER: calibrate against labeled logs.


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


def normalize_frame(points: np.ndarray,
                      matrix: np.ndarray | None = None,
                      rest_roll: float | None = None,
                      rest_yaw: float | None = None) -> tuple[np.ndarray, dict]:
    """Full pipeline for one mesh: scale -> deroll -> pose gates.

    Exclusion-only by design (protocol 3.3): geometric correction of real
    3D pose was tried and REMOVED — evidence showed the full-matrix inverse
    amplifying yaw ~2x (matrix lives in metric 3D space, our points in
    image space). Gates, from strongest signal to weakest:

    - roll absolute: outer guard against extreme tilt.
    - roll relative: excursion from the SUBJECT'S OWN rest posture
      (a subject resting at -9 deg has almost no room under an absolute
      gate — the gate must measure from their rest, not the horizon).
    - yaw: matrix angle in real degrees when available (absolute outer
      guard + excursion from the subject's own rest yaw), proxy fallback
      without matrix.

    Returns (normalized points, info). Rejected frames must be dropped by
    the caller, never silently corrected.
    """
    yaw = yaw_proxy(points)
    roll = roll_deg(points)
    yaw_deg = round(float(np.degrees(yaw_from_matrix(matrix))), 1) \
        if matrix is not None else None
    reason = None
    if yaw_deg is not None:
        if abs(yaw_deg) > YAW_EXCLUDE_DEG:
            reason = "yaw"
        elif rest_yaw is not None and abs(yaw_deg - rest_yaw) > YAW_REL_DEG:
            reason = "yaw-rel"
    elif abs(yaw) > YAW_EXCLUDE:
        reason = "yaw"
    if reason is None and abs(roll) > ROLL_EXCLUDE_DEG:
        reason = "roll"
    if reason is None and rest_roll is not None \
            and abs(roll - rest_roll) > ROLL_REL_DEG:
        reason = "roll-rel"
    info = {"roll_deg": roll, "yaw_proxy": yaw, "yaw_deg_matrix": yaw_deg,
            "accepted": reason is None, "rejected": reason}
    return normalize_scale(deroll(points)), info


def yaw_from_matrix(matrix: np.ndarray) -> float:
    """Yaw angle (radians) from a 4x4 facial pose matrix.

    Takes the rotation block, normalizes out scale per column, and reads
    yaw = atan2(R[0,2], R[2,2]) — the Y-rotation convention. Used only to
    feed the yaw gate (degrees); geometric correction was removed after
    evidence showed matrix-space mismatch (see risks.md R4).
    """
    r = np.asarray(matrix, dtype=float)[:3, :3]
    norms = np.linalg.norm(r, axis=0, keepdims=True)
    norms[norms == 0] = 1.0
    r = r / norms
    return float(np.arctan2(r[0, 2], r[2, 2]))


# NOTE (2026-10-24): frontalization helpers lived here and were REMOVED.
# Evidence from labeled logs: applying M^-1 to image-space points amplified
# yaw ~2x (the matrix lives in metric 3D space). Pose is gates-only since.
# See risks.md R4 and protocol 3.3. yaw_from_matrix stays: it feeds the gate.

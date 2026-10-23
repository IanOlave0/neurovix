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


def yaw_from_matrix(matrix: np.ndarray) -> float:
    """Yaw angle (radians) from a 4x4 facial pose matrix.

    Takes the rotation block, normalizes out scale per column, and reads
    yaw = atan2(R[0,2], R[2,2]) — the Y-rotation convention. Sign and
    magnitude are verified empirically (frontalized yaw_proxy must shrink
    on real tilted frames); if it ever grows, this convention is wrong.
    """
    r = np.asarray(matrix, dtype=float)[:3, :3]
    norms = np.linalg.norm(r, axis=0, keepdims=True)
    norms[norms == 0] = 1.0
    r = r / norms
    return float(np.arctan2(r[0, 2], r[2, 2]))


def frontalize_yaw(points: np.ndarray, yaw_rad: float) -> np.ndarray:
    """Inverse Y-rotation about the nose: undo the yaw turn in 3D instead
    of rejecting the frame. 2D deroll stays for roll; this covers yaw."""
    out = points.copy().astype(float)
    center = out[NOSE_TIP].copy()
    c, s = np.cos(-yaw_rad), np.sin(-yaw_rad)
    v = out - center
    out[:, 0] = c * v[:, 0] + s * v[:, 2] + center[0]
    out[:, 2] = -s * v[:, 0] + c * v[:, 2] + center[2]
    return out.astype(np.float32)


def frontalize_full(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Undo pose with the FULL 4x4 inverse: canonical ~= M^-1 @ detected.

    Why not just the yaw angle: extracting one angle and re-applying a
    hand-made rotation corrected one turn direction better than the other
    (directional bias seen in logs). The full inverse handles yaw + roll +
    pitch + translation uniformly, with no convention to get backwards —
    inversion is inversion.

    Why asymmetry survives: M is a rigid-ish fit (rotation/translation/
    scale of the generic canonical model onto this face). It cannot encode
    expression or palsy, so M^-1 removes pose/scale but keeps the subject's
    own shape deviations — the signal. A test below pins exactly this.
    """
    m = np.asarray(matrix, dtype=float)
    assert m.shape == (4, 4), f"expected 4x4 pose matrix, got {m.shape}"
    homo = np.ones((len(points), 4))
    homo[:, :3] = points[:, :3]
    frontal = homo @ np.linalg.inv(m).T
    w = frontal[:, 3:4]
    w[w == 0] = 1.0
    out = points.copy().astype(float)
    out[:, :3] = frontal[:, :3] / w
    return out.astype(np.float32)


def normalize_frame_3d(points: np.ndarray,
                       matrix: np.ndarray | None) -> tuple[np.ndarray, dict]:
    """normalize_frame plus full 3D frontalization when the pose matrix is
    available. Falls back to the 2D path (same contract) when it is not,
    so old callers and logs stay comparable.

    yaw_proxy_raw = pose BEFORE frontalization (diagnostic: how far the
    head really turned). yaw_proxy = residual AFTER (what the index sees).
    """
    raw_yaw = yaw_proxy(points)
    if matrix is None:
        norm, info = normalize_frame(points)
        info["yaw_proxy_raw"] = round(raw_yaw, 4)
        info["yaw_deg_matrix"] = None
        return norm, info
    yaw = yaw_from_matrix(matrix)
    frontal = frontalize_full(points, matrix)
    norm, info = normalize_frame(frontal)
    info["yaw_proxy_raw"] = round(raw_yaw, 4)
    info["yaw_deg_matrix"] = round(float(np.degrees(yaw)), 1)
    return norm, info

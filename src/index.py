"""Smile asymmetry index — the interpretable clinical number.

For a normalized mesh (see `normalize.py`), the index decomposes into two
visible components per mouth corner, measured against the facial midline
(vertical axis through the nose tip):

1. Half-width: horizontal distance from midline to each corner, in eye
   widths. A symmetric smile has equal halves; a droop shortens one side.
2. Deviation angle: angle between each corner-to-nose vector and the
   vertical. Symmetric smile = mirrored angles.

The composite `asymmetry` is |left − right| of half-widths (primary) plus
the angle difference (secondary). Every term is human-readable: a reviewer
can point at the face and see each number. That is the whole point of an
interpretable core — no black box between the pixels and the claim.

Gesture score: index(smile) − index(rest). Faces are asymmetric at rest by
nature, so the signal is always a DELTA against the subject's own baseline
(protocol section 2), never an absolute value.
"""

import numpy as np

from src.landmarks import MOUTH_LEFT, MOUTH_RIGHT, NOSE_TIP
from src.normalize import deroll, normalize_scale

SYMMETRIC_TOL = 0.02  # below this half-width gap: "symmetric" (tune in Phase 1)
MIN_MOVE = 0.05  # total corner travel below this = noise floor, not a gesture.
DYN_REL_TOL = 0.30  # CHECK when one side moves 30%+ more than the other.
# PLACEHOLDERS: calibrate against labeled normal-smile logs. Rationale for
# relative over absolute: a big healthy smile accumulates bigger absolute
# side gaps by pure size — the honest unit is proportion, not eye-widths.


def mouth_half_widths(pts: np.ndarray) -> tuple[float, float]:
    """(left, right) horizontal corner-to-midline distances, eye widths."""
    mid_x = pts[NOSE_TIP, 0]
    left = abs(pts[MOUTH_LEFT, 0] - mid_x)
    right = abs(pts[MOUTH_RIGHT, 0] - mid_x)
    return float(left), float(right)


def corner_angles_deg(pts: np.ndarray) -> tuple[float, float]:
    """(left, right) deviation angles of corner-to-nose vectors from the
    vertical, in degrees. Mirrored in a symmetric smile."""
    nose = pts[NOSE_TIP, :2]
    out = []
    for corner in (MOUTH_LEFT, MOUTH_RIGHT):
        v = pts[corner, :2] - nose
        out.append(float(np.degrees(np.arctan2(abs(v[0]), -v[1]))))
    return out[0], out[1]


def smile_index(pts: np.ndarray) -> dict:
    """Full decomposition for one normalized mesh."""
    left, right = mouth_half_widths(pts)
    ang_l, ang_r = corner_angles_deg(pts)
    gap = abs(left - right)
    weaker = "left" if left < right else "right" if right < left else "symmetric"
    return {
        "left": round(left, 4),
        "right": round(right, 4),
        "asymmetry": round(gap, 4),
        "angle_left_deg": round(ang_l, 2),
        "angle_right_deg": round(ang_r, 2),
        "angle_diff_deg": round(abs(ang_l - ang_r), 2),
        "weaker_side": "symmetric" if gap < SYMMETRIC_TOL else weaker,
    }


def gesture_score(smile: dict, rest: dict) -> float:
    """The clinical signal: smile asymmetry MINUS rest asymmetry."""
    return round(smile["asymmetry"] - rest["asymmetry"], 4)


def dynamic_asymmetry(smile_pts: np.ndarray, rest_pts: np.ndarray) -> dict:
    """Per-side movement comparison: how far each corner TRAVELED from its
    own rest position, then the difference between sides.

    Static index asks "is the mouth asymmetric NOW" (confounded by natural
    rest asymmetry + pose). Dynamic asks "did both sides RESPOND equally" —
    the actual palsy signal. Both inputs must be normalized meshes.
    """
    move_l = float(np.linalg.norm(smile_pts[MOUTH_LEFT, :2] - rest_pts[MOUTH_LEFT, :2]))
    move_r = float(np.linalg.norm(smile_pts[MOUTH_RIGHT, :2] - rest_pts[MOUTH_RIGHT, :2]))
    gap = abs(move_l - move_r)
    total = move_l + move_r
    # Proportional asymmetry: comparable across small and big smiles.
    # Guarded by MIN_MOVE — near rest, ratios explode on noise.
    dyn_rel = (gap / total) if total >= MIN_MOVE else 0.0
    status = "OK" if dyn_rel < DYN_REL_TOL else "CHECK"
    return {
        "move_left": round(move_l, 4),
        "move_right": round(move_r, 4),
        "dynamic": round(gap, 4),
        "dyn_rel": round(dyn_rel, 4),
        "status": status,
    }


def build_rest_index(meshes: list[np.ndarray]) -> dict:
    """Rest baseline from RAW meshes, normalized exactly like live frames
    (scale + deroll, no yaw gate — rest assumes a still, frontal subject).
    Fixes the raw-vs-normalized mismatch: a rest built on pixels cannot be
    subtracted from a live index built on eye-widths."""
    normed = [normalize_scale(deroll(m)) for m in meshes]
    mean_rest = np.mean(np.stack(normed), axis=0)
    return smile_index(mean_rest)

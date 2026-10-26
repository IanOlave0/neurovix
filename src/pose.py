"""Rest-referenced 2D pose alignment (risk R4 redesign).

Why this exists: gates alone kept shrinking the usable margin, and full 3D
matrix correction was removed after evidence showed ~2x yaw amplification.
This module does neither: it estimates the rigid head motion between the
current frame and the subject's OWN rest posture, then measures the mouth
in rest coordinates.

Contract (see approved design):
    PoseAligner input: current landmarks + rest landmarks (pixel space).
    PoseAligner output: aligned landmarks + pose quality (alignment RMSE).

Design rules:
- Stable points are rigid upper-face anatomy ONLY: four eye corners + nose
  tip. The chin/jaw is deliberately excluded because it moves with mouth
  gestures; including it would let the alignment absorb the signal.
- mouth points never participate in estimating the transform, so an
  asymmetric gesture cannot be "aligned away".
- 2D similarity (translation + rotation + uniform scale) is enough for
  small/moderate motion. When the residual is large, the frame is declared
  pose-limited instead of producing a false CHECK.
"""

import numpy as np

from src.landmarks import (
    LEFT_EYE_INNER,
    LEFT_EYE_OUTER,
    NOSE_TIP,
    RIGHT_EYE_INNER,
    RIGHT_EYE_OUTER,
)
from src.normalize import interocular

STABLE_POINTS = (
    LEFT_EYE_OUTER,
    LEFT_EYE_INNER,
    RIGHT_EYE_INNER,
    RIGHT_EYE_OUTER,
    NOSE_TIP,
)

ALIGN_RESID_TOL = 0.12  # eye-width RMSE on stable points above this means
# the 2D similarity no longer explains the head motion (strong yaw/pitch or
# bad landmarks): declare pose-limited instead of scoring. PLACEHOLDER:
# calibrate against labeled logs; chosen lenient to restore margin while
# the residual itself is now logged for evidence.


def estimate_similarity(src_xy: np.ndarray, dst_xy: np.ndarray):
    """Least-squares 2D similarity mapping src -> dst (Umeyama/Kabsch).

    Returns (scale, rotation_2x2, translation, rmse) where
    aligned ≈ scale * (src @ rotation) + translation.
    """
    src = np.asarray(src_xy, dtype=float)
    dst = np.asarray(dst_xy, dtype=float)
    if src.shape != dst.shape or src.shape[0] < 3 or src.shape[1] != 2:
        raise ValueError("need >=3 matched 2D point pairs")
    mux = src.mean(axis=0)
    muy = dst.mean(axis=0)
    src_c = src - mux
    dst_c = dst - muy
    var = float(np.sum(src_c ** 2))
    if var < 1e-12:
        raise ValueError("degenerate source points: no extent")
    h = src_c.T @ dst_c
    u, s, vt = np.linalg.svd(h)
    # Row-vector convention: we minimize ||src @ R - dst||, so with H = U S Vt
    # the optimal rotation is R = U D Vt (transpose of the column-vector form).
    d = float(np.linalg.det(u @ vt))
    d = 1.0 if d == 0.0 else np.sign(d)
    rot = u @ np.diag([1.0, d]) @ vt
    scale = float(np.sum(s * np.array([1.0, d])) / var)
    t = muy - scale * (mux @ rot)
    fitted = scale * (src @ rot) + t
    rmse = float(np.sqrt(np.mean(np.sum((fitted - dst) ** 2, axis=1))))
    return scale, rot, t, rmse


def align_to_rest(current_pts: np.ndarray, rest_pts: np.ndarray):
    """Align a full current mesh to the rest reference via stable points.

    Returns (aligned_full_points, rmse_eye_widths, transform_dict).
    Only x, y are transformed; z is carried through untouched because the
    dynamic metric uses x, y. Units: input pixels in, pixel-aligned out;
    callers divide by rest interocular for eye-width metrics.
    """
    current = np.asarray(current_pts, dtype=float)
    rest = np.asarray(rest_pts, dtype=float)
    stable = np.asarray(STABLE_POINTS, dtype=int)
    scale, rot, t, rmse_px = estimate_similarity(
        current[stable, :2], rest[stable, :2]
    )
    aligned = current.copy()
    aligned[:, :2] = scale * (current[:, :2] @ rot) + t
    unit = interocular(rest)
    if unit < 1e-9:
        raise ValueError("degenerate rest reference: eyes coincide")
    rmse_ew = rmse_px / unit
    return aligned.astype(np.float32), rmse_ew, {
        "scale": scale,
        "rotation": rot,
        "translation": t,
        "rmse_px": rmse_px,
    }

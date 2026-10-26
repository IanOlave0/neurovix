"""Controlled pixel-space deformation for R7 validation (risk R7).

R7 asks: does the landmarker FOLLOW real facial asymmetry, or snap back
to a symmetric prior (Kimura F5)? Moving landmark POINTS by hand cannot
answer this — it bypasses the detector. This module deforms the IMAGE
(pixels) with a known smooth field, so re-running the detector measures
detection itself.

Field: gaussian bump centered on a mouth corner, pulling toward the
facial midline (mimics the shortened half-width of a droop):
    D(p) = A * dir * exp(-|p - c|^2 / 2s^2)
Content at p moves to p + D(p). Expected landmark shift = D evaluated at
the BASELINE landmark position — no detector involved, pure math.
"""

import cv2
import numpy as np


def displacement_at(points_xy: np.ndarray, center_xy: np.ndarray,
                    sigma_px: float, direction_xy: np.ndarray,
                    amplitude_px: float) -> np.ndarray:
    """Expected shift D(p) for each point. A=0 -> zero everywhere."""
    p = np.asarray(points_xy, dtype=float)
    c = np.asarray(center_xy, dtype=float)
    d = np.asarray(direction_xy, dtype=float)
    n = float(np.linalg.norm(d))
    if n == 0:
        raise ValueError("direction must be non-zero")
    d = d / n
    dist2 = np.sum((p - c) ** 2, axis=-1, keepdims=True)
    w = np.exp(-dist2 / (2.0 * sigma_px ** 2))
    return (amplitude_px * w) * d


def apply_warp(frame_bgr: np.ndarray, center_xy: np.ndarray,
               sigma_px: float, direction_xy: np.ndarray,
               amplitude_px: float) -> np.ndarray:
    """Remap the frame so content at p moves to p + D(p).

    First-order inverse map (exact for smooth small fields): sample the
    source at (x - Dx, y - Dy). Identity when amplitude is 0.
    """
    h, w = frame_bgr.shape[:2]
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32),
                         np.arange(h, dtype=np.float32))
    grid = np.stack([xs, ys], axis=-1)
    disp = displacement_at(grid, np.asarray(center_xy, dtype=float),
                           sigma_px, direction_xy, amplitude_px)
    map_x = (grid[..., 0] - disp[..., 0]).astype(np.float32)
    map_y = (grid[..., 1] - disp[..., 1]).astype(np.float32)
    return cv2.remap(frame_bgr, map_x, map_y, cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_REPLICATE)

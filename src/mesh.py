"""Face mesh extraction: Tasks FaceLandmarker in VIDEO mode.

Design contract (see docs/protocol.md, section 3.1, and risk R7):
- Output is a (478, 3) float32 array of NORMALIZED landmarks (x, y in
  [0, 1], z in the same scale) or None when no face is detected.
- The first 468 points keep the canonical FaceMesh topology, so every index
  in `landmarks.py` stays valid; the last 10 are iris points we ignore.
- VIDEO mode requires monotonically increasing timestamps in ms. We feed it
  the real capture timestamps (the jitter lesson from `capture.py`): a slow
  frame arrives with a larger gap, which is the truth — plus a +1 ms guard
  so two frames never share a timestamp and violate the contract.
- No-face is a normal outcome, not an error: empty room, occlusions, head
  out of frame. Callers must handle None (protocol section 3.3).
- Lifecycle: create once, call `.close()` at the end. Never rely on the
  garbage collector — interpreter-teardown ordering breaks the internal
  dispatcher (same discipline as `cap.release()`).

Model file: `models/face_landmarker.task` (downloaded once, git-ignored —
regenerable artifact, see .gitignore):
https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
"""

from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"
MESH_POINTS = 478  # 468 canonical FaceMesh + 10 iris


def create_landmarker(model_path: Path = MODEL_PATH) -> vision.FaceLandmarker:
    """Build the landmarker or fail loudly (missing model = setup error,
    not a runtime condition to swallow)."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"missing model {model_path} — download it (see module docstring)"
        )
    base = mp.tasks.BaseOptions(model_asset_path=str(model_path))
    options = vision.FaceLandmarkerOptions(
        base_options=base,
        running_mode=vision.RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        # The 4x4 pose matrix is OFF by default — without this flag there is
        # no 3D frontalization data at all (verified in installed source).
        output_facial_transformation_matrixes=True,
    )
    return vision.FaceLandmarker.create_from_options(options)


def extract_with_matrix(frame_bgr: np.ndarray,
                        landmarker: vision.FaceLandmarker,
                        timestamp_ms: int) -> tuple[np.ndarray | None, np.ndarray | None]:
    """Same as extract_landmarks plus the 4x4 facial pose matrix
    (row-major ndarray) or (None, None) when no face is detected."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect_for_video(image, timestamp_ms)
    if not result.face_landmarks:
        return None, None
    pts = np.array(
        [(lm.x, lm.y, lm.z) for lm in result.face_landmarks[0]],
        dtype=np.float32,
    )
    assert pts.shape == (MESH_POINTS, 3), f"topology changed: {pts.shape}"
    matrix = result.facial_transformation_matrixes[0] \
        if result.facial_transformation_matrixes else None
    return pts, matrix


def extract_landmarks(frame_bgr: np.ndarray,
                      landmarker: vision.FaceLandmarker,
                      timestamp_ms: int) -> np.ndarray | None:
    """One BGR frame + its capture timestamp -> (478, 3) or None."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect_for_video(image, timestamp_ms)
    if not result.face_landmarks:
        return None
    pts = np.array(
        [(lm.x, lm.y, lm.z) for lm in result.face_landmarks[0]],
        dtype=np.float32,
    )
    assert pts.shape == (MESH_POINTS, 3), f"topology changed: {pts.shape}"
    return pts

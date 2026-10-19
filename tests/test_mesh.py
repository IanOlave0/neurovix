"""Mesh extraction contract (no camera needed for the blank case).

A blank frame contains no face, so the landmarker must return None —
never crash, never hallucinate points. Requires the model file; skips
cleanly on a fresh clone without it (tests must pass everywhere).
"""

import numpy as np
import pytest

from src.mesh import MODEL_PATH, create_landmarker, extract_landmarks


@pytest.fixture(scope="module")
def landmarker():
    if not MODEL_PATH.exists():
        pytest.skip("model file not downloaded (see src/mesh.py docstring)")
    return create_landmarker()


def test_blank_frame_yields_no_face(landmarker):
    blank = np.zeros((480, 640, 3), dtype=np.uint8)
    assert extract_landmarks(blank, landmarker, timestamp_ms=0) is None


def test_missing_model_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError):
        create_landmarker(tmp_path / "nope.task")

"""Landmark-module safety net (risk R7).

These tests need no camera: they check topology invariants.
If a `mediapipe` upgrade moves the indices, THIS fails first —
not the clinical pipeline.
"""

from src.landmarks import EYES, MOUTH, N_LANDMARKS, validate_indices


def test_full_mesh():
    assert N_LANDMARKS == 468


def test_indices_in_range_without_duplicates():
    validate_indices()  # raises AssertionError with details


def test_symmetric_groups():
    # Each side contributes the same number of points: measured asymmetry
    # must come from the face, not from a lopsided group definition.
    assert len([k for k in EYES if k.startswith("left")]) == len(
        [k for k in EYES if k.startswith("right")]
    )
    assert len([k for k in MOUTH if "left" in k or "right" in k]) == 2


def test_eyes_and_mouth_do_not_overlap():
    assert not set(EYES.values()) & set(MOUTH.values())

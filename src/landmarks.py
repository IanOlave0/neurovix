"""MediaPipe FaceMesh landmark groups used by NeuroVix.

Deliberate design (see docs/protocol.md, section 3.1, and risk R7):
- Indices live HERE as named constants, never as magic numbers scattered
  through the code. If MediaPipe changes the topology across versions,
  there is exactly ONE file to audit.
- `validate_indices()` is the safety net: any dependency upgrade that moves
  an index breaks the tests, not the clinical pipeline.

Canonical FaceMesh-topology indices (468 points), verified against the mesh
documentation. The Tasks FaceLandmarker used in `mesh.py` returns 478
points whose first 468 keep this exact topology (last 10 are iris), so
every constant below stays valid. When upgrading `mediapipe`, revalidate
this module by running the suite: `pytest tests/ -v`.
"""

N_LANDMARKS = 468

# Nose tip (facial-midline-axis reference).
NOSE_TIP = 1
# Chin (lower contour).
CHIN = 152

# Eyes: outer and inner corners per side.
# The interocular distance derived from these points is the scale
# normalization unit (protocol, section 3.2).
LEFT_EYE_OUTER = 33
LEFT_EYE_INNER = 133
RIGHT_EYE_INNER = 362
RIGHT_EYE_OUTER = 263

# Mouth: corners and lip centers (smile / teeth-baring gesture).
MOUTH_LEFT = 61
MOUTH_RIGHT = 291
UPPER_LIP = 13
LOWER_LIP = 14

EYES = {
    "left_outer": LEFT_EYE_OUTER,
    "left_inner": LEFT_EYE_INNER,
    "right_inner": RIGHT_EYE_INNER,
    "right_outer": RIGHT_EYE_OUTER,
}

MOUTH = {
    "left_corner": MOUTH_LEFT,
    "right_corner": MOUTH_RIGHT,
    "upper_lip": UPPER_LIP,
    "lower_lip": LOWER_LIP,
}

# TODO(Phase 1): eyebrow and contour groups for the eyebrow-raising gesture
# (central vs. peripheral discrimination, hypothesis H2).


def validate_indices() -> None:
    """Fail fast if any index falls outside the mesh range."""
    all_indices = [NOSE_TIP, CHIN, *EYES.values(), *MOUTH.values()]
    assert len(all_indices) == len(set(all_indices)), "duplicate indices in landmarks.py"
    out = [i for i in all_indices if not 0 <= i < N_LANDMARKS]
    assert not out, f"indices out of range [0, {N_LANDMARKS}): {out}"

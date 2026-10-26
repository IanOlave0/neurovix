# NeuroVix

> Quantitative neurological biomarker from any device camera: early stroke
> triage support through facial asymmetry detection.

**Status:** Phase 1 — Geometric MVP (complete)

## Problem

- Stroke is the leading cause of adult disability in Mexico and Latin America.
- Every untreated minute destroys ~1.9 million neurons (Saver, 2006 — *"Time is Brain"*).
- Bottleneck: in emergencies, subtle facial asymmetries make paramedics, primary-care staff, and families hesitate, delaying hospital transfer inside the golden hour.

## Solution

Turn the front camera of any phone, tablet, or laptop into an objective biomarker:

1. **Live capture** of the patient's face
2. **3D landmarking** with MediaPipe Face Landmarker (478-pt topology)
3. **Kinematic-dynamic metrics**: angular deviation, vector asymmetry, gesture velocity, inter-hemispheric onset lag
4. **Objective Facial Palsy Index** (interpretable)
5. **Copilot recommendation** — never an autonomous decision

## Design principles (non-negotiable)

| Principle | Implication |
|---|---|
| **Copilot, not judge** | Never output "no stroke". Deliberate false-positive bias. The human decides. |
| **100% on-device** | Video never leaves the device. Privacy by design. |
| **Interpretable core first** | Defensible geometric index before any classifier. ML is a v2 layer. |
| **Clinical grounding** | Clinically motivated gestures: a spared forehead points to central vs. peripheral palsy. |

## Stack

- **Capture / landmarks:** Python · OpenCV · MediaPipe FaceMesh
- **Features:** NumPy / SciPy (3D vector geometry, scale and pose normalization)
- **ML (Phase 2):** Scikit-learn / XGBoost
- **Deployment (Phase 3+):** ONNX / TFLite

## Repo structure

```
neurovix/
├── README.md
├── requirements.txt     # Pinned environment (see Setup below)
├── src/
│   ├── capture.py       # Camera loop: real timestamps + rest baseline
│   ├── mesh.py          # FaceLandmarker VIDEO mode -> pixel-space mesh
│   ├── landmarks.py     # Documented index constants + validation (R7 net)
│   ├── normalize.py     # Scale + rest-referenced pose gates (R4)
│   ├── pose.py          # Rest-referenced 2D alignment backend
│   ├── index.py         # Interpretable static + proportional dynamic index
│   ├── warp.py          # Controlled pixel deformation (R7 experiment)
│   └── demo.py          # Live demo: overlay + metrics + per-frame CSV logs
├── scripts/
│   └── r7_validate.py   # R7 follow-through experiment
├── tests/               # pytest suite (36 tests)
└── docs/
    ├── roadmap.md       # Phases, deliverables, acceptance criteria
    ├── protocol.md      # Experimental design: question, features, evaluation
    ├── risks.md         # Risk analysis with evidence
    ├── literature.md    # Literature survey (9 notes) + confirmed gaps
    └── experiments/     # Reproducible experiment reports (no face images)
```

## Setup (reproducible)

Requirements: Python 3.11 (via `uv`), a webcam, ~100 MB disk.

```bash
git clone https://github.com/IanOlave0/neurovix.git
cd neurovix
uv venv --python 3.11
uv pip install --python .venv/bin/python -r requirements.txt
mkdir -p models
curl -sL -o models/face_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
.venv/bin/python -m pytest tests/   # expect: all passing
.venv/bin/python -m src.demo        # live window (q=quit, r=rest baseline)
```

Notes:

- `models/` is git-ignored by design (regenerable artifact; biometric data
  is never versioned). The model URL also lives in `src/mesh.py`.
- `runs/` (per-frame CSV logs) and `data/` (experiment captures) are local
  only and never committed.
- See `docs/roadmap.md` for phases and acceptance criteria.

## Medical disclaimer

This project is research and education. **It is not a medical device, does
not diagnose, and does not replace professional care.** At any sign of
stroke, call emergency services immediately.

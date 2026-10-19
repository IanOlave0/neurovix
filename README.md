# NeuroVix

> Quantitative neurological biomarker from any device camera: early stroke
> triage support through facial asymmetry detection.

**Status:** Phase 1 — Geometric MVP (in progress)

## Problem

- Stroke is the leading cause of adult disability in Mexico and Latin America.
- Every untreated minute destroys ~1.9 million neurons (Saver, 2006 — *"Time is Brain"*).
- Bottleneck: in emergencies, subtle facial asymmetries make paramedics, primary-care staff, and families hesitate, delaying hospital transfer inside the golden hour.

## Solution

Turn the front camera of any phone, tablet, or laptop into an objective biomarker:

1. **Live capture** of the patient's face
2. **3D landmarking** with MediaPipe FaceMesh
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
├── requirements.txt     # Pinned environment (see setup below)
├── src/
│   ├── __init__.py
│   └── landmarks.py     # Documented FaceMesh index constants + validation
├── tests/               # pytest suite (topology safety net, risk R7)
└── docs/
    ├── roadmap.md       # Phases, deliverables, acceptance criteria
    ├── protocol.md      # Experimental design: question, features, evaluation
    ├── risks.md         # Risk analysis with evidence
    └── literature.md    # Literature survey (9 notes) + confirmed gaps
```

Setup: Python 3.11 via `uv` (`uv venv --python 3.11`), then install
`requirements.txt`. See `docs/roadmap.md` (Phase 0) for the full trail.

## Medical disclaimer

This project is research and education. **It is not a medical device, does
not diagnose, and does not replace professional care.** At any sign of
stroke, call emergency services immediately.

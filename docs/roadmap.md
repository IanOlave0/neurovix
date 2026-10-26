# Project roadmap — NeuroVix

> Phases, deliverables, and acceptance criteria.

## Goal

1. **Product:** on-device support tool for early stroke triage through facial
   asymmetry quantification. No special hardware.
2. **Research:** publishable artifact (preprint + reproducible public repo)
   answering the question in [protocol.md](protocol.md).

## Roadmap

| Phase | Status | Deliverable | Acceptance |
|---|---|---|---|
| 0. Planning and literature | Done | Study protocol, literature survey (9 notes), reproducible setup | protocol.md, literature.md, pinned env + 4/4 tests |
| 1. Geometric MVP | Done | Live demo + interpretable asymmetry index | Real-time on laptop; synthetic-asymmetry follow-through quantified; behavior on asymmetric faces documented |
| 2. Experimental protocol | Planned | Rigorous evaluation + results | Reproducible results table with metrics, ablations, error analysis |
| 3. Writing and publication | Planned | Preprint + public repo | Public PDF + reproducible repo |

## Phase 0 — Planning and literature

- [x] Design decisions (copilot, edge, interpretable geometric core)
- [x] Study protocol ([protocol.md](protocol.md))
- [x] Systematic literature sweep + related work (9 notes in [literature.md](literature.md); data and novelty gaps confirmed)
- [x] Reproducible setup (public repo, pinned environment, 4/4 tests)

## Phase 1 — Geometric MVP

- [x] Stable capture pipeline (OpenCV + MediaPipe Face Landmarker, real per-frame timestamps)
- [x] Landmark module with documented indices (`landmarks.py`, 478-pt topology)
- [x] Normalization: scale (interocular) and pose gates (roll/yaw, rest-referenced) + rest-aligned measurement backend (`pose.py`)
- [x] Per-session rest baseline (rest meshes, `rest_roll`, `rest_yaw`)
- [x] Gesture: smile → interpretable asymmetry index (static + proportional dynamic)
- [x] Live demo: mesh overlay + real-time metrics (`demo.py`, per-frame CSV logging)
- [x] **Robustness R7:** landmark follow-through under controlled synthetic pixel asymmetry (`docs/experiments/r7-landmark-robustness.md`)

**Acceptance:** the demo runs in real time on a laptop, quantifies
controlled induced asymmetry, and documents its behavior on asymmetric faces.

## Phase 2 — Experimental protocol

- [ ] Temporal kinematic features (velocity, onset lag, profiles)
- [ ] Additional gestures: teeth-baring, eyebrow-raising
- [ ] Data strategy implemented (synthesis + proxy search)
- [ ] Evaluation: per-subject splits, sens@spec, AUC with CI
- [ ] Baseline ladder and ablations
- [ ] False-negative error analysis
- [ ] **Milestone:** preliminary results before the writing phase

**Acceptance:** reproducible results table with metrics, ablations, and error analysis.

## Phase 3 — Writing and publication

- [ ] Preprint in English (arXiv format)
- [ ] English README + tests + reproducibility (seeds, versions)
- [ ] Target venue (LatinX in AI @ NeurIPS · ML4H · IEEE EMBC student track)

**Acceptance:** public PDF + reproducible repo.

## Backlog (post-v1)

- ML classifier as product layer (if the evidence justifies it)
- Mobile packaging (ONNX / TFLite)
- Full FAST scale (speech, arm weakness)
- Formal clinical validation (requires ethical protocol and hospital)
- Pre/post-thrombolysis comparison mode

## Active risks

See [risks.md](risks.md). The design-driving risks: R1 (data),
R2 (error tolerance), R7 (landmark degradation on asymmetric faces).

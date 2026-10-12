# Project roadmap — NeuroVix

> Phases, deliverables, and acceptance criteria.

## Goal

1. **Product:** on-device support tool for early stroke triage through facial
   asymmetry quantification. No special hardware.
2. **Research:** publishable artifact (preprint + reproducible public repo)
   answering the question in [protocolo.md](protocolo.md).

## Roadmap

| Phase | Status | Deliverable | Acceptance |
|---|---|---|---|
| 0. Planning and literature | Done | Study protocol, literature survey (9 notes), reproducible setup | protocolo.md, literatura.md, pinned env + 4/4 tests |
| 1. Geometric MVP | In progress | Live demo + interpretable asymmetry index | Real-time on laptop; quantified induced asymmetry; documented behavior on asymmetric faces |
| 2. Experimental protocol | Planned | Rigorous evaluation + results | Reproducible results table with metrics, ablations, error analysis |
| 3. Writing and publication | Planned | Preprint + public repo | Public PDF + reproducible repo |

## Phase 0 — Planning and literature

- [x] Design decisions (copilot, edge, interpretable geometric core)
- [x] Study protocol ([protocolo.md](protocolo.md))
- [x] Systematic literature sweep + related work (9 notes in [literatura.md](literatura.md); data and novelty gaps confirmed)
- [x] Reproducible setup (public repo, pinned environment, 4/4 tests)

## Phase 1 — Geometric MVP

- [ ] Stable capture pipeline (OpenCV + MediaPipe FaceMesh)
- [ ] Landmark module with documented indices (`landmarks.py`)
- [ ] Normalization: scale (interocular) and pose (roll/yaw)
- [ ] Per-session rest baseline
- [ ] Gesture: smile → interpretable asymmetry index
- [ ] Live demo: mesh overlay + real-time metrics
- [ ] **Robustness R7:** landmark stability check under controlled synthetic asymmetry

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

See [riesgos.md](riesgos.md). The design-driving risks: R1 (data),
R2 (error tolerance), R7 (landmark degradation on asymmetric faces).

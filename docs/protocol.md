# Experimental protocol — NeuroVix

> Study design turning the MVP into a research artifact. Version 0.1 (living document).
> Prior-art survey: `literature.md`.

## 1. Research question

**RQ:** To what extent do temporal kinematic features (gesture velocity,
inter-hemispheric onset lag, movement-profile symmetry) improve unilateral
facial palsy discrimination over static asymmetry metrics?

**Hypotheses:**

- **H1:** The model with kinematic features beats the static model (ΔAUC > 0) under per-subject validation.
- **H2:** The eyebrow-raising gesture distinguishes central (spared forehead) from peripheral impairment.
- **H3 (exploratory):** Inter-hemispheric onset lag is the single most discriminative feature.

## 2. Operational definitions

- **Healthy control subject:** no history of facial palsy or neurological syndromes.
- **Induced asymmetry (synthesis):** controlled deformation of one hemisphere's landmarks at documented intensity. Used for sensitivity testing — **not** clinical ground truth.
- **Baseline:** the subject's own rest capture at the start of each session; every gesture feature is expressed as a delta against rest.

## 3. Features

### 3.1 Landmarks (groups of interest)

| Group | Structure | Use |
|---|---|---|
| Mouth corners | mouth corners, upper/lower lip | Smile / teeth-baring asymmetry |
| Eyebrows | mid and outer points | Central vs. peripheral |
| Eyes | corners, eyelids | Scale normalization (interocular) |
| Facial contour | chin, cheeks | Pose normalization |

> Technical note: pin the exact MediaPipe FaceMesh indices in a `landmarks.py`
> module as documented constants (indices change across versions).
> Implementation uses the Tasks FaceLandmarker in VIDEO mode; its first 468
> points keep the FaceMesh topology (see `src/mesh.py`).

### 3.2 Feature families

**Static (per frame):**

- Euclidean distances between contralateral pairs, normalized by interocular distance
- Mouth-corner deviation angles against the facial midline axis
- Triangular areas of facial regions (orbit, mouth)

**Kinematic (per gesture):**

- Per-point velocity: `v_i(t) = ||p_i(t+Δt) − p_i(t)|| / Δt`
- Inter-hemispheric onset lag: max-cross-correlation lag between left and right displacement series
- Profile symmetry: peak-velocity and movement-duration differences between sides
- Per-side gesture amplitude (max displacement)

**Normalizations:**

- Scale: interocular distance (or facial width)
- Pose: gates only, no geometric correction. Yaw gate from the pose
  matrix in real degrees when available (proxy fallback); roll gate with
  an absolute outer guard plus excursion relative to the subject's own
  rest posture. Correction was tried and removed (evidence: 2x yaw
  amplification); see risks.md R4.
- Temporal: gesture-onset alignment by movement threshold

### 3.3 Exclusions

- No *z* coordinate as a primary feature without validating its stability (noisy monocular depth).
- Drop frames with out-of-range pose (yaw/roll above threshold) or occlusions (hands, glasses).

## 4. Data strategy

| Source | State | Use | Explicit limitation |
|---|---|---|---|
| Landmark-deformation synthesis | To be implemented | Sensitivity testing, calibration | A "deformed actor" does not reproduce patient kinematics |
| Bell's palsy proxy (public datasets) | To be sourced | Domain signal, cross-validation | Bell's is peripheral; not equivalent to central stroke |
| Clinical collaboration | Future work | External validation | Timelines, ethics, permissions |
| Developer-recorded sessions (with consent) | Available | Development and sanity checks | Not clinical evidence |

**Future direction:** motion-preserving de-identification (SafeTriage,
arXiv:2506.16578) as a mechanism for sharing facial kinematics without
exposing identities — see `literature.md` (F6).

### Detector robustness validation (R7, done Oct 2026)

Reproducible procedure (`scripts/r7_validate.py`, report in
`docs/experiments/r7-landmark-robustness.md`): capture neutral frames,
apply a known Gaussian pixel-space pull (0/6/12/20 px) on each mouth
corner toward the midline, re-run the detector, and report the follow
ratio (detected vs. expected displacement) with an amplitude-0 noise
control, fresh detector per frame, and seeded-shuffled amplitude order.
Result: 80/80 faces tracked, ~75–90% follow-through at 12–20 px, no
directional failure; ~1–1.4 px re-detection jitter floor. Synthetic,
single-subject evidence — not clinical validity.

**Rule:** every result declares its data source and what **cannot** be claimed from it.

## 5. Evaluation protocol

**Unit of analysis:** subject (not frame). **Per-subject splits** (GroupKFold) — never random per-frame splits (identity leakage).

**Primary metrics:**

- Sensitivity at fixed 90% specificity (triage metric)
- ROC AUC with 95% CI via subject-grouped bootstrap
- Calibration (reliability curve)

**Baseline ladder (ablation):**

1. Simple geometric rule (static-asymmetry threshold)
2. ML on static features
3. ML on static + kinematic features ← proposal
4. (Optional) Sequential temporal model as ceiling, if the data justifies it

**Error analysis:** false-negative characterization. In triage, the FN is the critical error.

**Reproducibility:** fixed seeds, dependency versions, single evaluation script.

## 6. Ethics and privacy

- 100% on-device processing; no video or landmark leaves the device.
- Informed consent for any recording used in development.
- Output is never "no stroke": an index plus a referral recommendation (copilot).
- No diagnostic use on real people until formal clinical validation.

## 7. Threats to validity

| Threat | Type | Mitigation |
|---|---|---|
| Synthesis ≠ real pathology | Construct | Declare it explicitly; seek clinical proxy |
| Bell's ≠ stroke | External | Limit conclusions to peripheral palsy where applicable |
| Capture confounders (light, pose, camera) | Internal | Normalization + exclusions + subgroup analysis |
| Extreme class imbalance | Statistical | Robust metrics (sens@spec, AUC), weighting |
| Multiple comparisons in ablations | Statistical | Pre-register the comparison ladder |

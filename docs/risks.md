# Risk analysis — NeuroVix

> Risks affecting scientific validity, safety, and reproducibility, with
> mitigations and evidence. Updated 2026-10-11.

## Risk summary (for evaluators)

- **R1 — No clinical data.** The design needs no training data (interpretable
  geometric core); classifiers are a v2 layer over synthesis + proxy data.
  Evidence: `protocol.md` §4.
- **R2 — False negatives cause false reassurance.** Copilot-only output,
  deliberately biased toward false positives; the human decides.
  Evidence: `protocol.md` §6.
- **R7 — Landmark degradation on asymmetric faces.** Preliminarily
  mitigated by synthetic image-level validation (60–80/80 faces tracked,
  ~75–90% follow-through, no directional failure); documented limits;
  fine-tuning and clinical validation remain open.
  Evidence: `docs/experiments/r7-landmark-robustness.md`,
  `scripts/r7_validate.py`, `src/landmarks.py`, `tests/`,
  `literature.md` (note F5).
- **R4 — Pose and lighting confounders.** Scale/pose normalization plus frame
  exclusions. Evidence: `protocol.md` §§3.2–3.3.
- **R6 — Regulatory scope.** Research framing; no clinical use, no diagnostic
  claims, visible disclaimer. Evidence: README, `protocol.md` §6.
- **R3 — "MediaPipe wrapper" perception.** Temporal kinematic features plus
  ablations plus mapped prior art (chronic peripheral palsy; no acute
  prehospital triage). Evidence: `literature.md` (9 notes), `protocol.md` §5.

## Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Evidence | Status |
|---|---|---|---|---|---|---|
| R1 | No clinical data available | High | High | Training-free core + controlled synthesis + proxy data; never claim beyond the data source | protocol.md §4 | Mitigated by design |
| R2 | False negative causes false reassurance | Medium | Very high | Copilot output + false-positive bias + disclaimers; never output "no stroke" | protocol.md §6 | Mitigated by design |
| R3 | Perceived as a "MediaPipe wrapper" | Medium | High | Kinematic features + ablations + literature survey | literature.md; protocol.md §5 | In mitigation (Phase 2) |
| R4 | Pose/lighting confounders | High | Medium | Normalization + exclusions | protocol.md §§3.2–3.3 | Open — closes with documented thresholds + tests (Phase 1) |
| R5 | Scope creep (features/gestures) | High | Medium | Phases with acceptance criteria; MVP first | roadmap.md | Controlled |
| R6 | Regulatory exposure if framed as diagnosis | Medium | High | Research/education framing; no clinical use | README disclaimer; protocol.md §6 | Mitigated by design |
| R7 | Landmark degradation on asymmetric faces (models trained on healthy faces) | High | High | Synthetic image-level validation + documented limits; fine-tuning and clinical validation as follow-ups | docs/experiments/r7-landmark-robustness.md; scripts/r7_validate.py; src/landmarks.py; tests/; literature.md (F5) | Preliminarily mitigated (Oct 2026); clinical/multi-subject validation open |

## Appendix: viability assessment (internal framework)

The table below is the internal 6-test framework that drove the design
decisions above (geometric-first core, copilot framing, edge deployment).
Kept for traceability; it is not the evaluation contract.

| Test | Verdict | Rationale |
|---|---|---|
| 1. Build feasibility | [OK] Strong pass | Geometric MVP in 2–3 weeks; CPU-only; pretrained models |
| 2. Usability and adoption | [OK] Strong pass | Clear users; no special hardware; interactive demo; regulatory caveat |
| 3. Competition and novelty | [Watch] Pass with caveats | Prior art exists; differentiation: temporal kinematics + prehospital triage + edge LATAM + central vs. peripheral |
| 4. Data | [Critical] Critical risk | No public dataset of acute stroke facial palsy with gestures |
| 5. Error tolerance | [Watch] High risk, mitigable | Lethal-false-negative category — requires copilot design |
| 6. Economics | [OK] Strong pass | Edge inference ~$0; golden-hour ROI |

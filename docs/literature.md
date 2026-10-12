# Literature review — NeuroVix (Phase 0)

> Systematic sweep, Oct 2026, via paper-search MCP (PubMed, arXiv, medRxiv).
> Inclusion criterion: automated facial asymmetry/palsy quantification with
> landmarks, video-based stroke triage, or transferable methods (geometric
> features, temporal dynamics, clinical-video privacy).

## Search log (method trail)

| Source | Queries | Outcome |
|---|---|---|
| PubMed | "automated facial palsy detection facial landmarks" | 5 relevant hits (clinical core) |
| PubMed | "prehospital stroke triage facial video computer vision", "automated Cincinnati stroke scale facial droop detection", "facial palsy dataset video landmarks" | Empty — queries too specific for keyword indexing |
| PubMed | "stroke facial video", "stroke triage artificial intelligence" | Noise (TIA clinics, hospital management) — word match, not problem match |
| arXiv | "facial palsy detection facial landmarks", "stroke detection facial asymmetry video", "MediaPipe face mesh facial analysis" | 2 direct hits + 3 methodological; rest noise (deepfakes, animatronics, MRI) |
| medRxiv | "facial palsy detection video", "stroke face video triage" | Tool ignored the queries (returned unrelated results) — do not use until fixed |

## Notes

### Clinical core (automated facial palsy)

**F1. Heinrich et al. 2026 — Asymmetry angle maps in peripheral palsy.**
405 datasets from 198 patients, 9 standardized expressions, 478 landmarks →
225 pairs → 91 informative pairs (eyes, nose, mouth). 0.32–0.73 correlation
with clinical scores. Robust to head rotation.
PubMed 42072220 · doi:10.3390/bioengineering13040426
*Relevance: dense-static-asymmetry baseline; our contrast is kinematics + acute triage.*

**F2. Heinrich et al. 2025 — Deep-learning symmetry scoring (Sci Rep).**
Same cohort; difference heatmaps + 0–0.99 symmetry score. In 9% of cases the
score changed while the Stennert clinical score did not → higher sensitivity
than the human scale. −0.32 to −0.66 correlation with severity.
PubMed 40866588 · doi:10.1038/s41598-025-17172-1
*Relevance: evidence that automation can exceed clinical scales in sensitivity.*

**F3. Zhou et al. 2026 — Objective facial-paralysis evaluation system.**
Automation of FACE-gram (manual today). Frames the problem as
"subjective, inconsistent, inefficient".
PubMed 40623140 · doi:10.1097/SCS.0000000000011638
*Relevance: validates the "objectify the subjective" framing.*

**F4. Supratak et al. 2025 — Dynamic blink features (key for H1).**
103 subjects (86 healthy, 17 FNP), high-frame-rate video. Blink normality
scores via Isolation Forest: **+75% F1 over static parameters, +35% over raw
dynamic ones**. Winning feature: upper-eyelid closing velocity.
CompBiomed 2025. PubMed 39914202 · doi:10.1016/j.compbiomed.2025.109722
*Relevance: EMPIRICAL backing for H1 — velocity beats statics. Core preprint citation.*

**F5. Kimura et al. 2025 — Landmarkers fail on paretic faces (key for R7).**
68-point model trained on healthy subjects applied to 30 patients: detects
them as symmetric, misses eye closure. Requires annotation fine-tuning.
PubMed 39688730 · doi:10.1097/PRS.0000000000011924
*Relevance: EVIDENCE for risk R7. Justifies our robustness validation from Phase 1.*

### Problem space (stroke + video + privacy)

**F6. SafeTriage, Cai et al. 2025 (arXiv:2506.16578) — Stroke triage from facial video + de-identification.**
Confirms AI models detecting subtle facial-muscle coordination patterns in
emergency patient videos. Proposes motion transfer onto synthetic identities
for data sharing without exposing patients + prompt tuning for the
healthy→patient shift.
*Relevance, twofold: (a) validates the problem space is real and active;
(b) motion-preserving de-identification is a future avenue for the data
problem (R1): share kinematics without sharing faces.*

**F7. Oo et al. 2024/25 (arXiv:2405.16496) — Multimodal facial-palsy detection, N=21.**
Modality comparison: feed-forward net on *expression features* (76.22
precision) vs. ResNet on facial line segments (83.47 recall); fusion 77.05.
Landmarks + engineered features compete with CNNs.
*Relevance: small-N precedent with classical ML on features — our exact regime.*

### Methodological precedents (transferable)

**F8. Ghimire & Lee 2016 (arXiv:1604.03225) — Point/line/triangle geometric features + SVM.**
Landmark tracking in sequences, features normalized against the first frame
(per-session baseline, like ours!), AdaBoost + DTW and SVM: 95–97% on CK+.
*Relevance: the "geometry + classical ML on sequences" blueprint, with a decade of precedent.*

**F9. Praveen et al. 2021/26 (arXiv:2101.09858) — Weakly-supervised FABA review.**
Taxonomy of weak-annotation learning for in-video facial affective
analysis: the paradigm for training on scarce labeled data.
*Relevance: theoretical frame if the data avenue requires semi-supervision (Phase 2).*

### Context references (established knowledge)

- **Saver JL. 2006 — "Time is brain — quantified"** (1.9M neurons/min). Stroke 37(1):263-266.
- **INEGI EDR 2024:** 34,784 cerebrovascular deaths in Mexico (7th national cause). Bulletin 142/25.

## Confirmed gaps (our window)

1. **No public dataset of acute stroke facial palsy with gestures** (confirms R1).
2. **No prehospital Cincinnati/FAST automation with gesture kinematics** (confirms R3 differentiation).
3. **Nearly all prior art is chronic peripheral palsy**, not acute central events (bounds our claims).

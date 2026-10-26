# R7 — Landmark Robustness Under Synthetic Facial Asymmetry

> Experiment date: 2026-10-25. Reproducible via `scripts/r7_validate.py`.
> Raw face images are NOT published (privacy); method, code, and aggregate
> results are.

## Objective

Evaluate whether the facial landmarker follows asymmetric facial motion in
the image domain, rather than projecting a symmetric prior onto the face.

## Motivation

Kimura et al. (2025; `literature.md` F5) reported that a facial-landmark
model trained primarily on healthy faces could interpret paretic faces as
symmetric and fail to capture eye closure. That failure mode motivates this
experiment: it is the reason we deform IMAGES and re-run the detector,
instead of moving landmark points by hand (which would bypass detection
entirely and therefore cannot test it).

## Experimental setup

Real camera frames were captured from one subject under controlled indoor
lighting with a neutral expression. Each frame was duplicated and modified
with a smooth Gaussian pixel-space deformation centered on one mouth
corner and directed toward the facial midline (mimicking a shortened
half-width, as in a droop).

Tested amplitudes: 0 (noise-floor control), 6, 12, and 20 px.
Both left and right mouth corners were tested, 10 frames per
amplitude per side: 80 measurements total.

The detector ran again on every warped image. No landmark coordinates
were manually modified.

## Controls

- **Amplitude 0:** no deformation — measures pure re-detection jitter.
- **Fresh detector per frame:** the landmarker runs in VIDEO mode with
  temporal state, so one instance per frame prevents tracking carryover.
- **Seeded-shuffled amplitude order** (`--seed 7`): prevents order bias.
- **Synthetic warp check** (`tests/test_warp.py`): a known dot travels the
  predicted displacement, pinning the deformation math independently.

An earlier uncontrolled run (fixed ascending order, shared detector)
returned a 6 px follow median of ~1.41; with controls it measured ~1.0.
The controls caught a real protocol bias — this is why they exist.

## Metric

Follow ratio:

    detected corner displacement / expected synthetic displacement

Close to 1.0 means the detector follows the imposed movement. Substantially
below 1.0 would suggest underestimation or reversion toward symmetry.

## Results

| Deformed side | Amplitude | Faces found | Median follow ratio |
|---|---:|---:|---:|
| Left | 0 px (control) | 10/10 | jitter 1.09 px |
| Left | 6 px | 10/10 | 1.162 |
| Left | 12 px | 10/10 | 0.852 |
| Left | 20 px | 10/10 | 0.841 |
| Right | 0 px (control) | 10/10 | jitter 1.36 px |
| Right | 6 px | 10/10 | 1.194 |
| Right | 12 px | 10/10 | 0.903 |
| Right | 20 px | 10/10 | 0.811 |

## Interpretation

The landmarker detected all 80 faces. For moderate and large deformations,
both sides followed the imposed displacement at roughly 75–90% of the
expected magnitude, with no substantial left/right failure pattern.

Follow ratios above 1 at 6 px reflect that detector noise (~1–1.4 px
jitter) is comparable to the smallest deformation — not super-tracking.
Small landmark changes must therefore not be interpreted on their own;
this independently supports a noise-floor guard (cf. `MIN_MOVE`).

## Limitations

Preliminary synthetic evidence from one subject, one camera, and indoor
lighting. Pixel deformation is not equivalent to real stroke-related
facial paralysis and cannot establish clinical validity. Multi-subject,
multi-device, and clinical-recording validation remain open.

The experiment mitigates the landmark-degradation risk for this setup; it
does not replace clinical validation.

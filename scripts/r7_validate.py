"""R7 validation experiment: does the detector FOLLOW pixel asymmetry?

Protocol: capture frames -> detect baseline -> warp the image with a KNOWN
gaussian pull on one mouth corner (toward the midline) -> re-detect ->
compare detected corner shift vs. the mathematically expected shift.

Metrics per (frame, amplitude):
- found: face still detected after warp
- expected_px: field displacement at the baseline corner
- detected_px: re-detected corner minus baseline corner
- follow_ratio: |detected| / |expected| (1.0 = perfect tracking;
  <<1.0 = detector snapping back toward symmetry, the Kimura failure).
  Amplitude 0 is the noise-floor control: no deformation, so follow is
  undefined ("") and detected_px measures pure re-detection jitter.
- asym_orig / asym_warp: static half-width gap before/after (index response)

Controls against tracking contamination: a FRESH landmarker per frame and
a SEEDED-SHUFFLED amplitude order per frame, so VIDEO-mode temporal state
cannot bias one amplitude systematically. Default amplitudes "0,6,12,20".

Usage (repo root):
    python -m scripts.r7_validate --frames 5 --amplitudes 0,6,12,20
    python -m scripts.r7_validate --frames 5 --side left --out data/r7/manual

Outputs to data/r7/<timestamp>/: originals, warped PNGs, results.csv.
Needs a face in front of the camera; exits gracefully without one.
"""

import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from src.capture import open_camera
from src.index import mouth_half_widths
from src.landmarks import MOUTH_LEFT, MOUTH_RIGHT, NOSE_TIP
from src.mesh import create_landmarker, extract_with_matrix
from src.normalize import interocular
from src.warp import apply_warp, displacement_at

SIDES = {"right": MOUTH_RIGHT, "left": MOUTH_LEFT}


def run(args) -> int:
    out = Path(args.out or f"data/r7/{datetime.now():%Y%m%d_%H%M%S}")
    out.mkdir(parents=True, exist_ok=True)
    corner_idx = SIDES[args.side]
    amplitudes = [float(a) for a in args.amplitudes.split(",") if a.strip()]

    cap = open_camera()
    landmarker = create_landmarker()
    # Single monotonic clock shared by capture AND all measurement loops:
    # VIDEO mode rejects any timestamp a landmarker has already seen, and
    # each fresh landmarker starts its own clock — one global counter keeps
    # every call across every instance strictly increasing.
    last_ms = [0]

    def tick() -> int:
        last_ms[0] = max(int(time.time() * 1000), last_ms[0] + 1)
        return last_ms[0]

    frames = []
    try:
        start = time.time()
        while len(frames) < args.frames and time.time() - start < 60:
            ok, frame = cap.read()
            if not ok:
                continue
            pts, _ = extract_with_matrix(frame, landmarker, tick())
            if pts is None:
                continue
            frames.append((frame, pts))
    finally:
        cap.release()
        landmarker.close()

    if not frames:
        print("[r7] no face captured in 60 s — nothing to validate")
        return 1

    rng = np.random.default_rng(args.seed)
    rows = []
    for fi, (frame, base) in enumerate(frames):
        cv2.imwrite(str(out / f"frame{fi:02d}_orig.png"), frame)
        corner = base[corner_idx, :2].astype(float)
        nose_x = float(base[NOSE_TIP, 0])
        direction = np.array([np.sign(nose_x - corner[0]), 0.0])
        sigma = interocular(base) * 0.6
        base_gap = abs(mouth_half_widths(base / interocular(base))[0]
                       - mouth_half_widths(base / interocular(base))[1])
        # Fresh detector + shuffled order per frame: VIDEO tracking state
        # can neither accumulate across amplitudes nor favor one order.
        order = rng.permutation(amplitudes).tolist()
        measurer = create_landmarker()
        try:
            for amp in order:
                warped = apply_warp(frame, corner, sigma, direction, amp)
                cv2.imwrite(str(out / f"frame{fi:02d}_warp{amp:g}.png"), warped)
                wpts, _ = extract_with_matrix(warped, measurer, tick())
                expected = displacement_at(corner.reshape(1, 2), corner,
                                           sigma, direction, amp).ravel()
                exp_norm = float(np.linalg.norm(expected))
                if wpts is None:
                    rows.append([fi, args.side, amp, False, exp_norm,
                                 "", "", "", ""])
                    continue
                detected = wpts[corner_idx, :2].astype(float) - corner
                det_norm = float(np.linalg.norm(detected))
                follow = "" if exp_norm == 0 else round(det_norm / exp_norm, 3)
                wg = abs(mouth_half_widths(wpts / interocular(wpts))[0]
                         - mouth_half_widths(wpts / interocular(wpts))[1])
                rows.append([fi, args.side, amp, True, round(exp_norm, 2),
                             round(det_norm, 2), follow,
                             round(base_gap, 4), round(wg, 4)])
        finally:
            measurer.close()

    with open(out / "results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame", "side", "amplitude_px", "found",
                    "expected_px", "detected_px", "follow_ratio",
                    "asym_orig", "asym_warp"])
        w.writerows(rows)

    print(f"[r7] {len(rows)} measurements -> {out}/results.csv")
    for amp in amplitudes:
        rs = [r for r in rows if r[2] == amp]
        found = [r for r in rs if r[3] is True]
        if amp == 0:
            noise = sorted(r[5] for r in found if r[5] != "")
            if noise:
                print(f"[r7] amp 0px (control): found {len(found)}/{len(rs)}, "
                      f"re-detection jitter median {noise[len(noise)//2]:.2f}px")
            else:
                print(f"[r7] amp 0px (control): found {len(found)}/{len(rs)}")
            continue
        fr = sorted(r[6] for r in found if r[6] != "")
        if fr:
            print(f"[r7] amp {amp:g}px: found {len(found)}/{len(rs)}, "
                  f"follow median {fr[len(fr)//2]:.3f}")
        else:
            print(f"[r7] amp {amp:g}px: found {len(found)}/{len(rs)}")
    return 0


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=5)
    p.add_argument("--amplitudes", default="0,6,12,20")
    p.add_argument("--side", default="right", choices=list(SIDES))
    p.add_argument("--seed", type=int, default=7,
                   help="order-shuffle seed (reproducible amplitude order)")
    p.add_argument("--out", default="")
    raise SystemExit(run(p.parse_args()))


if __name__ == "__main__":
    main()

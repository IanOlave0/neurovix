"""Live demo: mesh overlay + real-time asymmetry metrics.

Wires the whole Phase-1 chain per frame:
    camera -> frame + t -> mesh (or None) -> pose gates -> align-to-rest -> index -> draw

Drawing policy (deliberate): only the clinical groups (eyes, mouth, nose,
chin) as markers — all 478 points cost draw time and read as noise.
Rejected (yaw) and faceless frames say so ON SCREEN: an instrument that
announces when not to trust it.

Usage (from the repo root — module form so the `src` package resolves):
    python -m src.demo                  # interactive window
    python -m src.demo --headless 6     # no GUI: 6 s stats (None-path check)

Keys: q = quit, r = re-take rest baseline.
"""

import argparse
import csv
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from statistics import median

import cv2
import numpy as np

from src.capture import REST_SECONDS, open_camera
from src.index import (
    DYN_REL_TOL,
    build_rest_index,
    dynamic_asymmetry,
    gesture_score,
    smile_index,
)
from src.landmarks import (
    CHIN,
    EYES,
    LEFT_EYE_OUTER,
    MOUTH,
    NOSE_TIP,
    RIGHT_EYE_OUTER,
)
from src.mesh import create_landmarker, extract_with_matrix
from src.normalize import (
    deroll,
    interocular,
    normalize_frame,
    normalize_scale,
    roll_deg,
    yaw_from_matrix,
)
from src.pose import ALIGN_RESID_TOL, align_to_rest

MARKERS = {
    "eyes": (list(EYES.values()), (255, 255, 0)),
    "mouth": (list(MOUTH.values()), (0, 255, 255)),
    "axis": ([NOSE_TIP, CHIN], (0, 255, 0)),
}


def draw_markers(frame: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Circles on clinical groups. Points are PIXEL space (see mesh.py),
    so they map directly — no rescaling here (rescaling twice was a real
    bug caught when pixel space landed)."""
    out = frame
    for indices, color in MARKERS.values():
        for i in indices:
            x, y = int(pts[i, 0]), int(pts[i, 1])
            cv2.circle(out, (x, y), 3, color, -1)
    return out


def draw_text(frame: np.ndarray, lines: list[str]) -> np.ndarray:
    y = 28
    for line in lines:
        cv2.putText(frame, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        y += 30
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", type=float, default=0)
    parser.add_argument("--label", default="",
                        help="test label written into every CSV row "
                             "(e.g. rest-yaw, smile-frontal)")
    args = parser.parse_args()
    label = args.label

    cap = open_camera()
    landmarker = create_landmarker()
    last_ms = 0

    log_path = Path("runs") / f"demo_log_{datetime.now():%Y%m%d_%H%M%S}.csv"
    log_path.parent.mkdir(exist_ok=True)
    log_file = open(log_path, "w", newline="")
    log = csv.writer(log_file)
    log.writerow(["label", "t", "roll_deg", "roll_rel_deg", "yaw_proxy",
                  "yaw_deg_matrix", "rest_yaw_deg",
                  "accepted", "rejected", "align_rmse_ew", "dynamic",
                  "dyn_rel", "asymmetry", "angle_diff_deg", "gesture",
                  "interocular_px"])
    print(f"[demo] logging to {log_path}")

    rest_meshes: list[np.ndarray] = []
    rest_mats: list = []
    rest_until = time.time() + REST_SECONDS
    rest_index: dict | None = None
    rest_ref: np.ndarray | None = None  # raw-pixel rest mean: alignment target
    rest_ref: np.ndarray | None = None  # raw-pixel rest mean: alignment target
    rest_roll: float | None = None
    rest_yaw: float | None = None
    rest_ready = False
    window: deque[float] = deque(maxlen=5)  # temporal smoothing: status
    # follows the median of the last 5 dynamic values, so one noisy frame
    # cannot flip OK to CHECK on its own.
    print(f"[demo] rest baseline ({REST_SECONDS}s, stay still, neutral face)...")

    fps_ts: list[float] = []
    try:
        while True:
            ok, frame = cap.read()
            t = time.time()
            if not ok:
                continue
            ms = max(int(t * 1000), last_ms + 1)
            last_ms = ms
            fps_ts.append(t)

            pts, matrix = extract_with_matrix(frame, landmarker, ms)
            if pts is None:
                lines = ["no face detected"]
                log.writerow([label, round(t, 3), "", "", "", "", False,
                              "no-face", "", "", "", "", "", "", ""])
            else:
                if t < rest_until:
                    rest_meshes.append(pts)
                    rest_mats.append(matrix)
                    lines = [f"recording rest... {len(rest_meshes)}"]
                else:
                    if not rest_ready and rest_meshes:
                        rest_index = build_rest_index(rest_meshes)
                        rest_ref = np.mean(np.stack(rest_meshes), axis=0)
                        rest_ref = np.mean(np.stack(rest_meshes), axis=0)
                        rest_scale = interocular(rest_ref)
                        rest_roll = float(np.median(
                            [roll_deg(m) for m in rest_meshes]))
                        mat_yaws = [float(np.degrees(yaw_from_matrix(m)))
                                    for m in rest_mats if m is not None]
                        rest_yaw = float(np.median(mat_yaws)) if mat_yaws else None
                        rest_ready = True
                        print(f"[demo] rest ready: {rest_index} "
                              f"rest_roll={rest_roll:.1f} rest_yaw={rest_yaw}")
                    norm, info = normalize_frame(pts, matrix=matrix,
                                                 rest_roll=rest_roll,
                                                 rest_yaw=rest_yaw)
                    if not info["accepted"]:
                        lines = [f"pose out of range ({info['rejected']}: "
                                 f"roll {info['roll_deg']:.0f}d, yaw {info['yaw_proxy']:.2f})"]
                        rel = "" if rest_roll is None else round(
                            info["roll_deg"] - rest_roll, 1)
                        log.writerow([label, round(t, 3),
                                      round(info["roll_deg"], 1), rel,
                                      round(info["yaw_proxy"], 3),
                                      info["yaw_deg_matrix"],
                                      "" if rest_yaw is None else round(rest_yaw, 1),
                                      False,
                                      info["rejected"], "", "", "", "",
                                      "", "", ""])
                    else:
                        idx = smile_index(norm)
                        g = gesture_score(idx, rest_index) if rest_index else 0.0
                        common = [label, round(t, 3),
                                  round(info["roll_deg"], 1),
                                  round(info["roll_deg"] - rest_roll, 1)
                                  if rest_roll is not None else "",
                                  round(info["yaw_proxy"], 3),
                                  info["yaw_deg_matrix"],
                                  "" if rest_yaw is None else round(rest_yaw, 1)]
                        if rest_ref is None:
                            lines = ["waiting for rest baseline"]
                            log.writerow(common + [True, "", "", "", "", "",
                                                   "", "", g,
                                                   round(interocular(pts), 1)])
                        else:
                            aligned, rmse, _ = align_to_rest(pts, rest_ref)
                            rmse = round(rmse, 4)
                            if rmse > ALIGN_RESID_TOL:
                                lines = ["pose-limited: unstable alignment",
                                         f"(residual {rmse} > tol {ALIGN_RESID_TOL})"]
                                log.writerow(common + [True, "", rmse, "", "",
                                                       "", "", "", g,
                                                       round(interocular(pts), 1)])
                            else:
                                unit = interocular(rest_ref)
                                dyn = dynamic_asymmetry(aligned / unit,
                                                        rest_ref / unit)
                                window.append(dyn["dyn_rel"])
                                med = round(median(window), 4)
                                status = "OK" if med < DYN_REL_TOL else "CHECK"
                                lines = [
                                    f"rel: {dyn['dyn_rel']} (med {med}) [{status}]",
                                    f"L {dyn['move_left']} R {dyn['move_right']}  "
                                    f"gesture: {g}",
                                ]
                                log.writerow(common + [True, "", rmse,
                                                        dyn["dynamic"],
                                                        dyn["dyn_rel"],
                                                        idx["asymmetry"],
                                                        idx["angle_diff_deg"], g,
                                                        round(interocular(pts), 1)])
                    frame = draw_markers(frame, pts)

            if args.headless:
                if t - fps_ts[0] >= args.headless:
                    break
            else:
                cv2.imshow("neurovix - demo (q=quit, r=rest)", draw_text(frame, lines))
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if key == ord("r"):
                    rest_meshes, rest_mats = [], []
                    rest_ready, rest_yaw, rest_ref = False, None, None
                    rest_until = time.time() + REST_SECONDS
                    print("[demo] re-taking rest baseline...")
    finally:
        cap.release()
        landmarker.close()
        log_file.close()
        print(f"[demo] log saved to {log_path}")
        cv2.destroyAllWindows()

    if len(fps_ts) > 1:
        el = fps_ts[-1] - fps_ts[0]
        print(f"[demo] frames={len(fps_ts)} measured_fps={len(fps_ts)/el:.1f}")


if __name__ == "__main__":
    main()

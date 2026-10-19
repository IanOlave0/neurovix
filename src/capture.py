"""Live capture loop: real per-frame timestamps + rest baseline.

Phase 1, step 1. This module delivers frames with capture-time timestamps
and a rest baseline per session (protocol section 2). No landmarks yet:
later stages consume what this module produces.

Usage:
    python src/capture.py                  # interactive (window + keys)
    python src/capture.py --headless 5     # no GUI: capture 5 s, print stats

Keys (interactive): q = quit, r = re-take rest baseline.
"""

import argparse
import time

import cv2

CAMERA_INDEX = 0
REST_SECONDS = 3.0


def open_camera(index: int = CAMERA_INDEX) -> cv2.VideoCapture:
    """Open the camera or fail loudly — a silent retry loop would hide
    hardware problems behind fake data."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"could not open camera {index}")
    return cap


def summarize(timestamps: list[float], nominal_fps: float) -> dict:
    """Measured vs. nominal frame rate, plus jitter (std of inter-frame
    intervals). Jitter is why velocity features must use real timestamps."""
    import numpy as np

    dts = np.diff(np.array(timestamps))
    elapsed = timestamps[-1] - timestamps[0]
    return {
        "frames": len(timestamps),
        "elapsed_s": round(elapsed, 3),
        "measured_fps": round(len(timestamps) / elapsed, 2),
        "nominal_fps": round(nominal_fps, 2),
        "mean_dt_ms": round(float(dts.mean() * 1000), 2),
        "jitter_dt_std_ms": round(float(dts.std() * 1000), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", type=float, default=0,
                        help="seconds to capture without GUI (0 = interactive)")
    args = parser.parse_args()

    cap = open_camera()
    nominal = cap.get(cv2.CAP_PROP_FPS) or 30.0

    timestamps: list[float] = []
    rest_frames: list = []
    rest_until = time.time() + REST_SECONDS
    print(f"[capture] recording rest baseline ({REST_SECONDS}s, stay still)...")

    start = time.time()
    while True:
        ok, frame = cap.read()
        t = time.time()  # timestamp AT capture, before any processing
        if not ok:
            print("[capture] dropped frame (camera hiccup, not fatal)")
            continue
        timestamps.append(t)

        if t < rest_until:
            rest_frames.append(frame)
        elif len(rest_frames) and not getattr(main, "_rest_done", False):
            main._rest_done = True  # noqa: SLF001 — tiny script, no class needed
            print(f"[capture] rest baseline ready: {len(rest_frames)} frames")

        if args.headless:
            if t - start >= args.headless:
                break
        else:
            cv2.imshow("neurovix - capture (q=quit, r=rest)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("r"):
                rest_frames = []
                rest_until = time.time() + REST_SECONDS
                main._rest_done = False  # noqa: SLF001
                print("[capture] re-taking rest baseline...")

    cap.release()
    cv2.destroyAllWindows()

    stats = summarize(timestamps, nominal)
    print("[capture] session stats:", stats)
    print(f"[capture] rest frames stored: {len(rest_frames)}")


if __name__ == "__main__":
    main()

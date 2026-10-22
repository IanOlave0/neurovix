"""Live demo: mesh overlay + real-time asymmetry metrics.

Wires the whole Phase-1 chain per frame:
    camera -> frame + t -> mesh (or None) -> normalize -> index -> draw

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
import time

import cv2
import numpy as np

from src.capture import REST_SECONDS, open_camera
from src.index import SYMMETRIC_TOL, gesture_score, smile_index
from src.landmarks import (
    CHIN,
    EYES,
    LEFT_EYE_OUTER,
    MOUTH,
    NOSE_TIP,
    RIGHT_EYE_OUTER,
)
from src.mesh import create_landmarker, extract_landmarks
from src.normalize import normalize_frame

MARKERS = {
    "eyes": (list(EYES.values()), (255, 255, 0)),
    "mouth": (list(MOUTH.values()), (0, 255, 255)),
    "axis": ([NOSE_TIP, CHIN], (0, 255, 0)),
}


def draw_markers(frame: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Circles on clinical groups (normalized x, y -> pixels)."""
    h, w = frame.shape[:2]
    out = frame
    for indices, color in MARKERS.values():
        for i in indices:
            x, y = int(pts[i, 0] * w), int(pts[i, 1] * h)
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
    args = parser.parse_args()

    cap = open_camera()
    landmarker = create_landmarker()
    last_ms = 0

    rest_meshes: list[np.ndarray] = []
    rest_until = time.time() + REST_SECONDS
    rest_index: dict | None = None
    rest_ready = False
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

            pts = extract_landmarks(frame, landmarker, ms)
            if pts is None:
                lines = ["no face detected"]
            else:
                if t < rest_until:
                    rest_meshes.append(pts)
                    lines = [f"recording rest... {len(rest_meshes)}"]
                else:
                    if not rest_ready and rest_meshes:
                        mean_rest = np.mean(np.stack(rest_meshes), axis=0)
                        rest_index = smile_index(mean_rest)
                        rest_ready = True
                        print(f"[demo] rest ready: {rest_index}")
                    norm, info = normalize_frame(pts)
                    if not info["accepted"]:
                        lines = [f"pose out of range ({info['rejected']}: "
                                 f"roll {info['roll_deg']:.0f}d, yaw {info['yaw_proxy']:.2f})"]
                    else:
                        idx = smile_index(norm)
                        g = gesture_score(idx, rest_index) if rest_index else 0.0
                        status = "OK" if idx["asymmetry"] < SYMMETRIC_TOL else "CHECK"
                        lines = [
                            f"asymmetry: {idx['asymmetry']} [{status}]",
                            f"weaker: {idx['weaker_side']}  gesture: {g}",
                        ]
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
                    rest_meshes, rest_ready = [], False
                    rest_until = time.time() + REST_SECONDS
                    print("[demo] re-taking rest baseline...")
    finally:
        cap.release()
        landmarker.close()
        cv2.destroyAllWindows()

    if len(fps_ts) > 1:
        el = fps_ts[-1] - fps_ts[0]
        print(f"[demo] frames={len(fps_ts)} measured_fps={len(fps_ts)/el:.1f}")


if __name__ == "__main__":
    main()

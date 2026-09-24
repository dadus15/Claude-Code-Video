#!/usr/bin/env python3
"""Render the Ferrari photo slideshow to an MP4 video.

Uses the same timing and Ken Burns moves as the web slider: each photo holds
for 5 s including a 0.9 s crossfade, and moves only by uniform scale and
translation, clamped so the frame is always covered and the GT Turismo
watermark stays in view. Frames are resampled with sub-pixel precision, so
slow moves stay smooth.

    pip install pillow numpy imageio-ffmpeg
    python3 video/make_video.py                  # -> video/ferrari-slider.mp4
    python3 video/make_video.py --size 1920x1080 # 16:9 with thin side bars

Photos are looked up in photos/ by filename suffix (01-90248.jpg works).
Missing photos are skipped.
"""
import argparse
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = "ffmpeg"

ROOT = Path(__file__).resolve().parent.parent
SLIDE_S = 5.0
FADE_S = 0.9
LIFE_S = SLIDE_S + FADE_S
WATERMARK_BOTTOM = 0.975

# Same order and motion as app.js: s = scale, x/y = translation as a fraction
# of the frame (positive x moves the photo right, positive y moves it down).
SLIDES = [
    ("90241", (1.0, 0, 0), (1.045, 0.006, -0.008)),       # front three-quarter push-in
    ("90248", (1.035, -0.01, -0.002), (1.035, 0.01, -0.002)),  # nose to mirror
    ("90243", (1.03, 0.005, -0.004), (1.045, -0.008, 0.003)),  # toward the shield
    ("90242", (1.04, 0.004, -0.002), (1.04, -0.006, -0.002)),  # centre cap drift
    ("90244", (1.035, 0.006, 0.004), (1.045, 0.002, -0.008)),  # along the engraved lip
    ("90247", (1.0, 0, 0), (1.045, 0, -0.002)),              # centred wheel push-in
    ("90246", (1.035, 0.01, -0.002), (1.035, -0.01, -0.002)),  # along the rear haunch
    ("90245", (1.05, -0.006, -0.006), (1.0, 0, 0)),          # pullback to full car
]


def find_photos():
    files = [p for d in (ROOT / "photos", ROOT) if d.is_dir() for p in d.iterdir()]
    found = {}
    for p in sorted(files):
        m = re.search(r"(?:^|[^0-9])(9024[1-8])\.jpe?g$", p.name, re.I)
        if m and m.group(1) not in found:
            found[m.group(1)] = p
    return found


def drift(t):
    """Mostly linear with softened ends: calm, never visibly stopped."""
    return 0.55 * t + 0.45 * (0.5 - 0.5 * math.cos(math.pi * t))


def smoothstep(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def render_layer(img, motion, p, W, H, fit_w, fit_h):
    """Draw one photo into a fit_w x fit_h frame, centred in W x H."""
    (s0, x0, y0), (s1, x1, y1) = motion
    e = drift(min(1.0, max(0.0, p)))
    s = max(1.0, s0 + (s1 - s0) * e)
    iw, ih = img.size
    base = max(fit_w / iw, fit_h / ih)          # cover the photo frame
    bw, bh = iw * base, ih * base
    x = (x0 + (x1 - x0) * e) * fit_w
    y = (y0 + (y1 - y0) * e) * fit_h
    max_x = max(0.0, (s * bw - fit_w) / 2)
    max_y = max(0.0, (s * bh - fit_h) / 2)
    x = min(max_x, max(-max_x, x))
    y = min(max_y, max(-max_y, y))
    y_max = fit_h / 2 - (WATERMARK_BOTTOM - 0.5) * s * bh
    if y > y_max:
        y = max(y_max, -max_y)
    S = base * s
    ox, oy = (W - fit_w) / 2, (H - fit_h) / 2
    # Output pixel (X, Y) samples source (a*X + c, e*Y + f).
    a = 1 / S
    c = iw / 2 - (ox + fit_w / 2 + x) / S
    f = ih / 2 - (oy + fit_h / 2 + y) / S
    frame = img.transform((W, H), Image.AFFINE, (a, 0, c, 0, a, f), resample=Image.BICUBIC)
    arr = np.asarray(frame, dtype=np.float32)
    if (fit_w, fit_h) != (W, H):  # letterbox: black outside the photo frame
        mask = np.zeros((H, W, 1), np.float32)
        mask[int(round(oy)):int(round(oy + fit_h)), int(round(ox)):int(round(ox + fit_w))] = 1
        arr *= mask
    return arr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="1920x1152", help="WxH (default: the photos' native 5:3)")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--out", default=str(ROOT / "video" / "ferrari-slider.mp4"))
    args = ap.parse_args()
    W, H = (int(v) for v in args.size.lower().split("x"))

    found = find_photos()
    slides = [(sid, Image.open(found[sid]).convert("RGB"), a, b) for sid, a, b in SLIDES if sid in found]
    missing = [sid for sid, _, _ in SLIDES if sid not in found]
    if not slides:
        sys.exit("No photos found in photos/ (expected names ending in 90241.jpg ... 90248.jpg)")
    print("Using:", ", ".join(s[0] for s in slides), "| missing:", ", ".join(missing) or "none")

    # The photo frame keeps the photos' aspect ratio inside the video frame.
    iw, ih = slides[0][1].size
    r = iw / ih
    fit_w, fit_h = (W, W / r) if W / H < r else (H * r, H)
    if abs(fit_w - W) < 2 and abs(fit_h - H) < 2:
        fit_w, fit_h = W, H

    n = len(slides)
    total = n * SLIDE_S
    frames = int(round(total * args.fps))
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(args.fps), "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-movflags", "+faststart", args.out]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for fi in range(frames):
        t = fi / args.fps
        k = min(n - 1, int(t // SLIDE_S))
        born = k * SLIDE_S
        tau = t - born
        last = k == n - 1
        # The finale's move ends exactly at the end of the video on the full car.
        life = SLIDE_S if last else LIFE_S
        _, img, a, b = slides[k]
        out = render_layer(img, (a, b), tau / life, W, H, fit_w, fit_h)
        alpha = smoothstep(tau / FADE_S)
        if alpha < 1:
            if k > 0:  # crossfade over the previous photo, which keeps moving
                _, pimg, pa, pb = slides[k - 1]
                prev = render_layer(pimg, (pa, pb), (t - (k - 1) * SLIDE_S) / LIFE_S, W, H, fit_w, fit_h)
                out = alpha * out + (1 - alpha) * prev
            else:      # open from black
                out = alpha * out
        if last:       # close to black over the final 1.2 s
            out *= 1 - smoothstep((t - (total - 1.2)) / 1.2)
        enc.stdin.write(np.clip(out + 0.5, 0, 255).astype(np.uint8).tobytes())
        if fi % args.fps == 0:
            print(f"\r{t:5.1f}s / {total:.0f}s", end="", flush=True)

    enc.stdin.close()
    enc.wait()
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()

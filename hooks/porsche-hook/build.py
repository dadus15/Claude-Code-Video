"""Build the Porsche hook: cut + camera moves (FFmpeg), animation pass (HyperFrames), audio mix, final mux.

Usage:  python3 build.py [base|audio|mux|all]
Timeline is 24 fps; every in/out point below is a source frame index.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(HERE, "footage")
COMP = os.path.join(HERE, "composition")
BUILD = os.path.join(HERE, "build")
FPS = 24
W, H = 1920, 1080

# Camera moves. ax/ay = zoom anchor as a fraction of the frame (0,0 = top-left).
#   punch: 100% -> `to` over `frames`, starting at `at` (ease-out), held to the cut.
#   creep: 100% -> `to` across the whole shot (ease-in-out).
# Every shot starts at 100%, so the frame is back to 100% at every cut.
EDL = [
    # file,                          in,  out, camera move,                                         note
    ("headlight-rain.mp4",            34,  85, None,                                                "dark headlight in the rain"),
    ("ignition-garage-tunnel.mp4",     2,  23, dict(kind="punch", to=1.22, at=2, frames=8, ax=0.5, ay=0.53), "START pressed (lights up at src f9)"),
    ("headlight-rain.mp4",            85, 145, None,                                                "headlight ignites at src f90"),
    ("ignition-garage-tunnel.mp4",    24,  89, dict(kind="creep", to=1.10, ax=0.5, ay=0.40),        "garage door rises"),
    ("ignition-garage-tunnel.mp4",    89, 169, None,                                                "tunnel run (tachometer)"),
    ("details-badge-wheel-spoiler.mp4", 120, 169, None,                                             "spoiler rising"),
    ("details-badge-wheel-spoiler.mp4",  58,  93, None,                                             "caliper"),
    ("wheel-pullout.mp4",             58, 145, None,                                                "wheel pull-out (HUD lock-on)"),
    ("mountain-road-hero.mp4",         0, 169, dict(kind="creep", to=1.08, ax=0.5, ay=0.30),        "hero approach (headline)"),
]

# Sound design (seconds on the output timeline). Everything else is the clips' own audio.
CLIP_AUDIO_GAIN = 0.75
SFX = [
    # file,               at,     gain, trim (s)
    ("click.mp3",         2.40,   0.9,  None),   # START button press (src f9 of shot 2 -> T 2.417; click onset 0.04 s)
    ("impact-bass-1.mp3", 3.17,   0.45, None),   # headlight ignites (T 3.208)
    ("riser.mp3",         16.05,  0.30, 4.40),   # builds under the wheel shot, stops on the headline
    ("impact-bass-2.mp3", 20.45,  0.28, 1.40),   # headline lands (T 20.46)
]
FADE_OUT = 0.6


def run(cmd):
    print("+", " ".join(cmd[:6]), "..." if len(cmd) > 6 else "")
    subprocess.run(cmd, check=True)


def zoom_expr(move, n):
    if move is None:
        return "1", "0", "0"
    if move["kind"] == "punch":
        p = f"clip((on-{move['at']})/{move['frames']},0,1)"
        z = f"1+{move['to'] - 1:.4f}*(1-pow(1-{p},3))"
    else:
        p = f"(on/{n - 1})"
        z = f"1+{move['to'] - 1:.4f}*({p}*{p}*(3-2*{p}))"
    x = f"(iw-iw/zoom)*{move['ax']}"
    y = f"(ih-ih/zoom)*{move['ay']}"
    return z, x, y


def timeline():
    t, out = 0, []
    for f, a, b, move, note in EDL:
        out.append(dict(file=f, src_in=a, src_out=b, start=t, frames=b - a, move=move, note=note))
        t += b - a
    return out, t


def build_base():
    os.makedirs(BUILD, exist_ok=True)
    shots, total = timeline()
    parts = []
    for i, s in enumerate(shots):
        z, x, y = zoom_expr(s["move"], s["frames"])
        vf = (
            f"trim=start_frame={s['src_in']}:end_frame={s['src_out']},setpts=PTS-STARTPTS,"
            f"scale=3840:2160:flags=lanczos,"
            f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},"
            f"setsar=1,format=yuv420p"
        )
        out = os.path.join(BUILD, f"shot{i:02d}.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(FOOT, s["file"]), "-vf", vf, "-an",
             "-frames:v", str(s["frames"]), "-c:v", "libx264", "-crf", "12", "-preset", "medium",
             "-g", "12", "-r", str(FPS), out])
        parts.append(out)
    lst = os.path.join(BUILD, "concat.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    os.makedirs(os.path.join(COMP, "assets"), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
         os.path.join(COMP, "assets", "base.mp4")])
    with open(os.path.join(BUILD, "timeline.json"), "w") as fh:
        json.dump(dict(fps=FPS, total_frames=total, total_s=total / FPS,
                       shots=[{**s, "start_s": round(s["start"] / FPS, 3)} for s in shots]), fh, indent=1)
    print(f"base: {total} frames = {total / FPS:.3f}s")


def build_audio():
    shots, total = timeline()
    dur = total / FPS
    pad = 0.05  # short overlap at each cut so the clip audio crossfades instead of clicking
    inputs, chains, labels = [], [], []
    for i, s in enumerate(shots):
        a = max(0.0, s["src_in"] / FPS - pad)
        b = s["src_out"] / FPS + pad
        delay = max(0.0, s["start"] / FPS - (s["src_in"] / FPS - a))
        inputs += ["-i", os.path.join(FOOT, s["file"])]
        chains.append(
            f"[{i}:a]aresample=48000,atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d={pad},afade=t=out:st={b - a - pad:.4f}:d={pad},"
            f"volume={CLIP_AUDIO_GAIN},adelay={int(delay * 1000)}:all=1[c{i}]")
        labels.append(f"[c{i}]")
    n = len(shots)
    for j, (f, at, gain, trim) in enumerate(SFX):
        k = n + j
        inputs += ["-i", os.path.join(COMP, "assets", "sfx", f)]
        tr = f"atrim=0:{trim},afade=t=out:st={trim - 0.5}:d=0.5," if trim else ""
        chains.append(f"[{k}:a]aresample=48000,{tr}volume={gain},adelay={int(at * 1000)}:all=1[s{j}]")
        labels.append(f"[s{j}]")
    chains.append(
        f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,"
        f"atrim=0:{dur:.4f},afade=t=out:st={dur - FADE_OUT:.4f}:d={FADE_OUT},"
        f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[mix]",
         "-ac", "2", "-c:a", "pcm_s16le", os.path.join(BUILD, "mix.wav")])


def mux(name="porsche-hook_v1.mp4"):
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(BUILD, "overlay.mp4"), "-i",
         os.path.join(BUILD, "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "256k", "-movflags", "+faststart", os.path.join(HERE, "renders", name)])


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("base", "all"):
        build_base()
    if step in ("audio", "all"):
        build_audio()
    if step == "mux":
        mux(*sys.argv[2:3])

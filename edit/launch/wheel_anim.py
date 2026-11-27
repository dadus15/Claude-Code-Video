"""C26 spin-down + 3/4 turn sequence for launch scene S1 (Cycles, real object motion blur, transparent film).
usage: python3 wheel_anim.py <c26_m.blend> <outdir> <spp>
Timing (scene-local seconds, 24 fps): t 0.6-2.4 s = 44 frames. spin(t) = SPIN_END - W0*TAU*exp(-t/TAU), yaw 8 -> 28 deg (spring f 1.1 Hz, z 0.8), pitch 4 -> 6."""
import bpy, math, sys, os
a = sys.argv[1:]; C26, OUTD, SPP = a[0], a[1], int(a[2]); os.makedirs(OUTD, exist_ok=True)
sys.argv = ["x", C26, "/dev/null", "8", "4", "0", "1080", "1920", str(SPP), "1.95"]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wheel_studio.py")).read()
src = src.replace("S.render.filepath = OUT; bpy.ops.render.render(write_still=True)", "pass")      # build the scene only
exec(compile(src, "wheel_studio", "exec"))
W0, TAU, SPIN_END = 900.0, 0.40, 12.0
def spring(t, f=1.1, z=0.8):
    if t <= 0: return 0.0
    w = 2 * math.pi * f; wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
def pose(t):
    s = SPIN_END - W0 * TAU * math.exp(-t / TAU); y = 8 + 20 * spring(t - 0.6); p = 4 + 2 * spring(t - 0.6)
    return y, p, s
S.render.fps = 24; S.render.use_motion_blur = True; S.render.motion_blur_shutter = 0.5
for i in range(0, 46):
    t = 0.6 + (i - 1) / 24.0; y, p, s = pose(t)
    root.matrix_world = Matrix.Rotation(math.radians(y), 4, 'Z') @ Matrix.Rotation(math.radians(90), 4, 'X') @ Matrix.Rotation(math.radians(s), 4, 'Z')
    root.keyframe_insert("location", frame=i); root.keyframe_insert("rotation_euler", frame=i)
    cam.location = (0, -DIST * math.cos(math.radians(p)), DIST * math.sin(math.radians(p)))
    cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert("location", frame=i); cam.keyframe_insert("rotation_euler", frame=i)
import time
for i in range(1, 45):
    out = os.path.join(OUTD, f"w{i:03d}.png")
    if os.path.exists(out): continue
    t0 = time.time(); S.frame_set(i); S.render.filepath = out; bpy.ops.render.render(write_still=True); print("DONE", i, round(time.time() - t0, 1), flush=True)

"""3D Turismo T mark (extruded from the supplied logo PNG contours: titanium body + glossy red ceramic square)
with the client's Santa hat (santa_hat.blend) sitting on the top bar. Cycles, transparent film.
usage: python3 logo_hat.py <logo_navy.png> <santa_hat.blend> <out.png> yaw pitch hat_drop(0..1) [rx ry spp]"""
import bpy, bmesh, math, sys
import numpy as np, cv2
from mathutils import Vector, Matrix
a = sys.argv[1:]; LOGO, HATB, OUT = a[0], a[1], a[2]; YAW, PITCH, DROP = float(a[3]), float(a[4]), float(a[5])
RX, RY, SPP = (int(a[6]), int(a[7]), int(a[8])) if len(a) > 8 else (1080, 1920, 64)
bpy.ops.wm.read_factory_settings(use_empty=True); S = bpy.context.scene
img = cv2.imread(LOGO, cv2.IMREAD_UNCHANGED); al = img[..., 3] > 128
mark = np.zeros_like(al); mark[:, :1045] = al[:, :1045]
red = mark & (img[..., 2] > 150) & (img[..., 1] < 90); body = mark & ~cv2.dilate(red.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
GS = 3.3 / 0.62                             # world scale: the hat keeps its native size (hair strand width is absolute)
PX = 3.3 / (1038 - 19)                     # mark 3.3 units wide
def mesh_from(mask, name, depth, z0):
    """2D curve with all contours (outer + holes, even-odd fill) extruded to `depth`, small bevel; stands facing -Y"""
    cs, hier = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    cu.extrude = depth * GS / 2; cu.bevel_depth = 0.003 * GS; cu.bevel_resolution = 3
    for i, c in enumerate(cs):
        if cv2.contourArea(c) < 150: continue
        bx_, by_, bw_, bh_ = cv2.boundingRect(c)
        if bx_ > 800 and by_ > 300: continue          # the "T" of the TURISMO wordmark overlaps the mark's x-range
        c = cv2.approxPolyDP(c, 1.0, True)[:, 0, :]
        sp = cu.splines.new('POLY'); sp.points.add(len(c) - 1); sp.use_cyclic_u = True
        for k, (x, y) in enumerate(c): sp.points[k].co = ((x - 528) * PX, -(y - 280) * PX, 0, 1)
    o = bpy.data.objects.new(name, cu); S.collection.objects.link(o)
    o.rotation_euler = (math.radians(90), 0, 0); o.location = (0, (z0 + depth / 2) * GS, 0)
    return o
def mat(name, base, metal, rough, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.04
    if aniso: b.inputs["Anisotropic"].default_value = aniso
    return m
T = mesh_from(body, "T_body", 0.07, 0.0); T.data.materials.append(mat("titanium", (0.62, 0.62, 0.64), 1.0, 0.32, aniso=0.3))
R = mesh_from(red, "T_red", 0.074, -0.004); R.data.materials.append(mat("red_ceramic", (0.55, 0.02, 0.03), 0.0, 0.12, coat=1.0))
# Santa hat from the client's model
with bpy.data.libraries.load(HATB) as (src, dst): dst.objects = [n for n in src.objects if n.startswith("hat_")]
hat_root = bpy.data.objects.new("hat_root", None); S.collection.objects.link(hat_root)
for o in dst.objects:
    S.collection.objects.link(o); o.parent = hat_root
# brim centre in logo px (530, 38) -> top bar; hat native brim width ~2.4 units -> 0.745*PX*2400/... (745 px)
bx, bz = (530 - 528) * PX, -(38 - 280) * PX
hs = 0.92
hat_root.scale = (hs, hs, hs)
hat_root.location = (bx, 0.035 * GS, bz - 0.03 + 0.9 * GS * (1 - DROP))
hat_root.rotation_euler = (0, math.radians(9 - 32 * (1 - DROP)), 0)
import os
SHOW = os.environ.get("LH_SHOW", "both")            # logo | hat | both : separate layers for 2D animation
if SHOW == "logo":
    for o in list(hat_root.children): o.hide_render = True
if SHOW == "hat":
    T.hide_render = True; R.hide_render = True
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.lens = 70; D = 2.6 * GS
cam.location = (D * math.sin(math.radians(YAW)) * math.cos(math.radians(PITCH)), -D * math.cos(math.radians(YAW)) * math.cos(math.radians(PITCH)), 0.1 + D * math.sin(math.radians(PITCH)))
tgt = Vector((0.0, 0.03, 0.30)) * GS; cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
def area(name, loc, sx, sy, power, col=(1, 1, 1)):
    l = bpy.data.objects.new(name, bpy.data.lights.new(name, 'AREA')); S.collection.objects.link(l)
    l.data.shape = 'RECTANGLE'; l.data.size = sx * GS; l.data.size_y = sy * GS; l.data.energy = power * GS * GS; l.data.color = col; l.location = Vector(loc) * GS
    l.rotation_euler = (Vector((0, 0, 0)) - l.location).to_track_quat('-Z', 'Y').to_euler()
area("key", (-1.6, -2.0, 2.0), 2.0, 1.2, 260); area("strip", (2.0, -1.2, 0.3), 0.3, 2.5, 120, (0.9, 0.95, 1.0))
area("rim", (0.3, 2.0, 1.6), 1.5, 0.4, 160, (0.85, 0.92, 1.0)); area("red", (0, -1.0, -1.6), 2.2, 1.0, 35, (1.0, 0.1, 0.08))
wd = bpy.data.worlds.new("w"); S.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.015, 0.016, 0.02, 1)
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = SPP; S.cycles.use_denoising = True
S.render.film_transparent = True; S.render.resolution_x = RX; S.render.resolution_y = RY
S.view_settings.view_transform = 'AgX'; S.view_settings.look = 'AgX - Medium High Contrast'
S.render.image_settings.color_mode = 'RGBA'; S.render.filepath = OUT; bpy.ops.render.render(write_still=True)
from bpy_extras.object_utils import world_to_camera_view as w2c
bp = w2c(S, cam, hat_root.matrix_world.translation); print("BRIM_PX", round(bp.x * RX, 1), round((1 - bp.y) * RY, 1))
print("LOGO_DONE")

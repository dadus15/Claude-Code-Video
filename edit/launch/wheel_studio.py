"""Turismo C26 studio hero (Blender Cycles, transparent film) for the launch film.
usage: python3 wheel_studio.py <c26_m.blend> <out.png> yaw_deg pitch_deg spin_deg [res_x res_y samples dist]
CAD frame: metres, axle +Z, face +Z. Camera looks at the face; yaw = 3/4 turn, pitch = camera elevation."""
import bpy, math, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
C26, OUT = a[0], a[1]; YAW, PITCH, SPIN = (float(v) for v in a[2:5])
RX, RY, SPP, DIST = (int(a[5]), int(a[6]), int(a[7]), float(a[8])) if len(a) > 8 else (1080, 1920, 48, 1.95)
bpy.ops.wm.read_factory_settings(use_empty=True); S = bpy.context.scene
def mat(name, base, metal, rough, aniso=0.0, noise_r=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if aniso:
        b.inputs["Anisotropic"].default_value = aniso
        tg = nt.nodes.new("ShaderNodeTangent"); tg.direction_type = 'RADIAL'; tg.axis = 'Z'; nt.links.new(tg.outputs[0], b.inputs["Tangent"])
    if noise_r:
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 900.0
        mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs[3].default_value = rough - noise_r; mp.inputs[4].default_value = rough + noise_r * 1.4
        nt.links.new(nz.outputs[0], mp.inputs[0]); nt.links.new(mp.outputs[0], b.inputs["Roughness"])
    return m
M_WHEEL = mat("brushed_silver", (0.56, 0.565, 0.57), 1.0, 0.26, aniso=0.6, noise_r=0.05)
M_BARREL = mat("barrel", (0.30, 0.30, 0.31), 1.0, 0.5)
M_BOLT = mat("bolt", (0.82, 0.82, 0.84), 1.0, 0.16)
with bpy.data.libraries.load(C26) as (src, dst): dst.meshes = ["C26_cad"]
cad = dst.meshes[0]; cad.materials.clear(); cad.materials.append(M_WHEEL); cad.materials.append(M_BARREL)
n = len(cad.polygons); pc = np.zeros(n * 3); pn = np.zeros(n * 3)
cad.polygons.foreach_get("center", pc); cad.polygons.foreach_get("normal", pn); pc = pc.reshape(-1, 3); pn = pn.reshape(-1, 3)
barrel = (np.hypot(pc[:, 0], pc[:, 1]) > 0.245) & (pc[:, 2] < 0.118) & (np.abs(pn[:, 2]) < 0.5)
cad.polygons.foreach_set("material_index", barrel.astype(np.int32))
root = bpy.data.objects.new("C26_root", None); S.collection.objects.link(root)
w = bpy.data.objects.new("C26", cad); S.collection.objects.link(w); w.parent = root
import bmesh
for k in range(5):
    ang = math.radians(36 + 72 * k); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.0085, radius2=0.0085, depth=0.012)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.0115, radius2=0.0115, depth=0.004, matrix=Matrix.Translation((0, 0, -0.008)))
    me = bpy.data.meshes.new(f"bolt{k}"); bm.to_mesh(me); bm.free(); me.materials.append(M_BOLT)
    o = bpy.data.objects.new(f"bolt{k}", me); S.collection.objects.link(o); o.parent = root
    o.location = (0.056 * math.cos(ang), 0.056 * math.sin(ang), 0.0515)
# orientation: face (+Z) toward the camera (-Y), 3/4 yaw, own-axle spin
root.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ Matrix.Rotation(math.radians(90), 4, 'X') @ Matrix.Rotation(math.radians(SPIN), 4, 'Z')
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.lens = 85; cam.data.sensor_fit = 'HORIZONTAL'
p = math.radians(PITCH); cam.location = (0, -DIST * math.cos(p), DIST * math.sin(p))
cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
def area(name, loc, sx, sy, power, col=(1, 1, 1)):
    l = bpy.data.objects.new(name, bpy.data.lights.new(name, 'AREA')); S.collection.objects.link(l)
    l.data.shape = 'RECTANGLE'; l.data.size = sx; l.data.size_y = sy; l.data.energy = power; l.data.color = col; l.location = loc
    l.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return l
area("key", (-1.4, -1.6, 1.6), 1.6, 0.9, 110)                 # big softbox top-left front
area("strip", (1.6, -1.0, 0.2), 0.25, 2.2, 60, (0.92, 0.96, 1.0))   # vertical strip fill right
area("rim", (0.3, 1.5, 1.4), 1.2, 0.3, 90, (0.85, 0.92, 1.0))      # cool rim from behind
area("red", (0.0, -0.8, -1.4), 2.0, 1.0, 30, (1.0, 0.08, 0.06))    # red under-glow
wd = bpy.data.worlds.new("w"); S.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.012, 0.014, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 1.0
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = SPP; S.cycles.use_denoising = True
S.cycles.max_bounces = 6; S.render.film_transparent = True; S.render.resolution_x = RX; S.render.resolution_y = RY
S.view_settings.view_transform = 'AgX'; S.view_settings.look = 'AgX - Medium High Contrast'
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGBA'
S.render.filepath = OUT; bpy.ops.render.render(write_still=True)
from bpy_extras.object_utils import world_to_camera_view as w2c
c = w2c(S, cam, Vector((0, 0, 0))); print("HUB_PX", round(c.x * RX, 1), round((1 - c.y) * RY, 1))

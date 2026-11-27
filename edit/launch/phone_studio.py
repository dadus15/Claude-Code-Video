"""3D phone (titanium frame, black glass, emissive UI screen under a glossy glass layer), Cycles, transparent film.
usage: python3 phone_studio.py <ui.png> <out.png> yaw tilt roll [rx ry spp]"""
import bpy, math, sys
from mathutils import Vector, Matrix
a = sys.argv[1:]; UI, OUT = a[0], a[1]; YAW, TILT, ROLL = (float(v) for v in a[2:5])
RX, RY, SPP = (int(a[5]), int(a[6]), int(a[7])) if len(a) > 7 else (1080, 1920, 48)
bpy.ops.wm.read_factory_settings(use_empty=True); S = bpy.context.scene
PW, PH, R, D = 0.0716, 0.1476, 0.0112, 0.0082
def rrect_curve(name, w, h, r, depth, bevel):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'; cu.extrude = depth / 2
    cu.bevel_depth = bevel; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(17):
            t = math.radians(a0 + 90 * k / 16); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    sp.points.add(len(pts) - 1); sp.use_cyclic_u = True
    for i, (x, y) in enumerate(pts): sp.points[i].co = (x, y, 0, 1)
    o = bpy.data.objects.new(name, cu); S.collection.objects.link(o); return o
def principled(name, base, metal, rough, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.02
    if aniso: b.inputs["Anisotropic"].default_value = aniso
    return m
root = bpy.data.objects.new("phone", None); S.collection.objects.link(root)
body = rrect_curve("body", PW, PH, R, D - 0.0024, 0.0012); body.parent = root
body.data.materials.append(principled("titanium", (0.55, 0.54, 0.52), 1.0, 0.34, aniso=0.4))
glass = rrect_curve("glass", PW - 0.0012, PH - 0.0012, R - 0.0006, 0.0004, 0.0); glass.parent = root; glass.location = (0, 0, D / 2 + 0.0001)
glass.data.materials.append(principled("black_glass", (0.004, 0.004, 0.005), 0.0, 0.05, coat=1.0))
bpy.ops.mesh.primitive_plane_add(size=1.0); scr = bpy.context.active_object; scr.parent = root
scr.scale = (PW - 0.0052, (PW - 0.0052) * 2556 / 1179, 1); scr.location = (0, 0, D / 2 + 0.00035)
m = bpy.data.materials.new("screen"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial"); tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(UI)
import os
em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 0.0 if os.environ.get("PHONE_BLACK") else 1.15
gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.02
fr = nt.nodes.new("ShaderNodeFresnel"); fr.inputs[0].default_value = 1.5
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(tex.outputs[0], em.inputs[0]); nt.links.new(fr.outputs[0], mx.inputs[0]); nt.links.new(em.outputs[0], mx.inputs[1])
nt.links.new(gl.outputs[0], mx.inputs[2])
tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx2 = nt.nodes.new("ShaderNodeMixShader")      # rounded screen corners from the PNG alpha
nt.links.new(tex.outputs[1], mx2.inputs[0]); nt.links.new(tr.outputs[0], mx2.inputs[1]); nt.links.new(mx.outputs[0], mx2.inputs[2])
nt.links.new(mx2.outputs[0], out.inputs[0]); scr.data.materials.append(m)
# camera plateau on the back is hidden from the front view; side buttons
for i, (yy, ln) in enumerate(((0.030, 0.012), (0.012, 0.012), (0.045, 0.006))):
    bpy.ops.mesh.primitive_cube_add(size=1.0); b = bpy.context.active_object; b.parent = root
    b.scale = (0.0012, ln, 0.0026); b.location = (-PW / 2 - 0.0004, yy, 0); b.data.materials.append(body.data.materials[0])
root.matrix_world = Matrix.Rotation(math.radians(ROLL), 4, 'Y') @ Matrix.Rotation(math.radians(YAW), 4, 'Z') @ Matrix.Rotation(math.radians(90 - TILT), 4, 'X')
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.lens = 85; cam.location = (0, -0.62, 0.0); cam.rotation_euler = (math.radians(90), 0, 0)
def area(name, loc, sx, sy, power, col=(1, 1, 1)):
    l = bpy.data.objects.new(name, bpy.data.lights.new(name, 'AREA')); S.collection.objects.link(l)
    l.data.shape = 'RECTANGLE'; l.data.size = sx; l.data.size_y = sy; l.data.energy = power; l.data.color = col; l.location = loc
    l.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area("key", (-0.5, -0.6, 0.6), 0.6, 0.35, 14); area("strip", (0.55, -0.35, 0.05), 0.08, 0.8, 8, (0.92, 0.96, 1.0))
area("rim", (0.15, 0.5, 0.45), 0.4, 0.12, 12, (0.85, 0.92, 1.0)); area("red", (0, -0.3, -0.5), 0.6, 0.3, 4, (1.0, 0.1, 0.08))
wd = bpy.data.worlds.new("w"); S.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.015, 0.016, 0.02, 1)
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = SPP; S.cycles.use_denoising = True
S.render.film_transparent = True; S.render.resolution_x = RX; S.render.resolution_y = RY
S.view_settings.view_transform = 'Standard'; S.view_settings.look = 'None'
S.render.image_settings.color_mode = 'RGBA'; S.render.filepath = OUT; bpy.ops.render.render(write_still=True)
from bpy_extras.object_utils import world_to_camera_view as w2c
S.frame_set(1); hw, hh = scr.scale.x / 2, scr.scale.y / 2; cs = []
for x, y in ((-hw, hh), (hw, hh), (hw, -hh), (-hw, -hh)):
    p = w2c(S, cam, root.matrix_world @ Vector((x, y, D / 2 + 0.00035))); cs.append((round(p.x * RX, 2), round((1 - p.y) * RY, 2)))
print("SCREEN_CORNERS", cs)
print("PHONE_DONE")

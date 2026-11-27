"""Realistic Santa hat (Cycles): lofted velvet body on a drooping spine, particle-hair fur brim and pompom.
Rendered from the front on a transparent background for compositing onto the Turismo logo."""
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix, noise
OUT = sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
def node_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; return m, m.node_tree
# ---------------- velvet body: loft along a drooping spine
def spine(t):            # t 0..1 ; rises, then flops over to the left and down
    a = t * 1.0
    x = -1.45 * (t ** 2.2); z = 0.10 + 2.05 * math.sin(min(1, t * 1.15) * math.pi / 2) - 1.05 * max(0, t - 0.55) ** 1.6
    y = 0.10 * math.sin(t * math.pi)
    return Vector((x, y, z))
N_U, N_V = 64, 120
bm = bmesh.new(); rings = []
for i in range(N_V + 1):
    t = i / N_V; c = spine(t)
    tg = (spine(min(1, t + 1e-3)) - spine(max(0, t - 1e-3))).normalized()
    ref = Vector((0, 1, 0)); nx = tg.cross(ref).normalized(); ny = tg.cross(nx).normalized()
    r = 0.92 * (1 - t) ** 0.95 + 0.07
    ring = []
    for j in range(N_U):
        a = 2 * math.pi * j / N_U
        crease = 0.09 * math.exp(-((t - 0.52) / 0.07) ** 2) * max(0, math.cos(a - 1.2)) ** 2      # compression folds at the bend
        fold = (1 + 0.05 * math.sin(5 * a + 7 * t) * (1 - t) + 0.045 * noise.noise(Vector((math.cos(a) * 2.5, math.sin(a) * 2.5, t * 9)))
                - crease * (0.5 + 0.5 * math.sin(26 * t + 3 * a)))
        ring.append(bm.verts.new(c + (nx * math.cos(a) + ny * math.sin(a)) * r * fold))
    rings.append(ring)
for r0, r1 in zip(rings[:-1], rings[1:]):
    for j in range(N_U):
        bm.faces.new((r0[j], r0[(j + 1) % N_U], r1[(j + 1) % N_U], r1[j]))
me = bpy.data.meshes.new("hat_body"); bm.to_mesh(me); bm.free()
for p in me.polygons: p.use_smooth = True
body = bpy.data.objects.new("hat_body", me); S.collection.objects.link(body)
sub = body.modifiers.new("sub", 'SUBSURF'); sub.levels = 1; sub.render_levels = 2
m, nt = node_mat("velvet_red"); b = nt.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.30, 0.003, 0.008, 1); b.inputs["Roughness"].default_value = 0.78
b.inputs["Sheen Weight"].default_value = 0.5; b.inputs["Sheen Roughness"].default_value = 0.3; b.inputs["Sheen Tint"].default_value = (1.0, 0.18, 0.2, 1)
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180; nz.inputs["Detail"].default_value = 8
bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.45; bp.inputs["Distance"].default_value = 0.004
nt.links.new(nz.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
me.materials.append(m)
# ---------------- fur parts
def fur_mat():
    m, nt = node_mat("fur_white"); nt.nodes.clear()
    h = nt.nodes.new("ShaderNodeBsdfHairPrincipled"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    h.parametrization = 'MELANIN'; h.inputs["Melanin"].default_value = 0.02; h.inputs["Melanin Redness"].default_value = 0.3
    h.inputs["Roughness"].default_value = 0.45; h.inputs["Random Color"].default_value = 0.15; h.inputs["Random Roughness"].default_value = 0.3
    nt.links.new(h.outputs[0], o.inputs[0]); return m
def base_mat():
    m, nt = node_mat("fur_base"); b = nt.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.82, 0.82, 0.80, 1); b.inputs["Roughness"].default_value = 1.0
    return m
FUR, FURB = fur_mat(), base_mat()
def add_fur(ob, count, length, kids=12):
    ob.data.materials.append(FURB); ob.data.materials.append(FUR)
    bpy.context.view_layer.objects.active = ob
    md = ob.modifiers.new("fur", 'PARTICLE_SYSTEM'); ps = ob.particle_systems[0].settings
    ps.type = 'HAIR'; ps.count = count; ps.hair_length = length; ps.material_slot = "fur_white"
    ps.use_advanced_hair = False
    ps.child_type = 'INTERPOLATED'; ps.child_percent = kids; ps.rendered_child_count = kids
    ps.clump_factor = 0.15; ps.roughness_1 = 0.02; ps.roughness_2 = 0.03; ps.roughness_endpoint = 0.02
    ps.root_radius = 1.0; ps.tip_radius = 0.0; ps.radius_scale = 0.0035; ps.length_random = 0.45
    ps.kink = 'CURL'; ps.kink_amplitude = 0.004; ps.kink_frequency = 3.0
# brim: fat torus around the hat opening
bpy.ops.mesh.primitive_torus_add(major_radius=0.98, minor_radius=0.22, major_segments=96, minor_segments=24, location=(0, 0, 0.12))
brim = bpy.context.active_object; brim.name = "hat_brim"; brim.scale = (1.0, 1.0, 0.95)
for v in brim.data.vertices: v.co += v.co.normalized() * 0.02 * noise.noise(v.co * 4)
for p in brim.data.polygons: p.use_smooth = True
add_fur(brim, 9000, 0.11)
# pompom at the tip
tip = spine(1.0)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=0.24, location=tip + Vector((-0.05, 0, -0.10)))
pom = bpy.context.active_object; pom.name = "hat_pompom"
for p in pom.data.polygons: p.use_smooth = True
add_fur(pom, 3500, 0.13)
# ---------------- camera, lights, render
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.lens = 85; cam.location = (-0.35, -11.0, 3.2); cam.rotation_euler = (math.radians(82), 0, 0)
def area(name, loc, size, power, color=(1, 1, 1)):
    l = bpy.data.objects.new(name, bpy.data.lights.new(name, 'AREA')); S.collection.objects.link(l)
    l.data.size = size; l.data.energy = power; l.data.color = color; l.location = loc
    d = (Vector((-0.4, 0, 1.0)) - Vector(loc)); l.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return l
area("key", (-5, -6, 7), 5, 1700); area("fill", (6, -5, 2), 6, 380, (0.9, 0.95, 1.0)); area("rim", (1, 6, 5), 3, 1300)
w = bpy.data.worlds.new("w"); S.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = int(__import__("os").environ.get("HAT_SPP", 96)); S.cycles.use_denoising = True
S.render.film_transparent = True; S.render.resolution_x = S.render.resolution_y = int(__import__("os").environ.get("HAT_RES", 1400))
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGBA'
S.view_settings.view_transform = 'Standard'; S.view_settings.look = 'None'
S.render.filepath = OUT; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".png", ".blend"))
print("HAT_DONE")

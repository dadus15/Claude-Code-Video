# Turismo Wheels - Audi RS5 8W + Turismo Forged V05 (brushed) - scena v2 wg analizy klatka po klatce
# Kamera: przedni LEWY narozkik, ~15 cm nad ziemia, patrzy DO TYLU na przednie lewe kolo (CAM-RIG).
# Os czasu (24 fps, 311 kl.): P0 postoj (L) | P1 cofanie 0.4-2.4 s | P2 stop | P3 skret L->P 3.1-5.1 s | P4 pauza | P5 jazda w przod od 5.9 s
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon

S = bpy.context.scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for d in list(coll):
        if d.users == 0:
            coll.remove(d)

def col(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in S.collection.children:
        S.collection.children.link(c)
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    return c
C_WHEEL, C_CAR, C_ENV, C_RIG = col("WHEEL"), col("CAR"), col("ENV"), col("RIG")

def link(o, c):
    c.objects.link(o); return o

def empty(name, c, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); e.empty_display_size = 0.1
    link(e, c); e.parent = parent; e.location = loc; e.rotation_euler = rot
    return e

def mat(name, base, metal=0.0, rough=0.5, coat=0.0, coat_rough=0.03, aniso=0.0, emit=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    if aniso:
        b.inputs["Anisotropic"].default_value = aniso
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = 6.0
    return m

M = {
    "brushed": mat("M_V05_brushed_aluminium", (0.58, 0.59, 0.61), 1.0, 0.27, aniso=0.7),
    "brushed_dark": mat("M_V05_chamfer", (0.42, 0.43, 0.45), 1.0, 0.16),
    "lip": mat("M_V05_lip_polished", (0.78, 0.78, 0.80), 1.0, 0.06),
    "barrel": mat("M_barrel_inner", (0.05, 0.05, 0.055), 0.8, 0.3),
    "slot": mat("M_slot_shadow", (0.006, 0.006, 0.007), 0.0, 0.7),
    "cap": mat("M_cap_brushed", (0.55, 0.56, 0.58), 1.0, 0.22, aniso=0.5),
    "bolt": mat("M_bolt_black", (0.03, 0.03, 0.035), 0.9, 0.25),
    "paint": mat("M_RS5_matte_black_wrap", (0.018, 0.018, 0.02), 0.25, 0.48, coat=0.2, coat_rough=0.35),
    "trim": mat("M_trim_black", (0.012, 0.012, 0.014), 0.0, 0.5),
    "gloss_black": mat("M_gloss_black", (0.01, 0.01, 0.012), 0.0, 0.08, coat=1.0),
    "carbon": mat("M_carbon", (0.03, 0.03, 0.035), 0.3, 0.22, coat=1.0),
    "headlight": mat("M_headlight_lens", (0.05, 0.055, 0.06), 0.6, 0.05, coat=1.0),
    "drl": mat("M_drl_led", (0.9, 0.95, 1.0), 0.0, 0.3, emit=(0.85, 0.92, 1.0)),
    "caliper": mat("M_caliper_red", (0.55, 0.02, 0.015), 0.0, 0.25, coat=1.0),
    "disc": mat("M_disc_drilled", (0.38, 0.38, 0.39), 0.9, 0.35),
    "post": mat("M_post", (0.35, 0.36, 0.38), 0.7, 0.4),
    "bldg": mat("M_building", (0.72, 0.72, 0.74), 0.0, 0.85),
    "bldg_dark": mat("M_building_windows", (0.15, 0.16, 0.18), 0.2, 0.3),
    "tree": mat("M_tree_bare", (0.10, 0.08, 0.07), 0.0, 0.9),
    "snowbank": mat("M_snowbank", (0.88, 0.90, 0.93), 0.0, 0.6),
}

# tyre: rubber + tread blocks (angle-based bump)
mt = bpy.data.materials.new("M_tyre"); mt.use_nodes = True; nt = mt.node_tree
bs = nt.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = (0.02, 0.02, 0.022, 1); bs.inputs["Roughness"].default_value = 0.7
tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
an = nt.nodes.new("ShaderNodeMath"); an.operation = "ARCTAN2"; nt.links.new(sp.outputs["Y"], an.inputs[0]); nt.links.new(sp.outputs["X"], an.inputs[1])
mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = 95.0; nt.links.new(an.outputs[0], mu.inputs[0])
zk = nt.nodes.new("ShaderNodeMath"); zk.operation = "MULTIPLY"; zk.inputs[1].default_value = 55.0; nt.links.new(sp.outputs["Z"], zk.inputs[0])
ad = nt.nodes.new("ShaderNodeMath"); ad.operation = "ADD"; nt.links.new(mu.outputs[0], ad.inputs[0]); nt.links.new(zk.outputs[0], ad.inputs[1])
si = nt.nodes.new("ShaderNodeMath"); si.operation = "SINE"; nt.links.new(ad.outputs[0], si.inputs[0])
gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.5; nt.links.new(si.outputs[0], gt.inputs[0])
bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.45; bp.inputs["Distance"].default_value = 0.004
nt.links.new(gt.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bs.inputs["Normal"])
M["tyre"] = mt

# packed snow / ice ground
ms = bpy.data.materials.new("M_snow_ground"); ms.use_nodes = True; nt = ms.node_tree
bs = nt.nodes["Principled BSDF"]; bs.inputs["Roughness"].default_value = 0.55
tc = nt.nodes.new("ShaderNodeTexCoord")
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0; nz.inputs["Detail"].default_value = 10.0
nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
rp = nt.nodes.new("ShaderNodeValToRGB")
rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[0].color = (0.42, 0.45, 0.50, 1)   # compacted grey ice
rp.color_ramp.elements[1].position = 0.62; rp.color_ramp.elements[1].color = (0.88, 0.90, 0.94, 1)   # fresh snow
nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"]); nt.links.new(rp.outputs["Color"], bs.inputs["Base Color"])
fn = nt.nodes.new("ShaderNodeTexNoise"); fn.inputs["Scale"].default_value = 160.0; fn.inputs["Detail"].default_value = 8.0
nt.links.new(tc.outputs["Object"], fn.inputs["Vector"])
b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.5; b2.inputs["Distance"].default_value = 0.004
nt.links.new(fn.outputs["Fac"], b2.inputs["Height"]); nt.links.new(b2.outputs["Normal"], bs.inputs["Normal"])
M["snow"] = ms

# ---------------------------------------------------------------- helpers
def lathe(name, prof, c, material, steps=128, angle=2 * math.pi, start=0.0, smooth=True):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((r * math.cos(start), r * math.sin(start), z)) for r, z in prof]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    full = abs(angle - 2 * math.pi) < 1e-6
    res = bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=angle, steps=steps, use_duplicate=False)
    if full:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    else:
        last = [e for e in res["geom_last"] if isinstance(e, bmesh.types.BMEdge)]
        try:
            bmesh.ops.edgenet_fill(bm, edges=es); bmesh.ops.edgenet_fill(bm, edges=last)
        except Exception:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), c); o.data.materials.append(material)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    return o

def loft(name, sections, c, material, cap=True, closed=True):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    rings = [[bm.verts.new(v) for v in sec] for sec in sections]
    n = len(sections[0]); m = n if closed else n - 1
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(m):
            bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cap:
        bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), c); o.data.materials.append(material)
    return o

def bevel(o, w=0.0012, seg=2, ang=30):
    m = o.modifiers.new("Bevel", "BEVEL"); m.width = w; m.segments = seg
    m.limit_method = "ANGLE"; m.angle_limit = math.radians(ang); return m

def extrude_polys(name, loops, zfront, depth, c, mats):
    """loops: [outer, hole1, hole2...] lists of (x,y). zfront(x,y)->z. Builds a solid plate with holes."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    front, back = [], []
    for lp in loops:
        front.append([bm.verts.new((x, y, zfront(x, y))) for x, y in lp])
        back.append([bm.verts.new((x, y, zfront(x, y) - depth)) for x, y in lp])
    flat = [v for lp in front for v in lp]
    tris = tessellate_polygon([[Vector((x, y, 0)) for x, y in lp] for lp in loops])
    flatb = [v for lp in back for v in lp]
    for t in tris:
        try:
            bm.faces.new((flat[t[0]], flat[t[1]], flat[t[2]]))
        except ValueError:
            pass
        try:
            f = bm.faces.new((flatb[t[2]], flatb[t[1]], flatb[t[0]])); f.material_index = 1
        except ValueError:
            pass
    for F, B in zip(front, back):
        n = len(F)
        for i in range(n):
            f = bm.faces.new((F[i], B[i], B[(i + 1) % n], F[(i + 1) % n])); f.material_index = 1
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), c)
    for mm in mats:
        o.data.materials.append(mm)
    return o

# ---------------------------------------------------------------- rig (car origin = ground under front axle centre)
R_TYRE = 0.349                      # 275/30 R21
TRACK_HALF = 0.80                    # front-left wheel centre plane
RIG = empty("RIG_car", C_RIG)
STEER = empty("RIG_steer_FL", C_RIG, RIG, (-TRACK_HALF, 0.0, R_TYRE))
SPIN = empty("RIG_spin_FL", C_RIG, STEER)
# wheel built with axis local +Z = outer face; left wheel -> outer face looks -X  (R_y(-90): +Z -> -X, +X -> +Z, +Y -> +Y)
OFF = 0.118
ORI_S = empty("RIG_orient_spin", C_RIG, SPIN, (-OFF, 0, 0), (0, math.radians(-90), 0))
ORI_F = empty("RIG_orient_fixed", C_RIG, STEER, (-OFF, 0, 0), (0, math.radians(-90), 0))
def to_wheel(o, spinning=True):
    o.parent = ORI_S if spinning else ORI_F; return o

# ---------------------------------------------------------------- V05 wheel (21", 2-piece, slotted face ring)
# barrel + thin polished outer lip edge
barrel = [(0.2600, 0.004), (0.2700, 0.008), (0.2790, 0.006), (0.2805, -0.004), (0.2720, -0.014), (0.2680, -0.018),
          (0.2680, -0.100), (0.2560, -0.115), (0.2560, -0.200), (0.2680, -0.215), (0.2680, -0.232), (0.2760, -0.236),
          (0.2780, -0.246), (0.2580, -0.246), (0.2500, -0.232), (0.2460, -0.215), (0.2460, -0.115), (0.2520, -0.060),
          (0.2560, -0.002)]
to_wheel(lathe("WHL_barrel_lip", barrel, C_WHEEL, M["lip"], steps=200))
to_wheel(lathe("WHL_barrel_inner", [(0.2450, -0.060), (0.2500, -0.060), (0.2450, -0.215), (0.2400, -0.215)], C_WHEEL, M["barrel"], steps=160))
# wide brushed face ring (carries the slots) r 0.226..0.262, front surface ~ -0.010
ring = [(0.2240, -0.016), (0.2600, -0.004), (0.2620, -0.010), (0.2620, -0.040), (0.2240, -0.040), (0.2215, -0.024)]
o_ring = to_wheel(lathe("WHL_face_ring", ring, C_WHEEL, M["brushed"], steps=240))
# 34 slanted rectangular slots on the ring (dark recessed windows)
me = bpy.data.meshes.new("WHL_ring_slots"); bm = bmesh.new()
NS = 34
for k in range(NS):
    a = 2 * math.pi * k / NS
    rr = 0.2435
    cx, cy = rr * math.cos(a), rr * math.sin(a)
    u = Vector((math.cos(a), math.sin(a), 0)); t = Vector((-math.sin(a), math.cos(a), 0))
    # slot: 0.020 radial x 0.0075 tangential, skewed 28 deg
    sk = math.radians(28)
    du = u * 0.010; dt = (t * math.cos(sk) + u * math.sin(sk)) * 0.0038
    corners = [Vector((cx, cy, 0)) + s1 * du + s2 * dt for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    def zring(px, py):
        r = math.hypot(px, py); return -0.016 + (r - 0.224) / 0.036 * 0.012 + 0.0005
    top = [bm.verts.new((p.x, p.y, zring(p.x, p.y))) for p in corners]
    bot = [bm.verts.new((p.x, p.y, -0.030)) for p in corners]
    bm.faces.new(top)
    for i in range(4):
        bm.faces.new((top[i], bot[i], bot[(i + 1) % 4], top[(i + 1) % 4]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
slots = link(bpy.data.objects.new("WHL_ring_slots", me), C_WHEEL); slots.data.materials.append(M["slot"]); to_wheel(slots)

# hub
hub = [(0.0, -0.022), (0.045, -0.022), (0.070, -0.027), (0.086, -0.036), (0.090, -0.050), (0.090, -0.090), (0.0, -0.090)]
to_wheel(lathe("WHL_hub", hub, C_WHEEL, M["brushed"], steps=96))
# 5 directional spokes: elongated triangle widening clockwise, hammer-head tip, big triangular window + small tip window
def pol(r, deg):
    return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
OUT = [(0.080, 9), (0.150, 6), (0.205, 7), (0.232, 8), (0.236, 2), (0.236, -30), (0.226, -31),
       (0.205, -26), (0.150, -14), (0.080, -8)]
WIN1 = [(0.118, -1), (0.195, 2), (0.195, -16)]                      # main triangular window
WIN2 = [(0.208, -3), (0.226, -3), (0.226, -25), (0.209, -21)]       # small window at the hammer-head
def zf_spoke(x, y):
    r = math.hypot(x, y); t = max(0.0, min(1.0, (r - 0.08) / 0.155))
    return -0.020 - 0.018 * t + 0.010 * math.sin(math.pi * t)       # slightly domed, recessing toward the ring
for k in range(5):
    base = 72 * k
    loops = [[pol(r, d + base) for r, d in OUT],
             [pol(r, d + base) for r, d in WIN1],
             [pol(r, d + base) for r, d in WIN2]]
    o = extrude_polys(f"WHL_spoke_{k}", loops, zf_spoke, 0.030, C_WHEEL, [M["brushed"], M["brushed_dark"]])
    bevel(o, 0.0022, 2, 30)
    to_wheel(o)
# lug bolts (5x112) + centre cap with brushed face
for k in range(5):
    a = 2 * math.pi * k / 5 + math.radians(36)
    ob = lathe(f"WHL_bolt_{k}", [(0.0, -0.015), (0.0100, -0.015), (0.0112, -0.019), (0.0112, -0.030), (0.0, -0.030)], C_WHEEL, M["bolt"], steps=6, smooth=False)
    ob.location = (0.056 * math.cos(a), 0.056 * math.sin(a), 0); to_wheel(ob)
to_wheel(lathe("WHL_cap", [(0.0, -0.010), (0.028, -0.012), (0.034, -0.016), (0.036, -0.024), (0.0, -0.024)], C_WHEEL, M["cap"], steps=64))

# tyre 275/30 R21
tp = [(0.2680, 0.004), (0.2860, 0.016), (0.3130, 0.0235), (0.3360, 0.0215), (0.3450, 0.0140), (0.3490, 0.0040),
      (0.3490, -0.0240), (0.3430, -0.0260), (0.3430, -0.0360), (0.3490, -0.0380), (0.3490, -0.0790), (0.3430, -0.0810),
      (0.3430, -0.0910), (0.3490, -0.0930), (0.3490, -0.1430), (0.3430, -0.1450), (0.3430, -0.1550), (0.3490, -0.1570),
      (0.3490, -0.2000), (0.3430, -0.2020), (0.3430, -0.2120), (0.3490, -0.2140), (0.3490, -0.2400), (0.3450, -0.2500),
      (0.3360, -0.2575), (0.3130, -0.2595), (0.2860, -0.2520), (0.2680, -0.2400), (0.2620, -0.2300), (0.2620, -0.0060)]
to_wheel(lathe("WHL_tyre", tp, C_WHEEL, M["tyre"], steps=256))
# brakes: drilled disc spins, red caliper fixed at rear-top (local angle -35 deg -> world up/rear)
to_wheel(lathe("BRK_disc", [(0.090, -0.130), (0.200, -0.130), (0.200, -0.165), (0.090, -0.165)], C_WHEEL, M["disc"], steps=128))
oc = lathe("BRK_caliper", [(0.145, -0.088), (0.236, -0.088), (0.240, -0.098), (0.240, -0.195), (0.145, -0.195)], C_WHEEL, M["caliper"],
           steps=24, angle=math.radians(66), start=math.radians(-35 - 33))
bevel(oc, 0.005, 3, 30); to_wheel(oc, spinning=False)

# ---------------------------------------------------------------- RS5 8W front-left quarter (simplified, matte black)
ARCH_C = (0.0, R_TYRE + 0.020); ARCH_R = 0.392
def body_x(y, z):
    """left side surface x (negative). Wide RS fender flare around the arch, bumper wrap at the front, tumblehome."""
    x = -0.935
    d = math.hypot(y - ARCH_C[0], z - ARCH_C[1])
    x -= 0.035 * math.exp(-((d - ARCH_R - 0.06) / 0.11) ** 2) * (1.0 if z > 0.18 else 0.6)   # flare
    x += 0.11 * max(0.0, (z - 0.62) / 0.20) ** 2                                                # shoulder tuck
    x += 0.05 * max(0.0, (0.24 - z) / 0.10) ** 2                                                # rocker tuck
    if y > 0.55:
        x += 2.2 * (y - 0.55) ** 2                                                              # bumper corner wraps inward
    if y < -2.2:
        x += 0.25 * (-2.2 - y) ** 2
    return x
ny, nz = 140, 46
y0, y1, z0, z1 = -2.7, 0.98, 0.14, 0.80
me = bpy.data.meshes.new("CAR_body_side"); bm = bmesh.new(); grid = []
for j in range(nz + 1):
    grid.append([bm.verts.new((body_x(y0 + (y1 - y0) * i / ny, z0 + (z1 - z0) * j / nz),
                                y0 + (y1 - y0) * i / ny, z0 + (z1 - z0) * j / nz)) for i in range(ny + 1)])
for j in range(nz):
    for i in range(ny):
        a, b, c_, d = grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]
        cy = (a.co.y + c_.co.y) / 2; cz = (a.co.z + c_.co.z) / 2
        if math.hypot(cy - ARCH_C[0], cz - ARCH_C[1]) < ARCH_R:
            continue
        bm.faces.new((d, c_, b, a))
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
for v in bm.verts:
    if v.is_boundary:
        dy, dz = v.co.y - ARCH_C[0], v.co.z - ARCH_C[1]; dd = math.hypot(dy, dz)
        if dd < ARCH_R + 0.04 and v.co.z > 0.145 and -0.6 < v.co.y < 0.6:
            v.co.y = ARCH_C[0] + dy / dd * ARCH_R; v.co.z = ARCH_C[1] + dz / dd * ARCH_R; v.co.x = body_x(v.co.y, v.co.z)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
body = link(bpy.data.objects.new("CAR_body_side", me), C_CAR); body.data.materials.append(M["paint"]); body.parent = RIG
for p in body.data.polygons:
    p.use_smooth = True
s = body.modifiers.new("Solidify", "SOLIDIFY"); s.thickness = 0.004; s.offset = 1
# hood / top surface (visible at top-left of frame)
hood = bpy.data.meshes.new("CAR_hood"); bm = bmesh.new(); g = []
for j in range(13):
    xx = -0.84 + 0.84 * j / 12
    g.append([bm.verts.new((xx, -0.9 + 1.88 * i / 30, 0.80 + 0.04 * (1 - (xx / 0.84) ** 2) - 0.10 * max(0, (-0.9 + 1.88 * i / 30 - 0.4)) ** 1.5)) for i in range(31)])
for j in range(12):
    for i in range(30):
        bm.faces.new((g[j][i], g[j][i + 1], g[j + 1][i + 1], g[j + 1][i]))
bm.to_mesh(hood); bm.free()
ho = link(bpy.data.objects.new("CAR_hood", hood), C_CAR); ho.data.materials.append(M["paint"]); ho.parent = RIG
for p in ho.data.polygons:
    p.use_smooth = True
# arch lip, liner, underbody, side skirt (carbon), door gap, mirror
fl = []
for i in range(81):
    a = math.radians(-8 + 196 * i / 80)
    yy = ARCH_C[0] + math.cos(a) * ARCH_R; zz = ARCH_C[1] + math.sin(a) * ARCH_R
    if zz < 0.15:
        continue
    xo = body_x(yy, zz); n = Vector((0, math.cos(a), math.sin(a)))
    fl.append([Vector((xo, yy, zz)), Vector((xo - 0.006, yy, zz)) + n * 0.014, Vector((xo + 0.05, yy, zz)) + n * 0.018, Vector((xo + 0.055, yy, zz))])
lip = loft("CAR_arch_lip", fl, C_CAR, M["paint"], cap=False, closed=False); lip.parent = RIG
lp = []
for i in range(81):
    a = math.radians(-12 + 204 * i / 80)
    yy = math.cos(a) * (ARCH_R + 0.004); zz = ARCH_C[1] + math.sin(a) * (ARCH_R + 0.004)
    lp.append([Vector((-0.93, yy, zz)), Vector((-0.50, yy, zz)), Vector((-0.50, yy * 1.05, ARCH_C[1] + (zz - ARCH_C[1]) * 1.05)),
               Vector((-0.93, yy * 1.05, ARCH_C[1] + (zz - ARCH_C[1]) * 1.05))])
ln = loft("CAR_arch_liner", lp, C_CAR, M["trim"], cap=False); ln.parent = RIG
ub = bpy.data.meshes.new("CAR_underbody"); ub.from_pydata([(-0.92, -2.7, 0.14), (-0.92, 0.95, 0.14), (0.9, 0.95, 0.14), (0.9, -2.7, 0.14)], [], [(0, 1, 2, 3)])
ubo = link(bpy.data.objects.new("CAR_underbody", ub), C_CAR); ubo.data.materials.append(M["trim"]); ubo.parent = RIG
def box(name, size, loc, material, c=C_ENV, rot=(0, 0, 0), parent=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), c); o.scale = size; o.location = loc; o.rotation_euler = rot
    o.data.materials.append(material); o.parent = parent; return o
sk = box("CAR_side_skirt_carbon", (0.07, 1.95, 0.07), (-0.94, -1.45, 0.175), M["carbon"], C_CAR, parent=RIG)
bevel(sk, 0.012, 3, 40)
box("CAR_door_gap", (0.004, 0.004, 0.52), (body_x(-0.62, 0.48) - 0.002, -0.62, 0.48), M["trim"], C_CAR, parent=RIG)
mir = box("CAR_mirror", (0.12, 0.20, 0.10), (-1.03, -0.88, 0.98), M["gloss_black"], C_CAR, rot=(0, 0, math.radians(-12)), parent=RIG)
bevel(mir, 0.03, 4, 30)
box("CAR_mirror_arm", (0.10, 0.04, 0.03), (-0.97, -0.84, 0.93), M["gloss_black"], C_CAR, parent=RIG)
# headlight (top-left of frame) + DRL strip, bumper side intake (honeycomb black)
hl = box("CAR_headlight", (0.16, 0.42, 0.075), (-0.73, 0.70, 0.705), M["headlight"], C_CAR, rot=(math.radians(-8), 0, math.radians(14)), parent=RIG)
bevel(hl, 0.02, 3, 30)
box("CAR_headlight_drl", (0.012, 0.36, 0.010), (-0.808, 0.68, 0.672), M["drl"], C_CAR, rot=(math.radians(-8), 0, math.radians(14)), parent=RIG)
box("CAR_bumper_intake", (0.06, 0.30, 0.20), (-0.80, 0.82, 0.32), M["trim"], C_CAR, rot=(0, 0, math.radians(35)), parent=RIG)

# ---------------------------------------------------------------- environment: overcast snowy lot
gm = bpy.data.meshes.new("ENV_ground"); bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=150.0); bm.to_mesh(gm); bm.free()
go = link(bpy.data.objects.new("ENV_ground", gm), C_ENV); go.data.materials.append(M["snow"])
rnd = random.Random(7)
# tyre tracks in the snow (darker compacted bands) - strong parallax/motion cues
mtrk = mat("M_tyre_tracks", (0.30, 0.32, 0.36), 0.0, 0.45)
for i in range(26):
    ang = rnd.uniform(-0.6, 0.6); L = rnd.uniform(6, 18); x = rnd.uniform(-9, 9); y = rnd.uniform(-14, 20)
    box(f"ENV_track_{i:02d}", (0.22, L, 0.003), (x, y, 0.0015), mtrk, rot=(0, 0, ang))
# ice chunks / snow lumps near the car
for i in range(60):
    me = bpy.data.meshes.new(f"ENV_lump_{i}"); bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(f"ENV_lump_{i}", me), C_ENV); s = rnd.uniform(0.03, 0.12)
    o.scale = (s, s * rnd.uniform(0.8, 1.6), s * 0.45); o.location = (rnd.uniform(-6, 4), rnd.uniform(-10, 12), s * 0.15)
    o.rotation_euler = (0, 0, rnd.uniform(0, 6.3)); o.data.materials.append(M["snowbank"])
# snowbanks around the lot
for i, (x, y, L, rz) in enumerate([(-14, 4, 40, 0), (16, 8, 40, 0.1), (0, 32, 40, 1.57), (0, -26, 40, 1.57)]):
    o = box(f"ENV_snowbank_{i}", (2.6, L, 1.4), (x, y, 0.3), M["snowbank"], rot=(0, 0, rz)); bevel(o, 0.9, 4, 30)
# apartment blocks + bare trees far away, a few lamp posts for parallax
for i in range(7):
    w, h = rnd.uniform(14, 26), rnd.uniform(12, 24)
    x, y = rnd.choice([-1, 1]) * rnd.uniform(45, 90), rnd.uniform(-60, 90)
    box(f"ENV_block_{i}", (w, 12, h), (x, y, h / 2), M["bldg"])
    for r in range(int(h // 3)):
        box(f"ENV_block_{i}_win_{r}", (w * 0.9, 12.05, 0.9), (x, y, 1.6 + r * 3.0), M["bldg_dark"])
for i in range(40):
    x = rnd.choice([-1, 1]) * rnd.uniform(22, 40); y = rnd.uniform(-40, 60); h = rnd.uniform(5, 10)
    box(f"ENV_tree_{i}", (0.18, 0.18, h), (x, y, h / 2), M["tree"], rot=(rnd.uniform(-.05, .05), rnd.uniform(-.05, .05), 0))
for i, (x, y) in enumerate([(-7.5, -9.0), (-8.5, -24.0), (6.5, -16.0), (-9.0, 14.0)]):
    box(f"ENV_lamp_post_{i}", (0.12, 0.12, 9.0), (x, y, 4.5), M["post"])
    box(f"ENV_lamp_arm_{i}", (1.6, 0.08, 0.08), (x + 0.75, y, 8.9), M["post"])
    box(f"ENV_lamp_head_{i}", (0.55, 0.22, 0.10), (x + 1.5, y, 8.8), M["post"])

# world: bright overcast, soft clouds
W = bpy.data.worlds.get("World") or bpy.data.worlds.new("World"); S.world = W; W.use_nodes = True; nt = W.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground"); nt.links.new(bg.outputs[0], out.inputs[0])
tc = nt.nodes.new("ShaderNodeTexCoord"); sz = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sz.inputs[0])
gr = nt.nodes.new("ShaderNodeValToRGB")
gr.color_ramp.elements[0].position = 0.48; gr.color_ramp.elements[0].color = (0.90, 0.91, 0.93, 1)
gr.color_ramp.elements[1].position = 0.95; gr.color_ramp.elements[1].color = (0.70, 0.74, 0.80, 1)
nt.links.new(sz.outputs["Z"], gr.inputs["Fac"])
cl = nt.nodes.new("ShaderNodeTexNoise"); cl.inputs["Scale"].default_value = 2.4; cl.inputs["Detail"].default_value = 8.0
nt.links.new(tc.outputs["Generated"], cl.inputs["Vector"])
cr = nt.nodes.new("ShaderNodeValToRGB")
cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[0].color = (0, 0, 0, 1)
cr.color_ramp.elements[1].position = 0.65; cr.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(cl.outputs["Fac"], cr.inputs["Fac"])
mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.inputs["B"].default_value = (0.62, 0.65, 0.70, 1)
nt.links.new(cr.outputs["Color"], mx.inputs["Factor"]); nt.links.new(gr.outputs["Color"], mx.inputs["A"]); nt.links.new(mx.outputs["Result"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.25
sun = bpy.data.lights.new("LGT_soft_sun", "SUN"); sun.energy = 1.6; sun.angle = math.radians(40)
so = link(bpy.data.objects.new("LGT_soft_sun", sun), C_ENV); so.rotation_euler = (math.radians(55), 0, math.radians(200))

# ---------------------------------------------------------------- camera: rigid on the front-left corner, looking rearward
cam = bpy.data.cameras.new("CAM_rig"); cam.lens = 16.0; cam.sensor_width = 36.0; cam.sensor_fit = "HORIZONTAL"; cam.clip_start = 0.02
co = link(bpy.data.objects.new("CAM_rig", cam), C_RIG); co.parent = RIG
CAM_LOC = Vector((-1.05, 0.78, 0.16)); CAM_TGT = Vector((-0.86, -0.25, 0.42)); CAM_ROLL = 7.0
def place_cam(loc, tgt, roll_deg):
    q = (tgt - loc).to_track_quat("-Z", "Y")
    co.matrix_parent_inverse = Matrix.Identity(4)
    co.matrix_basis = Matrix.Translation(loc) @ q.to_matrix().to_4x4() @ Matrix.Rotation(math.radians(roll_deg), 4, "Z")
place_cam(CAM_LOC, CAM_TGT, CAM_ROLL)
S.camera = co

# ---------------------------------------------------------------- render basics
S.render.resolution_x = 1080; S.render.resolution_y = 1920; S.render.resolution_percentage = 40
S.render.fps = 24; S.frame_start = 1; S.frame_end = 311
S.view_settings.view_transform = "AgX"
try:
    S.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
S.render.engine = "BLENDER_EEVEE"; S.eevee.taa_render_samples = 1

# ---------------------------------------------------------------- animation (exact phase timing from the reference analysis)
FPS = 24
def fr(t):  # seconds -> frame (1-based)
    return 1 + round(t * FPS)
def sstep(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
LOCK_L, LOCK_R = math.radians(34), math.radians(-34)    # +Z rotation = steer left
V_REV, V_FWD = 0.80, 1.15                                 # m/s (reverse peak, forward cruise)
def speed(t):
    if 0.40 <= t < 2.40:                                  # reverse bell: ease in to 1.0 s, ease out to 2.4 s
        return -V_REV * (sstep((t - 0.40) / 0.60) if t < 1.0 else 1 - sstep((t - 1.0) / 1.40))
    if t >= 5.90:                                         # forward: accelerate to 8.5 s, then slight rise
        return V_FWD * sstep((t - 5.90) / 2.60) * (1.0 + 0.08 * max(0.0, (t - 8.5) / 4.45))
    return 0.0
def steer(t):
    if t < 3.10:
        return LOCK_L
    if t < 5.10:
        return LOCK_L + (LOCK_R - LOCK_L) * sstep((t - 3.10) / 2.00)
    return LOCK_R
WHEELBASE = 2.77
pos = Vector((0, 0, 0)); yaw = 0.0; dist = 0.0
for f in range(1, 312):
    t = (f - 1) / FPS
    v = speed(t); d = v / FPS; st = steer(t)
    dist += d
    yaw += d * math.tan(st) / WHEELBASE * 0.55             # bicycle model, damped (reference shows gentle turn)
    pos += Vector((-math.sin(yaw), math.cos(yaw), 0)) * d
    RIG.location = pos; RIG.rotation_euler = (0, 0, yaw)
    RIG.keyframe_insert("location", frame=f); RIG.keyframe_insert("rotation_euler", frame=f)
    SPIN.rotation_euler = (-dist / R_TYRE, 0, 0); SPIN.keyframe_insert("rotation_euler", frame=f)
    STEER.rotation_euler = (0, 0, st); STEER.keyframe_insert("rotation_euler", frame=f)
    # camera mount sag (reference: mirror drifts ~5% of width between 2 s and 6 s, back by 8 s)
    sag = 1.4 * (sstep((t - 2.0) / 4.0) - sstep((t - 6.0) / 2.0))
    place_cam(CAM_LOC, CAM_TGT + Vector((0, 0, 0)), CAM_ROLL)
    co.matrix_basis = co.matrix_basis @ Matrix.Rotation(math.radians(sag), 4, "Y")
    co.keyframe_insert("location", frame=f); co.keyframe_insert("rotation_euler", frame=f)
for o in (RIG, SPIN, STEER, co):
    if o.animation_data and o.animation_data.action:
        try:
            for fc in o.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
        except Exception:
            pass
S.frame_set(1)
result = {"objects": len(bpy.data.objects), "travel_m": round(dist, 2), "yaw_deg": round(math.degrees(yaw), 1),
          "end_pos": [round(pos.x, 2), round(pos.y, 2)]}

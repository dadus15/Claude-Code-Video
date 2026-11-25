# Turismo Wheels - RS6 C7 "Wheel Reveal" - scena 3D Jutsu (bpy 5.2)
# Felga one-off "KONCEPT 2" wg szkicu projektantki: 10 szprych z fioletowymi insertami,
# 10 insertow na pierscieniu przy rancie, gleboki polerowany rant, 5x112, dekiel.
# Uklad: metry. Auto jedzie w +Y. Prawe przednie kolo (x>0). Kamera nisko za kolem.
import bpy, bmesh, math
from mathutils import Vector, Matrix, Euler

S = bpy.context.scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

def col(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in S.collection.children:
        S.collection.children.link(c)
    return c
C_WHEEL, C_CAR, C_ENV, C_RIG = col("WHEEL"), col("CAR"), col("ENV"), col("RIG")

def link(o, c):
    c.objects.link(o)
    return o

def empty(name, c, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.1
    link(e, c)
    e.parent = parent
    e.location = loc
    e.rotation_euler = rot
    return e

# ---------------------------------------------------------------- materials
def mat(name, base, metal=0.0, rough=0.5, coat=0.0, coat_rough=0.03, aniso=0.0):
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
    return m

M = {
    "spoke": mat("M_spoke_brushed_titanium", (0.62, 0.63, 0.66), 1.0, 0.16, aniso=0.5),
    "spoke_side": mat("M_spoke_dark_chrome", (0.20, 0.21, 0.23), 1.0, 0.12),
    "lip": mat("M_lip_polished", (0.95, 0.95, 0.96), 1.0, 0.03),
    "barrel": mat("M_barrel_gloss_black", (0.03, 0.03, 0.035), 0.7, 0.25),
    "insert": mat("M_insert_purple", (0.30, 0.03, 0.85), 0.55, 0.12, coat=1.0),
    "groove": mat("M_groove_black", (0.01, 0.01, 0.012), 0.0, 0.6),
    "cap": mat("M_cap_black", (0.02, 0.02, 0.025), 0.3, 0.2, coat=1.0),
    "bolt": mat("M_bolt_chrome", (0.85, 0.85, 0.87), 1.0, 0.08),
    "paint": mat("M_paint_purple", (0.20, 0.025, 0.55), 0.6, 0.18, coat=1.0, coat_rough=0.02),
    "trim": mat("M_trim_black", (0.015, 0.015, 0.017), 0.0, 0.45),
    "caliper": mat("M_caliper_purple", (0.28, 0.035, 0.75), 0.1, 0.22, coat=1.0),
    "disc": mat("M_disc_carbon_ceramic", (0.16, 0.16, 0.17), 0.3, 0.45),
    "post": mat("M_post_grey", (0.45, 0.46, 0.48), 0.8, 0.4),
    "line": mat("M_road_paint", (0.85, 0.85, 0.83), 0.0, 0.7),
    "tree": mat("M_tree", (0.06, 0.10, 0.05), 0.0, 0.8),
    "bldg": mat("M_building", (0.55, 0.56, 0.58), 0.0, 0.8),
}

# tire: rubber + procedural tread blocks via angle-based bump
mt = bpy.data.materials.new("M_tire_rubber")
mt.use_nodes = True
nt = mt.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.018, 0.018, 0.02, 1)
bsdf.inputs["Roughness"].default_value = 0.72
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tc.outputs["Object"], sep.inputs[0])
ang = nt.nodes.new("ShaderNodeMath"); ang.operation = "ARCTAN2"
nt.links.new(sep.outputs["Y"], ang.inputs[0]); nt.links.new(sep.outputs["X"], ang.inputs[1])
mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 90.0
nt.links.new(ang.outputs[0], mul.inputs[0])
zsk = nt.nodes.new("ShaderNodeMath"); zsk.operation = "MULTIPLY"; zsk.inputs[1].default_value = 40.0
nt.links.new(sep.outputs["Z"], zsk.inputs[0])
add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
nt.links.new(mul.outputs[0], add.inputs[0]); nt.links.new(zsk.outputs[0], add.inputs[1])
sin = nt.nodes.new("ShaderNodeMath"); sin.operation = "SINE"
nt.links.new(add.outputs[0], sin.inputs[0])
gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.55
nt.links.new(sin.outputs[0], gt.inputs[0])
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.004
nt.links.new(gt.outputs[0], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
M["tire"] = mt

# asphalt
ma = bpy.data.materials.new("M_asphalt")
ma.use_nodes = True
nt = ma.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.85
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180.0; nz.inputs["Detail"].default_value = 12.0
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.045, 0.045, 0.048, 1)
ramp.color_ramp.elements[1].color = (0.17, 0.17, 0.175, 1)
nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 400.0
bmp = nt.nodes.new("ShaderNodeBump"); bmp.inputs["Strength"].default_value = 0.6; bmp.inputs["Distance"].default_value = 0.002
nt.links.new(vor.outputs["Distance"], bmp.inputs["Height"])
nt.links.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])
M["asphalt"] = ma

# ---------------------------------------------------------------- mesh helpers
def lathe(name, prof, c, material, steps=128, angle=2 * math.pi, start=0.0, smooth=True):
    """prof: list of (r, z) closed polygon, revolved around local Z."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r * math.cos(start), r * math.sin(start), z)) for r, z in prof]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    full = abs(angle - 2 * math.pi) < 1e-6
    res = bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1),
                         angle=angle, steps=steps, use_duplicate=False)
    if full:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    else:
        # cap ends
        last = [e for e in res["geom_last"] if isinstance(e, bmesh.types.BMEdge)]
        try:
            bmesh.ops.edgenet_fill(bm, edges=es)
            bmesh.ops.edgenet_fill(bm, edges=last)
        except Exception:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    link(o, c)
    o.data.materials.append(material)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    return o

def loft(name, sections, c, material, cap=True):
    """sections: list of lists of Vector (same count), bridged in order."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = [[bm.verts.new(v) for v in sec] for sec in sections]
    n = len(sections[0])
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(n):
            bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cap:
        bm.faces.new(list(reversed(rings[0])))
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    link(o, c)
    o.data.materials.append(material)
    return o

def bevel(o, w=0.0012, seg=2, ang=30):
    m = o.modifiers.new("Bevel", "BEVEL")
    m.width = w; m.segments = seg
    m.limit_method = "ANGLE"; m.angle_limit = math.radians(ang)
    return m

# ---------------------------------------------------------------- rig
R_TIRE = 0.352            # 285/30 R21
RIG = empty("RIG_car", C_RIG)
STEER = empty("RIG_steer_FR", C_RIG, RIG, (0.835, 0.0, R_TIRE))
SPIN = empty("RIG_spin_FR", C_RIG, STEER)
# wheel geometry is built with axis = local Z, face toward +Z -> rotate Y+90 so face looks +X (outboard)
# tire centre plane is local z=-0.118, so orient empties are offset +0.118 along the axle
ORI_S = empty("RIG_orient_spin", C_RIG, SPIN, (0.118, 0, 0), (0, math.radians(90), 0))
ORI_F = empty("RIG_orient_fixed", C_RIG, STEER, (0.118, 0, 0), (0, math.radians(90), 0))

def to_wheel(o, spinning=True):
    o.parent = ORI_S if spinning else ORI_F
    return o

# ---------------------------------------------------------------- rim
# barrel + polished deep lip (closed profile r,z)
barrel = [(0.2560, 0.006), (0.2600, 0.010), (0.2780, 0.010), (0.2835, 0.004), (0.2835, -0.006),
          (0.2760, -0.016), (0.2680, -0.018), (0.2680, -0.100), (0.2560, -0.115), (0.2560, -0.200),
          (0.2680, -0.215), (0.2680, -0.232), (0.2760, -0.236), (0.2780, -0.246), (0.2580, -0.246),
          (0.2500, -0.232), (0.2460, -0.215), (0.2460, -0.115), (0.2520, -0.072), (0.2530, -0.006)]
o_lip = to_wheel(lathe("WHL_lip_barrel", barrel, C_WHEEL, M["lip"], steps=180))
# inner barrel surface darker (separate thin liner behind the face so the gaps read dark like the sketch)
liner = [(0.2455, -0.078), (0.2510, -0.078), (0.2450, -0.215), (0.2400, -0.215)]
to_wheel(lathe("WHL_barrel_liner", liner, C_WHEEL, M["barrel"], steps=180))

# face outer ring (spokes merge into it)
ring = [(0.2260, -0.052), (0.2500, -0.055), (0.2525, -0.060), (0.2525, -0.078), (0.2260, -0.078), (0.2230, -0.060)]
o_ring = to_wheel(lathe("WHL_face_ring", ring, C_WHEEL, M["spoke"], steps=180))

# hub
hub = [(0.0, -0.030), (0.040, -0.030), (0.066, -0.034), (0.086, -0.044), (0.090, -0.056),
       (0.090, -0.095), (0.0, -0.095)]
o_hub = to_wheel(lathe("WHL_hub", hub, C_WHEEL, M["spoke"], steps=96))

# spokes (10, straight, faceted, widening slightly toward the rim)
N_SPOKES = 10
def zfront(r):
    # face is slightly concave: hub front -0.032 -> ring front -0.054
    t = (r - 0.070) / (0.240 - 0.070)
    return -0.032 - 0.022 * t
def spoke_sections(theta):
    secs = []
    for i in range(15):
        r = 0.070 + (0.242 - 0.070) * i / 14
        t = i / 14
        wb = 0.036 - 0.008 * math.sin(math.pi * t) + 0.006 * t   # bottom width
        wt = wb * 0.62                                             # flat top width
        h = 0.030 - 0.006 * t                                      # depth
        u = Vector((math.cos(theta), math.sin(theta), 0))
        tv = Vector((-math.sin(theta), math.cos(theta), 0))
        zf = zfront(r)
        prof = [(-wb / 2, 0.0), (-wb / 2, h * 0.55), (-wt / 2, h), (wt / 2, h), (wb / 2, h * 0.55), (wb / 2, 0.0)]
        secs.append([u * r + tv * s + Vector((0, 0, zf - h + d)) for s, d in prof])
    return secs

spoke_me = None
for k in range(N_SPOKES):
    th = 2 * math.pi * k / N_SPOKES
    o = loft(f"WHL_spoke_{k:02d}", spoke_sections(th), C_WHEEL, M["spoke"])
    o.data.materials.append(M["spoke_side"])
    # side facets dark chrome (faces whose normal is mostly tangential)
    for p in o.data.polygons:
        if abs(p.normal.z) < 0.55:
            p.material_index = 1
    bevel(o, 0.0010, 2, 25)
    to_wheel(o)

# spoke inserts: dark groove + purple insert on the flat top, outer half of each spoke
def slot(name, theta, r0, r1, w, lift, material, depth=0.0025):
    u = Vector((math.cos(theta), math.sin(theta), 0))
    tv = Vector((-math.sin(theta), math.cos(theta), 0))
    secs = []
    n = 10
    for i in range(n + 1):
        r = r0 + (r1 - r0) * i / n
        tt = (r - 0.070) / (0.242 - 0.070)
        h = 0.030 - 0.006 * tt
        ztop = zfront(r) + lift
        # rounded ends: narrow width near the ends
        e = min(i, n - i) / 2.0
        ww = w * min(1.0, 0.55 + 0.45 * e)
        secs.append([u * r + tv * s + Vector((0, 0, ztop + dz)) for s, dz in
                     [(-ww / 2, -depth), (-ww / 2, 0), (ww / 2, 0), (ww / 2, -depth)]])
    o = loft(name, secs, C_WHEEL, material)
    return to_wheel(o)

for k in range(N_SPOKES):
    th = 2 * math.pi * k / N_SPOKES
    slot(f"WHL_spoke_groove_{k:02d}", th, 0.128, 0.232, 0.0150, 0.0004, M["groove"])
    o = slot(f"WHL_spoke_insert_{k:02d}", th, 0.132, 0.228, 0.0104, 0.0009, M["insert"])
    bevel(o, 0.0006, 2, 30)

# ring inserts between the spokes (tangential purple bars near the lip), per sketch
for k in range(N_SPOKES):
    mid = 2 * math.pi * (k + 0.5) / N_SPOKES
    span = math.radians(19)
    g = [(0.2335, -0.0525), (0.2455, -0.0540), (0.2455, -0.0565), (0.2335, -0.0555)]
    og = lathe(f"WHL_ring_groove_{k:02d}", g, C_WHEEL, M["groove"], steps=16, angle=span + math.radians(3),
               start=mid - (span + math.radians(3)) / 2)
    to_wheel(og)
    p = [(0.2355, -0.0518), (0.2435, -0.0532), (0.2435, -0.0555), (0.2355, -0.0545)]
    oi = lathe(f"WHL_ring_insert_{k:02d}", p, C_WHEEL, M["insert"], steps=16, angle=span, start=mid - span / 2)
    to_wheel(oi)

# lug bolts 5x112 + center cap
bolt_me = None
for k in range(5):
    a = 2 * math.pi * k / 5 + math.pi / 10
    pc = [(0.0, -0.026), (0.0105, -0.026), (0.0115, -0.030), (0.0115, -0.040), (0.0, -0.040)]
    ob = lathe(f"WHL_bolt_{k}", pc, C_WHEEL, M["bolt"], steps=6, smooth=False)
    ob.location = (0.056 * math.cos(a), 0.056 * math.sin(a), 0)
    to_wheel(ob)
    pk = [(0.0, -0.0305), (0.0150, -0.0305), (0.0150, -0.0345), (0.0, -0.0345)]
    ok = lathe(f"WHL_bolt_pocket_{k}", pk, C_WHEEL, M["groove"], steps=24)
    ok.location = ob.location
    to_wheel(ok)
cap = [(0.0, -0.018), (0.020, -0.020), (0.030, -0.025), (0.033, -0.031), (0.0, -0.031)]
to_wheel(lathe("WHL_center_cap", cap, C_WHEEL, M["cap"], steps=64))
capring = [(0.030, -0.0245), (0.0345, -0.0275), (0.0345, -0.0315), (0.029, -0.0315)]
to_wheel(lathe("WHL_center_cap_ring", capring, C_WHEEL, M["bolt"], steps=64))

# ---------------------------------------------------------------- tire 285/30 R21
tp = [(0.2680, 0.004), (0.2860, 0.016), (0.3150, 0.0235), (0.3380, 0.0215), (0.3480, 0.0140),
      (0.3520, 0.0040), (0.3520, -0.0240), (0.3460, -0.0260), (0.3460, -0.0360), (0.3520, -0.0380),
      (0.3520, -0.0790), (0.3460, -0.0810), (0.3460, -0.0910), (0.3520, -0.0930),
      (0.3520, -0.1430), (0.3460, -0.1450), (0.3460, -0.1550), (0.3520, -0.1570),
      (0.3520, -0.2000), (0.3460, -0.2020), (0.3460, -0.2120), (0.3520, -0.2140),
      (0.3520, -0.2400), (0.3480, -0.2500), (0.3380, -0.2575), (0.3150, -0.2595), (0.2860, -0.2520),
      (0.2680, -0.2400), (0.2620, -0.2300), (0.2620, -0.0060)]
o_tire = to_wheel(lathe("WHL_tire", tp, C_WHEEL, M["tire"], steps=256))

# ---------------------------------------------------------------- brake (disc spins, caliper fixed)
dp = [(0.085, -0.140), (0.205, -0.140), (0.205, -0.176), (0.085, -0.176)]
to_wheel(lathe("BRK_disc", dp, C_WHEEL, M["disc"], steps=128))
hat = [(0.060, -0.098), (0.090, -0.098), (0.090, -0.176), (0.060, -0.176)]
to_wheel(lathe("BRK_hat", hat, C_WHEEL, M["bolt"], steps=64))
# caliper centred toward rear-top of the wheel (world -Y,+Z) -> local angle ~215 deg
cal_c = math.radians(215)
cal_span = math.radians(62)
cp = [(0.150, -0.108), (0.238, -0.108), (0.242, -0.118), (0.242, -0.205), (0.150, -0.205)]
oc = lathe("BRK_caliper", cp, C_WHEEL, M["caliper"], steps=24, angle=cal_span, start=cal_c - cal_span / 2)
bevel(oc, 0.004, 3, 30)
to_wheel(oc, spinning=False)

# ---------------------------------------------------------------- car body (right front quarter, simplified)
ARCH_C = (0.0, R_TIRE + 0.012)
ARCH_R = 0.392
def body_x(y, z):
    x = 0.975 - 0.10 * max(0.0, (z - 0.50) / 0.30) ** 2 - 0.05 * max(0.0, (0.26 - z) / 0.14) ** 2
    if y > 0.70:
        x -= 2.6 * (y - 0.70) ** 2
    if y < -1.6:
        x -= 0.3 * (-1.6 - y) ** 2
    return x
ny, nz = 120, 40
y0, y1, z0, z1 = -2.4, 1.05, 0.13, 0.78
me = bpy.data.meshes.new("CAR_body_side")
bm = bmesh.new()
grid = []
for j in range(nz + 1):
    row = []
    for i in range(ny + 1):
        y = y0 + (y1 - y0) * i / ny
        z = z0 + (z1 - z0) * j / nz
        row.append(bm.verts.new((body_x(y, z), y, z)))
    grid.append(row)
for j in range(nz):
    for i in range(ny):
        a, b, c_, d = grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]
        cy = (a.co.y + c_.co.y) / 2; cz = (a.co.z + c_.co.z) / 2
        if math.hypot(cy - ARCH_C[0], cz - ARCH_C[1]) < ARCH_R:
            continue
        bm.faces.new((a, b, c_, d))
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
# snap arch boundary verts onto the circle for a clean arch edge
for v in bm.verts:
    if v.is_boundary:
        dy, dz = v.co.y - ARCH_C[0], v.co.z - ARCH_C[1]
        dd = math.hypot(dy, dz)
        if dd < ARCH_R + 0.04 and v.co.z > 0.135 and -0.6 < v.co.y < 0.6:
            v.co.y = ARCH_C[0] + dy / dd * ARCH_R
            v.co.z = ARCH_C[1] + dz / dd * ARCH_R
            v.co.x = body_x(v.co.y, v.co.z)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(me); bm.free()
body = link(bpy.data.objects.new("CAR_body_side", me), C_CAR)
body.data.materials.append(M["paint"])
for p in body.data.polygons:
    p.use_smooth = True
sol = body.modifiers.new("Solidify", "SOLIDIFY"); sol.thickness = 0.004; sol.offset = -1
body.parent = RIG

# arch flare lip (body colour) and black arch liner
fl = []
for i in range(73):
    a = math.radians(-8 + (196 * i / 72))  # from front-low over the top to rear-low
    yy = ARCH_C[0] + math.cos(a) * ARCH_R
    zz = ARCH_C[1] + math.sin(a) * ARCH_R
    if zz < 0.14:
        continue
    xo = body_x(yy, zz)
    n = Vector((0, math.cos(a), math.sin(a)))
    fl.append([Vector((xo, yy, zz)), Vector((xo + 0.004, 0, 0)) + n * 0.012 + Vector((0, yy, zz)),
               Vector((xo - 0.045, 0, 0)) + n * 0.016 + Vector((0, yy, zz)), Vector((xo - 0.05, yy, zz))])
lip = loft("CAR_arch_lip", fl, C_CAR, M["paint"], cap=False)
lip.parent = RIG
for p in lip.data.polygons:
    p.use_smooth = True
lp = []
for i in range(73):
    a = math.radians(-12 + (204 * i / 72))
    yy = ARCH_C[0] + math.cos(a) * (ARCH_R + 0.004)
    zz = ARCH_C[1] + math.sin(a) * (ARCH_R + 0.004)
    lp.append([Vector((0.95, yy, zz)), Vector((0.55, yy, zz)),
               Vector((0.55, yy * 1.05, ARCH_C[1] + (zz - ARCH_C[1]) * 1.05)),
               Vector((0.95, yy * 1.05, ARCH_C[1] + (zz - ARCH_C[1]) * 1.05))])
liner_o = loft("CAR_arch_liner", lp, C_CAR, M["trim"], cap=False)
liner_o.parent = RIG
# underbody + door gap + side blade
ub = bpy.data.meshes.new("CAR_underbody")
ub.from_pydata([(0.94, -2.4, 0.13), (0.94, 1.0, 0.13), (-0.9, 1.0, 0.13), (-0.9, -2.4, 0.13)], [], [(0, 1, 2, 3)])
ubo = link(bpy.data.objects.new("CAR_underbody", ub), C_CAR); ubo.data.materials.append(M["trim"]); ubo.parent = RIG
gap = bpy.data.meshes.new("CAR_door_gap")
gy = -0.62
gap.from_pydata([(body_x(gy, 0.20) + 0.0015, gy, 0.20), (body_x(gy, 0.20) + 0.0015, gy - 0.004, 0.20),
                 (body_x(gy, 0.74) + 0.0015, gy - 0.004, 0.74), (body_x(gy, 0.74) + 0.0015, gy, 0.74)], [], [(0, 1, 2, 3)])
gpo = link(bpy.data.objects.new("CAR_door_gap", gap), C_CAR); gpo.data.materials.append(M["trim"]); gpo.parent = RIG

# ---------------------------------------------------------------- environment
gm = bpy.data.meshes.new("ENV_ground")
gm.from_pydata([(-200, -200, 0), (200, -200, 0), (200, 200, 0), (-200, 200, 0)], [], [(0, 1, 2, 3)])
go = link(bpy.data.objects.new("ENV_ground", gm), C_ENV); go.data.materials.append(M["asphalt"])
# parking bay lines (perpendicular to travel) + a long edge line
def box(name, size, loc, material, c=C_ENV, rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), c)
    o.scale = size; o.location = loc; o.rotation_euler = rot
    o.data.materials.append(material)
    return o
for i in range(14):
    box(f"ENV_bay_line_{i:02d}", (3.0, 0.12, 0.004), (2.9, 3.0 + i * 2.6, 0.002), M["line"])
box("ENV_edge_line", (0.12, 60.0, 0.004), (1.35, 25.0, 0.002), M["line"])
# lamp posts (as in the reference: tall, slim, with an arm)
for i, (x, y) in enumerate([(7.5, 9.0), (8.5, 26.0), (9.5, 43.0), (-6.0, 30.0), (14.0, 15.0)]):
    p = box(f"ENV_lamp_post_{i}", (0.12, 0.12, 9.0), (x, y, 4.5), M["post"])
    box(f"ENV_lamp_arm_{i}", (1.6, 0.08, 0.08), (x - 0.75, y, 8.9), M["post"], rot=(0, math.radians(-8), 0))
    box(f"ENV_lamp_head_{i}", (0.55, 0.22, 0.10), (x - 1.5, y, 8.8), M["post"])
# guard rail, tree line and low buildings far away
box("ENV_guardrail", (0.06, 120.0, 0.35), (16.0, 30.0, 0.75), M["post"])
for i in range(26):
    x = 22 + (i % 3) * 4
    y = -20 + i * 5.5
    tm = bpy.data.meshes.new(f"ENV_tree_{i}")
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0); bm.to_mesh(tm); bm.free()
    t = link(bpy.data.objects.new(f"ENV_tree_{i}", tm), C_ENV)
    s = 2.5 + (i * 37 % 10) * 0.25
    t.scale = (s, s, s * 1.4); t.location = (x, y, s * 1.2); t.data.materials.append(M["tree"])
for i in range(6):
    box(f"ENV_building_{i}", (12, 18, 6 + i % 3 * 4), (-40 - i * 6, 10 + i * 22, 3 + i % 3 * 2), M["bldg"])

# ---------------------------------------------------------------- world: bright overcast sky with clouds
W = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
S.world = W
W.use_nodes = True
nt = W.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputWorld")
bg = nt.nodes.new("ShaderNodeBackground")
nt.links.new(bg.outputs[0], out.inputs[0])
tc = nt.nodes.new("ShaderNodeTexCoord")
sepz = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tc.outputs["Generated"], sepz.inputs[0])
grad = nt.nodes.new("ShaderNodeValToRGB")
grad.color_ramp.elements[0].position = 0.48
grad.color_ramp.elements[0].color = (0.80, 0.82, 0.86, 1)
grad.color_ramp.elements[1].position = 0.95
grad.color_ramp.elements[1].color = (0.42, 0.55, 0.78, 1)
nt.links.new(sepz.outputs["Z"], grad.inputs["Fac"])
cl = nt.nodes.new("ShaderNodeTexNoise"); cl.inputs["Scale"].default_value = 2.2; cl.inputs["Detail"].default_value = 8.0
cl.inputs["Roughness"].default_value = 0.62
nt.links.new(tc.outputs["Generated"], cl.inputs["Vector"])
cr = nt.nodes.new("ShaderNodeValToRGB")
cr.color_ramp.elements[0].position = 0.42; cr.color_ramp.elements[0].color = (0, 0, 0, 1)
cr.color_ramp.elements[1].position = 0.62; cr.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(cl.outputs["Fac"], cr.inputs["Fac"])
mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
mix.inputs["B"].default_value = (0.97, 0.97, 0.98, 1)
nt.links.new(cr.outputs["Color"], mix.inputs["Factor"])
nt.links.new(grad.outputs["Color"], mix.inputs["A"])
nt.links.new(mix.outputs["Result"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.6

sun = bpy.data.lights.new("LGT_key_sun", "SUN")
sun.energy = 2.2
sun.angle = math.radians(25)
so = link(bpy.data.objects.new("LGT_key_sun", sun), C_ENV)
so.rotation_euler = (math.radians(50), 0, math.radians(150))

# ---------------------------------------------------------------- camera (rigged to the car, low, behind the wheel)
cam = bpy.data.cameras.new("CAM_main")
cam.lens = 13.0
cam.sensor_width = 36.0
cam.sensor_fit = "HORIZONTAL"
cam.clip_start = 0.02
co = link(bpy.data.objects.new("CAM_main", cam), C_RIG)
co.parent = RIG
cam_loc = Vector((1.10, -0.82, 0.115))
target = Vector((0.86, 0.15, 0.42))
q = (target - cam_loc).to_track_quat("-Z", "Y")
roll = Matrix.Rotation(math.radians(-9), 4, "Z")
co.matrix_world = Matrix.Translation(cam_loc) @ q.to_matrix().to_4x4() @ roll
S.camera = co

# ---------------------------------------------------------------- render basics
S.render.resolution_x = 1080
S.render.resolution_y = 1920
S.render.resolution_percentage = 50
S.render.fps = 24
S.frame_start = 1
S.frame_end = 310
S.view_settings.view_transform = "AgX"
try:
    S.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
S.render.engine = "BLENDER_EEVEE"

# ---------------------------------------------------------------- animation
# 0-3.3 s: steered LEFT to lock (face turned away, only tyre visible)
# 3.3-4.6 s: steering swings to the right -> face revealed toward the camera
# 4.2 s ->: car rolls forward at walking pace, wheel spins (rolling contact), slight right yaw
FPS = 24
STEER_HIDE = math.radians(34)
STEER_SHOW = math.radians(-24)
f_turn0, f_turn1 = 80, 111
f_roll0, f_roll1 = 101, 150
V_MAX = 1.0           # m/s
YAW_TOTAL = math.radians(-26)

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

dist = 0.0
yaw = 0.0
pos = Vector((0, 0, 0))
total_frames = S.frame_end
# precompute total travel after roll start for yaw distribution
speeds = []
for f in range(1, total_frames + 1):
    v = V_MAX * smooth((f - f_roll0) / (f_roll1 - f_roll0)) if f >= f_roll0 else 0.0
    speeds.append(v)
travel_total = sum(speeds) / FPS
for f in range(1, total_frames + 1):
    v = speeds[f - 1]
    d = v / FPS
    dist += d
    yaw += YAW_TOTAL * (d / travel_total)
    pos += Vector((-math.sin(yaw), math.cos(yaw), 0)) * d
    RIG.location = pos
    RIG.rotation_euler = (0, 0, yaw)
    RIG.keyframe_insert("location", frame=f)
    RIG.keyframe_insert("rotation_euler", frame=f)
    SPIN.rotation_euler = (-dist / R_TIRE, 0, 0)
    SPIN.keyframe_insert("rotation_euler", frame=f)
    st = STEER_HIDE + (STEER_SHOW - STEER_HIDE) * smooth((f - f_turn0) / (f_turn1 - f_turn0))
    STEER.rotation_euler = (0, 0, st)
    STEER.keyframe_insert("rotation_euler", frame=f)
S.frame_set(1)

result = {
    "objects": len(bpy.data.objects),
    "wheel_parts": len([o for o in bpy.data.objects if o.name.startswith("WHL_")]),
    "travel_m": round(dist, 3),
    "yaw_deg": round(math.degrees(yaw), 2),
}

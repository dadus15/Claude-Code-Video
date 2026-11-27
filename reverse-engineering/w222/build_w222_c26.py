"""Build the W222 S560 4MATIC L + Turismo C26 22x10.5J rig scene from the calibrated rev24 rig.
Usage: python3 build_w222_c26.py <rev24.blend> <c26_m.blend (normalised CAD, metres, axle +Z, face +Z)> <out.blend>
Everything below is computed from published W222 data + measurements on the Turismo project photos."""
import bpy, bmesh, math, random, sys
import numpy as np
from mathutils import Matrix, Vector
REV24, C26, OUT, CAM_SCALE = sys.argv[-4], sys.argv[-3], sys.argv[-2], float(sys.argv[-1])
bpy.ops.wm.open_mainfile(filepath=REV24)
S = bpy.context.scene
OB = bpy.data.objects
# ---------------------------------------------------------------- vehicle data (V222 S560 4MATIC L)
WB = 3.165                     # wheelbase
ET_SHIFT = 0.038 - 0.0297      # OEM front ET38 -> C26 ET29.7 : wheel centre moves out 8.3 mm per side
TF = 1.630 + 2 * ET_SHIFT      # front track at tyre centres with C26
TR = 1.643 + 2 * ET_SHIFT
TURN_D = 12.3                  # turning circle (m)
R_STAT = 0.346                 # loaded radius 255/30 R22 (photo: 147 px / 424.5 px/m)
R_ROLL = 0.350                 # rolling radius for spin
OD, BEAD, SECW = 0.7118, 0.5588, 0.255
FRONT_OH, REAR_OH, HALF_W = 0.95, 1.14, 0.947
Ro = TURN_D / 2
RR_LOCK = math.sqrt(Ro**2 - WB**2) - TF / 2
D_LOCK = math.atan(WB / RR_LOCK)
P = {"vr": 0.581, "vf": 1.084, "dL": D_LOCK, "dR": math.radians(14.0)}
FPS = 24
# ---------------------------------------------------------------- remove RS5 / V05 parts
old_tyre = OB["WHL_tyre"]
tco = np.array([v.co[:] for v in old_tyre.data.vertices])
zc_old = float((tco[:, 2].min() + tco[:, 2].max()) / 2)
for o in list(OB):
    if (o.name.startswith("WHL_") and o.name != "WHL_tyre") or o.name.startswith("CAR_") or o.name == "BRK_RS_logo" \
       or o.name.startswith("TRK_"):
        bpy.data.objects.remove(o, do_unlink=True)
RIG = OB["RIG_car"]; ST = OB["RIG_steer_FL"]; SP = OB["RIG_spin_FL"]
OSPIN = OB["RIG_orient_spin"]; OFIX = OB["RIG_orient_fixed"]; CAMO = OB["CAM_rig"]
old_pivot = ST.location.copy()
ST.location = (-TF / 2, 0.0, R_STAT)
# ---------------------------------------------------------------- materials
def mat(name, base, metal=0.0, rough=0.5, coat=0.0, aniso=0.0, emit=None, alpha=1.0, trans=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(b.outputs[0], o.inputs[0])
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.03
    if aniso:
        b.inputs["Anisotropic"].default_value = aniso
        tg = nt.nodes.new("ShaderNodeTangent"); tg.direction_type = 'RADIAL'; tg.axis = 'Z'
        nt.links.new(tg.outputs[0], b.inputs["Tangent"])
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 900.0
        mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs[3].default_value = rough - 0.05; mp.inputs[4].default_value = rough + 0.07
        nt.links.new(nz.outputs[0], mp.inputs[0]); nt.links.new(mp.outputs[0], b.inputs["Roughness"])
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = 6.0
    if trans: b.inputs["Transmission Weight"].default_value = trans
    if alpha < 1: b.inputs["Alpha"].default_value = alpha
    return m
M_PAINT = mat("M_W222_obsidian_black", (0.002, 0.002, 0.0025), 0.0, 0.40, coat=1.0)
M_GLASS = mat("M_W222_glass", (0.015, 0.02, 0.025), 0.0, 0.03, coat=0.0)
M_CHROME = mat("M_chrome", (0.95, 0.95, 0.95), 1.0, 0.05)
M_TRIM = mat("M_trim_black_plastic", (0.02, 0.02, 0.02), 0.0, 0.6)
M_LINER = mat("M_arch_liner_felt", (0.012, 0.012, 0.012), 0.0, 0.95)
M_GAP = mat("M_panel_gap", (0.0, 0.0, 0.0), 0.0, 0.9)
M_HL = mat("M_W222_headlight", (0.06, 0.065, 0.07), 0.9, 0.08)
M_DRL = mat("M_W222_drl", (1, 1, 1), 0.0, 0.2, emit=(0.92, 0.95, 1.0))
M_WHEEL = mat("M_C26_brushed_silver", (0.50, 0.505, 0.51), 1.0, 0.30, aniso=0.55)
M_BARREL = mat("M_C26_barrel", (0.30, 0.30, 0.31), 1.0, 0.55)
M_BOLT = mat("M_bolt_steel", (0.8, 0.8, 0.82), 1.0, 0.18)
M_CAL = mat("M_caliper_w222_grey", (0.18, 0.18, 0.19), 0.6, 0.35)
# ---------------------------------------------------------------- C26 wheel (CAD) on the spin frame
with bpy.data.libraries.load(C26) as (src, dst): dst.meshes = ["C26_cad"]
cad = dst.meshes[0]
cad.materials.clear(); cad.materials.append(M_WHEEL); cad.materials.append(M_BARREL)
n = len(cad.polygons)
pc = np.empty(n * 3); cad.polygons.foreach_get("center", pc); pc = pc.reshape(-1, 3)
pn = np.empty(n * 3); cad.polygons.foreach_get("normal", pn); pn = pn.reshape(-1, 3)
pr = np.hypot(pc[:, 0], pc[:, 1])
barrel = (pr > 0.245) & (pc[:, 2] < 0.118) & (np.abs(pn[:, 2]) < 0.5)
cad.polygons.foreach_set("material_index", barrel.astype(np.int32))
for p in cad.polygons: p.use_smooth = False
cad.update()
def add_wheel(name, parent, zc):
    w = bpy.data.objects.new(name, cad); S.collection.objects.link(w)
    w.parent = parent; w.matrix_parent_inverse = Matrix.Identity(4); w.location = (0, 0, zc)
    return w
add_wheel("WHL_C26_FL", OSPIN, zc_old)
# wheel bolts (5 x M14 collar bolts, PCD 112) seated at z = 0.0415 in the pockets
def bolts(parent, zc, tag):
    for k in range(5):
        a = math.radians(36 + 72 * k)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.0085, radius2=0.0085, depth=0.012)
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.0115, radius2=0.0115, depth=0.004,
                              matrix=Matrix.Translation((0, 0, -0.008)))
        me = bpy.data.meshes.new(f"bolt_{tag}{k}"); bm.to_mesh(me); bm.free(); me.materials.append(M_BOLT)
        o = bpy.data.objects.new(f"WHL_bolt_{tag}{k}", me); S.collection.objects.link(o)
        o.parent = parent; o.location = (0.056 * math.cos(a), 0.056 * math.sin(a), zc + 0.0415 + 0.010)
bolts(OSPIN, zc_old, "FL")
# centre cap with the GT logo is part of the CAD model (face at z = 0.0672)
# ---------------------------------------------------------------- tyre 255/30 R22 (remap old winter tyre, keeps tread shader)
r_old = np.hypot(tco[:, 0], tco[:, 1]); r0, r1 = r_old.min(), r_old.max()
z0, z1 = tco[:, 2].min(), tco[:, 2].max()
new = []
for (x, y, z), r in zip(tco, r_old):
    rn = BEAD / 2 + (r - r0) / (r1 - r0) * (OD / 2 - BEAD / 2)
    zn = zc_old + (z - zc_old) * (0.262 / (z1 - z0))
    k = rn / r if r > 1e-9 else 1
    new.extend((x * k, y * k, zn))
old_tyre.data.vertices.foreach_set("co", new); old_tyre.data.update(); old_tyre.name = "WHL_tyre_255_30R22_winter"
# winter tyre shader: dark rubber, directional V tread (object space: angle around Z, z across the tread), sipes, packed snow in grooves
mt = bpy.data.materials.new("M_tyre_winter_255_30R22"); mt.use_nodes = True; nt = mt.node_tree; nt.nodes.clear(); L = nt.links.new
out = nt.nodes.new("ShaderNodeOutputMaterial"); bs = nt.nodes.new("ShaderNodeBsdfPrincipled"); L(bs.outputs[0], out.inputs[0])
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sep.inputs[0])
def M(op, a, b=None, v=None):
    n_ = nt.nodes.new("ShaderNodeMath"); n_.operation = op
    for idx, val in ((0, a), (1, b)):
        if val is None: continue
        if isinstance(val, (int, float)): n_.inputs[idx].default_value = val
        else: L(val, n_.inputs[idx])
    return n_.outputs[0]
ang = M("ARCTAN2", sep.outputs[1], sep.outputs[0])
zr = M("ABSOLUTE", M("SUBTRACT", sep.outputs[2], zc_old))
rad = M("SQRT", M("ADD", M("POWER", sep.outputs[0], 2.0), M("POWER", sep.outputs[1], 2.0)))
tread = M("GREATER_THAN", rad, OD / 2 - 0.012)
ph = M("FRACT", M("ADD", M("MULTIPLY", ang, 64 / (2 * math.pi)), M("MULTIPLY", zr, 9.0)))
blockg = M("LESS_THAN", ph, 0.20)                                   # V-shaped lateral grooves
circ = M("LESS_THAN", M("ABSOLUTE", M("SUBTRACT", zr, 0.045)), 0.006)  # two circumferential grooves
centre = M("LESS_THAN", zr, 0.004)
sipe = M("LESS_THAN", M("FRACT", M("ADD", M("MULTIPLY", ang, 64 * 5 / (2 * math.pi)), M("MULTIPLY", zr, 45.0))), 0.08)
groove = M("MINIMUM", M("ADD", M("ADD", blockg, circ), centre), 1.0)
gmask = M("MULTIPLY", groove, M("MULTIPLY", tread, M("LESS_THAN", zr, 0.118)))
smask = M("MULTIPLY", M("MULTIPLY", sipe, tread), M("LESS_THAN", zr, 0.11))
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 60.0; L(tc.outputs["Object"], nz.inputs["Vector"])
snow = M("MULTIPLY", gmask, M("GREATER_THAN", nz.outputs[0], 0.68))
mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.inputs["A"].default_value = (0.034, 0.034, 0.036, 1); mix.inputs["B"].default_value = (0.55, 0.57, 0.6, 1)
mx2 = nt.nodes.new("ShaderNodeMix"); mx2.data_type = "RGBA"; mx2.inputs["B"].default_value = (0.006, 0.006, 0.007, 1)
L(mix.outputs["Result"], mx2.inputs["A"]); L(M("MULTIPLY", gmask, M("SUBTRACT", 1.0, snow)), mx2.inputs["Factor"])
L(snow, mix.inputs["Factor"]); L(mx2.outputs["Result"], bs.inputs["Base Color"])
bs.inputs["Roughness"].default_value = 0.82
h = M("MAXIMUM", gmask, M("MULTIPLY", smask, 0.5))
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.9; bump.inputs["Distance"].default_value = 0.004
L(M("SUBTRACT", 1.0, h), bump.inputs["Height"]); L(bump.outputs[0], bs.inputs["Normal"])
old_tyre.data.materials.clear(); old_tyre.data.materials.append(mt)
# ---------------------------------------------------------------- brake: 370 x 36 perforated disc, 4-piston caliper
disc = OB["BRK_disc"]; cal = OB["BRK_caliper"]
dco = np.array([v.co[:] for v in disc.data.vertices]); dr = np.hypot(dco[:, 0], dco[:, 1]).max()
k = 0.185 / dr; mount = zc_old + 0.0297; dz_new = mount - 0.0645 + 0.018
dzc = (dco[:, 2].min() + dco[:, 2].max()) / 2
disc.data.vertices.foreach_set("co", [c for x, y, z in dco for c in (x * k, y * k, dz_new + (z - dzc) * (0.036 / (np.ptp(dco[:, 2]) or 1)))])
disc.data.update()
cco = np.array([v.co[:] for v in cal.data.vertices]); czc = (cco[:, 2].min() + cco[:, 2].max()) / 2
cal.data.vertices.foreach_set("co", [c for x, y, z in cco for c in (x * k, y * k, dz_new + (z - czc))])
cal.data.update(); cal.data.materials.clear(); cal.data.materials.append(M_CAL)
# ---------------------------------------------------------------- body (left half visible; full closed loft for clean booleans)
def interp(tab, y):
    ys = [a for a, b in tab]; zs = [b for a, b in tab]
    return float(np.interp(y, ys, zs))
BELT = [(-4.31, 0.74), (-4.22, 0.80), (-4.10, 1.02), (-3.95, 1.06), (-3.70, 1.09), (-3.30, 1.062), (-2.6, 1.051),
        (-2.0, 1.041), (-1.2, 1.002), (-0.8, 1.030), (-0.4, 0.999), (0.0, 0.954), (0.2, 0.926), (0.4, 0.886),
        (0.55, 0.841), (0.75, 0.79), (0.88, 0.74), (0.95, 0.68)]
ROOF = [(-4.31, 0.0), (-3.95, 0.0), (-3.75, 0.0), (-3.70, 0.05), (-3.05, 1.0), (-2.2, 1.0), (-1.75, 1.0), (-0.80, 0.0), (0.95, 0.0)]
ZROOF = 1.494
ZB = [(-4.31, 0.30), (-4.15, 0.20), (-3.6, 0.17), (-0.6, 0.15), (0.5, 0.15), (0.80, 0.17), (0.95, 0.24)]
def plan(y):     # plan-view rounding of the corners (superellipse)
    yf0, yr0 = 0.40, -3.95
    if y > yf0: t = min(1, (y - yf0) / (FRONT_OH - yf0 + 0.02)); return (1 - t**3.2) ** (1 / 3.2)
    if y < yr0: t = min(1, (yr0 - y) / (REAR_OH - (-yr0 - WB) + 0.02)); return (1 - t**4) ** 0.25
    return 1.0
def section(y):
    w = HALF_W * plan(y); zb = interp(ZB, y); zbt = interp(BELT, y); g = interp(ROOF, y)
    zr = zbt + g * (ZROOF - zbt)
    wr = (0.70 if g > 0 else 0.0) * plan(y)
    hood = zbt + 0.04 * plan(y)
    pts = [(-0.0, zb), (-(w - 0.07), zb), (-(w - 0.025), zb + 0.09), (-w, 0.50), (-(w - 0.006), zbt - 0.16),
           (-(w - 0.03), zbt - 0.02), (-(w - 0.065), zbt + 0.005)]
    if g > 0:
        pts += [(-(w - 0.075), zbt + 0.012), (-(wr + 0.06) * 1.0, zr - 0.07), (-wr, zr - 0.01), (-wr * 0.5, zr + 0.012), (0.0, zr + 0.015)]
    else:
        pts += [(-(w - 0.075), zbt + 0.010), (-(w - 0.20), hood - 0.005), (-(w - 0.45), hood + 0.0), (-(w - 0.75), hood + 0.005), (0.0, hood + 0.008)]
    return pts
SEG = ["bot", "sillin", "sill", "lower", "side", "shoulder", "belt", "beltlip", "glass", "frame", "roof", "roofc"]
def cr(pts, k=5):   # Catmull-Rom densify, keeps segment ids
    out = []; ids = []
    P_ = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = map(np.array, P_[i - 1:i + 3])
        for j in range(k):
            t = j / k
            q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
            out.append(tuple(q)); ids.append(i - 1)
    out.append(pts[-1]); ids.append(len(pts) - 2)
    return out, ids
ys = sorted(set(list(np.round(np.arange(-4.31, -1.6, 0.04), 4)) + list(np.round(np.arange(-1.6, 0.951, 0.012), 4))))
bm = bmesh.new(); rings = []; seg_of = []
for y in ys:
    sec, ids = cr(section(y))
    left = [(x, y, z) for x, z in sec]
    right = [(-x, y, z) for x, z in reversed(sec[1:-1])]
    ring = [bm.verts.new(p) for p in left + right]; rings.append(ring)
    seg_of = ids + list(reversed(ids[1:-1]))
for a, b in zip(rings[:-1], rings[1:]):
    N = len(a)
    for i in range(N):
        f = bm.faces.new((a[i], a[(i + 1) % N], b[(i + 1) % N], b[i])); f.material_index = 0
for ring, rev in ((rings[0], True), (rings[-1], False)):
    c = Vector((0, 0, 0))
    for v in ring: c += v.co
    cv = bm.verts.new(c / len(ring)); N = len(ring)
    for i in range(N):
        tri = (ring[i], ring[(i + 1) % N], cv) if not rev else (ring[(i + 1) % N], ring[i], cv)
        bm.faces.new(tri)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
body_me = bpy.data.meshes.new("W222_body"); bm.to_mesh(body_me); bm.free()
for m_ in (M_PAINT, M_GLASS, M_HL, M_LINER, M_TRIM): body_me.materials.append(m_)
body = bpy.data.objects.new("CAR_W222_body", body_me); S.collection.objects.link(body)
for p in body_me.polygons: p.use_smooth = True
# wheel-arch cutters (front + rear), liner material comes from the cutter
def cutter(yc, name):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=128, radius1=0.388, radius2=0.388, depth=0.55,
                          matrix=Matrix.Translation((-HALF_W + 0.20, yc, R_STAT + 0.012)) @ Matrix.Rotation(math.pi / 2, 4, 'Y'))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(M_LINER)
    o = bpy.data.objects.new(name, me); S.collection.objects.link(o); return o
for yc, nm in ((0.0, "CUT_F"), (-WB, "CUT_R")):
    cu = cutter(yc, nm)
    md = body.modifiers.new("arch_" + nm, 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = cu
    try: md.solver = 'EXACT'
    except Exception: pass
    bpy.context.view_layer.objects.active = body
    with bpy.context.temp_override(object=body, active_object=body):
        bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.data.objects.remove(cu, do_unlink=True)
# material assignment by surface region
def in_poly(y, z, poly):
    c = False; n_ = len(poly)
    for i in range(n_):
        y1, z1 = poly[i]; y2, z2 = poly[(i + 1) % n_]
        if (z1 > z) != (z2 > z) and y < (y2 - y1) * (z - z1) / (z2 - z1 + 1e-12) + y1: c = not c
    return c
HEADLIGHT = [(0.32, 0.795), (0.45, 0.832), (0.62, 0.842), (0.74, 0.805), (0.78, 0.70), (0.70, 0.655), (0.52, 0.705), (0.32, 0.782)]
mi = []
for p in body_me.polygons:
    x, y, z = p.center; nx = p.normal.x
    m_ = p.material_index
    if body_me.materials[m_] == M_LINER: mi.append(3); continue
    g = interp(ROOF, y); zbt = interp(BELT, y)
    if g > 0 and z > zbt + 0.015 and z < (zbt + g * (ZROOF - zbt)) - 0.075 and abs(x) > 0.5: mi.append(1); continue      # side glass
    if 0 < g < 1 and z > zbt + 0.03 and abs(x) < 0.66: mi.append(1); continue                                            # wind/rear screens
    if z < interp(ZB, y) + 0.06: mi.append(4); continue                                                                  # sill / lower trim
    mi.append(0)
body_me.polygons.foreach_set("material_index", mi); body_me.update()
body.parent = RIG; body.matrix_parent_inverse = Matrix.Identity(4)
# helper: outer surface x at (y,z) on the left side
def side_x(y, z):
    sec, _ = cr(section(y)); best = None
    for (x1, z1), (x2, z2) in zip(sec[:-1], sec[1:]):
        if (z1 - z) * (z2 - z) <= 0 and x1 < -0.3:
            t = (z - z1) / (z2 - z1 + 1e-12); xv = x1 + t * (x2 - x1)
            best = xv if best is None else min(best, xv)
    return best if best is not None else -HALF_W * plan(y)
def ribbon(name, pts_yz, width, mat_, out=0.0015, vertical=False):
    bm = bmesh.new(); prev = None
    for (y, z) in pts_yz:
        x = side_x(y, z) - out
        a = bm.verts.new((x, y, z - width / 2) if not vertical else (x, y - width / 2, z))
        b = bm.verts.new((x, y, z + width / 2) if not vertical else (x, y + width / 2, z))
        if prev: bm.faces.new((prev[0], prev[1], b, a))
        prev = (a, b)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat_)
    o = bpy.data.objects.new(name, me); S.collection.objects.link(o); o.parent = RIG; return o
yy = np.arange(-3.62, -0.79, 0.02)
ribbon("CAR_belt_chrome", [(y, interp(BELT, y) + 0.008) for y in yy], 0.012, M_CHROME)
ribbon("CAR_window_frame_chrome", [(y, interp(BELT, y) + interp(ROOF, y) * (ZROOF - interp(BELT, y)) - 0.072) for y in yy if interp(ROOF, y) > 0.15], 0.010, M_CHROME)
ribbon("CAR_sill_chrome", [(y, 0.235) for y in np.arange(-2.90, -0.42, 0.02)], 0.008, M_CHROME)
for yg in (-0.72, -1.95, -3.02):
    ribbon(f"CAR_gap_{yg}", [(yg + 0.012 * (z - 0.2), z) for z in np.arange(0.20, interp(BELT, yg) - 0.005, 0.02)], 0.004, M_GAP, vertical=True)
# W222 facelift DRL: three stacked light strips in the headlight
for kk, zz in enumerate((0.818, 0.800, 0.782)):
    ribbon(f"CAR_drl_{kk}", [(y, zz + 0.10 * (y - 0.60) ** 2) for y in np.arange(0.47 + 0.03 * kk, 0.74, 0.01)], 0.006, M_DRL, out=0.003)
# headlight lens: separate smooth patch projected onto the body surface (Delaunay of densified outline + interior grid)
from mathutils.geometry import delaunay_2d_cdt
bnd = []
for (a1, b1), (a2, b2) in zip(HEADLIGHT, HEADLIGHT[1:] + HEADLIGHT[:1]):
    for t in np.linspace(0, 1, 14, endpoint=False): bnd.append((a1 + t * (a2 - a1), b1 + t * (b2 - b1)))
inner = [(y, z) for y in np.arange(0.30, 0.80, 0.01) for z in np.arange(0.64, 0.85, 0.008) if in_poly(y, z, HEADLIGHT)]
pts2 = [Vector(p) for p in bnd + inner]
edges = [(i, (i + 1) % len(bnd)) for i in range(len(bnd))]
vco, ed, fc, _, _, _ = delaunay_2d_cdt(pts2, edges, [], 2, 1e-6)
me = bpy.data.meshes.new("headlight")
me.from_pydata([(side_x(v.x, v.y) - 0.004, v.x, v.y) for v in vco], [], [list(f) for f in fc])
me.materials.append(M_HL)
for p in me.polygons: p.use_smooth = True
hl = bpy.data.objects.new("CAR_headlight_W222", me); S.collection.objects.link(hl); hl.parent = RIG
# door mirror (body colour cap + black arm)
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=1.0)
for v in bm.verts:   # W222 mirror: ~250 mm long housing, 150 mm tall, flat glass face toward the rear
    x, y, z = v.co; y = min(y, 0.35)
    v.co = Vector((x * 0.115 * (1 - 0.15 * z), y * 0.105, z * 0.078 * (1 + 0.1 * x)))
me = bpy.data.meshes.new("mirror"); bm.to_mesh(me); bm.free(); me.materials.append(M_PAINT)
for p in me.polygons: p.use_smooth = True
mir = bpy.data.objects.new("CAR_mirror", me); S.collection.objects.link(mir); mir.parent = RIG
mir.location = (-1.05, -0.95, 1.10); mir.rotation_euler = (0, 0, math.radians(-12))
bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
for v in bm.verts: v.co = Vector((v.co.x * 0.16, v.co.y * 0.07, v.co.z * 0.035))
me = bpy.data.meshes.new("mirror_arm"); bm.to_mesh(me); bm.free(); me.materials.append(M_PAINT)
arm = bpy.data.objects.new("CAR_mirror_arm", me); S.collection.objects.link(arm); arm.parent = RIG
arm.location = (side_x(-0.93, 1.06) - 0.06, -0.93, 1.06)
# ---------------------------------------------------------------- kinematics (Ackermann, rear-axle bicycle model, no-slip tracks)
CAM = [list(r) for r in CAMO.matrix_basis] if False else None
DR = [[-0.0,-0.0],[0.2,0.0],[0.5,0.2],[0.6,0.2],[0.9,0.1],[1.0,0.2],[0.7,0.5],[-0.3,1.2],[-1.7,1.9],[-3.4,2.7],[-5.1,3.5],[-6.7,4.2],[-8.5,4.7],[-10.2,5.1],[-11.1,5.2],[-11.5,5.2],[-11.9,5.2],[-12.8,5.2],[-13.6,5.4],[-14.0,5.9],[-14.7,6.3],[-15.8,6.8],[-17.3,7.3],[-18.0,7.9],[-18.2,8.1],[-18.2,7.8],[-16.2,6.3],[-12.3,3.5],[-9.4,2.6],[-8.0,4.5],[-4.1,3.0],[-1.6,2.0],[0.0,1.3],[1.2,0.8],[1.3,0.8],[1.1,0.8],[1.2,0.5],[1.0,0.2],[0.9,0.2],[1.1,0.2],[1.0,0.1],[0.7,0.1],[0.5,0.2],[0.5,0.3],[0.5,0.3],[0.5,0.1],[0.4,-0.0],[0.3,-0.1],[0.2,-0.1],[-0.1,-0.1],[-0.2,-0.1],[-0.1,-0.1]]
F = 163.6
CAM0 = [[-0.62659,-0.15607,-0.76361,-1.25],[-0.77841,0.17474,0.60297,0.50842],[0.03931,0.97213,-0.23094,0.28]]
# camera keeps its calibrated pose relative to the wheel centre (wheel moved out/up)
# reframing: camera keeps its calibrated orientation, its offset from the wheel centre is scaled (CAM_SCALE)
for k_, wc_old, wc_new in ((0, old_pivot.x, -TF / 2), (1, 0.0, 0.0), (2, old_pivot.z, R_STAT)):
    CAM0[k_][3] = wc_new + CAM_SCALE * (CAM0[k_][3] - wc_old)
M0 = Matrix((CAM0[0], CAM0[1], CAM0[2], (0, 0, 0, 1)))
def ss(k): k = min(1, max(0, k)); return k * k * (3 - 2 * k)
def v_rear(t):
    rev = 1.0 if t < 0.9 else ((1 - min(1, (t - 0.9) / 1.35)) ** 1.5 if t < 2.25 else 0.0)
    fwd = 0.0 if t < 5.6 else ss((t - 5.6) / 2.2) * (1 + 0.25 * min(1, max(0, (t - 7.8) / 4.5)))
    return -P["vr"] * rev + P["vf"] * fwd
def delta(t):
    if t < 3.1: return P["dL"]
    if t < 5.1: return P["dL"] + (-P["dR"] - P["dL"]) * ss((t - 3.1) / 2.0)
    return -P["dR"]
def wheel_angle(dc, side):
    if abs(dc) < 1e-6: return 0.0
    Rr = WB / math.tan(abs(dc)); s = math.copysign(1, dc)
    inner = (side == -1 and s > 0) or (side == 1 and s < 0)
    return s * math.atan(WB / (Rr - TF / 2)) if inner else s * math.atan(WB / (Rr + TF / 2))
def wheel_pts(x, y, p, dc):
    fx, fy = x - math.sin(p) * WB, y + math.cos(p) * WB; c, s = math.cos(p), math.sin(p); out = {}
    for nm, (ax_, ay_, half, front, side) in {"FL": (fx, fy, TF / 2, True, -1), "FR": (fx, fy, TF / 2, True, 1),
                                               "RL": (x, y, TR / 2, False, -1), "RR": (x, y, TR / 2, False, 1)}.items():
        out[nm] = (ax_ + c * side * half, ay_ + s * side * half, p + (wheel_angle(dc, side) if front else 0.0))
    return out
# rear-left wheel (visible far down the flank)
RLS = bpy.data.objects.new("RIG_spin_RL", None); S.collection.objects.link(RLS); RLS.parent = RIG
RLS.location = (-TR / 2, -WB, R_STAT)
RLO = bpy.data.objects.new("RIG_orient_spin_RL", None); S.collection.objects.link(RLO); RLO.parent = RLS
RLO.location = OSPIN.location; RLO.rotation_euler = OSPIN.rotation_euler
add_wheel("WHL_C26_RL", RLO, zc_old)
t2 = bpy.data.objects.new("WHL_tyre_RL", old_tyre.data); S.collection.objects.link(t2); t2.parent = RLO
bolts(RLO, zc_old, "RL")
for o in (RIG, ST, SP, CAMO, RLS): o.animation_data_clear()
CAMO.parent = RIG; CAMO.matrix_parent_inverse = Matrix.Identity(4); CAMO.rotation_mode = 'QUATERNION'; CAMO.data.lens = F / 360 * 36
pre = []; bx, by, bp = 0.0, -WB, 0.0
for i in range(120):
    ds = P["vr"] / FPS; d = P["dL"]; bx -= math.sin(bp) * ds; by += math.cos(bp) * ds; bp += ds * math.tan(d) / WB
    pre.append((-(i + 1) / FPS, bx, by, bp, d))
pre = pre[::-1]
rnd = random.Random(7); jx = jy = 0.0; xr_, yr_, psi = 0.0, -WB, 0.0; prevq = None; spin = spinR = 0.0; path = []; last = None
for f in range(1, 312):
    i = f - 1; t = i / FPS; d = delta(t); W_ = wheel_pts(xr_, yr_, psi, d)
    if last is not None:
        for nm in ("FL", "RL"):
            dx_, dy_ = W_[nm][0] - last[nm][0], W_[nm][1] - last[nm][1]; hd = W_[nm][2]
            ds_ = (dx_ * (-math.sin(hd)) + dy_ * math.cos(hd)) / R_ROLL
            if nm == "FL": spin += ds_
            else: spinR += ds_
    last = W_
    RIG.location = (xr_ - math.sin(psi) * WB, yr_ + math.cos(psi) * WB, 0); RIG.rotation_euler = (0, 0, psi)
    RIG.keyframe_insert("location", frame=f); RIG.keyframe_insert("rotation_euler", frame=f)
    ST.rotation_euler = (0, 0, wheel_angle(d, -1)); ST.keyframe_insert("rotation_euler", frame=f)
    SP.rotation_euler = (-spin, 0, 0); SP.keyframe_insert("rotation_euler", frame=f)
    RLS.rotation_euler = (-spinR, 0, 0); RLS.keyframe_insert("rotation_euler", frame=f)
    a = i / 6; k0 = min(int(a), len(DR) - 1); k1 = min(k0 + 1, len(DR) - 1); w = a - int(a)
    dx = DR[k0][0] * (1 - w) + DR[k1][0] * w; dy = DR[k0][1] * (1 - w) + DR[k1][1] * w
    jx = 0.6 * jx + rnd.gauss(0, 0.35); jy = 0.6 * jy + rnd.gauss(0, 0.35)
    Mc = M0 @ Matrix.Rotation(math.atan((dx + jx) / F), 4, 'Y') @ Matrix.Rotation(math.atan((dy + jy) / F), 4, 'X')
    loc, q, _ = Mc.decompose()
    if prevq is not None: q.make_compatible(prevq)
    prevq = q.copy(); CAMO.location = loc; CAMO.rotation_quaternion = q
    CAMO.keyframe_insert("location", frame=f); CAMO.keyframe_insert("rotation_quaternion", frame=f)
    path.append((t, xr_, yr_, psi, d))
    ds = v_rear(t) / FPS; xr_ += -math.sin(psi) * ds; yr_ += math.cos(psi) * ds; psi += ds * math.tan(d) / WB
for o in (RIG, ST, SP, CAMO, RLS):
    for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
allp = pre + path
trk = bpy.data.materials["M_tyre_track"]; envc = bpy.data.collections.get("ENV") or S.collection
PROF = [(-0.135, 0.0), (-0.118, 0.016), (-0.105, 0.006), (0.105, 0.006), (0.118, 0.016), (0.135, 0.0)]
def track(nm):
    pts = []; lastp = None
    for (t, x, y, p, d) in allp:
        cx, cy, hd = wheel_pts(x, y, p, d)[nm]
        if lastp and math.hypot(cx - lastp[0], cy - lastp[1]) < 0.010: continue
        pts.append((cx, cy, hd, t)); lastp = (cx, cy)
    me = bpy.data.meshes.new("TRK_" + nm); bm = bmesh.new(); uvl = bm.loops.layers.uv.new("UVMap"); tl = bm.verts.layers.float.new("tpass")
    s = 0.0; prev = None; rows = []
    for (cx, cy, hd, t) in pts:
        if prev: s += math.hypot(cx - prev[0], cy - prev[1])
        nx, ny = math.cos(hd), math.sin(hd); row = []
        for (l, h) in PROF:
            vv = bm.verts.new((cx + nx * l, cy + ny * l, 0.002 + h)); vv[tl] = t; row.append(vv)
        rows.append((row, s)); prev = (cx, cy)
    for (r0_, s0), (r1_, s1) in zip(rows[:-1], rows[1:]):
        for kq in range(len(PROF) - 1):
            fa = bm.faces.new((r0_[kq], r0_[kq + 1], r1_[kq + 1], r1_[kq]))
            for lp, (uu, vv) in zip(fa.loops, [(s0, kq / 5), (s0, (kq + 1) / 5), (s1, (kq + 1) / 5), (s1, kq / 5)]): lp[uvl].uv = (uu, vv)
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("TRK_" + nm, me); envc.objects.link(o); me.materials.append(trk); return len(rows)
rows = [track(nm) for nm in ("FL", "FR", "RL", "RR")]
sun = [o for o in OB if o.type == 'LIGHT']
for l in sun: l.data.specular_factor = 0.0; l.visible_glossy = False
# final look: Cycles path tracing (correct occlusion inside the deep-concave C26 face)
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = 32; S.cycles.use_denoising = True
S.cycles.max_bounces = 6; S.cycles.transparent_max_bounces = 64; S.render.use_persistent_data = True
S.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("RESULT", {"zc_old": round(zc_old, 4), "TF": round(TF, 4), "lock_bicycle_deg": round(math.degrees(D_LOCK), 2),
      "FL_inner_lock_deg": round(math.degrees(wheel_angle(D_LOCK, -1)), 2), "FR_outer_lock_deg": round(math.degrees(wheel_angle(D_LOCK, 1)), 2),
      "FL_right_deg": round(math.degrees(wheel_angle(-P["dR"], -1)), 2), "end_yaw_deg": round(math.degrees(psi), 1),
      "spin_turns": round(spin / 6.2832, 2), "track_rows": rows, "body_faces": len(body_me.polygons)})

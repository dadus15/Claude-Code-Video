"""Turismo Forged — modele proceduralne C01, C19-R, RR odtworzone z packshotów (widok 3/4).
Przybliżenia wizualne do filmu, NIE geometria produkcyjna (do tego CAD).
Oś felgi = Y, czoło patrzy w -Y. R = promień zewnętrzny rantu, W = szerokość beczki.

C01  : 5 ramion rozwidlonych w „Y” (10 końcówek), okna frezowane w ramionach, wąski rant czołowy.
C19-R: rodzina C19 („Y” + gałęzie) + szeroki zintegrowany aero-ring z 18 prostokątnymi kieszeniami.
RR   : 40 cienkich prostych szprych, duży dekiel TURISMO typu gravity cap (nie obraca się z felgą).
"""
import bpy, math
from mathutils import Vector

def _link(o, mat, parent):
    o.data.materials.append(mat); o.parent = parent; return o

def _box(p1, p2, width, thick, mat, parent, bevel=0.0025):
    d = p2 - p1; L = d.length
    bpy.ops.mesh.primitive_cube_add(location=(p1 + p2) / 2); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.normalized().to_track_quat('X', 'Y')
    o.scale = (L / 2, thick / 2, width / 2)
    if bevel:
        b = o.modifiers.new('bev', 'BEVEL'); b.width = bevel; b.segments = 2; b.limit_method = 'ANGLE'
    return _link(o, mat, parent)

def _pol(r, deg, y):
    a = math.radians(deg); return Vector((math.cos(a) * r, y, math.sin(a) * r))

def _cyl(r, depth, y, mat, parent, verts=160, fill='NGON'):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=(0, y, 0), rotation=(math.radians(90), 0, 0),
                                        vertices=verts, end_fill_type=fill)
    return _link(bpy.context.object, mat, parent)

def _torus(R, r, y, mat, parent):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=(0, y, 0),
                                     rotation=(math.radians(90), 0, 0), major_segments=160)
    return _link(bpy.context.object, mat, parent)

def _annulus(r_in, r_out, depth, y, mat, parent, cutters=()):
    ring = _cyl(r_out, depth, y, mat, parent)
    hole = _cyl(r_in, depth * 3, y, mat, parent)
    m = ring.modifiers.new('hole', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = hole
    for c in cutters:
        mc = ring.modifiers.new('cut', 'BOOLEAN'); mc.operation = 'DIFFERENCE'; mc.object = c
    bpy.context.view_layer.objects.active = ring
    for mod in list(ring.modifiers): bpy.ops.object.modifier_apply(modifier=mod.name)
    for o in (hole, *cutters): bpy.data.objects.remove(o, do_unlink=True)
    return ring

def _barrel(R, W, m_face, m_lip, m_dark, parent):
    b = _cyl(R - 0.010, W, W / 2, m_face, parent, fill='NOTHING'); b.modifiers.new('s', 'SOLIDIFY').thickness = 0.006
    _torus(R - 0.007, 0.008, 0.0, m_lip, parent)          # rant czołowy
    _torus(R - 0.007, 0.007, W, m_face, parent)           # rant tylny
    _cyl(R - 0.016, 0.004, W * 0.75, m_dark, parent)      # ciemne wnętrze beczki (głębia za ramionami)

def _hub(R, y_hub, m_face, m_dark, m_lip, parent, r_boss=0.27, cap=0.08, lugs=True):
    _cyl(r_boss * R, 0.05, y_hub + 0.012, m_face, parent, verts=96)
    if lugs:
        for i in range(5):
            a = math.radians(90 + 36 + i * 72)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.035 * R, depth=0.012, location=(math.cos(a) * 0.19 * R, y_hub - 0.0135, math.sin(a) * 0.19 * R),
                                                rotation=(math.radians(90), 0, 0), vertices=24)
            _link(bpy.context.object, m_dark, parent)
    _cyl(cap * R, 0.012, y_hub - 0.016, m_dark, parent, verts=64)
    _torus(cap * R * 1.06, 0.004, y_hub - 0.022, m_lip, parent)

def _y_spokes(R, m_face, parent, r_hub, r_fork, r_end, spread, y_rim, y_hub, w_trunk, w_arm, windows=True, extra_branch=False):
    def y_at(r): return y_hub + (y_rim - y_hub) * (r - r_hub) / (r_end - r_hub)
    ends = []
    for i in range(5):
        base = 90 + i * 72
        offs = (-1, 1) if windows else (0,)
        for off in offs:   # pień: dwie listwy = okno frezowane
            _box(_pol(r_hub, base + off * 4.0, y_at(r_hub)), _pol(r_fork, base + off * 2.2, y_at(r_fork)), w_trunk * R, 0.022, m_face, parent)
        for side in (-1, 1):
            a_end = base + side * spread; ends.append(a_end)
            for off in offs:
                _box(_pol(r_fork, base + side * 2.5 + off * 1.0, y_at(r_fork)), _pol(r_end, a_end + off * 1.6, y_at(r_end)), w_arm * R, 0.020, m_face, parent)
            _box(_pol(r_end - 0.01, a_end, y_rim), _pol(R * 0.93, a_end, y_rim), 0.16 * R, 0.022, m_face, parent)   # stopka
            if extra_branch:   # C19: gałąź łącząca ramię z sąsiednim polem (pajęczyna)
                _box(_pol((r_fork + r_end) / 2, base + side * spread * 0.55, y_at((r_fork + r_end) / 2)),
                     _pol(r_end, base + side * (spread + 20), y_rim), w_arm * 0.7 * R, 0.016, m_face, parent)
        _box(_pol(r_fork - 0.01, base - 4, y_at(r_fork)), _pol(r_fork - 0.01, base + 4, y_at(r_fork)), 0.022, 0.024, m_face, parent)
    return ends

def build_c01(holder, R, W, m_face, m_dark, m_lip):
    _barrel(R, W, m_face, m_lip, m_dark, holder)
    _annulus(0.90 * R, 0.975 * R, 0.014, 0.008, m_face, holder)          # wąski rant czołowy, bez aero-ringu
    _y_spokes(R, m_face, holder, 0.24 * R, 0.50 * R, 0.89 * R, 15.0, 0.004, 0.042, 0.096, 0.059)
    _hub(R, 0.042, m_face, m_dark, m_lip, holder)

def build_c19r(holder, R, W, m_face, m_dark, m_lip):
    _barrel(R, W, m_face, m_lip, m_dark, holder)
    # aero-ring: szeroki pierścień czołowy z 18 prostokątnymi kieszeniami (przelotowymi), między nimi promieniowe żebra
    r_in, r_out, n = 0.78 * R, 0.975 * R, 18
    cutters = []
    for k in range(n):
        a = math.radians(k * 360 / n + 10)
        rm = (r_in + r_out) / 2 + 0.004
        bpy.ops.mesh.primitive_cube_add(location=(math.cos(a) * rm, 0.012, math.sin(a) * rm)); c = bpy.context.object
        c.rotation_euler = (0, -a, 0); c.scale = ((r_out - r_in) * 0.36, 0.06, 2 * math.pi * rm / n * 0.34)
        bv = c.modifiers.new('b', 'BEVEL'); bv.width = 0.006; bv.segments = 3
        bpy.context.view_layer.objects.active = c; bpy.ops.object.modifier_apply(modifier='b'); cutters.append(c)
    _annulus(r_in, r_out, 0.030, 0.014, m_face, holder, cutters)
    _y_spokes(R, m_face, holder, 0.24 * R, 0.47 * R, 0.79 * R, 17.0, 0.006, 0.048, 0.090, 0.050, windows=False, extra_branch=True)
    _hub(R, 0.048, m_face, m_dark, m_lip, holder)

def build_rr(holder, R, W, m_face, m_dark, m_lip, cap_parent=None):
    """cap_parent: obiekt NIEobracający się (pivot położenia) — gravity cap zostaje poziomo w trakcie obrotu."""
    _barrel(R, W, m_face, m_lip, m_dark, holder)
    _annulus(0.92 * R, 0.975 * R, 0.012, 0.007, m_face, holder)
    y_rim, y_hub, r_hub, r_end = 0.006, 0.030, 0.36 * R, 0.93 * R
    for k in range(40):
        a = k * 9.0
        _box(_pol(r_hub, a, y_hub), _pol(r_end, a, y_rim), 0.028 * R, 0.016, m_face, holder, bevel=0.0015)
    _cyl(r_hub + 0.004, 0.04, y_hub + 0.01, m_face, holder, verts=128)
    capp = cap_parent or holder
    _cyl(0.22 * R, 0.010, y_hub - 0.012, m_dark, capp, verts=96)               # dekiel (czarny połysk)
    _torus(0.225 * R, 0.005, y_hub - 0.017, m_lip, capp)                       # chromowany pierścień
    bpy.ops.object.text_add(location=(0, y_hub - 0.0185, 0), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = 'TURISMO'; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
    t.data.size = 0.022; t.data.extrude = 0.0005; t.rotation_euler = (math.radians(90), 0, 0)
    t.data.materials.append(m_lip); t.parent = capp

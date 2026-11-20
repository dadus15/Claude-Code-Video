"""Turismo | 'Nie o takie Turismo' v2 — scena Blender: felga z ekranu na podstawkę z rolkami + podmiana modeli C01 -> C19-R -> RR w obrocie.
Uruchomienie:  blender -b -P scena_c01.py -- [--wheel /sciezka/C01.obj] [--out katalog] [--preview] [--stills]
Bez --wheel używana jest felga ZASTĘPCZA (nie geometria C01).
Jednostki: metry. 25 kl./s. Kadr 9:16.
"""
import bpy, math, sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import felgi
from mathutils import Vector

argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--wheel', default='')            # (zgodność wstecz) = pierwszy model
ap.add_argument('--models', default='C01,C19-R,RR')   # kolejność pokazu na podstawce
ap.add_argument('--files', default='')               # pliki CAD w tej samej kolejności, rozdzielone przecinkami (puste = zastępcza)
ap.add_argument('--swap', action='store_true')       # render sekwencji podmiany modeli z kamery detalu            # OBJ/FBX/GLB C01 (oś obrotu = oś Y po imporcie, patrz WHEEL_AXIS_FIX)
ap.add_argument('--out', default='//render')
ap.add_argument('--preview', action='store_true') # animacja 360x640 niska jakość
ap.add_argument('--stills', action='store_true')  # 4 klatki kluczowe K1-K4 720x1280
ap.add_argument('--finish', default='brushed_grey', choices=['brushed_grey','satin_black','brushed_bronze','gloss_silver'])
a = ap.parse_args(argv)

FPS = 25
R_WHEEL = 0.27      # promień zewn. rantu felgi 20" (ok. 54 cm średnicy)
W_WHEEL = 0.24      # szerokość beczki (~9.5")
R_ROLL = 0.03       # promień rolki
ROLL_GAP = 0.22     # rozstaw osi rolek
TABLE_Z = 0.45      # blat stolika
STAND_H = 0.045     # wysokość podstawy
# wysokość środka felgi leżącej na dwóch rolkach (geometria styku)
ROLL_Z = TABLE_Z + STAND_H + R_ROLL
WHEEL_REST_Z = ROLL_Z + math.sqrt((R_WHEEL+R_ROLL)**2 - (ROLL_GAP/2)**2)
STAND_X = 0.42      # podstawka na prawo od laptopa
SCREEN_C = Vector((-0.05, 0.212, TABLE_Z+0.115))
SCREEN_TILT = -15.0   # środek obrazu felgi na matrycy laptopa
SCREEN_DIAM = 0.10  # średnica felgi na stronie (~1/3 szerokości matrycy 14")

# ---------- czysta scena ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = 380
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y = (720, 1280)
sc.view_settings.view_transform = 'Filmic' if 'Filmic' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Standard'

def mat(name, base, metal=0.0, rough=0.5, aniso=0.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*base, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    if 'Anisotropic' in p.inputs: p.inputs['Anisotropic'].default_value = aniso
    if emit:
        key = 'Emission Color' if 'Emission Color' in p.inputs else 'Emission'
        p.inputs[key].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = strength
    return m

FIN = {'brushed_grey':((0.42,0.43,0.45),1,0.28,0.6), 'satin_black':((0.03,0.03,0.035),0.6,0.45,0.0),
       'brushed_bronze':((0.45,0.30,0.17),1,0.3,0.6), 'gloss_silver':((0.8,0.81,0.83),1,0.12,0.0)}
c,mt,ro,an = FIN[a.finish]
M_WHEEL = mat('Felga_'+a.finish, c, mt, ro, an)
M_LIP   = mat('Rant_polerowany', (0.85,0.86,0.88), 1, 0.08)
M_BLACK = mat('Czarny_anod', (0.015,0.015,0.017), 0.8, 0.35)
M_ROLL  = mat('Stal_rolki', (0.7,0.7,0.72), 1, 0.2)
M_WALL  = mat('Lamele', (0.02,0.02,0.022), 0, 0.55)
M_TABLE = mat('Blat', (0.012,0.012,0.012), 0, 0.7)
M_SCREEN= mat('Ekran', (0.8,0.8,0.82), 0, 0.3, emit=(0.85,0.87,0.9), strength=1.2)
M_LAP   = mat('Laptop', (0.55,0.56,0.58), 1, 0.3)

def add(obj, m): obj.data.materials.append(m); return obj

# ---------- otoczenie ----------
bpy.ops.mesh.primitive_plane_add(size=6, location=(0,0,0)); add(bpy.context.object, M_TABLE)
bpy.ops.mesh.primitive_cube_add(location=(0.15,0.15,TABLE_Z/2)); t=bpy.context.object; t.scale=(0.75,0.32,TABLE_Z/2); add(t,M_TABLE)
for i in range(-30,31):   # ściana z pionowych lameli (jak tło @STAND)
    bpy.ops.mesh.primitive_cube_add(location=(i*0.05, 1.6, 1.4)); s=bpy.context.object; s.scale=(0.017,0.02,1.4); add(s,M_WALL)
# laptop: matryca pod ~25° do kamery
bpy.ops.mesh.primitive_cube_add(location=(-0.05,0.12,TABLE_Z+0.008)); b=bpy.context.object; b.scale=(0.16,0.11,0.008); add(b,M_LAP)
bpy.ops.mesh.primitive_cube_add(location=(-0.05,0.23,TABLE_Z+0.11)); lid=bpy.context.object; lid.scale=(0.16,0.006,0.105); lid.rotation_euler=(math.radians(-15),0,0); add(lid,M_BLACK)
bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.05,0.222,TABLE_Z+0.11)); scr=bpy.context.object
scr.scale=(0.148,0.095,1); scr.rotation_euler=(math.radians(90-15),0,0); add(scr,M_SCREEN)

# ---------- podstawka z dwiema rolkami (kształt jak @STAND, bez napisów) ----------
bpy.ops.mesh.primitive_cube_add(location=(STAND_X,0.05,TABLE_Z+STAND_H/2)); base=bpy.context.object
base.scale=(0.19,0.13,STAND_H/2); add(base,M_BLACK)
bev=base.modifiers.new('bev','BEVEL'); bev.width=0.006; bev.segments=3
rollers=[]
for dx in (-ROLL_GAP/2, ROLL_GAP/2):
    bpy.ops.mesh.primitive_cylinder_add(radius=R_ROLL, depth=0.26, location=(STAND_X+dx,0.05,ROLL_Z), rotation=(math.radians(90),0,0))
    r=bpy.context.object; add(r,M_ROLL); rollers.append(r)
    for sy in (-0.135,0.135):   # boczne wsporniki
        bpy.ops.mesh.primitive_cube_add(location=(STAND_X+dx,0.05+sy,TABLE_Z+STAND_H+0.012)); k=bpy.context.object; k.scale=(0.022,0.008,0.03); add(k,M_BLACK)

# ---------- felga ----------
wheel = bpy.data.objects.new('FELGA', None); sc.collection.objects.link(wheel)   # pivot = oś felgi (Y), animowany
def build_placeholder(style, holder):
    """Felgi ZASTĘPCZE — różne układy ramion, żeby było widać podmianę. To NIE są geometrie Turismo."""
    def part(o, m=M_WHEEL):
        add(o,m); o.parent = holder; return o
    bpy.ops.mesh.primitive_cylinder_add(radius=R_WHEEL-0.012, depth=W_WHEEL, location=(0,W_WHEEL/2,0), rotation=(math.radians(90),0,0), vertices=128, end_fill_type='NOTHING')
    b=part(bpy.context.object); b.modifiers.new('s','SOLIDIFY').thickness=0.006
    bpy.ops.mesh.primitive_torus_add(major_radius=R_WHEEL-0.008, minor_radius=0.009, rotation=(math.radians(90),0,0), major_segments=128)
    part(bpy.context.object, M_LIP)
    ring = 0.022 if style=='C19-R' else 0.012          # C19-R: grubszy pierścień = miejsce na aero-ring
    bpy.ops.mesh.primitive_torus_add(major_radius=R_WHEEL-0.03, minor_radius=ring, location=(0,0.012,0), rotation=(math.radians(90),0,0), major_segments=128)
    part(bpy.context.object)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.06, location=(0,0.035,0), rotation=(math.radians(90),0,0), vertices=64); part(bpy.context.object)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.034, depth=0.012, rotation=(math.radians(90),0,0), vertices=48); part(bpy.context.object, M_BLACK)
    layout = {'C01':[(i*72+o) for i in range(5) for o in (-7,7)],
              'C19-R':[i*36 for i in range(10)],
              'RR':[(i*72+o) for i in range(5) for o in (-14,0,14)]}.get(style,[i*72 for i in range(5)])
    w = {'C01':0.022,'C19-R':0.016,'RR':0.012}.get(style,0.02)
    for deg in layout:
        ang=math.radians(deg+90); L=R_WHEEL-0.03-0.08; mid=0.08+L/2
        bpy.ops.mesh.primitive_cube_add(location=(math.cos(ang)*mid,0.03,math.sin(ang)*mid))
        sp=part(bpy.context.object); sp.scale=(L/2,w,0.013); sp.rotation_euler=(0,-ang,0)
        bv=sp.modifiers.new('b','BEVEL'); bv.width=0.005; bv.segments=2
    ang=math.radians(-30)   # wentyl na 4:00
    bpy.ops.mesh.primitive_cylinder_add(radius=0.005, depth=0.02, location=(math.cos(ang)*(R_WHEEL-0.045),0.0,math.sin(ang)*(R_WHEEL-0.045)), rotation=(math.radians(90),0,0))
    part(bpy.context.object, M_BLACK)

def import_cad(path, holder):
    ext=os.path.splitext(path)[1].lower(); before=set(bpy.data.objects)
    if ext=='.obj': bpy.ops.wm.obj_import(filepath=path)
    elif ext=='.fbx': bpy.ops.import_scene.fbx(filepath=path)
    elif ext in ('.glb','.gltf'): bpy.ops.import_scene.gltf(filepath=path)
    new=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
    pts=[o.matrix_world @ Vector(v) for o in new for v in o.bound_box]
    mn=Vector([min(p[i] for p in pts) for i in range(3)]); mx=Vector([max(p[i] for p in pts) for i in range(3)])
    size=mx-mn; ctr=(mn+mx)/2; k=2*R_WHEEL/sorted(size)[-1]; axis=min(range(3), key=lambda i:size[i])
    inner=bpy.data.objects.new(holder.name+'_CAD',None); sc.collection.objects.link(inner); inner.parent=holder
    inner.scale=(k,k,k); inner.rotation_euler={0:(0,0,math.radians(90)),1:(0,0,0),2:(math.radians(90),0,0)}[axis]
    for o in new:
        o.location-=ctr; o.parent=inner; o.data.materials.clear(); o.data.materials.append(M_WHEEL)

MODELS=[m.strip() for m in a.models.split(',') if m.strip()]
FILES=(a.files.split(',') if a.files else ([a.wheel] if a.wheel else []))
holders=[]; PLACEHOLDER=True
for i,mname in enumerate(MODELS):
    h=bpy.data.objects.new('MODEL_'+mname,None); sc.collection.objects.link(h); h.parent=wheel
    f=FILES[i].strip() if i < len(FILES) else ''
    if f and os.path.exists(f): import_cad(f,h); PLACEHOLDER=False
    elif mname=='C01':   felgi.build_c01(h, R_WHEEL, W_WHEEL, M_WHEEL, M_BLACK, M_LIP)
    elif mname=='C19-R': felgi.build_c19r(h, R_WHEEL, W_WHEEL, M_WHEEL, M_BLACK, M_LIP)
    elif mname=='RR':
        # gravity cap: podąża za położeniem i przechyłem felgi, ale NIE za obrotem wokół osi (Child Of bez rotacji Y)
        capp=bpy.data.objects.new('RR_GRAVITY_CAP',None); sc.collection.objects.link(capp)
        cc=capp.constraints.new('CHILD_OF'); cc.target=wheel; cc.use_rotation_y=False
        felgi.build_rr(h, R_WHEEL, W_WHEEL, M_WHEEL, M_BLACK, M_LIP, cap_parent=capp)
    else: build_placeholder(mname,h)
    holders.append(h)

# ---------- choreografia (klatki od 19,0 s spotu = kl. 1 tutaj) ----------
# K1 kl.1 felga na ekranie | K2 kl.11 kciuk na rancie 12:00 | podmiana 2D->3D kl.11-17 pod kciukiem
# wyjście z ekranu + skala do 1:1 kl.17-63 | lot nad podstawkę do kl.101 (K3) | styk na rolkach kl.116 (K4)
# puszczenie kl.116-126 | pchnięcie kl.126 | obrót do kl.200 (okno detalu ok. kl.146-153)
def key(f, loc, scl, rot_y=0.0, tilt=0.0, pitch=0.0):
    wheel.location = loc; wheel.scale = (scl,scl,scl)
    wheel.rotation_euler = (math.radians(pitch), rot_y, math.radians(tilt))
    wheel.keyframe_insert('location', frame=f); wheel.keyframe_insert('rotation_euler', frame=f)
    wheel.keyframe_insert('scale', frame=f)
s0 = SCREEN_DIAM/(2*R_WHEEL)
rest = Vector((STAND_X, 0.05, WHEEL_REST_Z))
above = rest + Vector((0,0,0.10))          # dłoń szerokości nad rolkami
key(1,  SCREEN_C, s0, pitch=SCREEN_TILT)
key(17, SCREEN_C + Vector((0,-0.004,0)), s0, pitch=SCREEN_TILT)
key(40, Vector((0.08,-0.10,TABLE_Z+0.30)), 0.6, tilt=-10, pitch=-6)
key(63, Vector((0.30,-0.06,TABLE_Z+0.40)), 1.0, tilt=-8)
key(101, above, 1.0, tilt=0)
key(116, rest, 1.0, tilt=0)
key(126, rest, 1.0, tilt=0)
# obrót: profil prędkości (obr./s) liczony klatka po klatce, zgodnie z ruchem wskazówek widziany z kamery;
# rolki przeciwnie z przełożeniem R/r. Podmiana modelu w szczycie obrotów (rozmycie ruchu ją ukrywa).
SWAPS=[245, 320][:max(0,len(MODELS)-1)]          # klatki podmiany: C01->C19-R, C19-R->RR
def omega(f):
    w=0.0
    if f>=126: w=1.4*math.exp(-(f-126)/60.0)+0.35          # pchnięcie: 1,4 obr./s, wygasa do 0,35
    for sw in SWAPS:                                         # „dopchnięcie”: 0,35 -> 5 obr./s -> 0,35
        d=f-sw; w+= 4.7*math.exp(-(d/9.0)**2)
    return w
ang=0.0
for f in range(126, sc.frame_end+1):
    ang += omega(f)*2*math.pi/FPS
    wheel.rotation_euler.y = ang; wheel.keyframe_insert('rotation_euler', index=1, frame=f)
    for r in rollers:
        r.rotation_euler.y = -ang*(R_WHEEL/R_ROLL); r.keyframe_insert('rotation_euler', index=1, frame=f)
for ob in [wheel]+rollers:
    for fc in ob.animation_data.action.fcurves:
        if fc.data_path=='rotation_euler' and fc.array_index==1:
            for kp in fc.keyframe_points: kp.interpolation='LINEAR'
for i,h in enumerate(holders):
    on_from = 1 if i==0 else SWAPS[i-1]
    on_to   = SWAPS[i] if i < len(SWAPS) else sc.frame_end+1
    for f,vis in ((1, i==0), (on_from, True), (on_to, False)):
        if f>sc.frame_end: continue
        extra=[o for o in bpy.data.objects if o.name.startswith('RR_GRAVITY_CAP')] if MODELS[i]=='RR' else []
        for ob in [h]+list(h.children_recursive)+[c for e in extra for c in [e]+list(e.children_recursive)]:
            ob.hide_render = not vis; ob.hide_viewport = not vis
            ob.keyframe_insert('hide_render', frame=f); ob.keyframe_insert('hide_viewport', frame=f)
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5

# ---------- światło: biuro + refleks z boku (jak @STAND) + czerwony akcent ----------
def area(name, loc, rot, size, energy, color=(1,1,1)):
    bpy.ops.object.light_add(type='AREA', location=loc, rotation=rot); L=bpy.context.object; L.name=name
    L.data.size=size; L.data.energy=energy; L.data.color=color; return L
area('Key_lewy', (-1.2,-0.8,1.6), (math.radians(55),0,math.radians(-55)), 1.2, 260)
area('Refleks_pasek', (1.1,-0.2,0.9), (math.radians(90),0,math.radians(75)), 0.15, 120)
L=area('Czerwony_akcent', (1.0,1.2,1.1), (math.radians(90),0,math.radians(130)), 0.08, 90, (1,0.05,0.08)); L.data.shape='RECTANGLE'; L.data.size_y=1.8
world=bpy.data.worlds.new('W'); sc.world=world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[1].default_value=0.03

# ---------- kamera produktowa 3/4 (jak KF-O2) ----------
bpy.ops.object.camera_add(location=(0.80,-1.30,TABLE_Z+0.30)); cam=bpy.context.object; sc.camera=cam
cam.data.lens=30; cam.data.sensor_width=36
tgt=bpy.data.objects.new('cel',None); sc.collection.objects.link(tgt); tgt.location=(0.20,0.08,TABLE_Z+0.26)
tc=cam.constraints.new('TRACK_TO'); tc.target=tgt; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
cam.data.dof.use_dof=True; cam.data.dof.focus_object=tgt; cam.data.dof.aperture_fstop=4.0

bpy.ops.object.camera_add(location=(STAND_X+0.05,-1.05,WHEEL_REST_Z+0.05)); camd=bpy.context.object; camd.name='CAM_DETAL'
camd.data.lens=50; cd=camd.constraints.new('TRACK_TO'); tg2=bpy.data.objects.new('cel_detal',None); sc.collection.objects.link(tg2)
tg2.location=(STAND_X,0.05,WHEEL_REST_Z-0.06); cd.target=tg2; cd.track_axis='TRACK_NEGATIVE_Z'; cd.up_axis='UP_Y'
# ---------- render ----------
out = bpy.path.abspath(a.out); os.makedirs(out, exist_ok=True)
sc.cycles.use_denoising = False   # build z Ubuntu nie ma OIDN
if a.stills:
    sc.cycles.samples = 64
    for f,name in ((1,'K1'),(11,'K2'),(101,'K3'),(116,'K4'),(170,'F_obrot')):
        sc.frame_set(f); sc.render.filepath=os.path.join(out,f'{name}.png'); bpy.ops.render.render(write_still=True)
if a.swap:
    sc.camera=camd; sc.frame_start=200; sc.frame_end=380
    sc.render.resolution_x, sc.render.resolution_y = (360, 640); sc.cycles.samples = 10
    sc.render.image_settings.file_format='PNG'; sc.render.filepath=os.path.join(out,'swap_')
    bpy.ops.render.render(animation=True)
if a.preview:
    sc.frame_end=200; sc.render.resolution_x, sc.render.resolution_y = (360, 640); sc.cycles.samples = 10
    sc.render.image_settings.file_format='PNG'; sc.render.filepath=os.path.join(out,'prev_')
    bpy.ops.render.render(animation=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'scena_c01.blend'))
print('MODELE:', MODELS, 'ZASTEPCZE' if PLACEHOLDER else 'CAD', 'rest_z=%.3f' % WHEEL_REST_Z, 'swaps', SWAPS)

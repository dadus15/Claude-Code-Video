"""Render porównawczy modeli z packshotami: blender -b -P porownanie_felg.py -- KATALOG_WYJ [C01,C19-R,RR]"""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import felgi
argv = sys.argv[sys.argv.index('--')+1:]; out = argv[0]; models = (argv[1] if len(argv) > 1 else 'C01,C19-R,RR').split(',')
os.makedirs(out, exist_ok=True)
FIN = {'C01': ((0.30, 0.31, 0.33), 0.24), 'C19-R': ((0.78, 0.79, 0.81), 0.10), 'RR': ((0.30, 0.31, 0.33), 0.24)}
BUILD = {'C01': felgi.build_c01, 'C19-R': felgi.build_c19r, 'RR': felgi.build_rr}
for name in models:
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = 560
    def mat(n, c, met, r, an=0.0):
        m = bpy.data.materials.new(n); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
        p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Metallic'].default_value = met; p.inputs['Roughness'].default_value = r
        if 'Anisotropic' in p.inputs: p.inputs['Anisotropic'].default_value = an
        return m
    col, rough = FIN[name]
    face = mat('face', col, 1, rough, 0.6); dark = mat('dark', (0.01, 0.01, 0.012), 0.3, 0.25); lip = mat('lip', (0.85, 0.85, 0.87), 1, 0.08)
    h = bpy.data.objects.new(name, None); sc.collection.objects.link(h)
    BUILD[name](h, 0.27, 0.24, face, dark, lip)
    h.rotation_euler = (math.radians(-4), 0, math.radians(-32))
    w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.8
    for loc, rot, e in (((-1.2, -1.0, 1.0), (55, 0, -50), 300), ((1.2, -0.6, 0.4), (80, 0, 60), 200), ((0, 1.0, 1.4), (-40, 0, 180), 150)):
        bpy.ops.object.light_add(type='AREA', location=loc, rotation=[math.radians(v) for v in rot]); L = bpy.context.object; L.data.size = 1.5; L.data.energy = e
    bpy.ops.object.camera_add(location=(0, -1.9, 0.12)); cam = bpy.context.object; sc.camera = cam
    cam.rotation_euler = (math.radians(86.5), 0, 0); cam.data.lens = 62
    sc.render.filepath = os.path.join(out, f'BL_{name}.png'); bpy.ops.render.render(write_still=True)
print('OK', models)

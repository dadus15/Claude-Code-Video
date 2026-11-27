import bpy, time, numpy as np, sys
t=time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=sys.argv[-1], forward_axis='NEGATIVE_Z', up_axis='Y')
print('import', time.time()-t)
for o in bpy.context.scene.objects:
    me=o.data
    co=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',co); co=co.reshape(-1,3)
    print(o.name, len(me.vertices), len(me.polygons), [m.name for m in me.materials])
    print(' min',co.min(0).round(2),' max',co.max(0).round(2))
    # per-material bounds
    mi=np.empty(len(me.polygons),int); me.polygons.foreach_get('material_index',mi)
    for k,m in enumerate(me.materials):
        idx=np.where(mi==k)[0]
        vs=set()
        for p in idx[:200000]: vs.update(me.polygons[p].vertices)
        c=co[list(vs)]
        print('  mat',m.name,len(idx),'polys', c.min(0).round(1), c.max(0).round(1))
bpy.ops.wm.save_as_mainfile(filepath='/tmp/claude-0/-home-user-Claude-Code-Video/c7e0edf9-1a55-5bde-9974-f2ac598a2992/scratchpad/c26/c26_raw.blend')

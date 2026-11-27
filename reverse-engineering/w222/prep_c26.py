# normalize C26 CAD: metres, axle = +Z, outboard face toward +Z, wheel centreline at z=0
import bpy, numpy as np, mathutils, math
D='/tmp/claude-0/-home-user-Claude-Code-Video/c7e0edf9-1a55-5bde-9974-f2ac598a2992/scratchpad/c26/'
bpy.ops.wm.open_mainfile(filepath=D+'c26_raw.blend')
o=bpy.data.objects[0]; me=o.data; o.name='WHL_C26'; me.name='C26_cad'
me.transform(o.matrix_world); o.matrix_world=mathutils.Matrix.Identity(4)
me.transform(mathutils.Matrix.Translation((0,-0.285,-55.53)))
me.transform(mathutils.Matrix.Rotation(-math.pi/2,4,'X'))   # world Y -> Z ; face now at -Z
me.transform(mathutils.Matrix.Rotation(math.pi,4,'X'))      # flip: face toward +Z
me.transform(mathutils.Matrix.Scale(0.001,4))
co=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',co); co=co.reshape(-1,3)
r=np.hypot(co[:,0],co[:,1]); print('bounds',co.min(0).round(4),co.max(0).round(4))
# bolt holes: look for through holes near r=0.056 : angular histogram of verts with 0.045<r<0.067 near mounting face
n=len(me.polygons); pc=np.empty(n*3); me.polygons.foreach_get('center',pc); pc=pc.reshape(-1,3)
pn=np.empty(n*3); me.polygons.foreach_get('normal',pn); pn=pn.reshape(-1,3)
pr=np.hypot(pc[:,0],pc[:,1])
# faces whose normal points radially toward/away a hole axis: cylinder walls -> normals perpendicular to Z, at r 0.045..0.067
m=(np.abs(pn[:,2])<0.2)&(pr>0.044)&(pr<0.068)
th=np.degrees(np.arctan2(pc[m,1],pc[m,0]))%360
h,_=np.histogram(th,bins=72,range=(0,360)); print('hole angle hist peaks',np.argsort(-h)[:10]*5)
# outboard-facing flats (seat bottoms) near r 0.056
m2=(pn[:,2]>0.95)&(pr>0.045)&(pr<0.07)
zs=np.round(pc[m2,2],4); u,c=np.unique(zs,return_counts=True); print('seat flats z',[(float(a),int(b)) for a,b in zip(u,c) if b>20][:10])
m3=(pn[:,2]>0.95)&(pr<0.045); zs=np.round(pc[m3,2],4); u,c=np.unique(zs,return_counts=True); print('centre flats z',[(float(a),int(b)) for a,b in zip(u,c) if b>20][:10])
bpy.ops.wm.save_as_mainfile(filepath=D+'c26_m.blend')

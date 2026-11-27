import bpy, numpy as np, mathutils
D='/tmp/claude-0/-home-user-Claude-Code-Video/c7e0edf9-1a55-5bde-9974-f2ac598a2992/scratchpad/c26/'
bpy.ops.wm.open_mainfile(filepath=D+'c26_raw.blend')
o=bpy.data.objects[0]; me=o.data
me.transform(o.matrix_world); o.matrix_world=mathutils.Matrix.Identity(4)
me.transform(mathutils.Matrix.Translation((0,-0.285,-55.53)))
# rotate so axle = +Z (face toward +Z): world Y -> Z
me.transform(mathutils.Matrix.Rotation(-np.pi/2,4,'X'))
co=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',co); co=co.reshape(-1,3)
print('bounds',co.min(0).round(2),co.max(0).round(2))
n=len(me.polygons)
pc=np.empty(n*3); me.polygons.foreach_get('center',pc); pc=pc.reshape(-1,3)
pn=np.empty(n*3); me.polygons.foreach_get('normal',pn); pn=pn.reshape(-1,3)
pa=np.empty(n); me.polygons.foreach_get('area',pa)
r=np.hypot(pc[:,0],pc[:,1])
# planar faces facing -Z (mounting face, toward car) at r<100
m=(pn[:,2]<-0.99)&(r<110)
zs=np.round(pc[m,2],1)
u,inv=np.unique(zs,return_inverse=True); ar=np.bincount(inv,pa[m])
for k in np.argsort(-ar)[:6]: print('flat -Z at z=%.1f area=%.0f mm2'%(u[k],ar[k]))
m=(pn[:,2]>0.99)&(r<110)
zs=np.round(pc[m,2],1); u,inv=np.unique(zs,return_inverse=True); ar=np.bincount(inv,pa[m])
for k in np.argsort(-ar)[:6]: print('flat +Z at z=%.1f area=%.0f'%(u[k],ar[k]))
# radial profile: max z vs r (face profile)
rv=np.hypot(co[:,0],co[:,1])
for rr in range(0,300,15):
    s=(rv>=rr)&(rv<rr+15)
    if s.any(): print('r %3d-%3d  zmax %.1f zmin %.1f'%(rr,rr+15,co[s,2].max(),co[s,2].min()))
# spoke count: angular histogram at r=200..240 of verts with z near face
s=(rv>190)&(rv<230)&(co[:,2]>co[(rv>190)&(rv<230),2].max()-15)
th=np.degrees(np.arctan2(co[s,1],co[s,0]))%360
h,_=np.histogram(th,bins=720,range=(0,360))
f=np.abs(np.fft.rfft(h-h.mean())); print('angular fft top k:',np.argsort(-f[1:200])[:6]+1)
bpy.ops.wm.save_as_mainfile(filepath=D+'c26_norm.blend')

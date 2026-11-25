import numpy as np, sys
sys.path.insert(0,'motion')
src=open('motion/calib5.py').read().split("lb=[")[0]
exec(src)            # obs, SKX, gflow, sflow, model, C
M=np.array([[-0.6233,-0.0455,-0.7807,-1.30],[-0.7706,0.2058,0.6032,0.55],[0.1332,0.9775,-0.1633,0.36]])
R8=M[:,:3]; pos8=M[:,3]; F8=180.0
def wheelpix(R,pos,f):
    p={'R':R,'pos':pos,'f':f}; Rc,t=C.campose((0,-C.L,0),p)
    u,v,_=C.proj(C.WHEEL_C,Rc,t,f); _,vt,_=C.proj(C.WHEEL_T,Rc,t,f); _,vb,_=C.proj(C.WHEEL_B,Rc,t,f)
    return u[0],v[0],vb[0]-vt[0]
U8,V8,H8=wheelpix(R8,pos8,F8); print('rev8 wheel px',round(U8,1),round(V8,1),'h',round(H8,1))
def rotvec(w):
    th=np.linalg.norm(w)
    if th<1e-12: return np.eye(3)
    k=w/th; K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]]); return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*K@K
def mk(x):
    w=x[0:3]; R=R8@rotvec(w)          # small rotation in camera frame
    pos=pos8+np.array([x[3],x[4],x[5]])
    return {'R':R,'pos':pos,'f':x[6],'vr':x[7],'vf':x[8],'dL':x[9],'dR':x[10]}
def res(x):
    p=mk(x); m,_=model(p); out=[]
    for (tc,g,s),(pg,ps) in zip(obs,m):
        if np.all(np.isfinite(g)): out += list((pg-g)/0.6) if pg is not None else [60,60]
        if np.all(np.isfinite(s)): out += list((ps-s)/0.12)
        sx=SKX[round(tc,3)]
        if np.isfinite(sx): out += [(ps[0]-sx)/0.25]
    u,v,h=wheelpix(p['R'],p['pos'],p['f']); out += [(u-U8)/3,(v-V8)/3,(h-H8)/3]
    out += [(x[8]/np.cos(x[10])-1.2)/0.08]            # front-wheel speed from measured rim rotation (~200 deg/s)
    return np.array(out)
lb=[-0.35,-0.35,-0.35,-0.15,-0.25,-0.08,140,0.2,0.6,np.radians(15),np.radians(5)]
ub=[ 0.35, 0.35, 0.35, 0.05, 0.25, 0.10,260,2.0,2.0,np.radians(42),np.radians(42)]
best=None
for dl,dr in [(35,25),(42,10),(30,30)]:
    x0=np.array([0,0,0,0,0,0,180,0.6,1.1,np.radians(dl),np.radians(dr)])
    sol=least_squares(res,x0,bounds=(lb,ub),diff_step=1e-3,max_nfev=150)
    c=float((sol.fun**2).sum()); print('start',dl,dr,'cost',round(c,1),flush=True)
    if best is None or c<best[0]: best=(c,sol.x)
x=best[1]; np.save('motion/calib_rev8fit.npy',x); p=mk(x)
print('rot(deg)',np.round(np.degrees(x[:3]),2),'dpos',np.round(x[3:6],3),'f',round(x[6],1),'vr',round(x[7],3),'vf',round(x[8],3),'dL',round(np.degrees(x[9]),1),'dR',round(np.degrees(x[10]),1))
m,tr=model(p)
for (tc,g,s),(pg,ps) in list(zip(obs,m))[::2]:
    pg=pg*24 if pg is not None else np.array([np.nan]*2); sx=SKX[round(tc,3)]*24
    print(f"{tc:5.2f} g({g[0]*24:5.0f},{g[1]*24:5.0f})->({pg[0]:5.0f},{pg[1]:5.0f})  s({s[0]*24:6.1f},{s[1]*24:6.1f}|{sx:6.1f})->({ps[0]*24:6.1f},{ps[1]*24:6.1f})")
print('yaw P1:',round(np.degrees(tr[int(2.3*24)][2]),1),'P5:',round(np.degrees(tr[-1][2]-tr[int(5.9*24)][2]),1))
print('CAM', np.round(np.c_[p['R'],p['pos']],5).tolist())

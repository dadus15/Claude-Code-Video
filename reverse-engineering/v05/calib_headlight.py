import numpy as np, sys
sys.path.insert(0,'motion')
exec(open("motion/calib_rev8.py").read().split("\nlb=")[0])     # obs, model, wheelpix, R8, rotvec...
HL=np.array([[-0.86,0.50,0.70],[-0.83,0.47,0.66],[-0.86,0.60,0.74]])   # rear-outer corner of the RS5 headlight
DR_FIX=np.radians(25.0)
def mk2(x):
    R=R8@rotvec(x[0:3]); pos=np.array([x[3],x[4],x[5]])
    return {'R':R,'pos':pos,'f':x[6],'vr':x[7],'vf':x[8],'dL':x[9],'dR':DR_FIX}
def res2(x):
    p=mk2(x); m,_=model(p); out=[]
    for (tc,g,s),(pg,ps) in zip(obs,m):
        if np.all(np.isfinite(g)): out += list((pg-g)/0.6) if pg is not None else [60,60]
        if np.all(np.isfinite(s)): out += list((ps-s)/0.12)
        sx=SKX[round(tc,3)]
        if np.isfinite(sx): out += [(ps[0]-sx)/0.5]
    u,v,h=wheelpix(p['R'],p['pos'],p['f']); out += [(u-U8)/3,(v-V8)/3,(h-H8)/3]
    Rc,t=C.campose((0,-C.L,0),p); hu,hv,ok=C.proj(HL,Rc,t,p['f'])
    # headlight corner must sit in the top-left like the original (x 5..45, y 150..230)
    out += [max(0,hu[0]-45)/3, max(0,5-hu[0])/3, max(0,hv[0]-230)/3, max(0,150-hv[0])/3, 0 if ok[0] else 50]
    out += [(x[8]/np.cos(DR_FIX)-1.2)/0.08]
    return np.array(out)
lb=[-0.6,-0.6,-0.6,-1.40,0.60,0.20,120,0.2,0.6,np.radians(25)]
ub=[ 0.6, 0.6, 0.6,-1.02,1.00,0.45,260,2.0,2.0,np.radians(42)]
best=None
for y0 in (0.70,0.85):
    for x0 in (-1.10,-1.25):
        x=np.array([0,0,0,x0,y0,0.30,163.6,0.43,1.2,np.radians(40)])
        sol=least_squares(res2,x,bounds=(lb,ub),diff_step=1e-3,max_nfev=120)
        c=float((sol.fun**2).sum()); print('start',x0,y0,'cost',round(c,1),flush=True)
        if best is None or c<best[0]: best=(c,sol.x)
x=best[1]; np.save('motion/calib_headlight.npy',x); p=mk2(x)
print('pos',np.round(x[3:6],3),'rot',np.round(np.degrees(x[:3]),1),'f',round(x[6],1),'vr',round(x[7],3),'vf',round(x[8],3),'dL',round(np.degrees(x[9]),1),'dR 25')
Rc,t=C.campose((0,-C.L,0),p); print('headlight px',np.round(C.proj(HL,Rc,t,p['f'])[:2],0).T.tolist(),'wheel',np.round(wheelpix(p['R'],p['pos'],p['f']),1))
m,tr=model(p)
for (tc,g,s),(pg,ps) in list(zip(obs,m))[::3]:
    pg=pg*24 if pg is not None else np.array([np.nan]*2); sx=SKX[round(tc,3)]*24
    print(f"{tc:5.2f} g({g[0]*24:5.0f},{g[1]*24:5.0f})->({pg[0]:5.0f},{pg[1]:5.0f})  s({s[0]*24:6.1f},{s[1]*24:6.1f}|{sx:6.1f})->({ps[0]*24:6.1f},{ps[1]*24:6.1f})")
print('yaw P5',round(np.degrees(tr[-1][2]-tr[int(5.9*24)][2]),1))
print('CAM',np.round(np.c_[p['R'],p['pos']],5).tolist())

# pixel-uniform model: region pixels are back-projected onto the ground plane (z=0) / sky at infinity
import numpy as np, sys
sys.path.insert(0,'motion'); import calib as C
from scipy.optimize import least_squares
exec(open('motion/calib3.py').read().split('def residuals')[0])
HF=np.load('motion/horizon_flow.npy')
SKX={}
for tc,g,sk in obs:
    m=(HF[:,0]>=tc-0.125)&(HF[:,0]<tc+0.125)
    SKX[round(tc,3)]=(np.nanmedian(HF[m,3])+1.0)/24 if tc>5.6 and m.sum() else np.nan
def pix(reg,n=8):
    x0,y0,x1,y1=reg; u,v=np.meshgrid(np.linspace(x0+3,x1-3,n),np.linspace(y0+3,y1-3,n*2)); return u.ravel(),v.ravel()
GU,GV=pix(C.GREG); SU,SV=pix(C.SREG)
def rays(u,v,Rc,f):
    d=np.c_[(u-180)/f,-(v-320)/f,-np.ones_like(u)]; return d@Rc.T
def gflow(A,B,f):
    Rc,t=A; d=rays(GU,GV,Rc,f); ok=d[:,2]<-1e-3
    if ok.sum()<len(GU)*0.9: return None
    s=-t[2]/d[ok,2]; P=t+d[ok]*s[:,None]
    ub,vb,okb=C.proj(P,*B,f); return np.median(np.c_[ub-GU[ok],vb-GV[ok]],0)
def sflow(A,B,f):
    Rc,t=A; d=rays(SU,SV,Rc,f); P=t+d*1e5; ub,vb,_=C.proj(P,*B,f); return np.median(np.c_[ub-SU,vb-SV],0)
def model(p):
    tr=C.traj(p); out=[]
    for tc,g,s in obs:
        i=int(tc*24); A_=C.campose(tr[i],p); B_=C.campose(tr[i+1],p); out.append((gflow(A_,B_,p['f']),sflow(A_,B_,p['f'])))
    return out,tr
def residuals(x):
    p=C.unpack(x); m,_=model(p); out=[]
    for (tc,g,s),(pg,ps) in zip(obs,m):
        if np.all(np.isfinite(g)): out += list((pg-g)/0.6) if pg is not None else [60,60]
        if np.all(np.isfinite(s)): out += list((ps-s)/0.12)
        sx=SKX[round(tc,3)]
        if np.isfinite(sx): out += [(ps[0]-sx)/0.25]
    Rc,t=C.campose((0,-C.L,0),p)
    u,v,_=C.proj(C.WHEEL_C,Rc,t,p['f']); out += [(u[0]-216)/4,(v[0]-358)/4]
    _,vt,_=C.proj(C.WHEEL_T,Rc,t,p['f']); _,vb,_=C.proj(C.WHEEL_B,Rc,t,p['f']); out += [((vb[0]-vt[0])-0.44*640)/6]
    out += [(p['vf']-1.15)/0.10]
    return np.array(out)
lb=[-1.9,0.2,0.12, np.radians(140), np.radians(-5), np.radians(-30), 70, 0.3, 0.8, np.radians(10), np.radians(10)]
ub=[-1.03,1.3,0.70, np.radians(240), np.radians(45), np.radians(30), 400, 2.0, 1.5, np.radians(42), np.radians(42)]
starts=[np.load('motion/calib_x6_1.08.npy'),np.load('motion/calib_x6_1.03.npy'),
        [-1.0,0.6,0.33,np.radians(205),np.radians(10),np.radians(-18),280,0.9,1.1,np.radians(33),np.radians(33)],
        [-1.1,0.5,0.30,np.radians(200),np.radians(5),np.radians(-10),200,1.0,1.15,np.radians(30),np.radians(30)],
        [-1.3,0.55,0.36,np.radians(190),np.radians(15),np.radians(-8),180,1.0,1.15,np.radians(35),np.radians(35)]]
best=None
for k,x0 in enumerate(starts):
    x0=np.clip(np.array(x0,float),np.array(lb)+1e-6,np.array(ub)-1e-6)
    sol=least_squares(residuals,x0,bounds=(lb,ub),diff_step=1e-3,max_nfev=150)
    c=float((sol.fun**2).sum()); print('start',k,'cost',round(c,1),flush=True)
    if best is None or c<best[0]: best=(c,sol.x)
x=best[1]; np.save('motion/calib_x7.npy',x); p=C.unpack(x); print('BEST',round(best[0],1))
for kname in C.NAMES:
    v=p[kname]; print(f"  {kname:6} = {np.degrees(v):8.2f} deg" if kname in ('yaw','pitch','roll','dL','dR') else f"  {kname:6} = {v:8.3f}")
m,tr=model(p)
for (tc,g,s),(pg,ps) in list(zip(obs,m))[::2]:
    pg=pg*24 if pg is not None else np.array([np.nan]*2)
    sx=SKX[round(tc,3)]*24; print(f"skx {sx:6.1f} ",end=''); print(f"{tc:5.2f} g({g[0]*24:5.0f},{g[1]*24:5.0f})->({pg[0]:5.0f},{pg[1]:5.0f})  s({s[0]*24:6.1f},{s[1]*24:6.1f})->({ps[0]*24:6.1f},{ps[1]*24:6.1f})")
print('yaw P1:',round(np.degrees(tr[int(2.3*24)][2]),1),'P5:',round(np.degrees(tr[-1][2]-tr[int(5.9*24)][2]),1))

import numpy as np, sys
sys.path.insert(0,'motion'); import calib as C
from scipy.optimize import least_squares
R=np.load('motion/flows_unique.npy')
drift=np.nanmedian(R[(R[:,0]>2.5)&(R[:,0]<5.5),3:5],0)
obs=[]
for t0 in np.arange(0,12.5,0.25):
    m=(R[:,0]>=t0)&(R[:,0]<t0+0.25)
    if m.sum()==0: continue
    g=np.nanmedian(R[m,1:3],0)/24; s=(np.nanmedian(R[m,3:5],0)-drift)/24
    if t0>5.6: s=np.array([np.nan,np.nan])      # lamp posts contaminate the sky window while driving
    obs.append((t0+0.125,g,s))
C.obs=obs
r=np.geomspace(0.3,120,140); a=np.linspace(-np.pi,np.pi,240); RR,AA=np.meshgrid(r,a)
C.G=np.c_[(RR*np.cos(AA)).ravel()-1.0,(RR*np.sin(AA)).ravel()+0.4,np.zeros(RR.size)]
# data-driven speed shapes
def shape_rev(t): return np.where(t<0.9,1.0,np.where(t<2.25,(1-np.clip((t-0.9)/1.35,0,1))**1.5,0.0))
def shape_fwd(t):
    k=np.clip((t-5.6)/2.2,0,1); base=k*k*(3-2*k); return np.where(t<5.6,0.0,base*(1+0.25*np.clip((t-7.8)/4.5,0,1)))
C.shape_rev=shape_rev; C.shape_fwd=shape_fwd
def residuals(x):
    p=C.unpack(x); tr=C.traj(p); out=[]
    for tc,g,s in obs:
        i=int(tc*24); A_=C.campose(tr[i],p); B_=C.campose(tr[i+1],p)
        pg=C.regflow(C.G,A_,B_,p['f'],C.GREG)
        if np.all(np.isfinite(g)): out += list(((pg-g)/0.6) if np.all(np.isfinite(pg)) else [80,80])
        if np.all(np.isfinite(s)):
            ps=C.regflow(C.SK,A_,B_,p['f'],C.SREG); out += list(((ps-s)/0.12) if np.all(np.isfinite(ps)) else [80,80])
    Rc,t=C.campose((0,-C.L,0),p)
    u,v,_=C.proj(C.WHEEL_C,Rc,t,p['f']); out += [(u[0]-216)/4,(v[0]-358)/4]
    _,vt,_=C.proj(C.WHEEL_T,Rc,t,p['f']); _,vb,_=C.proj(C.WHEEL_B,Rc,t,p['f']); out += [((vb[0]-vt[0])-0.44*640)/6]
    out += [(p['vf']-1.15)/0.10]
    return np.array(out)
lb=[-1.9,0.2,0.12, np.radians(140), np.radians(-5), np.radians(-30), 70, 0.3, 0.8, np.radians(10), np.radians(10)]
ub=[-0.96,1.3,0.70, np.radians(240), np.radians(45), np.radians(30), 400, 2.0, 1.5, np.radians(42), np.radians(42)]
best=None
starts=[[-1.0,0.6,0.33,np.radians(200),np.radians(11),np.radians(-17),266,0.7,1.1,np.radians(20),np.radians(20)],
        [-1.0,0.45,0.30,np.radians(200),np.radians(30),np.radians(-17),121,0.6,1.1,np.radians(30),np.radians(30)],
        [-1.3,0.55,0.36,np.radians(185),np.radians(15),np.radians(-8),180,0.9,1.15,np.radians(35),np.radians(35)],
        [-1.1,0.8,0.40,np.radians(215),np.radians(20),np.radians(-20),150,0.8,1.15,np.radians(25),np.radians(25)]]
for k,x0 in enumerate(starts):
    sol=least_squares(residuals,np.array(x0),bounds=(lb,ub),diff_step=1e-3,max_nfev=120)
    c=float((sol.fun**2).sum()); print('start',k,'cost',round(c,1),flush=True)
    if best is None or c<best[0]: best=(c,sol.x)
x=best[1]; np.save('motion/calib_x5.npy',x); p=C.unpack(x); print('BEST',round(best[0],1))
for kname in C.NAMES:
    v=p[kname]; print(f"  {kname:6} = {np.degrees(v):8.2f} deg" if kname in ('yaw','pitch','roll','dL','dR') else f"  {kname:6} = {v:8.3f}")
tr=C.traj(p)
for tc,g,s in obs[::2]:
    i=int(tc*24); A_=C.campose(tr[i],p); B_=C.campose(tr[i+1],p)
    pg=C.regflow(C.G,A_,B_,p['f'],C.GREG)*24; ps=C.regflow(C.SK,A_,B_,p['f'],C.SREG)*24
    print(f"{tc:5.2f} ({g[0]*24:6.0f},{g[1]*24:6.0f})->({pg[0]:6.0f},{pg[1]:6.0f})   sky ({s[0]*24:5.1f},{s[1]*24:5.1f})->({ps[0]:5.1f},{ps[1]:5.1f})")
print('yaw P1:',round(np.degrees(tr[int(2.3*24)][2]),1),'P5:',round(np.degrees(tr[-1][2]-tr[int(5.9*24)][2]),1))

import numpy as np
from scipy.optimize import least_squares
res=np.load('motion/res.npy',allow_pickle=True).item(); O=res['orig']
gr=np.load('motion/ground_right.npy')
FPS=24; N=len(gr)
# ---------- observations (per 0.25 s window, px/frame @360x640)
def win(arr,a,b): 
    x=arr[a:b]; x=x[np.all(np.isfinite(x),1)]; return np.median(x,0) if len(x) else np.array([np.nan,np.nan])
drift=np.nanmedian(O['sky'][int(2.5*FPS):int(5.8*FPS)],0)          # cloud drift while the car stands
obs=[]
for t0 in np.arange(0,12.75,0.25):
    a,b=int(t0*FPS),int((t0+0.25)*FPS)
    obs.append((t0+0.125, win(gr,a,b), win(O['sky'],a,b)-drift))
# speed shape from ground-strip magnitude (normalised per phase)
mag=np.array([np.linalg.norm(g) if np.all(np.isfinite(g)) else 0 for _,g,_ in obs])
tt=np.array([o[0] for o in obs])
def shape_rev(t):   # 1.0 until 0.6 s, eases to 0 at 2.25 s (from data)
    return np.where(t<0.6,1.0,np.where(t<2.25,(1-np.clip((t-0.6)/1.65,0,1))**1.6,0.0))
def shape_fwd(t):   # 0 until 5.5 s, smooth rise to 1 at 7.5 s, then plateau
    k=np.clip((t-5.5)/2.0,0,1); return np.where(t<5.5,0.0,k*k*(3-2*k))
L=2.77
def delta(t,dL,dR):
    k=np.clip((t-3.1)/2.0,0,1); k=k*k*(3-2*k)
    return np.where(t<3.1,dL,np.where(t<5.1,dL+(-dR-dL)*k,-dR))
def traj(p):
    vr,vf,dL,dR=p['vr'],p['vf'],p['dL'],p['dR']
    xr,yr,psi=0.0,-L,0.0; out=[]
    for i in range(N+1):
        t=i/FPS; out.append((xr,yr,psi))
        v=-vr*shape_rev(t)+vf*shape_fwd(t); d=v/FPS; dl=float(delta(t,dL,dR))
        xr+=-np.sin(psi)*d; yr+=np.cos(psi)*d; psi+=d*np.tan(dl)/L
    return out
def rot(yaw,pitch,roll):
    # camera looks along local -Z; build from yaw (about Z), pitch (about X), roll (about view axis)
    cy,sy,cp,sp,cr,sr=np.cos(yaw),np.sin(yaw),np.cos(pitch),np.sin(pitch),np.cos(roll),np.sin(roll)
    fwd=np.array([-sy*cp, cy*cp, sp])          # yaw=0 -> looking +Y ; yaw=pi -> looking -Y (rearward)
    right0=np.cross(fwd,[0,0,1]); right0/=np.linalg.norm(right0); up0=np.cross(right0,fwd)
    right=cr*right0+sr*up0; up=np.cross(right,fwd)
    return np.c_[right,up,-fwd]                 # columns = camera X,Y,Z in car frame
def campose(state,cp):
    xr,yr,psi=state; xf=xr-np.sin(psi)*L; yf=yr+np.cos(psi)*L
    c,s=np.cos(psi),np.sin(psi); Rz=np.array([[c,-s,0],[s,c,0],[0,0,1]])
    Rc=Rz@cp['R']; t=np.array([xf,yf,0])+Rz@cp['pos']; return Rc,t
def proj(P,Rc,t,f):
    c=(P-t)@Rc; z=-c[:,2]; ok=z>0.05; z=np.where(ok,z,1)
    return 180+f*c[:,0]/z, 320-f*c[:,1]/z, ok
gx,gy=np.meshgrid(np.linspace(-12,6,90),np.linspace(-14,8,110)); G=np.c_[gx.ravel(),gy.ravel(),np.zeros(gx.size)]
ang=np.linspace(-np.pi,np.pi,360); SK=np.vstack([np.c_[np.cos(e)*np.cos(ang),np.cos(e)*np.sin(ang),np.sin(e)*np.ones_like(ang)]*1e4 for e in np.radians(np.arange(5,80,5))])
GREG=(312,400,360,560); SREG=(200,50,360,200)
def regflow(P,A,B,f,reg,static_world=True):
    ua,va,oa=proj(P,*A,f); ub,vb,ob=proj(P,*B,f)
    x0,y0,x1,y1=reg; m=oa&ob&(ua>x0)&(ua<x1)&(va>y0)&(va<y1)
    return np.median(np.c_[ub-ua,vb-va][m],0) if m.sum()>4 else np.array([np.nan,np.nan])
NAMES=['px','py','pz','yaw','pitch','roll','f','vr','vf','dL','dR']
def unpack(x):
    p=dict(zip(NAMES,x)); p['R']=rot(p['yaw'],p['pitch'],p['roll']); p['pos']=np.array([p['px'],p['py'],p['pz']]); return p
WHEEL_C=np.array([[-0.80,0.0,0.349]]); WHEEL_T=np.array([[-0.80,0.0,0.698]]); WHEEL_B=np.array([[-0.80,0.0,0.0]])
def residuals(x, verbose=False):
    p=unpack(x); tr=traj(p); r=[]
    for tc,g,s in obs:
        i=int(tc*FPS); A=campose(tr[i],p); B=campose(tr[i+1],p)
        pg=regflow(G,A,B,p['f'],GREG); ps=regflow(SK,A,B,p['f'],SREG)
        if np.all(np.isfinite(g)): r += list(((pg-g) if np.all(np.isfinite(pg)) else np.array([5,5]))/2.0)
        if np.all(np.isfinite(s)) and (tc<2.3 or tc>6.5): r += list(((ps-s) if np.all(np.isfinite(ps)) else np.array([3,3]))/0.6)
    # framing constraints (car at rest, frame 0 geometry identical every frame because camera is rigid)
    Rc,t=campose((0,-L,0),p)
    u,v,_=proj(WHEEL_C,Rc,t,p['f']); r += [(u[0]-216)/3, (v[0]-358)/3]
    _,vt,_=proj(WHEEL_T,Rc,t,p['f']); _,vb,_=proj(WHEEL_B,Rc,t,p['f']); r += [((vb[0]-vt[0])-0.44*640)/4]
    r += [(p['vf']-1.15)/0.08]     # wheel-rotation speed anchor
    return np.array(r)
x0=np.array([-1.30,0.55,0.36, np.radians(140), np.radians(10), np.radians(8), 180, 1.0, 1.15, np.radians(30), np.radians(30)])
lb=[-2.0,0.2,0.12, np.radians(100), np.radians(-10), np.radians(-25), 120, 0.3, 0.7, np.radians(5), np.radians(5)]
ub=[-1.0,1.2,0.70, np.radians(200), np.radians(40),  np.radians(25),  420, 2.0, 1.6, np.radians(38), np.radians(38)]
if __name__=='__main__':
    r0=residuals(x0); print('init cost',float((r0**2).sum()))
    sol=least_squares(residuals,x0,bounds=(lb,ub),diff_step=1e-3,max_nfev=300,verbose=0)
    p=unpack(sol.x); print('final cost',float((sol.fun**2).sum()))
    for k in NAMES:
        v=p[k]; print(f"  {k:6} = {np.degrees(v):8.2f} deg" if k in ('yaw','pitch','roll','dL','dR') else f"  {k:6} = {v:8.3f}")
    np.save('motion/calib_x.npy',sol.x)

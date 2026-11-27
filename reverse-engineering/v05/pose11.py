import cv2,numpy as np,math
from scipy.optimize import least_squares
a=cv2.imread('../assets_rs5/AUDI-RS5-8W-TURISMO-FORGED-V05-BRUSHED-BLACK_11.jpg'); g=cv2.GaussianBlur(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY).astype(float),(0,0),1.5)
lip=[]
for y in range(40,1520,20):
    row=g[y,2150:2500]; d=np.diff(row); idx=[i for i in range(len(d)-16) if d[i]<-15 and row[i+3:i+16].mean()<70]
    if idx: lip.append((2150+idx[-1]+0.5,y))
lip=np.array(lip,float)
nuts=np.array([(1304,768),(1507,838),(1501,1129),(1304,1223),(1141,996)],float)   # image order around the centre (clockwise in image)
W,H=2560,1536; R=0.2805; PCD=0.056
def proj(P,rv,tv,f):
    p,_=cv2.projectPoints(P,rv,tv,np.array([[f,0,W/2],[0,f,H/2],[0,0,1]]),None); return p.reshape(-1,2)
TH=np.linspace(0,2*np.pi,1440,endpoint=False)
def res(x,ret=False):
    rv=x[0:3]; tv=x[3:6]; f=x[6]; zn=x[7]; phi=x[8]
    Pn=np.c_[PCD*np.cos(phi-np.radians(72)*np.arange(5)),PCD*np.sin(phi-np.radians(72)*np.arange(5)),np.full(5,zn)]
    rn=(proj(Pn,rv,tv,f)-nuts).ravel()/3.0
    C=proj(np.c_[R*np.cos(TH),R*np.sin(TH),np.zeros_like(TH)],rv,tv,f)
    dd=np.sqrt(((lip[:,None,:]-C[None,:,:])**2).sum(-1)).min(1)
    rl=np.minimum(dd,25)/3.0          # robust (outliers capped)
    return (rn,rl) if ret else np.r_[rn,rl]
best=None
for f0 in (1800,2600,3600):
    for sgn in (1,-1):
        for rx in (-0.6,0.0,0.6):
            for ry in (-0.8,0.0,0.8):
                x0=np.array([rx,ry,0.0, 0.03,0.0,0.9*f0/2600, f0,-0.05, 0.3*sgn])
                try: s=least_squares(res,x0,loss='soft_l1',f_scale=2.0,max_nfev=400)
                except Exception: continue
                c=float((s.fun**2).sum())
                if best is None or c<best[0]: best=(c,s.x)
c,x=best; rn,rl=res(x,True)
print('cost',round(c,1),'f',round(x[6],1),'z_nut',round(x[7],4),'phi',round(np.degrees(x[8]),1))
print('nut rms px',round(float(np.sqrt((rn*3)**2).mean()),2),'lip median px',round(float(np.median(rl*3)),2))
R_,_=cv2.Rodrigues(x[0:3]); print('axis tilt deg',round(float(np.degrees(np.arccos(abs(R_[2,2])))),1),'dist m',round(float(np.linalg.norm(x[3:6])),3))
np.save('pose11.npy',x)

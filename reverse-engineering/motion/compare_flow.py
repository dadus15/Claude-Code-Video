# same LK + forward-backward measurement on original (unique frames) and on the guide; per-phase table
import cv2, numpy as np, sys
def load(p):
    v=cv2.VideoCapture(p); fr=[]
    while True:
        ok,f=v.read()
        if not ok: break
        fr.append(cv2.cvtColor(cv2.resize(f,(360,640)),cv2.COLOR_BGR2GRAY))
    return fr
REG={'ground':(312,400,360,560),'sky':(200,50,360,200)}
def lk(fr,a,b,reg):
    x0,y0,x1,y1=reg; m=np.zeros_like(fr[a]); m[y0:y1,x0:x1]=255
    p=cv2.goodFeaturesToTrack(fr[a],120,0.005,3,mask=m)
    if p is None: return None
    q,st,_=cv2.calcOpticalFlowPyrLK(fr[a],fr[b],p,None,winSize=(15,15),maxLevel=3)
    r,st2,_=cv2.calcOpticalFlowPyrLK(fr[b],fr[a],q,None,winSize=(15,15),maxLevel=3)
    ok=(st[:,0]==1)&(st2[:,0]==1)&(np.linalg.norm((r-p).reshape(-1,2),axis=1)<0.5)
    d=(q-p).reshape(-1,2)[ok]; return np.median(d,0)/(b-a) if len(d)>6 else None
def series(fr,unique):
    idx=[0]+[i for i in range(1,len(fr)) if (not unique) or np.abs(fr[i].astype(int)-fr[i-1]).mean()>0.8]
    out=[]
    for a,b in zip(idx[:-1],idx[1:]):
        row=[a/24]
        for k,r in REG.items():
            f=lk(fr,a,b,r); row+=list(f*24) if f is not None else [np.nan,np.nan]
        out.append(row)
    return np.array(out)
O=series(load(sys.argv[1]),True); G=series(load(sys.argv[2]),False)
ph=[('P1 cofanie 0-1',0,1),('P1 hamowanie 1-2.25',1,2.25),('P2-P4 postoj 2.4-5.5',2.4,5.5),('P5 ruszanie 5.9-7.8',5.9,7.8),('P5 jazda 7.8-12.9',7.8,12.9)]
print(f"{'faza':24} {'ORYG asfalt':>16} {'PROW asfalt':>16} {'ORYG niebo':>14} {'PROW niebo':>14}")
for n,a,b in ph:
    mo=(O[:,0]>=a)&(O[:,0]<b); mg=(G[:,0]>=a)&(G[:,0]<b)
    o=np.nanmedian(O[mo,1:],0); g=np.nanmedian(G[mg,1:],0)
    print(f"{n:24} ({o[0]:6.0f},{o[1]:6.0f})  ({g[0]:6.0f},{g[1]:6.0f})  ({o[2]:5.1f},{o[3]:5.1f})  ({g[2]:5.1f},{g[3]:5.1f})")
np.save('motion/compare_O.npy',O); np.save('motion/compare_G.npy',G)

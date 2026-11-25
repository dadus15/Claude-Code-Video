import cv2, numpy as np, sys, json
def load(p, size=(360,640)):
    c=cv2.VideoCapture(p); fr=[]
    while True:
        ok,f=c.read()
        if not ok: break
        fr.append(cv2.cvtColor(cv2.resize(f,size),cv2.COLOR_BGR2GRAY))
    return fr
REG={'sky':(200,50,360,200),'horizon':(230,230,360,330),'ground':(150,470,360,560)}
def track(fr):
    out={k:[] for k in REG}
    for a,b in zip(fr[:-1],fr[1:]):
        for k,(x0,y0,x1,y1) in REG.items():
            m=np.zeros_like(a); m[y0:y1,x0:x1]=255
            p=cv2.goodFeaturesToTrack(a,80,0.01,4,mask=m)
            if p is None: out[k].append((0,0)); continue
            q,st,_=cv2.calcOpticalFlowPyrLK(a,b,p,None,winSize=(21,21),maxLevel=3)
            d=(q-p)[st[:,0]==1].reshape(-1,2)
            out[k].append(tuple(np.median(d,0)) if len(d)>5 else (0,0))
    return {k:np.array(v) for k,v in out.items()}
res={}
for name,p in (('orig',sys.argv[1]),('guide',sys.argv[2])):
    res[name]=track(load(p))
np.save('motion/res.npy',res,allow_pickle=True)
phases=[('P0',0,0.4),('P1 cofanie',0.4,2.4),('P2',2.4,3.1),('P3 skret',3.1,5.1),('P4',5.1,5.9),('P5a rozp.',5.9,8.5),('P5b jazda',8.5,12.9)]
print(f"{'faza':12} {'reg':8} {'ORIG dx/s':>9} {'dy/s':>7} {'GUIDE dx/s':>10} {'dy/s':>7}")
for ph,t0,t1 in phases:
    a,b=int(t0*24),int(t1*24)
    for k in REG:
        o=res['orig'][k][a:b].mean(0)*24; g=res['guide'][k][a:b].mean(0)*24
        print(f"{ph:12} {k:8} {o[0]:9.1f} {o[1]:7.1f} {g[0]:10.1f} {g[1]:7.1f}")

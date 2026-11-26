import cv2,numpy as np,math,json
from scipy.optimize import minimize
r=cv2.imread('v05_rect_c.png'); g=cv2.GaussianBlur(cv2.cvtColor(r,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),1.6)
gx=cv2.Sobel(g,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,ksize=3); G=np.hypot(gx,gy)+1e-3
SPOKE=[(0.02,0.16),(-0.035,0.50),(0.12,0.87),(0.48,0.80),(0.44,0.735),(0.29,0.625),(0.18,0.15)]
H0=[[(0.035,0.47),(0.235,0.605),(0.055,0.27)],[(0.10,0.68),(0.16,0.79),(0.33,0.79),(0.27,0.70)]]
def shrink(p,k):
    cx=sum(x for x,_ in p)/len(p); cy=sum(y for _,y in p)/len(p); return [(cx+(x-cx)*k,cy+(y-cy)*k) for x,y in p]
HOLES=[shrink(H0[0],0.70),shrink(H0[1],0.76)]
polys0=[SPOKE]+HOLES; sizes=[len(p) for p in polys0]
x0=np.array([c for p in polys0 for v in p for c in v])
def unpack(x):
    out=[];i=0
    for n in sizes: out.append(x[i:i+2*n].reshape(n,2)); i+=2*n
    return out
def bil(img,xs,ys):
    return cv2.remap(img,xs.astype(np.float32).reshape(1,-1),ys.astype(np.float32).reshape(1,-1),cv2.INTER_LINEAR).ravel()
def edge_score(P):
    s=0;n=0
    for k in range(5):
        a=-math.radians(72*k); c,si=math.cos(a),math.sin(a)
        Q=np.c_[P[:,0]*c-P[:,1]*si,P[:,0]*si+P[:,1]*c]
        for i in range(len(Q)):
            A,B=Q[i],Q[(i+1)%len(Q)]; mid=(A+B)/2; rm=np.hypot(*mid)
            if rm>0.80 or rm<0.27: continue           # edge merges into ring/hub: no image edge there
            t=np.linspace(0.08,0.92,22); pts=A+np.outer(t,B-A)
            xs=600+pts[:,0]*500; ys=600-pts[:,1]*500
            d=B-A; nrm=np.array([-d[1],d[0]])/(np.hypot(*d)+1e-9); nimg=np.array([nrm[0],-nrm[1]])
            gg=bil(G,xs,ys); gxx=bil(gx,xs,ys); gyy=bil(gy,xs,ys)
            s+=np.mean(np.abs(gxx*nimg[0]+gyy*nimg[1])); n+=1
    return s/max(n,1)
def obj(x):
    Ps=unpack(x); sc=sum(edge_score(P) for P in Ps)
    reg=np.sum((x-x0)**2)*400       # keep near the reviewed topology
    return -sc+reg
print('start score',-obj(x0))
res=minimize(obj,x0,method='Powell',options={'maxiter':6000,'xtol':1e-4,'ftol':1e-5})
x=res.x; print('end score',-obj(x),'max move',np.round(np.abs(x-x0).max(),4))
Ps=unpack(x); json.dump([P.round(4).tolist() for P in Ps],open('v05_fit_polys.json','w'))
ov=r.copy()
for k in range(5):
    a=-math.radians(72*k); c,si=math.cos(a),math.sin(a)
    for P0,P1 in zip(unpack(x0),Ps):
        for P,col in ((P0,(0,0,255)),(P1,(0,255,0))):
            Q=np.c_[P[:,0]*c-P[:,1]*si,P[:,0]*si+P[:,1]*c]; pts=np.array([[600+q[0]*500,600-q[1]*500] for q in Q],np.int32)
            cv2.polylines(ov,[pts],True,col,2)
cv2.imwrite('../scratchpad/fit_spoke.jpg',cv2.resize(ov[100:1100,100:1100],(800,800)))

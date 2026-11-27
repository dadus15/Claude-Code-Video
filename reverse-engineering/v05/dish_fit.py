import cv2,numpy as np,json,math
from scipy.optimize import minimize
x=np.load('pose11.npy'); W,H=2560,1536; K=np.array([[x[6],0,W/2],[0,x[6],H/2],[0,0,1]])
p=cv2.imread('../assets_rs5/AUDI-RS5-8W-TURISMO-FORGED-V05-BRUSHED-BLACK_11.jpg',0)
E=cv2.Canny(cv2.GaussianBlur(p,(0,0),1.5),40,110); DT=cv2.distanceTransform(255-E,cv2.DIST_L2,3)
R=0.2805; TOP=-0.005
P=[np.array(q) for q in json.load(open('v05_fit_polys2.json'))]
def dense(poly,step=0.004):
    out=[]
    for i in range(len(poly)):
        a,b=poly[i],poly[(i+1)%len(poly)]; n=max(2,int(np.linalg.norm(b-a)/step))
        for t in np.linspace(0,1,n,endpoint=False): out.append(a+(b-a)*t)
    return np.array(out)
base=[dense(q) for q in P]
def model_pts(dish,expo,delta):
    pts=[]
    for k in range(5):
        a=math.radians(72*k)
        for q in base:
            xy=q@np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]])
            r=np.hypot(xy[:,0],xy[:,1]); keep=(r>0.27)&(r<0.79)
            L=np.c_[xy[:,1]*R,-xy[:,0]*R][keep]; rr=r[keep]
            s=np.clip((0.80-rr)/(0.80-0.25),0,1); s=s**expo
            z=TOP-dish*s
            c,si=math.cos(delta),math.sin(delta)
            pts.append(np.c_[L[:,0]*c-L[:,1]*si,L[:,0]*si+L[:,1]*c,z])
    return np.vstack(pts)
def score(dish,expo,delta):
    Q=model_pts(dish,expo,delta); pr,_=cv2.projectPoints(Q,x[0:3],x[3:6],K,None); pr=pr.reshape(-1,2)
    ok=(pr[:,0]>2)&(pr[:,0]<W-3)&(pr[:,1]>2)&(pr[:,1]<H-3)
    if ok.sum()<200: return 99
    d=DT[pr[ok,1].astype(int),pr[ok,0].astype(int)]
    return float(np.mean(np.minimum(d,30)))
phi=x[8]; base_delta=math.radians(35.98)-phi
best=None
for k in range(5):
    for dish in np.arange(0.02,0.16,0.01):
        for expo in (0.6,1.0,1.6):
            for dd in np.radians(np.arange(-8,8.1,2)):
                d0=base_delta+math.radians(72*k)+dd
                s=score(dish,expo,d0)
                if best is None or s<best[0]: best=(s,dish,expo,d0)
print('grid best',best[0],'dish',best[1],'expo',best[2],'delta deg',round(math.degrees(best[3])%360,1))
res=minimize(lambda v: score(*v),[best[1],best[2],best[3]],method='Nelder-Mead',options={'xatol':1e-4,'fatol':1e-3,'maxiter':400})
dish,expo,delta=res.x; print('refined score',round(res.fun,3),'dish m',round(dish,4),'expo',round(expo,3),'delta deg',round(math.degrees(delta)%360,2))
for dtest in (0.045,dish):
    print(' score at dish',round(dtest,3),':',round(score(dtest,expo,delta),3))
json.dump({'dish':dish,'expo':expo,'delta':delta},open('dish_fit.json','w'))
Q=model_pts(dish,expo,delta); pr,_=cv2.projectPoints(Q,x[0:3],x[3:6],K,None)
vis=cv2.cvtColor(p,cv2.COLOR_GRAY2BGR)
for u,v in pr.reshape(-1,2).astype(int):
    if 0<=u<W and 0<=v<H: cv2.circle(vis,(u,v),3,(0,0,255),-1)
cv2.imwrite('../scratchpad/dish_fit.jpg',cv2.resize(vis,(1280,768)))

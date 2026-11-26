import cv2,numpy as np,math,json
from scipy.optimize import minimize
exec(open('fit_spoke.py').read().split("SPOKE=")[0])
P1=[np.array(p) for p in json.load(open('v05_fit_polys.json'))]
def subdiv(P):
    out=[]
    for i in range(len(P)): out.append(P[i]); out.append((P[i]+P[(i+1)%len(P)])/2)
    return np.array(out)
polys0=[subdiv(p) for p in P1]; sizes=[len(p) for p in polys0]
x0=np.concatenate([p.ravel() for p in polys0])
def unpack(x):
    out=[];i=0
    for n in sizes: out.append(x[i:i+2*n].reshape(n,2)); i+=2*n
    return out
exec("def bil"+open('fit_spoke.py').read().split("def bil")[1].split("def obj")[0])
def obj(x):
    Ps=unpack(x); sc=sum(edge_score(P) for P in Ps)
    smooth=sum(np.sum((np.roll(P,1,0)-2*P+np.roll(P,-1,0))**2) for P in Ps)*30
    anchor=np.sum((x-x0)**2)*60
    return -sc+smooth+anchor
print('start',-obj(x0))
res=minimize(obj,x0,method='Powell',options={'maxiter':12000,'xtol':1e-4,'ftol':1e-6})
x=res.x; Ps=unpack(x); print('end',-obj(x),'edge score',sum(edge_score(P) for P in Ps))
json.dump([P.round(4).tolist() for P in Ps],open('v05_fit_polys2.json','w'))
ov=r.copy()
for k in range(5):
    a=-math.radians(72*k); c,si=math.cos(a),math.sin(a)
    for P in Ps:
        Q=np.c_[P[:,0]*c-P[:,1]*si,P[:,0]*si+P[:,1]*c]; pts=np.array([[600+q[0]*500,600-q[1]*500] for q in Q],np.int32)
        cv2.polylines(ov,[pts],True,(0,255,0),2)
cv2.imwrite('../scratchpad/fit_spoke2.jpg',cv2.resize(ov[100:1100,100:1100],(800,800)))

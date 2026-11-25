import numpy as np
SPOKE=[(0.02,0.16),(-0.03,0.50),(0.12,0.86),(0.47,0.80),(0.43,0.74),(0.28,0.63),(0.17,0.15)]
HOLES=[[(0.035,0.47),(0.235,0.605),(0.055,0.27)],[(0.10,0.68),(0.16,0.79),(0.33,0.79),(0.27,0.70)]]
RING_IN,RING_OUT,HUB_R=0.80,1.0,0.25
NSLOT=34; SLOT_R=0.895; SLOT_SLANT=np.radians(40); SLOT_PHASE=np.radians(5.3+2.9)
SLOT=[(-0.045,-0.013),(0.045,-0.023),(0.045,0.013),(-0.045,0.023)]
def rot(p,a): c,s=np.cos(a),np.sin(a); return [(x*c-y*s,x*s+y*c) for x,y in p]
def slots():
    out=[]
    for i in range(NSLOT):
        loc=[(x,y+SLOT_R) for x,y in rot(SLOT,SLOT_SLANT)]
        out.append(rot(loc,2*np.pi*i/NSLOT+SLOT_PHASE))
    return out

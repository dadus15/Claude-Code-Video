import sys, numpy as np
from PIL import Image, ImageFilter
from matplotlib.path import Path
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.float32)/255.
hsv = np.asarray(im.convert('HSV')).astype(np.float32)
H = hsv[...,0]*360/255; S = hsv[...,1]/255; V = hsv[...,2]/255
h,w = V.shape; yy,xx = np.mgrid[0:h,0:w]
screen = Path([(952,86),(1797,0),(1722,534),(965,512)]).contains_points(np.c_[xx.ravel(),yy.ravel()]).reshape(h,w)
lum = 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def soft(m,r=7): return np.asarray(Image.fromarray((np.clip(m,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)/255
colored = np.clip((S-0.10)/0.30,0,1)                       # how "neon-tinted" a pixel is
bright  = np.clip((V-0.22)/0.25,0,1)                       # neon tubes + strong glow
k_red  = np.clip(soft(colored*bright*((H>=255)|(H<=20)))*1.7,0,1)           # magenta/pink/purple highlights -> red
k_grey = soft(colored) * (1-k_red)                         # remaining tint (blue/violet wash) -> neutral
red  = np.stack([np.clip(lum*2.3,0,1), lum*0.20, lum*0.24],-1)
grey = np.stack([lum*0.95, lum*0.97, lum*1.0],-1)
o = a*(1-k_red[...,None]) + red*k_red[...,None]
o = o*(1-k_grey[...,None]) + grey*k_grey[...,None]
o = np.clip((o-0.015)*1.05,0,1)
sm = soft(screen.astype(np.float32),2)[...,None]
o = o*(1-sm) + np.array([0.07,0.07,0.075])*sm                # blank screen plate for the GT recording
Image.fromarray((o*255).astype(np.uint8)).save(out, quality=92)
print('ok')

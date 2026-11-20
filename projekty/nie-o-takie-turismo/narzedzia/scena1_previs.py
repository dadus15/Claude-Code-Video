import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
room, card, out, tmp = sys.argv[1:5]; os.makedirs(tmp, exist_ok=True)
FPS=25; W,H=1080,1920
F='/usr/share/fonts/opentype/inter/'; fnt=lambda s,w='SemiBold': ImageFont.truetype(F+f'Inter-{w}.otf', s)
R=Image.open(room).convert('RGB')
d=ImageDraw.Draw(R)
for k,t in enumerate(['GT7','personalizacja','felg auta']): d.text((1330,200+k*40),t,fill=(200,200,205),font=fnt(30),anchor='mm')
# --- postać z karty (wycięta z szarego tła), od pasa w górę
C=Image.open(card).convert('RGB').crop((95,10,415,470))
from scipy import ndimage
hsv=np.asarray(C.convert('HSV')).astype(np.int16); sat=hsv[...,1]; val=hsv[...,2]
cand=(sat<22)&(val>88)&(val<185)
lab,n=ndimage.label(cand); edge=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
bgm=np.isin(lab,list(edge)); bgm=ndimage.binary_closing(bgm,iterations=2); bgm[:4,:]=bgm[-4:,:]=True; bgm[:,:4]=bgm[:,-4:]=True
m=Image.fromarray(((~bgm)*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
k=2.2; fig=C.resize((int(320*k),int(460*k)),Image.LANCZOS); m=m.resize(fig.size,Image.LANCZOS)
# --- tło kontrplanu: lustrzany, mocno rozmyty pokój (bokeh za nim)
rev=R.transpose(Image.FLIP_LEFT_RIGHT).crop((300,0,948,1152)).resize((W,H)).filter(ImageFilter.GaussianBlur(28))
rev=Image.blend(rev,Image.new('RGB',(W,H),(10,8,8)),0.35)
plate=rev.copy(); pd=ImageDraw.Draw(plate)
plate.paste(fig,((W-fig.width)//2,420),m)
pd.rounded_rectangle((W//2-140,1270,W//2+140,1370),radius=40,fill=(15,15,17),outline=(60,60,64),width=3)   # pad (szkic)
pd.rectangle((0,1520,W,H),fill=(22,20,20))                                                                 # oparcie kanapy / dół kadru
def ease(t): return t*t*(3-2*t)
frames=[]
# 1) 0–3,4 s: najazd nad jego ramieniem na ekran (sylwetka z tyłu wypada dołem szybciej niż tło = paralaksa)
N1=85
for i in range(N1):
    t=ease(i/(N1-1)); cw=648+(648/2.1-648)*t; ch=1152+(1152/2.1-1152)*t; cx=1060+(1360-1060)*t; cy=576+(300-576)*t
    fr=R.crop((int(cx-cw/2),int(cy-ch/2),int(cx+cw/2),int(cy+ch/2))).resize((W,H),Image.LANCZOS)
    dd=ImageDraw.Draw(fr); sy=1500+t*900; sc_=1+1.2*t
    dd.ellipse((W/2-150*sc_,sy-190*sc_,W/2+150*sc_,sy+150*sc_),fill=(8,8,9))          # głowa z tyłu
    dd.rounded_rectangle((W/2-420*sc_,sy+80*sc_,W/2+420*sc_,sy+700*sc_),radius=int(160*sc_),fill=(6,6,7))  # barki
    frames.append(fr)
# 2) 3,4–3,8 s: szybka panorama (rozmycie kierunkowe) z ekranu na niego
last=frames[-1]
def hblur(img,n):
    a=np.asarray(img).astype(np.float32); acc=np.zeros_like(a)
    for k in range(n): acc+=np.roll(a,k*6,axis=1)
    return Image.fromarray((acc/n).astype(np.uint8))
for i in range(10):
    t=(i+1)/10; off=int(W*t)
    comp=Image.new('RGB',(W,H)); comp.paste(last,(-off,0)); comp.paste(plate,(W-off,0))
    frames.append(hblur(comp, int(40*np.sin(np.pi*t))+1))
# 3) 3,8–7,6 s: on na kanapie z padem, kwestia, uniesiona dłoń
N3=95
for i in range(N3):
    fr=plate.copy(); dd=ImageDraw.Draw(fr); ts=3.8+i/FPS
    if 4.4<=ts<=6.6: dd.text((W//2,1640),'„Nie o takie Turismo nam chodzi.”',fill=(255,255,255),font=fnt(52),anchor='mm')
    if ts>=6.9: dd.text((W//2,1640),'↑ prawa dłoń do pstryknięcia',fill=(220,30,45),font=fnt(44),anchor='mm')
    frames.append(fr)
for i,fr in enumerate(frames):
    dd=ImageDraw.Draw(fr); ts=i/FPS
    dd.rectangle((0,0,W,70),fill=(0,0,0)); dd.text((24,35),f'SCENA 1 · PREVIS (szkic, nie render) · {ts:4.1f} s',fill=(220,30,45),font=fnt(30),anchor='lm')
    fr.save(f'{tmp}/f{i:03d}.jpg',quality=88)
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{tmp}/f%03d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','21',out],check=True)
frames[40].resize((360,640)).save(f'{tmp}/s1.png'); frames[90].resize((360,640)).save(f'{tmp}/s2.png'); frames[150].resize((360,640)).save(f'{tmp}/s3.png')
print('ok',len(frames))

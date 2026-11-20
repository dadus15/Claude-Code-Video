import sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont
src, out, tmp = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(tmp, exist_ok=True)
im = Image.open(src).convert('RGB'); W,H = im.size
d = ImageDraw.Draw(im); f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 34)
for k,t in enumerate(['GT7','personalizacja','felg auta','','nagranie z konsoli','felga w środkowej','1/3 kadru gry']):
    d.text((1360,180+k*34),t,fill=(200,200,205) if k<3 else (120,120,128),font=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 26),anchor='mm')
d.rectangle((1220,40,1500,520),outline=(220,30,45),width=3)
N=100
def ease(t): return t*t*(3-2*t)
# crop 9:16: start = wide strip incl. table + left part of screen ; end = screen centre, 2.1x closer
cw0, ch0 = 648, 1152; cx0, cy0 = 1060, 576
cw1, ch1 = 648/2.1, 1152/2.1; cx1, cy1 = 1360, 300
for i in range(N):
    t = ease(i/(N-1)); cw = cw0+(cw1-cw0)*t; ch = ch0+(ch1-ch0)*t; cx = cx0+(cx1-cx0)*t; cy = cy0+(cy1-cy0)*t
    box = (cx-cw/2, cy-ch/2, cx+cw/2, cy+ch/2)
    im.crop(tuple(int(round(v)) for v in box)).resize((1080,1920), Image.LANCZOS).save(f'{tmp}/p{i:03d}.jpg', quality=90)
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','25','-i',f'{tmp}/p%03d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','20',out],check=True)
print('ok')

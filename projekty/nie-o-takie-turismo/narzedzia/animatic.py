import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
SB, OUT, TMP = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(TMP, exist_ok=True)
F='/usr/share/fonts/opentype/inter/'
f=lambda s,w='Regular': ImageFont.truetype(F+f'Inter-{w}.otf', s)
seq=[(0,1.6,'A_first','A','(dźwięk gry → klik pauzy 1.6 s)'),(1.6,6,'A_last','A','„Chyba nie o takie Turismo nam chodzi”'),
(6,8,'B_first','B','PSTRYK 1 (cięcie na trzasku)'),(8,10.4,'B_last','B','„Coś mi nie pasuje”'),
(10.4,11.4,'C_first','C','PSTRYK 2 → twarde cięcie, ta sama klatka'),(11.4,13,'C_last','C','„Od razu lepiej”'),
(13,17,'D_first','D','„W Turismo Wheels robimy kute felgi na zamówienie.”'),(17,19,'D_last','D','„Mamy sporo wzorów. Pokażę Ci jeden”'),
(19,19.4,'EF_K1','E','(dłoń wchodzi)'),(19.4,21,'EF_K2','E','„Ten”.  [kciuk kryje rant → 2D→3D]'),(21,23,'EF_K3','E','(cisza)'),
(23,24.8,'EF_K4','F','(stuk osadzenia, popchnięcie) „To C19-R”'),(24.8,26,'F_last','F','okno detalu'),
(26,30,'G_first','G','„Ten pierścień na obwodzie to zintegrowany aero-ring”'),(30,34,'G_last','G','„Spójrz, jak głęboko schodzą ramiona”'),
(34,38.8,'H_first','H','„Rozmiar, ET i wykończenie dobieramy pod Twoje auto. Napisz, czym jeździsz. Strzała!”'),(38.8,40,'H_last','H','plansza: koło jak w 0:00 + CTA')]
lines=[]
for i,(a,b,img,L,txt) in enumerate(seq):
    src=Image.open(f'{SB}/{img}.png').convert('RGB')
    fr=Image.new('RGB',(1080,1920),(10,10,12))
    s=min(1080/src.width,1640/src.height); im=src.resize((int(src.width*s),int(src.height*s)),Image.LANCZOS)
    fr.paste(im,((1080-im.width)//2,40)); d=ImageDraw.Draw(fr)
    d.rectangle((0,1700,1080,1920),fill=(0,0,0))
    d.text((40,1735),f'{L}   {a:05.2f}–{b:05.2f} s   ANIMATIK (plansze, nie render)',fill=(220,30,45),font=f(30,'SemiBold'))
    import textwrap
    for k,l in enumerate(textwrap.wrap(txt,44)): d.text((40,1790+k*52),l,fill=(245,245,245),font=f(42,'Medium'))
    p=f'{TMP}/f{i:02d}.png'; fr.save(p); lines.append(f"file '{p}'\nduration {b-a:.2f}\n")
lines.append(f"file '{TMP}/f{len(seq)-1:02d}.png'\n")
open(f'{TMP}/list.txt','w').write(''.join(lines))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{TMP}/list.txt','-vf','fps=25,format=yuv420p','-t','40','-c:v','libx264','-crf','23',OUT],check=True)
print('done')

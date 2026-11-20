import sys, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REF, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/opentype/inter/'
def font(sz, w='Regular'): return ImageFont.truetype(F+f'Inter-{w}.otf', sz)
BG=(18,18,20); LINE=(200,200,205); DIM=(110,110,118); RED=(220,30,45); WHITE=(245,245,245); SILVER=(196,200,206)

def glow(img, xy, r, col, a=150):
    g=Image.new('RGBA', img.size, (0,0,0,0)); d=ImageDraw.Draw(g)
    x,y=xy; d.ellipse((x-r,y-r,x+r,y+r), fill=col+(a,)); g=g.filter(ImageFilter.GaussianBlur(r/2.2))
    img.alpha_composite(g)

def wheel(d, cx, cy, r, spokes=10, rot=0, col=SILVER, w=3, tyre=False, ring=True):
    if tyre: d.ellipse((cx-r*1.28,cy-r*1.28,cx+r*1.28,cy+r*1.28), fill=(28,28,30), outline=(60,60,64), width=2)
    d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=col, width=w+1)
    if ring: d.ellipse((cx-r*0.88,cy-r*0.88,cx+r*0.88,cy+r*0.88), outline=col, width=max(1,w-1))
    for i in range(spokes):
        a=math.radians(rot+i*360/spokes)
        d.line((cx+math.cos(a)*r*0.18, cy+math.sin(a)*r*0.18, cx+math.cos(a)*r*0.86, cy+math.sin(a)*r*0.86), fill=col, width=w)
    d.ellipse((cx-r*0.17,cy-r*0.17,cx+r*0.17,cy+r*0.17), outline=col, width=w)

def person(d, x, y, s=1.0, shirt='GT', face=True, back=False):
    # x,y = top of head center
    hr=26*s
    d.ellipse((x-hr,y,x+hr,y+2.2*hr), fill=(196,160,140) if not back else (70,60,55))
    d.chord((x-hr-2,y-4*s,x+hr+2,y+1.4*hr), 180, 360, fill=(95,90,88))   # hair
    if face and not back:
        d.ellipse((x-10*s,y+22*s,x-5*s,y+27*s), fill=(40,40,40)); d.ellipse((x+5*s,y+22*s,x+10*s,y+27*s), fill=(40,40,40))
    ty=y+2.3*hr
    d.rounded_rectangle((x-62*s,ty,x+62*s,ty+120*s), radius=int(22*s), fill=(12,12,12), outline=(70,70,74), width=2)
    if shirt=='GT' and not back:
        d.rectangle((x-24*s,ty+28*s,x+24*s,ty+46*s), outline=WHITE, width=2)
        d.text((x,ty+37*s),'GT',fill=WHITE,font=font(int(13*s),'Bold'),anchor='mm')
    if shirt=='TW' and not back:
        ex=x-30*s   # wearer's left chest appears on viewer's... (front view: wearer's left = viewer's right)
        ex=x+30*s
        d.polygon([(ex-12*s,ty+40*s),(ex-2*s,ty+28*s),(ex+14*s,ty+28*s),(ex+4*s,ty+40*s)], outline=WHITE, width=2)
        d.ellipse((ex-9*s,ty+34*s,ex-5*s,ty+38*s), fill=RED)
    if shirt=='TW' and back:
        d.text((x,ty+20*s),'TURISMO',fill=SILVER,font=font(int(10*s),'Medium'),anchor='mm')
        wheel(d,x,ty+62*s,32*s,spokes=5,col=SILVER,w=1)
    return ty

def hand(d, x, y, s=1.0, pose='snap', col=(196,160,140)):
    d.rounded_rectangle((x-22*s,y,x+22*s,y+48*s), radius=int(12*s), fill=col)
    if pose=='snap':
        d.rounded_rectangle((x-6*s,y-34*s,x+6*s,y+4*s), radius=int(6*s), fill=col)       # middle finger
        d.rounded_rectangle((x+8*s,y-24*s,x+19*s,y+4*s), radius=int(6*s), fill=col)      # ring
        d.rounded_rectangle((x-30*s,y-14*s,x-18*s,y+20*s), radius=int(6*s), fill=col)    # thumb
        d.ellipse((x-12*s,y-40*s,x+2*s,y-26*s), outline=RED, width=2)
    elif pose=='open':
        for i,dx in enumerate((-17,-6,5,16)):
            d.rounded_rectangle((x+dx*s-5*s,y-(36-abs(dx)*0.6)*s,x+dx*s+5*s,y+4*s), radius=int(5*s), fill=col)
        d.rounded_rectangle((x-34*s,y+6*s,x-20*s,y+30*s), radius=int(6*s), fill=col)

def laptop(d, x, y, w, h, content=None, angle=0):
    d.rectangle((x,y,x+w,y+h), fill=(8,8,10), outline=(90,90,96), width=4)   # bezel
    d.rectangle((x+8,y+8,x+w-8,y+h-8), fill=(235,235,238))
    d.polygon([(x-14,y+h),(x+w+14,y+h),(x+w+40,y+h+18),(x-40,y+h+18)], fill=(70,70,76))
    return (x+8,y+8,x+w-8,y+h-8)

def stand(d, cx, y, w=120):
    d.polygon([(cx-w/2,y),(cx+w/2,y),(cx+w/2-12,y+22),(cx-w/2+12,y+22)], fill=(10,10,12), outline=(80,80,86))
    for dx in (-w*0.25, w*0.25):
        d.ellipse((cx+dx-11,y-9,cx+dx+11,y+13), fill=(30,30,34), outline=(150,150,156), width=2)

def wall_wheels(d, box, n=3, m=2):
    x0,y0,x1,y1=box
    for i in range(n):
        for j in range(m):
            cx=x0+(i+0.5)*(x1-x0)/n; cy=y0+(j+0.5)*(y1-y0)/m
            wheel(d,cx,cy,min((x1-x0)/n,(y1-y0)/m)*0.38,spokes=7,col=(120,122,128),w=1)

def thumb(sz):
    return Image.new('RGBA', sz, BG+(255,))

def frame_label(d, txt, w):
    d.rectangle((0,0,w,26), fill=(0,0,0)); d.text((8,13), txt, fill=LINE, font=font(14,'SemiBold'), anchor='lm')

TW,TH=300,533
def A1():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,TW,TH), fill=(40,52,70))
    wheel(d,150,280,105,spokes=10,col=(205,205,210),w=4,tyre=True)
    d.text((150,500),'gameplay GT (nagranie)',fill=WHITE,font=font(13),anchor='mm')
    frame_label(d,'PIERWSZA 0:00',TW); return im
def A2():
    im=thumb((TW,TH)); glow(im,(250,120),110,(200,0,20),170); d=ImageDraw.Draw(im)
    for y in (90,150,210): d.line((180,y,300,y),fill=WHITE,width=3); [d.rectangle((190+k*30,y-10,210+k*30,y-1),fill=RED) for k in range(3)]
    hand(d,150,300,2.6,'snap')
    d.text((150,500),'palce tuż przed pstryk.',fill=WHITE,font=font(13),anchor='mm')
    frame_label(d,'OSTATNIA 0:06',TW); return im
def B1():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(58,58,62))
    hand(d,150,300,2.6,'snap'); d.text((150,500),'ta sama skala dłoni, biuro',fill=WHITE,font=font(13),anchor='mm')
    frame_label(d,'PIERWSZA 0:06',TW); return im
def seated(shirt, hands='pinch', label='', smile=False):
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(52,52,56))
    wall_wheels(d,(20,40,280,190))
    d.rounded_rectangle((10,330,290,450),radius=18,fill=(30,30,32),outline=(80,80,84))  # sofa
    ty=person(d,150,150,1.15,shirt)
    if hands=='pinch':
        hand(d,182,ty+100,0.8,'open'); d.text((210,ty+130),'L: chwyt',fill=RED,font=font(11),anchor='lm')
        hand(d,85,ty+30,0.9,'snap'); d.text((40,ty+80),'P: pstryk',fill=RED,font=font(11),anchor='lm')
    else:
        hand(d,185,ty+130,0.8,'open'); hand(d,110,ty+130,0.8,'open')
    d.text((150,500),label,fill=WHITE,font=font(13),anchor='mm')
    return im,d
def B2():
    im,d=seated('GT','pinch','C-PRZED: koszulka GT'); frame_label(d,'OSTATNIA 0:10.4',TW); return im
def C1():
    im,d=seated('TW','pinch','C-PO: kopia C-PRZED + znak TW'); frame_label(d,'PIERWSZA 0:10.4',TW); return im
def C2():
    im,d=seated('TW','free','puszcza materiał, „Od razu lepiej”'); frame_label(d,'OSTATNIA 0:13',TW); return im
def D1():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(50,50,54))
    laptop(d,170,290,110,70); person(d,95,110,1.6,"TW",back=True)
    d.text((150,500),'zza ramienia: wzór na plecach',fill=WHITE,font=font(13),anchor='mm')
    frame_label(d,'PIERWSZA 0:13',TW); return im
def scr_wheel(d,box,r_frac=0.33):
    x0,y0,x1,y1=box; d.rectangle((x0,y0,x0+(x1-x0),y0+14),fill=(20,20,22))
    wheel(d,(x0+x1)/2,(y0+y1)/2+6,(x1-x0)*r_frac,spokes=10,col=(150,152,158),w=2)
def D2():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(50,50,54))
    b=laptop(d,30,170,200,130); scr_wheel(d,b); stand(d,262,330,60)
    d.ellipse((126,168,144,186),outline=RED,width=3)
    hand(d,215,150,0.9,'open'); d.text((150,500),'@WEB: karta C19-R, dłoń nad rantem',fill=WHITE,font=font(12),anchor='mm')
    frame_label(d,'OSTATNIA 0:19',TW); return im
def K(n, big=False):
    W,H=(TW,TH) if not big else (540,960); s=W/TW
    im=Image.new('RGBA',(W,H),(48,48,52,255)); glow(im,(int(70*s),int(240*s)),int(90*s),(170,190,255),60); d=ImageDraw.Draw(im)
    d.rectangle((0,int(380*s),W,H),fill=(36,34,34))       # table
    lx,ly,lw,lh=int(14*s),int(225*s),int(120*s),int(82*s)
    box=laptop(d,lx,ly,lw,lh); sx=int(212*s); sty=int(372*s); stand(d,sx,sty,int(70*s))
    cx,cy=(box[0]+box[2])/2,(box[1]+box[3])/2+4*s; r=(box[2]-box[0])*0.30
    if n==1:
        wheel(d,cx,cy,r,col=(150,152,158),w=2); hand(d,cx+40*s,cy-r-38*s,0.75*s,'open')
        cap='K1  19.0 s  felga na stronie, dłoń nadchodzi'
    elif n==2:
        wheel(d,cx,cy,r,col=(150,152,158),w=2)
        tx,ty_=cx,cy-r
        d.ellipse((tx-14*s,ty_-6*s,tx+14*s,ty_+22*s),fill=(196,160,140),outline=RED,width=3)  # thumb pad
        d.rounded_rectangle((tx-6*s,ty_-60*s,tx+30*s,ty_-4*s),radius=int(10*s),fill=(196,160,140))
        d.line((tx-34*s,ty_-2*s,tx+34*s,ty_-2*s),fill=RED,width=2)
        cap='K2  19.4 s  kciuk na rancie (12:00), palce znikają za rantem'
    elif n==3:
        d.rectangle((cx-r-2,cy-r-2,cx+r+2,cy+r+2),fill=(222,222,226))   # neutral field on page
        R=int(82*s); wx,wy=int(205*s),int(262*s)
        wheel(d,wx,wy,R,col=SILVER,w=max(2,int(3*s)))
        d.ellipse((wx-16*s,wy-R-12*s,wx+16*s,wy-R+18*s),fill=(196,160,140))
        d.rounded_rectangle((wx-30*s,wy+R-6*s,wx+34*s,wy+R+20*s),radius=int(10*s),fill=(196,160,140))
        d.line((wx,wy+R+24*s,wx,sty-12*s),fill=RED,width=2); d.text((wx+6*s,(wy+R+sty)/2+6*s),'~1 dłoń',fill=RED,font=font(int(11*s)),anchor='lm')
        cap='K3  23.0 s  pełna obręcz nad podstawką, lewa dłoń pod spodem'
    else:
        d.rectangle((cx-r-2,cy-r-2,cx+r+2,cy+r+2),fill=(222,222,226))
        R=int(82*s); wx=sx; wy=sty-9*s-R+2*s
        wheel(d,wx,wy,R,col=SILVER,w=max(2,int(3*s)),rot=12)
        for dx in (-int(70*s)*0.25,int(70*s)*0.25): d.ellipse((wx+dx-4*s,sty-6*s,wx+dx+4*s,sty+2*s),fill=RED)
        d.arc((wx-R-14*s,wy-R-14*s,wx+R+14*s,wy+R+14*s),-40,10,fill=RED,width=3)
        cap='K4  23.6 s  obręcz na obu rolkach (2 punkty styku)'
    import textwrap
    d.rectangle((0,H-int(60*s),W,H),fill=(0,0,0))
    for k,l in enumerate(textwrap.wrap(cap,40)): d.text((int(10*s),H-int(48*s)+k*int(17*s)),l,fill=WHITE,font=font(int(12*s),'Medium'),anchor='lm')
    return im
def F2():
    im=K(4); d=ImageDraw.Draw(im)
    d.rectangle((150,40,290,180),outline=RED,width=4); wheel(d,220,110,80,col=SILVER,w=3,rot=30)
    d.text((220,30),'okno detalu (po 1. obrocie)',fill=RED,font=font(11),anchor='mm')
    frame_label(d,'OSTATNIA 0:26',TW); return im
def G1():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(16,16,18))
    wheel(d,150,260,120,col=SILVER,w=3); d.arc((150-128,260-128,150+128,260+128),200,290,fill=RED,width=5)
    d.text((24,62),'Zintegrowany aero-ring',fill=WHITE,font=font(17,'SemiBold')); d.text((24,86),'Integrated aero-ring',fill=DIM,font=font(11))
    d.text((150,500),'3D/turntable C19-R (bez tekstu)',fill=WHITE,font=font(12),anchor='mm')
    frame_label(d,'PIERWSZA 0:26',TW); return im
def G2():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(16,16,18))
    d.ellipse((-60,150,330,520),outline=SILVER,width=4)
    for a in (200,240,280,320): d.line((135,335,135+math.cos(math.radians(a))*190,335+math.sin(math.radians(a))*170),fill=SILVER,width=6)
    d.line((60,250,135,335),fill=WHITE,width=2); d.ellipse((128,328,142,342),fill=RED)
    d.text((24,62),'Profil ramion',fill=WHITE,font=font(17,'SemiBold')); d.text((24,86),'Spoke profile',fill=DIM,font=font(11))
    frame_label(d,'OSTATNIA 0:34',TW); return im
def H1():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(52,52,56))
    wall_wheels(d,(20,40,280,170)); person(d,110,150,1.05,'TW'); stand(d,235,430,70); wheel(d,235,360,62,col=SILVER,w=2,rot=40)
    for i,t in enumerate(('Rozmiar','ET','Wykończenie')): d.text((200,210+i*24),t,fill=WHITE if i==0 else DIM,font=font(14,'SemiBold'))
    frame_label(d,'PIERWSZA 0:34',TW); return im
def H2():
    im=thumb((TW,TH)); d=ImageDraw.Draw(im); d.rectangle((0,0,TW,TH),fill=(12,12,14))
    wheel(d,150,280,105,spokes=10,col=SILVER,w=4,tyre=False)
    d.text((150,70),'TURISMO WHEELS',fill=WHITE,font=font(18,'Bold'),anchor='mm')
    d.text((150,430),'Napisz, czym jeździsz',fill=WHITE,font=font(17,'SemiBold'),anchor='mm')
    d.text((150,455),'+48 501 404 861',fill=DIM,font=font(11),anchor='mm')
    d.text((150,500),'koło = ten sam rozmiar/środek co 0:00',fill=RED,font=font(11),anchor='mm')
    frame_label(d,'OSTATNIA 0:40',TW); return im

SHOTS=[
 ('A','0:00–0:06','Pauza i pierwszy pstryk',A1,A2,'„Chyba nie o takie Turismo nam chodzi”','Insert gry → kciuk → kanapa; cięcie ciasno na palce'),
 ('B','0:06–0:10.4','Przeskok do biura',B1,B2,'„Coś mi nie pasuje”','Match palców → odjazd → siada pod ścianą felg'),
 ('C','0:10.4–0:13','Zmiana koszulki',C1,C2,'„Od razu lepiej”','Statyw, twarde cięcie na pstryk, ta sama klatka'),
 ('D','0:13–0:19','Strona i wybór',D1,D2,'„W Turismo Wheels robimy kute felgi…”','Zza ramienia → rack na ekran; ekran = @WEB'),
 ('E','0:19–0:23','Wyjęcie felgi',lambda:(lambda im:(frame_label(ImageDraw.Draw(im),'PIERWSZA 0:19.4',TW),im)[1])(K(2)),lambda:(lambda im:(frame_label(ImageDraw.Draw(im),'OSTATNIA 0:23',TW),im)[1])(K(3)),'„Ten”. Cisza.','Płytki 3/4, rant przecina ramkę laptopa'),
 ('F','0:23–0:26','Osadzenie i okno',lambda:(lambda im:(frame_label(ImageDraw.Draw(im),'PIERWSZA 0:23',TW),im)[1])(K(3)),F2,'„To C19-R”','Stop na rolkach, popchnięcie, okno 6–8 kl.'),
 ('G','0:26–0:34','Dwie cechy',G1,G2,'„Ten pierścień…” / „Spójrz, jak głęboko…”','Makro: frontal → 3/4, ta sama faza obrotu'),
 ('H','0:34–0:40','Domknięcie',H1,H2,'„Rozmiar, ET… Napisz, czym jeździsz. Strzała!”','Oczy w obiektyw, potem koło jak w 0:00'),
]
PW,PH=640,860
sheet=Image.new('RGB',(PW*4+50,PH*2+150),BG); sd=ImageDraw.Draw(sheet)
sd.text((25,40),'„Nie o takie Turismo” — storyboard 9:16, plan kompozycji (szkic, nie render)',fill=WHITE,font=font(30,'Bold'))
sd.text((25,85),'Każdy panel: pierwsza i ostatnia klatka ujęcia. Felga na szkicach to schemat — nie geometria C19-R.',fill=DIM,font=font(18))
for i,(L,tc,title,f1,f2,vo,cam) in enumerate(SHOTS):
    px=25+(i%4)*PW; py=130+(i//4)*PH
    p=Image.new('RGB',(PW-20,PH-20),(28,28,31)); pd=ImageDraw.Draw(p)
    pd.text((14,14),L,fill=RED,font=font(40,'Bold')); pd.text((64,18),title,fill=WHITE,font=font(20,'SemiBold')); pd.text((64,46),tc,fill=DIM,font=font(15))
    a=f1().convert('RGB'); b=f2().convert('RGB')
    p.paste(a,(4,80)); p.paste(b,(PW-20-TW-4,80))
    pd.text((14,630),'Dialog:',fill=DIM,font=font(14)); 
    import textwrap
    for k,line in enumerate(textwrap.wrap(vo,52)): pd.text((14,652+k*22),line,fill=WHITE,font=font(16,'Medium'))
    pd.text((14,730),'Kamera/akcja:',fill=DIM,font=font(14))
    for k,line in enumerate(textwrap.wrap(cam,56)): pd.text((14,752+k*22),line,fill=LINE,font=font(15))
    sheet.paste(p,(px,py))
    a.save(f'{OUT}/{L}_first.png'); b.save(f'{OUT}/{L}_last.png')
sheet.save(f'{OUT}/00_storyboard_A-H.png')

# E–F four-frame board + timeline
W=540*4+5*20; eb=Image.new('RGB',(W,960+540),BG); ed=ImageDraw.Draw(eb)
for n in range(1,5):
    k=K(n,big=True).convert('RGB'); eb.paste(k,(20+(n-1)*560,20)); k.save(f'{OUT}/EF_K{n}.png')
y0=1040; x0=60; x1=W-60; t0,t1=19.0,26.0
def X(t): return x0+(t-t0)/(t1-t0)*(x1-x0)
ed.line((x0,y0,x1,y0),fill=LINE,width=3)
for t in [19+i*0.5 for i in range(15)]:
    ed.line((X(t),y0-8,X(t),y0+8),fill=LINE,width=2); ed.text((X(t),y0+22),f'{t:.1f}s',fill=DIM,font=font(15),anchor='mm')
    ed.text((X(t),y0+42),f'kl.{int(round(t*25))}',fill=(80,80,86),font=font(12),anchor='mm')
ev=[(19.0,19.4,'dłoń wchodzi','LINE'),(19.4,19.64,'KCIUK KRYJE RANT 12:00 → podmiana 2D→3D pod kciukiem (kl. 485–491)','RED'),
    (19.64,21.2,'ręka cofa się; górny rant przecina ramkę laptopa; skala rośnie do 1:1','LINE'),
    (20.9,21.5,'lewa dłoń pod 6:00','LINE'),(21.5,23.0,'skala zablokowana, obręcz płynie nad podstawkę','LINE'),
    (23.0,23.6,'opuszcza na 2 rolki','LINE'),(23.6,24.0,'dłonie puszczają','LINE'),(24.0,24.2,'popchnięcie styczne','RED'),
    (24.8,25.1,'okno detalu otwiera się (6–8 kl.)','RED')]
for i,(a,b,txt,c) in enumerate(ev):
    yy=y0+80+i*42; col=RED if c=='RED' else SILVER
    ed.rectangle((X(a),yy,max(X(b),X(a)+6),yy+22),fill=col); ed.text((max(X(b),X(a)+6)+10,yy+11),txt,fill=WHITE,font=font(16),anchor='lm')
ed.text((x0,y0-52),'VO: „Ten” na 19.4 s (kontakt kciuka) → cisza do „To C19-R” ok. 24.2 s. Muzyka odsunięta 19.4–24.0 s.',fill=WHITE,font=font(20,'SemiBold'))
eb.save(f'{OUT}/01_E-F_4_klatki_os_czasu.png')

# C mockup: real emblem on approved card (placement/scale check only)
card=Image.open(f'{REF}/Postac-FINAL.png').convert('RGB')
fig=card.crop((95,10,415,560)).resize((640,1100),Image.LANCZOS)
emb=Image.open(f'{REF}/TURISMO-TSHIRT-DIAMONDS_03_oneck.jpg').convert('RGB').crop((420,1150,1150,1600))
# key out black-ish background for overlay
emb=emb.resize((92,57),Image.LANCZOS); mask=emb.convert('L').point(lambda v:255 if v>70 else 0).filter(ImageFilter.GaussianBlur(0.6))
before=fig.copy(); bd=ImageDraw.Draw(before)
bd.rectangle((250,395,400,455),outline=WHITE,width=3); bd.text((325,425),'@GT logo',fill=WHITE,font=font(18,'Bold'),anchor='mm')
after=fig.copy(); after.paste(emb,(384,388),mask)
mk=Image.new('RGB',(1340,1240),BG); md=ImageDraw.Draw(mk)
mk.paste(before,(20,110)); mk.paste(after,(680,110))
md.text((20,30),'C — makieta umiejscowienia znaku (karta Postac-FINAL, prawdziwy znak z @TWdetail)',fill=WHITE,font=font(24,'Bold'))
md.text((20,68),'C-PRZED: placeholder @GT (do podmiany)',fill=DIM,font=font(18)); md.text((680,68),'C-PO: znak na lewej piersi noszącego, ~1/6 szer. barków',fill=DIM,font=font(18))
mk.save(f'{OUT}/02_C_makieta_znaku.png')
print('ok')

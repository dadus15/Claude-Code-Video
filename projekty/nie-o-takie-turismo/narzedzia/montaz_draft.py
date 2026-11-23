"""Montaż wersji roboczej „Nie o takie Turismo” (Black Friday) w stylu Kareemy:
krótkie ujęcia, cięcia na akcji/trzasku, natywny dźwięk ujęć, muzyka z dropem przy wyjęciu felgi,
napisy TikTok, hook BF, plansza końcowa. 1080x1920, 24 kl./s.
Użycie: python3 montaz_draft.py <katalog_projektu_v2> <nagranie_ekranu.webm> <wyjście.mp4> <tmp>"""
import sys, os, math, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

V2, SCREEN, OUT, TMP = sys.argv[1:5]; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 24
K = f'{V2}/klipy/draft'; A = f'{V2}/klipy/audio'
FD = '/usr/share/fonts/opentype/inter/'
def font(s, w='Black', disp=True): return ImageFont.truetype(FD + ('InterDisplay-' if disp else 'Inter-') + w + '.otf', s)
RED = (226, 30, 45); WHITE = (255, 255, 255)

# ---------------------------------------------------------------- dekodowanie
def decode(path, t0, t1, vf='scale=1080:1920:flags=lanczos', n=None):
    n = n or round((t1 - t0) * FPS)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.4f}', '-i', path, '-t', f'{t1 - t0 + 0.2:.4f}',
                        '-vf', f'fps={FPS},{vf}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(p, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr[:n]

def zoom(fr, z, cx=0.5, cy=0.5):
    if abs(z - 1) < 1e-3: return fr
    im = Image.fromarray(fr); w, h = W / z, H / z; x0 = cx * W - w / 2; y0 = cy * H - h / 2
    x0 = min(max(0, x0), W - w); y0 = min(max(0, y0), H - h)
    return np.asarray(im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC))

def hblur(fr, k):
    k = int(k)
    if k < 2: return fr
    c = np.cumsum(np.pad(fr.astype(np.float32), ((0, 0), (k, k), (0, 0)), mode='edge'), axis=1)
    return np.clip((c[:, 2 * k:2 * k + W] - c[:, :W]) / (2 * k), 0, 255).astype(np.uint8)

def whip(fr, s):                     # s: -1..1, przesunięcie w poziomie z rozmyciem (panorama szarpana)
    sh = int(s * W * 0.55); out = np.roll(fr, sh, axis=1); return hblur(out, abs(s) * 140)

# ---------------------------------------------------------------- tekst
def text_img(lines, size=96, color=WHITE, stroke=7, w='Black', spacing=8, shadow=True):
    f = font(size, w); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    boxes = [d0.textbbox((0, 0), t, font=f, stroke_width=stroke) for t, _ in lines]
    tw = max(b[2] - b[0] for b in boxes) + 40; th = sum(b[3] - b[1] for b in boxes) + spacing * (len(lines) - 1) + 40
    im = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 20
    for (t, col), b in zip(lines, boxes):
        x = (tw - (b[2] - b[0])) / 2 - b[0]
        d.text((x, y - b[1]), t, font=f, fill=col or color, stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += (b[3] - b[1]) + spacing
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.55))
        base = Image.new('RGBA', im.size, (0, 0, 0, 0)); base.alpha_composite(sh, (0, 6)); base.alpha_composite(im); im = base
    return im

def paste(fr, im, cx, cy, alpha=1.0, scale=1.0):
    base = Image.fromarray(fr).convert('RGBA')
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if alpha < 1: a = im.split()[3].point(lambda v: v * alpha); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    return np.asarray(base.convert('RGB'))

def pop(t, d=0.12):                  # skala „wyskoku” napisu
    if t >= d: return 1.0
    x = t / d; return 0.82 + 0.18 * (1 - (1 - x) ** 3) + 0.06 * math.sin(x * math.pi)

def caption(chunk): return text_img([(chunk, WHITE)], size=78, stroke=7, w='ExtraBold')

# ---------------------------------------------------------------- oś czasu
# (nazwa, plik, in, out, opcje)
G = lambda n: f'{K}/{n}.mp4'
SEG = [
    ('H1', G('G1'), 3.60, 4.40, {}),
    ('H2', G('G7'), 3.65, 4.45, {}),
    ('H3', G('G7'), 5.10, 6.00, {}),
    ('S1', G('G1'), 0.90, 4.60, {'whip_out': 6, 'zoom': (1.0, 1.06)}),
    ('S2', G('G2'), 1.40, 4.60, {'whip_in': 5}),
    ('S3a', G('G3'), 0.00, 1.00, {}),
    ('S3b', G('G3'), 2.30, 4.85, {'zoom': (1.12, 1.12), 'cy': 0.42}),
    ('S4', G('G4'), 0.00, 4.90, {}),
    ('S5', G('G5'), 0.10, 9.20, {}),
    ('S6', G('G6b'), 0.35, 4.95, {}),
    ('S7', 'SCREEN', 0.00, 5.90, {}),
    ('S8', G('G7'), 0.00, 6.00, {}),
    ('S9', f'{V2}/klipy/gama_spin_11s.mp4', 0.00, 11.00, {'native': True}),
    ('S10', G('G8'), 0.00, 3.60, {}),
    ('S11', G('G9'), 0.00, 5.70, {}),
    ('S12', 'END', 0.00, 3.20, {}),
]
T = {}; t = 0.0
for name, src, a, b, o in SEG: T[name] = t; t += round((b - a) * FPS) / FPS
TOTAL = t
print('długość', round(TOTAL, 2), json.dumps({k: round(v, 2) for k, v in T.items()}))

# napisy: (segment, start, koniec w czasie segmentu, tekst)
def src2seg(seg, ts):                # czas źródła -> czas segmentu
    s = next(x for x in SEG if x[0] == seg); return ts - s[2]
CAPS = [
    ('S2', src2seg('S2', 2.10), src2seg('S2', 2.85), 'Nie o takie Turismo'),
    ('S2', src2seg('S2', 2.85), src2seg('S2', 3.80), 'nam chodzi.'),
    ('S3b', src2seg('S3b', 3.35), src2seg('S3b', 4.40), 'Coś mi nie pasuje.'),
    ('S4', src2seg('S4', 1.05), src2seg('S4', 2.00), 'Od razu lepiej.'),
    ('S5', src2seg('S5', 0.60), src2seg('S5', 1.80), 'W Turismo Wheels'),
    ('S5', src2seg('S5', 1.80), src2seg('S5', 3.45), 'projektujemy customowe felgi kute'),
    ('S5', src2seg('S5', 3.45), src2seg('S5', 5.20), 'na indywidualne zamówienie.'),
    ('S5', src2seg('S5', 5.65), src2seg('S5', 6.70), 'Chodźcie,'),
    ('S5', src2seg('S5', 6.70), src2seg('S5', 8.40), 'przedstawię wam naszą gamę modelową.'),
    ('S7', 0.40, 2.40, 'Tutaj znajduje się lista naszych produktów.'),
    ('S7', 2.55, 5.05, 'Weźmy pod lupę na przykład model C01.'),
    ('S10', src2seg('S10', 0.40), src2seg('S10', 1.35), 'Teraz możesz'),
    ('S10', src2seg('S10', 1.35), src2seg('S10', 2.15), 'je zamówić'),
    ('S10', src2seg('S10', 2.15), src2seg('S10', 3.55), 'z 15% off.'),
    ('S11', src2seg('S11', 0.10), src2seg('S11', 1.25), 'Rozmiar, ET i wykończenie'),
    ('S11', src2seg('S11', 1.25), src2seg('S11', 3.15), 'dobieramy pod Twoje auto.'),
    ('S11', src2seg('S11', 3.40), src2seg('S11', 4.85), 'Napisz, czym jeździsz.'),
    ('S11', src2seg('S11', 5.10), src2seg('S11', 5.70), 'Na razie!'),
]
CAP_IMG = {c[3]: caption(c[3]) for c in CAPS}
def wrap_caption(txt):
    im = CAP_IMG[txt]
    if im.width <= 940: return im
    words = txt.split(); half = len(words) // 2 + (1 if len(words) % 2 else 0)
    return text_img([(' '.join(words[:half]), WHITE), (' '.join(words[half:]), WHITE)], size=78, stroke=7, w='ExtraBold')
CAP_IMG = {k: wrap_caption(k) for k in CAP_IMG}

# hook i plansze
HOOK1 = text_img([('TO JEST', WHITE), ('TURISMO', WHITE)], size=150, stroke=9)
HOOK2 = text_img([('A TO JEST', WHITE), ('TURISMO', RED)], size=150, stroke=9)
def bf_bar():
    im = Image.new('RGBA', (W, 430), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 40, W, 230), fill=RED + (255,))
    f = font(132); b = d.textbbox((0, 0), 'BLACK FRIDAY', font=f); d.text(((W - b[2] + b[0]) / 2 - b[0], 135 - (b[3] + b[1]) / 2), 'BLACK FRIDAY', font=f, fill=WHITE)
    t2 = text_img([('−15% NA KAŻDY PRODUKT', WHITE)], size=70, stroke=6, w='ExtraBold', shadow=False)
    im.alpha_composite(t2, (int((W - t2.width) / 2), 250)); return im
BF = bf_bar()
BADGE = text_img([('−15%', RED)], size=300, stroke=12)
BADGE_EN = text_img([('BLACK FRIDAY · 15% off every wheel', WHITE)], size=44, stroke=5, w='Bold')

# ---------------------------------------------------------------- plansza końcowa
def cutout(path, size):
    src = Image.open(path).convert('RGB'); g = np.asarray(src.convert('L')).astype(np.float32)
    cols = np.nonzero((g < 235).sum(0) > 3)[0]; rows = np.nonzero((g < 235).sum(1) > 3)[0]
    x0, x1 = cols[0], cols[-1]; r = (x1 - x0) / 2; cxs = (x0 + x1) / 2; cys = rows[0] + r
    pad = r * 1.01; src = src.crop((int(cxs - pad), int(cys - pad), int(cxs + pad), int(cys + pad))).resize((size, size), Image.LANCZOS)
    a = np.asarray(src).astype(np.float32); d = np.sqrt(((255 - a) ** 2).sum(-1)); alpha = np.clip((d - 18) / 30, 0, 1)
    yy, xx = np.mgrid[0:size, 0:size]; rr = np.hypot(xx - size / 2, yy - size / 2) / (size / 2)
    alpha *= np.clip((0.99 - rr) / 0.015, 0, 1); a = np.clip(((a / 255) ** 1.15) * 255 * 0.9, 0, 255)
    return Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), 'RGBA')

def end_base():
    yy = np.linspace(0, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]
    g = np.exp(-((xx) ** 2 * 1.2 + (yy - 0.42) ** 2 * 6)); r = 10 + 60 * g; gg = 10 + 8 * g; b = 12 + 10 * g
    bg = Image.fromarray(np.dstack([r + 0 * xx, gg + 0 * xx, b + 0 * xx]).clip(0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(bg)
    t = text_img([('TURISMO WHEELS', WHITE)], size=84, stroke=0, w='Black', shadow=False); bg.alpha_composite(t, (int((W - t.width) / 2), 250))
    t = text_img([('CUSTOM FORGED · MADE TO ORDER', (200, 200, 205))], size=30, stroke=0, w='SemiBold', shadow=False); bg.alpha_composite(t, (int((W - t.width) / 2), 350))
    side = [cutout(f'{V2}/assety/F_C19-R_front.jpg', 380), cutout(f'{V2}/assety/F_RR_front.jpg', 380)]
    main = cutout(f'{V2}/assety/F_C01_front.jpg', 560)
    for im, cx in ((side[0], 230), (side[1], 850)):
        dim = im.copy(); dim = Image.fromarray((np.asarray(dim).astype(np.float32) * [0.8, 0.8, 0.8, 1]).astype(np.uint8), 'RGBA'); bg.alpha_composite(dim, (int(cx - 190), 620))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((W / 2 - 300, 545, W / 2 + 300, 1145), fill=(0, 0, 0, 180)); sh = sh.filter(ImageFilter.GaussianBlur(30)); bg.alpha_composite(sh)
    bg.alpha_composite(main, (int(W / 2 - 280), 530))
    for txt, cx, y in (('C19-R', 230, 1020), ('C01', W / 2, 1110), ('RR', 850, 1020)):
        t = text_img([(txt, (230, 230, 235))], size=34, stroke=0, w='Bold', shadow=False); bg.alpha_composite(t, (int(cx - t.width / 2), y))
    return bg
END = end_base()
PILL = Image.new('RGBA', (700, 110), (0, 0, 0, 0)); ImageDraw.Draw(PILL).rounded_rectangle((0, 0, 699, 109), 55, fill=RED + (255,))
t = text_img([('−15% · BLACK FRIDAY', WHITE)], size=58, stroke=0, w='Black', shadow=False); PILL.alpha_composite(t, (int((700 - t.width) / 2), int((110 - t.height) / 2)))
END_CTA = text_img([('Napisz, czym jeździsz', WHITE)], size=66, stroke=0, w='ExtraBold')
END_CONTACT = text_img([('+48 501 404 861', (225, 225, 230)), ('daniel.chmielewski@turismo-wheels.com', (190, 190, 196))], size=36, stroke=0, w='SemiBold', shadow=False)

def end_frame(ts):
    z = 1.0 + 0.03 * ts / 3.2; im = END.copy()
    if abs(z - 1) > 1e-3:
        w, h = W / z, H / z; im = im.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2), Image.BICUBIC)
    fr = np.asarray(im.convert('RGB'))
    if ts > 0.25: fr = paste(fr, PILL, W / 2, 1265, scale=pop(ts - 0.25))
    if ts > 0.55: fr = paste(fr, END_CTA, W / 2, 1395, alpha=min(1, (ts - 0.55) / 0.15))
    if ts > 0.8: fr = paste(fr, END_CONTACT, W / 2, 1505, alpha=min(1, (ts - 0.8) / 0.2))
    if ts < 0.12: fr = (fr.astype(np.float32) * (ts / 0.12)).astype(np.uint8)
    return fr

# ---------------------------------------------------------------- ekran laptopa
def screen_frames(n):
    vf = ("[0:v]trim=0.8:10.3,setpts=(PTS-STARTPTS)/2.6[a];[0:v]trim=10.3:13.2,setpts=(PTS-STARTPTS)/1.25[b];"
          f"[a][b]concat=n=2:v=1,fps={FPS},scale=1440:900[o]")
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', SCREEN, '-filter_complex', vf, '-map', '[o]', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True, check=True).stdout
    fr = np.frombuffer(p, np.uint8).reshape(-1, 900, 1440, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    out = []
    for i in range(n):
        ts = i / FPS; im = Image.fromarray(fr[i])
        bg = im.resize((int(1440 * 1920 / 900), 1920), Image.BILINEAR).crop((int((3072 - W) / 2), 0, int((3072 - W) / 2) + W, H)).filter(ImageFilter.GaussianBlur(40))
        bg = Image.fromarray((np.asarray(bg).astype(np.float32) * 0.35).astype(np.uint8))
        z = 1.0 + 0.22 * (ts / (n / FPS)) ** 1.2; w = int(W * 1.18 * z); h = int(w * 900 / 1440)
        # pod koniec dryf w lewo (na zdjęcie felgi na karcie C01)
        dx = int(-180 * max(0, (ts - 3.6) / 2.3)) ; fg = im.resize((w, h), Image.LANCZOS)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 28, fill=255)
        shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(shadow).rounded_rectangle((W / 2 - w / 2 + dx, 900 - h / 2 + 20, W / 2 + w / 2 + dx, 900 + h / 2 + 20), 28, fill=(0, 0, 0, 200))
        shadow = shadow.filter(ImageFilter.GaussianBlur(30)); base = bg.convert('RGBA'); base.alpha_composite(shadow)
        base.paste(fg, (int(W / 2 - w / 2 + dx), int(900 - h / 2)), m); out.append(np.asarray(base.convert('RGB')))
    return np.stack(out)

# ---------------------------------------------------------------- render obrazu
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-vf', 'unsharp=5:5:0.55:5:5:0,eq=contrast=1.04:saturation=0.96,vignette=angle=PI/6,noise=alls=7:allf=t',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', f'{TMP}/video.mp4'], stdin=subprocess.PIPE)
for name, src, a, b, o in SEG:
    n = round((b - a) * FPS); t0 = T[name]
    if src == 'SCREEN': frames = screen_frames(n)
    elif src == 'END': frames = None
    else: frames = decode(src, a, b, n=n)
    for i in range(n):
        ts = i / FPS
        fr = end_frame(ts) if frames is None else frames[i]
        if 'zoom' in o:
            z0, z1 = o['zoom']; fr = zoom(fr, z0 + (z1 - z0) * i / max(1, n - 1), 0.5, o.get('cy', 0.5))
        if 'whip_out' in o and i >= n - o['whip_out']: k = (i - (n - o['whip_out']) + 1) / o['whip_out']; fr = whip(fr, -k ** 2)
        if 'whip_in' in o and i < o['whip_in']: k = 1 - i / o['whip_in']; fr = whip(fr, k ** 2)
        # hook
        if name == 'H1': fr = paste(fr, HOOK1, W / 2, 760, scale=pop(ts))
        if name == 'H2': fr = paste(fr, HOOK2, W / 2, 760, scale=pop(ts))
        if name == 'H3': fr = paste(fr, BF, W / 2, 700, scale=pop(ts))
        if name == 'S10' and ts >= src2seg('S10', 2.15):
            tt = ts - src2seg('S10', 2.15); fr = paste(fr, BADGE, W / 2 - 20, 430, scale=pop(tt)); fr = paste(fr, BADGE_EN, W / 2 - 20, 600, alpha=min(1, tt / 0.15))
        for seg, c0, c1, txt in CAPS:
            if seg == name and c0 <= ts < c1:
                fr = paste(fr, CAP_IMG[txt], W / 2 - 20, 1440 if name == 'S7' else 1270, scale=pop(ts - c0, 0.08))
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
    print('ok', name, flush=True)
enc.stdin.close(); enc.wait()

# ---------------------------------------------------------------- dźwięk
SR = 48000
def load(path, t0=0, t1=None, tempo=1.0):
    args = ['ffmpeg', '-v', 'error', '-ss', f'{t0}', '-i', path] + (['-t', f'{t1 - t0}'] if t1 else []) + \
           (['-af', f'atempo={tempo}'] if tempo != 1 else []) + ['-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(args, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
N = int(TOTAL * SR) + SR
dia = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32); mus = np.zeros((N, 2), np.float32)
def put(bus, x, at, gain=1.0, fade=0.012):
    x = x * gain; f = int(fade * SR)
    if f and len(x) > 2 * f: x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(at * SR); j = min(N, i + len(x)); bus[i:j] += x[:j - i]

# natywny dźwięk ujęć (głos tymczasowy Seedance + otoczenie)
for name, src, a, b, o in SEG:
    if src in ('SCREEN', 'END') or o.get('native'): continue
    try: x = load(src, a, b)
    except Exception: continue
    g = 0.55 if name.startswith('H') else 1.0
    put(dia if name in ('S2', 'S3a', 'S3b', 'S4', 'S5', 'S10', 'S11') else amb, x, T[name], g)
# głos z offu (tymczasowy klon)
put(dia, load(f'{A}/vo06.wav'), T['S7'] + 0.05, 1.0)
put(dia, load(f'{A}/vo08.wav', tempo=1.15), T['S9'] + 0.10, 1.0)
put(dia, load(f'{A}/vo09.wav', tempo=1.10), T['S9'] + 4.66, 1.0)
put(dia, load(f'{A}/vo10.wav', tempo=1.10), T['S9'] + 7.95, 1.0)

# syntetyczne SFX
def boom(d=1.4, f0=70, f1=34):
    t = np.arange(int(d * SR)) / SR; ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * 5)) / SR
    x = np.sin(ph) * np.exp(-t * 2.6) + 0.25 * np.random.default_rng(1).normal(size=t.size) * np.exp(-t * 30)
    return np.repeat((x * 0.9)[:, None], 2, 1).astype(np.float32)
def whoosh(d=0.45):
    rng = np.random.default_rng(2); n = int(d * SR); x = rng.normal(size=n); t = np.arange(n) / n
    env = np.sin(np.pi * t) ** 2; out = np.zeros(n); y = 0.0
    for i in range(n):                                    # filtr dolnoprzepustowy z przemiataną częstotliwością
        a = 0.02 + 0.35 * env[i]; y += a * (x[i] - y); out[i] = y
    out = out / np.abs(out).max() * env * 0.8; pan = np.linspace(-0.6, 0.6, n)
    return np.stack([out * (1 - pan) / 1.6, out * (1 + pan) / 1.6], 1).astype(np.float32)
B, WH = boom(), whoosh()
for at in (T['H1'], T['H2'] + 0.0, T['H3']): put(sfx, B, at, 0.9)
put(sfx, WH, T['S2'] - 0.30, 1.0)                        # panorama szarpana
tel = load(f'{A}/sfx_teleport.mp3')
put(sfx, tel, T['S3a'] - 1.30, 0.8); put(sfx, B, T['S3a'], 0.6)   # pstryk 1 = teleport
put(sfx, tel, T['S4'] - 1.30, 0.6); put(sfx, B * 0.5, T['S4'], 0.5)  # pstryk 2 = koszulka
pp = load(f'{A}/sfx_pop.mp3', 0, 0.12)
put(sfx, pp, T['S10'] + src2seg('S10', 2.15), 0.9); put(sfx, B, T['S10'] + src2seg('S10', 2.15), 0.5)
put(sfx, B, T['S12'], 0.8); put(sfx, pp, T['S12'] + 0.25, 0.8)
put(sfx, WH, T['S9'] + 4.55, 0.7); put(sfx, WH, T['S9'] + 7.55, 0.7)   # podmiany felg

# muzyka: hook = fragment z dropu, potem intro; „stop” muzyki tuż przed wyjęciem felgi, drop przy wyjęciu
M = f'{A}/muzyka_draft.mp3'; DROP = 31.2
drop_at = T['S8'] + 1.55
put(mus, load(M, DROP, DROP + (T['S1'] - T['H1'])), T['H1'], 1.0, 0.01)
pre = drop_at - T['S1']; loop = pre - DROP              # brakujący czas przed dropem dokładamy powtórką wstępu
put(mus, load(M, 0, loop), T['S1'], 1.0, 0.02)
put(mus, load(M, 0, DROP + (T['S12'] - drop_at)), T['S1'] + loop, 1.0, 0.02)
put(mus, load(M, 60.0, 65.0), T['S12'], 1.0, 0.02)

def wav(path, x): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', path], input=x.astype(np.float32).tobytes(), check=True)
for nm, x in (('dia', dia), ('amb', amb), ('sfx', sfx), ('mus', mus)): wav(f'{TMP}/{nm}.wav', x)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/dia.wav', '-i', f'{TMP}/amb.wav', '-i', f'{TMP}/sfx.wav', '-i', f'{TMP}/mus.wav', '-filter_complex',
                '[0:a]highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,asplit[d][key];'
                '[3:a]volume=0.55[m];[m][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[md];'
                '[d][1:a][2:a][md]amix=inputs=4:normalize=0:weights=1 0.8 0.9 1,loudnorm=I=-14:TP=-1.0:LRA=9[o]',
                '-map', '[o]', '-ar', '48000', f'{TMP}/mix.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{TMP}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT], check=True)
print('gotowe', OUT, round(TOTAL, 2), 's')

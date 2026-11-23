"""Pokaz gamy C01 -> C19-R -> RR: obrót z rozmyciem ruchu (migawka 180°), podmiana w szczycie obrotów. 1080x1920, 24 kl./s."""
import sys, os, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
assets, out, tmp = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(tmp, exist_ok=True)
W, H, FPS = 1080, 1920, 24; DUR = float(os.environ.get("GAMA_DUR", "7.0"))
F = '/usr/share/fonts/opentype/inter/'
def font(s, w='SemiBold'): return ImageFont.truetype(F + f'Inter-{w}.otf', s)
def cutout(path, size):
    src = Image.open(path).convert('RGB'); g = np.asarray(src.convert('L')).astype(np.float32)
    cols = np.nonzero((g < 235).sum(0) > 3)[0]; rows = np.nonzero((g < 235).sum(1) > 3)[0]
    x0, x1 = cols[0], cols[-1]; r = (x1 - x0) / 2; cxs = (x0 + x1) / 2; cys = rows[0] + r     # obręcz: szerokość = średnica, góra = górny rant
    pad = r * 1.01; src = src.crop((int(cxs - pad), int(cys - pad), int(cxs + pad), int(cys + pad))).resize((size, size), Image.LANCZOS)
    a = np.asarray(src).astype(np.float32)
    d = np.sqrt(((255 - a) ** 2).sum(-1)); alpha = np.clip((d - 18) / 30, 0, 1)
    yy, xx = np.mgrid[0:size, 0:size]; rr = np.hypot(xx - size / 2, yy - size / 2) / (size / 2)
    alpha *= np.clip((0.99 - rr) / 0.015, 0, 1)                     # maska dokładnie na obręczy
    a = np.clip(((a / 255) ** 1.15) * 255 * 0.9, 0, 255)
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8); return Image.fromarray(rgba, 'RGBA')
D = 820
wheels = [cutout(f'{assets}/F_C01_front.jpg', D), cutout(f'{assets}/F_C19-R_front.jpg', D), cutout(f'{assets}/F_RR_front.jpg', D)]
cm = Image.new('L', (D, D), 0); ImageDraw.Draw(cm).ellipse((D/2 - 0.205*D, D/2 - 0.205*D, D/2 + 0.205*D, D/2 + 0.205*D), fill=255)
CAP = wheels[2].copy(); ca = np.asarray(CAP).copy(); ca[..., 3] = (ca[..., 3].astype(np.float32) * (np.asarray(cm.filter(ImageFilter.GaussianBlur(3))) / 255)).astype(np.uint8); CAP = Image.fromarray(ca, 'RGBA')
labels = [('TURISMO FORGED C01', 'Deep concave', 'Nasz bestseller · frezowane detale'),
          ('TURISMO FORGED C19-R', 'Zintegrowany aero-ring', 'Integrated aero-ring'),
          ('TURISMO FORGED RR', 'Gravity cap', 'Klasyka · minimalizm')]
SW = [float(x) for x in os.environ.get("GAMA_SW", "2.3,4.6").split(",")]                     # momenty podmiany (s)
def omega(t):                          # obr./s
    w = 0.45
    for s in SW: w += 3.2 * math.exp(-((t - s) / 0.28) ** 2)
    return w
# tło: ciemny gradient + delikatna poświata za felgą + odbicie podłogi
bg = Image.new('RGB', (W, H), (10, 10, 12)); g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((W/2-620, 380, W/2+620, 1620), fill=70)
g = g.filter(ImageFilter.GaussianBlur(160)); bg = Image.composite(Image.new('RGB', (W, H), (46, 46, 52)), bg, g)
ImageDraw.Draw(bg).rectangle((0, 1560, W, H), fill=(14, 14, 16)); ImageDraw.Draw(bg).line((0, 1560, W, 1560), fill=(200, 30, 45), width=3)
cx, cy = W // 2, 1010
ang, N = 0.0, int(DUR * FPS)
for f in range(N):
    t = f / FPS; w = omega(t); idx = 0 if t < SW[0] else (1 if t < SW[1] else 2)
    shutter = 0.5 * w * 360 / FPS                      # stopnie obrotu w czasie otwarcia migawki
    n = max(1, min(24, int(shutter / 2.5) + 1))
    acc = np.zeros((D, D, 4), np.float32)
    for k in range(n):
        a = ang + shutter * (k / max(1, n - 1) - 0.5) if n > 1 else ang
        acc += np.asarray(wheels[idx].rotate(-a, resample=Image.BICUBIC)).astype(np.float32)
    wl = Image.fromarray((acc / n).astype(np.uint8), 'RGBA')
    if idx == 2:                                                    # RR: gravity cap stoi nieruchomo
        wl.paste(CAP, (0, 0), CAP)
    fr = bg.copy(); fr.paste(wl, (cx - D // 2, cy - D // 2), wl)
    refl = wl.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, D, 260)); ra = np.asarray(refl).astype(np.float32); ra[..., 3] *= np.linspace(0.22, 0, 260)[:, None]
    refl = Image.fromarray(ra.astype(np.uint8), 'RGBA'); fr.paste(refl, (cx - D // 2, 1565), refl)
    d = ImageDraw.Draw(fr); k1, h1, s1 = labels[idx]
    seg_start = [0, SW[0], SW[1]][idx]; vis = min(1, max(0, (t - seg_start - 0.35) / 0.25))
    if vis > 0:
        y0 = 250; col = lambda c: tuple(int(v * vis) for v in c)
        d.text((80, y0), k1, fill=col((220, 30, 45)), font=font(30, 'Bold'))
        d.text((80, y0 + 50), h1, fill=col((245, 245, 245)), font=font(74, 'Bold'))
        d.text((80, y0 + 145), s1, fill=col((160, 160, 168)), font=font(34, 'Regular'))
    fr.save(f'{tmp}/r{f:04d}.jpg', quality=92)
    ang += w * 360 / FPS
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{tmp}/r%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', out], check=True)
print('ok', N)

"""Przejście na pstryk: logo GT z koszulki -> odłamki -> logo Turismo Wheels -> lot w kamerę, przez logo widać następną scenę.
Wejście: klatka „przed” (pstryk), klatka „po” (pierwsza klatka nowej sceny), pozycja logo GT na koszulce.
Wyjście: klatki PNG 1080x1920 + podgląd mp4. 24 kl./s.
Użycie: python3 logo_morph.py PRZED.png PO.png GT_LOGO.jpg TW_SYGNET.png TW_WORDMARK.png OUT_DIR [cx cy w]"""
import sys, os, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy.spatial import Delaunay

W, H, FPS = 1080, 1920, 24
RED = np.array([237, 59, 34], np.float32); WHITE = np.array([255, 255, 255], np.float32)
before_p, after_p, gt_p, sg_p, wm_p, out = sys.argv[1:7]
cx0, cy0, w0 = (float(v) for v in (sys.argv[7:10] if len(sys.argv) >= 10 else (540, 820, 260)))
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(7)

def cover(p):
    im = Image.open(p).convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((l, t, l + W, t + H))).astype(np.float32)
BEFORE, AFTER = cover(before_p), cover(after_p)

# --- maski logo (alpha 0..1), przycięte do kształtu
gt = ImageOps.invert(Image.open(gt_p).convert('L'))                # czarne logo na białym -> maska
ga = np.asarray(gt).astype(np.float32) / 255
# sam znak GT (bez napisu „GRAN TURISMO 7”): górne 78% wysokości oficjalnego logo
gt = gt.crop((0, 0, gt.width, int(gt.height * 0.78))); gt = gt.point(lambda v: 255 if v > 128 else 0); gt = gt.crop(gt.getbbox())
sg = Image.open(sg_p).convert('RGBA'); wm = Image.open(wm_p).convert('RGBA')

def sample_tris(mask_img, size_w, center, n_pts=900):
    """Triangulacja wnętrza maski; zwraca trójkąty (N,3,2) w pikselach kadru."""
    m = mask_img.convert('L'); s = size_w / m.width; m = m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS)
    a = np.asarray(m) > 128; ys, xs = np.nonzero(a)
    idx = rng.choice(len(xs), min(n_pts, len(xs)), replace=False)
    pts = np.c_[xs[idx], ys[idx]].astype(np.float32)
    # dołóż punkty krawędzi, żeby trójkąty trzymały kształt
    edge = a & ~np.asarray(Image.fromarray(a.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3))).astype(bool)
    ey, ex = np.nonzero(edge); j = rng.choice(len(ex), min(n_pts, len(ex)), replace=False)
    pts = np.r_[pts, np.c_[ex[j], ey[j]]]
    tri = Delaunay(pts); T = pts[tri.simplices]
    c = T.mean(1).astype(int); keep = a[np.clip(c[:, 1], 0, a.shape[0] - 1), np.clip(c[:, 0], 0, a.shape[1] - 1)]
    T = T[keep]
    T[:, :, 0] += center[0] - m.width / 2; T[:, :, 1] += center[1] - m.height / 2
    return T, m.size

SG_W = 640; SG_C = (W / 2, H * 0.44)
Tsrc_small, _ = sample_tris(gt, w0, (cx0, cy0), 260)
Tdst, sg_size = sample_tris(sg, SG_W, SG_C, 260)
# wyrównaj liczbę trójkątów i sparuj po kącie wokół środka (płynniejszy przelot)
n = max(len(Tsrc_small), len(Tdst))
def pad(T): return T[rng.choice(len(T), n, replace=True)] if len(T) < n else T[:n]
def order(T, c): a = np.arctan2(T.mean(1)[:, 1] - c[1], T.mean(1)[:, 0] - c[0]); r = np.hypot(*(T.mean(1) - c).T); return np.lexsort((r, np.round(a * 6)))
Ts = pad(Tsrc_small); Td = pad(Tdst)
Ts = Ts[order(Ts, (cx0, cy0))]; Td = Td[order(Td, SG_C)]

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_in(x): x = min(max(x, 0), 1); return x ** 3

# losowe rozrzuty i obroty dla fazy wybuchu
cen = Ts.mean(1); dirv = cen - np.array([cx0, cy0]); dirv /= (np.linalg.norm(dirv, axis=1, keepdims=True) + 1e-6)
burst = dirv * rng.uniform(140, 420, (n, 1)) + rng.normal(0, 70, (n, 2))
rot = rng.uniform(-3.5, 3.5, n)

def rot_tri(T, ang):
    c = T.mean(1, keepdims=True); ca, sa = np.cos(ang)[:, None], np.sin(ang)[:, None]
    d = T - c; return c + np.stack([d[..., 0] * ca - d[..., 1] * sa, d[..., 0] * sa + d[..., 1] * ca], -1)

def draw_tris(T, cols, ss=2):
    im = Image.new('RGBA', (W * ss, H * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for t, c in zip(T, cols):
        d.polygon([tuple(p * ss) for p in t], fill=tuple(int(v) for v in c) + (255,))
    return np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255

def logo_layer(scale=1.0, center=SG_C, wm_alpha=1.0, wm_dx=0.0):
    """Ostre logo TW (sygnet + napis) jako RGBA float."""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s = Image.open(sg_p).convert('RGBA'); k = SG_W * scale / s.width; s = s.resize((max(1, round(s.width * k)), max(1, round(s.height * k))), Image.LANCZOS)
    L.alpha_composite(s, (round(center[0] - s.width / 2), round(center[1] - s.height / 2))) if -s.width < center[0] < W + s.width else None
    if wm_alpha > 0:
        w = Image.open(wm_p).convert('RGBA'); kw = 760 * scale / w.width; w = w.resize((max(1, round(w.width * kw)), max(1, round(w.height * kw))), Image.LANCZOS)
        a = np.asarray(w).copy(); a[..., 3] = (a[..., 3] * wm_alpha).astype(np.uint8); w = Image.fromarray(a)
        L.alpha_composite(w, (round(center[0] - w.width / 2 + wm_dx), round(center[1] + SG_W * scale * 0.52)))
    return np.asarray(L).astype(np.float32) / 255

def over(base, rgba):
    a = rgba[..., 3:4]; return base * (1 - a) + rgba[..., :3] * 255 * a

frames = []
# 0-1: zamrożenie + negatyw
frames += [255 - BEFORE, BEFORE * 0.6 + 255 * 0.4]
# 2-9: logo GT wyrywa się z koszulki i leci do środka; tło gaśnie
N_LIFT, N_BURST, N_FORM, N_HOLD, N_ZOOM = 7, 6, 8, 8, 9
gt_cols = np.tile(WHITE, (n, 1))
for i in range(N_LIFT):
    t = ease((i + 1) / N_LIFT); sc = 1 + t * 1.6
    c_now = np.array([cx0, cy0]) * (1 - t) + np.array(SG_C) * t
    T = (Ts - np.array([cx0, cy0])) * sc + c_now
    bg = BEFORE * (1 - 0.85 * t)
    lay = draw_tris(T, gt_cols)
    glow = np.asarray(Image.fromarray((lay[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32)[..., None] / 255
    frames.append(np.clip(over(bg, lay) + glow * 60 * t, 0, 255))
Ts_big = (Ts - np.array([cx0, cy0])) * 2.6 + np.array(SG_C)
# 10-18: wybuch w odłamki, kolor biel -> czerwień, rozmycie ruchu (4 podklatki)
prev = Ts_big
for i in range(N_BURST):
    acc = np.zeros((H, W, 4), np.float32)
    for sub in range(4):
        t = (i + sub / 4 + 1) / N_BURST; e = ease_out(t)
        T = rot_tri(Ts_big + burst[:, None, :] * e, rot * e)
        cols = WHITE * (1 - e) + RED * e
        acc += draw_tris(T, np.tile(cols, (n, 1)), ss=1)
    lay = acc / 4; bg = BEFORE * 0.15 * (1 - (i + 1) / N_BURST)
    g = np.asarray(Image.fromarray((lay[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
    lay = lay.copy(); lay[..., :3] = np.clip(lay[..., :3] + 0, 0, 1)
    bg = bg + g * RED * 0.55
    frames.append(over(bg, lay))
# 19-27: odłamki lecą w kształt sygnetu TW
Tb = rot_tri(Ts_big + burst[:, None, :], rot)
for i in range(N_FORM):
    acc = np.zeros((H, W, 4), np.float32)
    for sub in range(4):
        t = ease_in(min(1, (i + sub / 4 + 1) / N_FORM)) if i < N_FORM - 2 else ease((i + sub / 4 + 1) / N_FORM)
        T = Tb * (1 - t) + Td * t
        T = rot_tri(T, rot * 0)  # obrót wygasa przez interpolację wierzchołków
        acc += draw_tris(T, np.tile(RED * (1 - t) + WHITE * t, (n, 1)), ss=1)
    lay = acc / 4
    g = np.asarray(Image.fromarray((lay[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
    frames.append(over(g * RED * 0.5, lay))
# 28-33: ostre logo, błysk na krawędziach, napis wsuwa się
for i in range(N_HOLD):
    t = (i + 1) / N_HOLD
    L = logo_layer(1.0, SG_C, wm_alpha=ease(t * 1.5), wm_dx=(1 - ease(t)) * 60)
    f = over(np.zeros_like(BEFORE), L)
    if i < 2: f = np.clip(f * (1.6 - 0.3 * i), 0, 255)
    frames.append(f)
# 34-43: lot w kamerę: wnętrze logo odsłania nową scenę, całe logo rośnie aż wypełni kadr
focus = np.array([SG_C[0] - SG_W * 0.06, SG_C[1] - SG_W * 0.02])   # pełny fragment belki „T”
for i in range(N_ZOOM):
    t = ease_in((i + 1) / N_ZOOM); sc = 1 + t * 26
    c = np.array(SG_C) + (np.array(SG_C) - focus) * (sc - 1)
    L = logo_layer(sc, tuple(c), wm_alpha=max(0, 1 - t * 3))
    a = L[..., 3:4]
    zoom_after = AFTER  # scena „po” lekko dojeżdża
    f = np.zeros_like(BEFORE) * (1 - a) + zoom_after * a
    if i == N_ZOOM - 1: f = AFTER
    frames.append(f)
frames += [AFTER] * 2

for k, f in enumerate(frames):
    Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).save(f'{out}/m{k:03d}.png')
os.system(f"ffmpeg -v error -y -framerate {FPS} -i {out}/m%03d.png -c:v libx264 -crf 16 -pix_fmt yuv420p {out}/logo_morph_preview.mp4")
print('klatek', len(frames), 'czas', round(len(frames) / FPS, 2), 's')

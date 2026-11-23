"""v3: wstawki renderowane w kodzie (0 kr): przeglądarka z wpisywaniem adresu, nawigacja po stronie, kafelek C01,
oznaczenia cech C01, aero-ring C19-R, obrót RR z nieruchomym gravity cap, plansza końcowa.
Użycie: python3 v3_inserts.py <katalog v3> <katalog v2>"""
import sys, os, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V3, V2 = sys.argv[1], sys.argv[2]
OUT = f'{V3}/montaz/projekt/broll'; os.makedirs(OUT, exist_ok=True)
FPS = 24; RED = (237, 59, 34); NEAR = (22, 18, 22)
FD = '/usr/share/fonts/opentype/inter/'
def font(s, w='SemiBold'): return ImageFont.truetype(FD + f'Inter-{w}.otf', s)
SITE = f'{V3}/site'
ONLY = os.environ.get('ONLY', '').split(',')
def want(n): return not ONLY[0] or n in ONLY

def encode(frames_iter, out, w, h):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = 0
    for fr in frames_iter: p.stdin.write(np.ascontiguousarray(fr).tobytes()); n += 1
    p.stdin.close(); p.wait(); print('ok', os.path.basename(out), n, 'klatek')

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def video_frames(src, t0, t1, speed=1.0, size=(1440, 900)):
    n = int(round((t1 - t0) / speed * FPS))
    vf = f"trim={t0}:{t1},setpts=(PTS-STARTPTS)/{speed},fps={FPS},scale={size[0]}:{size[1]}"
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0], 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr[:n]

# ---------- okno przeglądarki (jasny motyw jak Chrome) ----------
BAR = 92
def browser(page_img, url, w=1440, typed=None, caret=False, load=1.0):
    """page_img: PIL RGB 1440x900 strony; zwraca okno (w x 900+BAR)."""
    win = Image.new('RGB', (w, 900 + BAR), (255, 255, 255)); d = ImageDraw.Draw(win)
    d.rectangle((0, 0, w, BAR), fill=(222, 225, 230))
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]): d.ellipse((22 + i * 30, 18, 38 + i * 30, 34), fill=c)
    d.rounded_rectangle((140, 10, 420, 44), 10, fill=(255, 255, 255)); d.text((160, 17), 'Turismo Wheels', font=font(20, 'Medium'), fill=(40, 40, 40))
    d.rounded_rectangle((20, 52, w - 20, 86), 17, fill=(255, 255, 255))
    txt = url if typed is None else typed
    d.text((56, 57), txt, font=font(22, 'Medium'), fill=(30, 30, 30))
    if caret:
        tw = d.textlength(txt, font=font(22, 'Medium')); d.rectangle((58 + tw, 58, 60 + tw, 82), fill=(30, 30, 30))
    d.text((30, 56), '⌕' if typed is not None else '🔒', font=font(20), fill=(90, 90, 90))
    if page_img is not None:
        pg = page_img
        if load < 1.0:   # pasek ładowania
            d.rectangle((0, BAR - 4, int(w * load), BAR), fill=(66, 133, 244))
        win.paste(pg, (0, BAR))
    return win

def place_on(bg_rgb, win, cx, cy, scale, radius=26, shadow=True):
    """Wkleja okno ze skalą i cieniem na tło 1080 szer."""
    W_, H_ = bg_rgb.size; ww, wh = int(win.width * scale), int(win.height * scale)
    win = win.resize((ww, wh), Image.LANCZOS)
    m = Image.new('L', (ww, wh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, ww - 1, wh - 1), radius, fill=255)
    base = bg_rgb.convert('RGBA')
    if shadow:
        sh = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((cx - ww / 2, cy - wh / 2 + 24, cx + ww / 2, cy + wh / 2 + 24), radius, fill=(0, 0, 0, 170))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
    base.paste(win, (int(cx - ww / 2), int(cy - wh / 2)), m)
    return base.convert('RGB')

def dark_bg(src_rgb, W_, H_, k=0.30, blur=36):
    s = max(W_ / src_rgb.width, H_ / src_rgb.height)
    b = src_rgb.resize((int(src_rgb.width * s) + 1, int(src_rgb.height * s) + 1), Image.BILINEAR)
    b = b.crop(((b.width - W_) // 2, (b.height - H_) // 2, (b.width - W_) // 2 + W_, (b.height - H_) // 2 + H_)).filter(ImageFilter.GaussianBlur(blur))
    return Image.fromarray((np.asarray(b).astype(np.float32) * k).astype(np.uint8))

_cache = {}
def sframe(t):
    """Pojedyncza klatka nagrania strony (dekodowana na żądanie, bez ładowania całego wideo do pamięci)."""
    k = round(t * FPS) / FPS
    if k not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{k:.3f}', '-i', f'{SITE}/site_c01.webm', '-frames:v', '1', '-vf', 'scale=1440:900',
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        _cache[k] = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(900, 1440, 3))
    return _cache[k]

# 1) przeglądarka: wpisywanie adresu (do układu split: 1080x960), 4.6 s
def gen_type():
    W_, H_ = 1080, 960; url = 'turismo-wheels.com'; home = sframe(14.0); n = int(4.6 * FPS)
    for i in range(n):
        t = i / FPS
        k = int(min(len(url), max(0, (t - 0.5) / 2.0 * len(url))))
        if t < 3.0: win = browser(Image.new('RGB', (1440, 900), (246, 246, 246)), url, typed=url[:k], caret=(int(t * 3) % 2 == 0) or k < len(url))
        else:
            load = min(1, (t - 3.0) / 0.6); pg = home if t > 3.35 else Image.new('RGB', (1440, 900), (246, 246, 246))
            win = browser(pg, 'turismo-wheels.com', load=load)
        zin = 1.0 - ease((t - 2.9) / 0.7)                 # 1 = najazd na pasek adresu, 0 = całe okno
        sc = 0.70 * (1 + 1.25 * zin); win_h = (900 + BAR) * sc
        cx = W_ / 2 + (1440 * sc / 2 - 380) * zin          # lewa część paska w kadrze
        cy = H_ / 2 + (win_h / 2 - 140) * zin              # pasek adresu przy górze kadru
        bg = dark_bg(home, W_, H_)
        yield np.asarray(place_on(bg, win, cx, cy, sc))
if want('type'): encode(gen_type(), f'{OUT}/i_browser_type.mp4', 1080, 960)

# 2) nawigacja: strona główna → menu „Felgi aluminiowe” → „Kute felgi … na zamówienie” → lista (pełny kadr), 4.1 s
def gen_nav():
    W_, H_ = 1080, 1920
    seq = [(14.0, 24.5, 4.2), (25.5, 33.0, 4.0)]   # (od, do, przyspieszenie)
    frames = []
    for a, b, sp in seq:
        for k in range(int((b - a) / sp * FPS)): frames.append(a + k * sp / FPS)
    frames = frames[:int(4.1 * FPS)]
    for i, ts in enumerate(frames):
        pg = sframe(ts); win = browser(pg, 'turismo-wheels.com/felgi' if ts > 25 else 'turismo-wheels.com')
        t = i / FPS; z = 1.0 + 0.35 * ease(t / 4.1)
        bg = dark_bg(pg, W_, H_)
        # najazd na lewą-górną część (menu)
        yield np.asarray(place_on(bg, win, W_ / 2 + 120 * ease(t / 4.1), H_ / 2 + 60 * ease(t / 4.1), 0.74 * z))
if want('nav'): encode(gen_nav(), f'{OUT}/i_site_nav.mp4', 1080, 1920)

# 3) lista modeli (przewijanie + najazd na C01), 1.8 s, pełny kadr
def gen_list():
    W_, H_ = 1080, 1920; n = int(1.8 * FPS)
    for i in range(n):
        t = i / FPS; ts = 54.0 + t * 6.5
        pg = sframe(ts); win = browser(pg, 'turismo-wheels.com/pc/felgi-aluminiowe-kute')
        z = 1.05 + 0.5 * ease(t / 1.8)
        yield np.asarray(place_on(dark_bg(pg, W_, H_), win, W_ / 2 - 40 * ease(t / 1.8), H_ / 2 + 120 * ease(t / 1.8), 0.74 * z))
if want('list'): encode(gen_list(), f'{OUT}/i_site_list.mp4', 1080, 1920)

# ---------- packshoty FRONT (wycięte) ----------
def cutout(path, size):
    src = Image.open(path).convert('RGB'); g = np.asarray(src.convert('L')).astype(np.float32)
    cols = np.nonzero((g < 235).sum(0) > 3)[0]; rows = np.nonzero((g < 235).sum(1) > 3)[0]
    x0, x1 = cols[0], cols[-1]; r = (x1 - x0) / 2; cxs = (x0 + x1) / 2; cys = rows[0] + r
    pad = r * 1.01; src = src.crop((int(cxs - pad), int(cys - pad), int(cxs + pad), int(cys + pad))).resize((size, size), Image.LANCZOS)
    a = np.asarray(src).astype(np.float32); d = np.sqrt(((255 - a) ** 2).sum(-1)); alpha = np.clip((d - 18) / 30, 0, 1)
    yy, xx = np.mgrid[0:size, 0:size]; rr = np.hypot(xx - size / 2, yy - size / 2) / (size / 2)
    alpha *= np.clip((0.99 - rr) / 0.015, 0, 1); a = np.clip(((a / 255) ** 1.1) * 255 * 0.95, 0, 255)
    return Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), 'RGBA')
FRONT = {k: cutout(f'{V2}/assety/F_{k}_front.jpg', 1400) for k in ('C01', 'C19-R', 'RR')}

def studio_bg(W_, H_):
    yy = np.linspace(0, 1, H_)[:, None]; xx = np.linspace(-1, 1, W_)[None, :]
    g = np.exp(-(xx ** 2 * 1.3 + (yy - 0.45) ** 2 * 5)); v = 12 + 38 * g
    return Image.fromarray(np.dstack([v + 6 * g, v, v + 2]).clip(0, 255).astype(np.uint8))

def wheel_layer(img, scale, cx, cy, W_, H_, rot=0.0):
    w = img if rot == 0 else img.rotate(rot, resample=Image.BICUBIC)
    s = int(img.width * scale); w = w.resize((s, s), Image.LANCZOS)
    L = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); L.alpha_composite(w, (int(cx - s / 2), int(cy - s / 2))); return L

def draw_arc(img, cx, cy, r, frac, width=9, color=RED, start=-90):
    d = ImageDraw.Draw(img)
    if frac > 0: d.arc((cx - r, cy - r, cx + r, cy + r), start, start + 360 * frac, fill=color, width=width)

# 4) kafelek C01 (split 1080x960): rozmyta lista + karta wyskakuje po kliknięciu, 1.9 s
def gen_tile():
    W_, H_ = 1080, 960; n = int(1.9 * FPS); bg0 = dark_bg(sframe(66.0), W_, H_, 0.45, 22)
    card_w, card_h = 620, 760
    for i in range(n):
        t = i / FPS; s = ease_out(t / 0.28) * (1 + 0.06 * math.sin(min(1, t / 0.28) * math.pi))
        base = bg0.convert('RGBA')
        card = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, card_w - 1, card_h - 1), 34, fill=(250, 250, 250, 255))
        wl = FRONT['C01'].resize((520, 520), Image.LANCZOS).rotate(-30 * t, resample=Image.BICUBIC)
        card.alpha_composite(wl, (50, 40))
        d.text((card_w / 2, 600), 'TURISMO FORGED C01', font=font(40, 'Bold'), fill=(20, 20, 20), anchor='mm')
        d.rounded_rectangle((card_w / 2 - 150, 650, card_w / 2 + 150, 706), 28, fill=RED)
        d.text((card_w / 2, 678), 'BESTSELLER', font=font(30, 'Bold'), fill=(255, 255, 255), anchor='mm')
        if s > 0.02:
            cw, ch = int(card_w * s * 0.92), int(card_h * s * 0.92)
            c2 = card.resize((max(1, cw), max(1, ch)), Image.LANCZOS)
            sh = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((W_ / 2 - cw / 2, H_ / 2 - ch / 2 + 26, W_ / 2 + cw / 2, H_ / 2 + ch / 2 + 26), 34, fill=(0, 0, 0, 150))
            base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26))); base.alpha_composite(c2, (int(W_ / 2 - cw / 2), int(H_ / 2 - ch / 2)))
        yield np.asarray(base.convert('RGB'))
if want('tile'): encode(gen_tile(), f'{OUT}/i_tile_C01.mp4', 1080, 960)

# 5) cechy C01: deep concave (okrąg), linie (ślad wzdłuż ramienia), frezowane detale (makro), 3.6 s
def gen_c01_features():
    W_, H_ = 1080, 1920; n = int(3.6 * FPS); bg = studio_bg(W_, H_)
    for i in range(n):
        t = i / FPS
        if t < 1.0:   zc, cx, cy = 0.62 + 0.10 * ease(t), W_ / 2, H_ * 0.45
        elif t < 2.2: zc, cx, cy = 0.72 + 0.25 * ease(t - 1.0), W_ / 2 - 120 * ease(t - 1.0), H_ * 0.45 + 60 * ease(t - 1.0)
        else:         zc, cx, cy = 0.97 + 0.55 * ease((t - 2.2) / 1.4), W_ / 2 - 120 - 160 * ease((t - 2.2) / 1.4), H_ * 0.45 + 60 + 180 * ease((t - 2.2) / 1.4)
        base = bg.convert('RGBA'); base.alpha_composite(wheel_layer(FRONT['C01'], zc, cx, cy, W_, H_, rot=-4 * t))
        R = 1400 * zc / 2
        if t < 1.25: draw_arc(base, cx, cy, R * 0.42, ease((t - 0.15) / 0.55))            # wklęsłość piasty
        if 0.95 < t < 2.4:                                                                    # linia wzdłuż ramienia
            p = ease((t - 1.05) / 0.6); x0, y0 = cx + R * 0.10, cy - R * 0.12; x1, y1 = cx + R * 0.78, cy - R * 0.55
            ImageDraw.Draw(base).line((x0, y0, x0 + (x1 - x0) * p, y0 + (y1 - y0) * p), fill=RED, width=9)
        if t > 2.3:                                                                           # ramka makro na frezowaniu
            p = ease((t - 2.35) / 0.4); d = ImageDraw.Draw(base); bx, by, bw = W_ * 0.52, H_ * 0.40, 300 * p
            d.rectangle((bx - bw / 2, by - bw / 2, bx + bw / 2, by + bw / 2), outline=RED, width=7)
        yield np.asarray(base.convert('RGB'))
if want('cechy'): encode(gen_c01_features(), f'{OUT}/i_C01_cechy.mp4', 1080, 1920)

# 6) C19-R: karta produktu (1.4 s) → packshot z rysowanym aero-ringiem (3.0 s)
def gen_c19r():
    W_, H_ = 1080, 1920
    bg = studio_bg(W_, H_)
    for i in range(int(4.4 * FPS)):
        t = i / FPS - 1.3; zc = 0.58 + 0.16 * ease((t + 1.3) / 4.4)
        base = bg.convert('RGBA'); base.alpha_composite(wheel_layer(FRONT['C19-R'], zc, W_ / 2, H_ * 0.45, W_, H_, rot=-6 * t))
        R = 1400 * zc / 2
        draw_arc(base, W_ / 2, H_ * 0.45, R * 0.80, ease((t - 0.35) / 0.8), width=10)
        draw_arc(base, W_ / 2, H_ * 0.45, R * 0.70, ease((t - 0.55) / 0.8), width=4, color=(255, 255, 255))
        yield np.asarray(base.convert('RGB'))
if want('c19r'): encode(gen_c19r(), f'{OUT}/i_C19R.mp4', 1080, 1920)

# 7) RR: felga się kręci, dekiel gravity cap stoi, 3.2 s (rozmycie ruchu 180°)
def gen_rr():
    W_, H_ = 1080, 1920; bg = studio_bg(W_, H_); img = FRONT['RR']; S = img.width
    cm = Image.new('L', (S, S), 0); ImageDraw.Draw(cm).ellipse((S / 2 - 0.205 * S, S / 2 - 0.205 * S, S / 2 + 0.205 * S, S / 2 + 0.205 * S), fill=255)
    cap = img.copy(); ca = np.asarray(cap).copy(); ca[..., 3] = (ca[..., 3].astype(np.float32) * (np.asarray(cm.filter(ImageFilter.GaussianBlur(3))) / 255)).astype(np.uint8); cap = Image.fromarray(ca, 'RGBA')
    ang = 0.0
    for i in range(int(3.2 * FPS)):
        t = i / FPS; om = 0.15 + 1.6 * ease(t / 1.2) - 0.9 * ease((t - 2.2) / 1.0)
        acc = np.zeros((H_, W_, 4), np.float32); zc = 0.62 + 0.06 * ease(t / 3.2)
        for k in range(4):
            a = ang + om * 360 / FPS * (k / 4) * 0.5
            acc += np.asarray(wheel_layer(img, zc, W_ / 2, H_ * 0.45, W_, H_, rot=-a)).astype(np.float32)
        ang += om * 360 / FPS
        L = Image.fromarray((acc / 4).astype(np.uint8), 'RGBA'); base = bg.convert('RGBA'); base.alpha_composite(L)
        base.alpha_composite(wheel_layer(cap, zc, W_ / 2, H_ * 0.45, W_, H_))
        if t > 1.4: draw_arc(base, W_ / 2, H_ * 0.45, 1400 * zc / 2 * 0.23, ease((t - 1.5) / 0.5), width=8)
        yield np.asarray(base.convert('RGB'))
if want('rr'): encode(gen_rr(), f'{OUT}/i_RR_gravity.mp4', 1080, 1920)

# 8) plansza końcowa 2.6 s (bez Black Friday)
def gen_end():
    W_, H_ = 1080, 1920; bg = studio_bg(W_, H_).convert('RGBA')
    logo = Image.open(f'{V3}/assety/logo/tw_logo_white_2000.png').convert('RGBA'); lw = 760; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    for i in range(int(2.6 * FPS)):
        t = i / FPS; base = bg.copy()
        for k, (key, x, sz) in enumerate((('C19-R', 250, 420), ('RR', 830, 420), ('C01', 540, 600))):
            p = ease_out((t - 0.05 * k) / 0.45); s = sz / 1400 * (0.9 + 0.1 * p)
            L = wheel_layer(FRONT[key], s, x, 900 + (1 - p) * 60, W_, H_, rot=-12 * t * (1 if key != 'RR' else 0))
            a = np.asarray(L).copy(); a[..., 3] = (a[..., 3] * min(1, p) * (0.75 if key != 'C01' else 1)).astype(np.uint8); base.alpha_composite(Image.fromarray(a))
        pl = ease_out((t - 0.15) / 0.4); lg = logo.copy(); la = np.asarray(lg).copy(); la[..., 3] = (la[..., 3] * pl).astype(np.uint8)
        base.alpha_composite(Image.fromarray(la), (int(W_ / 2 - lw / 2), int(420 - lg.height / 2 + (1 - pl) * 30)))
        d = ImageDraw.Draw(base)
        if t > 0.5:
            a = min(1, (t - 0.5) / 0.3)
            d.text((W_ / 2, 1290), 'turismo-wheels.com', font=font(40, 'Medium'), fill=(230, 230, 230, int(255 * a)), anchor='mm')
        if t > 0.75:
            a = min(1, (t - 0.75) / 0.3)
            d.text((W_ / 2, 1380), '+48 501 404 861', font=font(52, 'Bold'), fill=(255, 255, 255, int(255 * a)), anchor='mm')
            d.text((W_ / 2, 1448), 'daniel.chmielewski@turismo-wheels.com', font=font(34, 'Medium'), fill=(200, 200, 205, int(255 * a)), anchor='mm')
        yield np.asarray(base.convert('RGB'))
if want('end'): encode(gen_end(), f'{OUT}/i_plansza.mp4', 1080, 1920)

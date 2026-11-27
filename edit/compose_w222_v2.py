"""Turismo C26 x Mercedes-Benz S 560 (W222) - montaz v2 (9:16, 1080x1920, 24 fps, bez lektora).

Kolejnosc wg uwag klienta: najpierw CALE ujecie z rigu (prowadnica v2 / Seedance) bez hooka, potem "magia montazu"
w jezyku rolki referencyjnej Turismo INVENTA (ciemne tlo z czerwona poswiata i pylem, czerwony kicker "| ...",
naglowek w szeryfie z czerwonym akcentem + podpis EN, wyskakujace kafelki z prawdziwymi zdjeciami, licznik, badge,
karuzela, glitch RGB i smugi swiatla) oraz zimowy final: biale logo, czapka Mikolaja spada na znak T, snieg.

  R   0.00-12.46  rig shot w calosci (klatki 1-299), drop muzyki przy ruszeniu 5.6 s
  R'  12.46-12.71 rampa 2x (klatki 300-311 z rozmyciem ruchu), push w piaste, aberracja RGB -> glitch
  B   12.83-14.42 klatka z rigu kurczy sie do kafelka, przechyla w 3D; licznik 0 -> 40 szprych
  C   14.42-16.42 siatka 2x2 prawdziwych zdjec wyskakuje kafelek po kafelku; kafelek _07 rozwija sie na caly ekran
  D   16.42-17.92 zdjecie _07 na pelnym ekranie, smuga swiatla, tytul wykonczenia -> glitch
  E   17.92-19.58 karta felgi w 3D, czerwony badge odlicza 18" -> 22", pigulki 10.5J / 40 szprych
  F   19.58-21.75 karuzela realizacji (strzalki, kropki, pasek postepu) + kontakt
  G   21.75-21.88 glitch + bialy blysk
  H   21.88-25.63 final: ciemne zdjecie piasty, snieg, logo z czapka Mikolaja, kicker, kontakt w czerwonej ramce
"""
import argparse, json, math, os, subprocess, tempfile
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
DMS = "/usr/share/fonts/opentype/inter/Inter-{}.otf"   # Inter: full Polish glyph set (DM Sans from the skill has no ę/ł/ń)
INTER_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTER_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
RED = (214, 44, 52); WHITE = (255, 255, 255); CREAM = (233, 214, 160); GREY = (150, 150, 158)

# ------------------------------------------------------------------ easing
def clamp01(t): return min(1.0, max(0.0, t))
def ease_out(t): t = clamp01(t); return 1 - (1 - t) ** 3
def ease_io(t): t = clamp01(t); return t * t * (3 - 2 * t)
def expo_out(t): t = clamp01(t); return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)
def expo_io(t):
    t = clamp01(t)
    if t in (0, 1): return t
    return 2 ** (20 * t - 10) / 2 if t < 0.5 else (2 - 2 ** (-20 * t + 10)) / 2
def back_out(t, c=1.25):
    t = clamp01(t); c3 = c + 1; return 1 + c3 * (t - 1) ** 3 + c * (t - 1) ** 2

# ------------------------------------------------------------------ fonts / text
def F(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

def rgba_from_pil(im):
    a = np.asarray(im).astype(np.float32) / 255.0; a[..., :3] = a[..., 2::-1].copy(); return a

def text_block(lines, x, y, f, lh, track=0.0, align="left"):
    """lines: list of list of (text, rgb) segments -> BGRA float layer"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for li, segs in enumerate(lines):
        width = sum(sum(f.getlength(c) + f.size * track for c in t) for t, _ in segs)
        xx = x if align == "left" else (W - width) / 2 if align == "center" else x - width
        for t, col in segs:
            for c in t:
                d.text((xx, y + li * lh), c, font=f, fill=(*col, 255)); xx += f.getlength(c) + f.size * track
    return rgba_from_pil(im)

def comp(img, lay, alpha=1.0, dy=0):
    if dy: lay = np.roll(lay, int(dy), axis=0)
    a = lay[..., 3:4] * alpha
    return img * (1 - a) + lay[..., :3] * 255 * a

class Title:
    """kicker (red bar + tracked caps), serif headline with red accent words, small EN subtitle; rises in, fades out"""
    def __init__(self, kicker, head_lines, sub, y=290, size=66):
        fk = F(DMS.format("Bold"), 25); fh = F(os.path.join(FD, "Lora.ttf"), size, "Medium"); fs = F(DMS.format("Medium"), 29)
        self.k = text_block([[("|  " + kicker, RED)]], 72, y, fk, 30, track=0.22)
        self.h = text_block(head_lines, 72, y + 44, fh, int(size * 1.18))
        self.s = text_block([[(sub, CREAM)]], 74, y + 52 + int(size * 1.18) * len(head_lines), fs, 34)
    def draw(self, img, t_in, t_out=None):
        """t_in, t_out in frames since the title started / since it started leaving"""
        for lay, d0 in ((self.k, 0), (self.h, 3), (self.s, 7)):
            e = ease_out((t_in - d0) / 12.0)
            if e <= 0: continue
            a, dy = e, 40 * (1 - e)
            if t_out is not None:
                o = ease_io(t_out / 7.0); a *= 1 - o; dy -= 30 * o
            img = comp(img, lay, a, dy)
        return img

# ------------------------------------------------------------------ backgrounds and particles
def make_bg(glow):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = 10 + 18 * np.exp(-((xx - W * 0.5) ** 2 / (W * 0.9) ** 2 + (yy - H * 0.42) ** 2 / (H * 0.55) ** 2))
    img = np.repeat(base[..., None], 3, axis=2)
    if glow:
        g = np.exp(-((xx - W * 0.55) ** 2 / (W * 0.55) ** 2 + (yy - H * 0.55) ** 2 / (H * 0.30) ** 2))
        img += g[..., None] * np.array([12, 10, 95], np.float32) * glow
    return img
BG = None; BG_RED = None
class Dust:
    def __init__(self, n=160, seed=1):
        r = np.random.default_rng(seed); self.p = np.c_[r.uniform(0, W, n), r.uniform(0, H, n), r.uniform(0.2, 1, n), r.uniform(0, 6.3, n)]
    def draw(self, img, k, strength=1.0, snow=False):
        lay = np.zeros((H, W), np.float32)
        for x, y, z, ph in self.p:
            if snow: xx = (x + 30 * math.sin(ph + k * 0.05 * z)) % W; yy = (y + k * 4.5 * z) % H; r = 1 + 4 * z; v = 0.35 + 0.6 * z
            else: xx = (x + k * 0.25 * z) % W; yy = (y - k * 0.4 * z) % H; r = 1 + 0.8 * z; v = (0.25 + 0.5 * z) * (0.6 + 0.4 * math.sin(ph + k * 0.15))
            cv2.circle(lay, (int(xx), int(yy)), max(1, int(r)), float(v), -1, cv2.LINE_AA)
        lay = cv2.GaussianBlur(lay, (0, 0), 1.2 if snow else 0.7)[..., None] * strength
        return img * (1 - lay) + 255 * lay

# ------------------------------------------------------------------ image helpers
def cover(img, w, h, focus=None, zoom=1.0):
    ih, iw = img.shape[:2]; s = max(w / iw, h / ih) * zoom
    fx, fy = focus if focus else (iw / 2, ih / 2)
    tx = min(0, max(w - iw * s, w / 2 - fx * s)); ty = min(0, max(h - ih * s, h / 2 - fy * s))
    return cv2.warpAffine(img, np.float32([[s, 0, tx], [0, s, ty]]), (w, h), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

def round_mask(w, h, r):
    m = np.zeros((h, w), np.float32); r = int(max(0, min(r, w // 2, h // 2)))
    if r == 0: m[:] = 1; return m
    cv2.rectangle(m, (r, 0), (w - r - 1, h - 1), 1, -1); cv2.rectangle(m, (0, r), (w - 1, h - r - 1), 1, -1)
    for cx, cy in ((r, r), (w - r - 1, r), (r, h - r - 1), (w - r - 1, h - r - 1)): cv2.circle(m, (cx, cy), r, 1, -1, cv2.LINE_AA)
    return m

def tile(canvas, content, cx, cy, scale=1.0, rot_y=0.0, rot_z=0.0, alpha=1.0, radius=26, border=None, bw=3, shadow=0.65, f=1900.0):
    """place a rounded card (content = BGR float, its own size) with perspective (rot_y deg about vertical axis)"""
    if alpha <= 0.003 or scale <= 0.01: return canvas
    h, w = content.shape[:2]; c = content.copy(); m = round_mask(w, h, radius)
    if border is not None:
        mb = round_mask(w, h, radius) - cv2.erode(round_mask(w, h, radius), np.ones((bw * 2 + 1, bw * 2 + 1), np.uint8))
        c = c * (1 - mb[..., None]) + np.array(border[::-1], np.float32) * mb[..., None]
    ry, rz = math.radians(rot_y), math.radians(rot_z); dst = []
    for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        x, y = x * scale, y * scale
        X, Z = x * math.cos(ry), x * math.sin(ry); p = f / (f + Z); X, Y = X * p, y * p
        dst.append((cx + X * math.cos(rz) - Y * math.sin(rz), cy + X * math.sin(rz) + Y * math.cos(rz)))
    Hm = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32(dst))
    wc = cv2.warpPerspective(c, Hm, (W, H), flags=cv2.INTER_LINEAR)
    wm = cv2.warpPerspective(m, Hm, (W, H), flags=cv2.INTER_LINEAR)[..., None] * alpha
    if shadow:
        sh = cv2.GaussianBlur(np.roll(wm[..., 0], int(28 * scale), axis=0), (0, 0), 30 * max(scale, 0.3))[..., None] * shadow
        canvas = canvas * (1 - sh)
    return canvas * (1 - wm) + wc * wm

def light_leak(img, t, angle=-28, width=260, strength=0.9):
    """diagonal soft white streak crossing the frame (screen blend); t 0..1"""
    if t <= 0 or t >= 1: return img
    x = -400 + t * (W + 800); lay = np.zeros((H, W), np.float32)
    dx = math.tan(math.radians(angle)) * H
    cv2.line(lay, (int(x), 0), (int(x + dx), H), 1.0, width)
    lay = cv2.GaussianBlur(lay, (0, 0), width * 0.45)[..., None] * strength * math.sin(math.pi * t)
    warm = np.array([235, 242, 255], np.float32)
    return 255 - (255 - img) * (1 - lay * warm / 255)

def glitch(img, amt, seed):
    """RGB split + horizontal slice displacement + slight lift; amt 0..1"""
    if amt <= 0: return img
    r = np.random.default_rng(seed); o = img.copy(); d = int(28 * amt)
    o[..., 2] = np.roll(img[..., 2], d, axis=1); o[..., 0] = np.roll(img[..., 0], -d, axis=1)
    for _ in range(int(9 * amt)):
        y0 = int(r.uniform(0, H - 40)); hh = int(r.uniform(12, 90)); s = int(r.uniform(-90, 90) * amt)
        o[y0:y0 + hh] = np.roll(o[y0:y0 + hh], s, axis=1)
    return o * (1 - 0.15 * amt) + 255 * 0.15 * amt

def chroma(img, px):
    if px < 0.5: return img
    o = img.copy(); cx, cy = W / 2, H / 2
    for ch, s in ((2, 1 + px / 900), (0, 1 - px / 900)):
        M = np.float32([[s, 0, (1 - s) * cx], [0, s, (1 - s) * cy]])
        o[..., ch] = cv2.warpAffine(img[..., ch], M, (W, H), borderMode=cv2.BORDER_REFLECT)
    return o

def zoom_at(img, cx, cy, s):
    return cv2.warpAffine(img, np.float32([[s, 0, (1 - s) * cx], [0, s, (1 - s) * cy]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def pill(text, f, fg, bg, pad=(28, 14), r=None):
    w = int(f.getlength(text) + 2 * pad[0]); h = int(f.size * 1.25 + 2 * pad[1])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r if r is not None else h // 4, fill=(*bg, 255))
    d.text((pad[0], pad[1] - f.size * 0.05), text, font=f, fill=(*fg, 255))
    a = rgba_from_pil(im); return a

def put_rgba(canvas, rgba, cx, cy, scale=1.0, alpha=1.0):
    h, w = rgba.shape[:2]
    M = np.float32([[scale, 0, cx - w * scale / 2], [0, scale, cy - h * scale / 2]])
    L = cv2.warpAffine(rgba, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = L[..., 3:4] * alpha
    return canvas * (1 - a) + L[..., :3] * 255 * a

# ------------------------------------------------------------------ main
def main():
    global BG, BG_RED
    ap = argparse.ArgumentParser()
    ap.add_argument("--rig", required=True); ap.add_argument("--photos", required=True)
    ap.add_argument("--hubs", default=os.path.join(HERE, "w222", "hubs_photos.json"))
    ap.add_argument("--righub", default=os.path.join(HERE, "w222", "rig_hub.json"))
    ap.add_argument("--hat", default=os.path.join(HERE, "w222", "santa_hat.png"))
    ap.add_argument("--logo", default=os.path.join(HERE, "..", "brand", "turismo_logo_white.png"))
    ap.add_argument("--out", required=True); ap.add_argument("--crf", default="16")
    ap.add_argument("--frames", default="", help="debug: write only these output frames as PNG")
    a = ap.parse_args()
    BG = make_bg(0.0); BG_RED = make_bg(1.0); dust = Dust(170, 2); snow = Dust(230, 5)
    hubs = {int(k): v for k, v in json.load(open(a.hubs)).items()}; rh = json.load(open(a.righub))
    cap = cv2.VideoCapture(a.rig); rig = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        rig.append(fr)
    def R(i): return cv2.resize(rig[int(min(len(rig), max(1, i))) - 1], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    NR = len(rig)                                        # rig length (guide 311, Seedance may differ)
    if os.environ.get("RIG_HUB"):                        # constant hub (x, y, rim) for the ramp when the rig is not the Blender guide
        x_, y_, r_ = (float(v) for v in os.environ["RIG_HUB"].split(",")); rh = [[x_, y_, r_, r_]] * NR
    def RH(i): return rh[int(min(len(rh), max(1, i))) - 1]
    PH = {}
    def P(k):
        if k not in PH: PH[k] = cv2.imread(os.path.join(a.photos, f"C26_{k:02d}.jpg")).astype(np.float32)
        return PH[k]
    FOCUS = {k: tuple(v[:2]) for k, v in hubs.items()}
    FOCUS[7] = (1180, 960); FOCUS[5] = (1465, 1000); FOCUS[9] = (1600, 900); FOCUS[6] = (1500, 900); FOCUS[10] = (1100, 1000); FOCUS[8] = (1350, 950)

    only = set(int(v) for v in a.frames.split(",")) if a.frames else None
    tmp = tempfile.mkdtemp(); n = [0]; cues = {}
    def emit(img, tag=None):
        i = n[0]
        if tag: cues.setdefault(tag, round(i / FPS, 3))
        if only is None: cv2.imwrite(os.path.join(tmp, f"{i:05d}.png"), np.clip(img, 0, 255).astype(np.uint8))
        elif i in only: cv2.imwrite(a.out.replace(".mp4", f"_f{i:03d}.png"), np.clip(img, 0, 255).astype(np.uint8))
        n[0] += 1
    def skip(): return only is not None and n[0] not in only        # debug speed-up: skip compositing of unrequested frames

    # ---------------- R: the whole rig shot
    for i in range(1, NR - 11):
        tg = "rig_start" if i == 1 else ("drop_car_pulls_away" if i == 135 else None)
        if skip():
            if tg: cues.setdefault(tg, round(n[0] / FPS, 3))
            n[0] += 1; continue
        emit(R(i), tg)
    # ---------------- R': 2x ramp with motion blur, push into the hub, chromatic split
    for j in range(6):
        if skip(): n[0] += 1; continue
        i0 = NR - 11 + 2 * j; img = (R(i0) + R(i0 + 1)) / 2; hx, hy = RH(i0)[:2]; t = (j + 1) / 6
        img = zoom_at(img, hx, hy, 1 + 0.25 * t * t); img = chroma(img, 18 * t)
        emit(img, "ramp" if j == 0 else None)
    last = R(NR); hx, hy = RH(NR)[:2]; last_z = zoom_at(last, hx, hy, 1.25)
    for j in range(3):                                   # glitch hit
        if skip(): n[0] += 1; continue
        emit(glitch(chroma(last_z, 22), 1.0 - 0.25 * j, 10 + j), "glitch_1" if j == 0 else None)

    # ---------------- B: rig frame shrinks into a 3D card, counter 0 -> 40
    tB = Title("TURISMO FORGED  ·  C26", [[("Jedna felga.", WHITE)], [("Zero ", WHITE), ("kompromisów.", RED)]], "One wheel. Zero compromise.")
    f_num = F(INTER_BLACK, 190); f_lab = F(DMS.format("Bold"), 30); f_lab2 = F(DMS.format("Medium"), 24)
    card_rig = cv2.resize(last, (558, 992), interpolation=cv2.INTER_AREA)
    nB = 38
    for k in range(nB):
        if skip(): n[0] += 1; continue
        e = expo_out(k / 14)
        img = BG_RED.copy(); img = dust.draw(img, k)
        # rect from full screen to the card
        cx = W / 2 + (690 - W / 2) * e; cy = H / 2 + (1075 - H / 2) * e; sc = (W / 558) * (1 - e) + 0.9 * e
        if k < 14:
            full = cv2.resize(zoom_at(last, hx, hy, 1.25 - 0.25 * e), (558, 992), interpolation=cv2.INTER_AREA)
        else: full = card_rig
        img = tile(img, full, cx, cy, scale=sc, rot_y=-10 * ease_io((k - 10) / 26), radius=int(40 * e), border=(70, 70, 76), bw=2, shadow=0.7 * e)
        if k < 3: img = glitch(img, 0.6 - 0.2 * k, 20 + k)
        img = tB.draw(img, k - 6)
        c = int(round(40 * ease_out((k - 10) / 20))) if k >= 10 else 0
        if k >= 8:
            al = ease_out((k - 8) / 8)
            img = comp(img, text_block([[(str(c), RED)]], 64, 1150, f_num, 200), al)
            img = comp(img, text_block([[("SZPRYCH", WHITE)]], 74, 1365, f_lab, 30, track=0.14), al)
            img = comp(img, text_block([[("SPOKES", GREY)]], 74, 1402, f_lab2, 30, track=0.14), al)
            for s_ in range(8):                         # dashed progress
                col = RED if s_ < round(8 * c / 40) else (90, 90, 96)
                cv2.rectangle(img, (74 + s_ * 34, 1448), (74 + s_ * 34 + 24, 1453), col[::-1], -1)
        emit(img, "cards" if k == 0 else None)

    # ---------------- C: 2x2 grid of real photos pops, then _07 expands to full screen
    tC = Title("REALIZACJA  ·  W222", [[("Mercedes S 560", WHITE)], [("na ", WHITE), ("Turismo C26", RED)]], "Mercedes-Benz S 560 on Turismo Forged C26")
    grid = [(12, (330, 840)), (7, (750, 840)), (1, (330, 1260)), (8, (750, 1260))]
    G = {k: cover(P(k), 400, 400, FOCUS[k], zoom=z) for k, z in ((12, 1.35), (7, 1.5), (1, 1.0), (8, 1.4))}
    nC = 48
    for k in range(nC):
        if skip(): n[0] += 1; continue
        img = BG.copy(); img = dust.draw(img, nB + k)
        if k < 9:                                          # previous card flies away up-left, title swaps
            e = ease_io(k / 8)
            img = tile(img, card_rig, 690 - 520 * e, 1075 - 760 * e, scale=0.9 - 0.65 * e, rot_y=-10 - 25 * e, rot_z=-12 * e, alpha=1 - e, radius=40, border=(70, 70, 76), bw=2)
            img = tB.draw(img, 40, t_out=k)
        img = tC.draw(img, k - 5)
        for g, (pk, (gx, gy)) in enumerate(grid):
            t0 = 6 + 4 * g
            if k < t0: continue
            if k >= 34 and pk == 7: continue
            s = back_out((k - t0) / 8, 1.4) * (1 - (0.1 if k >= 34 else 0) * ease_io((k - 34) / 12))
            al = clamp01((k - t0) / 3) * (1 - (ease_io((k - 34) / 10) if k >= 34 else 0))
            img = tile(img, G[pk], gx, gy, scale=s, alpha=al, radius=22, border=(64, 64, 70), bw=2, shadow=0.6)
        if k >= 34:                                        # _07 expands to full screen (expo in-out ramp)
            e = expo_io((k - 34) / 13)
            big = cover(P(7), 400 + int(680 * e), 400 + int(1520 * e), FOCUS[7], zoom=1.5 - 0.3 * e)
            img = tile(img, big, 750 + (540 - 750) * e, 840 + (960 - 840) * e, radius=int(22 * (1 - e)), border=(64, 64, 70) if e < 0.9 else None, shadow=0.6 * (1 - e))
        emit(img, "grid_real_photos" if k == 0 else None)

    # ---------------- D: _07 full screen, light leak, finish title -> glitch
    tD = Title("WYKOŃCZENIE", [[("Brushed ", WHITE), ("Silver", RED)]], "Brushed aluminium finish")
    nD = 36; full7 = cover(P(7), W, H, FOCUS[7], zoom=1.2)
    for k in range(nD):
        if skip(): n[0] += 1; continue
        img = zoom_at(full7, 600, 1150, 1 + 0.07 * ease_io(k / nD))
        sc = np.clip(1 - (np.arange(H, dtype=np.float32) - 150) / 600, 0, 1) ** 1.5; sc[:150] = 1
        img = img * (1 - 0.6 * sc[:, None, None])
        img = tD.draw(img, k - 2)
        img = light_leak(img, (k - 4) / 16)
        if k >= nD - 3: img = glitch(img, 0.5 + 0.25 * (k - nD + 3), 40 + k)
        emit(img, "full_photo" if k == 0 else None)

    # ---------------- E: wheel card in 3D + red badge counting 18" -> 22"
    tE = Title("SPECYFIKACJA", [[("Rozmiar ", WHITE), ("22 cale", RED)]], "22 inch  ·  10.5J  ·  forged")
    wheel_card = cover(P(4), 700, 700, FOCUS[4], zoom=1.25)
    f_badge = F(INTER_BLACK, 120); f_pill = F(DMS.format("Bold"), 34)
    p1 = pill("10.5J", f_pill, WHITE, (40, 40, 46)); p2 = pill("40 SPOKES", f_pill, WHITE, (40, 40, 46)); p3 = pill("BRUSHED SILVER", f_pill, (20, 20, 24), (236, 236, 240))
    nE = 40
    for k in range(nE):
        if skip(): n[0] += 1; continue
        img = BG_RED.copy(); img = dust.draw(img, 200 + k)
        img = glitch(img, 0.6 - 0.2 * k, 50 + k) if k < 3 else img
        img = tE.draw(img, k - 3)
        e = expo_out(k / 16)
        img = tile(img, wheel_card, 540, 900, scale=0.6 + 0.4 * e, rot_y=24 - 34 * ease_io(k / nE), alpha=clamp01(k / 4), radius=30, border=(70, 70, 76), bw=2, shadow=0.7)
        if k >= 10:
            v = 18 + 4 * ease_out((k - 10) / 18); txt = f"{v:.0f}″" if k < 28 else "22″"
            b = pill(txt, f_badge, WHITE, RED, pad=(40, 6), r=26)
            img = put_rgba(img, b, 540, 1340, scale=back_out((k - 10) / 7, 1.6))
        for pi, (pp, px, py) in enumerate(((p1, 250, 1180), (p2, 830, 1180), (p3, 540, 1470 - 1000))):
            t0 = 16 + 4 * pi
            if k >= t0 and pi < 2: img = put_rgba(img, pp, px, py, scale=back_out((k - t0) / 7, 1.5))
        emit(img, "spec_badge" if k == 0 else None)

    # ---------------- F: carousel of projects + contact pill
    tF = Title("ZOBACZ REALIZACJĘ", [[("Więcej na ", WHITE)], [("turismo-wheels.com", RED)]], "More projects at turismo-wheels.com")
    car = [5, 9, 6, 10]; CW, CHh = 760, 560
    C_ = {k: cover(P(k), CW, CHh, FOCUS[k], zoom=1.0) for k in car}
    f_c = F(DMS.format("Bold"), 30); f_c2 = F(DMS.format("Medium"), 24)
    contact = text_block([[("+48 501 404 861", WHITE)]], 112, 1272, f_c, 36)
    contact2 = text_block([[("daniel.chmielewski@turismo-wheels.com", CREAM)]], 112, 1316, f_c2, 30)
    nF = 52
    for k in range(nF):
        if skip(): n[0] += 1; continue
        img = BG.copy(); img = dust.draw(img, 260 + k)
        pos = min(3.0, max(0.0, (k - 6) / 14.0)); idx = int(pos); fr_ = expo_io(pos - idx) if idx < 3 else 0.0; p = idx + fr_
        for ci, pk in enumerate(car):
            off = ci - p
            if abs(off) > 1.6: continue
            sc = 1 - 0.18 * min(1, abs(off)); x = 540 + off * (CW * 0.86)
            img = tile(img, C_[pk], x, 880, scale=sc * back_out(k / 9, 1.2) if k < 9 else sc, rot_y=-14 * off, alpha=clamp01(1.4 - abs(off) * 0.5) * clamp01(k / 3), radius=24, shadow=0.6)
        img = tF.draw(img, k - 2)
        # arrows, dots, progress line
        for ax_, sym in ((150, "‹"), (930, "›")):
            cv2.circle(img, (ax_, 1205), 26, (200, 200, 205), 2, cv2.LINE_AA)
            img = comp(img, text_block([[(sym, WHITE)]], ax_ - 9, 1180, F(DMS.format("Medium"), 40), 40))
        for di in range(4):
            cv2.circle(img, (495 + di * 30, 1205), 6, RED[::-1] if di == round(p) else (120, 120, 126), -1, cv2.LINE_AA)
        cv2.line(img, (110, 1240), (970, 1240), (70, 70, 76), 3); cv2.line(img, (110, 1240), (110 + int(860 * (p + 1) / 4), 1240), RED[::-1], 3)
        if k >= 10:
            al = ease_out((k - 10) / 8)
            img = tile(img, np.full((120, 860, 3), 22, np.float32), 540, 1300, alpha=al * 0.92, radius=18, shadow=0.0)
            img = comp(img, contact, al); img = comp(img, contact2, al)
        img = light_leak(img, (k - 38) / 14, angle=24, strength=0.8)
        emit(img, "carousel" if k == 0 else None)

    # ---------------- G + H: glitch flash -> winter end card with the Santa hat on the logo
    end_bg = cover(P(1), W, H, FOCUS[1], zoom=1.15)
    end_bg = cv2.GaussianBlur(end_bg, (0, 0), 6) * 0.22
    logo = Image.open(a.logo).convert("RGBA"); lw = 700; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    LX, LY = (W - lw) // 2 + 18, 430
    logo_l = Image.new("RGBA", (W, H), (0, 0, 0, 0)); logo_l.paste(logo, (LX, LY), logo); logo_a = rgba_from_pil(logo_l)
    hat = cv2.imread(a.hat, cv2.IMREAD_UNCHANGED).astype(np.float32); hm = json.load(open(os.path.splitext(a.hat)[0] + ".json"))
    BRIM = (LX + 0.221 * lw, LY + 0.0158 * lw); HAT_W = 236.0 * lw / 760
    tag = text_block([[("|  TURISMO WHEELS  ·  UNLOCK YOUR STYLE", RED)]], 0, 690, F(DMS.format("Bold"), 25), 30, track=0.2, align="center")
    big = text_block([[("Odezwij się!", WHITE)]], 0, 790, F(INTER_BLACK, 118), 120, align="center")
    sub_big = text_block([[("Get in touch", CREAM)]], 0, 935, F(DMS.format("Medium"), 30), 34, align="center")
    f_n = F(os.path.join(FD, "Lora.ttf"), 40, "Medium"); f_s = F(DMS.format("Medium"), 22); f_t = F(DMS.format("Bold"), 30); f_l = F(DMS.format("Bold"), 20)
    box = [text_block([[("Daniel Chmielewski", WHITE)]], 150, 1066, f_n, 44),
           text_block([[("Turismo Wheels  ·  Forged C26", GREY)]], 152, 1118, f_s, 26),
           text_block([[("TEL", RED)]], 152, 1180, f_l, 24, track=0.1), text_block([[("+48 501 404 861", WHITE)]], 260, 1174, f_t, 34),
           text_block([[("E-MAIL", RED)]], 152, 1234, f_l, 24, track=0.1), text_block([[("daniel.chmielewski@turismo-wheels.com", WHITE)]], 260, 1229, F(DMS.format("Medium"), 27), 32)]
    nH = 90
    for k in range(-3, nH):
        if skip(): n[0] += 1; continue
        img = end_bg.copy()
        img = snow.draw(img, k + 3, strength=0.85, snow=True)
        if k < 0: img = glitch(img * 0.6 + 255 * 0.4 * (k + 3) / 3, 0.8, 70 + k); emit(img, "glitch_end" if k == -3 else None); continue
        e = ease_out(k / 8); img = comp(img, logo_a, e, 20 * (1 - e))
        t = (k - 8) / 13.0
        if t >= 0:                                         # hat drops onto the T (cubic ease-out, no bounce)
            ee = ease_out(t); s = HAT_W / hm["brim_w"]; bx, by = hm["brim_c"]
            M = cv2.getRotationMatrix2D((bx, by), -32 + 23 * ee, s); M[0, 2] += BRIM[0] - bx; M[1, 2] += BRIM[1] - 700 * (1 - ee) - by
            L = cv2.warpAffine(hat, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)) / 255.0
            img = img * (1 - L[..., 3:4]) + L[..., :3] * 255 * L[..., 3:4]
            if 21 <= k < 40:                               # snow puff on landing
                rr = np.random.default_rng(3); lay = np.zeros((H, W), np.float32); tt = (k - 21) / 19
                for _ in range(50):
                    ang = rr.uniform(-math.pi, 0); sp = rr.uniform(40, 170)
                    cv2.circle(lay, (int(BRIM[0] + math.cos(ang) * sp * tt * 1.6), int(BRIM[1] + 10 + math.sin(ang) * sp * tt + 90 * tt * tt)), int(rr.uniform(2, 5)), 1.0, -1, cv2.LINE_AA)
                lay = cv2.GaussianBlur(lay, (0, 0), 1.2)[..., None] * (1 - tt); img = img * (1 - lay) + 255 * lay
        for lay, t0 in ((tag, 22), (big, 26), (sub_big, 30)):
            if k >= t0: img = comp(img, lay, ease_out((k - t0) / 10), 36 * (1 - ease_out((k - t0) / 10)))
        if k >= 34:
            al = ease_out((k - 34) / 10)
            img = tile(img, np.full((250, 840, 3), 14, np.float32), 540, 1165, alpha=al * 0.85, radius=6, border=RED, bw=2, shadow=0.0)
            for bi, lay in enumerate(box):
                if k >= 36 + 2 * bi: img = comp(img, lay, ease_out((k - 36 - 2 * bi) / 8))
        if 62 <= k <= 80: img = light_leak(img, (k - 62) / 18, strength=0.45)
        emit(img, "end_card" if k == 0 else None)

    total = n[0]
    if only is not None: print("debug frames", sorted(only), "of", total, cues); return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", a.crf, "-preset", "slow", "-movflags", "+faststart",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", a.out], check=True)
    json.dump({"fps": FPS, "frames": total, "duration_s": round(total / FPS, 3), "cues_s": cues}, open(a.out + ".timeline.json", "w"), indent=1)
    print(a.out, total, "frames", round(total / FPS, 2), "s", cues)

if __name__ == "__main__":
    main()

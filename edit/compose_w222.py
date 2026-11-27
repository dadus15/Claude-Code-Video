"""Turismo C26 x Mercedes-Benz S 560 (W222) - montaz rolki 9:16 (24 fps, bez lektora, muzyka z trendow dodawana w TikToku).

Struktura (styl Karimy: hook bez ciecia, bialy flash + match cut, strobe na bit, tytul na odbarwionym kadrze, karta z elementami po kolei):
  A  0.00-1.50  HOOK: skret kol z rig shotu przyspieszony 1.5x, uderzenie 110->100 % na 1. klatce, slowo kluczowe w szeryfie
  B  1.50-1.75  bialy flash ze snieznym podmuchem (zimowa wersja "zlotego plynu")
  C  1.58-9.45  rig shot od 5.1 s: pauza na licu, RUSZENIE = DROP (2.08 s), tytul C26
  D  9.00-9.55  push w piaste + rozmycie obrotowe -> bialy flash
  E  9.58-10.0  match cut na zdjecie _12 (felga w tym samym punkcie kadru), rozmycie gasnie
  F 10.08-11.5  strobe 6 zdjec realizacji po 0.25 s, piasta zawsze w tym samym punkcie
  G 11.58-14.0  hero _07: kadr B&W -> tytul -> kolor wraca, powolny push na kole
  H 14.08-14.8  iris z piasty w karte koncowa
  I 14.88-18.4  karta: logo, czapka Mikolaja spada na znak T, platki sniegu, haslo, kontakt

Uzycie (z katalogu repo):
  python3 edit/compose_w222.py --rig renders/w222_c26_guide_v2_720x1280.mp4 --photos <katalog C26_xx.jpg> \
      --hubs edit/w222/hubs_photos.json --righub edit/w222/rig_hub.json --hat edit/w222/santa_hat.png --out renders/OUT.mp4
"""
import argparse, json, math, os, subprocess, tempfile
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 24
SKILL_FONTS = "/root/.claude/skills/synced/5628d1e2-09fa-4684-99d7-f6f5adccad20_383ed38f-cdf3-40a8-92c9-21fa68bbbc10/youtube-edit/assets/fonts/DMSans-{}.ttf"
NAVY, RED, GREY = (10, 27, 43), (199, 34, 42), (95, 104, 115)
CREAM = (243, 231, 196)
CYAN = (10, 240, 240)
HUB_T = (540.0, 1000.0)            # wspolny punkt piasty na ekranie dla match cutu i strobe

def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)
def expo_out(t): t = min(1, max(0, t)); return 1 - 2 ** (-10 * t) if t < 1 else 1.0

# ------------------------------------------------------------------ image ops (float32 BGR 0..255)
def warp(img, M, size=(W, H)):
    return cv2.warpAffine(img, M, size, flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

def zoom_at(img, cx, cy, s):
    return warp(img, np.float32([[s, 0, (1 - s) * cx], [0, s, (1 - s) * cy]]))

def spin_blur(img, cx, cy, deg, n=11):
    if deg < 0.3: return img
    acc = np.zeros_like(img, np.float32)
    for k in range(n):
        M = cv2.getRotationMatrix2D((cx, cy), deg * (k / (n - 1) - 0.5), 1.0)
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return acc / n

def desat(img, k):
    g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)[..., None]
    return img * (1 - k) + g * k

def photo_frame(ph, hub, s, target=HUB_T):
    """photo placed so its hub lands on `target`, scale s (out px per src px); translation clamped so the crop never leaves the photo"""
    ph_h, ph_w = ph.shape[:2]; s = max(s, H / ph_h, W / ph_w)
    tx = target[0] - s * hub[0]; ty = target[1] - s * hub[1]
    tx = min(0, max(W - s * ph_w, tx)); ty = min(0, max(H - s * ph_h, ty))
    return warp(ph, np.float32([[s, 0, tx], [0, s, ty]])), (s * hub[0] + tx, s * hub[1] + ty)

# ------------------------------------------------------------------ snow particles (deterministic)
class Snow:
    def __init__(self, n, seed, burst=None):
        r = np.random.default_rng(seed); self.n = n
        self.x = r.uniform(-60, W + 60, n); self.y = r.uniform(-200, H, n); self.z = r.uniform(0.25, 1.0, n)
        self.ph = r.uniform(0, 6.28, n); self.burst = burst
        if burst is not None:
            a = r.uniform(0, 6.28, n); sp = r.uniform(400, 2600, n)
            self.vx, self.vy = np.cos(a) * sp, np.sin(a) * sp
    def layer(self, t, color=(255, 255, 255), alpha=1.0, fall=110.0, size=7.0):
        """returns (rgb, a) float layers; t in seconds"""
        lay = np.zeros((H, W), np.float32)
        if self.burst is not None:
            cx, cy = self.burst; xs = cx + self.vx * t; ys = cy + self.vy * t + 300 * t * t
            rs = size * self.z * (1 + 3 * t); bl = 0
        else:
            xs = (self.x + 25 * np.sin(self.ph + t * 1.3 * self.z)) % (W + 120) - 60
            ys = (self.y + fall * self.z * t) % (H + 200) - 100; rs = size * self.z
        for x, y, r in zip(xs, ys, rs if np.ndim(rs) else [rs] * self.n):
            if -20 < x < W + 20 and -20 < y < H + 20: cv2.circle(lay, (int(x), int(y)), max(1, int(r)), 1.0, -1, cv2.LINE_AA)
        lay = cv2.GaussianBlur(lay, (0, 0), 1.6) * alpha
        return np.array(color, np.float32)[None, None, ::-1], np.clip(lay, 0, 1)[..., None]

def over(img, rgb, a): return img * (1 - a) + rgb * a

# ------------------------------------------------------------------ text layers (PIL -> RGBA float)
def font(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

def text_layer(items):
    """items: list of (text, font, (x,y), rgb, tracking) -> RGBA float32 (H,W,4) 0..1"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for txt, f, (x, y), col, tr in items:
        if tr:
            for c in txt: d.text((x, y), c, font=f, fill=(*col, 255)); x += f.getlength(c) + f.size * tr
        else: d.text((x, y), txt, font=f, fill=(*col, 255))
    a = np.asarray(im).astype(np.float32) / 255; a[..., :3] = a[..., 2::-1]   # RGBA -> BGRA
    return a

SCRIM = np.clip(1 - (np.arange(H, dtype=np.float32) - 120) / 560, 0, 1) ** 1.6       # dark top gradient behind titles (sky is near white)
SCRIM[:120] = 1.0
def scrim(img, k): return img * (1 - 0.55 * min(1, max(0, k)) * SCRIM[:, None, None])

def masked_rise(img, lay, box, t, dist=60, shadow=0.0):
    """title rises out of a clip rect: box=(x0,y0,x1,y1); t 0..1 (cubic ease-out applied)"""
    e = ease_out(t); dy = int(round(dist * (1 - e)))
    L = np.zeros_like(lay); x0, y0, x1, y1 = box
    L[y0:y1, x0:x1] = np.roll(lay, dy, axis=0)[y0:y1, x0:x1]
    a = L[..., 3:4] * min(1, t * 3)
    if shadow:
        sh = cv2.GaussianBlur(a, (0, 0), 14)[..., None] * shadow
        img = img * (1 - sh)
    return img * (1 - a) + L[..., :3] * 255 * a

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rig", required=True); ap.add_argument("--photos", required=True)
    ap.add_argument("--hubs", required=True); ap.add_argument("--righub", required=True)
    ap.add_argument("--hat", required=True); ap.add_argument("--logo", default="brand/turismo_logo_navy.png")
    ap.add_argument("--out", required=True); ap.add_argument("--crf", default="16")
    ap.add_argument("--frames", default="", help="render only these output frames (debug), e.g. 0,40,230")
    a = ap.parse_args()
    PF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
    PF = os.environ.get("FONT_DIR", PF)
    F_SERIF = PF + "PlayfairDisplay-Italic.ttf"; F_COND = PF + "Oswald.ttf"
    hubs = {int(k): v for k, v in json.load(open(a.hubs)).items()}
    rh = json.load(open(a.righub))                      # per rig frame: [x, y, rim_px_max, rim_px_mean] at 1080x1920
    cap = cv2.VideoCapture(a.rig); rig = []
    while True:
        ok, f = cap.read()
        if not ok: break
        rig.append(f)
    n_rig = len(rig)
    def R(i):                                           # rig frame (1-based index like Blender), float, 1080x1920
        i = int(min(n_rig, max(1, round(i)))); return cv2.resize(rig[i - 1], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    def RH(i): i = int(min(len(rh), max(1, round(i)))); return rh[i - 1]
    photos = {}
    def P(k):
        if k not in photos: photos[k] = cv2.imread(os.path.join(a.photos, f"C26_{k:02d}.jpg")).astype(np.float32)
        return photos[k]

    # ---------------- text layers
    t_hook = text_layer([("Forty spokes.", font(F_SERIF, 112, "Medium Italic"), (70, 300), CREAM, 0),
                         ("TURISMO FORGED C26  ·  22 × 10.5J", font(SKILL_FONTS.format(500), 30), (78, 445), (255, 255, 255), 0.12)])
    t_drive = text_layer([("TURISMO FORGED C26", font(F_COND, 92, "Bold"), (64, 330), (255, 255, 255), 0.01),
                          ("BRUSHED SILVER", font(SKILL_FONTS.format(700), 34), (68, 452), CYAN, 0.16)])
    t_hero = text_layer([("MERCEDES-BENZ", font(F_COND, 88, "Bold"), (64, 250), (255, 255, 255), 0.01),
                         ("S 560 4MATIC", font(F_COND, 88, "Bold"), (64, 350), (255, 255, 255), 0.01),
                         ("on Turismo Forged C26", font(F_SERIF, 54, "Italic"), (68, 470), CREAM, 0)])

    # ---------------- end card layers
    card_bg = np.full((H, W, 3), 255, np.float32)
    logo = Image.open(a.logo).convert("RGBA"); lw = 760; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    LOGO_XY = ((W - lw) // 2 + 20, 640)
    logo_l = Image.new("RGBA", (W, H), (0, 0, 0, 0)); logo_l.paste(logo, LOGO_XY, logo)
    logo_a = np.asarray(logo_l).astype(np.float32) / 255; logo_a[..., :3] = logo_a[..., 2::-1]
    def tracked_layer(parts, f, y, track):
        sp = f.size * track; widths = [sum(f.getlength(c) + sp for c in t) - sp for t, _ in parts]
        space = f.getlength(" ") + sp; total = sum(widths) + space * (len(parts) - 1); x = W / 2 - total / 2; items = []
        for (t, col), w_ in zip(parts, widths): items.append((t, f, (x, y), col, track)); x += w_ + space
        return text_layer(items)
    y_tag = LOGO_XY[1] + logo.height + 90
    c_tag = tracked_layer([("UNLOCK", NAVY), ("YOUR", NAVY), ("STYLE", RED)], font(SKILL_FONTS.format(700), 58), y_tag, 0.16)
    y_rule = LOGO_XY[1] + logo.height + 200
    c_model = tracked_layer([("TURISMO FORGED C26", NAVY), ("·", RED), ("MERCEDES-BENZ S-CLASS", NAVY)], font(SKILL_FONTS.format(500), 30), y_rule + 40, 0.12)
    c_name = tracked_layer([("DANIEL", NAVY), ("CHMIELEWSKI", NAVY)], font(SKILL_FONTS.format(700), 40), 1262, 0.08)
    c_tel = tracked_layer([("+48 501 404 861", NAVY)], font(SKILL_FONTS.format(700), 44), 1330, 0.06)
    c_mail = tracked_layer([("daniel.chmielewski@turismo-wheels.com", GREY)], font(SKILL_FONTS.format(500), 32), 1400, 0.02)
    hat = cv2.imread(a.hat, cv2.IMREAD_UNCHANGED).astype(np.float32)          # BGRA, trimmed, brim centre stored in json next to it
    hat_meta = json.load(open(os.path.splitext(a.hat)[0] + ".json"))
    HAT_W = 236.0                                                            # brim width on the card (px)
    BRIM_ON_CARD = (348.0, 652.0)                                            # top bar of the T mark (measured on end_card.png)
    snow_card = Snow(140, 3); snow_puff = Snow(60, 9, burst=BRIM_ON_CARD)

    def hat_layer(c):
        """hat drops onto the T: cubic ease-out 0.55 s, settles from -32 deg to -9 deg, no bounce"""
        t = (c - 6) / 13.0
        if t < 0: return None
        e = ease_out(t); s = HAT_W / hat_meta["brim_w"]
        ang = -32 + 23 * e; dy = -760 * (1 - e)
        bx, by = hat_meta["brim_c"]
        M = cv2.getRotationMatrix2D((bx, by), ang, s)
        M[0, 2] += BRIM_ON_CARD[0] - bx; M[1, 2] += BRIM_ON_CARD[1] + dy - by
        L = cv2.warpAffine(hat, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)) / 255.0
        return L, e

    def card(c, with_hat=True):
        img = card_bg.copy()
        # contact shadow of the hat on the logo
        img = img * (1 - logo_a[..., 3:4]) + logo_a[..., :3] * 255 * logo_a[..., 3:4]
        if with_hat:
            hl = hat_layer(c)
            if hl:
                L, e = hl
                sh = np.zeros((H, W), np.float32)
                cv2.ellipse(sh, (int(BRIM_ON_CARD[0]), int(BRIM_ON_CARD[1] + 18)), (int(HAT_W * 0.5), 16), -9, 0, 360, 1.0, -1)
                sh = cv2.GaussianBlur(sh, (0, 0), 10)[..., None] * 0.28 * e ** 4
                img = img * (1 - sh)
                img = img * (1 - L[..., 3:4]) + L[..., :3] * 255 * L[..., 3:4]
            if c >= 19:
                rgb, al = snow_puff.layer((c - 19) / FPS * 0.35, color=(232, 238, 245), alpha=max(0, 1 - (c - 19) / 16), size=5)
                img = over(img, rgb, al)
        for lay, c0, dist in ((c_tag, 14, 50), (c_model, 26, 30), (c_name, 32, 30), (c_tel, 36, 30), (c_mail, 40, 30)):
            if c >= c0: img = masked_rise(img, lay, (0, 0, W, H), (c - c0) / 17.0, dist)
        if c >= 22:
            k = ease_out((c - 22) / 12.0); half = int(60 * k)
            cv2.rectangle(img, (W // 2 - half, y_rule), (W // 2 + half, y_rule + 4), RED[::-1], -1)
        rgb, al = snow_card.layer(c / FPS, color=(196, 212, 228), alpha=0.85, fall=140, size=6)
        img = over(img, rgb, al)
        if 55 <= c <= 76:                                                     # one light sweep on the ink only
            p = (c - 55) / 21.0; x = int(-W * 0.3 + p * W * 1.6)
            sw = np.zeros((H, W), np.float32); cv2.line(sw, (x, 0), (x - 500, H), 1.0, 120)
            sw = cv2.GaussianBlur(sw, (0, 0), 50)[..., None]; dark = (img.mean(2, keepdims=True) < 200).astype(np.float32)
            img = img + sw * dark * 80
        return img

    # ---------------- timeline
    only = set(int(v) for v in a.frames.split(",")) if a.frames else None
    tmp = tempfile.mkdtemp(); frames_out = [0]; cues = {}            # frames go straight to disk (441 float frames would need ~11 GB)
    def emit(img, tag=None):
        i = frames_out[0]
        if tag: cues.setdefault(tag, i / FPS)
        if only is None: cv2.imwrite(os.path.join(tmp, f"{i:05d}.png"), np.clip(img, 0, 255).astype(np.uint8))
        elif i in only: cv2.imwrite(a.out.replace(".mp4", f"_f{i:03d}.png"), np.clip(img, 0, 255).astype(np.uint8))
        frames_out[0] += 1

    # A: hook (36 f)
    for k in range(36):
        src = 75 + 1.5 * k if k < 32 else 123 + (k - 32)
        img = R(src); hx, hy = RH(src)[:2]
        z = 1.10 - 0.10 * ease_out(k / 5) if k < 6 else 1.0 + 0.06 * ease_io((k - 6) / 29)
        img = zoom_at(img, hx, hy, z)
        if k >= 20: img = scrim(img, (k - 20) / 8)
        if k >= 22: img = masked_rise(img, t_hook, (0, 250, W, 520), (k - 22) / 17, 70, shadow=0.35)
        emit(img, "hook" if k == 0 else None)
    # B + C: flash with a snow gust, then the rig shot from 5.1 s at real speed
    gust = Snow(260, 5, burst=(RH(123)[0], RH(123)[1]))
    white = {36: 0.55, 37: 1.0, 38: 0.9, 39: 0.55, 40: 0.25, 41: 0.08}
    src = 123
    for k in range(36, 36 + 2):                       # last two hook frames burn out to white
        img = zoom_at(R(123 + (k - 32)), *RH(123)[:2], 1.06 + 0.04 * (k - 35))
        img = masked_rise(scrim(img, 1), t_hook, (0, 250, W, 520), 1, 70, shadow=0.35)
        rgb, al = gust.layer((k - 35) / FPS * 0.6, alpha=1.0, size=9); img = over(img, rgb, al)
        emit(img * (1 - white[k]) + 255 * white[k])
    n_c = 311 - 123 + 1
    for j in range(n_c):
        k = frames_out[0]; src = 123 + j; img = R(src); hx, hy, rim = RH(src)[:3]
        if j < 6:
            rgb, al = gust.layer((j + 3) / FPS * 0.6, alpha=max(0, 1 - j / 6), size=9); img = over(img, rgb, al)
        w_ = white.get(k, 0.0); img = img * (1 - w_) + 255 * w_
        if 68 <= k < 182: img = scrim(img, min((k - 68) / 8, (182 - k) / 10))
        if 72 <= k: img = masked_rise(img, t_drive, (0, 300, W, 520), (k - 72) / 17, 70, shadow=0.45) if k < 170 else img
        if 170 <= k < 180:                            # title leaves: fade + rise 0.35 s
            e = (k - 170) / 9; L = np.roll(t_drive, -int(30 * e), axis=0); al = L[..., 3:4] * (1 - e)
            img = img * (1 - al) + L[..., :3] * 255 * al
        tail = n_c - j
        if tail <= 12:                                # D: push into the hub + spin blur building
            t = ease_out((12 - tail + 1) / 12)
            img = spin_blur(zoom_at(img, hx, hy, 1.0 + 0.9 * t), hx, hy, 34 * t)
        emit(img, "drop_car_pulls_away" if src == 135 else None)
    hx_end, hy_end, rim_end = RH(311)[:3]
    for k in range(3):                                # white peak
        img = spin_blur(zoom_at(R(311), hx_end, hy_end, 1.9 + 0.1 * k), hx_end, hy_end, 34)
        w_ = (0.7, 1.0, 1.0)[k]; emit(img * (1 - w_) + 255 * w_, "flash_match_cut" if k == 0 else None)
    # E: match cut on _12 (hub on HUB_T, rim matches the zoomed rig rim), spin blur and white decay
    rim12 = hubs[12][2]; s12 = (rim_end * 1.9) / rim12 * 0.62
    for k in range(12):
        img, (px, py) = photo_frame(P(12), hubs[12][:2], s12 * (1 + 0.03 * k / 11))
        img = spin_blur(img, px, py, 30 * max(0, 1 - k / 8) ** 2)
        w_ = max(0, 0.85 - 0.28 * k); img = img * (1 - w_) + 255 * w_
        emit(img, "match_cut_photo" if k == 0 else None)
    # F: strobe on the beat (6 x 6 frames), hub on the same point, 4 % punch-in decaying
    strobe = [(4, 1.40), (1, 1.45), (8, 1.55), (5, 1.70), (10, 1.85), (2, 1.45)]
    for n_, (pk, s) in enumerate(strobe):
        hb = hubs[pk]
        for k in range(6):
            img, _ = photo_frame(P(pk), hb[:2], s * (1.04 - 0.04 * ease_out(k / 5)))
            emit(img, "strobe" if (n_ == 0 and k == 0) else None)
    # G: hero _07 - B&W, title, colour returns; slow push on the wheel
    for k in range(60):
        img, (px, py) = photo_frame(P(7), hubs[7][:2], 1.32 * (1 + 0.06 * ease_io(k / 59)), target=(390, 1150))
        img = desat(img, 1 - ease_io((k - 30) / 14))
        if k >= 2: img = scrim(img, (k - 2) / 8)
        if k >= 6: img = masked_rise(img, t_hero, (0, 220, W, 560), (k - 6) / 17, 80, shadow=0.55)
        emit(img, "hero" if k == 0 else None)
    # H: iris from the hub of _07 into the card (card zooms through 1.15 -> 1)
    last, (px, py) = photo_frame(P(7), hubs[7][:2], 1.32 * 1.06, target=(390, 1150))
    last = masked_rise(scrim(last, 1), t_hero, (0, 220, W, 560), 1, 80, shadow=0.55)
    Rmax = math.hypot(W, H); r0 = hubs[7][2] * 1.32 * 1.06
    for k in range(19):
        t = ease_out((k + 1) / 19)
        bg = zoom_at(last, px, py, 1.0 + 2.2 * t)
        cz = zoom_at(card(0, with_hat=False), W / 2, H / 2, 1.0 + 0.15 * (1 - t))
        mask = np.zeros((H, W), np.float32)
        cv2.circle(mask, (int(px + (W / 2 - px) * t), int(py + (H / 2 - py) * t)), int(r0 * 0.25 + (Rmax - r0 * 0.25) * t ** 1.4), 1.0, -1, cv2.LINE_AA)
        m = cv2.GaussianBlur(mask, (0, 0), 6)[..., None]
        emit(cz * m + bg * (1 - m), "iris" if k == 0 else None)
    # I: end card 3.5 s
    for c in range(84):
        emit(card(c), "end_card" if c == 0 else None)

    # ---------------- write
    n_out = frames_out[0]
    if only: print("debug frames", sorted(only), "of", n_out, cues); return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", a.crf, "-preset", "slow", "-movflags", "+faststart",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", a.out], check=True)
    json.dump({"fps": FPS, "frames": n_out, "duration_s": round(n_out / FPS, 3),
               "cues_s": {k: round(v, 3) for k, v in cues.items()}}, open(a.out + ".timeline.json", "w"), indent=1)
    print(a.out, n_out, "frames", round(n_out / FPS, 2), "s", cues)

if __name__ == "__main__":
    main()

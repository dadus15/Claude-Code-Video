"""Launch film C26 x S 560 - animated part (S1-S4) after the W222 v2 rig shot, plus final assembly.
usage: python3 launch_anim.py <scratch_dir> <out.mp4> [--frames i,j,k (debug PNGs, film frame indices)] [--scale 0.25 (preview)]
All motion is a pure function of time (springs, expo easings, sines): any frame renders exactly."""
import sys, os, math, json, subprocess, argparse
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, ".."))
import compose_w222_v2 as K
from compose_w222_v2 import W, H, make_bg, Dust, cover, light_leak, RED, WHITE, CREAM, GREY, INTER_BLACK, FD
FPS = 24
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
LORA = os.path.join(FD, "Lora.ttf")
N_RIG = 311
SC_LEN = {"S1": 5.2, "S2": 5.2, "S3": 4.4, "S4": 4.2}

# ------------------------------------------------------------------ motion primitives
def clamp01(t): return min(1.0, max(0.0, t))
def spring(t, f, z):
    """closed-form damped spring 0 -> 1 (x(t) = 1 - e^(-z w t)(cos wd t + z w / wd sin wd t))"""
    if t <= 0: return 0.0
    w = 2 * math.pi * f; wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
def heavy(t): return spring(t, 1.05, 0.68)
def pop(t): return spring(t, 2.3, 0.42)
def expo_out(t): t = clamp01(t); return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)
def expo_in(t): t = clamp01(t); return 0.0 if t <= 0 else 2 ** (10 * t - 10)
def expo_io(t):
    t = clamp01(t)
    if t in (0.0, 1.0): return t
    return 2 ** (20 * t - 10) / 2 if t < 0.5 else (2 - 2 ** (-20 * t + 10)) / 2
def ease_io(t): t = clamp01(t); return t * t * (3 - 2 * t)
def drift(t, seed, amp):
    r = np.random.default_rng(seed); ph = r.uniform(0, 6.28, 3); fr = r.uniform(0.15, 0.45, 3)
    return amp * sum(math.sin(2 * math.pi * f * t + p) for f, p in zip(fr, ph)) / 3

# ------------------------------------------------------------------ layers
def font(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f
def rgba_crop(text, f, col, track=0.0, pad=34):
    w = int(sum(f.getlength(c) + f.size * track for c in text) + 2 * pad); h = int(f.size * 1.45 + 2 * pad)
    im = Image.new("RGBA", (max(1, w), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = pad
    for c in text: d.text((x, pad), c, font=f, fill=(*col, 255)); x += f.getlength(c) + f.size * track
    a = np.asarray(im).astype(np.float32) / 255.0; a[..., :3] = a[..., 2::-1].copy(); return a, pad
def paste(img, crop, x, y, alpha=1.0, blur=0.0, scale=1.0):
    """composite float RGBA crop (0..1) with top-left at (x, y); optional blur and scale about the crop centre"""
    if alpha <= 0.002: return img
    c = crop
    if scale != 1.0:
        h0, w0 = c.shape[:2]; c = cv2.resize(c, (max(1, int(w0 * scale)), max(1, int(h0 * scale))), interpolation=cv2.INTER_LINEAR)
        x += (w0 - c.shape[1]) / 2; y += (h0 - c.shape[0]) / 2
    if blur > 0.3: c = cv2.GaussianBlur(c, (0, 0), blur)
    h, w = c.shape[:2]; xi, yi = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, xi), max(0, yi), min(W, xi + w), min(H, yi + h)
    if x1 <= x0 or y1 <= y0: return img
    cc = c[y0 - yi:y1 - yi, x0 - xi:x1 - xi]; a = cc[..., 3:4] * alpha
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + cc[..., :3] * 255 * a
    return img

class Words:
    """text split into words (or characters): each rises 0.5 em, fades in and un-blurs (expo-out 0.9 s, stagger)"""
    def __init__(self, lines, x, y, f, lh, track=0.0, align="left", chars=False):
        self.items = []; self.f = f
        for li, segs in enumerate(lines):
            toks = []
            for text, col in segs:
                parts = list(text) if chars else [p for p in text.replace(" ", " \0").split("\0")]
                toks += [(p, col) for p in parts if p]
            width = sum(sum(f.getlength(c) + f.size * track for c in t) for t, _ in toks)
            xx = x if align == "left" else (W - width) / 2
            for t, col in toks:
                tw = sum(f.getlength(c) + f.size * track for c in t)
                if t.strip():
                    crop, pad = rgba_crop(t.strip(), f, col, track)
                    self.items.append((crop, xx - pad + (f.getlength(t[0]) + f.size * track if t.startswith(" ") else 0), y + li * lh - pad))
                xx += tw
    def draw(self, img, t, stagger=0.06, dur=0.9, rise_em=0.5, blur0=14.0, t_exit=None):
        for i, (crop, x, y) in enumerate(self.items):
            lt = t - i * stagger
            if lt <= 0: continue
            e = expo_out(lt / dur); a = clamp01(lt / 0.3); dy = rise_em * self.f.size * (1 - e); bl = blur0 * (1 - e)
            if t_exit is not None and t_exit > 0:
                le = clamp01((t_exit - i * 0.03) / 0.45); a *= 1 - le; dy -= 0.4 * self.f.size * expo_in(le); bl += 12 * le
            img = paste(img, crop, x, y + dy, a, bl)
        return img

def rounded_mask(w, h, r):
    m = np.zeros((h, w), np.float32); r = int(max(1, min(r, w // 2, h // 2)))
    cv2.rectangle(m, (r, 0), (w - r - 1, h - 1), 1, -1); cv2.rectangle(m, (0, r), (w - 1, h - r - 1), 1, -1)
    for cx, cy in ((r, r), (w - r - 1, r), (r, h - r - 1), (w - r - 1, h - r - 1)): cv2.circle(m, (cx, cy), r, 1, -1, cv2.LINE_AA)
    return m

def glass(img, cx, cy, w, h, r, scale=1.0, alpha=1.0, tint=0.09, edge=0.55, border=None, blur=24, dark=0.0):
    """frosted glass panel (blurred backdrop + tint + 1.5 px bright edge + top sheen), computed on a crop"""
    w, h = w * scale, h * scale
    if alpha <= 0.002 or w < 4 or h < 4: return img
    x0, y0 = int(cx - w / 2), int(cy - h / 2); x1, y1 = int(cx + w / 2), int(cy + h / 2)
    m = int(blur * 2.5); X0, Y0, X1, Y1 = max(0, x0 - m), max(0, y0 - m), min(W, x1 + m), min(H, y1 + m)
    if X1 <= X0 or Y1 <= Y0: return img
    reg = img[Y0:Y1, X0:X1]; bl = cv2.GaussianBlur(reg, (0, 0), blur)
    mask = np.zeros(reg.shape[:2], np.float32); mm = rounded_mask(max(2, x1 - x0), max(2, y1 - y0), int(r * scale))
    sx0, sy0 = x0 - X0, y0 - Y0; ex, ey = min(mask.shape[1], sx0 + mm.shape[1]), min(mask.shape[0], sy0 + mm.shape[0])
    if sx0 < 0 or sy0 < 0:
        cx0, cy0 = max(0, -sx0), max(0, -sy0); mask[max(0, sy0):ey, max(0, sx0):ex] = mm[cy0:cy0 + ey - max(0, sy0), cx0:cx0 + ex - max(0, sx0)]
    else: mask[sy0:ey, sx0:ex] = mm[:ey - sy0, :ex - sx0]
    yy = (np.arange(reg.shape[0], dtype=np.float32) - sy0)[:, None, None]
    sheen = np.clip(1 - yy / max(1, (y1 - y0)), 0, 1) * 0.10
    glass_px = bl * (1 - tint - sheen - dark) + 255 * (tint + sheen)
    a = mask[..., None] * alpha
    out = reg * (1 - a) + glass_px * a
    e = mask - cv2.erode(mask, np.ones((3, 3), np.uint8)); e = cv2.GaussianBlur(e, (0, 0), 0.7)[..., None] * alpha
    col = np.array(border[::-1], np.float32) if border else np.array([255, 255, 255], np.float32)
    img[Y0:Y1, X0:X1] = out * (1 - e * edge) + col * e * edge
    return img

def touch(img, x, y, appear, press, ripple):
    """translucent touch circle (appear 0..1), squish (press 0..1), ripple ring (0..1)"""
    if appear <= 0 and ripple <= 0: return img
    lay = np.zeros((H, W), np.float32)
    if appear > 0: cv2.circle(lay, (int(x), int(y)), int(46 * (1 - 0.14 * press) * (0.6 + 0.4 * appear)), 0.40 * appear, -1, cv2.LINE_AA)
    if 0 < ripple < 1: cv2.circle(lay, (int(x), int(y)), int(56 + 150 * expo_out(ripple)), 0.6 * (1 - ripple), 3, cv2.LINE_AA)
    lay = cv2.GaussianBlur(lay, (0, 0), 1.2)[..., None]; return img * (1 - lay) + 255 * lay

def warp_rgba(src, M, persp=False):
    if persp: return cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
def over(img, L, alpha=1.0):
    a = L[..., 3:4] / 255.0 * alpha; return img * (1 - a) + L[..., :3] * a
def sim(s, rot, tx, ty, cx, cy):
    """scale s and rotate rot (deg) about (cx, cy), then translate to (tx, ty)"""
    M = cv2.getRotationMatrix2D((cx, cy), rot, s); M[0, 2] += tx - cx; M[1, 2] += ty - cy; return M
def shadow_ellipse(img, cx, cy, rx, ry, a):
    if a <= 0: return img
    m = np.zeros((H, W), np.float32); cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), 0, 0, 360, 1, -1)
    return img * (1 - cv2.GaussianBlur(m, (0, 0), max(4, ry * 0.8))[..., None] * a)
def marquee(img, text, y, size, alpha, x):
    crop, pad = rgba_crop(text, font(INTER_BLACK, size), WHITE, -0.03); return paste(img, crop, x - pad, y - pad, alpha)

# ------------------------------------------------------------------ scene assets
class Assets:
    def __init__(self, sc):
        self.sc = sc; L = os.path.join(sc, "launch"); self.L = L
        self.BG = make_bg(0.0); self.BGR = make_bg(1.0); self.dust = Dust(170, 2); self.snow = Dust(260, 5)
        rd = lambda p: cv2.imread(os.path.join(L, p), cv2.IMREAD_UNCHANGED).astype(np.float32)
        self.face = rd("wheel_hero_face.png"); self.hero = rd("wheel_hero.png")
        self.seq = [rd(f"s1seq/w{i:03d}.png") if os.path.exists(os.path.join(L, f"s1seq/w{i:03d}.png")) else None for i in range(1, 45)]
        if any(v is None for v in self.seq): print("WARNING: S1 sequence incomplete, preview uses the hero still")
        self.seq = [v if v is not None else self.hero for v in self.seq]
        self.logo = rd("logo_only.png"); self.hat = rd("hat_only.png"); self.phone = rd("phone_black.png")
        st = open(os.path.join(L, "static.log")).read()
        self.brim = [float(v) for v in st.split("BRIM_PX")[1].split()[:2]]
        self.corners = np.float32(json.loads(st.split("SCREEN_CORNERS")[1].split("\n")[0].strip().replace("(", "[").replace(")", "]")))
        self.hubs = {int(k): v for k, v in json.load(open(os.path.join(REPO, "edit/w222/hubs_photos.json"))).items()}
        self.rh = json.load(open(os.path.join(REPO, "edit/w222/rig_hub.json")))
        ph = os.path.join(sc, "..", "sclass"); self.P = lambda k: cv2.imread(os.path.join(ph, f"C26_{k:02d}.jpg")).astype(np.float32)
        cap = cv2.VideoCapture(self.rig_path()); self.rig = []
        while True:
            ok, fr = cap.read()
            if not ok: break
            self.rig.append(fr)
        hull = cv2.convexHull(np.argwhere(self.hero[..., 3] > 40)[:, ::-1].astype(np.int32))
        self.hero_hull = np.zeros((H, W), np.float32); cv2.fillConvexPoly(self.hero_hull, hull, 1.0)
        self.grain = np.random.default_rng(11).normal(0, 3.0, (H + 64, W + 64)).astype(np.float32)
        f = lambda k: cover(self.P(k), 640, 820, {7: (1180, 960), 5: (1465, 1040), 8: (1350, 980)}.get(k, tuple(self.hubs[k][:2])), zoom={7: 1.15, 5: 1.0, 12: 1.05, 8: 1.2}[k])
        self.cards = {k: f(k) for k in (5, 7, 8, 12)}
        self.end_bg = cv2.GaussianBlur(cover(self.P(1), W, H, self.hubs[1][:2], zoom=1.15), (0, 0), 7) * 0.18
        self.ui_base = make_ui_base(ph)
    def rig_path(self): return os.environ.get("RIG", os.path.join(REPO, "renders/w222_c26_guide_v2_720x1280.mp4"))
    def R(self, i): return cv2.resize(self.rig[int(min(len(self.rig), max(1, i))) - 1], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)

S2_OFF = 0.6
WHEEL_OFF = (0.0, 60.0)          # all wheel renders are camera-centred (hub 540,960): shift down in the frame
HUB = (540.0 + WHEEL_OFF[0], 960.0 + WHEEL_OFF[1])
FACE_RIM = 421.0

# ------------------------------------------------------------------ phone UI (1179 x 2556), base + dynamic layer
UW, UH = 1179, 2556
def ufont(w, s): return font(INTER.format(w), s)
def make_ui_base(ph):
    im = Image.new("RGB", (UW, UH), (12, 12, 14)); d = ImageDraw.Draw(im)
    lora = font(LORA, 76, "Medium")
    d.text((110, 62), "9:41", font=ufont("Bold", 52), fill=(255, 255, 255)); d.rounded_rectangle((UW / 2 - 190, 40, UW / 2 + 190, 150), 55, fill=(0, 0, 0))
    d.rounded_rectangle((UW - 240, 74, UW - 140, 116), 12, outline=(255, 255, 255), width=4); d.rectangle((UW - 234, 80, UW - 160, 110), fill=(255, 255, 255))
    logo = Image.open(os.path.join(REPO, "brand", "turismo_logo_white.png")).convert("RGBA"); lw = 420
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS); im.paste(logo, (80, 230), logo)
    d.text((80, 360), "PROJECTS", font=ufont("Bold", 34), fill=(150, 150, 158))
    p = cv2.cvtColor(cv2.imread(os.path.join(ph, "C26_07.jpg")), cv2.COLOR_BGR2RGB); ch, cw = 1180, 1019
    s = max(cw / p.shape[1], ch / p.shape[0]) * 1.35; cx, cy = 1180, 980
    crop = cv2.warpAffine(p, np.float32([[s, 0, cw / 2 - cx * s], [0, s, ch / 2 - cy * s]]), (cw, ch), flags=cv2.INTER_AREA)
    mask = Image.new("L", (cw, ch), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), 48, fill=255)
    im.paste(Image.fromarray(crop), (80, 450), mask)
    d.text((80, 1680), "Mercedes-Benz", font=lora, fill=(255, 255, 255)); d.text((80, 1770), "S 560 4MATIC L", font=lora, fill=(255, 255, 255))
    for i, (t, bg) in enumerate((("C26", RED), ("Brushed Silver", (38, 38, 44)), ("22 × 10.5J", (38, 38, 44)))):
        x0 = [80, 260, 690][i]; w = d.textlength(t, font=ufont("Bold", 40)) + 70
        d.rounded_rectangle((x0, 1905, x0 + w, 1985), 40, fill=bg); d.text((x0 + 35, 1920), t, font=ufont("Bold", 40), fill=(255, 255, 255))
    d.rounded_rectangle((UW / 2 - 200, UH - 40, UW / 2 + 200, UH - 28), 6, fill=(220, 220, 225))
    return im
def make_ui(base, press, morph, toast, icon, lines, tch, ripple_btn):
    im = base.copy(); d = ImageDraw.Draw(im)
    k = 16 * press; bx0, by0, bx1, by1 = 80 + k, 2140 + k * 0.4, UW - 80 - k, 2310 - k * 0.4
    c0, c1 = np.array(RED), np.array((150, 26, 34)); col = tuple(int(v) for v in c0 * (1 - morph) + c1 * morph)
    d.rounded_rectangle((bx0, by0, bx1, by1), 85, fill=col)
    for lab, a in (("Wyceń dla mojego auta", 1 - morph), ("Zapytanie wysłane ✓", morph)):
        if a <= 0.01: continue
        lay = Image.new("RGBA", (UW, UH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); f = ufont("Bold", 54)
        tw = ld.textlength(lab, font=f); ld.text(((UW - tw) / 2, (by0 + by1) / 2 - 36 + 20 * (1 - a) * (1 if lab.startswith("Z") else -1)), lab, font=f, fill=(255, 255, 255, int(255 * a)))
        im.paste(lay, (0, 0), lay)
    if ripple_btn > 0:
        lay = Image.new("RGBA", (UW, UH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); rr = 60 + 520 * expo_out(ripple_btn)
        ld.ellipse((UW * 0.62 - rr, (by0 + by1) / 2 - rr, UW * 0.62 + rr, (by0 + by1) / 2 + rr), fill=(255, 255, 255, int(60 * (1 - ripple_btn))))
        m = Image.new("L", (UW, UH), 0); ImageDraw.Draw(m).rounded_rectangle((bx0, by0, bx1, by1), 85, fill=255)
        im.paste(lay, (0, 0), Image.fromarray((np.asarray(m) / 255 * np.asarray(lay)[..., 3]).astype(np.uint8)))
    if tch[0] > 0:
        lay = Image.new("RGBA", (UW, UH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); tx, ty, ap, pr = tch; r = 72 * (1 - 0.14 * pr) * (0.6 + 0.4 * ap)
        ld.ellipse((tx - r, ty - r, tx + r, ty + r), fill=(255, 255, 255, int(95 * ap))); im.paste(lay, (0, 0), lay)
    if toast > 0.001:
        ty0 = int(-300 + toast * 480); bg = im.crop((50, max(0, ty0), UW - 50, max(1, ty0 + 260))).filter(ImageFilter.GaussianBlur(30)).resize((UW - 100, 260))
        tl = Image.alpha_composite(bg.convert("RGBA"), Image.new("RGBA", (UW - 100, 260), (40, 40, 46, 205)))
        tdl = ImageDraw.Draw(tl)
        if icon > 0:
            s = max(0.05, icon); c = (111, 127); hw = 75 * s
            tdl.rounded_rectangle((c[0] - hw, c[1] - hw, c[0] + hw, c[1] + hw), int(36 * s), fill=RED)
            mark = Image.open(os.path.join(REPO, "brand", "turismo_logo_white.png")).convert("RGBA").crop((19, 20, 1040, 541)).resize((max(1, int(112 * s)), max(1, int(57 * s))))
            tl.paste(mark, (int(c[0] - 56 * s), int(c[1] - 28 * s)), mark)
        for li, (txt, f, colr, y) in enumerate((("Daniel Chmielewski · Turismo Wheels", ufont("Bold", 40), (255, 255, 255), 50),
                                                ("Dziękuję! Twoje zapytanie dotarło.", ufont("Medium", 38), (220, 220, 226), 112), ("teraz", ufont("Medium", 32), (150, 150, 158), 166))):
            a = clamp01(lines - li * 0.35)
            if a <= 0: continue
            lay = Image.new("RGBA", tl.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text((220, y + 18 * (1 - expo_out(a))), txt, font=f, fill=(*colr, int(255 * a)))
            tl = Image.alpha_composite(tl, lay)
        m = Image.new("L", (UW - 100, 260), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, UW - 101, 259), 60, fill=255)
        im.paste(tl.convert("RGB"), (50, ty0), m)
    a = np.asarray(im).astype(np.float32)[..., ::-1].copy()
    return a

# ------------------------------------------------------------------ scenes
F_CHIP = None
class Film:
    def __init__(self, A):
        self.A = A; global F_CHIP; F_CHIP = font(INTER.format("Bold"), 34)
        fk = font(INTER.format("Bold"), 25); fh = font(LORA, 66, "Medium"); fs = font(INTER.format("Medium"), 29)
        def title(kicker, head, sub, y=290):
            return (Words([[("|  " + kicker, RED)]], 72, y, fk, 30, track=0.22), Words(head, 72, y + 44, fh, 78), Words([[(sub, CREAM)]], 74, y + 52 + 78 * len(head), fs, 34))
        self.t1 = title("TURISMO FORGED  ·  C26", [[("Czterdzieści ", WHITE), ("szprych.", RED)]], "Forty spokes. One forged piece.")
        self.t2 = title("REALIZACJA  ·  W222", [[("Na Mercedesie ", WHITE), ("S 560", RED)]], "Real project: Mercedes-Benz S 560 4MATIC L")
        self.t3 = title("KONTAKT", [[("Zapytaj o ", WHITE), ("swój projekt.", RED)]], "Ask about your own build.")
        self.end_k = Words([[("|  TURISMO WHEELS  ·  UNLOCK YOUR STYLE", RED)]], 0, 845, fk, 30, track=0.2, align="center")
        self.end_big = Words([[("Odezwij się!", WHITE)]], 0, 885, font(INTER_BLACK, 112), 120, align="center", chars=True)
        self.end_sub = Words([[("Get in touch", CREAM)]], 0, 1020, fs, 34, align="center")
        fn = font(LORA, 40, "Medium")
        self.card_lines = [Words([[("Daniel Chmielewski", WHITE)]], 160, 1116, fn, 44), Words([[("Turismo Wheels  ·  Forged C26", GREY)]], 162, 1170, font(INTER.format("Medium"), 22), 26),
                           Words([[("TEL", RED)]], 162, 1232, font(INTER.format("Bold"), 20), 24, track=0.1), Words([[("+48 501 404 861", WHITE)]], 270, 1226, font(INTER.format("Bold"), 30), 34),
                           Words([[("E-MAIL", RED)]], 162, 1286, font(INTER.format("Bold"), 20), 24, track=0.1), Words([[("daniel.chmielewski@turismo-wheels.com", WHITE)]], 270, 1281, font(INTER.format("Medium"), 27), 32)]
    def titles(self, img, T, t, t0, t_exit=None):
        k, h, s = T; te = None if t_exit is None else t - t_exit
        img = k.draw(img, t - t0, t_exit=te); img = h.draw(img, t - t0 - 0.10, t_exit=te); img = s.draw(img, t - t0 - 0.35, stagger=0.03, t_exit=te)
        return img
    def chip(self, img, text, cx, cy, t, active=0.0, squish=0.0, fade=1.0):
        if t <= 0: return img
        s = 0.45 + 0.55 * pop(t); s *= 1 - 0.06 * squish; a = clamp01(t / 0.2) * fade; bl = 10 * (1 - expo_out(t / 0.35)) + 10 * (1 - fade)
        w = F_CHIP.getlength(text) + 64; h = F_CHIP.size * 1.2 + 34
        img = glass(img, cx, cy, w, h, int(h / 2), scale=s, alpha=a, tint=0.08 + 0.08 * active, edge=0.5 + 0.4 * active, border=RED if active > 0.5 else None)
        crop, pad = rgba_crop(text, F_CHIP, WHITE, 0.06)
        return paste(img, crop, cx - w / 2 + 32 - pad, cy - F_CHIP.size * 0.62 - pad, a, bl, s)

    # ---------------- S1
    def s1_wheel_layer(self, t):
        """returns (BGRA float 0..255 layer of the wheel, hub xy)"""
        A = self.A; dx, dy = drift(t, 1, 5), drift(t, 2, 6); push = 1 + 0.03 * ease_io(t / 5.2)
        if t < 0.6:
            th = 12.0 - 900.0 * 0.4 * math.exp(-t / 0.4); om = 900.0 * math.exp(-t / 0.4) / FPS * 0.5
            # match-cut scale: rig rim (zoomed) -> hero size
            hx, hy, rim = A.rh[-1][:3]; s0 = rim * 1.55 / FACE_RIM; e = expo_out(t / 0.6)
            s = s0 + (1.0 - s0) * e; cx = hx + (HUB[0] - hx) * e; cy = hy + (HUB[1] - hy) * e
            M = sim(s, -th, cx, cy, 540, 960); L = warp_rgba(A.face, M)
            if om > 0.4:
                acc = np.zeros_like(L)
                for k in range(9): acc += warp_rgba(A.face, sim(s, -th + om * (k / 8 - 0.5), cx, cy, 540, 960))
                L = acc / 9
            return L, (cx, cy)
        if t < 2.4 - 1e-6:
            i = min(43, int(round((t - 0.6) * FPS))); src = A.seq[i]
        else: src = A.hero
        M = sim(push, drift(t, 3, 0.6), HUB[0] + dx, HUB[1] + dy, 540, 960)
        return warp_rgba(src, M), (HUB[0] + dx, HUB[1] + dy)
    def S1(self, t, for_iris=False):
        A = self.A; img = A.BGR * (0.93 + 0.07 * math.sin(t * 1.7))          # breathing red glow
        img = A.dust.draw(img, int(t * FPS) + 30)
        img = marquee(img, "C26  C26  C26", 640, 560, 0.055, -260 - 38 * t)
        L, (hx, hy) = self.s1_wheel_layer(t)
        img = shadow_ellipse(img, hx + 20, hy + 470, 330, 46, 0.75 * clamp01((t - 0.3) / 0.6))
        img = over(img, L)
        if 3.45 <= t <= 4.35: img = light_leak(img, (t - 3.45) / 0.9, angle=-32, width=170, strength=0.32)
        img = self.titles(img, self.t1, t, 1.0, t_exit=4.55)
        tap = 3.4; act = clamp01((t - tap - 0.05) / 0.15); sq = math.exp(-((t - tap) / 0.06) ** 2)
        for txt, cx, cy, t0 in (("40 SPOKES", 250, 640, 2.2), ("22 × 10.5J", 850, 760, 2.4), ("FORGED", 850, 1340, 2.6), ("BRUSHED SILVER", 300, 1420, 2.8)):
            if txt == "40 SPOKES" and t - t0 < 0.8: txt = f"{int(round(40 * expo_out((t - t0) / 0.8)))} SPOKES"
            fade = 1.0 - clamp01((t - 4.55) / 0.3)
            if fade <= 0: continue
            bs = txt == "BRUSHED SILVER"
            img = self.chip(img, txt, cx, cy, t - t0, active=act if bs else 0, squish=sq if bs else 0, fade=fade)
        img = touch(img, 380, 1424, clamp01((t - 3.2) / 0.12) * (1 - clamp01((t - 3.75) / 0.2)), sq, clamp01((t - tap) / 0.5) if t > tap else 0)
        return img

    # ---------------- S2
    def card_pose(self, k, t):
        """(cx, cy, scale, rot_y, rot_z, alpha) of each photo card at S2 time t"""
        home = {12: (560, 1010, 1.0, -8, -2), 5: (330, 820, 0.74, 22, -6), 8: (760, 900, 0.80, -20, 5), 7: (760, 900, 0.80, -20, 5)}
        t0 = {5: 0.0, 8: 0.12, 12: 0.24, 7: 2.55}[k]; e = heavy(t - t0)
        cx, cy, s, ry, rz = home[k]
        if k == 7:                          # replaces _8 in the back, then springs to the front after the swipe
            e2 = heavy(t - 2.85); f = home[12]
            cx, cy, s, ry, rz = (v0 + (v1 - v0) * e2 for v0, v1 in zip(home[7], f))
            s *= 0.5 + 0.5 * e; return cx + drift(t, 70, 6), cy + drift(t, 71, 6), s, ry + drift(t, 72, 1.5), rz, clamp01((t - t0) / 0.2)
        if k == 8:                          # back-right card leaves upward when _7 takes the front
            out = expo_in(clamp01((t - 2.6) / 0.5)); cy -= 900 * out
        a = clamp01((t - t0) / 0.2) * (1 - (clamp01((t - 2.6) / 0.5) if k == 8 else 0))
        s = s * (0.5 + 0.5 * e); ry = ry + 40 * (1 - e) * (1 if ry >= 0 else -1)
        if k == 12:                         # the swipe: follows the finger, then flies off left
            g = clamp01((t - 2.35) / 0.35); fly = expo_in(clamp01((t - 2.65) / 0.4))
            cx -= 220 * ease_io(g) + 900 * fly; rz -= 10 * ease_io(g) + 18 * fly; a *= 1 - clamp01((t - 2.9) / 0.15)
        return cx + drift(t, k, 6), cy + drift(t, k + 9, 6), s, ry + drift(t, k + 20, 1.5), rz + drift(t, k + 30, 0.8), a
    def S2(self, t, phone_handoff=True):
        A = self.A; img = A.BG.copy(); img = A.dust.draw(img, int(t * FPS) + 200)
        img = marquee(img, "W222", 1190, 420, 0.03, -30 - 30 * t)
        order = [5, 8, 7, 12] if t < 2.85 else [5, 8, 12, 7]
        for k in order:
            cx, cy, s, ry, rz, a = self.card_pose(k, t)
            if a <= 0.003: continue
            if k == 7 and t > 5.0 and phone_handoff: continue        # drawn by the phone hand-off
            n = 3 if (k == 12 and 2.6 < t < 3.0) else 1
            acc = None
            for j in range(n):                                        # 180-degree shutter for the fast fly-off
                tt = t + (j / max(1, n - 1) - 0.5) / FPS * 0.5 if n > 1 else t
                p = self.card_pose(k, tt); fr = K.tile(img, A.cards[k], p[0], p[1], scale=p[2], rot_y=p[3], rot_z=p[4], alpha=p[5], radius=34, border=(225, 225, 232), bw=5, shadow=0.75)
                acc = fr if acc is None else acc + fr
            img = acc / n
        img = self.titles(img, self.t2, t, 0.3, t_exit=4.9)
        pa = 1 - clamp01((t - 4.9) / 0.3)
        if t > 1.0 and pa > 0:
            s = 0.45 + 0.55 * pop(t - 1.0); txt = "S 560 4MATIC L  ·  C26 22″  ·  " + ("2/12" if t > 2.9 else "1/12")
            img = glass(img, 540, 1435, 580, 80, 40, scale=s, alpha=clamp01((t - 1.0) / 0.2) * pa, tint=0.12)
            crop, pad = rgba_crop(txt, font(INTER.format("Bold"), 30), WHITE, 0.04); img = paste(img, crop, 540 - (crop.shape[1] - 2 * pad) / 2 - pad, 1435 - 20 - pad, clamp01((t - 1.0) / 0.2) * pa, 0, s)
        fx = 560 - 260 * ease_io(clamp01((t - 2.35) / 0.35))
        img = touch(img, fx, 1180, clamp01((t - 2.2) / 0.12) * (1 - clamp01((t - 2.75) / 0.15)), clamp01((t - 2.3) / 0.06), clamp01((t - 2.32) / 0.5) if t > 2.32 else 0)
        return img

    # ---------------- S3 (phone)
    def phone_tf(self, t):
        """2D similarity applied to the phone render: rise (heavy spring), idle drift, haptic wiggle at the toast"""
        e = heavy(t + 0.35); y = 900 * (1 - e) + drift(t, 40, 8); x = drift(t, 41, 6)
        wig = 2.2 * math.sin(2 * math.pi * 9 * (t - 1.9)) * math.exp(-(t - 1.9) / 0.12) if t > 1.9 else 0.0
        rot = drift(t, 42, 0.8) + wig; s = 0.92 + 0.08 * e
        return sim(s, rot, 600 + x, 960 + y + 40, 540, 960)
    def ui_state(self, t):
        tch_a = clamp01((t - 1.15) / 0.1) * (1 - clamp01((t - 1.6) / 0.15)); press = math.exp(-((t - 1.35) / 0.07) ** 2)
        morph = clamp01((t - 1.42) / 0.18); ripple = clamp01((t - 1.38) / 0.5) if 1.38 < t < 1.9 else 0
        toast = spring(t - 1.9, 2.2, 0.4) if t > 1.9 else 0; icon = pop(t - 2.05) if t > 2.05 else 0; lines = clamp01((t - 2.1) / 0.25) * 1.7
        tch2 = clamp01((t - 3.55) / 0.1)
        if tch2 > 0: return dict(press=0, morph=1, toast=toast, icon=icon, lines=lines, tch=(UW * 0.5, 130 + 180, tch2, math.exp(-((t - 3.7) / 0.06) ** 2)), ripple_btn=0)
        return dict(press=press, morph=morph, toast=toast, icon=icon, lines=lines, tch=(UW * 0.62, 2225, tch_a, press), ripple_btn=ripple)
    def screen_quad(self, M):
        c = np.c_[self.A.corners, np.ones(4)] @ M.T; return np.float32(c)
    def S3(self, t, ui_override=None):
        A = self.A; img = A.BGR.copy(); img = A.dust.draw(img, int(t * FPS) + 400)
        img = marquee(img, "TURISMO", 1250, 330, 0.03, -60 - 30 * t)
        M = self.phone_tf(t)
        sp = M @ np.array([560.0, 1640.0, 1.0]); img = shadow_ellipse(img, sp[0], sp[1], 260, 34, 0.7)
        img = over(img, warp_rgba(A.phone, M))
        st = self.ui_state(t); ui = ui_override if ui_override is not None else make_ui(A.ui_base, **st)
        q = self.screen_quad(M); Hm = cv2.getPerspectiveTransform(np.float32([(0, 0), (UW, 0), (UW, UH), (0, UH)]), q)
        uw = cv2.warpPerspective(ui, Hm, (W, H), flags=cv2.INTER_AREA, borderValue=(0, 0, 0))
        m = cv2.warpPerspective(rounded_mask(UW, UH, 150), Hm, (W, H), flags=cv2.INTER_LINEAR)[..., None]
        refl = warp_rgba(A.phone, M)[..., :3]                       # black-screen render = glass reflections only
        img = img * (1 - m) + (255 - (255 - uw) * (1 - refl / 255.0 * 0.9)) * m
        img = self.titles(img, self.t3, t, 0.2, t_exit=3.6)
        if t > 3.7:                                                  # tap on the toast -> ripple floods to black
            tp = np.c_[[[UW * 0.5, 310]], [1]] ; Hp = Hm @ np.r_[tp.T]; px, py = Hp[0, 0] / Hp[2, 0], Hp[1, 0] / Hp[2, 0]
            r = 30 + 2300 * expo_in(clamp01((t - 3.7) / 0.7)) ** 0.8
            mk = np.zeros((H, W), np.float32); cv2.circle(mk, (int(px), int(py)), int(r), 1, -1, cv2.LINE_AA)
            mk = cv2.GaussianBlur(mk, (0, 0), 10)[..., None]; ring = np.zeros((H, W), np.float32); cv2.circle(ring, (int(px), int(py)), int(r), 1, 6, cv2.LINE_AA)
            img = img * (1 - mk) + 8 * mk; img = img + cv2.GaussianBlur(ring, (0, 0), 6)[..., None] * 160 * (1 - clamp01((t - 3.7) / 0.7))
        return img

    # ---------------- S4 (finale)
    def S4(self, t):
        A = self.A; img = A.end_bg * clamp01(t / 0.4) + 8 * (1 - clamp01(t / 0.4))
        img = A.snow.draw(img, int(t * FPS) + 40, strength=0.9 * clamp01(t / 0.5), snow=True)
        ls = 0.62; bx, by = 540 - (102 + 994) / 2 * ls, 175 - 591 * ls
        e = heavy(t - 0.05); y = 380 * (1 - e) + drift(t, 60, 4)
        M = np.float32([[ls * (0.9 + 0.1 * e), 0, bx + 0.1 * ls * 540 * (1 - e)], [0, ls * (0.9 + 0.1 * e), by + y]])
        img = over(img, warp_rgba(A.logo, M), clamp01(t / 0.25))
        if t > 0.9:
            h = spring(t - 0.9, 1.0, 0.6); drop = -900 * (1 - h); rot = -22 * (1 - h)
            bxp, byp = A.brim; Mh = cv2.getRotationMatrix2D((bxp, byp), rot, 1.0); Mh = np.vstack([Mh, [0, 0, 1]])
            Mh = np.vstack([M, [0, 0, 1]]) @ Mh; Mh[1, 2] += drop
            img = over(img, warp_rgba(A.hat, Mh[:2]))
            if 1.3 < t < 2.1:                                        # snow puff on landing
                rr = np.random.default_rng(3); lay = np.zeros((H, W), np.float32); tt = (t - 1.3) / 0.8
                p = Mh @ np.array([bxp, byp, 1.0])
                for _ in range(60):
                    ang = rr.uniform(-math.pi, 0); sp = rr.uniform(40, 190)
                    cv2.circle(lay, (int(p[0] + math.cos(ang) * sp * tt * 1.6), int(p[1] + 6 + math.sin(ang) * sp * tt + 120 * tt * tt)), int(rr.uniform(2, 5)), 1.0, -1, cv2.LINE_AA)
                lay = cv2.GaussianBlur(lay, (0, 0), 1.2)[..., None] * (1 - tt); img = img * (1 - lay) + 255 * lay
        img = self.end_k.draw(img, t - 1.3); img = self.end_big.draw(img, t - 1.4, stagger=0.035); img = self.end_sub.draw(img, t - 1.9)
        if t > 1.9:
            s = 0.6 + 0.4 * spring(t - 1.9, 1.6, 0.5); img = glass(img, 540, 1220, 840, 260, 18, scale=s, alpha=clamp01((t - 1.9) / 0.2), tint=0.06, edge=0.9, border=RED)
            for i, w in enumerate(self.card_lines): img = w.draw(img, t - 2.05 - 0.07 * i, stagger=0.03)
        if 3.0 <= t <= 3.6: img = light_leak(img, (t - 3.0) / 0.6, strength=0.4)
        return img

    # ---------------- transitions + timeline
    def frame(self, n):
        """n = film frame index (0-based). Rig frames are passed through untouched."""
        A = self.A
        if n < N_RIG: return A.R(n + 1)
        t = (n - N_RIG) / FPS
        if t < 5.2:
            if t < 0.6:                                              # match cut: rig -> hub push, iris at the rim
                hx, hy, rim = A.rh[-1][:3]; z = 1 + 0.55 * expo_out(t / 0.35)
                rig = K.zoom_at(A.R(N_RIG), hx, hy, z); acc = np.zeros_like(rig)
                for s in np.linspace(1.0, 1.0 + 0.10 * (1 - t / 0.6), 6): acc += K.zoom_at(rig, hx, hy, s)
                rig = acc / 6; s1 = self.S1(t)
                r = rim * z * 1.06 + (2300 - rim * z * 1.06) * expo_in(clamp01((t - 0.12) / 0.48))
                L, (cx, cy) = self.s1_wheel_layer(t)
                mk = np.zeros((H, W), np.float32); cv2.circle(mk, (int(cx), int(cy)), int(r), 1, -1, cv2.LINE_AA); mk = cv2.GaussianBlur(mk, (0, 0), 14)[..., None]
                img = rig * (1 - mk) + s1 * mk
                ring = np.zeros((H, W), np.float32); cv2.circle(ring, (int(cx), int(cy)), int(r), 1, 8, cv2.LINE_AA)
                img = 255 - (255 - img) * (1 - cv2.GaussianBlur(ring, (0, 0), 12)[..., None] * 0.8 * (1 - clamp01(t / 0.6)))
                return K.chroma(img, 10 * (1 - clamp01(t / 0.4)))
            if t < 4.6: return self.S1(t)
            # iris through the spokes: hero flies at the camera, its gaps reveal S2
            p = (t - 4.6) / 0.6; s = 1 + 8 * expo_in(p) ** 0.9
            base = self.S1(t); s2 = self.S2(S2_OFF * p)          # cards fan in while the wheel flies through
            M = sim(s, 0, HUB[0], HUB[1], HUB[0], HUB[1])
            wl = cv2.warpAffine(A.hero, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
            hull = cv2.warpAffine(A.hero_hull, M, (W, H), flags=cv2.INTER_LINEAR)[..., None]
            hole = hull * (1 - wl[..., 3:4] / 255.0)
            bgless = base * (1 - hull) + s2 * hole + wl[..., :3] * (wl[..., 3:4] / 255.0)
            acc = bgless.copy()
            for k in range(1, 4): acc += K.zoom_at(bgless, HUB[0], HUB[1], 1 + 0.03 * k * p)
            img = acc / 4; fade = clamp01((p - 0.75) / 0.25)
            return img * (1 - fade) + s2 * fade
        t -= 5.2
        if t < 5.2:
            t = t + S2_OFF                                           # S2 internal clock starts where the iris left it
            if t < 5.0: return self.S2(t)
            # hand-off: _7 card flies into the phone screen as the phone rises
            p = expo_io((t - 5.0) / 0.8); tp = t - 5.0 - 0.8           # phone time (negative while rising)
            s3 = self.S3_bg_phone(tp); s2 = self.S2(t)
            img = s2 * (1 - p) + s3 * p
            cx, cy, s, ry, rz, a = self.card_pose(7, t); Mp = self.phone_tf(tp); q = self.screen_quad(Mp)
            h0, w0 = A.cards[7].shape[:2]; src = np.float32([(0, 0), (w0, 0), (w0, h0), (0, h0)])
            K_ = K.tile(np.zeros_like(img), A.cards[7], cx, cy, scale=s, rot_y=ry, rot_z=rz, radius=34, shadow=0)
            # interpolate the card quad toward the photo area of the screen (top part of the UI)
            ph_q = cv2.perspectiveTransform(np.float32([[(80, 450), (1099, 450), (1099, 1630), (80, 1630)]]), cv2.getPerspectiveTransform(np.float32([(0, 0), (UW, 0), (UW, UH), (0, UH)]), q))[0]
            card_q = self.card_quad(cx, cy, s, ry, rz, w0, h0); dq = card_q + (ph_q - card_q) * p
            Hm = cv2.getPerspectiveTransform(src, np.float32(dq)); cw = cv2.warpPerspective(A.cards[7], Hm, (W, H), flags=cv2.INTER_LINEAR)
            cm = cv2.warpPerspective(rounded_mask(w0, h0, int(34 + 14 * p)), Hm, (W, H), flags=cv2.INTER_LINEAR)[..., None] * (1 - clamp01((p - 0.85) / 0.15))
            return img * (1 - cm) + cw * cm
        t -= 5.2
        if t < 4.4: return self.S3(t)
        t -= 4.4
        return self.S4(min(t, 4.2 - 1e-3))
    def S3_bg_phone(self, tp):
        return self.S3(max(tp, -0.35)) if tp >= -0.35 else self.S3(-0.35)
    def card_quad(self, cx, cy, sc, ry, rz, w, h, f=1900.0):
        ry, rz = math.radians(ry), math.radians(rz); out = []
        for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
            x, y = x * sc, y * sc; X, Z = x * math.cos(ry), x * math.sin(ry); pz = f / (f + Z); X, Y = X * pz, y * pz
            out.append((cx + X * math.cos(rz) - Y * math.sin(rz), cy + X * math.sin(rz) + Y * math.cos(rz)))
        return np.float32(out)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sc"); ap.add_argument("out")
    ap.add_argument("--frames", default=""); ap.add_argument("--every", type=float, default=0.0, help="preview: one frame every N seconds of the animation")
    ap.add_argument("--start", type=int, default=0)
    a = ap.parse_args()
    A = Assets(a.sc); Fm = Film(A); total = N_RIG + int(round(19.0 * FPS))
    def finish(img, n):
        g = A.grain[(n * 7) % 64:(n * 7) % 64 + H, (n * 13) % 64:(n * 13) % 64 + W][..., None]
        return np.clip(img + (g if n >= N_RIG else 0), 0, 255).astype(np.uint8)
    if a.frames or a.every:
        idx = [int(v) for v in a.frames.split(",")] if a.frames else list(range(N_RIG - 1, total, max(1, int(a.every * FPS))))
        for n in idx: cv2.imwrite(a.out.replace(".mp4", f"_f{n:04d}.jpg"), finish(Fm.frame(n), n), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print("debug", idx); return
    tmp = a.out + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                          "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", tmp], stdin=subprocess.PIPE)
    for n in range(total):
        p.stdin.write(finish(Fm.frame(n), n).tobytes())
        if n % 24 == 0: print("FRAME", n, flush=True)
    p.stdin.close(); p.wait(); os.replace(tmp, a.out); print("DONE", a.out, total)

if __name__ == "__main__":
    main()

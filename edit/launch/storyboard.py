"""Phase 2 storyboard: 5 key frames 1080x1920 for the C26 x S 560 launch film (after the W222 v2 rig shot)."""
import sys, os, math, json
import numpy as np, cv2
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import compose_w222_v2 as K
from compose_w222_v2 import W, H, F, text_block, comp, Title, make_bg, Dust, tile, cover, light_leak, put_rgba, pill, RED, WHITE, CREAM, GREY, DMS, INTER_BLACK, FD
SC, OUTD = sys.argv[1], sys.argv[2]; os.makedirs(OUTD, exist_ok=True)
PHOTOS = os.path.join(SC, "..", "sclass"); L = os.path.join(SC, "launch")
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
hubs = {int(k): v for k, v in json.load(open(os.path.join(REPO, "edit/w222/hubs_photos.json"))).items()}
rh = json.load(open(os.path.join(REPO, "edit/w222/rig_hub.json")))
def P(k): return cv2.imread(os.path.join(PHOTOS, f"C26_{k:02d}.jpg")).astype(np.float32)
def rgba(p): return cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32)
def over_rgba(img, im, x, y, s=1.0):
    """paste RGBA float (0..255) at top-left (x,y) with scale s"""
    M = np.float32([[s, 0, x], [0, s, y]])
    Lr = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = Lr[..., 3:4] / 255; return img * (1 - a) + Lr[..., :3] * a
def glass(img, x0, y0, x1, y1, r=40, tint=0.10, edge=0.55, blur=28, border=None):
    """frosted glass panel: blurred backdrop + white tint + bright 1.5 px edge + top sheen"""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1); m = np.zeros((H, W), np.float32)
    cv2.rectangle(m, (x0 + r, y0), (x1 - r, y1), 1, -1); cv2.rectangle(m, (x0, y0 + r), (x1, y1 - r), 1, -1)
    for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)): cv2.circle(m, (cx, cy), r, 1, -1, cv2.LINE_AA)
    bl = cv2.GaussianBlur(img, (0, 0), blur); m3 = m[..., None]
    sheen = np.clip(1 - (np.arange(H, dtype=np.float32)[:, None, None] - y0) / max(1, (y1 - y0)), 0, 1) * 0.10
    out = img * (1 - m3) + (bl * (1 - tint - sheen) + 255 * (tint + sheen)) * m3
    e = m - cv2.erode(m, np.ones((3, 3), np.uint8)); e = cv2.GaussianBlur(e, (0, 0), 0.7)[..., None]
    col = np.array(border[::-1], np.float32) if border else np.array([255, 255, 255], np.float32)
    return out * (1 - e * edge) + col * e * edge
def drop_shadow(img, cx, cy, rx, ry, a=0.6):
    m = np.zeros((H, W), np.float32); cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), 0, 0, 360, 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), ry * 0.8)[..., None] * a; return img * (1 - m)
def touch(img, x, y, press=1.0, ripple=0.6):
    lay = np.zeros((H, W), np.float32); cv2.circle(lay, (int(x), int(y)), int(44 * (1 - 0.12 * press)), 0.42, -1, cv2.LINE_AA)
    cv2.circle(lay, (int(x), int(y)), int(60 + 120 * ripple), 0.55 * (1 - ripple), 3, cv2.LINE_AA)
    lay = cv2.GaussianBlur(lay, (0, 0), 1.2)[..., None]; return img * (1 - lay) + 255 * lay
def chip(img, text, cx, cy, f, active=False):
    w = f.getlength(text) + 64; h = f.size * 1.2 + 34
    img = glass(img, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, r=int(h / 2), tint=0.16 if active else 0.08, edge=0.9 if active else 0.5, border=RED if active else None)
    return comp(img, text_block([[(text, WHITE)]], cx - w / 2 + 32, cy - f.size * 0.62, f, 40, track=0.06))
def marquee(img, text, y, size, alpha=0.06, x=-120):
    return comp(img, text_block([[(text, WHITE)]], x, y, F(INTER_BLACK, size), size, track=-0.03), alpha)
BG = make_bg(0.0); BGR = make_bg(1.0); dust = Dust(170, 2); snow = Dust(230, 5)
f_chip = F(DMS.format("Bold"), 34)
frames = {}
# ---------------- K0: last rig frame -> hub push -> match cut into the 3D C26 (mid-transition)
cap = cv2.VideoCapture(os.path.join(REPO, "renders/w222_c26_guide_v2_720x1280.mp4")); last = None
while True:
    ok, fr = cap.read()
    if not ok: break
    last = fr
rig = cv2.resize(last, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32); hx, hy, rim = rh[-1][:3]
z = 1.55; img = K.zoom_at(rig, hx, hy, z)
acc = np.zeros_like(img)
for s in np.linspace(1.0, 1.12, 8): acc += K.zoom_at(img, hx, hy, s)
img = acc / 8
wh = rgba(os.path.join(L, "wheel_hero_face.png")) if os.path.exists(os.path.join(L, "wheel_hero_face.png")) else rgba(os.path.join(L, "wheel_hero.png"))
whx, why, wrim = 540, 960, 421.0           # hub and rim radius of wheel_hero_face.png (alpha bbox)
s = (rim * z) / wrim; wl = cv2.warpAffine(wh, np.float32([[s, 0, hx - s * whx], [0, s, hy - s * why]]), (W, H), flags=cv2.INTER_LANCZOS4, borderValue=(0, 0, 0, 0))
mask = np.zeros((H, W), np.float32); cv2.circle(mask, (int(hx), int(hy)), int(rim * z * 1.08), 1, -1, cv2.LINE_AA); mask = cv2.GaussianBlur(mask, (0, 0), 18)[..., None]
dark = BGR * mask + img * (1 - mask); a = wl[..., 3:4] / 255 * 0.85
img = dark * (1 - a) + wl[..., :3] * a
ring = np.zeros((H, W), np.float32); cv2.circle(ring, (int(hx), int(hy)), int(rim * z * 1.08), 1, 10, cv2.LINE_AA); ring = cv2.GaussianBlur(ring, (0, 0), 14)[..., None] * 0.9
img = 255 - (255 - img) * (1 - ring); img = K.chroma(img, 8)
frames["K0_przejscie_rig_do_3D"] = img
# ---------------- K1: S1 hero 3D wheel + glass chips + touch on BRUSHED SILVER
img = BGR.copy(); img = dust.draw(img, 30)
img = marquee(img, "C26  C26  C26", 640, 560, 0.055, x=-260)
img = drop_shadow(img, 560, 1540, 330, 46, 0.75)
wh = rgba(os.path.join(L, "wheel_hero.png")); img = over_rgba(img, wh, 0, 110, 1.0)
img = light_leak(img, 0.55, angle=-30, width=160, strength=0.18)
tK = Title("TURISMO FORGED  ·  C26", [[("Czterdzieści ", WHITE), ("szprych.", RED)]], "Forty spokes. One forged piece.")
img = tK.draw(img, 40)
img = chip(img, "40 SPOKES", 250, 640, f_chip); img = chip(img, "22 × 10.5J", 850, 760, f_chip)
img = chip(img, "BRUSHED SILVER", 300, 1420, f_chip, active=True); img = chip(img, "FORGED", 850, 1340, f_chip)
img = touch(img, 380, 1424, 1.0, 0.45)
frames["K1_felga_3D_chipy"] = img
# ---------------- K2: real photo cards fanned in depth, swipe on the front card
img = BG.copy(); img = dust.draw(img, 60)
img = marquee(img, "W222", 1190, 420, 0.03, x=-30)
cards = [(5, 330, 820, 0.74, 22, -6), (12, 760, 900, 0.80, -20, 5), (7, 560, 1010, 1.0, -8, -2)]
for k, cx, cy, sc, ry, rz in cards:
    c = cover(P(k), 640, 820, {7: (1180, 960), 5: (1465, 1040)}.get(k, tuple(hubs[k][:2])), zoom={7: 1.15, 5: 1.0, 12: 1.05}[k])
    img = tile(img, c, cx, cy, scale=sc, rot_y=ry, rot_z=rz, radius=34, border=(225, 225, 232), bw=5, shadow=0.75)
tK = Title("REALIZACJA  ·  W222", [[("Na Mercedesie ", WHITE), ("S 560", RED)]], "Real project: Mercedes-Benz S 560 4MATIC L")
img = tK.draw(img, 40)
img = glass(img, 250, 1395, 830, 1475, r=40, tint=0.12)
img = comp(img, text_block([[("S 560 4MATIC L  ·  C26 22″  ·  ", WHITE), ("1/12", RED)]], 290, 1418, F(DMS.format("Bold"), 30), 36, track=0.04))
img = touch(img, 640, 1180, 0.6, 0.25)
trail = np.zeros((H, W), np.float32)
for i in range(14): cv2.circle(trail, (int(640 + i * 14), 1180), int(30 - i * 1.6), 0.18 * (1 - i / 14), -1, cv2.LINE_AA)
img = img * (1 - cv2.GaussianBlur(trail, (0, 0), 3)[..., None]) + 255 * cv2.GaussianBlur(trail, (0, 0), 3)[..., None]
frames["K2_realne_zdjecia_karty"] = img
# ---------------- K3: phone with the app, pressed CTA, toast
img = BGR.copy(); img = dust.draw(img, 90)
img = marquee(img, "TURISMO", 1250, 330, 0.03, x=-60)
ph = rgba(os.path.join(L, "phone_final.png")) if os.path.exists(os.path.join(L, "phone_final.png")) else rgba(os.path.join(L, "phone_test.png"))
img = drop_shadow(img, 600, 1560, 260, 34, 0.7)
if ph.shape[1] == 1080: img = over_rgba(img, ph, 40, 120, 1.0)
else: img = over_rgba(img, ph, 40, 120, 2.0)
tK = Title("KONTAKT", [[("Zapytaj o ", WHITE), ("swój projekt.", RED)]], "Ask about your own build.")
img = tK.draw(img, 40)
frames["K3_telefon_zapytanie"] = img
# ---------------- K4: winter finale, 3D logo with the Santa hat
end_bg = cv2.GaussianBlur(cover(P(1), W, H, hubs[1][:2], zoom=1.15), (0, 0), 7) * 0.18
img = snow.draw(end_bg.copy(), 40, strength=0.9, snow=True)
lg = rgba(os.path.join(L, "logo_hat_final.png")); ls_ = 0.62
img = over_rgba(img, lg, 540 - (102 + 994) / 2 * ls_, 175 - 591 * ls_, ls_)
img = comp(img, text_block([[("|  TURISMO WHEELS  ·  UNLOCK YOUR STYLE", RED)]], 0, 845, F(DMS.format("Bold"), 25), 30, track=0.2, align="center"))
img = comp(img, text_block([[("Odezwij się!", WHITE)]], 0, 885, F(INTER_BLACK, 112), 120, align="center"))
img = comp(img, text_block([[("Get in touch", CREAM)]], 0, 1020, F(DMS.format("Medium"), 30), 34, align="center"))
img = glass(img, 120, 1090, 960, 1350, r=18, tint=0.06, edge=0.9, border=RED)
fn = F(os.path.join(FD, "Lora.ttf"), 40, "Medium")
for lay in (text_block([[("Daniel Chmielewski", WHITE)]], 160, 1116, fn, 44), text_block([[("Turismo Wheels  ·  Forged C26", GREY)]], 162, 1170, F(DMS.format("Medium"), 22), 26),
            text_block([[("TEL", RED)]], 162, 1232, F(DMS.format("Bold"), 20), 24, track=0.1), text_block([[("+48 501 404 861", WHITE)]], 270, 1226, F(DMS.format("Bold"), 30), 34),
            text_block([[("E-MAIL", RED)]], 162, 1286, F(DMS.format("Bold"), 20), 24, track=0.1), text_block([[("daniel.chmielewski@turismo-wheels.com", WHITE)]], 270, 1281, F(DMS.format("Medium"), 27), 32)):
    img = comp(img, lay)
frames["K4_final_logo_czapka"] = img
# ---------------- grain + write + contact sheet
rng = np.random.default_rng(7)
for name, im in frames.items():
    g = rng.normal(0, 3.2, (H, W, 1)).astype(np.float32); im = np.clip(im + g, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(OUTD, name + ".png"), im); frames[name] = im
labels = ["S0→S1  ostatnia klatka rigu: push w piastę, match cut na felgę 3D", "S1  felga 3D z CAD, szklane chipy, dotyk BRUSHED SILVER",
          "S2  prawdziwe zdjęcia S 560 jako karty w głębi, swipe", "S3  telefon z aplikacją Turismo, wysłane zapytanie + powiadomienie",
          "S4  finał zimowy: logo T w 3D z czapką Mikołaja, kontakt"]
from PIL import Image, ImageDraw
sheet = Image.new("RGB", (5 * 432 + 6 * 24, 768 + 210), (16, 16, 18)); d = ImageDraw.Draw(sheet); fl = F(DMS.format("Medium"), 22)
for i, (name, im) in enumerate(frames.items()):
    th = Image.fromarray(cv2.cvtColor(cv2.resize(im, (432, 768), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)); x = 24 + i * (432 + 24)
    sheet.paste(th, (x, 24))
    words = labels[i].split(); line = ""; yy = 812
    for wd in words:
        if fl.getlength(line + " " + wd) > 420: d.text((x, yy), line.strip(), font=fl, fill=(230, 230, 235)); yy += 30; line = ""
        line += " " + wd
    d.text((x, yy), line.strip(), font=fl, fill=(230, 230, 235))
sheet.save(os.path.join(OUTD, "storyboard_contact_sheet.jpg"), quality=92); print("OK", list(frames))

"""Turismo RS5 V05 - montaz: rig shot -> przejscie przez piaste -> scena RS5 -> iris -> end card.

Uzycie:
  python3 compose.py --rig RIG.mp4 --hero HERO.mp4|HERO_START.jpg,HERO_END.jpg --card end_card.png --out OUT.mp4

- RIG: ujecie z kamera na aucie (prowadnica z Blendera albo wersja z Seedance), 24 fps, 9:16.
- HERO: wideo z Seedance (pull-back z piasty na cale RS5) ALBO para klatek (start,end) -> animatik
  (plynny odjazd kamery od piasty, 0 kredytow) do akceptacji przejscia.
Styl wg youtube-edit/AUTOMOTIVE-SHORTS: max 3 zabiegi, ease-out cubic, bez flashy, iris przez piaste.
"""
import argparse, math, subprocess, tempfile, os
import numpy as np, cv2

W, H, FPS = 1080, 1920, 24
T_PUSH = 0.50     # koncowka rig shotu: push-in w piaste + rozmycie rotacyjne
T_HERO = 4.00     # scena RS5
T_IRIS = 0.70     # iris z piasty do karty
T_CARD = 2.60     # karta z logo (hold + light sweep)

def ease_out(t): return 1 - (1 - t) ** 3
def ease_in_out(t): return t * t * (3 - 2 * t)

def read_video(path):
    cap = cv2.VideoCapture(path); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4))
    return fr

def zoom_at(img, cx, cy, s):
    M = np.float32([[s, 0, (1 - s) * cx], [0, s, (1 - s) * cy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def spin_blur(img, cx, cy, deg, n=9):
    if deg < 0.2: return img
    acc = np.zeros_like(img, np.float32)
    for k in range(n):
        a = deg * (k / (n - 1) - 0.5)
        M = cv2.getRotationMatrix2D((cx, cy), a, 1.0)
        acc += cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    return (acc / n).astype(np.uint8)

def hero_animatic(start_p, end_p, n):
    """Plynny odjazd: interpolacja kadru po zdjeciu startowym (piasta) -> koncowym (cale auto)."""
    a = cv2.resize(cv2.imread(start_p), (W, H)); b = cv2.resize(cv2.imread(end_p), (W, H))
    out = []
    hx, hy = 0.728 * W, 0.685 * H     # piasta na kadrze koncowym (hero_end_9x16)
    S0 = 1536 / 760                   # skala kadru startowego wzgledem koncowego (oba z tego samego zdjecia)
    for i in range(n):
        t = ease_in_out(i / (n - 1))
        s = S0 ** (1 - t)                                   # 2.02 -> 1.0 (wykladniczo = stala predkosc odjazdu)
        px, py = W / 2 + (hx - W / 2) * t, H / 2 + (hy - H / 2) * t   # gdzie lezy piasta na ekranie
        M = np.float32([[s, 0, px - s * hx], [0, s, py - s * hy]])
        fb = cv2.warpAffine(b, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        sa = s / S0                                          # ten sam ruch na ostrym kadrze startowym
        Ma = np.float32([[sa, 0, px - sa * W / 2], [0, sa, py - sa * H / 2]])
        fa = cv2.warpAffine(a, Ma, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        k = float(np.clip((t - 0.15) / 0.35, 0, 1))
        out.append(cv2.addWeighted(fa, 1 - k, fb, k, 0))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rig", required=True); ap.add_argument("--hero", required=True)
    ap.add_argument("--card", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--rig_hub", default="0.60,0.56", help="pozycja piasty w rig shot (ulamki W,H)")
    ap.add_argument("--hero_hub_end", default="0.728,0.685")
    a = ap.parse_args()
    rig = read_video(a.rig)
    rx, ry = [float(v) for v in a.rig_hub.split(",")]; rcx, rcy = rx * W, ry * H
    frames = []
    n_push = int(T_PUSH * FPS)
    body, tail = rig[:-n_push], rig[-n_push:]
    frames += body
    # 1) push-in w piaste + narastajace rozmycie rotacyjne (zgodne z kierunkiem obrotu kola)
    for i, f in enumerate(tail):
        t = ease_out((i + 1) / n_push)
        z = zoom_at(f, rcx, rcy, 1.0 + 1.8 * t)
        z = zoom_at(z, rcx, rcy, 1.0)
        frames.append(spin_blur(z, rcx, rcy, 28 * t))
    # 2) scena RS5: start na piascie (match cut), rozmycie gasnie przez pierwsze 6 klatek
    n_hero = int(T_HERO * FPS)
    if "," in a.hero:
        s, e = a.hero.split(","); hero = hero_animatic(s, e, n_hero)
    else:
        hero = read_video(a.hero)[:n_hero]
    for i, f in enumerate(hero):
        if i < 6:
            t = 1 - i / 6
            f = spin_blur(zoom_at(f, W / 2, H / 2, 1.0 + 0.6 * t), W / 2, H / 2, 28 * t)
        frames.append(f)
    # 3) iris z piasty kola na scenie RS5 do bialej karty (zoom przez piaste, nie wklejka)
    card = cv2.resize(cv2.imread(a.card), (W, H))
    hx, hy = [float(v) for v in a.hero_hub_end.split(",")]; hcx, hcy = hx * W, hy * H
    last = hero[-1]; n_iris = int(T_IRIS * FPS); R = math.hypot(W, H)
    for i in range(n_iris):
        t = ease_out((i + 1) / n_iris)
        bg = zoom_at(last, hcx, hcy, 1.0 + 2.5 * t)
        cz = zoom_at(card, W / 2, H / 2, 1.0 + 0.15 * (1 - t))
        mask = np.zeros((H, W), np.uint8)
        cv2.circle(mask, (int(hcx + (W / 2 - hcx) * t), int(hcy + (H / 2 - hcy) * t)), int(12 + R * t), 255, -1, cv2.LINE_AA)
        m = cv2.GaussianBlur(mask, (0, 0), 6).astype(np.float32)[..., None] / 255
        frames.append((cz * m + bg * (1 - m)).astype(np.uint8))
    # 4) karta: hold + jeden light sweep
    n_card = int(T_CARD * FPS)
    for i in range(n_card):
        f = card.copy().astype(np.float32)
        t = i / n_card
        if 0.15 < t < 0.55:
            p = (t - 0.15) / 0.40; x = int(-W * 0.3 + p * W * 1.6)
            sweep = np.zeros((H, W), np.float32)
            cv2.line(sweep, (x, 0), (x - 500, H), 1.0, 120)
            sweep = cv2.GaussianBlur(sweep, (0, 0), 50)[..., None]
            dark = (f.mean(2, keepdims=True) < 200).astype(np.float32)   # tylko na logo/tekscie
            f = f + sweep * dark * 90
        frames.append(np.clip(f, 0, 255).astype(np.uint8))
    tmp = tempfile.mkdtemp()
    for i, f in enumerate(frames):
        cv2.imwrite(os.path.join(tmp, f"{i:05d}.png"), f)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out], check=True)
    print(a.out, len(frames), "frames", round(len(frames) / FPS, 2), "s")

if __name__ == "__main__":
    main()

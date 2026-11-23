"""v3: miks programu -> audio/program_master.wav (48 kHz stereo, -14 LUFS, TP -1 dB).
Szyny: głos (vo.wav), dźwięk natywny ujęć (natywny.wav), muzyka (ściszana pod głosem), SFX syntetyczne z edl.json.
Użycie: python3 mix_v3.py <katalog projektu>"""
import sys, json, subprocess
import numpy as np
P = sys.argv[1]; SR = 48000
EDL = json.load(open(f'{P}/edl.json')); TL = json.load(open(f'{P}/timeline.json'))
T = TL['total']; N = int(T * SR)
rng = np.random.default_rng(7)

def load(f, ch=1):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'],
                                     capture_output=True, check=True).stdout, np.float32).copy()
    x = x.reshape(-1, ch) if ch > 1 else x
    out = np.zeros((N, ch) if ch > 1 else N, np.float32); n = min(N, len(x)); out[:n] = x[:n]; return out
def db(g): return 10 ** (g / 20)
def env_follow(x, att=0.01, rel=0.25):
    """Obwiednia głosu (RMS 20 ms, szybki atak, wolne puszczenie)."""
    hop = int(0.01 * SR); r = np.sqrt(np.convolve(x ** 2, np.ones(2 * hop) / (2 * hop), 'same'))[::hop]
    e = np.zeros_like(r); a, b = np.exp(-0.01 / att), np.exp(-0.01 / rel)
    for i in range(1, len(r)): e[i] = a * e[i - 1] + (1 - a) * r[i] if r[i] > e[i - 1] else b * e[i - 1] + (1 - b) * r[i]
    return np.interp(np.arange(N) / hop, np.arange(len(e)), e)

vo = load(f'{P}/audio/vo.wav'); nat = load(f'{P}/audio/natywny.wav'); mus = load(f'{P}/audio/muzyka_v3.mp3', 2)
# --- głos: lekka korekcja i kompresja w ffmpeg (bez zmiany barwy)
def ff(x, af):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', af, '-f', 'f32le', '-'],
                                        input=x.tobytes(), capture_output=True, check=True).stdout, np.float32)[:N].copy()
vo = ff(vo, 'highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2,acompressor=threshold=-22dB:ratio=3:attack=5:release=120:makeup=3')
vo = np.pad(vo, (0, N - len(vo)))

# --- muzyka: przycięcie, wejście po hooku mocniej, ducking pod głosem, wyciszenie na końcu
e = env_follow(vo); speech = np.clip((e - 0.01) / 0.03, 0, 1)
duck = db(-12 * speech)                                   # -12 dB pod mową
g = np.full(N, db(-16), np.float32)
t = np.arange(N) / SR
g *= np.where(t < 0.15, t / 0.15, 1)
g *= np.clip((T - t) / 2.6, 0, 1) ** 0.7 * 0.6 + 0.4 * np.clip((T - t) / 0.4, 0, 1)   # plansza: muzyka jeszcze gra, wycisza się w ostatnich ~0,4 s
mus = mus * (g * duck)[:, None]

# --- SFX syntetyczne
sfx = np.zeros(N, np.float32)
def add(x, at, gain=1.0):
    i = int(at * SR); j = min(N, i + len(x))
    if 0 <= i < N: sfx[i:j] += x[:j - i] * gain
def whoosh(d=0.42, up=True):
    n = int(d * SR); w = rng.standard_normal(n).astype(np.float32)
    # filtr pasmowy sweepowany: prosta implementacja przez ruchomy jednobiegunowy LP + HP
    fc = np.geomspace(400, 6000, n) if up else np.geomspace(6000, 400, n)
    y = np.zeros(n, np.float32); lp = 0.0; hp_prev = 0.0; hp = 0.0
    for k in range(n):
        a = 1 - np.exp(-2 * np.pi * fc[k] / SR); lp += a * (w[k] - lp)
        hp = 0.97 * (hp + lp - hp_prev); hp_prev = lp; y[k] = hp
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.6
    return y * env / (np.abs(y).max() + 1e-9)
def boom(d=1.2, f0=55):
    n = int(d * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * (f0 * tt + 30 * (1 - np.exp(-tt * 18)) / 18)) * np.exp(-tt * 3.2)
    x += 0.25 * rng.standard_normal(n) * np.exp(-tt * 40)
    return (x / np.abs(x).max()).astype(np.float32)
def pop(d=0.09, f=1500):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt * (1 - tt * 3)) * np.exp(-tt * 55)).astype(np.float32)
def click():
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return ((rng.standard_normal(n) * 0.6 + np.sin(2 * np.pi * 3200 * tt)) * np.exp(-tt * 300)).astype(np.float32)
def riser(d=1.6):
    n = int(d * SR); tt = np.arange(n) / SR
    x = rng.standard_normal(n) * (tt / d) ** 2 + 0.4 * np.sin(2 * np.pi * (200 * tt + 400 * tt ** 2 / d)) * (tt / d) ** 1.5
    x = np.convolve(x, np.ones(6) / 6, 'same')
    return (x / np.abs(x).max()).astype(np.float32)

W = whoosh(); WD = whoosh(0.32, up=False); B = boom(); Bs = boom(0.7, 70)
seg = {s['id']: s for s in TL['segments']}
for I in EDL['inserts']:
    tr = I.get('trans', 'whip')
    if I['id'] == 'hook_gt': add(B, 0.0, 0.55); continue
    if tr in ('whip', 'whipL'): add(W, I['t0'] - 0.2, 0.32)
    elif tr in ('zoom', 'bulge'): add(WD, I['t0'] - 0.12, 0.30); add(Bs, I['t0'], 0.20)
    elif I.get('layout') == 'split': add(WD, I['t0'] - 0.1, 0.22)
    if I['id'] == 'tile': add(click(), I['t0'] - 0.04, 0.5); add(pop(), I['t0'], 0.30)
add(B, 1.2, 0.35)        # „A TO JEST TURISMO”
add(riser(), seg['morph']['t0'] - 1.45, 0.18)                             # narasta przed pstryknięciem
add(B, seg['morph']['t0'] + 0.05, 0.6); add(W, seg['morph']['t0'] + 1.0, 0.30)   # transformacja loga
for tx in EDL['text']:                                                    # delikatny „tick” pod czerwone słowa
    if tx['font'] == 'anton' and tx.get('color', '').upper() == '#ED3B22': add(pop(0.07, 900), tx['t0'], 0.12)
add(Bs, seg['end']['t0'], 0.35)

# --- suma
mono = vo * 1.0 + nat * db(-4) + sfx
mix = mus + mono[:, None]
x = mix.astype(np.float32)
tmp = f'{P}/audio/_premix.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', tmp], input=x.tobytes(), check=True)
# dwuprzebiegowa normalizacja głośności
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-c:a', 'pcm_s24le', f'{P}/audio/program_master.wav'], check=True)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f'{P}/audio/program_master.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('\n'.join(r.strip().splitlines()[-12:]))

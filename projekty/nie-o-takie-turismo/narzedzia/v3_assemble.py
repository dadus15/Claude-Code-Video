"""v3: składa ścieżkę prowadzącego (presenter.mp4) i ścieżkę głosu (vo.wav) + timeline.json dla EDL renderera Kareemy.
Czas programu = czas finalnego spotu. Wstawki (strona, kafelki, realizacje, plansza) zasłaniają fragmenty „hold”.
Użycie: python3 v3_assemble.py <katalog v3>"""
import sys, os, json, subprocess
V3 = sys.argv[1]; K = f'{V3}/klipy'; VO = f'{V3}/glos/vo_final'; OUT = f'{V3}/montaz/projekt'; WORK = f'{OUT}/work'
os.makedirs(WORK, exist_ok=True); os.makedirs(f'{OUT}/audio', exist_ok=True); os.makedirs(f'{OUT}/footage', exist_ok=True)
FPS, W, H, SR = 24, 1080, 1920, 48000
SYNC = {'V2': -0.19, 'V3': 0.20, 'V4': 0.03, 'V6': -0.10, 'V7': 0.0, 'V8': 0.48, 'V9': 0.86, 'V10': 0.40, 'V11': 0.24}

# (id, typ, źródło, in, out | dur, [głos: (plik, in, out, przesunięcie względem startu segmentu)], dźwięk natywny: (od, do, gain) w czasie klipu)
def clip(sid, v, a, b, vo=(), nat=None): return dict(id=sid, kind='clip', src=f'{K}/{v}.mp4', v=v, a=a, b=b, vo=list(vo), nat=nat)
def hold(sid, dur, vo=()): return dict(id=sid, kind='hold', dur=dur, vo=list(vo))
def vo_at_clip(v, f, a, b, clip_in=0.0): return (f, a, b, SYNC[v] - clip_in)

SEG = [
    clip('hook', 'V1', 0.0, 2.4),                                   # pod wstawkami hooka
    clip('V1', 'V1', 1.0, 3.6, nat=(1.0, 3.6, 0.6)),
    clip('V2', 'V2', 0.0, 4.03, vo=[vo_at_clip('V2', 'N01_hook.wav', 0, 2.70)], nat=(3.55, 4.03, 1.0)),
    dict(id='morph', kind='frames', src=f'{V3}/montaz/work/morph', dur=42 / FPS),
    clip('V3', 'V3', 0.0, 4.6, vo=[vo_at_clip('V3', 'L02.wav', 0, 1.20)], nat=(1.5, 4.6, 0.9)),
    clip('V4', 'V4', 0.0, 7.4, vo=[vo_at_clip('V4', 'chunks/c04_hol.wav', 0, 6.19)]),
    clip('V5', 'V5', 2.5, 4.8, nat=(2.5, 4.8, 0.9)),
    clip('V6', 'V6', 0.0, 5.05, vo=[vo_at_clip('V6', 'N05_przegladarka.wav', 0, 9.00)]),
    hold('screen1', 9.00 - 0.10 - 5.05 + 0.25),
    clip('V7', 'V7', 0.0, 5.40, vo=[vo_at_clip('V7', 'N07_lista_C01.wav', 5.36, 10.50)]),
    clip('V8', 'V8', 0.0, 5.75, vo=[vo_at_clip('V8', 'L08.wav', 0, 5.06)]),
    hold('real_C01', 4.75, vo=[('N10_realizacje_C01.wav', 9.12, 11.34, 0.15), ('N10_realizacje_C01.wav', 14.96, 16.96, 0.15 + 2.22 + 0.14)]),
    clip('V9', 'V9', 0.0, 4.65, vo=[vo_at_clip('V9', 'L11.wav', 0, 6.04)]),
    hold('C19R_ring', 0.86 + 6.04 - 4.65 + 0.2),
    hold('real_C19R', 6.10, vo=[('L12.wav', 0, 5.82, 0.12)]),
    clip('V10', 'V10', 0.0, 6.0, vo=[vo_at_clip('V10', 'L13.wav', 0, 5.58)]),
    hold('real_RR', 4.95, vo=[('L15.wav', 0, 4.62, 0.12)]),
    clip('V11', 'V11', 0.0, 10.05, vo=[vo_at_clip('V11', 'chunks/c11_CTA.wav', 0, 9.56)], nat=(0.0, 1.1, 1.0)),
    hold('end', 2.6),
]

def run(cmd): subprocess.run(cmd, check=True)
VF = f'scale={W}:{H}:flags=lanczos,unsharp=5:5:0.55:5:5:0,fps={FPS}'
t = 0.0; parts = []; timeline = []
for i, s in enumerate(SEG):
    out = f'{WORK}/p{i:02d}.mp4'
    if s['kind'] == 'clip':
        dur = round((s['b'] - s['a']) * FPS) / FPS
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{s['a']:.4f}", '-i', s['src'], '-t', f'{dur:.4f}', '-vf', VF, '-an',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out])
    elif s['kind'] == 'frames':
        dur = s['dur']
        run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f"{s['src']}/m%03d.png", '-frames:v', '42', '-vf', f'fps={FPS}',
             '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out])
    else:   # hold: ostatnia klatka poprzedniego segmentu
        dur = round(s['dur'] * FPS) / FPS
        prev = parts[-1]
        run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.05', '-i', prev, '-frames:v', '1', f'{WORK}/last.png'])
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', f'{WORK}/last.png', '-t', f'{dur:.4f}',
             '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out])
    timeline.append(dict(id=s['id'], kind=s['kind'], t0=round(t, 4), t1=round(t + dur, 4), v=s.get('v'), a=s.get('a'), vo=s.get('vo', []), nat=s.get('nat')))
    parts.append(out); t += dur
TOTAL = t
open(f'{WORK}/concat.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{WORK}/concat.txt', '-c', 'copy', f'{OUT}/footage/presenter.mp4'])

# ---- głos + dźwięk natywny ujęć (osobne szyny, miks finalny robi mix_v3.py)
import numpy as np
def load(f, a=None, b=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', f'{a}'] if a else []) + ['-i', f] + (['-t', f'{b - (a or 0)}'] if b else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()
N = int((TOTAL + 1) * SR); vo = np.zeros(N, np.float32); nat = np.zeros(N, np.float32); vo_items = []
def put(bus, x, at, fade=0.012):
    f = int(fade * SR)
    if len(x) > 2 * f: x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(round(at * SR))
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x)); bus[i:j] += x[:j - i]
for s in timeline:
    for (f, a, b, off) in s['vo']:
        x = load(f'{VO}/{f}', a, b); at = s['t0'] + off
        put(vo, x, at); vo_items.append(dict(file=f, src_in=a, src_out=b, at=round(at, 3), seg=s['id']))
    if s.get('nat'):
        a, b, g = s['nat']; seg_in = s['a']
        x = load(f'{K}/{s["v"]}.mp4', a, b) * g; put(nat, x, s['t0'] + (a - seg_in), fade=0.03)
for nm, x in (('vo', vo), ('natywny', nat)):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', f'{OUT}/audio/{nm}.wav'], input=x.tobytes(), check=True)
json.dump(dict(total=round(TOTAL, 3), segments=timeline, vo_items=vo_items), open(f'{OUT}/timeline.json', 'w'), indent=1, ensure_ascii=False)
print('czas', round(TOTAL, 2), 's')
for s in timeline: print(f"{s['id']:10s} {s['t0']:7.2f}-{s['t1']:7.2f}")

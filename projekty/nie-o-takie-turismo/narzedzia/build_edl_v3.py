"""v3: buduje edl.json dla renderera talking-head-reels (styl Kareemy) z timeline.json i czasów słów.
Duże słowa: polskie cytaty (Anton / Playfair), napisy: angielskie, słowo po słowie.
Użycie: python3 build_edl_v3.py <katalog projektu> <katalog vo_final>"""
import sys, os, json, subprocess
P, VO = sys.argv[1], sys.argv[2]
TL = json.load(open(f'{P}/timeline.json')); WORDS = json.load(open(f'{VO}/words.json'))
SEG = {s['id']: s for s in TL['segments']}
REAL = os.path.relpath(os.path.join(os.path.dirname(os.path.dirname(P)), 'assety', 'realizacje'), P)
REFS = os.path.relpath(os.path.join(os.path.dirname(os.path.dirname(P)), 'assety', 'referencje_gt_ps5'), P)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)

def words_of(fname):
    """Słowa (tekst, start, koniec) pliku źródłowego głosu; obsługuje sklejone fragmenty c04/c11."""
    if fname == 'chunks/c04_hol.wav':
        a = WORDS['vo_final/N03_hol.wav']; off = dur(f'{VO}/N03_hol.wav') + 0.35
        return [tuple(w) for w in a] + [(w[0], w[1] + off, w[2] + off) for w in WORDS['vo_final/L04.wav']]
    if fname == 'chunks/c11_CTA.wav':
        return [(w[0], w[1] + 1.0, w[2] + 1.0) for w in WORDS['vo_final/L17.wav']]
    return [tuple(w) for w in WORDS['vo_final/' + fname]]

PW = []   # słowa w czasie programu
for it in TL['vo_items']:
    for (w, s, e) in words_of(it['file']):
        if it['src_in'] - 0.02 <= s < it['src_out']:
            PW.append(dict(w=w, s=round(it['at'] + s - it['src_in'], 3), e=round(it['at'] + e - it['src_in'], 3), seg=it['seg']))
PW.sort(key=lambda x: x['s'])
os.makedirs(f'{P}/analysis', exist_ok=True); json.dump([dict(w=x['w'], s=x['s'], e=x['e']) for x in PW], open(f'{P}/analysis/program_words.json', 'w'), indent=0, ensure_ascii=False)

def at(word, after=0.0, n=1):
    """Czas początku n-tego wystąpienia słowa (prefiks, bez wielkości liter) po czasie `after`."""
    k = 0
    for x in PW:
        if x['s'] >= after - 1e-3 and x['w'].lower().strip('.,!?–').startswith(word.lower()):
            k += 1
            if k == n: return x['s']
    raise KeyError(word)
def end(word, after=0.0):
    for x in PW:
        if x['s'] >= after - 1e-3 and x['w'].lower().strip('.,!?–').startswith(word.lower()): return x['e']
    raise KeyError(word)
S = lambda k: SEG[k]['t0']; E = lambda k: SEG[k]['t1']

text, inserts, zoom = [], [], []
def big(t, t0, y, size=190, color='#FFFFFF', t1=None, keep=False):
    text.append(dict(font='anton', text=t, t0=round(t0, 3), t1=round(t1 or t0 + 1.0, 3), y=y, size=size, color=color, anim='build', keep_t1=keep))
def serif(t, t0, y, size=140, t1=None, keep=False):
    text.append(dict(font='serif', text=t, t0=round(t0, 3), t1=round(t1 or t0 + 1.0, 3), y=y, size=size, anim='soft', tracking=-40, keep_t1=keep, shadow=True))
def label(t, t0, t1, y, size=70):
    text.append(dict(font='sub', text=t, t0=round(t0, 3), t1=round(t1, 3), y=y, size=size, anim='pop', shadow=True, keep_t1=True))
def en(t, t0, t1, y=1330, size=80):
    """Angielski napis słowo po słowie, pocięty na krótkie linie (jedna linia naraz)."""
    ws = t.split(); lines, cur = [], []
    for w in ws:
        if cur and len(' '.join(cur + [w])) > 24: lines.append(cur); cur = []
        cur.append(w)
    lines.append(cur)
    tot = sum(len(' '.join(l)) for l in lines); span = max(0.4, t1 - t0); t = t0
    for k, l in enumerate(lines):
        d = span * len(' '.join(l)) / tot; n = len(l)
        wt = [round(t + (d - 0.1) * i / n, 3) for i in range(n)]
        last = k == len(lines) - 1
        text.append(dict(font='sub', text=' '.join(l), t0=round(t, 3), t1=round(t1 + 0.2 if last else t + d - 0.02, 3), y=min(y, 1340), size=size,
                         anim='words', wt=wt, shadow=True, keep_t1=True, color='#FFFFFF', fadeout=last))
        t += d
def ins(id_, t0, t1, kind='full', trans='whip', flash='invert', layout='full', **kw):
    d = dict(id=id_, t0=round(t0, 3), t1=round(t1, 3), kind=kind, trans=trans, flash=flash, layout=layout); d.update(kw); inserts.append(d)
def still(src, dur_=None, z=(1.0, 1.10), fx=0.5):
    c = dict(src=src, t_in=0.0, zoom=list(z), fx=fx, color=True)
    if dur_: c['dur'] = dur_
    return c
def clipc(src, t_in=0.0, z=(1.0, 1.04), speed=1.0):
    return dict(src=src, t_in=t_in, zoom=list(z), color=True, speed=speed)

# ---------------- HOOK 0–2.42: kontrast dwóch „Turismo”
ins('hook_gt', 0.0, 1.2, trans='cut', flash=None, clips=[still(f'{REFS}/ref_gt7_gtauto.jpg', z=(1.15, 1.35), fx=0.42)])
big('TO JEST', 0.06, 900, 210, keep=True, t1=1.2); serif('Turismo', 0.32, 1080, 170, keep=True, t1=1.2)
ins('hook_c01', 1.2, 2.42, trans='whip', flash='invert', clips=[still(f'{REAL}/C01/BMW-M4-G83-TURISMO-FORGED-C01-SATIN-BRONZE_06-scaled.jpg', z=(1.05, 1.25), fx=0.5)])
big('A TO JEST', 1.22, 860, 190, keep=True, t1=2.42); big('TURISMO', 1.45, 1050, 230, color='#ED3B22', keep=True, t1=2.42)
zoom += [[0.0, S('V2'), 'wide']]

# ---------------- V2: kanapa
z0 = S('V2'); zoom += [[z0, S('morph'), 'tight']]
serif('innego', at('innego'), 960, 140, t1=S('morph'), keep=True); big('TURISMO', at('turizmu') - 0.05 if any(x['w'].lower().startswith('turizm') for x in PW) else at('Turismo', z0), 1150, 200, t1=S('morph'), keep=True)
en('Bet everyone expected a different Turismo.', at('Chyba') - 0.05, end('turizmu') if any(x['w'].lower().startswith('turizm') for x in PW) else z0 + 2.6, y=1310)

# ---------------- morph + V3 wejście
zoom += [[S('morph'), S('V4'), 'wide']]
serif('od razu', at('od', S('V3')), 960, 140, t1=at('od', S('V3')) + 1.5, keep=True); big('LEPIEJ', at('lepiej', S('V3')), 1160, 210, t1=at('od', S('V3')) + 1.6, keep=True)
en('Now, that’s better.', at('No', S('V3')) - 0.05, end('lepiej', S('V3')), y=1320)

# ---------------- V4 hol
t_proj = at('projektujemy', S('V4')); t_ind = at('indywidualne', S('V4')); t_ch = at('Chodźcie', S('V4'))
big('PROJEKTUJEMY', t_proj, 1150, 160, t1=t_ind - 0.05, keep=True); serif('na indywidualne\nzamówienie', t_ind, 1050, 120, t1=t_ch - 0.1, keep=True)
en('At Turismo Wheels we design', at('W', S('V4')), t_ind - 0.05, y=1330)
en('wheels made to order.', t_ind, end('zamówienie', S('V4')), y=1330)
serif('pokażę wam', at('pokażę', S('V4')), 930, 120, t1=E('V4'), keep=True); big('GAMĘ', at('gamę', S('V4')), 1160, 220, t1=E('V4'), keep=True)
en('Come on, let me show you our range.', t_ch, end('gamę', S('V4')), y=1330)
zoom += [[S('V4'), S('V6'), 'wide']]

# ---------------- V6 laptop + przeglądarka (split), potem nawigacja (pełny)
ins('browser', S('V6') + 0.35, S('screen1'), layout='split', trans='cut', flash='invert', clips=[clipc('broll/i_browser_type.mp4', 0.0)])
en('In the browser we type turismo-wheels.com,', at('W', S('V6')) - 0.05, at('następnie', S('V6')) - 0.3, y=960)
ins('site_nav', S('screen1'), E('screen1'), layout='split', trans='cut', flash='invert', clips=[clipc('broll/i_site_nav.mp4', 0.0)])
serif('felgi aluminiowe', at('felgi', S('V6')), 690, 110, t1=at('customowe', S('V6')), keep=True)
big('FELGI KUTE', at('customowe', S('V6')), 850, 170, color='#ED3B22', t1=E('screen1'), keep=True)
en('then under Aluminium Wheels we pick custom forged wheels.', at('następnie', S('V6')) - 0.1, E('screen1') - 0.15, y=960)

# ---------------- V7: lista → C01 → kafelek → BESTSELLER
t_c01 = at('C01', S('V7')); t_best = at('bestsellerem', S('V7'))
ins('list', S('V7'), t_c01 - 0.35, layout='split', trans='cut', flash=None, clips=[clipc('broll/i_site_list.mp4', 0.0)])
zoom += [[S('V6'), t_best, 'tight']]
ins('tile', t_c01, t_best - 0.05, layout='split', trans='zoom', flash='invert', clips=[clipc('broll/i_tile_C01.mp4', 0.0)])
big('C01', t_c01, 860, 200, t1=t_best - 0.05, keep=True)
en('Here we have, for example, the C01,', at('Mamy', S('V7')) - 0.05, t_c01 + 0.5, y=960)
en('which is our bestseller.', at('który', S('V7')), end('bestsellerem', S('V7')), y=1330)
zoom += [[t_best, S('V8'), 'wide']]
serif('nasz', t_best - 0.05, 980, 120, t1=E('V7'), keep=True); big('BESTSELLER', t_best, 1150, 190, color='#ED3B22', t1=E('V7'), keep=True)

# ---------------- V8: cechy C01
t_deep = at('deep', S('V8')); t_agr = at('agresywnymi', S('V8')); t_frez = at('frezowanymi', S('V8'))
zoom += [[S('V8'), t_deep, 'tight']]
en('It stands out with a really', at('Ten', S('V8')) - 0.05, t_deep - 0.1, y=1330)
ins('c01_cechy', t_deep - 0.3, E('V8'), trans='bulge', flash='invert', clips=[clipc('broll/i_C01_cechy.mp4', 0.0)])
big('DEEP CONCAVE', t_deep, 1150, 170, t1=t_agr - 0.05, keep=True)
serif('agresywne linie', t_agr, 1150, 130, t1=t_frez - 0.05, keep=True)
big('FREZOWANE DETALE', t_frez, 1150, 130, color='#ED3B22', t1=E('V8'), keep=True)
en('deep concave, aggressive lines and milled details.', t_deep, E('V8') - 0.2, y=1300)

# ---------------- realizacje C01
r0, r1 = S('real_C01'), E('real_C01'); t_bmw = at('BMW', r0); t_uw = at('uważam', r0)
ins('real_C01', r0, r1, trans='whip', flash='invert', clips=[
    still(f'{REAL}/C01/BMW-M4-G83-TURISMO-FORGED-C01-SATIN-BRONZE_03-scaled.jpg', 1.25, fx=0.55),
    still(f'{REAL}/C01/BMW-M4-G83-TURISMO-FORGED-C01-SATIN-BRONZE_05-scaled.jpg', 1.05, fx=0.58),
    still(f'{REAL}/C01/FERRARI-F8-TURISMO-FORGED-C01-GLOSS-BLACK_06.jpg', 1.2, fx=0.4),
    still(f'{REAL}/C01/FERRARI-F8-TURISMO-FORGED-C01-GLOSS-BLACK_08.jpg', None, fx=0.5)])
big('BMW M4', t_bmw, 900, 190, t1=r0 + 2.3, keep=True); label('C01 · Satin Bronze', t_bmw + 0.3, r0 + 2.3, 1040, 62)
big('FERRARI F8', r0 + 2.3, 900, 180, t1=r1, keep=True); label('C01 · Gloss Black', r0 + 2.55, r1, 1040, 62)
en('Here’s a BMW M4,', at('Mamy', r0) - 0.05, end('M4', r0), y=1180)
en('and I think it looks truly exciting.', t_uw, r1 - 0.1, y=1180)

# ---------------- V9: C19-R + aero-ring
t_c19 = at('C19R', S('V9')); t_now = at('nowsza', S('V9')); t_ze = at('ze', S('V9'))
zoom += [[S('V9'), t_ze, 'wide']]
big('C19-R', t_c19, 1180, 220, t1=t_now - 0.05, keep=True); serif('nowsza wersja C19', t_now, 1180, 120, t1=t_ze - 0.05, keep=True)
en('Next up: the C19-R,', at('Kolejny', S('V9')) - 0.05, t_now - 0.1, y=1360)
en('a newer version of the C19', t_now, t_ze - 0.05, y=1360)
ins('c19r_ring', t_ze - 0.1, E('C19R_ring'), trans='zoom', flash='invert', clips=[clipc('broll/i_C19R.mp4', 0.0)])
serif('zintegrowany', t_ze, 980, 120, t1=E('C19R_ring'), keep=True); big('AERO-RING', at('zintegrowanym', S('V9')) + 0.2, 1140, 190, color='#ED3B22', t1=E('C19R_ring'), keep=True)
en('with an integrated aero ring.', t_ze, E('C19R_ring') - 0.1, y=1300)

# ---------------- realizacje C19-R (Audi RS5)
a0, a1 = S('real_C19R'), E('real_C19R'); t_audi = at('Audi', a0); t_agr2 = at('agresywnie', a0)
ins('real_C19R', a0, a1, trans='whip', flash='invert', clips=[
    still(f'{REAL}/C19-R/AUDI-RS5-C19-R_02.jpg', 2.0, fx=0.42), still(f'{REAL}/C19-R/AUDI-RS5-C19-R_01.jpg', 2.0, fx=0.55),
    still(f'{REAL}/C19-R/AUDI-RS5-C19-R_03.jpg', None, fx=0.45)])
big('AUDI RS5', t_audi, 900, 200, t1=t_agr2 - 0.3, keep=True); label('C19-R', t_audi + 0.3, t_agr2 - 0.3, 1040, 70)
serif('naprawdę', t_agr2 - 0.3, 860, 120, t1=a1, keep=True); big('AGRESYWNIE', t_agr2, 1010, 180, color='#ED3B22', t1=a1, keep=True)
en('Here’s an Audi RS5 on C19-R,', at('Mamy', a0) - 0.05, at('i', at('C19R', a0)) - 0.05, y=1180)
en('and I think it looks seriously aggressive.', at('uważam', a0), a1 - 0.1, y=1180)

# ---------------- V10: RR + gravity cap
t_rr = at('RR', S('V10')); t_kl = at('klasyka', S('V10')); t_id = at('idealny', S('V10')); t_rot = at('rotacyjnym', S('V10'))
zoom += [[S('V10'), t_rot, 'tight']]
big('RR', t_rr, 1180, 260, t1=t_kl - 0.02, keep=True); serif('klasyka', t_kl, 1180, 170, t1=t_id - 0.05, keep=True)
en('And the RR, a classic.', at('No', S('V10')) - 0.05, t_id - 0.1, y=1360)
serif('dla luksusowych\nlimuzyn', t_id, 1060, 120, t1=t_rot - 0.05, keep=True)
en('Perfect for luxury saloons,', t_id, t_rot - 0.05, y=1360)
ins('rr_gravity', t_rot - 0.15, E('V10'), trans='bulge', flash='invert', clips=[clipc('broll/i_RR_gravity.mp4', 0.0)])
big('GRAVITY CAP', at('Gravity', S('V10')) - 0.2, 1150, 170, color='#ED3B22', t1=E('V10'), keep=True)
en('with a floating gravity cap.', t_rot, E('V10') - 0.1, y=1300)

# ---------------- realizacje RR
b0, b1 = S('real_RR'), E('real_RR'); t_i7 = at('BMW', b0); t_mer = at('Mercedesa', b0)
ins('real_RR', b0, b1, trans='whip', flash='invert', clips=[
    still(f'{REAL}/RR/BMW-i7-G70-RR_01.jpg', 1.2, fx=0.5), still(f'{REAL}/RR/BMW-i7-G70-RR_10.jpg', t_mer - b0 - 1.2, fx=0.35),
    still(f'{REAL}/RR/MERCEDES-S-COUPE-RR-SILVER-BRUSHED_06.jpg', 1.3, fx=0.55), still(f'{REAL}/RR/MERCEDES-S-COUPE-RR-SILVER-BRUSHED_09.jpg', None, fx=0.6)])
big('BMW i7', t_i7, 900, 200, t1=t_mer - 0.05, keep=True)
big('MERCEDES', t_mer, 860, 180, t1=b1, keep=True); serif('S Coupé', t_mer + 0.25, 1030, 130, t1=b1, keep=True)
en('Here’s a BMW i7 and a Mercedes S Coupé on RR.', at('Mamy', b0) - 0.05, b1 - 0.15, y=1180)

# ---------------- V11: CTA (zawsze przed prowadzącym)
c0 = S('V11'); t_nam = at('namiastka', c0); t_zap = at('Zapraszam', c0); t_cen = at('cennika', c0); t_poz = at('pozostałych', c0)
t_zap2 = at('Zapraszam', t_poz); t_str = at('Strzała', c0)
zoom += [[c0, t_zap, 'wide'], [t_zap, t_str, 'tight'], [t_str, E('V11'), 'wide']]
serif('to tylko', at('To', c0) - 0.05, 960, 130, t1=t_zap - 0.1, keep=True); big('NAMIASTKA', t_nam, 1160, 190, t1=t_zap - 0.1, keep=True)
en('This is just a taste of what we offer.', at('To', c0) - 0.05, t_zap - 0.15, y=1320)
label('zapraszam po', t_zap, t_str - 0.1, 1010, 74); big('CENNIK', t_cen, 1150, 220, color='#ED3B22', t1=t_str - 0.1, keep=True)
en('Get in touch for pricing and all the project details.', t_zap, t_zap2 - 0.1, y=1320)
big('STRZAŁA!', t_str - 0.05, 1150, 230, color='#ED3B22', t1=E('V11'), keep=True)
en('See you. Cheers!', t_zap2, E('V11') - 0.2, y=1320)

# ---------------- plansza końcowa
ins('end', S('end'), E('end'), trans='zoom', flash='invert', clips=[clipc('broll/i_plansza.mp4', 0.0, z=(1.0, 1.02))])
zoom += [[S('end'), E('end') + 0.01, 'wide']]

# napisy: jedna linia naraz
subs = sorted([t for t in text if t['anim'] == 'words'], key=lambda t: t['t0'])
for a_, b_ in zip(subs, subs[1:]):
    if a_['t1'] > b_['t0'] - 0.02: a_['t1'] = round(b_['t0'] - 0.02, 3)
# porządek, nachodzenie wstawek
inserts.sort(key=lambda i: i['t0'])
for a_, b_ in zip(inserts, inserts[1:]):
    if a_['t1'] > b_['t0']: a_['t1'] = b_['t0']
zoom.sort(key=lambda z: z[0]); clean = []
for z in zoom:
    if clean and z[0] < clean[-1][1]: clean[-1][1] = z[0]
    clean.append(z)
edl = dict(name='TurismoV3', W=1080, H=1920, fps=24, accent='#ED3B22', audio='audio/program_master.wav', zoom=clean,
           inserts=inserts, text=text, look=dict(halftone='assets/halftone_1080x1920.png', halftone_opacity=18, vignette=36, grain=4),
           fonts=dict(anton='Anton-Regular', serif='PlayfairDisplay-Bold', didot='PlayfairDisplay-Regular', sub='Inter-SemiBold'),
           presenter=dict(framing=dict(tight=dict(scale=1.22, face_y=0.33), wide=dict(scale=1.0125, face_y=0.30), half=dict(scale=1.0, face_y=0.05))))
json.dump(edl, open(f'{P}/edl.json', 'w'), indent=1, ensure_ascii=False)
print('wstawek', len(inserts), 'tekstów', len(text), 'zoom', len(clean))

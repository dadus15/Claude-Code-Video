# Analiza v2: oryginał klatka po klatce (pomiar, nie oko)

Materiał: 484 klatki nagrania ekranu (330 unikalnych, efektywnie 24 fps). Właściwy klip ma **12,95 s ≈ 311 klatek przy 24 fps**, a potem TikTok go zapętla.
Metody: śledzenie punktów na asfalcie (Lucas-Kanade), slit-scan bieżnika, tła i asfaltu, template matching lusterka, korelacja kołowa obrotu felgi.

Pliki: `oryginal_fazy_ruchu.png` (klatki graniczne faz), `slitscan_kolo.png`, `slitscan_tlo.png`, `slitscan_asfalt.png`.

## 1. Kamera (CAM-RIG)
- **Sztywno przykręcona do karoserii.** Lusterko przez cały klip zmienia pozycję w kadrze o ≤ 14 px na 234 px (<6%): drobny, płynny „sag” uchwytu w 2–7 s, potem wraca.
- **Pozycja: przedni LEWY narożnik auta** (zderzak/przód błotnika), ok. 5–10 cm na zewnątrz karoserii i bardzo nisko (~15 cm). **Patrzy DO TYŁU** wzdłuż lewego boku na **przednie lewe koło**.
  Dowody: w lewym górnym rogu widać krawędź reflektora, lusterko jest *za* kołem (prawa góra kadru), dalej bok auta ucieka w głąb. Przy cofaniu asfalt płynie *do* kamery, przy jeździe w przód ucieka *od* niej.
- Obiektyw ultraszeroki (action-cam), lekka beczka, głęboka ostrość. Lekki dutch tilt, horyzont nisko (~55% wysokości kadru).
- Kompozycja 9:16 (stała przez cały klip):
  - lewe ~25% szerokości: przód błotnika/zderzaka w kolorze auta, pionowa krawędź nadkola przy x≈23%;
  - koło: środek przy x≈61%, y≈56%; koło z oponą zajmuje ~55% szerokości i ~47% wysokości;
  - prawa góra: lusterko (x≈70%, y≈35%), bok auta ucieka w prawo;
  - górne ~30%: jasne, zachmurzone niebo, latarnie, na horyzoncie ciemne góry;
  - dolne ~15%: asfalt, od ~7,5 s białe linie parkingowe.

## 2. Oś czasu ruchu (24 fps)
| Faza | Czas | Klatki | Co się dzieje | Pomiar |
|---|---|---|---|---|
| P0 | 0,00–0,40 s | 0–9 | Postój. Koła **skręcone w LEWO do oporu**, do kamery zwrócony bieżnik, felgi nie widać | asfalt 0 px/s |
| P1 | 0,40–2,40 s | 10–58 | **COFANIE** na lewym skręcie. Płynne ruszenie, max ~1,0 s, wyhamowanie do zera przy 2,4 s. Bieżnik obraca się „do tyłu”, asfalt płynie w dół/prawo (do kamery), niebo dryfuje w lewo (auto lekko zawraca) | asfalt do ~140 px/s, niebo −10 px/s |
| P2 | 2,40–3,10 s | 58–74 | **Stop, pauza 0,7 s**. Ruszają się tylko chmury | asfalt ≈ 0 |
| P3 | 3,10–5,10 s | 74–122 | **Skręt kół z lewej do prawej** (lock-to-lock, ~2,0 s, ease-in-out), auto stoi. 3,5 s: pojawia się rant; 4,2 s: pół felgi; 4,8–5,1 s: pełny front felgi. Felga się NIE obraca | asfalt ≈ 0 |
| P4 | 5,10–5,90 s | 122–142 | **Pauza 0,8 s** na pełnym widoku felgi (w audio cisza przed dropem 5,0–5,5 s) | 0 |
| P5 | 5,90–12,95 s | 142–311 | **Jazda DO PRZODU na prawym skręcie.** Rozpędzanie 5,9→~8,5 s, potem prawie stała prędkość ~0,5 obr/s (≈1,1 m/s, tempo spaceru). Asfalt i linie uciekają w górę (od kamery), latarnie maleją ku horyzontowi, auto skręca w prawo. **Drop basu ≈ 6,0 s = moment ruszenia** | obrót felgi 0→~190°/s |
| Pętla | 12,95 s | → 0 | Twarde cięcie na P0 (opona): hook wraca | |

Kierunki zgadzają się z fizyką. Cofanie z kołami w lewo daje obrót auta w prawo (CW), jazda w przód z kołami w prawo też daje CW, więc niebo dryfuje w lewo w obu fazach ruchu ✔.

## 3. Co było źle w mojej animacji v1 (do wyrzucenia)
1. Kamera za kołem patrzyła do przodu, z prawej strony auta. Powinna stać przed kołem, patrzeć do tyłu, z lewej strony.
2. Auto stało w 0–3,3 s. W oryginale **cofa** (0,4–2,4 s), a potem stoi.
3. Nie było pauz P2 (0,7 s) i P4 (0,8 s), a to one budują napięcie i synchronizację z muzyką.
4. Skręt v1 trwał 1,3 s. W oryginale **~2,0 s**, z miękkim dojściem do oporu.
5. Jazda ruszała już w trakcie odsłaniania. W oryginale rusza dopiero po pauzie, **na dropie (5,9–6,0 s)**, i to **do przodu**.
6. Kadr: w v1 koło było za małe i za daleko. Powinno zajmować ~55% szerokości, a przód błotnika ~25% z lewej.

## 4. Skill: cinedance-block-library (wybrany)
Reguła „jeden trik na wideo” plus blok **CAM-RIG**: obiekt stoi w kadrze, rusza się świat. Ten opis 1:1 pasuje do oryginału.
Bloki: `CAM-RIG` · `OPT-WIDE` · `GRADE-BRIGHT` · `GRADE-LOCK` · `LIVING-BACKGROUND` (tylko chmury, bez ptaków) · `PEOPLE-LAW` (zero ludzi) · `CONTAMINATION` · `COUNT` · `FAIL` · `SOUND` · `STOP-BASE` (z wyjątkiem logo na dekielku, jeśli felga je ma) · `STOP-INVERSION`.
Bez bloków postaci (FACE/BODY/ACTING/TASK/MODEST), bo w kadrze nie ma człowieka. `NO-FREEZING` zastąpiony regułą „pauzy P2/P4 są zamierzone, ruszają się tylko chmury”.

### Brief (do uzupełnienia assetami)
```
TRICK: kamera przykręcona do przedniego lewego narożnika auta, 15 cm nad asfaltem, patrzy do tyłu na przednie lewe koło;
       koło i karoseria NIGDY nie ruszają się w kadrze — rusza się świat (asfalt, linie, latarnie, niebo), a koło tylko skręca i się toczy
FORMAT: 13 s (311 kl. @24 fps), jedno ujęcie bez cięć, 9:16, bez muzyki (muzyka w TikToku), pętla
ASSETS: @1 = auto [DO DOSTARCZENIA], @2 = felga kuta custom [DO DOSTARCZENIA], @3 = prowadnica ruchu z Blendera (tylko ruch i kadr, nie wygląd)
MAIN: (1) oś czasu P0–P5 co do klatki; (2) wzór felgi identyczny z @2 w każdej klatce
FAIL: felga zmienia liczbę ramion / kształt podczas obrotu; kamera „odkleja się” od auta; auto jedzie w złą stronę
COUNT: 1 auto, 1 koło w kadrze, [N] ramion felgi, [5] śrub, 0 ludzi
BLOCKS: CAM-RIG OPT-WIDE GRADE-BRIGHT GRADE-LOCK LIVING-BACKGROUND PEOPLE-LAW CONTAMINATION COUNT FAIL SOUND STOP-BASE STOP-INVERSION
```

## 5. Plan produkcji v2 (po otrzymaniu assetów)
1. Blender (3D Jutsu, 0 kr): nowe auto (przód + lewy bok) i nowa felga wg assetów, rig kamery z pkt 1, animacja co do klatki wg tabeli z pkt 2.
   Kontrola: porównanie side-by-side z oryginałem (slit-scan + klatki graniczne) **przed** jakąkolwiek generacją.
2. Seedance 2.5 `video_edit` (fotorealizm): szkic 480p (~46 kr), potem 1080p (~259 kr), wyłącznie po akceptacji.

# Blender: C01 z ekranu na rolki, obrót, gama C01 → C19-R → RR

Plik: `blender/scena_c01.py` (parametryczny, Blender 4.0+).
```bash
blender -b -P scena_c01.py -- --stills --finish brushed_grey
```
```bash
blender -b -P scena_c01.py -- --preview
```
```bash
blender -b -P scena_c01.py -- --wheel /sciezka/C01.obj --stills
```

## Co robi Blender w tym spocie (0 kredytów)
| Zadanie | Dlaczego Blender, a nie AI |
|---|---|
| Felga C01 we wszystkich ujęciach produktu | ta sama geometria w każdej klatce, liczba ramion nie pływa |
| Ortograficzny render „jak zdjęcie katalogowe” | pod kciukiem (U8) podmiana obrazu 2D → 3D jest niewidoczna, bo oba obrazy pokrywają się 1:1 |
| Tor wyjęcia: ekran → powietrze → rolki | skala od 0,19 do 1:1 (z 10 cm na stronie do 54 cm) kończy się przed lotem nad podstawkę |
| Styk na **dwóch** rolkach i obrót | piasta stoi; rolki kręcą się przeciwnie z przełożeniem R/r = 9:1, policzonym w skrypcie |
| Zbliżenia cech C01 (U9) | macro, refleks prowadzony po ramieniu, ta sama faza obrotu we wszystkich ujęciach |
| Plansza końcowa | C01 dokładnie w miejscu i rozmiarze felgi z gry (pętla) |
| Okno detalu | ten sam obrót z drugiej kamery, idealnie zsynchronizowany |

## Gama trzech modeli (v2.1)
```bash
blender -b -P scena_c01.py -- --models C01,C19-R,RR --files C01.obj,C19R.obj,RR.obj --swap
```
- Wszystkie modele wiszą pod jednym obracanym punktem (pivot), więc pozycja, faza i kierunek obrotu są wspólne.
- Profil obrotów liczony klatka po klatce: pchnięcie 1,4 obr./s z wygaszaniem do 0,35; przy każdej podmianie krótki szczyt do ok. 5 obr./s (kl. 245 i 320). Model zmienia się w klatce szczytu, a rozmycie ruchu (migawka 0,5) zlewa ramiona w dysk.
- Rolki zawsze kręcą się przeciwnie z przełożeniem 9:1.
- Bez plików CAD każdy model dostaje **inną felgę zastępczą** (C01: 5 podwójnych ramion, C19-R: 10 prostych + grubszy pierścień, RR: 5 × 3 cienkie). Dzięki temu podmiana jest widoczna w podglądzie, ale to nie są wzory Turismo.

## Stan
- ✅ Scena: stolik, laptop z matrycą, ściana z lameli jak tło @STAND, podstawka z dwiema rolkami (bez napisów), światło biurowe, refleks z boku, czerwony akcent.
- ✅ Choreografia (200 kl. = 8 s): kl. 1–17 felga na ekranie (11–17 to kciuk i podmiana), 17–63 wyjście i wzrost skali, do 101 lot nad rolki, 116 styk, 126 pchnięcie, potem obrót z wygaszaniem.
- ✅ Render kontrolny K1–K4 + podgląd animacji (`plansze/BL_*.png`, `plansze/BL_podglad_U8.mp4`).
- ⚠️ **Felga jest ZASTĘPCZA** (5 podwójnych ramion). To nie jest geometria C01.

## Geometria C01 — czego potrzebuję (jedno z dwóch)
1. **CAD C01** (OBJ / FBX / GLB / STEP) — najlepiej.
   - Na Drive jest CAD tylko dla **C26** (folder `Computex_C26`: OBJ + PRT + DWG) i **C11** (`C11 21105.obj`).
   - Nazwa folderu sugeruje producenta „Computex”. Warto poprosić go o C01 w tym samym formacie.
   - Skrypt sam wyśrodkuje model, przeskaluje go do 54 cm i ustawi oś obrotu.
2. **Odbudowa C01 w Blenderze z packshotów**. Wystarczą trzy pliki z Drive (folder `C01`):
   - `TURISMO_FORGED_C1_TR42_BRUSHED GREY_FRONT_.png`
   - `TURISMO_FORGED_C1_TR42_BRUSHED GREY_SIDE_.png`
   - `TURISMO_FORGED_C1_TR42_BRUSHED GREY_ANGLE_.png`

   **Załącz je w czacie.** Mają 9–10 MB, a narzędzie Drive w tej sesji nie przenosi tak dużych plików do kontenera. Przód odwzoruję wiernie. Głębokość ramion odczytam z SIDE/ANGLE z dokładnością „na oko”, czego nie zrobię przy CAD.

Wykończenia C01 na Drive: Satin Black (TR02), Brushed Deep Black (TR40), **Brushed Grey (TR42)**, Brushed Bronze (TR48). Domyślnie biorę Brushed Grey, bo najlepiej czyta się na czarno-czerwonym tle. Zmiana to jeden parametr: `--finish`.

## Ograniczenie mocy w tej sesji
Kontener ma 4 CPU, nie ma GPU, a Blender z Ubuntu nie ma denoisera. Klatka 720×1280 przy 64 próbkach to ok. 40 s, a finałowe 1080×1920 kosztowałoby kilka minut na klatkę. Około 20 s produktu oznacza godziny liczenia.
- **Testy i podglądy** renderuję tutaj.
- **Finał** najlepiej policzyć na komputerze z kartą graficzną: ten sam skrypt i `.blend`, z denoiserem. Alternatywnie liczę tutaj w 720p z wyłączonymi ujęciami bez felgi.

## Dopasowanie do klipu AI z dłońmi (U8)
1. Klatki AI w salonie mają znaną geometrię: stolik 45 cm, rolki co 22 cm, felga 54 cm. Kamerę Blendera dopasowuję do KF-U5 po tych wymiarach (ręcznie albo fSpy).
2. Render C01 z kanałem alfa + przebieg cienia (shadow catcher na stoliku) + odbicie pokoju w metalu.
3. Roto kciuka zawsze **nad** felgą, palce **za** rantem. W AI dłonie trzymają proxy (ciemnoszary krążek), więc roto jest proste.

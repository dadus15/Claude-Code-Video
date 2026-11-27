# Montaż rolki: Turismo Forged C26 × Mercedes-Benz S 560 (W222), zima

Skrypt: `edit/compose_w222.py` (9:16, 1080×1920, 24 fps, 18,4 s, bez lektora). Wejście `--rig` to prowadnica z Blendera (animatik), a po akceptacji wideo z Seedance w tym samym kadrze i timingu.
Muzykę dodajemy w TikToku (trend). Wybierz utwór z dropem i ustaw drop na **2,08 s**.

| Czas (s) | Segment | Co widać | Styl (Karima) |
|---|---|---|---|
| 0,00–1,50 | **HOOK** | Opona → skręt (1,5×) → lico 40 szprych prosto w obiektyw; uderzenie 110→100 % na 1. klatce, potem wolny push | hook bez cięcia; słowo kluczowe w szeryfie „Forty spokes.” (kremowe) przy pełnym widoku felgi |
| 1,50–1,75 | Przejście | Śnieżny podmuch z piasty i biały flash | zimowa wersja „złotego płynu” → biel → dalsza część ujęcia |
| 1,58–9,45 | Rig shot | Pauza na licu, **2,08 s ruszenie = DROP**, jazda na prawym skręcie, reflektor w lewym górnym rogu | tytuł TURISMO FORGED C26 / BRUSHED SILVER (maska, cubic ease-out) |
| 9,00–9,58 | Przejście | Push w piastę i narastające rozmycie obrotowe → biały flash | ukryte cięcie w jasności |
| 9,58–10,08 | Match cut | Zdjęcie _12: felga w tym samym punkcie kadru, rozmycie gaśnie (koło „dokręca się” do zatrzymania) | match cut |
| 10,08–11,58 | **Strobe** | 6 zdjęć realizacji po 0,25 s (_04, _01, _08, _05, _10, _02), piasta zawsze w tym samym punkcie, punch-in 4 % | strobe na bit (2 uderzenia/s, ok. 120 BPM) |
| 11,58–14,08 | Hero | _07 (przód, reflektor, tablica TURISMO): kadr B&W → tytuł → kolor wraca | tytuł „STEP” na odbarwionym kadrze |
| 14,08–14,88 | Iris | Iris z piasty koła w białą kartę | przejście przez piastę |
| 14,88–18,38 | Karta | Logo → **czapka Mikołaja spada na znak T** (0,55 s, bez odbicia, puch śniegu przy lądowaniu) → UNLOCK YOUR STYLE → model → Daniel Chmielewski, telefon, e-mail; prószy śnieg | elementy wskakują po kolei, jeden light sweep |

Czapka: model 3D w Blenderze (`edit/w222/santa_hat.py`): aksamitny stożek z fałdami, futro z cząsteczek (włosy), pompon, render Cycles na przezroczystym tle (`edit/w222/santa_hat.png`).
Pozycje piast na zdjęciach: `edit/w222/hubs_photos.json` (Hough + korekta ręczna). Pozycja piasty w prowadnicy dla każdej klatki: `edit/w222/rig_hub.json` (rzut z kamery Blendera).
Fonty: DM Sans (skill), Playfair Display Italic i Oswald (Google Fonts, OFL) w `edit/fonts/`.

## Wersja 2 (uwagi klienta): najpierw cały rig shot, potem „magia montażu” w stylu rolki referencyjnej INVENTA
Skrypt `edit/compose_w222_v2.py`. Wynik: 25,6 s, 615 klatek. Referencja (WeTransfer, 44 s): ciemne tło z czerwoną poświatą i pyłem, kicker „| …”, nagłówek Lora z czerwonym akcentem i podpisem EN, wyskakujące kafelki, licznik, badge, karuzela, glitch RGB, smugi światła, kontakt w czerwonej ramce.

| Czas (s) | Segment |
|---|---|
| 0,00–12,46 | Cały rig shot (prowadnica v2 / Seedance), ruszenie auta 5,58 s = drop |
| 12,46–12,83 | Rampa 2× z rozmyciem ruchu, push w piastę, aberracja RGB, glitch |
| 12,83–14,42 | Klatka z rigu kurczy się do kafelka 3D; licznik 0→40 SZPRYCH; „Jedna felga. Zero kompromisów.” |
| 14,42–16,42 | Siatka 2×2 prawdziwych zdjęć (_12, _07, _01, _08) wyskakuje kafelek po kafelku; _07 rozwija się na pełny ekran |
| 16,42–17,92 | _07 na pełnym ekranie, smuga światła, „Brushed Silver”, glitch |
| 17,92–19,58 | Karta felgi w 3D, badge 18″→22″, pigułki 10.5J / 40 SPOKES; „Rozmiar 22 cale” |
| 19,58–21,75 | Karuzela realizacji (_05, _09, _06, _10) ze strzałkami, kropkami, paskiem postępu i kontaktem |
| 21,75–25,63 | Glitch → finał: ciemne zdjęcie piasty, śnieg, białe logo, czapka Mikołaja spada na T, „Odezwij się!”, kontakt w czerwonej ramce |
Fonty: Lora (OFL) w `edit/fonts/`, Inter Display (systemowy), DM Sans (skill).

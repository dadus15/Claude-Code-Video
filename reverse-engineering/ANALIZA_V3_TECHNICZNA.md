# Analiza v3: oryginał pod każdym względem (pomiar, nie oko)

Narzędzia: OpenCV (Lucas-Kanade z kontrolą forward-backward, Farneback, korelacja fazowa), wyłącznie **unikalne klatki** z prawdziwymi znacznikami czasu.
Wersje v1 i v2 liczyły ruch na klipie przepróbkowanym do 24 fps, a zdublowane klatki zaniżały prędkości.

## A. Technika nośnika
| Cecha | Wartość |
|---|---|
| Źródło | nagranie ekranu TikToka (WhatsApp), 484 klatki, 312 unikalnych; film źródłowy **24 fps** |
| Długość właściwa | **12,95 s** (311 kl.), potem pętla |
| Kadr | 9:16, w nagraniu 234×414 px (niska rozdzielczość) |
| Cięcia | brak, jedno ujęcie |
| Tekst / grafika | brak (tylko UI TikToka) |

## B. Kamera i optyka
| Cecha | Pomiar |
|---|---|
| Mocowanie | Karoseria w polu ruchu ma **zerowy wektor**, więc kamera jest sztywno związana z nadwoziem |
| „Praca” mocowania | wolny dryf obrazu względem auta: 0 → **−18 px / +8 px** (przy 360 px szerokości) między 2,0 a 6,0 s, powrót do 0 przy 8,0 s (≈ 8° / 4°); plik `motion/mount_drift_px.npy` |
| Mikrodrgania | σ ≈ 0,8–1,1 px przy 360 px (~0,4°), przez cały klip |
| Obiektyw | ultraszeroki, linie proste pozostają proste (tryb liniowy), mocno zadarty w górę (latarnie przy krawędzi „pochylone” perspektywą) |
| Migawka | ostrość asfaltu podczas jazdy spada **~6×** względem postoju, czyli wyraźny motion blur (~180°) |

## C. Ruch: fizyka (pole wektorów `motion/flowfields.jpg`)
- **Cofanie (0–2,25 s):** auto **jest w ruchu od pierwszej klatki**, z prędkością maksymalną do ~0,9 s, potem płynnie hamuje do 0 przy 2,25 s.
  Asfalt „rozlewa się” w prawo w dół: (180, 130) px/s, potem do 0. Niebo w tym czasie: (−14, +7) px/s po odjęciu dryfu chmur, czyli **auto obraca się**.
- **Postój i skręt (2,25–5,6 s):** asfalt 0, chmury dryfują (−1, +0,8) px/s (wiatr). Skręt kół L→P 3,1–5,1 s.
- **Jazda w przód (od 5,6 s):** asfalt ucieka w prawo w górę, narasta do (210, −175) przy 7,75 s, potem lekko przyspiesza do ~(250, −250).
  Latarnie przesuwają się po skosie w lewo w górę (−40…−90, −40…−100) px/s: auto skręca.
- **Kluczowy wniosek (błąd v2):** przy cofaniu i przy jeździe asfalt ucieka **w tę samą stronę poziomo**, a w pionie w przeciwną.
  To sygnatura **przodu auta sunącego bokiem na skręconych kołach** (przednia oś porusza się w kierunku kół, tylna wzdłuż nadwozia).
  W v2 przód jechał wzdłuż osi nadwozia, dlatego tło wyglądało jak jazda na wprost.

## D. Felga i koło
- Obrót felgi przy jeździe ~190–215°/s, czyli **v ≈ 1,1–1,25 m/s** (niezależnie od modelu kamery).
- Podczas skrętu (3,1–5,1 s) felga się nie obraca. Ruch kół i asfaltu jest spójny (brak poślizgu).

## E. Obraz (grade)
| Cecha | Pomiar |
|---|---|
| Ekspozycja | bardzo jasna, mediana luminancji 189/255, **21% kadru ≥ 250** (niebo wypalone do bieli) |
| Czerń | p1 = 8 (głęboka, nie zgnieciona) |
| Nasycenie | średnio 95/255, kolor auta bardzo nasycony |
| Niebo | neutralnie białe (BGR 245/250/249) |
| Szum / ziarno | σ ≈ 4,6 na płaskim niebie (ziarno + kompresja) |

## F. Montaż i dźwięk
- Jedno ujęcie bez cięć. Hook to opona w pierwszej klatce **w trakcie ruchu** (cofanie już trwa), więc pętla jest płynna, bo koniec też jest w ruchu.
- Dźwięk: intro bez basu, „oddechy” 2,0 / 3,0 / 5,0–5,5 s, **drop ~6,0 s = ruszenie auta (5,6–6,0 s)**, dalej uderzenia co ~0,75 s.

## G. Metoda odtworzenia (v3)
1. Kalibracja kamery i kinematyki (`motion/calib3.py`): jednoczesne dopasowanie pozycji, kątów i ogniskowej kamery, kąta skrętu kół oraz profilu prędkości do zmierzonego ruchu asfaltu i nieba co 0,25 s, z warunkami na położenie i wielkość koła w kadrze.
2. Animacja w Blenderze z modelu rowerowego z tylną osią (przód sunie bokiem), z dryfem i drganiami mocowania z pomiaru oraz z motion blur.
3. Weryfikacja: ten sam pomiar ruchu na renderze prowadnicy co na oryginale, z tabelą zgodności dla każdej fazy przed jakąkolwiek generacją AI.

## H. Kalibracja (wynik) i co zmieniło się w scenie (rev. 10)
Metoda: piksele obszaru asfaltu (prawy dolny róg kadru) rzutowane na płaszczyznę ziemi, piksele nieba na nieskończoność; ten sam ruch auta
liczony modelem rowerowym (tylna oś jedzie wzdłuż nadwozia, przednia w kierunku skręconych kół). Dopasowanie do przepływu zmierzonego w oryginale
co 0,25 s (asfalt cały klip, niebo w P1, obrót chmur w P5), przy zachowaniu zatwierdzonego kadru RS5 (koło w tym samym miejscu i rozmiarze).

| Parametr | Wartość |
|---|---|
| Kamera | x −1,25 m (na zewnątrz nadwozia), 0,51 m przed osią, 0,28 m nad ziemią; obrót ≤ 5° względem kadru rev. 8 |
| Obiektyw | 16,4 mm (przetwornik 36 mm), ok. 95° w poziomie, bez dystorsji |
| Skręt kół | **42° w lewo** (cofanie) → **8° w prawo** (jazda); zmiana 3,1–5,1 s |
| Prędkość tylnej osi | cofanie 0,43 m/s od klatki 0, hamowanie do 0 przy 2,25 s; jazda 1,33 m/s od 5,6 s (smoothstep do 7,8 s, +25% do końca) |
| Obrót auta | P1 −11,6°, P5 −26,6° (zgodne z dryfem chmur ~3–4°/s) |
| Koło | toczy się bez poślizgu po własnym kierunku: ω = v / (R·cos δ) ≈ 220°/s (oryginał 190–215°/s) |
| Mocowanie | dryf z pomiaru (do −18/+8 px między 2 a 6 s) + mikrodrgania σ ≈ 0,9 px |

Zgodność przepływu asfaltu model ↔ oryginał (px/s, kadr 360×640): cofanie (187,139) ↔ (244,149)…(158,116); jazda 7,1 s (151,−141) ↔ (169,−127);
9–12 s (204…233, −191…−218) ↔ (186…302, −167…−302). Kierunek zgadza się w każdej fazie: przy obu manewrach asfalt ucieka w prawo, czyli przód auta sunie bokiem.

Odrzucone warianty: kamera w miejscu „idealnym” dla oryginału wypada wewnątrz karoserii RS5 albo 2 cm od opony, bo oryginał to inne auto
(większe koło, węższy narożnik). Dlatego zachowujemy kadr RS5, a dopasowujemy ruch.

## I. Weryfikacja prowadnicy v3 (rev. 11)
- Dokładny test geometryczny (punkty ziemi rzutowane przez kamerę Blendera klatka po klatce): cofanie ~(220,160) px/s, jazda ~(180…280, −110…−260) px/s; oryginał (160…244, 118…149) i (169…318, −126…−302). Kierunek i wielkość zgodne.
- Pomiar optyczny na samym wideo prowadnicy zaniża prędkość (śnieg ma mało faktury), ale kierunek jest zgodny w każdej fazie: przy cofaniu i przy jeździe asfalt ucieka w prawo.
- Drgania mocowania zmniejszone do zmierzonych σ ≈ 0,45 px; dryf mocowania 2–8 s z pomiaru.
- Pliki: `renders/rs5_v05_guide_v3_720x1280.mp4`, `renders/porownanie_oryginal_vs_prowadnica_v3.mp4`.

## J. Prowadnica v4 (rev. 17): uwagi klienta
- **Felga V05:** obrys z wyprostowanego zdjęcia _06 (elipsa → koło, R = krawędź rantu). 5 ramion z oknem trójkątnym i oknem w „głowie”, pierścień 0,80–1,0 R z 34 skośnymi oknami, piasta 0,25 R, lico wklęsłe 20 mm. Geometria powstaje z operacji boolowskich (powtarzalnie), plik `reverse-engineering/v05/`.
  Wykończenie: szczotkowane aluminium (anizotropia z promieniowym kierunkiem szlifu, mikroszum chropowatości). W EEVEE przy białym niebie wygląda jaśniej niż na zdjęciu, dlatego finalne wykończenie bierzemy ze zdjęć referencyjnych w Seedance.
- **Opony zimowe:** kierunkowy bieżnik „V”, gęste lamele, rowek obwodowy, ubity śnieg w rowkach.
- **Ślady w śniegu:** 4 koleiny (FL, FR, RL, RR) wzdłuż prawdziwej trajektorii z modelu rowerowego; każdy fragment pojawia się dopiero, gdy koło po nim przejedzie. Ślady z cofania sprzed klatki 1 są już widoczne.
- **Skręt w prawo:** 14° zamiast 8°; ruch tła dalej zgodny z oryginałem (koszt 1415 przy 1050). 25° dawało tło jadące wyraźnie bokiem (koszt 2959).
- **Reflektor:** kamera z narożnikiem reflektora w kadrze (0,85 m przed osią) wymaga patrzenia wzdłuż długiej maski RS5. Czarna karoseria zajmuje wtedy pół kadru, a koło maleje. Zostaje kadr v3, a narożnik reflektora z białym DRL opisany jest w prompcie Seedance (z referencji RS5).

## K. Prowadnica v5 (rev. 19)
- **Pierścień aero (pomiar z rozwinięcia biegunowego zdjęcia _06, `v05/pierscien_aero_rozwiniecie.png`):** 20 przelotowych okien (4 na przęsło między ramionami, brak okien pod głowami ramion), rozstaw 13,1°, pas 0,85–0,95 R, kształt zaokrąglony 0,11 × 0,045 R, pochylenie 25° od promienia (zgodnie z ruchem wskazówek zegara), zawór między 2. a 3. oknem jednego przęsła.
- **Hamulce:** tarcza nawiercana (otwory w łukowych rzędach, 48 na obwód, pas 0,62–0,93 R tarczy), logo RS na zacisku.
- **Ślady:** auto cofało na pełnym skręcie 5 s przed pierwszą klatką, więc koleina przed kołem jest łukiem (R ≈ 4 m). Koleina ma przekrój: wgłębienie z bieżnikiem + wały śniegu po bokach (+16 mm). Stare ślady innych aut to łuki R 4–16 m (wcześniej proste pasy). Kontrola z góry: `renders/kontrola_slady_z_gory.png`.

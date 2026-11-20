# Pierwsze próby produkcyjne: C (zmiana koszulki) oraz E–F (felga z ekranu na rolki)

Status: 🟥 plany kompozycji gotowe (plansze w `storyboard/`), 🟨 prompty gotowe, 🟩 klipów brak.

---

## C — zmiana koszulki na drugim pstryknięciu

Plansze: `storyboard/02_C_makieta_znaku.png` pokazuje prawdziwy znak z @TWdetail na zatwierdzonej karcie. To sprawdzian pozycji i skali, nie render.

### Mechanika (dlaczego to wyjdzie idealnie i tanio)
Zmiana koszulki **nie powstaje w generatorze wideo**. Robi ją twarde cięcie między dwiema klatkami, które różnią się wyłącznie nadrukiem:

| Krok | Co | Koszt |
|---|---|---|
| 1 | KF-C1 (C-PRZED): siedzi, lewa dłoń trzyma fałdę 8 cm pod lewą piersią, prawa w pozie pstryknięcia, wzrok na koszulce, logo GT | 0,5 kr |
| 2 | KF-C2 (C-PO) = **edycja kopii KF-C1**: usuwamy tylko logo GT, wstawiamy znak na lewą pierś noszącego | 0,5 kr |
| 3 | Kontrola różnicowa C1 vs C2 (lokalnie, 0 kr): `ffmpeg -i C1.png -i C2.png -filter_complex blend=all_mode=difference -frames:v 1 diff.png` — świecić może tylko miejsce logo GT i znaku TW | 0 |
| 4 | Klip B kończy się na **C1** (end_image), klip C startuje z **C2** (start_image) | w B i C |
| 5 | W montażu: cięcie dokładnie na trzasku 10:40 (kl. 260). Ostatnia klatka B = KF-C1 wstawiona jako 1 klatka (gwarancja zgodności), pierwsza klatka C = KF-C2 | 0 |

Krok 5 to zabezpieczenie: Seedance zbliża się do end_image, ale nie trafia piksel w piksel. Dlatego na cięciu stawiamy dokładnie te dwie klatki, które przeszły kontrolę różnicową. Jeśli koniec B odbiega pozą od C1 o więcej niż kilka pikseli, wydłużamy ruch dłoni w B o 2–3 klatki i tniemy w środku ruchu prawej ręki. Rozmycie ruchu przy pstryknięciu ukryje resztę.

### Umiejscowienie znaku (z @TWfront i @TWdetail)
- Lewa pierś **noszącego**, czyli prawa strona kadru. Na makiecie i w @TWfront wygląda to identycznie.
- Szerokość znaku ok. 1/6 szerokości barków (ok. 7 cm), środek 9 cm pod szwem dekoltu.
- Czerwone kryształki w lewym dolnym rogu znaku.
- Dekolt okrągły według @TWfront. Na plecach (widoczne dopiero w D): napis TURISMO nad dużą felgą.
- Plan awaryjny: jeśli edycja C2 zniekształci znak, nakładamy znak z @TWdetail w montażu, z deformacją po fałdzie materiału (mesh warp). Brief przewiduje to wprost.

### Kryteria odbioru C
- Dokładnie **dwa** pstryknięcia w całym spocie (6:00 i 10:40). Koszulka GT zostaje na aktorze od gry aż do drugiego pstryknięcia.
- Na cięciu nie zmienia się nic poza nadrukiem: dłonie, dekolt, szew kanapy i linia wzroku zostają te same.
- Kamera stoi przez cięcie i jeszcze 0,6 s po nim.

---

## E–F — wyciągnięcie felgi z ekranu i postawienie na rolkach

Plansza: `storyboard/01_E-F_4_klatki_os_czasu.png`, osobno `storyboard/EF_K1.png`…`EF_K4.png`.

### Cztery kolejne klatki

| Klatka | Czas | Kadr |
|---|---|---|
| **K1** | 19,00 s (kl. 475) | Felga na stronie: C19-R dokładnie z przodu, 1/3 szerokości ekranu, wentyl na 4:00. Prawa dłoń nadchodzi z prawej góry, 6 cm przed matrycą |
| **K2** | 19,40 s (kl. 485) | Kciuk na przednim rancie obrazu w 12:00, opuszki pozostałych palców znikają **za** rantem |
| **K3** | 23,00 s (kl. 575) | Pełnowymiarowa obręcz 54 cm, pionowo, kciuk w 12:00, lewa dłoń pod 6:00, dłoń szerokości nad rolkami. Na ekranie neutralne pole w miejscu zdjęcia |
| **K4** | 23,60 s (kl. 590) | Ta sama obręcz na **obu** rolkach (2 punkty styku, piasta nad środkiem między rolkami), dłonie puszczają |

Wszystkie cztery klatki to edycje jednego planu bazowego KF-O2. Kamera, światło i stół są więc identyczne, a różni się tylko dłoń i felga.

### Kiedy kciuk zasłania przejście (odpowiedź na pytanie z briefu)

**Klatki 485–491 (19,40–19,64 s, 0,24 s).** Kciuk leży nieruchomo na przednim rancie obrazu katalogowego w punkcie 12:00 i zakrywa go całkowicie, łącznie z krawędzią rantu.

1. **Kl. 485:** opuszek kciuka dotyka matrycy dokładnie na zewnętrznej krawędzi rantu w 12:00. Pada „Ten”.
2. **Kl. 485–487:** opuszki palca wskazującego, środkowego i serdecznego „wsuwają się” za rant. W montażu ich końcówki ucina maska wzdłuż zewnętrznej krawędzi rantu, więc wyglądają, jakby były za felgą, czyli w głębi obrazu.
3. **Kl. 487–491 (pod kciukiem):** podmiana warstw. Płaskie zdjęcie katalogowe 2D znika, a na jego miejscu staje render 3D tej samej felgi (albo dopasowana płyta produktowa). Render ma identyczną pozycję na ekranie, średnicę, fazę ramion (wentyl na 4:00) i rzut dokładnie z przodu. Zdjęcie z przodu i ortograficzny render z przodu wyglądają niemal identycznie. Różnią się tylko grubością rantu w miejscu chwytu, a to miejsce zakrywa kciuk. Dlatego podmiany nie widać.
4. **Kl. 492:** ręka zaczyna się cofać. Obręcz pochyla się 8–12° do kamery i pierwszy raz widać głębokość rantu i beczki. To pierwszy dowód, że felga jest przestrzenna.
5. **Kl. 500–510 (20,0–20,4 s):** górny rant przechodzi **przed** górną ramką laptopa, a ramka pozostaje widoczna za obręczą. To moment, w którym widz czyta: „wyszła z ekranu”.
6. **Kl. 491–538 (19,64–21,5 s):** skala rośnie od ok. 12 cm (rozmiar na ekranie) do 54 cm z wygładzonym początkiem i końcem. Zmiana skali kończy się przed lotem nad podstawkę, zgodnie z briefem. Od kl. 538 skala jest zablokowana.
7. **Kl. 491–525:** chłodna poświata ekranu na metalu gaśnie od 100% do 0%, a felgę przejmuje światło biura.
8. **Kl. 523–538:** lewa dłoń wchodzi pod 6:00 i przejmuje ciężar.

### Warstwy w kompozycji (od tyłu do przodu)
1. **Ekran:** nagranie @WEB po korekcji perspektywy. Od kl. 487 w miejscu zdjęcia produktu jest neutralne pole karty www (clean plate strony: jednolite tło z wypełnieniem, 0 kr).
2. **Palce za rantem:** płyta AI dłoni z maską opuszków wzdłuż rantu.
3. **Obręcz:** od kl. 487 render 3D śledzony do dłoni (albo felga z płyty AI, jeśli przejdzie kontrolę ramion).
4. **Kciuk:** płyta AI, roto kciuka zawsze **na wierzchu**.
5. Cień kciuka i palców na rancie, refleks pokoju na metalu.

### F — osadzenie i okno detalu
- **23,00–23,60 s:** opuszczanie. Styk na **dwóch** rolkach w kl. 590 (jeden głuchy metaliczny stuk).
- **23,60–24,00 s:** obie dłonie puszczają, podstawka stoi.
- **24,00 s:** styczne pchnięcie prawymi palcami na zewnętrznym rancie w 3:00, w dół. Felga kręci się **zgodnie z ruchem wskazówek zegara** (widziana z kamery), piasta stoi w miejscu, rolki kręcą się przeciwnie.
- **24,80–25,10 s (6–8 kl.):** z okolicy styku wysuwa się czerwony narożnik i rozwija w ramkę w prawej górnej ćwiartce. W środku jest zbliżenie z **tego samego źródła obrotu** (3D albo powiększony wycinek F), z tym samym kierunkiem i tą samą fazą. Prowadzący zostaje widoczny w tle.
- **24,20–25,40 s:** „To C19-R” („ce dziewiętnaście er”).

### Śledzenie ciągłości
Ramię kontrolne to ramię najbliżej wentyla (wentyl na 4:00 w K1). Klatka po klatce sprawdzamy: wentyl i to ramię przechodzą z ekranu, przez dłonie, na rolki bez skoku fazy. Piasta, rant, lakier i kierunek obrotu zachowują ciągłość. Dłonie i rant przesłaniają się zgodnie z głębią: kciuk przed rantem, pozostałe palce za nim.

### Ścieżka testu (od najtańszej)
| Krok | Co | Koszt |
|---|---|---|
| T0 | Plansze + oś czasu (gotowe) | 0 kr |
| T1 | Klatki K1–K4 (`gpt_image_2_6`, medium 1k) | 4 × 0,5 = **2 kr** |
| T2 | Ruch E i F jako drafty `seedance_2_5` 480p, 4 s każdy | 2 × 12 = **24 kr** |
| T3 | Akceptujesz drafty → finalize tych samych generacji do 720p | ok. 2 × 28 = **~56 kr** (stawka 720p; potwierdzę przy pierwszym finalize) |
| T4 | Podmiana 2D→3D pod kciukiem, okno detalu, @WEB: montaż | 0 kr |

**Czego brakuje do perfekcyjnej wersji E–F:**
1. Packshot C19-R Gloss Silver z przodu (bez niego klatki K1–K4 nie mają wzoru felgi).
2. Model 3D C19-R z konfiguratora Turismo (rendery na Drive powstały z CAD, więc model istnieje). Bez niego warstwa 3 jest płytą AI, a liczba ramion może pływać.
3. Nagranie @WEB z kartą C19-R w widoku z przodu.

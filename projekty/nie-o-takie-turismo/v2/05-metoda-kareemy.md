# Metoda Kareemy (kaye.creatives) krok po kroku → „Nie o takie Turismo”

Źródło: transkrypcja filmu „I Made a Professional Commercial Using Only AI (Step-by-Step)” (wklejona przez Ciebie) + analiza scen Higgsfield.
Uwaga: Twój `cinedance-block-library.skill` (domyślna twarz „Karima”) to jej narzędzie do pisania promptów. Pracujemy więc jej systemem.

## Jej workflow (fakty z filmu)
| Krok | Co robi | Narzędzie / model | Koszt u niej |
|---|---|---|---|
| 0. Koncepcja | historia scena po scenie na tablicy z referencjami z Pinteresta; hook z jednego mocnego zdjęcia | Higgsfield **Canvas** | 0 |
| 1a. Karty postaci | dla **każdej** postaci i każdego kostiumu (11 kart) wieloczęściowa karta, czyli „mapa 360°”, żeby twarz i ciało nie „pływały”. Prompt pisze Claude z selfie + referencji kostiumu i produktu | **Seedream 5.0 Pro** („Dream 5 Pro”), 16:9 | 27,5 kr |
| 1b. Karty lokacji | osobna płyta dla każdej lokacji, prompt z opisu albo z **odręcznego szkicu** | **Soul Cinema** (ziarno filmowe, naturalne światło, najtańszy), 16:9 | ~1,1 kr |
| 2. Sceny | Claude pisze prompt z karty postaci + karty lokacji + prostego opisu. Generacja w **Seedance 2.5 draft 480p**, partiami, aż wyjdzie „złote ujęcie”, potem **ten sam take** jest skalowany do wysokiej jakości | Seedance 2.5 | ~1150 kr |
| 2a. Naprawa | przy trudnym układzie przestrzennym **szkic** (kreska + strzałka ruchu kamery) zamiast długiego opisu | szkic → Claude | 0 |
| 3. Rytm i przejścia | przejście **wewnątrz jednej generacji** (wingsuit przelatuje nad rowerzystką); po serii szybkich ujęć **zwolnienie** (slow-motion); scena dzielona na 2 ujęcia (szeroki + ECU); obiektyw w mm (100 mm); nazwisko operatora w prompcie (Lubezki = surowa kamera z ręki); „ludzie w tle = poczucie prędkości” | prompt | — |
| 4. Detale | ujęcie statyczne zawsze z dopiskiem **„camera does not move”**, bo AI lubi dodać zoom; pojedynczy ciasny close-up może iść bez karty (selfie + produkt wystarczą); **wiele osób w kadrze = każda musi mieć kartę** | prompt | — |
| 5. Montaż | 13 scen, efekty dźwiękowe, muzyka | Premiere Pro | — |
| **Razem** | | | **~1180 kr** |

## Jak to stosujemy u nas

### Krok 0 — koncepcja ✅ (0 kr)
Pełni ją storyboard, previs sceny 1, pokój z assetu w barwach Turismo oraz previs Blendera.
Jej „szkice” zastępujemy czymś dokładniejszym: **klatkami previs z Blendera**, z prawdziwymi proporcjami, kamerą i strzałkami ruchu. Dołączamy je do generacji jako referencję kompozycji.

### Krok 1a — karty postaci (Seedream 5.0 Pro, 2k, 16:9, 2,5 kr/szt.)
| Karta | Referencje | Uwagi |
|---|---|---|
| **CS0 Ty — baza** | `Postac-FINAL.png` | ✅ już jest (front / tył / zbliżenie), zatwierdzona |
| **CS1 Ty w koszulce GT + pad** | CS0 + @GT (**do podmiany**) | do sceny w pokoju gier |
| **CS2 Ty w koszulce Turismo** | CS0 + @TWfront + @TWback + @TWdetail | znak na lewej piersi, TURISMO + felga na plecach |
| **CS3 Podstawka z rolkami** (karta produktu) | `brixton…wheel-25.jpg` (tylko kształt) | front / bok / 3/4 / góra, bez napisów |
| Felgi C01 / C19-R / RR | packshoty z Drive (FRONT/SIDE/ANGLE) | to są już gotowe „karty produktu”, kart nie generujemy (0 kr) |

Innych ludzi w spocie nie ma, więc nie grozi nam jej wpadka z ogniskiem.

**Prompt CS2** (styl jej kart):
```
Three-panel character sheet, 16:9, neutral mid-grey seamless studio backdrop, soft even studio light, photorealistic, real skin texture. The SAME man as the reference sheet (identity, face, hair with ash-silver top and low skin fade, 163 cm compact athletic build) in three panels: [1] full body front, standing relaxed, arms at sides; [2] full body back; [3] head-and-shoulders close-up, three-quarter angle. He wears a plain black crew-neck cotton T-shirt with a small crystal rhinestone emblem on his LEFT chest (exact shape and red crystal accent from the emblem reference), and on the back the crystal word TURISMO above a large crystal wheel outline (exact layout from the back reference); straight mid-blue jeans with no brand tab; plain white leather low-top sneakers. No other logos, no text, no watermark. Do not copy the reference model's face, beard or trousers from the T-shirt photos.
```
**Prompt CS1** — ten sam, ale: `black T-shirt with the white logo print exactly as in the GT shirt reference; holding a plain black game controller with no brand in both hands at waist height in panels 1 and 3`.

### Krok 1b — karty lokacji (Soul Cinema, 2k, 16:9, ~0,12 kr/szt., maks. 1 referencja)
| Karta | Referencja | Panele |
|---|---|---|
| **L1 Pokój gier** | `plansze/G0_pokoj_kolory_Turismo.jpg` | (1) zza kanapy na ekran, jak w assecie, (2) **kontrplan od ekranu na kanapę**, (3) bok, (4) detal: kanapa z padem |
| **L2 Wejście do biura** | — | (1) fasada z daleka, (2) szklane drzwi bliżej, (3) od środka na drzwi, (4) detal klamki |
| **L3 Hol z felgami** | — | (1) od wejścia w głąb, (2) kontrplan od drzwi salonu, (3) detal ściany z felgami, (4) sufit i światło |
| **L4 Salon z laptopem** | KF-O1 z v1 albo bez referencji | (1) front na kanapę, (2) kamera produktowa 3/4, (3) zza ramienia z boku kanapy, (4) widok z góry na stolik (laptop + podstawka) |

**Prompt L1** (z referencją G0):
```
Location sheet, 16:9, four panels in a 2×2 grid showing the SAME room from the reference photo — keep its exact layout, furniture and black/red/white colour scheme: black brick walls, red LED strips on wall edges and ceiling, big projector screen, white low media cabinets, dark sofa with red cushions, striped dark rug, low black coffee table with two controllers. [1] the reference viewpoint from behind the sofa toward the screen; [2] reverse angle from beside the screen looking back at the sofa and the wall behind it, which has a white shelf of small racing-car models and a horizontal red LED strip; [3] side view across the room; [4] close detail of the sofa seat with a black controller. The screen is a flat dark-grey surface in every panel. No people, no posters with text, no logos. Real photograph, natural film grain, physically motivated light.
```
**Prompt L3**:
```
Location sheet, 16:9, 2×2 grid, the SAME interior in four panels: a premium forged-wheel showroom hallway 2.2 m wide, 9 m long. Both walls covered floor to ceiling with forged alloy wheels mounted face-out on hidden brackets in neat rows, mostly satin black, gunmetal and brushed grey, a few brushed bronze, no logos. Black slatted ceiling with one continuous white linear light, a thin red LED line at the base of both walls, dark polished concrete floor reflecting the wheels. [1] from the glass entrance looking down the hallway to an open doorway of a lounge; [2] reverse from the lounge doorway toward the glass entrance; [3] close detail of the wheel wall, shallow depth of field; [4] low angle of the floor reflections. No people. Real photograph, overcast daylight from the entrance, natural film grain.
```
(L2 i L4 według tego samego wzoru; wymiary i materiały jak w `02-prompty-v2.md`.)

**Koszt kroku 1:** 3 karty × 2,5 + 4 lokacje × ~0,12 + powtórki ≈ **10–15 kr**.

### Krok 2 — sceny (Seedance 2.5: draft 480p → ten sam take w wyższej jakości)
| Gen. | Ujęcia (rytm v3) | Karty | Długość | Jej trik |
|---|---|---|---|---|
| G1 | najazd nad ramieniem na ekran → początek szybkiej panoramy | CS1, L1, previs S1 | 4 s | szkic = klatka previs |
| G2 | z rozmycia panoramy: Ty z padem, kwestia, pstryk | CS1, L1 | 5 s | lip-sync z Twojego nagrania |
| G3 | **jedna generacja, 3 ujęcia**: dłoń na klamce → hol, mówisz → „Chodźcie…” | CS2, L2, L3 | 10 s | ujęcia jedno po drugim w jednym klipie; „Steadicam walk-and-talk, Emmanuel Lubezki style, 24 mm” |
| G4 | wchodzisz, siadasz, dłonie otwierają laptop | CS2, L4 | 5 s | ostatnie ujęcie: „camera does not move” |
| G5 | kciuk na rancie → felga wychodzi z ekranu, **slow-motion** | CS2, L4, CS3, packshot C01, previs BL | 5 s | zwolnienie po szybkim holu (jej zasada rytmu); felgę zastępuje Blender |
| G6 | Twoja twarz przy kręcącej się feldze (gama) | CS2, L4 | 4 s | ciasny close-up: wystarczy selfie + produkt |
| G7 | CTA do kamery | CS2, L4 | 5 s | „100 mm, shallow depth of field” |
| — | ekran laptopa, gama C01 → C19-R → RR, plansza | Blender + Twoje nagranie | — | 0 kr |
| **Razem** | | | **38 s** | |

### Budżet: jej jakość kontra nasze saldo
Kareema wydała **~1180 kr** na 56 s. My mamy **298 kr**, więc jej metodę stosujemy w całości, ale na mniejszej liczbie sekund z generatora (felgi i ekran robią Blender i Twoje nagrania).

| Wariant | Sekundy AI | Koszt | Uwagi |
|---|---|---|---|
| **A — pełny (G1–G7)** | 38 s | drafty ~170 + finał 720p ~266 + karty ~15 = **~450 kr** | wymaga doładowania ok. 200 kr |
| **B — skrócony (rekomendowany przy obecnym saldzie)** | 24 s: G1, G2, G3 (skrócony do 8 s), G5, G7 | drafty ~110 + finał 720p ~168 + karty ~15 = **~290 kr** | mieści się w saldzie bez rezerwy; G4 zastępuje cięcie na ekran, G6 zastępuje Blender |
| B + Topaz | 24 s | finalizacja 480p → Topaz 1080p zamiast finalizacji 720p | możliwa oszczędność ok. 60–100 kr; Topaz nie da się wycenić z góry, więc testujemy na jednym ujęciu |

Zasady wydawania bez zmian: przed każdą partią podaję wycenę, a w wysokiej jakości finalizujemy tylko take'i z Twoim „akcept”.

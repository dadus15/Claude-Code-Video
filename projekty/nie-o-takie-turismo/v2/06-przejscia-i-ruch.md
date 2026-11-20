# Przejścia i ruch — jak uzyskać realistyczną, płynną dynamikę

Kolejność (Twoja wersja):
1. Pokój gier.
2. **Pstryk 1 = teleport** przed budynek Turismo (nadal w koszulce GT).
3. **Pstryk 2 = zmiana koszulki** GT → Turismo.
4. Wejście do biura, hol, **sales room** (kanapa + laptop).

## Zasada nadrzędna: AI nie łączy ujęć, robimy to my
Najbardziej nienaturalne w reklamach AI są przejścia „morfujące”: twarz albo ubranie płynie przez kilka klatek. Profesjonalnie robi się to tak:
- **Twarde cięcie na akcji** (na trzask palców, w ruchu dłoni) między dwoma ujęciami, które w miejscu cięcia mają **identyczny kadr i pozę**.
- **Dźwięk przełącza się w tej samej klatce**, a obraz i dźwięk razem „sprzedają” teleport. Tak samo przełączają się sceny u Kareemy.

Każde przejście składa się z **dwóch klatek bazowych, które różnią się tylko jedną rzeczą**. Kończymy na nich klip „przed” i zaczynamy klip „po”.

## Przejście 1 — teleport (pstryk 1)
| | Klip G2 (koniec) | | Klip G3 (start) |
|---|---|---|---|
| Kadr | od pasa w górę, głowa 28% od góry, prawa dłoń przy barku w pozie pstryknięcia | = | identyczny |
| Tło | pokój gier (czerwone LED-y) | **zmiana** | fasada biura Turismo, szklane drzwi, dzienne światło |
| Koszulka | GT | = | GT |
| Światło na twarzy | ekran + czerwony kontur | **zmiana** | miękkie światło dzienne |

- Klatka **T-A** to ostatnia klatka G2, a **T-B** to edycja T-A, w której zmieniamy tylko tło i światło. Postać zostaje.
- Cięcie wypada dokładnie w klatce trzasku, z 2 klatkami rozmycia palców.
- Dźwięk: trzask → natychmiast cisza pokoju gier zamienia się w ulicę (wiatr, daleki ruch). Bez przenikania.
- Wariant B (do testu, 12–15 kr): Seedance robi tę zmianę w jednej generacji, jak przejście wingsuit → rower u Kareemy. Rekomenduję A, bo daje pewną zgodność twarzy.

## Przejście 2 — zmiana koszulki (pstryk 2)
Ta sama mechanika, którą sprawdziłem w v1 (makieta `storyboard/02_C_makieta_znaku.png`):
1. G3 (przed budynkiem): opuszczasz dłoń, patrzysz w dół na koszulkę GT. Proponuję wrócić do kwestii z pierwotnego briefu: **„Coś mi nie pasuje.”** Lewą ręką chwytasz materiał, prawą unosisz do pstryknięcia.
2. Klatki **S-GT** i **S-TW** są identyczne piksel w piksel. Różni je tylko koszulka: logo GT na piersi kontra znak Turismo na lewej piersi. Sprawdzamy to nałożeniem w trybie „różnica”.
3. G3 kończy się na S-GT, G4 zaczyna się na S-TW. **Kamera stoi przez cięcie i jeszcze 0,6 s po nim.**
4. G4: puszczasz materiał. **„Od razu lepiej.”** Odwracasz się i idziesz do drzwi.

Referencje koszulek: GT = `referencje_koszulki/GT_przod.jpg` (+ detal logo, wszywka z szachownicą), Turismo = assety @TWfront / @TWback / @TWdetail.

## Chód, drzwi, siadanie — jak AI ma się ruszać jak człowiek
### 1. Najważniejsze: Twój prawdziwy ruch jako referencja (0 kr)
Seedance 2.5 przyjmuje **video_references**, czyli nagranie ruchu, które model odwzorowuje. **Nagraj telefonem siebie**:
- podchodzisz do dowolnych drzwi, otwierasz je i wchodzisz;
- idziesz korytarzem i mówisz kwestię;
- skręcasz, siadasz na kanapie, otwierasz laptop.

Kamera powinna prowadzić tak jak w spocie (ktoś idzie tyłem przed Tobą albo kamera na gimbalu). Wnętrze nie ma znaczenia, liczy się **rytm kroków, przeniesienie ciężaru, ruch dłoni na klamce i ruch kamery**. AI przeniesie to na wygenerowane biuro. Tylko tak „chód” będzie naprawdę Twój, a nie generyczny. Higgsfield ma też osobne przenoszenie ruchu (motion control), jeśli Seedance nie utrzyma tempa.

### 2. Fizyka w promptach (konkrety zamiast przymiotników)
- **Chód:** spokojne tempo ok. 1,1 m/s, ok. 105 kroków/min; pięta → palce; ręce w przeciwfazie do nóg; pionowe kołysanie 3–4 cm; stopy nie ślizgają się po podłodze, ciężar widać w kontakcie.
- **Drzwi:** szklane drzwi otwierane **do środka**, zawiasy po lewej, pionowy uchwyt. Kolejność: dłoń sięga (0,3 s) → palce obejmują uchwyt **zanim** drzwi drgną → pchnięcie, drzwi obracają się o ok. 70° w 0,8 s → przejście → puszczenie → samozamykacz domyka je powoli w 3–4 s. Odbicia w szkle przesuwają się z kątem.
- **Siadanie:** dłoń podpiera się o siedzisko, poduszka ugina się, ciało osiada z opóźnieniem ok. 0,2 s.
- **Kamera:** steadicam prowadzący tyłem w tym samym tempie co Ty; 24–35 mm; bez zoomu, bez przyspieszeń. Przy ujęciach statycznych dopisek „camera does not move”. Dla stylu kamery nazwisko operatora (u Kareemy: Lubezki).
- **Kierunek ekranowy:** od wyjścia z pokoju gier do sales roomu poruszasz się konsekwentnie w jednym kierunku (np. w kadrze z lewej w prawo albo do kamery). Nie łamiemy zasady 180°.

### 3. Cięcie w ruchu ukrywa błędy AI
- Przy drzwiach dwa ujęcia: na zewnątrz dłoń dotyka uchwytu → **cięcie, gdy drzwi są w połowie otwarcia** → w środku, drzwi otwierają się w stronę kamery. Kąt drzwi i pozycja dłoni zgadzają się na cięciu.
- Hol: cięcie na krok (ta sama noga w powietrzu po obu stronach cięcia).
- Generator robi 1 klip 10 s, a w montażu wycinamy z niego 2–3 ujęcia (metoda Kareemy).

### 4. Technika płynności w montażu
- Klatkaż natywny generatora (24 kl./s, jeśli taki oddaje). Bez konwersji na 25 i bez slow-motion w chodzie (zwolnienie tylko przy wyjęciu felgi).
- Rozmycie ruchu jak z migawki 180°, w Blenderze to samo.
- Stabilizacja tylko gdy konieczna, lekka. Prawdziwe drobne drgania kamery to element realizmu.
- **Dźwięk realizmu:** każdy krok podłożony na klatkę kontaktu pięty, klik zamka, syk samozamykacza, zmiana tła dźwiękowego ulica → hol (pogłos), materiał kanapy, zawias laptopa. Połowa wrażenia „to prawdziwe” pochodzi z dźwięku.
- Wspólne ziarno i kolorystyka na całość.

## Klipy po zmianie kolejności
| Gen. | Co | Długość | Klatka start / koniec |
|---|---|---|---|
| G1 | najazd nad ramieniem na ekran GT | 4 s | — |
| G2 | Ty z padem, „Nie o takie Turismo nam chodzi.”, dłoń do pstryknięcia | 5 s | → T-A |
| G3 | przed budynkiem w koszulce GT: „Coś mi nie pasuje.”, chwyt koszulki | 5 s | T-B → S-GT |
| G4 | koszulka Turismo: „Od razu lepiej.”, idziesz do drzwi, dłoń na uchwycie | 5 s | S-TW → |
| G5 | drzwi → hol, kwestie, „Chodźcie…”, skręt do sales roomu | 10 s | + Twoje nagranie ruchu |
| G6 | sales room: siadasz, otwierasz laptop | 5 s | + Twoje nagranie ruchu |
| G7 | wyjęcie felgi z ekranu (slow-mo) | 5 s | packshot ANGLE jako referencja |
| G8 | Twoja twarz przy kręcącej się feldze | 4 s | — |
| G9 | CTA | 5 s | — |
| **Razem** | | **48 s** | spot ok. 60 s |

## Felgi bez plików 3D
- **Gama w obrocie (C01 → C19-R → RR) w widoku z przodu: prawdziwe packshoty FRONT** obracane w montażu i podmieniane w szczycie obrotów. Geometria jest dokładnie taka, jak w Waszych renderach, i nie kosztuje kredytów. Blender dokłada podstawkę, rolki, cień i rozmycie ruchu.
- **Ujęcia pod kątem (wyjęcie z ekranu, felga na rolkach obok Ciebie):** Seedance z packshotem ANGLE jako referencją produktu. U Kareemy tak samo trzymały się gogle.
- Proceduralne modele z Blendera służą tylko do ruchu, czasu i masek.
- Potrzebne: **packshoty FRONT** C01 / C19-R / RR z Drive (folder „RENDERY FELG”). Załącz je w czacie. Strona turismo-wheels.com ma tylko widoki ANGLE.

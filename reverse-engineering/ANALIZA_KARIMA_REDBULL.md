# Analiza: reklama Red Bull F1 (Karima, YouTube) i co przenosimy do projektu Turismo

Źródło: plik z WeTransfer (18 min, 640×360, 23,976 fps) + transkrypcja.
Uwaga: skill **cinedance-block-library**, z którego już korzystamy, to jej biblioteka bloków (stąd „Karima's face lock” w jego opisie).

## 1. Silnik i algorytm (z transkrypcji)
| Etap | U niej | U nas |
|---|---|---|
| Assety najpierw | arkusze postaci / auta / byka / lokacji (Seedream, Cinema Studio) zanim powstanie jakiekolwiek wideo | arkusz felgi V05 (5 widoków), arkusz RS5 satin black, arkusz lokacji (zimowy parking): obraz → potem wideo |
| Prompty | zawsze pisze Claude (Opus), nigdy ręcznie | tak robimy (cinedance-block-library + cinema-worldbuilder) |
| „Optical block” | stały dopisek do promptu lokacji: dystorsja anamorficzna, grading, ziarno filmowe | bloki OPT-WIDE + GRADE-BRIGHT + GRADE-LOCK + ziarno; dla nas obiektyw action-cam, nie anamorfa |
| Wideo | Seedance 2.5, najpierw niska jakość, potem upscale | szkic 480p (~46 kr) → 1080p (~259 kr) |
| Precyzyjny ruch | Blender (wtyczka Higgsfield + Opus pisze Python) → render → Seedance z poleceniem „kamera i fizyka identyczne z referencją Blendera” | to jest nasz pipeline (prowadnica v4, 3D Jutsu) |
| Poprawki | nie przepisuje promptu, gdy ruch jest dobry: generuje kilka razy i skleja najlepsze fragmenty | 2–3 warianty szkicu, montaż z najlepszych |
| Genjutsu | podmiana obiektu w gotowym klipie z zachowaniem ruchu kamery (auto → byk) do match cutów | match cut: obracająca się felga → logo Turismo / zdjęcie RS5 |

## 2. Montaż reklamy (pomiar cięć, 0–40 s)
- **Hook 0–8,6 s:** jedno długie ujęcie (postać + auto w dymie), bez cięć.
- **Rozwinięcie 8,6–20 s:** ujęcia 0,6–1,3 s, inserty makro (puszka, wlew, opona z wyładowaniem).
- **Przejście „flash”:** złoty płyn wypełnia kadr → biel → nowa scena (cięcie ukryte w jasności).
- **Transformacja:** białe auto → malowanie Red Bull z błyskawicami (reveal w ruchu).
- **Hero 19,8–24,2 s:** jedno dłuższe ujęcie 4,4 s (oddech przed dropem).
- **Kulminacja 27,8–28,7 s i 36,4–38,5 s:** cięcia co 0,12–0,25 s, zsynchronizowane z bitem (strobe montage).
- **Match cut auto ↔ byk:** ten sam ruch kamery, podmieniony obiekt.
- **Grade:** nocny stadion, teal/blue z ciepłymi akcentami, flary, ziarno.

## 3. Plan dla Turismo (po zatwierdzeniu głównego ujęcia)
1. **0–13 s:** główne ujęcie rig (prowadnica v4 → Seedance), jak oryginał TikToka.
2. **Przejście:** felga kręci się coraz szybciej → spin blur → biały flash (jak złoty płyn u Karimy) → match cut na zdjęcie RS5 _01 (koło w tym samym miejscu kadru).
3. **Strobe ze zdjęć RS5 (0,25 s/zdjęcie, na bit):** _15, _04, _11, _13, _06 z lekkim push-in i dopasowaniem pozycji felgi (felga zawsze w tym samym punkcie kadru = „match cut” na zdjęciach).
4. **End card:** iris przez piastę → TURISMO WHEELS · UNLOCK YOUR STYLE · Daniel Chmielewski · +48 501 404 861 · e-mail.

## 4. Pełna analiza montażu całego filmu (18 min, wykrycie cięć + arkusze klatek co 5 s)
### Rytm (cięcia na minutę, mediana długości ujęcia)
| min | cięcia | mediana ujęcia | co się dzieje |
|---|---|---|---|
| 0 | 51 | 0,60 s | reklama (hook) + intro: najszybszy fragment |
| 1–2 | 18 / 12 | 2,5–2,8 s | „dlaczego”, memy, liczby |
| 3–9 | 5–12 | 3,5–8 s | tutorial (gadająca głowa + ekran), oddech |
| 10 | 15 | 0,96 s | iteracje / porównania ujęć: przyspieszenie |
| 11–14 | 7–11 | 4,6–9 s | Blender / Genjutsu (tutorial) |
| 15 | 31 | 0,40 s | finałowa reklama w całości: drugi szczyt |
| 16–17 | 6–7 | 9–11 s | koszt, CTA, outro |
Zasada: **dwa szczyty tempa (początek i finał) przedzielone spokojnym tutorialem**, a co ~60–90 s „reset uwagi” (mem, karta, liczba).

### Napisy (typografia)
- **Słowa kluczowe:** elegancki szeryf (kursywa/regular), kremowo‑żółty, nad lub obok obiektu („hey”, „brainstorm”, „Asset consistency”, „real value”), pod spodem drobny podpis bezszeryfowy. Pojawiają się 1 słowo na raz, synchronicznie z mową.
- **Napisy dialogowe na B-rollu:** małe, żółtawe, bezszeryfowe, małymi literami, na środku kadru (nie klasyczne paski).
- **Listy:** biała kursywa bez szeryfów, wyrównana do lewej, punkty wjeżdżają linijka po linijce („- my character sheet / - f1 car model sheet …”).
- **Tytuły rozdziałów:** „STEP 3 / BLENDER & OPUS 5.5”, czyli grube, wąskie, białe wersaliki + niebieski znak „#” ze świeceniem, w lewym dolnym rogu, na **odbarwionym (B&W) kadrze** tła.
- **Prawa autorskie:** „© Red Bull Media House”, mała biała linijka w lewym dolnym rogu.

### Karty i grafika
- **Karty w kolorze marki kanału** (intensywny niebieski) z delikatnym wzorem linii i szeryfowym tekstem („rule #1”, „every single model”, „now that we have all our assets prepared”).
- **Okno „picture‑in‑picture”:** klip w zaokrąglonym oknie na **rozmytym tle** jej pokoju (B-roll bez cięcia z gadającej głowy).
- **Licznik kredytów:** żółta „pigułka” w prawym górnym rogu, wraca cyklicznie (seria, pętla ciekawości do końca filmu).
- **Dowody społeczne:** wyskakujące „1.1m” z ikoną, zrzut komentarza pracownika Apple jako karta.
- **Memy i reakcje** na niebieskiej karcie (Futurama, Joker, „what I got”), 0,5–1,5 s.
- **Ekran:** nagrania UI na białym tle z dojazdem do kursora; „flowchart” z kart, które wyskakują po kolei („Ask for the prompt → Generate → Test and iterate”).
- **Kolaż:** zdjęcia „rzucane” na białe tło z lekkim obrotem (Genjutsu), porównania obok siebie na bieli.
- **Outro:** logotypy marek wskakują jeden po drugim (LEGO, Chupa Chups, Apple, adidas, Red Bull).

### Przejścia i rampy
- **Punch‑in / jump cut:** gadająca głowa na przemian w planie pełnym i zbliżeniu (cięcie na oddechu).
- **Biały / złoty flash:** przejście przez wypełnienie kadru światłem (wlew paliwa → transformacja).
- **Match cut z podmianą obiektu:** ten sam ruch kamery, auto ↔ byk (Genjutsu).
- **Strobe na bit:** w szczytach cięcia 0,12–0,25 s, z rampą prędkości (zwolnienie przed dropem, przyspieszenie na dropie).
- **Desaturacja tła pod tytułem:** kadr gaśnie do B&W, wjeżdża tytuł rozdziału, kolor wraca.

## 5. Co bierzemy do rolki Turismo (13–20 s, pion 9:16)
1. **Hook bez cięcia** (nasz rig shot 0–5,6 s), bez napisów w pierwszych 1,5 s.
2. **Słowo kluczowe w szeryfie** obok felgi w chwili pełnego widoku (5,1 s): „V05” / „forged”, kremowe, 1 słowo.
3. **Drop 6,0 s:** krótka rampa (zwolnienie 0,3 s, potem ruszenie), bez cięcia.
4. **Biały flash → match cut** na zdjęcie RS5 z felgą w tym samym punkcie kadru.
5. **Strobe ze zdjęć RS5** 0,2–0,25 s na bit, z punch‑in 3–5% na każdym.
6. **Tytuł w stylu „STEP”:** odbarwione zdjęcie RS5 + „TURISMO FORGED V05 / BRUSHED”.
7. **Karta końcowa** w kolorach Turismo (granat/czerwień), elementy wskakują po kolei: logo → UNLOCK YOUR STYLE → DANIEL CHMIELEWSKI → telefon → e-mail.
8. Licznik/pigułka i memy pomijamy: to format kanału edukacyjnego, nie reklamy marki premium.
